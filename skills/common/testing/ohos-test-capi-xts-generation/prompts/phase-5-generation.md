## Phase 5: Generate Test Cases

---

### 📚 参考文档（按需查阅）

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `modules/L2_Generation/generator/test_generation_c.md` | 测试代码生成规则（N-API 封装结构、ETS 测试结构） | 本 Phase 必须加载 |
| `modules/L2_Generation/generator/test_patterns_napi_ets.md` | N-API 封装和 ETS 测试的公共模式 | 本 Phase 必须加载 |

---

### ⚙️ 按需加载

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 回调/异步/句柄类 API | `modules/L2_Generation/generator/test_patterns_napi_ets_advance.md` | N-API 高级模式 |
| 创建新工程 | `modules/L2_Generation/generator/project_config_templates.md` | 工程配置模板 |
| 使用不常见 N-API 函数 | `modules/L2_Generation/generator/napi_api_reference.md` | N-API API 参考 |
| 子系统特有测试模式 | `references/test_patterns_c.md` | CAPI 测试模式参考 |

---

### 🚫 Do NOT Load

```
所有 modules/L1_Analysis 模块
所有 modules/L3_Validation 模块
modules/L2_Generation/generator/verification_common.md（Phase 6 才加载）
```

---

**关键变更**：此阶段严格依据 Phase 4 生成的测试设计文档执行。设计驱动生成确保测试用例的完整性和 N-API 映射的一致性。

### 生成范围

| 条件 | 生成范围 | 说明 |
|------|---------|------|
| Flow A（覆盖率报告） | 仅生成报告中的未覆盖项 | 精准：严格按照报告列出的未覆盖项生成 |
| Flow C（新增接口） | 依据设计文档生成所有目标 API 的测试 | 基于 Phase 4 设计文档生成 |

### 生成顺序

1. **N-API 封装（C++）**：基于设计文档中的 N-API 函数名映射，生成 `NapiTest.cpp` 中的封装函数
2. **TypeScript 声明（index.d.ts）**：声明 ETS 侧可调用的函数接口
3. **ETS 测试代码（.test.ets）**：基于设计文档中的测试步骤和预期结果生成

### 生成约束

- **仅使用 .h 中声明的接口** — 禁止猜测或使用未声明的 API
- **每个用例必须包含 @tc 注解块**
- **nm_modname 必须为 "entry"**
- **错误处理使用 napi_throw_error**，返回 nullptr
- **cleanup 必须处理异常** — 资源泄漏会影响后续用例执行
- **支持并行**：多个测试文件可并行生成

### Generated Artifacts

| Artifact | Path |
|----------|------|
| C++ N-API wrapper | `entry/src/main/cpp/NapiTest.cpp` |
| TypeScript declaration | `entry/src/main/cpp/types/libentry/index.d.ts` |
| ETS test cases | `entry/src/ohosTest/ets/test/*.test.ets` |
| Build config | BUILD.gn, Test.json, etc.（仅新工程时） |

### 工程创建策略

优先级：**补充已有工程 > 创建新工程**

1. 用户指定目标测试套 → 直接在该工程中补充用例
2. 分析后发现可添加到已有工程 → 在已有工程中补充用例
3. 用户未指定且无合适已有工程 → 创建新工程（必须先从 `template_project/capi_test_template/` 复制完整模板）
