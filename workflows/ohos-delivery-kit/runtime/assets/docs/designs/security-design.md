# 安全设计：安全如何融入 SDD

> 面向后来者：本文解释 OHOS Delivery Kit (ODK) 里「安全」是怎么嵌进 spec-driven 开发流程的——两层模型、单一触发源、各阶段产物，以及当前实现到哪一步。
>
> 状态时间点：`2026-06-27`（基于 dev `c45709f`，含 #44 的条件章节单一源改动）。

---

## 1. 概述

ODK 的安全采用**两层模型**，安全随 SDD 主流程自然产生，而非另起炉灶：

- **Tier 1（普适）**：`安全基础检查` —— design 阶段的条件章节，触发即必产，轻量基线。
- **Tier 2（深度）**：`threat-model.md` —— 高风险变更按需产出，STRIDE + 合规的深度威胁分析。

两层都由 propose 阶段的 **`安全/权限` 维度裁定**作为单一触发源驱动，并最终回流到 spec-for-validation 的安全场景做验证：

```
propose ── 8 维评估，安全/权限 裁定（唯一触发源）
   │  安全/权限 = 是
   ▼
design ── 「安全基础检查」条件章节（Tier 1，触发即必产）
              └─ 「深度威胁分析(如需)」小节 = 升级指针
                     │  命中高风险判据
                     ▼
              threat-model.md ── Tier 2，按需（STRIDE + DFD + 合规）
                     │
                     ▼
spec-for-validation ── [安全与权限 security] 场景（验证缓解措施，追溯到 AC）
```

---

## 2. 设计目标

- **普适轻量 + 深度按需**：普通变更只触发轻量检查，不背深度建模成本；高风险才升级。
- **随流程自然产生**：安全检查落在已有的 design / validation 阶段，不新增独立流程。
- **单一触发源、可追溯**：一个信号（propose 的 `安全/权限`）驱动整条链；缓解措施能追到 AC / Task。

---

## 3. 两层安全架构

### 3.1 Tier 1：安全基础检查（design 条件章节）

`安全基础检查` 是 `design.md` 的一个**条件章节**（`core/templates/ai/design.md`），由 `odk-design` 在设计阶段按需展开。

**触发条件**：当 `proposal.md` 的 `安全/权限` 维度为「是」时展开「安全基础检查」（单一上游信号，见 `odk-design` 步骤 6）。下列信号是 **propose 阶段判定 `安全/权限=是` 的依据**，不是 design 阶段的并列触发条件：

- 变更涉及跨进程 / 跨服务 / 跨网络交互（IPC、Binder、共享内存、Socket）；
- 变更涉及跨安全层级（用户态 ↔ 内核态、沙箱内外、不同 SELinux 域）；
- 变更涉及敏感数据处理（用户数据、凭证、密钥）；
- 变更涉及加密 / 认证 / 授权 / 权限申请，或 `spec.md` 含权限 / 加密 / 认证相关 AC。

不满足时（`安全/权限=否`），章节填「不涉及」并说明理由（不留空）。

**章节内容**：信任边界交叉分析表 + 基础安全要求检查表（加密算法 / 密钥管理 / 随机数 / 输入验证 / 错误处理 / 配置）+ 敏感数据处理表。详细清单见 `docs/security-guide.md`。

**为什么是「条件章节」**：通过 `core/contracts/artifacts.yaml` 的 `conditional_sections` 登记 + `check-examples.sh` 的单一源机制（见 §5），章节在触发时才要求出现、不触发时合法省略——避免每个变更都被强制写安全章节。

### 3.2 Tier 2：威胁模型（threat-model.md，按需）

`threat-model.md` 是一个**独立的深度威胁分析产物**，由 `/odk-security-threat-model` 生成（`core/skills/odk-security-threat-model`），采用 Microsoft STRIDE + 法规合规检查。

**触发条件**：`proposal.md` `安全/权限` = 「是」**且** 命中任一高风险判据，或用户显式调用（与 skill 的 Trigger Conditions 一致）。高风险判据：
- 涉及敏感数据（PII、生物特征、位置、通讯录、支付信息）；
- 新增网络接口 / 远程 API / 云同步 / 外部连通；
- 修改认证、授权、权限模型；
- 涉及法规合规（GDPR、个人信息保护法、数据出境）；
- 涉及关键安全组件（内核、安全框架）；
- 用户显式调用 `/odk-security-threat-model`。

**内容**：数据流图（DFD，标注信任边界）+ STRIDE 威胁表（每条带现有控制 / 建议控制 / 优先级 / 关联 AC）+ 法规合规检查 + 风险与缓解（关联 Task）。要求**每条威胁的缓解措施可追溯到 Task**。

> design 模板里的「深度威胁分析（如需）」小节是 **Tier 1 → Tier 2 的升级指针**：它不重复 threat-model 的内容，只记录「为什么产 / 未产」并链到 `threat-model.md`。

---

## 4. SDD 流程中的安全（追溯链）

| 阶段 | skill | 产物 | 触发 / 职责 |
|---|---|---|---|
| propose | `odk-propose` | proposal.md 的 8 维评估 | `安全/权限` 维度裁定 = **唯一触发信号** |
| design | `odk-design` | design.md 的 `安全基础检查` 条件章节 | `安全/权限=是` 或信任边界 / 敏感数据等（总是，触发即产） |
| 深度（按需） | `odk-security-threat-model` | `threat-model.md` | `安全/权限=是` **且** 高风险判据 |
| validation | `odk-spec-for-validation` | spec-for-validation.md 的 `[安全与权限 security]` 场景 | 验证 design / threat-model 的缓解措施，追溯到 AC |

链条：propose 的 `安全/权限` 裁定 → design 必产 `安全基础检查` → 命中高风险则升级 threat-model → spec-for-validation 的 security 场景验证缓解措施并追到 AC。

---

## 5. 触发机制（条件章节怎么自动起来的）

安全检查「按需出现」靠的是 ODK 的**条件章节 + 单一真相源**机制：

1. **真相源**：`core/contracts/artifacts.yaml` 的 `conditional_sections` 登记「哪些章节是条件章节」+ `required_when`（何时需要）。当前 design 的条件章节：`代码事实基线` / `状态归属与不变量` / `既有模式复用` / `类图` / `安全基础检查`。
2. **读取方**：`scripts/check-examples.sh` 的 `is_conditional_section` 不再用手写白名单，而是在启动时经 `scripts/lib/odk_yaml.py conditional-section-keys` 读契约（#44 落地），用 `grep -qxF` 查表。**新增 / 改名条件章节只需改 `artifacts.yaml` 一处**，消除「模板注释 + 契约 + bash 白名单」三处同步的漂移（正是这个漂移让 `安全基础检查` 一度漏登记、check-examples 跑红）。
3. **加载失败不静默**：契约解析失败时显式报根因并退出，不降级成一堆「missing chapter」。

> **触发术语已统一**：propose 的 8 维 `安全/权限` 维度（曾写作 `安全权限`）已在 PR-2 对齐成统一写法 `安全/权限`，跨 propose / design / threat-model / spec-for-validation 一致。

---

## 6. 实现现状（as-built，含 PR-2，基于 dev `fbcd0a5`）

| 组件 | 位置 | 状态 |
|---|---|---|
| `安全基础检查` design 条件章节（模板 + 触发逻辑） | `core/templates/ai/design.md`、`core/skills/odk-design/SKILL.md` 步骤 6 | ✅ 已落地（`1e99c33`） |
| `安全基础检查` 契约登记 | `core/contracts/artifacts.yaml`（design `conditional_sections`） | ✅ 已落地（#44） |
| 条件章节单一源机制 | `scripts/lib/odk_yaml.py`（`conditional-section-keys`）、`scripts/check-examples.sh` | ✅ 已落地（#44） |
| propose 8 维 `安全/权限` 触发维度 | `core/skills/odk-propose/SKILL.md` | ✅ 已落地（#70 item 11） |
| threat-model 模板 / skill | `core/templates/ai/threat-model.md`、`core/skills/odk-security-threat-model/SKILL.md` | ✅ 存在（`1e99c33`） |
| threat-model **契约登记为一等旁路 artifact** | `core/contracts/artifacts.yaml`（`threat-model`：`required:false / bypass:true`） | ✅ 已登记（PR-2，镜像 `spec-for-validation`） |
| router 接线（`odk-security-threat-model` 可达） | `core/skills/using-odk/SKILL.md`（artifact / skill / template 三处） | ✅ 已落地（PR-2） |
| 触发术语 / 触发链单一源 | 跨 propose / design / threat-model / spec-for-validation | ✅ 已统一为 `安全/权限`（PR-2） |
| 端到端安全示例 | `examples/issue-002-payment-api/`（design / execution-plan / threat-model / spec-for-validation） | ✅ 已补齐（PR-2） |
| spec-for-validation 安全场景 | `core/templates/ai/spec-for-validation.md`（`[安全与权限 security]`） | ✅ 已落地 |
| 安全文档收敛 | 删冗余 summary、保留 `security-guide.md` + 本文 | ✅ 已落地（PR-2） |
| **present optional artifact 的结构校验自动化** | `validate-artifacts-contract.py`（新增 Level B2：present optional artifact 按 `required_sections` 校验）；threat-model / spec-for-validation 已声明 `required_sections` | ✅ 已落地（PR-2，惠及 threat-model 与 spec-for-validation） |
| 安全操作指南 | `docs/security-guide.md` | ✅ 已落地（`1e99c33`） |

**一句话**：两层安全均已落地并契约化——Tier 1（`安全基础检查`）为 design 条件章节；Tier 2（`threat-model`）已登记为 optional bypass artifact、router 可达、触发统一、有端到端示例，且**结构校验已自动化**（present optional artifact 按 `required_sections` 校验，惠及 `spec-for-validation`）。

---

## 7. 关键文件

| 关注点 | 路径 |
|---|---|
| 安全基础检查模板（Tier 1） | `core/templates/ai/design.md`（`## 安全基础检查` 条件章节） |
| 安全基础检查触发逻辑 | `core/skills/odk-design/SKILL.md`（步骤 6） |
| threat-model 模板（Tier 2） | `core/templates/ai/threat-model.md` |
| threat-model skill | `core/skills/odk-security-threat-model/SKILL.md` |
| 触发维度定义 | `core/skills/odk-propose/SKILL.md`（8 维 `安全/权限`） |
| 条件章节契约（真相源） | `core/contracts/artifacts.yaml`（design `conditional_sections`） |
| 条件章节读取机制 | `scripts/lib/odk_yaml.py`、`scripts/check-examples.sh` |
| 验证层安全场景 | `core/templates/ai/spec-for-validation.md`（`[安全与权限 security]`） |
| 操作层检查清单 / STRIDE 步骤 / 合规 | `docs/security-guide.md` |

---

## 8. 使用指引

- **什么时候会看到「安全基础检查」**：当你在 propose 阶段把 `安全/权限` 标为「是」（或变更确实碰了 IPC / 敏感数据 / 加密认证），design 阶段会自动展开该章节要求你填。
- **什么时候跑 threat-model**：上面的轻量检查暴露出高风险信号（敏感数据、网络暴露面、认证授权变更、合规要求）时，运行 `/odk-security-threat-model` 生成独立的 `threat-model.md`；design 里的「深度威胁分析（如需）」小节负责记录这个升级决定。
- **怎么和验收衔接**：threat-model 的 P0/P1 缓解措施应落到 execution-plan 的 Task，并在 spec-for-validation 的 `[安全与权限 security]` 场景里被验证（追到 AC）。

---

## 9. 后续（roadmap）

PR-2 已落地：threat-model 契约登记（含 `required_sections`）、router 接线、触发术语 / 链路统一、端到端示例、文档收敛，**以及 present optional artifact 的结构校验自动化**（`validate-artifacts-contract.py` 新增 Level B2：threat-model / spec-for-validation 存在时按 `required_sections` 校验；空壳或缺 DFD/STRIDE 等核心章节会被拦）。

剩余仅深度语义层面（非结构）：threat-model 的威胁场景是否覆盖到位、缓解措施是否真正有效，仍靠人工审（issue-002 示例保留了 manual review gate 作为参照）。

---

## 10. 关联文档

- `docs/security-guide.md` —— 操作层：轻量检查清单、STRIDE 步骤、密码学黑白名单、合规检查表。
- `docs/designs/spec-for-validation.md` —— 旁路 artifact 的设计范式（threat-model 已在 PR-2 对齐该范式）。
- `docs/contracts.md` —— artifact 契约总览（含 8 维 `安全/权限` 分级判断）。
