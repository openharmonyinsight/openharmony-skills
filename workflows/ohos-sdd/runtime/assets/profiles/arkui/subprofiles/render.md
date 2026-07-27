---
name: render
applies_to:
  - "**/render/**"
  - "**/render_service/**"
---

# ArkUI Render Sub-profile

适用于渲染管线、布局算法、绘制管线等底层开发。

## Define 追加要求

`proposal.md` 必须确认：

- 变更命中 layout、paint、render context、drawing、GPU 或动画路径的哪一层
- 是否位于高频路径或帧内路径
- 性能预算、内存预算和目标设备范围
- 是否影响视觉输出、像素结果、帧率或内存峰值
- 是否需要截图、trace、benchmark 或人工视觉验证

## Specify / Design 追加要求

`design.md` 与 `spec.md` 必须对齐：

- 渲染对象、布局算法、绘制属性或 GPU 资源的所有权
- 触发布局 / 绘制 / 合成的条件
- Performance & Memory Budget：帧时间增量、内存峰值、缓存策略
- 视觉回归场景和截图/像素验证策略
- 验证映射：render unittest、benchmark、SpecTest、截图、trace 或人工验证项
- 若布局算法、render context 或绘制属性最终可通过 Inspector 的节点树、`$rect`、节点属性稳定观测，P0/P1 AC 必须映射到 SpecTest case；不适用时写明 N/A 理由
- 若验证目标是 GPU 合成、像素级输出、帧率、内存峰值或真实设备差异，必须声明 SpecTest 不覆盖的边界，并转入 benchmark、trace、截图/黄金图、人工视觉回归或设备矩阵

## Plan / Post-Plan 自闭环

### Unittest 编译

全部渲染测试：

```bash
./build.sh --product-name rk3568 --ccache --build-target //foundation/arkui/ace_engine/test/unittest/core/render:core_render_unittest
```

具体测试目标（`test/unittest/core/render/BUILD.gn` 中定义了多个 `ace_unittest`）：

- `painter_test` — 绘制器测试
- `render_context_test_ng` — 渲染上下文测试
- `render_property_test_ng` — 渲染属性测试
- `drawing_prop_convertor_test_ng` — 绘制属性转换测试

### 编译目标推导规则

1. 定位 Task 涉及的渲染模块目录，如 `test/unittest/core/render/`
2. 读取 `BUILD.gn` 中的 `group("core_render_unittest")` 获取整体编译目标
3. 或读取具体 `ace_unittest("<target>")` 获取单个测试目标
4. 完整路径：`//foundation/arkui/ace_engine/test/unittest/core/render:<target_name>`

### 测试文件约定

- 测试文件位置：`test/unittest/core/render/`
- 测试文件命名：`<aspect>_test_ng.cpp`
- 多个 `ace_unittest` 共存于同一 BUILD.gn，通过不同 `module_name` 区分

### SpecTest Host Preview

布局或可观测渲染行为满足以下任一条件时，必须补充 SpecTest 验证：

- 结果可表达为节点尺寸、位置、边界、显示状态或稳定 Inspector 属性
- 用例可通过 `operationSequence` 触发状态变化后再采集 Inspector
- 变更影响公共属性在真实 ArkTS 页面中的最终布局结果

执行命令：

```bash
cd examples/SpecTest
./tools/host_preview/run_feature.sh --case-id <case-id>
./tools/host_preview/run_feature.sh --suite-id <suite-id>
```

完成条件：

1. `spec.md` 的 AC 映射到 feature / suite / case / targetNodeId / expected
2. affected case / suite 执行结果 `failed_cases=0`
3. `summary_report.md`、case `report.md`、`previewer.log` 和 Inspector 响应路径写入 Task Card、`evidence/checks/` 或 `review.md`
4. SpecTest 不能覆盖的像素级、GPU、帧率或设备差异，必须补充 benchmark、trace、截图/黄金图、人工视觉回归或设备矩阵证据

## 最终交付追加要求

- 渲染管线变更必须有性能或内存验证证据；无法自动化时写入 `evidence/reviews/`
- 视觉输出变化必须有截图、像素、黄金图或人工视觉回归结论
- 命中 GPU / 合成路径时，必须评估帧率、内存峰值和设备形态影响
- SpecTest 适用项必须归档报告；裁剪执行时记录 suite/case 范围和理由
- SpecTest N/A 项必须在 `evidence/reviews/` 中关联替代证据，不能只写“不适用”
