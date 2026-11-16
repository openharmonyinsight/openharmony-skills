# Task 级评审（风险分级）

每个 Task 的验证通过之后、标记 Done 之前执行本指南。它定义风险分级、固定评审席位、
证据格式与门禁。整变更评审仍由配置的 `pre_commit_reviews` 交接执行，Task 评审不替代它，
也不重复派发整变更 reviewer。

协调者使用 `odk-task-review` skill 执行本门禁；该 skill 提供角色指南、候选发现复核和
定向修复复审。本指南继续作为风险、席位、证据与门禁的唯一契约来源。

## 风险等级

| 等级 | 适用 | 评审方式 | 证据 |
|------|------|----------|------|
| R0 | 仅文档、翻译、注释，或无法被任何测试/运行路径执行的配置 | 不派评审者；在 `Actual Result` 记 `Task review: 不适用（R0：<理由>）` | 无 |
| R1 | 单模块代码或测试文件，不命中任何 R2 触发项 | 1 名评审者一次完成五维检查 | `verdict.md` |
| R2 | 命中任一 R2 触发项 | 固定 3 名评审者 | `arch.md`、`scope.md`、`security.md`、`verdict.md` |

R2 触发项（命中任一即 R2）：

- 公共声明或接口：`.d.ts`、`.h`、`interfaces/inner_api/`、`interfaces/kits/`
- 跨仓调用；IPC/Binder；序列化/持久化；共享内存/socket
- 权限、认证、授权、敏感数据、加解密
- 并发、锁、异步、回调、生命周期
- 公共宏、编译开关、`BUILD.gn` 或构建清单
- 资源、国际化
- native ↔ ArkTS 边界（NAPI/CAPI/JSI）
- 公共常量、错误码

## 风险从哪来

`odk-plan` 为每个 Task 写入初始 `风险等级` 与判断依据。执行阶段只允许升级：实际 diff
命中新的 R2 触发项时，把 `风险升级 R1→R2（触发文件：<path>）` 追加到该 Task 的
`Actual Result`，把 Task 列表的 `风险等级` 单元格更新为 `R2`，并按 R2 评审。降级必须写明理由并经协调者确认，同时保留原判断记录。
R0 只允许用于确实无法执行的文档/配置；代码变更不得降为 R0。

## 评审席位与五维分工

R2 使用固定三席，不得增加席位：

| 席位 | 负责维度 | 主要检查 |
|------|----------|----------|
| arch | ①重复造轮子、②性能 | 仓内既有实现/工具函数；启动路径与热路径、循环内分配/复制、增长输入、复杂度 |
| scope | ③漏改分支、④外部接口影响 | 计划文件是否全部落地；正常/异常/清理/兼容分支；inner API、JS/C API、宏、错误码、跨仓调用方 |
| security | ⑤安全与攻击面 | 信任边界、输入校验、权限/认证、敏感数据与日志、IPC 入口、竞态 |

R1 由 1 名评审者按同一五维检查表完成，只写 `verdict.md`。

评审者规则：

- 只读：不得修改源码、计划或契约；发现问题只报告。
- 不得再派评审者；固定席位由协调者一次派出。
- 先看代码和原始证据，再看作者结论；作者说明只是待验证的主张。
- 用 `templates/review/task-arch.md`、`task-scope.md`、`task-security.md` 作为检查表，
  最终汇入 `templates/review/task-verdict.md`。

## 能力探测与串行降级

协调者在派发前运行能力探测。安装态执行：

```bash
python3 <executables>/lib/odk_host_capabilities.py --host <claude|codex|opencode> [--version <host-version>]
```

源码检出时 `<executables>` 为 `scripts`，安装态为 `runtime/executables`。把当前宿主名
显式传给 `--host`；无法确定时省略，让环境探测决定。宿主版本已知时一并传入
`--version`，供 opencode 选择 1.x/2.x 派发协议。

- `can_delegate: true`：按 `max_parallel`（固定 3）派发。宿主机制见下表。
- `can_delegate: false` 或探测失败：按 arch → scope → security 串行做三次只读检查，
  仍写同样的证据文件，并在 `verdict.md` 写 `independent: false`。
- `supports_nesting: false`：评审者不得再派子代理。
- opencode 的 `protocol` 为 `subagent`/`task` 时按对应协议派发；为 `confirm` 时先确认
  宿主实际暴露的工具与必填参数，再按对应协议派发。工具或必填参数不可用时不得强行
  派发，按串行降级并写 `independent: false`；仅后台能力不可用时改为同步派发，三席
  只读检查不变。

| 宿主 | 派发方式 |
|------|----------|
| claude | Agent/Task 工具：一条消息内发 3 个只读 agent；Agent Teams 仅在用户已启用时使用 |
| opencode 2.x | `subagent` 工具：3 次调用，`agent: "general"`；后台执行仅在宿主确认可用时加 `background: true` |
| opencode 1.x | `task` 工具：3 次调用，必填 `subagent_type: "general"`；后台执行需 `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true`，未设置时同步派发 |
| codex | 配置好的 subagent/agent 线程：一次批量提交 3 份只读 brief；不可用时串行 |
| 无委派宿主 | 串行三次只读检查，`independent: false` |

评审 brief 只传路径与约束，不粘贴全文：Task 在 `execution-plan.md` 的章节位置、完整 diff
范围（含未提交/未跟踪文件）、`spec.md` 相关 AC、`design.md` 相关决策、验证证据路径、
本指南与对应角色模板路径。

## 证据布局

```text
evidence/reviews/task-<n>/
├── arch.md        # R2
├── scope.md       # R2
├── security.md    # R2
└── verdict.md     # R1/R2 必须有
```

`TASK-<n>` 对应目录 `task-<n>`（去掉 `TASK-` 前缀、序号小写）。`verdict.md` 必须含
frontmatter：`task_id`、`risk`、`independent`、`verdict`、`blocking_findings`。
`verdict` 取值 `PASS` / `FAIL` / `BLOCKED`；`blocking_findings` 为未闭环 Critical/High 数量。
frontmatter 缺失、无法解析或缺少闭合 `---` 时按评审结论无效处理：Draft 告警、归档失败。
五个必填字段只接受单行标量；非注释的缩进续行同样按无效 frontmatter 处理，不得截取首行放行。
顶层必须使用受支持的 `key: value` 映射语法；重复字段、顶层列表项或其他无法识别的顶层非注释行同样无效，不得忽略后继续判为 PASS。
首个顶层字段之前的非注释缩进内容同样无效；额外元数据的嵌套内容必须位于其顶层字段之后，注释和空行不建立父字段。

风险列只从唯一的 `## Task 列表` 章节读取。该章节重复，或章节内出现多张含 `TASK ID` 与
`风险等级` 的表格时，Draft 与归档阶段都失败；风险列存在但单元格为空、无法解析为
`R0`/`R1`/`R2` 时，Draft 阶段告警、归档阶段失败。单元格必须是唯一确定的等级，允许
带括号说明（如 `R2（公共接口）`）；`R1→R2`、`R0/R2`、`R0.5` 等歧义值按无法解析处理。
`TASK ID` 必须是精确的 `TASK-<n>`；单元格带附加文本或合并写法（如 `TASK-1（回调）`、
`TASK-1, TASK-2`）时同样 Draft 告警、归档失败。以上情况都不得跳过该 Task 的评审检查。

## 判定与门禁

- `Critical` / `High` 未闭环：`verdict: FAIL` 或 `BLOCKED`，Task 标记 `❌ Blocked`，
  不标记 Done，不启动下一 Task；按 `feedback.md` 回填受影响交付件并复验。
- `Medium` / `Low`：写入 findings 与建议，不阻塞。
- 无法从 diff 或证据验证的项：记「待确认」，不得记 Pass；只有与 High 风险点直接相关时
  才作为阻塞项。
- 评审修复后只复验受影响范围；旧证据不得用于已变化的输入。
- 全部通过才写 `verdict: PASS` 与 `blocking_findings: 0`，然后才能标记 Task Done。

## 与整变更评审的关系

Task verdict 是整变更评审的输入。`odk-review` 必须先核对每个 R1/R2 Task 的 verdict：
缺失、非 PASS 或 `blocking_findings > 0` 时不得给出整变更 PASS。Task 评审不检查跨 Task
接口一致性与最终集成，这些仍属于整变更评审。
