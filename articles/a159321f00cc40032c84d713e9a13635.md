# ObjC runtime源码 阅读笔记（二）
今天开始第二篇的阅读笔记，当然还是继续着上一篇的分析
-------
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
* **types：**



