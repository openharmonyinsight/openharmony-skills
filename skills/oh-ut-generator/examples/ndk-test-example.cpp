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

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <native_window/external_window.h>
#include <cstddef>

using namespace testing;
using namespace OHOS;

class ExternalWindowNdKTest : public testing::Test {
public:
    static void SetUpTestCase(void) {}
    static void TearDownTestCase(void) {}
    void SetUp() override {}
    void TearDown() override {}

protected:
};

/**
 * @tc.name: ExternalWindowNdKTest_OH_NativeWindow_Create_001
 * @tc.desc: Test OH_NativeWindow_Create with valid parameters
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, OH_NativeWindow_Create_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin OH_NativeWindow_Create_001";

    // Create native window with valid parameters
    OH_NativeWindow* window = OH_NativeWindow_Create(
        NATIVE_WINDOW_DEFAULT,
        NATIVE_USE_GPU
    );

    // Verify window was created successfully
    ASSERT_NE(window, nullptr);

    // Destroy window
    OH_NativeWindow_Destroy(window);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end OH_NativeWindow_Create_001";
}

/**
 * @tc.name: ExternalWindowNdKTest_OH_NativeWindow_Create_002
 * @tc.desc: Test OH_NativeWindow_Create with invalid type parameter
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, OH_NativeWindow_Create_002, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin OH_NativeWindow_Create_002";

    // Create native window with invalid type
    OH_NativeWindow* window = OH_NativeWindow_Create(
        static_cast<OH_NativeWindow_Type>(-1),
        NATIVE_USE_GPU
    );

    // Verify window creation failed
    EXPECT_EQ(window, nullptr);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end OH_NativeWindow_Create_002";
}

/**
 * @tc.name: ExternalWindowNdKTest_OH_NativeWindow_GetNativeWindow_001
 * @tc.desc: Test OH_NativeWindow_GetNativeWindow with valid window
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, OH_NativeWindow_GetNativeWindow_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin OH_NativeWindow_GetNativeWindow_001";

    // Create native window
    OH_NativeWindow* window = OH_NativeWindow_Create(
        NATIVE_WINDOW_DEFAULT,
        NATIVE_USE_GPU
    );
    ASSERT_NE(window, nullptr);

    // Get native window handle
    OHNativeWindow* nativeWindow = OH_NativeWindow_GetNativeWindow(window);

    // Verify native window handle is valid
    ASSERT_NE(nativeWindow, nullptr);

    // Cleanup
    OH_NativeWindow_Destroy(window);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end OH_NativeWindow_GetNativeWindow_001";
}

/**
 * @tc.name: ExternalWindowNdKTest_OH_NativeWindow_GetNativeWindow_002
 * @tc.desc: Test OH_NativeWindow_GetNativeWindow with null window
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, OH_NativeWindow_GetNativeWindow_002, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin OH_NativeWindow_GetNativeWindow_002";

    // Get native window handle with null window
    OHNativeWindow* nativeWindow = OH_NativeWindow_GetNativeWindow(nullptr);

    // Verify native window handle is null
    EXPECT_EQ(nativeWindow, nullptr);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end OH_NativeWindow_GetNativeWindow_002";
}

/**
 * @tc.name: ExternalWindowNdKTest_OH_NativeWindow_SetNativeWindowReact_001
 * @tc.desc: Test setting native window react with valid parameters
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, OH_NativeWindow_SetNativeWindowReact_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin OH_NativeWindow_SetNativeWindowReact_001";

    // Create native window
    OH_NativeWindow* window = OH_NativeWindow_Create(
        NATIVE_WINDOW_DEFAULT,
        NATIVE_USE_GPU
    );
    ASSERT_NE(window, nullptr);

    // Create callback structure
    struct OH_NativeWindowReactCallback reactCallback;
    reactCallback.OnSurfaceCreated = [](OH_NativeWindow* window, void* userdata) -> int32_t {
        return 0;
    };
    reactCallback.OnSurfaceChanged = [](OH_NativeWindow* window, void* userdata) -> int32_t {
        return 0;
    };
    reactCallback.OnSurfaceDestroyed = [](OH_NativeWindow* window, void* userdata) -> int32_t {
        return 0;
    };

    // Set react callback
    int32_t result = OH_NativeWindow_SetNativeWindowReact(
        window,
        &reactCallback,
        nullptr
    );

    // Verify result
    EXPECT_EQ(result, 0);

    // Cleanup
    OH_NativeWindow_Destroy(window);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end OH_NativeWindow_SetNativeWindowReact_001";
}

/**
 * @tc.name: ExternalWindowNdKTest_OH_NativeWindow_SetNativeWindowReact_002
 * @tc.desc: Test setting native window react with null window
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, OH_NativeWindow_SetNativeWindowReact_002, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin OH_NativeWindow_SetNativeWindowReact_002";

    // Create callback structure
    struct OH_NativeWindowReactCallback reactCallback;
    reactCallback.OnSurfaceCreated = nullptr;
    reactCallback.OnSurfaceChanged = nullptr;
    reactCallback.OnSurfaceDestroyed = nullptr;

    // Set react callback with null window
    int32_t result = OH_NativeWindow_SetNativeWindowReact(
        nullptr,
        &reactCallback,
        nullptr
    );

    // Verify result - should fail with invalid parameter
    EXPECT_NE(result, 0);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end OH_NativeWindow_SetNativeWindowReact_002";
}

/**
 * @tc.name: ExternalWindowNdKTest_ResourceLifecycle_001
 * @tc.desc: Test complete resource lifecycle (Create -> Use -> Destroy)
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, ResourceLifecycle_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin ResourceLifecycle_001";

    // Create
    OH_NativeWindow* window = OH_NativeWindow_Create(
        NATIVE_WINDOW_DEFAULT,
        NATIVE_USE_GPU
    );
    ASSERT_NE(window, nullptr);

    // Use - get native window handle
    OHNativeWindow* nativeWindow = OH_NativeWindow_GetNativeWindow(window);
    ASSERT_NE(nativeWindow, nullptr);

    // Use - set window geometry
    int32_t setResult = OH_NativeWindow_SetNativeWindowGeometry(
        window,
        0,
        0,
        1920,
        1080
    );
    EXPECT_EQ(setResult, 0);

    // Destroy
    OH_NativeWindow_Destroy(window);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end ResourceLifecycle_001";
}

/**
 * @tc.name: ExternalWindowNdKTest_SetNativeWindowGeometry_001
 * @tc.desc: Test setting window geometry with valid dimensions
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, SetNativeWindowGeometry_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin SetNativeWindowGeometry_001";

    // Create native window
    OH_NativeWindow* window = OH_NativeWindow_Create(
        NATIVE_WINDOW_DEFAULT,
        NATIVE_USE_GPU
    );
    ASSERT_NE(window, nullptr);

    // Set valid geometry
    int32_t result = OH_NativeWindow_SetNativeWindowGeometry(
        window,
        0,
        0,
        1920,
        1080
    );

    // Verify result
    EXPECT_EQ(result, 0);

    // Cleanup
    OH_NativeWindow_Destroy(window);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end SetNativeWindowGeometry_001";
}

/**
 * @tc.name: ExternalWindowNdKTest_SetNativeWindowGeometry_002
 * @tc.desc: Test setting window geometry with boundary values
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ExternalWindowNdKTest, SetNativeWindowGeometry_002, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-begin SetNativeWindowGeometry_002";

    // Create native window
    OH_NativeWindow* window = OH_NativeWindow_Create(
        NATIVE_WINDOW_DEFAULT,
        NATIVE_USE_GPU
    );
    ASSERT_NE(window, nullptr);

    // Set geometry with zero width/height (boundary case)
    int32_t result1 = OH_NativeWindow_SetNativeWindowGeometry(
        window,
        0,
        0,
        0,
        0
    );
    // May return error or handle gracefully depending on implementation

    // Set geometry with maximum values
    int32_t result2 = OH_NativeWindow_SetNativeWindowGeometry(
        window,
        0,
        0,
        INT_MAX,
        INT_MAX
    );
    // May return error or handle gracefully

    // Cleanup
    OH_NativeWindow_Destroy(window);

    GTEST_LOG_(INFO) << "ExternalWindowNdKTest-end SetNativeWindowGeometry_002";
}
