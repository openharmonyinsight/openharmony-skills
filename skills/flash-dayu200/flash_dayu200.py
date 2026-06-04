#!/usr/bin/env python3
"""
flash_dayu200.py — 通过 hdc updater 模式刷写 DAYU200/RK3568

将指定目录下的 .img 文件通过 hdc 刷到板上。
必须在能直接 USB 连板子的机器上运行（通常是 Windows）。

用法:
    python3 flash_dayu200.py [--img-dir DIR]

默认镜像目录: ~/Desktop/daily_build/
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import time


PARTITIONS = [
    ("uboot.img", "uboot"),
    ("boot_linux.img", "boot_linux"),
    ("resource.img", "resource"),
    ("ramdisk.img", "ramdisk"),
    ("updater.img", "updater"),
    ("sys_prod.img", "sys-prod"),
    ("chip_prod.img", "chip-prod"),
    ("chip_ckm.img", "chip_ckm"),
    ("system.img", "system"),
    ("vendor.img", "vendor"),
]


def find_hdc():
    """Find hdc executable: PATH -> fixed paths -> search."""
    found = shutil.which("hdc")
    if found:
        return found
    fixed = r"C:\Program Files\Huawei\DevEco Studio\sdk\default\openharmony\toolchains\hdc.exe"
    if os.path.isfile(fixed):
        return fixed
    search_roots = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Huawei"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Huawei"),
        os.path.join(os.path.expanduser("~"), "Huawei"),
    ]
    for root in search_roots:
        if root:
            for m in glob.glob(os.path.join(root, "**", "hdc.exe"), recursive=True):
                return m
    raise FileNotFoundError("hdc not found. Install OpenHarmony SDK or add hdc to PATH.")


def hdc_cmd(hdc_path, *args):
    """Run an hdc command and print output."""
    r = subprocess.run([hdc_path] + list(args), capture_output=True, text=True, timeout=600)
    out = (r.stdout + r.stderr).strip()
    if out:
        print(f"    {out}")
    return r


def find_img_dir(base_dir):
    """Find the directory containing system.img (may be nested)."""
    if os.path.exists(os.path.join(base_dir, "system.img")):
        return base_dir
    for d in os.listdir(base_dir):
        full = os.path.join(base_dir, d)
        if os.path.isdir(full) and os.path.exists(os.path.join(full, "system.img")):
            return full
    return None


def main():
    parser = argparse.ArgumentParser(description="Flash DAYU200 via hdc updater mode")
    parser.add_argument("--img-dir", default=os.path.join(os.path.expanduser("~"), "Desktop", "daily_build"))
    args = parser.parse_args()

    img_dir = find_img_dir(args.img_dir)
    if not img_dir:
        print(f"FAIL: system.img not found in {args.img_dir}")
        sys.exit(1)

    hdc = find_hdc()
    print(f"[1] hdc: {hdc}")
    print(f"    images: {img_dir}")

    print("[2] Reboot to updater mode...")
    hdc_cmd(hdc, "shell", "reboot", "updater")
    print("    Waiting 35s...")
    time.sleep(35)
    hdc_cmd(hdc, "list", "targets")

    print("[3] Mount userdata as temp storage...")
    hdc_cmd(hdc, "shell", "mkdir -p /data && mount /dev/block/by-name/userdata /data")
    hdc_cmd(hdc, "shell", "mkdir -p /data/flash_tmp")

    print("[4] Flashing partitions...")
    for img_name, part_name in PARTITIONS:
        local = os.path.join(img_dir, img_name)
        if not os.path.exists(local):
            print(f"    SKIP {img_name} (not found)")
            continue
        sz = os.path.getsize(local)
        print(f"    {part_name} ({sz:,} bytes)...")
        hdc_cmd(hdc, "file", "send", local, f"/data/flash_tmp/{img_name}")
        hdc_cmd(hdc, "shell", f"dd if=/data/flash_tmp/{img_name} of=/dev/block/by-name/{part_name} bs=4M")
        hdc_cmd(hdc, "shell", f"rm -f /data/flash_tmp/{img_name}")

    print("[5] Flashing userdata (unmount first)...")
    hdc_cmd(hdc, "shell", "umount /data")
    userdata = os.path.join(img_dir, "userdata.img")
    if os.path.exists(userdata):
        hdc_cmd(hdc, "file", "send", userdata, "/dev/block/by-name/userdata")
    else:
        print("    SKIP userdata.img (not found)")

    print("[6] Reboot...")
    hdc_cmd(hdc, "shell", "sync")
    hdc_cmd(hdc, "shell", "reboot")
    print("DONE. Wait ~60s for device to boot.")


if __name__ == "__main__":
    main()
