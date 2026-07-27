# ArkWeb 子系统概览

> 更新时间：2026-05-19 | 适用版本：OpenHarmony 5.x | 置信度：基于源码结构 + 试点分析

## 定位

ArkWeb 是 OpenHarmony 的 Web 引擎子系统，基于 Chromium 内核为应用提供 WebView 能力。核心仓为 `web_webview`。

## 模块划分

```
web_webview/
├── ohos_adapter/        # OHOS 平台适配层（display、power、window 等）
├── engine/              # Chromium 引擎封装（Browser Context、Render 进程管理）
├── interfaces/          # 对外接口
│   ├── kits/            # @ohos.web.webview ArkTS SDK API（.d.ts）
│   └── inner_api/       # InnerKit 接口
├── test/                # unittest / xtstest
└── oseprofiling/        # 性能打点
```

## 核心交互边界

| 边界 | 交互方式 | 说明 |
|------|----------|------|
| ArkWeb ↔ 应用 | ArkTS SDK API | @ohos.web.webview，Public API |
| ArkWeb ↔ ArkUI | 组件嵌入 | Web 组件作为 ArkUI 声明式组件嵌入页面 |
| ArkWeb ↔ Chromium | 内部进程间通信 | Browser/Render 进程模型 |
| ArkWeb ↔ 系统服务 | OHOS Adapter | 显示、输入、网络、权限等通过 adapter 桥接 |

## 关键约束

- Public API 变更需走 API Review 流程，影响 XTS 兼容性测试
- Chromium 侧修改涉及上游同步成本，优先在 OHOS 适配层解决
- 跨进程通信（Browser ↔ Render）存在数据大小和时序约束
- Web 组件生命周期与 ArkUI 页面生命周期绑定，需注意销毁时序

## 待确认

- [ ] Chromium 版本升级节奏与 OHOS 发行版的对齐策略（置信度：低）
- [ ] NWeb（系统 WebView）与 Web 组件的能力边界差异（置信度：中）
