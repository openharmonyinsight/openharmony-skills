# 折痕避让指南（官方基线）

## 目标

在折叠设备悬停态下，确保关键内容与关键交互不落在折痕区域。

## 官方 UX 标准对齐（4.4 折痕避让）

来源：华为开发者联盟《折叠屏应用 UX 体验标准》4.4。

- 悬停态下折痕区域操作困难且内容易变形，涉及视频/通话/会议/拍摄类应用时需要折痕避让。
- 距离基线：上半屏内容由中线向上避让 `16 vp`（约 `3 mm`）。
- 距离基线：下半屏内容由中线向下避让 `40 vp`（约 `7 mm`）。
- 标准等级：涉及则必须。

补充解释：
- `16 vp / 40 vp` 是内容安全间距，不是分屏边界定位锚点。
- 分屏边界应先对齐真实折痕矩形的上/下边界（或左/右边界），再在分区内部应用安全间距。

## 官方 API

- `display.getCurrentFoldCreaseRegion()`：读取当前折痕矩形。
- `display.convertGlobalToRelativeCoordinate(...)`：全局坐标转页面相对坐标。
- `display.on('foldStatusChange', ...)` / `display.off(...)`：状态变化与回收。

## 折痕定位最小骨架（边界锚定版）

```typescript
import display from '@ohos.display';

type CreaseBand = {
  axis: 'horizontal' | 'vertical';
  topInRoot: number;
  bottomInRoot: number;
  leftInRoot: number;
  rightInRoot: number;
  splitYInRoot: number;
  splitXInRoot: number;
};

function resolveCreaseBand(rootOffsetInSameUnit: { x: number; y: number }): CreaseBand | undefined {
  const region = display.getCurrentFoldCreaseRegion();
  if (!region || !region.creaseRects || region.creaseRects.length === 0) {
    return undefined;
  }

  const rect = region.creaseRects[0];
  const p1 = display.convertGlobalToRelativeCoordinate({ x: rect.left, y: rect.top }, region.displayId).position;
  const p2 = display.convertGlobalToRelativeCoordinate(
    { x: rect.left + rect.width, y: rect.top + rect.height },
    region.displayId
  ).position;

  // rootOffset 与 p1/p2 必须是同一坐标单位，再做扣减。
  const leftInRoot = Math.min(p1.x, p2.x) - rootOffsetInSameUnit.x;
  const rightInRoot = Math.max(p1.x, p2.x) - rootOffsetInSameUnit.x;
  const topInRoot = Math.min(p1.y, p2.y) - rootOffsetInSameUnit.y;
  const bottomInRoot = Math.max(p1.y, p2.y) - rootOffsetInSameUnit.y;

  const axis = (rightInRoot - leftInRoot) >= (bottomInRoot - topInRoot)
    ? 'horizontal'
    : 'vertical';

  return {
    axis,
    topInRoot,
    bottomInRoot,
    leftInRoot,
    rightInRoot,
    splitYInRoot: (topInRoot + bottomInRoot) * 0.5,
    splitXInRoot: (leftInRoot + rightInRoot) * 0.5
  };
}
```

## 分区落点规则（用于修复“避让区偏下/偏上”）

- 横向折痕（上下分屏）：
  - 上分区下边界 = `topInRoot`
  - 下分区上边界 = `bottomInRoot`
  - 分界线仅用于视觉或辅助计算：`splitYInRoot`
- 纵向折痕（左右分屏）：
  - 左分区右边界 = `leftInRoot`
  - 右分区左边界 = `rightInRoot`
  - 分界线仅用于视觉或辅助计算：`splitXInRoot`
- `16 vp / 40 vp` 仅应用在分区内部内容的安全间距上，不替代上面的边界锚点。
- 禁止使用“中线 + 固定偏移”直接生成容器边界，否则容易出现整体偏下或偏上。

## 旋转稳定性与黑屏防护（工程经验补充）

当页面同时涉及“悬停方向切换 + 折痕分区重算”时，建议增加以下防护：

- 折痕轴判定优先使用折痕原始矩形 `rect.width/rect.height`，再用映射后坐标做二次校验；不要只依赖映射坐标。
- 若 `convertGlobalToRelativeCoordinate(...)` 在旋转中出现轴互换或跳变，允许回退到“原始折痕矩形 + root 偏移（同单位）”计算。
- 折痕厚度必须设置异常阈值（建议不超过可用高/宽的约 `35%`）；超过阈值应回退到薄边估算，防止整屏被误判为折痕区。
- 折痕重算前先确认方向锁是否已失效：`foldStatus / foldDisplayMode / 折痕轴` 任一变化，需先清锁再重算。

推荐伪代码：

```typescript
const axisByRaw = rawRect.height > rawRect.width ? 'vertical' : 'horizontal';
let creaseThickness = axisByRaw === 'horizontal' ? mappedRect.height : mappedRect.width;
const maxReasonable = (axisByRaw === 'horizontal' ? rootHeight : rootWidth) * 0.35;
if (creaseThickness <= 0 || creaseThickness > maxReasonable) {
  creaseThickness = Math.max(1, Math.min(mappedRect.width, mappedRect.height));
}
```

排查“悬停黑屏”时，必须同时满足：
- `snapshot_display`：确认是否视觉黑屏；
- `dumpLayout`：确认关键组件（如视频/详情）是否仍在渲染树；
- `DisplayManagerService`：确认当前 `FoldStatus` 与 `CurrentCreaseRects`。

## 使用场景

| 场景 | 触发条件 | 推荐用法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 悬停态分区重算 | 用户折展设备，页面需实时更新 | `getFoldStatus()` + `on('foldStatusChange')` | 避让依赖当前状态，变化后必须重算。 | 页面仍使用旧分区，控件跨折痕。 |
| 按真实折痕边界落分区 | 页面要做上/下或左/右职责分区 | `getCurrentFoldCreaseRegion()` + 边界锚定 | 真实折痕边界是唯一可靠分区锚点。 | 经验比例在不同机型失效。 |
| 页面根节点存在偏移 | 页面非全局原点（沉浸式/容器偏移） | `mapped - rootOffset(同单位)` | 统一坐标系后才能正确落线。 | 分界线整体偏移，视觉不居中。 |
| 需要内容安全间距 | 分区内容紧贴折痕，易误触或难读 | 在分区内部应用 `16 vp / 40 vp` | 安全间距解决可读性与可操作性问题。 | 内容贴边导致误触或阅读困难。 |
| 页面离开时清理监听 | 页面销毁或路由切换 | `display.off(...)` | 避免旧页面继续响应折展事件。 | 状态串扰、性能下降。 |

## 验证清单

- 悬停态下关键按钮、输入框不落在折痕区。
- 分区边界与真实折痕边界对齐（误差应控制在 `<= 1` 布局单位）。
- 分界线与折痕中点一致，且仅作为视觉辅助或计算中间量。
- 需要安全间距时，确认上分区内容与折痕上边界至少 `16 vp`，下分区内容与折痕下边界至少 `40 vp`。
- 折展切换后布局可稳定刷新，无明显跳变。

## 官方来源

- [折叠屏悬停态适配（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-folded-hover)
