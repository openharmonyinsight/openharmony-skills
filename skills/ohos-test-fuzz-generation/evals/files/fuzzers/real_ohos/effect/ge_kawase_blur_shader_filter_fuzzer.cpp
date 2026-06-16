/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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

#include "ge_kawase_blur_shader_filter_fuzzer.h"
#include "ge_kawase_blur_shader_filter.h"
#include "ge_system_properties.h"
#include "get_object.h"
#include <fuzzer/FuzzedDataProvider.h>

namespace OHOS {
namespace Rosen {

std::shared_ptr<Drawing::Image> ProcessImageFuzzTest()
{
    Drawing::Rect src = GETest::GetPlainData<Drawing::Rect>();
    Drawing::Rect dst = GETest::GetPlainData<Drawing::Rect>();

    Drawing::GEKawaseBlurShaderFilterParams params = {5};
    std::unique_ptr<GEKawaseBlurShaderFilter> shaderFilter =
        std::make_unique<GEKawaseBlurShaderFilter>(params);

    Drawing::Canvas canvas;
    std::shared_ptr<Drawing::Image> image { nullptr };
    shaderFilter->ProcessImage(canvas, image, src, dst);
    shaderFilter->InitSimpleFilter();
    GESystemProperties::GetBoolSystemProperty("persist.sys.graphic.supports_af", false);

    Drawing::Bitmap bmp;
    Drawing::BitmapFormat format { Drawing::COLORTYPE_RGBA_8888, Drawing::ALPHATYPE_PREMUL };
    bmp.Build(50, 50, format); // 50, 50  bitmap size
    bmp.ClearWithColor(Drawing::Color::COLOR_BLUE);
    image = bmp.MakeImage();
    auto res = shaderFilter->ProcessImage(canvas, image, src, dst);
    return res;
}

int GetRadiusFuzzTest()
{
    int radius = GETest::GetPlainData<int>();

    Drawing::GEKawaseBlurShaderFilterParams params = {radius};
    std::unique_ptr<GEKawaseBlurShaderFilter> kawaseBlurShaderFilter =
        std::make_unique<GEKawaseBlurShaderFilter>(params);
    kawaseBlurShaderFilter->GetDescription();
    int res = kawaseBlurShaderFilter->GetRadius();
    return res;
}

std::shared_ptr<Drawing::Image> ScaleAndAddRandomColorFuzzTest(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);

    Drawing::GEKawaseBlurShaderFilterParams params { 1 };
    auto shaderFilter = std::make_shared<GEKawaseBlurShaderFilter>(params);
    Drawing::Canvas canvas;

    Drawing::Bitmap bmp;
    Drawing::BitmapFormat format { Drawing::COLORTYPE_RGBA_8888, Drawing::ALPHATYPE_PREMUL };
    bmp.Build(50, 50, format); // 50, 50  bitmap size
    bmp.ClearWithColor(Drawing::Color::COLOR_BLUE);
    auto image = bmp.MakeImage();

    bmp.Build(100, 30, format); // 100, 30  bitmap size
    bmp.ClearWithColor(Drawing::Color::COLOR_RED);
    auto imageBlur = bmp.MakeImage();

    Drawing::Rect src{fdp.ConsumeFloatingPoint<float>(), fdp.ConsumeFloatingPoint<float>(),
        fdp.ConsumeFloatingPoint<float>(), fdp.ConsumeFloatingPoint<float>()};
    Drawing::Rect dst{fdp.ConsumeFloatingPoint<float>(), fdp.ConsumeFloatingPoint<float>(),
        fdp.ConsumeFloatingPoint<float>(), fdp.ConsumeFloatingPoint<float>()};
    int width = fdp.ConsumeIntegral<int32_t>();
    int height = fdp.ConsumeIntegral<int32_t>();

    auto res = shaderFilter->ScaleAndAddRandomColor(canvas, image, imageBlur, src, dst, width, height);
    return res;
}

void OutputOriginalImageFuzzTest()
{
    Drawing::GEKawaseBlurShaderFilterParams params { 1 };
    auto shaderFilter = std::make_shared<GEKawaseBlurShaderFilter>(params);
    Drawing::Canvas canvas;
    Drawing::Bitmap bmp;
    Drawing::BitmapFormat format { Drawing::COLORTYPE_RGBA_8888, Drawing::ALPHATYPE_PREMUL };
    bmp.Build(50, 50, format); // 50, 50  bitmap size
    bmp.ClearWithColor(Drawing::Color::COLOR_BLUE);
    auto image = bmp.MakeImage();
    Drawing::Rect src = GETest::GetPlainData<Drawing::Rect>();
    Drawing::Rect dst = GETest::GetPlainData<Drawing::Rect>();
    shaderFilter->OutputOriginalImage(canvas, image, src, dst);
}

} // namespace Rosen
} // namespace OHOS

/* Fuzzer entry point */
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    if (data == nullptr) {
        return 0;
    }
    // initialize
    OHOS::Rosen::GETest::g_data = data;
    OHOS::Rosen::GETest::g_size = size;
    OHOS::Rosen::GETest::g_pos = 0;
    /* Run your code on data */
    OHOS::Rosen::ProcessImageFuzzTest();
    OHOS::Rosen::GetRadiusFuzzTest();
    OHOS::Rosen::ScaleAndAddRandomColorFuzzTest(data, size);
    OHOS::Rosen::OutputOriginalImageFuzzTest();
    return 0;
}
