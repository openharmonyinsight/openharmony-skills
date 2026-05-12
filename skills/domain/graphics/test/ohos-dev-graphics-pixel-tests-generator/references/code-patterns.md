# 代码模式

## 最小自动像素测试

```cpp
GRAPHIC_TEST(ExampleTest, CONTENT_DISPLAY_TEST, Example_Property_Test)
{
    auto testNode = RSCanvasNode::Create();
    testNode->SetBounds({ 100, 100, 300, 300 });
    testNode->SetFrame({ 100, 100, 300, 300 });
    testNode->SetBackgroundColor(0xffff0000);
    GetRootNode()->AddChild(testNode);
    RegisterNode(testNode);
}
```

自动测试通常不需要显式 transaction flush，因为 `TearDown()` 会统一 flush 并截图。

## 参数矩阵网格

当用户希望在同一张图片中对比多个参数值时，使用一个测试并把多个节点放到网格中：

```cpp
int columnCount = 3;
int rowCount = 2;
auto sizeX = screenWidth / columnCount;
auto sizeY = screenHeight / rowCount;
std::vector<float> values = { -1.0f, 0.0f, 0.5f, 1.0f, 2.0f };

for (int i = 0; i < static_cast<int>(values.size()); i++) {
    int x = (i % columnCount) * sizeX;
    int y = (i / columnCount) * sizeY;
    auto node = RSCanvasNode::Create();
    node->SetBounds({ x, y, sizeX - 10, sizeY - 10 });
    node->SetFrame({ x, y, sizeX - 10, sizeY - 10 });
    node->SetBackgroundColor(0xff00ff00);
    node->SetAlpha(values[i]);
    GetRootNode()->AddChild(node);
    RegisterNode(node);
}
```

## 背景图片节点

```cpp
auto node = SetUpNodeBgImage("/data/local/tmp/Images/backGroundImage.jpg", { x, y, width, height });
node->SetBorderWidth(5);
node->SetBorderColor(Vector4<Color>(RgbPalette::Red()));
node->SetBackgroundBlurRadius(radius);
GetRootNode()->AddChild(node);
RegisterNode(node);
```

除非用户提供新资源路径，否则复用同目录已有资源路径。

## 使用 Brush 或 Pen 的 Drawing::Canvas

本地很多 Drawing 示例会把 brush/pen attach 到 canvas，而不是给每个绘制调用传 paint 对象：

```cpp
auto recordingCanvas = testNode->BeginRecording(width, height);
Drawing::Brush brush;
brush.SetColor(Drawing::Color::COLOR_CYAN);
recordingCanvas->AttachBrush(brush);
recordingCanvas->DrawRect(Drawing::Rect(0, 0, width, height));
recordingCanvas->DetachBrush();
testNode->FinishRecording();
```

绘制描边时：

```cpp
Drawing::Pen pen;
pen.SetColor(Drawing::Color::COLOR_RED);
pen.SetWidth(4);
recordingCanvas->AttachPen(pen);
recordingCanvas->DrawRect(Drawing::Rect(50, 50, 250, 250));
recordingCanvas->DetachPen();
```

不要使用 `paintSetColor` 这类占位 helper；先确认相邻文件里的真实 Drawing API 风格。

## 自定义 Modifier

当被测行为是 modifier 绘制或动画时，使用 `ModifierNG::RSContentStyleModifier`：

```cpp
class TestContentStyleModifier : public ModifierNG::RSContentStyleModifier {
public:
    void Draw(ModifierNG::RSDrawingContext& context) const override
    {
        auto canvas = context.canvas;
        if (canvas == nullptr) {
            return;
        }
        Drawing::Brush brush;
        brush.SetColor(Drawing::Color::COLOR_CYAN);
        canvas->AttachBrush(brush);
        canvas->DrawRect(Drawing::Rect(0, 0, 500, 500));
        canvas->DetachBrush();
    }
};
```

添加到节点：

```cpp
auto node = RSCanvasNode::Create(true);
auto modifier = std::make_shared<TestContentStyleModifier>();
node->AddModifier(modifier);
GetRootNode()->AddChild(node);
RegisterNode(node);
```

## 动画

动画测试通常先创建可见节点，添加 modifier 或属性，然后执行动画。现有动画测试经常使用 `RSUIContext`。

```cpp
RSAnimationTimingProtocol protocol;
protocol.SetDuration(300);
auto curve = RSAnimationTimingCurve::LINEAR;
RSNode::Animate(GetRSUIContext(), protocol, curve, [&]() {
    modifier->SetPosition(500);
}, []() {
    std::cout << "animation finish callback" << std::endl;
});
```

除非相邻文件已有不同等待设计，否则动画时长尽量控制在几百毫秒级。

## 手动截图

当测试需要控制截图时机时，使用 `GRAPHIC_N_TEST`：

```cpp
RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
usleep(SLEEP_TIME_FOR_PROXY);
TestCaseCapture();
```

手动截图 helper 常用：

```cpp
auto pixelMap = DisplayManager::GetInstance().GetScreenshot(
    DisplayManager::GetInstance().GetDefaultDisplayId());
```

随后按需要 crop 或通过 `WriteToPngWithPixelMap` 写图。如果文件中已有 `// NOT MODIFY THE COMMENTS` 这类特殊失败注释，必须保留。

## 子窗口测试

```cpp
SubWindowOptions opts;
opts.bounds = { 100, 100, 500, 500 };
opts.order = SubWindowOrder::ABOVE_MAIN;
auto subId = CreateSubWindow(opts);

auto node = RSCanvasNode::Create();
node->SetBounds({ 0, 0, 300, 300 });
node->SetBackgroundColor(0xffff0000);
GetRootNode()->AddChildToSubWindow(subId, node);
RegisterNode(node);
```

存在子窗口时，框架自动改用 display capture。

## PixelMap 和 Surface 查询

提交节点后立即查询 surface 或 PixelMap 的测试，通常需要 flush 并等待：

```cpp
GetRootNode()->SetTestSurface(surfaceNode);
RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
usleep(SLEEP_TIME_FOR_PROXY);

SurfaceId surfaceId = surfaceNode->GetSurface()->GetUniqueId();
auto pixelMap = RSInterfaces::GetInstance().CreatePixelMapFromSurfaceId(surfaceId, rect, true);
```

需要存活到查询完成的 surface 或 node 也要注册。
