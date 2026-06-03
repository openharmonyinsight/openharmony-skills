---
name: flash_daily_dayu200
description: Use when the user wants to download OpenHarmony daily build images for DAYU200/RK3568, flash them to a real device, or update the OpenHarmony source tree. Triggers on mentions of daily build, DY200, DAYU200, RK3568, flashing, burning, hdc reboot bootloader, or upgrading firmware.
---

# Flash DAYU200 (RK3568) with Daily Build

## Overview

End-to-end workflow: download today's OpenHarmony master daily build for DAYU200 (RK3568), flash it via hdc in updater mode, and update the local source tree.

## Prerequisites

- `hdc` (OpenHarmony Device Connector) on the machine with USB connection to DAYU200
- SSH access to that machine (via reverse SSH / jump host if needed)
- `curl`, `python3` available
- `repo` tool for source sync

## Quick Reference

| Step | Command / Action |
|------|-----------------|
| Download image | On Windows: Python script calls DCP API + downloads to local disk |
| Enter updater mode | `hdc shell reboot updater` |
| Flash partition | `hdc file send <local_img> /data/flash_tmp/<img> && hdc shell dd if=... of=/dev/block/by-name/...` |
| Flash userdata | `hdc file send userdata.img /dev/block/by-name/userdata` (direct write) |
| Reboot | `hdc shell reboot` |
| Update source | `repo sync -c --no-tags -j8` (on Linux build server) |

## Step 1: Download Daily Build Image (on Windows target)

Download directly on the Windows target machine to avoid transferring large images over SSH.

### DCP API

DCP page: `https://dcp.openharmony.cn/workbench/cicd/dailybuild/dailylist`

**IMPORTANT**: Date format must be `YYYYMMDDHHMMSS`, NOT `YYYY-M-D`.

```python
# Run on Windows target via SSH:
# ssh <target> "python download_daily.py"

import json, urllib.request, os, tarfile
from datetime import datetime

TODAY = datetime.now().strftime("%Y%m%d")
DL_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "daily_build")
os.makedirs(DL_DIR, exist_ok=True)

# Query DCP API
req = urllib.request.Request(
    "https://dcp.openharmony.cn/api/daily_build/build",
    data=json.dumps({
        "projectName": "openharmony", "branch": "master",
        "pageNum": 1, "pageSize": 50, "deviceLevel": "",
        "components": [], "type": 0,
        "startTime": f"{TODAY}000000", "endTime": f"{TODAY}235959",
        "sortType": "", "sortField": "", "withDomain": 1
    }).encode(),
    headers={"Content-Type": "application/json"}
)
resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
builds = resp.get("data", {}).get("dailyBuildVos", [])

# Find dayu200 image URL
img_url = None
for b in builds:
    if "dayu200" in (b.get("component", "") or "").lower():
        img_url = b.get("imgObsPath", "")
        break

if not img_url:
    raise RuntimeError("No dayu200 build found for today")

# Download
tar_path = os.path.join(DL_DIR, "dayu200_img.tar.gz")
print(f"Downloading: {img_url}")
urllib.request.urlretrieve(img_url, tar_path)

# Extract
print("Extracting...")
with tarfile.open(tar_path) as tf:
    tf.extractall(DL_DIR)
print("Done. Images in:", DL_DIR)
```

Run via SSH: `ssh <target> "python <path>/download_daily.py"`

### Image Contents

After extracting `dayu200_img.tar.gz`:
- `MiniLoaderAll.bin`, `parameter.txt`, `config.cfg`
- `uboot.img`, `boot_linux.img`, `resource.img`, `ramdisk.img`
- `system.img` (~2GB), `vendor.img` (~256MB), `userdata.img` (~1.4GB)
- `sys_prod.img`, `chip_prod.img`, `chip_ckm.img`, `updater.img`

## Step 2: Flash Device via HDC (Updater Mode)

### Why Updater Mode?

In normal mode, system/vendor/chip partitions are **mounted read-only**. Writing to mounted block devices causes silent failures. Updater mode keeps all partitions unmounted.

**Do NOT use `hdc reboot bootloader` + Rockusb** — USB re-enumeration through SSH/usbipd is unreliable.

### Partition Map

```
uboot       -> /dev/block/by-name/uboot
boot_linux  -> /dev/block/by-name/boot_linux
resource    -> /dev/block/by-name/resource
ramdisk     -> /dev/block/by-name/ramdisk
system      -> /dev/block/by-name/system
vendor      -> /dev/block/by-name/vendor
userdata    -> /dev/block/by-name/userdata
sys_prod    -> /dev/block/by-name/sys-prod
chip_prod   -> /dev/block/by-name/chip-prod
chip_ckm    -> /dev/block/by-name/chip_ckm
updater     -> /dev/block/by-name/updater
```

### Flash Procedure

Images are already on the Windows target (downloaded in Step 1). Use `hdc` from Windows directly.

```python
# Run on Windows target via SSH (hdc operates on locally-connected USB device)
import subprocess, time, os, shutil, glob

def find_hdc():
    """Find hdc.exe: fixed path -> PATH -> search common locations."""
    # 1. Fixed known path
    fixed = r"C:\Program Files\Huawei\DevEco Studio\sdk\default\openharmony\toolchains\hdc.exe"
    if os.path.isfile(fixed):
        return fixed

    # 2. Search in PATH
    found = shutil.which("hdc")
    if found:
        return found

    # 3. Search common install locations
    search_roots = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Huawei"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Huawei"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Huawei"),
        os.path.join(os.path.expanduser("~"), "Huawei"),
    ]
    for root in search_roots:
        for match in glob.glob(os.path.join(root, "**", "hdc.exe"), recursive=True):
            return match

    raise FileNotFoundError(
        "hdc.exe not found. Install OpenHarmony SDK or DevEco Studio, "
        "or add hdc.exe to PATH."
    )

HDC = find_hdc()
print(f"Using hdc: {HDC}")
IMG_DIR = r"C:\Users\<user>\Desktop\daily_build"

def hdc(*args):
    r = subprocess.run([HDC] + list(args), capture_output=True, text=True, timeout=600)
    print(r.stdout + r.stderr)
    return r

# 1. Reboot to updater mode
hdc("shell", "reboot", "updater")
time.sleep(30)  # Wait for device to come back

# 2. Mount userdata as temp storage
hdc("shell", "mkdir -p /data && mount /dev/block/by-name/userdata /data")
hdc("shell", "mkdir -p /data/flash_tmp")

# 3. Flash each partition (except userdata)
partitions = [
    ("uboot.img", "uboot"), ("boot_linux.img", "boot_linux"),
    ("resource.img", "resource"), ("ramdisk.img", "ramdisk"),
    ("updater.img", "updater"), ("sys_prod.img", "sys-prod"),
    ("chip_prod.img", "chip-prod"), ("chip_ckm.img", "chip_ckm"),
    ("system.img", "system"), ("vendor.img", "vendor"),
]
for img, part in partitions:
    local = f"{IMG_DIR}\\{img}"
    print(f"Flashing {part}...")
    hdc("file", "send", local, f"/data/flash_tmp/{img}")
    hdc("shell", f"dd if=/data/flash_tmp/{img} of=/dev/block/by-name/{part} bs=4M")
    hdc("shell", f"rm -f /data/flash_tmp/{img}")

# 4. Flash userdata (unmount first, then direct write)
hdc("shell", "umount /data")
hdc("file", "send", f"{IMG_DIR}\\userdata.img", "/dev/block/by-name/userdata")

# 5. Reboot
hdc("shell", "sync")
hdc("shell", "reboot")
```

### Partition Flash Order

Flash userdata **last** because it's used as temp storage. Recommended order:
1. uboot, boot_linux, resource, ramdisk (small, fast)
2. updater, sys_prod, chip_prod, chip_ckm (medium)
3. system, vendor (large)
4. userdata (last — unmount /data first, then direct write)

## Step 3: Update OpenHarmony Source (on Linux build server)

```bash
cd <openharmony_root>
repo sync -c --no-tags -j$(nproc) --force-sync --optimized-fetch
# If gitcode.com TLS errors occur, retry without proxy:
# http_proxy= https_proxy= repo sync -c --no-tags -j1 --force-sync <failed_repos>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| hdc.exe 找不到 | 按顺序查找：固定路径 → PATH 环境变量 → 搜索 Huawei/DevEco 目录 |
| DCP API 返回空数据 | 日期格式必须是 `YYYYMMDDHHMMSS`，不是 `YYYY-M-D` |
| dd 大分区无输出 | 必须在 updater 模式下烧写，正常模式分区被挂载 |
| hdc shell 无输出 | 设备可能启动失败（分区写入不完整），长按电源键重启 |
| Rockusb/usbipd 烧写失败 | USB 重枚举导致连接断开，改用 hdc updater 模式方案 |
| userdata 写入失败 | 必须先 umount /data，然后直接 `hdc file send` 到块设备 |
| DCP 需要登录 | 每日构建列表 API 不需要登录，但日期格式必须正确 |

## Troubleshooting

**设备黑屏（烧写后）：** 可能是在正常模式下 dd 导致分区损坏。长按电源键 10 秒重启，用 RKDevTool 刷回旧固件，然后用 updater 模式重新烧写。

**验证烧写成功：**
```
hdc shell param get const.product.software.version
# 应显示类似 "OpenHarmony 7.0.0.27"
```
