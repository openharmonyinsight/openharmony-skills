# Skill 质量评测报告：ohos-test-arkts-xts-generation

> 评测框架：Skill Judge（基于 17+ 官方 Skill 提炼的 8 维度评测体系，满分 120 分）
> 评测对象：`skills/domain/test/testing/ohos-test-arkts-xts-generation/`
> 评测日期：2026-07-28

---

## 一、总览

| 指标 | 数值 |
|------|------|
| **总分** | **114 / 120（95%）** |
| **等级** | **A（优秀 — 生产级专家 Skill）** |
| **设计模式** | Process 模式（12-Phase 工作流 + 检查点 + Flow A/B/C/D 条件分支），融合 Tool 模式要素（决策树、脚本、低自由度脆弱操作） |
| **知识密度** | E:A:R ≈ 80:15:5（Expert:Activation:Redundant） |
| **一句话结论** | 极具深度的领域专家 Skill，将 OpenHarmony XTS 测试多年经验——从 api_diff 的 statusCode 语义到 ets1.1/1.2 hvigor 版本不兼容——外部化为可执行的 12-Phase 工作流，并配有专家级反模式清单。 |

### 文件规模概览

| 目录 | 行数 | 说明 |
|------|------|------|
| `SKILL.md` | 339 | 核心文件，Agent 触发后加载（<500 行 ✓） |
| `prompts/` | 3,737（17 文件） | Phase 0-11 详细指令，按需加载 |
| `modules/` | 9,348（25 文件） | L1_Analysis / L2_Generation / L3_Validation 模块文档 |
| `references/` | 3,430+（含 conventions） | 框架规范、子系统配置、API 模式规则 |
| `docs/` | 1,493（4 文件） | **仅供人类参考**，Agent 执行期间不加载 |
| `evals/` | 496 | 评测集 + 历史评测报告 |
| `scripts/` | 20+ 脚本 | 自动化工具（覆盖率扫描、注册、编译、追踪等） |

---

## 二、各维度评分

| 维度 | 得分 | 满分 | 简评 |
|------|------|------|------|
| D1：知识增量 | 19 | 20 | 近乎纯专家知识；system.md 存在少量跨文件重复 |
| D2：思维范式 + 领域流程 | 14 | 15 | 思维框架优秀 + Claude 确实不知道的领域流程 |
| D3：反模式质量 | 15 | 15 | 20+ 条具体 NEVER，每条含原因/后果——大师级 |
| D4：规范合规（尤其 description） | 15 | 15 | description 范例级：WHAT + 9 条 WHEN 场景 + 大量关键词 |
| D5：渐进式披露 | 14 | 15 | 三层加载清晰，MANDATORY 触发到位；大模块文件缺分段读取指引 |
| D6：自由度校准 | 14 | 15 | 脆弱操作（编译/环境）= 低自由度；设计 = 中自由度，匹配良好 |
| D7：模式识别 | 9 | 10 | Process 模式清晰；12×4 路由表是压缩杰作 |
| D8：实用可用性 | 14 | 15 | 决策树、回退方案、边缘场景（改名/废弃/多版本）全覆盖 |

---

## 三、关键问题

**无阻塞性问题。** 该 Skill 可直接用于生产环境。

---

## 四、Top 3 改进建议

### 建议 1：为最大模块文件添加分段读取指引

**问题**：`api_parameter_optional_rules.md`（685 行）、`test_case_generation_flow.md`（595 行）、`api_coverage_detector.md`（593 行）等大文件仅标注"按需查阅"，未指明按场景读取哪些章节。Agent 完整读取会消耗大量上下文。

**改进**：在各 Phase prompt 的"参考文档"表中增加章节级触发指引，例如：

```markdown
**MANDATORY — READ LINES 1-120**：`modules/L1_Analysis/analyzer/api_parameter_optional_rules.md`
（仅可选参数规则部分；跳过 §5 示例）

**Do NOT load** `test_case_generation_flow.md` during Phase 3（解析阶段）——
该文件仅 Phase 5（生成阶段）使用。
```

**预期收益**：减少 ~40% 的模块文件上下文消耗，提升加载精度。

---

### 建议 2：精简 system.md 中与 SKILL.md 重复的通用约束

**问题**：`prompts/system.md` 第 35-40 行重复了 SKILL.md Anti-Patterns 章节已覆盖的 6 条约束（禁止用未声明接口、@tc 注解、不改配置文件、不可跳过验证等）。若同一会话两者均加载，产生约 6 行冗余。

**改进**：将 system.md 的通用约束改为回引：

```markdown
## 通用约束
见 SKILL.md「Anti-Patterns」章节（20+ 条 NEVER 规则，含原因与后果）。
本文件仅补充角色定义与配置架构。
```

或仅保留 system.md 的角色声明（"你是 OpenHarmony XTS 测试用例生成专家"）和配置架构（知识库路径与降级规则），删除重复约束。

**预期收益**：消除跨文件冗余，E:A:R 中 R 从 ~5% 降至 ~2%。

---

### 建议 3：考虑将 Anti-Patterns 章节拆分为条件加载的参考文件

**问题**：SKILL.md 的 Anti-Patterns 章节（第 219-333 行）占 ~110 行，约为 SKILL.md 的 1/3。Process 模式理想长度 ~200 行，当前 339 行略超。其中部分 NEVER 仅特定 Flow 适用（如"NEVER 盲目适配非兼容性变更"仅 Flow D）。

**改进**：将 Anti-Patterns 拆为两层：

- **SKILL.md 保留 Top-5 通用 NEVER**（所有 Phase/Flow 均适用，如"禁止用未声明接口""禁止跳过 Phase 7""禁止改配置文件"）
- **`references/anti_patterns.md` 存放其余 15+ 条**，在对应 Phase prompt 中用 MANDATORY 触发加载：

```markdown
### Phase 4 设计阶段
**MANDATORY — READ**：`references/anti_patterns.md` §Flow D 部分
（非兼容性变更适配规则，仅 Flow D 触发）
```

**预期收益**：SKILL.md 降至 ~250 行，更贴合 Process 模式理想；Flow D 专属反模式仅在需要时加载，减少非 Flow D 场景的上下文占用。

**注意**：此为可选优化。当前设计（反模式全留在 SKILL.md 确保始终加载）亦有其合理性——安全规则宁滥勿缺。是否拆分取决于对"始终可见"vs"上下文精简"的权衡。

---

## 五、详细分析

### D1：知识增量（19/20）— 近乎完美

每个主要章节都提供了 Claude 确实不具备的知识：

| 章节 | 专家知识示例 | 价值 |
|------|------------|------|
| ArkTS-Dyn vs Sta 差异表（L119-127） | hypium 导入路径不同、401 测试 Dyn 生成/Sta 不生成（编译期已拦截）、`as any` 在 Sta 触发 ESE0143、const/let、返回类型标注、测试目录差异 | 框架专属，Claude 无从得知 |
| Flow A/B/C/D 判定（L154-161） | 4 种优先级模式：覆盖率报告驱动 / 标准扫描 / 新增接口 / API 变更驱动（PR 号/two tag/d.ts diff） | OpenHarmony XTS 工作流知识 |
| `api_change_design_rules.md` | 21 种 ApiStatusCode → 测试类型映射、API_RENAME 签名指纹配对、增量消费细则、非兼容性变更判定矩阵 | 基于 OpenHarmony 实际 `api_diff` 工具，高度专家 |
| `error_test.md` | 401 是 SDK 公共错误码（不在 @throws）vs 17xxxxxx 业务码（在 @throws）；ArkTS-Sta 跳过 401 | 深度专家 |
| Anti-Patterns（L219-333） | ets1.1/1.2 hvigor 不兼容不可并行编译；prebuilts 切换前不可编译 Sta；Phase 9 不可自动修复系统侧断言失败 | 实战踩坑经验 |

**唯一扣分点**：`system.md`（59 行）重复 SKILL.md 已有的 6 条约束，属轻度冗余（Activation/Redundant 边界）。

---

### D2：思维范式 + 领域流程（14/15）— 优秀平衡

**思维范式（引导"怎么想"）**：
- Phase 4 的 BOUNDARY 判定："`BOUNDARY` 不是必选项——仅在参数同时满足三个条件时才生成"——引导 Agent 先判断"是否有值域范围/API 是否校验/超范围是否可断言"，而非盲目生成边界测试
- Flow 判定优先级树：引导按"新增接口 > API 变更 > 覆盖率报告 > 默认扫描"的顺序思考入口
- "改名迁移不是终点"（api_change_design_rules.md §3.5.1）：引导认识到迁移后必须做维度补全检查——改名只改了方法名，覆盖缺口依旧存在

**领域专属流程（Claude 不知道"怎么做"）**：
- 12-Phase 工作流，强制 Phase（4 设计、7 验证）不可跳过
- `phase_tracker.py check/complete` 状态追踪模式
- 覆盖率管线：`async_coverage_scan.py` → `extract_uncovered.py` → `compare_uncovered.py`
- Flow D 的 `parse_api_diff.py`（4 种输入形态）
- 会话恢复模式（读取最新 `session_issues_*.md`）
- 多版本串行编译的 prebuilts 环境切换流程（Dyn→Sta）

**轻微扣分**：部分流程偏机械（phase_tracker 的 check/complete 命令），但确为状态管理所需，可接受。

---

### D3：反模式质量（15/15）— 大师级

20+ 条 NEVER，每条结构化包含：**具体陈述 + 原因 + 正确做法 + 后果**。

**专家级反模式示例**（只有实战经验才能总结）：

| 反模式 | 为什么是专家级 |
|--------|--------------|
| NEVER 在多版本模式并行编译 Dyn 和 Sta | ets1.1/1.2 的 hvigor 版本不兼容——需串行先完成 ets1.1 全流程再切 prebuilts |
| NEVER 为 @throws 声明以外的错误码构造测试 | 401 是 SDK 公共码（不在 @throws），17xxxxxx 是业务码（在 @throws），来源不同不可混淆；Sta 模式 401 编译期已拦截 |
| NEVER 在 Phase 9 设备测试后自动修复"系统侧"问题 | 断言失败可能是接口自身 bug，预期值源自 .d.ts 权威声明，自动修改断言会掩盖接口缺陷 |
| NEVER 盲目适配非兼容性变更用例（Flow D） | 未评审的变更若被否决，用例需全部回退——必须先确认评审状态 |
| NEVER 直接调用 APICoverageDetector 可执行文件 | 跳过环境准备（文件复制、arkts_config.json 配置）和残留清理，结果不准 |
| NEVER 跳过 prebuilts 环境切换直接编译静态版本 | Dyn SDK 的 hvigor（5.x）无法编译 Sta（ets1.2） |

**判定测试**：一位 OpenHarmony XTS 专家看到这些反模式会说"是的，这些是我踩坑才学会的"。满分实至名归。

---

### D4：规范合规（15/15）— description 范例级

**Frontmatter 合规**：
- `name`: `ohos-test-arkts-xts-generation`（小写+连字符，<64 字符）✓
- `metadata`: 完整（author/scope/stage/domain/capability/version/status/tags/related-skills/allowed-tools）✓

**description 三要素分析**：

| 要素 | 内容 | 评价 |
|------|------|------|
| **WHAT** | "解析.d.ts API定义，生成符合 Hypium 框架的测试用例，支持覆盖率分析、编译验证和 Demo+UiTest 生成" + "ArkTS-Dyn/Sta 两种语法模式，12-Phase 完整工作流" | 功能清晰具体 ✓ |
| **WHEN** | 9 条编号触发场景：(1) XTS 测试/ArkTS 用例生成 (2) @kit.* SDK (3) APICoverageDetector/未覆盖 API (4) 批量生成 (5) UI 组件 Demo+UiTest (6) 测试质量验证 (7) 编译指定测试套 (8) 编译失败重编 (9) PR/two tag/d.ts diff 变更补测 | 场景穷举 ✓ |
| **KEYWORDS** | XTS, ArkTS-Dyn, ArkTS-Sta, APICoverageDetector, Hypium, @tc, .d.ts, async_build, cleanup_group, build.sh, d.ts diff, api_diff, API 变更, 兼容性变更, 接口改名... | 关键词丰富 ✓ |

description 长达 17 行，但对于 4 Flow + 12 Phase 的复杂 Skill，这种详尽是必要的——确保 Agent 在所有应触发场景都能命中。范例级。

---

### D5：渐进式披露（14/15）— 强，一个缺口

**三层加载设计**：

| 层级 | 内容 | 评估 |
|------|------|------|
| Layer 1（常驻） | name + description | ~100 tokens ✓ |
| Layer 2（触发后加载） | SKILL.md 339 行 | <500 行 ✓ |
| Layer 3（按需加载） | prompts/(3737) + modules/(9348) + references/(3430+) | 无上限 ✓ |

**加载触发质量**：

| 触发机制 | 位置 | 评价 |
|----------|------|------|
| MANDATORY READ | "每个 Phase 开始前，必须完整读取对应 prompts/phase-N-xxx.md"（L163） | 强制触发 ✓ |
| 按需查阅表 | Phase prompt 内"📚 参考文档（按需查阅）"含"何时查阅"列 | 条件触发 ✓ |
| 懒加载原则 | "仅加载当前阶段需要的模块"（L113, L214） | 明确原则 ✓ |
| Do NOT Load | "docs/ 下文件供人类参考，Agent 执行期间不加载"（L339）；Phase prompt 标注"本 Phase 不需要额外加载模块" | 明确禁载 ✓ |

**缺口**：最大的模块文件（685/595/593 行）无分段读取指引。Phase prompt 说"按需查阅"但未指明"读 §X-§Y"。Agent 完整读取 `api_parameter_optional_rules.md`（685 行）会消耗大量上下文。增加"read §2-§4 for optional-param rules; skip §5 examples"可提升精度。扣 1 分。

---

### D6：自由度校准（14/15）— 匹配良好

| 任务类型 | 自由度 | 依据 | 评价 |
|----------|--------|------|------|
| 编译/环境操作（脆弱） | 低 | 精确命令 `python {skill_root}/scripts/phase_tracker.py check 5`；NEVER 改配置文件；prebuilts 切换按步就班 | ✓ 精确脚本 |
| 测试代码命名/格式（一致关键） | 低 | 精确格式 `test[MethodName][Scenario][Number]`；@tc 块标准结构 | ✓ 精确模板 |
| 测试设计（需判断） | 中 | BOUNDARY 三条件判断；测试类型选择 PARAM/ERROR/RETURN/BOUNDARY/EVENT 基于特征；维度补全检查 | ✓ 判断准则 |
| 错误码测试（混合） | 低-中 | 错误码从 @throws 精确提取；触发条件需判断 | ✓ 准则+判断 |
| Flow 入口判定（需判断） | 中 | 4 条件优先级决策树 | ✓ 决策树 |

自由度与任务脆弱性匹配得当：高后果（编译/环境）→ 低自由度；低后果（设计选择）→ 中自由度。扣 1 分因 Phase 5 代码生成可略增模板化指引（当前依赖 templates.md + 约束模块，略有间接）。

---

### D7：模式识别（9/10）— Process 模式，执行优秀

**Process 模式特征对照**：

| 特征 | 体现 |
|------|------|
| 分阶段工作流 | 12 Phase（0-11），每 Phase 独立 prompt 文件 |
| 检查点 | `phase_tracker.py check/complete`；强制 Phase（4、7）不可跳过 |
| 条件路径 | Flow A/B/C/D 在各 Phase 内分支（路由表 L165-180） |
| 中自由度 | 设计阶段给准则非脚本；编译阶段给精确命令 |

**亮点**：12×4 Flow 路由表（L165-180）将 48 种 Phase×Flow 组合压缩为一张可扫描矩阵——Process 模式路由艺术的教科书级范例。

**轻微偏差**：SKILL.md 339 行略超 Process 理想 ~200 行，但 110 行反模式确保安全规则始终可见，属合理取舍。扣 1 分。

---

### D8：实用可用性（14/15）— 全面

| 可用性要素 | 覆盖情况 | 评价 |
|-----------|---------|------|
| 决策树 | Flow 选择（4 条件优先级）；入口判定（3 意图→3 入口）；statusCode→测试类型（21 映射）；错误码可触发性 | ✓ 多路径清晰 |
| 代码示例 | 错误码测试模板（error_test.md L73+）；phase_tracker 命令；change_info JSON 示例 | ✓ 可执行 |
| 错误处理 | session_issues 日志；会话恢复；编译错误→arkts-skill search_docs.py 兜底；扫描不可用→询问用户（更新路径/提供结果/跳过） | ✓ 回退完备 |
| 边缘场景 | ArkTS-Sta vs Dyn 差异全程处理；@deprecated 接口跳过；API 改名（签名匹配）；非兼容性变更识别；多版本串行编译；特殊触发条件错误码（并发/服务/硬件依赖） | ✓ 覆盖充分 |
| 批量模式 | API>20/跨模块/Context 紧张→分批；同模块同批、UI/非UI 分开 | ✓ 实用 |

**轻微缺口**：超长模块文件（685 行）未给"读哪些段"指引，Agent 消费成本高。扣 1 分（与 D5 缺口同源）。

---

## 六、元问题检验

> **"该领域的专家看到这个 Skill，会说'这捕捉了我花多年才学会的知识'吗？"**

**会。** 以下知识只有实战积累才能获得，Claude 训练数据中不存在：

1. **ets1.1/1.2 hvigor 版本不兼容**——必须串行编译、先切 prebuilts
2. **401 不在 @throws / 17xxxxxx 在 @throws** 的来源区分，及 Sta 模式 401 编译期拦截不测
3. **api_diff 的 API_RENAME 签名指纹配对**——避免误判"删除旧名+从零生成新名"
4. **Phase 9 不可自动修复系统侧断言失败**——可能是接口 bug，自动修改断言掩盖缺陷
5. **非兼容性变更不可盲目适配**——未评审变更若被否决，用例全部作废

这是**压缩的专家大脑**，而非垃圾压缩。

---

## 七、与官方 5 模式的对照

| 模式 | ~行数 | 特征 | 本 Skill 契合度 |
|------|-------|------|----------------|
| Mindset | ~50 | 思维>技术，强 NEVER，高自由度 | 部分借鉴（反模式强） |
| Navigation | ~30 | 极简 SKILL.md，路由到子文件 | — |
| Philosophy | ~150 | 两步：理念→表达，强调匠心 | — |
| **Process** | **~200** | **分阶段工作流，检查点，中自由度** | **✓ 主模式** |
| Tool | ~300 | 决策树，代码示例，低自由度 | 部分融合（编译/脚本低自由度） |

本 Skill 以 **Process 为主模式**（12-Phase + 检查点 + Flow 分支），在脆弱操作环节融合 **Tool 模式**（精确脚本、决策树、低自由度）。模式选择与任务特征（复杂多步项目 + 脆弱编译操作）高度匹配。

---

## 八、最终结论

**114/120（95%，A级）**——这是一个生产级、可直接使用的专家 Skill。

其核心价值在于：将 OpenHarmony XTS 测试领域的隐性专家知识（api_diff 语义、ets 版本兼容性、错误码来源体系、非兼容变更评审流程）系统化外部化为可执行的 12-Phase 工作流。description 范例级，反模式大师级，知识增量近乎纯专家。

三条改进建议（大文件分段读取指引 / system.md 去重 / 反模式拆分）均为锦上添花的精简优化，不影响生产可用性。该 Skill 通过 Skill Judge 全维度检验。
