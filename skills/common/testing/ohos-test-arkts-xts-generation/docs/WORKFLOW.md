# ohos-test-arkts-xts-generation 工作流程

> 为指定 d.ts 文件补充 XTS 测试用例的完整工作流程

## 流程总览

```
Phase 1         Phase 2              Phase 3           Phase 4         Phase 5/5A/5B
配置加载  →  覆盖率扫描+报告  →  API深度解析  →  测试设计文档  →  测试代码生成
                                                      ↓
              Phase 6         Phase 7         Phase 8         Phase 9         Phase 10
              注册测试  →  格式验证+编译  →  编译验证  →  覆盖率验证+报告  →  输出结果
```

---

## Phase 1：配置加载

1. 读取 `.oh-xts-config.json`（首次使用从 `.oh-xts-config.example.json` 初始化）
2. 从用户消息中提取 d.ts 文件路径（如 `component\text.d.ts`）
3. 通过 `references/component_subsystem_mapping.json`（360+ 组件→56 子系统映射）确定所属子系统
4. 通过目标工程的 `build-profile.json5` 中 `arkTSVersion` 判断语法类型（ArkTS-Dyn / ArkTS-Sta）
5. 加载子系统配置：`references/subsystems/{Subsystem}/_common.md` + 模块配置

---

## Phase 2：覆盖率扫描（确定覆盖缺口）

### Flow 判定

| 优先级 | 条件 | Flow |
|--------|------|------|
| 1 | 用户提供覆盖率报告 | **Flow A**（解析报告 + 代码风格扫描） |
| 2 | 无报告 | **Flow B**（APICoverageDetector 扫描） |
| 3 | 新增接口 | **Flow C**（跳过扫描，覆盖率为 0） |

### Flow B 详细步骤（最常见）

| 步骤 | 操作 | 脚本 |
|------|------|------|
| 1 | 准备扫描环境（复制子系统文件+SDK到扫描目录） | `manage_scan_env.py setup --subsystem {Subsystem}` 或 `manage_scan_env.py setup --module {ModuleName}`；也可用 `manage_scan_env.py sync` 同步已有环境 |
| 2 | 启动异步扫描，轮询等待完成（30-60 分钟） | `async_coverage_scan.py start` → `status` → `get_results` |
| 3 | 按 d.ts 文件筛选，提取未覆盖 API | `extract_uncovered.py --dts-file "component\\text.d.ts"` |
| 3.5 | 可选：Excel→CSV 转换 | `convert_results.py --iter 1 --phase before` |
| 3.6 | **生成覆盖率 MD 报告（生成前）** | `generate_coverage_report.py --phase before --dts-file "..."` |

### 8 维度（AQ-AX 列，独立判断）

| 维度 | 说明 | 对应 Excel 列 |
|------|------|---------------|
| call | 调用覆盖 | AQ |
| param | 入参覆盖 | AR |
| param_spec | 参数规格覆盖 | AS |
| return_value | 返回值覆盖 | AT |
| error_code | 错误码覆盖 | AU |
| permission | 权限覆盖 | AV |
| stage | stagemodel 标签覆盖 | AW |
| meta | 元服务覆盖 | AX |

### Phase 2 输出文件

| 文件 | 内容 |
|------|------|
| `uncovered_apis_{ts}.json` | 未覆盖 API（Phase 3 输入） |
| `manual_confirm_{ts}.json` | 需人工确认的 API |
| `coverage_report_before_{ver}_{ts}.md` | 生成前覆盖率报告（Phase 9 对比基准） |
| `coverage_report_before_{ver}_{ts}.json` | 结构化数据（供 `--compare-with` 引用） |

---

## Phase 3：API 深度解析

仅解析 Phase 2 识别出的**未覆盖 API**，构建完整知识库。

### 信息源优先级

| 信息源 | 获取内容 | 优先级 |
|--------|---------|--------|
| .d.ts 文件 | 方法签名、参数类型、返回值、@throws 错误码、@since 版本 | 最高 |
| 官方文档 | 使用场景、限制条件、最佳实践 | 高 |
| 现有测试 | 断言方法、代码模式、错误处理 | 中 |
| 子系统配置 | 特殊规则、命名规范 | 补充 |

### 信息源降级策略

| 缺失的信息源 | 处理方式 |
|-------------|---------|
| .d.ts 文件 | **终止**该 API 解析（无法 import，代码无法编译） |
| 官方文档 | 降级：仅使用 .d.ts + 现有测试 + 子系统配置 |
| 现有测试 | 降级：使用通用模板 |
| 子系统配置 | 降级：仅使用核心配置 |
| 全部缺失 | **终止**该 API 解析 |

---

## Phase 4：生成测试设计文档（**强制**，不可跳过）

为每个未覆盖 API 生成 `.design.md`：

- 测试场景设计（PARAM / ERROR / RETURN / BOUNDARY）
- 测试用例列表（含预期结果）
- **控件 ID 契约**（UI 类用例的 Demo ↔ UiTest 控件 ID 预定义）
- 分批执行计划（API > 20 或复杂场景时分批）

---

## Phase 5：测试代码生成

### 执行顺序

```
Phase 5A（用例分类 + Demo 生成）— 仅 UI 类
     ↓
Phase 5（非 UI 类）| Phase 5B（UiTest）| Phase 5A Step1（Demo）— 并行
     ↓
Demo + UiTest 同 HAP 编译
```

### 生成时加载的规范

| 规范文件 | 用途 |
|---------|------|
| `references/conventions/hypium_framework.md` | 断言方法 |
| `references/conventions/test_conventions.md` | 命名规范 |
| `references/conventions/arkts_standards.md` | ArkTS 语法 |
| `references/conventions/ets_version_naming.md` | ETS 版本命名（影响目录名/bundleName/hap_name） |
| `references/subsystems/{Subsystem}/_common.md` | 子系统特有规则 |

---

## Phase 6：注册测试

在 List.test.ets 中注册新测试文件：

```bash
python {skill_root}/scripts/register_test.py
```

---

## Phase 7：格式验证（**强制**，不可跳过）

| 步骤 | 内容 |
|------|------|
| A | `validate_test_context.py` 检查 5/9 项 + `arkts-static-spec` 校验（仅 ArkTS-Sta） |
| B | `check-test-code-quality` 技能执行 11 条规则深度扫描 |

---

## Phase 8：编译验证（推荐）

独立编译模式：

- Linux: `build_workflow_linux.md`
- Windows: `build_workflow_windows.md`

---

## Phase 9：覆盖率验证 + 报告

| 步骤 | 操作 | 脚本 |
|------|------|------|
| 9.1 | 再次执行 APICoverageDetector 扫描 | `async_coverage_scan.py` |
| 9.2 | 保存 after_generation CSV | `convert_results.py --phase after` |
| 9.4 | **生成覆盖率 MD 报告（生成后）+ before/after 对比** | `generate_coverage_report.py --phase after --compare-with before.json` |

### 对比报告内容

| 章节 | 内容 |
|------|------|
| 总体变化 | 已覆盖接口数、覆盖率的 before → after 变化 |
| 8 维度变化 | 每个维度的覆盖率变化 |
| 新增覆盖的接口 | API + 新覆盖维度 + 原未覆盖 → 现已覆盖 |
| 仍然未覆盖的接口 | API + 未覆盖维度 + 优先级 |

---

## Phase 10：输出结果

- 文件清单（所有新建/修改的 .test.ets 文件）
- 测试设计文档路径
- 覆盖率报告文件路径
- 覆盖率变化表
- 工作流执行检查清单（`phase_tracker.py report`）
- 上库前检查提醒（删除 hypium、注释 test_hap、命名合规、签名文件等）

---

## 关键约束

1. **Phase 4/7 不可跳过** — 设计文档和格式验证是质量门禁
2. **严格遵循 .d.ts 声明** — 未声明的接口在编译环境中不存在
3. **@tc 注解必须** — 每个测试用例必须有标准 @tc 块
4. **ETS 版本命名规范** — 目录名/bundleName/hap_name 必须符合 `ets_version_naming.md`
5. **Demo-UiTest 三方契约** — 控件 ID 在设计文档预定义，三方必须一致
6. **不修改 BUILD.gn** — 仅在指定目录创建测试文件

---

## Prompt 模板

详见 [USAGE_PROMPTS.md](./USAGE_PROMPTS.md)。
