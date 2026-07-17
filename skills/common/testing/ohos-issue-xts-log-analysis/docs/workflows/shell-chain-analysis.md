# Shell命令执行链分析详细说明

> **核心定界点**：通过检查 shell 命令执行链判定测试是否正常执行

## 概述

Shell命令执行链分析是前置分析的关键步骤，用于判定测试是否真正执行。若测试未执行（install/aa test失败），则**不做 hilog 切片**——直接定界为环境问题。

---

## module_run.log 结构

### 实际日志示例

```text
[2026-06-26 15:53:44,232] [Hdc] hdc shell date '2026-06-26 15:53:44'   ← ① 同步设备时钟
[2026-06-26 15:53:44,890] [Hdc] hdc shell bm install -p .../ActsAACommandImplicitStartTest.hap  ← ② hap 安装
[2026-06-26 15:53:47,034] [Hdc] hdc shell aa test -m entry_test -b com.example...  ← ③ aa test 执行
[2026-06-26 15:53:48,165] [OHJSUnitDriver] [Collected suite count is: 1, test count is: 32]  ← ④ 用例收集数
[2026-06-26 15:53:48,645] [Listener] [[1/32 SN] AACommandImplicitStartTest#SUB_..._0100 PASSED]  ← ⑤ 逐用例结果
[2026-06-26 15:53:52,973] [Listener] [[31/32 SN] AACommandImplicitStartTest#SUB_..._3100 FAILED]  ← 失败用例 + PC 时间
[2026-06-26 15:53:53,118] [Listener] [End test suite [AACommandImplicitStartTest].]  ← ⑥ 结束标记
```

### 关键字段

| 字段 | 格式 | 示例 | 用途 |
|------|------|------|------|
| PC 时间 | `[YYYY-MM-DD HH:MM:SS,mmm]` | `[2026-06-26 15:53:44,232]` | 时间窗提取（回退） |
| 设备 SN | `[Hdc]` 行内含设备 SN | `FMR0123417000740` | 定位 hilog 子目录 |
| bundle name | `aa test` 命令 `-b` 参数 | `com.example...` | 报告基本信息 |
| 用例结果 | `[Listener] [...] PASSED/FAILED` | `PASSED` / `FAILED` | 锁定失败用例 |

---

## 执行阶段检查（4阶段）

### 阶段①：bm install → hap 安装检查

**AI操作**：
```bash
grep "bm install" module_run.log
grep -A 5 "bm install" module_run.log  # 查 install 后是否有报错
```

**成功判定**：
- install 后无报错
- 出现后续 aa test 命令
- 出现 [Listener] 输出

**失败判定**：
- install 后有报错（如 "install failed"）
- 无后续 aa test 命令
- 日志中断在 install 阶段

**失败示例**：
```text
[2026-06-26 15:53:44,890] [Hdc] hdc shell bm install -p .../ActsAACommandImplicitStartTest.hap
[2026-06-26 15:53:45,123] [Hdc] install failed: signature verification failed
```

**定界结论**：
- **hap 安装失败** → 定界：环境问题（签名/包问题）
- **不做 hilog 切片**

---

### 阶段②：aa test → 测试命令检查

**AI操作**：
```bash
grep "aa test" module_run.log
grep "OHJSUnitDriver" module_run.log  # 查是否出现 run test
```

**成功判定**：
- 出现 `aa test` 命令
- 出现 `[OHJSUnitDriver]` 标记
- 出现后续 Collected count

**失败判定**：
- aa test 命令报错（如 "aa test failed"）
- 无后续 OHJSUnitDriver 输出
- 日志中断在 aa test 阶段

**失败示例**：
```text
[2026-06-26 15:53:47,034] [Hdc] hdc shell aa test -m entry_test -b com.example...
[2026-06-26 15:53:47,156] [Hdc] aa test failed: bundle not found
```

**定界结论**：
- **aa test 执行失败** → 定界：环境问题（bundle/命令问题）
- **不做 hilog 切片**

---

### 阶段③：Collected count → 用例收集检查

**AI操作**：
```bash
grep "Collected suite count" module_run.log
```

**成功判定**：
- suite count > 0
- test count > 0
- 出现后续 [Listener] 输出

**失败判定**：
- suite count = 0
- test count = 0
- 无后续 [Listener] 输出

**失败示例**：
```text
[2026-06-26 15:53:48,165] [OHJSUnitDriver] [Collected suite count is: 0, test count is: 0]
```

**定界结论**：
- **用例收集失败** → 定界：环境问题（用例未注册/配置问题）
- **不做 hilog 切片**

---

### 阶段④：[Listener] → 逐用例结果检查

**AI操作**：
```bash
grep "[Listener]" module_run.log
grep "PASSED" module_run.log
grep "FAILED" module_run.log
```

**成功判定**：
- 有 [Listener] 行
- 有 PASSED 或 FAILED 输出
- 逐用例结果正常输出

**失败判定**：
- 无 [Listener] 行
- 无 PASSED/FAILED 输出
- 用例未真正运行

**失败示例**：
```text
[2026-06-26 15:53:48,165] [OHJSUnitDriver] [Collected suite count is: 32, test count is: 100]
[2026-06-26 15:53:48,200] [OHJSUnitDriver] run test...
（无后续 [Listener] 输出）
```

**定界结论**：
- **用例未真正运行** → 定界：测试框架/启动问题
- **不做 hilog 切片**

---

## 执行状态判定矩阵

| 阶段① | 阶段② | 阶段③ | 阶段④ | 判定结果 | 后续操作 |
|-------|-------|-------|-------|---------|---------|
| ✅ | ✅ | ✅ | ✅ | **测试正常执行** | 继续 hilog 切片 |
| ❌ | - | - | - | **hap 安装失败** | 不做切片，定界环境问题 |
| ✅ | ❌ | - | - | **aa test 执行失败** | 不做切片，定界环境问题 |
| ✅ | ✅ | ❌ | - | **用例收集失败** | 不做切片，定界环境问题 |
| ✅ | ✅ | ✅ | ❌ | **用例未真正运行** | 不做切片，定界框架问题 |

---

## 报告输出格式

### Shell命令执行链判定表格

在报告"一、测试执行概况"章节中，输出以下表格：

```markdown
### Shell命令执行链判定
| 阶段 | 状态 | 时间 | 详情 |
|------|------|------|------|
| ① bm install | ✅ 成功 | 09:23:15-09:23:16 | hap安装成功 |
| ② aa test | ✅ 成功 | 09:23:18 | aa test命令正常下发 |
| ③ Collected count | ✅ 成功 | 09:23:19 | 18 suites, 130 tests |
| ④ Listener输出 | ✅ 成功 | 09:23:25-09:29:38 | 逐用例结果输出 |

**执行状态判定**: 测试正常执行，可以进行hilog切片分析。
```

### 失败情况报告

若任一阶段失败，输出：

```markdown
### Shell命令执行链判定
| 阶段 | 状态 | 时间 | 详情 |
|------|------|------|------|
| ① bm install | ❌ 失败 | 09:23:15-09:23:16 | 签名验证失败 |
| ② aa test | ⚠️ 未执行 | - | 因install失败中断 |
| ③ Collected count | ⚠️ 未执行 | - | 因install失败中断 |
| ④ Listener输出 | ⚠️ 未执行 | - | 因install失败中断 |

**执行状态判定**: hap安装失败（环境问题），不做hilog切片分析。

**定界结论**: 环境问题（hap签名验证失败）
```

---

## 常见失败场景

### 场景1：hap安装失败

**日志特征**：
- install 后有报错
- 无后续 aa test 命令

**定界**：环境问题（签名/包/权限）

**报告标注**：
```markdown
**定界结论**: 环境问题（hap签名验证失败）
**建议流转**: 检查hap签名配置，确认设备权限
```

### 场景2：aa test执行失败

**日志特征**：
- aa test 命令报错
- 无后续 OHJSUnitDriver 输出

**定界**：环境问题（bundle/命令/设备）

**报告标注**：
```markdown
**定界结论**: 环境问题（bundle未找到）
**建议流转**: 检查bundle name配置，确认hap是否正确安装
```

### 场景3：用例未真正运行

**日志特征**：
- Collected count > 0
- 无 [Listener] 输出

**定界**：测试框架/启动问题

**报告标注**：
```markdown
**定界结论**: 测试框架问题（用例未真正运行）
**建议流转**: 检查测试框架配置，确认测试启动逻辑
```

---

## AI执行检查清单

| 检查项 | 操作 | 输出 |
|--------|------|------|
| ✅ 检查 bm install | grep "bm install" + grep -A 5 | 成功/失败状态 |
| ✅ 检查 aa test | grep "aa test" + grep "OHJSUnitDriver" | 成功/失败状态 |
| ✅ 检查 Collected count | grep "Collected suite count" | 成功/失败状态 |
| ✅ 检查 [Listener] | grep "[Listener]" + grep "PASSED/FAILED" | 成功/失败状态 |
| ✅ 判定执行状态 | 根据矩阵判定 | 正常执行/环境问题/框架问题 |
| ✅ 输出判定表格 | 生成表格 + 定界结论 | 报告内容 |

---

## 关键改进说明

| 对比项 | 原设计 | 新设计 | 改进效果 |
|--------|--------|--------|---------|
| 执行状态检查 | 不检查，直接做 hilog 切片 | 强制4阶段检查 | 避免无用切片（环境问题不做切片） |
| 定界结论 | 无明确定界 | 明确定界（环境问题/框架问题） | 提高报告准确性 |
| 报告格式 | 无执行链表格 | 强制输出执行链判定表格 | 提高报告可追溯性 |

---

**更新时间**：2026-07-03  
**文档来源**：IMPROVEMENT_PLAN.md 第202-212行  
**设计理念**：执行状态强制检查，未执行不做切片