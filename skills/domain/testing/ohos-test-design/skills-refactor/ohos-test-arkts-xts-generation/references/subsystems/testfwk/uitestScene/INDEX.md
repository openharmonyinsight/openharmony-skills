# UiTestScene 辅助包文档索引

本文档索引提供了 uitest 辅助包相关的所有文档资源的快速访问链接。

## 主要文档

### 1. [辅助包文档](README.md)
- **内容**: 辅助包界面内容和扩展指南
- **包括**: 概述、目录结构、当前界面内容、辅助包扩展指南
- **适用**: 需要了解辅助包界面结构和添加新功能的开发人员

### 2. [uitest 模块配置](../UiTest.md)
- **内容**: testfwk 子系统 uitest 模块的完整配置
- **包括**: API 信息、错误码测试、代码模板、辅助包启动和使用方法、典型测试场景等
- **适用**: 配置管理、测试生成和使用辅助包进行测试的开发人员和测试人员

## 快速参考

### 辅助包当前页面
- [主页面 (Index.ets)](README.md#1-主页面-indexets) - 主要测试界面，包含各种UI组件
- [第二页面 (second.ets)](README.md#2-第二页面-secondets) - 基础页面测试
- [其他功能页面](README.md#3-其他功能页面) - 第三页、第四页、滚动、拖拽、捏合、穿戴列表、并行测试

### 辅助包扩展指南
- [添加新页面](README.md#添加新页面的方式和思路) - 详细的步骤和示例
- [添加新组件](README.md#添加新组件的方式和思路) - 组件类型、属性设置、事件处理
- [测试支持](README.md#辅助包测试支持) - 设备适配、状态记录、数据重置

## 辅助包使用指南

> **注意**: 辅助包的启动、使用方法、典型测试场景等内容已移至 [uitest 模块配置](../UiTest.md) 文档中。

### 快速访问
- [辅助包启动和使用方法](../UiTest.md#辅助包启动和使用方法)
- [辅助包典型测试场景](../UiTest.md#辅助包典型测试场景)
- [辅助包使用注意事项](../UiTest.md#辅助包使用注意事项)
- [辅助包错误处理](../UiTest.md#辅助包错误处理)
- [辅助包测试最佳实践](../UiTest.md#辅助包测试最佳实践)

## 辅助包元素快速参考

### 主页面 (Index.ets) 元素
| 元素类型 | ID/Key | 功能描述 |
|---------|--------|----------|
| Button | `toastBtn` | Toast 测试按钮 |
| Button | `dialogBtn` | Dialog 测试按钮 |
| Button | `my-key` | 下一页跳转按钮 |
| Button | `twiceBtn` | 双击测试按钮 |
| Button | `jump` | 悬停测试按钮 |
| Button | `scrollBtn` | 滚动测试按钮 |
| Button | `to5` | 并行测试按钮 |
| TextInput | `changTest` | 文本输入框 |
| TextInput | `changContext` | 上下文输入框 |
| Checkbox | `hi` | 复选框1 |
| Checkbox | `go` | 复选框2 |
| Button | `enableFalse` | 禁用按钮 |
| Scroll | `parentScroll` | 滚动容器 |

### 第二页面 (second.ets) 元素
| 元素类型 | ID/Key | 功能描述 |
|---------|--------|----------|
| TextInput | `changTest` | 文本输入框 |
| TextInput | `changContext` | 上下文输入框 |

## 扩展指南快速链接

- [添加新页面的方式和思路](README.md#添加新页面的方式和思路)
  - 确定测试需求
  - 创建新页面文件
  - 页面文件结构
  - 注册新页面
  - 在主页面添加跳转按钮
  - ID 命名规范

- [添加新组件的方式和思路](README.md#添加新组件的方式和思路)
  - 确定组件类型
  - 组件属性设置
  - 状态管理
  - 交互事件处理
  - 手势支持
  - 复杂布局示例

- [辅助包测试支持](README.md#辅助包测试支持)
  - 设备适配
  - 状态记录
  - 测试数据重置

## 相关链接

- [OpenHarmony 官方文档](https://gitee.com/openharmony/docs)
- [OpenHarmony UiTest API 参考](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-test-kit/UiTest.md)
- [OpenHarmony UI 组件开发指南](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/application-test/)