# iOS二维码扫描识别
## 2015-12-23 12:35:36

### 前言
二维码功能在app中很常用，在iOS7之前iOS的二维码功能通常用**ZXing**等框架完成。iOS7之后**AVFoundation**已经支持了原生的二维码扫描功能。这篇文章帮助大家在app中实现此功能，并且会详细的解释一下其中的过程。在开始编码之前，先介绍一下相关的概念。
### 概念相关
#### AVCaptureSession
熟悉**AVFoundation**的同学都会知道**AVCaptureSession**是其中的核心类。**AVCaptureSession**协调了一个物理设备的输入（input）和输出（output）。
#### AVCaptureInput
顾名思义，就是上文中**AVCaptureSession**协调的输入。不过**AVCaptureInput**是一个虚类不能直接实例化，可以使用其子类。**AVCaptureInput**有多个接口可以同时承载一种或多种媒体数据，比如可以同时承载音频数据流和视频数据流。本文章使用的输入是**AVCaptureInput**的子类**AVCaptureDeviceInput**。**AVCaptureDeviceInput**提供了利用**AVCaptureDevice**捕捉流媒体的功能，顾名思义，就是利用这个输入就可以捕捉到二维码并且识别。
#### AVCaptureDevice
物理设备的一个抽象，具体到设备上比如摄像头，麦克风。
#### AVCaptureOutput
跟**AVCaptureInput**相同也是抽象基类，比如说我们看到的视频，听到的音频都是通过它处理输出。**AVCaptureInput**可以持有一个或多个**AVCaptureConnection**实例。本文章使用的是其子类**AVCaptureMetadataOutput**，该类可以捕获从输出中获取的元数据（metadata）。
#### AVCaptureConnection
本文中没有使用到，但是还是简单介绍一下概念。**AVCaptureConnection**可以将**AVCaptureInputPort**和**AVCaptureOutput**或者**AVCaptureVideoPreviewLayer**关联起来。本文不需要手动调用这些关联，当利用**AVCaptureSession**关联输入和输出的时候，这些关联就已经生成。

### 开始
首先看一下接口文件

```objectivec
@protocol  QRCodeParserDelegate<NSObject>

@required

- (void)QRCodeParser:(AVMetadataMachineReadableCodeObject *)object;

@end

typedef NS_ENUM(NSInteger, QRCodeParserStatus) {
    QRCodeParserStatusPrepare  = 1,
    QRCodeParserStatusScanning = 2,
    QRCodeParserStatusStop     = 3
};

@interface QRCodeParser : NSObject

@property (nonatomic, assign)QRCodeParserStatus status;

- (instancetype)initWithFrame:(CGRect)rect
                  andDelegate:(UIViewController<QRCodeParserDelegate>*)delegate;
- (void)stopReading;
- (void)startReading;
- (BOOL)initQRScanner;

@end
```

* **QRCodeParserDelegate**作为识别出二维码的回调。
* **QRCodeParserStatus**parser的状态机，本文没有使用到。
* **initWithFrame:andDelegate:**为parser的初始化方法。
* **startReading**开始扫描。
* **stopReading**停止扫描。
* **initQRScanner**初始化二维码扫描器

以下是核心部分代码：

```objectivec
- (BOOL)initQRScanner{
    NSError *error = nil;
    
    //1
    AVCaptureDevice *captureDevice = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
    //2
    AVCaptureDeviceInput *input = [AVCaptureDeviceInput deviceInputWithDevice:captureDevice
                                                                        error:&error];
    if (!input || error) {
        NSLog(@"%@", [error localizedDescription]);
        return NO;
    }
    //3
    _captureSession = [AVCaptureSession new];
    [_captureSession addInput:input];
    SafeRelease(input);
    
    //4
    _captureMetadataOutput = [AVCaptureMetadataOutput new];
    [_captureMetadataOutput setRectOfInterest:CGRectMake(0.25, 0.25, 0.5, 0.5)];
    [_captureSession addOutput:_captureMetadataOutput];
    
    //5
    dispatchQueue = dispatch_queue_create("QRQueue", NULL);
    [_captureMetadataOutput setMetadataObjectsDelegate:self queue:dispatchQueue];
    [_captureMetadataOutput setMetadataObjectTypes:[NSArray arrayWithObject:AVMetadataObjectTypeQRCode]];
    
    //6
    _videoPreviewLayer = [[AVCaptureVideoPreviewLayer alloc] initWithSession:_captureSession];
    [_videoPreviewLayer setVideoGravity:AVLayerVideoGravityResizeAspectFill];
    [_videoPreviewLayer setFrame:_rect];
    [_ownerVC.view.layer addSublayer:_videoPreviewLayer];
    
    //7
    [_captureSession startRunning];
    
    return YES;
    
}
```

接下来一步步解释上述代码：

1. 初始化捕捉设备，并且该设备类型为视频设备**AVMediaTypeVideo**
2. 利用**captureDevice**生成输入源**AVCaptureDeviceInput**，从而此输入源交给**AVCaptureSession**来协调处理。
3. 初始化**_captureSession**协调输入输出，并将输入源**input**赋值。
4. 生成输出源**_captureMetadataOutput**，并将它付给**AVCaptureSession**，**rectOfInterest**表示将输出源可识别的范围控制在一个方形中。
5. 注册一个线程，并在该线程中设置**_captureMetadataOutput**代理为**self**。
6. 初始化**_videoPreviewLayer**来承载**input**提供的画面，并将其加在目标视图上。

接下来实现其**startReading**，**stopReading**方法：

```Objective-c
- (void)startReading{
    [_captureSession startRunning];
}

-(void)stopReading{
    [_captureSession stopRunning];
}
```

扫描二维码之后的回调：

```objectivec
- (void)captureOutput:(AVCaptureOutput *)captureOutput didOutputMetadataObjects:(NSArray *)metadataObjects fromConnection:(AVCaptureConnection *)connection{
    for (AVMetadataObject *object in metadataObjects) {
        if ([[object type] isEqualToString:AVMetadataObjectTypeQRCode]
            && [object isKindOfClass:[AVMetadataMachineReadableCodeObject class]]) {
            [self stopReading];
            if ([_ownerVC respondsToSelector:@selector(QRCodeParser:)]) {
                [_ownerVC performSelector:@selector(QRCodeParser:)
                                 onThread:[NSThread mainThread]
                               withObject:object
                            waitUntilDone:YES];
            }
        }
    }
}
```
需要注意的是该回调触发在后台线程，如果有处理UI相关的操作请在主线程。
接下来是有关根据二维码图片读取内容和根据内容生成二维码的代码截取：

```objectivec
@implementation UIImage (QRCodeGenerator)

- (NSString *)QRCodeParserToContent{
    CIContext *context = [CIContext contextWithOptions:nil];
    CIDetector *detector = [CIDetector detectorOfType:CIDetectorTypeQRCode
                                              context:context
                                              options:@{CIDetectorAccuracy:CIDetectorAccuracyHigh}];
    NSMutableString *result = [NSMutableString new];
    CIImage *ciImage = [CIImage imageWithCGImage:self.CGImage];
    NSArray *features = [detector featuresInImage:ciImage];
    if ([features count] > 0) {
        for (CIQRCodeFeature *feature in features) {
            [result appendString:feature.messageString];
        }
    }else{
        result = nil;
    }
    return result;
}

+ (UIImage *)createQRForString:(NSString *)qrString
                     imageSize:(CGSize)imageSize {
    NSData *stringData = [qrString dataUsingEncoding:NSUTF8StringEncoding];
    CIFilter *qrFilter = [CIFilter filterWithName:@"CIQRCodeGenerator"];
    [qrFilter setDefaults];
    [qrFilter setValue:stringData forKey:@"inputMessage"];
    [qrFilter setValue:@"M" forKey:@"inputCorrectionLevel"];
    
    CIImage *outPutCIImage = qrFilter.outputImage;

    CGImageRef imageRef = [[CIContext contextWithOptions:nil] createCGImage:outPutCIImage
                                                                   fromRect:outPutCIImage.extent];
    CGSize size = CGSizeMake(outPutCIImage.extent.size.width,
                             outPutCIImage.extent.size.height);
    
    UIGraphicsBeginImageContextWithOptions(CGSizeMake(size.width * 10.0,
                                                      size.height * 10.0),
                                           NO,
                                           1.0);
    CGContextRef context = UIGraphicsGetCurrentContext();
    CGContextSetInterpolationQuality(context, kCGInterpolationNone);
    CGContextSetAllowsAntialiasing(context, YES);
    CGAffineTransform trans = CGAffineTransformMakeTranslation(0.0, size.height * 10.0);
    trans = CGAffineTransformScale(trans, 10.0, -10.0);
    CGContextConcatCTM(context, trans);
    CGContextDrawImage(context, CGRectMake(0, 0, size.width, size.height), imageRef);
    
    UIImage *result = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    
    return result;
}
@end
```
接下来解释一下上面的代码：
**QRCodeParserToContent**方法中，首先创建一个用来渲染**CIImage**的上下文**context**，值得注意的是**CIContext**线程安全，**CIFilter**非安全。然后创建一个**detector**用来探测image中得元素，用来获取一个图片中的**CIFeature**数组，这里**CIDetectorTypeQRCode**表示**detector**需要探测的元素为二维码。接下来的代码简洁明了，获取图片中的**CIFeature**，并将其中的**messageString**拼接返回。
**这个方法最低支持到iOS8.0**

**createQRForString:imageSize:**方法中，利用的核心类是**CIFilter**，这个**CIFilter**可以看做是一个滤镜，核心的思路是交给**filter**一个输入，也就是原图片，然后配置**filter**的属性，最后获取的**outputImage**就是加完滤镜的图片。方法中的**imageRef**就是结果图片。最后利用**CoreGraphics**中的绘制图片的函数绘制出**UIImage**。


