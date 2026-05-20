#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鸿蒙开发文档下载脚本
从 GitCode 仓库下载文档并按树形结构组织到 hm-docs 文件夹
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download_hm_docs.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 文档源配置
DOC_SOURCES = {
    "UI开发和鸿蒙应用 (最高优先级)": {
        "仓库": "https://gitcode.com/openharmony-sig/docs_cangjie.git",
        "分支": "master",  # 如果报错尝试 "main"
        "路径": "zh-cn/application-dev",
        "适用": "所有UI组件、界面开发、用户交互相关问题",
        "本地目录": "hm-docs/ui-dev"
    },
    
    "标准扩展库 (UI组件补充)": {
        "仓库": "https://gitcode.com/Cangjie/cangjie_stdx.git", 
        "分支": "release/1.0",
        "路径": "doc",
        "适用": "高级UI组件、扩展功能",
        "本地目录": "hm-docs/stdx"
    },
    
    "语法和语言特性": {
        "仓库": "https://gitcode.com/Cangjie/cangjie_docs.git",
        "分支": "release/1.0", 
        "路径": "docs/dev-guide",
        "适用": "语法问题、语言特性",
        "本地目录": "hm-docs/syntax"
    },
    
    "标准库API": {
        "仓库": "https://gitcode.com/Cangjie/cangjie_runtime.git",
        "分支": "release/1.0",
        "路径": "std/doc/libs",
        "适用": "基础数据结构、算法",
        "本地目录": "hm-docs/stdlib"
    },
    
    "命令行工具和构建": {
        "仓库": "https://gitcode.com/Cangjie/cangjie_docs.git",
        "分支": "release/1.0",
        "路径": "docs/tools",
        "适用": "构建、打包、工具链问题",
        "本地目录": "hm-docs/tools"
    }
}

class HMDocsDownloader:
    def __init__(self, base_dir: str = ".", temp_dir: str = "temp_repos"):
        self.base_dir = Path(base_dir)
        self.temp_dir = Path(temp_dir)
        self.hm_docs_dir = self.base_dir / "hm-docs"
        
    def setup_directories(self):
        """创建必要的目录结构"""
        logger.info("设置目录结构...")
        
        # 创建临时目录
        self.temp_dir.mkdir(exist_ok=True)
        
        # 创建 hm-docs 目录
        self.hm_docs_dir.mkdir(exist_ok=True)
        
        # 创建 README
        readme_content = """# HarmonyOS 仓颉开发文档

这是从官方仓库下载的鸿蒙仓颉开发文档的本地副本。

## 文档结构

- `ui-dev/` - UI开发和鸿蒙应用开发 (最高优先级)
- `stdx/` - 标准扩展库 (UI组件补充)  
- `syntax/` - 语法和语言特性
- `stdlib/` - 标准库API
- `tools/` - 命令行工具和构建

## 更新文档

运行 `python download_hm_docs.py` 来更新文档。

## 最后更新

由 download_hm_docs.py 脚本自动生成和更新。
"""
        
        readme_path = self.hm_docs_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        logger.info(f"目录结构已设置: {self.hm_docs_dir}")

    def check_git_available(self) -> bool:
        """检查 Git 是否可用"""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True, check=True)
            logger.info(f"Git 可用: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Git 不可用，请安装 Git")
            return False

    def clone_or_update_repo(self, repo_url: str, branch: str, repo_name: str) -> Optional[Path]:
        """克隆或更新仓库"""
        repo_path = self.temp_dir / repo_name
        
        try:
            if repo_path.exists():
                logger.info(f"更新现有仓库: {repo_name}")
                # 切换到仓库目录并拉取最新代码
                subprocess.run(['git', 'fetch', 'origin'], 
                             cwd=repo_path, check=True, capture_output=True)
                subprocess.run(['git', 'checkout', branch], 
                             cwd=repo_path, check=True, capture_output=True)
                subprocess.run(['git', 'pull', 'origin', branch], 
                             cwd=repo_path, check=True, capture_output=True)
            else:
                logger.info(f"克隆新仓库: {repo_name}")
                subprocess.run(['git', 'clone', '-b', branch, repo_url, str(repo_path)], 
                             check=True, capture_output=True)
            
            return repo_path
            
        except subprocess.CalledProcessError as e:
            # 尝试使用 main 分支
            if branch == "master":
                logger.warning(f"master 分支失败，尝试 main 分支: {repo_name}")
                try:
                    if repo_path.exists():
                        shutil.rmtree(repo_path)
                    subprocess.run(['git', 'clone', '-b', 'main', repo_url, str(repo_path)], 
                                 check=True, capture_output=True)
                    return repo_path
                except subprocess.CalledProcessError:
                    pass
            
            logger.error(f"无法克隆/更新仓库 {repo_name}: {e}")
            return None

    def copy_docs(self, repo_path: Path, source_path: str, target_dir: str) -> bool:
        """复制文档文件到目标目录"""
        source_full_path = repo_path / source_path
        target_full_path = self.hm_docs_dir / target_dir
        
        if not source_full_path.exists():
            logger.error(f"源路径不存在: {source_full_path}")
            return False
        
        try:
            # 如果目标目录存在，先删除
            if target_full_path.exists():
                shutil.rmtree(target_full_path)
            
            # 复制文档
            shutil.copytree(source_full_path, target_full_path)
            
            # 统计文件数量
            file_count = sum(1 for _ in target_full_path.rglob('*') if _.is_file())
            logger.info(f"已复制 {file_count} 个文件到: {target_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"复制文档失败 {source_path} -> {target_dir}: {e}")
            return False

    def generate_index(self):
        """生成文档索引"""
        logger.info("生成文档索引...")
        
        index_data = {
            "生成时间": str(Path().resolve()),
            "文档源": {},
            "文件统计": {}
        }
        
        for name, config in DOC_SOURCES.items():
            target_dir = Path(config["本地目录"]).name
            target_path = self.hm_docs_dir / target_dir
            
            if target_path.exists():
                file_count = sum(1 for _ in target_path.rglob('*') if _.is_file())
                md_count = sum(1 for _ in target_path.rglob('*.md'))
                
                index_data["文档源"][name] = {
                    "仓库": config["仓库"],
                    "分支": config["分支"],
                    "源路径": config["路径"],
                    "本地路径": config["本地目录"],
                    "适用范围": config["适用"]
                }
                
                index_data["文件统计"][target_dir] = {
                    "总文件数": file_count,
                    "Markdown文件数": md_count
                }
        
        # 保存索引文件
        index_path = self.hm_docs_dir / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"索引文件已生成: {index_path}")

    def cleanup_temp(self):
        """清理临时文件"""
        if self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
                logger.info("临时文件已清理")
            except Exception as e:
                logger.warning(f"清理临时文件失败: {e}")

    def download_all_docs(self, sources: Optional[List[str]] = None):
        """下载所有文档"""
        if not self.check_git_available():
            return False
        
        self.setup_directories()
        
        success_count = 0
        total_count = len(DOC_SOURCES)
        
        # 如果指定了特定源，只下载那些
        sources_to_download = DOC_SOURCES
        if sources:
            # 支持模糊匹配
            matched_sources = {}
            for source_name in sources:
                for k, v in DOC_SOURCES.items():
                    if source_name in k or k in source_name:
                        matched_sources[k] = v
                        break
            sources_to_download = matched_sources if matched_sources else DOC_SOURCES
            total_count = len(sources_to_download)
        
        logger.info(f"开始下载 {total_count} 个文档源...")
        
        for name, config in sources_to_download.items():
            logger.info(f"\n处理文档源: {name}")
            
            # 生成仓库名称
            repo_name = config["仓库"].split('/')[-1].replace('.git', '')
            
            # 克隆或更新仓库
            repo_path = self.clone_or_update_repo(
                config["仓库"], 
                config["分支"], 
                repo_name
            )
            
            if repo_path:
                # 复制文档
                target_dir = Path(config["本地目录"]).name
                if self.copy_docs(repo_path, config["路径"], target_dir):
                    success_count += 1
        
        # 生成索引
        self.generate_index()
        
        # 清理临时文件
        self.cleanup_temp()
        
        logger.info(f"\n下载完成! 成功: {success_count}/{total_count}")
        logger.info(f"文档位置: {self.hm_docs_dir.absolute()}")
        
        return success_count == total_count

def main():
    parser = argparse.ArgumentParser(description="下载鸿蒙仓颉开发文档")
    parser.add_argument('--sources', nargs='*', 
                       help='指定要下载的文档源 (默认下载所有)')
    parser.add_argument('--list-sources', action='store_true',
                       help='列出所有可用的文档源')
    parser.add_argument('--base-dir', default='.',
                       help='基础目录 (默认: 当前目录)')
    
    args = parser.parse_args()
    
    if args.list_sources:
        print("\n可用的文档源:")
        for i, (name, config) in enumerate(DOC_SOURCES.items(), 1):
            print(f"{i}. {name}")
            print(f"   仓库: {config['仓库']}")
            print(f"   适用: {config['适用']}")
            print()
        return
    
    downloader = HMDocsDownloader(base_dir=args.base_dir)
    
    try:
        success = downloader.download_all_docs(args.sources)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n用户取消下载")
        downloader.cleanup_temp()
        sys.exit(1)
    except Exception as e:
        logger.error(f"下载过程中出现错误: {e}")
        downloader.cleanup_temp()
        sys.exit(1)

if __name__ == "__main__":
    main()