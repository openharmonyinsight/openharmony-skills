# 阶段 5 · summary — 归档总结

**前置**：已完成 verify（test-only：测试通过；optimization：测试通过 + MAP 改善达标或用户接受）。

**约定路径**：

- 提案文档：`xts_test/proposals/<proposal-id>/`
- 验证结果：`xts_test/reports/verify_result.md`
- 实现报告：`xts_test/reports/implementation_report.md`
- 目标代码仓：经 `ohos-ci-lite-deploy-burn/config.json` 配置的连接方式
- 经验文件：`xts_test/lessons.md`（追加式，跨多次验证累积）

## 执行步骤

### 1. 归档提案与产物

将本轮验证的所有产物整理归档：

```
xts_test/
├── archive/<timestamp>_<proposal-id>/     # 本轮归档
│   ├── proposals/                         # 提案文档副本
│   ├── reports/                           # 基线 + 验证结果 + 实现报告
│   └── maps/                              # 基线 MAP + 最终 MAP (.map 文件)
├── reports/                               # 始终保留最新
├── proposals/                             # 当前活跃提案
└── lessons.md                             # 累积经验
```

归档内容：
- `proposal.md` + `design.md` + `specs.md` + `tasks.md`
- `baseline_map.md` + `verify_result.md` + `implementation_report.md`
- 基线 .map 文件 + 最终 .map 文件

**test-only 模式**：无提案，归档目录名用 `<timestamp>_test_only`，归档内容为测试报告（`verify_result.md`）+ MAP 文件（如有），跳过提案类文件。

### 2. 目标代码仓提交

**test-only 模式**：本 skill 未改动代码，跳过目标代码仓提交（用户的代码变动由其自行管理），直接进入步骤 3。

通过配置的连接方式进入目标代码仓，执行 git 操作：

**commit 信息约束**（强制格式）：

```
<type>(<scope>): <subject>

<body>
Proposal: <proposal-id>
RAM: <baseline> -> <final> (<delta>)
Flash: <baseline> -> <final> (<delta>)
Test: <strategy> <result>
</body>
```

**type 取值**：

| type | 使用场景 |
|------|---------|
| `feat` | 新增功能 / 新模块适配 |
| `fix` | 修复 bug / 修复回归 |
| `perf` | 性能优化（RAM/ROM/速度） |
| `refactor` | 重构（不改行为） |
| `chore` | 构建/工具链/配置变更 |

**scope**：写模块名，如 `hi3861/wifi`、`stm32/gpio`、`kernel/sched`

**示例**：
```
perf(hi3861/hilog): trim unused log levels to reduce RAM

Proposal: opt-20260701-hilog
RAM: 312KB -> 287KB (-25KB, -8.0%)
Flash: 1840KB -> 1790KB (-50KB, -2.7%)
Test: XTS acts: 142 pass, 0 fail
```

提交前向用户展示 commit message 草稿确认。

**推送策略**：
- 默认只 `commit`，不 `push`
- 询问用户是否需要 `push`（以及 push 到哪个 remote/branch）

### 3. 沉淀经验

追加写入 `xts_test/lessons.md`（**test-only 模式**：模板中"优化/验证手法"记测试手法（测试策略/烧录配置等），"数据记录"只记测试结果，无优化 delta）：

**每次追加的内容**：

```markdown
## <date> — <proposal-id> — <一句话概括>

### 优化/验证手法
- <手法1>: <实际收益>
- <手法2>: <实际收益>

### 流程备忘
- <遇到的坑及解决方案>
- <可改进的流程节点>

### 数据记录
- 基线: RAM xxxKB / Flash xxxKB
- 优化后: RAM xxxKB / Flash xxxKB
- 测试: <策略> <结果>
```

**若发现本 skill 本身可改进**，在此记录改进建议（下次迭代时落实）。

### 4. 更新基线（可选）

若用户希望以本次结果作为新一轮优化的基线：
- 将 `verify_result.md` 中的最终 MAP 数据复制为新的 `baseline_map.md`
- 标注基线日期和来源 proposal

### 5. 阶段收尾

确认清单：
- [ ] 本轮产物已归档（optimization：`archive/<timestamp>_<proposal-id>/`；test-only：`archive/<timestamp>_test_only/`）
- [ ] 目标代码仓改动已 commit（仅 optimization 模式；message 符合约束格式）
- [ ] `lessons.md` 已追加本次经验
- [ ] 用户已确认 commit message（仅 optimization；test-only 无代码提交，标 N/A）

回显本轮验证完整摘要（optimization：基线→优化后 delta + 测试结果 + commit hash；test-only：测试结果 + 通过率，MAP/commit hash 不适用标 N/A），
宣告本轮验证工作流完成。提示用户可开启新一轮（explore 针对新模块/新目标）。
