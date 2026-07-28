## Phase 3: Coverage Analysis / Style Scan

---

### 📚 参考文档（按需查阅）

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `modules/L1_Analysis/analyzer/coverage_analyzer.md` | 覆盖率分析方法、代码风格提取规则 | Flow A 时必须加载 |

---

### ⚙️ 按需加载

无额外模块。

---

### 🚫 Do NOT Load

```
所有 modules/L2_Generation 模块
所有 modules/L3_Validation 模块
modules/L1_Analysis/parser/（已在 Phase 2 加载）
```

---

### Flow 差异

| Flow | 执行内容 | 说明 |
|------|---------|------|
| **Flow A** | **Style Scan Only** — 提取已有测试的代码风格（命名模式、注释风格、N-API 封装模式、测试结构） | 不要重新分析覆盖率，覆盖率信息从用户报告中获取 |
| **Flow C** | **跳过** — 新增接口无已有覆盖率数据 | 直接进入 Phase 4 |

---

### Flow A: Style Scan 详情

扫描已有测试文件，提取以下风格信息：

| 信息 | 提取方式 | 后续用途 |
|------|---------|---------|
| N-API 封装函数命名模式 | 从 `NapiTest.cpp` 中的函数名提取 | Phase 5 保持一致风格 |
| ETS 测试结构 | 从 `*.test.ets` 提取 import、describe/it 模式 | Phase 5 保持一致风格 |
| @tc 注解格式 | 从已有测试中提取注解模板 | Phase 5 保持一致格式 |
| N-API 参数转换模式 | 从已有 N-API 封装中提取 `napi_get_value_*` 模式 | Phase 5 保持一致模式 |
| 错误处理模式 | 从已有代码中提取 `napi_throw_error` 使用模式 | Phase 5 保持一致模式 |

**输出**：代码风格摘要（不重新分析覆盖率）。
