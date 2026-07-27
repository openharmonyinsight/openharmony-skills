---
name: component
applies_to:
  - "**/components_ng/**/*.ets"
  - "**/components_ng/**/*.cpp"
  - "**/components_ng/**/*.h"
---

# ArkUI Component Sub-profile

适用于 NG 组件 pattern、组件交互、组件状态机和组件属性开发。

## Define 追加要求

`proposal.md` 必须确认：

- 组件名称、组件类别和主要源码目录
- 涉及 Pattern / Model / Layout / Paint / Event / Accessibility 的哪些层
- 用户可见行为和不涉及项
- 是否影响现有 DSL、ArkTS API、C API 或默认样式
- 是否涉及多设备形态、焦点、手势、键鼠、无障碍

## Specify / Design 追加要求

`design.md` 与 `spec.md` 必须对齐以下内容：

- Pattern / Model / Property / Layout / Paint 的对象边界
- 状态流转、生命周期入口和事件链路
- 属性更新是否触发布局、绘制或语义树更新
- 兼容性：现有组件 API、默认行为和边界条件是否变化
- 验证映射：每条 AC 至少对应一个组件 unittest 或明确的人工验证项
- 若组件行为可通过 Host Preview Inspector 观测，必须优先映射到 SpecTest case；不适用时写明 N/A 理由
- 若涉及组件属性（尺寸、位置、对齐、flex、显示优先级等），长期 `specs` 与 SpecTest feature/suite/case 必须建立可追溯关系

## Plan / Post-Plan 自闭环

每个 Task 必须记录具体组件测试目标；不能只写全量 unittest 兜底命令。

### Unittest 编译

具体模块 unittest：

```bash
./build.sh --product-name rk3568 --ccache --build-target //foundation/arkui/ace_engine/test/unittest/core/pattern:<target_name>
```

### 编译目标推导规则

1. 定位 Task 涉及的组件目录，如 `test/unittest/core/pattern/<component>/`
2. 读取该目录下 `BUILD.gn` 中的 `ace_unittest("<target_name>")` 获取编译目标名
3. 拼装完整编译目标：`//foundation/arkui/ace_engine/test/unittest/core/pattern/<component>:<target_name>`
4. 若组件目录下没有 BUILD.gn 或目标不存在，逐级向上查找父目录 BUILD.gn 中的 group 目标

### 测试文件约定

- 测试文件位置：`test/unittest/core/pattern/<component>/`
- 测试文件命名：`<component>_<aspect>_test_ng.cpp`
- 测试注册：在组件目录 `BUILD.gn` 的 `sources` 列表中添加新测试文件
- BUILD.gn 模式：`ace_unittest("<target>") { module_name = "..."; type = "new"; sources = [...] }`

### SpecTest Host Preview

组件属性或交互最终能反映为节点树、布局矩形、节点属性或稳定 Inspector 输出时，必须补充 SpecTest 验证：

```bash
cd examples/SpecTest
./tools/host_preview/run_feature.sh --case-id <case-id>
./tools/host_preview/run_feature.sh --suite-id <suite-id>
```

完成条件：

1. 新增/修改的 case 已同步 `suite.manifest.json`、`expected/expected.json` 和 `main_pages.json`
2. affected case / suite 执行结果 `failed_cases=0`
3. `summary_report.md`、case `report.md`、`previewer.log` 和 Inspector 响应路径写入 Task Card 或 `review.md`
4. 无法用 Inspector 断言的组件行为必须转入组件 unittest、人工交互回归或设备最小矩阵

## 最终交付追加要求

- 交互组件必须完成真实交互回归或记录人工验证阻塞项
- 视觉相关组件必须完成布局 / 绘制 / 主题回归或记录不适用理由
- 涉及多形态时，发布 gate 必须记录设备形态验证范围
- SpecTest 适用项必须归档报告；裁剪执行时记录 suite/case 范围和理由
