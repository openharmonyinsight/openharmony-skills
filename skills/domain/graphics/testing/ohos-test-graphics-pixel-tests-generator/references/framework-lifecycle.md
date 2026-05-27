# 框架生命周期

## 优先查看的核心文件

- `graphic_test/graphic_test_framework/include/rs_graphic_test.h`
- `graphic_test/graphic_test_framework/include/rs_graphic_test_ext.h`
- `graphic_test/graphic_test_framework/src/rs_graphic_test.cpp`
- `graphic_test/graphic_test_framework/include/rs_graphic_test_img.h`
- `graphic_test/graphic_test_framework/include/rs_graphic_rootnode.h`

## 测试生命周期

`RSGraphicTest::SetUp()`：

1. 检查 `TestDefManager` 注册信息和命令行过滤条件。
2. 创建名为 `TestSurface<N>` 的测试 `RSSurfaceNode`。
3. 将默认 bounds/frame 设置为当前屏幕尺寸，并设置白色背景。
4. 调用用户重写的 `BeforeEach()`。
5. 普通测试会把 screen-surface bounds 设置为 fixture 的屏幕尺寸。
6. `GRAPHIC_TESTS` 会根据同一 fixture 下的测试数量，把每个 test surface 放到网格中的对应位置。

`RSGraphicTest::TearDown()`：

1. 如果测试被过滤或设置了 `skipCapture_`，跳过截图。
2. 对 `GRAPHIC_TESTS`，会等到同一 fixture 的最后一个测试结束后再截图。
3. 启动 UI 动画。
4. 调用 `FlushMessageAndWait(testCaseWaitTime)`，再等待 `normalWaitTime`。
5. 手动测试只等待 `manualTestWaitTime`；自动和动态测试调用 `TestCaseCapture`。
6. 调用用户重写的 `AfterEach()`，重置 surface/sub-window，清空注册节点，发送 `rssubtree_clear`，并再次 flush。

## 宏行为

`rs_graphic_test_ext.h` 定义：

```cpp
GRAPHIC_TEST(TestClass, Type, Name)
GRAPHIC_TEST(Type, Name)
GRAPHIC_TESTS(TestClass, Type, Name)
GRAPHIC_TESTS(Type, Name)
GRAPHIC_N_TEST(TestClass, Type, Name)
GRAPHIC_N_TEST(Type, Name)
GRAPHIC_D_TEST(TestClass, Type, Name)
GRAPHIC_D_TEST(Type, Name)
```

所有宏都会先注册 `(testCaseName, testName, testType, testMode, filePath, isMultiple)`，再展开为 `TEST_F`。

模式说明：

- `GRAPHIC_TEST`：在 `TearDown` 中自动截图。
- `GRAPHIC_TESTS`：自动截图，但同一 fixture 中多个测试函数会合成一张网格图片。
- `GRAPHIC_N_TEST`：手动模式；框架不会调用 `TestCaseCapture`，测试需要自己处理截图。
- `GRAPHIC_D_TEST`：动态回放模式；只在明确需要录制/回放时使用。

## 截图输出规则

自动截图写入：

```text
/data/local/graphic_test/<从源文件路径提取的路径>/<TestClass>_<TestName>.png
```

对于 `GRAPHIC_TESTS`，文件名不包含单个测试名：

```text
/data/local/graphic_test/<path>/<TestClass>.png
```

`TestCaseCapture` 默认使用主 surface 截图；当测试请求 screenshot 模式、设置 `CaptureScope::FULL_DISPLAY` 或使用子窗口时，框架会使用 display capture。

## 节点生命周期

`RegisterNode(node)` 会把 `shared_ptr` 保存到测试和 root node 中。所有在局部变量离开作用域后仍需要渲染的节点都要注册。

典型顺序：

```cpp
auto node = RSCanvasNode::Create();
node->SetBounds({ x, y, w, h });
node->SetFrame({ x, y, w, h });
node->SetBackgroundColor(0xffff0000);
GetRootNode()->AddChild(node);
RegisterNode(node);
```

`SetUpNodeBgImage(path, bounds)` 已经设置 bounds、frame、背景图片尺寸和背景图片，但仍然需要加入场景并注册。

## 常用框架 API

`RSGraphicTest`：

- `GetRootNode()`
- `GetScreenSize()`
- `SetScreenSize(width, height)`
- `SetSurfaceBounds(bounds)`
- `SetScreenSurfaceBounds(bounds)`
- `SetSurfaceColor(color)`
- `RegisterNode(node)`
- `StartUIAnimation()`
- `CreateSubWindow(options)`
- `AddChildToSubWindow(id, child, index)`
- `SetCaptureScope(CaptureScope::FULL_DISPLAY)`
- `AddFileRenderNodeTreeToNode(node, filePath)`
- `PlaybackRecover(filePath, pauseTimeStamp)`

图片辅助：

- `DecodePixelMap(path, allocatorType, dstFormat)`
- `SetUpNodeBgImage(path, bounds)`
- `SetUpNodeBgImage(data, size, bounds)`
- `ImageCustomModifier`：通过 content-style modifier 绘制图片内容。

## 事务提交建议

框架会在 `TearDown` 中 flush 并等待，所以很多自动测试不需要显式 transaction flush。

以下情况需要添加 `RSTransactionProxy::GetInstance()->FlushImplicitTransaction()`：

- 测试函数内部手动截图。
- 提交节点后立即调用查询渲染输出或 surface 的 API。
- 测试需要 sleep 到特定渲染状态。
- 同一功能区域的相邻测试已经采用显式提交模式。

使用 `RSTransactionProxy` 时 include `transaction/rs_interfaces.h`。
