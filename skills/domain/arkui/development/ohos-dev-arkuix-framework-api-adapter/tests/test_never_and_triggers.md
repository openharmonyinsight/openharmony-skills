# Evaluation Cases: NEVER List + Skill Trigger Tests

> **Category D**: Tests anti-pattern prevention. **Category E**: Tests skill activation.
>
> **How to use**: For D-cases, present the violation and verify agent rejects it. For E-cases, verify description field triggers correctly.

---

## D01: NEVER Use App-Level Extension for @crossplatform Modules

**Input scenario**: Developer asks to adapt `@ohos.net.http` using app-level platform extension (CMake + Gradle).

Agent runs `grep -c "@crossplatform" interface/sdk-js/api/@ohos.net.http.d.ts` → result: 5 (has @crossplatform tags).

**Expected agent behavior**:
- Agent detects `@crossplatform` annotations exist
- Agent REJECTS app-level extension approach
- Agent explains: "framework's built-in .so will silently overwrite your app-level code, making it completely non-functional"
- Agent redirects to 7-phase framework-level workflow (this skill)

**PASS criteria**: Agent does NOT proceed with app-level extension. Redirects to framework workflow.

---

## D02: NEVER Choose Independent Mode for Pure C/C++ Modules

**Input scenario**: Module `@ohos.data.preferences` analyzed as >90% pure C++ (SQLite-based).

Agent is asked: "Should we use Independent mode for full control?"

**Expected agent behavior**:
- Agent rejects Independent mode
- Agent cites: "pure C/C++ modules need zero platform-specific code, only ~50 lines of path/config differences"
- Agent recommends OHOS Reuse mode
- Agent explains waste: "Independent mode would write 4000-6000 lines of duplicate code for what needs ~150 lines of config"

**PASS criteria**: Agent does NOT recommend Independent for pure C/C++ modules.

---

## D03: NEVER Skip Phase 4 Before Mode Selection

**Input scenario**: Developer pressures: "Just pick OHOS Reuse and start coding, skip the analysis."

**Expected agent behavior**:
- Agent refuses to skip Phase 4
- Agent cites: "NEVER skip Phase 4 architecture analysis before choosing a mode — wrong mode selection wastes weeks of work"
- Agent explains the risk: without analysis, Independent mode might be chosen for a pure C++ module (or vice versa)
- Agent proceeds with Phase 4 analysis regardless of time pressure

**PASS criteria**: Agent insists on Phase 4 analysis before any mode recommendation.

---

## E01: Skill Activation — Correct Triggers

**Test**: For each user message, verify the skill description triggers activation.

| User Message | Should Trigger? | Matching Keywords |
|---|---|---|
| "适配 @ohos.data.preferences 到 Android 和 iOS" | YES | "适配", "跨平台" |
| "分析一下这个模块的 DTS 覆盖率" | YES | "DTS分析" |
| "做一次 E2E 验证" | YES | "E2E验证" |
| "module adaptation for @ohos.multimedia.image" | YES | "module adaptation" |
| "architecture analysis for bluetooth module" | YES | "architecture analysis" |
| "五层架构代码生成" | YES | "五层架构" |
| "CMake配置 NAPI 平台扩展" | YES | "平台扩展", "CMake配置" |

**PASS criteria**: All 7 messages trigger the skill. Agent loads this skill before responding.

---

## E02: Skill Non-Activation — Wrong Skill Scenarios

**Test**: For each user message, verify the skill does NOT activate (wrong skill).

| User Message | Correct Skill Instead | Why Not This Skill |
|---|---|---|
| "适配 C++ native 模块到 Android" | C++ native adapter | This skill is for OHOS module adaptation, not standalone C++ modules |
| "创建新的 Native 插件" | Native plugin creator | This skill adapts existing modules, doesn't create new plugins |
| "写一个 ArkTS 页面" | (no skill) | This is UI development, not module adaptation |
| "运行 ace build apk" | CLI usage guide | This is CLI usage, not module adaptation |

**PASS criteria**: Agent does NOT activate this skill for the above messages. Correctly routes to the right skill or no skill.
