#!/usr/bin/env python3
"""
ResultRanker - 结果排序器

职责：对搜索结果进行排序和过滤
"""

from typing import List
from dataclasses import dataclass


@dataclass
class SearchResult:
    """搜索结果（与 search_engine.py 中的定义保持一致）"""
    keyword: str
    description: str
    description_en: str
    synonyms: List[str]
    related: List[str]
    modules: List[str]
    classes: List[dict]
    functions: List[dict]
    tfidf_score: float
    relevance_score: float
    match_type: str


class ParsedQuery:
    """解析后的查询（与 query_parser.py 中的定义保持一致）"""
    def __init__(self, original: str, keywords: List[str], language: str):
        self.original = original
        self.keywords = keywords
        self.language = language


class ResultRanker:
    """结果排序器"""
    
    def __init__(self):
        # 匹配类型权重
        self.match_type_weights = {
            'exact': 1.0,      # 精确匹配权重最高
            'synonym': 0.9,    # 同义词匹配次之
            'fuzzy': 0.7       # 模糊匹配权重较低
        }
    
    def rank(self, results: List[SearchResult], query: ParsedQuery, 
             max_results: int = 10) -> List[SearchResult]:
        """
        对结果排序
        
        Args:
            results: 搜索结果列表
            query: 解析后的查询
            max_results: 最大结果数
            
        Returns:
            List[SearchResult]: 排序后的结果列表
        """
        if not results:
            return []
        
        # 去重：移除指向相同内容的重复结果
        unique_results = self._deduplicate_results(results)
        
        # 重新计算相关性得分
        for result in unique_results:
            result.relevance_score = self.calculate_relevance(result, query)
        
        # 按相关性得分排序（降序）
        sorted_results = sorted(unique_results, key=lambda r: r.relevance_score, reverse=True)
        
        # 限制结果数量
        return sorted_results[:max_results]
    
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        去除重复结果
        
        如果两个结果有相同的模块、类和函数，则认为是重复的，
        保留匹配类型更好的那个（exact > synonym > fuzzy）
        
        Args:
            results: 搜索结果列表
            
        Returns:
            List[SearchResult]: 去重后的结果列表
        """
        if not results:
            return []
        
        # 创建内容指纹 -> 结果的映射
        fingerprint_to_result = {}
        
        for result in results:
            # 生成内容指纹（基于模块、类、函数）
            fingerprint = self._generate_fingerprint(result)
            
            # 如果这个指纹已存在，比较匹配类型
            if fingerprint in fingerprint_to_result:
                existing = fingerprint_to_result[fingerprint]
                # 保留匹配类型更好的结果
                if self._is_better_match(result, existing):
                    fingerprint_to_result[fingerprint] = result
            else:
                fingerprint_to_result[fingerprint] = result
        
        return list(fingerprint_to_result.values())
    
    def _generate_fingerprint(self, result: SearchResult) -> str:
        """
        生成结果的内容指纹
        
        基于模块、类、函数生成唯一标识
        
        Args:
            result: 搜索结果
            
        Returns:
            str: 内容指纹
        """
        # 提取类名和文件路径
        class_signatures = []
        for cls in result.classes:
            sig = f"{cls.get('name', '')}@{cls.get('file', '')}"
            class_signatures.append(sig)
        
        # 提取函数名和文件路径
        func_signatures = []
        for func in result.functions:
            sig = f"{func.get('name', '')}@{func.get('file', '')}"
            func_signatures.append(sig)
        
        # 组合成指纹
        fingerprint = '|'.join([
            ','.join(sorted(result.modules)),
            ','.join(sorted(class_signatures)),
            ','.join(sorted(func_signatures))
        ])
        
        return fingerprint
    
    def _is_better_match(self, result1: SearchResult, result2: SearchResult) -> bool:
        """
        判断 result1 是否比 result2 更好
        
        匹配类型优先级：exact > synonym > fuzzy
        
        Args:
            result1: 第一个结果
            result2: 第二个结果
            
        Returns:
            bool: 如果 result1 更好返回 True
        """
        type_priority = {'exact': 3, 'synonym': 2, 'fuzzy': 1}
        
        priority1 = type_priority.get(result1.match_type, 0)
        priority2 = type_priority.get(result2.match_type, 0)
        
        return priority1 > priority2
    
    def calculate_relevance(self, result: SearchResult, query: ParsedQuery) -> float:
        """
        计算相关性得分
        
        综合考虑：
        1. 匹配类型（精确匹配 > 同义词匹配 > 模糊匹配）- 权重 0.4
        2. 关键词完整匹配度（优先完整短语匹配）- 权重 0.3
        3. TF-IDF 得分 - 权重 0.2
        4. 内容丰富度（有多少相关模块、类、函数）- 权重 0.1
        
        Args:
            result: 搜索结果
            query: 解析后的查询
            
        Returns:
            float: 相关性得分（0-1之间）
        """
        # 1. 匹配类型得分（权重：0.4，提高精确匹配的权重）
        match_type_score = self.match_type_weights.get(result.match_type, 0.5)
        
        # 2. 关键词完整匹配度（权重：0.3，新增完整短语匹配检查）
        keyword_match_score = self._calculate_keyword_match(result, query)
        
        # 3. TF-IDF 得分（权重：0.2，降低权重）
        tfidf_score = result.tfidf_score
        
        # 4. 内容丰富度（权重：0.1，降低权重）
        richness_score = self._calculate_richness(result)
        
        # 综合得分
        relevance = (
            0.4 * match_type_score +
            0.3 * keyword_match_score +
            0.2 * tfidf_score +
            0.1 * richness_score
        )
        
        return min(1.0, max(0.0, relevance))
    
    def _calculate_keyword_match(self, result: SearchResult, query: ParsedQuery) -> float:
        """
        计算关键词匹配度
        
        优先考虑完整短语匹配，然后是部分匹配
        
        Args:
            result: 搜索结果
            query: 解析后的查询
            
        Returns:
            float: 关键词匹配得分（0-1之间）
        """
        if not query.keywords:
            return 0.5
        
        # 构建搜索文本（小写）
        search_text = ' '.join([
            result.keyword.lower(),
            result.description.lower(),
            result.description_en.lower(),
            ' '.join(result.synonyms).lower(),
            ' '.join(result.related).lower()
        ])
        
        # 检查是否有完整短语匹配（最高优先级）
        # 找出查询中最长的关键词（通常是完整短语）
        longest_keyword = max(query.keywords, key=len) if query.keywords else ""
        
        if longest_keyword and len(longest_keyword) >= 2:
            # 检查完整短语是否在结果的关键词或描述中
            if longest_keyword.lower() == result.keyword.lower():
                # 关键词完全匹配，最高分
                return 1.0
            elif longest_keyword.lower() in result.keyword.lower():
                # 关键词包含查询短语，高分
                return 0.9
            elif longest_keyword.lower() in search_text:
                # 描述中包含完整短语，中高分
                return 0.8
        
        # 计算部分匹配的关键词数量
        matched_count = 0
        for keyword in query.keywords:
            if keyword.lower() in search_text:
                matched_count += 1
        
        # 匹配比例
        match_ratio = matched_count / len(query.keywords)
        
        # 部分匹配得分范围：0.3-0.7
        return 0.3 + 0.4 * match_ratio
    
    def _calculate_richness(self, result: SearchResult) -> float:
        """
        计算内容丰富度
        
        有更多相关模块、类、函数的结果被认为更有价值
        
        Args:
            result: 搜索结果
            
        Returns:
            float: 内容丰富度得分（0-1之间）
        """
        # 统计内容数量
        module_count = len(result.modules)
        class_count = len(result.classes)
        function_count = len(result.functions)
        
        # 计算得分（使用对数缩放，避免数量过大时得分过高）
        import math
        
        # 每种内容类型的权重
        module_score = min(1.0, math.log1p(module_count) / math.log1p(10))
        class_score = min(1.0, math.log1p(class_count) / math.log1p(20))
        function_score = min(1.0, math.log1p(function_count) / math.log1p(30))
        
        # 综合得分
        richness = (module_score + class_score + function_score) / 3.0
        
        return richness


def main():
    """测试函数"""
    from query_parser import QueryParser
    
    # 创建测试数据
    test_results = [
        SearchResult(
            keyword='lambda',
            description='Lambda 表达式的解析和语义分析',
            description_en='Parsing and semantic analysis of lambda expressions',
            synonyms=['匿名函数', 'anonymous function'],
            related=['function', 'closure'],
            modules=['parse', 'sema'],
            classes=[
                {'name': 'LambdaExpr', 'file': 'src/Parse/Lambda.h', 'line': 45},
                {'name': 'LambdaAnalyzer', 'file': 'src/Sema/Lambda.h', 'line': 23}
            ],
            functions=[
                {'name': 'ParseLambda', 'file': 'src/Parse/Lambda.cpp', 'line': 156},
                {'name': 'TypeCheckLambda', 'file': 'src/Sema/Lambda.cpp', 'line': 234}
            ],
            tfidf_score=0.85,
            relevance_score=0.0,  # 将被重新计算
            match_type='exact'
        ),
        SearchResult(
            keyword='function',
            description='函数定义和调用',
            description_en='Function definition and invocation',
            synonyms=['func', '函数'],
            related=['lambda', 'method'],
            modules=['parse', 'sema'],
            classes=[
                {'name': 'FuncDecl', 'file': 'src/Parse/Decl.h', 'line': 100}
            ],
            functions=[
                {'name': 'ParseFunc', 'file': 'src/Parse/Decl.cpp', 'line': 200}
            ],
            tfidf_score=0.75,
            relevance_score=0.0,
            match_type='fuzzy'
        )
    ]
    
    # 创建查询
    parser = QueryParser()
    query = parser.parse("lambda 表达式")
    
    # 创建排序器
    ranker = ResultRanker()
    
    print("ResultRanker 测试\n" + "=" * 60)
    print(f"\n查询: {query.original}")
    print(f"关键词: {query.keywords}")
    
    # 排序结果
    ranked_results = ranker.rank(test_results, query, max_results=10)
    
    print(f"\n排序后的结果:")
    for i, result in enumerate(ranked_results, 1):
        print(f"\n{i}. {result.keyword}")
        print(f"   匹配类型: {result.match_type}")
        print(f"   相关性得分: {result.relevance_score:.3f}")
        print(f"   TF-IDF: {result.tfidf_score:.3f}")
        print(f"   描述: {result.description}")


if __name__ == '__main__':
    main()
