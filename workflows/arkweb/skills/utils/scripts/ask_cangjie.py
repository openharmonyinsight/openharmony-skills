#!/usr/bin/env python3
"""
AI Agent (Claude) 通过命令行调用仓颉知识库的入口脚本
用法: python ask_cangjie.py 'query'

自动初始化功能：
- 首次运行时自动下载官方文档到 hm-docs/
- 首次运行时自动构建向量数据库到 chroma_db/
"""

import sys
import os
import subprocess
from dotenv import load_dotenv

# 确保读取 scripts 目录下的 .env 文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 项目根目录（scripts 的上一级）
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# 数据目录路径（注意：新的逻辑将压缩包解压到 scripts/ 目录下）
HM_DOCS_DIR = os.path.join(SCRIPT_DIR, "hm-docs")
CHROMA_DB_DIR = os.path.join(SCRIPT_DIR, "chroma_db")
EVOLUTION_MD = os.path.join(PROJECT_ROOT, "Evolution.md")
# 压缩包文件路径
HM_DOCS_ZIP = os.path.join(SCRIPT_DIR, "hm-docs.zip")
CHROMA_DB_ZIP = os.path.join(SCRIPT_DIR, "chroma_db.zip")


def extract_zip(zip_path: str, target_dir: str) -> bool:
    """
    解压缩 .zip 文件到指定的目标目录
    
    Args:
        zip_path: 压缩包路径
        target_dir: 目标目录路径（如 scripts/hm-docs）
    
    Returns:
        成功返回 True，失败返回 False
    """
    if not os.path.exists(zip_path):
        return False

    try:
        import zipfile
        
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"[OK] 已解压: {zip_path} -> {target_dir}")
        return True
    except Exception as e:
        print(f"[ERROR] 解压失败: {e}")
        return False


def check_and_init_docs():
    """
    检查并初始化本地文档（L3 必需，无论 L1 是否启用都要执行）
    """
    check_passed = True
    
    # ========== hm-docs 处理 ==========
    docs_exists = os.path.exists(HM_DOCS_DIR) and os.listdir(HM_DOCS_DIR)
    docs_zip_exists = os.path.exists(HM_DOCS_ZIP)

    if docs_exists:
        print("[OK] 本地文档已存在")
    elif docs_zip_exists:
        print("[INIT] 检测到文档压缩包，开始解压...")
        if extract_zip(HM_DOCS_ZIP, HM_DOCS_DIR):
            print("[OK] 本地文档解压完成")
        else:
            print("[ERROR] 文档解压失败")
            check_passed = False
    else:
        print("[INIT] 本地文档目录和压缩包都不存在，开始自动下载...")
        download_script = os.path.join(SCRIPT_DIR, "download_hm_docs.py")
        if os.path.exists(download_script):
            try:
                result = subprocess.run(
                    [sys.executable, download_script],
                    check=True,
                    capture_output=True,
                    text=True,
                    cwd=SCRIPT_DIR
                )
                print("[OK] 本地文档下载完成")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] 下载文档失败: {e}")
                print(f"错误输出: {e.stderr}")
                check_passed = False
        else:
            print(f"[WARNING] 文档下载脚本不存在: {download_script}")
            check_passed = False

    return check_passed


def check_and_init_l1_db():
    """
    检查并初始化 L1 RAG 数据库（仅在 L1 启用时需要）
    """
    check_passed = True

    # ========== chroma_db 处理 ==========
    db_exists = os.path.exists(CHROMA_DB_DIR) and os.listdir(CHROMA_DB_DIR)
    db_zip_exists = os.path.exists(CHROMA_DB_ZIP)

    if db_exists:
        print("[OK] 向量数据库已存在")
    elif db_zip_exists:
        print("[INIT] 检测到数据库压缩包，开始解压...")
        if extract_zip(CHROMA_DB_ZIP, CHROMA_DB_DIR):
            print("[OK] 向量数据库解压完成")
        else:
            print("[ERROR] 数据库解压失败")
            check_passed = False
    else:
        print("[INIT] 向量数据库目录和压缩包都不存在，开始自动构建...")
        db_builder_script = os.path.join(SCRIPT_DIR, "Database-Builder.py")
        if os.path.exists(db_builder_script):
            try:
                result = subprocess.run(
                    [sys.executable, db_builder_script],
                    check=True,
                    capture_output=True,
                    text=True,
                    cwd=SCRIPT_DIR
                )
                print("[OK] 向量数据库构建完成")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] 构建数据库失败: {e}")
                print(f"错误输出: {e.stderr}")
                check_passed = False
        else:
            print(f"[WARNING] 数据库构建脚本不存在: {db_builder_script}")
            check_passed = False

    return check_passed


def check_and_init_evolution():
    """
    检查并初始化 Evolution.md 文件（通用功能）
    """
    if not os.path.exists(EVOLUTION_MD):
        print("[INIT] Evolution.md 不存在，创建中...")
        evolution_template = """# Evolution - 项目重难点记录

## 项目: [项目名称]
### 初始日期: YEAR-MM-DD

## 重难点记录

*(每次构建成功后，将本次开发中遇到的重难点记录在此处)*

### 示例格式

#### 1. [问题描述]
**日期**: MM-DD
**现象**: 错误信息
**原因**: 根本原因分析
**解决方案**: 修复步骤
**正确代码**:
```cangjie
// 正确的代码示例
```

---
"""
        with open(EVOLUTION_MD, "w", encoding="utf-8") as f:
            f.write(evolution_template)
        print("[OK] Evolution.md 已创建")
    else:
        print("[OK] Evolution.md 已存在")


def is_l1_rag_enabled() -> bool:
    """检查是否启用 L1 RAG 功能"""
    # 检查 API Key 是否为默认值或未配置
    api_key = os.environ.get("SILICONFLOW_API_KEY", "").strip()
    
    # 如果是默认值或空值，则跳过 L1
    if not api_key or api_key == "YOUR_API_KEY":
        return False
    
    return True


def main():
    """主函数：处理命令行参数并执行知识库查询"""

    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: python ask_cangjie.py 'query'")
        sys.exit(1)

    # 获取查询字符串
    query = sys.argv[1]

    # 首先检查并初始化本地文档（L3 必需，无论 L1 是否启用都要执行）
    print("[CHECK] 检查本地文档...")
    if not check_and_init_docs():
        print("[ERROR] 本地文档初始化失败，L3 搜索将无法使用")
        print("请手动运行: python download_hm_docs.py")
        # 不退出，继续尝试 L1（如果启用的话）
    
    # 检查并初始化 Evolution.md
    check_and_init_evolution()

    # 检查是否启用 L1 RAG
    vector_enabled = is_l1_rag_enabled()
    if not vector_enabled:
        print("[INFO] 未配置 SILICONFLOW_API_KEY，向量语义检索已禁用")
        print("[INFO] 系统将自动降级为纯 BM25 关键词检索模式...")
    else:
        print("[CHECK] L1 RAG 已启用，检查向量数据库...")
        
    # L1 检查并初始化数据库
    if not check_and_init_l1_db():
        print("[ERROR] L1 数据库初始化失败，请手动运行以下命令：")
        print(f"  cd {SCRIPT_DIR}")
        print("  python Database-Builder.py")
        print("NO_RAG_RESULT")
        return
    print("[OK] L1 数据检查完成\n")

    try:
        # 尝试导入 CangjieRetriever
        from cangjie_retriever import CangjieRetriever

        # 初始化检索器（使用基于 SCRIPT_DIR 的绝对路径）
        retriever = CangjieRetriever(
            chroma_db_dir=CHROMA_DB_DIR,
            bm25_docs_path=os.path.join(CHROMA_DB_DIR, "bm25_documents.pkl")
        )

        # 执行检索并格式化结果
        result = retriever.search_and_format(query, top_k=6)

        # 判断是否找到相关结果
        if not result or result.strip() == "" or "未找到相关知识点" in result:
            print("NO_RAG_RESULT")
        else:
            # 直接输出格式化结果
            print(result)

    except FileNotFoundError as e:
        print(f"Error: 数据库文件不存在 - {e}")
        print("NO_RAG_RESULT")
    except ImportError as e:
        print(f"Error: 导入模块失败 - {e}")
        print("NO_RAG_RESULT")
    except Exception as e:
        print(f"Error: {e}")
        print("NO_RAG_RESULT")


if __name__ == "__main__":
    main()
