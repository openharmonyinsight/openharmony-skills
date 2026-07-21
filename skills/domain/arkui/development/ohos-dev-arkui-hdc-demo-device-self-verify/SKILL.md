---
name: ohos-dev-arkui-hdc-demo-device-self-verify
description: >
  Use this skill when an OpenHarmony ArkUI or ACE Engine task needs device-side end-to-end
  self-verification through HDC, including pushing a demo HAP or native library to a
  USB-connected device, installing or replacing artifacts, launching the demo, collecting
  screenshots, dumps, logs, and producing concise verification evidence. Trigger for E2E
  self-verification, device validation, HAP verification, native library replacement
  verification, or SDD end-to-end test evidence.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: hdc-demo-device-self-verify
  version: 0.1.0
  status: trial
  tags:
    - arkui
    - ace-engine
    - hdc
    - e2e-verification
    - self-verification
  related-skills:
    - name: ohos-dev-hdc-command-usage
      min_version: "0.1.0"
      required: true
      probes:
        - "test -f {dir}/references/hdc-command-reference.md"
    - name: ohos-dev-hdc-reverse-ssh-setup
      min_version: "0.1.0"
      required: false
---

# HDC Demo Device Self Verify

## Required HDC Foundation

Use `ohos-dev-hdc-command-usage` as the source of truth for target selection, connection diagnosis, package-shape installation, file transfer, system-partition writes, logging, and HDC service recovery. Install or index it before running this workflow:

```bash
bash ${SKILL_BASE_DIR}/scripts/install_related_skills.sh
```

If the dependency is already installed, the script only verifies its index entry. Do not duplicate or override its safety rules in this skill.

This skill adds the ArkUI-specific orchestration that the common HDC skill does not provide: Windows reverse-SSH delegation, ability launch, screen readiness, ArkUI/window/UI-tree evidence, ACE native-library load proof, and end-to-end pass/blocker reporting.

Use this skill after HDC access is available. If Linux reaches the device through a Windows USB host, first use `ohos-dev-hdc-reverse-ssh-setup` and verify that this works:

```text
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost
```

The goal is to perform device-side end-to-end self-verification from Linux by delegating HDC operations to the Windows host, then report concrete evidence instead of only command intent.

## Required Inputs

Before running commands, confirm or replace these values:

```text
REVERSE_SSH_PORT=<linux localhost reverse ssh port, usually 2222>
WINDOWS_USER=<windows ssh login user>
HDC_EXE=<Windows hdc.exe path or hdc if in PATH>
DEVICE_ID=<hdc connect-key; optional only after proving exactly one Connected target>
RUN_ID=<unique UTC timestamp plus random suffix for this verification>
WINDOWS_WORK_DIR=<unique Windows directory, for example C:\Users\<user>\Desktop\ohos_e2e_<RUN_ID>>
LINUX_REPO_ROOT=<OpenHarmony root on Linux>
LINUX_ARTIFACT=<local Linux file to deploy, for example demo.hap or lib*.z.so>
DEVICE_TMP_DIR=/data/local/tmp/ohos_e2e_<RUN_ID>
BUNDLE_NAME=<demo bundle name>
ABILITY_NAME=<entry ability name, usually EntryAbility>
MODULE_NAME=<optional module name for bm install if needed>
LIBRARY_NAME=<optional native library name, for example libace_compatible.z.so>
PROCESS_NAME=<optional process that should load the library>
DEVICE_DESTINATION=<optional verified device path for replacement>
SCREENSHOT_NAME=<short evidence file name>
```

If the task is component-specific, also confirm the exact verification action and expected visible result.

## Command Helpers

Set `<HDC_TARGET_ARGS>` to `-t '<DEVICE_ID>'` when `DEVICE_ID` is required, or to an empty argument list only after `hdc list targets -v` proves exactly one intended `Connected` target. Use one consistent HDC expression in every later command.

If `DEVICE_ID` is set:

```powershell
& '<HDC_EXE>' -t '<DEVICE_ID>' <hdc args>
```

If `DEVICE_ID` is empty:

```powershell
& '<HDC_EXE>' <hdc args>
```

Every native HDC invocation in a PowerShell sequence must be followed immediately by an exit-code check. Do not rely on the last command's exit status:

```powershell
& '<HDC_EXE>' <HDC_TARGET_ARGS> <hdc args>
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Create a new `RUN_ID` for every attempt. Before mutation, prove that `WINDOWS_WORK_DIR` and `DEVICE_TMP_DIR` do not already exist; if either exists, generate another ID rather than reusing or deleting an unknown directory. Only clean directories containing the current `RUN_ID`.

Before any install, file write, shell state change, cleanup, reboot, or system replacement, run `hdc list targets -v`. If the output does not prove exactly one intended `Connected` target, require `DEVICE_ID` and add `-t '<DEVICE_ID>'` to every mutating HDC command. Treat `Unauthorized`, `Offline`, `[Empty]`, and multiple targets as blockers according to `ohos-dev-hdc-command-usage`.

From Linux, run PowerShell through SSH:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"<powershell hdc command>\""
```

For files, first copy Linux artifacts to Windows:

```bash
scp -P <REVERSE_SSH_PORT> <LINUX_ARTIFACT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/'
```

Use Windows paths in HDC commands, for example:

```powershell
& '<HDC_EXE>' <HDC_TARGET_ARGS> file send '<WINDOWS_WORK_DIR>\demo.hap' '<DEVICE_TMP_DIR>/demo.hap'
```

## Preflight

Verify HDC and prepare the device:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' list targets -v; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Only after target selection succeeds, create fresh run directories. Fail if either path already exists:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"if (Test-Path '<WINDOWS_WORK_DIR>') { exit 17 }; New-Item -ItemType Directory -Path '<WINDOWS_WORK_DIR>' -ErrorAction Stop | Out-Null; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'test ! -e <DEVICE_TMP_DIR> && mkdir -p <DEVICE_TMP_DIR>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Use the command-helper form above to wake the device, set display mode, and perform the unlock gesture.

Capture a baseline screenshot:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"Remove-Item '<WINDOWS_WORK_DIR>\before.jpeg' -ErrorAction SilentlyContinue; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'rm -f <DEVICE_TMP_DIR>/before.jpeg && snapshot_display -f <DEVICE_TMP_DIR>/before.jpeg && test -s <DEVICE_TMP_DIR>/before.jpeg'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> file recv '<DEVICE_TMP_DIR>/before.jpeg' '<WINDOWS_WORK_DIR>\before.jpeg'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; if (-not (Test-Path '<WINDOWS_WORK_DIR>\before.jpeg')) { exit 18 }\""
scp -P <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/before.jpeg' ./before.jpeg
```

## Install Demo HAP

Choose the install path from the package shape using `ohos-dev-hdc-command-usage`. A single HAP can use the device-side flow below; HAP/HSP sets must use the dependency-aware folder or `-s` flow instead of repeatedly installing only the entry HAP.

```bash
scp -P <REVERSE_SSH_PORT> <LINUX_ARTIFACT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/demo.hap'
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> file send '<WINDOWS_WORK_DIR>\demo.hap' '<DEVICE_TMP_DIR>/demo.hap'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'test -s <DEVICE_TMP_DIR>/demo.hap && bm install -p <DEVICE_TMP_DIR>/demo.hap'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

If the install command requires a different package path or module option for the target device image, use the device's supported `bm install` syntax and record the exact command.

Verify the bundle:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'bm dump -n <BUNDLE_NAME> | head -n 80'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

## Push Native Libraries Or Other Files

For native libraries built on Linux, first identify both the local build output and the existing device path. Do not assume a destination only from the library name.

Find the local artifact:

```bash
find <LINUX_REPO_ROOT>/out -path '*arkui/ace_engine*' -name '<library_name>' -type f -print
find <LINUX_REPO_ROOT>/out -name '<library_name>' -type f -print
```

Find matching files already present on the device:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'find /system /vendor /chip_prod /data -name <library_name> 2>/dev/null'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

If the process is already running, use `/proc/<pid>/maps` as the strongest evidence for the real loaded path:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'pid=\$(pidof <process_name>); pid=\${pid%% *}; test -n \"\$pid\" && grep <library_name> /proc/\$pid/maps'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Before replacement, record the original hash, numeric mode, owner/group, and security context. If the image cannot report or restore required attributes for a system path, stop instead of guessing:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'set -e; test -f <device_destination>; stat -c %a:%u:%g <device_destination>; ls -lZ <device_destination>; sha256sum <device_destination>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Create a rollback copy before overwriting a system library. Prefer a same-filesystem backup such as `<device_destination>.bak.<RUN_ID>` plus a received copy under `WINDOWS_WORK_DIR`. Record the exact backup path and do not proceed if the backup or metadata capture fails.

Push the replacement only to the fresh device run directory first:

```bash
scp -P <REVERSE_SSH_PORT> <LINUX_ARTIFACT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/'
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> file send '<WINDOWS_WORK_DIR>\<artifact_name>' '<DEVICE_TMP_DIR>/<artifact_name>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'test -s <DEVICE_TMP_DIR>/<artifact_name> && sha256sum <DEVICE_TMP_DIR>/<artifact_name>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

On the device, copy the staged file to a sibling path on the destination filesystem, restore the recorded numeric owner/group and mode, and restore the original security context using a supported `chcon --reference`, explicit `chcon`, or `restorecon` flow. Verify every attribute before atomically renaming the sibling over the destination. If any step fails, restore the backup and report Blocked.

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'set -e; cp -p <device_destination> <device_destination>.bak.<RUN_ID>; cp <DEVICE_TMP_DIR>/<artifact_name> <device_destination>.new.<RUN_ID>; chown <ORIGINAL_UID>:<ORIGINAL_GID> <device_destination>.new.<RUN_ID>; chmod <ORIGINAL_MODE> <device_destination>.new.<RUN_ID>; <RESTORE_ORIGINAL_SECURITY_CONTEXT>; stat -c %a:%u:%g <device_destination>.new.<RUN_ID>; ls -lZ <device_destination>.new.<RUN_ID>; mv -f <device_destination>.new.<RUN_ID> <device_destination>; sync'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Common destinations:

```text
/system/lib64/platformsdk/<library>.z.so
/system/lib64/<library>.z.so
/data/local/tmp/ohos_e2e_<RUN_ID>/<file>
```

After replacement, compare metadata and restart the relevant process, app, or device as required:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'set -e; sync; stat -c %a:%u:%g <device_destination>; ls -lZ <device_destination>; sha256sum <device_destination>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Replacing system libraries may require remount/root-capable images and can require reboot or service restart. Do not claim validation passed until `/proc/<pid>/maps`, logs, or behavior show the running process used the intended library.

## Screen Readiness

Wake the device, keep the screen on, and unlock before launching or validating UI:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'power-shell wakeup'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'power-shell setmode 602'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'power-shell display -s 100'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'uinput -T -m 360 1180 360 120 800'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

If launch fails with a lock-screen error or the screenshot is black, capture state before retrying:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"Remove-Item '<WINDOWS_WORK_DIR>\lock_check.jpeg' -ErrorAction SilentlyContinue; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'power-shell dump -s'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'rm -f <DEVICE_TMP_DIR>/lock_check.jpeg && snapshot_display -f <DEVICE_TMP_DIR>/lock_check.jpeg && test -s <DEVICE_TMP_DIR>/lock_check.jpeg'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> file recv '<DEVICE_TMP_DIR>/lock_check.jpeg' '<WINDOWS_WORK_DIR>\lock_check.jpeg'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
scp -P <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/lock_check.jpeg' ./lock_check.jpeg
```

Treat a black screenshot with an awake display state as a device/display blocker. Manual unlock or device-side display recovery is needed before UI verification is meaningful.

## Launch Demo

Stop any stale instance, launch the ability, then check process/window state:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'aa force-stop <BUNDLE_NAME>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'aa start -a <ABILITY_NAME> -b <BUNDLE_NAME>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'pidof <BUNDLE_NAME>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'hidumper -s WindowManagerService | grep -i <BUNDLE_NAME> -C 2'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

If `aa start` reports the screen is locked, run wake/unlock again and capture a lock-state screenshot before retrying.

## Exercise The Feature

Use the smallest deterministic operation that proves the feature:

- tap or swipe with `uinput`
- send text with the device input mechanism used by the project
- call app, framework, or system `hidumper` commands relevant to the feature
- trigger app-specific UI actions
- inspect `hilog` for fixed tags and error summaries

Example tap and log collection:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'hilog -r'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'uinput -T -c 360 640'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; Start-Sleep -Seconds 2; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'hilog | tail -n 120'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Do not validate privacy-sensitive UI text unless the user explicitly asks and the text is part of a fixed demo.

## Dump Tree And Screenshot Evidence

Capture window and UI tree evidence around the expected result. Use the commands supported by the current image and report which one produced evidence.

Window and focus state:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'hidumper -s WindowManagerService | head -n 200'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'hidumper -s AbilityManagerService | grep -i <BUNDLE_NAME> -C 5'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Try a layout/tree dump after deleting any old output. A failed dump or missing fresh file is a blocker for layout evidence; never receive a pre-existing `/data/local/tmp/layout.json`:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"Remove-Item '<WINDOWS_WORK_DIR>\layout.json' -ErrorAction SilentlyContinue; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'rm -f <DEVICE_TMP_DIR>/layout.json && uitest dumpLayout <DEVICE_TMP_DIR>/layout.json && test -s <DEVICE_TMP_DIR>/layout.json'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> file recv '<DEVICE_TMP_DIR>/layout.json' '<WINDOWS_WORK_DIR>\layout.json'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; if (-not (Test-Path '<WINDOWS_WORK_DIR>\layout.json')) { exit 18 }\""
scp -P <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/layout.json' ./evidence/<RUN_ID>/layout.json
```

If `uitest dumpLayout` is unavailable, use the component/framework dump command for the target subsystem and save its output with the final report.

Capture after-action evidence:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"Remove-Item '<WINDOWS_WORK_DIR>\<SCREENSHOT_NAME>.jpeg' -ErrorAction SilentlyContinue; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'rm -f <DEVICE_TMP_DIR>/<SCREENSHOT_NAME>.jpeg && snapshot_display -f <DEVICE_TMP_DIR>/<SCREENSHOT_NAME>.jpeg && test -s <DEVICE_TMP_DIR>/<SCREENSHOT_NAME>.jpeg'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> file recv '<DEVICE_TMP_DIR>/<SCREENSHOT_NAME>.jpeg' '<WINDOWS_WORK_DIR>\<SCREENSHOT_NAME>.jpeg'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; if (-not (Test-Path '<WINDOWS_WORK_DIR>\<SCREENSHOT_NAME>.jpeg')) { exit 18 }\""
scp -P <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost:'<WINDOWS_WORK_DIR>/<SCREENSHOT_NAME>.jpeg' ./evidence/<RUN_ID>/<SCREENSHOT_NAME>.jpeg
```

If visual validation matters, open the local screenshot and inspect it before reporting success.

## Cleanup

Only clean files created by this verification:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'case <DEVICE_TMP_DIR> in /data/local/tmp/ohos_e2e_*) rm -rf <DEVICE_TMP_DIR> ;; *) exit 19 ;; esac'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'aa force-stop <BUNDLE_NAME>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

Do not uninstall the demo unless the user requested cleanup or the test requires a fresh install:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'bm uninstall -n <BUNDLE_NAME>'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

## Pass Criteria

Report pass only when all required evidence exists:

- `hdc list targets -v` proved the intended connected target and all mutating commands used `-t` when target uniqueness was not guaranteed.
- artifact copy to Windows and HDC file send succeeded.
- demo install or file replacement command returned success.
- `aa start` launched the expected bundle/ability.
- feature action was executed.
- dump tree, screenshot, or log evidence confirms the expected result.

When blocked, report the exact failing command, exit/output summary, and the next manual action needed.

## Interrupted Run Recovery

If reverse SSH disconnects, the HDC target disappears, or HDC changes to `[Empty]`, `Unauthorized`, or `Offline` at any point, stop the current sequence immediately. Do not resume install, file replacement, wake/unlock, launch, evidence collection, cleanup, reboot, or another device mutation until the same intended target is proven `Connected` again.

Preserve the current run's evidence and recover layer by layer:

1. Recheck the Linux loopback listener. If it is missing, confirm `reverse_ssh_windows_setup.bat` is still running and that its Linux user/address and SSH/reverse ports match the Linux validation script.
2. Recheck SSH through the reverse port. Verify Linux `sshd`, `AllowTcpForwarding`, `authorized_keys`, network/firewall reachability, Windows `sshd`, and the intended Windows login.
3. Through the recovered Windows SSH session, run `hdc checkserver` and `hdc list targets -v`. Re-select the same explicit connect-key when multiple targets are present; never assume the remaining target is the original device.
4. For `[Empty]`, `Unauthorized`, or `Offline`, ask the user to check device power and complete boot, USB debugging, the data-capable USB cable, a direct USB port, the Windows HDC driver/interface, and the device trust prompt.
5. If Windows enumerates the USB device but HDC daemon or version checks fail, verify that the device has the intended board/product/variant image, that the image contains and starts the HDC daemon, and that the Windows SDK/toolchains are compatible with the image.
6. Create a new `RUN_ID` after recovery. Do not reuse partially written Windows/device directories or stale screenshots, layout dumps, HAPs, libraries, or logs from the interrupted attempt.

Before any reflash, save the failed command, SSH/HDC output, available device/image build identity, and relevant logs. Explain the suspected image/daemon mismatch and obtain explicit user approval; reflashing is never an automatic recovery action.

## Never Do

- Never declare pass from successful file transfer alone; require launch/runtime evidence and visible, dump, map, or log confirmation.
- Never continue after `[Empty]`, `Unauthorized`, `Offline`, or ambiguous multiple-target output; follow `ohos-dev-hdc-command-usage` and require an explicit connect-key where needed.
- Never replace a native library at a guessed device path. Verify the existing path with device `find`, package layout, or `/proc/<pid>/maps` first.
- Never overwrite a native library without preserving and comparing hash, mode, owner/group, and security context; never replace those attributes with a fixed `chmod 755`.
- Never reuse a Windows/device evidence directory from another run or accept a screenshot/layout file that was not freshly generated under the current `RUN_ID`.
- Never treat a black screenshot, locked screen, or unavailable layout dump as visual proof. Capture the blocker state and report manual recovery needed.
- Never validate privacy-sensitive UI text unless the user explicitly asks and the text is part of a fixed demo.
- Never resume a partially completed run after transport or target loss; revalidate every layer and start with a fresh `RUN_ID`.
- Never reflash automatically; preserve evidence and obtain explicit user approval first.
