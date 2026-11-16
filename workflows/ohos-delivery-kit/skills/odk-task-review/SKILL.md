---
name: odk-task-review
description: "Use when reviewing one implemented ODK Task before Done, or re-reviewing its fixes. Routes arch/scope/security across five dimensions and produces the existing Task verdict. Zero plugin dependencies."
license: MIT
---

# ODK Task Review

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

## 入口与边界

协调者在一个 Task 验证完成后、标记 Done 前调用；显式请求修复复审也使用此入口。
这不授予修改源码、执行设备操作、提交 PR 或扩展任务范围的权限。
整变更与跨 Task 集成仍交给 `odk-review`。

协调者先加载 `using-odk`，复用已完成的资源检查；从同一安装定位契约、模板和执行目录。
已加载则不重复启动路由。被委派的评审者直接复用 brief 的绝对资源路径，不启动阶段流程。

<!-- ODK:reference contracts/skill-guides/delivery/task-review.md -->
Read `contracts/skill-guides/delivery/task-review.md` for risk triggers, fixed
seats, host dispatch, evidence paths and the completion gate. It is authoritative;
this skill supplies the review procedure without changing the archive contract.
<!-- /ODK:reference -->

默认进入协调模式。被委派且 brief 明确指定 `role: arch|scope|security|all` 时，
只执行“评审者模式”，不得再派 agent，也不得接管协调流程。

## Steps

以下步骤由协调者执行；被委派的 reviewer 直接进入评审者模式。

### 1. 固定评审输入

读取 Task 的计划条目、相关 AC、设计约束和现有验证证据。对照实际 diff 重新确认
`R0/R1/R2`；升级时按契约同时更新 Task 列表的风险单元格和 Actual Result，保留依据。
`R0` 只记录带理由的不适用结论，不派 reviewer。

为 R1/R2 准备一份三席共用的 brief，传路径、定位和约束，避免粘贴整份文档：

| 字段 | 内容 |
|------|------|
| Task 与风险 | Task ID；计划绝对路径及章节；实际风险与触发文件 |
| 代码范围 | 仓库绝对路径；Task 开始前的基线提交；当前 HEAD；完整变更文件清单 |
| 当前快照 | 基线到当前的完整 patch 路径；未跟踪文件及内容摘要；快照标识 |
| 契约 | spec 的相关 AC 定位；design 的相关决策定位（不要求有效交付级别之外的文档） |
| 验证 | 命令、结果及原始日志路径；无法验证的环境限制 |
| 角色与输出 | role；本 skill 路径；对应模板；既有发现及复审范围（仅复审时） |

基线应覆盖整个 Task，不能默认为 `HEAD~1`。可用 `git diff --binary <task-base> --`
核对已提交、暂存和未暂存的最终内容；另用 `git ls-files --others --exclude-standard`
核对未跟踪文件。先看全仓文件清单，再按 Task 范围分配，避免路径过滤漏掉改动。
多仓分别记录基线。基线无法恢复或混入其他 Task 无法分离时，记录缺口并 BLOCKED。

快照标识包含基线/HEAD、patch 与未跟踪文件内容摘要，不能只用 HEAD；把标识及文件清单
位置填入报告元数据。协调者保持这些输入不变，等评审结束才交给实现者修复。
结束前重新核对输入；代码、AC、设计约束或验证输入发生变化时，旧结论不覆盖新输入。
证据报告自身的写入不算代码变化。

### 2. 按风险派发

使用资源检查已定位的 `<executables>`，运行契约中的
`python3 <executables>/lib/odk_host_capabilities.py --host <host>`（版本已知则带上版本）。
探测结果还须与当前实际工具及权限一致；探测成功不等于 agent 已成功派出。

| 风险 | 有可用委派能力 | 无可用委派能力 / 派发失败 |
|------|----------------|--------------------------|
| R1 | 一名只读 reviewer，`role: all`，一次覆盖五维 | 协调者按 arch → scope → security 做三次只读检查 |
| R2 | 固定三名只读 reviewer：arch、scope、security | 协调者按相同顺序串行三次检查，保留三份报告 |

只有实际由独立 reviewer 完成对应检查才写 `independent: true`；串行自审或混合降级均为
`independent: false`。独立指与实现者分离，不要求三席同时运行。不增加第四个整变更
reviewer，不让评审者递归派发；使用新上下文，只给同一份 brief，不传实现者的推理历史
或其他席结论。协调者统一落盘，reviewer 返回报告内容，避免并发改写共享发现。

| role | 维度 | 按需读取的角色指南 | 报告模板 |
|------|------|--------------------|----------|
| arch | ①重复造轮子、②性能 | [arch](references/arch.md) | `templates/review/task-arch.md` |
| scope | ③漏改/完整性、④外部接口影响 | [scope](references/scope.md) | `templates/review/task-scope.md` |
| security | ⑤安全/攻击面 | [security](references/security.md) | `templates/review/task-security.md` |
| all | 五维 | 上述三份指南 | `templates/review/task-verdict.md` |

### 3. 复核并汇总

按 [发现复核与修复复审](references/findings-and-rereview.md) 处理候选发现。
协调者核对位置、触发条件、影响与反证，按根因去重，保留稳定 ID；不能以票数或作者认同
代替验证。需要专业补查时回到现有对应席位，不另建一组 reviewer。

R2 把三份返回内容写入 `evidence/reviews/task-<n>/arch.md`、`scope.md`、`security.md`；
R1 将单席五维检查与发现写入 verdict，不要求额外三份报告。
协调者用 `templates/review/task-verdict.md` 生成 `evidence/reviews/task-<n>/verdict.md`，
保留单行 frontmatter：`task_id`、`risk`、`independent`、`verdict`、`blocking_findings`。

未闭环 Critical/High 为 FAIL；High 风险点因证据缺失无法判定为 BLOCKED，计入阻塞数。
Task 标记 `❌ Blocked`，按反馈程序回填，不能标记 Done 或启动下一 Task。
Medium/Low 为建议；无 High 关联的待确认项可不阻塞，但该维度仍写“待确认”，不能伪装 Pass。
只有必需检查完成、快照有效且无阻塞项时才写 `verdict: PASS`、`blocking_findings: 0`。
skill 不自动标记 Done，由调用的实现流程在验证与门禁都通过后执行。

### 4. 修复后复审

实现者在原授权范围内修复后，收集受影响验证结果。向原席位传旧发现 ID、上一快照、
修复 diff 和新输入；按复审指南核对旧发现与修复引入的回归。变更触及新维度时让相应
现有席位补查；独立 agent 不可用则如实降级。更新原报告，保留处置与复验记录。
自动修复/复审最多三轮，已有轮次计入；到上限仍有阻塞或缺少外部事实时保持 BLOCKED，
报告尚缺的决策或证据，等待用户继续指示。上限不会将未解决问题转为 PASS。

## 评审者模式

先确认 brief 的 role 与快照，读取对应角色指南和模板。直接检查 diff、相关实现、调用方
及原始验证记录，再核对作者结论。只读范围可沿具体调用链扩展，记录查过的范围和缺口。
不修改源码、计划或报告文件，不派 agent；如需验证，仅用隔离的临时副本及不产生外部
副作用的检查。缺失设备、跨仓代码或可达性证据时，返回缺少的事实，不虚构执行结果。

每个负责维度给出 Pass / Fail / 待确认或有理由的不适用，并按
[发现协议](references/findings-and-rereview.md) 返回可复核候选项。报告只保留代码事实、
判断依据、风险和验证结论，不写模型逐步思考、作者填写提示或实现过程自述。
`role: all` 用 verdict 的五维表返回评估，最终 YAML 与门禁由协调者核定。

## Output

用不超过 15 行报告 verdict 路径、风险、实际独立性、五维结论、阻塞数及未验证限制。
不自动提交 PR 或触发整变更 review。
设计取舍与上游参考见 [参考来源](references/sources.md)，仅维护本 skill 时读取；运行时无需联网。
