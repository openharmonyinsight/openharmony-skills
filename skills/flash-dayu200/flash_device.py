#!/usr/bin/env python3
"""
flash_device.py — Flash OpenHarmony device via hdc updater mode.
Parses partition table from parameter.txt automatically.
"""
import argparse, glob, os, re, shutil, subprocess, sys, time

def find_hdc():
    found = shutil.which("hdc")
    if found: return found
    for env_key in ["LOCALAPPDATA", "ProgramFiles", "ProgramFiles(x86)"]:
        v = os.environ.get(env_key, "")
        if v:
            for m in glob.glob(os.path.join(v, "Huawei", "**", "hdc*"), recursive=True):
                if os.path.isfile(m): return m
    for m in glob.glob(os.path.join(os.path.expanduser("~"), "Huawei", "**", "hdc*"), recursive=True):
        if os.path.isfile(m): return m
    raise FileNotFoundError("hdc not found")

def hdc_cmd(hdc, *args):
    r = subprocess.run([hdc]+list(args), capture_output=True, text=True, timeout=600)
    out = (r.stdout+r.stderr).strip()
    if out: print(f"    {out}")
    if r.returncode != 0:
        raise RuntimeError(f"hdc {' '.join(args)} failed with {r.returncode}: {out}")
    return r

def find_img_dir(base):
    if os.path.exists(os.path.join(base, "system.img")): return base
    for d in os.listdir(base):
        f = os.path.join(base, d)
        if os.path.isdir(f) and os.path.exists(os.path.join(f, "system.img")): return f
    return None

def parse_partitions(img_dir):
    pf = os.path.join(img_dir, "parameter.txt")
    if not os.path.exists(pf): return None
    content = open(pf).read()
    m = re.search(r"CMDLINE:.*mtdparts=\S+:(.*)", content)
    if not m: return None
    parts = []
    for p in m.group(1).split(","):
        m2 = re.search(r"\(([^:)]+)", p)
        if m2:
            name = m2.group(1)
            img = f"{name}.img"
            if os.path.exists(os.path.join(img_dir, img)):
                parts.append((img, name))
    return parts

def build_arg_parser():
    ap = argparse.ArgumentParser(description="Flash OpenHarmony device via hdc updater mode")
    ap.add_argument("--img-dir", default="daily_build")
    return ap

def main():
    ap = build_arg_parser()
    args = ap.parse_args()
    img_dir = find_img_dir(args.img_dir)
    if not img_dir: print(f"FAIL: system.img not found in {args.img_dir}"); sys.exit(1)
    hdc = find_hdc()
    print(f"[1] hdc: {hdc}\n    images: {img_dir}")
    parts = parse_partitions(img_dir)
    if parts: print(f"    Parsed {len(parts)} partitions from parameter.txt")
    else:
        print("    WARN: parameter.txt not found, using fallback")
        parts = [("uboot.img","uboot"),("boot_linux.img","boot_linux"),("resource.img","resource"),
            ("ramdisk.img","ramdisk"),("updater.img","updater"),("sys_prod.img","sys-prod"),
            ("chip_prod.img","chip-prod"),("chip_ckm.img","chip_ckm"),
            ("system.img","system"),("vendor.img","vendor"),("userdata.img","userdata")]
    ud = [(i,p) for i,p in parts if p=="userdata"]
    others = [(i,p) for i,p in parts if p!="userdata"]
    print("[2] Reboot to updater..."); hdc_cmd(hdc,"shell","reboot","updater"); print("    Waiting 35s..."); time.sleep(35); hdc_cmd(hdc,"list","targets")
    print("[3] Mount userdata..."); hdc_cmd(hdc,"shell","mkdir -p /data && mount /dev/block/by-name/userdata /data"); hdc_cmd(hdc,"shell","mkdir -p /data/flash_tmp")
    print("[4] Flashing...")
    for img,blk in others:
        local = os.path.join(img_dir, img)
        if not os.path.exists(local): continue
        print(f"    {blk} ({os.path.getsize(local):,} bytes)...")
        hdc_cmd(hdc,"file","send",local,f"/data/flash_tmp/{img}"); hdc_cmd(hdc,"shell",f"dd if=/data/flash_tmp/{img} of=/dev/block/by-name/{blk} bs=4M"); hdc_cmd(hdc,"shell",f"rm -f /data/flash_tmp/{img}")
    if ud:
        print("[5] Flashing userdata..."); hdc_cmd(hdc,"shell","umount /data")
        local = os.path.join(img_dir, ud[0][0])
        if os.path.exists(local): hdc_cmd(hdc,"file","send",local,"/dev/block/by-name/userdata")
    print("[6] Reboot..."); hdc_cmd(hdc,"shell","sync"); hdc_cmd(hdc,"shell","reboot"); print("DONE.")

if __name__ == "__main__": main()
