# 高级主题：内置对象与 animateTo 迁移

## 内置对象迁移

### 滚动组件（List/WaterFlow的ChildrenMainSize/WaterFlowSections）

V1中 @State 可观察这些框架内置对象的API调用。V2中 @Local 只能观察自身变化，且无法给框架类加 @Trace。

**解决方案**：使用 `UIUtils.makeObserved()`
```typescript
import { UIUtils } from '@kit.ArkUI';

// V1
@State listChildrenSize: ChildrenMainSize = new ChildrenMainSize(100);

// V2
listChildrenSize: ChildrenMainSize = UIUtils.makeObserved(new ChildrenMainSize(100));
```

> 从API version 22开始，可直接用 @Local 标注 ChildrenMainSize。

### attributeModifier

V1用 @State 观察 Modifier 变化，V2用 makeObserved：
```typescript
// V1
@State modifier: MyButtonModifier = new MyButtonModifier();

// V2
modifier: MyButtonModifier = UIUtils.makeObserved(new MyButtonModifier());
```

### CommonModifier / 组件Modifier

同 attributeModifier，使用 makeObserved：
```typescript
@Local myModifier: TextModifier = UIUtils.makeObserved(new MyModifier().width(100).height(100));
```
整体赋值时也需 makeObserved：
```typescript
this.myModifier = UIUtils.makeObserved(new MyModifier().backgroundColor(Color.Orange));
```

### AttributeUpdater

V2中需给 AttributeUpdater 子类加 @ObservedV2，属性加 @Trace，且需在 initializeModifier 中触发属性读取以建立关联：
```typescript
@ObservedV2
class MyButtonModifier extends AttributeUpdater<ButtonAttribute> {
  @Trace public flag: boolean = false;
  initializeModifier(instance: ButtonAttribute): void {
    this.flag; // 触发读取建立关联
    instance.backgroundColor('#ff2787d9').width('50%').height(30)
  }
}
```

## animateTo 迁移

### 问题
V2的异步更新机制与 animateTo 不兼容：animateTo 闭包前的额外状态修改不会生效。

### API < 22 解决方案
用 `animateToImmediately({ duration: 0 }, () => {})` 先同步刷新：
```typescript
this.w = 100;
this.h = 100;
animateToImmediately({ duration: 0 }, () => {})
this.getUIContext().animateTo({ duration: 1000 }, () => {
  this.w = 200;
  this.h = 200;
})
```

### API >= 22 解决方案
用 `UIUtils.applySync()` 同步刷新：
```typescript
import { UIUtils } from '@kit.ArkUI';

UIUtils.applySync(() => {
  this.w = 100;
  this.h = 100;
})
this.getUIContext().animateTo({ duration: 1000 }, () => {
  this.w = 200;
  this.h = 200;
})
```

## V1与V2更新机制差异

| 特性 | V1 | V2 |
|------|-----|-----|
| 观察方式 | 同步 | 异步（Promise） |
| @Watch/@Monitor触发 | 同步 | 异步（事件逻辑完成后） |
| 每VSync重渲染次数 | 最多3次 | 最多3次 |
| @Computed更新 | 无 | @Monitor之前执行 |
| 一帧内多次修改 | 每次修改立即触发 | 以最终结果判断是否触发 |
