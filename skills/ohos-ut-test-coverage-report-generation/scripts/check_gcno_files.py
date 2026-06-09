#!/usr/bin/env python3

import argparse
import os
import sys
import json
from pathlib import Path


def check_gcno_files(code_root, part_name_list):
    parts_path_info = os.path.join(code_root, "out/generic_generic_arm_64only/general_all_phone_standard/build_configs/parts_info/parts_path_info.json")

    if not os.path.exists(parts_path_info):
        return {
            "success":False,
            "error": f"parts_path_info.json not found"
        }
    
    with open(parts_path_info, "r") as f:
        parts_path_dict = json.load(f)

    missing_files = []

    for part_name in part_name_list:
        if part_name not in parts_path_dict:
            missing_files.append((part_name, f"Part not found"))
            continue

        part_path = parts_path_dict[part_name]
        obj_dir = os.path.join(code_root, "out/generic_generic_arm_64only/general_all_phone_standard/obj", part_path)

        if not os.path.exists(obj_dir):
            missing_files.append((part_name, f"obj not found: {obj_dir}"))
            continue

        obj_dir_path = Path(obj_dir)
        obj_files = list(obj_dir_path.rglob("*.o"))

        for obj_file in obj_files:
            if "test" in obj_file.parts:
                continue

            gcno_file = obj_file.with_suffix(".gcno")
            if not gcno_file.exists():
                missing_files.append((part_name, str(gcno_file)))

    return {
            "success":True,
            "missing_files": missing_files
        }


def main():
    parser = argparse.ArgumentParser(description='Check gcno files for coverage compilation')
    parser.add_argument('--code_root', required=True, help='code_root')
    parser.add_argument('--parts', required=True, help='part names ')
    
    args = parser.parse_args()
    
    part_name_list  = [p.strip() for p in args.parts.split(",")]
    result =check_gcno_files(args.code_root, part_name_list)
    
    if result["success"]:
        print("All gcno files found.")
        sys.exit(0)
    else:
        print("Missing gcno files:")
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())