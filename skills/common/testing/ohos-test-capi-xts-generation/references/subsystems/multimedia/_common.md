# Multimedia 子系统 CAPI 配置

## 一、子系统基础信息

- **子系统名称**: Multimedia
- **子系统描述**: 多媒体子系统，包含相机、音频、视频、图像、媒体库、音视频会话、DRM等多个Kit
- **API 语言**: C（通过 N-API 封装供 ETS/ArkTS 测试）
- **测试路径**: `test/xts/acts/multimedia/`

## 二、测试方式说明

### 2.1 测试架构

Multimedia 子系统支持两种测试方式：

#### 方式1：Native C 测试（用于标准系统）
- 使用 gtest/HWTEST_F 测试框架
- 直接测试 C 函数
- 适用于：标准系统的 C 接口测试
- 参考用例：`{OH_ROOT}/test/xts/acts/multimedia/*/`

#### 方式2：N-API 封装测试（用于标准系统）
- 将 C 函数封装为 N-API (napi_value、napi_env) 接口
- 封装函数返回 `napi_value` 类型供 ETS/ArkTS 测试调用
- 适用于：标准系统的跨语言集成测试
- 参考用例：`{OH_ROOT}/test/xts/acts/multimedia/camera/camera_ndk_test/entry/src/main/cpp/`

### 2.2 N-API 测试特点

- **封装目的**：将 C API 封装为 JS/ArkTS 可调用接口
- **调用方式**：ETS/ArkTS 测试调用封装后的 N-API 函数
- **测试分层**：
  - N-API 封装层（C++）测试 N-API 接口正确性
  - ETS/ArkTS 测试层（.ets）测试业务逻辑
- **优势**：支持跨语言测试，模拟实际使用场景

## 三、Kit 概览

Multimedia 子系统包含以下 Kit：

| Kit | 说明 | 头文件路径 | 文档路径 | 系统能力 |
|-----|------|-----------|---------|---------|
| **Audio** | 音频播放、录音、音频流管理 | `audio_framework/` | `apis-audio-kit` | SystemCapability.Multimedia.Audio.* |
| **AVCodec** | 音视频编解码器 | `av_codec/` | `apis-avcodec-kit` | SystemCapability.Multimedia.AVCodec.* |
| **AVSession** | 音视频会话管理 | `av_session/` | `apis-avsession-kit` | SystemCapability.Multimedia.AVSession.* |
| **Camera** | 相机设备管理、拍照、录像 | `camera_framework/` | `apis-camera-kit` | SystemCapability.Multimedia.Camera.* |
| **DRM** | 数字版权管理 | `drm_framework/` | `apis-drm-kit` | SystemCapability.Multimedia.Drm.* |
| **Image** | 图像处理、图像效果 | `image_framework/`, `image_effect/` | `apis-image-kit` | SystemCapability.Multimedia.Image.* |
| **Media** | 媒体播放器、媒体基础 | `media_foundation/`, `player_framework/` | `apis-media-kit` | SystemCapability.Multimedia.Media.* |
| **Media Library** | 媒体库、照片访问 | `media_library/` | `apis-media-library-kit` | SystemCapability.Multimedia.MediaLibrary.* |
| **MIDI** | MIDI 音频处理 | `midi_framework/` | - | SystemCapability.Multimedia.Audio.* |

## 四、头文件路径

### 4.1 Audio Kit

```c
#include "native_audio_manager.h"
#include "native_audiorenderer.h"
#include "native_audiocapturer.h"
#include "native_audio_stream_manager.h"
#include "native_audio_common.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/audio_framework/
├── audio_manager/
│   ├── native_audio_manager.h
│   ├── native_audio_stream_manager.h
│   ├── native_audio_session_manager.h
│   └── ...
├── audio_renderer/
│   └── native_audiorenderer.h
├── audio_capturer/
│   └── native_audiocapturer.h
└── common/
    ├── native_audio_common.h
    └── ...
```

### 4.2 AVCodec Kit

```c
#include "native_avcodec_audiodecoder.h"
#include "native_avcodec_audioencoder.h"
#include "native_avcodec_videodecoder.h"
#include "native_avcodec_videoencoder.h"
#include "native_avdemuxer.h"
#include "native_avmuxer.h"
#include "native_avsource.h"
#include "native_avcapability.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/av_codec/
├── native_avcodec_audiodecoder.h
├── native_avcodec_audioencoder.h
├── native_avcodec_videodecoder.h
├── native_avcodec_videoencoder.h
├── native_avdemuxer.h
├── native_avmuxer.h
├── native_avsource.h
├── native_avcapability.h
└── ...
```

### 4.3 AVSession Kit

```c
#include "native_avsession.h"
#include "native_avsession_base.h"
#include "native_avmetadata.h"
#include "native_avqueueitem.h"
#include "native_avplaybackstate.h"
#include "native_avcastcontroller.h"
#include "native_deviceinfo.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/av_session/
├── native_avsession.h
├── native_avsession_base.h
├── native_avmetadata.h
├── native_avqueueitem.h
├── native_avplaybackstate.h
├── native_avcastcontroller.h
├── native_deviceinfo.h
└── ...
```

### 4.4 Camera Kit

**Include 方式**：Camera CAPI 头文件必须使用 `<ohcamera/xxx.h>` 格式。

```cpp
// 正确方式 ✅
#include <ohcamera/camera.h>
#include <ohcamera/camera_manager.h>
#include <ohcamera/camera_input.h>
#include <ohcamera/camera_device.h>
#include <ohcamera/capture_session.h>
#include <ohcamera/preview_output.h>
#include <ohcamera/photo_output.h>
#include <ohcamera/photo_native.h>
#include <ohcamera/video_output.h>
#include <ohcamera/metadata_output.h>

// 错误方式 ❌（会导致编译错误：file not found）
#include "camera.h"
#include "camera_manager.h"
```

**详细配置**：参见 [camera/_common.md](./camera/_common.md)

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/camera_framework/
├── camera.h
├── camera_manager.h
├── camera_input.h
├── camera_device.h
├── capture_session.h
├── preview_output.h
├── photo_output.h
├── photo_native.h
├── video_output.h
├── metadata_output.h
└── ...
```

### 4.5 DRM Kit

```c
#include "native_drm_framework.h"
#include "native_drm_session.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/drm_framework/
└── ...
```

### 4.6 Image Kit

```c
#include "native_image.h"
#include "native_pixelmap.h"
#include "native_image_packer.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/image_framework/
├── native_image.h
├── native_pixelmap.h
├── native_image_packer.h
└── ...

{OH_ROOT}/interface/sdk_c/multimedia/image_effect/
└── ...
```

### 4.7 Media Kit

```c
#include "native_avplayer.h"
#include "native_avrecorder.h"
#include "native_screen_capture.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/media_foundation/
└── ...

{OH_ROOT}/interface/sdk_c/multimedia/player_framework/
├── native_avplayer.h
├── native_avrecorder.h
├── native_screen_capture.h
└── ...
```

### 4.8 Media Library Kit

```c
#include "media_asset_capi.h"
#include "media_asset_manager_capi.h"
#include "media_access_helper_capi.h"
#include "media_asset_base_capi.h"
```

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/media_library/
├── media_asset_capi.h
├── media_asset_manager_capi.h
├── media_access_helper_capi.h
├── media_asset_base_capi.h
└── ...
```

### 4.9 MIDI Kit

**位置（相对于 {OH_ROOT}/interface/sdk_c）**：
```
{OH_ROOT}/interface/sdk_c/multimedia/midi_framework/
└── ...
```

## 五、测试路径

### 5.1 Audio 测试路径

```
test/xts/acts/multimedia/audio/
test/xts/acts/multimedia/audio_ndk/
```

### 5.2 AVCodec 测试路径

```
test/xts/acts/multimedia/av_codec/
test/xts/acts/multimedia/avcodec/
test/xts/acts/multimedia/avcodeNDK20/
```

### 5.3 AVSession 测试路径

```
test/xts/acts/multimedia/avsession/
```

### 5.4 Camera 测试路径

```
test/xts/acts/multimedia/camera/
```

### 5.5 DRM 测试路径

```
test/xts/acts/multimedia/drm/
```

### 5.6 Image 测试路径

```
test/xts/acts/multimedia/image/
test/xts/acts/multimedia/image_effect/
```

### 5.7 Media 测试路径

```
test/xts/acts/multimedia/media/
```

### 5.8 Media Library 测试路径

```
test/xts/acts/multimedia/photoAccess/
```

## 六、参考文档

### 6.1 API 参考文档

| Kit | 文档路径 |
|-----|---------|
| Audio | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-audio-kit` |
| AVCodec | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-avcodec-kit` |
| AVSession | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-avsession-kit` |
| Camera | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-camera-kit` |
| DRM | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-drm-kit` |
| Image | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-image-kit` |
| Media | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-media-kit` |
| Media Library | `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-media-library-kit` |

### 6.2 开发指南

| Kit | 文档路径 |
|-----|---------|
| Audio | `{OH_ROOT}/docs/zh-cn/application-dev/media/audio` |
| AVCodec | `{OH_ROOT}/docs/zh-cn/application-dev/media/avcodec` |
| AVSession | `{OH_ROOT}/docs/zh-cn/application-dev/media/avsession` |
| Camera | `{OH_ROOT}/docs/zh-cn/application-dev/media/camera` |
| Image | `{OH_ROOT}/docs/zh-cn/application-dev/media/image` |
| Media | `{OH_ROOT}/docs/zh-cn/application-dev/media/video` |

## 七、模块配置说明

本配置文件包含 Multimedia 子系统的所有 Kit 配置，每个 Kit 有独立的目录和 _common.md 配置文件。

### 支持的模块目录

```
references/subsystems/multimedia/
├── _common.md                    # Multimedia 子系统通用配置（本文件）
├── camera/                       # Camera Kit 配置（已完成）
│   └── _common.md
├── audio/                        # Audio Kit 配置（待添加）
│   └── _common.md
├── avcodec/                      # AVCodec Kit 配置（待添加）
│   └── _common.md
├── avsession/                    # AVSession Kit 配置（待添加）
│   └── _common.md
├── drm/                         # DRM Kit 配置（待添加）
│   └── _common.md
├── image/                        # Image Kit 配置（待添加）
│   └── _common.md
├── media/                        # Media Kit 配置（待添加）
│   └── _common.md
└── media_library/                # Media Library Kit 配置（待添加）
    └── _common.md
```

### 配置优先级

```
用户自定义配置 > Kit 配置 > 子系统配置 > 核心配置
```

---

**版本**: 1.0.1
**创建日期**: 2026-03-24
**更新日期**: 2026-03-24
**兼容性**: OpenHarmony API 11+
**参考文档**:
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-audio-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-avcodec-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-avsession-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-camera-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-drm-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-image-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-media-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-media-library-kit`
- `{OH_ROOT}/docs/zh-cn/application-dev/media/audio`
- `{OH_ROOT}/docs/zh-cn/application-dev/media/avcodec`
- `{OH_ROOT}/docs/zh-cn/application-dev/media/avsession`
- `{OH_ROOT}/docs/zh-cn/application-dev/media/camera`
- `{OH_ROOT}/docs/zh-cn/application-dev/media/image`
- `{OH_ROOT}/docs/zh-cn/application-dev/media/video`
