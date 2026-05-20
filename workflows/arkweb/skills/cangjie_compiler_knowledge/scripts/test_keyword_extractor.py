#!/usr/bin/env python3
"""
测试 KeywordExtractor 的功能
"""

from keyword_extractor import KeywordExtractor
from cpp_parser import ClassInfo, FunctionInfo


def test_camel_case_splitting():
    """测试驼峰命名拆分"""
    print("=== 测试驼峰命名拆分 ===")
    extractor = KeywordExtractor()
    
    test_cases = [
        ('TypeChecker', ['type', 'checker']),
        ('LambdaExpr', ['lambda', 'expr']),
        ('HTTPServer', ['http', 'server']),
        ('ParseLambda', ['parse', 'lambda']),
        ('BuildLambdaClosure', ['build', 'lambda', 'closure']),
        ('GenericInstantiator', ['generic', 'instantiator']),
        ('AST', ['ast']),
        ('ASTNode', ['ast', 'node']),
    ]
    
    passed = 0
    failed = 0
    
    for name, expected in test_cases:
        result = extractor.split_camel_case(name)
        if result == expected:
            print(f"✓ {name} -> {result}")
            passed += 1
        else:
            print(f"✗ {name} -> {result} (期望: {expected})")
            failed += 1
    
    print(f"\n通过: {passed}/{len(test_cases)}")
    return failed == 0


def test_class_keyword_extraction():
    """测试类名关键词提取"""
    print("\n=== 测试类名关键词提取 ===")
    extractor = KeywordExtractor()
    
    test_classes = [
        ClassInfo(name='TypeChecker', file='test.cpp', line=10),
        ClassInfo(name='LambdaExpr', file='test.cpp', line=20),
        ClassInfo(name='GenericInstantiator', file='test.cpp', line=30, is_struct=True),
        ClassInfo(name='ModuleAnalyzer', file='test.cpp', line=40),
    ]
    
    for cls in test_classes:
        keywords = extractor.extract_from_class(cls)
        print(f"{cls.name} -> {sorted(keywords)}")
        
        # 验证必须包含的关键词
        assert cls.name.lower() in keywords, f"应包含完整类名: {cls.name.lower()}"
        if cls.is_struct:
            assert 'struct' in keywords, "struct 类应包含 'struct' 关键词"
        else:
            assert 'class' in keywords, "class 类应包含 'class' 关键词"
    
    print("✓ 所有测试通过")
    return True


def test_function_keyword_extraction():
    """测试函数名关键词提取"""
    print("\n=== 测试函数名关键词提取 ===")
    extractor = KeywordExtractor()
    
    test_functions = [
        FunctionInfo(name='ParseLambda', file='test.cpp', line=100),
        FunctionInfo(name='TypeCheckFunction', file='test.cpp', line=200),
        FunctionInfo(name='BuildDependencyGraph', file='test.cpp', line=300),
        FunctionInfo(name='InferModule', file='test.cpp', line=400),
    ]
    
    for func in test_functions:
        keywords = extractor.extract_from_function(func)
        print(f"{func.name} -> {sorted(keywords)}")
        
        # 验证必须包含的关键词
        assert func.name.lower() in keywords, f"应包含完整函数名: {func.name.lower()}"
        assert 'function' in keywords, "函数应包含 'function' 关键词"
    
    print("✓ 所有测试通过")
    return True


def test_english_word_extraction():
    """测试英文单词提取"""
    print("\n=== 测试英文单词提取 ===")
    extractor = KeywordExtractor()
    
    test_cases = [
        ('TypeChecker', ['typechecker']),  # 提取完整单词
        ('parse_lambda_expression', ['parse', 'lambda', 'expression']),
        ('HTTP_SERVER_PORT', ['http', 'server', 'port']),
    ]
    
    for text, expected_words in test_cases:
        words = extractor.extract_english_words(text)
        print(f"{text} -> {words}")
        
        # 验证期望的单词都被提取出来
        for word in expected_words:
            assert word in words, f"应包含单词: {word}"
    
    print("✓ 所有测试通过")
    return True


def test_chinese_tokenization():
    """测试中文分词"""
    print("\n=== 测试中文分词 ===")
    extractor = KeywordExtractor()
    
    if not extractor.jieba_available:
        print("⚠ jieba 未安装，跳过中文分词测试")
        return True
    
    test_texts = [
        '类型检查器',
        'Lambda表达式',
        '泛型实例化',
        '模块分析器',
    ]
    
    for text in test_texts:
        words = extractor.tokenize_chinese(text)
        print(f"{text} -> {words}")
        assert len(words) > 0, f"应该能分词: {text}"
    
    print("✓ 所有测试通过")
    return True


def test_text_keyword_extraction():
    """测试通用文本关键词提取"""
    print("\n=== 测试通用文本关键词提取 ===")
    extractor = KeywordExtractor()
    
    test_texts = [
        'lambda',
        'TypeChecker',
        'parse_function',
        'generic_instantiation',
    ]
    
    for text in test_texts:
        keywords = extractor.extract_from_text(text)
        print(f"{text} -> {sorted(keywords)}")
        assert len(keywords) > 0, f"应该能提取关键词: {text}"
    
    print("✓ 所有测试通过")
    return True


def main():
    """运行所有测试"""
    print("开始测试 KeywordExtractor\n")
    
    tests = [
        test_camel_case_splitting,
        test_class_keyword_extraction,
        test_function_keyword_extraction,
        test_english_word_extraction,
        test_chinese_tokenization,
        test_text_keyword_extraction,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"✗ 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ 测试出错: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
