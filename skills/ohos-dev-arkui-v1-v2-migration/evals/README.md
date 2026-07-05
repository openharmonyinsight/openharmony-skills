# V1→V2 Migration Skill Evals

`evals.json` 是基准测试的种子集（seed set）。设计原则与覆盖约定如下。

## 设计哲学：从工作流优势出发，不从真实工程出发

case **不从大真实工程挖掘**（真实工程太大、无法进 skill 仓库，且耦合多、断言难定位）。
而是用**极小的合成 fixture**，把 skill 的每个**工作流决策**隔离出来测——这些决策正是 skill 相对通用知识的真正增量。

skill 目前的两个核心优势，对应两类工作流 case：

1. **迁移范围判定**（主动让用户选组件 + 独立/联合/桥接策略）
   - 情况二：用户没指定组件 → 先 scan、列清单、向用户确认，不直接改码
   - 联合迁移：目标组件在 `@Provide`/`@Consume` 耦合团里 → `mustMigrate` 不止自身 → 报告需联合迁
   - 独立迁移：目标组件是叶子（无 `@Provide`/`@Consume`/`@StorageLink`）→ `mustMigrate` 只含自身
2. **Storage key 追踪**（`stateApiByKey` + "保留 V1 API，所有 decoratorUsage 迁完才删"规则）
   - 共享 key：key 被多个组件用，迁移其中之一 → 新增 V2 等价、**保留** V1 调用
   - 私有 key：key 的所有 decoratorUsage 都在本次迁移范围 → V1 调用**可以**移除

## Fixture

`fixtures/scope-demo/` —— 一个极小合成工程（4 个组件 + 1 个 storage 生产者）：

| 文件 | 角色 | 用于 |
|---|---|---|
| `Root.ets` | `@Provide` pageStack/user + `@StorageLink('theme')` | 联合迁移 / 共享 key |
| `Profile.ets` | `@Consume` pageStack/user | 联合迁移判定（mustMigrate 含 Root） |
| `Settings.ets` | `@Consume` pageStack + `@StorageLink('theme')` | 共享 / 私有 key 判定 |
| `Badge.ets` | 仅 `@State`/`@Prop` | 独立迁移判定 |
| `store.ts` | `AppStorage.setOrCreate('theme')` | key 保留 / 移除判定 |
| `build-profile.json5` | `compatibleSdkVersion` | API 版本检测 |

fixture 已用 skill 自带脚本验证过解析正确性：
`scan-v1` → 4 组件 + theme 生产者；`dependency_tracer Profile` → mustMigrate=[Profile,Settings,Root]；`dependency_tracer Badge` → [Badge]。

## 覆盖约定（Minimum success criteria）

| eval | 类型 | 覆盖点 |
|---|---|---|
| 1–5 | mechanics（装饰器映射基线） | @State→@Local、@Prop→@Param、@Link→@Param+@Event、@Observed→@ObservedV2、LocalStorage、桥接 |
| 6 | workflow_scope | 情况二：未指定组件 → scan + 确认，不改码 |
| 7 | workflow_scope | 情况二：scan + 列出 4 组件 + 向用户确认 |
| 8 | workflow_scope | 联合迁移：Profile → mustMigrate 含 Root，不单独迁 |
| 9 | workflow_scope | 独立迁移：Badge → mustMigrate=[自身]，可独立迁 |
| 10 | workflow_storage_key | 共享 key：迁 Settings 时保留 theme 的 V1 调用（Root 仍在用） |
| 11 | workflow_storage_key | 私有 key：迁全部 consumer 后 theme 的 V1 调用可移除 |

最低标准：
- 至少 1 条 case 测"未指定组件 → 先 scan + 确认"。
- 至少 1 条 case 测"`@Provide`/`@Consume` 耦合团的联合迁移判定"。
- 至少 1 条 case 测"叶子组件的独立迁移判定"。
- 至少 1 条 case 测"共享 storage key 时保留 V1 调用"。
- 至少 1 条 case 测"所有 decoratorUsage 迁完后移除 V1 调用"。

## 断言性质说明

- **mechanics（1–5）** 的断言是结构性文本断言（"@State 替换为 @Local"），通用知识也能答对大半 → Delta 偏小，作基线。
- **workflow（6–11）** 的断言针对 skill 独有的工作流决策（scope 判定、key 追踪）→ 通用知识不会做，是真正的区分点。
- 凡可机器判定的断言，建议在评分时改用 skill 自带脚本作 oracle（见下）。

## 评分 oracle（可执行判定）

迁移类 skill 的优势：对错可由自带脚本判定，不必纯靠 LLM 读文本。建议的断言→脚本映射：

| 断言 | 可执行 oracle |
|---|---|
| "组件已迁到 V2" | `component_analyzer.py <out> --json` → `version == "V2"` |
| "无 V1/V2 装饰器混用" | `mixing_validator.py <proj> --json` → `violations` 中无 `WITHIN_COMPONENT_MIXING` |
| "混用校验无 violation" | `mixing_validator.py` → `summary.isCompliant == true` |
| "mustMigrate 判定正确" | `dependency_tracer.py <comp> <proj>` 的 `mustMigrate` 与回答一致 |

