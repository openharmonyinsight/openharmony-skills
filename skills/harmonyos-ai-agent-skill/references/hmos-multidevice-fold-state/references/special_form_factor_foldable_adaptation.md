# 特殊比例折叠屏适配指南（官方基线）

## 目标

用于内外屏比例差异显著的折叠屏（例如方形外屏 + 宽比例内屏）进行布局、窗口、方向和开合接续适配。

## 适配范围

- 内外屏分辨率与比例差异较大。
- 折叠态/展开态/悬停态存在明显布局策略差异。
- 需要处理全屏、分屏、悬浮窗等窗口模式切换。

## 核心原则

- 页面布局以窗口尺寸与断点为主，不以设备型号硬编码分支。
- 折叠状态用于“折叠特性分支”，不替代常规响应式布局。
- 内外屏策略分离：外屏保核心信息，内屏扩展信息密度与并行任务。
- 方向策略按页面语义设置，并在退出场景时恢复默认策略。

## 推荐实现路径

1. 状态入口：`getFoldStatus()` + `foldStatusChange`，必要时接入 `foldDisplayModeChange`。
2. 尺寸入口：`windowSizeChange` + 断点体系，统一驱动结构切换。
3. 布局策略：
   - 外屏（可视区小）：核心内容优先、降低层级深度；
   - 内屏（可视区大）：分栏/栅格提升信息密度。
4. 生命周期：页面离开时回收监听，方向恢复 `AUTO_ROTATION`。

## 配套资产

- 断点观察器：`./assets/foldable_form_factor_assets/BreakpointObserverExample.ets`
- 窗口变化监听：`./assets/foldable_form_factor_assets/WindowSizeChangeExample.ets`
- 响应式布局：`./assets/foldable_form_factor_assets/ResponsiveLayoutExample.ets`
- 模块配置示例：`./assets/foldable_form_factor_assets/foldable_module_config.json5`

## 使用场景

| 场景 | 触发条件 | 推荐做法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 内外屏策略拆分 | 内外屏比例差异显著 | 外屏保核心、内屏扩展信息密度 | 不同可视区承载能力不同。 | 外屏拥挤、内屏空白。 |
| 开合接续 | 折叠态/展开态频繁切换 | 状态 + 尺寸双入口同步 | 仅看单一信号会丢失上下文。 | 页面跳变、状态丢失。 |
| 多窗口模式适配 | 全屏/分屏/悬浮窗切换 | `windowSizeChange` 驱动断点重算 | 窗口模式直接改变可用空间。 | 布局错位、裁切。 |
| 方向与语义绑定 | 页面在不同场景下方向要求不同 | `setPreferredOrientation` + 退出恢复 | 方向决定阅读和交互路径。 | 方向错置、交互效率下降。 |

## 验证清单

- 内外屏切换后结构稳定，无关键内容缺失。
- 全屏/分屏/悬浮窗切换后布局无重叠或裁切。
- 退出页面后监听已回收、方向已恢复。

## 官方来源

- [折叠屏悬停态适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-folded-hover)
- [多设备响应式布局（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-device-responsive-layout)
- [多设备窗口方向适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-device-window-direction)
