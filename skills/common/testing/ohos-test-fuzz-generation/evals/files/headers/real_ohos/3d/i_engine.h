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

#ifndef OHOS_RENDER_3D_I_ENGINE_H
#define OHOS_RENDER_3D_I_ENGINE_H

#include <cstdint>
#include <string>
#include <memory>

#include <EGL/egl.h>
#include <GLES/gl.h>

#include "custom/custom_render_descriptor.h"
#include "custom/shader_input_buffer.h"
#include "data_type/constants.h"
#include "data_type/geometry/cube.h"
#include "data_type/geometry/cone.h"
#include "data_type/geometry/sphere.h"
#include "data_type/gltf_animation.h"
#include "data_type/light.h"
#include "data_type/position.h"
#include "data_type/pointer_event.h"
#include "data_type/quaternion.h"
#include "data_type/vec3.h"
#include "platform_data.h"
#include "texture_info.h"

namespace OHOS::Render3D {
class IEngine {
public:
    virtual ~IEngine() = default;
    virtual void Clone(IEngine* proto) = 0;
    virtual bool LoadEngineLib() = 0;
    virtual bool InitEngine(EGLContext eglContext, const PlatformData& data) = 0;
    virtual void DeInitEngine() = 0;
    virtual void UnloadEngineLib() = 0;

    virtual void InitializeScene(uint32_t key) = 0;
    virtual void SetupCameraViewPort(uint32_t width, uint32_t height) = 0;
    virtual void SetupCameraTransform(const OHOS::Render3D::Position& position, const OHOS::Render3D::Vec3& lookAt,
        const OHOS::Render3D::Vec3& up, const OHOS::Render3D::Quaternion& rotation) = 0;
    virtual void SetupCameraViewProjection(float zNear, float zFar, float fovDegrees) = 0;

    virtual void LoadSceneModel(const std::string& modelPath) = 0;
    virtual void LoadEnvModel(const std::string& modelPath, BackgroundType type) = 0;
    virtual void UnloadSceneModel() = 0;
    virtual void UnloadEnvModel() = 0;

    virtual void OnTouchEvent(const PointerEvent& event) = 0;
    virtual void OnWindowChange(const TextureInfo& textureInfo) = 0;

    virtual void DrawFrame() = 0;

    virtual void UpdateGeometries(const std::vector<std::shared_ptr<Geometry>>& shapes) = 0;
    virtual void UpdateGLTFAnimations(const std::vector<std::shared_ptr<GLTFAnimation>>& animations) = 0;
    virtual void UpdateLights(const std::vector<std::shared_ptr<OHOS::Render3D::Light>>& lights) = 0;
    virtual void UpdateCustomRender(const std::shared_ptr<CustomRenderDescriptor>& customRender) = 0;
    virtual void UpdateShaderPath(const std::string& shaderPath) = 0;
    virtual void UpdateImageTexturePaths(const std::vector<std::string>& imageTextures) = 0;
    virtual void UpdateShaderInputBuffer(
        const std::shared_ptr<OHOS::Render3D::ShaderInputBuffer>& shaderInputBuffer) = 0;

    virtual bool NeedsRepaint() = 0;

#if defined(MULTI_ECS_UPDATE_AT_ONCE) && (MULTI_ECS_UPDATE_AT_ONCE == 1)
    virtual void DeferDraw() = 0 ;
    virtual void DrawMultiEcs(const std::unordered_map<void*, void*>& ecss) = 0;
#endif
};
} // namespace OHOS::Render3D
#endif // OHOS_RENDER_3D_I_ENGINE_H
