# dual_group_interleave_test 虚拟设备验证

- **日期**: 2026-06-05
- **设备**: DAYU200 (RK3568)
- **测试二进制**: `dual_group_interleave_test`

## 验证项

| 能力 | 步骤 | 结果 | dump 证据 |
|------|------|------|-----------|
| 鼠标设备创建 (BUS_USB) | Step 2 | PASS | `FindDevice` 在 3 秒内发现设备 |
| 键盘设备创建 (BUS_USB) | Step 8 | PASS | 4 个设备同时在线 |
| vendor/product 唯一性 | Step 2/8 | PASS | 4 个设备 product ID 各不相同 |
| 鼠标相对移动注入 | Step 3-5 | PASS | `PointerStateByGroup.cursorPos` 按注入量变化 |
| 鼠标按钮注入 (BTN_LEFT) | Step 6 | PASS | per-group 按键状态独立 |
| 键盘按键注入 (KEY_LEFTCTRL/SHIFT) | Step 9 | PASS | `KeyboardStateByGroup` 修饰键独立 |
| 滚轮注入 (REL_WHEEL) | Step 17 | PASS | 两组各注入不同方向，互不影响 |
| 设备发现轮询 (FindDevice) | Step 2 | PASS | 30 次轮询 x 500ms 内发现 |
| 热拔插 (UI_DEV_DESTROY) | Step 11 | PASS | 绑定自动清理，RuntimeBindings 从 3→2 条 |
| warm-up 事件初始化 | Step 3 | PASS | 跳过 warm-up 会导致 group 状态为空 |
| 并发快速交替注入 | Step 18 | PASS | 100 次交替，两组光标仅各在 X/Y 变化 |

## 关键 dump 数据

### 设备绑定 (Step 4: 绑定后)

```
--- RuntimeBindings ---
  deviceId=7 displayId=1 groupId=1
  deviceId=6 displayId=0 groupId=0
```

### 键盘 + 鼠标全绑定 (Step 8)

```
--- RuntimeBindings ---
  deviceId=9 displayId=1 groupId=1    (键盘 B)
  deviceId=8 displayId=0 groupId=0    (键盘 A)
  deviceId=7 displayId=1 groupId=1    (鼠标 B)
  deviceId=6 displayId=0 groupId=0    (鼠标 A)
```

### 热拔插后 (Step 11: 设备 C 销毁)

```
--- RuntimeBindings ---
  deviceId=7 displayId=1 groupId=1
  deviceId=6 displayId=0 groupId=0
  (设备 C 的绑定已自动清理)
```

### 光标位置隔离 (Step 5: 交互移动后)

```
--- PointerStateByGroup ---
  groupId=0: cursorPos=(719,1280)   captureMode=false
  groupId=1: cursorPos=(0,1)        captureMode=false
  (两组独立变化，互不影响)
```

## 已知限制

| 限制 | 原因 |
|------|------|
| 鼠标绝对定位不精确 | libinput 加速导致 uinput 相对移动无法精确到达目标坐标 |
| 首次事件可能被吃掉 | `EnsureGroupState` 懒初始化消耗首次事件 |
