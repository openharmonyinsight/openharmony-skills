# Skill Evaluation Report: ohos-test-capi-xts-generation

## Summary

- **Total Score**: 110/120 (91.7%)
- **Grade**: A
- **Pattern**: Process (~200 lines, phased workflow)
- **Knowledge Ratio**: E:A:R = 75:20:5
- **SKILL.md Lines**: 402
- **Total Reference Lines**: ~3,845 (across prompts/, modules/, references/)
- **Verdict**: A well-architected expert Skill with deep domain knowledge of OpenHarmony CAPI N-API testing, excellent anti-patterns, and outstanding progressive disclosure; minor redundancy in code templates and inline Phase guidance prevents a perfect score.

---

## Dimension Scores

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| D1: Knowledge Delta | 16 | 20 | Expert-heavy content; some verbose/repeated code templates in references |
| D2: Mindset + Procedures | 14 | 15 | Exceptional "Thinking Framework" section; domain-specific N-API procedures |
| D3: Anti-Pattern Quality | 14 | 15 | 12 specific NEVERs with root causes; expert-grade failure patterns |
| D4: Specification Compliance | 15 | 15 | Perfect description: WHAT + WHEN (9 scenarios) + KEYWORDS |
| D5: Progressive Disclosure | 14 | 15 | 3-layer architecture with MANDATORY/Do NOT Load triggers |
| D6: Freedom Calibration | 14 | 15 | Well-calibrated low freedom for fragile N-API code generation |
| D7: Pattern Recognition | 9 | 10 | Clear Process pattern; SKILL.md slightly over 200-line ideal |
| D8: Practical Usability | 14 | 15 | Decision trees, error handling, edge cases all covered |

---

## Step 1: Knowledge Delta Scan

### SKILL.md Content Classification

| Section | Lines | Classification | Justification |
|---------|-------|---------------|---------------|
| 配置加载 | 47-69 | **[E] Expert** | Skill-specific config schema, script table with calling时机 — Claude wouldn't know these |
| Initialization | 71-81 | **[E] Expert** | Flow routing logic (A vs C), module loading principle — domain-specific |
| Architecture Overview | 84-101 | **[E] Expert** | 4-layer generation architecture C API → N-API → d.ts → ETS; SUB_ naming convention |
| Workflow (入口判定, Flow判定, Phase总览) | 103-133 | **[A] Activation** | Phase routing table — useful reminder but structurally obvious |
| Phase 内联指导 | 135-220 | **[A] Activation** | Summarizes prompt files — redundant with prompts themselves but helps quick decisions |
| Module Loading | 222-239 | **[E] Expert** | Directory responsibility model (prompts vs modules vs references vs scripts vs template) |
| Configuration Architecture | 241-248 | **[A] Activation** | Priority chain pattern — standard config override pattern |
| Anti-Patterns (12 NEVERs) | 250-295 | **[E] Expert** | All 12 items are domain-specific with non-obvious reasons |
| Thinking Framework | 296-362 | **[E] Expert** | C API characteristic analysis table, N-API wrapping decision tree, test count estimation, priority ranking — pure expert knowledge |
| Common Failure Patterns | 364-394 | **[E] Expert** | 6 failure patterns with symptom → root cause → fix path |
| Generation Strategy | 396-402 | **[E] Expert** | Priority: supplement existing > create new; template_project copy rule |

### Reference Files Content Classification

| File | Lines | E | A | R | Notes |
|------|-------|---|---|---|-------|
| `references/subsystems/_common.md` | 613 | 60% | 15% | 25% | Sections I-II, XI, XIII, XV are Expert; Section IV (N-API常用API) is Redundant |
| `references/test_patterns_c.md` | 192 | 70% | 20% | 10% | Test patterns extracted from real code — high delta |
| `references/error_handling.md` | 118 | 85% | 15% | 0% | Error classification levels, retry strategies — pure Expert |
| `modules/L2_Generation/generator/test_generation_c.md` | 581 | 40% | 20% | 40% | Heavy code templates repeat the same N-API boilerplate 5+ times |
| `prompts/phase-5-generation.md` | 75 | 70% | 30% | 0% | Good loading triggers and generation constraints |
| `prompts/system.md` | 34 | 60% | 40% | 0% | Concise system prompt with essential constraints |

### Overall Ratio: E:A:R = 75:20:5

---

## Step 2: Structure Analysis

```
[x] Frontmatter: Valid YAML, all required fields present
[x] name: "ohos-test-capi-xts-generation" — lowercase, hyphens, 33 chars (< 64)
[x] description: Comprehensive, 14 lines, covers WHAT + WHEN + KEYWORDS
[x] metadata: author, scope, stage, domain, capability, version, status, tags
[x] related-skills: 2 related skills listed
[x] allowed-tools: 6 tools listed (Read, Write, Edit, Grep, Glob, Bash)

SKILL.md: 402 lines (slightly over Process pattern ideal of ~200)
Reference files: 3,845 total lines across 15+ files
Template project: Complete capi_test_template with all required files
Scripts: 6 automation scripts (verify, fix, build, cleanup)
Evals: 3 eval cases covering Flow B, Flow A, and new project scenarios
```

### File Structure

```
SKILL.md                          402 lines  (orchestration)
prompts/                          1,102 lines (phase-specific workflows)
  system.md                         33 lines
  phase-1-config.md                 77 lines
  phase-2-header-parse.md           90 lines
  phase-3-coverage.md               50 lines
  phase-4-design.md                165 lines
  phase-5-generation.md             74 lines
  phase-6-verification.md           82 lines
  phase-7-build.md                  85 lines
  phase-8-test-execution.md        268 lines
  phase-9-output.md                178 lines
modules/                          1,000+ lines (technical details)
references/                       1,600+ lines (subsystem configs, patterns)
scripts/                          6 automation scripts
template_project/                  complete project template
evals/                             3 eval cases
examples/                          4 example files
```

---

## Step 3: Dimension-by-Dimension Analysis

### D1: Knowledge Delta — 16/20

**Evidence of Expert Knowledge:**

1. **4-layer generation architecture** (lines 92-96): `C API (.h) → N-API 封装 (C++) → JS 接口 (index.d.ts) → ETS/ArkTS 测试 (.test.ets)` — This is a non-obvious architectural pattern specific to OpenHarmony testing that Claude would not invent.

2. **Triple Verification concept** (lines 186-197): The idea that C++, TypeScript, and ETS layers must have perfectly matching function names, parameter counts, and types — with automated shell scripts for verification and auto-fix. This is domain-specific operational knowledge.

3. **Memory ownership transfer rules** (lines 288-294): The distinction between `OH_*Create` (caller must free, needs `napi_finalize`) vs `OH_*Get` (system-managed, pass reference only) — expert knowledge that prevents real-world crashes.

4. **`nm_modname = "entry"` requirement** (line 282): A non-obvious OpenHarmony N-API constraint where the module name MUST be "entry" and ETS imports from `libentry.so`. Mismatch causes complete function loading failure.

5. **Flow routing with tool limitations** (lines 78-80): "CAPI 无 APICoverageDetector 扫描工具，无法执行标准扫描" — explaining WHY Flow B doesn't exist for CAPI, not just THAT it doesn't exist.

6. **Stop-expansion signals** (lines 358-361): Three concrete criteria for when to stop adding test cases — prevents over-engineering.

**Redundant Content:**

1. `references/subsystems/_common.md` Section IV (lines 224-308): "N-API 常用 API 规范" explains how to use `napi_get_value_int32`, `napi_get_value_string_utf8`, etc. — standard N-API knowledge Claude already has.

2. `modules/L2_Generation/generator/test_generation_c.md`: The same 30-line N-API boilerplate (get_cb_info → typeof check → extract value → call C function → create result) is repeated verbatim in sections 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4. This is ~200 lines of near-identical code.

3. Code style rules (`_common.md` lines 470-492): "使用 2 个空格缩进（TypeScript）", "变量名：使用驼峰命名法" — universal conventions.

**Score Justification**: The Expert content is strong and consistently high-value. The -4 deduction comes from the ~200 lines of repeated N-API boilerplate in `test_generation_c.md` and the ~80 lines of standard N-API reference in `_common.md`. A condensed version covering only the non-obvious OpenHarmony-specific patterns would push this to 18-19.

---

### D2: Mindset + Procedures — 14/15

**Thinking Frameworks (Exceptional):**

1. **"C API 特性分析" table** (lines 299-311): 7 questions to ask about every C API before generating N-API wrappers. Each question includes "为什么重要" (why it matters) and "影响生成策略" (how it affects generation). Example: "是否分配内存？→ N-API 封装需要 napi_finalize 回调释放内存；测试需验证无泄漏". This is expert thinking transfer.

2. **N-API 封装决策树** (lines 313-332): A return-type-driven decision tree with specific N-API function choices for each branch. The tree handles int (with/without output params), pointers (caller-frees vs system-managed), primitives, and void — each with the correct N-API conversion strategy.

3. **Test value priority** (lines 346-362): P0/P1/P2 ranking with specific API characteristics mapped to test strategies. "停止扩展信号" — three anti-over-engineering criteria.

4. **用例数量估算** (lines 334-344): Maps API complexity to recommended test case counts with coverage dimensions.

**Domain-Specific Procedures (Strong):**

1. Phase workflow with clear routing: compile-only → Phase 7 direct; full generation → Phase 1-9
2. Triple verification procedure: `verify_napi_triple.sh` → `auto_fix_napi_triple.sh` if failed
3. Error handling 4-level classification in `references/error_handling.md`: auto-fix → retry → user-confirm → terminate
4. Async build with retry: `async_build.sh` + `cleanup_group.sh` + 3-retry limit

**Score Justification**: The thinking framework is among the best I've seen in any Skill. -1 because some procedural content in `_common.md` (sections on code style, naming conventions) is generic rather than domain-specific.

---

### D3: Anti-Pattern Quality — 14/15

**12 NEVER Items (all with reasons):**

| # | Anti-Pattern | Reason Quality |
|---|-------------|---------------|
| 1 | NEVER use undeclared .h interfaces | "编译时找不到符号 → undefined reference" — specific error message |
| 2 | NEVER skip Phase 6 (triple verification) | "任一不匹配都会导致运行时崩溃" — consequence-driven |
| 3 | NEVER skip Phase 4 (design document) | "编号重复、函数映射混乱，且无法通过 Phase 6 的三重校验" — cascade effect |
| 4 | NEVER return error objects from N-API | "必须返回napi_value类型" — type system constraint |
| 5 | NEVER modify existing project config files | "会影响其他开发者的编译环境" — blast radius reasoning |
| 6 | NEVER omit @tc annotations | "测试报告系统无法识别" — downstream dependency |
| 7 | NEVER create project without template copy | "手动创建容易遗漏关键文件" — practical experience |
| 8 | NEVER hardcode module name | "不一致会导致加载失败" + correct value specified |
| 9 | NEVER create new project in Flow A | "明确目标是补充已有工程的缺失测试" — mode-specific reasoning |
| 10 | NEVER ignore memory ownership transfer | "use-after-free" + correct N-API finalize pattern |
| 11 | NEVER fabricate ERROR tests without error codes | "构造错误码测试无规范依据" — .h-grounded reasoning |
| 12 | (in test_generation_c.md) NEVER hardcode error code numbers | Must use named constants from .h — prevents magic numbers |

**Failure Patterns (6 detailed):**

Each pattern follows symptom → root cause → fix path format:
- `undefined reference` → check .h declarations + CMakeLists.txt
- `is not a function` → check descriptor registration + function name spelling
- Type mismatch → check napi_get_value_* vs C type correspondence
- Triple mismatch → run verify script → auto_fix script
- Runtime crash → null pointer checks + napi_finalize verification
- New project build failure → copy from template_project completely

**Score Justification**: This is expert-grade. An experienced OpenHarmony tester would recognize these as real production issues. -1 because a few failure patterns in `error_handling.md` (like "字符串参数截断" at line 107-111) could include more specific buffer size guidance.

---

### D4: Specification Compliance — 15/15

**Frontmatter Analysis:**

```yaml
name: ohos-test-capi-xts-generation  # ✅ lowercase, hyphens, 33 chars
description: >                        # ✅ multi-line, comprehensive
  OpenHarmony CAPI XTS测试用例生成器。解析.h头文件，生成C++ N-API封装和ETS/ArkTS测试代码...
  Use when: (1) ... (9)               # ✅ 9 explicit trigger scenarios
  Trigger keywords: CAPI, N-API...    # ✅ exhaustive keyword list
metadata:                             # ✅ well-structured
  author, scope, stage, domain, capability, version, status
  tags: [xts, capi, napi, test-generation]
  related-skills: [...]               # ✅ 2 related skills
  allowed-tools: [...]                # ✅ 6 tools
```

**Description Quality Checklist:**

- [x] **WHAT**: "解析.h头文件，生成C++ N-API封装和ETS/ArkTS测试代码，支持N-API三重校验和编译验证" + architecture diagram
- [x] **WHEN**: 9 explicit scenarios numbered (1)-(9), covering: CAPI testing, N-API wrapping, coverage reports, new APIs, build/compile, async build, XTS testing, build failures
- [x] **KEYWORDS**: 25+ trigger keywords including: CAPI, N-API, napi, .h文件, 头文件解析, Native测试, 编译, build, compile, 覆盖率报告, XTS, async_build, cleanup_group, N-API封装, 三重校验, 新增接口, new API
- [x] **Specific enough**: The 9 scenarios are concrete enough that an Agent can match user requests precisely
- [x] **MUST-use scenarios**: Explicitly states when this skill MUST be used (e.g., "用户提到编译失败、编译错误")

This is one of the best descriptions I've seen — comprehensive, searchable, and unambiguous.

---

### D5: Progressive Disclosure — 14/15

**Three-Layer Architecture:**

```
Layer 1: Metadata (description field)
         ~150 tokens
         → 9 trigger scenarios + 25+ keywords

Layer 2: SKILL.md Body
         402 lines
         → Phase routing, decision trees, anti-patterns, thinking framework

Layer 3: Reference Files (loaded on demand)
         prompts/    → Phase-specific workflows with embedded loading triggers
         modules/    → Technical details (parser, generator, builder)
         references/ → Subsystem configs, test patterns, error handling
         scripts/    → Automation tools
         template_project/ → Complete project template
```

**Loading Trigger Quality:**

Every phase prompt includes three standardized sections:
- 📚 **参考文档（按需查阅）**: Files to load for this phase
- ⚙️ **按需加载**: Conditional loading based on task type
- 🚫 **Do NOT Load**: Explicit prevention of over-loading

Example from `phase-5-generation.md`:
```markdown
### 📚 参考文档（按需查阅）
| modules/L2_Generation/generator/test_generation_c.md | 本 Phase 必须加载 |
| modules/L2_Generation/generator/test_patterns_napi_ets.md | 本 Phase 必须加载 |

### ⚙️ 按需加载
| 回调/异步/句柄类 API | test_patterns_napi_ets_advance.md |
| 创建新工程 | project_config_templates.md |

### 🚫 Do NOT Load
所有 modules/L1_Analysis 模块
所有 modules/L3_Validation 模块
```

**Module Loading Principle** (SKILL.md line 82):
> 仅加载当前阶段需要的模块，不要一次性加载所有模块。参考各 Phase prompt 文件开头的加载指令。

**Score Justification**: Nearly perfect progressive disclosure. -1 because the inline Phase guidance (SKILL.md lines 139-220, ~80 lines) partially duplicates the phase prompts. If Agent always loads the prompt file anyway, this inline summary adds token cost without proportional value. A more concise version (single-line per Phase + MANDATORY/Do NOT Load) would be more efficient.

---

### D6: Freedom Calibration — 14/15

**Task Fragility Analysis:**

N-API wrapper generation is a **high-fragility** task:
- One wrong function name → runtime crash
- Missing napi_property_descriptor → function not registered
- Wrong napi type conversion → type mismatch at runtime
- Memory ownership confusion → leak or use-after-free

**Freedom Calibration in Practice:**

| Aspect | Freedom Level | Implementation |
|--------|-------------|----------------|
| Phase routing | Low | Exact decision tables, no ambiguity |
| API parsing | Low | Must use `.h` declarations only, no guessing |
| N-API wrapping | Low | Decision tree (return type → specific napi function), template required |
| Test case design | Medium | Priority framework (P0/P1/P2) with stop-expansion signals |
| Test case content | Medium | Type categories defined (PARAM/ERROR/RETURN/BOUNDARY/MEMORY) but specific values flexible |
| Project structure | Very Low | Must copy from template_project, no manual creation |

**Scripts enforce low freedom:**
```bash
bash scripts/verify_napi_triple.sh ${TARGET_PATH}
bash scripts/auto_fix_napi_triple.sh ${TARGET_PATH}
bash scripts/check_test_suite_structure.sh ${TARGET_PATH}
```

**Score Justification**: Excellent calibration. The only area where freedom could be tighter is the error code constant naming convention — the current guidance (`let errCode[Scenario][Type]`) is good but could be even more rigid with exact naming templates per subsystem. -1 for this minor gap.

---

### D7: Pattern Recognition — 9/10

**Pattern Match: Process**

| Process Pattern Feature | Present? | Evidence |
|------------------------|----------|---------|
| Phased workflow | ✅ | 9 Phases with clear transitions |
| Entry point routing | ✅ | Compile-only vs full generation |
| Flow branching | ✅ | Flow A (coverage) vs Flow C (new API) |
| Checkpoints | ✅ | Phase 6 verification is non-skippable |
| MANDATORY/optional distinction | ✅ | Phase 8 is optional; Phase 4, 6 are mandatory |
| ~200 lines target | ⚠️ | 402 lines (2x target) |
| Progressive loading | ✅ | 3-layer with triggers |

**Deviations from ideal Process pattern:**

1. SKILL.md is 402 lines vs ideal ~200. The excess comes from:
   - Inline Phase guidance (~80 lines) — could be condensed
   - Thinking Framework (~67 lines) — justified as high-value Expert content
   - Common Failure Patterns (~31 lines) — justified as high-value Expert content

2. The "Architecture Overview" section (lines 84-101) and "Configuration Architecture" section (lines 241-248) are slightly redundant — both appear elsewhere.

**Score Justification**: Clear Process pattern with minor line-count excess. The extra lines are mostly high-value content (anti-patterns, decision trees), not padding. -1 for the 2x line count over ideal.

---

### D8: Practical Usability — 14/15

**Decision Trees:**

1. **Entry routing** (SKILL.md lines 104-111): User intent → Phase entry point
2. **Flow detection** (SKILL.md lines 113-119): Priority-ordered conditions → Flow A/C
3. **N-API wrapping** (SKILL.md lines 313-332): Return type → N-API strategy
4. **Subsystem detection** (phase-1-config.md lines 46-53): Information source priority → subsystem name
5. **Project creation** (SKILL.md lines 396-402): 3-level priority for supplement vs create

**Error Handling & Fallbacks:**

1. **4-level error classification** (`error_handling.md`): auto-fix → retry → confirm → terminate
2. **Build failure handling**: 3-retry with automatic analysis; falls back to user confirmation
3. **Triple verification failure**: `verify` script → `auto_fix` script → manual check
4. **Config not found**: Prompt user to set OH_ROOT, write config file

**Edge Cases Covered:**

1. Conditional compilation (`#ifdef OHOS_ENABLE_*`) in .h files
2. String buffer truncation in N-API wrappers
3. Suite name mismatch between build command and BUILD.gn
4. Memory ownership ambiguity in C API return values
5. All N-API functions failing (nm_modname mismatch)
6. Single function failing (name inconsistency across layers)
7. Header file too large for single read (chunked reading strategy)

**Working Code Examples:**

- Complete N-API wrapper templates in `test_generation_c.md`
- ETS test case templates in `_common.md`
- Full project template in `template_project/`
- Working automation scripts in `scripts/`

**Score Justification**: Very high usability. Agent can immediately act on the guidance without guessing. -1 because the retry strategy in error handling lacks exponential backoff guidance, and Phase 8 (device testing) has no failure mode documentation despite being 268 lines long.

---

## Critical Issues

None found. This Skill has no fundamental design flaws.

---

## Top 3 Improvements

### 1. Reduce Redundant Code Templates in References (Impact: D1 +4)

**Problem**: `test_generation_c.md` (581 lines) contains 5+ near-identical copies of the same ~30-line N-API wrapper boilerplate (sections 2.2-2.5, 3.1-3.4). Claude can generate standard N-API wrappers from a specification — repeating the full code template for each test type wastes ~200 lines of context.

**Specific Fix**: Replace the repeated code templates with a constraint table:

```markdown
### N-API Wrapper Constraints (applies to ALL test types)

| C Parameter Type | napi_get_value_* | napi_create_* | Notes |
|-----------------|-------------------|---------------|-------|
| int32_t | napi_get_value_int32 | napi_create_int32 | |
| char* | napi_get_value_string_utf8 | napi_create_string_utf8 | Allocate with malloc, free after use |
| bool | napi_get_value_bool | napi_get_boolean | |
| float/double | napi_get_value_double | napi_create_double | |
| pointer (caller-frees) | napi_wrap + napi_finalize | napi_create_external | Register finalize callback |
| pointer (system-managed) | — | napi_create_external | No finalize needed |

Keep ONE complete template (e.g., section 3.1) as reference. Replace sections 3.2-3.4 with:
"For ERROR/BOUNDARY/MEMORY tests, apply the same wrapper structure with test-type-specific
modifications described in Section VII rules."
```

Also remove `_common.md` Section IV (lines 224-308, ~85 lines) — standard N-API API documentation Claude already knows.

**Expected savings**: ~285 lines of redundant content → D1 improves to ~18-19.

### 2. Condense Inline Phase Guidance (Impact: D5 +1, D7 +1)

**Problem**: SKILL.md lines 139-220 (~80 lines) contain inline summaries for each Phase that duplicate information already present in the corresponding `prompts/phase-X-*.md` files. Since the Agent MUST load the prompt file to execute the Phase, the inline summary is redundant routing information.

**Specific Fix**: Replace the detailed inline guidance with a concise Phase-at-a-glance table:

```markdown
### Phase Quick Reference

| Phase | MANDATORY Load | Conditional Load | Do NOT Load |
|-------|---------------|-----------------|-------------|
| 1 | `references/subsystems/_common.md` | Subsystem `_common.md` if specified | All modules/ |
| 2 | `modules/L1_Analysis/parser/unified_api_parser_c.md` | — | `project_parser.md` |
| 3 | `modules/L1_Analysis/analyzer/coverage_analyzer.md` (Flow A) | — (Flow C skips) | — |
| 4 | `prompts/phase-4-design.md` (self-contained) | — | — |
| 5 | `test_generation_c.md` + `test_patterns_napi_ets.md` | `_advance.md` for callbacks | All L1, L3 modules |
| 6 | `prompts/phase-6-verification.md` + scripts | `verification_common.md` if unclear | — |
| 7 | `prompts/phase-7-build.md` + scripts | `build_workflow_c.md` if unclear | `linux_compile_env_setup_c.md` |
| 8 | `prompts/phase-8-test-execution.md` | — | — |
| 9 | `prompts/phase-9-output.md` | — | — |
```

This reduces ~80 lines to ~15 lines while preserving all routing information.

**Expected improvement**: SKILL.md drops from 402 to ~335 lines, closer to Process pattern ideal.

### 3. Add Subsystem-Specific Memory Ownership Quick Reference (Impact: D8 +1)

**Problem**: The "NEVER ignore memory ownership transfer" anti-pattern (lines 288-294) correctly identifies the issue but the fix is generic. Different subsystems have different conventions for which functions allocate memory that callers must free.

**Specific Fix**: Add a subsystem-specific memory convention table to `references/subsystems/_common.md`:

```markdown
### Memory Ownership Quick Reference by API Prefix

| API Prefix | Allocation Convention | Free Function | N-API Strategy |
|-----------|----------------------|---------------|---------------|
| OH_NativeBundle_*Get* | System-managed | None | napi_create_external |
| OH_NativeBundle_*Create* | Caller-frees | OH_*Destroy | napi_wrap + napi_finalize |
| OH_Camera_*Create* | Caller-frees | OH_Camera_*Delete | napi_wrap + napi_finalize |
| OH_Log* | No allocation | N/A | Direct napi_create_* |

When encountering a new subsystem, check .h comments for "caller must free" / "owned by system" indicators.
```

This would give Agents a fast path for the most common memory ownership decisions.

---

## Appendix: Eval Coverage Analysis

The Skill includes 3 evaluation cases:

| Eval ID | Name | Flow Tested | Coverage |
|---------|------|-------------|----------|
| 1 | capi-flowb-hilog-core | Flow B (standard) | Full N-API pipeline, triple verification, @tc annotations |
| 2 | capi-flowa-hilog-coverage | Flow A (coverage-driven) | Supplement existing project, uncovered APIs |
| 3 | capi-newproject-zlib | New project creation | Template copy, complete project structure |

**Assertion count**: 30 total assertions across 3 evals — strong coverage of the key quality gates (triple consistency, nm_modname, @tc annotations, Hypium framework, import paths).

**Gap**: No eval tests error handling / retry scenarios (e.g., "N-API wrapper has wrong type conversion, Agent should detect and fix"). Consider adding an eval that starts with intentionally broken code.

---

*Report generated: 2026-06-05*
*Evaluator: skill-judge (self-evaluation against specification)*
