#!/usr/bin/env python3
"""
download_daily.py — 下载 OpenHarmony DAYU200/RK3568 日构建镜像

从 DCP API 查询今日（或最近7天）的 master 分支 dayu200 日构建，
下载 img tar.gz 并解压到指定目录。

用法:
    python3 download_daily.py [--output-dir DIR] [--days N]

默认输出到 ~/Desktop/daily_build/
"""

import argparse
import json
import os
import sys
import tarfile
import urllib.request
from datetime import datetime, timedelta


DCP_API = "https://dcp.openharmony.cn/api/daily_build/build"


def query_dcp(date_str):
    """查询指定日期的日构建列表"""
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


def find_dayu200_url(builds):
    """从构建列表中找到 dayu200 的镜像 URL"""
    for b in builds:
        if "dayu200" in (b.get("component", "") or "").lower():
            return b.get("imgObsPath", "")
    return None


def main():
    parser = argparse.ArgumentParser(description="下载 DAYU200 日构建镜像")
    parser.add_argument("--output-dir", default=os.path.join(os.path.expanduser("~"), "Desktop", "daily_build"))
    parser.add_argument("--days", type=int, default=7, help="搜索最近N天（默认7）")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    img_url = None
    found_date = None
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

        img_url = find_dayu200_url(builds)
        if img_url:
            found_date = date_str
            print(f"  FOUND dayu200 build")
            break
        else:
            comps = [b.get("component", "?") for b in builds[:5]]
            print(f"  {len(builds)} builds, no dayu200 (sample: {comps})")

    if not img_url:
        print(f"FAIL: No dayu200 build found in last {args.days} days")
        sys.exit(1)

    tar_path = os.path.join(args.output_dir, "dayu200_img.tar.gz")
    if os.path.exists(tar_path) and os.path.getsize(tar_path) > 100_000_000:
        print(f"Image already exists ({os.path.getsize(tar_path)} bytes), skip download")
        print(f"  Delete {tar_path} to force re-download")
    else:
        print(f"Downloading: {img_url}")
        urllib.request.urlretrieve(img_url, tar_path)
        print(f"  Done: {os.path.getsize(tar_path)} bytes")

    print("Extracting...")
    with tarfile.open(tar_path) as tf:
        tf.extractall(args.output_dir)

    # Find extracted image subdir
    img_dir = args.output_dir
    for d in os.listdir(args.output_dir):
        full = os.path.join(args.output_dir, d)
        if os.path.isdir(full) and os.path.exists(os.path.join(full, "system.img")):
            img_dir = full
            break

    print(f"Images ready in: {img_dir}")
    print(f"Date: {found_date}")


if __name__ == "__main__":
    main()
