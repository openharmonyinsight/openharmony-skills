# Skill 质量评测报告：ohos-ci-security-gitcode-pr

> 评测框架：Skill Judge（基于官方 Skill 提炼的 8 维度评测体系，满分 120 分）
> 评测对象：`skills/domain/security/cicd/ohos-ci-security-gitcode-pr/`
> 评测日期：2026-09-09

---

## 一、总览

| 指标 | 数值 |
|------|------|
| **总分** | **97 / 120（80.8%）** |
| **等级** | **B+（良好偏优 — 可用于生产的专家 Skill，关键脆弱操作有精确防护）** |
| **设计模式** | Tool 模式（决策树 + 精确脚本 + 低自由度脆弱操作）融合 Process 要素（6 步工作流 + 检查点） |
| **知识密度** | E:A:R ≈ 60:35:5（Expert:Activation:Redundant） |
| **一句话结论** | 将 GitCode 跨仓 PR 提交的脆弱操作（head 格式、远端分类、幂等检查、issue 关联）外部化为决策矩阵 + 精确 MCP 调用序列，知识增量集中在 GitCode API 的隐式校验规则，满足 B+ 级入库要求。 |

### 文件规模概览

| 目录 | 行数 | 说明 |
|------|------|------|
| `SKILL.md` | 320 | 核心文件，Agent 触发后加载（<500 行 ✓） |
| `references/` | 52（1 文件） | issue 模板 |
| `evals/` | 496 | 5 个 case + 评测报告 |

---

## 二、各维度评分

| 维度 | 得分 | 满分 | 简评 |
|------|------|------|------|
| D1：知识增量 | 15 | 20 | GitCode API head 格式校验、owner 分类、PR 幂等检查属专家知识 |
| D2：思维范式 + 领域流程 | 12 | 15 | 6 步工作流 + 检查点（PR 存在性）清晰；思维范式引导适中 |
| D3：反模式质量 | 10 | 15 | 错误处理章节含隐式反模式；无显式 NEVER 章节 |
| D4：规范合规（尤其 description） | 14 | 15 | description 含 WHAT + WHEN + 关键词；MCP 前置检查声明明确 |
| D5：渐进式披露 | 12 | 15 | 单文件 320 行结构清晰；references 仅 issue 模板，无分层加载 |
| D6：自由度校准 | 14 | 15 | 脆弱操作（head 格式、MCP 调用）低自由度；远端歧义中自由度（用户选择）恰当 |
| D7：模式识别 | 10 | 10 | Tool 模式 + 轻量 Process，与脆弱 PR 提交任务匹配（封顶） |
| D8：实用可用性 | 10 | 15 | 决策矩阵、决策树、错误处理表全覆盖；缺 fixture 评测产物 |

---

## 三、关键问题

**无阻塞性问题。** 该 Skill 可直接用于生产环境，满足入库 B+ 级要求。

---

## 四、Top 3 改进建议

### 建议 1：增加显式反模式章节

**问题**：SKILL.md 有 `## Error Handling` 章节（9 条错误场景），但无 `## Anti-Patterns` 或 `NEVER` 章节。关键反模式（如"不要假设远端名""不要用 curl 绕过 MCP""不要在 PR 已存在时重复创建"）散落在工作流和错误处理中，未集中可见。

**改进**：在 SKILL.md 增加 `## Anti-Patterns` 章节，列 Top 6 NEVER：

```markdown
## Anti-Patterns

- NEVER 假设远端名为 upstream/fork——必须运行 git remote -v 并按 owner 解析分类。
- NEVER 在没有 gitcode MCP 时用 curl 或直接 HTTP 调用绕过——立即警告用户并终止 skill。
- NEVER 在 PR 已存在时重复创建——先 gitcode_list_pull_requests 检查幂等性。
- NEVER 把 head 格式写成 `origin:branch` 或 `fork:branch`——必须是 `fork-owner:branch-name`，GitCode API 严格校验。
- NEVER 在 fork 仓库创建 issue——issue 必须在上游（openharmony owner）仓库创建。
- NEVER 跳过 PR 模板直接写 body——必须读取 .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md 并填充 issue 关联。
```

**预期收益**：D3 从 10 升至 ~13，关键脆弱操作防护提升。

---

### 建议 2：补充 eval fixture（远程场景模拟产物）

**问题**：evals/ 目前为纯 prompt 驱动（无 fixture 文件），无法验证 Agent 是否真的执行了 `git remote -v` 解析、PR 存在性检查、issue 创建等操作。grader 只能靠 Agent 口述判断。

**改进**：为 eval case 增加 fixture 工作区：

```text
evals/files/two-remote-workspace/
  .git/config               # 含 origin(openharmony) + fork(personal) 两个远端
  .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md  # 模板
  .gitcode-pr-preview/
    pr-list-response.json   # 模拟 gitcode_list_pull_requests 返回（有/无现有 PR 两种）
    issue-create-response.json
    pr-create-response.json
```

让 grader 能验证 Agent 是否正确解析远端、是否检查了 PR 列表、是否用了正确 head 格式。

**预期收益**：D8 从 10 升至 ~13，评测可验证性大幅提升。

---

### 建议 3：将决策矩阵与决策树合并为可扫描路由表

**问题**：SKILL.md 同时有 `### Decision Matrix`（5 行表格，L60-68）和 `## Decision Tree`（37 行 ASCII 图，L271-310），内容有重叠。Agent 需读两处才能确定动作，增加上下文消耗。

**改进**：将决策矩阵嵌入决策树对应节点，合并为单一路由表：

```markdown
## Remote Detection → Action Routing

| Upstream | Fork | Action |
|----------|------|--------|
| ✓ openharmony | ✓ personal | push to fork → check PR → create issue+PR on upstream |
| ✓ openharmony | ✗ | Ask: "Need to fork first?" |
| ✗ | ✓ personal | Use fork as both push + PR target (warn: no upstream) |
| ✗ | Multiple | Ask user to select fork remote |
| ✗ | ✗ Single | Use as fork, warn: no upstream |
```

删除独立决策树 ASCII 图（其内容已被路由表覆盖），节省 ~37 行。

**预期收益**：D5 从 12 升至 ~13，上下文消耗减少；D7 维持封顶。

---

## 五、详细分析

### D1：知识增量（15/20）— 良好

**专家知识示例**：

| 知识点 | 位置 | 价值 |
|--------|------|------|
| GitCode 跨仓 PR head 格式 `fork-owner:branch-name`（严格校验） | L166-168 | Claude 默认写 `origin:branch` 或 `fork:branch`，必失败 |
| owner=openharmony 为 UPSTREAM 的分类规则 | L44-48 | GitCode 仓库归属语义，Claude 不会自发推导 |
| PR 合并自动关闭 issue（通过 #number） | L243-247 | GitCode issue-PR 关联机制 |
| .gitee/PULL_REQUEST_TEMPLATE.zh-CN.md 模板路径 | L200 | OpenHarmony 仓库约定的 PR 模板位置 |
| gitcode_list_pull_requests 幂等检查 | L104-125 | 避免重复创建 PR 的关键步骤 |

**扣分点**：部分知识（如 PR 模板路径）是 OpenHarmony 仓库约定而非 GitCode API 知识，知识增量密度中等；references 仅 issue 模板（52 行），无分层专家参考。

### D2：思维范式 + 领域流程（12/15）— 合格偏优

**领域流程**：6 步工作流（检查状态→检查PR存在→创建issue→push fork→创建PR→完成）清晰，含 PR 存在性检查点（步骤 2 分支）✓

**思维范式**：远端分类决策矩阵引导"先列所有远端、按 owner 分类、再决定动作"的思考顺序 ✓

**扣分**：部分流程偏机械（bash 远端解析脚本），思维引导集中在决策矩阵一处。

### D3：反模式质量（10/15）— 中等

Error Handling 章节（9 条）隐含反模式（如"PR already exists → don't create duplicate"），但无显式 NEVER 章节。关键脆弱操作（head 格式、MCP 前置、issue 创建仓库）的误用防护散落在工作流中，Agent 加载 SKILL.md 时无法一眼扫到全部禁令。

非阻塞性：工作流本身实现了正确逻辑，反模式缺失不影响功能正确性。

### D4：规范合规（14/15）— 良好

**Frontmatter 合规**：name/description/metadata 完整，与目录位置一致 ✓

**description 分析**：

| 要素 | 内容 | 评价 |
|------|------|------|
| WHAT | "Handle GitCode PR workflow for OpenHarmony - commit changes, push to fork, create issue, create PR" | 功能清晰 ✓ |
| WHEN | "Use when user wants to submit/create PR or commit changes" + "Auto-checks if PR exists" | 场景明确 ✓ |
| KEYWORDS | security, gitcode-pr, cicd, pr-workflow | 关键词适中 ✓ |
| MCP 前置 | "Use the gitcode mcp. If gitcode mcp is not present, warn and terminate immediately"（L21） | 前置检查明确 ✓ |

**扣分**：description 略长（3 句），但信息密度高，可接受。

### D5：渐进式披露（12/15）— 合格

**两层结构**：
- Layer 1：name + description ✓
- Layer 2：SKILL.md 320 行 <500 行 ✓
- Layer 3：references/issue_template.md（52 行）按需 ✓

**缺口**：决策矩阵（L60-68）和决策树（L271-310）内容重叠，Agent 需读两处。无 MANDATORY 触发标注（如"加载 issue 模板前必须读取 references/issue_template.md"已隐含但未显式标注）。

### D6：自由度校准（14/15）— 良好偏优

| 任务类型 | 自由度 | 评价 |
|----------|--------|------|
| head 格式（极脆弱） | 低 | 精确格式 `fork-owner:branch-name`，标注 CRITICAL ✓ |
| MCP 调用（脆弱） | 低 | 精确 gitcode_create_pull_request 参数 ✓ |
| 远端解析 | 低 | 精确 bash 脚本 ✓ |
| 远端歧义处理 | 中 | 要求用户选择，不自动猜测 ✓ |
| PR 模板填充 | 中 | 引导按模板方向填充，留内容自由度 ✓ |

自由度校准优秀：极脆弱操作（head 格式）给极低自由度 + CRITICAL 标注，是本 Skill 亮点。扣 1 分因 issue 描述生成完全依赖 git log/diff 自动填充，未约束自由度（可能产生低质量 issue 描述）。

### D7：模式识别（10/10）— 封顶

**Tool + 轻量 Process 模式对照**：

| 特征 | 体现 |
|------|------|
| 脚本/MCP 驱动 | gitcode_create_pull_request 等精确调用 |
| 决策树 | 远端检测→PR 存在性→创建流程的完整 ASCII 决策树 |
| 低自由度 | head 格式 CRITICAL、MCP 前置检查 |
| 检查点 | PR 存在性检查（步骤 2）分支为"只 push"或"创建 issue+PR" |

模式选择与任务（脆弱的跨仓 PR 提交）高度匹配。封顶。

### D8：实用可用性（10/15）— 合格

| 可用性要素 | 覆盖 | 评价 |
|-----------|------|------|
| 决策矩阵 | 5 行远端分类表 ✓ | ✓ |
| 决策树 | 37 行完整 ASCII 流程图 ✓ | ✓ |
| 代码示例 | bash 远端解析 + MCP 调用示例 ✓ | ✓ |
| 错误处理 | 9 条错误场景表 ✓ | ✓ |
| 边缘场景 | 多远端歧义、无 fork、PR 已存在、模板缺失 ✓ | ✓ |
| 上下文采集 | git log/diff/branch/remote 来源表 ✓ | ✓ |

**主要缺口**：无 eval fixture 文件（纯 prompt 驱动），grader 无法验证 Agent 是否真的执行了远端解析和 PR 存在性检查。这是 D8 扣分主因——可用性知识全面，但评测可验证性不足。改进建议 2 可解决。

---

## 六、元问题检验

> **"该领域的专家看到这个 Skill，会说'这捕捉了我花多年才学会的知识'吗？"**

**会。** 以下知识只有实战积累才能获得：

1. **head 格式 `fork-owner:branch-name`**——GitCode API 严格校验，少了 owner 前缀或多了 remote 名前缀都会失败，这是踩坑知识
2. **owner=openharmony 为 UPSTREAM**——GitCode 仓库归属语义决定 PR base/issue 创建目标
3. **PR 合并自动关闭 issue**——通过 #number 关联的机制
4. **先检查 PR 存在性再决定是否创建**——避免重复 PR 的幂等设计
5. **issue 必须在上游仓库创建**——跨仓 issue 归属语义

这是**压缩的 PR 提交经验**，而非通用 git 知识。

---

## 七、与官方模式对照

| 模式 | ~行数 | 契合度 |
|------|-------|--------|
| Tool | ~300 | ✓ 主模式（MCP 调用、决策树、低自由度） |
| Process | ~200 | 部分融合（6 步工作流 + PR 存在性检查点） |

本 Skill 以 **Tool 模式为主**，融合轻量 Process 要素。模式选择与任务（脆弱的跨仓 PR 提交 + 幂等检查点）匹配良好。

---

## 八、最终结论

**97/120（80.8%，B+ 级）**——满足入库 B 级要求，超出至 B+，可用于生产环境。

核心价值：将 GitCode 跨仓 PR 提交的脆弱操作（head 格式、远端分类、幂等检查、issue 关联）外部化为决策矩阵 + 精确 MCP 调用序列，head 格式 CRITICAL 标注是亮点。三条改进建议（显式反模式、eval fixture、决策矩阵与决策树合并）可提升至 A-，但不影响当前入库资格。

该 Skill 通过 Skill Judge B+ 级检验。
