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
SKILL_NAME = "ohos-issue-xts-log-analysis"

def _is_skill_root(d):
    """通过标记文件判断 d 是否为 skill 根目录（跨平台、跨安装位置）。"""
    if not d or not os.path.isdir(d):
        return False
    return (
        os.path.isfile(os.path.join(d, "SKILL.md"))
        or os.path.exists(os.path.join(d, "data", "xts_rules.db"))
        or os.path.isdir(os.path.join(d, "tools"))
    )

def _resolve_skill_dir():
    """
    跨平台解析 skill 根目录（多候选 + 标记文件验证）。
    覆盖场景：
      - 全局安装：~/.config/opencode/skills/<name>/（文档默认）
      - 本机安装：~/.opencode/skills/<name>/
      - Windows 用户反馈：~/.opencode/.config/opencode/skills/<name>/
      - 自定义：$OPENCODE_CONFIG_DIR/skills/<name>/ 或 $OHS_XTS_SKILL_DIR
      - 脚本就地运行：__file__ 向上查找
      - 项目内：CWD 向上查找 .opencode/skills/<name>
    """
    # 0. 显式环境变量覆盖（最高优先级）
    env_dir = os.environ.get("OHS_XTS_SKILL_DIR")
    if env_dir and _is_skill_root(env_dir):
        return env_dir

    home = os.path.expanduser("~")

    # 1. 基于 __file__ 向上查找（脚本自身位置，最多 5 层）
    try:
        p = os.path.abspath(__file__)
        for _ in range(5):
            if _is_skill_root(p):
                return p
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    except Exception:
        pass

    # 2. 基于 CWD 向上查找项目内 .opencode/skills/<name>
    try:
        p = os.getcwd()
        for _ in range(6):
            cand = os.path.join(p, ".opencode", "skills", SKILL_NAME)
            if _is_skill_root(cand):
                return cand
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    except Exception:
        pass

    # 3. 已知全局候选位置（文档默认 + 实际观察到的安装路径）
    candidates = [
        os.path.join(home, ".config", "opencode", "skills", SKILL_NAME),               # 文档默认全局
        os.path.join(home, ".opencode", "skills", SKILL_NAME),                         # 本机安装
        os.path.join(home, ".opencode", ".config", "opencode", "skills", SKILL_NAME),  # Windows 用户反馈
        os.path.join(home, ".claude", "skills", SKILL_NAME),                           # Claude 兼容
        os.path.join(home, ".agents", "skills", SKILL_NAME),                           # Agent 兼容
    ]
    cfg_dir = os.environ.get("OPENCODE_CONFIG_DIR")  # 自定义 config 目录
    if cfg_dir:
        candidates.insert(0, os.path.join(cfg_dir, "skills", SKILL_NAME))

    for c in candidates:
        if _is_skill_root(c):
            return c

    # 4. 递归搜索兜底：在常见 opencode 根目录下任意深度查找 skills/<name>/SKILL.md
    #    覆盖任意嵌套层级（如 ~/.opencode/.config/opencode/skills/... 等无法穷举的结构）
    try:
        search_bases = [
            os.path.join(home, ".opencode"),
            os.path.join(home, ".config", "opencode"),
            os.path.join(home, ".opencode", ".config", "opencode"),
            os.path.join(home, ".claude"),
            os.path.join(home, ".agents"),
        ]
        if cfg_dir:
            search_bases.insert(0, cfg_dir)
        for base in search_bases:
            if not os.path.isdir(base):
                continue
            for hit in glob.glob(
                os.path.join(base, "**", "skills", SKILL_NAME, "SKILL.md"),
                recursive=True,
            ):
                found = os.path.dirname(hit)
                if _is_skill_root(found):
                    return found
    except Exception:
        pass

    # 5. 最终回退（不验证，保留旧路径以输出可读错误）
    return os.path.join(home, ".opencode", "skills", SKILL_NAME)

SKILL_DIR = _resolve_skill_dir()

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
    import platform
    
    # 平台检测：Windows原生直接运行hilogtool.exe，Linux用wine64
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        # Windows原生：直接运行.exe，无需wine
        cmd = [
            hilogtool_path,
            "parse",
            "-i", gz_file,
            "-o", output_dir,
            "-d", dict_file
        ]
        env = os.environ.copy()
    else:
        # Linux：通过wine64运行Windows程序
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
        # Windows下 hilogtool.exe 可能输出 GBK/CP936，用 errors='replace' 避免解码异常
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120
        )
        
        if result.returncode == 0:
            return {"file": gz_file, "status": "success"}
        else:
            return {"file": gz_file, "status": "failed", "error": result.stderr}
    
    except subprocess.TimeoutExpired:
        return {"file": gz_file, "status": "failed", "error": "Timeout"}
    except FileNotFoundError as e:
        return {"file": gz_file, "status": "failed", "error": f"工具未找到: {e}"}
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
        "log_dir": os.path.dirname(output_dir[:-7] if output_dir.endswith('_parsed') else output_dir),
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
            print("   请手动清理：")
            import platform as _pf
            if _pf.system() == "Windows":
                print(f'   cmd:        rmdir /s /q "{skill_dict_dir}"')
                print(f'   PowerShell: Remove-Item -Recurse -Force "{skill_dict_dir}"')
            else:
                print(f'   rm -rf "{skill_dict_dir}"')

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
    
    # 设置hilogtool路径（跨平台：基于skill目录，自动适配正斜杠/反斜杠）
    if hilogtool_path is None:
        hilogtool_path = os.path.join(
            SKILL_DIR, "tools", "hilogtool.exe"
        )
    
    if not os.path.exists(hilogtool_path):
        print(f"❌ hilogtool不存在: {hilogtool_path}")
        print(f"   解析到的 SKILL_DIR = {SKILL_DIR}")
        if not _is_skill_root(SKILL_DIR):
            print(f"   ⚠️ 该目录未通过标记校验（无 SKILL.md / data/xts_rules.db），说明 skill 实际不在该位置。")
            print(f"   已尝试：__file__ 向上查找 / CWD 向上查找 / 常规候选位置 / 递归搜索 ~/.opencode ~/.config/opencode")
        print(f"   解决方案（任选其一）：")
        print(f"   1) 设置环境变量指向真实 skill 根目录（含 SKILL.md）：")
        print(f"      set OHS_XTS_SKILL_DIR=<真实skill根目录绝对路径>")
        print(f"   2) 直接把 hilogtool.exe 路径作为第5个参数传入：")
        print(f"      python parallel_decrypt.py <日志目录> <输出目录> <dict文件> <线程数> <hilogtool.exe绝对路径>")
        print(f"   3) 若已知 skill 真实安装路径，请反馈以补充到候选列表。")
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
        print("用法: python3 parallel_decrypt.py <日志目录> [输出目录] [dict文件] [线程数] [hilogtool路径]")
        print("\n功能：")
        print("  - 并行解密多个hilog.gz文件（提升10倍效率）")
        print("  - 自动检查缓存（避免重复解密）")
        print("  - 验证解密结果（确保解密成功）")
        print("  - 跨平台：Windows原生运行exe，Linux用wine64")
        print("\n示例:")
        print("  python3 parallel_decrypt.py /path/to/hilog_FMR0123417000740")
        print("  python3 parallel_decrypt.py /path/to/logs /path/to/output 4")
        print("  python3 parallel_decrypt.py D:\\logs\\hilog D:\\logs\\hilog_parsed")
        print("  python3 parallel_decrypt.py D:\\logs\\hilog D:\\out D:\\dict.zip 4 D:\\hilogtool.exe")
        sys.exit(1)
    
    log_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dict_file = sys.argv[3] if len(sys.argv) > 3 else None
    max_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    hilogtool_path = sys.argv[5] if len(sys.argv) > 5 else None
    
    if not os.path.exists(log_dir):
        print(f"❌ 日志目录不存在: {log_dir}")
        sys.exit(1)
    
    success = parallel_decrypt(log_dir, output_dir, dict_file, hilogtool_path=hilogtool_path, max_workers=max_workers)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()