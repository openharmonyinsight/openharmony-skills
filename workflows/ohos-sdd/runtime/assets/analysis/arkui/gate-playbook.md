# ArkUI Gate Playbook

本 playbook 承载 ArkUI gate 的细粒度执行规则。默认不要在 ArkUI profile 命中时全量读取；只有实际执行 gate、编写 `evidence/checks/*`、或 review gate 证据时才读取对应章节。

信息检索流程、上下文预算和读取停止条件见 `context-loading.md`。本文件只定义 gate 证据、Blocked 条件和阶段检查细则。

## Gate 记录通用规则

在 `evidence/checks/check-proposal.md`、`evidence/checks/check-spec.md` 和 `evidence/checks/check-design.md` 中，每条检查结果必须记录：

| 字段 | 要求 | 示例 |
|------|------|------|
| 证据/缺口 | 包含信息来源 + 源码核验结果 | `kb_search.py 手势 -> Gesture 知识库 -> 源码核对 gesture_recognizer.h:50 确认` |
| 确认来源 | 标注获取途径 | `kb_search.py -> <知识库名>` / `DeepWiki ace_engine` / `源码核对 <path>:<line>` / `Owner 对话确认` |

仅引用知识库、DeepWiki 或长期 spec，未经源码核验的结论不得标记为 `通过`；应写为 `待确认` 或 `Blocked`。

## Define Gate

### arkui-define-entry

Define 阶段采用双重确认：

- 证据确认：源码、知识库或现有 specs 只能证明事实依据，状态写为 `源码初步核对/待确认`。
- Owner 输入确认：FuncID、FeatID、`specs/index.md` 功能域注册信息、Profile/Lineage、影响范围、验证适用性和审批结论必须由需求 Owner 明确给出。

缺少 Owner 输入确认时，Define 总结论必须为 `Blocked`；不得创建 `spec.md`、`design.md` 或 `evidence/checks/check-spec.md` / `check-design.md`。

Owner 提问规则：

- Agent 可以先基于源码或目录准备候选选项供 Owner 选择，但不得把候选写入 `manifest.md`、`.codespec/registry.md`、`specs/index.md` 或 gate 结论字段。
- 每次只问一个问题；Owner 回答后，把原文或评审链接写入 `proposal.md` 讨论记录和 `evidence/checks/check-proposal.md` 的确认来源列。
- Owner 未回答时，字段必须保持 `TBD (pending requirement Owner)`，gate 结果为 `Blocked`。
- FuncID、FeatID、功能域各级名称、影响范围四类信息禁止由 Agent 代填或从历史路径自动编号。
- `specs/index.md` 的功能域/特性注册视为 Define 阶段 registry 写入的一部分；确认 FuncID 和 FeatID 后必须完成该索引注册。

必问/必检项：

- FuncID 是什么；未给出时记录 `TBD (pending requirement Owner)`。
- FeatID 是什么；未给出时记录 `TBD (pending requirement Owner)`，不得自动分配编号。
- `specs/index.md` 是否已注册该 FuncID 和 FeatID。
- 若 FuncID 已存在，必须在对应已注册特性清单中注册 FeatID、特性名称、Spec 文件和 Draft/Baselined 状态。
- 若 FuncID 不存在，必须先向 Owner 确认每一级功能域名称；目录英文 slug、说明和 `design.md` 链接可由 Agent 给出候选，但写入前必须经 Owner 确认。
- `profile` / `subprofiles` 是否已选择，并说明选择理由。
- `lineage` 是否已选择，并说明依据。
- `.codespec/changes/{id}` 流程实例路径是否已创建。
- `long_term_spec_path` / `long_term_design_path` 是否已确定；未确定时必须记录补齐策略。
- `spectest_feature_path` 是否适用；不适用时必须记录 N/A 理由。
- 交互开始 / 结束判定、合法延迟状态、异常状态边界、异常规则（规则表中类型为"异常"的条目）。
- 维测合同：日志、dump、测试或其他可观测证据。
- 热路径预算：是否命中 input / layout / render / animation 等路径。
- 前端/API/依赖/跨平台影响。
- 无障碍、国际化、多形态适配是否适用；不适用时记录 N/A 理由。
- Host 可测项、SpecTest 可测项、设备补验项和 N/A 理由。

每一项必须有 Owner 给出的结论、证据位置和确认来源。源码核对只能作为辅助证据，不能生成影响范围结论。

`evidence/checks/check-proposal.md` 包含 arkui-define-entry 和 arkui-define-exit 两张检查表：

| 检查项 | 结果 | 证据/缺口 | 确认来源 | 后续动作 |
|--------|------|-----------|----------|----------|
| [检查项] | 通过/Blocked | [路径或缺口说明] | [需求 Owner 原文/链接/无] | [无/需提问的问题] |

判定规则：

- `通过`：所有必问/必检项均有明确结论和证据，且不存在待补齐项。
- `Blocked`：缺少需求 Owner 对范围、Profile、Lineage、AC、影响面或基线审批的明确输入。

未经逐项检查，不得把 arkui-define-entry 或 arkui-define-exit 写成 `通过`。若 Define gate 总结论不是 `通过`，不得进入 Specify。

### arkui-define-exit

基线审批检查：

- Owner 已审阅 `proposal.md` 并批准基线（`manifest.baseline_approval.approved=true`，approver/evidence 非空）。

信息来源记录检查：

- gate 文件顶部包含信息检索手段记录区段，记录使用了哪些手段及检索内容。
- 每条检查项的证据/缺口列包含 `检索手段 -> 知识库/规格 -> 源码核验 path:line` 的完整链路。
- 每条检查项的确认来源列标注具体途径。
- 通过手段 1-3 获取的关键结论，其源码核验已记录具体文件路径和行号。
- 未核验项不得标记为 `通过`。

上述任一项不满足，Define gate 不得判定为 `通过`。

## Specify Gate

### arkui-specify-entry

进入 Specify 后、编写 `spec.md` 之前，必须先完成存量特性归档检查。历史规格信息作为当前规格说明和设计参考。

FeatID 连续性预检：

1. 从 `specs/index.md` 读取当前 FuncID 下已注册的所有 FeatID。
2. 若当前 FeatID 为 `Feat-NN` 且 `NN > 01`，检查 `Feat-01` 到 `Feat-(NN-1)` 是否全部存在于已注册列表中。
3. 若任何中间编号缺失，必须判定为 `Blocked`，不得以 `不存在`、`未注册`、`首次建立` 等理由判定为 N/A。
4. 当前 FeatID 为 `Feat-01` 时，连续性预检自动通过。
5. `Feat-01` 到 `Feat-(NN-1)` 均视为该功能域存量能力，必须已在 `specs/index.md` 注册，且已有长期规格文件与功能域长期 `design.md`。

若存量 Feat 缺少注册或归档文件，优先由需求 Owner 确认并补录缺失项；或由需求 Owner 更正 FeatID 编号，并同步修订 `manifest.md`、`.codespec/registry.md`、`specs/index.md`。

所有已归档的存量 spec 和 design.md 必须在编写当前 spec.md / design.md 之前读取。读取记录写入 `evidence/checks/check-spec.md` 的 arkui-specify-entry 部分，包含读取了哪些文件、获取了哪些关键参考点。

`arkui-specify-entry` 未通过时，不得开始编写 `spec.md`。

### arkui-specify-exit

Specify / Design 产物写入短期流程实例目录 `.codespec/changes/{id}/`，禁止直接写入长期 `specs/` 目录。

出口检查必须包含：

- `.codespec/changes/{id}/spec.md` 已创建且内容完整。
- 长期 `specs/` 下当前 Feat 对应文件状态正确（已有内容 / Draft 占位 / N/A）。
- 后续 Design / Plan / 长期归档路径已在 manifest 中记录。

## Design Gate

### arkui-design-entry

进入 Design 后，必须在已批准的 `spec.md` 基础上补齐 `design.md`，并完成交叉校验：

- `spec.md` 写清规则定义（行为/边界/异常/恢复）、验收标准。
- `design.md` 写清分层、对象关系、状态流转、验证路径和构建影响。
- `design.md` 与 `spec.md` 的 API 名称、模块边界、不涉及项、验证映射必须一致。
- 涉及热路径时，`design.md` 必须填写 Performance & Memory Budget。
- 涉及内存分配时，`design.md` 必须说明分配/释放点和所有权。
- 源码与 SDK 定义一致或差异已声明，P0/P1 AC 已映射验证。
- 存量能力优先补录长期 `specs/.../Feat-XX-*-spec.md`，行为描述以现有实现为准。
- 功能域已有 `specs/.../design.md` 时只能增量合并，不新增平行顶层设计。
- P0/P1 AC 必须映射到 Task 和验证命令；可 Inspector 断言的能力优先映射到 SpecTest case。
- SpecTest 映射至少记录 feature、suite、case、expected、目标节点 id 和执行命令；不适用项必须记录 N/A 理由。

### arkui-design-exit

`evidence/checks/check-design.md` 总结论为 `通过` 前，必须逐项核验：

- gate 文件包含存量规格读取记录。
- design.md 中引用的代码路径、API、类名等关键结论已通过源码核对验证，并记录具体文件路径和行号。
- Define 基线与存量设计差异已核验；若有差异，核验过程和结论已记录。
- gate 文件每条检查项的确认来源列标注 `源码核对 <path>:<line>` / `kb_search.py -> <知识库名>` / `Owner 确认` 等。
- 未核验项不得标记为 `通过`。

上述任一项不满足，Design gate 不得判定为 `通过`。

## Plan Gate

每个 Task 必须满足以下自闭环条件后才能标记完成：

1. 生产代码编写完成。
2. TDD 单元测试代码编写完成，或子 profile 定义的替代验证方式完成。
3. 测试编译通过：从该 Task 命中的子 profile 推导编译命令。
4. 若涉及生产代码变更，生产代码编译也通过。
5. 验证证据写入 Task Card / `evidence/reviews/review.md`，不得跨会话补证。
6. 若命中 SpecTest 适用场景，先执行单 case，再执行 affected suite，必要时执行全量。
7. SpecTest 报告路径必须写入 Task Card、`evidence/checks/check-execution-plan.md` 或 `evidence/reviews/review.md`。

Plan 后实现审查必须额外检查：

- 热路径额外开销是否符合 `design.md` Performance & Memory Budget。
- 是否有内存泄漏风险：有 allocate 无 deallocate、有裸指针无 RAII 包装、循环引用。
- 是否增加不必要的 layout / paint / render pass。
- 是否保持组件 API、DSL、状态机和既有交互兼容。
- 是否遵守 Task 文件范围；若超范围，先修订 Plan 再继续。
- SpecTest 适用项是否 `failed_cases=0`，不适用项是否有明确替代验证证据。

## 长期归档迁移

Plan 通过后，最终交付前必须将短期产物迁移到长期 `specs/` 目录，迁移前不得标记最终交付为通过。

迁移清单：

- `.codespec/changes/{id}/spec.md` 最终内容迁移到 `specs/<func-domain>/Feat-NN-<name>-spec.md`。
- `.codespec/changes/{id}/design.md` 增量内容合并到 `specs/<func-domain>/design.md`，不得新增平行重复设计。
- `specs/index.md` 特性行状态更新为 Baselined。
- `manifest.long_term_spec_path`、`manifest.long_term_design_path` 指向迁移后的长期路径。
- `evidence/checks/check-execution-plan.md` 或最终 review 记录迁移状态、差异摘要和未迁移理由。

## 发布验证

最终交付前必须按适用性补齐：

- 交互回归：核心手势、焦点、输入、状态切换。
- 视觉回归：布局、绘制、主题、字体、多窗口。
- 设备形态验证：手机、平板、折叠屏、横竖屏，按需求适用性裁剪。
- 性能观察：命中热路径时必须有目标设备或等价环境证据。
- 人工验证阻塞项：无法自动化的真实设备、真实输入、视觉判断必须写入 `evidence/checks/check-execution-plan.md` 或最终 review 证据。
- SpecTest 全量或风险裁剪验证报告必须归档；裁剪时说明 suite/case 范围和理由。
- `.codespec/registry.md`、`manifest.md`、`lineage.md`、`evidence/checks/*`、`evidence/reviews/review.md` 状态必须一致。
- 长期 `specs`、knowledge index、SpecTest 报告索引和 release view 按需回灌。
