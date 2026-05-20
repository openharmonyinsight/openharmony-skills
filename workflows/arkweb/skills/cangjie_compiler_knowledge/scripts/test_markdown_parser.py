#!/usr/bin/env python3
"""
测试 MarkdownParser 的功能
"""

import os
import tempfile
import shutil
from markdown_parser import MarkdownParser, DescriptionEntry


def test_parse_valid_file():
    """测试解析有效的 Markdown 文件"""
    print("=== 测试解析有效的 Markdown 文件 ===")
    
    parser = MarkdownParser()
    
    # 创建测试内容
    test_content = """---
keyword: lambda
synonyms: [匿名函数, anonymous function, closure]
related: [function, closure, capture]
category: language-feature
---

# Lambda 表达式

## 中文描述
Lambda 表达式是仓颉语言中的匿名函数特性，支持捕获外部变量。

## English Description
Lambda expressions are anonymous function features in Cangjie language, supporting variable capture.

## 使用场景
- 函数式编程
- 回调函数
- 高阶函数参数

## 相关实现
- LambdaExpr 类 (src/Parse/Lambda.h)
- BuildLambdaClosure 函数 (src/Sema/Lambda.cpp)
"""
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is not None, "解析应该成功"
        assert entry.keyword == 'lambda', f"关键词应为 'lambda'，实际为 '{entry.keyword}'"
        assert '匿名函数' in entry.synonyms, "同义词应包含 '匿名函数'"
        assert 'function' in entry.related, "相关概念应包含 'function'"
        assert entry.category == 'language-feature', f"类别应为 'language-feature'，实际为 '{entry.category}'"
        assert entry.concept_name == 'Lambda 表达式', f"概念名称应为 'Lambda 表达式'，实际为 '{entry.concept_name}'"
        assert entry.description_zh is not None, "应有中文描述"
        assert entry.description_en is not None, "应有英文描述"
        assert len(entry.use_cases) == 3, f"应有 3 个使用场景，实际有 {len(entry.use_cases)}"
        assert entry.implementation_notes is not None, "应有实现说明"
        
        print("✓ 所有断言通过")
        return True
        
    finally:
        os.unlink(temp_file)


def test_parse_chinese_only():
    """测试只有中文描述的文件"""
    print("\n=== 测试只有中文描述的文件 ===")
    
    parser = MarkdownParser()
    
    test_content = """---
keyword: generic
synonyms: [泛型]
---

# 泛型

## 中文描述
泛型是一种参数化类型的机制。
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is not None, "解析应该成功"
        assert entry.keyword == 'generic', "关键词应为 'generic'"
        assert entry.description_zh is not None, "应有中文描述"
        assert entry.description_en is None, "不应有英文描述"
        
        print("✓ 所有断言通过")
        return True
        
    finally:
        os.unlink(temp_file)


def test_parse_english_only():
    """测试只有英文描述的文件"""
    print("\n=== 测试只有英文描述的文件 ===")
    
    parser = MarkdownParser()
    
    test_content = """---
keyword: interface
---

# Interface

## English Description
Interface defines a contract for classes to implement.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is not None, "解析应该成功"
        assert entry.keyword == 'interface', "关键词应为 'interface'"
        assert entry.description_zh is None, "不应有中文描述"
        assert entry.description_en is not None, "应有英文描述"
        
        print("✓ 所有断言通过")
        return True
        
    finally:
        os.unlink(temp_file)


def test_parse_missing_keyword():
    """测试缺少 keyword 字段的文件"""
    print("\n=== 测试缺少 keyword 字段的文件 ===")
    
    parser = MarkdownParser()
    
    test_content = """---
synonyms: [test]
---

# Test Concept

## 中文描述
测试描述
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is None, "解析应该失败（缺少 keyword）"
        
        print("✓ 正确处理缺少 keyword 的情况")
        return True
        
    finally:
        os.unlink(temp_file)


def test_parse_missing_description():
    """测试缺少描述的文件"""
    print("\n=== 测试缺少描述的文件 ===")
    
    parser = MarkdownParser()
    
    test_content = """---
keyword: test
---

# Test Concept
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is None, "解析应该失败（缺少描述）"
        
        print("✓ 正确处理缺少描述的情况")
        return True
        
    finally:
        os.unlink(temp_file)


def test_parse_missing_concept_name():
    """测试缺少概念名称（一级标题）的文件"""
    print("\n=== 测试缺少概念名称的文件 ===")
    
    parser = MarkdownParser()
    
    test_content = """---
keyword: test
---

## 中文描述
测试描述
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is None, "解析应该失败（缺少一级标题）"
        
        print("✓ 正确处理缺少概念名称的情况")
        return True
        
    finally:
        os.unlink(temp_file)


def test_validate_format():
    """测试格式验证功能"""
    print("\n=== 测试格式验证功能 ===")
    
    parser = MarkdownParser()
    
    # 有效格式
    valid_content = """---
keyword: test
---

# Test

## 中文描述
测试
"""
    
    assert parser.validate_format(valid_content), "有效格式应通过验证"
    print("✓ 有效格式通过验证")
    
    # 缺少 keyword
    invalid_content1 = """---
synonyms: [test]
---

# Test

## 中文描述
测试
"""
    
    assert not parser.validate_format(invalid_content1), "缺少 keyword 应验证失败"
    print("✓ 缺少 keyword 验证失败")
    
    # 缺少描述
    invalid_content2 = """---
keyword: test
---

# Test
"""
    
    assert not parser.validate_format(invalid_content2), "缺少描述应验证失败"
    print("✓ 缺少描述验证失败")
    
    return True


def test_load_all_descriptions():
    """测试加载目录下所有描述文件"""
    print("\n=== 测试加载目录下所有描述文件 ===")
    
    parser = MarkdownParser()
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 创建多个测试文件
        files = {
            'lambda.md': """---
keyword: lambda
---

# Lambda

## 中文描述
Lambda 表达式
""",
            'generic.md': """---
keyword: generic
---

# Generic

## English Description
Generic types
""",
            'invalid.md': """---
synonyms: [test]
---

# Invalid
""",
            'readme.txt': "This is not a markdown file"
        }
        
        for filename, content in files.items():
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 加载所有描述
        descriptions = parser.load_all_descriptions(temp_dir)
        
        # 验证结果
        assert len(descriptions) == 2, f"应加载 2 个有效文件，实际加载 {len(descriptions)}"
        assert 'lambda' in descriptions, "应包含 lambda"
        assert 'generic' in descriptions, "应包含 generic"
        assert descriptions['lambda'].concept_name == 'Lambda', "lambda 的概念名称应为 'Lambda'"
        assert descriptions['generic'].concept_name == 'Generic', "generic 的概念名称应为 'Generic'"
        
        print("✓ 所有断言通过")
        return True
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)


def test_parse_empty_lists():
    """测试解析空列表"""
    print("\n=== 测试解析空列表 ===")
    
    parser = MarkdownParser()
    
    test_content = """---
keyword: test
synonyms: []
related: []
---

# Test

## 中文描述
测试

## 使用场景
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        entry = parser.parse_description_file(temp_file)
        
        assert entry is not None, "解析应该成功"
        assert entry.synonyms == [], "同义词应为空列表"
        assert entry.related == [], "相关概念应为空列表"
        assert entry.use_cases == [], "使用场景应为空列表"
        
        print("✓ 所有断言通过")
        return True
        
    finally:
        os.unlink(temp_file)


def main():
    """运行所有测试"""
    print("开始测试 MarkdownParser\n")
    
    tests = [
        test_parse_valid_file,
        test_parse_chinese_only,
        test_parse_english_only,
        test_parse_missing_keyword,
        test_parse_missing_description,
        test_parse_missing_concept_name,
        test_validate_format,
        test_load_all_descriptions,
        test_parse_empty_lists,
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
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
