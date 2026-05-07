# L1_Analysis（分析提取层）

> **层级**: 第 1 层 | **输出**: API 信息、覆盖率数据、工程配置

本层整合 C API 解析和覆盖率分析功能，从 .h 头文件、NAPI 封装代码和文档中提取被测 API 信息，为后续测试生成提供完整上下文。

---

## 子模块

### parser/（API 解析）

| 文件 | 说明 |
|------|------|
| `unified_api_parser_c.md` | C API 头文件统一解析器 |
| `doc_reader.md` | 官方文档读取与提取 |
| `project_parser.md` | 工程配置解析 |

### analyzer/（覆盖率分析）

| 文件 | 说明 |
|------|------|
| `coverage_analyzer.md` | 测试覆盖率分析器（C++ NapiTest + ETS 双维度） |

---

## 使用方式

### Phase 2: API 解析

```
modules/L1_Analysis/parser/unified_api_parser_c.md
modules/L1_Analysis/parser/doc_reader.md（可选）
modules/L1_Analysis/parser/project_parser.md（可选）
```

### Phase 3: 覆盖率分析（Flow B）

```
modules/L1_Analysis/analyzer/coverage_analyzer.md
```

---

## 注意事项

1. 信息源依赖 .h 头文件、NAPI C++ 封装和 index.d.ts 的完整性
2. 覆盖率分析覆盖 C++ NapiTest.cpp 和 ETS test.ets 两个维度
3. 头文件宏定义和条件编译可能影响解析准确性

---

**更新日期**: 2026-04-07
**版本**: 2.0.0
