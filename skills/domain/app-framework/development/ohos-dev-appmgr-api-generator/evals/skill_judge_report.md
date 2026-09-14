# Skill 质量评测报告：ohos-dev-appmgr-api-generator

> 评测框架：Skill Judge（基于 17+ 官方 Skill 提炼的 8 维度评测体系，满分 120 分）
> 评测对象：`skills/domain/app-framework/development/ohos-dev-appmgr-api-generator/`
> 评测日期：2026-09-08

---

## 一、总览

| 指标 | 数值 |
|------|------|
| **总分** | **99 / 120（82.5%）** |
| **等级** | **B+（良好 — 可投入生产，有改进空间）** |
| **设计模式** | Tool 模式（脚本驱动代码生成 + 精确路径文档 + 低自由度脆弱操作），以确定性 Python 脚本为核心，references 提供手工补全指引 |
| **知识密度** | E:A:R ≈ 70:25:5（Expert:Activation:Redundant） |
| **一句话结论** | 一个实用、可投产的 AppMgr IPC 代码生成器，将 12 文件调用链的机械性劳动外部化为确定性脚本。在 AppMgrResultCode 跨层传输契约、sptr broker 封送差异等专家知识上表现出色，但缺乏深层踩坑经验和条件决策树，反模式不够结构化。 |

### 文件规模概览

| 目录 | 行数 | 说明 |
|------|------|------|
| `SKILL.md` | 65 | 核心文件，Agent 触发后加载（<500 行 ✓，极为精简） |
| `scripts/` | 1,159（1 文件） | `generate_appmgr_api.py` — 确定性代码生成器，含输入校验、枚举扫描、5 种返回类型分支 |
| `references/` | 454（2 文件） | `patterns.md`（封送模式表 + 错误码表）+ `files.md`（12 文件路径 + 插入点 + checklist） |
| `evals/` | 712（2 文件） | 20 用例 / 70 断言 / 100% 通过率 + HTML/JSON/MD 三格式报告 |

---

## 二、各维度评分

| 维度 | 得分 | 满分 | 简评 |
|------|------|------|------|
| D1：知识增量 | 16 | 20 | AppMgrResultCode 跨层契约 + 宏选择规则 + sptr 封送差异是真实专家知识；但缺乏"只有踩坑才能知道"的深层经验 |
| D2：思维范式 + 领域流程 | 11 | 15 | 5 步线性工作流清晰可执行；但缺乏条件分支决策树，流程本质是"跑脚本+贴输出" |
| D3：反模式质量 | 11 | 15 | ~10 条 pitfall 含原因+后果；但散落在 3 个文件中，未集中为 NEVER 章节，结构化不足 |
| D4：规范合规 | 13 | 15 | frontmatter 完整、description 含 WHAT+WHEN+触发词、放置规范正确；关键词密度可更丰富 |
| D5：渐进式披露 | 13 | 15 | 三层加载清晰，SKILL.md 仅 65 行极精简；但缺条件加载指引（何时读哪个 reference） |
| D6：自由度校准 | 14 | 15 | 脆弱操作（代码生成/路径）= 低自由度脚本；业务逻辑 = 高自由度 TODO；校准得当 |
| D7：模式识别 | 9 | 10 | Tool 模式选择正确，脚本为核心；未显式声明模式选型理由 |
| D8：实用可用性 | 12 | 15 | 示例全面、脚本 fail-closed、20 用例验证；缺恢复指引和 variation 深度 |

---

## 三、关键问题

**无阻塞性问题。** 该 Skill 可直接用于生产环境，脚本生成的代码经过 5 轮检视修复和 20 用例 70 断言验证。

---

## 四、Top 3 改进建议

### 建议 1：集中反模式为结构化 NEVER 章节

**问题**：当前 ~10 条 pitfall/anti-pattern 散落在 3 个文件中——SKILL.md 的 Implementation Notes（4 条）、files.md 的 Common Pitfalls（6 条）、patterns.md 的 Variations（3 条）。每条虽含原因和后果，但未采用"具体陈述 + 原因 + 正确做法 + 后果"四段式结构，且分散读取增加了 Agent 的上下文管理成本。

**改进**：在 SKILL.md 新增 `## Anti-Patterns` 章节，集中 Top-5 通用 NEVER（所有 API 均适用），格式如下：

```markdown
## Anti-Patterns

### NEVER hand-edit AppMgrResultCode back into proxy/interface/service signatures
- **原因**: AppMgrResultCode 是 Client 专属 enum；IPC 层传输 int32_t
- **正确做法**: 仅 Client 返回 enum，其余层保持 int32_t
- **后果**: 手动改回 enum 导致 int32_t 传输契约断裂，编译错误或语义偏移

### NEVER use _RET_INT macro for bool/std::string return types
...（同上四段式）
```

将其余 pitfall 保留在 `references/files.md` Common Pitfalls 中，SKILL.md 中用"详见 files.md §Common Pitfalls"引用。

**预期收益**：反模式从分散→集中、从散文→结构化，安全规则始终可见，降低 Agent 遗漏风险。

---

### 建议 2：为 references 增加条件加载指引

**问题**：SKILL.md 仅在末尾用两行链接引用 `files.md` 和 `patterns.md`，未指明"何时读哪个"。Agent 可能一次性加载全部 references（454 行），也可能不读就尝试应用 snippet。对于 65 行的极简 SKILL.md，缺少"在 Workflow 第 3 步读 files.md、在理解宏选择时读 patterns.md"的条件触发。

**改进**：在 Workflow 步骤中嵌入 MANDATORY/按需标注：

```markdown
## Workflow

1. Collect API signature (name, return type, params, async) from the user.
2. Run `scripts/generate_appmgr_api.py` to generate all snippets.
3. Apply each snippet to its target file.
   **MANDATORY — READ**: `references/files.md`（12 文件精确路径 + 插入点 + checklist）
4. For the stub, three artifacts are produced ...
5. Fill in the business logic ...
   **按需查阅**: `references/patterns.md` §Variations（当需要 nullable sptr / Parcelable / vector 时）
```

**预期收益**：Agent 在正确的步骤加载正确的 reference，减少 ~30% 非必要上下文加载。

---

### 建议 3：补充 variation 深度与恢复指引

**问题**：`patterns.md` 的 Variations 章节列出了 4 种生成器不覆盖的场景（nullable sptr、Parcelable、async task queue、XCOLLIE_TIMER），但每项仅一行描述 + "Add by hand"，缺乏可操作的代码模板。例如 nullable sptr 仅说"real code writes a bool sentinel before the optional object"，未给出 sentinel 读写对称代码。此外，脚本中途失败（如枚举文件格式变化）后无恢复指引。

**改进**：

1. 为每种 variation 提供最小代码模板：

```markdown
### Nullable sptr (optional broker parameter)

```cpp
// Proxy: write bool sentinel + optional object
data.WriteBool(hasObserver);
if (hasObserver) {
    PARCEL_UTIL_WRITE_RET_INT(data, RemoteObject, observer->AsObject());
}

// Stub: read sentinel, conditionally read object
bool hasObserver = false;
if (!data.ReadBool(hasObserver)) return ERR_INVALID_VALUE;
sptr<IXxx> observer;
if (hasObserver) {
    observer = iface_cast<IXxx>(data.ReadRemoteObject());
    if (!observer) return ERR_INVALID_VALUE;
}
```
```

2. 在 SKILL.md 补充恢复指引：

```markdown
## Failure Recovery

- **Script rejects input**: fix the input and re-run — no partial state.
- **Enum file format changed**: script exits with a diagnostic; inspect
  `app_mgr_ipc_interface_code.h` manually and pick a code by hand.
- **Snippet already partially applied**: use `git diff` to identify
  applied vs. pending snippets; apply remaining ones from the script output.
```

**预期收益**：覆盖从"知道不能做"到"知道怎么做"的最后一公里，减少 Agent 遇到 variation 时的卡顿。

---

## 五、详细分析

### D1：知识增量（16/20）— 良好，但缺深层踩坑

每个主要章节都提供了 Claude 训练数据中不具备的知识：

| 章节 | 专家知识示例 | 价值 |
|------|------------|------|
| Return-type contract（SKILL.md:58） | AppMgrResultCode 是 Client 专属 enum；IPC 层传输 int32_t；Stub 写 `WriteInt32(result)` 无需 enum cast | 框架专属架构契约 ✓ |
| Macro choice（SKILL.md:59） | void→`_NORET`；int32_t+AppMgrResultCode→`_RET_INT`；bool/std::string→explicit Write + SendRequest wrapper（因 `_RET_INT` 返回 int 无法转换） | 类型安全推理 ✓ |
| sptr accessor（patterns.md:116-120） | `sptr<IRemoteObject>` 用 `GetRefPtr()`；`sptr<IXxx broker>` 用 `->AsObject()`（GetRefPtr 得到接口指针而非 IRemoteObject） | 真实代码惯例 ✓ |
| Stub dispatch（SKILL.md:51） | `OnRemoteRequestInner()` fan-out 到 N 个函数（当前至 Ninth）；新 code 加入对应分组 | 代码结构知识 ✓ |
| Parcel validation（SKILL.md:60） | bool-form `ReadXxx(value)` + `ERR_INVALID_VALUE`（非默认值形） | 安全编码实践 ✓ |
| Null guard（SKILL.md:60） | sptr 参数在 dereference 前判空；Stub `iface_cast`/`ReadRemoteObject` 结果判空 | UB 防御 ✓ |
| Enum scanning（脚本） | `_scan_ipc_enum()` 解析 enum body，收集所有 enumerator name（含表达式/隐式值），fail-closed 选择 next code | 自动化工具 ✓ |

**扣分点（4 分）**：

1. 缺乏"只有实战踩坑才能获得"的深层经验。对比 XTS skill 的"ets1.1/1.2 hvigor 版本不兼容不可并行编译"或"Phase 9 不可自动修复系统侧断言失败"——这些是只有经历才能总结的。本 skill 的知识更多来自"读代码"而非"踩坑"。

2. Variations 章节（patterns.md:222-229）列出 4 种不支持场景，但每项仅一行，未展开为可操作模板。

**判定测试**：一位 AppMgr 开发者看到这个 skill 会说"是的，这些是我读代码后总结的规则"——而非"这些是我踩坑才学会的"。差距在于经验的深度。

---

### D2：思维范式 + 领域流程（11/15）— 流程清晰但线性

**思维范式（引导"怎么想"）**：
- Return-type contract 思维："AppMgrResultCode 是 client-facing 的，IPC 层用 int32_t"——引导 Agent 理解 IPC 边界
- 宏选择推理："为什么 _RET_INT 不能用于 bool"——引导理解类型安全
- 但缺乏条件决策树：没有"如果参数是 X 则走 Y 路径"的分支思维

**领域专属流程（Claude 不知道"怎么做"）**：
- 5 步工作流：collect → run script → apply snippets → stub 3 artifacts → fill TODO ✓
- 脚本驱动的确定性生成 ✓
- 12 文件精确路径 + 插入点 ✓
- IPC enum 扫描 + next-free-code 选择 ✓
- Stub dispatch fan-out 读取 ✓

**扣分点（4 分）**：

1. 流程本质是线性的"跑脚本+贴输出"，缺乏条件分支。对比 XTS skill 的 Flow A/B/C/D/E 五路条件决策树，本 skill 的 5 步始终走同一条路径。

2. Workflow 中步骤 3（apply snippets）是最容易出错的环节（12 文件、12 snippet、不同插入点），但 SKILL.md 仅一句"apply each snippet to its target file (see references/files.md for exact paths and insertion guidance)"——将全部复杂度委托给 reference，未在主文件中提供任何 guardrail。

**对比**：XTS skill 有 12 Phase × 5 Flow = 60 种组合的路由表。本 skill 有 1 条路径。简单性是优点（Tool 模式不需要复杂路由），但在思维引导上深度不足。

---

### D3：反模式质量（11/15）— 有覆盖但不够结构化

共 ~10 条 pitfall/anti-pattern，分布在 3 个文件：

| 位置 | 条数 | 示例 |
|------|------|------|
| SKILL.md Implementation Notes | 4 | "Async forces void"、"do NOT hand-edit signatures back"、"do not hand-edit to _RET_INT for bool/string"、"do not inline stub case bodies" |
| files.md Common Pitfalls | 6 | "Return type mismatch"、"Wrong macro"、"Async with non-void"、"Missing static_cast"、"Inlining case bodies"、"Wrong stub file" |
| patterns.md Variations | 3 | "Nullable sptr"、"Parcelable/vector rejected"、"XCOLLIE_TIMER" |

**质量分析**：

每条 pitfall 包含**原因**和**后果**，例如：
- "Using _RET_INT for bool/std::string causes compile errors or wrong semantics (e.g. negative error code → true for bool)" ✓ 原因+后果
- "do NOT hand-edit signatures back to AppMgrResultCode or the int32_t transport contract breaks" ✓ 后果

但与 XTS skill 的四段式（"具体陈述 + 原因 + 正确做法 + 后果"）相比：
- 缺少**正确做法**段（仅说"不要做X"，未说"应该做Y"）
- 未集中为独立 NEVER 章节，散落在 3 个文件的散文段落中
- 无优先级排序（哪些是编译级 fatal，哪些是风格建议）

**扣分点（4 分）**：结构化不足（散落 + 无四段式）、数量偏少（~10 vs XTS 的 20+）、缺正确做法段。

---

### D4：规范合规（13/15）— frontmatter 完整，description 可更密

**Frontmatter 合规**：

| 字段 | 值 | 评价 |
|------|------|------|
| `name` | `ohos-dev-appmgr-api-generator` | ✓ 匹配目录名 |
| `description` | 3 句覆盖 WHAT + WHEN + 触发词 | ✓ 良好 |
| `metadata.author` | `openharmony` | ✓ |
| `metadata.scope` | `domain` | ✓ 匹配 domain 前缀 |
| `metadata.stage` | `development` | ✓ 匹配目录 `development/` |
| `metadata.domain` | `app-framework` | ✓ 匹配目录 `app-framework/` |
| `metadata.capability` | `appmgr-api-generator` | ✓ |
| `metadata.version` | `0.1.0` | ✓ |
| `metadata.status` | `draft` | ✓ 反映成熟度 |
| `metadata.tags` | 5 个 | ✓ 有检索价值 |

**description 三要素分析**：

| 要素 | 内容 | 评价 |
|------|------|------|
| **WHAT** | "Generate the complete API implementation chain from AppMgrClient to AppMgrServiceInner" + "12 files" | 功能清晰 ✓ |
| **WHEN** | "Use when adding a new IPC API that requires code across these 12 files" + 3 条触发短语 | 场景明确 ✓ |
| **KEYWORDS** | AppMgrClient, AppMgrServiceInner, app_mgr_client, app_mgr_proxy, IPC, AppMgrInterfaceCode | 有关键词 ✓ |

**扣分点（2 分）**：

1. description 可更密——缺少 `PARCEL_UTIL`、`Handle dispatch`、`OnRemoteRequestInner`、`AppMgrResultCode` 等会出现在用户请求中的关键词。
2. 未列出 12 个具体文件名（description 中仅说"these 12 files"，实际文件名在 description 中列举会提升路由命中率）。

---

### D5：渐进式披露（13/15）— 极精简但缺条件触发

**三层加载设计**：

| 层级 | 内容 | 评估 |
|------|------|------|
| Layer 1（常驻） | name + description | ~100 tokens ✓ |
| Layer 2（触发后加载） | SKILL.md 65 行 | 极精简 ✓（远低于 500 行上限） |
| Layer 3（按需加载） | patterns.md(229) + files.md(225) + 脚本(1159) + evals(712) | 无上限 ✓ |

**加载触发质量**：

| 触发机制 | 位置 | 评价 |
|----------|------|------|
| 链接引用 | SKILL.md:65 "See references/files.md..." + "See references/patterns.md..." | 有引用 ✓ |
| Workflow 步骤→reference | 缺失 | ✗ 未在步骤中嵌入"何时读哪个 reference" |
| Do NOT Load | 缺失 | ✗ 未标注"执行期间不需要完整读取脚本" |

**扣分点（2 分）**：SKILL.md 极精简（65 行）是优点，但也导致它将全部应用复杂度委托给 references，未在步骤中指明"第 3 步读 files.md、理解宏选择时读 patterns.md"。

---

### D6：自由度校准（14/15）— 校准得当

| 任务类型 | 自由度 | 依据 | 评价 |
|----------|--------|------|------|
| 代码生成（脆弱） | 低 | 确定性脚本 `python generate_appmgr_api.py <root>` | ✓ 精确脚本 |
| Snippet 应用（一致关键） | 低 | 12 文件精确路径 + 插入点 + 12 项 checklist | ✓ 精确路径 |
| Stub dispatch 分组（需判断） | 中 | "Read the current fan-out...pick the OnRemoteRequestInnerN" | ✓ 判断准则 |
| 业务逻辑（需创造） | 高 | `// TODO: implement` — 刻意留给开发者 | ✓ 高自由度 |
| Variations（手工补全） | 中 | "Add by hand" + pattern reference | ✓ 模式参考 |

**扣分点（1 分）**：Stub dispatch 分组选择（"read the current fan-out and pick the group"）可更精确——例如"查找覆盖新 enum value 的 case range"而非泛泛"read the fan-out"。

---

### D7：模式识别（9/10）— Tool 模式正确

**Tool 模式特征对照**：

| 特征 | 体现 |
|------|------|
| 决策树 | 5 种返回类型 → 3 种宏路径（void/int32_t/bool+string），脚本内自动选择 |
| 代码示例 | patterns.md 含全部 5 种返回类型的 Proxy/Client/Stub 代码模板 |
| 低自由度 | 脚本处理生成；精确路径处理应用；仅业务逻辑留高自由度 |
| 脚本为核心 | 1159 行 Python 脚本是 skill 的核心资产 |

**模式选择理由**：代码生成任务是**确定性+重复性**的——12 文件、固定模式、每次相同结构。Tool 模式（脚本+精确路径+低自由度）是唯一正确选择。Process 模式（多阶段+条件分支）会过度设计。

**扣分点（1 分）**：未在 SKILL.md 显式声明"本 skill 采用 Tool 模式"并解释选型理由（XTS skill 有此自省）。

---

### D8：实用可用性（12/15）— 可用但缺恢复指引

| 可用性要素 | 覆盖情况 | 评价 |
|-----------|---------|------|
| 代码示例 | patterns.md 含 5 种返回类型完整 Proxy/Client/Stub 模板 + 封送表 | ✓ 全面 |
| 错误处理 | 脚本 fail-closed：非法参数 sys.exit(1)、枚举冲突 raise、目录伪装文件拒绝 | ✓ 强 |
| 边缘场景 | async 强制 void、nullable sptr、Parcelable/vector 拒绝、非 broker sptr 拒绝、enum 冲突检测 | ✓ 良好 |
| Checklist | files.md 12 项 checklist | ✓ 清晰 |
| Common pitfalls | files.md 6 项 | ✓ 实用 |
| Eval 验证 | 20 用例 / 70 断言 / 100% 通过（含 7 项 R5 修复验证） | ✓ 强 |
| 恢复指引 | **缺失** | ✗ 脚本失败后无恢复步骤 |
| Variation 深度 | 4 种 variation 各一行 | △ 浅 |

**扣分点（3 分）**：

1. 无失败恢复指引——脚本拒绝输入后如何重试？枚举格式变化后如何手工处理？部分 snippet 已应用后如何续传？
2. Variation 深度不足——nullable sptr / Parcelable / async task queue 各仅一行描述，无可操作模板。
3. 无"代码库已变化"的适应性指引——如 OnRemoteRequestInnerTenth 已出现时如何发现。

---

## 六、元问题检验

> **"该领域的专家看到这个 Skill，会说'这捕捉了我花多年才学会的知识'吗？"**

**部分会。** 以下知识确实需要读代码或经验才能获得：

1. **AppMgrResultCode 跨层 int32_t 传输契约**——需要理解 Client/IPC 边界才能正确设计
2. **`_RET_INT` 宏返回 int32_t 无法转换到 bool/string**——需要理解宏展开和类型安全
3. **sptr<IRemoteObject> 用 GetRefPtr() vs sptr<IXxx broker> 用 ->AsObject()**——需要阅读真实 AppMgr 代码
4. **Stub Handle* dispatch + OnRemoteRequestInnerN fan-out**——需要阅读 `app_mgr_stub.cpp` 结构
5. **bool-form ReadXxx + ERR_INVALID_VALUE（非默认值形）**——需要理解 parcel 安全编码

但以下知识更偏"机械总结"而非"踩坑经验"：

- 12 个文件路径（可从目录结构推断）
- camelCase 命名约定（通用 C++ 惯例）
- `static_cast<uint32_t>` for case labels（通用 IPC 知识）

**结论**：这是一个**高效的代码生成工具**，将读代码总结的规则外部化为确定性脚本。它不是"压缩的专家大脑"（如 XTS skill），而是"压缩的代码模板"——这在 Tool 模式下是合理的定位。

---

## 七、与官方 5 模式的对照

| 模式 | ~行数 | 特征 | 本 Skill 契合度 |
|------|-------|------|----------------|
| Mindset | ~50 | 思维>技术，强 NEVER，高自由度 | — |
| Navigation | ~30 | 极简 SKILL.md，路由到子文件 | 部分（65 行极简） |
| Philosophy | ~150 | 两步：理念→表达，强调匠心 | — |
| Process | ~200 | 分阶段工作流，检查点，中自由度 | — |
| **Tool** | **~300** | **决策树，代码示例，低自由度** | **✓ 主模式** |

本 Skill 以 **Tool 为唯一模式**：脚本为核心资产、精确路径+代码模板为辅助、低自由度处理脆弱操作、高自由度仅留业务逻辑。模式选择与任务特征（确定性代码生成）完全匹配。

---

## 八、最终结论

**99/120（82.5%，B+ 级）**——这是一个可投产的 Tool 模式代码生成 Skill。

**核心价值**：将 AppMgr IPC 12 文件调用链的机械性劳动（路径查找、宏选择、参数封送、stub dispatch）外部化为确定性 Python 脚本，消除了手写代码中的路径错误、宏选择错误和封送不对称风险。经过 5 轮检视修复（R1-R5）和 20 用例 70 断言验证，生成代码的编译安全性和 fail-closed 行为已得到充分证明。

**与 A 级（110+）的差距**：
1. D1 知识增量（-4）：缺深层踩坑经验，知识偏"读代码总结"而非"实战积累"
2. D2 思维范式（-4）：线性流程无决策树，思维引导深度不足
3. D3 反模式（-4）：散落非结构化，数量偏少，缺四段式
4. D5 渐进披露（-2）：缺条件加载指引
5. D8 实用性（-3）：缺恢复指引和 variation 深度

三条改进建议（集中反模式 / 条件加载指引 / variation 深度+恢复）可将总分提升至 ~107/120（A- 级）。该 Skill 通过 Skill Judge 全维度检验，推荐投入生产使用。
