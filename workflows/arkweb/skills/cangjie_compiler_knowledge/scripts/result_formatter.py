#!/usr/bin/env python3
"""
ResultFormatter - 结果格式化器

职责：将搜索结果格式化为 AI 友好的输出
"""

import json
from typing import List, Dict, Any, Optional


class SearchResult:
    """搜索结果（与 search_engine.py 中的定义保持一致）"""
    def __init__(self, keyword: str, description: str, description_en: str,
                 synonyms: List[str], related: List[str], modules: List[str],
                 classes: List[dict], functions: List[dict], 
                 tfidf_score: float, relevance_score: float, match_type: str):
        self.keyword = keyword
        self.description = description
        self.description_en = description_en
        self.synonyms = synonyms
        self.related = related
        self.modules = modules
        self.classes = classes
        self.functions = functions
        self.tfidf_score = tfidf_score
        self.relevance_score = relevance_score
        self.match_type = match_type


class ResultFormatter:
    """结果格式化器"""
    
    def __init__(self, output_format: str = 'text', language: str = 'zh'):
        """
        初始化格式化器
        
        Args:
            output_format: 输出格式 ('text' 或 'json')
            language: 输出语言 ('zh' 或 'en')
        """
        self.output_format = output_format
        self.language = language
    
    def format(self, results: List[SearchResult], 
               module_dependencies: Optional[Dict[str, Any]] = None,
               function_calls: Optional[Dict[str, Any]] = None) -> str:
        """
        格式化搜索结果
        
        Args:
            results: 搜索结果列表
            module_dependencies: 模块依赖关系（可选）
            function_calls: 函数调用关系（可选）
            
        Returns:
            str: 格式化后的输出
        """
        if not results:
            if self.output_format == 'json':
                return json.dumps({'results': [], 'count': 0}, 
                                ensure_ascii=False, indent=2)
            else:
                return "未找到匹配的结果。"
        
        if self.output_format == 'json':
            return self._format_json(results, module_dependencies, function_calls)
        else:
            return self._format_text(results, module_dependencies, function_calls)
    
    def format_single_result(self, result: SearchResult,
                            module_dependencies: Optional[Dict[str, Any]] = None,
                            function_calls: Optional[Dict[str, Any]] = None) -> str:
        """
        格式化单个结果
        
        Args:
            result: 搜索结果
            module_dependencies: 模块依赖关系（可选）
            function_calls: 函数调用关系（可选）
            
        Returns:
            str: 格式化后的输出
        """
        if self.output_format == 'json':
            return self._format_single_json(result, module_dependencies, function_calls)
        else:
            return self._format_single_text(result, module_dependencies, function_calls)
    
    def _format_text(self, results: List[SearchResult],
                    module_dependencies: Optional[Dict[str, Any]] = None,
                    function_calls: Optional[Dict[str, Any]] = None) -> str:
        """格式化为文本输出"""
        output_lines = []
        
        # 标题
        if self.language == 'zh':
            output_lines.append(f"找到 {len(results)} 个结果：")
        else:
            output_lines.append(f"Found {len(results)} result(s):")
        
        output_lines.append("=" * 80)
        
        # 格式化每个结果
        for i, result in enumerate(results, 1):
            output_lines.append("")
            output_lines.append(f"结果 {i}:" if self.language == 'zh' else f"Result {i}:")
            output_lines.append(
                self._format_single_text(result, module_dependencies, function_calls)
            )
            output_lines.append("-" * 80)
        
        return "\n".join(output_lines)
    
    def _format_single_text(self, result: SearchResult,
                           module_dependencies: Optional[Dict[str, Any]] = None,
                           function_calls: Optional[Dict[str, Any]] = None) -> str:
        """格式化单个结果为文本"""
        lines = []
        
        # 概念名称
        if self.language == 'zh':
            lines.append(f"概念: {result.keyword}")
        else:
            lines.append(f"Concept: {result.keyword}")
        
        # 描述
        description = result.description if self.language == 'zh' else result.description_en
        if description:
            if self.language == 'zh':
                lines.append(f"描述: {description}")
            else:
                lines.append(f"Description: {description}")
        
        # 匹配类型和相关性得分
        if self.language == 'zh':
            lines.append(f"匹配类型: {result.match_type} (相关性: {result.relevance_score:.2f})")
        else:
            lines.append(f"Match Type: {result.match_type} (Relevance: {result.relevance_score:.2f})")
        
        # 同义词
        if result.synonyms:
            if self.language == 'zh':
                lines.append(f"同义词: {', '.join(result.synonyms)}")
            else:
                lines.append(f"Synonyms: {', '.join(result.synonyms)}")
        
        # 相关概念
        if result.related:
            if self.language == 'zh':
                lines.append(f"相关概念: {', '.join(result.related)}")
            else:
                lines.append(f"Related: {', '.join(result.related)}")
        
        # 相关模块
        if result.modules:
            if self.language == 'zh':
                lines.append("\n相关模块:")
            else:
                lines.append("\nRelated Modules:")
            for module in result.modules:
                lines.append(f"  - {module}")
        
        # 相关类
        if result.classes:
            if self.language == 'zh':
                lines.append("\n相关类:")
            else:
                lines.append("\nRelated Classes:")
            for cls in result.classes:
                name = cls.get('name', 'Unknown')
                file_path = cls.get('file', '')
                line = cls.get('line', 0)
                if file_path and line:
                    lines.append(f"  - {name} ({file_path}:{line})")
                else:
                    lines.append(f"  - {name}")
        
        # 相关函数
        if result.functions:
            if self.language == 'zh':
                lines.append("\n相关函数:")
            else:
                lines.append("\nRelated Functions:")
            for func in result.functions:
                name = func.get('name', 'Unknown')
                file_path = func.get('file', '')
                line = func.get('line', 0)
                if file_path and line:
                    lines.append(f"  - {name} ({file_path}:{line})")
                else:
                    lines.append(f"  - {name}")
        
        # 模块依赖关系
        if module_dependencies and result.modules:
            if self.language == 'zh':
                lines.append("\n模块依赖:")
            else:
                lines.append("\nModule Dependencies:")
            
            for module in result.modules:
                deps = module_dependencies.get(module)
                if deps:
                    depends_on = deps.get('depends_on', [])
                    depended_by = deps.get('depended_by', [])
                    
                    if depends_on:
                        if self.language == 'zh':
                            lines.append(f"  {module} 依赖: {', '.join(depends_on)}")
                        else:
                            lines.append(f"  {module} depends on: {', '.join(depends_on)}")
                    
                    if depended_by:
                        if self.language == 'zh':
                            lines.append(f"  {module} 被依赖: {', '.join(depended_by)}")
                        else:
                            lines.append(f"  {module} depended by: {', '.join(depended_by)}")
        
        # 函数调用链路
        if function_calls and result.functions:
            if self.language == 'zh':
                lines.append("\n调用链路:")
            else:
                lines.append("\nCall Chain:")
            
            for func in result.functions:
                func_name = func.get('name', '')
                calls = function_calls.get(func_name)
                if calls:
                    calls_list = calls.get('calls', [])
                    called_by = calls.get('called_by', [])
                    
                    if calls_list:
                        if self.language == 'zh':
                            lines.append(f"  {func_name} 调用: {', '.join(calls_list[:5])}")
                        else:
                            lines.append(f"  {func_name} calls: {', '.join(calls_list[:5])}")
                    
                    if called_by:
                        if self.language == 'zh':
                            lines.append(f"  {func_name} 被调用: {', '.join(called_by[:5])}")
                        else:
                            lines.append(f"  {func_name} called by: {', '.join(called_by[:5])}")
        
        return "\n".join(lines)
    
    def _format_json(self, results: List[SearchResult],
                    module_dependencies: Optional[Dict[str, Any]] = None,
                    function_calls: Optional[Dict[str, Any]] = None) -> str:
        """格式化为 JSON 输出"""
        output = {
            'count': len(results),
            'results': []
        }
        
        for result in results:
            result_dict = self._result_to_dict(result, module_dependencies, function_calls)
            output['results'].append(result_dict)
        
        return json.dumps(output, ensure_ascii=False, indent=2)
    
    def _format_single_json(self, result: SearchResult,
                           module_dependencies: Optional[Dict[str, Any]] = None,
                           function_calls: Optional[Dict[str, Any]] = None) -> str:
        """格式化单个结果为 JSON"""
        result_dict = self._result_to_dict(result, module_dependencies, function_calls)
        return json.dumps(result_dict, ensure_ascii=False, indent=2)
    
    def _result_to_dict(self, result: SearchResult,
                       module_dependencies: Optional[Dict[str, Any]] = None,
                       function_calls: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """将搜索结果转换为字典"""
        result_dict = {
            'keyword': result.keyword,
            'description': result.description,
            'description_en': result.description_en,
            'match_type': result.match_type,
            'relevance_score': round(result.relevance_score, 3),
            'tfidf_score': round(result.tfidf_score, 3),
            'synonyms': result.synonyms,
            'related': result.related,
            'modules': result.modules,
            'classes': result.classes,
            'functions': result.functions
        }
        
        # 添加模块依赖
        if module_dependencies and result.modules:
            result_dict['module_dependencies'] = {}
            for module in result.modules:
                deps = module_dependencies.get(module)
                if deps:
                    result_dict['module_dependencies'][module] = deps
        
        # 添加函数调用
        if function_calls and result.functions:
            result_dict['function_calls'] = {}
            for func in result.functions:
                func_name = func.get('name', '')
                calls = function_calls.get(func_name)
                if calls:
                    result_dict['function_calls'][func_name] = calls
        
        return result_dict


def main():
    """测试函数"""
    # 创建测试数据
    test_result = SearchResult(
        keyword='lambda',
        description='Lambda 表达式的解析和语义分析',
        description_en='Parsing and semantic analysis of lambda expressions',
        synonyms=['匿名函数', 'anonymous function', 'closure'],
        related=['function', 'closure', 'capture'],
        modules=['parse', 'sema'],
        classes=[
            {'name': 'LambdaExpr', 'file': 'src/Parse/Lambda.h', 'line': 45},
            {'name': 'LambdaAnalyzer', 'file': 'src/Sema/Lambda.h', 'line': 23}
        ],
        functions=[
            {'name': 'BuildLambdaClosure', 'file': 'src/Sema/Lambda.cpp', 'line': 156},
            {'name': 'TypeCheckLambda', 'file': 'src/Sema/Lambda.cpp', 'line': 234}
        ],
        tfidf_score=0.85,
        relevance_score=0.92,
        match_type='exact'
    )
    
    # 模拟模块依赖
    module_deps = {
        'parse': {
            'depends_on': ['basic', 'lex'],
            'depended_by': ['sema', 'frontend']
        },
        'sema': {
            'depends_on': ['parse', 'ast'],
            'depended_by': ['chir', 'codegen']
        }
    }
    
    # 模拟函数调用
    func_calls = {
        'TypeCheckLambda': {
            'calls': ['BuildLambdaClosure', 'InferType', 'CheckCapture'],
            'called_by': ['TypeCheckExpr', 'AnalyzeFunction']
        }
    }
    
    print("ResultFormatter 测试\n" + "=" * 80)
    
    # 测试文本格式（中文）
    print("\n1. 文本格式（中文）:")
    print("-" * 80)
    formatter_zh = ResultFormatter(output_format='text', language='zh')
    output = formatter_zh.format([test_result], module_deps, func_calls)
    print(output)
    
    # 测试文本格式（英文）
    print("\n\n2. 文本格式（英文）:")
    print("-" * 80)
    formatter_en = ResultFormatter(output_format='text', language='en')
    output = formatter_en.format([test_result], module_deps, func_calls)
    print(output)
    
    # 测试 JSON 格式
    print("\n\n3. JSON 格式:")
    print("-" * 80)
    formatter_json = ResultFormatter(output_format='json', language='zh')
    output = formatter_json.format([test_result], module_deps, func_calls)
    print(output)


if __name__ == '__main__':
    main()
