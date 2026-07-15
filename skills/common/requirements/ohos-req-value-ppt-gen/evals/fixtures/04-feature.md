# 04 特性需求：运行时将 HID 设备绑定到指定屏幕

## 一、概述与价值
多模输入（multimodalinput_input）当前无法在运行时将某个 USB / 蓝牙 HID 设备
（鼠标 / 键盘 / 触控板）定向投递到指定屏幕。在多屏 / 屏幕组场景下，外设事件只能
进入全局焦点窗口，导致跨屏操作错位。本特性提供运行时绑定能力，使指定 HID 设备的
输入事件解析到目标屏幕组上下文，提升多屏办公与拼接大屏的可用性。

## 二、范围
- In scope：运行时绑定表、屏幕组上下文解析、normalize 前的坐标 / 命中归一。
- Out of scope：HID 设备驱动适配、蓝牙配对流程、应用层多屏 UI 适配。

## 三、验收标准（AC）
1. 调用绑定接口后，目标 HID 设备的指针 / 点击事件仅出现在绑定屏幕。
2. 解绑或设备拔出后，事件回退至默认全局焦点行为。
3. 高频事件（≥ 200 Hz）链路时延相比绑定前无可感知劣化。
4. 绑定关系按 InputDeviceContextKey 维度隔离，多设备互不影响。

## 四、受影响跨仓模块
- multimodalinput_input：新增运行时绑定表与 InputDisplayBindHelper。
- window_window_manager（WMS）：提供窗口 / 焦点 / 屏幕组信息查询。
- display_display_manager（DMS）：提供屏幕组拓扑与上 / 下线通知。
- graphic_graphic_2d（RS）：光标 Surface 按绑定屏幕渲染。

## 五、拆解指引
按"控制面（绑定表 / 权限校验）"与"数据面（采集 → normalize → 命中 → 投递）"
两条线拆解；变更点集中在 normalize 前的统一解析阶段。

## 六、技术方向
跨线程经 DelegateTasks 投递；多鼠标全局态拆分至 InputDeviceContextKey 维度；
绑定结果在 normalize 前解析屏幕组上下文，再进入高频事件链路。

## 七、风险与前置条件
- 风险：屏幕组热插拔时绑定表与 DMS 拓扑短暂不一致。
- 前置条件：依赖 DMS 屏幕组上 / 下线事件、WMS 屏幕组信息查询接口就绪。
