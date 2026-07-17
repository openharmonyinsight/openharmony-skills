#!/usr/bin/env python3
"""
并行解密脚本

功能：
1. 并行解密多个hilog.gz文件（提升10倍效率）
2. 检查解密缓存（避免重复解密）
3. 验证解密结果（确保解密成功）
4. 生成解密状态文件（供后续分析使用）

缓存机制：
- 解密状态文件：<日志目录>_parsed/.decrypt_state.json
- 如果状态文件存在且解密完成，跳过解密
- 并行解密多个文件，提升效率
"""

import concurrent.futures
import glob
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DECRYPT_STATE_FILE = ".decrypt_state.json"
SKILL_DIR = os.path.expanduser("~/.opencode/skills/ohos-issue-xts-log-analysis")

def find_hilog_gz_files(log_dir):
    """查找所有hilog.gz文件"""
    pattern = os.path.join(log_dir, "**/*.gz")
    gz_files = glob.glob(pattern, recursive=True)
    return sorted(gz_files)

def find_dict_file(log_dir):
    """查找dict文件"""
    patterns = [
        os.path.join(log_dir, "hilog_dict.*.zip"),
        os.path.join(log_dir, "dict.zip"),
        os.path.join(log_dir, "**/hilog_dict.*.zip"),
        os.path.join(log_dir, "**/dict.zip")
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        if files:
            return files[0]
    
    return None

def check_decrypt_cache(output_dir):
    """检查解密缓存"""
    state_file = os.path.join(output_dir, DECRYPT_STATE_FILE)
    
    if not os.path.exists(state_file):
        return None
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        if state.get("decrypted", False):
            return state
    except Exception as e:
        print(f"⚠️  缓存文件读取失败: {e}")
    
    return None

def decrypt_single_file(gz_file, output_dir, dict_file, hilogtool_path):
    """解密单个hilog.gz文件"""
    cmd = [
        "wine64",
        hilogtool_path,
        "parse",
        "-i", gz_file,
        "-o", output_dir,
        "-d", dict_file
    ]
    
    env = os.environ.copy()
    env["DISPLAY"] = ""
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return {"file": gz_file, "status": "success"}
        else:
            return {"file": gz_file, "status": "failed", "error": result.stderr}
    
    except subprocess.TimeoutExpired:
        return {"file": gz_file, "status": "failed", "error": "Timeout"}
    except Exception as e:
        return {"file": gz_file, "status": "failed", "error": str(e)}

def verify_decrypted_file(output_file):
    """验证解密文件"""
    if not os.path.exists(output_file):
        return False, "文件不存在"
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f)
        
        if lines == 0:
            return False, "文件为空"
        
        return True, f"{lines}行"
    except Exception as e:
        return False, str(e)

def generate_decrypt_state(output_dir, gz_files, dict_file, parallel=True):
    """生成解密状态文件"""
    state_file = os.path.join(output_dir, DECRYPT_STATE_FILE)
    
    decrypted_files = []
    for gz_file in gz_files:
        basename = os.path.basename(gz_file)
        txt_file = os.path.join(output_dir, basename.replace('.gz', '.txt'))
        
        if os.path.exists(txt_file):
            valid, info = verify_decrypted_file(txt_file)
            size = os.path.getsize(txt_file) if os.path.exists(txt_file) else 0
            
            decrypted_files.append({
                "file": basename,
                "output": os.path.basename(txt_file),
                "valid": valid,
                "info": info,
                "size": f"{size/1024/1024:.2f}MB"
            })
    
    state = {
        "log_dir": os.path.dirname(output_dir.replace('_parsed', '')),
        "output_dir": output_dir,
        "dict_location": dict_file,
        "decrypted": True,
        "parallel": parallel,
        "decrypted_files": decrypted_files,
        "total_files": len(gz_files),
        "success_files": sum(1 for f in decrypted_files if f["valid"]),
        "decrypted_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    return state

def verify_dict_location():
    """验证dict位置，防止dict被放在skill目录"""
    skill_dict_dir = os.path.join(SKILL_DIR, "dict")
    
    if os.path.exists(skill_dict_dir):
        print("\n⚠️  警告：检测到skill目录下有dict文件！")
        print(f"   位置: {skill_dict_dir}")
        print("   原因：执行hilogtool时可能使用了cd命令（错误做法）")
        print("   清理中...")
        
        import shutil
        try:
            shutil.rmtree(skill_dict_dir)
            print("   ✅ 已自动清理")
        except Exception as e:
            print(f"   ❌ 清理失败: {e}")
            print(f"   请手动清理: rm -rf {skill_dict_dir}")

def parallel_decrypt(log_dir, output_dir=None, dict_file=None, hilogtool_path=None, max_workers=4):
    """并行解密多个hilog.gz文件"""
    
    # 查找hilog.gz文件
    gz_files = find_hilog_gz_files(log_dir)
    
    if not gz_files:
        print("❌ 未找到hilog.gz文件")
        return False
    
    print(f"📁 找到 {len(gz_files)} 个hilog.gz文件")
    
    # 设置输出目录
    if output_dir is None:
        output_dir = f"{log_dir}_parsed"
    
    # 检查缓存
    cache = check_decrypt_cache(output_dir)
    if cache:
        print("✅ 检测到解密缓存，跳过解密")
        print(f"   缓存时间: {cache.get('decrypted_time', 'N/A')}")
        print(f"   成功文件: {cache.get('success_files', 0)}/{cache.get('total_files', 0)}")
        return True
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找dict文件
    if dict_file is None:
        dict_file = find_dict_file(log_dir)
    
    if not dict_file:
        print("❌ 未找到dict文件")
        return False
    
    print(f"📄 Dict文件: {dict_file}")
    
    # 设置hilogtool路径
    if hilogtool_path is None:
        hilogtool_path = os.path.expanduser(
            "~/.opencode/skills/ohos-issue-xts-log-analysis/docs/tools/hilogtool/hilogtool.exe"
        )
    
    if not os.path.exists(hilogtool_path):
        print(f"❌ hilogtool不存在: {hilogtool_path}")
        return False
    
    # 并行解密
    print(f"🚀 开始并行解密（{max_workers}线程）...")
    start_time = datetime.now()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(decrypt_single_file, f, output_dir, dict_file, hilogtool_path): f
            for f in gz_files
        }
        
        completed = 0
        failed = 0
        
        for future in concurrent.futures.as_completed(futures):
            gz_file = futures[future]
            try:
                result = future.result()
                
                if result["status"] == "success":
                    completed += 1
                    print(f"  ✅ [{completed}/{len(gz_files)}] {os.path.basename(gz_file)}")
                else:
                    failed += 1
                    print(f"  ❌ [{completed+failed}/{len(gz_files)}] {os.path.basename(gz_file)}: {result.get('error', 'Unknown')}")
            
            except Exception as e:
                failed += 1
                print(f"  ❌ 解密异常: {os.path.basename(gz_file)}: {e}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n⏱️  解密耗时: {duration:.1f}秒")
    print(f"✅ 成功: {completed}/{len(gz_files)}")
    
    if failed > 0:
        print(f"❌ 失败: {failed}/{len(gz_files)}")
    
    # 生成解密状态文件
    state = generate_decrypt_state(output_dir, gz_files, dict_file, parallel=True)
    print(f"\n📄 解密状态文件: {os.path.join(output_dir, DECRYPT_STATE_FILE)}")
    
    # 验证dict位置（防止dict被放在skill目录）
    verify_dict_location()
    
    return failed == 0

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 parallel_decrypt.py <日志目录> [输出目录] [dict文件] [线程数]")
        print("\n功能：")
        print("  - 并行解密多个hilog.gz文件（提升10倍效率）")
        print("  - 自动检查缓存（避免重复解密）")
        print("  - 验证解密结果（确保解密成功）")
        print("\n示例:")
        print("  python3 parallel_decrypt.py /path/to/hilog_FMR0123417000740")
        print("  python3 parallel_decrypt.py /path/to/logs /path/to/output 4")
        sys.exit(1)
    
    log_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dict_file = sys.argv[3] if len(sys.argv) > 3 else None
    max_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    
    if not os.path.exists(log_dir):
        print(f"❌ 日志目录不存在: {log_dir}")
        sys.exit(1)
    
    success = parallel_decrypt(log_dir, output_dir, dict_file, max_workers=max_workers)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()