# ReactNative源码解析（一）：RCTUIManager
[date] 2017-3-20 17:52:11
[tag] ReactNative
## 主要流程梳理
### 初始化
bridge会持有一个uiManager，这个uiManager负责rootView的布局和渲染逻辑。

```objc
@implementation RCTBridge (RCTUIManager)
- (RCTUIManager *)uiManager
{
  return [self moduleForClass:[RCTUIManager class]];
}
@end
```
rootContentView是rootView的子视图，真正负责承载视图的功能。
rootContentView在bundle加载结束后初始化，初始化过程中uiManager将rootContentView注册成基本视图。

```objc
- (void)bundleFinishedLoading:(RCTBridge *)bridge
{
// logic code
  _contentView = 
  [[RCTRootContentView alloc] initWithFrame:self.bounds 
  bridge:bridge 
  reactTag:self.reactTag 
  sizeFlexiblity:_sizeFlexibility];
// logic code
}
```
```objc
[_bridge.uiManager registerRootView:self
 withSizeFlexibility:sizeFlexibility];
```
在注册rootView之后在uiManager会维护一套shadowViewTree用来跟真正的viewTree做映射，这些shadowView负责用来布局的计算。其实更深层的是内部维护了一套CSSNodeTree来根shadowViewTree做一一对应。接下来会更详细的介绍。
>从以上的过程，串联了一条如下的关系：

![image](http://mmmmmax.cn/uimanager.png)

到这里，初始化中有关uiManager基本结束。接下来是渲染的重头戏。
### 渲染
#### 渲染源头
>要触发uiManager的渲染有两个主要的方法，一个是通过js端，一个是通过native端。

```objc
//js端触发渲染
- (void)batchDidComplete
- //native端触发渲染
- (void)setNeedsLayout
```
这两个均是uiManager的方法。其中**- (void)setNeedsLayout**由native主动发起渲染。**- (void)batchDidComplete**是由bridge中的**- (void)handleBuffer:(id)buffer batchEnded:(BOOL)batchEnded**调用，而这个方法真是js回调native的统一路口。
#### 渲染过程
那么接下来就要开始梳理**RCTUIManager**这个类了。
首先梳理native暴露给js的方法：

```objc
//移除rootShadowView以及其subViews
//在uiBlock移除rootView以及其subViews
RCT_EXPORT_METHOD(removeRootView:(nonnull NSNumber *)rootReactTag);
//顾名思义，替换rootView
RCT_EXPORT_METHOD(replaceExistingNonRootView:(nonnull NSNumber *)reactTag
                  withView:(nonnull NSNumber *)newReactTag);
//管理节点位置                  
RCT_EXPORT_METHOD(manageChildren:(nonnull NSNumber *)containerTag
                  moveFromIndices:(NSArray<NSNumber *> *)moveFromIndices
                  moveToIndices:(NSArray<NSNumber *> *)moveToIndices
                  addChildReactTags:(NSArray<NSNumber *> *)addChildReactTags
                  addAtIndices:(NSArray<NSNumber *> *)addAtIndices
                  removeAtIndices:(NSArray<NSNumber *> *)removeAtIndices)
//添加子视图，注意这个方法只是像shadowViewTree和viewTree中加节点，并没有真正的触发渲染。并且两个tree增加节点的时机也不同。
RCT_EXPORT_METHOD(setChildren:(nonnull NSNumber *)containerTag
                  reactTags:(NSArray<NSNumber *> *)reactTags);
//根据viewName构建shadowView和view并放入各自的tree中。
RCT_EXPORT_METHOD(createView:(nonnull NSNumber *)reactTag
                  viewName:(NSString *)viewName
                  rootTag:(__unused NSNumber *)rootTag
                  props:(NSDictionary *)props);
//更新视图props。
RCT_EXPORT_METHOD(updateView:(nonnull NSNumber *)reactTag
                  viewName:(NSString *)viewName // not always reliable, use shadowView.viewName if available
                  props:(NSDictionary *)props)；
//将对应视图设置成firstResponder。
RCT_EXPORT_METHOD(focus:(nonnull NSNumber *)reactTag);
//取消对应视图firstResponder。
RCT_EXPORT_METHOD(blur:(nonnull NSNumber *)reactTag);
//获取对应视图点击的坐标系。
RCT_EXPORT_METHOD(findSubviewIn:(nonnull NSNumber *)reactTag atPoint:(CGPoint)point callback:(RCTResponseSenderBlock)callback);
//向所给视图分发command事件。
RCT_EXPORT_METHOD(dispatchViewManagerCommand:(nonnull NSNumber *)reactTag
                  commandID:(NSInteger)commandID
                  commandArgs:(NSArray<id> *)commandArgs);
//获取对应视图坐标。                  
RCT_EXPORT_METHOD(measure:(nonnull NSNumber *)reactTag
                  callback:(RCTResponseSenderBlock)callback);
//获取对应视图相对window坐标。
RCT_EXPORT_METHOD(measureInWindow:(nonnull NSNumber *)reactTag
                  callback:(RCTResponseSenderBlock)callback);
//判断是否为后代视图。
RCT_EXPORT_METHOD(viewIsDescendantOf:(nonnull NSNumber *)reactTag
                  ancestor:(nonnull NSNumber *)ancestorReactTag
                  callback:(RCTResponseSenderBlock)callback);
//计算视图的相对于某个给定视图的布局
RCT_EXPORT_METHOD(measureLayout:(nonnull NSNumber *)reactTag
                  relativeTo:(nonnull NSNumber *)ancestorReactTag
                  errorCallback:(__unused RCTResponseSenderBlock)errorCallback
                  callback:(RCTResponseSenderBlock)callback);
//计算视图相对于父视图的布局。
RCT_EXPORT_METHOD(measureLayoutRelativeToParent:(nonnull NSNumber *)reactTag
                  errorCallback:(__unused RCTResponseSenderBlock)errorCallback
                  callback:(RCTResponseSenderBlock)callback);
//计算给定rect内某个视图的子视图的布局队列。
RCT_EXPORT_METHOD(measureViewsInRect:(CGRect)rect
                  parentView:(nonnull NSNumber *)reactTag
                  errorCallback:(__unused RCTResponseSenderBlock)errorCallback
                  callback:(RCTResponseSenderBlock)callback);  
//截图。
RCT_EXPORT_METHOD(takeSnapshot:(id /* NSString or NSNumber */)target
                  withOptions:(NSDictionary *)options
                  resolve:(RCTPromiseResolveBlock)resolve
                  reject:(RCTPromiseRejectBlock)reject)；    
//设置responder，提供给scrollView使用。
RCT_EXPORT_METHOD(setJSResponder:(nonnull NSNumber *)reactTag
                  blockNativeResponder:(__unused BOOL)blockNativeResponder)   
//清理responder。
RCT_EXPORT_METHOD(clearJSResponder);   
//配置下一步动画。
RCT_EXPORT_METHOD(configureNextLayoutAnimation:(NSDictionary *)config
                  withCallback:(RCTResponseSenderBlock)callback
                  errorCallback:(__unused RCTResponseSenderBlock)errorCallback)             
```
暴露的方法比较多，我这里只是做一个简单的注释总结，详细请参阅源码。接下来是native端两个最重要的方法。

```objc
typedef void (^RCTViewManagerUIBlock)(RCTUIManager *uiManager, NSDictionary<NSNumber *, UIView *> *viewRegistry);
//将对应视图的block添加到队列中，等待_layoutAndMount触发时执行。
- (void)addUIBlock:(RCTViewManagerUIBlock)block;
- 
- (void)_layoutAndMount
{
  // 在即将渲染前进行最后自定义的uiBlock，即将启用，不深入分析。
  for (RCTComponentData *componentData in _componentDataByName.allValues) {
    RCTViewManagerUIBlock uiBlock = [componentData uiBlockToAmendWithShadowViewRegistry:_shadowViewRegistry];
    [self addUIBlock:uiBlock];
  }

  //perform layout
  for (NSNumber *reactTag in _rootViewTags) {
    RCTRootShadowView *rootView = (RCTRootShadowView *)_shadowViewRegistry[reactTag];
    //递归执行layout
    [self addUIBlock:[self uiBlockWithLayoutUpdateForRootView:rootView]];
    [self _amendPendingUIBlocksWithStylePropagationUpdateForShadowView:rootView];
  }

  [self addUIBlock:^(RCTUIManager *uiManager, __unused NSDictionary<NSNumber *, UIView *> *viewRegistry) {
    /**
     * TODO(tadeu): Remove it once and for all
     */
    for (id<RCTComponent> node in uiManager->_bridgeTransactionListeners) {
      [node reactBridgeDidFinishTransaction];
    }
  }];
  //真正执行UI队列任务。
  [self flushUIBlocks];
}
```
当然**uiBlockWithLayoutUpdateForRootView**和**_amendPendingUIBlocksWithStylePropagationUpdateForShadowView**中也有很多细节要梳理。这些东西就交给大家自己梳理吧～



