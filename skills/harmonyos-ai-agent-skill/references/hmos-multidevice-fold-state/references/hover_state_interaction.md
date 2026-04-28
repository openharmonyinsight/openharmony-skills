# 悬停态交互指南（官方基线）

## 目标

在折叠设备悬停态下，稳定实现“上内容下操作”或固定分栏，并确保折痕避让与方向策略可回收。

## 官方 UX 标准对齐（4.3 悬停适配）

来源：华为开发者联盟《折叠屏应用 UX 体验标准》4.3。

- 长视频、短视频、直播、通话、会议、拍摄类应用，涉及悬停态时需要单独适配。
- 设计分工建议：下半屏优先承载交互操作，上半屏优先承载浏览型信息。
- 控件落位建议：弹出框和半模态优先下半屏；跟随上下文的控件跟随触发元素所在侧。
- 标准等级：涉及则必须。

## 官方优先路径

1. `FolderStack`：优先用于上下分屏职责明确的页面。
2. `FoldSplitContainer`：优先用于固定主次分栏的页面。
3. 自定义容器：仅在系统组件无法满足交互需求时使用。

## 推荐实现

### 路径一：FolderStack（推荐）

```typescript
FolderStack({ upperItems: ['upper'] }) {
  VideoPanel().id('upper')
  ControlsPanel()
}
```

### 路径二：FoldSplitContainer（推荐）

```typescript
FoldSplitContainer({
  primary: () => this.primaryArea(),
  secondary: () => this.secondaryArea()
})
```

## 方向策略

- 使用 `window.setPreferredOrientation(...)` 设置窗口方向。
- 仅使用官方 `window.Orientation` 枚举。
- 方向决策优先级建议为“页面语义 > 设备固定折痕轴约束 > 折痕矩形几何推断”。
- 若设备是固定竖折痕，且页面语义是“上展示下操作”，即使 `creaseRect` 呈横向宽条，也应先旋转 90 度再落上下分栏。
- 退出悬停态后恢复 `AUTO_ROTATION`。

## 使用场景

| 场景 | 触发条件 | 推荐路径 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 上内容下操作的标准悬停页 | 页面语义明确为“上展示、下操作” | `FolderStack` | 容器语义与悬停职责直接匹配，改造最小。 | 继续沿用单屏结构会导致职责混放。 |
| 固定主次分栏页面 | 主区/次区关系长期稳定 | `FoldSplitContainer` | 由容器承载分栏规则，减少手写分支。 | 分区逻辑分散在业务代码，回归风险高。 |
| 悬停态方向与页面语义绑定 | 页面在悬停下有方向要求 | `setPreferredOrientation` + `window.Orientation` | 方向影响阅读和交互路径，必须按场景决策。 | 分区正确但交互方向反了。 |
| 页面离开时清理状态 | 页面销毁或路由离开 | 监听回收 + 方向恢复 | 防止旧页面继续响应状态事件。 | 监听残留、串态、方向异常。 |

## 验证清单

- 可正确进入/退出悬停态。
- 关键内容和关键交互不跨折痕。
- 页面退出后监听已回收，方向策略已恢复。

## 官方来源

- [折叠屏悬停态适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-folded-hover)
- [多设备窗口方向适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-device-window-direction)
