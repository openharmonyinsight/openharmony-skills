## 资源索引

资源优先级约定：
- `P0`：官方推荐文档路径（优先加载，作为主方案）。
- `P1`：基于官方 API 的工程模板或场景化落实清单（用于加速落地，不替代 `P0`）。

## 三块主线结构（折展适配）

> 当前模块的折展适配按三块主线组织：`悬停适配`、`折痕避让`、`开合连续性`。

| 主线 | 主资源（P0） | 关键验收点 |
| --- | --- | --- |
| 悬停适配 | `RSC_FOLD_03` | 上半屏展示、下半屏交互，职责分工稳定 |
| 折痕避让 | `RSC_FOLD_05` | 分区边界对齐真实折痕，内容安全间距满足 `16/40 vp` |
| 开合连续性 | `RSC_FOLD_17` | 无步骤增加；滚动/输入/清晰度/播放连续 |

#### `RSC_FOLD_01` 折叠状态检测参考

```yaml
resource_id: RSC_FOLD_01
resource_type: reference
path: ./references/fold_status_detection.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义折叠态、展开态、半折叠态
  - 设计状态切换后的刷新入口
load_when:
  - 命中 FOLD-01 或 FOLD-04
avoid_when:
  - 当前不涉及状态识别
supports_scenes:
  - FOLD-01
  - FOLD-04
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - root_cause_hypothesis
  - verification_matrix
```

#### `RSC_FOLD_02` 状态监听实现资产

```yaml
resource_id: RSC_FOLD_02
resource_type: asset
path: ./assets/FoldableStatusExample.ets
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 工程落地时的状态监听接线样例
  - 配套主路径：RSC_FOLD_01（状态检测官方基线）
load_when:
  - 已按 RSC_FOLD_01 完成官方方案选型后，需要工程模板加速落地
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-01
  - FOLD-04
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - pass_criteria
```

#### `RSC_FOLD_03` 悬停态交互参考

```yaml
resource_id: RSC_FOLD_03
resource_type: reference
path: ./references/hover_state_interaction.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义悬停态上下分屏职责
  - 设计方向锁定和退出恢复策略
load_when:
  - 命中 FOLD-02 或 FOLD-05
avoid_when:
  - 当前不涉及悬停态
supports_scenes:
  - FOLD-02
  - FOLD-05
output_fields:
  - device_constraints
  - acceptance_focus
  - implementation_notes
  - fix_plan
  - verification_matrix
```

#### `RSC_FOLD_04` 悬停态布局资产

```yaml
resource_id: RSC_FOLD_04
resource_type: asset
path: ./assets/HoverStateInteractionExample.ets
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 工程落地时的悬停分屏样例
  - 配套主路径：RSC_FOLD_03（FolderStack / FoldSplitContainer 官方路径）
load_when:
  - 已按 RSC_FOLD_03 确认容器策略后，需要页面级模板快速接入
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-02
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - regression_watchlist
  - pass_criteria
```

#### `RSC_FOLD_05` 折痕避让参考

```yaml
resource_id: RSC_FOLD_05
resource_type: reference
path: ./references/crease_avoidance.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义折痕区域获取和避让原则
  - 设计折痕重算时机
  - 修复“避让区偏下/偏上、分界线不在中线”的定位问题
  - 区分“分区边界定位”和“内容安全间距（16/40 vp）”
load_when:
  - 命中 FOLD-03
  - 出现折痕分界线整体偏移或不同机型落点不一致
avoid_when:
  - 当前与折痕无关
supports_scenes:
  - FOLD-03
  - FOLD-06
output_fields:
  - device_constraints
  - acceptance_focus
  - implementation_notes
  - root_cause_hypothesis
  - verification_matrix
  - pass_criteria
```

#### `RSC_FOLD_06` 折痕避让实现资产

```yaml
resource_id: RSC_FOLD_06
resource_type: asset
path: ./assets/CreaseAvoidance.ets
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 工程落地时的折痕避让模板样例
  - 配套主路径：RSC_FOLD_05（真实折痕几何 + 坐标映射）
  - 提供“边界锚定（top/bottom 或 left/right）+ 内容安全间距”的代码落点
load_when:
  - 已按 RSC_FOLD_05 完成折痕映射方案后，需要快速拼接页面结构
  - 已确认偏移根因为坐标系混用或中线偏移策略错误，需要快速修复
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-03
  - FOLD-06
output_fields:
  - code_touchpoints
  - implementation_notes
  - fix_plan
  - evidence_requirements
```

#### `RSC_FOLD_07` 多段折叠形态状态参考

```yaml
resource_id: RSC_FOLD_07
resource_type: reference
path: ./references/multi_fold_states.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义多段折叠形态映射差异（可抽象为 F/M/G 等）
  - 明确大可视区形态下的方向和结构差异
load_when:
  - 命中 FOLD-04
avoid_when:
  - 当前设备不存在多形态映射需求
supports_scenes:
  - FOLD-04
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - pass_criteria
```

#### `RSC_FOLD_08` 特殊比例折叠屏适配参考

```yaml
resource_id: RSC_FOLD_08
resource_type: reference
path: ./references/special_form_factor_foldable_adaptation.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义内外屏比例显著差异场景下的布局差异（如 1:1 外屏、16:10 内屏）
  - 提供特殊比例折叠屏的窗口模式和设备规格基线
load_when:
  - 命中 FOLD-05
avoid_when:
  - 当前设备不是宽折叠
supports_scenes:
  - FOLD-05
output_fields:
  - device_constraints
  - capability_boundary
  - reuse_resources
  - implementation_notes
  - verification_matrix
```

#### `RSC_FOLD_09` 特殊比例折叠屏断点观察器资产

```yaml
resource_id: RSC_FOLD_09
resource_type: asset
path: ./assets/foldable_form_factor_assets/BreakpointObserverExample.ets
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 特殊比例折叠屏工程示例：断点观察器接线
  - 配套主路径：RSC_FOLD_08（特殊比例折叠屏官方基线）
load_when:
  - 已按 RSC_FOLD_08 确定策略后，需要代码模板落地
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-05
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - pass_criteria
```

#### `RSC_FOLD_10` 特殊比例折叠屏响应式布局资产

```yaml
resource_id: RSC_FOLD_10
resource_type: asset
path: ./assets/foldable_form_factor_assets/ResponsiveLayoutExample.ets
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 特殊比例折叠屏工程示例：内外屏布局切换
  - 配套主路径：RSC_FOLD_08（特殊比例折叠屏官方基线）
load_when:
  - 已按 RSC_FOLD_08 完成布局策略后，需要代码模板落地
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-05
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - regression_watchlist
  - pass_criteria
```

#### `RSC_FOLD_11` 特殊比例折叠屏窗口变化监听资产

```yaml
resource_id: RSC_FOLD_11
resource_type: asset
path: ./assets/foldable_form_factor_assets/WindowSizeChangeExample.ets
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 特殊比例折叠屏工程示例：窗口变化监听
  - 配套主路径：RSC_FOLD_08（特殊比例折叠屏官方基线）
load_when:
  - 已按 RSC_FOLD_08 确定窗口策略后，需要代码模板落地
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-05
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - evidence_requirements
  - pass_criteria
```

#### `RSC_FOLD_12` 特殊比例折叠屏模块配置资产

```yaml
resource_id: RSC_FOLD_12
resource_type: asset
path: ./assets/foldable_form_factor_assets/foldable_module_config.json5
phase_tags: [REQ, DEV, FIX]
priority: P1
used_for:
  - 特殊比例折叠屏工程配置样例
  - 配套主路径：RSC_FOLD_08（特殊比例折叠屏官方基线）
load_when:
  - 已按 RSC_FOLD_08 完成前置条件核对后，需要配置模板
avoid_when:
  - 当前尚未完成对应 P0 主路径设计
supports_scenes:
  - FOLD-05
output_fields:
  - device_constraints
  - capability_boundary
  - code_touchpoints
  - fix_plan
```

#### `RSC_FOLD_13` 折展问题修复场景库

```yaml
resource_id: RSC_FOLD_13
resource_type: reference
path: ./references/bug-fix-cases.md
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 统一沉淀问题修复场景的结构化模板（问题描述、根因分析、通用修复方案）
  - 为 FOLD-06 提供通用修复路径，不依赖页面类型或业务案例
load_when:
  - 命中 FOLD-06
  - 需要快速定位折展问题的通用根因与修复动作
avoid_when:
  - 当前任务是新页面从零设计
supports_scenes:
  - FOLD-06
output_fields:
  - problem_profile
  - root_cause_hypothesis
  - implementation_notes
  - fix_plan
  - regression_watchlist
  - verification_matrix
```

#### `RSC_FOLD_16` 折展适配三块主线总览

```yaml
resource_id: RSC_FOLD_16
resource_type: reference
path: ./references/fold_adaptation_four_blocks.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 统一折展适配结构为三块主线
  - 作为需求评审和问题分流的主入口
load_when:
  - 涉及折叠屏适配范围定义
  - 需要按主线组织输出结构
avoid_when:
  - 当前任务不是折叠屏折展适配
supports_scenes:
  - FOLD-02
  - FOLD-03
  - FOLD-07
output_fields:
  - primary_scene
  - secondary_scenes
  - acceptance_focus
  - verification_matrix
```

#### `RSC_FOLD_17` 开合连续性参考

```yaml
resource_id: RSC_FOLD_17
resource_type: reference
path: ./references/fold_continuity.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 对齐官方 4.1 开合连续性标准
  - 约束滚动、输入、图像与播放状态在折展后的连续性
  - 强制拆分验证悬停链路(y->z->y)与单屏链路(y->p->y)，避免单路径漏检
load_when:
  - 命中 FOLD-07
  - 问题表现为步骤增加、滚动偏移、输入丢失、图片模糊或进度漂移
avoid_when:
  - 当前不涉及折展连续性风险
supports_scenes:
  - FOLD-07
output_fields:
  - acceptance_focus
  - root_cause_hypothesis
  - fix_plan
  - verification_matrix
  - gate_cases
```
