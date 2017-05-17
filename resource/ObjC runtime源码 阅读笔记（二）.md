# ObjC runtime源码 阅读笔记（二）
今天开始第二篇的阅读笔记，当然还是继续着上一篇的分析
-------
[date] 2016-10-28 12:35:36
[tag] Objective-C runtime
## 1.objc-private.h
紧接着**objc_object**的就是如下一些很熟悉的结构体，让我们一个一个的分析。

```c
typedef struct method_t *Method;
typedef struct ivar_t *Ivar;
typedef struct category_t *Category;
typedef struct property_t *objc_property_t;
```
如果大家以前接触过**objc/runtime.h**里的api的话一定不会对**Method**感到陌生，实际上这就真正代表了一个Objective-c中的方法。

```c
struct method_t {
    SEL name;
    const char *types;
    IMP imp;

    struct SortBySELAddress :
        public std::binary_function<const method_t&,
                                    const method_t&, bool>
    {
        bool operator() (const method_t& lhs,
                         const method_t& rhs)
        { return lhs.name < rhs.name; }
    };
};
```
* **name：**很遗憾我并没有看到**SEL**内部真正的实现，但是可以简单的把**name**当作一个方法的名字。
* **types：**方法的类型，比如说返回参数类型，入参类型。
* **imp：**可以看成方法的实现。（方法地址？）

紧接着又是一个熟悉的东东**ivar_t**。
```c
struct ivar_t {
    int32_t *offset;
    const char *name;
    const char *type;
    // alignment is sometimes -1; use alignment() instead
    uint32_t alignment_raw;
    uint32_t size;

    uint32_t alignment() const {
        if (alignment_raw == ~(uint32_t)0) return 1U << WORD_SHIFT;
        return 1 << alignment_raw;
    }
};
```
* **offset：**地址偏移量，用来寻找ivar。
* **name：**ivar名称。
* **type：**ivar数据类型。（具体定义可在**runtime.h**中找到）
* **alignment：**内存偏移量，用于内存对齐。
* **size：**ivar的size。

上面的两个结构体会作为item组成相应list。

```c
struct method_list_t : entsize_list_tt<method_t, method_list_t, 0x3> {
    bool isFixedUp() const;
    void setFixedUp();

    uint32_t indexOfMethod(const method_t *meth) const {
        uint32_t i = 
            (uint32_t)(((uintptr_t)meth - (uintptr_t)this) / entsize());
        assert(i < count);
        return i;
    }
};

struct ivar_list_t : entsize_list_tt<ivar_t, ivar_list_t, 0> {
    bool containsIvar(Ivar ivar) const {
        return (ivar >= (Ivar)&*begin()  &&  ivar < (Ivar)&*end());
    }
};
```
其实这一部分的作用和声明都比较简单。大概理解里面的成员就可以了。


