# Camera 模块 CAPI 配置

## 一、模块基础信息

- **模块名称**: Camera
- **模块描述**: 相机框架，提供相机设备管理、会话管理、输入输出控制等能力
- **子系统**: Multimedia
- **API 语言**: C（通过 N-API 封装供 ETS/ArkTS 测试）
- **测试路径**: `test/xts/acts/multimedia/camera/`
- **系统能力**: `SystemCapability.Multimedia.Camera.Core`

## 二、模块功能概述

Camera 模块提供相机设备的完整管理能力：

### 2.1 核心能力

- **相机设备管理**：获取相机设备列表、设备查询
- **会话管理**：创建和配置拍照会话、录像会话
- **输入控制**：相机输入（预览流、拍照输入）
- **输出控制**：预览输出、照片输出、视频输出
- **闪光灯控制**：支持查询和设置闪光灯模式
- **对焦控制**：支持变焦控制
- **曝光控制**：支持曝光模式、曝光时间
- **场景模式**：正常照片、正常视频、安全拍照
- **变焦模式**：平滑变焦、手动对焦
- **视频防抖**：开启/关闭视频防抖

### 2.2 支持的场景

- **拍照场景**：正常拍照、安全拍照、连拍
- **录像场景**：预览录像、后台录像、慢动作录像
- **预览场景**：前后置摄像头预览、变焦测试
- **闪光灯场景**：自动闪光、强制闪光、关闭闪光
- **对焦场景**：单点对焦、连续对焦
- **曝光场景**：自动曝光、手动曝光、曝光补偿
- **视频防抖场景**：防抖开、防抖关

## 三、头文件路径

### 3.1 Include 方式（重要）

**Camera CAPI 头文件必须使用 `<ohcamera/xxx.h>` 格式**，这是系统头文件的正确引用方式。

```cpp
// 正确方式 ✅
#include <ohcamera/camera.h>
#include <ohcamera/camera_manager.h>
#include <ohcamera/camera_input.h>
#include <ohcamera/capture_session.h>
#include <ohcamera/camera_device.h>
#include <ohcamera/preview_output.h>
#include <ohcamera/photo_output.h>
#include <ohcamera/photo_native.h>
#include <ohcamera/video_output.h>
#include <ohcamera/metadata_output.h>

// 错误方式 ❌（会导致编译错误：file not found）
#include "camera.h"
#include "camera_manager.h"
#include "camera_input.h"
```

**项目内本地头文件**使用 `"xxx.h"` 格式：
```cpp
#include "CameraTest.h"
#include "CameraComTest.h"
#include "native_common.h"
```

**其他常用系统头文件**：
```cpp
#include <napi/native_api.h>                                           // N-API 接口
#include <hilog/log.h>                                                 // 日志
#include <multimedia/image_framework/image/image_receiver_native.h>    // 图像处理
#include <native_window/external_window.h>                             // 原生窗口
#include <cstdint>
#include <cstring>
#include <string>
```

### 3.2 完整 Include 示例（参考 camera_ndk_supplement）

```cpp
// CameraTest.h - 头文件示例
#ifndef OHCAMERATEST_CAMERA_TEST_H
#define OHCAMERATEST_CAMERA_TEST_H

#include <ohcamera/camera.h>
#include <ohcamera/camera_manager.h>
#include <ohcamera/capture_session.h>
#include <ohcamera/camera_device.h>
#include <ohcamera/camera_input.h>
#include <ohcamera/photo_output.h>
#include <string>

// ... class 定义
#endif
```

```cpp
// CameraOutTest.cpp - 源文件示例
#include <hilog/log.h>
#include <ohcamera/camera.h>
#include <ohcamera/camera_manager.h>
#include <ohcamera/capture_session.h>
#include <ohcamera/camera_device.h>
#include <ohcamera/camera_input.h>
#include <ohcamera/photo_output.h>
#include <ohcamera/photo_native.h>
#include <ohcamera/video_output.h>
#include <string>
#include <napi/native_api.h>
#include <unistd.h>
#include "CameraComTest.h"
#include "CameraErrCodeTest.h"
```

### 3.3 头文件位置（相对于 {OH_ROOT}/interface/sdk_c）

```
{OH_ROOT}/interface/sdk_c/multimedia/camera_framework/
  ├── camera.h                  // 相机核心定义
  ├── camera_manager.h           // 相机管理器
  ├── camera_input.h            // 相机输入控制
  ├── camera_output.h           // 相机输出控制
  ├── preview_output.h          // 预览输出
  ├── photo_output.h           // 照片输出
  ├── video_output.h           // 视频输出
  ├── capture_session.h        // 拍照会话
  └── ...
```

## 四、API 列表

### 4.1 相机管理器 API

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|---------|
| `OH_Camera_GetCameraManager` | 获取相机管理器实例 | Camera_ErrorCode | camera_manager.h |
| `OH_Camera_DeleteCameraManager` | 删除相机管理器实例 | Camera_ErrorCode | camera_manager.h |
| `OH_Camera_RegisterCallback` | 注册相机状态回调 | Camera_ErrorCode | camera_manager.h |

### 4.2 相机管理回调类型

| 回调类型 | 说明 | 头文件 |
|---------|------|---------|
| `OH_CameraManager_StatusCallback` | 相机状态变化回调 | camera_manager.h |
| `OH_CameraManager_TorchStatusCallback` | 手电筒状态变化回调 | camera_manager.h |
| `OH_CameraManager_OnFoldStatusInfoChange` | 折叠状态信息变化回调 | camera_manager.h |

### 4.3 相机状态相关

| 类型 | 枚举值 | 说明 | 头文件 |
|------|--------|------|---------|
| `Camera_Status` | CAMERA_STATUS_APPEAR、CAMERA_STATUS_AVAILABLE、CAMERA_STATUS_UNAVAILABLE | 相机状态 | camera.h |
| `Camera_ErrorCode` | CAMERA_OK、CAMERA_INVALID_ARGUMENT、CAMERA_OPERATION_NOT_ALLOWED 等（16+ 个错误码） | camera.h |

### 4.4 设备相关

| 类型 | 说明 | 头文件 |
|------|------|---------|
| `Camera_Manager` | 相机管理器类型 | camera_manager.h |
| `Camera_Device` | 相机设备信息 | camera_manager.h |
| `Camera_DeviceQueryInfo` | 设备查询信息 | camera_manager.h |

### 4.5 输入控制相关

| 类型 | 说明 | 头文件 |
|------|------|---------|
| `Camera_Input` | 相机输入流 | camera_input.h |
| `OH_Camera_CreateCameraInput` | 创建相机输入 | Camera_ErrorCode | camera_input.h |
| `OH_Camera_DeleteCameraInput` | 删除相机输入 | Camera_ErrorCode | camera_input.h |
| `OH_CameraInput_Close` | 关闭相机输入 | Camera_ErrorCode | camera_input.h |

### 4.6 输出控制相关

| 类型 | 说明 | 头文件 |
|------|------|---------|
| `Preview_Output` | 预览输出 | preview_output.h |
| `Photo_Output` | 照片输出 | photo_output.h |
| `Video_Output` | 视频输出 | video_output.h |
| `OH_Camera_CreatePreviewOutput` | 创建预览输出 | Camera_ErrorCode | preview_output.h |
| `OH_Camera_CreatePhotoOutput` | 创建照片输出 | Camera_ErrorCode | photo_output.h |
| `OH_Camera_CreateVideoOutput` | 创建视频输出 | Camera_ErrorCode | video_output.h |

### 4.7 会话相关

| 类型 | 说明 | 头文件 |
|------|------|---------|
| `Capture_Session` | 拍照会话 | capture_session.h |
| `OH_CameraManager_CreateCaptureSession` | 创建拍照会话 | Camera_ErrorCode | camera_manager.h |
| `OH_CameraManager_DeleteCaptureSession` | 删除拍照会话 | Camera_ErrorCode | camera_manager.h |
| `OH_CaptureSession_Begin` | 开始会话配置 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_CommitConfig` | 提交会话配置 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_Start` | 开始会话 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_Stop` | 停止会话 | Camera_ErrorCode | capture_session.h |

### 4.8 场景模式

| 场景模式 | 枚举值 | 说明 | 头文件 |
|---------|--------|------|---------|
| `Camera_SceneMode` | NORMAL_PHOTO、NORMAL_VIDEO、SECURE_PHOTO | 场景模式 | camera.h |
| `Camera_Position` | CAMERA_POSITION_BACK、CAMERA_POSITION_FRONT、CAMERA_POSITION_UNSPECIFIED 摄像头位置 | camera.h |

### 4.9 闪光灯相关

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|---------|
| `OH_CaptureSession_HasFlash` | 检测是否有闪光灯 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_IsFlashModeSupported` | 检查闪光灯模式是否支持 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_SetFlashMode` | 设置闪光灯模式 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_GetFlashMode` | 获取当前闪光灯模式 | Camera_ErrorCode | capture_session.h |

### 4.10 变焦相关

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|---------|
| `OH_CaptureSession_GetZoomRatio` | 获取变焦范围 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_SetZoomRatio` | 设置变焦比例 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_GetZoomRatioRange` | 获取支持的变焦范围 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_GetZoomRatio` | 获取当前变焦值 | Camera_ErrorCode | capture_session.h |
| `OH_CaptureSession_SetZoomRatio` | 设置变焦值 | Camera_ErrorCode | capture_session.h |

## 五、错误码枚举

| 错误码 | 值 | 说明 | 头文件 |
|--------|------|------|------|
| `CAMERA_OK` | 0 | 操作成功 | camera_manager.h |
| `CAMERA_INVALID_ARGUMENT` | 7400101 | 参数无效 | camera_manager.h |
| `CAMERA_OPERATION_NOT_ALLOWED` | 7400102 | 操作不被允许 | camera_manager.h |
| `CAMERA_SESSION_NOT_CONFIG` | 7400103 | 会话未配置 | camera_manager.h |
| `CAMERA_SESSION_NOT_RUNNING` | 7400104 | 会话未运行 | camera_manager.h |
| `CAMERA_SESSION_CONFIG_LOCKED` | 7400105 | 会话配置锁定 | camera_manager.h |
| `CAMERA_DEVICE_SETTING_LOCKED` | 7400106 | 设备设置锁定 | camera_manager.h |
| `CAMERA_CONFLICT_CAMERA` | 7400107 | 相机冲突 | camera_manager.h |
| `CAMERA_DEVICE_DISABLED` | 7400108 | 相机被禁用 | camera_manager.h |
| `CAMERA_DEVICE_PREEMPTED` | 7400109 | 相机被抢占 | camera_manager.h |
| `CAMERA_SERVICE_FATAL_ERROR` | 7400201 | 相机服务致命错误 | camera_manager.h |

## 六、N-API 封装规范

### 6.1 辅助函数

#### CameraManager 实例管理

```cpp
static Camera_Manager* g_cameraManager = nullptr;

static bool GetCameraManagerInstance()
{
    if (g_cameraManager == nullptr) {
        Camera_ErrorCode ret = OH_Camera_GetCameraManager(&g_cameraManager);
        if (ret != CAMERA_OK || g_cameraManager == nullptr) {
            return false;
        }
        return true;
    }
}

static void ReleaseCameraManagerInstance()
{
    if (g_cameraManager != nullptr) {
        Camera_ErrorCode ret = OH_Camera_DeleteCameraManager(g_cameraManager);
        g_cameraManager = nullptr;
    }
}
```

#### Callback 注册辅助函数

```cpp
static void RegisterCameraManagerCallback()
{
    CameraManager_RegisterStatusCallback(g_cameraManager, &CameraStatusCallback);
}
```

### 6.2 相机管理器 API 封装模板

#### 获取相机管理器

```cpp
static napi_value GetCameraManager_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_status status = napi_get_cb_info(env, info, &argc, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "GetCameraManager requires no arguments");
        return nullptr;
    }

    if (!GetCameraManagerInstance()) {
        napi_throw_error(env, nullptr, "Failed to get camera manager");
        return nullptr;
    }

    // 释放实例在 Init 函数中完成
    // Camera_ErrorCode ret = OH_Camera_DeleteCameraManager(g_cameraManager);

    napi_value result;
    napi_get_boolean(env, true, &result);
    return result;
}
```

#### 删除相机管理器

```cpp
static napi_value DeleteCameraManager_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_status status = napi_get_cb_info(env, info, &argc, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "DeleteCameraManager requires no arguments");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_Camera_DeleteCameraManager(g_cameraManager);
    g_cameraManager = nullptr;

    napi_value result;
    if (ret == CAMERA_OK) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_throw_error(env, nullptr, "DeleteCameraManager failed");
        return nullptr;
    }

    return result;
}
```

### 6.3 相机输入 API 封装模板

#### 创建相机输入

```cpp
static napi_value CreateCameraInput_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, & argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 1) {
        napi_throw_error(env, nullptr, "CreateCameraInput requires 1 argument (cameraId)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string (cameraId)");
        return nullptr;
    }

    size_t strLen;
    char cameraId[256];
    status = napi_get_value_string_utf8(env, args[0], cameraId, sizeof(cameraId) - 1, &strLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get cameraId string");
        return nullptr;
    }

    uint32_t cameraIdUint = 0;
    if (strLen > 0) {
        cameraIdUint = static_cast<uint32_t>(atoi(cameraId));
    }

    Camera_ErrorCode ret = OH_Camera_CreateCameraInput(g_cameraManager, cameraIdUint, &g_cameraInput);
    if (ret != CAMERA_OK || g_cameraInput == nullptr) {
        napi_throw_error(env, nullptr, "Failed to create camera input");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 关闭相机输入

```cpp
static napi_value CloseCameraInput_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, & argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 1) {
        napi_throw_error(env, nullptr, "CloseCameraInput requires 1 argument (cameraId)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string (cameraId)");
        return nullptr;
    }

    size_t strLen;
    char cameraId[256];
    status = napi_get_value_string_utf8(env, args[0], cameraId, sizeof(cameraId) - 1, &strLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get cameraId string");
        return nullptr;
    }

    uint32_t cameraIdUint = 0;
    if (strLen > 0) {
        cameraIdUint = static_cast<uint32_t>(atoi(cameraId));
    }

    Camera_ErrorCode ret = OH_CameraInput_Close(g_cameraInput);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to close camera input");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

### 6.4 相机输出 API 封装模板

#### 创建预览输出

```cpp
static napi_value CreatePreviewOutput_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "CreatePreviewOutput requires at least 1 argument (surfaceId)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument 1 must be a number (surfaceId)");
        return nullptr;
    }

    int32_t surfaceId;
    status = napi_get_value_int32(env, args[0], &surfaceId);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get surfaceId");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_Camera_CreatePreviewOutput(g_previewOutput, surfaceId);
    if (ret != CAMERA_OK || g_previewOutput == nullptr) {
        napi_throw_error(env, nullptr, "Failed to create preview output");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 删除预览输出

```cpp
static napi_value DeletePreviewOutput_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 1) {
        napi_throw_error(env, nullptr, "DeletePreviewOutput requires 1 argument (surfaceId)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument 1 must be a number (surfaceId)");
        return nullptr;
    }

    int32_t surfaceId;
    status = napi_get_value_int32(env, args[0], &surfaceId);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get surfaceId");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_Camera_DeletePreviewOutput(g_previewOutput, surfaceId);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to delete preview output");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 创建照片输出

```cpp
static napi_value CreatePhotoOutput_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 1) {
        napi_throw_error(env, nullptr, "CreatePhotoOutput requires 1 argument (surfaceId)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument 1 must be a number (surfaceId)");
        return nullptr;
    }

    int32_t surfaceId;
    status = napi_get_value_int32(env, args[0], &surfaceId);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get surfaceId");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_Camera_CreatePhotoOutput(g_photoOutput, surfaceId);
    if (ret != CAMERA_OK || g_photoOutput == nullptr) {
        napi_throw_error(env, nullptr, "Failed to create photo output");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

### 6.5 拍照会话 API 封装模板

#### 创建拍照会话

```cpp
static napi_value CreateCaptureSession_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "CreateCaptureSession requires no arguments");
        return nullptr;
    }

    if (!GetCameraManagerInstance()) {
        napi_throw_error(env, nullptr, "Failed to get camera manager");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CameraManager_CreateCaptureSession(g_cameraManager, &g_captureSession);
    if (ret != CAMERA_OK || g_captureSession == nullptr) {
        napi_throw_error(env, nullptr, "Failed to create capture session");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 开始会话配置

```cpp
static napi_value BeginCaptureSessionConfig_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "BeginCaptureSessionConfig requires no arguments");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CaptureSession_BeginConfig(g_captureSession);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to begin capture session config");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 提交会话配置

```cpp
static napi_value CommitCaptureSessionConfig_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "CommitCaptureSessionConfig requires no arguments");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CaptureSession_CommitConfig(g_captureSession);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to commit capture session config");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 开始会话

```cpp
static napi_value StartCaptureSession_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "StartCaptureSession requires no arguments");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CaptureSession_Start(g_captureSession);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to start capture session");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 停止会话

```cpp
static napi_value StopCaptureSession_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        n_throw_error(env, nullptr, "StopCaptureSession requires no arguments");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CaptureSession_Stop(g_captureSession);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to stop capture session");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

### 6.6 闪光灯 API 封装模板

#### 检测是否有闪光灯

```cpp
static napi_value HasFlash_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "HasFlash requires no arguments");
        return nullptr;
    }

    bool hasFlash = false;
    Camera_ErrorCode ret = OH_CaptureSession_HasFlash(g_captureSession, &hasFlash);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to check flash");
        return nullptr;
    }

    napi_value result;
    napi_get_boolean(env, hasFlash, &result);
    return result;
}
```

#### 检查闪光灯模式是否支持

```cpp
static napi_value IsFlashModeSupported_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != n_ok || argc != 1) {
        napi_throw_error(env, nullptr, "IsFlashModeSupported requires 1 argument (flashMode)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument must be a number (flashMode)");
        return nullptr;
    }

    int32_t flashMode;
    status = napi_get_value_int32(env, args[0], &flashMode);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get flash mode");
        return nullptr;
    }

    bool isSupported = false;
    Camera_ErrorCode ret = OH_CaptureSession_IsFlashModeSupported(g_captureSession, flashMode, &isSupported);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to check flash mode supported");
        return nullptr;
    }

    napi_value result;
    napi_get_boolean(env, isSupported, &result);
    return result;
}
```

#### 设置闪光灯模式

```cpp
static napi_value SetFlashMode_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 1) {
        napi_throw_error(env, nullptr, "SetFlashMode requires 1 argument (flashMode)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument must be a number (flashMode)");
        return nullptr;
    }

    int32_t flashMode;
    status = napi_get_value_int32(env, args[0], &flashMode);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get flash mode");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CaptureSession_SetFlashMode(g_captureSession, flashMode);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to set flash mode");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 获取当前闪光灯模式

```cpp
static napi_value GetFlashMode_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "GetFlashMode requires no arguments");
        return nullptr;
    }

    int32_t flashMode = 0;
    Camera_ErrorCode ret = OH_CaptureSession_GetFlashMode(g_captureSession, &flashMode);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to get flash mode");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, flashMode, &result);
    return result;
}
```

### 6.7 变焦 API 封装模板

#### 获取变焦范围

```cpp
static napi_value GetZoomRatioRange_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 2) {
        napi_throw_error(env, nullptr, "GetZoomRatioRange requires 2 arguments (minZoom, maxZoom)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument 1 (minZoom) must be a number");
        return nullptr;
    }

    float minZoom;
    status = napi_get_value_double(env, args[0], &minZoom);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get minZoom");
        return nullptr;
    }

    status = napi_typeof(env, args[1], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument 2 (maxZoom) must be a number");
        return nullptr;
    }

    float maxZoom;
    status = napi_get_value_double(env, args[1], &maxZoom);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get maxZoom");
        return nullptr;
    }

    float minZoomRet = 0.0f;
    float maxZoomRet = 0.0f;
    Camera_ErrorCode ret = OH_CaptureSession_GetZoomRatioRange(g_captureSession, &minZoomRet, &maxZoomRet);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to get zoom ratio range");
        return nullptr;
    }

    napi_value result;
    napi_create_object(env);
    
    napi_value minZoomValue;
    napi_create_double(env, minZoomRet, &minZoomValue);
    napi_set_named_property(env, result, "minZoom", minZoomValue);
    
    napi_value maxZoomValue;
    napi_create_double(env, maxZoomRet, &maxZoomValue);
    napi_set_named_property(env, result, "maxZoom", maxZoomValue);
    
    return result;
}
```

#### 设置变焦值

```cpp
static napi_value SetZoomRatio_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 1) {
        napi_throw_error(env, nullptr, "SetZoomRatio requires 1 argument (zoom)");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument must be a number (zoom)");
        return nullptr;
    }

    float zoom;
    status = napi_get_value_double(env, args[0], &zoom);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get zoom value");
        return nullptr;
    }

    Camera_ErrorCode ret = OH_CaptureSession_SetZoomRatio(g_captureSession, zoom);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to set zoom ratio");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}
```

#### 获取当前变焦值

```cpp
static napi_value GetZoomRatio_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_value args[0];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc != 0) {
        napi_throw_error(env, nullptr, "GetZoomRatio requires no arguments");
        return nullptr;
    }

    float zoom = 0.0f;
    Camera_ErrorCode ret = OH_CaptureSession_GetZoomRatio(g_captureSession, &zoom);
    if (ret != CAMERA_OK) {
        napi_throw_error(env, nullptr, "Failed to get zoom ratio");
        return nullptr;
    }

    napi_value result;
    napi_create_double(env, zoom, &result);
    return result;
}
```

## 七、ETS/ArkTS 测试用例模板

### 7.1 测试用例命名规范

```
格式：SUB_MULTIMEDIA_CAMERA_[API名称]_[类型]_[序号]
示例：SUB_MULTIMEDIA_CAMERA_GetCameraManager_PARAM_001
```

### 7.2 相机管理器测试模板

#### 获取相机管理器测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_GetCameraManager_PARAM_001
 * @tc.desc: 测试获取相机管理器
 * @tc.type: FUNC
 */
it('GetCameraManager', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================GetCameraManager start==================");
    try {
        const result = testNapi.getCameraManager();
        expect(result).assertTrue();
        hilog.info(domain, tag, `GetCameraManager result: ${result}`);
        done();
    } catch (err) {
        hilog.error(domain, tag, `GetCameraManager error: ${JSON.stringify(err)}`);
        expect().assertFail();
        done();
    }
    hilog.info(domain, tag, "==================GetCameraManager end==================");
});
```

#### 删除相机管理器测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_DeleteCameraManager_ERROR_001
 * @tc.desc: 测试删除相机管理器
 * @tc.type: FUNC
 */
it('DeleteCameraManager', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL2, async (done: Function) => {
    hilog.info(domain, tag, "==================DeleteCameraManager start==================");
    try {
        // 先获取管理器
        const result1 = testNapi.getCameraManager();
        expect(result1).assertTrue();
        
        // 再删除管理器
        const result2 = testNapi.deleteCameraManager();
        expect(result2).assertEqual(0);
        hilog.info(domain, tag, `DeleteCameraManager result: ${result2}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `DeleteCameraManager error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================DeleteCameraManager end==================");
});
```

### 7.3 相机输入测试模板

#### 创建相机输入测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_CreateCameraInput_PARAM_001
 * @tc.desc: 测试创建相机输入
 * @tc.type: FUNC
 */
it('CreateCameraInput', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================CreateCameraInput start==================");
    try {
        const cameraId = "0";
        const result = testNapi.createCameraInput(cameraId);
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `CreateCameraInput cameraId:${cameraId} result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `CreateCameraInput error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================CreateCameraInput end==================");
});
```

#### 关闭相机输入测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_CloseCameraInput_PARAM_001
 * @tc.desc: 测试关闭相机输入
 * @tc.type: FUNC
 */
it('CloseCameraInput', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================CloseCameraInput start==================");
    try {
        const cameraId = "0";
        // 先创建输入
        const result1 = testNapi.createCameraInput(cameraId);
        expect(result1).assertEqual(0);

        // 再关闭输入
        const result2 = testNapi.closeCameraInput(cameraId);
        expect(result2).assertEqual(0);
        hilog.info(domain, tag, "CloseCameraInput cameraId:${cameraId} result1:${result1} result2:${result2}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = ( (err as BusinessError).code;
        hilog.error(domain, tag, `CloseCameraInput error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================CloseCameraInput end==================");
});
```

### 7.4 相机输出测试模板

#### 创建预览输出测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_CreatePreviewOutput_PARAM_001
 * @tc.desc: 测试创建预览输出
 * @tc.type: FUNC
 */
it('CreatePreviewOutput', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================CreatePreviewOutput start==================");
    try {
        const surfaceId = 1;
        const result = testNapi.createPreviewOutput(surfaceId);
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `CreatePreviewOutput surfaceId:${surfaceId} result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `CreatePreviewOutput error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================CreatePreviewOutput end==================");
});
```

#### 删除预览输出测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_DeletePreviewOutput_ERROR_001
 * @tc.desc: 测试删除预览输出
 * @tc.type: FUNC
 */
it('DeletePreviewOutput', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================DeletePreviewOutput start==================");
    try {
        const surfaceId = 1;
        // 先创建输出
        const result1 = testNapi.createPreviewOutput(surfaceId);
        expect(result1).assertEqual(0);

        // 再删除输出
        const result2 = testNapi.deletePreviewOutput(surfaceId);
        expect(result2).assertEqual(0);
        hilog.info(domain, tag, `DeletePreviewOutput surfaceId:${surfaceId} result1:${result1} result2:${result2}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = ( err as BusinessError).code;
        hilog.error(domain, tag, `DeletePreviewOutput error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================DeletePreviewOutput end==================");
});
```

### 7.5 拍照会话测试模板

#### 创建拍照会话测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_CreateCaptureSession_PARAM_001
 * @tc.desc: 测试创建拍照会话
 * @tc.type: FUNC
 */
it('CreateCaptureSession', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================CreateCaptureSession start==================");
    try {
        const result = testNapi.createCaptureSession();
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `CreateCaptureSession result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `CreateCaptureSession error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================CreateCaptureSession end==================");
});
}
```

#### 开始会话配置测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_BeginCaptureSessionConfig_PARAM_001
 * @tc.desc: 测试开始会话配置
 * @tc.type: FUNC
 */
it('BeginCaptureSessionConfig', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1, async (done: Function) => {
    hilog.info(domain, tag, "==================BeginCaptureSessionConfig start==================");
    try {
        const result = testNapi.beginCaptureSessionConfig();
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `BeginCaptureSessionConfig result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `BeginCaptureSessionConfig error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================BeginCaptureSessionConfig end==================");
});
```

#### 提交会话配置测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_CommitCaptureSessionConfig_PARAM_001
 * @tc.desc: 测试提交会话配置
 * @tc.type: FUNC
 */
it('CommitCaptureSessionConfig', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1, async (done: Function) => {
    hilog.info(domain, tag, "==================CommitCaptureSessionConfig start==================");
    try {
        const result = testNapi.commitCaptureSessionConfig();
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `CommitCaptureSessionConfig result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `CommitCaptureSessionConfig error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================CommitCaptureSessionConfig end==================");
});
```

#### 开始会话测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_StartCaptureSession_PARAM_001
 * @tc.desc: 测试开始会话
 * @tc.type: FUNC
 */
it('StartCaptureSession', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================StartCaptureSession start==================");
    try {
        const result = testNapi.startCaptureSession();
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `StartCaptureSession result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `StartCaptureSession error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================StartCaptureSession end==================");
});
}
```

#### 停止会话测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_StopCaptureSession_PARAM_001
 * @tc.desc: 测试停止会话
 * @tc.type: FUNC
 */
it('StopCaptureSession', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================StopCaptureSession start==================");
    try {
        const result = testNapi.stopCaptureSession();
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `StopCaptureSession result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `StopCaptureSession error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================StopCaptureSession end==================");
});
}
```

### 7.6 闪光灯测试模板

#### 检测是否有闪光灯

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_HasFlash_PARAM_001
 * @tc.desc: 测试是否有闪光灯
 * @tc.type: FUNC
 */
it('HasFlash', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================HasFlash start==================");
    try {
        const result = testNapi.hasFlash();
        expect(result).assertEqual(true);
        hilog.info(domain, tag, `HasFlash result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `HasFlash error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================HasFlash end==================");
});
```

#### 检查闪光灯模式是否支持

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_IsFlashModeSupported_ERROR_001
 * @tc.desc: 测试不支持的闪光灯模式
 * @tc.type: FUNC
 */
it('IsFlashModeSupported', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL2, async (done: Function) => {
    hilog.info(domain, tag, "==================IsFlashModeSupported start==================");
    try {
        const flashMode = 9999; // 不存在的闪光灯模式
        const result = testNapi.isFlashModeSupported(flashMode);
        expect(result).assertFalse();
        hilog.info(domain, tag, `IsFlashModeSupported flashMode:${flashMode} result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `IsFlashModeSupported error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================IsFlashModeSupported end==================");
});
}
```

#### 设置闪光灯模式测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_SetFlashMode_PARAM_001
 * @tc.desc: 测试设置闪光灯模式
 * @tc.type: FUNC
 */
it('SetFlashMode', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: Function) => {
    hilog.info(domain, tag, "==================SetFlashMode start==================");
    try {
        // 测试支持的闪光灯模式（通常为 0，即关闭）
        const flashMode = 0;
        const result1 = testNapi.isFlashModeSupported(flashMode);
        expect(result1).assertTrue();
        
        // 设置闪光灯模式
        const result2 = testNapi.setFlashMode(flashMode);
        expect(result2).assertEqual(0);
        
        // 再次验证闪光灯模式
        const result3 = testNapi.getFlashMode();
        expect(result3).assertEqual(flashMode);
        hilog.info(domain, tag, `SetFlashMode flashMode:${flashMode} result1:${result1} result2:${result2} result3:${result3}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `SetFlashMode error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================SetFlashMode end==================");
});
}
```

#### 获取当前闪光灯模式测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_GetFlashMode_PARAM_001
 * @tc.desc: 测试获取闪光灯模式
 * @tc.type: FUNC
 */
it('GetFlashMode', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================GetFlashMode start==================");
    try {
        const result = testNapi.getFlashMode();
        expect(result).assertEqual(0);
        hilog.info(domain, tag, `GetFlashMode result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `GetFlashMode error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================GetFlashMode end==================");
});
}
```

### 7.7 变焦测试模板

#### 获取变焦范围测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_GetZoomRatioRange_PARAM_001
 * @tc.desc: 测试获取变焦范围
 * @tc.type: FUNC
 */
it('GetZoomRatioRange', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================GetZoomRatioRange start==================");
    try {
        const result = testNapi.getZoomRatioRange();
        expect(result).assertEqual(0);
        
        // 验证返回的对象结构
        if (result !== null) {
            expect(result.hasOwnProperty('minZoom')).assertTrue();
            expect(result.hasOwnProperty('maxZoom')).assertTrue();
            expect(typeof result.minZoom === 'number').assertTrue();
            expect(typeof result.maxZoom === 'number').assertTrue();
            expect(result.minZoom >= 0).assertTrue();
            expect(result.maxZoom >= result.minZoom).assertTrue();
        }
        hilog.info(domain, tag, `GetZoomRatioRange result:${JSON.stringify(result)}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `GetZoomRatioRange error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================GetZoomRatioRange end==================");
});
}
```

#### 设置变焦值测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_SetZoomRatio_PARAM_001
 * @tc.desc: 测试设置变焦值
 * @tc.type: FUNC
 */
it('SetZoomRatio', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: Function) => {
    hilog.info(domain, tag, "==================SetZoomRatio start==================");
    try {
        // 测试设置无效变焦值（超出范围）
        const invalidRatio = -1.0;
        const result1 = testNapi.setZoomRatio(invalidRatio);
        expect(result1).assertNotEqual(0);
        
        // 测试设置有效变焦值（在范围内）
        const validRatio = 2.5;
        const result2 = testNapi.setZoomRatio(validRatio);
        expect(result2).assertEqual(0);
        
        // 验证变焦值已更新
        const result3 = testNapi.getZoomRatio();
        expect(result3).assertEqual(validRatio);
        
        hilog.info(domain, tag, `SetZoomRatio ratio:${validRatio} result1:${result1} result2:${result2} result3:${result3}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `SetZoomRatio error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================SetZoomRatio end==================");
});
}
```

#### 获取当前变焦值测试

```typescript
/**
 * @tc.name: SUB_MULTIMEDIA_CAMERA_GetZoomRatio_PARAM_001
 * @tc.desc: 测试获取当前变焦值
 * @tc.type: FUNC
 */
it('GetZoomRatio', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================GetZoomRatio start==================");
    try {
        const result = testNapi.getZoomRatio();
        expect(result).assertEqual(0);
        expect(typeof result === 'number').assertTrue();
        expect(result >= 0).assertTrue();
        hilog.info(domain, tag, `GetZoomRatio result:${result}`);
        done();
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `GetZoomRatio error: errCode:${code} message:${errMsg}`);
        expect().assertFail(`Test should not throw error but got: ${errMsg}`);
        done();
    }
    hilog.info(domain, tag, "==================GetZoomRatio end==================");
});
}
```

## 八、测试覆盖要求

### 8.1 相机管理器测试

- ✅ 测试 `OH_Camera_GetCameraManager` 正常情况
- ✅ 测试 `OH_Camera_DeleteCameraManager` 正常删除

### 8.2 相机输入 API 测试

- ✅ 测试 `OH_Camera_CreateCameraInput` 正常创建不同 cameraId
- ✅ 测试 `OH_Camera_CreateCameraInput` 创建多个输入
- ✅ 测试 `OH_CameraInput_Close` 正常关闭
- ✅ 测试 `OH_CameraInput_Close` 关闭后重新创建

### 8.3 相机输出 API 测试

- ✅ 测试 `OH_Camera_CreatePreviewOutput` 正常创建预览输出
- ✅ 测试 `OH_Camera_CreatePhotoOutput` 正常创建照片输出
- ✅ 测试 `OH_Camera_CreateVideoOutput` 正常创建视频输出
- ✅ 测试 `OH_Camera_DeletePreviewOutput` 正常删除预览输出
- ✅ 测试 `OH_Camera_DeletePhotoOutput` 正常删除照片输出
- ✅ 测试 `OH_Camera_DeleteVideoOutput` 正常删除视频输出

### 8.4 拍照会话 API 测试

- ✅ 测试 `OH_CameraManager_CreateCaptureSession` 正常创建会话
- ✅ 测试 `OH_CaptureSession_BeginConfig` 正常开始配置
- ✅ 测试 `OH_CaptureSession_CommitConfig` 正常提交配置
- ✅ 测试 `OH_CaptureSession_Start` 正常开始会话
- ✅ 测试 `OH_CaptureSession_Stop` 正常停止会话

### 8.5 闪光灯 API 测试

- ✅ 测试 `OH_CaptureSession_HasFlash` 检测闪光灯
- ✅ 测试 `OH_CaptureSession_IsFlashModeSupported` 检查模式支持
- ✅ 测试 `OH_CaptureSession_SetFlashMode` 设置闪光灯模式
- ✅ 测试 `OH_CaptureSession_GetFlashMode` 获取闪光灯模式
- ✅ 测试所有闪光灯模式（0、1、2、3等）

### 8.6 变焦 API 测试

- ✅ 测试 `OH_CaptureSession_GetZoomRatioRange` 获取变焦范围
- ✅ 测试 `OH_CaptureSession_SetZoomRatio` 设置变焦值
- ✅ 测试 `OH_CaptureSession_GetZoomRatio` 获取当前变焦值
- ✅ 测试超出范围的变焦值（ERROR 测试）

## 九、参考文档

### 9.1 Zlib 官方文档

- **Zlib 官方文档**: https://zlib.net/manual.html
- **RFC 1950 (zlib format)**: https://www.rfc-editor.org/rfc/rfc1950
- **RFC 1951 (deflate format)**: https://www.rfc-editor.org/rfc/rfc1951
- **RFC 1952 (gzip format)**: https://www.rfc-editor.org/rfc1952

### 9.2 OpenHarmony 文档

- **Camera C API 参考**: `{OH_ROOT}/docs/zh-cn/application-dev/reference/native-lib/camera/`（待创建）
- **Camera Kit API 参考**: `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-camera-kit`
- **Camera 开发指南**: `{OH_ROOT}/docs/zh-cn/application-dev/media/camera`

### 9.3 历史测试用例参考

- **参考测试套**: `{OH_ROOT}/test/xts/acts/multimedia/camera/camera_ndk_test/`
- **N-API 封装**: `entry/src/main/cpp/camera_manager.cpp`
- **ETS 测试**: `entry/src/ohosTest/ets/test/*.test.ets`

### 9.4 N-API 开发指南

- **N-API 官方文档**: `{OH_ROOT}/docs/zh-cn/application-dev/napi`
- **NDK 开发指南**: `{OH_ROOT}/docs/zh-cn/application-dev/napi`

## 十、测试用例命名规范

### 10.1 测试用例编号格式

```
SUB_MULTIMEDIA_CAMERA_[API名称]_[类型]_[序号]
```

### 10.2 编号示例

```
SUB_MULTIMEDIA_CAMERA_GetCameraManager_PARAM_001
SUB_MULTIMEDIA_CAMERA_CreateCameraInput_PARAM_001
SUB_MULTIMEDIA_CAMERA_CreatePreviewOutput_PARAM_001
SUB_MULTIMEDIA_CAMERA_CreateCaptureSession_PARAM_001
SUB_MULTIMEDIA_CAMERA_BeginCaptureSessionConfig_PARAM_001
SUB_MULTIMEDIA_CAMERA_StartCaptureSession_PARAM_001
SUB_MULTIMEDIA_CAMERA_HasFlash_PARAM_001
SUB_MULTIMEDIA_CAMERA_SetFlashMode_PARAM_001
SUB_MULTIMEDIA_CAMERA_GetZoomRatioRange_PARAM_001
```

### 10.3 ETS 测试用例名称

```
格式：[API名]_[场景描述]
示例：GetCameraManager、CreateCameraInput、DeletePreviewOutput、CreateCaptureSession
```

---

**版本**: 1.0.0
**创建日期**: 2026-03-24
**兼容性**: OpenHarmony API 11+
**系统能力**: `SystemCapability.Multimedia.Camera.Core`
**基于测试用例**: ActsCameraFrameWorkNdkTest (N-API 封装）
