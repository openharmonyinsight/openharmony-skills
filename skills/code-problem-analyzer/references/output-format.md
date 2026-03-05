# 输出格式规范和示例

## 输出格式原则

### 1. 清晰性

- 使用清晰的标题层级
- 关键信息使用粗体标记
- 代码使用代码块格式
- 流程使用 ASCII 图或箭头符号

### 2. 结构化

- 按逻辑顺序组织内容
- 使用列表和表格展示结构化信息
- 相关信息分组展示

### 3. 可操作性

- 提供具体的操作步骤
- 指出需要用户做什么
- 给出验证方法

### 4. 精确性

- 代码引用包含文件名和行号
- 函数名使用准确
- 变量名使用准确

## 标准输出格式

### 格式1：完整分析结果

适用于：需要详细分析、有多个可能根因、需要用户确认的情况

```
## 问题分析结果

### 问题背景

**预期行为**: [用户期望的行为]
**实际现象**: [实际发生的行为]

### 所有可能的流程

#### 流程1：[流程名称]

**描述**: [流程的详细描述]

**执行路径**:
1. [步骤1描述]
   - 文件:file.cpp:行号 - [关键代码片段]
   - 文件:file.cpp:行号 - [关键代码片段]

2. [步骤2描述]
   - 文件:file.cpp:行号 - [关键代码片段]

3. [步骤3描述]
   - 文件:file.cpp:行号 - [关键代码片段]

#### 流程2：[流程名称]

**描述**: [流程的详细描述]

**执行路径**:
1. [步骤1描述]
   - 文件:file.cpp:行号 - [关键代码片段]

2. [步骤2描述]
   - 文件:file.cpp:行号 - [关键代码片段]

### 最有可能的根因

**根因**: [明确的根因描述]

**原因解释**:
1. [解释点1]
2. [解释点2]
3. [解释点3]

**关键代码位置**:
- file.cpp:行号 - [代码片段说明]
- file.cpp:行号 - [代码片段说明]

**证据链**:
1. [证据1] - [证据来源]
2. [证据2] - [证据来源]
3. [证据3] - [证据来源]

**建议的解决方案**:
1. [解决方案1]
   - 操作步骤：[具体步骤]
   - 验证方法：[如何验证]

2. [解决方案2]
   - 操作步骤：[具体步骤]
   - 验证方法：[如何验证]

### 需要进一步确认

[说明需要用户提供什么信息或做什么操作]

**建议操作**:
- [操作1]
- [操作2]
```

### 格式2：简洁分析结果

适用于：问题明确、根因确定、不需要用户确认的情况

```
## 问题分析结果

### 最有可能的根因

**根因**: [明确的根因描述]

**原因**: [简短解释，1-2句话]

**关键代码位置**: file.cpp:行号

**解决方案**: [具体操作步骤]

**验证方法**: [如何验证解决方案有效]
```

### 格式3：多根因分析结果

适用于：存在多个可能的根因，需要用户帮助确定

```
## 问题分析结果

### 可能的根因分析

我发现了 [数量] 个可能导致问题的原因：

#### 根因1：[根因描述]

**可能性**: 高/中/低

**原因解释**:
- [解释点1]
- [解释点2]

**关键代码位置**:
- file.cpp:行号

**证据**: [支持这个根因的证据]

#### 根因2：[根因描述]

**可能性**: 高/中/低

**原因解释**:
- [解释点1]
- [解释点2]

**关键代码位置**:
- file.cpp:行号

**证据**: [支持这个根因的证据]

### 需要进一步确认

为了确定最可能的根因，请提供以下信息：

[使用 question 工具询问用户]
```

## 输出示例

### 示例1：调试模式问题分析

```
## 问题分析结果

### 问题背景

**预期行为**: 开发者执行 `aa start -a EntryAbility -b com.huawei.idetest01 -m entry`（无 -D 参数）时，应用正常启动，不进入调试模式
**实际现象**: 应用自动进入调试模式，isStartWithDebug=true

### 所有可能的流程

#### 流程1：通过 -D 参数设置调试

**描述**: 用户使用 aa start -D 命令时，显式设置调试标志

**执行路径**:
1. aa 工具解析命令行参数
   - tools/aa/src/ability_command.cpp:2117-2121 - `case 'D': isDebugApp = true;`
   - tools/aa/src/ability_command.cpp:2183-2184 - `want.SetParam("debugApp", isDebugApp);`

2. AMS 接收并处理 Want
   - services/appmgr/src/app_mgr_service_inner.cpp:3971-3974 - 检测 debugApp 参数并调用 ProcessAppDebug

3. 设置调试状态
   - services/appmgr/src/app_mgr_service_inner.cpp:4868-4871 - `appRecord->SetDebugApp(true);`

#### 流程2：通过等待调试列表自动设置调试

**描述**: 应用在等待调试列表中时，启动时自动进入调试模式

**执行路径**:
1. AbilityRecord 构造时检查等待调试状态
   - services/abilitymgr/src/ability_record.cpp:152 - `SetDebugAppByWaitingDebugFlag();`

2. 检查是否满足调试条件
   - services/abilitymgr/src/ability_record.cpp:3069-3074 - 检查应用是调试版本、开发者模式开启

3. 检查应用是否在等待调试列表中
   - services/abilitymgr/src/ability_record.cpp:3076-3086 - 调用 IsWaitingDebugApp
   - services/appmgr/src/app_mgr_service_inner.cpp:8695-8713 - 检查 waitingDebugBundleList_

4. 自动设置 debugApp=true
   - services/abilitymgr/src/ability_record.cpp:3080 - `want_.SetParam(AbilityConfig::DEBUG_APP, true);`

5. StartAbility 检测到 debugApp 并进入调试
   - services/appmgr/src/app_mgr_service_inner.cpp:3971-3974 - 检测并调用 ProcessAppDebug

### 最有可能的根因

**根因**: 应用被添加到了等待调试列表中（waitingDebugBundleList_），导致启动时自动进入调试模式

**原因解释**:
1. 应用满足调试条件：是调试版本（applicationInfo.debug=true）、开发者模式开启
2. 应用在 waitingDebugBundleList_ 中，IsWaitingDebugApp 返回 true
3. AbilityRecordable 构造时自动调用 SetDebugAppByWaitingDebugFlag
4. 该函数检测到应用在等待调试列表中，自动设置 want_.SetParam("debugApp", true)
5. StartAbility 检测到 debugApp=true，调用 ProcessAppDebug 进入调试模式

**关键代码位置**:
- services/abilitymgr/src/ability_record.cpp:152 - 构造函数调用 SetDebugAppByWaitingDebugFlag
- services/abilitymgr/src/ability_record.cpp:3076-3086 - 检查等待调试列表并设置 debugApp
- services/appmgr/src/app_mgr_service_inner.cpp:3971-3974 - 检测 debugApp 并调用 ProcessAppDebug

**证据链**:
1. 用户没有使用 -D 参数 - 命令行分析
2. 应用自动进入调试模式 - 用户报告
3. 代码中有等待调试列表机制 - 代码分析
4. 该机制会在启动时自动设置 debugApp - 代码分析

**建议的解决方案**:
1. 取消等待调试状态
   - 操作步骤：执行 `aa appdebug cancel com.huawei.idetest01`
   - 验证方法：执行 `aa appdebug get` 确认应用不在列表中

2. 清空所有等待调试的应用
   - 操作步骤：执行 `aa appdebug cancel`
   - 验证方法：执行 `aa appdebug get` 确认列表为空

3. 检查是否有其他工具或脚本自动添加应用到等待调试列表
   - 操作步骤：检查 IDE、调试工具、自动化脚本
   - 验证方法：观察应用是否再次被添加到列表中
```

### 示例2：简洁分析结果

```
## 问题分析结果

### 最有可能的根因

**根因**: 应用被添加到了等待调试列表中，导致启动时自动进入调试模式

**原因**: 即使没有 -D 参数，只要应用在 waitingDebugBundleList_ 中，AbilityRecord 构造时会自动设置 debugApp=true

**关键代码位置**: services/abilitymgr/src/ability_record.cpp:3076-3086

**解决方案**: 执行 `aa appdebug cancel com.huawei.idetest01` 取消等待调试状态

**验证方法**: 执行 `aa appdebug get` 确认应用不在列表中，然后重新启动应用验证
```

### 示例3：多根因分析结果

```
## 问题分析结果

### 可能的根因分析

我发现了 2 个可能导致应用崩溃的原因：

#### 根因1：空指针解引用

**可能性**: 高

**原因解释**:
- services/appmgr/src/app_mgr_service_inner.cpp:1234 - appRecord 可能为 nullptr
- 代码中没有检查 appRecord 是否为空就直接使用
- 在某些异常情况下（如应用启动失败），appRecord 可能未创建

**关键代码位置**:
- services/appmgr/src/app_mgr_service_inner.cpp:1234 - `appRecord->LaunchAbility(ability);`

**证据**: 崩溃堆栈显示在 app_mgr_service_inner.cpp:1234 处访问空指针

#### 根因2：资源未初始化

**可能性**: 中

**原因解释**:
- services/appmgr/src/app_mgr_service_inner.cpp:1200 - ability 对象可能未完全初始化
- LaunchAbility 调用时，ability 的某些资源可能未准备好
- 在快速启动场景下，初始化可能未完成

**关键代码位置**:
- services/appmgr/src/app_mgr_service_inner.cpp:1200 - `auto ability = CreateAbility(...);`

**证据**: 崩溃发生在资源访问操作中

### 需要进一步确认

为了确定最可能的根因，请提供以下信息：

[使用 question 工具]
```

## 流程图格式

### 格式1：线性流程

```
入口点 → 步骤1 → 步骤2 → 步骤3 → 结果
```

### 格式2：分支流程

```
入口点
├─ 条件A → 分支A → 结果A
├─ 条件B → 分支B → 结果B
└─ 条件C → 分支C → 结果C
```

### 格式3：嵌套流程

```
入口点
├─ 步骤1
│  ├─ 子步骤1.1
│  └─ 子步骤1.2
├─ 步骤2
│  └─ 子步骤2.1
└─ 步骤3
```

## 代码引用格式

### 格式1：单行引用

```
文件:file.cpp:行号 - [代码片段说明)
```

### 格式2：多行引用

```
文件:file.cpp:行号-行号 - [代码片段说明)
```

### 格式3：带代码片段的引用

```
文件:file.cpp:行号
```cpp
// 代码片段
if (condition) {
    action();
}
```
```

## 表格格式

### 格式1：简单表格

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 值1 | 值2 | 值3 |
| 值4 | 值5 | 值6 |

### 格式2：带说明的表格

| 根因 | 可能性 | 证据 |
|------|--------|------|
| 根因1 | 高 | 证据描述 |
| 根因2 | 中 | 证据描述 |

## 列表格式

### 格式1：有序列表

1. 步骤1
2. 步骤2
3. 步骤3

### 格式2：无序列表

- 要点1
- 要点2
- 要点3

### 格式3：嵌套列表

1. 主要步骤
   - 子步骤1
   - 子步骤2
2. 主要步骤
   - 子步骤1

## 代码块格式

### 格式1：单行代码

`code`

### 格式2：多行代码

```cpp
// 代码
int main() {
    return 0;
}
```

### 格式3：带语言标识的代码块

```cpp
// C++ 代码
```

```bash
# Bash 命令
```

```json
// JSON 数据
```

## 强调格式

### 格式1：粗体强调

**重要信息**

### 格式2：斜体强调

*补充说明*

### 格式3：代码强调

`变量名`、`函数名()`

## 链接格式

### 格式1：内部引用

参见 [章节名称](#章节名称)

### 格式2：文件引用

参见 [文件名](path/to/file.md)

## 注意事项

1. **一致性**: 在整个分析过程中使用一致的格式
2. **简洁性**: 避免冗余信息，保持输出简洁
3. **准确性**: 确保所有代码引用准确无误
4. **可读性**: 使用适当的格式增强可读性
5. **完整性**: 确保输出包含所有必要信息
