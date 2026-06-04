---
name: flash-dayu200
description: Use when the user wants to download OpenHarmony daily build images for DAYU200/RK3568, flash them to a real device, or update the OpenHarmony source tree. Triggers on mentions of daily build, DY200, DAYU200, RK3568, flashing, burning, hdc reboot bootloader, or upgrading firmware.
---

# Flash DAYU200 (RK3568) with Daily Build

Download today's OpenHarmony master daily build, flash via hdc updater mode, update local source.

## Scripts

| Script | Where to run | Purpose |
|--------|-------------|---------|
| `download_daily.py` | Windows target (or any machine) | Query DCP API, download + extract dayu200 img |
| `flash_dayu200.py` | Windows target (USB to board) | Flash all partitions via hdc updater mode |

Scripts are in this skill directory: `~/.claude/skills/flash_daily_dayu200/`

## Quick Reference

```bash
# Step 1: Download daily build (on Windows via SSH, or directly)
python3 ~/.claude/skills/flash_daily_dayu200/download_daily.py --output-dir ~/Desktop/daily_build

# Step 2: Flash device (on Windows with USB to DAYU200)
python3 ~/.claude/skills/flash_daily_dayu200/flash_dayu200.py --img-dir ~/Desktop/daily_build

# Step 3: Update source (on Linux build server)
cd <openharmony_root> && repo sync -c --no-tags -j8 --force-sync --optimized-fetch
```

## Via SSH (typical setup)

```bash
# Upload scripts to Windows
scp -P 2222 ~/.claude/skills/flash_daily_dayu200/download_daily.py user@localhost:mmi_push/
scp -P 2222 ~/.claude/skills/flash_daily_dayu200/flash_dayu200.py user@localhost:mmi_push/

# Download on Windows
ssh -p 2222 user@localhost "python mmi_push\\download_daily.py"

# Flash from Windows
ssh -p 2222 user@localhost "python mmi_push\\flash_dayu200.py"

# Verify after ~60s boot
ssh -p 2222 user@localhost "hdc shell param get const.product.software.version"
```

## DCP API

- Endpoint: `https://dcp.openharmony.cn/api/daily_build/build`
- Response path: `data.builds.dataList[].component == "dayu200"` → `imgObsPath`
- Date format: `YYYYMMDDHHMMSS` (NOT `YYYY-M-D`)
- `download_daily.py` auto-searches last 7 days if today's build is missing

## Partition Map

| Image | Block device |
|-------|-------------|
| uboot.img | /dev/block/by-name/uboot |
| boot_linux.img | /dev/block/by-name/boot_linux |
| system.img | /dev/block/by-name/system |
| vendor.img | /dev/block/by-name/vendor |
| userdata.img | /dev/block/by-name/userdata |
| sys_prod.img | /dev/block/by-name/sys-prod |
| chip_prod.img | /dev/block/by-name/chip-prod |
| chip_ckm.img | /dev/block/by-name/chip_ckm |

## Why Updater Mode

Normal mode mounts system/vendor read-only → dd silently fails. Updater mode keeps partitions unmounted. Do NOT use `hdc reboot bootloader` + Rockusb — USB re-enumeration through SSH is unreliable.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| DCP API 返回空 | 检查日期格式 `YYYYMMDDHHMMSS`；脚本自动搜索最近 7 天 |
| API 解析失败 | 响应路径是 `data.builds.dataList`，不是 `data.dailyBuildVos` |
| dd 无输出 | 必须 updater 模式，不能正常模式下 dd |
| userdata 写入失败 | 先 umount /data，再直接 `hdc file send` 到块设备 |
| hdc 找不到 | 脚本自动搜索 PATH → DevEco Studio → Huawei 目录 |
| 设备黑屏 | 长按电源 10s 重启，用 RKDevTool 恢复后用 updater 模式重刷 |

## Verify

```bash
hdc shell param get const.product.software.version
# 应显示 "OpenHarmony 7.0.0.27" 或更新版本
```
