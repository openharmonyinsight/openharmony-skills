#!/usr/bin/env python3
"""
QueryParser - 查询解析器

职责：解析 AI 助手的查询请求，提取关键词和查询意图
"""

import re
from typing import List, Dict, Any

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("警告: jieba 未安装，中文分词功能将受限")
    print("请运行: pip3 install jieba")


class ParsedQuery:
    """解析后的查询对象"""
    
    def __init__(self, original: str, keywords: List[str], language: str):
        self.original = original  # 原始查询字符串
        self.keywords = keywords  # 提取的关键词列表
        self.language = language  # 查询语言：'zh', 'en', 'mixed'
    
    def __repr__(self):
        return f"ParsedQuery(original='{self.original}', keywords={self.keywords}, language='{self.language}')"


class QueryParser:
    """查询解析器"""
    
    def __init__(self):
        # 英文停用词列表
        self.english_stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
        }
        
        # 中文停用词列表
        self.chinese_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
            '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
            '看', '好', '自己', '这', '那', '里', '什么', '怎么', '哪里', '为什么',
            '如何', '吗', '呢', '吧', '啊', '哦', '嗯'
        }
    
    def parse(self, query: str) -> ParsedQuery:
        """
        解析查询字符串
        
        Args:
            query: 查询字符串
            
        Returns:
            ParsedQuery: 解析后的查询对象
        """
        if not query or not query.strip():
            return ParsedQuery(query, [], 'unknown')
        
        query = query.strip()
        
        # 检测语言
        language = self.detect_language(query)
        
        # 提取关键词
        keywords = self.extract_keywords(query, language)
        
        return ParsedQuery(query, keywords, language)
    
    def extract_keywords(self, query: str, language: str = None) -> List[str]:
        """
        提取查询关键词
        
        Args:
            query: 查询字符串
            language: 语言类型（可选，如果未提供则自动检测）
            
        Returns:
            List[str]: 关键词列表
        """
        if language is None:
            language = self.detect_language(query)
        
        keywords = []
        
        if language == 'zh' or language == 'mixed':
            # 中文分词
            chinese_keywords = self._extract_chinese_keywords(query)
            keywords.extend(chinese_keywords)
        
        if language == 'en' or language == 'mixed':
            # 英文分词
            english_keywords = self._extract_english_keywords(query)
            keywords.extend(english_keywords)
        
        # 去重并保持顺序
        seen = set()
        unique_keywords = []
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower not in seen:
                seen.add(kw_lower)
                unique_keywords.append(kw)
        
        return unique_keywords
    
    def detect_language(self, query: str) -> str:
        """
        检测查询语言
        
        Args:
            query: 查询字符串
            
        Returns:
            str: 'zh' (中文), 'en' (英文), 'mixed' (混合), 'unknown' (未知)
        """
        if not query:
            return 'unknown'
        
        # 统计中文字符和英文字符
        chinese_chars = 0
        english_chars = 0
        
        for char in query:
            if self._is_chinese_char(char):
                chinese_chars += 1
            elif char.isalpha():
                english_chars += 1
        
        total_chars = chinese_chars + english_chars
        
        if total_chars == 0:
            return 'unknown'
        
        chinese_ratio = chinese_chars / total_chars
        english_ratio = english_chars / total_chars
        
        # 判断语言类型
        if chinese_ratio > 0.7:
            return 'zh'
        elif english_ratio > 0.7:
            return 'en'
        elif chinese_ratio > 0.1 and english_ratio > 0.1:
            return 'mixed'
        else:
            return 'unknown'
    
    def _is_chinese_char(self, char: str) -> bool:
        """判断是否为中文字符"""
        return '\u4e00' <= char <= '\u9fff'
    
    def _extract_chinese_keywords(self, text: str) -> List[str]:
        """
        提取中文关键词
        
        对于中文查询,采用双重策略:
        1. 优先保留完整的中文短语作为关键词(用于精确匹配)
        2. 使用 jieba 分词提取词组(仅当词组长度>=2时)
        
        Args:
            text: 文本
            
        Returns:
            List[str]: 中文关键词列表
        """
        keywords = []
        
        # 策略1: 提取完整的中文短语(用于精确匹配) - 优先级最高
        chinese_sequences = re.findall(r'[\u4e00-\u9fff]+', text)
        for seq in chinese_sequences:
            if len(seq) >= 2:  # 至少2个字符
                keywords.append(seq)
        
        # 策略2: 使用 jieba 分词(用于部分匹配) - 仅保留有意义的词组
        if JIEBA_AVAILABLE:
            words = jieba.cut(text)
            for word in words:
                word = word.strip()
                # 过滤停用词、单字符、纯标点
                # 重要: 只保留长度>=2的词，避免单字符匹配导致噪音
                if (word and 
                    len(word) >= 2 and  # 至少2个字符，避免单字匹配
                    word not in self.chinese_stopwords and
                    not word.isspace() and
                    not all(not c.isalnum() for c in word)):
                    keywords.append(word)
        
        return keywords
    
    def _extract_english_keywords(self, text: str) -> List[str]:
        """
        提取英文关键词
        
        Args:
            text: 文本
            
        Returns:
            List[str]: 英文关键词列表
        """
        # 提取英文单词（包括驼峰命名）
        # 匹配连续的字母、数字、下划线
        words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', text)
        
        keywords = []
        for word in words:
            word_lower = word.lower()
            # 过滤停用词和单字符
            if (len(word) > 1 and 
                word_lower not in self.english_stopwords):
                # 处理驼峰命名
                camel_words = self._split_camel_case(word)
                keywords.extend(camel_words)
        
        return keywords
    
    def _split_camel_case(self, word: str) -> List[str]:
        """
        拆分驼峰命名
        
        Args:
            word: 单词
            
        Returns:
            List[str]: 拆分后的单词列表
        """
        # 在大写字母前插入空格
        spaced = re.sub(r'([A-Z])', r' \1', word)
        # 分割并过滤空字符串
        parts = [p.lower() for p in spaced.split() if p]
        
        # 如果没有拆分出多个部分，返回原单词
        if len(parts) <= 1:
            return [word.lower()]
        
        return parts


def main():
    """测试函数"""
    parser = QueryParser()
    
    # 测试用例
    test_queries = [
        "lambda",
        "lambda 在哪实现",
        "TypeChecker 在哪",
        "类型推断",
        "模式匹配穷尽性检查",
        "flow analysis",
        "泛型如何实例化",
        "LambdaExpr class",
        "ParseLambda function",
        "extend 关键字如何实现"
    ]
    
    print("QueryParser 测试\n" + "=" * 60)
    
    for query in test_queries:
        parsed = parser.parse(query)
        print(f"\n查询: {query}")
        print(f"语言: {parsed.language}")
        print(f"关键词: {parsed.keywords}")


if __name__ == '__main__':
    main()
