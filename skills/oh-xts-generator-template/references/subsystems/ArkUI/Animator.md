# Animator 模块配置

> **模块信息**
> - 所属子系统: ArkUI
> - 模块名称: Animator
> - API 声明文件: @ohos.animator.d.ts
> - 主要 API: animateTo, animateXXX, getAnimator 等
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、模块特有配置

### 1.1 模块概述

Animator 模块提供 ArkUI 的动画接口，包括属性动画、转场动画等功能。

### 1.2 API 声明文件

```
API声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.animator.d.ts
```

### 1.3 通用配置继承

本模块继承 ArkUI 子系统通用配置：

- **测试路径规范**: 见 `ArkUI/_common.md` 第 1.2 节
- **组件测试规则**: 见 `ArkUI/_common.md` 第 1.3.1 节
- **辅助工程配置**: 见 `ArkUI/_common.md` 第 2.2 节

## 二、模块特有 API 列表

### 2.1 动画API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| animateTo | 属性动画 | LEVEL0 | 参数、持续时间、回调 |
| animateXXX | XXX属性动画 | LEVEL1 | 特定属性动画 |
| getAnimator | 获取动画器 | LEVEL1 | 创建、配置、控制 |

### 2.2 转场API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| transition | 转场效果 | LEVEL1 | 类型、参数、组合 |
| animateTransition | 动画转场 | LEVEL2 | 复杂转场场景 |

## 三、模块特有测试规则

### 3.1 动画测试规则

1. **动画参数测试**：
   - 测试持续时间（duration）
   - 测试曲线（curve）
   - 测试延迟（delay）

2. **动画回调测试**：
   - 测试 onFinish 回调
   - 测试 onCancel 回调
   - 测试重复回调

3. **动画状态测试**：
   - 测试动画播放状态
   - 测试动画暂停/恢复
   - 测试动画取消

### 3.2 转场测试规则

1. **转场类型测试**：
   - 测试淡入淡出
   - 测试缩放
   - 测试滑动
   - 测试组合转场

2. **转场时机测试**：
   - 测试组件出现转场
   - 测试组件消失转场
   - 测试状态变化转场

## 四、模块特有代码模板

### 4.1 animateTo 测试模板

```typescript
/**
 * @tc.name ArkUI animateTo Animation Test
 * @tc.number SUB_ARKUI_ANIMATOR_ANIMATETO_001
 * @tc.desc 测试 animateTo 动画功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testAnimateTo001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建组件
  let component = new Component();
  component.width = 100;

  // 2. 执行动画
  let finishCalled = false;
  animateTo({
    duration: 1000,
    curve: Curve.EaseInOut,
    onFinish: () => {
      finishCalled = true;
    }
  }, () => {
    component.width = 200;
  });

  // 3. 验证动画执行
  // (需要等待动画完成)

  // 4. 验证回调
  expect(finishCalled).assertTrue();
});
```

## 五、测试注意事项

1. **动画持续时间**：
   - 测试时使用较短的持续时间
   - 避免测试时间过长

2. **异步验证**：
   - 动画是异步的
   - 需要等待动画完成后再验证

3. **性能测试**：
   - 测试动画流畅度
   - 测试帧率
   - 测试CPU/内存占用

## 六、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 Animator 模块配置
