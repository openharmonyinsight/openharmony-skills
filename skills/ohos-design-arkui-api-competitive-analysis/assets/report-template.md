# ArkUI API 竞品分析报告

## 快速扫描模式

仅在用户要求一页或极短输出时使用。先输出以下压缩 Analysis Brief，保证它是首个用户可见产物：

| 目标/目的 | 作用域/API 类别 | 版本基线 | 模式/排除项 |
|---|---|---|---|
| {{TARGET_AND_PURPOSE}} | {{SCOPE_AND_CATEGORY}} | {{PLATFORM_BASELINES}} | quick-scan；{{EXCLUSIONS}} |

若命中第 3 节条件产物，在 Analysis Brief 之后输出对应条件表，再输出以下最小审计表。完整报告删除“快速扫描模式”并使用后续章节。

| Comparator Map | 核心 Fact | Claim/结论 | 风险与待核 | Sources |
|---|---|---|---|---|
| `C-01`：ArkUI → Android/iOS；mapping type 与排除理由 | `A-01`/`D-01`/`I-01`：决定映射和风险的原子事实 | `CL-01`：fact-comparison 或 inference；置信度 | 已确认影响；`P-01` 待核项或“无” | `S1`/`S2`/`S3`：官方入口、版本、查询日期 |

表中出现的 ID 必须在单元格内完成定义，不能引用未展示的内部台账。默认重点维度可合并到核心 Fact，不要求复制完整报告的全部章节。

## 1. 分析契约

| 项目 | 内容 |
|---|---|
| 分析对象 | `{{ARKUI_TARGET}}` |
| 分析目的 | {{PURPOSE}} |
| 作用域层级 | {{SCOPE_TIER}} |
| API 类别 | {{CATEGORY}} |
| 报告模式 | {{MODE}} |
| 排除项 | {{EXCLUSIONS}} |

### 版本基线

| 平台 | 版本/分支 | 查询日期 |
|---|---|---|
| ArkUI | {{ARKUI_BASELINE}} | {{QUERY_DATE}} |
| Android | {{ANDROID_BASELINE}} | {{QUERY_DATE}} |
| iOS/iPadOS | {{IOS_BASELINE}} | {{QUERY_DATE}} |

## 2. 能力检查清单

| 能力 ID | 原子能力问题 | 适用维度 | 必查规格 | 状态与 Fact |
|---|---|---|---|---|
| C-01 | {{CAPABILITY_QUESTION}} | {{DIMENSIONS}} | {{REQUIRED_SPEC}} | confirmed/pending/not-applicable；{{FACT_IDS}} |

## 3. 条件必需产物

只保留当前任务命中的子节。未命中时删除对应子节；命中时不得删除或改到 Comparator Map 之后。

### 3.1 键盘快捷键 Path Check

键盘快捷键必须先完成本表，再输出 Comparator Map。触摸、手势等其它交互不要套用本表，改在 Fact Ledger 中记录其分发、命中、仲裁或 responder 事实。

| 平台 | 路径/API | 如何到达或发布 | 入口角色 | 有效作用域 | 状态 | Fact/Source |
|---|---|---|---|---|---|---|
| Android | {{ANDROID_PATH}} | {{ANDROID_DISPATCH_OR_PUBLICATION}} | {{ANDROID_ROLE}} | {{ANDROID_SCOPE}} | confirmed/pending/not-applicable | {{FACT_AND_SOURCE_IDS}} |
| iOS | {{IOS_PATH}} | {{IOS_RESPONDER_OR_COMMAND_CHAIN}} | {{IOS_ROLE}} | {{IOS_SCOPE}} | confirmed/pending/not-applicable | {{FACT_AND_SOURCE_IDS}} |

### 3.2 子类型闭环

| 子类型规格 | ArkUI | Android | iOS | 状态与 Fact |
|---|---|---|---|---|
| {{SUBTYPE_SPEC}} | {{ARKUI_STATUS}} | {{ANDROID_STATUS}} | {{IOS_STATUS}} | confirmed/pending/not-applicable；{{FACT_IDS}} |

### 3.3 List 条件矩阵

仅长列表/虚拟化集合保留。能力矩阵至少覆盖分组、多列、sticky、lazy、刷新、数据源、稳定身份、更新通知、复用、缓存、nested scrolling、大数据、选择/重排。

| 能力 | ArkUI | RecyclerView | Compose lazy list | UITableView | SwiftUI List |
|---|---|---|---|---|---|
| {{LIST_CAPABILITY}} | {{ARKUI_FACT}} | {{RECYCLERVIEW_FACT}} | {{COMPOSE_FACT}} | {{UITABLEVIEW_FACT}} | {{SWIFTUI_FACT}} |

| 框架 | 自动化定位/滚动/动作 | 无障碍检查 | 布局检查 | 性能诊断 | 状态与来源 |
|---|---|---|---|---|---|
| {{LIST_FRAMEWORK}} | {{TEST_PATH}} | {{A11Y_INSPECTION}} | {{LAYOUT_INSPECTION}} | {{PERFORMANCE_TOOLING}} | {{STATUS_AND_SOURCE_IDS}} |

### 3.4 动画条件矩阵

仅显式动画保留。不同 comparator API 不得合并单元格。

| Comparator API | duration/delay/defaults | curves/steps/spring/keyframe | completion/control/velocity | orchestration | availability/fallback | Fact/Source |
|---|---|---|---|---|---|---|
| {{ANIMATION_COMPARATOR}} | {{TIMING_SPEC}} | {{CURVE_SPEC}} | {{CONTROL_SPEC}} | {{ORCHESTRATION_SPEC}} | {{VERSION_AND_FALLBACK}} | {{FACT_AND_SOURCE_IDS}} |

## 4. 对标对象映射

| 能力 ID | ArkUI 锚点 | Android 目标与类型 | Android 选择/排除理由 | iOS 目标与类型 | iOS 选择/排除理由 |
|---|---|---|---|---|---|
| C-01 | {{ARKUI_ANCHOR}} | {{ANDROID_TARGET}}；{{ANDROID_MAPPING_TYPE}} | {{ANDROID_RATIONALE_AND_EXCLUSIONS}} | {{IOS_TARGET}}；{{IOS_MAPPING_TYPE}} | {{IOS_RATIONALE_AND_EXCLUSIONS}} |

映射类型内部 token 与显示标签固定为：`direct`（直接等价）、`functional`（功能等价）、`composite`（组合实现）、`fallback`（替代方案）、`no-equivalent-found`（未找到等价能力）。

## 5. Fact Ledger 与各平台规格事实

| Fact ID | 平台 | API/符号 | 原子事实 | 版本 | Source ID | 证据类型 | 状态 |
|---|---|---|---|---|---|---|---|
| A-01 | ArkUI | {{ARKUI_SYMBOL}} | {{ATOMIC_FACT}} | {{VERSION}} | S1 | API Reference | confirmed/pending/conflict |

### 5.1 ArkUI

- {{ARKUI_FACT}} [{{ARKUI_FACT_ID}}][{{SOURCE_ID}}]

```ts
{{ARKUI_USAGE_EXAMPLE}}
```

### 5.2 Android

- {{ANDROID_FACT}} [{{ANDROID_FACT_ID}}][{{SOURCE_ID}}]

```kotlin
{{ANDROID_USAGE_EXAMPLE}}
```

### 5.3 iOS

- {{IOS_FACT}} [{{IOS_FACT_ID}}][{{SOURCE_ID}}]

```swift
{{IOS_USAGE_EXAMPLE}}
```

## 6. Normalized Spec

| 能力 ID | ArkUI Fact | Android Fact | iOS Fact | 原始口径 | 归一化口径 |
|---|---|---|---|---|---|
| C-01 | {{ARKUI_FACT_IDS}} | {{ANDROID_FACT_IDS}} | {{IOS_FACT_IDS}} | {{ORIGINAL_SEMANTICS}} | {{NORMALIZED_SEMANTICS}} |

## 7. 能力差异矩阵

| 能力 | ArkUI | Android | iOS | 判定 | 证据 |
|---|---|---|---|---|---|
| {{CAPABILITY}} | {{ARKUI_SPEC}} | {{ANDROID_SPEC}} | {{IOS_SPEC}} | {{PARITY_CLASS}} | {{FACT_AND_SOURCE_IDS}} |

判定使用：`fully-equivalent`（完全等价）、`partially-equivalent`（部分等价）、`semantic-difference`（语义不同）、`composite`（组合实现）、`fallback`（替代方案）、`no-equivalent-found`（未找到等价能力）。

## 8. 关键差异与影响

### {{CLAIM_ID}} {{FINDING_TITLE}}

- **事实差异**：{{FACTUAL_DIFFERENCE}} [{{FACT_IDS}}][{{SOURCE_IDS}}]
- **分析推论**：{{INFERENCE}}
- **影响**：{{IMPACT}}
- **置信度**：{{CONFIDENCE}}

## 9. 建议

| ID | 问题 | 证据 | 影响 | 推荐动作 | 优先级 | 置信度 |
|---|---|---|---|---|---|---|
| R-01 | {{PROBLEM}} | {{CLAIM_OR_FACT_IDS}} | {{IMPACT}} | {{ACTION}} | P0/P1/P2 | high/medium/low |

## 10. 迁移映射

| 来源平台能力 | ArkUI 对应方式 | 适配工作 | 风险 |
|---|---|---|---|
| {{SOURCE_CAPABILITY}} | {{ARKUI_MAPPING}} | {{ADAPTATION}} | {{RISK}} |

## 11. Version / Fallback Matrix

动画或存在版本替代路径的任务必须保留；其它任务可按需要保留。

| 能力/API | 引入版本 | 废弃/替代 | 低版本 fallback | 状态与来源 |
|---|---|---|---|---|
| {{VERSIONED_CAPABILITY}} | {{INTRODUCED}} | {{DEPRECATED_OR_REPLACEMENT}} | {{LOWER_VERSION_FALLBACK_OR_NONE}} | {{STATUS_AND_SOURCE_IDS}} |

## 12. Conflict Log

| Conflict ID | 涉及事实 | Source A | Source B | 可能原因 | 处理状态 |
|---|---|---|---|---|---|
| CF-01 | {{CONFLICTED_FACT}} | {{SOURCE_A}} | {{SOURCE_B}} | {{POSSIBLE_CAUSE}} | resolved/pending |

没有资料冲突时写“无”。

## 13. 待核事项

| ID | 未确认内容 | 原因/冲突 | 已检查来源 | 下一步 |
|---|---|---|---|---|
| P-01 | {{PENDING_ITEM}} | {{REASON}} | {{CHECKED_SOURCES}} | {{NEXT_ACTION}} |

没有待核事项时写“无”。不要删除本节。

## 14. 来源

`Evidence type` 只使用 `evidence-ledger.md` 的 Canonical enums；分析推论不得作为来源类型。

| Source ID | 平台 | API/符号 | 证据类型 | 来源 | 版本/availability | 查询日期 | 章节 |
|---|---|---|---|---|---|---|---|
| S1 | {{PLATFORM}} | {{SYMBOL}} | {{EVIDENCE_TYPE}} | {{URL_OR_PATH}} | {{VERSION}} | {{QUERY_DATE}} | {{SECTION}} |

## 15. 断言审计摘要

| Claim ID | 断言类型 | 支撑事实 | 来源 | 双向检索 | 置信度 | 状态 |
|---|---|---|---|---|---|---|
| CL-01 | {{CLAIM_TYPE}} | {{FACT_IDS}} | {{SOURCE_IDS}} | {{SEARCH_STATUS}} | {{CONFIDENCE}} | accepted/pending/rejected |
