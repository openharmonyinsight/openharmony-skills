---
name: ohos-dev-hdc-reverse-ssh-setup
description: >
  Use this skill when an OpenHarmony development host needs to set up or verify a
  Linux-to-Windows reverse SSH tunnel so Linux can run HDC on a Windows host with a
  USB-connected device. Trigger for reverse SSH HDC setup, Windows USB HDC bridge,
  remote OpenHarmony device access, or preparation for device-side verification.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: hdc
  capability: reverse-ssh-setup
  version: 0.1.0
  status: trial
  tags:
    - hdc
    - reverse-ssh
    - windows
    - device-verification
  related-skills:
    - name: ohos-dev-hdc-command-usage
      min_version: "0.1.0"
      required: true
      probes:
        - "test -f {dir}/references/hdc-command-reference.md"
---

# Reverse SSH HDC Setup

Use `ohos-dev-hdc-command-usage` for HDC target states, device selection, service recovery, and remote-server security boundaries. This skill owns only the cross-platform transport and proof that Windows-side HDC is reachable through it.

```text
Linux host -> loopback reverse SSH -> Windows host -> USB HDC -> OpenHarmony device
```

Skip this skill when Linux already sees exactly one intended `Connected` target through local HDC.

## Required Inputs

Ask once for missing non-secret values:

```text
LINUX_USER=<linux login user>
LINUX_HOST=<linux IP or DNS reachable from Windows>
LINUX_SSH_PORT=<linux ssh port, usually 22>
WINDOWS_USER=<windows ssh login user>
WINDOWS_SSH_PORT=<windows sshd port, usually 22>
REVERSE_SSH_PORT=<linux loopback port forwarding to Windows sshd, usually 2222>
HDC_EXE=<Windows hdc.exe path or hdc when in PATH>
DEVICE_ID=<hdc connect-key; optional only after proving exactly one Connected target>
```

Never ask for or store SSH passwords. Let an interactive prompt or an SSH key handle authentication.

## Bundled Scripts

```text
${SKILL_BASE_DIR}/scripts/reverse_ssh_linux_setup.sh
${SKILL_BASE_DIR}/scripts/reverse_ssh_windows_setup.bat
```

The scripts are fail-closed:

- The Windows script validates `CHANGE_ME`, ports, and `HDC_EXE` before installing or changing services.
- The Linux script returns nonzero when sshd, its listener, or reverse-forwarding support is unavailable.
- A prerequisite check never claims the tunnel or HDC device is ready.

## Linux Prerequisites

Prefer the bundled script:

```bash
bash ${SKILL_BASE_DIR}/scripts/reverse_ssh_linux_setup.sh
```

Without root, it performs read-only checks and returns nonzero when administrator work is required. With root, it may install/start sshd, enable `AllowTcpForwarding`, and open only the Linux SSH ingress port when an active supported firewall is detected.

The reverse listener is explicitly bound to `127.0.0.1`, so do not enable `GatewayPorts` and do not expose the reverse port through the firewall.

After Windows starts the tunnel, verify the listener separately:

```bash
bash ${SKILL_BASE_DIR}/scripts/reverse_ssh_linux_setup.sh --verify-tunnel
```

## Windows Setup

Edit the configuration block before running the script as Administrator:

```bat
set LINUX_USER=<linux login user>
set LINUX_IP=<linux IP or DNS>
set LINUX_SSH_PORT=<linux ssh port>
set HDC_EXE=<hdc or full path to hdc.exe>
```

The script validates all inputs and HDC availability before installing OpenSSH or changing the sshd service. It does not add Windows HDC/SSH firewall rules because the forwarded target is Windows loopback.

The only reverse forward is Windows sshd:

```bat
ssh -N -T ^
  -o ConnectTimeout=<timeout_seconds> ^
  -o StrictHostKeyChecking=accept-new ^
  -o ServerAliveInterval=60 ^
  -o ServerAliveCountMax=3 ^
  -o ExitOnForwardFailure=yes ^
  -R 127.0.0.1:<REVERSE_SSH_PORT>:localhost:<WINDOWS_SSH_PORT> ^
  -p <LINUX_SSH_PORT> <LINUX_USER>@<LINUX_HOST>
```

Do not forward the HDC server port. HDC server forwarding is version-sensitive; invoke HDC through the verified Windows SSH session.

## Verify From Linux

Run these checks in order and stop at the first failure:

```bash
ss -tln | grep "127.0.0.1:<REVERSE_SSH_PORT>"
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost "hostname"
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' list targets -v; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

The bridge is ready only when:

- Linux has a listener on `127.0.0.1:<REVERSE_SSH_PORT>`.
- SSH through that listener reaches the intended Windows host.
- Windows-side `hdc list targets -v` proves the intended target is `Connected`, or exactly one intended target is Connected when `DEVICE_ID` is empty.

Treat `[Empty]`, `Unauthorized`, `Offline`, multiple targets, and a nonzero HDC exit as blockers. Do not install, send files, wake the device, or perform cleanup until target selection succeeds.

## Device Readiness

Use target-scoped, fail-fast commands. Check every native HDC exit code:

```bash
ssh -p <REVERSE_SSH_PORT> <WINDOWS_USER>@localhost \
  "powershell -NoProfile -Command \"& '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'power-shell wakeup'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'power-shell setmode 602'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }; & '<HDC_EXE>' <HDC_TARGET_ARGS> shell 'uinput -T -m 360 1100 360 200 300'; if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }\""
```

## Troubleshooting

- Reverse SSH exits immediately: inspect `ExitOnForwardFailure`, Linux SSH reachability, `AllowTcpForwarding`, authentication, and an occupied reverse port.
- Linux reaches Windows but HDC fails: confirm the Windows `HDC_EXE`, HDC service state, USB driver, device authorization, and SDK/device compatibility.
- A target is unhealthy: use `ohos-dev-hdc-command-usage` to diagnose before retrying or mutating the device.
- The device is locked or screenshots are black: leave transport setup and use the domain verification skill to capture display/window blockers.

## Interruption Recovery

Stop all device mutation when the tunnel disappears or HDC no longer proves the intended `Connected` target. Preserve the failing command, SSH exit code, `hdc list targets -v`, and `hdc checkserver` output before restarting services, reconnecting, or rebooting.

Recover in this order:

| Observation | Checks before retry |
|---|---|
| `127.0.0.1:<REVERSE_SSH_PORT>` listener disappeared | Confirm `reverse_ssh_windows_setup.bat` is still running. Recheck `LINUX_USER`, `LINUX_IP`, `LINUX_SSH_PORT`, `WIN_SSH_PORT`, and `REVERSE_SSH_PORT`; then check Linux `sshd`, `AllowTcpForwarding`, `authorized_keys`, network reachability, and firewall policy. |
| Listener exists but Windows SSH fails | Verify the reverse port reaches the intended Windows `sshd`, the Windows service is running, the login user/key is correct, and the configured Windows SSH port has not changed. |
| Windows SSH works but HDC returns `[Empty]`, `Unauthorized`, or `Offline` | Verify `HDC_EXE` and the HDC service first. Then check device power and complete boot, USB debugging, a data-capable cable, a direct USB port, the Windows HDC driver/interface, and the device trust prompt. |
| USB enumeration is healthy but the daemon or version fails | Confirm the device was flashed with the intended board/product/variant image, the image contains and starts the HDC daemon, and the host SDK/toolchains are compatible with that image. |

Do not present reflashing as an automatic recovery step. Capture the current image/build identity and HDC evidence first, explain why an image or daemon mismatch is suspected, and obtain explicit user approval before any reflash.

## Never Do

- Never store passwords, private keys, personal hostnames, or prior-session addresses in the skill or report.
- Never bind a reverse listener outside loopback without explicit user approval and a documented network risk.
- Never open HDC or reverse-forward ports in host firewalls for this loopback topology.
- Never claim readiness from SSH success alone; Windows-side HDC target proof is also required.
- Never run a mutating HDC command without a target unless inventory proves exactly one intended Connected device.
- Never continue a PowerShell HDC sequence after a nonzero `$LASTEXITCODE`.
- Never reflash a device as part of automatic interruption recovery; preserve evidence and obtain explicit user approval first.

## Report

Include the loopback reverse port, Linux prerequisite result, Windows SSH result, `hdc list targets -v` summary, the exact failing command/action, and which recovery layer blocked: script configuration/runtime, SSH transport, HDC service/target, USB hardware, or device image. Do not include secrets.
