#!/usr/bin/env python3
"""
KeywordExtractor - 关键词提取器
从代码元素中提取搜索关键词，支持中文分词和驼峰命名拆分
"""

import re
from typing import List, Set
from cpp_parser import ClassInfo, FunctionInfo

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("警告: jieba 未安装，中文分词功能将不可用")
    print("请运行: pip3 install jieba")


class KeywordExtractor:
    """关键词提取器"""
    
    def __init__(self):
        """初始化关键词提取器"""
        self.jieba_available = JIEBA_AVAILABLE
        
        # 停用词列表（常见的无意义词）
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can',
            'get', 'set', 'make', 'new', 'old', 'this', 'that', 'these', 'those'
        }
    
    def tokenize_chinese(self, text: str) -> List[str]:
        """
        中文分词
        
        Args:
            text: 输入文本
        
        Returns:
            分词结果列表
        """
        if not self.jieba_available:
            # 如果 jieba 不可用，返回原文本
            return [text] if text else []
        
        # 使用 jieba 分词
        words = jieba.cut(text)
        # 过滤空字符串和单字符
        return [w.strip() for w in words if w.strip() and len(w.strip()) > 1]
    
    def split_camel_case(self, name: str) -> List[str]:
        """
        拆分驼峰命名
        
        例如:
        - TypeChecker -> ['type', 'checker', 'check']
        - LambdaExpr -> ['lambda', 'expr']
        - HTTPServer -> ['http', 'server']
        - TypeInference -> ['type', 'inference', 'infer']
        
        Args:
            name: 驼峰命名的字符串
        
        Returns:
            拆分后的单词列表（小写），包括常见词根
        """
        # 处理连续大写字母（如 HTTPServer -> HTTP Server）
        # 在大写字母前插入空格，但连续大写字母视为一个单词
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
        
        # 分割并转小写
        words = s2.split()
        result = [w.lower() for w in words if w]
        
        # 添加常见词根变体（提高搜索召回率）
        extended = []
        for word in result:
            extended.append(word)
            # 添加词根变体（更严格的规则避免产生无效词根）
            if word.endswith('ence') and len(word) > 5:
                # inference -> infer
                extended.append(word[:-4])
            elif word.endswith('ance') and len(word) > 5:
                # instance -> inst
                extended.append(word[:-4])
            elif word.endswith('tion') and len(word) > 5:
                # instantiation -> instantiat
                extended.append(word[:-4])
            elif word.endswith('ing') and len(word) > 5:
                # parsing -> pars (增加最小长度避免短词)
                extended.append(word[:-3])
            elif word.endswith('ed') and len(word) > 4:
                # parsed -> pars (增加最小长度，避免 "inferred" -> "inferr")
                stem = word[:-2]
                # 检查词根是否以双辅音结尾（避免 inferr, referr 等）
                if len(stem) >= 2 and not (stem[-1] == stem[-2] and stem[-1] not in 'aeiou'):
                    extended.append(stem)
            elif word.endswith('er') and len(word) > 4:
                # checker -> check (增加最小长度)
                stem = word[:-2]
                # 检查词根是否以双辅音结尾
                if len(stem) >= 2 and not (stem[-1] == stem[-2] and stem[-1] not in 'aeiou'):
                    extended.append(stem)
            elif word.endswith('or') and len(word) > 4:
                # instantiator -> instantiat (增加最小长度)
                extended.append(word[:-2])
        
        return extended
    
    def extract_english_words(self, text: str) -> List[str]:
        """
        提取英文单词
        
        Args:
            text: 输入文本
        
        Returns:
            英文单词列表（小写，去除停用词）
        """
        # 提取所有英文单词
        words = re.findall(r'[a-zA-Z]+', text)
        
        # 转小写并过滤停用词和短词
        filtered = [
            w.lower() for w in words 
            if w.lower() not in self.stop_words and len(w) > 2
        ]
        
        return filtered
    
    def extract_from_class(self, class_info: ClassInfo) -> List[str]:
        """
        从类名提取关键词
        
        Args:
            class_info: 类信息
        
        Returns:
            关键词列表
        """
        keywords = set()
        
        # 添加完整类名（小写）
        keywords.add(class_info.name.lower())
        
        # 拆分驼峰命名
        camel_words = self.split_camel_case(class_info.name)
        keywords.update(camel_words)
        
        # 如果类名包含中文，进行中文分词
        if self._contains_chinese(class_info.name):
            chinese_words = self.tokenize_chinese(class_info.name)
            keywords.update(chinese_words)
        
        # 提取英文单词
        english_words = self.extract_english_words(class_info.name)
        keywords.update(english_words)
        
        # 添加类型标识
        if class_info.is_struct:
            keywords.add('struct')
        else:
            keywords.add('class')
        
        return list(keywords)
    
    def extract_from_function(self, func_info: FunctionInfo) -> List[str]:
        """
        从函数名提取关键词
        
        Args:
            func_info: 函数信息
        
        Returns:
            关键词列表
        """
        keywords = set()
        
        # 处理命名空间限定名，如 TypeChecker::TypeCheckerImpl::InferTypeOfThis
        # 提取完整名称和各个部分
        func_name = func_info.name
        
        # 添加完整函数名（小写）
        keywords.add(func_name.lower())
        
        # 如果包含命名空间，拆分并提取各部分
        if '::' in func_name:
            parts = func_name.split('::')
            for part in parts:
                if part:
                    keywords.add(part.lower())
                    # 拆分驼峰命名
                    camel_words = self.split_camel_case(part)
                    keywords.update(camel_words)
        else:
            # 拆分驼峰命名
            camel_words = self.split_camel_case(func_name)
            keywords.update(camel_words)
        
        # 如果函数名包含中文，进行中文分词
        if self._contains_chinese(func_name):
            chinese_words = self.tokenize_chinese(func_name)
            keywords.update(chinese_words)
        
        # 提取英文单词
        english_words = self.extract_english_words(func_name)
        keywords.update(english_words)
        
        # 添加函数标识
        keywords.add('function')
        
        return list(keywords)
    
    def extract_from_text(self, text: str) -> List[str]:
        """
        从任意文本提取关键词（通用方法）
        
        Args:
            text: 输入文本
        
        Returns:
            关键词列表
        """
        keywords = set()
        
        # 添加原文本（小写）
        keywords.add(text.lower())
        
        # 拆分驼峰命名
        camel_words = self.split_camel_case(text)
        keywords.update(camel_words)
        
        # 中文分词
        if self._contains_chinese(text):
            chinese_words = self.tokenize_chinese(text)
            keywords.update(chinese_words)
        
        # 提取英文单词
        english_words = self.extract_english_words(text)
        keywords.update(english_words)
        
        return list(keywords)
    
    def _contains_chinese(self, text: str) -> bool:
        """
        检查文本是否包含中文字符
        
        Args:
            text: 输入文本
        
        Returns:
            是否包含中文
        """
        return bool(re.search(r'[\u4e00-\u9fff]', text))


if __name__ == '__main__':
    # 测试代码
    extractor = KeywordExtractor()
    
    print("=== 测试驼峰命名拆分 ===")
    test_names = [
        'TypeChecker',
        'LambdaExpr',
        'HTTPServer',
        'ParseLambda',
        'BuildLambdaClosure'
    ]
    
    for name in test_names:
        words = extractor.split_camel_case(name)
        print(f"{name} -> {words}")
    
    print("\n=== 测试类名关键词提取 ===")
    from cpp_parser import ClassInfo
    
    test_classes = [
        ClassInfo(name='TypeChecker', file='test.cpp', line=10),
        ClassInfo(name='LambdaExpr', file='test.cpp', line=20),
        ClassInfo(name='GenericInstantiator', file='test.cpp', line=30, is_struct=True)
    ]
    
    for cls in test_classes:
        keywords = extractor.extract_from_class(cls)
        print(f"{cls.name} -> {keywords}")
    
    print("\n=== 测试函数名关键词提取 ===")
    from cpp_parser import FunctionInfo
    
    test_functions = [
        FunctionInfo(name='ParseLambda', file='test.cpp', line=100),
        FunctionInfo(name='TypeCheckFunction', file='test.cpp', line=200),
        FunctionInfo(name='BuildDependencyGraph', file='test.cpp', line=300)
    ]
    
    for func in test_functions:
        keywords = extractor.extract_from_function(func)
        print(f"{func.name} -> {keywords}")
    
    if JIEBA_AVAILABLE:
        print("\n=== 测试中文分词 ===")
        chinese_texts = [
            '类型检查器',
            'Lambda表达式',
            '泛型实例化'
        ]
        
        for text in chinese_texts:
            words = extractor.tokenize_chinese(text)
            print(f"{text} -> {words}")
    else:
        print("\n=== 中文分词测试跳过（jieba 未安装）===")
