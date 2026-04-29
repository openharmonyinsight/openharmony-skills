## 资源索引

资源优先级约定：
- `P0`：官方推荐文档路径（优先加载，作为主方案）。
- `P1`：基于官方 API 的工程模板或场景化落实清单（用于加速落地，不替代 `P0`）。

## 三块主线结构（方向适配）

> 当前模块的方向适配按三块主线组织：`检测监听`、`适配策略`、`问题修复`。

| 主线 | 主资源（P0） | 关键验收点 |
| --- | --- | --- |
| 检测监听 | `RSC_ORIENT_03` | display/window 监听时序正确、传感器数据防抖 |
| 适配策略 | `RSC_ORIENT_02` | 各设备形态方向行为一致、断点判断准确 |
| 问题修复 | `RSC_ORIENT_05` | 根因归类准确、修复后无回归 |

#### `RSC_ORIENT_01` 方向概念与 API 速查

```yaml
resource_id: RSC_ORIENT_01
resource_type: reference
path: ./orientation_concepts.md
phase_tags: [REQ, FIX]
priority: P0
used_for:
  - 理解屏幕旋转/屏幕方向/窗口方向的区别
  - 掌握自然方向概念和 18 种旋转策略
  - API 速查（display/window 核心接口）
load_when:
  - 需求阶段定义设备方向差异
  - Bug 修复时确认概念是否混淆
  - 需要选择旋转策略枚举值
avoid_when:
  - 已明确概念和策略，只需写代码
supports_scenes:
  - ORIENT-02
  - ORIENT-03
  - ORIENT-04
output_fields:
  - device_constraints
  - capability_boundary
  - problem_profile
  - root_cause_hypothesis
```

#### `RSC_ORIENT_02` 多设备方向适配指南

```yaml
resource_id: RSC_ORIENT_02
resource_type: reference
path: ./orientation_adaptation.md
phase_tags: [REQ, DEV, FIX]
priority: P0
used_for:
  - 多设备方向适配策略（一多）
  - 断点判断与 348vp 阈值
  - follow_desktop 策略详解
  - 三折叠 G 态适配
  - module.json5 方向配置
  - 常见方向适配问题
load_when:
  - 命中 ORIENT-02
  - 一多场景方向适配设计或实现
  - 需要选择设备方向映射策略
avoid_when:
  - 纯概念理解不涉及适配实现
supports_scenes:
  - ORIENT-02
  - ORIENT-04
output_fields:
  - device_constraints
  - code_touchpoints
  - implementation_notes
  - integration_risks
  - fix_plan
```

#### `RSC_ORIENT_03` 旋转检测指南

```yaml
resource_id: RSC_ORIENT_03
resource_type: reference
path: ./rotation_detection.md
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 传感器旋转检测（重力传感器 atan2）
  - 监听屏幕/窗口方向变化
  - 调试旋转问题（hdc 命令、日志过滤）
  - API 版本要求
load_when:
  - 命中 ORIENT-01
  - 需要获取连续旋转角度
  - 需要监听方向变化
  - 需要调试旋转问题
avoid_when:
  - 只需系统旋转策略，不需要自定义检测
supports_scenes:
  - ORIENT-01
output_fields:
  - code_touchpoints
  - implementation_notes
  - fix_plan
  - verification_matrix
```

#### `RSC_ORIENT_04` 视频横竖屏切换指南

```yaml
resource_id: RSC_ORIENT_04
resource_type: reference
path: ./video_rotation.md
phase_tags: [DEV, FIX]
priority: P1
used_for:
  - 视频类应用横竖屏切换实现
  - 短视频自适应旋转
  - adaptive_video 三方库使用
  - 屏幕锁定功能
  - 横竖屏切换性能优化
load_when:
  - 命中 ORIENT-03
  - 视频播放页需要横竖屏切换
  - 短视频页面需要自适应旋转
avoid_when:
  - 非视频类应用的方向适配
supports_scenes:
  - ORIENT-03
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - fix_plan
```

#### `RSC_ORIENT_05` 方向适配问题修复场景库

```yaml
resource_id: RSC_ORIENT_05
resource_type: reference
path: ./bug-fix-cases.md
phase_tags: [DEV, FIX, VAL]
priority: P1
used_for:
  - 方向适配实际 Bug 案例与修复方案
  - 折叠屏展开态被强制竖屏
  - Tabs + Swiper 方向锁定
  - 分屏/悬浮窗下旋转失效
  - 视频全屏退出方向未恢复
  - 折叠屏开合布局闪烁
load_when:
  - 命中 ORIENT-04
  - 遇到方向适配 Bug
avoid_when:
  - 新需求设计，不涉及 Bug 修复
supports_scenes:
  - ORIENT-04
output_fields:
  - problem_profile
  - root_cause_hypothesis
  - fix_plan
  - regression_watchlist
  - verification_matrix
```

#### `RSC_ORIENT_06` 获取设备旋转角度资产

```yaml
resource_id: RSC_ORIENT_06
resource_type: asset
path: ../assets/GetDeviceRotation.ets
phase_tags: [DEV]
priority: P0
used_for:
  - 获取设备屏幕旋转角度的示例代码
load_when:
  - 需要读取 display.rotation 值
  - 命中 ORIENT-01
avoid_when:
  - 不需要直接读取 rotation
supports_scenes:
  - ORIENT-01
output_fields:
  - code_touchpoints
  - reuse_resources
```

#### `RSC_ORIENT_07` Display API 完整示例资产

```yaml
resource_id: RSC_ORIENT_07
resource_type: asset
path: ../assets/DisplayApiExample.ets
phase_tags: [DEV]
priority: P1
used_for:
  - display API 完整使用示例
  - 获取 display 属性、监听 display 变化
load_when:
  - 需要获取 display 属性、监听 display 变化
avoid_when:
  - 已有成熟封装可用
supports_scenes:
  - ORIENT-01
output_fields:
  - code_touchpoints
  - reuse_resources
```

#### `RSC_ORIENT_08` 统一方向检测封装资产

```yaml
resource_id: RSC_ORIENT_08
resource_type: asset
path: ../assets/OrientationDetector.ets
phase_tags: [DEV, FIX]
priority: P0
used_for:
  - 统一方向检测封装（单例）
  - 基于 display/window 监听实现方向变化感知、自然方向判定和方向控制
load_when:
  - 需要监听屏幕/窗口方向变化
  - 需要统一管理多设备方向检测
  - 需要获取当前方向信息和运行时方向切换
avoid_when:
  - 只需简单的单次方向读取（用 RSC_ORIENT_06）
  - 需要传感器连续角度做动画（参考 RSC_ORIENT_03 传感器章节）
supports_scenes:
  - ORIENT-01
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
```

#### `RSC_ORIENT_09` 窗口方向设置示例资产

```yaml
resource_id: RSC_ORIENT_09
resource_type: asset
path: ../assets/OrientationExample.ets
phase_tags: [DEV]
priority: P1
used_for:
  - 窗口方向设置和运行时动态切换示例
  - 监听窗口尺寸变化判断横竖屏
load_when:
  - 需要实现动态旋转策略切换
  - 命中 ORIENT-02
avoid_when:
  - 已有成熟方案
supports_scenes:
  - ORIENT-02
output_fields:
  - code_touchpoints
  - reuse_resources
```

#### `RSC_ORIENT_10` 一多场景方向适配完整示例资产

```yaml
resource_id: RSC_ORIENT_10
resource_type: asset
path: ../assets/OneMultiOrientationDemo.ets
phase_tags: [DEV]
priority: P1
used_for:
  - 一多场景方向适配完整示例
  - 含断点判断和设备类型适配
load_when:
  - 需要一多场景完整适配参考
  - 命中 ORIENT-02
avoid_when:
  - 只需简单单设备适配
supports_scenes:
  - ORIENT-02
output_fields:
  - code_touchpoints
  - reuse_resources
```
