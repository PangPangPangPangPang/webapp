# FMDB阅读笔记（二）
[date] 2016-01-26 19:36:11
[tag] 数据库 Objective-C
###FMDatabase
**FMDatabase**作为核心类，封装了sqlite的大部分数据库操作。
初始化方法没什么可说的，从**- (BOOL)openWithFlags:(int)flags vfs:(NSString *)vfsName;
**说起。

```objectivec
- (BOOL)openWithFlags:(int)flags vfs:(NSString *)vfsName;
```
####flags
三个必选项：**SQLITE_OPEN_READONLY**，**SQLITE_OPEN_READWRITE**，**SQLITE_OPEN_CREATE**

[vfs](http://www.sqlite.org/vfs.html)

