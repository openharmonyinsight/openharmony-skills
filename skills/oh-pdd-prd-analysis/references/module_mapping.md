# 需求到模块映射规则

本文档定义如何将 PRD 需求映射到 HM Desktop 中的服务模块和系统组件。

## 映射层次

```
PRD 需求 → 功能模块 → 服务/组件 → SA/层别分配
```

## 标准模块类型

### 1. 信息服务

**用途**：查询和显示信息

**创建时机**：PRD 要求以下功能时：
- 查看列表
- 获取详情
- 显示状态
- 浏览内容

**命名模式**：`{领域}InfoService`

**示例**：
- DiskInfoService - 磁盘信息服务
- VolumeInfoService - 卷信息服务
- PartitionInfoService - 分区信息服务

**SA 分配**：通常 SA ID 范围 5000-5099

### 2. 管理服务

**用途**：管理生命周期和操作

**创建时机**：PRD 要求以下功能时：
- 创建/删除
- 启动/停止
- 配置/修改
- 管理生命周期

**命名模式**：`{领域}ManagerService`

**示例**：
- FormatManagerService - 格式化管理服务
- MountManagerService - 挂载管理服务
- RepairManagerService - 修复管理服务

**SA 分配**：通常与 InfoService 共享 SA，如复杂则使用独立 SA

### 3. 操作服务

**用途**：执行特定操作

**创建时机**：PRD 要求以下功能时：
- 执行特定操作
- 批量处理
- 定时任务

**命名模式**：`{操作}Service`

**示例**：
- FormatService - 格式化服务
- CheckService - 检测服务
- BackupService - 备份服务

### 4. 监听器/回调服务

**用途**：监控和通知变化

**创建时机**：PRD 要求以下功能时：
- 监听变化
- 事件通知
- 状态回调

**命名模式**：`{事件}Listener` 或 `{事件}Callback`

**示例**：
- DiskChangeListener - 磁盘变化监听
- FormatProgressListener - 格式化进度监听
- StateChangeListener - 状态变化监听

## KEP 到模块的映射

### 映射决策树

```
KEP 涉及：
│
├─ 查询/显示？
│  └─ → {领域}InfoService
│
├─ 生命周期管理？
│  └─ → {领域}ManagerService
│
├─ 一次性操作？
│  └─ → {操作}Service
│
└─ 事件监控？
   └─ → {事件}Listener
```

### 常见 KEP 模式

| KEP 模式 | 服务类型示例 | 示例 |
|----------|----------|------|
| 查看XX | InfoService | 查看磁盘 → DiskInfoService |
| 获取XX | InfoService | 获取容量 → CapacityInfoService |
| 格式化XX | ManagerService | 格式化磁盘 → FormatManagerService |
| 修复XX | ManagerService | 修复磁盘 → RepairManagerService |
| 设置XX | Service | 设置名称 → RenameService |
| 监听XX | Listener | 监听插拔 → DiskChangeListener |

## 服务模块设计

### 模块定义模板

```markdown
### {模块名称}

#### 职责
- [主要职责]
- [次要职责]

#### 输入
- [输入参数1]：[描述]
- [输入参数2]：[描述]

#### 输出
- [输出类型]：[描述]

#### 依赖
- [依赖1]：[原因]
- [依赖2]：[原因]

#### 相关KEP
- KEPX-YY：[KEP名称]
- KEPX-ZZ：[KEP名称]
```

### 模块粒度指南

| 模块规模 | 方法数量 | 建议 |
|----------|----------|------|
| 小 | 1-3个方法 | 考虑与相关模块合并 |
| 中 | 3-6个方法 | 良好粒度 |
| 大 | 6+个方法 | 考虑拆分为子模块 |

## SA 分配规则

### SA ID 分配

| SA ID 范围 | 类别 | 示例 |
|-----------|------|------|
| 1000-1999 | 基础服务 | OsAccount (4101) |
| 2000-2999 | 系统服务 | |
| 3000-3999 | 连接性 | |
| 4000-4999 | 数据与存储 | |
| 5000-5999 | 文件管理 | DiskManagement (5001)、StorageManager (5003) |
| 6000-6999 | 多媒体 | |
| 7000-7999 | 图形 | |
| 8000-8999 | AI与智能 | |
| 9000-9999 | 应用 | |

### 多模块 SA 分配

**何时共享 SA**：
- 模块紧密耦合
- 模块共享状态
- 模块有相似的生命周期

**何时使用独立 SA**：
- 模块独立
- 模块有不同的安全要求
- 模块有不同的可用性要求

**示例**：

```
DiskManagement SA (5001)
├── DiskInfoService (信息服务)
├── FormatManagerService (管理服务)
├── RepairManagerService (管理服务)
└── StatusManagerService (状态管理)
```

理由：所有模块操作相同实体（磁盘）并共享状态。

## 层别分配

### 应用层

**组件**：
- 设置应用页面
- 文件管理器集成
- 系统对话框

**技术**：ArkTS (ETS)

### 服务层

**组件**：
- SA 实现
- NAPI 接口
- 客户端库

**技术**：C++ / IDL / NAPI

### 工具层

**组件**：
- 格式化工具（e2fsprogs、f2fs-tools）
- 检测工具（fsck 变体）
- 分区工具（parted）

**技术**：C / Shell 脚本

### 系统层

**组件**：
- 内核接口
- 驱动接口
- 系统库

**技术**：Kernel / C 库

## 依赖映射

### 常见依赖

| 服务 | 常见依赖 |
|------|----------|
| 所有服务 | hilog、c_utils |
| 信息服务 | sysfs、procfs |
| 管理服务 | 信息服务、工具服务 |
| 格式化服务 | e2fsprogs、f2fs-tools |
| 修复服务 | e2fsprogs、fsck 工具 |
| 需要权限的服务 | OsAccount SA (4101) |
| 需要存储的服务 | StorageManager SA (5003) |
| 需要事件的服务 | HiSysEvent |
| 需要追踪的服务 | HiTrace |

### 依赖关系图示例

```
┌─────────────────────────────────────────────┐
│              应用层                           │
│  设置应用 | 文件管理器 | 系统对话框           │
└─────────────────────────────────────────────┘
                    ↓ NAPI
┌─────────────────────────────────────────────┐
│          DiskManagement SA (5001)            │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐  │
│  │DiskInfo   │  │ Format   │  │ Repair   │  │
│  │ Service   │→│ Manager  │  │ Manager  │  │
│  └───────────┘  └────┬─────┘  └────┬─────┘  │
└────────────────────────┼────────────┼────────┘
                       ↓            ↓
┌─────────────────────────────────────────────┐
│              工具层                           │
│  FormatTool | FsckTool | PartedTool          │
└─────────────────────────────────────────────┘
```

## 模块建议生成

### 算法

1. **提取所有 KEP**：从 PRD 中提取
2. **分组 KEP**：按领域/功能区域分组
3. **识别模式**：（信息服务、管理服务、操作服务、监听器）
4. **创建模块建议**：基于模式
5. **分配 SA ID**：基于类别
6. **映射依赖**：基于服务类型

### 示例输出

```
基于 KEP 分析，建议的模块：

1. DiskInfoService
   - KEP：KEP1-01（查看磁盘信息）、KEP1-02（查看磁盘详情）
   - 类型：信息服务
   - SA：DiskManagement (5001)

2. FormatManagerService
   - KEP：KEP1-03（格式化磁盘）、KEP1-04（格式化进度）
   - 类型：管理服务
   - SA：DiskManagement (5001)
   - 依赖：FormatTool、StorageManager

3. RepairManagerService
   - KEP：KEP1-05（检测磁盘）、KEP1-06（修复磁盘）
   - 类型：管理服务
   - SA：DiskManagement (5001)
   - 依赖：FsckTool、OsAccount

4. StatusManagerService
   - KEP：KEP1-07（查询状态）、KEP1-08（状态变化通知）
   - 类型：信息服务 + 监听器
   - SA：DiskManagement (5001)
```

## 模块命名规范

### C++ 类名

- 模式：`{模块}Service` 或 `{模块}Manager`
- 大小写：大驼峰（PascalCase）
- 示例：`DiskInfoService`、`FormatManagerService`

### IDL 接口名

- 模式：`I{模块}Service`
- 大小写：大驼峰带 I 前缀
- 示例：`IDiskInfoService`、`IFormatManagerService`

### 文件名

- 头文件：`{module}_service.h`（蛇形命名）
- 源文件：`{module}_service.cpp`
- IDL：`I{Module}Service.idl`
- 示例：`disk_info_service.h`、`IDiskInfoService.idl`

### 命名空间

- 模式：`OHOS::{领域}`
- 示例：`OHOS::DiskManagement`

## 快速参考

| 需求 | 建议模块 |
|------|----------|
| 查看列表 | `{领域}InfoService` |
| 获取详情 | `{领域}InfoService` |
| 执行操作 | `{操作}Service` |
| 管理生命周期 | `{领域}ManagerService` |
| 监听变化 | `{事件}ChangeListener` |
| 进度通知 | `{操作}ProgressListener` |
| 重命名 | `RenameService` |
| 删除 | `{领域}RemovalService` |
| 创建 | `{领域}CreationService` |
| 更新 | `{领域}UpdateService` |
