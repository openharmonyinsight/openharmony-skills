---
keyword: codegen
synonyms: [代码生成, code generation, code emit, IR generation, LLVM codegen]
related: [chir, llvm, compiler, backend, optimization]
category: compiler-module
---

# 代码生成 (CodeGen)

## 中文描述

代码生成模块负责将编译器的中间表示（CHIR）转换为目标代码。该模块是编译器后端的核心组件，负责生成 LLVM IR 或其他目标平台的机器码。主要功能包括：表达式代码生成、函数代码生成、类型转换、内存管理、优化等。

代码生成过程包括：
- 遍历 CHIR 节点树
- 为每个节点生成对应的 LLVM IR 指令
- 处理函数调用约定和参数传递
- 生成类和接口的虚函数表
- 处理异常处理代码
- 生成并发相关的运行时调用
- 应用目标平台特定的优化

## English Description

The CodeGen module is responsible for converting the compiler's intermediate representation (CHIR) into target code. This module is the core component of the compiler backend, responsible for generating LLVM IR or machine code for other target platforms. Main functions include: expression code generation, function code generation, type conversion, memory management, optimization, etc.

The code generation process includes:
- Traversing the CHIR node tree
- Generating corresponding LLVM IR instructions for each node
- Handling function calling conventions and parameter passing
- Generating vtables for classes and interfaces
- Handling exception handling code
- Generating runtime calls for concurrency
- Applying target platform-specific optimizations

## 使用场景

- 将类型检查后的 CHIR 转换为可执行代码
- 生成不同目标平台的代码（x86_64, ARM, etc.）
- 应用编译器优化（内联、循环优化等）
- 生成调试信息和符号表
- 处理 C FFI 调用的代码生成

## 相关实现

- **主要模块**: `src/CodeGen/`
- **核心类**: 
  - `CGContext` - 代码生成上下文
  - `CodeGenerator` - 代码生成器主类
- **关键函数**:
  - `EmitExpressionIR()` - 生成表达式的 IR
  - `EmitFunctionIR()` - 生成函数的 IR
  - `EmitClassIR()` - 生成类的 IR
  - `EmitCFFICall()` - 生成 C FFI 调用
- **依赖模块**: CHIR, LLVM
- **被依赖**: Driver, Frontend

## 代码示例

### 示例 1: CodegenOnePackage
文件: `include/cangjie/FrontendTool/DefaultCompilerInstance.h:45`

```cpp
bool CodegenOnePackage(AST::Package& pkg, bool enableIncrement) const;

private:
    class DefaultCIImpl* impl;
};
} // namespace Cangjie

#endif // CANGJIE_FRONTEND_DEFAULTCOMPILERINSTANCE_H
```

### 示例 2: LoadCachedCodegenResult
文件: `include/cangjie/FrontendTool/IncrementalCompilerInstance.h:57`

```cpp
void LoadCachedCodegenResult() const;
    void UpdateCachedInfo() override;
    void UpdateCHIROptEffectMap();
};
} // namespace Cangjie

#endif // CANGJIE_FRONTEND_INCREMENTALCOMPILERINSTANCE_H
```

### 示例 3: CodeGen::SaveToBitcodeFile
文件: `src/CodeGen/CGModule.cpp:178`

```cpp
CodeGen::SaveToBitcodeFile(*module, cachePath);
    }
    if (auto namedMD = module->getNamedMetadata("CodeGenAddedForIncr"); namedMD) {
        namedMD->eraseFromParent();
    }
    if (auto namedMD = module->getNamedMetadata("StaticGenericTIsForIncr"); namedMD) {
        namedMD->eraseFromParent();
    }
}

void CGModule::GenCodeGenAddedMetadata() const
{
    auto codegenAddedNamedMD = GetLLVMModule()->getOrInsertNamedMetadata("CodeGenAddedForIncr");
    const auto& codegenAddedFuncsOrVars = GetCGContext().GetCodeGenAddedFuncsOrVars();
    for (auto& kv : codegenAddedFuncsOrVars) {
        std::vector<llvm::Metadata*> ops;
        ops.push_back(llvm::MDString::get(GetLLVMContext(), kv.first));
        for (auto& name : kv.second) {
            ops.push_back(llvm::MDString::get(GetLLVMContext(), name));
        }
```

## 概念关系图谱

- **同义词**: 代码生成, code generation, code emit, IR generation, LLVM codegen
- **相关概念**: chir, llvm, compiler, backend, optimization
- **相关模块**: codegen, frontendtool, include

## 常见问题

### codegen 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 codegen？

请参考下面的代码示例部分。

### codegen 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

