---
name: doc-review
description: 工作流 Phase 6（合并文档+审查）——生成嵌入式 OS 适配文档、执行多维度代码审查、产出适配手册/API 参考/移植指南/审查报告。触发症状：用户说"写文档"、"代码审查"、"生成移植指南"、"8 维审查"、"交付物检查"。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: doc-review
  version: 0.1.0
  status: trial
  category: workflow-step-doc-review
---

# Phase 6: 文档与审查

> **本文件基于设计方法论校准。早期验证轮未实际执行到此阶段。**
> **★ P6 是子代理分发收益最大的阶段** — 宿主支持独立子代理会话时，6a(文档) 和 6b(审查) 必须派发给独立 Agent，以保证审查独立性（第二双眼睛原则）。单会话宿主不得伪造独立审查，必须记录 `UNVERIFIED_INDEPENDENCE`。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md` v0.1.0）

| 属性 | 值 |
|------|-----|
| **输入** | P1~P4 产出，以及 P5 的完成记录或 `SKIPPED_*` 状态；全部状态均须已写入 `verification_manifest` |
| **产出** | ① 芯片适配手册 ② API 参考文档 ③ 移植指南 ④ **8 维度代码审查报告** |
| **门控** | **GATE-R**：文档与独立代码审查均完成，Critical findings 已关闭，并完成一致性签署 |
| **特殊性** | 有独立会话能力时双 Agent 独立并行；否则记录 `UNVERIFIED_INDEPENDENCE`，GATE-R 不得 PASS |

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP：
- `get_conventions` — 查项目命名/架构/错误处理约定（审查对照）
- `impact_analysis` — 评估改动影响范围
- `get_call_graph` — 审查调用链合理性

> MCP 调失败或未装 → 按 skill 知识检索降级链回退。

## 子步骤

```
Step 6a: 文档生成 (doc-expert agent)
│   ├── 6a-1: 芯片适配手册 (Getting Started + Build + Flash + Run)
│   ├── 6a-2: API 参考文档 (每个 public 函数签名+参数+返回值)
│   └── 6a-3: 移植指南 (决策记录 + 已知限制 + 后续改进)
│
Step 6b: 代码审查 (ohos-dev-driver-review agent) ★ 宿主支持隔离会话时与 6a 完全并行
│   ├── 6b-1: 8 维度逐项检查
│   ├── 6b-2: 每个维度输出具体发现列表
│   └── 6b-3: 综合评分 + 改进建议
│
       ↓ (两者完成后合并；不支持隔离会话时标记 UNVERIFIED_INDEPENDENCE)
Step 6c: 交付物整合 + 最终检查
```

---

## Step 6a: 文档生成

### 6a-1: 芯片适配手册

**目标读者**: 第一次使用这个适配的开发者。

```markdown
# {Chip Model} Adapter for {Target OS} — Adaptation Manual

## 1. Prerequisites
- Toolchain: {prefix}gcc {version}
- {target_os} version: {version}
- Hardware: {board_name} development kit
- Host OS: {build_host}

## 2. Quick Start (5 分钟跑通)
```bash
# 1. Sync source
repo init -u {url} -b {branch}
repo sync -j$(nproc)

# 2. Configure
hb set -p {product} -t {type}

# 3. Build
./build.sh --product-name {product}
# Expected: exit 0, firmware in out/{board}/

# 4. Flash (see §3 for details)
{flash_command}
```

## 3. Build System
### 3.1 Directory Layout
(device tree diagram)

### 3.2 Configuration Files
- config.json: ...
- config.gni: ...
- Kconfig chain: ...

### 3.3 Common Build Issues & Fixes
(Issue → Symptom → Fix table, from 实测经验)

## 4. Flashing & Running
### 4.1 Connection
### 4.2 Flash Procedure
### 4.3 Serial Output Verification
$ expected first line of output

## 5. Peripheral Drivers
### 5.1 GPIO (✅ Supported)
### 5.2 UART (✅ Supported)
... (one subsection per peripheral)

## 6. Known Limitations
- WiFi: MVP only (Layers 4-7 not implemented)
- Watchdog: TODO (needs chip system manual)
...

## 7. Troubleshooting
(Q&A style, from compiler_fix_playbook findings)
```

### 6a-2: API 参考文档

对每个 public HAL/KAL 接口:

```c
/**
 * @brief  Write GPIO output value.
 * @param  resource  GPIO resource handle (from GpioOpen).
 * @param  val       Output value (0 = LOW, non-zero = HIGH).
 * @return #HDF_SUCCESS on success.
 *         #HDF_ERR_INVALID_PARAM if resource is NULL or pin out of range.
 *         #HDF_FAILURE on hardware error.
 * @see GpioRead()
 * @note Thread-safe. Interrupt-safe if called from task context only.
 */
int32_t GpioWrite(struct GpioResource *resource, uint16_t val);
```

**必须包含的元素**: `@brief` / `@param` / `@return` / `@see` / `@note` / thread-safety annotation

### 6a-3: 移植指南

面向下一个移植者的经验文档：

```markdown
# Porting Guide: {Chip Model} → Your Chip

## Decisions We Made (and Why)
| Decision | What | Why | Alternative Considered |
|----------|------|-----|----------------------|
| D1 | L0 IoT HAL (not HDF) | wifiiot doesn't use HDF | Would need full HCS config |
| D2 | Wrapper script for zicsr | GCC prebuilt lacks extension | Could rebuild toolchain (~2h) |
| D3 | ROM_TEXT +2KB margin | Cross-GCC code density diff | Could optimize code instead |
| ... | ... | ... | ... |

## Pitfalls We Hit
1. hb Python import broken → fix: pip install-e + __init__.py
2. CSR instruction missing → fix: wrapper script
3. linker overflow → fix: +2% margin rule
4. ...

## What's Left for Next Iteration
- [ ] WiFi Layers 4-7 (full implementation)
- [ ] Watchdog / Reset / Lowpower drivers
- [ ] HIL test automation
- [ ] Power optimization
```

---

## Step 6b: 代码审查 ★ 8 维度

> **与 Round-Trip Gate Report 的对齐**: Gate Report 衡量 regenerated vs GT 的结构+内容相似度。本阶段的 8 维度审查在**没有 GT** 的情况下追求同样的质量保证——通过系统化检查清单逼近 Gate Report 的判定力。

### 审查 8 维度 — 具体检查项

#### 🔴 Critical: 正确性

- [ ] **状态机完整性**: 所有状态转换都有处理? 没有 dangling state?
- [ ] **边界条件**: 数组访问有 bounds check? 整数溢出保护?
- [ ] **NULL/空指针**: 所有指针参数在使用前检查了 NULL?
- [ ] **返回码一致性**: 错误码在整个模块内语义一致?
- [ ] **资源泄漏**: Init 分配的资源都在 Release 中释放? (malloc/fd/lock)
- [ ] **并发安全**: 共享变量有锁/原子操作/临界区保护?

#### 🔴 Critical: 安全性

- [ ] **缓冲区溢出**: 所有 strcpy/memcpy/sprintf 有长度限制? → 用 snprintf/memcpy_s 替代
- [ ] **栈深度**: 递归或大局部数组不会导致栈溢出? (L0 栈通常只有几 KB)
- [ ] **注入风险**: 用户可控输入是否经过校验? (网络数据/串口命令/配置文件)
- [ ] **权限检查**: 关键操作 (擦除 flash / 复位) 是否有保护?
- [ ] **硬编码密钥/密码**: 没有在源码中嵌入凭证?

#### 🟡 Warning: 规范性

- [ ] **命名规范**: 函数名遵循 `{Module}_{Action}` 驼峰? 宏全大写下划线?
- [ ] **魔数消除**: 数字常量有命名宏定义? (`0x11000000` → `GPIO_BASE_ADDR`)
- [ ] **文件头注释**: 每个 .c/.h 有版权 + 简要描述 + 作者?
- [ ] **注释质量**: 非显而易见的逻辑有注释? 没有"废话注释" (解释代码本身)?
- [ ] **格式一致**: 缩进/花括号风格/行宽 在整个项目中统一?

#### 🟡 Warning: 性能

- [ ] **ISR 中无阻塞调用**: 中断服务函数不包含 sleep/wait/I/O?
- [ ] **无忙等待循环**: 轮询有超时退出条件?
- [ ] **动态分配最小化**: 热路径 (ISR/callback) 不含 malloc/free?
- [ ] **中断延迟可接受**: ISR 执行时间 < 系统允许的最大 latency?

#### 🟢 Info: 可测试性

- [ ] **Mock 点可注入**: 底层硬件操作可通过函数指针替换?
- [ ] **错误码可区分**: 不同错误原因返回不同错误码 (便于 test assertion)?
- [ ] **日志埋点充分**: 关键路径有 HDF_LOGI/LOGE/LOGW?
- [ ] **断言覆盖**: 编译时 debug 模式启用 ASSERT?

#### 🟢 Info: 可维护性

- [ ] **耦合度低**: 单一文件 fan-out (被依赖数) < 7?
- [ ] **配置外置**: 可调参数在 .h/.gni 中, 不硬编码在 .c?
- [ ] **SRP 遵守**: 单个函数职责明确?
- [ ] **死代码清除**: 没有 unreachable / commented-out 大段代码?

#### 🟢 Info: 兼容性

- [ ] **L0/L1 条件编译清晰**: `#ifdef LOSCFG_{FEATURE}` 使用正确?
- [ ] **字节序处理**: 多字节数据有 htons/ntohl 或显式转换?
- [ ] **编译器兼容**: 不依赖 compiler-specific extension (除非有 fallback)?
- [ ] **API 版本策略**: 公开接口有版本标记 (@deprecated / version guard)?

#### 🟢 Info: 文档

- [ ] **公开 API 有 Doxygen 注释**: @brief/@param/@return/@see 完整?
- [ ] **README 存在且有用**: 说明如何 build/run/test?
- [ ] **非显而易见决策有注释**: 为什么选 A 不选 B?
- [ ] **示例代码可编译**: 文档中的代码片段不是伪代码?

---

## Step 6c: 双 Agent 协议

### 信息隔离规则

```
┌─────────────────────────────────────────────┐
│              P6 执行 timeline               │
│                                             │
│  P5 完成或已显式跳过，并已更新 Manifest      │
│     │                                       │
│     ├─→ 6a doc-expert (会话 A)              │
│     │    输入: P1~P5 产出                   │
│     │    输出: 文档三件套                    │
│     │    ⚠️ 不知道 6b 的存在                │
│     │                                       │
│     ├─→ 6b ohos-dev-driver-review (会话 B) ★ 独立    │
│     │    输入: P1~P5 源码 (不含 6a 文档!)   │
│     │    输出: 8 维度审查报告                 │
│     │    ⚠️ 不知道 6a 的存在                │
│     │                                       │
│     └─→ 6c 合并点                            │
│          汇总: 文档 + 审查报告 + 一致性检查   │
│          签收: 双方独立 sign-off             │
└─────────────────────────────────────────────┘
```

**为什么信息隔离很重要**: 如果 6b 审查者看到了 6a 写的文档，会不自觉地被文档描述引导（确认偏差）。独立审查才能发现"代码实际行为 ≠ 文档描述"的不一致。

**宿主能力约束**：仅在宿主可创建两个隔离会话时执行 6a/6b 独立并行。否则可完成文档与单会话审查，但必须把 `independence_status: UNVERIFIED_INDEPENDENCE`、原因和风险写入 `verification_manifest`；此状态只能形成条件性交付，不得签发 GATE-R PASS 或声称“独立审查已完成”。

### 合并产出

（以下模板中的 `docs/*.md` 与 `out/{board}/` 为 P4~P6 运行时在目标项目生成的产物路径，非本 skill 包内文件）

```markdown
# 交付包 — {chip_model} 适配

## 内容清单
1. 适配手册 `docs/manual.md` ← 来自 6a
2. API 参考 `docs/api_reference.md` ← 来自 6a
3. 移植指南 `docs/porting_guide.md` ← 来自 6a
4. 代码审查报告 `docs/review_report.md` ← 来自 6b
5. 固件二进制 `out/{board}/` ← 来自 P4
6. 测试报告 `docs/test_report.md` ← 来自 P5（如执行）

## 审查摘要
| 维度 | 得分 | Critical 发现 | 状态 |
|-----------|:-----:|:-----------------|:------:|
| 正确性 | ?/?10 | ... | ✅/⚠️/❌ |
| 安全性  | ?/?10 | ... | ✅/⚠️/❌ |
| ...（全部 8 维度） |

## 签收（Sign-off）
- 文档作者 (6a): ____________ 日期: ______
- 审查者 (6b): ____________ 日期: ______
```

---

## 引用的 tools/

| 工具 | 用途 | 路径 |
|------|------|------|
| ohos-design-ref-retrieval | 参考资料检索（6a 文档辅助） | `skills/ohos-design-ref-retrieval/` |
| ohos-dev-driver-review | 6 类规则代码审查（6b） | `skills/ohos-dev-driver-review/` |

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | **双 Agent**: `doc-expert` (6a) + `ohos-dev-driver-review` (6b) |
| **category** | 6a: `writing` / 6b: `unspecified-high` |
| **load_skills** | 6a:`[ohos-design-ref-retrieval]` / 6b:`[ohos-dev-driver-review]` |
| **dispatch_mode** | 宿主支持时完全并行且独立会话；否则串行执行并记录 `UNVERIFIED_INDEPENDENCE` |
| **parallel_groups** | G1: [6a, 6b] 完全并行 |

### 6a Agent Prompt (doc-expert)

```
1. TASK: 为 {chip_model} 嵌入式 OS 适配项目生成完整文档三件套。
   你是文档专家。你不知道还有一个审查者在同时工作 (这是故意的)。
   
2. 产出:
   A. 芯片适配手册 (Getting Started + Build + Flash + Run + Known Limits)
   B. API 参考 (每个 public 函数 Doxygen 格式签名)
   C. 移植指南 (Decision log + Pitfalls + Roadmap)

3. 风格:
   - Markdown 格式
   - 代码示例必须是从实际源码提取的真实片段 (可编译)
   - 中文或英文 (按项目惯例)
   - 面向 "第一次接触这个适配的开发者"

4. MUST DO:
   - [ ] Build 命令可 copy-paste 执行
   - [ ] 每个 public API 有 @brief/@param/@return
   - [ ] Known Limitations 诚实列出 (不要隐藏未完成的功能)
   - [ ] Porting Guide 包含 Decision Log (我们做了什么选择, 为什么)
```

### 6b Agent Prompt (ohos-dev-driver-review)

```
1. TASK: 对 {chip_model} 嵌入式 OS 适配项目的全部源码执行 8 维度代码审查。
   你是代码审查专家。你不知道有一个文档作者在同时工作 (这是故意的——保证独立性)。
   
2. 审查范围:
   - P1: config.json, config.gni, BUILD.gn
   - P2: startup_S, system_init, linker.ld, KAL/*.c
   - P3: hals/**/*.c (所有驱动实现)
   - 排除: third_party/, musl/, test/

3. 8 个维度逐项检查 (每维度输出具体发现):
   🔴 正确性: 功能逻辑/状态机/边界/资源泄漏/并发
   🔴 安全性: 缓冲区溢出/注入/栈深度/凭证
   🟡 规范性: 命名/魔数/注释/格式
   🟡 性能: ISR/忙等/动态分配/延迟
   🟢 可测试性: Mock/错误码/日志/断言
   🟢 可维护性: 耦合/配置/SRP/死代码
   🟢 兼容性: L0/L1/字节序/编译器/API版本
   🟢 文档: Doxygen/README/示例/决策注释

4. 输出格式:
   每个维度: Score (1-10) + Findings list (each with file:line + description + severity)
   最终: 总分 + Top 5 must-fix + Nice-to-have list

5. MUST DO:
   - [ ] 每个发现必须有 file:line 定位 (不能模糊说 "某处有问题")
   - [ ] 区分 Critical/Warning/Info 三级
   - [ ] Top 5 must-fix 按 impact 排序 (先修影响最大的)
   - [ ] 诚实评分 (不要为了好看给高分)

6. MUST NOT DO:
   - [ ] 不要看任何文档文件 (保证独立性)
   - [ ] 不要假设意图 (只基于代码本身判断)
   - [ ] 不要修改代码 (只报告问题)
```

## MUST DO

- [ ] **宿主支持时双 Agent 必须独立会话**；不支持时记录 `UNVERIFIED_INDEPENDENCE`，不伪造独立性
- [ ] **8 个维度每个都要有具体检查项** — 不能只有 vague 描述
- [ ] **6b 审查者不能看到 6a 文档** — 信息隔离防止确认偏差
- [ ] **最终合并时做一致性交叉验证** — 文档说的 ≈ 代码做的?
- [ ] **Critical 发现必须 block 交付** — Correctness/Security 的 🔴 问题不修完不放行
- [ ] **GATE-R 必须记录** 6a/6b 产物路径、审查结果、独立性状态和最终 sign-off，并更新 `verification_manifest`

## MUST NOT DO

- [ ] 不要让 6a 和 6b 共享会话
- [ ] 不要弱化 8 维度中的任何一个 (即使 Info 级别也要检查)
- [ ] 不要跳过 sign-off 流程
