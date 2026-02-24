#!/usr/bin/env python3
"""
导出 HarmonyOS 设备当前页面的控件树
用法: python dump_controls.py [output_dir]
"""
import subprocess
import sys
import os
import json
import re
from datetime import datetime


def run_hdc_command(cmd: str) -> tuple:
    """执行 HDC 命令"""
    try:
        result = subprocess.run(f"hdc {cmd}", shell=True, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timeout"


def dump_layout():
    """导出控件树"""
    success, stdout, stderr = run_hdc_command("shell uitest dumpLayout")
    if not success:
        return None, f"导出控件树失败: {stderr}"
    return True, None


def find_layout_file():
    """查找设备上的控件树文件"""
    success, stdout, stderr = run_hdc_command("shell ls /data/local/tmp/layout*.json")
    if success and stdout:
        # 获取最新的文件
        files = stdout.strip().split('\n')
        for f in files:
            if f.strip():
                return f.strip()
    return None


def pull_layout_file(device_path: str, local_path: str):
    """拉取控件树文件"""
    success, stdout, stderr = run_hdc_command(f"file recv {device_path} {local_path}")
    return success, stderr


def translate_to_chinese(data: dict) -> dict:
    """将控件树字段翻译为中文"""
    field_mapping = {
        'text': '文本',
        'type': '类型',
        'id': '标识符',
        'key': '键值',
        'bounds': '边界',
        'description': '描述',
        'clickable': '可点击',
        'enabled': '可用',
        'scrollable': '可滚动',
        'checked': '已选中',
        'focused': '已聚焦',
        'selected': '已选择'
    }

    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_key = field_mapping.get(k, k)
            new_dict[new_key] = translate_to_chinese(v)
        return new_dict
    elif isinstance(data, list):
        return [translate_to_chinese(item) for item in data]
    return data


def flatten_controls(tree: dict, controls: list = None) -> list:
    """扁平化控件树"""
    if controls is None:
        controls = []

    control = {
        'type': tree.get('type', ''),
        'text': tree.get('text', ''),
        'id': tree.get('id', ''),
        'key': tree.get('key', ''),
        'bounds': tree.get('bounds', [])
    }

    # 生成定位器建议
    locators = {}
    if control['text']:
        locators['by_text'] = f"BY.text('{control['text']}')"
    if control['key']:
        locators['by_key'] = f"BY.key('{control['key']}')"
    if control['id']:
        locators['by_id'] = f"BY.id('{control['id']}')"
    if control['type']:
        locators['by_type'] = f"BY.type('{control['type']}')"

    control['locators'] = locators
    controls.append(control)

    # 递归处理子节点
    for child in tree.get('children', []):
        flatten_controls(child, controls)

    return controls


def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./output/controls"
    os.makedirs(output_dir, exist_ok=True)

    # 导出控件树
    print("正在导出控件树...")
    result, error = dump_layout()
    if error:
        print(f"错误: {error}")
        return 1

    # 查找文件
    print("查找控件树文件...")
    device_path = find_layout_file()
    if not device_path:
        print("错误: 未找到控件树文件")
        return 1

    # 拉取文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_path = os.path.join(output_dir, f"controls_{timestamp}.json")
    print(f"拉取控件树到: {local_path}")
    success, error = pull_layout_file(device_path, local_path)
    if not success:
        print(f"错误: {error}")
        return 1

    # 解析控件树
    with open(local_path, 'r', encoding='utf-8') as f:
        tree = json.load(f)

    # 生成翻译版本
    translated_tree = translate_to_chinese(tree)
    translated_path = os.path.join(output_dir, f"controls_zh_{timestamp}.json")
    with open(translated_path, 'w', encoding='utf-8') as f:
        json.dump(translated_tree, f, ensure_ascii=False, indent=2)

    # 扁平化控件列表
    controls = flatten_controls(tree)

    result = {
        "success": True,
        "snapshot_path": local_path,
        "translated_path": translated_path,
        "controls_count": len(controls),
        "controls_flat": controls[:50]  # 只输出前50个
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
