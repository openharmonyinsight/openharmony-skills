# ArkWeb 子系统通用配置

> **子系统信息**
> - 名称: ArkWeb
> - Kit包: @kit.ArkWeb
> - 测试路径: test/xts/acts/arkweb/
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、子系统通用配置

### 1.1 API Kit 映射

```typescript
// Web 组件导入
import {webview} from '@kit.ArkWeb';
import {Web, WebViewController} from '@kit.ArkWeb';
```

### 1.2 测试路径规范

```
测试用例目录: test/xts/acts/arkweb/test/
历史用例参考: ${OH_ROOT}/test/xts/acts/arkweb/
文档资料: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-arkweb/
```

### 1.3 模块映射配置

ArkWeb 子系统包含多个模块，每个模块对应一个或多个 API 声明文件：

| 模块名称 | API 声明文件 | 主要 API | 说明 |
|---------|-------------|---------|------|
| **Web** | @ohos.web.webview.d.ts | Web 组件 | Web 视图组件 |
| **WebViewController** | @ohos.web.webview.d.ts | WebViewController | Web 控制器 |
| **WebResourceRequest** | @ohos.web.webview.d.ts | WebResourceRequest | 资源请求 |
| **WebResourceResponse** | @ohos.web.webview.d.ts | WebResourceResponse | 资源响应 |

## 二、子系统通用测试规则

### 2.1 Web 组件测试规则

1. **Web 页面加载测试**：
   - 测试加载本地 HTML 文件
   - 测试加载远程 URL
   - 验证加载成功和失败场景

2. **Web 控制器测试**：
   - 测试 WebViewController 的控制方法
   - 验证 JavaScript 交互
   - 测试页面导航控制

3. **Web 资源加载测试**：
   - 测试资源拦截
   - 验证资源替换
   - 测试自定义响应

4. **辅助工程要求**：
   - Web 组件测试需要辅助工程提供测试页面
   - 辅助工程需包含 HTML/CSS/JavaScript 资源

### 2.2 JavaScript 交互测试规则

1. **JavaScript 执行测试**：
   - 测试 runJavaScript 执行 JavaScript 代码
   - 验证执行结果的返回值
   - 测试异步 JavaScript 执行

2. **JavaScript 对象注入测试**：
   - 测试将 ArkTS 对象注入到 Web 页面
   - 验证 JavaScript 调用 ArkTS 方法
   - 测试参数和返回值传递

### 2.3 辅助工程配置

1. **测试资源放置**：
   ```
   resources/
   └── rawfile/
       ├── test.html
       ├── test.js
       └── test.css
   ```

2. **BUILD.gn 配置**：
   ```gni
   # 辅助工程
   ohos_app_assist_suite("ArkWebTestEntry") {
     testonly = true
     subsystem_name = "arkweb"
     part_name = "arkweb_test"
     certificate_profile = "./signature/auto_ohos_default_com.arkweb.test.p7b"
     hap_name = "ArkWebTestEntry"
   }

   # 测试工程
   ohos_js_app_suite("ArkWebTest") {
     test_hap = true
     testonly = true
     certificate_profile = "./signature/auto_ohos_default_com.arkweb.test.p7b"
     hap_name = "ArkWebTest"
     part_name = "arkweb_test"
     subsystem_name = "arkweb"
     deps = [
       ":ArkWebTestEntry",
     ]
   }
   ```

## 三、已知问题和注意事项

### 3.1 Web 测试限制

1. **资源依赖**：
   - Web 测试需要 HTML/CSS/JavaScript 资源
   - 需要在辅助工程的 resources/rawfile 目录下放置测试页面
   - 远程 URL 测试需要网络环境

2. **异步加载**：
   - 页面加载是异步的
   - 需要通过事件监听验证加载状态
   - 使用 onPageBegin 和 onPageEnd 事件

3. **JavaScript 执行限制**：
   - 异步 JavaScript 执行需要等待
   - 需要页面加载完成后才能执行 JS
   - 注意线程安全和上下文

### 3.2 测试注意事项

1. **页面加载测试**：
   - 需要验证加载成功和失败场景
   - 测试无效 URL 的错误处理
   - 验证页面加载进度回调

2. **JavaScript 交互测试**：
   - 需要准备测试用的 JavaScript 代码
   - 验证参数和返回值的类型转换
   - 测试 JavaScript 异常处理

3. **资源拦截测试**：
   - 需要准备多种类型的资源请求
   - 测试资源替换功能
   - 验证自定义响应内容

4. **性能测试**：
   - 大页面加载性能
   - JavaScript 执行性能
   - 内存占用情况

## 四、参考示例

### 4.1 历史用例参考

```
${OH_ROOT}/test/xts/acts/arkweb/test/
```

### 4.2 测试页面示例

**test.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
</head>
<body>
    <h1 id="title">Test Page</h1>
    <button onclick="handleClick()">Click Me</button>
    <script>
        function handleClick() {
            alert('Button clicked');
        }

        function add(a, b) {
            return a + b;
        }
    </script>
</body>
</html>
```

## 五、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 ArkWeb 子系统通用配置
