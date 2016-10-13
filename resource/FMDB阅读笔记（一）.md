# FMDB阅读笔记（一）
## 2016-01-22 17:30:23
## FMDatabaseQueue
该类提供了多线程操作数据库的功能。尽量不要在多线程操作同一个**FMDatabase**实例。取而代之的是在每一个**FMDatabaseQueue**创建一个**FMDatabase**实例。下面来详细看代码吧。

```objectivec
- (instancetype)initWithPath:(NSString*)aPath flags:(int)openFlags {
    
    self = [super init];
    
    if (self != nil) {
        
        _db = [[[self class] databaseClass] databaseWithPath:aPath];
        FMDBRetain(_db);
        
#if SQLITE_VERSION_NUMBER >= 3005000
        BOOL success = [_db openWithFlags:openFlags];
#else
        BOOL success = [_db open];
#endif
        if (!success) {
            NSLog(@"Could not create database queue for path %@", aPath);
            FMDBRelease(self);
            return 0x00;
        }
        
        _path = FMDBReturnRetained(aPath);
        
        _queue = dispatch_queue_create([[NSString stringWithFormat:@"fmdb.%@", self] UTF8String], NULL);
        dispatch_queue_set_specific(_queue, kDispatchQueueSpecificKey, (__bridge void *)self, NULL);
        _openFlags = openFlags;
    }
    
    return self;
}
```

初始化方法，创建database实例，然后创建了一个串行队列，并用**dispatch_queue_set_specific**方法跟**FMDatabaseQueue**创建关联。**openWithFlags:openFlags**为开启文件的选项。默认**open**方法的选项为**SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE**。

```objectivec
- (void)inDatabase:(void (^)(FMDatabase *db))block {
    /* Get the currently executing queue (which should probably be nil, but in theory could be another DB queue
     * and then check it against self to make sure we're not about to deadlock. */
    FMDatabaseQueue *currentSyncQueue = (__bridge id)dispatch_get_specific(kDispatchQueueSpecificKey);
    assert(currentSyncQueue != self && "inDatabase: was called reentrantly on the same queue, which would lead to a deadlock");
    
    FMDBRetain(self);
    
    dispatch_sync(_queue, ^() {
        
        FMDatabase *db = [self database];
        block(db);
        
        if ([db hasOpenResultSets]) {
            NSLog(@"Warning: there is at least one open result set around after performing [FMDatabaseQueue inDatabase:]");
            
#if defined(DEBUG) && DEBUG
            NSSet *openSetCopy = FMDBReturnAutoreleased([[db valueForKey:@"_openResultSets"] copy]);
            for (NSValue *rsInWrappedInATastyValueMeal in openSetCopy) {
                FMResultSet *rs = (FMResultSet *)[rsInWrappedInATastyValueMeal pointerValue];
                NSLog(@"query: '%@'", [rs query]);
            }
#endif
        }
    });
    
    FMDBRelease(self);
}
```

利用**dispatch_get_specific**获得**FMDatabaseQueue**关联的线程，如果是同一个线程，则直接断言，因为同线程执行**dispatch_sync**会造成死锁。这里的**FMDBRetain(self)**和**FMDBRelease(self)**应该是为了防止block内提前将self释放造成后续访问野指针。接下来在关联线程中获取database并执行block，这里如果在database中存在多个查询结果则防处警告，debug模式下会打印出这些查询结果的query。这里的copy操作不理解。

```objectivec
- (void)inTransaction:(void (^)(FMDatabase *db, BOOL *rollback))block;
- (void)inDeferredTransaction:(void (^)(FMDatabase *db, BOOL *rollback))block;
```

这两个方法的内部逻辑很简单，判断事务开启**defer transaction** 或者**exclusive transaction**，关闭时根据业务逻辑**rollback**或者**commit**。这个类很简单，就分析到这里。

### FMDatabasePool
一开篇就强调不到万不得已不要用这个类，如果你只是用来读数据库，可以用这个类，否则可能造成死锁。

```objectivec
- (void)executeLocked:(void (^)(void))aBlock {
    dispatch_sync(_lockQueue, aBlock);
}
```

该类通过上述方法保证池子操作的线程安全（毕竟已经同步单线程跑了），但是该类并不能保证池内数据库操作安全，该死锁还是会死锁，同时读写会引发很大的问题。这个类没有什么太多值得说的地方，如果有大量并发读操作的需求的话推荐使用这个类，其他都不推荐。

### FMResultSet
query结果的类。通过**FMStatement**访问结果。这个类主要的功能算是提供了一套友好的OC接口来访问结果。


