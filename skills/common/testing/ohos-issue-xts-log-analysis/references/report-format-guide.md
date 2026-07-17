# XTS 测试分析报告格式指南

> 基于 20260703 改进计划优化

---

## 报告结构（4章节）

### 标准格式

```markdown
# XTS测试问题分析报告

**报告日期**: YYYY-MM-DD  
**测试套件**: TestsuiteName  
**设备SN**: FMR0123417000740  
**子系统**: SubsystemName

---

## 一、测试执行概况

### 1.1 测试套件信息

| 项目 | 内容 |
|------|------|
| 测试套件 | TestsuiteName |
| 用例总数 | N |
| 通过数 | M |
| 失败数 | X |
| 执行时间 | Ts（PC时间） |
| 设备SN | FMR0123417000740 |
| Bundle Name | com.example.testsuite |

### 1.2 Shell命令执行链判定

| 执行阶段 | 命令 | 结果 | 状态 |
|---------|------|------|------|
| ① HAP安装 | `bm install -p /data/local/tmp/Testsuite.hap` | ✅ 成功 | 正常 |
| ② aa test下发 | `aa test -m entry_test -b com.example...` | ✅ 成功 | 正常 |
| ③ 用例收集 | `Collected suite count is: 1, test count is: N` | ✅ 成功 | 正常 |
| ④ 用例执行 | `[Listener] PASSED/FAILED` 输出 | ✅ 成功 | 正常 |

**判定结论**: ✅ 测试正常执行，继续 hilog 切片分析

---

## 二、失败用例清单

### 2.1 失败用例列表

| 序号 | 用例名称 | 结果 | 执行时长 |
|------|---------|------|---------|
| 1 | SUB_Subsystem_Module_TestCase_0100 | FAILED | 1ms |
| 2 | SUB_Subsystem_Module_TestCase_0200 | FAILED | 0ms |

### 2.2 失败详情

| 用例名 | 失败信息 | 问题类型 |
|--------|---------|---------|
| SUB_Subsystem_Module_TestCase_0100 | `expect undefined equals 16000150` | API未返回预期错误码 |
| SUB_Subsystem_Module_TestCase_0200 | `expect undefined equals 16000150` | API未返回预期错误码 |

### 2.3 问题类型分组统计（可选）

| 问题类型 | 用例数 | 用例列表 |
|---------|--------|---------|
| API功能缺陷 | 2 | TestCase_0100, TestCase_0200 |

---

## 三、hilog日志用例详情

### 3.1 SUB_Subsystem_Module_TestCase_0100

#### 3.1.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | SUB_Subsystem_Module_TestCase_0100 |
| 测试套件 | TestsuiteName |
| 执行序号 | 1/N |
| 执行结果 | FAILED |
| 消耗时间 | 1ms |
| 所在日志（hilog） | hilog.050.20260626-160128.txt |

#### 3.1.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.050.20260626-160128.txt |
| 起始时间 | 06-26 16:01:29.239 |
| 起始行号 | 4000 |
| 结束时间 | 06-26 16:01:29.310 |
| 结束行号 | 4662 |
| 时间来源 | hilog [Hypium] 标记（设备时间） |

#### 3.1.3 源码→领域证据链

| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| api.method() | Subsystem | DomainTag | 4299-4307 | 16:01:29.306-307 |

**证据链追溯**:
```
失败用例源码(.ets)
    │ import api from '@ohos.module'
    ▼
@ohos 模块 → 子系统
    │ '@ohos.module' → Subsystem子系统
    ▼
子系统 → hilog domain
    │ "Subsystem" → DomainTag
    ▼
精准日志过滤
    │ 过滤域：DomainTag
    ▼
日志切片 → 行4299-4307
```

#### 3.1.4 关键日志片段

**所在日志**: hilog.050.20260626-160128.txt（行4266-4317）

**关键证据**:
```
行4299: [DomainTag] TestCase_0100 start
行4304: [DomainTag] TestCase_0100 success
行4317: [Hypium][failDetail]expect undefined equals expected_value
```

#### 3.1.5 源码定位与分析

**源码位置**: `/path/to/source/file.ets:80-105`

**源码片段**:
```typescript
it('SUB_Subsystem_Module_TestCase_0100', Level.LEVEL0, async (done: Function) => {
  // 测试代码
  api.method();  // ← 关键调用
  expect(result).assertEqual(expected);
  done();
})
```

**源码分析**:
1. 测试逻辑说明
2. 预期行为 vs 实际行为
3. 失败原因

#### 3.1.6 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | API功能缺陷 |
| 影响范围 | Subsystem子系统 - Module |
| 定界依据 | 关键字'keyword'匹配数据库规则 → Domain领域 |
| 归属判定 | **Subsystem子系统问题** |

---

### 3.2 SUB_Subsystem_Module_TestCase_0200 [同根因用例]

#### 3.2.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | SUB_Subsystem_Module_TestCase_0200 |
| 测试套件 | TestsuiteName |
| 执行序号 | 2/N |
| 执行结果 | FAILED |
| 消耗时间 | 0ms |
| 所在日志（hilog） | hilog.050.20260626-160128.txt |

#### 3.2.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.050.20260626-160128.txt |
| 起始时间 | 06-26 16:01:29.308 |
| 起始行号 | 4375 |
| 结束时间 | 06-26 16:01:29.309 |
| 结束行号 | 4445 |
| 时间来源 | hilog [Hypium] 标记（设备时间） |

#### 3.2.3 根因继承

**同根因说明**: 与用例 3.1 相同，API `method()` 在特定条件下未返回预期结果。

**差异点**: 参数差异，但失败根因与 3.1 一致。

#### 3.2.4 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | API功能缺陷（同根因） |
| 影响范围 | Subsystem子系统 - Module |
| 归属判定 | **Subsystem子系统问题**（继承3.1结论）

---

## 四、总结

### 4.1 问题汇总

**共性问题**: 
- Module 的多个 API 在特定条件下未返回预期结果
- 导致测试用例预期行为失效

**根本原因**:
- API 实现未正确处理特定条件
- 未按规范返回预期值或错误码

### 4.2 定界结论

| 用例名 | 问题类型 | 归属子系统 | 归属领域 | 流转建议 |
|--------|---------|-----------|---------|---------|
| SUB_Subsystem_Module_TestCase_0100 | API功能缺陷 | Subsystem | Domain | 流转至 Subsystem 子系统 |
| SUB_Subsystem_Module_TestCase_0200 | API功能缺陷 | Subsystem | Domain | 流转至 Subsystem 子系统（同根因） |

**定界依据**:
1. 测试正常执行（Shell命令链完整）
2. API调用成功但未返回预期结果
3. 属于 API 实现问题而非测试环境问题

### 4.3 建议流转

**主责任人**: Subsystem 子系统 - Module 模块  
**问题类型**: API 功能缺陷  
**修复建议**: 
- 检查 API 实现，确保在特定条件下正确返回预期结果
- 验证错误处理逻辑的一致性

**修复示例（可选）**:
```typescript
// 建议修复方案
if (condition) {
  throw new BusinessError(errorCode, "Error message");
}
```

### 4.4 用户确认提示

请确认以下关键信息：

1. ✅ **测试环境判定**: 
   - 环境条件说明
   - 此结论是否正确？是否需要验证其他环境条件？

2. ✅ **API行为判定**: 
   - API 在特定条件下应该返回预期结果
   - 此预期是否符合 API 规范？是否有 API 文档链接？

3. ✅ **定界结论判定**: 
   - 问题归属 Subsystem 子系统
   - 是否需要进一步验证环境配置？
   - 是否需要流转至 Subsystem 子系统责任人？

---

**报告生成时间**: YYYY-MM-DD HH:MM  
**报告生成工具**: xts-issue-analysis skill  
**数据来源**: hilog.txt + module_run.log + 源码验证
```

---

## 改进要点（20260703）

### 1. 移除"零、数据库查询记录"

**原因**: 数据库查询是分析过程的中间产物，对用户价值较低。

**替代**: 在"三、hilog日志用例详情"的"问题定界"部分简要说明定界依据。

### 2. "一、测试执行概况"不包含时间窗提取

**原因**: 时间窗提取属于技术细节，应下放到具体用例详情中。

**改进**: 时间窗提取信息在每个用例的"时间窗提取"章节中展示。

### 3. "三、hilog日志用例详情"展示所有失败用例

**原因**: 确保所有失败用例都有独立展示，避免遗漏。

**同根因处理**: 
- 标记 `[同根因用例]` 标签
- 包含根因继承章节
- 说明差异点（如有）

### 4. 每个用例包含完整时间窗追溯信息

**新增字段**:
- 所在日志文件（hilog文件名）
- 起始行号
- 结束行号

**目的**: 用户可快速定位到具体日志位置。

### 5. 用户确认提示更具体

**改进**: 包含详细说明，而非泛泛而谈。

**示例**: 
```markdown
1. ✅ **测试环境判定**: 
   - 设备不支持 HyperSnap（beforeAll 中通过 `hidumper -s 1901 -a -a` 检查）
   - 此结论是否正确？是否需要验证其他环境条件？
```

---

## 检查清单

### 一章节检查

- ✅ 测试套件信息表格（套件名、用例数、通过/失败数、设备SN、Bundle Name）
- ✅ Shell命令执行链判定表格（4阶段）
- ✅ 执行状态判定结论
- ❌ 不包含时间窗提取（已下放）

### 二章节检查

- ✅ 失败用例列表（表格形式）
- ✅ 失败详情（表格形式）
- ✅ 问题类型分组统计（可选）

### 三章节检查

- ✅ 展示所有失败用例（同根因标记）
- ✅ 基本信息（包含"所在日志（hilog）"）
- ✅ 时间窗提取（包含日志文件、起始/结束行号）
- ✅ 源码→领域证据链
- ✅ 关键日志片段（带行号）
- ✅ 源码定位与分析
- ✅ 问题定界（包含定界依据来源）

### 四章节检查

- ✅ 问题汇总
- ✅ 定界结论表格（5个字段）
- ✅ 建议流转（包含修复示例）
- ✅ 用户确认提示（至少3条，更具体）

---

**更新时间**: 2026-07-03  
**文档来源**: 基于 IMPROVEMENT_PLAN.md 改进