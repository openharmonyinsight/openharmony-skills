# ArkWeb + Chrome DevTools MCP 使用指南

## 📋 目录
1. [概述](#概述)
2. [快速开始](#快速开始)
3. [MCP 配置](#mcp-配置)
4. [26 种调试工具详解](#26-种调试工具详解)
5. [实战案例](#实战案例)
6. [高级技巧](#高级技巧)
7. [故障排除](#故障排除)

---

## 概述

### 什么是 Chrome DevTools MCP？

**Chrome DevTools MCP** 是 Google 官方提供的 MCP 服务器，让 AI 编程助手能够通过 **26 种调试工具**完全控制浏览器。

### 为什么集成 MCP？

✅ **AI 自动化测试**：让 AI 自动执行测试用例
✅ **智能调试**：AI 分析错误、性能瓶颈
✅ **自然语言交互**：用描述性语言控制浏览器
✅ **完整调试能力**：性能分析、网络监控、DOM 操作

### 完整流程

```
┌─────────────────┐
│ ArkWeb 应用     │
│ (HarmonyOS 设备)│
└────────┬────────┘
         │ HDC fport
         ▼
┌─────────────────┐
│ Localhost:9222  │ ← 端口转发
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Chrome DevTools MCP     │
│ (26 种调试工具)         │
└────────┬────────────────┘
         │ MCP 协议
         ▼
┌─────────────────────────┐
│ AI Agent                │
│ (Claude, Cursor, etc.)  │
└─────────────────────────┘
```

---

## 快速开始

### 步骤1：启动 ArkWeb 调试会话

```bash
# 使用 arkweb-app-debug 工具
arkweb-app-debug start --package com.example.arkwebtesting

# 输出示例：
# ✓ Device found: 2MM0223C13000700
# ✓ Application started
# ✓ Found socket: webview_devtools_remote_64811
# ✓ Port forward created: localhost:9222
# ✓ DevTools connection verified
#
# 🔧 MCP Browser URL: http://127.0.0.1:9222
```

### 步骤2：配置 MCP 客户端

根据你使用的 AI 助手，选择对应配置：

#### Claude Code

```bash
claude mcp add chrome-devtools --scope user \
  npx chrome-devtools-mcp@latest \
  --browser-url=http://127.0.0.1:9222
```

#### Cursor

```
Settings -> MCP -> New MCP Server
Command: npx
Args:
  - chrome-devtools-mcp@latest
  - --browser-url=http://127.0.0.1:9222
```

#### VS Code / Copilot

```bash
code --add-mcp '{"command":"npx","args":["chrome-devtools-mcp@latest","--browser-url=http://127.0.0.1:9222"],"env":{}}'
```

### 步骤3：开始使用

在 AI Agent 中输入：

```
请帮我测试登录功能
```

AI 会自动：
1. 打开登录页面
2. 填写表单
3. 点击登录
4. 验证结果
5. 生成报告

---

## MCP 配置

### 基础配置

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222"
      ]
    }
  }
}
```

### 可选参数

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222",
        "--no-usage-statistics",     // 禁用使用统计
        "--no-performance-crux"      // 禁用 CrUX API
      ]
    }
  }
}
```

### 端口配置

如果你使用不同端口：

```bash
# 启动时指定端口
arkweb-app-debug start --package com.example.app --local-port 9223

# MCP 配置对应修改
"--browser-url=http://127.0.0.1:9223"
```

---

## 26 种调试工具详解

### 🖱️ Input Automation（输入自动化）

#### 1. `click` - 点击元素

**用途**：测试按钮、链接交互

**参数**：
- `selector`: CSS 选择器
- `waitForNavigation`: 是否等待导航

**示例**：
```
请点击登录按钮
→ AI: click(selector="#login-button")
```

#### 2. `fill` - 填写表单

**用途**：输入文本

**参数**：
- `selector`: CSS 选择器
- `value`: 输入值

**示例**：
```
填写用户名 testuser
→ AI: fill(selector="#username", value="testuser")
```

#### 3. `fill_form` - 批量填写

**用途**：一次填写多个字段

**参数**：
- `fields`: 字典 `{selector: value}`

**示例**：
```
填写登录表单：用户名testuser，密码test123
→ AI: fill_form(fields={
    "#username": "testuser",
    "#password": "test123"
  })
```

#### 4. `drag` - 拖拽

**用途**：测试拖放功能

#### 5. `hover` - 鼠标悬停

**用途**：测试 tooltip、hover 效果

#### 6. `press_key` - 按键

**用途**：测试键盘快捷键

**示例**：
```
按 Enter 键提交表单
→ AI: press_key(key="Enter")
```

#### 7. `handle_dialog` - 处理对话框

**用途**：接受/拒绝 alert、confirm

#### 8. `upload_file` - 上传文件

**用途**：测试文件上传

---

### 🧭 Navigation Automation（导航自动化）

#### 9. `navigate_page` - 导航到 URL

**用途**：打开页面

**示例**：
```
打开登录页面
→ AI: navigate_page(url="/login")
```

#### 10. `new_page` - 打开新标签

**用途**：多标签测试

#### 11. `list_pages` - 列出所有页面

**用途**：查看打开的标签

#### 12. `select_page` - 选择页面

**用途**：切换测试标签

#### 13. `close_page` - 关闭页面

**用途**：清理测试标签

#### 14. `wait_for` - 等待条件

**用途**：等待元素加载/事件

**参数**：
- `selector`: 等待元素出现
- `timeout`: 超时时间

**示例**：
```
等待欢迎消息出现
→ AI: wait_for(selector=".welcome-message", timeout=5000)
```

---

### 📱 Emulation（模拟）

#### 15. `emulate` - 模拟设备/网络

**用途**：测试响应式设计、弱网

**参数**：
- `device`: 设备名称（如 "iPhone 12"）
- `network`: 网络类型（如 "offline", "slow 3G"）

**示例**：
```
模拟 iPhone 12 查看
→ AI: emulate(device="iPhone 12")

模拟慢速 3G 网络
→ AI: emulate(network="Slow 3G")
```

#### 16. `resize_page` - 调整视口

**用途**：测试不同屏幕尺寸

---

### 📊 Performance（性能分析）

#### 17. `performance_start_trace` - 开始性能追踪

**用途**：记录性能数据

#### 18. `performance_stop_trace` - 停止性能追踪

**用途**：生成性能报告

#### 19. `performance_analyze_insight` - 性能分析

**用途**：获取性能优化建议

**示例**：
```
分析首页性能
→ AI: 
  1. performance_start_trace()
  2. navigate_page(url="/")
  3. wait_for(condition="load")
  4. performance_stop_trace()
  5. performance_analyze_insight()
```

---

### 🌐 Network（网络监控）

#### 20. `list_network_requests` - 列出网络请求

**用途**：监控所有网络活动

**示例**：
```
列出所有 API 请求
→ AI: list_network_requests()
```

#### 21. `get_network_request` - 获取请求详情

**用途**：检查请求头、响应头、状态码

---

### 🐛 Debugging（调试）

#### 22. `evaluate_script` - 执行 JavaScript

**用途**：动态测试、数据提取

**示例**：
```
检查页面标题
→ AI: evaluate_script("document.title")

获取登录状态
→ AI: evaluate_script("document.cookie.includes('logged_in')")
```

#### 23. `list_console_messages` - 列出控制台消息

**用途**：查看所有日志

#### 24. `get_console_message` - 获取控制台消息

**用途**：查看详细错误信息

#### 25. `take_screenshot` - 截图

**用途**：视觉验证、bug 截图

**参数**：
- `path`: 保存路径

**示例**：
```
截图当前页面
→ AI: take_screenshot(path="screenshot.png")
```

#### 26. `take_snapshot` - 快照

**用途**：获取 HTML 快照

---

## 实战案例

### 案例1：自动化登录测试

```
用户提示：
"帮我测试登录功能，用户名testuser，密码test123"

AI 自动执行：
1. navigate_page(url="/login")
2. take_screenshot(path="before-login.png")
3. fill(selector="#username", value="testuser")
4. fill(selector="#password", value="test123")
5. click(selector="#login-button")
6. wait_for(selector=".user-profile", timeout=5000)
7. take_screenshot(path="after-login.png")
8. evaluate_script("""
    document.querySelector('.user-name').textContent === 'testuser'
   """)
9. list_console_messages()  # 检查错误
10. 生成测试报告
```

### 案例2：性能分析

```
用户提示：
"分析首页加载性能，找出瓶颈"

AI 自动执行：
1. performance_start_trace()
2. navigate_page(url="/")
3. wait_for(condition="load")
4. performance_stop_trace()
5. performance_analyze_insight()
6. list_network_requests()
7. analyze:
   - 最慢的资源
   - 阻塞渲染的资源
   - 未压缩的资源
8. 生成优化建议
```

### 案例3：API 测试

```
用户提示：
"测试 /api/users 接口，检查响应"

AI 自动执行：
1. navigate_page(url="/")
2. evaluate_script("""
    fetch('/api/users').then(r => r.json()).then(console.log)
   """)
3. list_network_requests(filter="/api/users")
4. get_network_request(id)
5. verify:
   - 状态码 = 200
   - 响应时间 < 500ms
   - 响应格式正确
6. 生成 API 报告
```

### 案例4：表单验证测试

```
用户提示：
"测试注册表单的验证逻辑"

AI 自动执行：
1. navigate_page(url="/register")
2. 测试空提交：
   - click(selector="#register-button")
   - wait_for(selector=".error")
   - take_screenshot(path="empty-error.png")
3. 测试无效邮箱：
   - fill(selector="#email", value="invalid-email")
   - click(selector="#register-button")
   - verify 错误提示
4. 测试弱密码：
   - fill(selector="#password", value="123")
   - click(selector="#register-button")
   - verify 密码强度提示
5. 生成验证报告
```

---

## 高级技巧

### 技巧1：组合多个工具

```
用户提示：
"测试完整的购物流程：登录、浏览商品、加入购物车、结账"

AI 自动执行完整流程：
1. navigate_page(url="/login")
2. fill_form(...)
3. click("#login-button")
4. wait_for(".user-profile")
5. navigate_page(url="/products")
6. wait_for(".product-card")
7. click(".product-card:first-child")
8. click("#add-to-cart")
9. navigate_page(url="/cart")
10. verify cart items
11. click("#checkout")
12. 填写支付信息
13. verify order confirmation
14. 生成完整测试报告
```

### 技巧2：条件判断

```
用户提示：
"检查页面是否有错误，有则截图"

AI 自动执行：
1. list_console_messages(level="error")
2. if errors.length > 0:
     - take_screenshot(path="errors.png")
     - get_console_message(id) for each error
     - generate error report
   else:
     - log("No errors found")
```

### 技巧3：数据驱动测试

```
用户提示：
"用以下数据测试登录：
- testuser/test123 (有效)
- invalid/test123 (无效)
- testuser/wrongpass (错误密码)"

AI 自动执行：
for each test_case:
  1. navigate_page(url="/login")
  2. fill(username, password)
  3. click("#login-button")
  4. verify expected result
  5. take_screenshot(path="test-{case}.png")
6. 生成对比报告
```

### 技巧4：性能回归测试

```
用户提示：
"对比当前版本和基准版本的性能"

AI 自动执行：
# 基准版本
1. navigate_page(url="/", version="baseline")
2. performance_start_trace()
3. reload
4. performance_stop_trace()
5. save_metrics("baseline.json")

# 当前版本
6. navigate_page(url="/", version="current")
7. performance_start_trace()
8. reload
9. performance_stop_trace()
10. save_metrics("current.json")

# 对比
11. compare_metrics("baseline.json", "current.json")
12. 生成回归报告
```

---

## 故障排除

### 问题1：MCP 连接失败

**症状**：
```
Error: Could not connect to browser at http://127.0.0.1:9222
```

**解决方案**：

1. 检查端口转发
```bash
arkweb-app-debug port list
# 应显示：localhost:9222 -> localabstract:webview_devtools_remote_XXXXX
```

2. 测试 DevTools 连接
```bash
curl http://localhost:9222/json
# 应返回 JSON 数组
```

3. 重启调试会话
```bash
arkweb-app-debug stop-all
arkweb-app-debug start --package com.example.app
```

### 问题2：工具调用失败

**症状**：
```
Error: Element not found: #login-button
```

**解决方案**：

1. 先截图查看页面状态
```
请截图当前页面
→ AI: take_screenshot(path="debug.png")
```

2. 列出所有页面
```
列出所有打开的页面
→ AI: list_pages()
```

3. 检查控制台错误
```
检查是否有 JavaScript 错误
→ AI: list_console_messages(level="error")
```

### 问题3：应用未响应

**症状**：AI 操作后页面无反应

**解决方案**：

1. 增加等待时间
```
点击后等待 5 秒
→ AI: 
  1. click(selector="#button")
  2. wait_for(timeout=5000)
```

2. 检查网络请求
```
检查是否有请求发出
→ AI: list_network_requests()
```

3. 评估页面状态
```
检查页面加载状态
→ AI: evaluate_script("document.readyState")
```

### 问题4：性能追踪无数据

**症状**：`performance_analyze_insight()` 返回空

**解决方案**：

1. 确保正确开始/停止追踪
```
请完整执行性能追踪
→ AI:
  1. performance_start_trace()
  2. navigate_page(url="/")
  3. wait_for(condition="load", timeout=10000)
  4. performance_stop_trace()
  5. performance_analyze_insight()
```

2. 增加等待时间
```
等待页面完全加载后再分析
→ AI:
  1. wait_for(selector="body.loaded", timeout=15000)
  2. performance_stop_trace()
```

---

## 最佳实践

### 1. 提示词编写

✅ **好的提示词**：
```
请测试登录功能：
1. 打开 /login 页面
2. 输入用户名 testuser
3. 输入密码 test123
4. 点击登录按钮
5. 等待跳转
6. 验证显示欢迎消息
7. 截图保存
8. 检查控制台错误
```

❌ **不好的提示词**：
```
测试登录
```

### 2. 测试流程

```
1. 明确测试目标
2. 编写详细步骤
3. 指定验证方法
4. 要求生成报告
5. 保存截图和数据
```

### 3. 性能测试

```
1. 多次测试取平均值
2. 清除缓存后再测试
3. 对比不同版本
4. 关注关键指标：
   - FCP (First Contentful Paint)
   - LCP (Largest Contentful Paint)
   - TTI (Time to Interactive)
```

### 4. 调试流程

```
1. 截图初始状态
2. 执行操作
3. 截图结果状态
4. 检查控制台
5. 检查网络请求
6. 评估页面状态
7. 生成完整报告
```

---

## 进阶：自定义场景

### 场景1：E2E 测试套件

```
用户提示：
"运行完整的 E2E 测试套件：
1. 用户注册
2. 用户登录
3. 浏览商品
4. 添加到购物车
5. 结账
6. 查看订单历史"

AI 自动执行完整测试套件，生成综合报告
```

### 场景2：兼容性测试

```
用户提示：
"测试页面在不同设备上的兼容性：
- iPhone 12
- iPad Pro
- Desktop 1920x1080
- Desktop 1366x768"

AI 自动：
1. emulate() 不同设备
2. resize_page() 不同尺寸
3. take_screenshot() 保存
4. 生成对比报告
```

### 场景3：压力测试

```
用户提示：
"测试页面在慢速网络下的表现：
1. Offline
2. Slow 3G
3. Fast 3G
4. Regular 4G"

AI 自动测试每种网络条件，生成性能报告
```

---

## 资源链接

- **Chrome DevTools MCP GitHub**: https://github.com/ChromeDevTools/chrome-devtools-mcp
- **MCP 协议规范**: https://modelcontextprotocol.io/
- **Claude Code MCP 文档**: https://code.anthropic.com/docs/mcp
- **ArkWeb 调试指南**: `docs/DEBUG_GUIDE.md`
- **设计文档**: `docs/DESIGN_V3.md`

---

**文档版本**: v3.0
**更新日期**: 2025-02-07
**适用于**: ArkWeb DevTools Debugging Skill v3.0+
