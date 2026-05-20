#!/usr/bin/env python3
"""
search.py - 搜索主脚本

用途：搜索知识库，供 AI 助手查询编译器实现细节

使用方法：
    python3 search.py <query> [options]

示例：
    python3 search.py "lambda"
    python3 search.py "类型推断" --max-results 5
    python3 search.py "TypeChecker" --json
    python3 search.py "模式匹配" --no-fuzzy
"""

import sys
import os
import argparse
from typing import Optional

# 添加脚本目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from query_parser import QueryParser
from search_engine import SearchEngine
from result_ranker import ResultRanker
from result_formatter import ResultFormatter


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='搜索仓颉编译器知识库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "lambda"                    # 搜索 lambda（默认不包含 unittest）
  %(prog)s "类型推断" --max-results 5   # 限制结果数量
  %(prog)s "TypeChecker" --json        # JSON 格式输出
  %(prog)s "模式匹配" --no-fuzzy        # 禁用模糊匹配
  %(prog)s "flow" --lang en            # 英文输出
  %(prog)s "lambda" --include-unittest # 包含 unittest 结果
        """
    )
    
    parser.add_argument(
        'query',
        help='搜索查询字符串'
    )
    
    parser.add_argument(
        '--index-path',
        default=None,
        help='索引文件路径 (默认: ../knowledge-base/search-index.json)'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=10,
        help='最大结果数 (默认: 10)'
    )
    
    parser.add_argument(
        '--no-fuzzy',
        action='store_true',
        help='禁用模糊匹配'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='输出 JSON 格式'
    )
    
    parser.add_argument(
        '--lang',
        choices=['zh', 'en'],
        default='zh',
        help='输出语言 (默认: zh)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    parser.add_argument(
        '--include-unittest',
        action='store_true',
        help='包含 unittest 相关结果 (默认: 不包含)'
    )
    
    return parser.parse_args()


def find_index_path(custom_path: Optional[str] = None) -> str:
    """
    查找索引文件路径
    
    Args:
        custom_path: 用户指定的路径
        
    Returns:
        str: 索引文件路径
        
    Raises:
        FileNotFoundError: 如果索引文件不存在
    """
    if custom_path:
        if os.path.exists(custom_path):
            return custom_path
        else:
            raise FileNotFoundError(f"索引文件不存在: {custom_path}")
    
    # 默认路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(script_dir, '..', 'knowledge-base', 'search-index.json')
    
    if os.path.exists(default_path):
        return default_path
    
    raise FileNotFoundError(
        f"索引文件不存在: {default_path}\n"
        "请先运行 generate_knowledge.py 生成知识库"
    )


def suggest_similar_keywords(query: str, index: dict, max_suggestions: int = 5) -> list:
    """
    建议相似的关键词
    
    Args:
        query: 查询字符串
        index: 搜索索引
        max_suggestions: 最大建议数
        
    Returns:
        list: 相似关键词列表
    """
    from search_engine import SearchEngine
    
    # 创建临时搜索引擎实例
    temp_engine = SearchEngine()
    temp_engine.index = index
    
    # 获取所有关键词
    all_keywords = list(index.keys())
    
    # 计算编辑距离
    suggestions = []
    for keyword in all_keywords:
        distance = temp_engine._edit_distance(query.lower(), keyword.lower())
        if distance <= 3:  # 编辑距离阈值
            suggestions.append((keyword, distance))
    
    # 按编辑距离排序
    suggestions.sort(key=lambda x: x[1])
    
    # 返回前 N 个建议
    return [kw for kw, _ in suggestions[:max_suggestions]]


def _is_unittest_result(result) -> bool:
    """
    判断搜索结果是否**主要**来自 unittest
    
    只有当结果的**所有**类和函数都来自 unittest 时才返回 True。
    如果结果包含非 unittest 的类或函数,则保留该结果。
    
    Args:
        result: SearchResult 对象
        
    Returns:
        bool: 如果是纯 unittest 结果返回 True
    """
    # 如果没有类和函数,检查模块名
    if not result.classes and not result.functions:
        return 'unittests' in result.modules
    
    # 检查是否有非 unittest 的类
    has_non_unittest_class = False
    for cls in result.classes:
        file_path = cls.get('file', '')
        if 'unittests/' not in file_path and '/unittests/' not in file_path:
            has_non_unittest_class = True
            break
    
    # 检查是否有非 unittest 的函数
    has_non_unittest_func = False
    for func in result.functions:
        file_path = func.get('file', '')
        if 'unittests/' not in file_path and '/unittests/' not in file_path:
            has_non_unittest_func = True
            break
    
    # 只有当所有类和函数都来自 unittest 时才过滤
    return not (has_non_unittest_class or has_non_unittest_func)


def main():
    """主函数"""
    args = parse_arguments()
    
    try:
        # 1. 查找索引文件
        if args.verbose:
            print(f"正在查找索引文件...", file=sys.stderr)
        
        index_path = find_index_path(args.index_path)
        
        if args.verbose:
            print(f"使用索引文件: {index_path}", file=sys.stderr)
        
        # 2. 加载搜索引擎
        if args.verbose:
            print(f"正在加载搜索引擎...", file=sys.stderr)
        
        engine = SearchEngine(index_path)
        
        # 3. 解析查询
        if args.verbose:
            print(f"正在解析查询: {args.query}", file=sys.stderr)
        
        parser = QueryParser()
        parsed_query = parser.parse(args.query)
        
        if args.verbose:
            print(f"检测到语言: {parsed_query.language}", file=sys.stderr)
            print(f"提取的关键词: {parsed_query.keywords}", file=sys.stderr)
        
        if not parsed_query.keywords:
            print("错误: 无法从查询中提取关键词", file=sys.stderr)
            return 1
        
        # 4. 执行搜索
        if args.verbose:
            print(f"正在搜索...", file=sys.stderr)
        
        enable_fuzzy = not args.no_fuzzy
        results = engine.search(
            parsed_query.keywords,
            max_results=args.max_results * 2,  # 获取更多结果用于排序
            enable_fuzzy=enable_fuzzy
        )
        
        # 5. 过滤 unittest 结果（如果未启用）
        if not args.include_unittest:
            if args.verbose:
                print(f"正在过滤 unittest 结果...", file=sys.stderr)
            
            results = [r for r in results if not _is_unittest_result(r)]
        
        # 6. 排序结果
        if args.verbose:
            print(f"正在排序结果...", file=sys.stderr)
        
        ranker = ResultRanker()
        ranked_results = ranker.rank(results, parsed_query, max_results=args.max_results)
        
        # 7. 处理空结果
        if not ranked_results:
            if args.json:
                formatter = ResultFormatter(output_format='json', language=args.lang)
                print(formatter.format([]))
            else:
                print(f"未找到匹配 '{args.query}' 的结果。")
                
                # 建议相似关键词
                suggestions = suggest_similar_keywords(args.query, engine.index)
                if suggestions:
                    print(f"\n您是否要搜索:")
                    for suggestion in suggestions:
                        print(f"  - {suggestion}")
            
            return 0
        
        # 8. 获取交叉引用信息
        module_dependencies = None
        function_calls = None
        
        if engine.cross_references:
            module_dependencies = engine.cross_references.get('module_dependencies', {})
            function_calls = engine.cross_references.get('function_calls', {})
        
        # 9. 格式化输出
        if args.verbose:
            print(f"正在格式化输出...", file=sys.stderr)
        
        output_format = 'json' if args.json else 'text'
        formatter = ResultFormatter(output_format=output_format, language=args.lang)
        
        output = formatter.format(ranked_results, module_dependencies, function_calls)
        print(output)
        
        return 0
    
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        print("\n提示: 请先运行以下命令生成知识库:", file=sys.stderr)
        print("  python3 scripts/generate_knowledge.py", file=sys.stderr)
        return 1
    
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        print("\n提示: 索引文件可能已损坏，请重新生成知识库:", file=sys.stderr)
        print("  python3 scripts/generate_knowledge.py", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
