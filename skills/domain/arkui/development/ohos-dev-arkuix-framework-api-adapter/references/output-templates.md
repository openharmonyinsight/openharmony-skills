# Phase Output Templates

Templates for each phase's output files. All files are written to `.arkuix-adaptation/` directory.

**Naming rule**: `{module_short_name}-{purpose}.md` (e.g., `settings-info.md`, `preferences-api-inventory.md`)

---

## Phase 1: {module}-info.md

```markdown
# @{module} — 模块信息

## 基本信息
- **模块名**: @{module}
- **子系统路径**: {subsystem_path}
- **仓库名**: {repo_name}
- **d.ts 路径**: interface/sdk-js/api/@{module}.d.ts
- **记录时间**: {timestamp}

## 代码同步状态
- [ ] OHOS 源码已存在于本工程
- [ ] 代码已同步到 plugins/ 目录
```

---

## Phase 3: {module}-api-inventory.md

```markdown
# @{module} — API 接口清单

## 统计概览
| 指标 | 值 |
|------|-----|
| 总接口数 | {total} |
| 已适配 (@crossplatform) | {adapted} ({percent}%) |
| 待适配 | {needs} ({percent}%) |
| 已废弃 | {deprecated} |

## 覆盖率
📈 {progress_bar} {percent}%

## 待适配接口清单

### {category_name}
| API | 签名 | since | 状态 |
|-----|------|-------|------|
| {name} | {signature} | {since} | ❌ needs_adaptation |

## 常量清单

### {namespace_name} 命名空间
| 常量名 | 类型 | since | 废弃 |
|--------|------|-------|------|
| {const_name} | {type} | {since} | {deprecated} |
```

---

## Phase 4: {module}-architecture.md

```markdown
# @{module} — 架构分析报告

## 代码量统计
| 层级 | 代码行数 | 占比 |
|------|---------|------|
| NAPI 绑定 | {napi_lines} | {napi_pct}% |
| 业务逻辑 | {biz_lines} | {biz_pct}% |
| 平台适配 | {plat_lines} | {plat_pct}% |
| **总计** | **{total}** | 100% |

## 平台依赖比: {dep_ratio}% ({level})

## C/C++ 纯度: {purity_result}

## 依赖清单
### 内部依赖
{internal_deps}

### 外部依赖
{external_deps}

## 平台实现必要性: {necessity}
{necessity_detail}

## 推荐模式: {mode} ({reuse_pct}%)
- 理由: {rationale}
```

---

## Phase 5: {module}-plan.md

Contains TWO sections: execution plan + E2E test case specification.

### Section 1: Execution Plan

```markdown
# @{module} — 适配执行计划

## 模式: {mode_name} (预计复用率 {reuse}%, 新增 ~{lines} 行)

## 任务分解

### Task A: {task_name} [无依赖]
- **范围**: {scope}
- **文件**: {files}
- **交付标准**: {criteria}
- **skills**: [{skills}]

### Task B: {task_name} [依赖 Task A]
- **范围**: {scope}
- **文件**: {files}
- **交付标准**: {criteria}
- **skills**: [{skills}]

### Task C: {task_name} [依赖 Task A]
- **范围**: {scope}
- **文件**: {files}
- **交付标准**: {criteria}
- **skills**: [{skills}]

### Task D: {task_name} [依赖 Task A]
- **范围**: {scope}
- **交付标准**: {criteria}
- **skills**: [{skills}]

### Task E: E2E 验证 [依赖 B + C + D]
- **范围**: 执行完整 E2E 验证管线 (build → overlay SDK → test project → deploy → validate)
- **交付标准**: {platform_count} 端均通过 {api_count} 个 API 的 E2E 测试

## 并行执行图
{execution_graph}
```

### Section 2: E2E Test Case Specification

```markdown
## E2E 测试用例规格

### test{ApiName}{NNN}
- **API**: {signature}
- **输入**: {input}
- **Android 预期**: {android_expected}
- **iOS 预期**: {ios_expected}
- **OHOS 预期**: {ohos_expected}
- **失败模式**: {failure_mode}
- **对等组**: {parity_group}

### 对等组统计
| 对等组 | 数量 | 说明 |
|--------|------|------|
| all_platforms_same | {n} | 三端行为一致 |
| ios_differs | {n} | iOS 行为不同 |
| android_only | {n} | 仅 Android 支持 |
| ohos_only | {n} | 仅 OHOS 支持 |
```

---

## Phase 7: {module}-e2e-report.md

```markdown
# @{module} — E2E 验证报告

## 基本信息
- **构建版本**: {build_version}
- **验证时间**: {timestamp}

## 平台汇总
| 平台 | 编译 | 部署 | 用例总数 | 通过 | 失败 |
|------|------|------|---------|------|------|
| Android | {status} | {status} | {total} | {pass} | {fail} |
| iOS | {status} | {status} | {total} | {pass} | {fail} |

## 逐用例结果
| 测试 ID | Android | iOS | OHOS |
|---------|---------|-----|------|
| {test_id} | {result} | {result} | {result} |

## 总体结论: {overall_result}

## 待解决问题
{issues}
```
