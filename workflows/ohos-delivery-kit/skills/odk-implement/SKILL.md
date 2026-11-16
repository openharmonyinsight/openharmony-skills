---
name: odk-implement
description: "Use when implementing an approved execution-plan.md Task-by-Task and backfilling code scope. Default: TDD 失败/通过循环（Red/Green）——先写失败测试，再实现让其通过. Zero plugin dependencies. Use after execution-plan.md approval."
license: MIT
---

# ODK Implement

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and obtain the effective
contract before choosing artifacts, sections or phase prerequisites.
<!-- /ODK:reference -->

## Purpose

Use after `execution-plan.md` has been approved. This is the **base layer** command — AI-assisted implementation guided by the plan, with zero plugin dependencies.

## Prerequisites

- Load `using-odk` first.
- `spec.md` exists with numbered ACs.
- `execution-plan.md` exists with Task IDs, AC-Task traceability, file-level scope, and verification commands.
- The user has approved implementation.
- Before the first build, verify the plan's `产品选择确认` against the user's actual product choice. A product copied from config or a generated command is not confirmation; missing evidence must be resolved using the shared build-product guide before compilation.

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/feedback.md -->
Read `contracts/skill-guides/delivery/feedback.md` for test failures or deviations.
Route corrections to their owning artifacts, record findings in the existing
plan, and set Verification Final Status from the current verification outcome.
<!-- /ODK:reference -->

For a plan explicitly scoped `host-only`, verify that every Task's command is a
repository-local host/document/configuration check with no target build, emulator,
flashing or device dependency. Execute and record those commands directly; skip
product selection, firmware preparation and final device integration. If any Task
needs a target/device, update the plan and follow the existing product safeguards.

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

0. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `codespec/changes/<repo-name>/<proposal-id>/spec.md` AC list and `execution-plan.md` 代码范围映射 (Task → file).
2. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list, dependency graph, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
   Treat the `spec.md` ACs and the execution principles in `execution-plan.md` as authoritative, then proceed in Task order.
3. **读取 execution-plan.md 国际化依赖（proposal中 i18n = 「是」时）**：
   从 plan 生成的 `execution-plan.md` 的 Task 详情中提取 i18n 调用信息（调用场景、仓路径、接口/方法）。
4. For each Task (respecting dependency order):
   - Present the Task description and planned file scope.
   - Start with the Task's declared read-only context. For impact discovery,
     read-only searches may extend within the authorized repository; add relevant
     new context to the Task before using it as an edit basis. Update file scope
     under the existing plan rules before modifying any newly discovered file.
   - **Analyze existing code patterns** for the Task's file scope:
     - Identify the change type (new API, query method, callback, member variable, etc.)
     - Search for similar existing functions — prefer files within the Task's declared file scope first, then widen to the same subsystem/layer
     - Study the conventions those functions follow: call chain layering, naming patterns, error handling, state management, logging/DFX, and interface contracts
     - Record the reference pattern, e.g.: "Call chain: `native_api → NativeEngine → ArkNativeEngine → DFXJSNApi → EcmaVM`" or "Naming: query APIs use `GetXxx()` returning `int32_t` with `napi_status` error code"
      - Follow the same conventions unless the user explicitly approves a deviation
      - **公开符号导出（条件触发：`API/SDK` = 是，或改动安装态公开头如 `jsnapi_expo.h`/`native_api.h`）**：新增/变更暴露到公开头的符号时，检查仓的符号导出/可见性文件（`.map` 如 `libark_jsruntime.map`、`.symdef`、`__attribute__((visibility))`），为新符号补齐导出条目；否则下游 `.so` 会因缺符号链接失败。
      - **测试落位与 fixture 复用**：优先在既有测试文件（`*_tests.cpp` / `*_test.cpp`）追加用例并复用既有 fixture（如 `TestHelper::CreateEcmaVMWithScope`、`HWTEST_F_L0`），而非为小变更新建独立大文件；新建前确认无既有测试入口可挂靠。
      - **版权年同步**：修改既有源文件时，将版权头年份更新为当前年（如 `2021-2024` → `2021-2026`）；新增文件直接写当前年。
      - If no similar function exists, note "no prior art found" and proceed without a pattern reference
   <!-- ODK:reference contracts/skill-guides/delivery/implementation-quality.md -->
   For code Tasks, read `contracts/skill-guides/delivery/implementation-quality.md`
   before choosing an implementation. Use it again for the completion check;
   assess the language/runtime, relevant repository patterns and actual workload.
   Apply its affected-path check before editing and before marking completion;
   reuse valid planning evidence and refresh changed query/test inputs.
   Follow its role boundaries: self-review inline Tasks, and use the existing
   configured handoff for review of the whole change.
   <!-- /ODK:reference -->
   - **Cross-repo interface confirmation (conditional)**: If the Task calls or consumes interfaces from another OpenHarmony repo (identified from execution-plan's code scope, design's module impact table, or i18n dependency analysis), verify the actual interface behavior at the source repo, not just from spec.md or header files:
     - Locate the upstream repo (from design.md module impact table, execution-plan task dependencies, or by asking the developer for the local path)
     - Read the interface's actual implementation (not just declarations): function body, return value semantics, error conditions, threading/concurrency requirements, lifecycle assumptions, and hidden side effects
     - If the repo is not locally available, ask the developer for the path; do not assume interface behavior from declarations alone
     - Record confirmed facts as `// cross-repo: <repo>/<file>:<line> — <interface>: <confirmed behavior>` in the Task's Actual Result
     - If the confirmed behavior contradicts spec.md or design.md assumptions, stop and apply the feedback procedure before continuing implementation
     - This step is mandatory when the called interface's behavior is non-trivial (returns error codes, has threading constraints, modifies shared state, or involves IPC); for trivial getters/setters it may be skipped with a note
   - **TDD 失败/通过循环（Red/Green，所有代码 Task 的默认方式；降级规则见下）：**
     1. **Red（失败）** — Write or update the failing test(s) covering this Task's ACs. **For Tasks whose ACs appear in `design.md` `### DFX 故障模式处置` `关联 AC` column, the Red step IS the fault-injection test** — write the fault-injection/exception-path test first (per the 验证方式/证据 column), confirm it fails for the right reason, and use that failure output as the Red evidence. Record the failure output as the first entry in `Actual Result` under a `[失败 Red]` label; do not erase it in later steps.
     2. **Green（通过）** — Implement the minimal code required to make the failing test(s) pass. Do not write more code than needed to pass the tests.
     3. **Build & Verify（编译与验证）** — Read the resolved commands from `execution-plan.md` `## 构建与验证环境` table (populated by `odk-plan`; do not re-read config for a confirmed snapshot). If the section is absent, follow the product-selection guide below first; obtain or recover an explicit choice, then resolve `{product}` and append the environment table. Never fill and execute an old plan directly from the configured default.
        <!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
        Read `contracts/skill-guides/delivery/build-products.md`. Reuse the plan's `编译产品`, `可选编译产品` and actual `产品选择确认`. If confirmation is missing or the user requests a switch, show the configured menu and wait for an explicit choice; configuration, generic plan approval or a generated build command alone does not confirm a product. Reuse a real confirmed choice for subsequent Tasks. For old plans, recover actual prior confirmation or ask once before compiling.
        <!-- /ODK:reference -->
        Read `验证范围`, `验证产品` and `验证目标确认` separately from `编译产品`. A concrete or abstract build name does not select a runtime target. Recover missing old-plan confirmations or ask before runtime verification. On a build-name/target/scope switch, update the corresponding snapshot and re-resolve affected commands via `--resolve-product-commands`; never globally replace one product string with another. Clear the emulator command outside `emulator`. Recheck artifact compatibility after build changes; invalidate device preparation, deployment and runtime test evidence after validation-product or device-ID changes. Determine the Task command shape, then apply a–d only where the explicit validation scope requires them:
        <!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
        Read `contracts/skill-guides/delivery/device-version.md` and consume the recorded strategy. `host-only`/`build-only` never ask for daily; `emulator` uses its confirmed validation target without physical firmware preparation. Only `device` chooses daily/existing for the validation product. Reuse preparation only for the same confirmed product and actual device.
        <!-- /ODK:reference -->
        - **Test-only Task** (only a test runner): skip a and artifact pushing. In `device`, still select and prepare the device via b; in `emulator`, execute c, then d. A build-only plan may run host checks but must not contain device/emulator commands.
        - **Build+test Task** (验证命令 contains `&&` separating a build and test command): execute all four sub-steps a → b → c → **d**.
        - **Build-only Task** (验证命令 contains only a build command, no `&&` test step): execute a → b → c, then use `测试命令` from `## 构建与验证环境` as sub-step **d**.

        Scope controls execution: `build-only` runs a and any recorded host check, skips b/c and skips d when its command is N/A; `device` uses b; `emulator` uses c. Never choose b/c by comparing the build name to arm64_virt or rk3568.

        Before an applicable, explicitly confirmed flash invokes its configured skill, read `contracts/skill-guides/router/configured-skills.md`; install it from matching config comment links if missing in the current agent, verify availability, then resume. Pending installation blocks device preparation.

        a. **编译**：run the build portion of the Task's `验证命令` field (single-module `--target <module>` or full build). Stop if the build fails.
        b. **设备准备（仅验证范围=device）**：
           - **刷机适用条件（所有入口共用）**：automatic daily flashing requires scope `device`, confirmed `验证产品=rk3568`, and non-empty `device_flash_skill`. The concrete or abstract build name is not part of this test. Keep the selected-device and explicit overwrite confirmation requirements. Other validation products need a confirmed supported manual preparation method. Reuse successful preparation only for the same validation product and actual device.
           - **推送编译产物**：find the `.so` files produced by this Task's build that correspond to the Task's changed source files:
             - **产物目录**：use explicit `device_so_dirs` when configured; otherwise start at `out/<plan 编译产品>/`, using the exact same concrete or abstract name as the build command. Locate actual libraries within that root using this Task's build log, output manifest or confirmed layout (e.g. lib/ or lib64/), matching component target and architecture/variant. Never replace the output product name with `验证产品`. Confirm artifact/device compatibility; ambiguous provenance or multiple candidates require confirmation before pushing. Record actual paths, build evidence and target binding in `Actual Result`. Test-only Tasks push no artifacts.
             - **服务推断**：if `device_service_restart` is non-empty use that command (replace `{service}`); otherwise look up the component's init `.cfg` file or systemd unit filename for the service name. If the service name cannot be determined, fall back to `hdc shell reboot` and wait for the device to return — record "service inference failed, used full reboot" in `Actual Result`.
             - **设备连接检测**：before pushing, run `hdc list targets` to detect connected devices. Filter out emulator entries (any device ID that appeared in sub-step c's emulator boot) — only consider physical board devices:
             - **发现设备**：select the actual hdc device ID (ask if multiple), confirm its product identity matches the plan's validation product, then apply the recorded version strategy. A device ID is not a product name; unknown or mismatched identity blocks preparation/pushing until confirmed:
               - `existing`: use the firmware already on the device and proceed to 推送步骤. Do not offer daily again or claim the firmware is today's daily.
               - `daily`: if preparation has already succeeded for this device and is recorded in `Actual Result`, reuse it. Otherwise follow the plan's `设备版本准备方式`. For an automatic skill, recheck the rk3568/config conditions above, pass the selected device ID, and obtain explicit confirmation before overwriting device data. If the conditions fail, do not invoke the skill; confirm a supported manual preparation method and update the plan. For manual preparation, wait for the user to confirm completion. Do not silently fall back to existing firmware when preparation fails or is incomplete.
               - After flashing, re-detect and confirm the target device before pushing. Record the preparation outcome and device ID for subsequent Tasks.
             - **未发现设备**：if `hdc list targets` returns no physical devices or returns an error, prompt:
               ```
               未检测到 hdc 设备，请选择：
               A) 输入设备 IP 地址（使用 hdc tconn <ip>:<port> 连接，默认端口 7777）
               B) 跳过设备验证

               设备 IP：
               ```
               If the user provides an IP, run `hdc tconn <ip>:7777` (or the port the user specifies), wait for the connection to succeed, then re-run `hdc list targets` to confirm and apply the same recorded version strategy under 发现设备 before pushing. If connection fails, report the error and offer to retry or skip. If the user picks B, skip the 推送步骤 below and proceed to sub-step d.
           - **推送步骤**：`hdc -t <device-id> shell mount -o rw,remount /`, push each confirmed `.so` via `hdc -t <device-id> file send <local> /system/lib/<name>` (use `/system/lib64/` for 64-bit libs), then execute the restart command. Record the resolved paths, device-id, and service name in `Actual Result`.
        c. **模拟器启动与 hdc 推包（仅验证范围=emulator）**：use the separately confirmed validation product, even when the build name is abstract:
           1. Before starting the emulator, run `hdc list targets` once and record the **pre-boot baseline**. Existing entries are not the emulator being started now.
           2. Run the `模拟器命令` row value from `## 构建与验证环境` to start qemu.
           3. Poll `hdc list targets` every 10 seconds until one or more **new** devices appear that were not in the pre-boot baseline; abort and report failure if no new device appears after 3 minutes.
           4. Confirm emulator identity — always ask, even for a single new device:
              - List all newly appeared devices and prompt the user:
                ```
                模拟器启动后检测到以下新设备：
                  1) <device-id-1>
                  2) <device-id-2>  （如有）
                请确认哪个是本次启动的模拟器？输入序号：
                ```
              - Wait for explicit user confirmation before proceeding. Never auto-select. This is required even when only one new device appeared, because a physical board plugged in during the wait is indistinguishable from the emulator by device ID alone.
              - Use the user-confirmed device ID as `<emulator-id>` for all subsequent hdc commands.
           4. Run `hdc -t <emulator-id> shell mount -o rw,remount /` first to make the filesystem writable.
           5. For Tasks with build outputs, apply b's artifact provenance/path/architecture checks against this validation product, record actual paths and emulator ID, then push the confirmed files with `hdc -t <emulator-id> file send <local> /system/lib/<name>` (or `/system/lib64/`). Test-only Tasks skip pushing and service restarts.
           6. Restart the relevant service: `hdc -t <emulator-id> shell <restart-command>`.
           7. Do not run this step for `device` or `build-only`; the build product name never selects this branch.
        d. **推包/测试**：run the test portion of the Task's `验证命令` field, or the `测试命令` row from `## 构建与验证环境` for build-only Tasks.
        Record the passing output as a `[验证 Verify]` entry in `Actual Result`, appending after the `[失败 Red]` entry — do not overwrite it.
     4. **Quality check & refactor** — Before completing a code Task, self-review its actual diff using the implementation-quality guide. This check is required; rewriting needs a concrete reason. Assess applicable readability, idiom, allocation/copy and complexity risks even when functional tests pass. Keep a suitable implementation, repair a demonstrated issue within scope and rerun affected tests, or record the specific evidence still needed. Append material choices and their basis to the existing `Actual Result`; route unresolved blocking findings through the feedback procedure before marking the Task Done. Task self-review does not replace the configured final review.
     5. **Task review gate** — After verification and the quality check, before marking the Task Done, invoke `odk-task-review`. It implements `contracts/skill-guides/delivery/task-review.md` with role-specific review, candidate validation and scoped fix re-review. Pass the Task's `风险等级`, full Task baseline/current diff (including untracked files), related ACs/decisions and verification paths:
        - `R0`: record `Task review: 不适用（R0：<理由>）` in `Actual Result` and skip reviewer dispatch. Code changes are never R0.
        - `R1`: one reviewer runs all five lenses and writes `evidence/reviews/task-<n>/verdict.md`.
        - `R2`: dispatch the fixed arch/scope/security seats and write `arch.md`, `scope.md`, `security.md`, `verdict.md`.
        - If the actual diff hits a new R2 trigger, append `风险升级 R1→R2（触发文件：<path>）` to `Actual Result`, update the Task-list `风险等级` cell to `R2`, and review as R2. Downgrading needs a recorded reason plus coordinator confirmation.
        - Before dispatch, run `python3 <executables>/lib/odk_host_capabilities.py --host <host>` from the resource-check executables directory. If it reports `can_delegate: false` or the probe fails, perform three sequential read-only passes (arch → scope → security) and write `independent: false` in `verdict.md`.
        - Use the skill's arch/scope/security role guides with one shared input snapshot. Reviewers are read-only and must not dispatch further reviewers; the coordinator validates findings and writes evidence.
        - Unresolved `Critical`/`High` findings: set `verdict: FAIL`/`BLOCKED` with `blocking_findings > 0`, run the feedback procedure for required spec/design/scope changes, mark the Task `❌ Blocked` in the Task list, do not mark it Done, and do not start the next Task. `Medium`/`Low` are advisory. Unverifiable items are recorded as `待确认`, never Pass; they block only when tied to a High risk point.
        - After fixes, use the skill's bounded re-review against stable finding IDs and affected verification evidence; old verdicts never cover changed inputs. Only `verdict: PASS` with `blocking_findings: 0` allows Done.
        - Summarize back to the main context in ≤15 lines: verdict path, per-dimension pass/fail, blocking count.
   - **TDD degradation rule:** If a Task genuinely cannot have an automated test — pure documentation, a configuration file that cannot be exercised by any test runner in this repository (document why), or a build system change with no runnable gate — state the reason explicitly before proceeding, record it in `Actual Result` as "TDD degraded: <reason>", and substitute a reproducible manual verification step. Do not degrade silently or skip verification entirely. A code change that touches business logic is never eligible for degradation even if it is delivered via a config or data file.
   - **API 声明文件生成（条件触发 — Task-1）**：如果当前是 plan 中的第一个 Task（API 声明文件 Task-1）且 `API/SDK` = 是：
     - 读取并校验所有适用的 `arkts-api-spec.yaml`、`c-api-spec.yaml`。它们是唯一 API 契约源；`spec.md` 必须声明 `API 契约版本 | 1.0.0`。不得从 `spec.md` 概览、既有声明文件或历史会话反推契约。若元数据缺失、非法、未确认，或存在旧 `api-spec.yaml`、旧混合语言声明 diff、旧逐 API Markdown 契约链路，停止 Task-1；可识别的 0.14 旧 Markdown 链路先路由到 `{{CMD_PREFIX}}upgrade-api-chain`，若升级助手无法闭环全部事实，再要求从 `proposal` 重新运行完整流程。Blocking mismatch 必须列出全部受影响产物、声明版本、要求版本 `1.0.0` 和迁移文档，并使用以下 action，不得建议手改版本字段：
   ```text
   Action:
   Do not implement Task-1.
   Restart the full API SDD flow from proposal.

   Required flow:
   proposal -> spec -> design -> plan -> implement

   Migration guide:
   docs/migrations/0.15.0-api-metadata-hard-migration.md
   ```
     - 获取 API 声明仓库路径（spec 阶段过程信息不落盘）：若本会话已有 spec 阶段确认的 `interface_sdk-js` / `interface_sdk_c` 本地路径，直接使用；否则询问开发者提供（不一定是绝对路径，只要能定位到即可）
     - **切分支（必须）**：API 声明仓库通常被多个需求共享，必须在修改声明文件前切出专用分支，避免多个需求的改动互相覆盖、diff 混淆。分支名建议关联 proposal ID，如 `feature/proposal-12345-arkui-focus`；询问开发者确认分支名或由开发者手动切好后告知分支名
     - **阅读仓库根目录的 `AGENTS.md`**：学习该仓库的 API 设计规范、命名约定、目录结构约定、声明文件格式要求等知识，作为生成声明文件的参照。AGENTS.md 中的内容与既有声明文件的实际格式共同构成格式参考，二者冲突时以 AGENTS.md 为准
     - 阅读仓库中与变更最相关的既有声明文件（≤10 个），仅提取格式规范（版权头、注释结构、命名风格），不得用其内容填补 metadata 文件缺口
     - 根据适用 metadata 文件逐 API、逐字段生成或修改声明文件：
       - ArkTS 声明写入 API 声明仓库中对应的 `.d.ts` / `.d.ets` 目录（参照仓库既有目录结构和命名约定）
       - C 声明写入 API 声明仓库中对应的 `.h` 目录（参照仓库既有目录结构和命名约定）
       - 每个元数据 API 必须生成对应声明；签名、参数、返回值、错误码、权限、`@syscap`、`@since`、平台、模型和设备差异必须逐字段消费
       - 声明注释直接使用 metadata 文件中的 description、参数描述、返回值描述和错误码描述；不得改写契约语义或遗漏要素
       - **描述正文闭包（必须）**：API 级 `description.en` / `description.zh` 的 8 个字段必须全部进入对应语言声明注释正文，顺序固定：
         1. `function`
         2. `scenario`
         3. `effect`
         4. `similarAPIs`
         5. `defaultBehavior`
         6. `constraints`
         7. `activation`
         8. `notes`
         - 字段值为 `N/A` / `不适用` 时必须完全省略该字段；不得在 JSDoc / Doxygen 中输出 `N/A`、`不适用` 或仅由该占位值组成的空段落；非 `N/A` 字段不得合并成一句、不得截断、不得只写 `function`
         - 每个字段的值直接作为独立一行或独立段落写入 JSDoc/Doxygen 正文，语义和措辞必须与 YAML 保持一致；不得输出字段名或要素类型前缀（如 `Scenario:`、`Effect:`、`Notes:`、`使用场景：`）
         - `parameters[].description` 必须逐参数进入 `@param` / `@param[in/out]` 描述；`returnType.description` 必须进入 `@returns` / `@return`；`errorCodes[].description` 必须进入错误码说明或仓库规范要求的错误码注释结构
         - 参数、返回值、错误码注释不得复用既有声明文案；必须以当前 metadata 文本为唯一来源
       - 声明文件须包含 Apache 2.0 版权声明头和完整声明注释（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）
       - **注释排版（必须）**：`/**` 必须与声明保持同缩进；注释正文和 `*/` 按仓库既有风格对齐；`*/` 与声明之间不得插入空行，注释内部不得插入空行。不得输出 `/**` 缩进漂移或 `*/` 后连续空行
       - **描述去重（必须）**：若 metadata 中 API 级描述与参数/返回值描述重复表达同一事实，停止 Task-1 并要求回到 `odk-spec` 修正 metadata；不得在声明文件中自行删改契约，也不得把重复文案写入声明注释
     - **按需调用 oh-api-definition 质量检查（可选，不阻塞）**：
       - 若开发环境已提供 oh-api-definition，则对新修改的声明文件执行其格式、命名、注释和语法检查；发现问题时修复后重跑
       - 若工具不可用时在 Task `Actual Result` 记录未执行并继续，不要求安装，也不得因此阻塞 Task-1
    - **按语言生成声明注释双语 diff（英文 + 中文）**：完成适用的质量检查后，基于同一修改前基线生成 diff，并按 API 声明仓库/语言拆分归档到 `codespec/changes/<repo-name>/<proposal-id>/evidence/` 目录下，作为变更证据：
      - ArkTS 仓库（存在 `arkts-api-spec.yaml` 时必选）：
        - **英文声明注释 diff**（文件名固定为 `task1-arkts-api-declaration-en.diff`）：`interface_sdk-js` 声明文件的实际修改内容，声明注释使用英文 JSDoc——这是提交到 ArkTS API 声明仓库的版本
        - **中文声明注释 diff**（文件名固定为 `task1-arkts-api-declaration-zh.diff`）：签名、代码、版权头与标记（`@syscap`/`@since`/`@kit`/`@permission` 等）与英文版完全一致，仅将声明注释的描述正文改为中文；中文内容以 `arkts-api-spec.yaml` 的 `description.zh`、参数描述、返回值描述和错误码描述为源头
      - C 仓库（存在 `c-api-spec.yaml` 时必选）：
        - **英文声明注释 diff**（文件名固定为 `task1-c-api-declaration-en.diff`）：`interface_sdk_c` 声明文件的实际修改内容，声明注释使用英文 Doxygen 或仓库既有注释规范——这是提交到 C API 声明仓库的版本
        - **中文声明注释 diff**（文件名固定为 `task1-c-api-declaration-zh.diff`）：签名、代码、版权头与标记与英文版完全一致，仅将声明注释的描述正文改为中文；中文内容以 `c-api-spec.yaml` 的 `description.zh`、参数描述、返回值描述和错误码描述为源头
      - **约束**：每个 diff 文件只允许包含其对应 API 声明仓库的路径；不得把 `interface_sdk-js` 与 `interface_sdk_c` 的变更混入同一份 evidence。中文版仅作为归档证据，不写回 API 声明仓库、不替代英文声明文件。所有 diff 均不得改变任何签名、入参、返回值、错误码或标记
      - **完整连续证据（必须）**：每个目标 API 的完整声明注释块（从 `/**` / `/*!` 到 `*/`）和对应声明必须出现在同一个连续 hunk 中；生成 diff 时使用足够上下文或按 API 裁剪 hunk，不得依赖默认 3 行上下文导致只提交签名变更。若同一文件中存在多个同签名声明，声明注释必须包含 API ID / qualifiedName，或提供可唯一关联的源位置，避免多复用同一证据
      - **生成后闭包校验（必须）**：Task-1 生成 diff 后立即运行 `python3 <executables>/validate-artifacts-contract.py <change-dir> --phase plan`；`<executables>` 使用 resource-check 已解析的目录（源码布局为 `scripts`，安装布局为 `runtime/executables`）。若出现 `API declaration description.* missing or mismatched`、参数/返回值/错误码描述缺失或不一致，必须回到声明注释与 diff 修复并重跑；不得修改 YAML 契约来迎合已生成文案，也不得用人工声明替代该校验
      - Task-1 之后若声明文件被任何后续任务或人工修改，必须重新生成对应语言 diff 并重跑上述校验；不得出现“声明文件已更新、diff 仍是旧内容”的证据漂移
   - After each Task, update `execution-plan.md` 代码范围映射 with actual files, tests, and commit references.
   - Backfill the Task's `Actual Result` with final completion evidence, appending after any `[失败 Red]` and `[验证 Verify]` entries already recorded — do not overwrite them.
   - Mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
5. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ 已完成（Done） / ❌ 阻塞（Blocked） / ⚠️ 跳过（Skipped，附原因）
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
6. If implementation reveals missing ACs, a design deviation or changed verification assumptions, apply the feedback procedure to the affected proposal/spec/design/plan and existing dependent artifacts. Resolve only genuinely new scope/design decisions with the user; do not weaken ACs to fit a bug or leave the correction solely in a report.
7. Keep changes within the Task file scope unless the user approves an execution-plan update.
8. When any `资源开销审视` dimension is `required` (`contracts/artifacts.yaml#resource_contract`), complete subsystem measurement/evidence Tasks and the business-repo `odk_resource_gate` (commonly under `evidence/resource/`).
9. After all Tasks are Done, **prompt about final device integration verification only for scope `device`**, before the automatic handoff. Show the validation product, actual device ID, strategy and preparation result. Reuse firmware prepared for that exact target; do not ask daily/existing again or reflash automatically. Needed preparation still follows b: automatic flashing requires `验证产品=rk3568`, non-empty `device_flash_skill` and explicit selected-device overwrite confirmation. Product/device changes invalidate the old preparation and test evidence.
   `build-only` skips device integration and records runtime verification as not performed; `emulator` uses the confirmed validation product and c/d results, without a physical-device/daily prompt.
   After this prompt, automatically follow the handoff below; do not require separate review/validate commands from the user.

## Output

<!-- ODK:reference contracts/skill-guides/delivery/handoff.md -->
When implementation is complete, read and follow `contracts/skill-guides/delivery/handoff.md`: automatically review and validate using the skills listed in `pre_commit_reviews` (config), remind and wait for the user to trigger source PR submission, prepare `metadata_tracking.yaml` from the actual PR, invoke any `post_commit_reviews` skills after PR URL is confirmed, then ask separately about design-docs. No automatic merge.
<!-- /ODK:reference -->

Report:

- **Execution Summary:** every Task listed with status (✅ 已完成（Done） / ❌ 阻塞（Blocked） / ⚠️ 跳过（Skipped）) and reason for any incomplete Tasks
- Tasks completed and status changes written to `execution-plan.md`
- Reference patterns used (architectural conventions followed or "no prior art found")
- Verification results per Task
- Code mapping rows updated in `execution-plan.md` 代码范围映射
- Any deviations from `execution-plan.md` or reference patterns (with justification)
- Before GitCode submission, the separate `codespec/` publication reminder and the developer-provided `design_docs_repository` address (or “待开发者填写”)

If any Task is incomplete, report the gaps and stop; do not start the automatic handoff.
