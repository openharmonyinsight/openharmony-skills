#!/usr/bin/env python3
"""
download_daily.py — 下载 OpenHarmony 测试设备日构建镜像

从 DCP API 查询最近的 master 分支日构建，下载并解压。
支持指定设备组件名（默认 dayu200）。

用法:
    python3 download_daily.py [--component dayu200] [--output-dir DIR] [--days N]
"""

import argparse
import json
import os
import sys
import tarfile
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path


DCP_API = "https://dcp.openharmony.cn/api/daily_build/build"


def build_arg_parser():
    parser = argparse.ArgumentParser(description="下载 OpenHarmony 日构建镜像")
    parser.add_argument("--component", default="dayu200", help="设备组件名（默认 dayu200）")
    parser.add_argument("--output-dir", default="daily_build")
    parser.add_argument("--days", type=int, default=7, help="搜索最近N天（默认7）")
    return parser


def safe_extract(tar, output_dir):
    output_path = Path(output_dir).resolve()
    for member in tar.getmembers():
        if member.issym() or member.islnk():
            raise ValueError(f"unsafe tar link member: {member.name}")
        if not (member.isfile() or member.isdir()):
            raise ValueError(f"unsupported tar member type: {member.name}")
        target_path = (output_path / member.name).resolve()
        if output_path != target_path and output_path not in target_path.parents:
            raise ValueError(f"unsafe tar member path: {member.name}")
    tar.extractall(output_path)


def query_dcp(date_str):
    req = urllib.request.Request(
        DCP_API,
        data=json.dumps({
            "projectName": "openharmony", "branch": "master",
            "pageNum": 1, "pageSize": 50, "deviceLevel": "",
            "components": [], "type": 0,
            "startTime": f"{date_str}000000", "endTime": f"{date_str}235959",
            "sortType": "", "sortField": "", "withDomain": 1
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return resp.get("data", {}).get("builds", {}).get("dataList", [])


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    img_url = None
    for days_ago in range(args.days):
        dt = datetime.now() - timedelta(days=days_ago)
        date_str = dt.strftime("%Y%m%d")
        label = "today" if days_ago == 0 else f"{days_ago}d ago"
        print(f"[{label}] Querying DCP for {date_str}...")
        try:
            builds = query_dcp(date_str)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        for b in builds:
            if args.component.lower() in (b.get("component", "") or "").lower():
                img_url = b.get("imgObsPath", "")
                if img_url:
                    print(f"  FOUND: {b.get('component')}")
                    break
        if img_url:
            break
        comps = [b.get("component", "?") for b in builds[:5]]
        print(f"  {len(builds)} builds, no {args.component} (sample: {comps})")

    if not img_url:
        print(f"FAIL: No {args.component} build found in last {args.days} days")
        sys.exit(1)

    tar_path = os.path.join(args.output_dir, f"{args.component}_img.tar.gz")
    need_download = True
    if os.path.exists(tar_path):
        try:
            with tarfile.open(tar_path) as tf:
                tf.getmembers()
            print(f"Image exists and is valid ({os.path.getsize(tar_path)} bytes), skip download")
            print(f"  Delete {tar_path} to force re-download")
            need_download = False
        except (tarfile.TarError, EOFError, OSError):
            print(f"Existing archive is corrupt, re-downloading")
            os.unlink(tar_path)

    if need_download:
        print(f"Downloading: {img_url}")
        urllib.request.urlretrieve(img_url, tar_path)
        size = os.path.getsize(tar_path)
        print(f"  Done: {size} bytes")
        # Verify downloaded archive integrity
        try:
            with tarfile.open(tar_path) as tf:
                tf.getmembers()
        except (tarfile.TarError, EOFError, OSError) as e:
            print(f"FAIL: Downloaded archive is corrupt: {e}")
            print(f"  Delete {tar_path} and retry")
            sys.exit(1)

    print("Extracting...")
    with tarfile.open(tar_path) as tf:
        safe_extract(tf, args.output_dir)

    img_dir = args.output_dir
    for d in os.listdir(args.output_dir):
        full = os.path.join(args.output_dir, d)
        if os.path.isdir(full) and os.path.exists(os.path.join(full, "system.img")):
            img_dir = full
            break

    print(f"Images ready in: {img_dir}")


if __name__ == "__main__":
    main()
