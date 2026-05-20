#!/usr/bin/env python3
"""
generate_knowledge.py - 知识库生成主脚本
整合所有组件，从编译器源码生成可搜索的知识库
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

# 导入所有组件
from file_scanner import FileScanner
from cpp_parser import CppParser, ParsedFile
from module_analyzer import ModuleAnalyzer, ModuleTree
from dependency_analyzer import DependencyAnalyzer
from keyword_extractor import KeywordExtractor
from markdown_parser import MarkdownParser
from search_index_builder import SearchIndexBuilder, SearchIndex
from cross_ref_builder import CrossRefBuilder


class KnowledgeGenerator:
    """知识库生成器主类"""
    
    def __init__(self, source_dir: str, output_dir: str, verbose: bool = False, parallel: int = 4):
        """
        初始化知识库生成器
        
        Args:
            source_dir: 编译器源码目录
            output_dir: 输出目录
            verbose: 是否显示详细日志
            parallel: 并行处理文件数
        """
        self.source_dir = os.path.abspath(source_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.verbose = verbose
        self.parallel = parallel
        
        # 初始化组件
        self.scanner = FileScanner()
        self.parser = CppParser()
        self.module_analyzer = ModuleAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.keyword_extractor = KeywordExtractor()
        self.markdown_parser = MarkdownParser()
        self.index_builder = SearchIndexBuilder()
        self.cross_ref_builder = CrossRefBuilder()
        
        # 配置日志
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_source_dir(self) -> bool:
        """
        验证源码目录是否存在
        
        Returns:
            True 如果目录存在，否则 False
        """
        if not os.path.exists(self.source_dir):
            self.logger.error(f"错误: 源码目录不存在: {self.source_dir}")
            return False
        
        if not os.path.isdir(self.source_dir):
            self.logger.error(f"错误: 路径不是目录: {self.source_dir}")
            return False
        
        self.logger.info(f"源码目录: {self.source_dir}")
        return True
    
    def scan_files(self, incremental: bool = False, since: datetime = None) -> List[str]:
        """
        扫描源码文件
        
        Args:
            incremental: 是否增量更新
            since: 增量更新的起始时间
        
        Returns:
            文件路径列表
        """
        self.logger.info("扫描源码文件...")
        
        extensions = ['.h', '.cpp']
        
        if incremental and since:
            files = self.scanner.get_modified_files(self.source_dir, extensions, since)
            self.logger.info(f"找到 {len(files)} 个修改过的文件")
        else:
            files = self.scanner.scan(self.source_dir, extensions)
            self.logger.info(f"找到 {len(files)} 个文件")
        
        return files

    
    def parse_files(self, files: List[str]) -> List[ParsedFile]:
        """
        解析源码文件
        
        Args:
            files: 文件路径列表
        
        Returns:
            ParsedFile 列表
        """
        self.logger.info(f"解析 {len(files)} 个文件...")
        
        parsed_files = []
        failed_files = []
        
        if self.parallel > 1:
            # 并行处理
            with ThreadPoolExecutor(max_workers=self.parallel) as executor:
                future_to_file = {
                    executor.submit(self._parse_single_file, file_path): file_path
                    for file_path in files
                }
                
                completed = 0
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        parsed = future.result()
                        if parsed:
                            parsed_files.append(parsed)
                        else:
                            failed_files.append(file_path)
                    except Exception as e:
                        self.logger.warning(f"解析失败: {file_path}: {e}")
                        failed_files.append(file_path)
                    
                    completed += 1
                    if completed % 100 == 0:
                        self.logger.info(f"进度: {completed}/{len(files)}")
        else:
            # 串行处理
            for i, file_path in enumerate(files, 1):
                try:
                    parsed = self._parse_single_file(file_path)
                    if parsed:
                        parsed_files.append(parsed)
                    else:
                        failed_files.append(file_path)
                except Exception as e:
                    self.logger.warning(f"解析失败: {file_path}: {e}")
                    failed_files.append(file_path)
                
                if i % 100 == 0:
                    self.logger.info(f"进度: {i}/{len(files)}")
        
        self.logger.info(f"成功解析 {len(parsed_files)} 个文件")
        if failed_files:
            self.logger.warning(f"解析失败 {len(failed_files)} 个文件")
            if self.verbose:
                for f in failed_files[:10]:
                    self.logger.debug(f"  失败: {f}")
        
        return parsed_files
    
    def _parse_single_file(self, file_path: str) -> ParsedFile:
        """
        解析单个文件
        
        Args:
            file_path: 相对文件路径
        
        Returns:
            ParsedFile 对象或 None
        """
        full_path = os.path.join(self.source_dir, file_path)
        # 传递相对路径，确保所有路径都是相对的
        parsed = self.parser.parse_file(full_path, relative_path=file_path)
        return parsed
    
    def build_module_tree(self, parsed_files: List[ParsedFile]) -> ModuleTree:
        """
        构建模块树
        
        Args:
            parsed_files: 解析后的文件列表
        
        Returns:
            ModuleTree 对象
        """
        self.logger.info("构建模块树...")
        tree = self.module_analyzer.build_module_tree(parsed_files)
        self.logger.info(f"找到 {len(tree.modules)} 个模块")
        return tree
    
    def analyze_dependencies(self, parsed_files: List[ParsedFile], tree: ModuleTree) -> Dict:
        """
        分析依赖关系
        
        Args:
            parsed_files: 解析后的文件列表
            tree: 模块树
        
        Returns:
            依赖关系字典
        """
        self.logger.info("分析模块依赖...")
        module_deps = self.dependency_analyzer.analyze_module_dependencies(tree, parsed_files)
        
        self.logger.info("分析函数调用...")
        function_calls = self.dependency_analyzer.analyze_function_calls(parsed_files)
        
        return {
            'module_dependencies': module_deps,
            'function_calls': function_calls
        }
    
    def load_descriptions(self) -> Dict:
        """
        加载 Markdown 描述文件
        
        Returns:
            描述字典
        """
        descriptions_dir = os.path.join(self.output_dir, 'descriptions')
        
        if not os.path.exists(descriptions_dir):
            self.logger.info("描述目录不存在，跳过加载描述")
            return {}
        
        self.logger.info("加载 Markdown 描述...")
        descriptions = self.markdown_parser.load_all_descriptions(descriptions_dir)
        self.logger.info(f"加载了 {len(descriptions)} 个描述")
        
        return descriptions

    
    def build_search_index(self, tree: ModuleTree, descriptions: Dict) -> SearchIndex:
        """
        构建搜索索引
        
        Args:
            tree: 模块树
            descriptions: 描述字典
        
        Returns:
            SearchIndex 对象
        """
        self.logger.info("构建搜索索引...")
        
        # 设置关键词提取器
        self.index_builder.keyword_extractor = self.keyword_extractor
        
        # 构建索引（传入 descriptions 而不是 keyword_extractor）
        index = self.index_builder.build_index(tree, descriptions)
        
        # 如果没有合并描述，现在合并
        if descriptions:
            index = self.index_builder.merge_descriptions(index, descriptions)
        
        self.logger.info(f"索引包含 {len(index.keywords)} 个关键词")
        
        return index
    
    def build_cross_references(self, dependencies: Dict) -> Dict:
        """
        构建交叉引用
        
        Args:
            dependencies: 依赖关系字典
        
        Returns:
            交叉引用字典
        """
        from dataclasses import asdict
        
        self.logger.info("构建交叉引用...")
        
        module_refs = self.cross_ref_builder.build_module_refs(
            dependencies['module_dependencies']
        )
        
        function_refs = self.cross_ref_builder.build_function_refs(
            dependencies['function_calls']
        )
        
        # 转换为可序列化的字典
        cross_refs = {
            'module_dependencies': {k: asdict(v) for k, v in module_refs.items()},
            'function_calls': {k: asdict(v) for k, v in function_refs.items()}
        }
        
        return cross_refs
    
    def save_outputs(self, index: SearchIndex, cross_refs: Dict, tree: ModuleTree):
        """
        保存输出文件
        
        Args:
            index: 搜索索引（SearchIndex 对象）
            cross_refs: 交叉引用
            tree: 模块树
        """
        self.logger.info("保存输出文件...")
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 保存搜索索引（转换为字典）
        index_path = os.path.join(self.output_dir, 'search-index.json')
        self._save_json(index_path, index.to_dict())
        self.logger.info(f"已保存: {index_path}")
        
        # 保存交叉引用
        cross_ref_path = os.path.join(self.output_dir, 'cross-references.json')
        self._save_json(cross_ref_path, cross_refs)
        self.logger.info(f"已保存: {cross_ref_path}")
        
        # 保存模块数据
        modules_dir = os.path.join(self.output_dir, 'modules')
        os.makedirs(modules_dir, exist_ok=True)
        
        for module in tree.get_all_modules():
            module_data = {
                'name': module.name,
                'path': module.path,
                'files': module.files,
                'classes': [
                    {'name': cls.name, 'file': cls.file, 'line': cls.line}
                    for cls in module.classes
                ],
                'functions': [
                    {'name': func.name, 'file': func.file, 'line': func.line}
                    for func in module.functions
                ],
                'submodules': module.submodules
            }
            
            module_path = os.path.join(modules_dir, f"{module.name}.json")
            self._save_json(module_path, module_data)
        
        self.logger.info(f"已保存 {len(tree.modules)} 个模块文件到: {modules_dir}")
    
    def _save_json(self, path: str, data: Dict):
        """
        保存 JSON 文件
        
        Args:
            path: 文件路径
            data: 数据字典
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存文件失败: {path}: {e}")
            raise
    
    def generate(self, incremental: bool = False):
        """
        执行完整的知识库生成流程
        
        Args:
            incremental: 是否增量更新
        """
        start_time = datetime.now()
        self.logger.info("=" * 60)
        self.logger.info("开始生成知识库")
        self.logger.info("=" * 60)
        
        # 1. 验证源码目录
        if not self.validate_source_dir():
            sys.exit(1)
        
        # 2. 扫描文件
        since = None
        if incremental:
            # 读取上次生成时间
            timestamp_file = os.path.join(self.output_dir, '.last_generated')
            if os.path.exists(timestamp_file):
                try:
                    with open(timestamp_file, 'r') as f:
                        timestamp = float(f.read().strip())
                        since = datetime.fromtimestamp(timestamp)
                        self.logger.info(f"增量更新自: {since}")
                except Exception as e:
                    self.logger.warning(f"读取时间戳失败: {e}，执行完整扫描")
                    incremental = False
        
        files = self.scan_files(incremental, since)
        
        if not files:
            self.logger.info("没有需要处理的文件")
            return
        
        # 3. 解析文件
        parsed_files = self.parse_files(files)
        
        if not parsed_files:
            self.logger.error("没有成功解析的文件")
            sys.exit(1)
        
        # 4. 构建模块树
        tree = self.build_module_tree(parsed_files)
        
        # 5. 分析依赖
        dependencies = self.analyze_dependencies(parsed_files, tree)
        
        # 6. 加载描述
        descriptions = self.load_descriptions()
        
        # 7. 构建搜索索引
        index = self.build_search_index(tree, descriptions)
        
        # 8. 构建交叉引用
        cross_refs = self.build_cross_references(dependencies)
        
        # 9. 保存输出
        self.save_outputs(index, cross_refs, tree)
        
        # 10. 保存时间戳
        timestamp_file = os.path.join(self.output_dir, '.last_generated')
        with open(timestamp_file, 'w') as f:
            f.write(str(datetime.now().timestamp()))
        
        # 完成
        elapsed = datetime.now() - start_time
        self.logger.info("=" * 60)
        self.logger.info(f"知识库生成完成！耗时: {elapsed.total_seconds():.2f} 秒")
        self.logger.info("=" * 60)



def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成仓颉编译器知识库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成完整知识库
  python3 generate_knowledge.py
  
  # 指定源码目录
  python3 generate_knowledge.py --source-dir /path/to/cangjie_compiler
  
  # 增量更新
  python3 generate_knowledge.py --incremental
  
  # 并行处理（8 个线程）
  python3 generate_knowledge.py --parallel 8
  
  # 显示详细日志
  python3 generate_knowledge.py --verbose
        """
    )
    
    parser.add_argument(
        '--source-dir',
        default='../../../cangjie_compiler',
        help='编译器源码目录 (默认: ../../../cangjie_compiler)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='../knowledge-base',
        help='输出目录 (默认: ../knowledge-base)'
    )
    
    parser.add_argument(
        '--incremental',
        action='store_true',
        help='增量更新模式（只处理修改过的文件）'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    parser.add_argument(
        '--parallel',
        type=int,
        default=4,
        help='并行处理文件数 (默认: 4)'
    )
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = KnowledgeGenerator(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        verbose=args.verbose,
        parallel=args.parallel
    )
    
    # 执行生成
    try:
        generator.generate(incremental=args.incremental)
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(130)
    except Exception as e:
        logging.error(f"生成失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
