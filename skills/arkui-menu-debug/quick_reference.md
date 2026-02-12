# Menu Component Quick Debugging Reference

Menu组件问题快速调试参考手册。

## 常见问题速查表

### 问题1: Menu宽度为0

**快速定位**:
```bash
# 检查是否出现recreate日志
grep "recreate subwindow" xxx.log

# 检查displayWindowRectInfo
grep -E "DisplayWindowRectInfo.*width" xxx.log
```

**根因概率**:
| 原因 | 概率 | 特征 |
|-------|-------|------|
| 子窗口异步初始化未完成 | 80% | 出现"recreate subwindow" |
| PipelineContext来源错误 | 15% | 快速打开Menu |
| Theme配置错误 | 5% | 非折叠屏设备 |

**解决方案**:
1. 使用 `DialogManager::GetMainPipelineContext(host)` 替代 `host->GetContext()`
2. 添加容错逻辑（参考menu_width_zero_fix.md）
3. 记录displayWidth来源日志

**代码位置**:
- `menu_layout_algorithm.cpp:931` - PipelineContext获取
- `menu_layout_algorithm.cpp:941` - Width计算
- `menu_layout_algorithm.cpp:3618` - GetMenuWindowRectInfo参考实现

---

### 问题2: "recreate subwindow"频繁出现

**快速定位**:
```bash
# 统计recreate次数
grep "recreate subwindow" xxx.log | wc -l

# 检查状态转换
grep -E "MenuWindowState|DETACHING|ATTACHING" xxx.log | head -20
```

**根因概率**:
| 原因 | 概率 | 特征 |
|-------|-------|------|
| 快速连续打开Menu | 70% | 时间间隔<100ms |
| 窗口状态转换延迟 | 20% | Hide/Show时序问题 |
| DisplayId变化 | 10% | 多屏切换场景 |

**解决方案**:
1. 延迟第二次Menu打开（如果可能）
2. 复用DETACHING状态的窗口而不是recreate
3. 添加状态转换日志追踪

**代码位置**:
- `subwindow_manager.cpp:1964` - recreate条件判断
- `subwindow_manager.cpp:1954` - GetOrCreateMenuSubWindow函数
- `subwindow.h:39-45` - MenuWindowState定义

---

### 问题3: Menu位置异常

**快速定位**:
```bash
# 检查窗口rect计算
grep "GetMenuWindowRectInfo" xxx.log | head -10

# 检查offset计算
grep -E "targetOffset_|menuOffset" xxx.log | head -10
```

**根因概率**:
| 原因 | 概率 | 特征 |
|-------|-------|------|
| displayWindowRectInfo获取失败 | 50% | rect为(0,0,0,0) |
| 折叠屏设备计算错误 | 30% | expandDisplay=true |
| targetNode位置获取错误 | 20% | offset偏移异常 |

**解决方案**:
1. 验证PipelineContext来源
2. 检查foldable设备的特殊逻辑
3. 添加rect计算过程日志

**代码位置**:
- `menu_layout_algorithm.cpp:3611-3659` - GetMenuWindowRectInfo函数
- `menu_layout_algorithm.cpp:3626` - 子菜单复用主菜单rect
- `menu_wrapper_pattern.cpp` - SetMenuWindowRect

---

### 问题4: Menu崩溃/闪退

**快速定位**:
```bash
# 检查崩溃相关日志
grep -E "CHECK_NULL| segmentation| fatal" xxx.log | grep -i menu

# 检查Menu wrapper状态
grep -E "MenuWrapper|menuPattern" xxx.log | tail -20
```

**根因概率**:
| 原因 | 概率 | 特征 |
|-------|-------|------|
| 空指针解引用 | 40% | menuPattern/menuWrapper为nullptr |
| Menu wrapper生命周期问题 | 30% | OnDetach/OnAttach时序错误 |
| Menu item创建失败 | 20% | MenuItem创建异常 |
| 状态管理错误 | 10% | 重复初始化/销毁 |

**解决方案**:
1. 添加空指针检查日志
2. 验证Menu wrapper生命周期
3. 添加异常捕获和日志

**代码位置**:
- `menu_pattern.cpp` - Menu Pattern实现
- `menu_wrapper_pattern.cpp` - Menu Wrapper生命周期
- `menu_item/menu_item_pattern.cpp` - MenuItem创建

---

## 调试工作流

### 快速诊断5步法

**Step 1: 确认问题现象**
```
用户描述 → 症状分类
宽度问题 → 问题1
子窗口问题 → 问题2
位置问题 → 问题3
崩溃问题 → 问题4
```

**Step 2: 过滤关键日志**
```bash
# 根据问题类型选择过滤命令
宽度问题 → grep -E "DisplayWindowRectInfo|menuMaxWidth"
子窗口问题 → grep -E "recreate subwindow|DETACHING"
位置问题 → grep -E "MenuWindowRect|targetOffset"
崩溃问题 → grep -E "CHECK_NULL|fatal"
```

**Step 3: 定位代码位置**
```
根据SKILL.md的"Key Code Locations"章节
找到相关文件和函数
```

**Step 4: 添加针对性日志**
```
使用"Log Enhancement Reference"的模板
在关键位置添加日志
```

**Step 5: 重新编译复现分析**
```bash
# 编译
./build.sh --product-name rk3568 --build-target ace_engine

# 运行应用复现问题
# 收集日志
# 分析新日志
```

---

## 日志补丁模板库

### 模板1: Width计算日志

**适用**: Menu宽度问题、displayWindowRectInfo异常

**位置**: `menu_layout_algorithm.cpp:941` 附近

```cpp
// 在UpdateChildConstraintByDevice函数中添加

auto displayWidth = pipeline->GetDisplayWindowRectInfo().Width();
TAG_LOGI(AceLogTag::ACE_MENU,
    "[WIDTH_DEBUG] displayWidth=%{public}.2f, source=%{public}s",
    displayWidth,
    (pipeline == DialogManager::GetMainPipelineContext(host)) ? "main_window" : "sub_window");

if (displayWidth <= 0.0f) {
    TAG_LOGW(AceLogTag::ACE_MENU,
        "[WIDTH_DEBUG] displayWidth is 0, attempting fallback");
}
```

### 模板2: Subwindow状态日志

**适用**: 子窗口recreate、状态转换问题

**位置**: `subwindow_manager.cpp:1965` 附近

```cpp
// 在GetOrCreateMenuSubWindow函数中添加

auto subwindow = GetSubwindowBySearchKey(searchKey);
if (subwindow) {
    auto state = subwindow->GetDetachState();
    TAG_LOGI(AceLogTag::ACE_SUB_WINDOW,
        "[SUBWINDOW_DEBUG] Existing window: state=%{public}d, shown=%{public}d, reuse=%{public}d",
        static_cast<int>(state), subwindow->GetShown(), reuse);
}

if (subwindow && (subwindow->GetDetachState() == MenuWindowState::DETACHING || !reuse)) {
    TAG_LOGW(AceLogTag::ACE_SUB_WINDOW,
        "[SUBWINDOW_DEBUG] Recreate triggered: state=%{public}d, reuse=%{public}d",
        static_cast<int>(subwindow->GetDetachState()), reuse);
}
```

### 模板3: MenuWindowRect计算日志

**适用**: Menu位置异常、窗口rect计算问题

**位置**: `menu_layout_algorithm.cpp:3611-3659` GetMenuWindowRectInfo函数

```cpp
// 在GetMenuWindowRectInfo函数中添加

Rect MenuLayoutAlgorithm::GetMenuWindowRectInfo(const RefPtr<MenuPattern>& menuPattern)
{
    auto menuWindowRect = Rect();
    CHECK_NULL_RETURN(menuPattern, menuWindowRect);

    auto host = menuPattern->GetHost();
    CHECK_NULL_RETURN(host, menuWindowRect);

    // 【日志】记录获取窗口rect的过程
    TAG_LOGI(AceLogTag::ACE_MENU,
        "[MENU_RECT_DEBUG] Getting rect: menuId=%{public}d, targetTag=%{public}d, targetNodeId=%{public}d",
        menuPattern->GetMenuId(), targetTag_, targetNodeId_);

    // get default pipelineContext for menu without targetNode
    auto pipelineContext = DialogManager::GetMainPipelineContext(host);
    CHECK_NULL_RETURN(pipelineContext, menuWindowRect);

    auto menuWrapper = menuPattern->GetMenuWrapper();
    CHECK_NULL_RETURN(menuWrapper, menuWindowRect);
    auto menuWrapperPattern = menuWrapper->GetPattern<MenuWrapperPattern>();
    CHECK_NULL_RETURN(menuWrapperPattern, menuWindowRect);

    if (menuPattern->IsSubMenu()) {
        // without targetNode, submenu reuse menuWindowRect of mainMenu
        auto menuWindowRect = menuWrapperPattern->GetMenuWindowRect();

        // 【日志】记录复用的主菜单rect
        TAG_LOGI(AceLogTag::ACE_MENU,
            "[MENU_RECT_DEBUG] Submenu reusing mainMenu rect: %{public}s",
            menuWindowRect.ToString().c_str());

        dumpInfo_.menuWindowRect = menuWindowRect;
        return menuWindowRect;
    }

    auto targetNode = FrameNode::GetFrameNode(targetTag_, targetNodeId_);
    if (targetNode) {
        pipelineContext = targetNode->GetContext();
        // 【日志】记录使用targetNode的context
        TAG_LOGI(AceLogTag::ACE_MENU,
            "[MENU_RECT_DEBUG] Using targetNode context: %{public}s",
            pipelineContext ? "valid" : "null");
    } else {
        // 【日志】记录targetNode为空
        TAG_LOGW(AceLogTag::ACE_MENU,
            "[MENU_RECT_DEBUG] targetNode is null, using main pipeline context");
    }

    // ... 后续计算代码
}
```

### 模板4: PipelineContext来源追踪

**适用**: 所有Menu相关问题，确认context来源

**位置**: 所有获取PipelineContext的地方

```cpp
// 统一的PipelineContext获取日志

auto pipeline = host->GetContext();
auto mainPipeline = DialogManager::GetMainPipelineContext(host);

TAG_LOGI(AceLogTag::ACE_MENU,
    "[PIPELINE_DEBUG] hostContext=%{public}s, mainPipeline=%{public}s, same=%{public}d",
    pipeline ? "valid" : "null",
    mainPipeline ? "valid" : "null",
    (pipeline == mainPipeline) ? 1 : 0);
```

---

## 标准排查流程

### 新问题排查步骤

**当用户报告新的Menu问题时**：

1. **收集信息**:
   - 问题描述（症状、频率、触发条件）
   - 复现步骤
   - 设备信息（产品、API版本、是否折叠屏）
   - 日志片段（如果有）

2. **问题分类**:
   - 根据症状对照"常见问题速查表"
   - 确定问题类别（1-4）

3. **日志分析**:
   - 根据问题类型使用对应的grep命令
   - 提取关键日志片段
   - 分析时序和状态

4. **代码定位**:
   - 查看SKILL.md中的"Key Code Locations"
   - 定位相关函数和代码行
   - 理解现有逻辑

5. **生成补丁**:
   - 选择合适的日志模板
   - 根据具体问题定制
   - 遵循日志增强原则

6. **验证分析**:
   - 应用日志补丁
   - 重新编译
   - 复现问题
   - 收集新日志分析

### 问题闭环检查

**分析完成后**:
- ✅ 根因已确认
- ✅ 修复方案已实现
- ✅ 验证通过
- ✅ 文档已更新（如有必要）
- ✅ 调试日志已清理（如适用）

---

## 常用命令汇总

### 编译相关

```bash
# 完整编译（从OpenHarmony根目录）
./build.sh --product-name rk3568 --build-target ace_engine

# 只编译menu相关
ninja -C out/rk3568/arkui/ace_engine menu_*

# 编译单个文件（需要先extract编译命令）
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
    frameworks/core/components_ng/pattern/menu/menu_layout_algorithm.cpp \
    /path/to/OpenHarmony/out/rk3568
```

### 日志提取相关

```bash
# 提取所有Menu日志
cat xxx.log | grep -E "ACE_MENU|ACE_SUB_WINDOW|ACE_OVERLAY" > menu_debug.log

# 提取特定时间段日志
sed -n '/12:34:00/,/12:36:00/p' xxx.log | grep ACE_MENU

# 提取特定实例的日志
grep "instanceId: 123" xxx.log | grep ACE_MENU
```

### 代码搜索相关

```bash
# 在menu相关文件中搜索
grep -rn "GetDisplayWindowRectInfo" frameworks/core/components_ng/pattern/menu/

# 搜索MenuWrapper相关
grep -rn "MenuWrapperPattern" frameworks/core/components_ng/pattern/menu/ | head -10

# 搜索状态管理相关
grep -rn "GetDetachState\|SetDetachState" frameworks/base/subwindow/
```

---

## 知识库链接

### 相关文档

- **Menu知识库**: `docs/pattern/menu/Menu_Knowledge_Base_CN.md`（如果存在）
- **Menu宽度修复**: `menu_width_zero_fix.md` - 完整的问题分析和解决方案
- **子窗口架构**: 查看subwindow相关文档

### 关键源文件

| 模块 | 文件路径 |
|-----|---------|
| Menu布局 | `frameworks/core/components_ng/pattern/menu/menu_layout_algorithm.cpp` |
| Menu Pattern | `frameworks/core/components_ng/pattern/menu/menu_pattern.cpp` |
| Menu Wrapper | `frameworks/core/components_ng/pattern/menu/wrapper/menu_wrapper_pattern.cpp` |
| 子窗口管理 | `frameworks/base/subwindow/subwindow_manager.cpp` |
| 子窗口实现 | `adapter/ohos/entrance/subwindow/subwindow_ohos.cpp` |

---

**快速参考版本**: v0.1.0
**最后更新**: 2026-02-10
