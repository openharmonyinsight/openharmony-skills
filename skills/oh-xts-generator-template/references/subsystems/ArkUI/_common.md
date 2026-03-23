# ArkUI 子系统配置

> **版本**: 2.0.0
> **更新日期**: 2026-02-05
> **基于核心配置**: _common.md v2.0.0

---

## 一、基础信息

```json
{
  "name": "ArkUI",
  "kitPackage": "@kit.ArkUI",
  "testPath": "test/xts/acts/arkui/",
  "apiDeclarationPath": "interface/sdk-js/api/@ohos.arkui.d.ts",
  "documentationPath": "docs/zh-cn/application-dev/reference/apis-arkui/",
  "apiType": "dynamic&static"
}
```

---

## 二、差异化配置

### 2.1 路径差异化

```json
{
  "paths": {
    "testPath": "test/xts/acts/arkui/",
    "pagePath": "src/main/ets/pages/{component}/",
    "testFilePath": "src/ohosTest/ets/test/{component}/",
    "pageRegistration": "src/main/resources/base/profile/main_pages.json",
    "testRegistration": "src/ohosTest/ets/test/List.test.ets"
  }
}
```

### 2.2 命名差异化

```json
{
  "naming": {
    "testFilePattern": "{Component}{Property}.test.ets",
    "testSuitePattern": "{Component}Test",
    "pageFilePattern": "{Component}{Property}.ets",
    "pageDirPattern": "pages/{component}/",
    "testDirPattern": "test/{component}/"
  }
}
```

### 2.3 导入差异化

```json
{
  "imports": {
    "kitPackage": "@kit.ArkUI",
    "additionalImports": [
      "Component, Column, Row, Text, Button"
    ],
    "conditionalImports": [
      "beforeAll, afterAll"  // 页面测试需要
    ]
  }
}
```

### 2.4 特殊规则

```json
{
  "specialRules": {
    "testTypeExtensions": ["EVENT"],
    "namingExtensions": [
      {
        "type": "测试用例编号",
        "rule": "扩展核心格式为 SUB_ARKUI_{模块}_{组件}_{属性}_{类型}_{序号}",
        "example": "SUB_ARKUI_BUTTON_FONTCOLOR_PARAM_001"
      }
    ],
    "apiSpecific": [
      {
        "api": "UiTest",
        "rule": "必须使用大写 T：@kit.ArkUI 中的 Driver, ON",
        "description": "UiTest 特殊导入规则"
      },
      {
        "api": "Component.onClick",
        "rule": "事件测试必须使用 EVENT 类型标识",
        "description": "ArkUI 事件测试特殊规则"
      }
    ]
  }
}
```

---

## 三、API映射表

### 3.1 Kit组件映射

| API名称 | Kit导入 | 组件路径 | 说明 |
|---------|---------|----------|------|
| Component | @kit.ArkUI | - | 基础组件接口 |
| Column | @kit.ArkUI | - | 布局容器 |
| Row | @kit.ArkUI | - | 布局容器 |
| Text | @kit.ArkUI | - | 文本组件 |
| Button | @kit.ArkUI | - | 按钮组件 |
| Driver | @kit.ArkUI | - | UiTest 驱动（注意大写 T） |
| ON | @kit.ArkUI | - | UiTest 选择器（注意大写 T） |

### 3.2 测试套映射

| 功能模块 | 测试套名称 | 测试文件路径 | 说明 |
|---------|-----------|-------------|------|
| 组件测试 | ComponentTest | test/{component}/ | 基础组件功能测试 |
| 事件测试 | EventTest | test/{component}/ | 组件事件交互测试 |
| 布局测试 | LayoutTest | test/layout/ | 布局容器测试 |
| 动画测试 | AnimationTest | test/animation/ | 动画效果测试 |

---

## 四、使用示例

```typescript
// 加载 ArkUI 配置
const arkuiConfig = loadSubsystemConfig('ArkUI');

// 生成组件测试
const componentTest = generateTest('Button.fontColor', {
  config: arkuiConfig,
  testTypes: ['PARAM', 'ERROR'],
  level: 'Level1'
});

// 生成事件测试
const eventTest = generateTest('Button.onClick', {
  config: arkuiConfig,
  testTypes: ['EVENT'],  // 使用扩展类型
  level: 'Level2'
});
```

---

## 五、测试文件示例

### 5.1 组件属性测试文件

```typescript
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 */

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
import {Button} from '@kit.ArkUI';

export default function ButtonFontColorTest() {
  describe('ButtonFontColorTest', () => {
    /**
     * @tc.name testButtonFontColorParam001
     * @tc.number SUB_ARKUI_BUTTON_FONTCOLOR_PARAM_001
     * @tc.desc 测试 Button 组件的 fontColor 属性 - 正常值场景
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL1
     */
    it('testButtonFontColorParam001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done: Function) => {
      // 测试实现
      done();
    });
  });
}
```

### 5.2 事件测试文件

```typescript
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 */

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
import {Driver, ON} from '@kit.ArkUI';

export default function ButtonClickTest() {
  let driver: Driver;

  beforeAll(async (done: Function) => {
    driver = await Driver.create();
    done();
  });

  afterAll(async (done: Function) => {
    await driver.close();
    done();
  });

  describe('ButtonClickTest', () => {
    /**
     * @tc.name testButtonClickEvent001
     * @tc.number SUB_ARKUI_BUTTON_ONCLICK_EVENT_001
     * @tc.desc 测试 Button 组件的 onClick 事件 - 点击事件
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('testButtonClickEvent001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, async (done: Function) => {
      const button = await driver.waitForComponent(ON.id('test-button'), 2000);
      if (button) {
        await button.click();
        expect(true).assertTrue();
      } else {
        expect().assertFail();
      }
      done();
    });
  });
}
```

---

**版本**: 2.0.0
**创建日期**: 2026-02-05
**更新日期**: 2026-02-05