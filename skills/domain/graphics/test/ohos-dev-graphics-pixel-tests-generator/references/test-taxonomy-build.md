# 测试分类和 BUILD.gn

## 顶层测试区域

当前 `graphic_test/test` 包含：

| 目录 | 典型内容 |
| --- | --- |
| `rs_display_effect` | 节点属性、内容节点、动画视觉行为 |
| `rs_effect_feature` | 新 effect/filter/shader/mask/shape 渲染特性 |
| `open_capability` | PixelMap、font、symbol 等开放 API |
| `rs_func_feature` | capture、多屏、水印、render group、无障碍等 RenderService 功能场景 |
| `rs_perform_feature` | 脏区、HWC、GPU composer、hybrid render、性能敏感渲染 |
| `rs_framework` | 框架和 surface 行为 |
| `effect_kit` | OH/native effect kit filter 测试 |
| `drawing_engine`、`hardware_manager`、`test_template` | 较小的 demo/template 区域；使用前先查看现有内容 |

优先扩展已有相关文件。只有当功能足够独立、追加会让旧文件明显混乱时，才新增文件。

## 类型选择

当前语料中的常见映射：

- `CONTENT_DISPLAY_TEST`：大多数节点外观、surface、capture、脏区、PixelMap/open-capability 和功能测试。
- `ANIMATION_TEST`：`rs_display_effect/animation`。
- `EFFECT_TEST`：`rs_effect_feature` 和 `effect_kit`。
- `GPU_COMPOSER_TEST`：GPU composer 性能特性文件。
- `HYBRID_RENDER_TEST`：hybrid render 性能特性文件。

如果某个目录已有同类测试，优先复制该目录/文件使用的类型，不要只凭目录名猜。

## Source List 规则

普通 graphic test 由 `graphic_test/test/BUILD.gn` 中现有的 `ohos_unittest("RSGraphicTest")` 构建。

普通生成测试不要新增 `ohos_unittest` target。

新增 `.cpp` 时，把相对路径插入以下数组之一：

- `drawing_engine_sources`
- `hardware_manager_sources`
- `open_capability_sources`
- `rs_display_effect_sources`
- `rs_effect_feature_sources`
- `rs_framework_sources`
- `rs_func_feature_sources`
- `rs_perform_feature_sources`
- `effect_kit_sources`

示例：

```gn
rs_display_effect_sources = [
  "rs_display_effect/property_display/background_color_test.cpp",
  "rs_display_effect/property_display/new_property_test.cpp",
]
```

保持被编辑数组的本地格式。有些列表使用两个空格缩进，不要重排整个文件。

## Include 和依赖

`RSGraphicTest` target 已经有较完整依赖。新增 `.cpp` 只 include 实际使用的头文件。

常见 include：

```cpp
#include "rs_graphic_test.h"
#include "rs_graphic_test_img.h"
#include "rs_graphic_test_text.h"
#include "rs_graphic_test_utils.h"
#include "transaction/rs_interfaces.h"
#include "ui/rs_canvas_node.h"
#include "ui/rs_surface_node.h"
#include "display_manager.h"
#include "pixel_map.h"
#include "image_source.h"
```

使用 `SetUpNodeBgImage`、`DecodePixelMap`、`ImageCustomModifier` 时 include `rs_graphic_test_img.h`。
使用 `WriteToPngWithPixelMap` 时 include `rs_graphic_test_utils.h`。
直接 display screenshot 时 include `display_manager.h`。
使用 `RSTransactionProxy` 时 include `transaction/rs_interfaces.h`。

## 命名风格

现有文件命名混合较多，但生成测试应稳定且可搜索：

- 文件：小写 feature 名，结尾 `_test.cpp`。
- Fixture：`FeatureNameTest`。
- Test name：扩展已有文件时沿用本地风格；新文件可用 `Feature_Property_Case_Test`，如果目录使用全大写功能名也可跟随。
- 注释块：相邻测试有 `@tc.name`、`@tc.desc`、`@tc.type` 时也要补齐。部分旧 property 文件使用单行注释，编辑时跟随本地文件。
