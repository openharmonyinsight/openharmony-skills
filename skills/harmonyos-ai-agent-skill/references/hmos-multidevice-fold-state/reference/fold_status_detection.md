# 折叠状态检测指南（官方基线）

## 目标

用官方 `@ohos.display` 能力完成折叠态、展开态、悬停态和显示模式识别，作为折展页面分支的统一入口。

## 官方 API

- `display.getFoldStatus()`：读取当前折叠状态。
- `display.on('foldStatusChange', callback)`：监听折叠状态变化。
- `display.off('foldStatusChange', callback?)`：取消折叠状态监听。
- `display.on('foldDisplayModeChange', callback)`：监听显示模式变化（MAIN/SUB/FULL/COORDINATION）。
- `display.off('foldDisplayModeChange', callback?)`：取消显示模式监听。

## 最小代码骨架

```typescript
import display from '@ohos.display';

const onFoldStatusChange = (status: display.FoldStatus) => {
  // 按 status 切换布局分支
};

const onFoldDisplayModeChange = (mode: display.FoldDisplayMode) => {
  // 按 MAIN/SUB/FULL/COORDINATION 调整页面策略
};

export function registerFoldListeners(): void {
  display.on('foldStatusChange', onFoldStatusChange);
  display.on('foldDisplayModeChange', onFoldDisplayModeChange);
}

export function unregisterFoldListeners(): void {
  display.off('foldStatusChange', onFoldStatusChange);
  display.off('foldDisplayModeChange', onFoldDisplayModeChange);
}
```

## 使用场景

| 场景 | 触发条件 | 推荐用法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 折叠特性页首帧初始化 | 页面首次渲染前需决定折展分支 | `display.getFoldStatus()` | 避免首帧先渲染错误布局再闪切。 | 首帧抖动、结构跳变。 |
| 折展过程中实时刷新 | 用户正在折/展开设备 | `display.on('foldStatusChange', ...)` | 状态会动态变化，需事件驱动刷新。 | 布局滞后，内容跨折痕。 |
| 区分主屏/副屏/全屏策略 | 外屏/内屏/全屏展示规则不同 | `display.on('foldDisplayModeChange', ...)` | `FoldStatus` 仅表示折叠程度；显示区域由 `FoldDisplayMode` 决定。 | 主/副屏规则混用，方向和交互入口错误。 |
| 页面退出清理监听 | 页面销毁或路由离开 | `display.off(...)` | 监听生命周期需与页面一致。 | 监听残留、状态串扰、性能下降。 |
| 悬停态分屏入口 | 页面有“上内容下操作”等悬停结构 | `status === FOLD_STATUS_HALF_FOLDED` | 仅在半折叠态切到悬停布局。 | 展开态误入悬停分支。 |
| 多段折叠形态入口（如 F/M/G） | 多形态折叠设备在不同形态间切换 | `getFoldStatus()` + 运行时窗口尺寸 | 状态给形态信号，尺寸决定真实可用空间。 | 断点误判，形态映射适配失真。 |

## 约束

- 通用响应式布局优先使用窗口尺寸与断点；`foldStatus` 用于折叠特性分支，不作为全局布局唯一决策条件。
- 工程代码直接使用 `display.FoldStatus` / `display.FoldDisplayMode` 枚举，不手写同名枚举。

## 官方来源

- [折叠屏悬停态适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-folded-hover)
- [多设备窗口方向适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-device-window-direction)
