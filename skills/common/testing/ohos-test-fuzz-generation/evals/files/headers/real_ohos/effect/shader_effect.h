/*
 * Copyright (c) 2021-2025 Huawei Device Co., Ltd.
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

#ifndef SHADER_EFFECT_H
#define SHADER_EFFECT_H

#include "impl_interface/shader_effect_impl.h"
#include "utils/drawing_macros.h"
#include "utils/extend_object.h"
#include "draw/sdf_shaper_base.h"

#ifdef ROSEN_OHOS
#include <parcel.h>
#endif

namespace OHOS {
namespace Rosen {
namespace Drawing {
enum class TileMode {
    CLAMP,
    REPEAT,
    MIRROR,
    DECAL,
};

class DRAWING_API ShaderEffect {
public:
    enum class ShaderEffectType : int32_t {
        NO_TYPE,
        COLOR_SHADER,
        BLEND,
        IMAGE,
        PICTURE,
        LINEAR_GRADIENT,
        RADIAL_GRADIENT,
        CONICAL_GRADIENT,
        SWEEP_GRADIENT,
        LIGHT_UP,
        EXTEND_SHADER,
        SDF_SHADER,
        LAZY_SHADER
    };

    static std::shared_ptr<ShaderEffect> CreateColorShader(ColorQuad color);
    static std::shared_ptr<ShaderEffect> CreateColorSpaceShader(const Color4f& color,
        std::shared_ptr<ColorSpace> colorSpace);
    static std::shared_ptr<ShaderEffect> CreateBlendShader(ShaderEffect& dst, ShaderEffect& src, BlendMode mode);
    static std::shared_ptr<ShaderEffect> CreateImageShader(
        const Image& image, TileMode tileX, TileMode tileY, const SamplingOptions& sampling, const Matrix& matrix);
    static std::shared_ptr<ShaderEffect> CreatePictureShader(const Picture& picture, TileMode tileX, TileMode tileY,
        FilterMode mode, const Matrix& matrix, const Rect& rect);
    static std::shared_ptr<ShaderEffect> CreateLinearGradient(const Point& startPt, const Point& endPt,
        const std::vector<ColorQuad>& colors, const std::vector<scalar>& pos, TileMode mode,
        const Matrix *matrix = nullptr);
    static std::shared_ptr<ShaderEffect> CreateRadialGradient(const Point& centerPt, scalar radius,
        const std::vector<ColorQuad>& colors, const std::vector<scalar>& pos, TileMode mode,
        const Matrix *matrix = nullptr);
    static std::shared_ptr<ShaderEffect> CreateTwoPointConical(const Point& startPt, scalar startRadius,
        const Point& endPt, scalar endRadius, const std::vector<ColorQuad>& colors, const std::vector<scalar>& pos,
        TileMode mode, const Matrix *matrix = nullptr);
    static std::shared_ptr<ShaderEffect> CreateSweepGradient(const Point& centerPt,
        const std::vector<ColorQuad>& colors, const std::vector<scalar>& pos, TileMode mode, scalar startAngle,
        scalar endAngle, const Matrix* matrix = nullptr);
    static std::shared_ptr<ShaderEffect> CreateLightUp(const float& lightUpDeg, ShaderEffect& imageShader);
    static std::shared_ptr<ShaderEffect> CreateExtendShader(std::shared_ptr<ExtendObject>);
    static std::shared_ptr<ShaderEffect> CreateSdfShader(const SDFShapeBase& shape);

    virtual ~ShaderEffect() = default;
    ShaderEffectType GetType() const;
    virtual bool IsLazy() const { return false; };

#ifdef ROSEN_OHOS
    virtual bool Marshalling(Parcel& parcel);
    static std::shared_ptr<ShaderEffect> Unmarshalling(Parcel& parcel, bool& isValid);
#endif

    virtual DrawingType GetDrawingType() const { return DrawingType::COMMON; }

    template<typename T>
    T* GetImpl() const { return impl_->DowncastingTo<T>(); }

    ShaderEffect(ShaderEffectType t, ColorQuad color) noexcept;
    ShaderEffect(ShaderEffectType t, const Color4f& color, std::shared_ptr<ColorSpace> colorSpace) noexcept;
    ShaderEffect(ShaderEffectType t, ShaderEffect& dst, ShaderEffect& src, BlendMode mode) noexcept;
    ShaderEffect(ShaderEffectType t, const Image& image, TileMode tileX, TileMode tileY,
        const SamplingOptions& sampling, const Matrix& matrix) noexcept;
    ShaderEffect(ShaderEffectType t, const Picture& picture, TileMode tileX, TileMode tileY, FilterMode mode,
        const Matrix& matrix, const Rect& rect) noexcept;
    ShaderEffect(ShaderEffectType t, const Point& startPt, const Point& endPt, const std::vector<ColorQuad>& colors,
        const std::vector<scalar>& pos, TileMode mode, const Matrix *matrix = nullptr) noexcept;
    ShaderEffect(ShaderEffectType t, const Point& centerPt, scalar radius, const std::vector<ColorQuad>& colors,
        const std::vector<scalar>& pos, TileMode mode, const Matrix *matrix = nullptr) noexcept;
    ShaderEffect(ShaderEffectType t, const Point& startPt, scalar startRadius, const Point& endPt, scalar endRadius,
        const std::vector<ColorQuad>& colors, const std::vector<scalar>& pos, TileMode mode,
        const Matrix *matrix = nullptr) noexcept;
    ShaderEffect(ShaderEffectType t, const Point& centerPt, const std::vector<ColorQuad>& colors,
        const std::vector<scalar>& pos, TileMode mode, scalar startAngle, scalar endAngle,
        const Matrix *matrix = nullptr) noexcept;
    ShaderEffect(ShaderEffectType t, const float& lightUpDeg, ShaderEffect& imageShader) noexcept;
    ShaderEffect(ShaderEffectType t, std::shared_ptr<ExtendObject> object) noexcept;
    ShaderEffect(ShaderEffectType t) noexcept;
    ShaderEffect(ShaderEffectType t, const SDFShapeBase& shape) noexcept;
    ShaderEffect() noexcept;

    std::shared_ptr<ExtendObject> GetExtendObject() { return object_; }

    virtual std::shared_ptr<Data> Serialize() const;
    virtual bool Deserialize(std::shared_ptr<Data> data);
protected:
    ShaderEffectType type_;
private:
    std::shared_ptr<ShaderEffectImpl> impl_;
    std::shared_ptr<ExtendObject> object_;
};
} // namespace Drawing
} // namespace Rosen
} // namespace OHOS
#endif
