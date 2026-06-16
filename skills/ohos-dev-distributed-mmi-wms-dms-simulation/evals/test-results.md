# dual_group_interleave_test WMS/DMS 模拟验证

- **日期**: 2026-06-05
- **设备**: DAYU200 (RK3568)
- **测试二进制**: `dual_group_interleave_test`

## 验证项

### 显示组与窗口构造

| 能力 | 步骤 | 结果 | dump 证据 |
|------|------|------|-----------|
| 双显示组构造 | Step 1 | PASS | `DisplayGroups` 显示 groupId=0 和 groupId=1 |
| UpdateDisplayInfo 返回 -201 | Step 1 | PASS (预期) | -201 来自 UIExtension，数据已写入 |
| 多窗口注入 (每组 3 个) | Step 1.5 | PASS | 6 个窗口在线，不同 zOrder/area |
| 焦点窗口预设 | Step 1 | PASS | 键盘事件正确路由到预设焦点窗口 |

### 状态隔离 (per-group)

| 能力 | 步骤 | 结果 | dump 证据 |
|------|------|------|-----------|
| 光标位置隔离 | Step 5 | PASS | group0=(719,1280), group1=(0,1) 独立变化 |
| 鼠标按钮隔离 | Step 6 | PASS | 各组按键状态独立按下/释放 |
| 键盘修饰键隔离 | Step 9 | PASS | group0 有 Ctrl, group1 有 Shift, 互不影响 |
| 焦点窗口隔离 | Step 9.5 | PASS | KEY 事件路由到各自组的焦点窗口 |
| captureMode 隔离 | Step 10 | PASS | group0=true, group1=false 独立 |
| 滚轮隔离 | Step 17 | PASS | 两组各注入不同方向滚轮 |
| 并发压力隔离 | Step 18 | PASS | 100 次快速交替，状态互不干扰 |

### 窗口管理

| 能力 | 步骤 | 结果 | dump 证据 |
|------|------|------|-----------|
| z-order 命中 (相对定位) | Step 13a-c | PARTIAL | 光标定位不精确导致未命中目标窗口，Cursor Info.windowId 仍为 1000 |
| 全屏 z-order (位置无关) | Step 16 | NOT RUN | P2 测试代码已写入但未在此次 dump 运行中包含 |
| 热区穿透 | Step 12a-b | PARTIAL | 光标定位限制，area 外/内的穿透/命中行为正确但 dump 时机受限 |
| 动态焦点切换 (group0) | Step 14b | PASS | 切换到 win1001 后键盘事件路由正确 |
| 动态焦点切换 (非主组) | Step 14c | PASS | 必须通过 UpdateDisplayInfo 切焦点 |
| 窗口 ADD | Step 15a | PARTIAL | 新窗口注入成功，但光标定位限制影响命中测试 |
| 窗口 CHANGE | Step 15b | PASS | 窗口位置变更后原位置穿透行为正确 |
| 窗口 DEL | Step 15c | PASS | 窗口列表恢复 |

### 设备生命周期

| 能力 | 步骤 | 结果 | dump 证据 |
|------|------|------|-----------|
| 热拔插自动清理 | Step 11 | PASS | RuntimeBindings 自动清理 |
| 跨绑定按键状态 | Step 7 | PASS | group1 按下 → 解绑 → 重绑 → 释放仍发给 group1 |
| 光标外观 per-window | Step 5.5 | PASS | `PointerStyleByWindow`: win1000=CROSS/red, win2000=HAND_POINTING/blue |

## 关键 dump 数据

### captureMode 隔离 (Step 10)

```
--- PointerStateByGroup ---
  groupId=0: cursorPos=(719,1280) captureMode=true
  groupId=1: cursorPos=(2,1)      captureMode=false
```

### 光标外观 (Step 5.5)

```
--- PointerStyleByWindow ---
  pid=20097 windowId=1000 groupId=0 style(id=13 size=3 color=0xFF0000)   # CROSS, red
  pid=20097 windowId=2000 groupId=1 style(id=19 size=5 color=0x0000FF)   # HAND_POINTING, blue
```

## 已知限制

| 限制 | 影响 | 规避 |
|------|------|------|
| 光标相对定位不精确 | z-order 和热区测试无法精确命中目标区域 | 使用全屏窗口的位置无关验证（Step 16，已编码但未在此次运行中包含） |
| SequenceSnapshots 可能为空 | 事件记录有 TTL | dump 时机需紧跟事件注入 |
| DisplayGroups.focusWindowId=-1 | MAIN_GROUPID 焦点存储在别处 | 通过 KeyboardStateByGroup 验证实际焦点 |

## 总结

- **19 步骤, 28 个 dump 阶段**全部捕获
- **核心隔离验证**: 7/7 PASS (光标、按钮、键盘、焦点、captureMode、滚轮、并发)
- **窗口管理**: 焦点切换和生命周期 PASS，z-order 命中受光标定位限制部分验证
- **设备生命周期**: 3/3 PASS (热拔插、跨绑定状态、光标外观)
