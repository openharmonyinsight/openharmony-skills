# 01. UI 组件接口测试指南

> 一、UI 组件接口（Component APIs）- 用来搭界面、放控件
>
> **版本**: 4.0.0
> **更新日期**: 2026-02-14
> **基于**: ArkUI/_common.md v4.0.0

---

## 接口说明

UI 组件接口是 ArkUI 最核心的一类，用来**搭界面、放控件**。

---

## 测试重点

### 1. 构造方法测试

**测试目的**：验证组件构造参数是否正确生效。

#### 页面侧规范

```typescript
// 创建多个组件实例，覆盖不同参数
// 使用唯一且有语义的 id
// Test 1: Button() - Empty constructor
Button()
  .id('button_empty_constructor')
  .width('100vp')
  .height('5%')

// Test 2: Button(options) - with type: Capsule
Button({ type: ButtonType.Capsule })
  .id('button_type_capsule')
  .width('100vp')
  .height('5%')
```

#### 测试侧规范

> **构造方法检查点**：既要检查组件存在，也要检查组件传入的构造方法属性值生效
>
> **重要**：以下示例遵循通用配置的 @tc 注释块规范

```typescript
/**
 * @tc.name   buttonConstructorEmpty001
 * @tc.number SUB_ARKUI_COMPONENT_BUTTON_EMPTY_CONSTRUCTOR_001
 * @tc.desc   Test Button empty constructor, verify button component exists test.
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('buttonConstructorEmpty001', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async () => {
  console.info('[buttonConstructorEmpty001] START');
  let strJson: string = getInspectorByKey('button_empty_constructor');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  console.info("[buttonConstructorEmpty001] obj is: " + JSON.stringify(obj.$attrs));
  // Verify button component exists
  expect(obj.$type).assertEqual('Button');
  console.info('[buttonConstructorEmpty001] END');
})

/**
 * @tc.name   buttonTypeCapsule001
 * @tc.number SUB_ARKUI_COMPONENT_BUTTON_TYPE_CAPSULE_PARAM_001
 * @tc.desc   Test Button with ButtonType.Capsule type test.
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('buttonTypeCapsule001', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async () => {
  console.info('[buttonTypeCapsule001] START');
  let strJson: string = getInspectorByKey('button_type_capsule');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  console.info("[buttonTypeCapsule001] obj is: " + JSON.stringify(obj.$attrs));
  expect(obj.$attrs.type).assertEqual('ButtonType.Capsule');
  console.info('[buttonTypeCapsule001] END');
})
```

### 2. 属性值测试

**测试目的**：验证属性值设置生效。

#### 页面侧

```typescript
// 测试 fontWeight是否设置成功
// Test number type: 700
TextArea({ placeholder: 'TextArea fontWeight 700' })
  .height('5%')
  .id('textArea_fontWeight_number_700')
  .fontWeight(700)
```

#### 测试侧

> **重要**：以下示例遵循通用配置的 @tc 注释块规范

```typescript
/**
 * @tc.name   textAreaFontWeight0400
 * @tc.number SUB_ARKUI_COMPONENT_TEXTAREA_FONTWEIGHT_700_PARAM_001
 * @tc.desc   Test TextArea fontWeight with number type value 700 test.
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('textAreaFontWeight0400', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async () => {
  console.info('[textAreaFontWeight0400] START');
  //从组件树中获取目标组件
  let strJson = getInspectorByKey('textArea_fontWeight_number_700');
  console.info("[textAreaFontWeight0400] obj is: " + JSON.stringify(JSON.parse(strJson).$attrs));
  //判断组件的属性值是否符合预期
  expect(JSON.parse(strJson).$attrs.fontWeight).assertEqual('700');
  console.info('[textAreaFontWeight0400] END');
})
```

### 3. 属性默认值测试

**测试目的**：验证属性设置为null/undefined时的默认行为。

**测试方法**：
- 构造一个"未设置该属性"的组件实例，作为默认值基准；
- 构造一个将该属性设置为 null / undefined 的组件实例；
- 首先断言各组件能正确获取到目标属性值（不为 undefined），防止因属性读取失败导致多个组件结果同时为 undefined 而误判通过；
- 再通过断言两者最终属性值（或渲染结果）相等，
-   来判断设置 null / undefined 时是否等价于未设置，
-   即是否正确触发默认值逻辑

#### 页面侧

```typescript
// 测试未设置 fontSize（默认行为）
Text('Text property without fontSize')
  .id('text_fontsize_default')

// 测试 null 参数
Text('Text property with null')
  .id('text_fontsize_null')
  .fontSize(null)

// 测试 undefined 参数
Text('Text property with undefined')
  .id('text_fontsize_undefined')
  .fontSize(undefined)
```

#### 测试侧

> **重要**：以下示例遵循通用配置的 @tc 注释块规范

```typescript
/**
 * @tc.name   textFontSize0100
 * @tc.number SUB_ARKUI_COMPONENT_TEXT_FONTSIZE_NULL_PARAM_001
 * @tc.desc   测试 Text fontSize 属性 - null 参数应恢复默认值 16fp test.
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('textFontSize0100', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async () => {
  let strJsonCompare: string = getInspectorByKey('text_fontsize_default');
  let objCompare: Record<string, ESObject> = JSON.parse(strJsonCompare);
  let strJson: string = getInspectorByKey('text_fontsize_null');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  //确保属性读取成功
  expect(obj.$attrs.fontSize).not().assertUndefined();
  // 断言断言两者最终属性值（或渲染结果）相等
  expect(obj.$attrs.fontSize).assertEqual(objCompare.$attrs.fontSize);
});
```

---

## 测试注意事项

UI 组件接口测试遵循通用测试规范，详见：[_common.md](./_common.md)

### 关键规范引用

| 规范项 | 说明 | 文档位置 |
|--------|------|---------|
| @tc 注释块规范 | 小驼峰命名、字段一致性 | 通用配置第六章 |
| ID 命名规范 | 格式：`{component}_{test_name}`，必须唯一且有语义 | ArkUI/_common.md 4.2 |
| 高度设置规范 | 推荐使用相对高度 `5%`，避免设备分辨率差异 | ArkUI/_common.md 4.3 |
| 颜色格式断言 | 组件树返回 `#AARRGGBB` 格式，断言时考虑大小写 | ArkUI/_common.md 5.4 |
| 等价类参数精简 | 同类型参数只需选择2个代表性值 | ArkUI/_common.md 5.5 |

---

## 参考文档

- ArkUI 子系统通用配置：[_common.md](./_common.md)
- ArkUI 接口分类概览：[arkui.md](./arkui.md)
- 通用配置：[../../_common.md](../../_common.md)
