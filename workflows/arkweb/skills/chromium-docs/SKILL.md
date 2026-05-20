---
name: chromium-docs
description: >-
  搜索 Chromium 官方文档索引（docs/**/*.md + 各模块 README）。
  基于 chromium_agents 的 chromium_docs.py 自动索引。
  用于理解 Chromium 架构、编程模式、构建系统、测试框架等。
  触发词：Chromium 文档、Chromium 架构、Blink 文档、Mojo 文档、线程模型。
---

# Chromium Documentation Search（集成自 chromium_agents）

## 功能

从 Chromium 源码仓库的 `docs/**/*.md` 和各模块 `README.md` 自动构建文档索引，支持关键词搜索和分类浏览。

**数据源**: `OpenHarmony-TPC/chromium_src` 仓库（`docs/` 下 183+ md 文件）
**工具**: `skills/chromium-docs/scripts/chromium_docs.py`
**索引生成**: 自动扫描，约 30 秒完成

## 使用方式

### 首次使用：构建索引

```bash
python skills/chromium-docs/scripts/chromium_docs.py --build-index
```

需要在 chromium_src 源码目录下执行，或通过 `--src-root` 指定路径。

### 搜索文档

```bash
python skills/chromium-docs/scripts/chromium_docs.py "mojo ipc"
python skills/chromium-docs/scripts/chromium_docs.py "gpu architecture"
python skills/chromium-docs/scripts/chromium_docs.py "threading model"
```

### AI Agent 调用

在 task 描述中注入搜索结果：

```
请搜索 Chromium 文档中关于"滚动"的相关内容，
使用 skills/chromium-docs/scripts/chromium_docs.py "scroll"
```

## 文档分类

| 分类 | 说明 |
|------|------|
| architecture | 架构设计、多进程模型 |
| api | Mojo/mojom 接口 |
| testing | 单元测试、browser test |
| gpu | GPU/WebGL/Vulkan |
| network | 网络栈/HTTP/QUIC |
| security | 沙箱/权限/CORS |
| media | 音视频/编解码 |
| ui | Views/Aura |
| build | GN/Ninja/编译 |
| ohos | OHOS 适配（自定义分类） |
| blink | Blink 渲染引擎 |
| content | Content 层 |

## 与 oh-chromium-knowledge 的关系

| 工具 | 索引内容 | 用途 |
|------|---------|------|
| **chromium-docs** | 文档（docs/*.md） | 理解架构、编程模式、开发规范 |
| **oh-chromium-knowledge** | 代码路径（routing_table） | 定位具体文件、代码路径 |

两者互补：先通过 chromium-docs 理解架构，再通过 oh-chromium-knowledge 定位代码。

## 索引维护

- **首次使用**前必须 `--build-index`
- chromium_src 大版本更新后建议重建
- 索引文件位于 `data/indexes/`（已被 .gitignore 排除）

## 文件结构

```
skills/chromium-docs/
├── SKILL.md              ← 本文件
├── scripts/
│   └── chromium_docs.py  ← 索引生成+搜索脚本
└── data/
    └── configs/
        └── search_config.json  ← 搜索配置
```
