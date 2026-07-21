# Eval: animateTo 动画 / Explicit animation

## Prompt（测试输入）

> 对 ArkUI 的 animateTo 显式动画做与 Android(ValueAnimator/ObjectAnimator/Compose 动画)、iOS(UIView.animate/Core Animation) 的竞品分析，给出能力与规格对比。

跑两遍：**with skill** 与 **without skill**。

## 预期关键发现 / Expected findings（with skill 必须命中）

ArkUI 侧以 `interface_sdk-js` 为准；状态/动画类高权重维度 1·3·7·8。

- [ ] **权威源**：ArkUI `animateTo(value: AnimateParam, event: () => void)`、`AnimateParam`(`duration`/`tempo`/`curve`/`delay`/`iterations`/`playMode`/`onFinish`)、`keyframeAnimateTo`、`curves.*`(`springMotion`/`cubicBezierCurve`/`stepsCurve`) 以 `interface_sdk-js` 为源；`@since`（核心 7+，子特性 标 `待核`）。
- [ ] **API 形态(1)**：状态驱动（`animateTo`/`withAnimation`/`animateXAsState`）vs 命令式（`ObjectAnimator`/`UIView.animate`/`CABasicAnimation`）。
- [ ] **规格精度(3)**：duration 默认值与单位（ArkUI 300ms / iOS 0.25s）；曲线预设与自定义贝塞尔/阶跃；弹簧参数（ArkUI response+dampingFraction vs CASpringAnimation mass/stiffness/damping）；`@since`。
- [ ] **性能/线程(7)**：主线程驱动 vs Core Animation 提交后离线渲染；ArkUI 声明式 diff 批量提交。
- [ ] **状态/生命周期(8)**：`onFinish` 回调；可中断/pause/resume/scrub 能力（ArkUI 较弱，UIViewPropertyAnimator 较强）；速度携带（velocity）。
- [ ] **心智(12)**：声明式终态 vs 命令式起止；编排容器（AnimatorSet/CAAnimationGroup vs ArkUI 无原生编排容器）。
- [ ] **不污染**：动画分析**不**引入触摸坐标/触点归属。
- [ ] **格式**：每平台结构化规格 + 用法代码；断言带来源编号；版本基线。

## 通过标准

- with skill：清单全中。
- without skill 对比：典型"概念形态描述、可能与版本略有出入"、不锁版本、无来源编号、自由结构。

## 备注

- 代表**状态/动画类**，验证框架在该类的适用性 + C7（不把 Touch 维度污染到动画）。
