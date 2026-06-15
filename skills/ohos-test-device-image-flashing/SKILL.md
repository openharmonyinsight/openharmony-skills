---
name: ohos-test-device-image-flashing
description: Use when the user wants to download OpenHarmony daily build images or flash them to a real device (DAYU200/RK3568 or others). Triggers on daily build, DAYU200, RK3568, flashing, burning, hdc reboot, upgrading firmware.
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: device
  capability: image-flashing
  version: 0.2.0
  status: draft
---

# Flash OpenHarmony Device with Daily Build

Download daily build and flash via hdc updater mode. Scripts are generic — not hardcoded to any specific repo or device.

## Scripts

| Script | Purpose |
|--------|---------|
| `download_daily.py` | Query DCP API, download + extract device image |
| `flash_device.py` | Parse `parameter.txt` for partitions, flash via hdc updater mode |

Use the actual installed skill directory when running the helper scripts.

## Required Workflow

Follow these steps in order. Do not skip connectivity checks.

### Step 1: Verify Device Connectivity

Before any download or flash operation, confirm the device is reachable.

**Direct USB:**
```bash
hdc list targets
# Must show at least one device serial. If empty, check USB cable and hdc server.
```

**Via SSH tunnel:**
```bash
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "echo connected && hdc list targets"
# Both SSH and hdc must succeed. If SSH fails, confirm port and that SSH service is running.
```

Record the current firmware version for post-flash comparison:
```bash
hdc shell param get const.product.software.version
```

### Step 2: Download Image

```bash
SKILL_DIR=<installed-skill-dir>
python3 "$SKILL_DIR/download_daily.py" --component dayu200
```

After download completes, the script verifies archive integrity. Check the output for errors before proceeding.

### Step 3: Flash Device

**Pre-flash checklist:**
- Device is reachable (Step 1 passed)
- Image downloaded and extracted (Step 2 passed, `system.img` exists in output dir)
- User has explicitly approved the destructive flash operation

Only pass `--yes` after the user has explicitly approved destructive device flashing. Otherwise let
`flash_device.py` prompt for `FLASH`.

```bash
python3 "$SKILL_DIR/flash_device.py" --img-dir daily_build --yes
```

**WARNING: Do not interrupt the flash process.** If hdc disconnects or power is lost during dd writes, the device may become unbootable. See Recovery section below.

### Step 4: Verify Success

Wait ~60 seconds after reboot, then:
```bash
hdc shell param get const.product.software.version
```

Compare with the version recorded in Step 1. If the version changed to the expected build, flash succeeded.

If the device does not appear in `hdc list targets` after 120 seconds, see Recovery below.

### Step 5: Push Custom Libraries (Optional)

After flashing the base image, push locally-compiled libraries:

```bash
hdc shell mount -o rw,remount /
for lib in lib1.z.so lib2.z.so; do
    hdc file send $lib /system/lib/$lib
done
hdc shell reboot
```

For SSH tunnel scenarios, upload via scp first, then send to device:
```bash
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc shell mount -o rw,remount /"
for lib in lib1.z.so lib2.z.so; do
    scp -P $SSH_PORT $lib $SSH_USER@$SSH_HOST:push_tmp/$lib
    ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc file send push_tmp/$lib /system/lib/$lib"
done
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc shell reboot"
```

## SSH Tunnel Usage

The scripts run on the target machine that has USB to the board. Upload via SSH then execute remotely.

```bash
SKILL_DIR=<installed-skill-dir>
SSH_PORT=<ssh-port>
SSH_USER=<ssh-user>
SSH_HOST=<ssh-host>

# Upload scripts
scp -P $SSH_PORT "$SKILL_DIR/download_daily.py" $SSH_USER@$SSH_HOST:download_daily.py
scp -P $SSH_PORT "$SKILL_DIR/flash_device.py" $SSH_USER@$SSH_HOST:flash_device.py

# Download on remote
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "python download_daily.py --component dayu200"

# Flash from remote
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "python flash_device.py --yes"
```

**WARNING: SSH disconnect during flash is dangerous.** If the SSH session drops while `dd` is writing a partition, the device may be left in a partially-written state. Mitigations:
- Use `nohup` or `tmux`/`screen` on the remote machine to keep the process alive if SSH drops.
- Ensure the remote machine has a stable power supply.
- If SSH drops mid-flash, do NOT power cycle the device. Reconnect SSH and check if the process is still running (`ps aux | grep flash_device`).

## Device Recovery

If a flash fails (power loss, hdc disconnect, corrupted image), the device may not boot normally.

### DAYU200 / RK3568 Recovery

1. **Try updater mode**: Hold the device's Vol+/recovery button while powering on. The device should enter updater/recovery mode. Then retry flashing.

2. **If hdc is unreachable in updater mode**: Use the RKDevTool (Windows) or upgrade_tool (Linux) from Rockchip to flash via USB in maskrom/loader mode:
   - Power off the device
   - Hold the maskrom button while connecting USB
   - Use RKDevTool to write the full image

3. **If maskrom is not accessible**: The hardware recovery button location varies by board revision. Consult the DAYU200 hardware documentation.

### General Checklist

| Symptom | Recovery |
|---------|----------|
| Device reboots to updater loop | Re-flash all partitions from updater mode |
| hdc list targets shows nothing | Try maskrom mode or check USB cable |
| Boot hangs on logo | system.img may be corrupt — re-download and flash |
| Services crash after custom .so push | IDL interface mismatch — do a full flash instead of partial push |

## Key Design Decisions

**Partition table from parameter.txt:** `flash_device.py` parses `CMDLINE:mtdparts=...` from the image's `parameter.txt` to discover partitions. The built-in RK3568 fallback partition list is used only when `--allow-fallback-partitions` is explicitly passed after verifying the image layout.

**SSH port fallback:** Scripts default to port 2222. If connection fails, prompt the user for the correct port rather than failing silently.

**DCP API:** Response path is `data.builds.dataList[].component`. Auto-searches last 7 days if today's build is missing.

**Archive safety:** `download_daily.py` rejects archive entries that would extract outside the output directory. After download, the archive is verified by opening it before extraction.

**Destructive action confirmation:** `flash_device.py` requires interactive `FLASH` confirmation unless `--yes` is passed by an already-approved workflow.

**Command failure handling:** `flash_device.py` stops immediately when an `hdc` command exits non-zero.

**Userdata write path:** `userdata.img` is flashed last. The helper unmounts `/data`, uploads the
image to updater ramdisk temporary storage, writes it with `dd`, runs `sync` on the userdata block
device, and removes the temporary file. Do not write `userdata.img` with a direct `hdc file send`
to `/dev/block/by-name/userdata`.

## Why Updater Mode

Normal mode mounts system/vendor read-only — dd silently fails. Updater mode keeps partitions unmounted. Userdata is flashed last because it's used as temp storage during the process.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| DCP 返回空 | 日期格式 `YYYYMMDDHHMMSS`；脚本自动搜索 7 天 |
| dd 无输出 | 必须 updater 模式 |
| userdata 失败 | 先 umount /data |
| 推包后 mmi_service 不启动 | IDL 接口变了需全量刷机，不能只推部分 .so |
| SSH 连不上 | 先启动目标机器的 SSH 或端口转发服务，确认端口 |
| SSH 断开导致烧录中断 | 用 nohup/tmux 运行脚本；不要立即断电 |
| 下载的镜像包损坏 | 删除 tar.gz 重新下载；检查网络连通性 |
