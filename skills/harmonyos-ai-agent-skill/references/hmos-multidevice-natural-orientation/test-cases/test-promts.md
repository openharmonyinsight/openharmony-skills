# Natural Orientation Test Prompts

用于验证 `device-natural-orientation` 的三层测试能力。

## 1. Smoke Prompt

设备在横竖屏切换后方向判断不稳定，需要明确自然方向、rotation 值和 setPreferredOrientation 的语义边界。请先给出需求分析设计。

## 2. Scene-Functional Prompt

请为需要锁定横屏视频页的应用补齐自然方向和 rotation 检测方案，要求在不同自然方向设备上都能得到一致的旋转语义。请输出可落到工程中的开发方案。

## 3. Real-World Prompt

视频播放页在部分平板和折叠设备上有两类线上问题：用户横拿设备时页面偶尔还是竖屏，日志里 rotation=90/270 但工程师解释不一致；部分机型锁横屏后返回列表又出现方向闪烁。请输出修复方案和工程验证要求。

## 典型验证点

- 是否命中 `ORIENT-01` 或 `ORIENT-03`
- 是否区分自然方向和窗口尺寸变化
- 是否避免把方向语义问题误归到布局场景
- 是否定义方向日志与真机验证要求
