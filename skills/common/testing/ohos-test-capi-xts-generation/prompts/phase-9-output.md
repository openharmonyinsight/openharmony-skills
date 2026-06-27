## Phase 9: Output Results

---

### ⚙️ 按需加载

本 Phase 不需要额外加载模块。

---

### 🚫 Do NOT Load

```
所有模块（仅输出结果）
```

---

### 输出总览

Phase 9 输出一份完整的生成报告，包含以下章节：

1. 任务信息
2. 生成文件清单
3. 测试用例统计
4. 设备测试执行结果（如执行了 Phase 8）

---

### 报告模板

```markdown
# XTS CAPI 测试用例生成报告

## 1. 任务信息

| 项目 | 值 |
|------|---|
| 日期 | {YYYY-MM-DD} |
| 子系统 | {Subsystem}（如 multimedia） |
| 测试套 | {测试套名称} |
| .h 头文件 | {文件名}（如 native_window.h） |
| Flow 类型 | Flow A（覆盖率报告驱动）/ Flow C（新增接口） |
| 目标 API 数量 | {N} 个 |
| 生成用例数量 | {M} 个 |

---

## 2. 生成文件清单

### {测试套名称}

#### N-API 封装文件

| 文件 | 路径 | 封装函数数 | 行数 |
|------|------|-----------|------|
| NapiTest.cpp | {relative_path} | {N} | {L} |
| index.d.ts | {relative_path} | {N} | {L} |

#### ETS 测试文件

| 文件 | 路径 | 用例数 | 行数 |
|------|------|--------|------|
| {TestFile1}.test.ets | {relative_path} | {N} | {L} |
| List.test.ets | {relative_path} | 已更新 | — |

#### 设计文档

| 文件 | 路径 |
|------|------|
| {Design}.design.md | {relative_path} |

### 总计

| 指标 | 数量 |
|------|------|
| 测试文件数 | {F} |
| N-API 封装函数数 | {N} |
| 总用例数 | **{total}** |

---

## 3. 测试用例统计

### 按类型统计

| 类型 | 数量 | 占比 |
|------|------|------|
| PARAM | {N} | {Pct}% |
| ERROR | {N} | {Pct}% |
| RETURN | {N} | {Pct}% |
| BOUNDARY | {N} | {Pct}% |
| MEMORY | {N} | {Pct}% |
| **合计** | **{total}** | 100% |

### 按级别统计

| 级别 | 数量 | 说明 |
|------|------|------|
| P0 | {N} | 必测（内存管理、句柄生命周期） |
| P1 | {N} | 重点（错误码、回调） |
| P2 | {N} | 基础（简单读写） |

### N-API 函数映射

| ETS 测试函数 | N-API C++ 函数 | C API |
|-------------|---------------|-------|
| testNapi.xxx_ParamTest | XxxParamTest | OH_XXX_xxx() |
| testNapi.xxx_ErrorTest | XxxErrorTest | OH_XXX_xxx() |
| ... | | |

---

## 4. 设备测试执行结果

> 本章节仅在执行了 Phase 8 时出现，跳过时标注「跳过 — {原因}」

### 执行环境

| 项目 | 值 |
|------|---|
| 执行方案 | WSL 原生 / Windows PowerShell / 跳过 |
| 设备 SN | {device_sn} |
| 执行耗时 | {X}m{Y}s |

### 测试结果汇总

| 结果 | 数量 | 占比 |
|------|------|------|
| ✅ 通过 | {N} | {Pct}% |
| ❌ 失败 | {N} | {Pct}% |
| ⏭️ 忽略 | {N} | {Pct}% |
| **合计** | **{total}** | 100% |

### 失败用例分析

> 无失败时标注「全部通过 ✅」

| 失败套件 | 失败数 | 错误类型 | 根因 | 新/旧 | 处理方式 |
|---------|--------|---------|------|-------|---------|
| {SuiteName} | {N} | crash / type mismatch / ... | N-API 未注册 / null 未处理 / ... | 新 / 旧 | 已修复 / 记录 / 回退 Phase {N} |

---

## 5. 工作流执行检查清单

| 状态 | Phase | 结果 |
|------|-------|------|
| ✅ | Phase 1 配置加载 | 通过 |
| ✅ | Phase 2 头文件解析 | 通过 |
| ✅/⏭️ | Phase 3 覆盖率/风格扫描 | 通过 / 跳过（Flow C） |
| ✅ | Phase 4 测试设计文档 | 通过 |
| ✅ | Phase 5 测试代码生成 | 通过 |
| ✅ | Phase 6 N-API 三重校验 | 通过 |
| ✅/⏭️ | Phase 7 编译验证 | 通过 / 跳过 — {原因} |
| ✅/⏭️ | Phase 8 设备测试执行 | 通过 / 跳过 — {原因} |
| ✅ | Phase 9 结果输出 | 通过 |

**未通过/跳过的 Phase 必须标注原因和后续计划。**
```

---

### 数据来源

| 章节 | 数据来源 |
|------|---------|
| 文件清单 | Phase 5 生成的文件列表 |
| 测试用例统计 | Phase 4 设计文档 + Phase 5 代码 |
| 设备测试结果 | Phase 8 的 `summary_report.xml` + `summary.ini` + hilog |

### 输出方式

1. **直接输出到对话**：按上述模板格式，填充实际数据，直接展示给用户
2. **保存报告文件（必须）**：将完整报告保存到 `{skill_root}/.task_summary/session_{日期}_{sessionId}.md`
   - 日期格式：`YYYYMMDD`
   - sessionId：本次会话的唯一标识
   - 如果 `{skill_root}/.task_summary/` 目录不存在，先创建
