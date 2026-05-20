## ACEHarness Spec Coding

**触发场景：**
- 用户要求 spec-first、先写规范再实现、把粗需求变成可执行计划
- 用户提到 requirements、design、tasks、需求文档、设计文档、实现计划
- 用户要求创建 workflow 前先澄清需求、沉淀需求、生成正式计划制品
- 用户要求根据规范执行任务或更新任务状态

**三阶段工作流：**

1. **需求文档 (requirements.md)**
   - 从用户输入和代码中提取已知事实
   - 针对会改变实现和验收的关键问题进行访谈（目标与价值、当前与目标行为、范围与非目标、兼容与迁移、验证方式）
   - 输出：用户故事 + WHEN/THEN 验收标准 + 术语表

2. **设计文档 (design.md)**
   - 基于 requirements.md 设计技术方案
   - 输出：Mermaid 架构图 + 组件接口 + 伪代码 + 关键决策表

3. **实现计划 (tasks.md)**
   - 基于 requirements.md + design.md 拆解任务
   - 输出：多级嵌套 checkbox + 需求追溯（`_需求：x.x_`）+ 检查点

**需求访谈原则：**
- 先吸收用户已说过的内容和代码中能确认的事实
- 只问会影响实现策略或验收标准的问题
- 给具体选项并允许补充，避免空泛问题
- 每个问题说明它会影响哪类决策（范围、数据模型、兼容、验证）

**质量标准：**
- requirements.md：每个需求有用户故事 + WHEN/THEN 验收标准
- design.md：至少 1 个 Mermaid 图 + 组件接口 + 关键决策表
- tasks.md：多级嵌套 checkbox + 每个子任务引用需求编号 + 检查点
- 三份制品术语一致、范围一致、语言一致

**执行循环：**
1. 确定制品目录 `specs/<domain>/`
2. 读取已有制品（requirements.md、design.md、tasks.md）
3. 补齐关键需求问题
4. 从 tasks.md 选择最小未完成任务
5. 按需求边界实现并验证
6. 更新 tasks.md 状态（`[x]` 已完成，`[-]` 进行中）
7. 必要时同步更新 requirements.md 或 design.md

**与 workflow 创建协同：**
1. 先用本 skill 生成并确认正式规范制品（requirements.md、design.md、tasks.md）
2. 再由 workflow creator 基于确认后的制品设计 workflow 草案（YAML 配置）
3. workflow 草案阶段不重新澄清需求、不重新生成制品
4. 运行态结构（phases、assignments、progress）只作为制品的结构化投影/快照，正式制品是规范源
5. 正式制品中使用业务术语，不混入 workflow/Agent/状态机等运行态概念

**校验：**
仅在创建、更新或校验正式制品时使用：

```bash
node skills/aceharness-spec-coding/scripts/validate-spec-coding.mjs <spec-root>
```

**持久化 Spec 模式：**
当工作流配置 `specCoding.persistMode: 'repository'` 时：
- spec 制品位于 `specCoding.specRoot` 目录（默认 `<workingDirectory>/.spec`）
- 目录结构：`spec.md`（master 输入）、`checklist.md`（问题清单输入）、`specs/<workflowName>-<runId>/`（delta 制品目录）
- 审查时检查 `checklist.md`，所有未回答问题（`- [ ]`）需要在审批时提出
- 修订制品时直接更新 requirements/design/tasks artifacts 的正文，保持术语、范围和需求追溯一致
