# Web 模块配置

> **模块信息**
> - 所属子系统: ArkWeb
> - 模块名称: Web
> - API 声明文件: @ohos.web.webview.d.ts
> - 主要 API: Web 组件及其属性、事件
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、模块特有配置

### 1.1 模块概述

Web 模块提供 Web 视图组件，用于在应用中加载和显示网页内容。

### 1.2 API 声明文件

```
API声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.web.webview.d.ts
```

### 1.3 通用配置继承

本模块继承 ArkWeb 子系统通用配置：

- **测试路径规范**: 见 `ArkWeb/_common.md` 第 1.2 节
- **Web 组件测试规则**: 见 `ArkWeb/_common.md` 第 2.1 节
- **辅助工程配置**: 见 `ArkWeb/_common.md` 第 2.3 节

## 二、模块特有 API 列表

### 2.1 Web 组件属性API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| src | 页面源地址 | LEVEL0 | 本地、远程、data:// |
| domStorageAccessEnabled | DOM存储访问 | LEVEL1 | 启用、禁用 |
| javaScriptAccessEnabled | JS执行权限 | LEVEL1 | 启用、禁用 |
| fileAccessEnabled | 文件访问权限 | LEVEL1 | 启用、禁用 |
| mixedMode | 混合内容模式 | LEVEL2 | None、Always、Compatible |
| cacheMode | 缓存模式 | LEVEL2 | Default、NoCache |
| zoomAccessEnabled | 缩放权限 | LEVEL2 | 启用、禁用 |

### 2.2 Web 组件事件API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| onPageBegin | 页面开始加载 | LEVEL0 | 触发时机、URL |
| onPageEnd | 页面加载完成 | LEVEL0 | 触发时机、URL |
| onProgressChange | 加载进度变化 | LEVEL1 | 进度值、频率 |
| onReceivedError | 加载错误 | LEVEL2 | 错误信息、类型 |
| onConsole | 控制台消息 | LEVEL2 | 消息内容、级别 |
| onAlert | Alert 对话框 | LEVEL2 | 消息内容、确认 |
| onConfirm | Confirm 对话框 | LEVEL2 | 消息内容、确认/取消 |
| onPrompt | Prompt 对话框 | LEVEL2 | 消息内容、输入值 |

### 2.3 Web 资源处理API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| onInterceptRequest | 拦截请求 | LEVEL1 | 拦截、修改、替换 |
| onHttpErrorReceive | HTTP错误 | LEVEL2 | 错误码、响应 |
| onResourceLoad | 资源加载 | LEVEL2 | 加载状态、类型 |

## 三、模块特有测试规则

### 3.1 页面加载测试规则

1. **本地页面加载**：
   - 测试加载 rawfile 中的 HTML
   - 测试相对路径和绝对路径
   - 测试页面间跳转

2. **远程URL加载**：
   - 测试 HTTP/HTTPS URL
   - 测试重定向处理
   - 测试加载失败场景

3. **Data URL 加载**：
   - 测试 data:// 协议
   - 测试 HTML 内容直接加载

### 3.2 权限控制测试规则

1. **JavaScript 执行权限**：
   - 测试启用/禁用 JavaScript
   - 验证禁用后 JS 不执行
   - 测试动态修改权限

2. **DOM 存储权限**：
   - 测试 localStorage 访问
   - 测试 sessionStorage 访问
   - 验证权限控制

3. **文件访问权限**：
   - 测试本地文件访问
   - 测试跨域访问
   - 验证安全限制

### 3.3 事件处理测试规则

1. **页面生命周期事件**：
   - 测试 onPageBegin 触发时机
   - 测试 onPageEnd 触发条件
   - 验证事件参数

2. **进度事件**：
   - 测试 onProgressChange 触发频率
   - 验证进度值范围
   - 测试进度回调准确性

3. **错误处理事件**：
   - 测试 onReceivedError 触发条件
   - 验证错误信息
   - 测试各类错误场景

## 四、模块特有代码模板

### 4.1 页面加载测试模板

```typescript
/**
 * @tc.name ArkWeb Load URL Test
 * @tc.number SUB_ARKWEB_WEB_LOAD_URL_001
 * @tc.desc 测试 Web 组件加载 URL 功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testWebLoadUrl001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建 WebViewController
  let controller = new webview.WebViewController();

  // 2. 加载测试页面
  let url = 'resource://rawfile/test.html';
  controller.loadUrl(url);

  // 3. 验证加载状态
  // (需要通过 onPageEnd 事件验证)
});
```

### 4.2 权限控制测试模板

```typescript
/**
 * @tc.name ArkWeb JavaScript Access Test
 * @tc.number SUB_ARKWEB_WEB_JS_ACCESS_001
 * @tc.desc 测试 Web 组件 JavaScript 执行权限控制
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testWebJsAccess001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建组件和控制器
  let controller = new webview.WebViewController();

  // 2. 禁用 JavaScript
  // (设置 javaScriptAccessEnabled = false)

  // 3. 加载包含 JS 的页面
  controller.loadUrl('resource://rawfile/test_with_js.html');

  // 4. 验证 JS 未执行
  // (需要通过验证页面状态)
});
```

## 五、测试注意事项

1. **页面资源准备**：
   - 准备多种类型的测试页面
   - 包含不同资源的页面
   - 包含 JavaScript 的页面

2. **异步验证**：
   - 页面加载是异步的
   - 需要监听事件验证
   - 使用回调或 Promise

3. **网络依赖**：
   - 远程 URL 测试需要网络
   - 需要处理网络异常
   - 考虑离线测试场景

## 六、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 Web 模块配置
