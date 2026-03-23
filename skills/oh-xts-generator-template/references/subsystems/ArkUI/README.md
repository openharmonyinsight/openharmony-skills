# ArkUI 子系统配置目录

> **版本**: 3.0.0
> **更新日期**: 2026-02-13
> **来源**: 基于 ARKUI_XTS_GENERATOR 配置整合

---

## 文档结构

本目录包含 ArkUI 子系统的完整配置，采用 **6 大接口分类** 的模块化架构：

```
ArkUI/
├── _common.md           # 子系统通用配置（核心文档）
├── arkui.md            # 接口分类概览
├── README.md            # 本文件
│
├── 01_component.md     # UI 组件接口测试指南
├── 02_layout.md        # 布局样式接口测试指南
├── 03_state.md         # 状态管理接口测试指南
├── 04_event.md         # 事件交互接口测试指南
├── 05_animation.md     # 动画转场接口测试指南
└── 06_system.md        # 系统能力接口测试指南
```

---

## 接口分类说明

| 分类 | 说明 | 优先级 | 详细文档 |
|------|------|--------|---------|
| **UI 组件接口** | 搭界面、放控件 | 核心 | [01_component.md](./01_component.md) |
| **布局样式接口** | 控制布局和外观 | 核心 | [02_layout.md](./02_layout.md) |
| **状态管理接口** | 响应式数据绑定 | 核心 | [03_state.md](./03_state.md) |
| **事件交互接口** | 响应用户操作 | 核心 | [04_event.md](./04_event.md) |
| **动画转场接口** | 动效和过渡 | 次要 | [05_animation.md](./05_animation.md) |
| **系统能力接口** | 与系统交互 | 次要 | [06_system.md](./06_system.md) |

---

## 使用指南

### 1. 快速开始

**步骤 1**：阅读接口分类概览 [arkui.md](./arkui.md)，了解 6 大接口分类

**步骤 2**：根据需要测试的 API 类型，选择对应的接口分类文档

**步骤 3**：参考 [_common.md](./_common.md) 了解通用测试规范

---

### 2. 各接口分类说明

#### 01. UI 组件接口测试指南

**适用场景**：
- 组件构造方法测试（Button()、Text() 等）
- 组件属性测试（fontColor、fontSize 等）
- 组件默认值测试

**关键要点**：
- 构造方法检查：既要检查组件存在，也要检查属性值生效
- 颜色格式断言：组件树返回 `#AARRGGBB` 格式
- 使用相对高度 `5%` 避免设备分辨率差异

**示例文档**：[01_component.md](./01_component.md)

---

#### 02. 布局样式接口测试指南

**适用场景**：
- 尺寸属性测试（width、height、padding、margin）
- 边框样式测试（border、borderColor、borderRadius）
- 背景样式测试（backgroundColor、opacity）
- 对齐方式测试（alignItems、justifyContent）

**关键要点**：
- 尺寸返回值带单位（如 `'200.00vp'`、`'5.00%'`）
- 边框属性在组件树中以独立属性存在（borderLeftWidth、borderRightWidth 等）
- CSS 概念对应关系清晰

**示例文档**：[02_layout.md](./02_layout.md)

---

#### 03. 状态管理接口测试指南

**适用场景**：
- @State 状态变化测试
- @Prop 单向传递测试
- @Link 双向绑定测试
- @Observed/@ObjectLink 嵌套对象测试

**关键要点**：
- 通过 UI 属性验证状态，而非直接访问状态变量
- 状态变化后需要等待 UI 更新完成（sleep 500ms）
- 测试父组件修改是否影响子组件，反之亦然

**示例文档**：[03_state.md](./03_state.md)

---

#### 04. 事件交互接口测试指南

**适用场景**：
- onClick 点击事件测试
- onTouch 触摸事件测试
- onAppear/onDisAppear 生命周期事件测试
- 手势事件测试（TapGesture、LongPressGesture 等）

**关键要点**：
- 使用 UiTest API 触发事件（Driver.create()、findComponent()、click()）
- 事件触发后需要等待足够时间让 UI 更新
- 手势测试通常为 LEVEL1 或更高级别

**示例文档**：[04_event.md](./04_event.md)

---

#### 05. 动画转场接口测试指南

**适用场景**：
- animateTo 显式动画测试
- animation 隐式动画测试
- 属性动画测试（scale、rotate、translate）
- transition 转场动画测试

**关键要点**：
- 验证最终状态，而非动画过程
- 动画等待时间应大于 duration（如 duration: 300ms，等待 500ms）
- 转场动画可能涉及组件的创建和销毁

**示例文档**：[05_animation.md](./05_animation.md)

---

#### 06. 系统能力接口测试指南

**适用场景**：
- Router 路由测试（pushUrl、replaceUrl、back）
- DeviceInfo 设备信息测试
- Preferences 数据存储测试
- HTTP 网络请求测试

**关键要点**：
- **无需创建测试页面**，直接在 test.ets 中调用 API
- 使用 async/await 或 done 回调处理异步操作
- 测试应包含成功和失败场景
- 系统资源使用后需要清理（如 HTTP 连接 destroy()）

**示例文档**：[06_system.md](./06_system.md)

---

## 通用测试规范

所有接口分类测试都遵循 [_common.md](./_common.md) 中定义的通用规范：

| 规范项 | 说明 | 参考章节 |
|--------|------|---------|
| **ID 命名规范** | 格式：`{component}_{test_name}`，必须唯一且有语义 | _common.md 3.2 |
| **高度设置规范** | 推荐使用相对高度 `5%`，避免设备分辨率差异 | _common.md 3.3 |
| **颜色格式断言** | 组件树返回 `#AARRGGBB` 格式，断言时考虑大小写 | _common.md 5.2 |
| **TypeScript 类型规范** | 禁止使用 `any` 类型，所有变量必须明确类型 | _common.md 第五章 |
| **等价类参数精简** | 同类型参数只需选择 2 个代表性值 | _common.md 第七章 |
| **null/undefined 参数测试** | 验证设置 null/undefined 时是否恢复默认值 | _common.md 第八章 |

---

## 测试用例编号规范

```
SUB_ARKUI_{组件}_{属性}_{类型}_{序号}
```

### 类型标识

| 类型 | 说明 | 示例 |
|------|------|------|
| PARAM | 参数测试 | SUB_ARKUI_BUTTON_FONTCOLOR_PARAM_001 |
| ERROR | 错误码测试 | SUB_ARKUI_BUTTON_FONTCOLOR_ERROR_001 |
| RETURN | 返回值测试 | SUB_ARKUI_BUTTON_FONTCOLOR_RETURN_001 |
| BOUNDARY | 边界值测试 | SUB_ARKUI_TEXT_FONTSIZE_BOUNDARY_001 |
| EVENT | 事件测试 | SUB_ARKUI_BUTTON_ONCLICK_EVENT_001 |

---

## 测试文件组织

### 页面侧（src/main/ets/pages/）

```
pages/
└── button/
    ├── ButtonFontColor.ets    # 页面文件
    └── ButtonOnClick.ets       # 页面文件
```

### 测试侧（src/ohosTest/ets/test/）

```
test/
└── button/
    ├── ButtonFontColor.test.ets    # 测试文件
    └── ButtonOnClick.test.ets       # 测试文件
```

### 注册文件

- **页面注册**：`src/main/resources/base/profile/main_pages.json`
- **测试注册**：`src/ohosTest/ets/test/List.test.ets`

## 已废弃文档（不推荐使用）

以下文档已被新的 6 大接口分类文档替代，仅保留用于参考：

| 已废弃文档 | 替代文档 |
|----------|---------|
| `Component.md` | 01_component.md、02_layout.md 等 |
| `Animator.md` | 05_animation.md |
| `Router.md` | 06_system.md |

**建议**：使用新的 6 大接口分类文档，旧文档将在未来版本中移除。

---

## 参考资源

- **ARKUI_XTS_GENERATOR**：原始配置源项目
- **HarmonyOS 官方文档**：ArkUI API 参考文档
- **通用配置**：[../_common.md](../_common.md)

---

## 联系方式

如有问题或建议，请通过项目仓库提交 Issue。
