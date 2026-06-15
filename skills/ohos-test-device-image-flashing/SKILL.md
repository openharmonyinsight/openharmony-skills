---
name: ohos-test-device-image-flashing
description: Use when the user wants to download OpenHarmony daily build images or flash them to a real device (DAYU200/RK3568 or others). Triggers on daily build, DAYU200, RK3568, flashing, burning, hdc reboot, upgrading firmware.
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: device
  capability: image-flashing
  version: 0.1.0
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

## Usage

Only pass `--yes` after the user has explicitly approved destructive device flashing. Otherwise let
`flash_device.py` prompt for `FLASH`.

### Direct (on Windows with USB to board)

```bash
SKILL_DIR=<installed-skill-dir>/ohos-test-device-image-flashing

# Download
python3 "$SKILL_DIR/download_daily.py" --component dayu200

# Flash (partitions auto-parsed from parameter.txt)
python3 "$SKILL_DIR/flash_device.py" --img-dir daily_build --yes
```

### Via SSH tunnel

The scripts run on the Windows target that has USB to the board. Upload via SSH then execute remotely.

```bash
SKILL_DIR=<installed-skill-dir>/ohos-test-device-image-flashing
SSH_PORT=<ssh-port>
SSH_USER=<ssh-user>
SSH_HOST=<ssh-host>

# Test connection
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "echo connected" || {
    echo "SSH connection failed. Enter SSH port:"
    read SSH_PORT
}

# Upload scripts
scp -P $SSH_PORT "$SKILL_DIR/download_daily.py" $SSH_USER@$SSH_HOST:download_daily.py
scp -P $SSH_PORT "$SKILL_DIR/flash_device.py" $SSH_USER@$SSH_HOST:flash_device.py

# Download on Windows
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "python download_daily.py --component dayu200"

# Flash from Windows
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "python flash_device.py --yes"

# Verify (~60s after reboot)
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc shell param get const.product.software.version"
```

### Push custom .so after flash

```bash
# After flashing base image, push locally-compiled libraries
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc shell mount -o rw,remount /"
for lib in lib1.z.so lib2.z.so; do
    scp -P $SSH_PORT $lib $SSH_USER@$SSH_HOST:push_tmp/$lib
    ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc file send push_tmp/$lib /system/lib/$lib"
done
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "hdc shell reboot"
```

## Key Design Decisions

**Partition table from parameter.txt:** `flash_device.py` parses `CMDLINE:mtdparts=...` from the image's `parameter.txt` to discover partitions. The built-in RK3568 fallback partition list is used only when `--allow-fallback-partitions` is explicitly passed after verifying the image layout.

**SSH port fallback:** Scripts default to port 2222. If connection fails, prompt the user for the correct port rather than failing silently.

**DCP API:** Response path is `data.builds.dataList[].component`. Auto-searches last 7 days if today's build is missing.

**Archive safety:** `download_daily.py` rejects archive entries that would extract outside the output directory.

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
