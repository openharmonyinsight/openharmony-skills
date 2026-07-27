# ArkUI Sub-profiles

> 路径说明：本文的相对路径默认面向运行时布局（`{{ASSET_ROOT}}/profiles/arkui/`）。
> 在源目录中，ArkUI base profile 位于 `../profile.md`（即 `openharmony/profiles/arkui/profile.md`）。

## 读取规则

manifest 使用两个字段声明 profile：

- `manifest.profile`：主 profile 名称，不含斜杠（如 `arkui`）
- `manifest.subprofiles`：命中的子 profile 列表（block seq 格式，如 `- component` + `- capi`）

加载顺序：

1. 先读取 base profile `../profile.md`（所有 ArkUI 共享约束）
2. 再读取 `manifest.subprofiles` 中声明的子 profile 文件（如 `component.md`，模块差异部分）
3. 合并：子 profile 中的字段覆盖 base 中的同名字段，子 profile 新增的字段直接追加

当 `manifest.subprofiles` 为空或未声明时，只加载 base profile。

## 执行规则

所有 ArkUI 子 profile 都继承 base profile（`../profile.md`）中的 ArkUI-SDD 执行约束：

1. 流程实例写入 `.codespec/changes/*`。
2. `manifest.md` 记录 `func_id`、`feat_id`、`profile`、`subprofiles`、`lineage`、长期 `specs` 路径和 SpecTest 路径（如适用）。
3. Define 执行 `arkui-define-entry`（入口）+ `arkui-define-exit`（出口）：功能树、profile/lineage、影响面矩阵和 Host/SpecTest/设备验证分流；基线审批与信息来源记录。
4. Specify 执行 `arkui-specify-entry`（入口）+ `arkui-specify-exit`（出口）：存量归档与 FeatID 连续性、规格基线、API 双向核对和验证映射。
5. Design 执行 `arkui-design-entry`（入口）+ `arkui-design-exit`（出口）：`design.md` / `spec.md` 交叉一致、对象关系、渲染链路和设计约束。
6. Plan 执行 `arkui-plan`：Task 级 TDD 与 SpecTest Host Preview 闭环、长期归档迁移计划、设备最小矩阵与资产回灌路径。

子 profile 只补充模块差异，例如编译目标、测试位置、API 兼容规则和 SpecTest 适用性裁剪。

## 已提供子 profile

| 子 profile | manifest.subprofiles 值 | 适用场景 |
|-----------|--------------------------|---------|
| component | `component` | NG 组件 pattern 开发（Text、Button、List 等） |
| capi | `capi` | C API / NDK 接口开发 |
| sdk-api | `sdk-api` | ArkTS SDK API 开发（.d.ets / Modifier） |
| render | `render` | 渲染管线、布局算法、绘制管线开发 |

## Define 推断依据

AI 在 `proposal.md` 澄清阶段根据以下线索推断子 profile：

| 需求关键词 / 文件路径线索 | 子 profile |
|---|---|
| 组件、pattern、UI 行为、交互、`frameworks/core/components_ng/pattern/` | `component` |
| C API、NDK、`ArkUI_` 前缀接口、`frameworks/core/interfaces/native/`、`interfaces/native/` | `capi` |
| SDK API、`.d.ets`、`interface/sdk-js/api/arkui/`、Modifier | `sdk-api` |
| 渲染、绘制、GPU、`frameworks/core/render/`、`frameworks/core/components_ng/render/` | `render` |

### 推断不出时

子 profile 是逐步建设的，并非所有模块类型都有对应子 profile。如果需求涉及的文件路径或关键词无法匹配到任何已有子 profile，按以下顺序处理：

1. 根据需求描述和推断依据表匹配
2. 向用户确认主要涉及哪类开发：组件 / C API / SDK API / 渲染管线
3. 如果用户也无法确定，分析需求的 file scope 所在目录结构、BUILD.gn 模式、已有测试文件位置，给出编译验证路径建议
4. 将分析结果和建议写入 `proposal.md`，等待用户确认

确认后如果仍无合适子 profile，`manifest.profile` 只填 `arkui`（base），`manifest.subprofiles` 留空，并在 `execution-plan.md` / Task Card 中记录具体编译验证路径。如果某个模块类型反复出现，再新增对应子 profile。

## 多子 profile 场景

一个需求可能涉及多个子 profile（如同时开发组件和 C API）：

1. `manifest.profile` 填 `arkui`（base profile 不变）
2. `manifest.subprofiles` 记录全部命中的子 profile（block seq 格式，每项一行 `- <name>`）
3. `execution-plan.md` 按 Task 维度指定各 Task 的子 profile
4. 每个 Task 的自闭环检查使用其对应子 profile 的编译验证命令
5. Plan 出口要求所有涉及的子 profile 都有对应 Task 和证据
6. 若任一子 profile 命中 SpecTest 适用场景，必须补充 AC 到 SpecTest case 的映射；不适用时记录 N/A 理由

## 扩展

新增子 profile 时：

1. 在本目录下新建 `<name>.md`，只写与 base 的差异
2. 在本 README 的已提供表格中追加一行
3. 在推断依据表中追加路径线索
