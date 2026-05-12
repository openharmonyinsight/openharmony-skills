---
name: ohos-dev-hdc-command-usage
description: Use when HarmonyOS or OpenHarmony OS development uses hdc for remount, system partition writes, file send or recv, log collection, hilog, bugreport, crash or tombstone retrieval, device connection failures, USB or TCP targets, multiple connected devices, automation or CI scripts, shell commands, sandbox access, HAP/HSP/APP install or uninstall, port forwarding, hdc service logs, or errors such as Empty, Unauthorized, Offline, Connect failed, or Failed to communicate with daemon.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: hdc
  capability: command-usage
  version: 0.1.0
  status: draft
  tags:
    - hdc
    - harmonyos
    - device-debugging
    - command-line
---

# hdc Command Usage

Use this skill to choose safe, targeted `hdc` commands and diagnose common host-to-device failures. The goal is not to memorize every command; it is to avoid wrong-device operations, unstable TCP assumptions, unsupported options, and noisy trial-and-error.

Source baseline: Huawei HarmonyOS guide "hdc", version `V205`, displayed update time `2026-05-07 09:37:20`, URL: `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc`.

For a compact command list, read [references/hdc-command-reference.md](references/hdc-command-reference.md) only when the needed command pattern is not already in this file.

## First Decision

Before giving or running an `hdc` command, classify the task:

| Task type | First command | Next decision |
| --- | --- | --- |
| Device not found or unstable | `hdc list targets -v` | Match the symptom table below before changing modes |
| Multiple devices possible | `hdc list targets -v` | Require `-t <connect-key>` for install, uninstall, file, shell, reboot |
| Automation or CI | `hdc list targets -v` | Prove exactly one intended target or require an explicit `connect-key` |
| USB debugging | `hdc list targets -v` | Resolve `Unauthorized`, `Offline`, driver, or cable before retry loops |
| Wireless/TCP debugging | `hdc tconn <IP:port>` | Treat as test-environment only; confirm network and port first |
| Remote server debugging | `hdc -s <server-ip>:<port> <command>` | Confirm who owns the server and whether non-loopback exposure is acceptable |
| OS component push | `hdc list targets -v` then probe path | Decide temp push, remount/system write, permission fix, or reboot |
| Pull OS evidence | inspect remote path first | Estimate size, then `file recv`; avoid blind large-directory pulls |
| App install | inspect package set | Choose single-file install, multi-package folder install, or device-side `bm install` |
| File transfer | inspect source and destination | Prefer writable data/app paths; avoid system writes unless explicitly required |
| Logs | decide service log vs device log | Use `hdc -l` for hdc service, `hilog` for device logs |

`connect-key` is the unique device identifier. USB uses a serial-like identifier; TCP uses `IP:port`.

## Target Selection

If more than one target can exist, never run mutating commands without `-t`.

Safe pattern:

```bash
hdc list targets -v
hdc -t <connect-key> shell echo ok
hdc -t <connect-key> install <path-to.hap>
```

High-risk commands without `-t`: `install`, `uninstall`, `file send`, `file recv`, `target boot`, `shell rm`, `shell param set`, and any command that changes app data or device state.

Do not parse transient hdc error text as stable automation logic. The Huawei guide notes command error text may be optimized later; automation should prefer stable system error codes where available.

## OS Development Fast Paths

For OS development, prefer these routes before application-install workflows:

| Goal | Route | Guardrails |
| --- | --- | --- |
| Push a temporary binary/config | `hdc -t <key> file send <local> /data/local/tmp/<name>` | Probe with `shell ls -l`; run from temp path if possible before replacing system files |
| Replace a system component | Confirm target, probe path, remount only if required, `file send`, then verify owner/mode and run `shell sync` | Do not remount from a generic permission error; confirm build/device supports it and user explicitly needs system write |
| Pull logs or crash evidence | `shell ls`/`du` first, then `file recv <remote> <local>` | Avoid blind pulls of broad directories; preserve remote directory names in local output |
| Capture runtime logs | Start focused `hilog`, reproduce, stop or save, then `file recv` if logs were persisted | Keep hdc service logs separate from device hilog |
| Diagnose target instability | `list targets -v`, `checkserver`, hdc service logs, then transport-specific triage | Capture evidence before rebooting, changing mode, or killing services |

After pushing OS artifacts:
- Verify remote file exists with expected size: `hdc -t <key> shell ls -l <path>`.
- Check execution or read permissions before running: `hdc -t <key> shell stat <path>`.
- Run `hdc -t <key> shell sync` after important system writes.
- Reboot only when the changed component or partition semantics require it; otherwise prefer restarting the affected service/process.

## Automation / CI Rules

Unattended `hdc` scripts must be stricter than manual debugging:
- Require an explicit `connect-key` input for mutating commands, or fail if `hdc list targets -v` does not show exactly one `Connected` target.
- Treat `Unauthorized`, `Offline`, `[Empty]`, and multiple targets as hard failures; do not wait indefinitely for a human trust prompt in CI.
- Run a harmless probe such as `hdc -t <connect-key> shell echo ok` before install, uninstall, file writes, reboot, or destructive shell commands.
- Capture hdc service context on infrastructure failures: `hdc checkserver`, `hdc list targets -v`, and when needed `hdc kill` followed by `hdc -l 5 start`.
- Use `hdc -l 6` only for USB/libusb investigations; it is high-volume and should not be the default CI log mode.
- Do not branch automation on exact hdc prose error strings; use target state, command exit status, and stable system/tool error codes where available.

## Connection Diagnosis

| Symptom | Likely causes | Action |
| --- | --- | --- |
| `[Empty]` from `list targets` | hdc not on PATH, debugging disabled, bad USB cable/port, missing driver, service stuck, SDK/device mismatch | Check `hdc -h`; enable USB/wireless debugging; use data cable/direct port; check HDC Device/Interface or `lsusb`; run `hdc kill -r`; update SDK/toolchains if device recently updated |
| `Unauthorized` | Device sees host but trust is not approved | Ask user to accept trust or permanent trust prompt on device; then rerun `hdc list targets -v` |
| `Offline` | Stale TCP target, disconnected USB, daemon restarted after mode change | Remove stale TCP with `hdc tconn <IP:port> -remove`; reconnect cable/network; rerun `hdc wait` or reconnect TCP |
| `Connect failed` from `tconn` | Wrong IP/port, not same network, wireless debugging off, unstable network | Confirm device-displayed `IP:port`; ping or otherwise verify network path; re-enable wireless debugging; retry only after network facts change |
| `Failed to communicate with daemon` | daemon/service mismatch, device daemon issue, hdc/SDK version mismatch, port conflict with another hdc variant | Restart hdc service; check no competing hdc/hdc_std service uses the same port; update SDK/toolchains; reconnect or reboot device if daemon stays broken |
| `ExecuteCommand need connect-key` | No target selected or device list empty | Run `hdc list targets -v`; if multiple targets exist, add `-t`; if empty, diagnose connection first |
| Local server connection failure with `-s` | Wrong server address/port, server not started with matching bind, firewall | On server, start foreground service with `hdc -s <server-ip>:8710 -m`; on client, use same IP/port |

Use `hdc kill -r` for abnormal hdc service state. Do not use it as a substitute for fixing cable, authorization, network, or version problems.

## Layered Triage

Use this order to avoid trying everything at once:

1. Host tool: `hdc -h`, `hdc -v`, `hdc checkserver`; if hdc and hdc_std or multiple SDKs may coexist, confirm which binary is on PATH and whether port `8710` or `OHOS_HDC_SERVER_PORT` conflicts.
2. Target inventory: `hdc list targets -v`; classify as `[Empty]`, `Unauthorized`, `Offline`, stale TCP, or multiple connected targets.
3. Transport branch: for USB, check cable, direct port, driver, and trust prompt; for TCP, check same network, current device-displayed `IP:port`, and wireless debugging state; for remote `-s`, check server bind address, firewall, and matching port.
4. Daemon/version branch: if transport exists but daemon communication fails, restart hdc service, reconnect target, then update SDK/toolchains if the device image is newer than the host tools.
5. Evidence capture: before rebooting devices or changing modes, capture `hdc list targets -v`, `hdc checkserver`, and relevant hdc service logs.

## Connection Modes

USB:
- Prefer USB for stable development and destructive operations.
- Use a data-capable cable and a direct host USB port.
- If Windows shows a warning on `HDC Device`, reinstall or switch the USB driver before debugging hdc commands.

TCP:
- Use mainly in test environments.
- Prefer device UI wireless debugging. `tmode port [port]` restarts the device daemon; established connections must reconnect.
- Close with device UI, network disconnect, `hdc tmode port close`, or remove a specific connection with `hdc tconn <IP:port> -remove`.

Remote server via `-s`:
- `-s` is per command and overrides `OHOS_HDC_SERVER_PORT` for that command.
- Binding hdc service to a non-loopback address exposes device-control capability. Call this out before recommending `0.0.0.0` or a LAN IP.

## Install Decision Tree

Choose the install path from the package shape, not from habit:

| Package shape | Prefer | Why |
| --- | --- | --- |
| One `.hap` on host | `hdc install <file.hap>` | Simplest host-side flow; overwrite is default per guide |
| One `.app` on host | `hdc install <file.app>` | Supported from API version 22 |
| Single HAP reinstall | `hdc install -r <file.hap>` | Explicit overwrite when communicating intent |
| HAP with application HSP dependency | `hdc install -s <hsp-path> <hap>` or folder-based install | HSP dependency must be present; each specified HSP directory should contain one HSP |
| Multiple HAP/HSP files | `hdc install -p <folder>` | Avoids installing only the entry HAP and missing shared modules |
| Files already pushed to device | `hdc shell bm install -p <remote-path>` | Use when host-side `hdc install` is not the actual package location |
| Debug package needing grants | `hdc install -g <package>` | Only for debug apps; supported from API version 24 |

When passing bm options through `hdc install`, quote flag/value pairs such as `"-w 180"` and `"-u 100"` to avoid argument parsing surprises.

For uninstall:
- Use `hdc uninstall <bundleName>` for normal uninstall.
- Add `-k` only when preserving app data is intentional.
- Add `-s` for shared-library/HSP uninstall scenarios.

If install fails with a missing dependent module, do not keep reinstalling the same HAP. Check whether required HSP files were built, signed, and included in the install folder or `-s` path.

## File Transfer Decisions

Choose the transfer pattern from the remote path:

| Scenario | Preferred pattern | Checks |
| --- | --- | --- |
| Temporary OS artifact | `hdc -t <key> file send <local> /data/local/tmp/<name>` | `shell ls -l`, `shell stat`, optional `chmod` only when execution is needed |
| System path replacement | Probe path, backup if feasible, remount only if required, `file send`, `shell sync` | Confirm target build supports write; verify owner/mode after push |
| App sandbox data | `hdc -t <key> file send -b <bundleName> <local> <sandbox-path>` | App must be installed, started, debuggable, and hdc version compatible |
| Pull crash/log evidence | `shell ls` or `du`, then `hdc -t <key> file recv <remote> <local>` | Avoid pulling broad trees without size check |
| Media files | Use `/mnt/data/<uid>/media_fuse/Photo/` carefully | API version 21 partial-operation behavior; directory creation may fail |

Baseline commands:

```bash
hdc file send <local> /data/local/tmp/<name>
hdc file recv /data/log/hilog <local_path>
hdc file send -b <bundleName> <local> <sandbox-relative-path>
```

Decision rules:
- Use `/data/local/tmp` or app-specific paths for temporary files.
- Use `-b <bundleName>` only for an installed, started, debuggable app and a compatible hdc version.
- Use `-a` when timestamps matter; use `-sync` for mtime-based incremental transfer.
- For media library paths under `/mnt/data/<uid>/media_fuse/Photo/`, remember API version 21 behavior and partial-operation limits; do not assume directory creation works.
- If a write fails with read-only or permission errors, first switch to a writable target or verify the path; consider remount only for explicit OS component replacement.

## Dangerous Shell And File Operations

For `shell rm`, `param set`, writes under system paths, reboot, remount, root-like flows, or broad file operations:
- Require explicit target selection with `-t <connect-key>`.
- Prefer reversible probes first: `pwd`, `ls`, `stat`, `id`, or writing a disposable file under `/data/local/tmp`.
- Prefer safer locations before privilege escalation: `/data/local/tmp`, app sandbox via `-b <bundleName>`, or documented log/media paths.
- Treat permission or read-only errors as path/permission facts, not automatic permission to remount system partitions.
- Before deleting or overwriting, verify the resolved path and scope with `ls` or `stat`; avoid glob-style destructive commands in examples.
- Only suggest remount/root/system writes when the user explicitly needs system-partition modification and the device/build supports it.

When remount/system write is truly required:
1. Confirm target: `hdc list targets -v` and use `-t <connect-key>`.
2. Probe current state: `shell id`, `shell mount`, `shell ls -l <target>`, `shell stat <target>`.
3. Preserve rollback when feasible: pull or copy the original file before replacement.
4. Push the new file, then verify size, mode, owner, and ability to read/execute.
5. Run `shell sync`; restart only the affected service when possible, reboot only when required.

## Logs

Pick the log source. OS development usually needs both device-side logs and pullable evidence files:

| Need | Command |
| --- | --- |
| Live device runtime logs | `hdc -t <key> hilog` |
| Persisted hilog flow | `hdc -t <key> shell hilog -w start`, reproduce, `hdc -t <key> shell hilog -w stop`, then `hdc -t <key> file recv /data/log/hilog <local_path>` |
| Crash/tombstone/log directory pull | `hdc -t <key> shell ls <remote>`, optionally `du`, then `hdc -t <key> file recv <remote> <local_path>` |
| hdc client/server behavior | `hdc -l <0-6> <command>` |
| hdc server log collection | `hdc kill`, then `hdc -l 5 start` |
| USB/libusb detail | `hdc -l 6 ...` only when needed; it is high-volume |
| System snapshot | `hdc bugreport [FILE]` |

Server log locations: Windows `%temp%\`, Linux `/tmp/`, macOS `$TMPDIR/`.

Log capture rules:
- Start log capture before reproducing; stop or snapshot after reproducing.
- Keep output directories per device and timestamp when multiple targets are involved.
- For broad evidence directories, check size first to avoid long or accidental pulls.
- Use `bugreport` when the question needs system state, not just live log lines.
- Use hdc service logs only for host/transport/debug-bridge issues; they do not replace device hilog.

## Port Forwarding

Use `fport` when the host should listen and forward to the device. Use `rport` when the device should listen and forward to the host.

```bash
hdc fport tcp:<host-port> tcp:<device-port>
hdc rport tcp:<device-port> tcp:<host-port>
hdc fport ls
hdc fport rm tcp:<from> tcp:<to>
```

If local listen fails, assume port conflict before assuming hdc is broken. From API version 20, `-e` can control the local listen IP for TCP forwarding, but non-loopback listen addresses are a security decision, not a convenience default.

## Environment Variables

Common hdc environment variables:
- `OHOS_HDC_SERVER_PORT`: server listen port, default `8710`, valid range `1-65535`.
- `OHOS_HDC_LOG_LEVEL`: server log level, default `3`.
- `OHOS_HDC_HEARTBEAT`: set `1` to disable heartbeat; other values keep it enabled.
- `OHOS_HDC_CMD_RECORD`: set `1` to record hdc commands only, supported from API version 20.
- `OHOS_HDC_ENCRYPT_CHANNEL`: set `1` to enable TCP channel encryption, supported from API version 20.

After changing environment variables, restart the terminal or software that uses HarmonyOS SDK, and restart hdc service if needed.

## Never

NEVER run mutating commands without `-t` when multiple or stale targets may exist. Installing, uninstalling, rebooting, or deleting files on the wrong device is worse than a command failure.

NEVER recommend `tmode usb` as an active switching command. The guide says it is deprecated from hdc 3.1.0e; use the device UI USB debugging switch.

NEVER expose an hdc server or forwarded port on a non-loopback address without naming the risk. It can expose device-control or debug surfaces to the network.

NEVER let CI wait forever for device authorization or connection recovery. Fail with target state and collected hdc diagnostics.

NEVER convert a permission/read-only failure directly into remount/root advice. First verify the path, use a writable destination, or ask whether system-partition modification is actually required.

NEVER push over an OS component without target confirmation, path probe, rollback plan when feasible, and post-push verification.

NEVER pull broad log or crash directories without first checking existence and approximate size.

NEVER recommend `file send -z` or `file recv -z`; the guide says LZ4 transfer is not open.

NEVER fix install dependency errors by repeatedly reinstalling only the entry HAP. Check HSP/shared modules and install package shape.
