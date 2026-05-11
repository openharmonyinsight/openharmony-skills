# 模板

这些模板只作为起点。编辑现有文件时，优先匹配现有文件风格。

## 新属性测试文件

```cpp
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "rs_graphic_test.h"

using namespace testing;
using namespace testing::ext;

namespace OHOS::Rosen {
class ExamplePropertyTest : public RSGraphicTest {
public:
    void BeforeEach() override
    {
        SetScreenSize(screenWidth, screenHeight);
    }

private:
    const int screenWidth = 1200;
    const int screenHeight = 2000;
};

/*
 * @tc.name: Example_Property_Test
 * @tc.desc: Test example property rendering.
 * @tc.type: FUNC
 */
GRAPHIC_TEST(ExamplePropertyTest, CONTENT_DISPLAY_TEST, Example_Property_Test)
{
    auto testNode = RSCanvasNode::Create();
    testNode->SetBounds({ 100, 100, 300, 300 });
    testNode->SetFrame({ 100, 100, 300, 300 });
    testNode->SetBackgroundColor(0xffff0000);
    GetRootNode()->AddChild(testNode);
    RegisterNode(testNode);
}
} // namespace OHOS::Rosen
```

## 新 effect feature 测试

```cpp
#include "rs_graphic_test.h"
#include "rs_graphic_test_img.h"

using namespace testing;
using namespace testing::ext;

namespace OHOS::Rosen {
class ExampleEffectTest : public RSGraphicTest {
public:
    void BeforeEach() override
    {
        SetScreenSize(screenWidth, screenHeight);
    }

private:
    const int screenWidth = 1200;
    const int screenHeight = 2000;
};

GRAPHIC_TEST(ExampleEffectTest, EFFECT_TEST, Example_Effect_Test)
{
    auto node = SetUpNodeBgImage("/data/local/tmp/Images/backGroundImage.jpg", { 0, 0, 1190, 990 });
    node->SetBorderWidth(5);
    node->SetBorderColor(Vector4<Color>(RgbPalette::Red()));
    node->SetSystemBarEffect();
    GetRootNode()->AddChild(node);
    RegisterNode(node);
}
} // namespace OHOS::Rosen
```

## 手动截图 fixture 草图

```cpp
#include <filesystem>
#include <unistd.h>

#include "display_manager.h"
#include "rs_graphic_test.h"
#include "rs_graphic_test_utils.h"
#include "transaction/rs_interfaces.h"

using namespace testing;
using namespace testing::ext;

namespace OHOS::Rosen {
namespace {
constexpr uint32_t SLEEP_TIME_FOR_PROXY = 1000000;
}

class ExampleManualCaptureTest : public RSGraphicTest {
public:
    void BeforeEach() override
    {
        auto size = GetScreenSize();
        SetSurfaceBounds({ 0, 0, size.x_, size.y_ });
    }

    void TestCaseCapture()
    {
        auto pixelMap = DisplayManager::GetInstance().GetScreenshot(
            DisplayManager::GetInstance().GetDefaultDisplayId());
        if (pixelMap == nullptr) {
            std::cout << "[   FAILED   ] image is null" << std::endl;
            return;
        }
        const ::testing::TestInfo* const testInfo = ::testing::UnitTest::GetInstance()->current_test_info();
        std::string fileName = "/data/local/graphic_test/example/";
        std::filesystem::create_directories(fileName);
        fileName += testInfo->test_case_name() + std::string("_") + testInfo->name() + ".png";
        WriteToPngWithPixelMap(fileName, *pixelMap);
    }
};

GRAPHIC_N_TEST(ExampleManualCaptureTest, CONTENT_DISPLAY_TEST, Example_Manual_Capture_Test)
{
    auto node = RSCanvasNode::Create();
    node->SetBounds({ 100, 100, 300, 300 });
    node->SetBackgroundColor(0xffff0000);
    GetRootNode()->AddChild(node);
    RegisterNode(node);

    RSTransactionProxy::GetInstance()->FlushImplicitTransaction();
    usleep(SLEEP_TIME_FOR_PROXY);
    TestCaseCapture();
}
} // namespace OHOS::Rosen
```

## BUILD.gn 插入提醒

```gn
rs_display_effect_sources = [
  "rs_display_effect/property_display/example_property_test.cpp",
]
```

选择与文件路径匹配的 source array。
