---
name: cangjie_compiler_knowledge
description: Search and query the Cangjie compiler source code knowledge base.
  Use this skill when users ask about compiler implementation details, where
  specific language features are implemented, location of classes or functions,
  compiler modules or architecture, or how keywords and syntax are handled.
  Trigger on queries like "where is lambda implemented", "find TypeChecker
  class", "how does pattern matching work in the compiler", "AST module
  location", or any question about compiler internals.
descriptionZH: 仓颉编译器知识库。【触发场景】编译器架构/模块/概念查询、TypeChecker/sema/AST/CHIR/CodeGen、解糖/去虚化/类型推导、lambda/闭包/泛型实现、编译流程/优化
  pass。【注意】提供概念说明、模块详情、关系图、源码导航。覆盖 18 模块 60+ 概念 714 文件 1036 类。
tags:
  - 知识库
  - 编译器
  - 仓颉
---

# Cangjie Compiler Knowledge Base

This skill provides AI assistants with the ability to search and query a knowledge base built from the Cangjie compiler source code. It enables quick lookup of implementation details, code locations, module dependencies, and architectural information.

## AI Quick Start Guide

When users ask about compiler internals, follow this workflow:

### Method 1: Search Script (Recommended - Now with improved precision!)
```bash
cd cangjie_ace_skills/cangjie_compiler_knowledge
python3 scripts/search.py "关键词"
```

### Method 2: Direct File Access (For browsing concepts)
- Read description files: `knowledge-base/descriptions/*.md`
- Contains 40+ detailed concept explanations
- Each file includes: Chinese/English descriptions, use cases, related implementations

### Available Topics
**Compiler Modules**: ast, parser, sema, codegen, chir, lexer, modules, package  
**Language Features**: lambda, generic, pattern-match, macro, reflection, concurrency  
**Type System**: type-system, type-inference, overload, generic  
**Advanced**: inline, desugaring, syntax-sugar, name-resolution, symbol-table

See `knowledge-base/descriptions/` directory for complete list.

## When to Use This Skill

Trigger this skill when users ask about:
- **Language feature implementations**: "Where is lambda implemented?", "How does the compiler handle generics?"
- **Class or function locations**: "Where is TypeChecker?", "Find the ParseExpr function"
- **Compiler modules and architecture**: "What's in the AST module?", "Show me the Sema components"
- **Keyword implementations**: "How is the extend keyword implemented?", "Where is match expression parsing?"
- **Code structure and dependencies**: "What modules does Parse depend on?", "Show me the call graph for TypeCheckLambda"

## Overview

The knowledge base is automatically generated from the Cangjie compiler source code located at `../cangjie_compiler`. It extracts:
- Classes and their locations
- Functions and method signatures
- Module structure and organization
- Dependencies between modules
- Function call relationships

AI assistants can maintain descriptive content (concept explanations, synonyms, usage scenarios) through Markdown files in the `knowledge-base/descriptions/` directory.

## Usage

### Searching the Knowledge Base

Use the search script to query the knowledge base:

```bash
python3 scripts/search.py "<query>" [options]
```

**Options:**
- `--index-path PATH`: Path to search index (default: `knowledge-base/search-index.json`)
- `--max-results N`: Maximum number of results (default: 10)
- `--no-fuzzy`: Disable fuzzy matching (default: enabled)
- `--json`: Output in JSON format
- `--lang {zh,en}`: Output language (default: zh)
- `--include-unittest`: Include unittest results (default: excluded for cleaner results)
- `--verbose`: Show detailed processing information

**Examples:**
```bash
# Search for lambda implementation (excludes unittest by default)
python3 scripts/search.py "lambda"

# Search for type inference (Chinese)
python3 scripts/search.py "类型推断"

# Include unittest results (useful when looking for test cases)
python3 scripts/search.py "lambda" --include-unittest

# Get JSON output
python3 scripts/search.py "pattern match" --json

# English output
python3 scripts/search.py "lambda" --lang en
```

### Generating/Updating the Knowledge Base

To generate or update the knowledge base from compiler source code:

```bash
python3 scripts/generate_knowledge.py [options]
```

**Options:**
- `--source-dir PATH`: Compiler source directory (default: `../cangjie_compiler`)
- `--output-dir PATH`: Output directory (default: `knowledge-base/`)
- `--incremental`: Only process modified files
- `--verbose`: Show detailed progress
- `--parallel N`: Number of parallel workers (default: 4)

**Examples:**
```bash
# Full generation
python3 scripts/generate_knowledge.py

# Incremental update
python3 scripts/generate_knowledge.py --incremental

# Verbose output with 8 workers
python3 scripts/generate_knowledge.py --verbose --parallel 8
```

## Search Result Format

Search results include:
- **Concept name and description**: What the feature/component is
- **Related modules**: Which compiler modules are involved
- **Related classes**: Class names with file paths and line numbers
- **Related functions**: Function names with file paths and line numbers
- **Module dependencies**: Which modules depend on each other
- **Call relationships**: Function call chains (when available)

Example output:
```
概念: lambda 表达式实现
描述: lambda 表达式的解析和语义分析

相关模块:
- parse
- sema

相关类:
- LambdaExpr (src/Parse/Lambda.h:45)
- LambdaAnalyzer (src/Sema/Lambda.h:23)

相关函数:
- BuildLambdaClosure (src/Sema/Lambda.cpp:156)
- TypeCheckLambda (src/Sema/Lambda.cpp:234)

模块依赖:
- parse -> sema
- sema -> chir
```

## Maintaining Descriptive Content

AI assistants can enhance the knowledge base by adding or updating concept descriptions in Markdown files.

### When to Add Descriptions

Add or update descriptions when:
- A user asks about a concept but search results lack clear explanations
- Existing descriptions are inaccurate or outdated
- Synonyms or related terms need to be added
- Usage scenarios need clarification

### How to Add Descriptions

1. Create or edit a Markdown file in `knowledge-base/descriptions/`
2. Use the concept keyword as the filename (e.g., `lambda.md`, `generic.md`)
3. Follow the standard format (see AI_MAINTENANCE_GUIDE.md)
4. Run `generate_knowledge.py` to merge descriptions into the search index

For detailed guidance on maintaining the knowledge base, see `AI_MAINTENANCE_GUIDE.md`.

## Knowledge Base Structure

```
cangjie_compiler_knowledge/
├── SKILL.md                      # This file
├── AI_MAINTENANCE_GUIDE.md       # Maintenance guide for AI assistants
├── scripts/
│   ├── generate_knowledge.py     # Knowledge base generator
│   └── search.py                 # Search interface
└── knowledge-base/
    ├── descriptions/             # AI-maintained concept descriptions
    │   └── *.md
    ├── search-index.json         # Search index
    ├── cross-references.json     # Module and function dependencies
    └── modules/                  # Per-module data
        └── *.json
```

## Supported Language Features

The knowledge base covers all major Cangjie language features and compiler components:

- **Type System**: Classes, structs, interfaces, enums, generics
- **Functions**: Function declarations, lambdas, closures, overloading
- **Control Flow**: Loops, pattern matching, error handling
- **Advanced Features**: Macros, reflection, annotations, concurrency
- **Standard Library**: Collections, networking, I/O
- **Interop**: C FFI
- **Module System**: Packages, imports, dependencies

## Performance

- Search response time: < 100ms (with index loaded)
- Supports fuzzy matching with edit distance ≤ 2
- Incremental updates process only modified files
- Parallel processing for large codebases

## Common Questions

**Q: The search returns no results. What should I do?**
A: The knowledge base may need to be generated or updated. Run `python3 scripts/generate_knowledge.py` to build the index.

**Q: How do I search in Chinese?**
A: The search engine automatically detects language and supports both Chinese and English queries, including mixed queries.

**Q: Can I search for partial names?**
A: Yes, fuzzy matching is enabled by default and will find partial matches with small edit distances.

**Q: How often should the knowledge base be updated?**
A: Run incremental updates (`--incremental` flag) when compiler source code changes. Full regeneration is rarely needed.

## Notes

- The knowledge base is read-only for queries; only the generator modifies it
- Descriptive content (Markdown files) is the only part AI assistants should edit directly
- All structural data (classes, functions, dependencies) is automatically extracted from source code
- The skill requires Python 3.8+ and the jieba library for Chinese text processing
