---
name: ohos-dev-hdc-command-usage
description: Use when using HarmonyOS hdc commands for device connection, shell execution, file transfer, app install or uninstall, logs, port forwarding, service management, or troubleshooting missing devices.
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

Use this skill when an OpenHarmony or HarmonyOS task needs `hdc` as the host-to-device command line bridge. Treat `hdc` as a device interaction tool for connection management, shell commands, data transfer, logs, app installation, port forwarding, and basic diagnostics.

Source baseline: Huawei HarmonyOS guide "hdc", version `V205`, displayed update time `2026-05-07 09:37:20`, URL: `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc`.

## First Checks

Before giving or running commands, identify:
- Connection mode: USB, wireless TCP, or remote server via `-s`.
- Target count: if more than one device may be connected, use `hdc list targets -v` and add `-t <connect-key>`.
- Package type: `.hap`, `.hsp`, or `.app`; `hdc install` supports HAP and application HSP, and supports APP packages from API version 22.
- Privilege need: do not assume system partitions are writable; prefer app/data paths unless the task explicitly requires remount or elevated access.

`connect-key` is the unique device identifier. USB uses a serial-like identifier; TCP uses `IP:port`.

## Command Map

| Task | Command pattern |
| --- | --- |
| Check tool/help/version | `hdc -h [verbose]`, `hdc -v`, `hdc version`, `hdc checkserver` |
| List devices | `hdc list targets [-v]` |
| Wait for device | `hdc wait`, `hdc -t <connect-key> wait` |
| Select one device | `hdc -t <connect-key> <command>` |
| Run shell command | `hdc shell <command>`, or `hdc shell` for interactive mode |
| Run in debuggable app sandbox | `hdc shell -b <bundleName> <command>` |
| Connect over TCP | `hdc tconn <IP:port>`, remove with `hdc tconn <IP:port> -remove` |
| Open/close device network channel | `hdc tmode port [port]`, `hdc tmode port close` |
| Send file to device | `hdc file send [options] <local> <remote>` |
| Receive file from device | `hdc file recv [options] <remote> <local>` |
| Install app file | `hdc install [options] <src>` |
| Uninstall bundle | `hdc uninstall [options] <bundleName>` |
| Print device logs | `hdc hilog`, `hdc shell hilog -w start`, `hdc shell hilog -w stop` |
| Port forwarding | `hdc fport ls`, `hdc fport <localnode> <remotenode>`, `hdc rport <remotenode> <localnode>`, `hdc fport rm <taskstr>` |
| Restart hdc service | `hdc start -r`, `hdc kill -r` |
| Export system info | `hdc bugreport [FILE]` |

## Connection Workflow

For USB:
1. Ensure the device has USB debugging enabled in developer options.
2. Use a data-capable cable and a direct USB port.
3. Run `hdc list targets -v`.
4. If the device is `Unauthorized`, ask the user to trust the host on the device.

For TCP:
1. Use TCP debugging mainly in test environments.
2. Ensure host and device are on the same network.
3. Enable wireless debugging on the device and record `IP:port`.
4. Run `hdc tconn <IP:port>` and expect `Connect OK`.
5. Confirm with `hdc list targets`.

For remote host/server debugging:
1. Start the server-side hdc service with an explicit address, for example `hdc -s <server-ip>:8710 -m`.
2. From the client, run `hdc -s <server-ip>:8710 <command>`.
3. Remember that an explicit `-s` ignores `OHOS_HDC_SERVER_PORT` for that command.
4. Be careful when binding to non-loopback addresses; treat exposed hdc service ports as sensitive.

## File Transfer Rules

Use:
- `hdc file send <local> <remote>` to push files to the device.
- `hdc file recv <remote> <local>` to pull files from the device.
- `-a` to preserve file timestamps.
- `-sync` to transfer only files with updated mtime.
- `-b <bundleName>` for a debuggable app sandbox; this requires a compatible hdc version and an installed debuggable app.

Do not recommend `-z`; the Huawei guide marks LZ4 transfer as not open for use.

For media library paths, API version 21 and later support partial operations under `/mnt/data/<uid>/media_fuse/Photo/`; do not assume arbitrary directory creation is supported there.

## App Install Rules

Use host-side simplified install first:

```bash
hdc install <path-to.hap>
hdc install -r <path-to.hap>
hdc install <path-to.app>
```

Important options:
- `-r` is overwrite install behavior; the guide notes overwrite is the default when omitted.
- `-s` is required when installing an application HSP; each specified directory should contain only one HSP.
- `-p` can point to a folder containing multiple HAP/HSP files; from API version 22, it can also point to an APP or a folder with a single APP.
- `"-w 180"` and `"-u 100"` style options should be quoted when passing bm options that combine a flag and value.
- `-g` applies only to debug apps and is supported from API version 24.

For uninstall:

```bash
hdc uninstall <bundleName>
hdc uninstall -k <bundleName>
hdc uninstall -s <bundleName>
```

Use `-k` when preserving app data matters. Use `-s` when uninstalling an HSP/shared library scenario requires it.

## Logs and Diagnostics

For hdc service issues:
- Try `hdc kill -r` when hdc behaves abnormally.
- Use `hdc -l <0-6> <command>` for current-process logging.
- Use `hdc kill` then `hdc -l 5 start` to collect server logs.
- Use `hdc -l 6` only when USB/libusb detail is needed; it is high-volume.

Server log locations:
- Windows: `%temp%\`
- Linux: `/tmp/`
- macOS: `$TMPDIR/`

For device logs:

```bash
hdc hilog
hdc shell hilog -w start
hdc shell hilog -w stop
hdc shell ls /data/log/hilog
hdc file recv /data/log/hilog <local_path>
```

For system snapshots, use `hdc bugreport [FILE]`.

## Troubleshooting

If `hdc list targets` returns `[Empty]`:
- Check that `hdc -h` works and the SDK `toolchains` path is available.
- Check USB debugging or wireless debugging is enabled.
- On USB, check cable, direct USB port, and host driver visibility (`HDC Device` or `HDC Interface` on Windows; `lsusb` or system USB info on Unix-like systems).
- If the device is `Unauthorized`, approve the device trust prompt.
- Restart the service with `hdc kill -r` or `hdc start -r`.
- If hdc or SDK version does not match a newly updated device, update SDK/toolchains.

If commands must target a specific device:
- Always include `-t <connect-key>` before the command.
- Never parse transient hdc error text as stable automation logic; use standard error codes where an automated program needs stable behavior.

If a file write fails:
- Prefer a writable destination such as app-specific paths or `/data/local/tmp`.
- Only remount or write system paths when the device/build supports it and the task explicitly requires it.

## Environment Variables

Common hdc environment variables:
- `OHOS_HDC_SERVER_PORT`: server listen port, default `8710`, valid range `1-65535`.
- `OHOS_HDC_LOG_LEVEL`: server log level, default `3`.
- `OHOS_HDC_HEARTBEAT`: set `1` to disable heartbeat; other values keep it enabled.
- `OHOS_HDC_CMD_RECORD`: set `1` to record hdc commands only, supported from API version 20.
- `OHOS_HDC_ENCRYPT_CHANNEL`: set `1` to enable TCP channel encryption, supported from API version 20.

After changing environment variables, restart the terminal or software that uses HarmonyOS SDK, and restart hdc service if needed.

## Never

NEVER use `tmode usb` as an active switching recommendation; the guide says it is deprecated from hdc 3.1.0e and the device UI should control USB debugging.

NEVER expose a non-loopback hdc server bind without calling out the security risk.

NEVER assume one connected target when automation or CI may have multiple devices; check and use `-t`.

NEVER use `-z` file transfer compression; the guide says it is not open.
