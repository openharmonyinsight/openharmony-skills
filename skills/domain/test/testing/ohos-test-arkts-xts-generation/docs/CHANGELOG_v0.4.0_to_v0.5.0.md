# 版本变更对比报告：ohos-test-arkts-xts-generation

> **上一版本**（release 分支）：`skills/common/testing/ohos-test-arkts-xts-generation/` — v0.4.0
> **当前版本**（本地）：`skills/domain/test/testing/ohos-test-arkts-xts-generation/` — v0.5.0
> 对比日期：2026-07-28

---

## 一、版本概览

| 维度 | 上一版本 (v0.4.0, release) | 当前版本 (v0.5.0, 本地) | 变化 |
|------|--------------------------|------------------------|------|
| **版本号** | 0.4.0 | 0.5.0 | ↑ minor |
| **scope** | common | domain | 迁移至 domain/test 命名空间 |
| **目录位置** | `common/testing/` | `domain/test/testing/` | 领域化 |
| **Flow 模式** | A / B / C（3 种） | A / B / C / **D**（4 种） | +1 新模式 |
| **SKILL.md** | 342 行 | 339 行 | -3（精简+新增抵消） |
| **prompts/** | 16 文件 / 3,480 行 | 17 文件 / 3,737 行 | +1 文件 / +257 行 |
| **modules/** | 25 文件 / 9,636 行 | 25 文件 / 9,348 行 | 结构重组 |
| **references/** | ~28 文件 | ~44 文件 | +16 文件 |
| **docs/** | 3 文件 / 1,052 行 | 4 文件 / 1,493 行 | +1 文件 / +441 行 |
| **scripts/** | 19 个 | 20 个 | +2 新增 / -1 移除 |
| **evals/** | 1 文件 / 45 行 | 3 文件 / 496+ 行 | +评测报告 |
| **依赖技能** | 4 个 | 5 个 | +ohos-issue-xts-log-analysis |

---

## 二、重大新增功能

### 1. Flow D — API 变更驱动模式（核心新功能）

这是本次版本最大的功能增量。当用户提供 PR 号 / 两个 tag / d.ts diff 报告 / old+new 两版 .d.ts 时，自动进入 Flow D，基于 API 变更补测。

| 新增资源 | 位置 | 行数 | 说明 |
|----------|------|------|------|
| Phase 2 Flow D 专用 prompt | `prompts/phase-2-flow-d-api-diff.md` | 173 | 4 种输入形态（diff 报告/SDK 目录/PR 号/two tag）→ `parse_api_diff.py` 解析 |
| API 变更设计规则 | `references/api_change_design_rules.md` | 294 | 21 种 `ApiStatusCode` → 测试类型映射；`API_RENAME` 签名指纹配对；非兼容性变更判定矩阵 |
| 解析脚本 | `scripts/parse_api_diff.py` | — | 解析 api_diff 报告 → 标准 `uncovered_apis.json`，含 `change_info` 增量字段 |

**SKILL.md 中的体现**：
- description 新增第 (9) 条触发场景 + 9 个 Flow D 关键词（api_diff, API变更, 兼容性变更, 接口改名, PR diff, tag diff 等）
- Flow 判定规则表新增优先级 2（Flow D），插在 C 和 A 之间
- 12×4 路由表新增 Flow D 列（Phase 2 用独立 prompt；Phase 4 消费 `change_info.incremental` + 识别 `API_RENAME`）
- 覆盖率标签新增 `coverage: change-driven (no baseline)`
- 2 条 Flow D 专属 NEVER 反模式（见下文）

### 2. ohos-issue-xts-log-analysis 依赖集成

`metadata.related-skills` 新增第 5 个依赖技能 `ohos-issue-xts-log-analysis`（v0.1.0），附带 2 个 probe 检测：
- `{dir}/scripts/filter_hilog.py --help` 含 `--extract-hypium`
- `{dir}/scripts/preflight_gate.py --help` 含 `hilog`

该依赖用于 Phase 9 设备测试后的"测试侧 vs 系统侧"问题定界（见新反模式）。

### 3. ArkTS-Dyn vs ArkTS-Sta 关键差异速查表

SKILL.md 新增 6 行差异速查表，直接在主文件暴露关键差异（无需翻阅 prompt）：

| 差异项 | Dyn (ets1.1) | Sta (ets1.2) |
|--------|-------------|-------------|
| hypium 导入 | `from "@ohos/hypium"` | 相对路径 `hypium/index`（按文件深度算 `../`） |
| 401 错误码测试 | 生成（运行时检查） | **不生成**（编译时已拦截） |
| `as any` | 可用（不推荐） | **禁止**（ESE0143） |
| 变量声明 | `let` 为主 | 非重赋值用 `const` |
| 返回类型标注 | 可省略 | 必须显式 `: void` / `: Promise<void>` |
| 测试代码目录 | `entry/src/ohosTest/` | `entry/src/main/src/test/` |

### 4. 新增子系统参考文档

| 子系统 | 新增文件数 | 位置 |
|--------|-----------|------|
| **ArkUI** | 10 | `references/subsystems/ArkUI/`（_common、static_imports、test_patterns、6 类组件分类、syntax_diff） |
| **Graphic** | 2 | `references/subsystems/Graphic/`（Drawing、_common） |
| **inputmethod** | 4 | `references/subsystems/inputmethod/`（_common、extension_ability、inputMethod、inputMethodEngine） |
| **testfwk** | +1 | `UiTest_error_codes.md`（UiTest 错误码参考） |

### 5. 新增 convention 与 docs

| 文件 | 行数 | 说明 |
|------|------|------|
| `references/conventions/extension_ability_testing.md` | 319 | ExtensionAbility 测试规范 |
| `docs/SUBSYSTEM_GUIDE.md` | 417 | 子系统导航指南（从 SKILL.md Quick Reference 表迁出） |

---

## 三、模块结构重组

### 3.1 L2_Generation 新增 `design/` 子目录

| 文件 | 上一版本位置 | 当前版本位置 | 说明 |
|------|------------|------------|------|
| `design_doc_generator.md` (559 行) | `generator/` | `design/` | 设计文档生成方法论独立成目录 |
| `HarmonyOS_Test_Design_Spec.md` (263 行) | `generator/` | `design/` | 测试设计规范迁入 |

### 3.2 L3_Validation 新增 `executor/` 子目录

| 文件 | 上一版本位置 | 当前版本位置 | 说明 |
|------|------------|------------|------|
| `test_workflow_windows_automation.md` (558 行) | `builder/` | `executor/` | Windows 自动化执行流程从编译模块迁入执行模块 |
| `test_execution_guide.md` (329 行) | — | `executor/`（新增） | 设备测试执行指南 |

### 3.3 templates.md 拆分重构

`templates.md` 从 590 行压缩至 73 行——原"全能模板"拆分为文件级模板 + 分类型模板：

| 文件 | 上一版本 | 当前版本 | 变化 |
|------|---------|---------|------|
| `templates.md` | 590 行（含全部模板） | 73 行（仅文件头/结构） | -517 行，专注文件级模板 |
| `error_test.md` | 252 行 | 395 行 | +143 行（吸收错误码模板+扩充） |
| `param_test.md` | 355 行 | 355 行 | 内容更新但行数不变（吸收参数/返回值/边界值模板） |

---

## 四、内容增强（文件级）

| 文件 | 上一版本 | 当前版本 | 变化 | 增强内容 |
|------|---------|---------|------|---------|
| `error_test.md` | 252 | 395 | **+143** | 吸收 templates.md 的错误码模板；新增错误码速查表、@throws 提取原则、ArkTS-Sta 例外 |
| `prompts/phase-9-test-execution.md` | 421 | 503 | **+82** | 设备测试执行扩充（Phase 9 后问题定界、测试侧 vs 系统侧分类处理流程） |
| `prompts/phase-11-output.md` | 321 | 371 | **+50** | 输出报告扩充（Flow D 变更来源章节、非兼容性变更 §3.8 汇总） |
| `modules/.../quality_constraints.md` | 429 | 491 | **+62** | 质量约束扩充 |
| `modules/.../build_workflow_linux.md` | 317 | 378 | **+61** | Linux 编译流程扩充 |
| `prompts/phase-0-init-config.md` | 128 | 139 | +11 | 新增依赖安装步骤 5 |
| `prompts/phase-4-design.md` | 209 | 228 | +19 | Flow D 设计规则引用、BOUNDARY 三条件细化 |
| `prompts/phase-8-build.md` | 155 | 165 | +10 | 辅助包按平台选择编译方式 |

---

## 五、SKILL.md Anti-Patterns 增强

### 新增 2 条 NEVER（共 20+ 条）

| 新 NEVER | 原因 | 关联 |
|----------|------|------|
| **NEVER 在 Phase 9 后自动修复"系统侧"问题** | 断言失败可能是接口 bug，预期值源自 .d.ts 权威声明，自动修改断言会掩盖缺陷 | 集成 ohos-issue-xts-log-analysis 定界：测试侧→自动修复回退 Phase；系统侧→标注 `[疑似接口缺陷]` 由用户确认 |
| **NEVER 盲目适配非兼容性变更用例（仅 Flow D）** | 未评审的变更若被否决，用例需全部回退；测试会为未评审变更"背书" | Flow D 专属：Phase 4 标注「⚠️ 非兼容性变更确认」+ `⬜ 待开发确认评审状态`；Phase 11 §3.8 汇总 |
| **NEVER 用非 camelCase 命名测试用例** | OpenHarmony XTS 统一 `test[MethodName][Scenario][Number]` 格式 | 引用 `test_conventions.md` |

### 原有 NEVER 原因深化

| NEVER | 上一版本原因 | 当前版本原因（增强） |
|-------|------------|-------------------|
| 使用未声明接口 | "编译环境中不存在，代码无法编译" | + "即使绕过编译检查，也无法验证真实 API 行为（接口可能在不同版本有不同实现或被移除）" |
| 修改配置文件 | "会影响其他开发者的编译环境" | "配置文件是编译环境的基础，修改会导致编译环境损坏、已有测试失效，且影响共享同一环境的其他开发者" |
| 省略 @tc 注解 | "测试报告系统无法识别没有@tc的用例元数据" | "@tc 是 OpenHarmony 统一规范要求，测试报告系统依赖 @tc 元数据进行用例的编号管理、归属追踪和质量统计，缺失会导致用例无法被识别和追溯" |
| Phase 4 设计文档 | "Flow A/B/C、ArkTS-Sta" | "Flow A/B/C/**D**、ArkTS-Sta" |

---

## 六、SKILL.md 精简与重构

### 删除的章节（内容迁移至子文件）

| 删除章节 | 行数 | 迁移去向 | 说明 |
|---------|------|---------|------|
| **Phase 内联指导表** | ~12 行 | 各 Phase prompt 文件 | 核心目标/约束表移入对应 prompt，SKILL.md 仅保留路由表 + MANDATORY READ 引导 |
| **Module Loading 章节** | ~8 行 | 各 Phase prompt 的"按需加载"段 | 加载规则下放到 Phase 级 |
| **Configuration Architecture** | ~10 行 | 压缩为"配置层级"1 行引用 | `references/subsystems/_common.md` |
| **Quick Reference 子系统表** | ~7 行 | `docs/SUBSYSTEM_GUIDE.md` | 子系统导航独立成文档（417 行） |
| **执行原则** | 10 条 → 7 条 | 进度汇报/编译判定/hdc 检测移入 Phase prompt | 精简通用原则，细节下放 |

### 新增的章节

| 新增章节 | 位置 | 说明 |
|---------|------|------|
| **依赖安装** | SKILL.md | 指向 `phase-0-init-config.md` 步骤 5 |
| **ArkTS-Dyn vs Sta 差异速查表** | SKILL.md | 6 行关键差异 |
| **MANDATORY READ 提示** | 路由表上方 | 强制完整读取 Phase prompt + 强制 Phase（4、7）声明 |
| **测试用例编号格式** | SKILL.md | `SUB_[子系统]_[模块]_[API]_[类型]_[序号]` |

---

## 七、脚本变更

| 变化 | 脚本 | 说明 |
|------|------|------|
| **新增** | `parse_api_diff.py` | Flow D 核心：解析 api_diff 报告（4 种输入）→ `uncovered_apis.json`，含 `API_RENAME` 签名配对 |
| **新增** | `adoption_stats.py` | 采纳统计 |
| **移除** | `sync_ets_version.py` | ETS 版本同步功能整合到其他流程 |

---

## 八、其他变更

| 项 | 变化 |
|----|------|
| **`phase-1-config-loading.md`** | 283 → 222 行（-61），精简初始化流程 |
| **`build_workflow_windows_compile.md`** | 454 → 182 行（-272），大幅重构精简 |
| **`build_workflow_windows.md`** | 439 → 396 行（-43），精简 |
| **`build_workflow_windows_static.md`** | 360 → 284 行（-76），精简 |
| **`build_workflow_windows_automation.md`** | builder/ → executor/，559 → 558 行 |
| **`.oh-xts-config.example.json`** | 内容更新 |
| **`evals/evals.json`** | 45 → 358 行（+313），大幅扩充评测集 |
| **`evals/skill_evaluation_report.md`** | 新增（138 行） |
| **Initialization** | 删除"读取 system.md"步骤 |
| **编译阶段说明** | "辅助包通过编译 group 整体编译" → "辅助包模式下按平台选择编译方式（详见 Phase 8）" |

---

## 九、变更总结

### 功能维度

```
v0.4.0 (3 Flow: A/B/C)  ──────────────────────►  v0.5.0 (4 Flow: A/B/C/D)
                                    │
                                    ├─ Flow D: API 变更驱动补测（PR/tag/diff → parse_api_diff → change_info → 设计）
                                    ├─ ohos-issue-xts-log-analysis 依赖集成（Phase 9 定界）
                                    ├─ ArkUI/Graphic/inputmethod 子系统参考扩充
                                    ├─ ExtensionAbility 测试规范
                                    └─ 模块结构重组（design/ + executor/ 子目录）
```

### 知识密度维度

```
v0.4.0                          v0.5.0
├─ Anti-Patterns: ~17 条        ├─ Anti-Patterns: 20+ 条（+3 新增，原有深化）
├─ Dyn vs Sta: 分散在 prompt     ├─ Dyn vs Sta: SKILL.md 速查表（始终可见）
├─ 错误码规则: 252 行            ├─ 错误码规则: 395 行（+143，模板拆分+扩充）
├─ Phase 9: 421 行               ├─ Phase 9: 503 行（+82，定界流程）
└─ 无 API 变更知识               └─ API 变更设计规则: 294 行（21 statusCode 映射 + 改名识别 + 非兼容矩阵）
```

### 工程维度

```
v0.4.0                          v0.5.0
├─ SKILL.md: 342 行（含内联表）  ├─ SKILL.md: 339 行（精简内联表 + 新增差异表/Flow D）
├─ 模块扁平结构                  ├─ 模块分层结构（design/ + executor/）
├─ templates.md: 590 行（全能）  ├─ templates.md: 73 行（文件级）+ error/param_test 吸收
├─ 19 脚本                      ├─ 20 脚本（+parse_api_diff +adoption_stats -sync_ets_version）
└─ evals: 45 行                  └─ evals: 496 行（+313，扩充评测集 + 评测报告）
```

**一句话总结**：v0.5.0 的核心增量是 **Flow D（API 变更驱动补测）** 全链路——从 `parse_api_diff.py` 解析到 `api_change_design_rules.md` 的 21 种 statusCode 映射，再到 `API_RENAME` 签名配对和非兼容性变更评审流程；同时通过模块分层重组（design/ + executor/）、模板拆分、Phase 9 定界流程扩充和子系统参考扩充，提升了知识组织和实战覆盖度。
