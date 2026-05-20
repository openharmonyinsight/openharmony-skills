#!/usr/bin/env python3
"""
集成测试 - AI 查询层组件

测试 QueryParser、SearchEngine、ResultRanker、ResultFormatter 的集成
"""

import os
import sys

# 导入组件
from query_parser import QueryParser, ParsedQuery
from search_engine import SearchEngine, SearchResult as EngineSearchResult
from result_ranker import ResultRanker
from result_formatter import ResultFormatter


def test_query_layer():
    """测试查询层集成"""
    print("AI 查询层集成测试")
    print("=" * 80)
    
    # 1. 创建查询解析器
    parser = QueryParser()
    
    # 2. 查找索引文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, '..', 'knowledge-base', 'search-index.json')
    
    if not os.path.exists(index_path):
        print(f"\n错误: 索引文件不存在: {index_path}")
        print("请先运行 generate_knowledge.py 生成知识库")
        return False
    
    # 3. 创建搜索引擎
    try:
        engine = SearchEngine(index_path)
    except Exception as e:
        print(f"\n错误: 加载索引失败: {e}")
        return False
    
    # 4. 创建结果排序器
    ranker = ResultRanker()
    
    # 5. 创建结果格式化器
    formatter = ResultFormatter(output_format='text', language='zh')
    
    # 测试查询
    test_queries = [
        "lambda",
        "类型推断",
        "TypeChecker",
    ]
    
    for query_str in test_queries:
        print(f"\n\n{'=' * 80}")
        print(f"查询: {query_str}")
        print('=' * 80)
        
        # 解析查询
        parsed_query = parser.parse(query_str)
        print(f"\n解析结果:")
        print(f"  语言: {parsed_query.language}")
        print(f"  关键词: {parsed_query.keywords}")
        
        # 搜索
        results = engine.search(parsed_query.keywords, max_results=5, enable_fuzzy=True)
        print(f"\n搜索结果: 找到 {len(results)} 个匹配")
        
        if not results:
            print("  未找到结果")
            continue
        
        # 排序
        ranked_results = ranker.rank(results, parsed_query, max_results=3)
        print(f"\n排序后: 保留前 {len(ranked_results)} 个结果")
        
        # 格式化输出
        print("\n格式化输出:")
        print("-" * 80)
        
        # 获取模块依赖和函数调用信息
        module_deps = {}
        func_calls = {}
        
        for result in ranked_results:
            for module in result.modules:
                deps = engine.get_module_dependencies(module)
                if deps:
                    module_deps[module] = deps
            
            for func in result.functions:
                func_name = func.get('name', '')
                calls = engine.get_function_calls(func_name)
                if calls:
                    func_calls[func_name] = calls
        
        output = formatter.format(ranked_results, module_deps, func_calls)
        print(output)
    
    print("\n\n" + "=" * 80)
    print("集成测试完成！")
    print("=" * 80)
    
    return True


if __name__ == '__main__':
    success = test_query_layer()
    sys.exit(0 if success else 1)
