# C++ 编码规范

本文档定义 HM Desktop C++ 代码的编码规范。

## 文件头

### Copyright 声明

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

## 命名规范

### 文件命名

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 头文件 | 小写下划线 | `disk_info_service.h` |
| 源文件 | 小写下划线 | `disk_info_service.cpp` |
| IDL 文件 | 大驼峰 | `IDiskInfoService.idl` |

### 类命名

大驼峰 (PascalCase)

```cpp
class DiskInfoService {
};

class FormatManager {
};
```

### 函数命名

大驼峰 (PascalCase)

```cpp
std::vector<DiskInfo> GetDiskList();
DiskInfo GetDiskInfo(const std::string& diskId);
bool Init();
void Release();
```

### 变量命名

小驼峰 (camelCase)

```cpp
int diskCount;
std::string diskId;
bool isMounted;
```

### 成员变量

小驼峰 + 下划线后缀

```cpp
class DiskInfoService {
private:
    std::mutex mutex_;
    bool inited_;
    std::vector<DiskInfo> diskList_;
};
```

### 常量命名

全大写 + 下划线

```cpp
const int MAX_DISK_COUNT = 128;
const std::string DEFAULT_DISK_PATH = "/data/storage";
```

### 命名空间

小写下划线

```cpp
namespace OHOS {
namespace DiskManagement {

} // namespace DiskManagement
} // namespace OHOS
```

## 头文件组织

### 头文件保护符

```cpp
#ifndef DISK_INFO_SERVICE_H
#define DISK_INFO_SERVICE_H

// 内容

#endif // DISK_INFO_SERVICE_H
```

命名格式: `{文件名全大写}_H`

### Include 顺序

1. 对应头文件
2. C 系统库
3. C++ 标准库
4. 第三方库
5. 项目内部库

```cpp
#include "disk_info_service.h"

#include <cstdint>
#include <string>
#include <vector>

#include "hilog/log.h"

#include "disk_info_types.h"
```

## 类定义

### 声明顺序

```cpp
class DiskInfoService {
public:
    // 构造/析构
    DiskInfoService();
    ~DiskInfoService();

    // 禁止拷贝和赋值
    DiskInfoService(const DiskInfoService&) = delete;
    DiskInfoService& operator=(const DiskInfoService&) = delete;

    // 公共接口
    bool Init();
    void Release();
    std::vector<DiskInfo> GetDiskList();

protected:
    // 保护成员

private:
    // 私有方法
    void LoadDiskInfo();

    // 私有成员变量
    std::mutex mutex_;
    bool inited_;
};
```

## 注释规范

### 文件注释

```cpp
/**
 * @file disk_info_service.h
 *
 * @brief 磁盘信息服务定义
 *
 * 该文件定义了磁盘信息服务的接口和实现
 */
```

### 类注释

```cpp
/**
 * @brief 磁盘信息服务
 *
 * 提供磁盘信息查询、磁盘列表获取、磁盘变化监听等功能
 */
class DiskInfoService {
};
```

### 方法注释

```cpp
/**
 * @brief 获取磁盘列表
 *
 * 查询系统中所有可用的磁盘信息
 *
 * @return 磁盘信息列表
 */
std::vector<DiskInfo> GetDiskList();

/**
 * @brief 获取指定磁盘的详细信息
 *
 * @param diskId 磁盘ID
 * @return 磁盘详细信息，如果磁盘不存在返回空
 */
DiskInfo GetDiskInfo(const std::string& diskId);
```

## 代码格式

### 缩进

使用 4 个空格，不使用 Tab

### 大括号

```cpp
// 推荐：K&R 风格
if (condition) {
    DoSomething();
} else {
    DoOther();
}

// 函数定义
bool DiskInfoService::Init()
{
    // 实现
}
```

### 空格

```cpp
// 操作符前后加空格
int result = a + b;
if (x == 0) {

// 逗号后加空格
void Func(int a, int b, int c);

// 模板尖括号
std::vector<DiskInfo> disks;
```

### 行宽

每行不超过 120 字符

## 日志规范

### HiLog 使用

```cpp
#include "hilog/log.h"

static constexpr HiLogLabel LABEL = { LOG_CORE, 0xD00430D, "DiskInfoService" };

// Info 级别
HiLog::Info(LABEL, "Disk info service initialized");

// Debug 级别
HiLog::Debug(LABEL, "Found %{public}zu disks", disks.size());

// Warning 级别
HiLog::Warn(LABEL, "Disk %{public}s not found", diskId.c_str());

// Error 级别
HiLog::Error(LABEL, "Failed to initialize: %{public}d", errorCode);
```

### 日志级别使用

| 级别 | 使用场景 |
|------|----------|
| Debug | 调试信息，生产环境关闭 |
| Info | 关键流程信息 |
| Warn | 可恢复的异常情况 |
| Error | 错误情况 |
| Fatal | 致命错误，服务无法继续 |

## 错误处理

### 返回值

```cpp
// 成功返回 true，失败返回 false
bool Init();

// 返回错误码
int32_t FormatDisk(const std::string& diskId);
// 返回 0 表示成功，负数表示错误码
```

### 异常

不在正常流程中使用异常，仅用于严重错误

```cpp
try {
    // 可能抛出异常的代码
} catch (const std::exception& e) {
    HiLog::Error(LABEL, "Exception: %{public}s", e.what());
}
```

## 资源管理

### 智能指针

优先使用智能指针管理资源

```cpp
// 使用 std::unique_ptr
std::unique_ptr<DiskInfoService> service =
    std::make_unique<DiskInfoService>();

// 使用 std::shared_ptr
std::shared_ptr<DiskInfo> info = std::make_shared<DiskInfo>();
```

### RAII

资源获取即初始化

```cpp
class FileManager {
public:
    FileManager(const std::string& path)
        : file_(fopen(path.c_str(), "r")) {
        if (!file_) {
            throw std::runtime_error("Failed to open file");
        }
    }

    ~FileManager() {
        if (file_) {
            fclose(file_);
        }
    }

private:
    FILE* file_;
};
```

## 线程安全

### 互斥锁

```cpp
class DiskInfoService {
private:
    mutable std::mutex mutex_;
    std::vector<DiskInfo> disks_;

public:
    std::vector<DiskInfo> GetDiskList() {
        std::lock_guard<std::mutex> lock(mutex_);
        return disks_;
    }
};
```

### 条件变量

```cpp
class FormatManager {
private:
    std::mutex mutex_;
    std::condition_variable cv_;
    bool formatDone_ = false;

public:
    void WaitForFormatComplete() {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return formatDone_; });
    }
};
```
