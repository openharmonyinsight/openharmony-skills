#!/usr/bin/env python3
"""
测试 SearchIndexBuilder 搜索索引构建器
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from search_index_builder import SearchIndexBuilder, SearchIndex, IndexEntry, CodeLocation
from module_analyzer import ModuleTree, ModuleInfo
from cpp_parser import ClassInfo, FunctionInfo
from markdown_parser import DescriptionEntry


def test_basic_index_building():
    """测试基本索引构建"""
    print("=== 测试基本索引构建 ===\n")
    
    # 创建模块树
    tree = ModuleTree()
    
    # 添加 parse 模块
    parse_module = ModuleInfo(
        name="parse",
        path="src/Parse",
        files=["src/Parse/Lambda.cpp", "src/Parse/Lambda.h"],
        classes=[
            ClassInfo(name="LambdaExpr", file="src/Parse/Lambda.h", line=45),
            ClassInfo(name="Parser", file="src/Parse/Parser.h", line=23)
        ],
        functions=[
            FunctionInfo(name="ParseLambda", file="src/Parse/Lambda.cpp", line=100),
            FunctionInfo(name="ParseExpression", file="src/Parse/Parser.cpp", line=200)
        ]
    )
    tree.add_module(parse_module)
    
    # 添加 sema 模块
    sema_module = ModuleInfo(
        name="sema",
        path="src/Sema",
        files=["src/Sema/TypeChecker.cpp"],
        classes=[
            ClassInfo(name="TypeChecker", file="src/Sema/TypeChecker.h", line=30)
        ],
        functions=[
            FunctionInfo(name="TypeCheckLambda", file="src/Sema/TypeChecker.cpp", line=150),
            FunctionInfo(name="CheckType", file="src/Sema/TypeChecker.cpp", line=200)
        ]
    )
    tree.add_module(sema_module)
    
    # 构建索引
    builder = SearchIndexBuilder()
    index = builder.build_index(tree)
    
    # 验证索引
    assert len(index.keywords) > 0, "索引应该包含关键词"
    
    # 检查 lambda 关键词
    lambda_entry = index.get_entry("lambda")
    assert lambda_entry is not None, "应该有 lambda 关键词"
    assert "parse" in lambda_entry.modules, "lambda 应该关联到 parse 模块"
    assert len(lambda_entry.classes) > 0, "lambda 应该关联到类"
    assert len(lambda_entry.functions) > 0, "lambda 应该关联到函数"
    
    print(f"✓ 基本索引构建测试通过")
    print(f"  关键词总数: {len(index.keywords)}")
    print(f"  lambda 关键词:")
    print(f"    模块: {lambda_entry.modules}")
    print(f"    类: {[cls.name for cls in lambda_entry.classes]}")
    print(f"    函数: {[func.name for func in lambda_entry.functions]}")
    print()
    
    return index


def test_merge_descriptions():
    """测试合并 Markdown 描述"""
    print("=== 测试合并 Markdown 描述 ===\n")
    
    # 创建简单的索引
    tree = ModuleTree()
    parse_module = ModuleInfo(
        name="parse",
        path="src/Parse",
        classes=[ClassInfo(name="LambdaExpr", file="src/Parse/Lambda.h", line=45)],
        functions=[FunctionInfo(name="ParseLambda", file="src/Parse/Lambda.cpp", line=100)]
    )
    tree.add_module(parse_module)
    
    builder = SearchIndexBuilder()
    index = builder.build_index(tree)
    
    # 创建描述
    lambda_desc = DescriptionEntry(
        keyword="lambda",
        synonyms=["匿名函数", "anonymous function", "closure"],
        related=["function", "closure", "capture"],
        category="language-feature",
        concept_name="Lambda 表达式",
        description_zh="Lambda 表达式是仓颉语言中的匿名函数特性，支持捕获外部变量。",
        description_en="Lambda expressions are anonymous function features in Cangjie language.",
        use_cases=["函数式编程", "回调函数"],
        implementation_notes="LambdaExpr 类实现",
        file_path="lambda.md"
    )
    
    generic_desc = DescriptionEntry(
        keyword="generic",
        synonyms=["泛型", "template"],
        related=["type", "parameter"],
        category="language-feature",
        concept_name="泛型",
        description_zh="泛型允许编写类型参数化的代码。",
        description_en="Generics allow writing type-parameterized code.",
        use_cases=["容器类", "算法"],
        implementation_notes=None,
        file_path="generic.md"
    )
    
    descriptions = {
        "lambda": lambda_desc,
        "generic": generic_desc
    }
    
    # 合并描述
    index = builder.merge_descriptions(index, descriptions)
    
    # 验证 lambda 描述
    lambda_entry = index.get_entry("lambda")
    assert lambda_entry is not None, "lambda 条目应该存在"
    assert lambda_entry.description == lambda_desc.description_zh, "中文描述应该匹配"
    assert lambda_entry.description_en == lambda_desc.description_en, "英文描述应该匹配"
    assert lambda_entry.synonyms == lambda_desc.synonyms, "同义词应该匹配"
    assert lambda_entry.related == lambda_desc.related, "相关概念应该匹配"
    
    print(f"✓ lambda 描述合并成功")
    print(f"  中文描述: {lambda_entry.description[:50]}...")
    print(f"  英文描述: {lambda_entry.description_en[:50]}...")
    print(f"  同义词: {lambda_entry.synonyms}")
    print(f"  相关概念: {lambda_entry.related}")
    
    # 验证同义词索引
    synonym_entry = index.get_entry("匿名函数")
    assert synonym_entry is not None, "同义词条目应该存在"
    assert "lambda" in synonym_entry.synonyms, "同义词应该指向主关键词"
    
    print(f"✓ 同义词索引创建成功")
    print(f"  '匿名函数' 指向: {synonym_entry.synonyms}")
    
    # 验证 generic 描述（新关键词）
    generic_entry = index.get_entry("generic")
    assert generic_entry is not None, "generic 条目应该存在"
    assert generic_entry.description == generic_desc.description_zh, "generic 描述应该匹配"
    
    print(f"✓ generic 描述合并成功（新关键词）")
    print(f"  中文描述: {generic_entry.description}")
    print()


def test_tfidf_calculation():
    """测试 TF-IDF 计算"""
    print("=== 测试 TF-IDF 计算 ===\n")
    
    # 创建包含多个模块的树
    tree = ModuleTree()
    
    # 添加多个模块和代码元素
    for i in range(3):
        module = ModuleInfo(
            name=f"module{i}",
            path=f"src/Module{i}",
            classes=[
                ClassInfo(name=f"Class{i}A", file=f"src/Module{i}/ClassA.h", line=10),
                ClassInfo(name=f"Class{i}B", file=f"src/Module{i}/ClassB.h", line=20)
            ],
            functions=[
                FunctionInfo(name=f"Function{i}A", file=f"src/Module{i}/func.cpp", line=100),
                FunctionInfo(name=f"Function{i}B", file=f"src/Module{i}/func.cpp", line=200)
            ]
        )
        tree.add_module(module)
    
    # 构建索引
    builder = SearchIndexBuilder()
    index = builder.build_index(tree)
    
    # 验证 TF-IDF 分数
    for keyword, entry in list(index.keywords.items())[:5]:
        assert entry.tfidf_score >= 0, "TF-IDF 分数应该非负"
        print(f"  {keyword}: TF-IDF = {entry.tfidf_score:.4f}, 文档数 = {len(entry.classes) + len(entry.functions)}")
    
    print(f"✓ TF-IDF 计算测试通过")
    print()


def test_json_serialization():
    """测试 JSON 序列化"""
    print("=== 测试 JSON 序列化 ===\n")
    
    # 创建简单索引
    tree = ModuleTree()
    parse_module = ModuleInfo(
        name="parse",
        path="src/Parse",
        classes=[ClassInfo(name="LambdaExpr", file="src/Parse/Lambda.h", line=45)],
        functions=[FunctionInfo(name="ParseLambda", file="src/Parse/Lambda.cpp", line=100)]
    )
    tree.add_module(parse_module)
    
    builder = SearchIndexBuilder()
    index = builder.build_index(tree)
    
    # 转换为字典
    index_dict = index.to_dict()
    
    # 验证结构
    assert "keywords" in index_dict, "应该包含 keywords 字段"
    assert isinstance(index_dict["keywords"], dict), "keywords 应该是字典"
    
    # 验证条目结构
    for keyword, entry_dict in list(index_dict["keywords"].items())[:3]:
        assert "description" in entry_dict, "条目应该包含 description"
        assert "description_en" in entry_dict, "条目应该包含 description_en"
        assert "synonyms" in entry_dict, "条目应该包含 synonyms"
        assert "related" in entry_dict, "条目应该包含 related"
        assert "modules" in entry_dict, "条目应该包含 modules"
        assert "classes" in entry_dict, "条目应该包含 classes"
        assert "functions" in entry_dict, "条目应该包含 functions"
        assert "tfidf_score" in entry_dict, "条目应该包含 tfidf_score"
        
        # 验证类和函数的结构
        for cls in entry_dict["classes"]:
            assert "name" in cls and "file" in cls and "line" in cls
        
        for func in entry_dict["functions"]:
            assert "name" in func and "file" in func and "line" in func
    
    print(f"✓ JSON 序列化测试通过")
    print(f"  关键词总数: {len(index_dict['keywords'])}")
    print()
    
    # 测试 JSON 导出
    import json
    json_str = json.dumps(index_dict, ensure_ascii=False, indent=2)
    assert len(json_str) > 0, "JSON 字符串应该非空"
    
    print(f"✓ JSON 导出成功")
    print(f"  JSON 大小: {len(json_str)} 字节")
    print()


def test_add_entry():
    """测试添加索引条目"""
    print("=== 测试添加索引条目 ===\n")
    
    builder = SearchIndexBuilder()
    
    # 创建自定义条目
    entry = IndexEntry(
        keyword="custom",
        description="自定义条目",
        modules=["module1", "module2"],
        classes=[
            CodeLocation(name="CustomClass", file="custom.h", line=10)
        ],
        functions=[
            CodeLocation(name="customFunction", file="custom.cpp", line=100)
        ]
    )
    
    # 添加条目
    builder.add_entry("custom", entry)
    
    # 验证内部映射
    assert "custom" in builder.keyword_to_modules, "关键词应该在模块映射中"
    assert "module1" in builder.keyword_to_modules["custom"], "模块应该被添加"
    assert "custom" in builder.keyword_to_classes, "关键词应该在类映射中"
    assert len(builder.keyword_to_classes["custom"]) == 1, "应该有一个类"
    assert "custom" in builder.keyword_to_functions, "关键词应该在函数映射中"
    assert len(builder.keyword_to_functions["custom"]) == 1, "应该有一个函数"
    
    print(f"✓ 添加索引条目测试通过")
    print(f"  关键词: custom")
    print(f"  模块: {list(builder.keyword_to_modules['custom'])}")
    print(f"  类: {[cls.name for cls in builder.keyword_to_classes['custom']]}")
    print(f"  函数: {[func.name for func in builder.keyword_to_functions['custom']]}")
    print()


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("SearchIndexBuilder 测试套件")
    print("=" * 60)
    print()
    
    try:
        test_basic_index_building()
        test_merge_descriptions()
        test_tfidf_calculation()
        test_json_serialization()
        test_add_entry()
        
        print("=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
