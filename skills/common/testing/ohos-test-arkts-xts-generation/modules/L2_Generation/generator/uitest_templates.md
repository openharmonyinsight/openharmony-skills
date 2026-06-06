# UiTest 测试代码模板（基于 Demo 控件 ID）

> **模块信息**
> - 层级：L2_Generation
> - 优先级：按需加载
> - 适用范围：Phase 5 Step 2b（UI 类用例的 UiTest 测试代码生成）
> - 依赖：`references/conventions/uitest_framework.md`、Phase 4 设计文档控件 ID 清单
> - 固定模板：`references/templates/Utils_dyn.ets`（动态模式）、`references/templates/Utils_sta.ets`（静态模式）

---

## 一、UiTest 测试文件模板

### 1.1 文件结构

```typescript
// ... Apache 2.0 license header ...

import { describe, beforeAll, afterAll, it, expect, TestType, Size, Level } from '@ohos/hypium';
import { Driver, ON } from '@ohos.UiTest';
import Utils from '../common/Utils';

export default function XXXUiTest() {
  let driver: Driver;

  beforeAll(async (done: Function) => {
    await Utils.pushPage('pages/{PageName}', done);
    driver = await Driver.create();
    done();
  });

  afterAll(() => {
    // Driver 使用完成后自动销毁
  });

  describe('{TestGroupName}', () => {
    // UI 测试用例
  });
}
```

### 1.2 关键约束

- `Utils.pushPage()` 的路由路径从设计文档的页面规划中读取
- `Utils.ets` 为固定模板文件，Phase 5B 根据目标模式（动态/静态）从 `references/templates/` 复制引用
- 每个页面一个 describe 块
- 所有控件 ID 从设计文档的控件 ID 清单附录中读取
- 使用 `waitForComponent` 而非 `findComponent`（推荐轮询等待）
- `Utils.pushPage` 内部自带 `sleep(2000)` 等待页面转场，beforeAll 中无需额外 sleep

---

## 二、测试场景模板

### 2.1 输入 → 执行 → 结果验证（标准模式）

```typescript
/**
 * @tc.number {用例编号}
 * @tc.name {用例名}
 * @tc.desc {用例描述}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level Level{n}
 */
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 输入参数
  const input = await driver.waitForComponent(ON.id('{input_control_id}'), 2000);
  if (input) {
    await input.setText('{param_value}');
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 点击执行
  const btn = await driver.waitForComponent(ON.id('{execute_btn_id}'), 2000);
  if (btn) {
    await btn.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 3. 验证结果
  const result = await driver.waitForComponent(ON.id('{result_control_id}'), 2000);
  if (result) {
    const text = await result.getProperty('text');
    expect(text).assertEqual('{expected_result}');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 2.2 选择 → 执行 → 结果验证（Select 模式）

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 选择选项（通过点击 Select 控件选择）
  const select = await driver.waitForComponent(ON.id('{select_control_id}'), 2000);
  if (select) {
    await select.click();
    const option = await driver.waitForComponent(ON.text('{option_text}'), 2000);
    if (option) {
      await option.click();
    }
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 点击执行
  const btn = await driver.waitForComponent(ON.id('{execute_btn_id}'), 2000);
  if (btn) {
    await btn.click();
  }

  // 3. 验证状态
  const status = await driver.waitForComponent(ON.id('{status_control_id}'), 2000);
  if (status) {
    const text = await status.getProperty('text');
    expect(text).assertEqual('PASS');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 2.3 开关切换 → 结果验证（Toggle 模式）

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 切换开关
  const toggle = await driver.waitForComponent(ON.id('{toggle_control_id}'), 2000);
  if (toggle) {
    await toggle.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 验证结果
  const result = await driver.waitForComponent(ON.id('{result_control_id}'), 2000);
  if (result) {
    const text = await result.getProperty('text');
    expect(text).assertEqual('{expected_result}');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 2.4 组件属性验证（只读模式）

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 导航到目标页面（已在 beforeAll 中完成）
  // 2. 直接读取组件属性
  const component = await driver.waitForComponent(ON.id('{component_id}'), 2000);
  if (component) {
    const propValue = await component.getProperty('{property_name}');
    expect(propValue).assertEqual('{expected_value}');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 2.5 错误场景验证

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 输入无效参数
  const input = await driver.waitForComponent(ON.id('{input_control_id}'), 2000);
  if (input) {
    await input.setText('{invalid_value}');
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 点击执行
  const btn = await driver.waitForComponent(ON.id('{execute_btn_id}'), 2000);
  if (btn) {
    await btn.click();
  }

  // 3. 验证错误状态
  const status = await driver.waitForComponent(ON.id('{status_control_id}'), 2000);
  if (status) {
    const text = await status.getProperty('text');
    expect(text).assertEqual('FAIL');
  } else {
    expect().assertFail();
  }

  // 4. 验证错误信息
  const result = await driver.waitForComponent(ON.id('{result_control_id}'), 2000);
  if (result) {
    const text = await result.getProperty('text');
    expect(text).assertContain('{expected_error_code}');
  }

  done();
});
```

### 2.6 List 滚动定位

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 定位 List 容器（已在当前页面渲染，使用 findComponent）
  const list = await driver.findComponent(ON.id('{list_container_id}'));
  if (!list) {
    expect().assertFail();
    done();
    return;
  }

  // 2. 在可滚动容器内搜索目标 ListItem
  const item = await list.scrollSearch(ON.id('{item_target_id}'));
  if (item) {
    const text = await item.getText();
    expect(text).assertEqual('{expected_result}');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 2.7 弹窗 Dialog

#### 分支 A：操作弹窗控件

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 点击触发弹窗
  const trigger = await driver.waitForComponent(ON.id('{trigger_btn_id}'), 2000);
  if (trigger) {
    await trigger.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 等待弹窗出现并操作弹窗内控件
  const dialogBtn = await driver.waitForComponent(ON.id('{dialog_btn_id}'), 2000);
  if (dialogBtn) {
    await dialogBtn.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 3. 验证弹窗关闭后的主页面状态
  const result = await driver.waitForComponent(ON.id('{result_control_id}'), 2000);
  if (result) {
    const text = await result.getProperty('text');
    expect(text).assertEqual('{expected_result}');
  } else {
    expect().assertFail();
  }

  done();
});
```

#### 分支 B：监听弹窗事件断言

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 注册事件监听，获取弹窗 UIElementInfo 做断言
  let eventReceived = false;
  let eventData: ESObject | null = null;
  events_emitter.once({
    eventId: {event_id}
  }, (eventDataInner: events_emitter.EventData) => {
    eventReceived = true;
    eventData = eventDataInner.data;
  });

  // 2. 点击触发弹窗
  const trigger = await driver.waitForComponent(ON.id('{trigger_btn_id}'), 2000);
  if (trigger) {
    await trigger.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 3. 验证事件数据
  await driver.waitForIdle(500, 3000);
  expect(eventReceived).assertTrue();
  if (eventData) {
    expect(eventData['{expected_key}']).assertEqual('{expected_value}');
  }

  done();
});
```

### 2.8 页面导航（Router 跳转）

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 点击导航按钮
  const navBtn = await driver.waitForComponent(ON.id('{navigate_btn_id}'), 2000);
  if (navBtn) {
    await navBtn.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 等待目标页面渲染并验证
  const target = await driver.waitForComponent(ON.id('{target_page_control_id}'), 3000);
  if (target) {
    const text = await target.getProperty('text');
    expect(text).assertEqual('{expected_result}');
  } else {
    expect().assertFail();
  }

  // 3. 可选：返回上一页（根据设计文档决定）
  // await driver.pressBack();

  done();
});
```

### 2.9 Tabs 切换

```typescript
it('{testName}', Level.LEVEL{n}, async (done: Function) => {
  // 1. 点击目标 Tab
  const tab = await driver.waitForComponent(ON.id('{tab_id}'), 2000);
  if (tab) {
    await tab.click();
  } else {
    expect().assertFail();
    done();
    return;
  }

  // 2. 等待新 TabContent 渲染并验证
  const content = await driver.waitForComponent(ON.id('{tab_content_control_id}'), 2000);
  if (content) {
    const text = await content.getProperty('text');
    expect(text).assertEqual('{expected_result}');
  } else {
    expect().assertFail();
  }

  done();
});
```

---

## 三、控件 ID 引用规则

| 规则 | 说明 |
|------|------|
| ID 来源 | 必须从设计文档的控件 ID 清单附录中读取，禁止自行编造 |
| ID 格式 | `{type}_{page_seq}_{semantic_name}`，如 `btn_001_execute` |
| 判空必选 | 每次 `waitForComponent` / `findComponent` 返回后必须判空，null 时 `expect().assertFail()` + `done(); return` |
| 超时统一 | `waitForComponent` 超时统一使用 2000ms，页面导航场景使用 3000ms |
| 操作间隔 | 操作间隔使用 `waitForComponent` 轮询等待，控件出现即返回；禁止使用 sleep 硬等待 |
| 滚动定位 | List/Grid 等可滚动组件使用 `component.scrollSearch(ON.id())` 定位目标子项 |
| 容器查找 | 已在当前页面渲染的容器控件使用 `findComponent`，非轮询场景的目标使用 `waitForComponent` |

---

## 四、变量替换说明

| 模板变量 | 来源 | 示例 |
|---------|------|------|
| `{PageName}` | 设计文档页面规划的路由路径 | `Page001` |
| `{TestGroupName}` | 按页面或 API 分组 | `XXXComponentUiTest` |
| `{用例编号}` | 设计文档的用例编号 | `SUB_ARKUI_COMPONENT_WIDTH_EVENT_001` |
| `{testName}` | 用例编号的函数名形式 | `testComponentWidthEvent001` |
| `{input_control_id}` | 设计文档控件 ID 清单 | `input_001_width_value` |
| `{execute_btn_id}` | 设计文档控件 ID 清单 | `btn_001_execute` |
| `{result_control_id}` | 设计文档控件 ID 清单 | `result_001_01` |
| `{status_control_id}` | 设计文档控件 ID 清单 | `status_001_01` |
| `{param_value}` | 设计文档测试步骤中的参数值 | `200` |
| `{expected_result}` | 设计文档预期 UI 结果 | `200.00vp` |
| `{list_container_id}` | 设计文档控件 ID 清单（list 类型） | `list_001_scroll` |
| `{item_target_id}` | 设计文档控件 ID 清单（item 类型） | `item_001_target` |
| `{tab_id}` | 设计文档控件 ID 清单（tab 类型） | `tab_001_second` |
| `{tab_content_control_id}` | 设计文档控件 ID 清单（result 类型） | `result_002_01` |
| `{navigate_btn_id}` | 设计文档控件 ID 清单（btn 导航类） | `btn_001_navigate` |
| `{target_page_control_id}` | 设计文档控件 ID 清单 | `result_002_01` |
| `{trigger_btn_id}` | 设计文档控件 ID 清单（触发弹窗按钮） | `btn_001_show_dialog` |
| `{dialog_btn_id}` | 设计文档控件 ID 清单（dialog_btn 类型） | `dialog_btn_001_confirm` |
| `{event_id}` | 设计文档事件 ID | `10001` |
| `{expected_key}` | 设计文档事件数据 key | `VALUE` |
| `{expected_value}` | 设计文档事件数据 value | `true` |
