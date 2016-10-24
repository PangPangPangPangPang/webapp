# ObjC runtime源码 阅读笔记（一）
今天开始记录一系列的阅读笔记，顺便督促一下自己阅读runtime的源码，本文的源码来自于[apple opensource](http://opensource.apple.com/source/objc4/)。
-------
## 1.objc-private.h
打开头文件就看到了两个熟悉的结构体指针

```c
typedef struct objc_class *Class;
typedef struct objc_object *id;
```
我们会经常用到**id**这个指针，比较老的**Foundation**框架中，一般的初始化方法都会返回一个**id**对象，并且一些有iOS编程经验的老鸟也会说**ObjC**中的所有对象都可以强转成**id**类型。那么现在就来分析一下**id**究竟是个什么东东。

从源码来看真的是好长的一坨结构体,首先看到的是一个**isa_t**的**union**：

```c
private:
    isa_t isa;
```
这个**isa_t**用一句话概括就是：

> 对64位的设备对象进行类对象指针的优化，利用合理的bit（arm64设备为32位）存储类对象的地址，其他位用来进行内存管理。这种优化模式被称为**tagged pointer**。用在**isa_t**的实现中称作**IndexedIsa**。

下面是**isa_t**在**arm64**架构下的结构：

```c
union isa_t 
{
    uintptr_t bits;
    
#   define ISA_MASK        0x00007ffffffffff8ULL
#   define ISA_MAGIC_MASK  0x001f800000000001ULL
#   define ISA_MAGIC_VALUE 0x001d800000000001ULL
    struct {
        uintptr_t indexed           : 1;
        uintptr_t has_assoc         : 1;
        uintptr_t has_cxx_dtor      : 1;
        uintptr_t shiftcls          : 33; // MACH_VM_MAX_ADDRESS 0x1000000000
        uintptr_t magic             : 6;
        uintptr_t weakly_referenced : 1;
        uintptr_t deallocating      : 1;
        uintptr_t has_sidetable_rc  : 1;
        uintptr_t extra_rc          : 19;
#       define RC_ONE   (1ULL<<45)
#       define RC_HALF  (1ULL<<18)
    };
};
```
* indexed：标记是否启动指针优化
* has_assoc：是否有关联对象
* has_cxx_dtor：是否有析构器
* shiftcls：类对象指针
* magic：标记初始化完成
* weakly_refrenced：是否弱引用
* deallocating：是否正在释放
* extra_rc：引用计数-1

至此，优化情况下的isa_t包含的内容大体总结完毕。
回过头来继续分析**objc_object**内的函数。

```c
Class ISA() //不支持tagged pointer时候获取Class的函数
Class getIsa() //支持tagged pointer时候获取Class的函数
```
下面是一系列isa初始化的函数：

```c
void initIsa(Class cls /*indexed=false*/);
void initClassIsa(Class cls /*indexed=maybe*/);
void initProtocolIsa(Class cls /*indexed=maybe*/);
void initInstanceIsa(Class cls, bool hasCxxDtor);
```
值得注意的是这几个函数最后调用的都是

```c
inline bool objc_object::initIsa(Class cls, bool indexed, bool hasCxxDtor) 
```
下面的函数是用来改变一个对象的Class：

```c
Class changeIsa(Class newCls);
```
印象中KVO的实现中，会改变一个对象的Class，以后会带来验证。
接下来的一些列函数顾名思义，我也不做解释，内部的实现基本也都是依赖于**isa**来进行的。

```c
    // changeIsa() should be used to change the isa of existing objects.
    // If this is a new object, use initIsa() for performance.
    Class changeIsa(Class newCls);

    bool hasIndexedIsa();
    bool isTaggedPointer();
    bool isClass();

    // object may have associated objects?
    bool hasAssociatedObjects();
    void setHasAssociatedObjects();

    // object may be weakly referenced?
    bool isWeaklyReferenced();
    void setWeaklyReferenced_nolock();
    
    // object may have -.cxx_destruct implementation?
    bool hasCxxDtor();
```
这里我解释一下下面这两个方法的区别。

```c
bool hasIndexedIsa();
bool isTaggedPointer();
```
本质上这两个函数都是来判断某个指针是否启用了tagged pointer。不同的是
**bool hasIndexedIsa();**是用来判断当前对象的**isa**是否启用**tagged pointer**，而**bool isTaggedPointer();**函数用来判断当前的对象指针是否启用了**tagged pointer**。根据我的调研，比如**NSNumber**、**NSDate**等值占用内存比较少的对象启用了**tagged pointer**。

接下来是一系列管理引用计数以及生命周期的函数：

```c
// Optimized calls to retain/release methods
    id retain();
    void release();
    id autorelease();
    // Implementations of retain/release methods
    id rootRetain();
    bool rootRelease();
    id rootAutorelease();
    bool rootTryRetain();
    bool rootReleaseShouldDealloc();
    uintptr_t rootRetainCount();

    // Implementation of dealloc methods
    bool rootIsDeallocating();
    void clearDeallocating();
    void rootDealloc();
```
是不是很熟悉呢？先看一下**id retain()**的内部实现：

```c
inline id 
objc_object::retain()
{
    // UseGC is allowed here, but requires hasCustomRR.
    assert(!UseGC  ||  ISA()->hasCustomRR());
    assert(!isTaggedPointer());

    if (! ISA()->hasCustomRR()) {
        return rootRetain();
    }

    return ((id(*)(objc_object *, SEL))objc_msgSend)(this, SEL_retain);
}
```
翻译一下，如果使用GC但是并没有custom的retain/release方法则会直接断言掉，如果支持tagged pointer这回直接断言掉。接下来的流程就是如果没有custom的retain/release方法就会调用rootRetain()。兜兜转转最后会调用如下方法：

```c

ALWAYS_INLINE id 
objc_object::rootRetain(bool tryRetain, bool handleOverflow)
{
    assert(!UseGC);
    if (isTaggedPointer()) return (id)this;

    bool sideTableLocked = false;
    bool transcribeToSideTable = false;

    isa_t oldisa;
    isa_t newisa;

    do {
        transcribeToSideTable = false;
        oldisa = LoadExclusive(&isa.bits);
        newisa = oldisa;
        if (!newisa.indexed) goto unindexed;
        // don't check newisa.fast_rr; we already called any RR overrides
        if (tryRetain && newisa.deallocating) goto tryfail;
        uintptr_t carry;
        newisa.bits = addc(newisa.bits, RC_ONE, 0, &carry);  // extra_rc++

        if (carry) {
            // newisa.extra_rc++ overflowed
            if (!handleOverflow) return rootRetain_overflow(tryRetain);
            // Leave half of the retain counts inline and 
            // prepare to copy the other half to the side table.
            if (!tryRetain && !sideTableLocked) sidetable_lock();
            sideTableLocked = true;
            transcribeToSideTable = true;
            newisa.extra_rc = RC_HALF;
            newisa.has_sidetable_rc = true;
        }
    } while (!StoreExclusive(&isa.bits, oldisa.bits, newisa.bits));

    if (transcribeToSideTable) {
        // Copy the other half of the retain counts to the side table.
        sidetable_addExtraRC_nolock(RC_HALF);
    }

    if (!tryRetain && sideTableLocked) sidetable_unlock();
    return (id)this;

 tryfail:
    if (!tryRetain && sideTableLocked) sidetable_unlock();
    return nil;

 unindexed:
    if (!tryRetain && sideTableLocked) sidetable_unlock();
    if (tryRetain) return sidetable_tryRetain() ? (id)this : nil;
    else return sidetable_retain();
}
```
这段代码确实值得仔细研读,转换成伪代码的形式为：

```c
ALWAYS_INLINE id 
objc_object::rootRetain(bool tryRetain, bool handleOverflow)
{
   if (not support tagged pointer) return this;
   do {
       if (isa not support indexed) 
           sidetable_tryRetain(); //利用sidetable进行管理对象的引用计数。 
       if (isa support indexed)
           newisa.bits = addc(newisa.bits, RC_ONE, 0, &carry);  // extra_rc+
   }
}
```
当然内部还有一些力**retry**已经对于**overflow**的处理，这篇文章就不做过多的分析。但是大体上对于没有进行**isa**的**indexed**优化的对象的引用计数是依赖于**SideTable()**管理，而进行**indexed**优化的对象则直接利用**isa**指针进行管理。

接下来的private函数我就不多做分析了，值得注意的是，里面有很多有关于**sidetable**的函数，但是这些函数是在**NSObject.mm**中实现的。

这样有关于**objc_obejct**这个结构体的分析就到此为止。接下来还有一系列的文章进行分析。加油！

