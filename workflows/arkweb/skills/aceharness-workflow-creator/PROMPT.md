## Aceharness 工作流创建（aceharness-workflow-creator 技能）

**触发场景：**
- 创建工作流 / 新建 workflow / 写工作流配置
- 需要 state-machine / phase-based 编排
- 用户给出复杂目标，希望拆成多 Agent、多阶段推进

## 核心规则

- 创建前必须收集目标、范围、工作目录、验收约束
- 不要直接用 bash 创建 YAML 代替 UI 创建流程
- 需要写入后校验时，使用本 skill 的校验脚本
- 用户未明确要求隔离执行时，优先 `context.workspaceMode: in-place`

## 输出协议

**本 skill 的所有结构化输出都必须遵守系统级 `<result>` 协议。**

| 上下文 | 阶段 | 输出格式 |
|--------|------|----------|
| 首页聊天 | 收集需求/澄清 | `<result>` 内输出 `{"kind":"home_sidebar","payload":{...}}` |
| 首页聊天 | 方案预览 | `<result>` 内输出 `{"kind":"card","payload":{...}}` |
| 创建弹窗 | 补充问答 | `<result>` 内输出 `{"kind":"clarification_form","payload":{...}}` |
| 创建弹窗 | 正式计划 | `<result>` 内输出 `{"kind":"plan_draft","payload":{...}}` |
| 创建弹窗 | YAML 草案 | `<result>` 内输出 `{"kind":"workflow_draft","payload":{...}}` |

约束：

- `<result>` 内只能放一个 JSON 对象
- 不要在 `<result>` 内使用 fenced code block
- 不要在 `<result>` 外输出结构化卡片或 JSON
- `<result>` 内直接放 JSON，禁止 fenced 围栏

## 工作方式

1. 收集需求  
   先确认问题、目标、工作目录、范围边界、参考 workflow、是否隔离执行。

2. 查询资源  
   查看可用 Agent 和参考 workflow。除非用户明确指定，优先帮助用户创建 `state-machine` 工作流。

3. 确认关键信息  
   包括：工作目录、主要产物、成功标准、参考结构、workspaceMode。

4. 设计方案  
   首页聊天里可以用 `kind=card` 预览方案；真正驱动首页右侧侧边栏时用 `kind=home_sidebar`。

5. 生成草案并校验  
   生成 `kind=workflow_draft` 后由系统解析和校验；写入流程仍走 UI。

## Agent 团队

- defender（红队）: 设计、实现、测试、文档
- attacker（蓝队）: 挑战方案、找风险
- judge（裁判）: 评审和定稿

详细 YAML 规范、验证规则和设计原则，查 `skills/aceharness-workflow-creator/SKILL.md`。
