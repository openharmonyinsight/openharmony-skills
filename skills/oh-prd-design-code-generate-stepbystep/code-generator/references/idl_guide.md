# IDL 编写指南

本文档介绍 OpenHarmony IDL (Interface Definition Language) 的编写规范。

## 基本结构

### 文件头

```idl
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0
 * 你可以获取该许可协议的副本：
 *     http://www.apache.org/licenses/LICENSE-2.0
 */
```

### Package 声明

```idl
package OHOS.DiskManagement;
```

命名规范：`OHOS.{模块名}`

### Import 语句

```idl
import "DiskInfoTypes.idl";
import "../common/Types.idl";
```

## 接口定义

### 基本接口

```idl
interface IDiskInfoService {
    // 方法声明
};
```

命名规范：`I{功能名}Service`

### 方法定义

#### 无参数方法

```idl
GetDiskList(): DiskInfo[];
```

#### 输入参数

```idl
GetDiskInfo([in] string diskId): DiskInfo;
```

#### 输出参数

```idl
GetDiskSize([in] string diskId, [out] uint64_t size): boolean;
```

#### 双向参数

```idl
UpdateDiskInfo([inout] DiskInfo info): int;
```

## 数据类型

### 基本类型

| IDL 类型 | C++ 类型 | 说明 |
|----------|----------|------|
| boolean | bool | 布尔值 |
| byte | int8_t | 8位整数 |
| short | int16_t | 16位整数 |
| int | int32_t | 32位整数 |
| long | int64_t | 64位整数 |
| string | std::string | 字符串 |
| float | float | 单精度浮点 |
| double | double | 双精度浮点 |

### 数组类型

```idl
GetDiskList(): DiskInfo[];
```

### 自定义类型

#### Struct 定义

```idl
struct DiskInfo {
    string diskId;
    string diskName;
    uint64_t totalCapacity;
    uint64_t usedCapacity;
    boolean isMounted;
};
```

#### Enum 定义

```idl
enum DiskState {
    UNKNOWN = 0,
    NORMAL = 1,
    ABNORMAL = 2
};
```

## 注释规范

### 接口注释

```idl
/** 磁盘信息服务
 *  提供磁盘信息查询、磁盘列表获取等功能
 */
interface IDiskInfoService {
    ...
};
```

### 方法注释

```idl
/// 获取磁盘列表
/// 返回 系统中所有磁盘的信息
GetDiskList(): DiskInfo[];

/// 获取指定磁盘的详细信息
/// @param diskId 磁盘ID
/// @return 磁盘详细信息
GetDiskInfo([in] string diskId): DiskInfo;
```

## 回调接口

### 定义

```idl
interface IDiskChangeListener {
    /// 磁盘添加事件
    OnDiskAdded([in] DiskInfo diskInfo): void;

    /// 磁盘移除事件
    OnDiskRemoved([in] string diskId): void;

    /// 磁盘变化事件
    OnDiskChanged([in] DiskInfo diskInfo): void;
};
```

### 使用回调

```idl
interface IDiskInfoService {
    /// 注册监听器
    RegisterChangeListener([in] IDiskChangeListener listener): void;

    /// 注销监听器
    UnregisterChangeListener([in] IDiskChangeListener listener): void;
};
```

## 方向参数

| 方向 | 说明 | 使用场景 |
|------|------|----------|
| [in] | 输入参数 | 客户端→服务端 |
| [out] | 输出参数 | 服务端→客户端 |
| [inout] | 双向参数 | 双向传递 |

## 完整示例

```idl
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0
 */

package OHOS.DiskManagement;

import "DiskInfoTypes.idl";

/** 磁盘信息服务
 *  提供磁盘信息查询和变化通知功能
 */
interface IDiskInfoService {
    /// 获取系统中所有磁盘的列表
    /// @return 磁盘信息数组
    GetDiskList(): DiskInfo[];

    /// 获取指定磁盘的详细信息
    /// @param diskId 磁盘唯一标识
    /// @return 磁盘详细信息，如果磁盘不存在返回空
    GetDiskInfo([in] string diskId): DiskInfo;

    /// 注册磁盘变化监听器
    /// @param listener 监听器对象
    RegisterChangeListener([in] IDiskChangeListener listener): void;

    /// 注销磁盘变化监听器
    /// @param listener 要注销的监听器对象
    UnregisterChangeListener([in] IDiskChangeListener listener): void;
};
```

## 常见错误

### 错误 1：缺少 import

```idl
// 错误：未导入 DiskInfoTypes.idl
interface IDiskInfoService {
    GetDiskList(): DiskInfo[];  // DiskInfo 未定义
}

// 正确
import "DiskInfoTypes.idl";
interface IDiskInfoService {
    GetDiskList(): DiskInfo[];
}
```

### 错误 2：参数缺少方向

```idl
// 错误：参数缺少 [in] 标记
GetDiskInfo(string diskId): DiskInfo;

// 正确
GetDiskInfo([in] string diskId): DiskInfo;
```

### 错误 3：返回类型不支持

```idl
// 错误：不支持复杂嵌套
GetComplexData(): map<string, list<DiskInfo>>;

// 正确：使用 struct 封装
GetComplexData(): ComplexData;
```
