# ArkUI 接口分类概览

> ArkUI（HarmonyOS UI 开发框架）的 6 大接口分类快速导航
>
> **版本**: 4.1.0
> **更新日期**: 2026-02-25
> **来源**: 基于 ARKUI_XTS_GENERATOR 配置整合
> **基于**: ArkUI/_common.md v4.1.0

---

## 接口分类总览

| 分类 | 说明 | 优先级 | 详细文档 |
|------|------|--------|---------|
| UI 组件接口 | 搭界面、放控件 | 核心 | [01_component.md](./01_component.md) |
| 布局样式接口 | 控制布局和外观 | 核心 | [02_layout.md](./02_layout.md) |
| 状态管理接口 | 响应式数据绑定 | 核心 | [03_state.md](./03_state.md) |
| 事件交互接口 | 响应用户操作 | 核心 | [04_event.md](./04_event.md) |
| 动画转场接口 | 动效和过渡 | 次要 | [05_animation.md](./05_animation.md) |
| 系统能力接口 | 与系统交互 | 次要 | [06_system.md](./06_system.md) |

---

## 各分类要点

### 一、UI 组件接口（Component APIs）

用来**搭界面、放控件**，是 ArkUI 最核心的一类。

**常见组件**：`Text`、`Image`、`Button`、`Row`、`Column`、`List`、`Grid`、`TextInput`...

**测试重点**：构造方法、属性默认值、不同类型参数

**→ 详细指南**：[01_component.md](./01_component.md)

---

### 二、布局样式接口（Layout & Style APIs）

用来**控制怎么排、长什么样**。

**常见接口**：`width()`、`height()`、`padding()`、`backgroundColor()`、`border()`、`fontSize()`...

**测试重点**：尺寸属性、样式属性、对齐方式

**→ 详细指南**：[02_layout.md](./02_layout.md)

---

### 三、状态管理接口（State Management APIs）

用来**让界面"动起来"**，是 ArkUI 的响应式核心。

**常见装饰器**：`@State`、`@Prop`、`@Link`、`@Observed`/`@ObjectLink`、`@Provide`/`@Consume`

**测试重点**：状态变化验证、父子组件传递、双向绑定

**→ 详细指南**：[03_state.md](./03_state.md)

---

### 四、事件交互接口（Event & Gesture APIs）

用来**响应用户操作**。

**常见接口**：`onClick()`、`onTouch()`、`onAppear()`、`TapGesture`、`LongPressGesture`...

**测试重点**：点击事件、生命周期事件、手势测试

**→ 详细指南**：[04_event.md](./04_event.md)

---

### 五、动画转场接口（Animation APIs）

用来**做动效和过渡**。

**常见接口**：`animateTo()`、`animation()`、`transition()`、`scale()`、`rotate()`...

**测试重点**：动画状态验证、转场效果

**→ 详细指南**：[05_animation.md](./05_animation.md)

---

### 六、系统能力接口（System & Ability APIs）

用来**和系统打交道**，通常来自 `@ohos.*` 模块。

**常见能力**：`router`、`UIAbility`、`deviceInfo`、`http`、`preferences`...

**测试重点**：API 调用、异步操作、错误处理

**→ 详细指南**：[06_system.md](./06_system.md)

---

## 快速参考

### 测试用例编号规范（ArkUI 特有）

**基础格式**（适用于大多数测试用例）：
```
SUB_ARKUI_{模块}_{组件}_{属性}_{类型}_{序号}
```

**详细格式**（适用于需要更细粒度描述的测试用例）：
```
SUB_ARKUI_{模块}_{API}_{METHOD}_{PARAM}_{SCENARIO}_{序号}
```

**类型标识**：

| 类型 | 说明 | 基础格式示例 | 详细格式示例 |
|------|------|------------|------------|
| PARAM | 参数测试 | `SUB_ARKUI_COMPONENT_BUTTON_FONTCOLOR_RED_PARAM_001` | `SUB_ARKUI_COMPONENT_TEXTAREA_FONTWEIGHT_700_PARAM_001` |
| ERROR | 错误码测试 | `SUB_ARKUI_COMPONENT_TEXT_FONTSIZE_NULL_ERROR_001` | - |
| RETURN | 返回值测试 | `SUB_ARKUI_COMPONENT_BUTTON_GETSTYLE_RETURN_001` | - |
| BOUNDARY | 边界值测试 | `SUB_ARKUI_COMPONENT_TEXT_FONTSIZE_MAX_BOUNDARY_001` | - |
| EVENT | 事件测试（ArkUI 特有） | `SUB_ARKUI_COMPONENT_BUTTON_ONCLICK_EVENT_001` | - |

| 类型 | 说明 | 示例 |
|------|------|------|
| PARAM | 参数测试 | SUB_ARKUI_BUTTON_FONTCOLOR_PARAM_001 |
| ERROR | 错误码测试 | SUB_ARKUI_BUTTON_FONTCOLOR_ERROR_001 |
| RETURN | 返回值测试 | SUB_ARKUI_BUTTON_FONTCOLOR_RETURN_001 |
| BOUNDARY | 边界值测试 | SUB_ARKUI_TEXT_FONTSIZE_BOUNDARY_001 |
| EVENT | 事件测试（ArkUI 特有） | SUB_ARKUI_BUTTON_ONCLICK_EVENT_001 |

### @tc 注释块规范（遵循通用配置）

**重要**：@tc 注释块规范遵循通用配置，详见：[../../_common.md#六@tc-注释块规范](../../_common.md#六@tc-注释块规范)

| 字段 | 格式要求 | 示例 |
|------|---------|------|
| `@tc.name` | 小驼峰命名（camelCase） | `buttonConstructorEmpty001` |
| `@tc.number` | `{describe名}_{序号}` | `buttonConstructorEmpty_001` |
| `@tc.desc` | `{API名} {错误码/场景} test.`（以 `. ` 结尾） | `Test Button with ButtonType.Capsule type test.` |
| `@tc.type` | `FUNCTION` / `PERFORMANCE` 等 | `FUNCTION` |
| `@tc.size` | `SMALLTEST` / `MEDIUMTEST` / `LARGETEST` | `SMALLTEST` |
| `@tc.level` | `LEVEL0` ~ `LEVEL4` | `LEVEL0` |

### 颜色格式提醒（ArkUI 特有）

> 组件树返回颜色格式为 **#AARRGGBB**（8位十六进制）

| 设置值 | 组件树返回值 |
|--------|-------------|
| `#FF0000` | `#FFFF0000` |
| `#00FF00` | `#FF00FF00` |
| `#0000FF` | `#FF0000FF` |

详见：[_common.md 5.4 节](./_common.md#54-颜色格式断言arkui-特有)

---

## 通用规范

所有接口分类测试都遵循通用规范，详见：[_common.md](./_common.md)

### 关键规范引用

| 规范项 | 说明 | 文档位置 |
|--------|------|---------|
| @tc 注释块规范 | 小驼峰命名、字段一致性 | 通用配置第六章 |
| hypium 导入规范 | 完整导入格式 | 通用配置第七章 |
| ID 命名规范 | 格式：`{component}_{test_name}`，必须唯一且有语义 | ArkUI/_common.md 4.2 |
| 高度设置规范 | 推荐使用相对高度 `5%`，避免设备分辨率差异 | ArkUI/_common.md 4.3 |
| 颜色格式断言 | 组件树返回 `#AARRGGBB` 格式，断言时考虑大小写 | ArkUI/_common.md 5.4 |
| 等价类参数精简 | 同类型参数只需选择2个代表性值 | ArkUI/_common.md 5.5 |
| TypeScript 类型规范 | 禁止使用 `any` 类型，所有变量必须明确类型 | 通用配置 1.6 节 |
| null/undefined 参数测试 | 验证设置 null/undefined 时是否恢复默认值 | ArkUI/_common.md 5.6 |
| UiTest API 规范 | ArkUI 特有的事件测试接口 | ArkUI/_common.md 5.7 |
