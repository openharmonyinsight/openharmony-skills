# L2_Report - 报告结构规范

> 报告生成流程见 [ReportGeneration.md](./ReportGeneration.md)。约束见 [report-constraints.md](../../references/report-constraints.md)。
---

## 报告格式规范

  - BLOCKED用例定界原则
  - BLOCKED类型识别方法
  - BLOCKED用例报告格式
- 一、hilog日志用例详情
  - 1.1 [FAILED用例名称]（完整6段落分析）
  - 1.X 级联阻塞用例汇总
- 二、总结
  - 崩溃作为根因时的报告结构（2026-07-14新增）
- 一、hilog日志用例详情
  - 1.1 [崩溃进程名]进程崩溃分析（根因）
  - 1.2 [第一个FAILED用例]（完整6段落，引用1.1崩溃分析）
  - 1.3 ~ 1.N [其他FAILED用例]（完整6段落，标注"同根因"）
  - 1.N+1 级联阻塞用例汇总
- 二、总结
  - 多根因报告结构（2026-07-15新增）
- 一、hilog日志用例详情
  - 1.1 [根因1：崩溃进程名]进程崩溃分析

---

> 基于 20260713 改进计划优化：移除测试执行概况和失败用例清单章节，总结改为问题分类视角

---

## 报告结构（2章节）

### 根据测试结果选择报告格式

| 用例结果 | 处理方式 | 报告内容 |
|---------|---------|---------|
| 有FAILED用例 | 完整6段落分析 | 每个FAILED用例完整6段落 + BLOCKED级联阻塞汇总 + 总结 |
| 无FAILED，有BLOCKED | 异常用例完整分析 + 其他汇总 | 类型A异常触发用例完整6段落 + 类型B级联阻塞汇总表格 + 总结 |
| 全部PASSED | 简化报告 | 测试通过说明，无需详细分析 |

### BLOCKED用例分类（核心概念）

BLOCKED用例分为两类：

**类型A：异常触发用例**（引发阻塞的异常用例）
- 该用例本身执行时发生异常（进程崩溃、服务异常、超时等），导致后续用例无法执行
- **按正常工作流完整分析**（与FAILED相同，完整6段落）

**类型B：级联阻塞用例**（因异常未执行的用例）
- 因类型A用例的异常导致后续测试套件/用例无法执行，被标记为BLOCKED
- **汇总说明**，不需逐条分析

### BLOCKED用例定界原则

**类型A（异常触发用例）定界原则**：
| 异常原因 | 问题归属 | 说明 |
|---------|---------|------|
| 被测系统进程崩溃 | **系统侧问题** | cppcrash日志指向系统服务 |
| 被测API返回异常 | **系统侧问题** | API返回值与规范不符 |
| 测试用例逻辑错误 | **测试侧问题** | 断言条件错误、参数错误 |
| 测试超时 | 需进一步分析 | 可能是测试侧或系统侧 |

**类型B（级联阻塞用例）定界原则**：
| 阻塞原因 | 问题归属 | 说明 |
|---------|---------|------|
| 系统崩溃导致后续用例无法执行 | **系统侧问题**（继承类型A结论） | 崩溃后服务异常 |
| 应用冻结（appfreeze）导致套件中断 | **系统侧问题** | 应用被系统冻结 |
| 设备不支持某功能 | **测试侧问题** | 设备能力限制 |
| 前置条件不满足 | **测试侧问题** | 测试环境或用例设计问题 |

### BLOCKED类型识别方法

```bash
# 检查BLOCKED时间分布（连续多条=级联阻塞）
grep -n "BLOCKED" module_run.log

# 检查"missed"标记（套件中断标志）
grep -n "missed" module_run.log

# 检查崩溃日志
ls crash_log_*/ | grep -E "cppcrash|appfreeze"
```

### BLOCKED用例报告格式

**有FAILED + BLOCKED时**：
```markdown
## 一、hilog日志用例详情

### 1.1 [FAILED用例名称]（完整6段落分析）
...（同FAILED模板）

### 1.X 级联阻塞用例汇总

#### 1.X.1 阻塞概况

| 项目 | 内容 |
|------|------|
| 阻塞用例总数 | [总数]个 |
| 阻塞范围 | [套件名]第[N]条之后 + [其他套件]全部 |
| 阻塞触发点 | [异常用例名称]（参见1.Y节分析） |
| 阻塞原因 | [进程崩溃 / 应用冻结 / 设备不支持] |
| 问题归属 | **[系统侧/测试侧]问题**（继承异常用例结论） |

#### 1.X.2 阻塞用例分布

| 测试套件 | 套件总数 | 已执行 | BLOCKED | 阻塞原因 |
|---------|---------|--------|---------|---------|
| [套件名1] | [Total] | [N] | [M] | 第[N]条后套件中断 |
| [套件名2] | [Total] | 0 | [Total] | 套件未执行（前一套件异常） |
| **合计** | **[Total]** | **[N]** | **[M]** | |

#### 1.X.3 阻塞说明

**阻塞链分析**:
[异常用例]执行异常 → [套件]中断 → 后续套件未执行 → 总计N条阻塞

**处理建议**: 优先处理异常用例（参见1.Y节），修复后重跑验证

---

## 二、总结
...
```

**无FAILED，只有BLOCKED时**：
- 类型A异常触发用例完整6段落分析
- 类型B级联阻塞用例汇总表格
- 设备不支持类BLOCKED用例（如有）按独立模板分析

> BLOCKED类型B级联阻塞用例用汇总表格格式（非逐条6段落），见上方「有FAILED+BLOCKED时」的格式示例。

### 崩溃作为根因时的报告结构（2026-07-14新增）

> 当系统进程崩溃（如media_service）同时导致FAILED和BLOCKED时，按以下结构组织报告。

**识别条件**：
- crash_log目录存在cppcrash/appfreeze日志
- FAILED用例的失败原因为"错误码不匹配"或"服务异常"
- BLOCKED用例为级联阻塞（时间戳连续相同）

**报告结构**：
```markdown
## 一、hilog日志用例详情

### 1.1 [崩溃进程名]进程崩溃分析（根因）
（崩溃基本信息 + 崩溃时间线 + 崩溃调用栈 + 崩溃根因分析）
> 此节是后续所有FAILED和BLOCKED的根因，必须放在最前

### 1.2 [第一个FAILED用例]（完整6段落，引用1.1崩溃分析）
### 1.3 ~ 1.N [其他FAILED用例]（完整6段落，标注"同根因"）
### 1.N+1 级联阻塞用例汇总
（阻塞概况 + 阻塞用例分布 + 阻塞链分析）

## 二、总结
（问题分类：全部为系统侧 + 定界结论表格 + 建议流转）
```

**关键要求**：
- 崩溃分析节（1.1）必须包含崩溃时间线（多次崩溃时逐条列出，**时间必须精确，禁止 `00:34:15.XXX` 占位符**）
  - ⚠️ **时间戳格式（2026-07-15新增）**：崩溃时间线表格中的时间戳必须使用**全格式** `2026-06-30 00:34:15.847`（含年份），不支持短格式 `00:34:15.847`（不含年份），因为 validate_report.py 校验崩溃时间线完整性时需要全格式匹配
- 崩溃分析节必须包含**真实调用栈**（`#00 pc <addr> /system/lib64/xxx.so (FuncName+<offset>)` 至少3-4帧），不得只写 `进程 └── 函数()` 示意图
- 阻塞链分析必须展示：崩溃 → 套件中断 → 后续套件未执行 → 总计N条阻塞
- **BLOCKED必须完整统计**：用 `grep -n "missed" module_run.log` 核对，含「套件内未执行」(如 `52 tests in X had missed`) + 「整套件未执行」(如 `2 suites have missed`)，阻塞用例分布表须列出全部，禁止漏算套件内中断条数
- 定界结论中所有用例标注"问题归属：系统侧"
- 建议流转中说明"优先处理崩溃（1.1节），修复后重跑验证"

### 多根因报告结构（2026-07-15新增）

> 当存在**多个独立根因**时（如：系统服务崩溃导致部分FAILED + 测试代码缺陷导致appfreeze导致BLOCKED），按以下结构组织报告。

**识别条件**：
- FAILED和BLOCKED的根因不同（如：FAILED由系统崩溃导致，BLOCKED由测试侧appfreeze导致）
- 崩溃日志和appfreeze日志指向不同的问题归属
- 两个根因的发生时间不重叠或因果链独立

**报告结构**：
```markdown
## 一、hilog日志用例详情

### 1.1 [根因1：崩溃进程名]进程崩溃分析
（崩溃基本信息 + 崩溃时间线 + 崩溃调用栈 + 崩溃根因分析）
> 此节是后续FAILED用例（1.2~1.N）的根因

### 1.2 ~ 1.N [FAILED用例]（完整6段落，引用1.1崩溃分析，标注"同根因"）

### 1.N+1 [根因2：appfreeze/测试阻塞分析]（BLOCKED类型A，完整6段落）
（基本信息 + 时间窗提取 + 源码→领域证据链 + 关键日志 + 源码分析 + 问题定界）
> 此节是后续级联BLOCKED用例的根因，与1.1是**独立根因**

### 1.N+2 级联阻塞用例汇总（BLOCKED类型B）
（阻塞概况 + 阻塞用例分布 + 阻塞链分析，引用1.N+1的根因）

## 二、总结
（问题分类：分为系统侧和测试侧两类 + 定界结论表格分别标注归属 + 建议分别流转）
```

**关键要求**：
- 多根因报告中，每个根因分析节（1.1和1.N+1）必须独立完整，包含各自的证据链和定界
- FAILED用例引用1.1的根因（"同根因"），BLOCKED用例引用1.N+1的根因
- "二、总结"中定界结论表格须**分别标注**每个用例的问题归属（系统侧/测试侧）
- 建议流转须**分两条**：系统侧问题流转给系统团队，测试侧问题流转给测试团队
- 判定多根因的依据：两个根因的崩溃栈/调用栈不同、发生时间不重叠或因果链独立

### 标准格式

```markdown
# XTS测试问题分析报告

**报告日期**: YYYY-MM-DD  
**测试套件**: TestsuiteName  
**设备SN**: FMR0123417000740  
**子系统**: SubsystemName

---

## 一、hilog日志用例详情

### 1.1 SUB_Subsystem_Module_TestCase_0100

#### 1.1.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | SUB_Subsystem_Module_TestCase_0100 |
| 测试套件 | TestsuiteName |
| 执行序号 | 1/N |
| 执行结果 | FAILED |
| 消耗时间 | 1ms |
| 所在日志（hilog） | hilog.050.20260626-160128.txt |

#### 1.1.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.050.20260626-160128.txt |
| 起始时间 | 06-26 16:01:29.239 |
| 起始行号 | 4000 |
| 结束时间 | 06-26 16:01:29.310 |
| 结束行号 | 4662 |
| 时间来源 | hilog [Hypium] 标记（设备时间） |

#### 1.1.3 源码→领域证据链

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

#### 1.1.4 关键日志片段

**所在日志**: hilog.050.20260626-160128.txt（行4266-4317）

**分层过滤结果**:
- 主分析集（domain匹配）：[N]行
- P1扩展（同PID/TID）：[X]行  
- P2扩展（同PID不同TID）：[Y]行
- P3扩展（位置窗口±20行）：[Z]行

**关键证据**:
```
[主] 行4299: [DomainTag] TestCase_0100 start
[主] 行4304: [DomainTag] TestCase_0100 success
[P1] 行4317: [Hypium][failDetail]expect undefined equals expected_value
```

#### 1.1.5 源码定位与分析

**源码位置**: `/home/user/code/subsystem/test/SourceFile.test.ets:80-105`

> ⚠️ **强制要求：源码位置必须使用绝对路径，禁止使用相对路径或仅文件名**
>
> 📖 **如何定位源码绝对路径？详见**：
> - [FailureAndSource.md Step 2.5：源码定位](../L0_PreAnalysis/FailureAndSource.md)（定位**具体测试文件**，4步流程）
> - [FailureAndSource.md Step 2.5：源码定位](../L0_PreAnalysis/FailureAndSource.md)（定位**测试套件目录**，基于BUILD.gn）
> - 或使用脚本：`python3 scripts/locate_xts_source.py --testcase "xxx" --root "$OH_ROOT"`

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

#### 1.1.6 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | API功能缺陷 |
| 问题归属 | **系统侧问题** |
| 影响范围 | Subsystem子系统 - Module |
| 定界依据 | 关键字'keyword'匹配数据库规则 → Domain领域 |
| 归属判定 | **Subsystem子系统问题** |

---

## BLOCKED用例完整示例

### 示例场景：设备不支持某功能导致用例阻塞

```markdown
### 1.1 testOHCaptureSessionAddSecureOutput0200

#### 1.1.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | testOHCaptureSessionAddSecureOutput0200 |
| 测试套件 | SecureCameraErrorCodeTest |
| 执行序号 | 1/8 |
| 执行结果 | BLOCKED |
| 消耗时间 | 0ms |
| 所在日志（hilog） | hilog.539.20260630-023904.txt |
| BLOCKED原因 | 设备不支持SECURE_PHOTO功能 |

#### 1.1.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.539.20260630-023904.txt |
| 起始时间 | 06-30 02:39:04.240 |
| 起始行号 | 229 |
| 结束时间 | 06-30 02:39:04.586 |
| 结束行号 | 1417 |
| 时间来源 | hilog [Listener] 标记（PC时间） |

#### 1.1.3 源码→领域证据链

| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| oHCameraManagerGetSupportedSceneModes | MultiMedia | C002B[0-9a-fA-F]/ | 229 | 02:39:04.240 |

**证据链追溯**:
```
失败用例源码(SecureCameraErrorCodeTest.test.ets)
    │ import cameraObj from 'libentry.so'
    ▼
NAPI接口 → 子系统
    │ libentry.so → Camera NDK → MultiMedia子系统
    ▼
子系统 → hilog domain
    │ "MultiMedia" → C002Bxx
    ▼
精准日志过滤
    │ 过滤域：C002B[0-9a-fA-F]/
    ▼
日志切片 → 行229-1417
```

#### 1.1.4 关键日志片段

**所在日志**: hilog.539.20260630-023904.txt（行229-1417）

**分层过滤结果**:
- 主分析集（domain匹配）：0行（设备不支持SECURE_PHOTO）
- P3扩展（位置窗口±20行）：40行

**关键证据**:
```
[P3] 行229: 06-30 02:39:04.240 45708 45708 I A03200/com.example.camerandk/CAMERA_TAGLOG: isSupported_NORMAL_PHOTO: 1, isSupported_NORMAL_VIDEO: 1, isSupported_NSECURE_PHOTO: 0.
```

> ⚠️ 设备能力检查结果：isSupported_NSECURE_PHOTO: 0（设备不支持安全相机）

#### 1.1.5 源码定位与分析

**源码位置**: `/home/user/code/multimedia/camera/test/SecureCameraErrorCodeTest.test.ets:341-362`

> ⚠️ **强制要求：源码位置必须使用绝对路径，禁止使用相对路径或仅文件名**
> 📖 定位流程见 [FailureAndSource.md Step 2.5](../L0_PreAnalysis/FailureAndSource.md)

**源码片段**:
```typescript
it('testOHCaptureSessionAddSecureOutput0200', Level.LEVEL0, () => {
  let supportedSceneModes = getSupportedSceneModes(Parameter_Setting.SET_CAMERA_FRONT_FOR_SECURE_PHOTO);
  if (!supportedSceneModes.isSecurePhoto) {
    console.error(TAG+"SECURE_PHOTO is not supported");  // ← 设备不支持时执行此分支
    expect(supportedSceneModes.isSecurePhoto).assertEqual(false);  // ← 断言通过
  } else {
    // ... SECURE_PHOTO测试逻辑（设备不支持时不执行）
  }
})
```

**源码分析**:
1. **测试逻辑**：检查设备是否支持SECURE_PHOTO场景模式
2. **预期行为**：如果设备不支持SECURE_PHOTO，执行断言检查
3. **实际行为**：设备返回`isSupported_NSECURE_PHOTO: 0`，断言通过
4. **BLOCKED原因**：Hypium框架将"设备不支持"的情况标记为BLOCKED

#### 1.1.6 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | 测试阻塞（设备功能不支持） |
| 问题归属 | **测试侧问题** |
| 影响范围 | multimedia/camera - SecureCamera功能 |
| 定界依据 | 设备不支持SECURE_PHOTO（isSupported_NSECURE_PHOTO: 0） |
| 归属判定 | **测试侧问题** - 设备能力限制 |
```

---

### 1.2 SUB_Subsystem_Module_TestCase_0200 [同根因用例]

#### 1.2.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | SUB_Subsystem_Module_TestCase_0200 |
| 测试套件 | TestsuiteName |
| 执行序号 | 2/N |
| 执行结果 | FAILED |
| 消耗时间 | 0ms |
| 所在日志（hilog） | hilog.050.20260626-160128.txt |

#### 1.2.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.050.20260626-160128.txt |
| 起始时间 | 06-26 16:01:29.308 |
| 起始行号 | 4375 |
| 结束时间 | 06-26 16:01:29.309 |
| 结束行号 | 4445 |
| 时间来源 | hilog [Hypium] 标记（设备时间） |

#### 1.2.3 根因继承

**同根因说明**: 与用例 1.1 相同，API `method()` 在特定条件下未返回预期结果。

**差异点**: 参数差异，但失败根因与 1.1 一致。

#### 1.2.4 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | API功能缺陷（同根因） |
| 问题归属 | **系统侧问题** |
| 影响范围 | Subsystem子系统 - Module |
| 归属判定 | **Subsystem子系统问题**（继承1.1结论）

---

## 二、总结

### 2.1 问题分类汇总

#### 测试侧问题

**问题数量**: 0个

**问题列表**: 无

**说明**: 本次分析未发现测试侧问题。

#### 系统侧问题

**问题数量**: 2个

**问题列表**:
| 序号 | 用例名 | 问题类型 | 影响子系统 |
|------|--------|---------|-----------|
| 1 | SUB_Subsystem_Module_TestCase_0100 | API功能缺陷 | Subsystem |
| 2 | SUB_Subsystem_Module_TestCase_0200 | API功能缺陷（同根因） | Subsystem |

**共性问题**: 
- Module 的多个 API 在特定条件下未返回预期结果
- 导致测试用例预期行为失效

**根本原因**:
- API 实现未正确处理特定条件
- 未按规范返回预期值或错误码

### 2.2 定界结论

| 用例名 | 问题类型 | 问题归属 | 归属子系统 | 归属领域 | 流转建议 |
|--------|---------|---------|-----------|---------|---------|
| SUB_Subsystem_Module_TestCase_0100 | API功能缺陷 | 系统侧 | Subsystem | Domain | 流转至 Subsystem 子系统责任人 |
| SUB_Subsystem_Module_TestCase_0200 | API功能缺陷 | 系统侧 | Subsystem | Domain | 流转至 Subsystem 子系统责任人（同根因） |

**定界依据**:
1. API调用成功但未返回预期结果
2. 属于 API 实现问题而非测试环境问题
3. 日志证据链完整，可追溯至具体子系统

### 2.3 建议流转

#### 系统侧问题流转

**主责任人**: Subsystem 子系统 - Module 模块  
**问题类型**: API 功能缺陷  
**修复建议**: 
- 检查 API 实现，确保在特定条件下正确返回预期结果
- 验证错误处理逻辑的一致性

#### 测试侧问题流转

**主责任人**: 无（本次未发现测试侧问题）  
**说明**: 如后续发现测试侧问题，需流转至测试用例维护责任人

---

**报告生成时间**: YYYY-MM-DD HH:MM  
**报告生成工具**: ohos-issue-xts-log-analysis skill  
**数据来源**: hilog.txt + module_run.log + 源码验证
```

---

## 问题分类标准

### 测试侧问题

**判定标准**：问题根因在测试代码或测试环境，而非被测系统。

**常见类型**：
| 问题类型 | 说明 | 示例 |
|---------|------|------|
| 用例逻辑错误 | 测试逻辑不符合测试规范 | 未正确初始化测试环境 |
| 断言错误 | expect断言条件错误 | 断言值与API规范不一致 |
| 环境配置错误 | 测试环境配置不当 | 设备权限未配置 |
| 测试框架问题 | Hypium框架缺陷 | 框架API返回异常 |
| 测试参数错误 | 测试参数不符合API规范 | 参数类型错误 |

**定界特征**：
- API调用本身成功，返回值符合规范
- 但测试用例的预期值或断言条件错误
- 或测试环境配置导致API行为异常

### 系统侧问题

**判定标准**：问题根因在被测系统（API实现、组件、服务等）。

**常见类型**：
| 问题类型 | 说明 | 示例 |
|---------|------|------|
| API实现缺陷 | API未按规范实现 | 返回值与文档不符 |
| 组件功能异常 | 组件功能未正确实现 | UI组件渲染异常 |
| 系统服务问题 | 系统服务异常 | 后台服务崩溃 |
| 内核问题 | 内核层面问题 | 内存泄漏、权限问题 |

**定界特征**：
- API调用失败或返回值不符合规范
- 日志证据指向特定子系统/组件
- 非测试环境配置问题

---

