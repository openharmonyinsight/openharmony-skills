---
name: hmos-multidevice-hardware-access
description: Handle HarmonyOS hardware-capability adaptation through a declarative scene and resource index. Use when the task involves camera selection, camera rotation/stride/foldable adaptation, sensor availability, canIUse or SysCap checks, hardware fallback strategy, external device access, or multi-device hardware behavior differences.
---

# 硬件调用适配

## 技能定义

| 字段 | 内容 |
| --- | --- |
| `skill_id` | `hardware-access` |
| `skill_name` | `硬件调用适配` |
| `one_line_purpose` | 为硬件能力检测、相机适配、传感器和外接设备提供统一接入与降级策略。 |
| `device_scope` | `phone / tablet / pc / foldable / wearables / 2in1` |
| `problem_scope` | `SysCap、canIUse、相机枚举、折叠态相机重建、预览旋转、拍照旋转、stride花屏、传感器、GPS、NFC、蓝牙、外接设备、热插拔` |
| `not_in_scope` | `与硬件无关的纯 UI 布局问题、无能力差异的普通业务逻辑、视频编解码与流媒体、第三方相机库` |
| `primary_outputs` | `primary_scene`、`device_constraints`、`code_touchpoints`、`fix_plan`、`verification_matrix` |

## 核心约束

### 通用硬件约束

1. 先做能力检测，再调用相关 API。
2. 涉及系统能力时，必须同时检查 `canIUse()` 和 `module.json5` 声明。
3. 涉及相机时优先枚举设备，不要硬编码相机 ID。
4. 涉及传感器时必须说明注册、取消注册和生命周期解绑逻辑。
5. 涉及外接设备时必须说明连接、断开、热插拔后的状态刷新策略。
6. 输出方案必须包含"不支持时怎么降级、隐藏、替代或提示"。

### 相机专用约束

7. **折叠状态变化必须重建相机**：折叠状态切换时，折叠前选择的相机可能不再可用，必须监听 `foldStatusChange` 并重新选择相机设备、重建 XComponent 和预览流。半折叠态（悬停态）是折叠/展开的过渡状态，正常情况下应忽略半折叠态变化、跳过重建；仅在用户明确需要悬停态适配时（HW-02-hover）才处理
8. **stride 必须与 width 比对**：通过 ImageReceiver 获取预览帧数据做二次处理时，`image.Component.rowStride` 与 `width` 不一致必须去除无效像素，否则花屏（堆叠状偏移）；stride 因平台而异，不可硬编码
9. **Surface 宽高比必须匹配预览流旋转后的比例**：`display.rotation` 为 0°/180° 时 Surface 宽高比是预览宽高比的倒数，90°/270° 时与预览宽高比相同。注意：画面拉伸/压缩（比例不匹配）归本约束；花屏堆叠（像素偏移）归约束 8
10. **预览旋转角度 = 镜头安装角度 + 屏幕旋转角度**：后置镜头安装角度 90°，前置镜头安装角度 270°；屏幕旋转角度通过 `Display.rotation × 90°` 获取。推荐使用 `getPreviewRotation()` API 获取，无需手动计算
11. **拍照旋转角度依赖重力传感器**：后置相机 `拍照旋转角度 = 镜头安装角度(90°) + 重力方向`，前置相机 `拍照旋转角度 = 镜头安装角度(270°) - 重力方向`；必须在 `capture()` 时设置 `rotation` 参数
12. **阔折叠外屏（如 PuraX）仅有前置相机**：阔折叠设备外屏可能仅有前置相机，切换到外屏时必须处理后置相机不可用的情况
13. **旋转策略区分**：sm 断点设备不支持旋转，md/lg 断点设备支持旋转（窗口最小维度 ≥ 600vp）
14. **2in1 设备相机特点**：2in1 设备大部分仅有前置内置相机，少部分同时有后置内置相机；外接摄像头不属于 HW-02 范围，归 HW-04

## 阶段标签

| 标签 | 阶段 | 当前模块关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 能力边界、设备差异、降级策略、相机能力与折叠态适配范围 |
| `DEV` | 开发 | 检测入口、枚举逻辑、生命周期绑定、折叠态相机重建、stride 处理、旋转角度计算 |
| `FIX` | 问题修复 | 无能力崩溃、相机选择错误、预览花屏、旋转异常、传感器泄漏、热插拔失效 |
| `VAL` | 功能验证 | canIUse 结果、设备枚举结果、降级行为、连接切换证据、相机功能全设备验证 |

## 统一输出字段

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`
- `REQ`：`device_constraints`、`capability_boundary`、`acceptance_focus`
- `DEV`：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- `FIX`：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- `VAL`：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`

## 字段释义

- `device_constraints`：指由设备硬件能力差异带来的适配硬约束。包括哪些设备具备目标硬件、调用前必须做哪些检测、缺失能力时是否必须降级、隐藏或替代；对于相机场景还包括 stride 值、折叠态限制等。
- `capability_boundary`：指当前方案支持哪些硬件能力组合、不支持哪些设备、哪些能力必须通过枚举或声明校验后才可用。
- `acceptance_focus`：指需求阶段验收时必须确认的能力检测结果、降级路径和设备切换行为。
- scene 中 `deliverables.REQ` 出现 `device_constraints`，表示"该硬件场景命中后，需求阶段必须先明确能力差异约束"，不是对字段重复说明。

## AI 检索要求

- 涉及是否支持某硬件能力、页面要不要展示功能入口时，优先命中 `HW-01`。
- 涉及拍照、预览、切前后摄、折叠态相机切换、相机花屏、旋转异常时，优先命中 `HW-02`。
- 涉及加速度、陀螺仪、光线、距离、GPS 等传感器时，优先命中 `HW-03`。
- 涉及 PC 外接摄像头、键盘、鼠标或 USB 热插拔时，优先命中 `HW-04`。

## 场景索引

#### `HW-01` 能力检测与功能降级

```yaml
scene_id: HW-01
scene_name: 能力检测与功能降级
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - canIUse
  - SystemCapability
  - SysCap
  - module.json5
  - 不支持
applies_when:
  - 需要判断设备是否支持某硬件能力
  - 当前问题表现为不支持设备上仍显示功能入口或直接调用崩溃
not_applies_when:
  - 当前功能不依赖任何设备硬件差异
decisions:
  - 定义能力检测入口和展示策略
  - 决定不支持时是隐藏、置灰、替代还是提示
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_HW_01
  - RSC_HW_02
```

#### `HW-02` 相机选择、预览与形态切换

```yaml
scene_id: HW-02
scene_name: 相机选择、预览与形态切换
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - 相机枚举
  - 前置相机
  - 后置相机
  - 预览旋转
  - 折叠屏相机
  - 花屏
  - stride
  - 拍照旋转
  - 录像角度
applies_when:
  - 需要拍照、预览、切前后摄或适配不同设备形态下的相机行为
  - 当前问题表现为默认相机错误、预览角度不对或设备切换后相机失效
  - 折叠状态变化导致相机设备不可用、黑屏
  - 预览流花屏、堆叠状偏移
  - 预览/拍照/录像旋转角度异常
not_applies_when:
  - 当前功能不使用相机
  - 外接摄像头（归 HW-04）
decisions:
  - 确定相机枚举逻辑和默认设备选择策略
  - 决定方向、预览、设备形态切换后的同步行为
  - 处理 stride 内存对齐问题
  - 计算预览/拍照/录像旋转角度
sub_scenes:
  - HW-02-fold: 折叠屏相机设备选择与重建
  - HW-02-layout: 基于断点的相机控制按钮布局
  - HW-02-stride: 预览流 stride 处理防花屏
  - HW-02-preview-rotation: 预览旋转角度与 Surface 宽高比
  - HW-02-capture-rotation: 拍照/录像旋转角度
  - HW-02-hover: 悬停态相机页面（可选，explicit_only）
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_HW_03
  - RSC_HW_04
  - RSC_HW_08
  - RSC_HW_09
  - RSC_HW_10
  - RSC_HW_11
  - RSC_HW_12
```

##### HW-02 子场景说明

| 子场景 | 说明 | 关键验收点 |
| --- | --- | --- |
| HW-02-fold | 折叠状态变化时相机设备选择与重建。覆盖阔折叠外屏仅前置、2in1 内置相机等特殊场景 | 折叠态切换无黑屏、相机设备正确重建 |
| HW-02-layout | 为不同设备类型和屏幕尺寸设计适配的相机界面控制按钮布局 | 各断点按钮布局正确 |
| HW-02-stride | 通过 ImageReceiver 获取预览流每帧数据做二次处理时，正确处理 stride 内存对齐 | stride ≠ width 时像素处理正确，无花屏堆叠 |
| HW-02-preview-rotation | 预览旋转角度获取与设置、Surface 宽高比计算 | 预览方向正确、无拉伸 |
| HW-02-capture-rotation | 拍照/录像旋转角度依赖重力传感器计算 | 拍照/录像角度与设备持握方向一致 |
| HW-02-hover | 折叠屏半折叠（悬停态）且横屏时的相机页面适配。仅在应用明确需要悬停态适配时启用，不主动添加 | 悬停态布局和旋转正确 |

##### HW-02 路由规则

```yaml
routing_rules:
  - keywords: [折叠, 折叠屏, foldStatus, 相机切换, PuraX, 外屏, 折叠后相机不可用]
    sub_scene: HW-02-fold
  - keywords: [断点, 相机按钮布局, 屏幕尺寸, 相机界面布局, 大屏按钮, 按钮显示异常, 按钮截断]
    sub_scene: HW-02-layout
  - keywords: [花屏, stride, 堆叠状, 内存对齐, rowStride, PixelMap, 预览花屏]
    sub_scene: HW-02-stride
  - keywords: [预览旋转, 预览方向, getPreviewRotation, setPreviewRotation, 预览拉伸, Surface宽高比, 预览画面压缩, 相机旋转]
    sub_scene: HW-02-preview-rotation
    auto_load_concepts: [RSC_HW_12]
  - keywords: [拍照方向, 照片旋转, 重力传感器, GRAVITY, capture(rotation), 录像角度, 录像方向]
    sub_scene: HW-02-capture-rotation
    auto_load_concepts: [RSC_HW_12]
  - keywords: [悬停态相机, 半折叠相机, FOLD_STATUS_HALF_FOLDED相机, 悬停态相机布局]
    sub_scene: HW-02-hover
    trigger_policy: explicit_only
    trigger_note: >
      半折叠态是折叠/展开的过渡状态，默认不路由。
      仅当用户提示词中显式包含"悬停态"+"相机"相关表述时才路由到 HW-02-hover。
      普通折叠切换导致的相机问题归 HW-02-fold。
```

#### `HW-03` 传感器订阅、读取与解绑

```yaml
scene_id: HW-03
scene_name: 传感器订阅、读取与解绑
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - 加速度
  - 陀螺仪
  - 光线
  - 距离
  - GPS
  - 生命周期解绑
applies_when:
  - 需要读取或订阅传感器数据
  - 当前问题表现为传感器不可用、数据不刷新或页面退出后未解绑
not_applies_when:
  - 功能不依赖传感器数据
decisions:
  - 选择订阅方式、刷新频率和生命周期绑定点
  - 决定传感器不可用时的回退逻辑
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_HW_05
  - RSC_HW_06
```

#### `HW-04` 外接设备与热插拔

```yaml
scene_id: HW-04
scene_name: 外接设备与热插拔
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - 外接设备
  - USB
  - 热插拔
  - 外接摄像头
  - 设备断连
applies_when:
  - 页面要适配外接摄像头、键盘、鼠标或 USB 设备
  - 当前问题表现为外接后状态不刷新或断开后仍保留旧状态
not_applies_when:
  - 当前功能只运行在单一内置硬件环境
decisions:
  - 定义连接、断开、热插拔后的状态刷新策略
  - 决定断连后的恢复、重试和回退行为
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_HW_07
  - RSC_HW_01
```

## 资源索引

### 通用硬件资源

#### `RSC_HW_01` 能力检测参考

```yaml
resource_id: RSC_HW_01
resource_type: reference
path: ./references/syscap_mechanism.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义 SysCap 和 canIUse 的检测边界
  - 设计功能展示、降级和异常提示策略
load_when:
  - 命中 HW-01 或 HW-04
avoid_when:
  - 当前功能不依赖硬件差异
supports_scenes:
  - HW-01
  - HW-04
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - fix_plan
  - verification_matrix
```

#### `RSC_HW_02` 能力检测实现资产

```yaml
resource_id: RSC_HW_02
resource_type: asset
path: ./assets/SysCapChecker.ets
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 能力检测主实现示例
  - 复用 CanIUseExample 的接线方式
load_when:
  - 需要落能力检测和功能开关代码
avoid_when:
  - 当前只做需求分析
supports_scenes:
  - HW-01
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - pass_criteria
```

### 相机资源

#### `RSC_HW_03` 相机适配参考

```yaml
resource_id: RSC_HW_03
resource_type: reference
path: ./references/camera-device-selection.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 设计相机枚举、默认选择和预览行为
  - 多设备环境下的相机设备选择逻辑
  - 阔折叠外屏/2in1 设备相机回退策略
  - 热启动相机恢复
load_when:
  - 命中 HW-02
avoid_when:
  - 当前不涉及相机
supports_scenes:
  - HW-02
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - root_cause_hypothesis
  - verification_matrix
```

#### `RSC_HW_04` 相机实现资产

```yaml
resource_id: RSC_HW_04
resource_type: asset
path: ./assets/CameraAdapter.ets
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 相机选择和预览主示例
  - 复用 CameraExample、CameraPreviewExample、GetAvailableCameras 的枚举与预览方式
load_when:
  - 需要实现或修复相机逻辑
avoid_when:
  - 当前只做需求分析
supports_scenes:
  - HW-02
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - regression_watchlist
  - pass_criteria
```

#### `RSC_HW_08` 折叠屏相机适配参考

```yaml
resource_id: RSC_HW_08
resource_type: reference
path: ./references/camera-foldable-display.md
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 折叠状态变化时的相机设备选择与重建
  - XComponent 重建实现
  - 折叠状态监听方式选择
  - 半折叠态过滤策略
load_when:
  - 命中 HW-02-fold 或 HW-02-hover
avoid_when:
  - 当前不涉及折叠态相机切换
supports_scenes:
  - HW-02
output_fields:
  - code_touchpoints
  - fix_plan
  - verification_matrix
```

#### `RSC_HW_09` 预览流 stride 处理参考

```yaml
resource_id: RSC_HW_09
resource_type: reference
path: ./references/camera-stride-handling.md
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 处理预览流 stride 内存对齐导致的相机花屏
  - ImageReceiver 二次处理场景
load_when:
  - 命中 HW-02-stride
  - 出现相机预览花屏、堆叠状
avoid_when:
  - 不涉及 ImageReceiver 帧数据处理
supports_scenes:
  - HW-02
output_fields:
  - code_touchpoints
  - fix_plan
  - verification_matrix
```

#### `RSC_HW_10` 相机旋转角度适配参考

```yaml
resource_id: RSC_HW_10
resource_type: reference
path: ./references/camera-rotation-adaptation.md
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 预览旋转角度获取与设置
  - Surface 宽高比计算
  - 拍照旋转角度计算
  - 录像旋转角度设置
load_when:
  - 命中 HW-02-preview-rotation 或 HW-02-capture-rotation
  - 出现预览拉伸、拍照方向异常
avoid_when:
  - 不涉及旋转角度问题
supports_scenes:
  - HW-02
output_fields:
  - code_touchpoints
  - fix_plan
  - verification_matrix
```

#### `RSC_HW_11` 相机问题修复场景库

```yaml
resource_id: RSC_HW_11
resource_type: reference
path: ./references/camera-bug-fix-cases.md
phase_tags: [FIX, VAL]
priority: P0
used_for:
  - 相机问题定位与修复
  - 正反例代码片段参考
  - 区分根因、问题场景和解决方案
load_when:
  - 命中 HW-02 且处于 FIX 阶段
  - 需要参考正反例代码
avoid_when:
  - 仅在需求分析阶段
supports_scenes:
  - HW-02
output_fields:
  - fix_plan
  - code_touchpoints
  - verification_matrix
```

#### `RSC_HW_12` 相机旋转角度术语参考

```yaml
resource_id: RSC_HW_12
resource_type: reference
path: ./references/camera-rotation-terms.md
phase_tags: [REQ, DEV, FIX]
priority: P0
used_for:
  - 理解相机旋转相关角度概念和术语
  - 作为角度适配的概念基线
  - 角度概念混淆排查
load_when:
  - 命中 HW-02-preview-rotation 或 HW-02-capture-rotation
  - 需求分析阶段涉及相机旋转
avoid_when:
  - 仅需实现代码，不涉及角度问题
supports_scenes:
  - HW-02
output_fields:
  - device_constraints
  - capability_boundary
```

### 传感器资源

#### `RSC_HW_05` 传感器参考

```yaml
resource_id: RSC_HW_05
resource_type: reference
path: ./references/sensor_adaptation.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 设计传感器可用性判断和订阅策略
  - 定义传感器不可用时的回退行为
load_when:
  - 命中 HW-03
avoid_when:
  - 当前不涉及传感器
supports_scenes:
  - HW-03
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - fix_plan
  - verification_matrix
```

#### `RSC_HW_06` 传感器实现资产

```yaml
resource_id: RSC_HW_06
resource_type: asset
path: ./assets/SensorAdapter.ets
phase_tags: [DEV, FIX, VAL]
priority: P0
used_for:
  - 传感器订阅和解绑主示例
  - 校验生命周期内的注册与释放逻辑
load_when:
  - 需要落传感器订阅代码
avoid_when:
  - 当前不进入开发或验证阶段
supports_scenes:
  - HW-03
output_fields:
  - code_touchpoints
  - reuse_resources
  - implementation_notes
  - evidence_requirements
  - pass_criteria
```

### 外接设备资源

#### `RSC_HW_07` 外接设备参考

```yaml
resource_id: RSC_HW_07
resource_type: reference
path: ./references/external_devices.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
used_for:
  - 设计外接设备连接、断开和热插拔策略
  - 定义外接设备断连后的恢复行为
load_when:
  - 命中 HW-04
avoid_when:
  - 当前不存在外设接入场景
supports_scenes:
  - HW-04
output_fields:
  - device_constraints
  - implementation_notes
  - root_cause_hypothesis
  - verification_matrix
  - residual_risks
```

## 问题修复场景库

> 完整问题修复场景（含正反例代码片段）参见 [camera-bug-fix-cases.md](./references/camera-bug-fix-cases.md)

## 设备特定考虑

### 阔折叠（如 PuraX）

- 外屏可能仅有前置相机（目前仅 PuraX 有此限制）
- 折叠状态：1:1 宽高比
- 展开状态：根据旋转角度为 3:4 或 4:3 宽高比

### 双折叠

- 折叠状态：类似于手机（3:4）
- 展开状态：更大的屏幕，支持旋转（4:3）

### 三折叠

- F 态（折叠）：类似于手机（3:4）
- M 态（部分展开）：中等屏幕（4:3）
- G 态（完全展开）：最大屏幕，支持旋转（4:3）

### 平板（tablet）

- 大屏幕，支持旋转
- 4:3 宽高比

### 2in1

- 大部分仅有前置内置相机，少部分同时有后置
- 外接摄像头不属于 HW-02 范围，归 HW-04
- 屏幕较大，通常使用 lg 断点布局

## 阶段输出契约

### `REQ`

- 必须输出：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`
- 必须输出：`device_constraints`、`capability_boundary`、`acceptance_focus`
- 额外要求：明确目标硬件能力、最小支持设备范围以及不支持时的降级方式

### `DEV`

- 必须输出：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- 额外要求：明确能力检测入口、枚举入口和生命周期绑定点

### `FIX`

- 必须输出：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- 额外要求：明确问题属于能力判断缺失、枚举错误、解绑缺失、热插拔状态未刷新、stride 未处理还是旋转角度计算错误

### `VAL`

- 必须输出：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`
- 额外要求：至少给出能力检测结果、设备枚举结果以及降级行为是否正确的证据；相机场景需覆盖多设备多折叠态多方向验证
