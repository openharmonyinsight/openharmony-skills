#!/usr/bin/env python3
"""
集成测试：验证 KeywordExtractor 与其他模块的集成
"""

import os
import tempfile
from file_scanner import FileScanner
from cpp_parser import CppParser
from module_analyzer import ModuleAnalyzer
from keyword_extractor import KeywordExtractor


def create_test_files():
    """创建测试用的 C++ 文件"""
    test_dir = tempfile.mkdtemp()
    
    # 创建目录结构
    src_dir = os.path.join(test_dir, 'src')
    parse_dir = os.path.join(src_dir, 'Parse')
    sema_dir = os.path.join(src_dir, 'Sema')
    
    os.makedirs(parse_dir)
    os.makedirs(sema_dir)
    
    # 创建测试文件
    lambda_h = os.path.join(parse_dir, 'Lambda.h')
    with open(lambda_h, 'w') as f:
        f.write("""
#include "Expr.h"

class LambdaExpr {
public:
    LambdaExpr();
    void parse();
};

class LambdaAnalyzer {
public:
    void analyze();
};
""")
    
    type_checker_cpp = os.path.join(sema_dir, 'TypeChecker.cpp')
    with open(type_checker_cpp, 'w') as f:
        f.write("""
#include "TypeChecker.h"

void TypeCheckLambda() {
    // Implementation
}

void InferType() {
    // Implementation
}
""")
    
    return test_dir


def test_full_pipeline():
    """测试完整的处理流程"""
    print("=== 集成测试：完整处理流程 ===\n")
    
    # 创建测试文件
    test_dir = create_test_files()
    print(f"创建测试目录: {test_dir}")
    
    try:
        # 1. 扫描文件
        print("\n1. 扫描文件...")
        scanner = FileScanner()
        files = scanner.scan(test_dir, ['.h', '.cpp'])
        print(f"   找到 {len(files)} 个文件:")
        for f in files:
            print(f"   - {f}")
        
        # 2. 解析文件
        print("\n2. 解析文件...")
        parser = CppParser()
        parsed_files = []
        for file_path in files:
            full_path = os.path.join(test_dir, file_path)
            parsed = parser.parse_file(full_path)
            parsed_files.append(parsed)
            print(f"   {file_path}:")
            print(f"     类: {[c.name for c in parsed.classes]}")
            print(f"     函数: {[f.name for f in parsed.functions]}")
        
        # 3. 构建模块树
        print("\n3. 构建模块树...")
        analyzer = ModuleAnalyzer()
        tree = analyzer.build_module_tree(parsed_files)
        print(f"   找到 {len(tree.modules)} 个模块:")
        for module in tree.get_all_modules():
            print(f"   - {module.name}: {len(module.classes)} 类, {len(module.functions)} 函数")
        
        # 4. 提取关键词
        print("\n4. 提取关键词...")
        extractor = KeywordExtractor()
        
        all_keywords = {}
        
        for module in tree.get_all_modules():
            print(f"\n   模块: {module.name}")
            
            # 从类提取关键词
            for cls in module.classes:
                keywords = extractor.extract_from_class(cls)
                all_keywords[cls.name] = keywords
                print(f"     类 {cls.name}: {keywords}")
            
            # 从函数提取关键词
            for func in module.functions:
                keywords = extractor.extract_from_function(func)
                all_keywords[func.name] = keywords
                print(f"     函数 {func.name}: {keywords}")
        
        # 5. 验证结果
        print("\n5. 验证结果...")
        
        # 验证 LambdaExpr 的关键词
        assert 'LambdaExpr' in all_keywords, "应该提取到 LambdaExpr"
        lambda_keywords = all_keywords['LambdaExpr']
        assert 'lambda' in lambda_keywords, "LambdaExpr 应包含 'lambda' 关键词"
        assert 'expr' in lambda_keywords, "LambdaExpr 应包含 'expr' 关键词"
        assert 'class' in lambda_keywords, "LambdaExpr 应包含 'class' 关键词"
        print("   ✓ LambdaExpr 关键词验证通过")
        
        # 验证 TypeCheckLambda 的关键词
        assert 'TypeCheckLambda' in all_keywords, "应该提取到 TypeCheckLambda"
        type_check_keywords = all_keywords['TypeCheckLambda']
        assert 'type' in type_check_keywords, "TypeCheckLambda 应包含 'type' 关键词"
        assert 'check' in type_check_keywords, "TypeCheckLambda 应包含 'check' 关键词"
        assert 'lambda' in type_check_keywords, "TypeCheckLambda 应包含 'lambda' 关键词"
        assert 'function' in type_check_keywords, "TypeCheckLambda 应包含 'function' 关键词"
        print("   ✓ TypeCheckLambda 关键词验证通过")
        
        print("\n✓ 集成测试通过！")
        return True
        
    finally:
        # 清理测试文件
        import shutil
        shutil.rmtree(test_dir)
        print(f"\n清理测试目录: {test_dir}")


def main():
    """运行集成测试"""
    try:
        success = test_full_pipeline()
        return success
    except Exception as e:
        print(f"\n✗ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
