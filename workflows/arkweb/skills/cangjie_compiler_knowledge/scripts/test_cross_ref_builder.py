#!/usr/bin/env python3
"""
测试 CrossRefBuilder 交叉引用构建器
"""

import unittest
import json
import tempfile
import os
from cross_ref_builder import CrossRefBuilder, CrossReference, ModuleReference, FunctionReference
from dependency_analyzer import DependencyGraph, CallGraph


class TestCrossRefBuilder(unittest.TestCase):
    """测试 CrossRefBuilder"""
    
    def setUp(self):
        """设置测试环境"""
        self.builder = CrossRefBuilder()
    
    def test_build_module_refs_empty(self):
        """测试空依赖图的模块引用构建"""
        dep_graph = DependencyGraph()
        module_refs = self.builder.build_module_refs(dep_graph)
        
        self.assertEqual(len(module_refs), 0)
    
    def test_build_module_refs_simple(self):
        """测试简单模块依赖的引用构建"""
        dep_graph = DependencyGraph(
            module_dependencies={
                "parse": ["lex", "basic"],
                "sema": ["parse"],
                "lex": [],
                "basic": []
            },
            module_dependents={
                "lex": ["parse"],
                "basic": ["parse"],
                "parse": ["sema"],
                "sema": []
            }
        )
        
        module_refs = self.builder.build_module_refs(dep_graph)
        
        # 验证 parse 模块
        self.assertIn("parse", module_refs)
        self.assertEqual(set(module_refs["parse"].depends_on), {"lex", "basic"})
        self.assertEqual(set(module_refs["parse"].depended_by), {"sema"})
        
        # 验证 sema 模块
        self.assertIn("sema", module_refs)
        self.assertEqual(module_refs["sema"].depends_on, ["parse"])
        self.assertEqual(module_refs["sema"].depended_by, [])
        
        # 验证 lex 模块
        self.assertIn("lex", module_refs)
        self.assertEqual(module_refs["lex"].depends_on, [])
        self.assertEqual(module_refs["lex"].depended_by, ["parse"])
    
    def test_build_function_refs_empty(self):
        """测试空调用图的函数引用构建"""
        call_graph = CallGraph()
        function_refs = self.builder.build_function_refs(call_graph)
        
        self.assertEqual(len(function_refs), 0)
    
    def test_build_function_refs_simple(self):
        """测试简单函数调用的引用构建"""
        call_graph = CallGraph(
            function_calls={
                "TypeCheckLambda": ["BuildLambdaClosure", "InferType"],
                "TypeCheckExpr": ["TypeCheckLambda"],
                "BuildLambdaClosure": [],
                "InferType": []
            },
            function_callers={
                "BuildLambdaClosure": ["TypeCheckLambda"],
                "InferType": ["TypeCheckLambda"],
                "TypeCheckLambda": ["TypeCheckExpr"],
                "TypeCheckExpr": []
            }
        )
        
        function_refs = self.builder.build_function_refs(call_graph)
        
        # 验证 TypeCheckLambda 函数
        self.assertIn("TypeCheckLambda", function_refs)
        self.assertEqual(set(function_refs["TypeCheckLambda"].calls), {"BuildLambdaClosure", "InferType"})
        self.assertEqual(set(function_refs["TypeCheckLambda"].called_by), {"TypeCheckExpr"})
        
        # 验证 BuildLambdaClosure 函数
        self.assertIn("BuildLambdaClosure", function_refs)
        self.assertEqual(function_refs["BuildLambdaClosure"].calls, [])
        self.assertEqual(function_refs["BuildLambdaClosure"].called_by, ["TypeCheckLambda"])
    
    def test_build_complete_cross_reference(self):
        """测试构建完整的交叉引用"""
        dep_graph = DependencyGraph(
            module_dependencies={"parse": ["lex"], "lex": []},
            module_dependents={"lex": ["parse"], "parse": []}
        )
        
        call_graph = CallGraph(
            function_calls={"ParseExpr": ["Lex"], "Lex": []},
            function_callers={"Lex": ["ParseExpr"], "ParseExpr": []}
        )
        
        cross_ref = self.builder.build(dep_graph, call_graph)
        
        # 验证模块引用
        self.assertIn("parse", cross_ref.module_dependencies)
        self.assertEqual(cross_ref.module_dependencies["parse"].depends_on, ["lex"])
        
        # 验证函数引用
        self.assertIn("ParseExpr", cross_ref.function_calls)
        self.assertEqual(cross_ref.function_calls["ParseExpr"].calls, ["Lex"])
    
    def test_to_json_format(self):
        """测试 JSON 输出格式"""
        dep_graph = DependencyGraph(
            module_dependencies={"parse": ["lex"], "lex": []},
            module_dependents={"lex": ["parse"], "parse": []}
        )
        
        call_graph = CallGraph(
            function_calls={"ParseExpr": ["Lex"], "Lex": []},
            function_callers={"Lex": ["ParseExpr"], "ParseExpr": []}
        )
        
        cross_ref = self.builder.build(dep_graph, call_graph)
        json_str = self.builder.to_json(cross_ref)
        
        # 验证 JSON 可以解析
        data = json.loads(json_str)
        
        # 验证结构
        self.assertIn("module_dependencies", data)
        self.assertIn("function_calls", data)
        
        # 验证模块依赖格式
        self.assertIn("parse", data["module_dependencies"])
        self.assertIn("depends_on", data["module_dependencies"]["parse"])
        self.assertIn("depended_by", data["module_dependencies"]["parse"])
        self.assertEqual(data["module_dependencies"]["parse"]["depends_on"], ["lex"])
        
        # 验证函数调用格式
        self.assertIn("ParseExpr", data["function_calls"])
        self.assertIn("calls", data["function_calls"]["ParseExpr"])
        self.assertIn("called_by", data["function_calls"]["ParseExpr"])
        self.assertEqual(data["function_calls"]["ParseExpr"]["calls"], ["Lex"])
    
    def test_save_to_file(self):
        """测试保存到文件"""
        dep_graph = DependencyGraph(
            module_dependencies={"parse": ["lex"]},
            module_dependents={"lex": ["parse"]}
        )
        
        call_graph = CallGraph(
            function_calls={"ParseExpr": ["Lex"]},
            function_callers={"Lex": ["ParseExpr"]}
        )
        
        cross_ref = self.builder.build(dep_graph, call_graph)
        
        # 使用临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # 保存到文件
            self.builder.save_to_file(cross_ref, temp_path)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(temp_path))
            
            # 读取并验证内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn("module_dependencies", data)
            self.assertIn("function_calls", data)
            self.assertIn("parse", data["module_dependencies"])
            self.assertIn("ParseExpr", data["function_calls"])
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_bidirectional_references(self):
        """测试双向引用的一致性"""
        dep_graph = DependencyGraph(
            module_dependencies={
                "parse": ["lex", "basic"],
                "sema": ["parse"],
                "lex": [],
                "basic": []
            },
            module_dependents={
                "lex": ["parse"],
                "basic": ["parse"],
                "parse": ["sema"],
                "sema": []
            }
        )
        
        module_refs = self.builder.build_module_refs(dep_graph)
        
        # 验证双向引用的一致性
        # 如果 A depends_on B，那么 B 应该在 depended_by 中有 A
        for module, ref in module_refs.items():
            for dep in ref.depends_on:
                self.assertIn(module, module_refs[dep].depended_by,
                             f"{module} depends on {dep}, but {dep} doesn't have {module} in depended_by")
            
            for dependent in ref.depended_by:
                self.assertIn(module, module_refs[dependent].depends_on,
                             f"{dependent} depends on {module}, but {module} doesn't have {dependent} in depends_on")
    
    def test_complex_dependency_graph(self):
        """测试复杂的依赖图"""
        dep_graph = DependencyGraph(
            module_dependencies={
                "frontend": ["parse", "sema"],
                "parse": ["lex", "basic"],
                "sema": ["parse", "chir"],
                "codegen": ["chir"],
                "chir": ["basic"],
                "lex": ["basic"],
                "basic": []
            },
            module_dependents={
                "basic": ["lex", "parse", "chir"],
                "lex": ["parse"],
                "parse": ["frontend", "sema"],
                "chir": ["sema", "codegen"],
                "sema": ["frontend"],
                "codegen": [],
                "frontend": []
            }
        )
        
        module_refs = self.builder.build_module_refs(dep_graph)
        
        # 验证 frontend 模块
        self.assertEqual(set(module_refs["frontend"].depends_on), {"parse", "sema"})
        self.assertEqual(module_refs["frontend"].depended_by, [])
        
        # 验证 basic 模块（被多个模块依赖）
        self.assertEqual(module_refs["basic"].depends_on, [])
        self.assertEqual(set(module_refs["basic"].depended_by), {"lex", "parse", "chir"})
        
        # 验证 parse 模块（既依赖又被依赖）
        self.assertEqual(set(module_refs["parse"].depends_on), {"lex", "basic"})
        self.assertEqual(set(module_refs["parse"].depended_by), {"frontend", "sema"})


class TestModuleReference(unittest.TestCase):
    """测试 ModuleReference 数据类"""
    
    def test_default_values(self):
        """测试默认值"""
        ref = ModuleReference()
        self.assertEqual(ref.depends_on, [])
        self.assertEqual(ref.depended_by, [])
    
    def test_with_values(self):
        """测试带值初始化"""
        ref = ModuleReference(
            depends_on=["lex", "basic"],
            depended_by=["sema"]
        )
        self.assertEqual(ref.depends_on, ["lex", "basic"])
        self.assertEqual(ref.depended_by, ["sema"])


class TestFunctionReference(unittest.TestCase):
    """测试 FunctionReference 数据类"""
    
    def test_default_values(self):
        """测试默认值"""
        ref = FunctionReference()
        self.assertEqual(ref.calls, [])
        self.assertEqual(ref.called_by, [])
    
    def test_with_values(self):
        """测试带值初始化"""
        ref = FunctionReference(
            calls=["BuildClosure", "InferType"],
            called_by=["TypeCheckExpr"]
        )
        self.assertEqual(ref.calls, ["BuildClosure", "InferType"])
        self.assertEqual(ref.called_by, ["TypeCheckExpr"])


class TestCrossReference(unittest.TestCase):
    """测试 CrossReference 数据类"""
    
    def test_default_values(self):
        """测试默认值"""
        cross_ref = CrossReference()
        self.assertEqual(cross_ref.module_dependencies, {})
        self.assertEqual(cross_ref.function_calls, {})
    
    def test_with_values(self):
        """测试带值初始化"""
        module_refs = {
            "parse": ModuleReference(depends_on=["lex"], depended_by=["sema"])
        }
        function_refs = {
            "ParseExpr": FunctionReference(calls=["Lex"], called_by=["TypeCheck"])
        }
        
        cross_ref = CrossReference(
            module_dependencies=module_refs,
            function_calls=function_refs
        )
        
        self.assertEqual(cross_ref.module_dependencies, module_refs)
        self.assertEqual(cross_ref.function_calls, function_refs)


if __name__ == '__main__':
    unittest.main()
