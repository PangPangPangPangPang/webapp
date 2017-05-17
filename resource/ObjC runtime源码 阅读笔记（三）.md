# ObjC runtime源码 阅读笔记（三）
[date] 2016-11-1 19:20:11
[tag] Objective-C runtime

## objc-references.h
这篇文章主要分析如下两个方法的内部实现。

```c
OBJC_EXPORT void objc_setAssociatedObject(id object, const void *key, id value, objc_AssociationPolicy policy)
    OBJC_AVAILABLE(10.6, 3.1, 9.0, 1.0);
OBJC_EXPORT id objc_getAssociatedObject(id object, const void *key)
    OBJC_AVAILABLE(10.6, 3.1, 9.0, 1.0);
```
这两个方法的内部实现就在**objc-references.mm**中，分别对应如下：

```c
extern void _object_set_associative_reference(id object, void *key, id value, uintptr_t policy);
extern id _object_get_associative_reference(id object, void *key);
```

先上代码

```c
// class AssociationsManager manages a lock / hash table singleton pair.
// Allocating an instance acquires the lock, and calling its assocations() method
// lazily allocates it.

class AssociationsManager {
    static spinlock_t _lock;
    static AssociationsHashMap *_map;               // associative references:  object pointer -> PtrPtrHashMap.
public:
    AssociationsManager()   { _lock.lock(); }
    ~AssociationsManager()  { _lock.unlock(); }
    
    AssociationsHashMap &associations() {
        if (_map == NULL)
            _map = new AssociationsHashMap();
        return *_map;
    }
};
```
根据注释可以看出**AssociationsManager**管理一个hash表，并且这个表是单例，最后强调了下这个hash表的初始化是一个懒加载的过程。

> 其实说到底，所有对象的关联属性都是靠这个**AssociationsHashMap**管理的。
贴上代码分析一下：

```c
void _object_set_associative_reference(id object, void *key, id value, uintptr_t policy) {
    // retain the new value (if any) outside the lock.
    ObjcAssociation old_association(0, nil);
    id new_value = value ? acquireValue(value, policy) : nil;
    {
        AssociationsManager manager;
        //associations 即为管理关联对象的Hash表
        AssociationsHashMap &associations(manager.associations());
        disguised_ptr_t disguised_object = DISGUISE(object);
        //正常流程
        if (new_value) {
            // break any existing association.
            AssociationsHashMap::iterator i = associations.find(disguised_object);
            //判断associatins中是否已经有object对应的ObjectAssociationMap
            if (i != associations.end()) {
                // 已经存在的case
                // secondary table exists
                ObjectAssociationMap *refs = i->second;
                ObjectAssociationMap::iterator j = refs->find(key);
                //判断ObjectAssociationMap中是否已经关联key
                if (j != refs->end()) {
                    //已经存在的case，直接替换成new_value
                    old_association = j->second;
                    j->second = ObjcAssociation(policy, new_value);
                } else {
                    //不存在的case，赋予新的key-value pair
                    (*refs)[key] = ObjcAssociation(policy, new_value);
                }
            } else {
                // 不存在的case
                // 生成新的ObjectAssociationMap并赋予新的key-value pair
                // create the new association (first time).
                ObjectAssociationMap *refs = new ObjectAssociationMap;
                associations[disguised_object] = refs;
                (*refs)[key] = ObjcAssociation(policy, new_value);
                object->setHasAssociatedObjects();
            }
        } else {
            // setting the association to nil breaks the association.
            AssociationsHashMap::iterator i = associations.find(disguised_object);
            if (i !=  associations.end()) {
                ObjectAssociationMap *refs = i->second;
                ObjectAssociationMap::iterator j = refs->find(key);
                if (j != refs->end()) {
                    old_association = j->second;
                    refs->erase(j);
                }
            }
        }
    }
    // release the old value (outside of the lock).
    if (old_association.hasValue()) ReleaseValue()(old_association);
}

```

get和set的处理大同小异，有兴趣的同学可以看一下源码。


