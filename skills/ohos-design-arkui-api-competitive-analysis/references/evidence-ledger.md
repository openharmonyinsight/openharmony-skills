# Evidence Ledger / 证据与断言台账

在开始各平台取证时建立 Fact Ledger，在形成比较结论前建立 Claim Ledger。台账可以保留在分析过程里，不要求作为独立文件交付，但正式报告必须保留其可追溯关系。

## Canonical enums

以下 token 是整个 Skill 的唯一 schema；其它文件只能引用，不得定义同义枚举：

- `Evidence type`: `API Reference`、`Guide`、`Sample`、`Source`、`Discovery`。
- `Fact status`: `confirmed`、`conflict`、`pending`。
- `Claim type`: `fact-comparison`、`inference`、`negative`、`advantage`。
- `Claim status`: `accepted`、`pending`、`rejected`。
- `Confidence`: `high`、`medium`、`low`。
- `Mapping type`: `direct`、`functional`、`composite`、`fallback`、`no-equivalent-found`。
- `Parity class`: `fully-equivalent`、`partially-equivalent`、`semantic-difference`、`composite`、`fallback`、`no-equivalent-found`。

分析推论只进入 Claim Ledger，不能作为 Source 或 Fact 的 Evidence type。

## Fact Ledger

每行只记录一个原子事实：

| 字段 | 说明 |
|---|---|
| Fact ID | `A-01`、`D-01`、`I-01`，分别表示 ArkUI/Android/iOS |
| Platform | ArkUI、Android、iOS |
| API/Symbol | 精确接口、类型或字段 |
| Atomic fact | 单一可验证事实，不使用比较级 |
| Version | `@since`、API Level、框架版本或 availability |
| Source ID | 对应来源表编号 |
| Evidence type | 必填；使用 Canonical enums 中的 `Evidence type` |
| Status | confirmed、conflict、pending |

示例：

```text
A-01 | ArkUI | List.cachedCount | cachedCount 配置列表项预加载数量 | API 7+ | S1 | API Reference | confirmed
```

## Comparator Map

| Capability ID | ArkUI anchor | Android target | iOS target | Mapping type | Rationale |
|---|---|---|---|---|---|

`Mapping type` 只能使用 Canonical enums 中的对应 token。

报告中的中文显示与内部 token 使用以下唯一映射：

| Token | 报告标签 |
|---|---|
| `direct` | 直接等价 |
| `functional` | 功能等价 |
| `composite` | 组合实现 |
| `fallback` | 替代方案 |
| `no-equivalent-found` | 未找到等价能力 |

Comparator mapping 描述“用哪个 API 路径实现能力”；能力矩阵的 parity class 描述“比较结果”，两者不得混用。

对容易混淆的相似 API，在 `Rationale` 中记录排除理由。例如组件对标时，说明为什么排除层级、生命周期或用户能力不一致的同名控件。

## Claim Ledger

| 字段 | 说明 |
|---|---|
| Claim ID | `CL-01`、`CL-02`... |
| Claim | 报告中准备出现的比较断言 |
| Claim type | fact-comparison、inference、negative、advantage |
| Supporting facts | 一个或多个 Fact ID |
| Sources | 一个或多个 Source ID |
| Bidirectional search | required/done/not-applicable |
| Confidence | high、medium、low |
| Status | accepted、pending、rejected |

只有 `accepted` 断言可以进入“关键差异”和“结论”。`pending` 只能进入“待核事项”。

## 证据强度

| 等级 | 证据 | 可支持内容 |
|---|---|---|
| E1 | 官方 API Reference / 公共接口定义 | 签名、字段、availability、明确行为 |
| E2 | 官方 Guide | 分发、生命周期、使用约束 |
| E3 | 官方 Sample | 推荐用法和组合方式 |
| E4 | AOSP、AndroidX、Swift SDK 等平台源码 | 实现佐证，不单独支持公共契约或 availability |
| E5 | 博客、聚合文档等社区资料 | 仅帮助定位官方入口，不支持确定性结论 |

高置信度断言通常需要 E1，行为类结论可由 E1+E2 支撑。性能优越性不能只凭 API 形态推断；没有官方数据或实测时改写为“API 模型差异”或标 `待核`。

## 双向检索协议

对 negative 或 advantage 断言执行：

1. 在目标平台 API Reference 检索对应符号和同义能力。
2. 在目标平台 Guide 检索相关行为。
3. 检索功能等价、组合实现和替代方案。
4. 在另一平台验证比较锚点确实存在且处于同一作用域。
5. 记录检索词、版本、入口和结果。

若只能证明“未找到”，使用“在当前版本官方资料中未找到直接等价能力”，不要写“平台不支持”。

## 冲突处理

- 不静默选择其中一个来源。
- 优先核对版本、框架层级、废弃状态和文档更新时间。
- 无法消解时将相关 Fact 标记 `conflict`，对应 Claim 标记 `pending`。
- 在报告“待核事项”中列出冲突来源和需要补充的验证。

## 引用覆盖门禁

- 规格表中的关键字段至少关联一个 Fact ID 或 Source ID。
- 能力矩阵每行至少关联支撑该行结论的来源。
- 关键差异、影响和建议分别引用，不能只在附录列出一组宽泛来源。
- 一个来源可以支撑多条事实，但一条断言必须指出具体使用了哪些事实。
- 快速扫描和极短回答也必须保留 Fact ID、Claim ID 与 Source ID；可以减少条目数量，不能删除 ID 关系。
- 输出中引用的每个 Capability、Fact、Claim 和 Source ID 必须在同一输出中有对应定义；不要引用仅存在于内部草稿的编号。
