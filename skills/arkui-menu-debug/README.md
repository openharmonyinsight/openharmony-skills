# Menu Debug Skill

Menu组件问题诊断和日志增强技能，提供系统化的Menu问题排查方案。

## 功能概述

本技能提供：
1. **问题分类** - 将Menu问题归类为4大类：宽度、子窗口、布局、崩溃
2. **定位指南** - 精确的代码位置和关键变量
3. **日志增强模板** - 基于问题场景的预定义日志补丁
4. **分析方法** - 系统化的问题排查流程

## 使用场景

### 何时使用此技能

当你遇到以下问题时：

- ✅ Menu宽度为0或异常
- ✅ "recreate subwindow"日志频繁出现
- ✅ 快速打开Menu时Menu显示异常
- ✅ Menu位置计算错误
- ✅ Menu子窗口创建/销毁问题
- ✅ Menu组件崩溃或不稳定

### 典型问题示例

**问题1**: 快速连续打开Menu导致宽度为0
```
症状：Menu宽度显示为0
日志：[ACE_SUB_WINDOW] recreate subwindow
原因：子窗口recreate时，异步窗口初始化未完成
代码位置：menu_layout_algorithm.cpp:941
```

**问题2**: Menu位置偏移
```
症状：Menu显示位置错误
原因：窗口rect计算错误或offset计算问题
代码位置：menu_layout_algorithm.cpp:3611
```

**问题3**: 子窗口频繁重建
```
症状：每次打开Menu都打印"recreate subwindow"
原因：DETACHING状态判断逻辑问题
代码位置：subwindow_manager.cpp:1965
```

## 工作流程

### 阶段1: 问题识别

根据用户提供的问题描述，识别问题类别：

```bash
# 用户提问示例映射
"Menu宽度为0" → Width Issues
"快速打开Menu问题" → Subwindow Recreation Issues
"Menu位置不对" → Layout Issues
"Menu闪退" → Crash/Instability Issues
```

### 阶段2: 代码定位

根据问题类别，定位关键代码位置：

| 问题类别 | 关键文件 | 关键函数 |
|---------|---------|---------|
| Width Issues | menu_layout_algorithm.cpp:920-966 | UpdateChildConstraintByDevice |
| Subwindow Issues | subwindow_manager.cpp:1954-1987 | GetOrCreateMenuSubWindow |
| Layout Issues | menu_layout_algorithm.cpp:3611-3659 | GetMenuWindowRectInfo |
| Crash Issues | menu_pattern.cpp / menu_wrapper_pattern.cpp | OnModifyDone / lifecycle methods |

### 阶段3: 日志补丁生成

基于问题场景，提供针对性的日志增强代码。

**示例：宽度为0问题的日志增强**

```cpp
// 在 menu_layout_algorithm.cpp:941 附近添加
TAG_LOGI(AceLogTag::ACE_MENU,
    "UpdateChildConstraintByDevice: displayWidth=%{public}f, menuMaxWidthRatio=%{public}f",
    displayWidth, menuMaxWidthRatio);
```

### 阶段4: 应用和分析

1. 应用日志补丁到源文件
2. 重新编译ace_engine组件
3. 复现问题并收集日志
4. 分析日志定位根因
5. 实现修复方案

## 关键日志标签

### OpenHarmony ACE Engine Log Tags

| 日志标签 | 用途 | 过滤命令 |
|---------|------|----------|
| `ACE_MENU` | Menu组件相关 | `grep ACE_MENU xxx.log` |
| `ACE_SUB_WINDOW` | 子窗口管理 | `grep ACE_SUB_WINDOW xxx.log` |
| `ACE_OVERLAY` | Overlay管理 | `grep ACE_OVERLAY xxx.log` |
| `ACE_MENU_TYPE` | Menu类型信息 | `grep ACE_MENU_TYPE xxx.log` |

### 日志级别

- **TAG_LOGI** - INFO级别，正常流程信息
- **TAG_LOGW** - WARN级别，异常但可恢复的情况
- **TAG_LOGE** - ERROR级别，错误和失败情况

## 快速参考

### 常见问题排查步骤

**场景1: Menu宽度为0**

```bash
# 1. 过滤相关日志
cat xxx.log | grep -E "recreate subwindow|DisplayWindowRectInfo.*width.*0"

# 2. 检查时序
cat xxx.log | grep -E "ShowMenuNG|HideMenuNG|UpdateChildConstraintByDevice" | head -20

# 3. 分析PipelineContext来源
# 查看是否使用GetMainPipelineContext还是GetContext
```

**场景2: 子窗口频繁recreate**

```bash
# 1. 统计recreate次数
cat xxx.log | grep "recreate subwindow" | wc -l

# 2. 查看状态转换
cat xxx.log | grep "MenuWindowState" | head -20

# 3. 分析reuse参数
cat xxx.log | grep "reuse=" | head -10
```

**场景3: Menu布局异常**

```bash
# 1. 查看窗口rect计算
cat xxx.log | grep "GetMenuWindowRectInfo"

# 2. 查看offset计算
cat xxx.log | grep -E "targetOffset_|menuOffset"

# 3. 查看菜单类型
cat xxx.log | grep "IsMenu\|IsContextMenu\|IsSubMenu"
```

## 与其他技能的集成

本技能与以下技能协同工作：

- **compile-analysis**: 分析Menu代码编译性能问题
- **build-error-analyzer**: 处理Menu修改导致的编译错误
- **tdd**: 为Menu修复编写测试用例

## 技能输出格式

### 日志补丁输出

技能应该输出：

```markdown
## 建议的日志增强

### 文件：frameworks/core/components_ng/pattern/menu/menu_layout_algorithm.cpp
### 位置：第941行附近

```cpp
void MenuLayoutAlgorithm::UpdateChildConstraintByDevice(...)
{
    // ... 现有代码 ...

    // 【新增日志】记录窗口宽度获取
    auto displayWidth = pipeline->GetDisplayWindowRectInfo().Width();
    TAG_LOGI(AceLogTag::ACE_MENU,
        "UpdateChildConstraintByDevice: displayWidth=%{public}f",
        displayWidth);

    // ... 后续代码 ...
}
```

### 分析说明
- 如果`displayWidth=0`，说明异步窗口初始化未完成
- 如果频繁出现此日志，说明存在时序竞争
```

### 问题定位建议

```markdown
## 排查方向

1. **检查PipelineContext来源**
   - 当前使用：`host->GetContext()`
   - 建议使用：`DialogManager::GetMainPipelineContext(host)`
   - 代码位置：menu_layout_algorithm.cpp:931

2. **验证子窗口初始化时序**
   - 检查InitContainer()完成后displayWindowRectInfo是否设置
   - 查看UpdateViewportConfig回调执行时机

3. **检查recreate条件**
   - 代码位置：subwindow_manager.cpp:1964
   - 条件：`subwindow->GetDetachState() == MenuWindowState::DETACHING`
```

## 示例使用

### 示例1: 用户报告"Menu宽度为0"

**用户输入**:
```
快速打开Menu时，Menu宽度显示为0，日志中看到"recreate subwindow"
```

**技能响应**:

1. **问题分类** → Width Issues + Subwindow Recreation Issues

2. **提供排查方向**:
   - 检查displayWindowRectInfo.Width()返回值
   - 分析PipelineContext来源（主窗口vs子窗口）
   - 验证UpdateViewportConfig异步回调时机

3. **生成日志补丁**:
   - 在UpdateChildConstraintByDevice函数添加displayWidth日志
   - 在GetOrCreateMenuSubWindow函数添加state和reuse参数日志
   - 在GetMenuWindowRectInfo函数添加返回值日志

4. **提供分析命令**:
   ```bash
   # 过滤关键日志
   grep -E "recreate subwindow|displayWidth" xxx.log
   ```

### 示例2: 用户报告"Menu位置错误"

**用户输入**:
```
Menu显示位置与目标组件不对应，有时偏上，有时偏下
```

**技能响应**:

1. **问题分类** → Layout Issues

2. **提供排查方向**:
   - 检查GetMenuWindowRectInfo返回值
   - 验证targetOffset_和targetSize_计算
   - 检查设备类型（折叠屏vs普通设备）

3. **生成日志补丁**:
   - 记录menuWindowRect的所有字段
   - 记录offset计算过程
   - 记录placement类型

4. **提供分析命令**:
   ```bash
   # 查看窗口rect和offset
   grep -E "MenuWindowRect|targetOffset|placement" xxx.log
   ```

## 最佳实践

### 日志增强原则

**DO（推荐）**:
- ✅ 添加上下文 - 记录相关变量值
- ✅ 记录状态转换 - 旧状态 → 新状态
- ✅ 使用适当的日志级别
- ✅ 包含标识符 - 节点ID、实例ID
- ✅ 记录计算 - 输入值和结果

**DON'T（不推荐）**:
- ❌ 无上下文日志 - 仅记录"进入函数"
- ❌ 过度日志 - 在循环中过多日志
- ❌ 记录敏感数据 - 用户信息、token
- ❌ 推测 - 只记录实际值

### 补丁生成准则

1. **最小化修改** - 只添加日志，不修改逻辑
2. **保持格式** - 遵循现有代码风格
3. **使用现有宏** - 使用正确的TAG_LOGI/W/E
4. **验证编译** - 应用前验证语法
5. **文档化变更** - 记录每个日志的内容和原因

## 限制和约束

### 技能限制

- ⚠️ 所有日志补丁必须基于实际代码分析
- ⚠️ 不推测或假设代码行为
- ⚠️ 只提供日志增强，不直接修复业务逻辑
- ⚠️ 遵循OpenHarmony日志标准

### 适用范围

- **组件**: Menu组件及相关（MenuWrapper, MenuItem, MenuLayout等）
- **平台**: OpenHarmony ACE Engine
- **代码库**: foundation/arkui/ace_engine

## 更新历史

- **v0.1.0** (2026-02-10): 初始版本
  - 支持4大类Menu问题诊断
  - 提供系统化排查流程
  - 包含日志增强模板和示例
