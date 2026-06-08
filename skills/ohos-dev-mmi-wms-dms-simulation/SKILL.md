---
name: ohos-dev-mmi-wms-dms-simulation
description: Use when testing OpenHarmony input features that depend on window/display state (display groups, focus windows, pointer styles, capture mode, z-order hit-testing, scroll wheel, device binding) without running real WMS/DMS. Covers UpdateDisplayInfo for display groups, UpdateWindowInfo for virtual windows, z-order hit-testing, hot area pass-through, dynamic focus switching, and window lifecycle management.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: wms-dms-simulation
  version: 0.2.0
  status: draft
  tags:
    - multimodalinput
    - wms-simulation
    - display-group
    - window-management
    - z-order
  related-skills:
    - ohos-dev-mmi-device-test-harness
    - ohos-dev-mmi-uinput-virtual-device
---

# WMS/DMS 模拟

测试进程直接通过 InputManager IPC 构造显示组和窗口，替代 WMS（窗口管理服务）和 DMS（显示管理服务），实现输入子系统的独立功能验证。

**前置 skill**: 权限获取、server 绕过、编译部署、hidumper 捕获等基础设施见 `ohos-dev-mmi-device-test-harness`；虚拟设备创建和事件注入见 `ohos-dev-mmi-uinput-virtual-device`。

## When to Use

- 测试依赖显示组/窗口状态的输入功能（设备绑定、光标路由、焦点分发）
- 验证多显示组场景（主屏+副屏、独立光标、隔离焦点）
- 不想或不能启动完整 WMS/DMS 栈时

## 已验证能力摘要

DAYU200 真机 `dual_group_interleave_test` 已覆盖双显示组构造、多窗口注入、per-group
光标/按钮/键盘/焦点/captureMode/滚轮隔离、热拔插绑定清理、跨绑定按键状态和 per-window
光标外观。详细步骤、dump 证据和 PARTIAL 项见 `evals/test-results.md`，不要把长篇实测表格复制到
`SKILL.md` 主流程。

## 构造显示组（替代 DMS）

```cpp
#include "input_manager.h"

UserScreenInfo screenInfo;
screenInfo.userId = 100;

// Group 0: 默认组（主屏）
DisplayGroupInfo group0;
group0.id = 0;
group0.name = "default";
group0.type = GroupType::GROUP_DEFAULT;
group0.mainDisplayId = 0;
group0.focusWindowId = 1000;

DisplayInfo disp0;
disp0.id = 0;
disp0.x = 0; disp0.y = 0;
disp0.width = 720; disp0.height = 1280;
disp0.dpi = 240;
disp0.name = "main";
disp0.direction = DIRECTION0;
disp0.displayDirection = DIRECTION0;
disp0.screenArea = { .id = 0, .area = { 0, 0, 720, 1280 } };
group0.displaysInfo.push_back(disp0);

// Group 1: 特殊组（副屏）
DisplayGroupInfo group1;
group1.id = 1;
group1.name = "secondary";
group1.type = GroupType::GROUP_SPECIAL;
group1.mainDisplayId = 1;
group1.focusWindowId = 2000;

DisplayInfo disp1;
disp1.id = 1;
disp1.x = 0; disp1.y = 0;
disp1.width = 1920; disp1.height = 1080;
disp1.dpi = 160;
disp1.name = "secondary";
disp1.direction = DIRECTION0;
disp1.displayDirection = DIRECTION0;
disp1.screenArea = { .id = 1, .area = { 0, 0, 1920, 1080 } };
group1.displaysInfo.push_back(disp1);

screenInfo.displayGroups.push_back(group0);
screenInfo.displayGroups.push_back(group1);

// 物理屏幕信息（必须与 displaysInfo 对应）
ScreenInfo screen0;
screen0.id = 0;
screen0.uniqueId = "default0";
screen0.width = 720; screen0.height = 1280;
screen0.physicalWidth = 62; screen0.physicalHeight = 110;
screen0.dpi = 240; screen0.ppi = 295;
screen0.tpDirection = DIRECTION0;
screenInfo.screens.push_back(screen0);

ScreenInfo screen1;
screen1.id = 1;
screen1.uniqueId = "secondary1";
screen1.width = 1920; screen1.height = 1080;
screen1.physicalWidth = 531; screen1.physicalHeight = 299;
screen1.dpi = 160; screen1.ppi = 92;
screen1.tpDirection = DIRECTION0;
screenInfo.screens.push_back(screen1);

InputManager::GetInstance()->UpdateDisplayInfo(screenInfo);
```

### 关键约束

| 字段 | 约束 | 后果 |
|------|------|------|
| `group0.type` | 必须有一个 `GROUP_DEFAULT` | `InitDisplayGroupInfo` 校验 groupId==MAIN_GROUPID |
| `group0.id` | DEFAULT 组 id 必须为 0 | 非 0 会被拒绝 |
| `focusWindowId` | 必须在 DisplayGroupInfo 中预设 | 键盘事件路由依赖此值，不设则为 -1 导致键盘事件无法分发 |
| `screenArea` | 必须与 width/height 一致 | 光标边界夹紧依赖此值 |
| `screens` 数量和 ID | 必须与 displaysInfo 对应 | 屏幕信息用于 DPI/PPI 计算 |
| `userState` | 默认 `USER_ACTIVE`，无需设置 | 非 ACTIVE 时 displayGroupInfoMap_ 不写入 |

### 返回码

`UpdateDisplayInfo` 返回 -201 是正常的 — 这是 `UpdateUIExtensionInfo` 的错误码，不影响显示组数据的写入。

## 注入虚拟窗口（替代 WMS）

每个显示组需要至少一个窗口，键盘和鼠标事件才能路由到目标：

```cpp
WindowGroupInfo wgi0;
wgi0.focusWindowId = 1000;
wgi0.displayId = 0;

WindowInfo win0;
win0.id = 1000;
win0.pid = getpid();
win0.uid = getuid();
win0.area = { 0, 0, 720, 1280 };
win0.defaultHotAreas = { { 0, 0, 720, 1280 } };
win0.pointerHotAreas = { { 0, 0, 720, 1280 } };
win0.agentWindowId = -1;
win0.flags = 0;
win0.action = WINDOW_UPDATE_ACTION::ADD;
win0.displayId = 0;
win0.groupId = 0;
win0.zOrder = 1.0f;
wgi0.windowsInfo.push_back(win0);

InputManager::GetInstance()->UpdateWindowInfo(wgi0);
```

### 关键约束

| 字段 | 约束 |
|------|------|
| `win.groupId` | 必须匹配目标显示组 ID |
| `win.displayId` | 必须匹配显示组内的 display ID |
| `win.pid` | 用 `getpid()` — 权限检查需要 |
| `win.action` | 首次用 `ADD`，更新用 `CHANGE` |
| `wgi.focusWindowId` | 对 MAIN_GROUPID 生效；非主组从 displayGroupInfoMap_ 读取 |
| `pointerHotAreas` | 鼠标事件命中测试依赖此区域 |

## 增量窗口操作

单个窗口的 ADD/CHANGE/DEL，无需重新注入全部窗口：

```cpp
static void InjectSingleWindow(int32_t winId, int32_t groupId, int32_t displayId,
    Rect area, float zOrder, WINDOW_UPDATE_ACTION action, int32_t focusWinId = -1)
{
    WindowGroupInfo wgi;
    wgi.focusWindowId = focusWinId;
    wgi.displayId = displayId;
    WindowInfo win;
    win.id = winId;
    win.pid = getpid();
    win.uid = getuid();
    win.area = area;
    win.defaultHotAreas = { area };
    win.pointerHotAreas = { area };
    win.agentWindowId = -1;
    win.flags = 0;
    win.action = action;
    win.displayId = displayId;
    win.groupId = groupId;
    win.zOrder = zOrder;
    wgi.windowsInfo.push_back(win);
    InputManager::GetInstance()->UpdateWindowInfo(wgi);
}
```

`UpdateDisplayInfoByIncrementalInfo` 处理：`ADD` 追加（已存在则替换），`CHANGE` 就地替换，`DEL` 从列表移除。

## 动态焦点切换

### 主组 (groupId=0)

`UpdateWindowInfo` 使用传入的 `wgi.focusWindowId`，直接生效。

### 非主组 (groupId!=0)

`UpdateWindowInfo` 忽略传入的 `focusWindowId`，始终从 `displayGroupInfoMap_` 读取。**必须通过 `UpdateDisplayInfo` 更新焦点：**

```cpp
SetupDualDisplayGroups(1000, 2002);  // 重新调用 UpdateDisplayInfo
sleep(1s);
InjectVirtualWindows();               // 重新注入窗口（同步 focusWinId 全局变量）
sleep(1s);
```

**实现模式**：使用全局变量跟踪焦点，`SetupDualDisplayGroups` 和 `InjectVirtualWindows` 共享：

```cpp
static int32_t g_focusWin0 = 1000;
static int32_t g_focusWin1 = 2000;

static void SetupDualDisplayGroups(int32_t focusWin0 = 1000, int32_t focusWin1 = 2000)
{
    g_focusWin0 = focusWin0;
    g_focusWin1 = focusWin1;
    // ... UpdateDisplayInfo with focusWin0/focusWin1
}

static void InjectVirtualWindows()
{
    // wgi.focusWindowId = g_focusWin0;  // 不再硬编码
    // ...
}
```

## 多窗口 z-order 命中测试

### 基本模式：不同区域不同层级

```cpp
// Group 0: 3 个窗口
// win1000: 应用窗口(背景)  area={0,80,720,1200}   zOrder=10
// win1001: 状态栏          area={0,0,720,80}       zOrder=100
// win1002: 悬浮球          area={600,600,120,120}   zOrder=200
```

`SelectWindowInfo` 按 zOrder 降序遍历，第一个 `pointerHotAreas` 命中的窗口为目标。重叠区域 zOrder 高的优先。

### 全屏重叠模式：位置无关验证

ADD 多个全屏窗口（不同 zOrder），无需光标定位 — 全屏窗口在任意光标位置都命中：

```cpp
InjectSingleWindow(1005, 0, 0, {0,0,720,1280}, 50.0f, WINDOW_UPDATE_ACTION::ADD, g_focusWin0);
InjectSingleWindow(1006, 0, 0, {0,0,720,1280}, 150.0f, WINDOW_UPDATE_ACTION::ADD, g_focusWin0);
InjectSingleWindow(1007, 0, 0, {0,0,720,1280}, 250.0f, WINDOW_UPDATE_ACTION::ADD, g_focusWin0);
// 点击 → Cursor Info.windowId = 1007 (z=250 最高)
// DEL win1007 → 点击 → windowId 变为原有最高层（可能是 win1002=z200，不一定是 win1006=z150）
```

**注意**：DEL 全屏窗口后，命中目标取决于剩余所有窗口的 zOrder，包括原有非全屏窗口。上例中 DEL win1007(z=250) 后，如果光标位置在 win1002(z=200) 的 hotArea 内，则命中 win1002 而非 win1006(z=150)。

### 热区穿透

`area` 和 `pointerHotAreas` 可以不同。光标在 `area` 内但 `pointerHotAreas` 外时，点击穿透到下层窗口：

```cpp
// win1004: area 大于 hotArea
WindowInfo win;
win.area = { 100, 200, 400, 400 };
win.defaultHotAreas = { { 200, 300, 200, 200 } };  // hotArea 小于 area
win.pointerHotAreas = { { 200, 300, 200, 200 } };
// 点击 (150,250) — area 内但 hotArea 外 → 穿透到下层
// 点击 (350,450) — hotArea 内 → 命中此窗口
```

## 窗口生命周期 (ADD → CHANGE → DEL)

```cpp
// ADD: 新增弹窗
InjectSingleWindow(1003, 0, 0, {200,200,320,320}, 300.0f, WINDOW_UPDATE_ACTION::ADD, 1000);
// 点击 (360,360) → 命中 win1003

// CHANGE: 移动弹窗位置
InjectSingleWindow(1003, 0, 0, {400,800,320,320}, 300.0f, WINDOW_UPDATE_ACTION::CHANGE, 1000);
// 点击原位置 (360,360) → 穿透到 win1000

// DEL: 删除弹窗
InjectSingleWindow(1003, 0, 0, {0,0,0,0}, 0.0f, WINDOW_UPDATE_ACTION::DEL, 1000);
// 窗口列表恢复
```

## 可用的验证 API

```cpp
// 设备绑定（详见 ohos-dev-mmi-device-test-harness）
InputManager::GetInstance()->BindDeviceToDisplayGroupByDisplay(deviceId, displayId, msg);
InputManager::GetInstance()->UnbindDeviceFromDisplayGroup(deviceId, msg);

// 光标样式（per-window）
PointerStyle style;
style.id = 13;            // MOUSE_ICON::CROSS
style.size = 3;
style.color = 0xFF0000;   // red
InputManager::GetInstance()->SetPointerStyle(windowId, style);
InputManager::GetInstance()->GetPointerStyle(windowId, style);

// 全局光标大小/颜色
InputManager::GetInstance()->SetPointerSize(4);
InputManager::GetInstance()->SetPointerColor(0x00FF00);

// 捕获模式
InputManager::GetInstance()->EnterCaptureMode(windowId);
InputManager::GetInstance()->LeaveCaptureMode(windowId);
```

## 执行顺序

```
1. InitNativeToken()           — 权限 (见 ohos-dev-mmi-device-test-harness)
2. UpdateDisplayInfo()         — 显示组（等 1 秒）
3. UpdateWindowInfo() x N      — 每组多个窗口（等 1 秒）
4. 创建虚拟设备 + FindDevice   — 见 ohos-dev-mmi-uinput-virtual-device
5. BindDeviceToDisplayGroupByDisplay()
6. warm-up 事件注入（2 次，初始化 group state）
7. 测试逻辑 + DumpPhase()     — dump 捕获见 ohos-dev-mmi-device-test-harness
8. 清理：解绑 → UI_DEV_DESTROY → close(fd)
```

## 已知限制

| 限制 | 原因 | 规避方案 |
|------|------|---------|
| 光标定位不精确 | libinput 鼠标加速导致 uinput 相对移动无法精确到绝对坐标 | 使用全屏窗口避免依赖光标位置 |
| `focusWindowId=-1` 在 DisplayGroups dump 中 | dump 读 `displayGroupInfoMap_`，MAIN_GROUPID 的焦点从 `UpdateWindowInfo` 传入 | 通过 `KeyboardStateByGroup` 或 `SequenceSnapshots` 验证实际焦点 |
| 非主组焦点切换 | `UpdateWindowInfo` 忽略非主组 focusWindowId | 必须通过 `UpdateDisplayInfo` 更新 |
| DEL 全屏后命中非预期窗口 | 剩余窗口中 zOrder 最高的命中，包括原有非全屏窗口 | 注意已有窗口的 zOrder 关系 |

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 不设 `focusWindowId` | 键盘事件不分发到任何窗口 | 在 DisplayGroupInfo 中预设 |
| `groupId != 0` 的组用 `GROUP_DEFAULT` | `InitDisplayGroupInfo` 拒绝 | 非 0 组用 `GROUP_SPECIAL` |
| 窗口的 `groupId` 与显示组不匹配 | 事件路由到错误的组 | 确保一致 |
| 非主组通过 UpdateWindowInfo 切焦点 | focusWindowId 被忽略 | 必须通过 UpdateDisplayInfo 切焦点 |
| 所有窗口用相同 zOrder | 命中顺序不确定 | 按业务层级分配不同 zOrder |
| 忘记注入窗口 | 鼠标事件无 hit test 目标 | 每组至少一个全屏窗口 |
| UpdateDisplayInfo 返回 -201 就认为失败 | 实际数据已写入 | -201 来自 UIExtension，可忽略 |
| InjectVirtualWindows 硬编码 focusWindowId | 动态焦点切换后被覆盖 | 使用全局变量同步焦点 |
| DEL 全屏窗口后假设次高全屏命中 | 原有非全屏窗口可能 zOrder 更高 | 检查所有窗口的 zOrder 关系 |
