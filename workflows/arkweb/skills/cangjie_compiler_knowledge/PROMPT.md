## 仓颉编译器知识库（cangjie_compiler_knowledge 技能）

**⚠️ 触发关键词：**
lambda在哪实现 | TypeChecker在哪 | 类型推断 | 模式匹配穷尽性 | AST模块 | 语义分析 | 泛型实例化 | 编译器架构

**⚠️ 功能：**
搜索仓颉编译器源码知识库，快速定位语言特性实现、类/函数位置、模块依赖关系

**用法：**
```bash
# 搜索知识库
python3 scripts/search.py "关键词"

# 生成/更新知识库
python3 scripts/generate_knowledge.py
```

**支持查询：**
- 语言特性实现位置（lambda、泛型、模式匹配等）
- 类和函数定义位置（TypeChecker、ParseExpr等）
- 编译器模块架构（Parse、Sema、CodeGen等）
- 模块依赖关系和函数调用链

**知识库内容：**
- 自动提取：类、函数、模块、依赖关系
- AI维护：概念描述、同义词、使用场景（通过 Markdown 文件）

详细文档见 `SKILL.md` 和 `AI_MAINTENANCE_GUIDE.md`
