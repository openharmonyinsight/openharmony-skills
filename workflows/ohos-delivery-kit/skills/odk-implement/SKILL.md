---
name: odk-implement
description: "Use when implementing an approved execution-plan.md Task-by-Task and backfilling code scope. Default: TDD 失败/通过循环（Red/Green）——先写失败测试，再实现让其通过. Zero plugin dependencies. Use after execution-plan.md approval."
license: MIT
---

# ODK Implement

## Purpose

Use after `execution-plan.md` has been approved. This is the **base layer** command — AI-assisted implementation guided by the plan, with zero plugin dependencies.

## Prerequisites

- Load `using-odk` first.
- `spec.md` exists with numbered ACs.
- `execution-plan.md` exists with Task IDs, AC-Task traceability, file-level scope, and verification commands.
- The user has approved implementation.

## Steps

0. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `codespec/changes/<repo-name>/<proposal-id>/spec.md` AC list and `execution-plan.md` 代码范围映射 (Task → file).
2. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list, dependency graph, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
   Treat the `spec.md` ACs and the execution principles in `execution-plan.md` as authoritative, then proceed in Task order.
3. For each Task (respecting dependency order):
   - Present the Task description and planned file scope.
   - Read only the Task's declared read-only context before editing.
   - **Analyze existing code patterns** for the Task's file scope:
     - Identify the change type (new API, query method, callback, member variable, etc.)
     - Search for similar existing functions — prefer files within the Task's declared file scope first, then widen to the same subsystem/layer
     - Study the conventions those functions follow: call chain layering, naming patterns, error handling, state management, logging/DFX, and interface contracts
     - Record the reference pattern, e.g.: "Call chain: `native_api → NativeEngine → ArkNativeEngine → DFXJSNApi → EcmaVM`" or "Naming: query APIs use `GetXxx()` returning `int32_t` with `napi_status` error code"
     - Follow the same conventions unless the user explicitly approves a deviation
     - If no similar function exists, note "no prior art found" and proceed without a pattern reference
   - **TDD 失败/通过循环（Red/Green，所有代码 Task 的默认方式；降级规则见下）：**
     1. **Red（失败）** — Write or update the failing test(s) covering this Task's ACs. **For Tasks whose ACs appear in `design.md` `### DFX 故障模式处置` `关联 AC` column, the Red step IS the fault-injection test** — write the fault-injection/exception-path test first (per the 验证方式/证据 column), confirm it fails for the right reason, and use that failure output as the Red evidence. Record the failure output as the first entry in `Actual Result` under a `[失败 Red]` label; do not erase it in later steps.
     2. **Green（通过）** — Implement the minimal code required to make the failing test(s) pass. Do not write more code than needed to pass the tests.
     3. **Build & Verify（编译与验证）** — Read the resolved commands from `execution-plan.md` `## 构建与验证环境` table (populated by `odk-plan`; do not re-read config). If the section is absent (plans created before ODK 0.14.0), read `build_product`, `build_command`, `emulator_command`, `test_command` directly from config (odk_config_ext.yaml overrides config.yaml), resolve `{product}`, append the `## 构建与验证环境` table into the plan, and proceed — so the plan is upgraded in place rather than failing.
        **Before the first build in this session**, confirm the target product with the user once — reuse the confirmed product for all subsequent Tasks in this session without re-asking unless the user explicitly requests a switch. Skip this prompt if `## 构建与验证环境` in `execution-plan.md` already has a resolved `编译产品` row — "resolved" means the row contains a literal product name (e.g. `arm64_virt` or `rk3568`) with no placeholder braces `{}`, question marks, or inline conditionals, as written by `odk-plan` — and the user has not requested a change:
        ```
        当前编译产品：<plan 表中的值>
        请选择（直接回车确认，或输入切换）：
        A) arm64_virt — qemu 模拟器验证
        B) rk3568    — 物理板验证
        ```
        If the user switches product: (1) update the `## 构建与验证环境` table's `编译产品` row; (2) re-resolve `{product}` in all remaining Task `验证命令` fields that still contain the old product name — replace the old product name with the new one; (3) when switching away from `arm64_virt`, clear the `模拟器命令（仅 arm64_virt）` row (mark N/A) so the plan does not leave a stale emulator command under a non-arm64_virt product; when switching to `arm64_virt`, populate the `模拟器命令` row from config. Do not re-ask on subsequent Tasks unless the user requests another switch. Determine the shape of the Task's `验证命令` field first, then execute the sub-steps labelled a–d below accordingly:
        - **Test-only Task** (验证命令 does not begin with a build tool invocation such as `./build.sh`, `ninja`, `make`, or similar — only contains a test runner command): skip sub-steps a and b; execute c (arm64_virt only) then **d** (the test runner).
        - **Build+test Task** (验证命令 contains `&&` separating a build and test command): execute all four sub-steps a → b → c → **d**.
        - **Build-only Task** (验证命令 contains only a build command, no `&&` test step): execute a → b → c, then use `测试命令` from `## 构建与验证环境` as sub-step **d**.

        Sub-steps b and c are independent conditions — b fires on physical boards, c fires on arm64_virt; they never both apply to the same product.

        a. **编译**：run the build portion of the Task's `验证命令` field (single-module `--target <module>` or full build). Stop if the build fails.
        b. **设备准备（物理板路径，arm64_virt 跳过此步）**：
           - **刷入 daily 镜像（仅 rk3568，其他产品跳过）**：if `device_flash_skill` is non-empty in config AND the confirmed product is `rk3568`, confirm with the user before invoking the skill:
             ```
             准备获取今日 daily 镜像并刷机到 rk3568 设备，请确认。
             （当前选择：<confirmed product from session>）
             此操作将调用 <device_flash_skill>，会覆盖设备数据，请确认。
             ```
             Only invoke the skill after explicit user confirmation. Skip if the developer confirms the device already runs today's daily. For any product other than rk3568, skip this sub-step entirely — `device_flash_skill` only supports rk3568.
           - **推送编译产物**：find the `.so` files produced by this Task's build that correspond to the Task's changed source files:
             - **产物目录**：if `device_so_dirs` is non-empty use those paths; otherwise infer from `build_product` — search `out/{product}/lib/` and `out/{product}/lib64/` for `.so` files whose name contains the `name` field from the component's `BUILD.gn`. When multiple candidates exist, list them and ask the user to confirm before pushing.
             - **服务推断**：if `device_service_restart` is non-empty use that command (replace `{service}`); otherwise look up the component's init `.cfg` file or systemd unit filename for the service name. If the service name cannot be determined, fall back to `hdc shell reboot` and wait for the device to return — record "service inference failed, used full reboot" in `Actual Result`.
             - **设备连接检测**：before pushing, run `hdc list targets` to detect connected devices. Filter out emulator entries (any device ID that appeared in sub-step c's emulator boot) — only consider physical board devices:
             - **发现设备**：if one or more physical devices are listed, select the first one (or ask the user to choose if multiple). Then prompt whether to fetch today's daily build or use the existing firmware on the device:
               ```
               检测到设备：<device-id>

               请选择设备上的版本：
               A) 获取今日 daily 版本并刷机（需配置 device_flash_skill）
               B) 使用设备现有版本，直接推送 .so（默认）
               C) 跳过设备验证

               （无输入默认选 B）
               ```
               - If the user picks A: check whether `device_flash_skill` is non-empty in config (`odk_config_ext.yaml` overrides `odk_config.yaml`). If it is, invoke the configured skill — the skill handles downloading the daily build and flashing the device. If `device_flash_skill` is empty, warn: "device_flash_skill 未配置，无法自动获取 daily 版本，请在 odk_config_ext.yaml 中配置 device_flash_skill，或手动刷机后重试。" and fall back to B.
               - If the user picks B or gives no response, proceed to 推送步骤 below with the existing device firmware.
               - If the user picks C, skip the 推送步骤 below and proceed to sub-step d.
             - **未发现设备**：if `hdc list targets` returns no physical devices or returns an error, prompt:
               ```
               未检测到 hdc 设备，请选择：
               A) 输入设备 IP 地址（使用 hdc tconn <ip>:<port> 连接，默认端口 7777）
               B) 跳过设备验证

               设备 IP：
               ```
               If the user provides an IP, run `hdc tconn <ip>:7777` (or the port the user specifies), wait for the connection to succeed, then re-run `hdc list targets` to confirm. If connection fails, report the error and offer to retry or skip. If the user picks B, skip the 推送步骤 below and proceed to sub-step d.
           - **推送步骤**：`hdc -t <device-id> shell mount -o rw,remount /`, push each confirmed `.so` via `hdc -t <device-id> file send <local> /system/lib/<name>` (use `/system/lib64/` for 64-bit libs), then execute the restart command. Record the resolved paths, device-id, and service name in `Actual Result`.
        c. **模拟器启动与 hdc 推包（仅 arm64_virt）**：only when `编译产品` row value is `arm64_virt`:
           1. Before starting the emulator, run `hdc list targets` once and record the current device list as the **pre-boot baseline**. Any device already present is a physical board — do not treat it as the emulator.
           2. Run the `模拟器命令` row value from `## 构建与验证环境` to start qemu.
           3. Poll `hdc list targets` every 10 seconds until one or more **new** devices appear that were not in the pre-boot baseline; abort and report failure if no new device appears after 3 minutes.
           4. Confirm emulator identity — always ask, even for a single new device:
              - List all newly appeared devices and prompt the user:
                ```
                QEMU 启动后检测到以下新设备：
                  1) <device-id-1>
                  2) <device-id-2>  （如有）
                请确认哪个是本次启动的 QEMU 模拟器？输入序号：
                ```
              - Wait for explicit user confirmation before proceeding. Never auto-select. This is required even when only one new device appeared, because a physical board plugged in during the wait is indistinguishable from the emulator by device ID alone.
              - Use the user-confirmed device ID as `<emulator-id>` for all subsequent hdc commands.
           4. Run `hdc -t <emulator-id> shell mount -o rw,remount /` first to make the filesystem writable.
           5. Push the `.so` files: `hdc -t <emulator-id> file send <local> /system/lib/<name>` (use `/system/lib64/` for 64-bit libs).
           6. Restart the relevant service: `hdc -t <emulator-id> shell <restart-command>`.
           7. Do not run this step for any product other than `arm64_virt`.
        d. **推包/测试**：run the test portion of the Task's `验证命令` field, or the `测试命令` row from `## 构建与验证环境` for build-only Tasks.
        Record the passing output as a `[验证 Verify]` entry in `Actual Result`, appending after the `[失败 Red]` entry — do not overwrite it.
     4. **Refactor (optional)** — If the passing implementation has obvious duplication or violates the established code pattern, refactor while keeping tests green.
   - **TDD degradation rule:** If a Task genuinely cannot have an automated test — pure documentation, a configuration file that cannot be exercised by any test runner in this repository (document why), or a build system change with no runnable gate — state the reason explicitly before proceeding, record it in `Actual Result` as "TDD degraded: <reason>", and substitute a reproducible manual verification step. Do not degrade silently or skip verification entirely. A code change that touches business logic is never eligible for degradation even if it is delivered via a config or data file.
   - **API 声明文件修改（条件触发 — Task-1）**：如果当前是 plan 中的第一个 Task（API 声明文件 Task-1）且 `API/SDK` = 是：
     - 读取 `spec.md` 的 `## API 规格定义`（`### 公共规格属性` + 逐 API 的 `#### API: <完整签名>` 子节，含各 API 的规格表、API 描述三要素+五要素、设备行为差异），作为修改声明文件的精确蓝图
     - 获取 API 声明仓库路径（spec 阶段过程信息不落盘）：若本会话已有 spec 阶段确认的 `interface_sdk-js` / `interface_sdk_c` 本地路径，直接使用；否则询问开发者提供（不一定是绝对路径，只要能定位到即可）
     - **切分支（必须）**：API 声明仓库通常被多个需求共享，必须在修改声明文件前切出专用分支，避免多个需求的改动互相覆盖、diff 混淆。分支名建议关联proposal ID，如 `feature/proposal-12345-arkui-focus`；询问开发者确认分支名或由开发者手动切好后告知分支名
     - **阅读仓库根目录的 `AGENTS.md`**：学习该仓库的 API 设计规范、命名约定、目录结构约定、声明文件格式要求等知识，作为修改声明文件的参照。AGENTS.md 中的内容与既有声明文件的实际格式共同构成格式参考，二者冲突时以 AGENTS.md 为准。若 AGENTS.md 不存在，退回仅参照既有声明文件格式（降级模式）；若未引用声明注释规范，参照既有声明文件的 注释风格
     - 阅读仓库中与变更最相关的既有声明文件（≤10 个），提取格式规范（版权头、注释结构、命名风格），作为修改声明文件的参照
     - 参照既有声明文件的格式规范，根据规格表在 API 仓库中修改或新增声明文件：
       - ArkTS 声明写入 API 声明仓库中对应的声明文件目录（参照仓库既有目录结构和命名约定）
       - C 声明写入 API 声明仓库中对应的声明文件目录（参照仓库既有目录结构和命名约定）
       - 声明文件须包含 Apache 2.0 版权声明头和完整声明注释（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）
     - **按需调用 oh-api-definition 质量检查（可选，不阻塞）**：
       - 若开发环境已提供 oh-api-definition，则对新修改的声明文件执行其格式、命名、注释和语法检查；发现问题时修复后重跑
       - 若工具不可用时在 Task `Actual Result` 记录未执行并继续，不要求安装，也不得因此阻塞 Task-1
    - **生成声明注释双语 diff（英文 + 中文）**：完成适用的质量检查后，基于同一修改前基线生成两份 diff，归档到 `codespec/changes/<repo-name>/<proposal-id>/evidence/` 目录下，作为变更证据：
      - **英文声明注释 diff**（文件名固定为 `task1-api-declaration-en.diff`）：声明文件的实际修改内容，声明注释（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）使用英文——这是提交到 API 声明仓库的版本
      - **中文声明注释 diff**（文件名固定为 `task1-api-declaration-zh.diff`）：签名、代码、版权头与标记（`@syscap`/`@since`/`@kit`/`@permission` 等）与英文版完全一致，仅将声明注释的描述正文改为中文；中文内容以 `spec.md` 逐 API 子节的 `**API 描述**`（三要素+五要素）为源头，与英文注释保持语义一致
      - **约束**：中文版仅作为归档证据，不写回 API 声明仓库、不替代英文声明文件。两份 diff 均不得改变任何签名、入参、返回值、错误码或标记
   - After each Task, update `execution-plan.md` 代码范围映射 with actual files, tests, and commit references.
   - Backfill the Task's `Actual Result` with final completion evidence, appending after any `[失败 Red]` and `[验证 Verify]` entries already recorded — do not overwrite them.
   - Mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
4. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ 已完成（Done） / ❌ 阻塞（Blocked） / ⚠️ 跳过（Skipped，附原因）
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
5. If implementation reveals missing ACs or changed scope, pause and update `spec.md` / `execution-plan.md` before continuing.
6. Keep changes within the Task file scope unless the user approves an execution-plan update.
7. When any `资源开销审视` dimension is `required` (`contracts/artifacts.yaml#resource_contract`), complete subsystem measurement/evidence Tasks and the business-repo `odk_resource_gate` (commonly under `evidence/resource/`).
8. After all Tasks are Done, **prompt the user about device verification** before starting the automatic handoff — this is a one-time final integration verification, separate from the per-Task `.so` pushes already done in sub-step b. Choose A or B if you want to verify the fully-integrated build end-to-end (e.g. all changed `.so` together, fresh daily base); choose C if per-Task verification was sufficient. Only applies when the confirmed build product is a physical board (not arm64_virt):
   ```
   所有 Task 已完成。是否需要最终设备集成验证？
   （此步骤与实现过程中的逐 Task .so 推送独立，用于验证完整集成构建）
   A) 获取今日 daily 版本并刷机到本地设备，然后推送本次变更涉及的 .so 并重启服务
   B) 仅推送本次变更涉及的 .so 并重启服务（设备已运行今日 daily）
   C) 跳过设备验证，直接进入 review

   （当前编译产品：<confirmed product>）
   ```
   Option A is only shown when `device_flash_skill` is non-empty in config AND the confirmed product is `rk3568`. If `device_flash_skill` is empty (the default) or the product is not rk3568, omit option A — present only B and C. This mirrors the same guard as per-Task sub-step b.
   - If the user chooses A: invoke `device_flash_skill` (only rk3568 supported), then push `.so` files and restart service as described in sub-step b.
   - If the user chooses B: skip flashing, push `.so` files and restart service as described in sub-step b.
   - If the user chooses C: skip device verification entirely.
   - If the confirmed product is `arm64_virt`, skip this prompt (qemu verification was done per-Task in sub-steps c/d).
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
