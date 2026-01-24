# OpenHarmony UI 参考文档

本文档目录包含了从 OpenHarmony v6.0 官方文档中提取的核心 UI 开发参考文档。

## 📁 目录结构

```
docs/
├── overview/              # UI 开发概览
│   └── arkts-ui-development-overview.md
├── state-management/      # 状态管理
│   ├── arkts-state-management-overview.md
│   ├── arkts-mvvm-V2.md          # V2 状态管理(推荐)
│   ├── arkts-mvvm.md             # V1 状态管理(传统)
│   ├── arkts-rendering-control-*.md
│   ├── arkts-style.md
│   └── arkts-builder.md
├── layout/                # 布局开发
│   ├── arkts-layout-development-overview.md
│   ├── arkts-layout-development-linear.md
│   ├── arkts-layout-development-stack-layout.md
│   ├── arkts-layout-development-flex-layout.md
│   ├── arkts-layout-development-relative-layout.md
│   ├── arkts-layout-development-grid-layout.md
│   └── arkts-layout-development-create-*.md
├── components/            # 通用组件
│   ├── arkts-common-components-text-display.md
│   ├── arkts-common-components-text-input.md
│   ├── arkts-common-components-button.md
│   ├── arkts-graphics-display.md
│   └── arkts-common-components-richeditor.md
├── navigation/            # 导航路由
│   ├── arkts-navigation-navigation.md
│   ├── arkts-navigation-tabs.md
│   └── arkts-routing.md
├── animation/             # 动画效果
│   ├── arkts-attribute-animation-overview.md
│   ├── arkts-transition-overview.md
│   └── arkts-component-animation.md
├── dialogs/               # 对话框
│   └── arkts-base-dialog-overview.md
├── popup/                 # 弹窗和提示
│   ├── arkts-popup-and-menu-components-popup.md
│   └── arkts-create-toast.md
└── uicontext/             # UI 上下文
    └── arkts-uicontext-custom-dialog.md
```

## 📚 文档说明

### 概览 (overview)
- `arkts-ui-development-overview.md`: OpenHarmony UI 开发总体概览,包含核心概念和开发范式

### 状态管理 (state-management)
- `arkts-state-management-overview.md`: 状态管理概述
- `arkts-mvvm-V2.md`: V2 版本状态管理(推荐用于新项目)
- `arkts-mvvm.md`: V1 版本状态管理(传统方式)
- `arkts-rendering-control-*.md`: 渲染控制(if/else, ForEach, LazyForEach)
- `arkts-style.md`: 样式装饰器(@Styles, @Extend)
- `arkts-builder.md`: @Builder 装饰器

### 布局 (layout)
- `arkts-layout-development-overview.md`: 布局开发概述
- `arkts-layout-development-linear.md`: 线性布局(Row/Column)
- `arkts-layout-development-stack-layout.md`: 层叠布局(Stack)
- `arkts-layout-development-flex-layout.md`: 弹性布局(Flex)
- `arkts-layout-development-relative-layout.md`: 相对布局
- `arkts-layout-development-grid-layout.md`: 网格布局
- `arkts-layout-development-create-*.md`: List, Grid, WaterFlow, Swiper 等容器组件

### 组件 (components)
- `arkts-common-components-text-display.md`: 文本显示组件
- `arkts-common-components-text-input.md`: 文本输入组件
- `arkts-common-components-button.md`: 按钮组件
- `arkts-graphics-display.md`: 图片显示
- `arkts-common-components-richeditor.md`: 富文本编辑器

### 导航 (navigation)
- `arkts-navigation-navigation.md`: Navigation 组件(推荐)
- `arkts-navigation-tabs.md`: Tabs 标签页
- `arkts-routing.md`: Router 路由(传统方式)

### 动画 (animation)
- `arkts-attribute-animation-overview.md`: 属性动画概述
- `arkts-transition-overview.md`: 转场动画
- `arkts-component-animation.md`: 组件动画

### 对话框和弹窗 (dialogs, popup, uicontext)
- `arkts-base-dialog-overview.md`: 基础对话框概览
- `arkts-uicontext-custom-dialog.md`: 自定义对话框
- `arkts-popup-and-menu-components-popup.md`: Popup 弹窗
- `arkts-create-toast.md`: Toast 提示

## 🔗 使用说明

这些文档是从 OpenHarmony v6.0 官方文档中提取的核心参考文档,覆盖了 UI 开发的主要方面。

- **快速查找**: 根据需求查找对应目录下的文档
- **相对路径**: 技能文件中的引用路径为相对于此目录的路径
- **完整文档**: 如需查看完整文档,请参考官方文档仓库

## 📖 官方文档

完整文档位置: `docs-OpenHarmony-v6.0-Release/zh-cn/application-dev/ui/`
