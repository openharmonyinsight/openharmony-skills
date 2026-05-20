---
name: arkweb-brainstorm
description: ArkWeb 需求拆解与方案设计。可作为独立 subagent 运行。通过结构化分析拆解需求、评估技术可行性、输出 2-3 个可选方案。触发词：ArkWeb 需求分析、新需求、需求拆解、技术方案设计、PRD 拆解。
---

# ArkWeb 需求拆解与方案设计

**Announce at start:** "我正在使用 arkweb-brainstorm skill 进行需求拆解。"

## 运行模式

### 模式 A：Subagent 模式 — 预注入（推荐）

作为独立 subagent 被 `arkweb-architect` 调度。主 Session 已完成知识库检索、参考文档读取和专家团讨论，所有关键信息通过 task 描述直接注入，subagent **不需要自行读取知识库或参考文件**。

**优势：** 避免 subagent 重复检索知识库导致 token 消耗过大和超时。

**输入格式（从 task 描述中解析）：**
```
## 用户需求
{需求描述}

## 约束
- 目标设备：{设备范围，默认全覆盖}
- OHOS 版本：{版本范围，默认全部}
- 已确认的边界条件：{Q&A 结果，如有}

## 参考信息摘要（主 Session 预读取）
{关键信息，由主 Session 从参考文档中提取注入}

## 知识库证据包（主 Session 预检索）
{通过知识库降级策略检索到的证据，包含 LOCAL_KB / DEEPWIKI / LOCAL_DOC / CODE 证据}

## 专家团讨论纪要（主 Session 预收集）
{专家意见汇总}
```

**执行规则：**
1. **不自行检索知识库**——知识库证据包已在 task 描述中提供
2. **不读取任何参考文件**——所有信息已在 task 描述中提供
3. 直接从 Step 2（需求拆解）开始，跳过 Step 1（理解项目上下文 + 知识库检索）
4. 在方案设计中引用知识库证据包中的条目
5. 跳过 Step 2.5（专家团讨论）——已在主 Session 完成
6. 直接进入 Step 3（提出方案）→ Step 4（交互场景分析）→ Step 5（输出）
7. **【强制】** 文档末尾必须输出「知识证据清单」，引用知识库证据包中的条目

**输出：** 完整的 brainstorm 文档 → 保存到指定路径 → 回复摘要

### 模式 B：交互模式

在主 session 中直接调用时，逐项确认需求边界后再输出方案。流程见下方 Step 2。

---

## 概述

将 ArkWeb 相关需求从 PRD/想法拆解为可落地的技术方案。输出 2-3 个可选方案及推荐建议。

## 知识库驱动规则

通用规则统一引用：`../_shared/KB_RULES.md`。本 skill 的增量要求：

- **模式 A**：主 Session 已在 Phase 2 Step 2.0 执行知识库检索并注入证据包，subagent 直接引用，不重复检索
- **模式 B**：subagent 自行按 `_shared/KB_RULES.md` 的降级策略检索
- brainstorm 文档必须新增「知识证据清单」小节
- 专家团讨论与方案推荐必须引用同一份证据包，避免跨专家口径不一致

## 流程

### Step 1: 理解项目上下文

> **⚠️ Subagent 预注入模式下跳过此步骤**——主 Session 已在 Phase 2 Step 2.0 完成知识库检索并注入证据包。

1. 读取已有参考文档：
   - `{DOCS_REPO}/docs/` 下的相关文档
   - `{DOCS_REPO}/analysis/arkweb-ace-engine-analysis.md`（ACE Engine 代码索引）
   - `{DOCS_REPO}/references/arkweb-architecture.md`（架构参考）
2. 检查 git 最近提交，了解项目当前状态
3. 按 `_shared/KB_RULES.md` 的降级策略执行知识库检索
4. 生成「候选子系统/部件/API」列表
5. 输出知识证据包（后续专家讨论与方案设计都必须引用该证据包）
6. **【强制持久化】** 证据包 Write 到 `{DOCS_REPO}/tmp/`，详见 `_shared/KB_RULES.md` 第 10 节

### Step 2: 需求拆解

#### Subagent 模式
直接从 task 描述中读取约束条件，跳过交互确认。

#### 交互模式
逐项确认，一次只问一个问题：

1. **功能边界**：这个需求涉及哪些 ArkWeb 层？（API 层 / 框架层 / 内核层 / 平台层）
2. **设备范围**：目标设备有哪些？（手机/平板/PC/2in1/智慧屏/手表/车机/IoT）
3. **兼容性要求**：需要兼容哪些 OHOS 版本 / API Level？
4. **性能基线**：有无明确的性能指标要求？
5. **安全约束**：有无隐私/安全/沙箱方面的限制？

### Step 2.3: 知识库候选集收敛（新增）

在专家讨论前，基于知识库证据包先输出候选集，避免专家讨论偏题：

- 核心候选子系统（1~3 个）
- 核心候选部件（3~8 个）
- 代表性候选接口（5~15 个）
- 每项都必须附证据来源（按 `_shared/KB_RULES.md` 的 source_type 标注）

### Step 2.5: 专家团讨论（Subagent 并行）

#### 总架构师（自己）角色
你是总 Web 大架构师，负责召集专家团、收集意见、总结归纳。

#### 专家团成员（10 个独立 Subagent）
| # | Expert ID | 角色 | Skill 路径 |
|---|-----------|------|-----------|
| 1 | arkweb-expert-performance | ⚡ 性能专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-performance/SKILL.md |
| 2 | arkweb-expert-multimedia | 🎬 多媒体专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-multimedia/SKILL.md |
| 3 | arkweb-expert-peripheral | 🔌 外设服务专家（传感器/电池/唤醒锁/震动/屏幕） | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-peripheral/SKILL.md |
| 4 | arkweb-expert-interaction-security | 🔐 交互安全专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-interaction-security/SKILL.md |
| 5 | arkweb-expert-rendering | 🎨 渲染引擎专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-rendering/SKILL.md |
| 6 | arkweb-expert-compositing | 🖼️ 渲染合成专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-compositing/SKILL.md |
| 7 | arkweb-expert-interaction-motion | ✨ 交互专家（滚动/缩放/菜单/选择/拖拽/上传/焦点/填充/AI化） | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-interaction-motion/SKILL.md |
| 8 | arkweb-expert-network | 🌐 网络加载专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-network/SKILL.md |
| 9 | arkweb-expert-js-engine | ⚙️ JS 引擎专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-js-engine/SKILL.md |
| 10 | arkweb-expert-stability | 🛡️ 稳定性与 DFX 专家 | ~/.openclaw/workspace/skills/arkweb-experts/arkweb-expert-stability/SKILL.md |

#### 执行方式

**并行 spawn 10 个专家 subagent**，每个专家独立分析需求并输出意见。

每个专家的 task 模板：
```
你是 ArkWeb 领域的{角色名}专家。请分析以下需求，从你的专业角度给出意见。

1. 读取你的 skill 文件：{skill_path}
2. 按 skill 定义的输出格式给出意见

## 用户需求
{user_requirement}

## 约束条件
- 目标设备：{device_scope}
- OHOS 版本：{ohos_versions}

## 参考资料（按需读取）
- 架构参考：{DOCS_REPO}/references/arkweb-architecture.md
- ACE Engine 分析：{DOCS_REPO}/analysis/arkweb-ace-engine-analysis.md
- 离线知识库：{kb_root}
- DeepWiki 补充证据：{deepwiki_hits}

## 输出
直接输出你的专家意见，不需要保存文件。意见必须引用知识证据（LOCAL_KB 或 DEEPWIKI）。
```

#### 总架构师汇总

所有专家意见收集完成后，总架构师执行以下汇总工作：

1. **分类整理**：将专家意见按"采纳/参考/暂不考虑"分类
2. **提取共识**：多个专家共同关注的问题
3. **识别冲突**：不同专家之间的意见分歧
4. **融入方案**：将采纳的意见融入后续方案设计中

汇总格式：
```markdown
## 🧠 专家团讨论纪要

### 共识（3+专家一致）
- {共识1}

### 高价值建议（2专家提出）
- {建议1}

### 分歧与权衡
- {分歧1}：{专家A} 认为... vs {专家B} 认为... → 结论：{总架构师裁定}

### 领域特定关切
- ⚡ 性能：{关键点}
- 🎬 多媒体：{关键点}
- ...

### 对方案的影响
- 采纳的专家意见将如何影响方案设计
```

#### 注意事项
- 专家团讨论仅在 **Subagent 模式**下执行（交互模式下可跳过）
- 如果需求明确只涉及 1-2 个领域，可以只 spawn 相关专家（但至少 3 个）
- 专家意见是输入，不是决定权——最终方案由总架构师综合判断

#### 相关度权重机制

防止讨论偏离主题，必须遵守相关度权重规则：

**权重等级：**
- 🟢 **核心专家**（权重 3x）：需求的主要功能直接属于该专家领域
- 🟡 **关联专家**（权重 2x）：需求可能间接影响该专家领域
- ⚪ **旁听专家**（权重 1x）：需求与该专家领域基本无关

**判定方式：** spawn 专家之前，总架构师先判定每个专家的相关度级别。

**讨论控制：**
- 核心专家的意见篇幅应占总意见的 40%+
- 关联专家的意见篇幅应占 30%
- 旁听专家简短表态即可（1-2 点），不超过 30%
- 如果判定为"旁听"的专家超过 5 个，可以不 spawn 这些专家（节省资源）

**汇总标注：** 在专家团讨论纪要中，每个专家意见标注权重级别（🟢/🟡/⚪）。

**示例：** 如果需求是"手势模拟注入"：
- 🟢 核心专家：交互专家（滚动/手势/拖拽）、渲染引擎（DOM事件分发）
- 🟡 关联专家：渲染合成（合成器手势处理）、性能（输入延迟）、稳定性（ANR）
- ⚪ 旁听专家：多媒体、网络、JS引擎、外设

### Step 3: 提出方案

> **注意：方案设计必须融入 Step 2.5 专家团讨论中采纳的建议。在方案说明中标注"采纳了 XX 专家的建议"。**

输出 **2-3 个方案**，按侵入程度分类：

| 方案 | 侵入程度 | 说明 |
|------|---------|------|
| A | API 层 | 纯 ArkWeb API 扩展，不涉及内核修改 |
| B | 框架层 | 修改 web_webview / ace_engine |
| C | 内核层 | 修改 Chromium 源码分支 |

每个方案包含：
- **架构**：分层描述 + ASCII 架构图
- **关键修改点**：涉及的仓库、模块、文件
- **优缺点**：对比矩阵（10+ 维度）
- **风险**：技术风险 / 兼容性风险 / 工期风险
- **工期估算**：按人天
- **知识依据**：对应的子系统/部件/API 证据（离线路径 + DeepWiki URL）

### Step 4: 交互场景分析（补充）

针对方案中涉及用户交互的部分，分析边界场景：
- 拖拽 + 滚动冲突
- 多指操作
- 键盘/鼠标 vs 触控模式差异
- 特殊布局（RTL、嵌套 overflow 等）

### Step 5: 输出

#### Subagent 模式
直接保存文档并回复摘要。

#### 交互模式
- 用户选择方案后，通知主 session 进入 design-doc 阶段
- 如果用户要求修改方案，回到 Step 3 修订

## 产出物

- **路径**：`{project_root}/docs/YYYY-MM-DD-{feature-name}-brainstorm.md`
- **Subagent 回复格式**：
  ```
  ✅ brainstorm 完成
  📄 文档：{file_path}
  📋 方案摘要：
  - 方案 A（{侵入程度}）：{一句话描述}，工期 {N}d
  - 方案 B（{侵入程度}）：{一句话描述}，工期 {N}d
  - 推荐：方案 {X}
  ```
