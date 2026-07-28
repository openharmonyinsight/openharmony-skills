# Demo 控件 ID 与 UiTest 契约规范

> **模块信息**
> - 层级：conventions（跨层共享）
> - 优先级：按需加载
> - 适用范围：Phase 5（Demo 生成 + UiTest 测试代码生成）
> - 依赖：`uitest_framework.md`

---

## 一、契约概述

Demo 应用和 UiTest 测试代码通过**控件 ID** 建立契约。控件 ID 在 Phase 4 设计文档中预定义，Demo 生成和 UiTest 测试代码生成均从同一份设计文档读取。

```
Phase 4 设计文档（控件 ID 清单附录）
         │
         ├──→ Demo 生成：控件带 .id('xxx') 修饰符
         │
         └──→ UiTest 生成：通过 ON.id('xxx') 定位控件
```

---

## 二、控件 ID 命名规范

### 2.1 格式

```
{type}_{page_seq}_{semantic_name}
```

| 组成部分 | 规则 | 示例 |
|---------|------|------|
| `type` | 控件类型缩写 | `btn`、`input`、`select`、`toggle`、`result`、`status`、`log` |
| `page_seq` | 3 位零填充页面序号 | `001`、`002` |
| `semantic_name` | 语义化名称（小写下划线） | `execute`、`reset`、`width_value` |

### 2.2 控件类型映射

| type | ArkUI 组件 | UiTest 操作 |
|------|-----------|------------|
| `btn` | Button | `click()` |
| `input` | TextInput | `setText()`、`getProperty('text')` |
| `textarea` | TextArea | `setText()`、`getProperty('text')` |
| `select` | Select | `click()` → 选择选项 |
| `toggle` | Toggle | `click()` |
| `result` | Text（结果展示） | `getProperty('text')` |
| `status` | Text（状态指示） | `getProperty('text')` |
| `log` | List（日志区域） | `getProperty('text')` |
| `list` | List/Grid/WaterFlow | `scrollSearch(ON.id())` 定位子项 |
| `item` | ListItem/GridItem | `getText()`、`click()` |
| `tab` | Tabs TabBar 子项 | `click()` 切换 TabContent |
| `dialog_btn` | Dialog 内 Button | `click()` 确认/取消 |
| `dialog_text` | Dialog 内 Text | `getText()` 获取弹窗信息 |

---

## 三、三方一致性约束

### 3.1 一致性要求

| 数据源 | 必须一致的项 |
|--------|------------|
| Phase 4 设计文档（控件 ID 清单） | 控件 ID、类型、所在页面 |
| Demo `Constants.ets` | 控件 ID 常量定义 |
| UiTest 测试代码 `ON.id()` | 控件 ID 引用 |

### 3.2 Phase 7 验证规则

| 检查项 | 验证方式 |
|--------|---------|
| 设计文档 → Demo | 设计文档中的每个控件 ID 在 `Constants.ets` 中有对应常量 |
| 设计文档 → UiTest | 每条 `ON.id('xxx')` 引用的 ID 在设计文档控件 ID 清单中存在 |
| 页面路由一致性 | 设计文档页面路由 ↔ Demo `main_pages.json` ↔ UiTest `Utils.pushPage()` |

---

## 四、Demo 控件规范

### 4.1 强制 id() 修饰符

Demo 中所有可交互控件必须添加 `.id()` 修饰符：

```typescript
// ✅ 正确
Button('执行')
  .id('btn_001_execute')
  .onClick(() => this.executeApi())

TextInput({ placeholder: '请输入参数' })
  .id('input_001_value')

Text(this.resultText)
  .id('result_001_01')
```

```typescript
// ❌ 错误：缺少 id()
Button('执行')
  .onClick(() => this.executeApi())
```

### 4.2 Demo 结果展示规范

Demo 必须提供以下可读取的 UI 区域供 UiTest 验证：

| 区域 | 控件 ID 模式 | 内容 |
|------|-------------|------|
| 结果展示 | `result_{page_seq}_{seq}` | API 调用返回值或执行结果文本 |
| 状态指示 | `status_{page_seq}_{seq}` | `PASS` / `FAIL` / `WAITING` |

UiTest 通过 `getProperty('text')` 读取这些区域的文本内容进行断言。

---

## 五、UiTest 测试代码规范

### 5.1 控件查找

```typescript
// ✅ 推荐：使用 waitForComponent 轮询等待
const component = await driver.waitForComponent(ON.id('btn_001_execute'), 2000);

// ❌ 禁止：使用 findComponent（控件可能尚未渲染完成）
const component = await driver.findComponent(ON.id('btn_001_execute'));
```

### 5.2 判空必选

```typescript
// ✅ 正确：判空后操作
const btn = await driver.waitForComponent(ON.id('btn_001_execute'), 2000);
if (btn) {
  await btn.click();
} else {
  expect().assertFail();
  done();
  return;
}
```

### 5.3 操作间隔

操作间隔使用 `waitForComponent` 轮询等待，控件出现即返回，禁止使用 sleep 硬等待：

```typescript
await btn.click();
const result = await driver.waitForComponent(ON.id('result_001_01'), 2000);
```
