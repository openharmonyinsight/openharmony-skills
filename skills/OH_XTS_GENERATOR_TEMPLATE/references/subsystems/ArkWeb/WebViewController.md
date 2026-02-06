# WebViewController 模块配置

> **模块信息**
> - 所属子系统: ArkWeb
> - 模块名称: WebViewController
> - API 声明文件: @ohos.web.webview.d.ts
> - 主要 API: WebViewController 控制方法
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、模块特有配置

### 1.1 模块概述

WebViewController 模块提供 Web 视图控制器，用于控制 Web 组件的行为，包括页面导航、JavaScript 交互、缩放等功能。

### 1.2 API 声明文件

```
API声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.web.webview.d.ts
```

### 1.3 通用配置继承

本模块继承 ArkWeb 子系统通用配置：

- **测试路径规范**: 见 `ArkWeb/_common.md` 第 1.2 节
- **Web 组件测试规则**: 见 `ArkWeb/_common.md` 第 2.1 节
- **JavaScript 交互测试规则**: 见 `ArkWeb/_common.md` 第 2.2 节

## 二、模块特有 API 列表

### 2.1 页面导航API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| loadUrl | 加载URL | LEVEL0 | 本地、远程、失败 |
| reload | 重新加载 | LEVEL1 | 刷新、缓存 |
| goBack | 后退 | LEVEL1 | 历史记录 |
| goForward | 前进 | LEVEL1 | 历史记录 |
| accessBackward | 后退能力 | LEVEL2 | 查询、验证 |
| accessForward | 前进能力 | LEVEL2 | 查询、验证 |
| getOriginalUrl | 获取原始URL | LEVEL2 | 重定向前 |

### 2.2 JavaScript 交互API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| runJavaScript | 执行JS | LEVEL0 | 同步、异步、返回值 |
| javaScriptProxy | JS对象代理 | LEVEL1 | 注入、调用、参数 |
| deleteJavaScriptRegister | 删除JS注册 | LEVEL2 | 删除、验证 |

### 2.3 页面状态API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| getTitle | 获取页面标题 | LEVEL1 | 标题内容 |
| getPageHeight | 获取页面高度 | LEVEL2 | 滚动高度 |
| getScrollX | 获取水平滚动位置 | LEVEL2 | 位置值 |
| getScrollY | 获取垂直滚动位置 | LEVEL2 | 位置值 |

### 2.4 缩放控制API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| zoomIn | 放大 | LEVEL2 | 缩放级别 |
| zoomOut | 缩小 | LEVEL2 | 缩放级别 |
| getZoomFactor | 获取缩放因子 | LEVEL2 | 缩放比例 |

## 三、模块特有测试规则

### 3.1 页面导航测试规则

1. **loadUrl 测试**：
   - 测试加载本地页面
   - 测试加载远程 URL
   - 测试加载无效 URL
   - 测试加载特殊协议（data://）

2. **页面跳转历史**：
   - 测试 goBack 后退
   - 测试 goForward 前进
   - 测试历史记录边界
   - 测试 accessBackward/Forward 查询

3. **页面刷新**：
   - 测试 reload 刷新
   - 测试缓存刷新
   - 测试刷新后状态

### 3.2 JavaScript 交互测试规则

1. **runJavaScript 测试**：
   - 测试执行简单表达式
   - 测试执行函数调用
   - 测试异步 JavaScript
   - 测试返回值类型
   - 测试 JavaScript 错误处理

2. **JavaScript 对象注入**：
   - 测试注入 ArkTS 对象
   - 测试 JavaScript 调用 ArkTS 方法
   - 测试参数传递
   - 测试返回值传递
   - 测试对象生命周期

3. **JavaScript 注册管理**：
   - 测试 deleteJavaScriptRegister
   - 测试删除后验证
   - 测试重复注册

### 3.3 页面状态测试规则

1. **页面信息获取**：
   - 测试 getTitle 获取标题
   - 测试 getOriginalUrl 获取原始 URL
   - 测试重定向后的 URL

2. **滚动位置获取**：
   - 测试 getScrollX 获取水平位置
   - 测试 getScrollY 获取垂直位置
   - 测试滚动后的位置变化

3. **页面尺寸获取**：
   - 测试 getPageHeight 获取页面高度
   - 测试页面内容高度
   - 测试视口高度

### 3.4 缩放控制测试规则

1. **缩放操作**：
   - 测试 zoomIn 放大
   - 测试 zoomOut 缩小
   - 测试缩放级别限制

2. **缩放状态**：
   - 测试 getZoomFactor 获取缩放因子
   - 测试缩放后页面显示
   - 测试缩放后交互

## 四、模块特有代码模板

### 4.1 runJavaScript 测试模板

```typescript
/**
 * @tc.name ArkWeb Run JavaScript Test
 * @tc.number SUB_ARKWEB_WEBVIEWCONTROLLER_RUNJS_001
 * @tc.desc 测试 WebViewController 执行 JavaScript 功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testRunJs001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  // 1. 创建 WebViewController
  let controller = new webview.WebViewController();

  // 2. 加载测试页面
  controller.loadUrl('resource://rawfile/test.html');

  // 3. 等待页面加载完成
  // (需要实现等待机制)

  // 4. 执行 JavaScript 代码
  let result = await controller.runJavaScript('1 + 1');

  // 5. 验证执行结果
  expect(result).assertEqual('2');
});
```

### 4.2 JavaScript 对象注入测试模板

```typescript
/**
 * @tc.name ArkWeb JavaScript Proxy Test
 * @tc.number SUB_ARKWEB_WEBVIEWCONTROLLER_JSPROXY_001
 * @tc.desc 测试 WebViewController JavaScript 对象注入功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testJsProxy001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  // 1. 创建 WebViewController
  let controller = new webview.WebViewController();

  // 2. 创建注入对象
  let controllerObj = {
    onJsCallback: (message: string) => {
      console.log('JS callback: ' + message);
    }
  };

  // 3. 注册 JavaScript 对象
  controller.javaScriptProxy({
    object: controllerObj,
    name: "jsObject",
    methodList: ["onJsCallback"],
    controller: controller
  });

  // 4. 加载测试页面
  controller.loadUrl('resource://rawfile/test.html');

  // 5. 等待页面加载完成
  // (需要实现等待机制)

  // 6. 从 JavaScript 调用 ArkTS 方法
  await controller.runJavaScript('jsObject.onJsCallback("test")');

  // 7. 验证回调被触发
  // (需要验证 controllerObj 的状态)
});
```

### 4.3 页面导航测试模板

```typescript
/**
 * @tc.name ArkWeb Navigation Test
 * @tc.number SUB_ARKWEB_WEBVIEWCONTROLLER_NAVIGATION_001
 * @tc.desc 测试 WebViewController 页面导航功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testNavigation001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建 WebViewController
  let controller = new webview.WebViewController();

  // 2. 加载第一个页面
  controller.loadUrl('resource://rawfile/page1.html');

  // 3. 等待加载完成
  // (需要实现等待机制)

  // 4. 加载第二个页面
  controller.loadUrl('resource://rawfile/page2.html');

  // 5. 等待加载完成
  // (需要实现等待机制)

  // 6. 测试后退
  expect(controller.accessBackward()).assertTrue();
  controller.goBack();

  // 7. 验证返回到第一个页面
  let currentUrl = controller.getOriginalUrl();
  expect(currentUrl).assertContain('page1.html');

  // 8. 测试前进
  expect(controller.accessForward()).assertTrue();
  controller.goForward();

  // 9. 验证前进到第二个页面
  currentUrl = controller.getOriginalUrl();
  expect(currentUrl).assertContain('page2.html');
});
```

## 五、测试注意事项

1. **JavaScript 执行环境**：
   - JavaScript 需要页面加载完成后才能执行
   - 注意异步 JavaScript 的执行时机
   - 注意 JavaScript 错误的捕获

2. **对象注入安全**：
   - 注入对象的方法需要正确声明
   - 注意参数类型转换
   - 注意线程安全

3. **页面加载依赖**：
   - 导航操作需要页面加载完成
   - 需要实现等待机制
   - 需要处理加载失败场景

4. **历史记录管理**：
   - 测试前准备页面栈
   - 测试后清理页面栈
   - 注意边界条件（栈底、栈顶）

## 六、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 WebViewController 模块配置
