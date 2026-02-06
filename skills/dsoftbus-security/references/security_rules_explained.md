# 软总线安全卫士 - 安全规则详解与示例

> **本文档用途**：这是软总线安全卫士的详细规则参考文档，包含40+条安全规则的完整说明、代码示例和修复方案。
>
> **快速参考**：
> - 📋 [规则索引和工作流程 → 主文档](../skill.md)
> - 📊 [常见错误速查表 → 主文档](../skill.md#常见错误速查表)
>
> **文档组织**：本文档按规则类别组织，每条规则包含：
> - 问题描述
> - 风险等级
> - 问题示例（❌ 错误代码）
> - 修复方案（✅ 正确代码）
> - 检查要点

本文档详细说明软总线安全卫士的40+条安全规则，每条规则都包含详细的解释、问题代码示例和修复方案。

---

## 目录

1. [日志规范](#1-日志规范)
2. [指针安全](#2-指针安全)
3. [临时变量检查](#3-临时变量检查)
4. [数组下标检查](#4-数组下标检查)
5. [锁管理检查](#5-锁管理检查)
6. [fd管理检查](#6-fd管理检查)
7. [内存管理检查](#7-内存管理检查)
8. [敏感信息检查](#8-敏感信息检查)
9. [整数运算检查](#9-整数运算检查)
10. [循环变量检查](#10-循环变量检查)
11. [安全函数检查](#11-安全函数检查)
12. [权限校验检查](#12-权限校验检查)
13. [外部输入校验检查](#13-外部输入校验检查)
14. [外部数据有效性检查](#14-外部数据有效性检查)
15. [常见问题检查](#15-常见问题检查)

---

## 1. 日志规范

### 规则 1.1: 禁止返回 SOFTBUS_ERR

**问题描述**：
函数返回值使用通用的 `SOFTBUS_ERR` 错误码，导致问题定位困难。应返回具体的错误码。

**风险等级**：⚠️ 警告

**问题示例**：
```c
int32_t ConnectToDevice(const char *networkId) {
    if (networkId == NULL) {
        HILOG_ERROR("networkId is NULL");
        return SOFTBUS_ERR;  // ❌ 通用错误码
    }

    if (strlen(networkId) > MAX_NETWORK_ID_LEN) {
        HILOG_ERROR("networkId too long");
        return SOFTBUS_ERR;  // ❌ 通用错误码
    }

    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ConnectToDevice(const char *networkId) {
    if (networkId == NULL) {
        HILOG_ERROR("networkId is NULL");
        return SOFTBUS_INVALID_PARAM;  // ✅ 具体错误码
    }

    if (strlen(networkId) > MAX_NETWORK_ID_LEN) {
        HILOG_ERROR("networkId too long: %{public}zu", strlen(networkId));
        return SOFTBUS_INVALID_PARAM;  // ✅ 具体错误码
    }

    return SOFTBUS_OK;
}
```

**检查要点**：
- 使用 Grep 搜索 `return SOFTBUS_ERR`
- 确认是否可以返回更具体的错误码
- 常用具体错误码：`SOFTBUS_INVALID_PARAM`、`SOFTBUS_MALLOC_ERR`、`SOFTBUS_MUTEX_ERR` 等

---

## 2. 指针安全

### 规则 2.1: 禁止指针位运算

**问题描述**：
对指针进行位运算（`&`, `|`, `^`, `~`, `<<`, `>>`）是未定义行为，可能导致程序崩溃或安全漏洞。

**风险等级**：🔴 严重

**问题示例**：
```c
char *ptr = (char *)0x12345678;
uint32_t value = *(uint32_t *)ptr;  // ❌ 可能未对齐
uint32_t result = ptr & 0xF;        // ❌ 指针位运算
char *aligned = (ptr + 15) & ~15;   // ❌ 指针位运算
```

**修复方案**：
```c
// 使用标准工具对齐
#include <stdalign.h>
alignas(16) char buffer[256];

// 使用 uintptr_t 进行地址运算
uintptr_t addr = (uintptr_t)ptr;
uint32_t alignment = addr & 0xF;  // ✅ 对整数进行位运算
uintptr_t aligned = ((addr + 15) / 16) * 16;  // ✅ 对齐计算
char *alignedPtr = (char *)aligned;
```

**检查要点**：
- 搜索模式：`ptr &`, `ptr |`, `ptr ^`, `~ptr`, `ptr <<`, `ptr >>`
- 确认操作数是否为指针类型
- 建议使用 `uintptr_t` 进行地址运算

---

### 规则 2.2: 检查 sizeof 使用

**问题描述**：
使用 `sizeof(ptr)` 获取的是指针大小（4或8字节），而非指向对象的大小。

**风险等级**：🔴 严重

**问题示例**：
```c
void ProcessData(int32_t *data) {
    memset(data, 0, sizeof(data));  // ❌ 只清零4或8字节
    // 应该清零整个数组
}

void CopyData(char *src) {
    char *dst = SoftBusMalloc(sizeof(src));  // ❌ 只分配4或8字节
    // 应该分配strlen(src) + 1
}
```

**修复方案**：
```c
void ProcessData(int32_t *data, size_t count) {
    memset(data, 0, sizeof(*data) * count);  // ✅ 使用 sizeof(*ptr)
    // 或者
    memset(data, 0, sizeof(int32_t) * count);  // ✅ 使用具体类型
}

void CopyData(const char *src) {
    size_t len = strlen(src);
    char *dst = SoftBusMalloc(len + 1);  // ✅ 基于实际长度分配
    if (dst != NULL) {
        memcpy(dst, src, len + 1);
    }
}
```

**检查要点**：
- 搜索 `sizeof(ptr)` 或 `sizeof(p_)` 等指针变量
- 确认是否应使用 `sizeof(*ptr)` 或具体类型大小
- 内存分配应基于实际数据大小，而非指针大小

---

### 规则 2.3: 空指针解引用检查

**问题描述**：
在使用指针前未检查是否为 NULL，可能导致空指针解引用崩溃。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessMessage(Message *msg) {
    msg->type = MSG_TYPE_REQUEST;  // ❌ 未判空
    return ProcessData(msg->data);  // ❌ 未判空
}

char* GetDeviceName(const DeviceInfo *info) {
    return info->name;  // ❌ 未判空
}
```

**修复方案**：
```c
int32_t ProcessMessage(Message *msg) {
    if (msg == NULL) {  // ✅ 判空
        HILOG_ERROR("msg is NULL");
        return SOFTBUS_INVALID_PARAM;
    }

    msg->type = MSG_TYPE_REQUEST;

    if (msg->data == NULL) {  // ✅ 判空
        HILOG_ERROR("msg->data is NULL");
        return SOFTBUS_INVALID_PARAM;
    }

    return ProcessData(msg->data);
}

char* GetDeviceName(const DeviceInfo *info) {
    if (info == NULL || info->name == NULL) {  // ✅ 判空
        HILOG_ERROR("info or info->name is NULL");
        return NULL;
    }
    return info->name;
}
```

**检查要点**：
- 搜索 `*ptr`, `ptr->` 模式
- 确认使用前是否有 NULL 检查
- 特别注意函数参数、返回值、malloc/calloc 结果

---

### 规则 2.4: IPC 结果判空

**问题描述**：
IPC 流程中的 `ReadCString`、`ReadRawData` 等函数返回值未判空。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t HandleIpcMessage(MessageParcel &data) {
    char *networkId = data.ReadCString();  // ❌ 未判空
    uint32_t len = data.ReadUint32();      // ❌ 未检查读取是否成功

    HILOG_INFO("networkId=%{public}s", networkId);  // 可能崩溃

    return ProcessDevice(networkId, len);
}
```

**修复方案**：
```c
int32_t HandleIpcMessage(MessageParcel &data) {
    char *networkId = data.ReadCString();
    if (networkId == NULL) {  // ✅ 判空
        HILOG_ERROR("ReadCString failed");
        return SOFTBUS_READ_MSG_ERR;
    }

    uint32_t len;
    if (!data.ReadUint32(len)) {  // ✅ 检查读取是否成功
        HILOG_ERROR("ReadUint32 failed");
        return SOFTBUS_READ_MSG_ERR;
    }

    HILOG_INFO("networkId=%{private}s", networkId);

    return ProcessDevice(networkId, len);
}
```

**检查要点**：
- `ReadCString`, `ReadRawData`, `ReadBuffer` 等函数返回值必须判空
- `ReadInt32`, `ReadUint32` 等函数应检查返回值（bool）
- 在使用读取的数据前必须验证读取成功

---

## 3. 临时变量检查

### 规则 3.1: 指针变量初始化

**问题描述**：
指针变量声明时未初始化，使用时可能包含随机值。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessData(void) {
    char *buffer;  // ❌ 未初始化
    int32_t result;

    result = AllocateBuffer(&buffer);
    if (result != SOFTBUS_OK) {
        // buffer 未初始化，如果在错误处理中使用会崩溃
        return result;
    }

    // 使用 buffer...
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ProcessData(void) {
    char *buffer = NULL;  // ✅ 初始化为 NULL
    int32_t result;

    result = AllocateBuffer(&buffer);
    if (result != SOFTBUS_OK) {
        // 安全：buffer 是 NULL
        return result;
    }

    if (buffer == NULL) {  // ✅ 再次检查
        HILOG_ERROR("buffer is NULL");
        return SOFTBUS_ERR;
    }

    // 使用 buffer...
    return SOFTBUS_OK;
}
```

**检查要点**：
- 指针变量声明时必须初始化为 `NULL` 或有效值
- 特别注意局部变量指针
- 检查所有指针声明语句

---

### 规则 3.2: 资源描述符变量初始化

**问题描述**：
文件描述符、socket 等资源描述符未初始化，可能导致错误的关闭操作。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t CreateConnection(void) {
    int32_t fd;  // ❌ 未初始化
    int32_t ret;

    ret = ConnectToServer(&fd);
    if (ret != SOFTBUS_OK) {
        // fd 未初始化，关闭操作可能误关其他fd
        SoftBusSocketClose(fd);
        return ret;
    }

    // 使用 fd...
    SoftBusSocketClose(fd);
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t CreateConnection(void) {
    int32_t fd = -1;  // ✅ 初始化为无效值
    int32_t ret;

    ret = ConnectToServer(&fd);
    if (ret != SOFTBUS_OK) {
        // 安全：fd 是 -1
        return ret;
    }

    if (fd < 0) {  // ✅ 检查有效性
        HILOG_ERROR("Invalid fd: %{public}d", fd);
        return SOFTBUS_ERR;
    }

    // 使用 fd...
    SoftBusSocketClose(fd);
    fd = -1;  // ✅ 关闭后置为无效值
    return SOFTBUS_OK;
}
```

**检查要点**：
- fd、socket 等资源描述符初始化为 `-1`
- 关闭后置为 `-1`
- 使用前检查有效性

---

### 规则 3.3: bool 变量初始化

**问题描述**：
bool 变量未初始化，使用时值不确定。

**风险等级**：🟡 警告

**问题示例**：
```c
int32_t ProcessRequest(Request *req) {
    bool isValid;  // ❌ 未初始化

    ValidateRequest(req, &isValid);

    if (isValid) {  // isValid 值不确定
        // 处理请求
    }
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ProcessRequest(Request *req) {
    bool isValid = false;  // ✅ 初始化为 false

    ValidateRequest(req, &isValid);

    if (isValid) {
        // 处理请求
    }
    return SOFTBUS_OK;
}
```

**检查要点**：
- bool 变量声明时必须初始化为 `true` 或 `false`
- 默认值通常是 `false`（安全默认值）

---

## 4. 数组下标检查

### 规则 4.1: 数组越界风险

**问题描述**：
访问数组元素时未验证下标范围，可能导致缓冲区溢出。

**风险等级**：🔴 严重

**问题示例**：
```c
#define MAX_DEVICES 32
static DeviceInfo g_devices[MAX_DEVICES];

int32_t GetDevice(uint32_t index) {
    // ❌ 未验证 index 范围
    return g_devices[index].id;
}

int32_t UpdateDeviceStatus(uint32_t index, int32_t status) {
    // ❌ 未验证 index 范围
    g_devices[index].status = status;
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
#define MAX_DEVICES 32
static DeviceInfo g_devices[MAX_DEVICES];

int32_t GetDevice(uint32_t index) {
    if (index >= MAX_DEVICES) {  // ✅ 验证范围
        HILOG_ERROR("Invalid index: %{public}u (max: %{public}d)", index, MAX_DEVICES);
        return SOFTBUS_INVALID_PARAM;
    }
    return g_devices[index].id;
}

int32_t UpdateDeviceStatus(uint32_t index, int32_t status) {
    if (index >= MAX_DEVICES) {  // ✅ 验证范围
        HILOG_ERROR("Invalid index: %{public}u (max: %{public}d)", index, MAX_DEVICES);
        return SOFTBUS_INVALID_PARAM;
    }
    g_devices[index].status = status;
    return SOFTBUS_OK;
}
```

**检查要点**：
- 所有数组访问前必须验证下标
- 检查 `arr[index]`, `arr[i]` 等模式
- 同时检查下标类型（signed/unsigned）

---

### 规则 4.2: 外部输入下标合法性校验

**问题描述**：
来自外部的下标值（如网络消息、用户输入）必须严格校验。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t HandleNetworkMessage(const char *data, uint32_t len) {
    uint32_t index = *(uint32_t *)data;  // ❌ 来自网络的值

    // 直接使用外部输入作为下标
    return g_devices[index].id;
}

int32_t ProcessUserRequest(int32_t userId, int32_t slotId) {
    // ❌ 用户输入未验证
    return userTable[userId].slots[slotId];
}
```

**修复方案**：
```c
int32_t HandleNetworkMessage(const char *data, uint32_t len) {
    if (len < sizeof(uint32_t)) {
        HILOG_ERROR("Message too short");
        return SOFTBUS_ERR;
    }

    uint32_t index = *(uint32_t *)data;

    // ✅ 严格验证外部输入
    if (index >= MAX_DEVICES) {
        HILOG_ERROR("Invalid index from network: %{public}u", index);
        return SOFTBUS_INVALID_PARAM;
    }

    return g_devices[index].id;
}

int32_t ProcessUserRequest(int32_t userId, int32_t slotId) {
    // ✅ 验证所有外部输入
    if (userId < 0 || userId >= MAX_USERS) {
        HILOG_ERROR("Invalid userId: %{public}d", userId);
        return SOFTBUS_INVALID_PARAM;
    }

    if (slotId < 0 || slotId >= MAX_SLOTS) {
        HILOG_ERROR("Invalid slotId: %{public}d", slotId);
        return SOFTBUS_INVALID_PARAM;
    }

    return userTable[userId].slots[slotId];
}
```

**检查要点**：
- 所有来自网络、用户输入、文件的下标必须校验
- 检查下限和上限（>= 0 && < MAX）
- 记录非法输入值用于调试

---

## 5. 锁管理检查

### 规则 5.1: SoftBusMutexLock 与 SoftBusMutexUnlock 成对使用

**问题描述**：
Lock 和 Unlock 不成对，可能导致死锁或数据竞争。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessData(void) {
    SoftBusMutexLock(&g_mutex);

    if (errorCondition) {
        return SOFTBUS_ERR;  // ❌ 忘记解锁
    }

    if (anotherError) {
        goto cleanup;  // ❌ 跳过解锁
    }

    SoftBusMutexUnlock(&g_mutex);
    return SOFTBUS_OK;

cleanup:
    // 忘记解锁
    return SOFTBUS_ERR;
}
```

**修复方案**：
```c
int32_t ProcessData(void) {
    int32_t ret = SoftBusMutexLock(&g_mutex);
    if (ret != 0) {
        HILOG_ERROR("Lock failed: %{public}d", ret);
        return SOFTBUS_MUTEX_ERR;
    }

    if (errorCondition) {
        SoftBusMutexUnlock(&g_mutex);  // ✅ 所有返回路径都解锁
        return SOFTBUS_ERR;
    }

    if (anotherError) {
        SoftBusMutexUnlock(&g_mutex);  // ✅ 所有返回路径都解锁
        return SOFTBUS_ERR;
    }

    SoftBusMutexUnlock(&g_mutex);
    return SOFTBUS_OK;
}
```

**检查要点**：
- 每个 Lock 必须有对应的 Unlock
- 检查所有返回路径（return、goto）
- 使用控制流分析验证成对性

---

### 规则 5.2: 锁变量一致性

**问题描述**：
Lock 和 Unlock 使用不同的锁变量，导致同步失败。

**风险等级**：🔴 严重

**问题示例**：
```c
static SoftBusMutex g_mutex1;
static SoftBusMutex g_mutex2;

int32_t ProcessData(void) {
    SoftBusMutexLock(&g_mutex1);

    // 临界区操作

    SoftBusMutexUnlock(&g_mutex2);  // ❌ 锁变量不一致！
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ProcessData(void) {
    int32_t ret = SoftBusMutexLock(&g_mutex1);
    if (ret != 0) {
        return SOFTBUS_MUTEX_ERR;
    }

    // 临界区操作

    ret = SoftBusMutexUnlock(&g_mutex1);  // ✅ 使用同一个锁
    if (ret != 0) {
        HILOG_ERROR("Unlock failed: %{public}d", ret);
    }
    return SOFTBUS_OK;
}
```

**检查要点**：
- Lock 和 Unlock 的锁变量必须一致
- 注意变量名相似的锁（如 mutex1, mutex2）
- 使用宏定义或 RAII 模式避免错误

---

### 规则 5.3: 所有返回路径释放锁

**问题描述**：
部分错误处理路径忘记释放锁。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t MultiStepProcess(void) {
    SoftBusMutexLock(&g_mutex);

    if (step1() != SOFTBUS_OK) {
        SoftBusMutexUnlock(&g_mutex);
        return SOFTBUS_ERR;
    }

    if (step2() != SOFTBUS_OK) {
        // ❌ 忘记解锁
        return SOFTBUS_ERR;
    }

    if (step3() != SOFTBUS_OK) {
        SoftBusMutexUnlock(&g_mutex);
        return SOFTBUS_ERR;
    }

    SoftBusMutexUnlock(&g_mutex);
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t MultiStepProcess(void) {
    int32_t ret = SoftBusMutexLock(&g_mutex);
    if (ret != 0) {
        return SOFTBUS_MUTEX_ERR;
    }

    if (step1() != SOFTBUS_OK) {
        SoftBusMutexUnlock(&g_mutex);
        return SOFTBUS_ERR;
    }

    if (step2() != SOFTBUS_OK) {
        SoftBusMutexUnlock(&g_mutex);  // ✅ 所有路径都解锁
        return SOFTBUS_ERR;
    }

    if (step3() != SOFTBUS_OK) {
        SoftBusMutexUnlock(&g_mutex);
        return SOFTBUS_ERR;
    }

    SoftBusMutexUnlock(&g_mutex);
    return SOFTBUS_OK;
}
```

**检查要点**：
- 遍历所有可能的退出路径
- 确保 Unlock 在每个 return 前调用
- 使用 goto 统一清理代码也是一种方案

---

## 6. fd管理检查

### 规则 6.1: SoftBusSocketCreate 与 SoftBusSocketClose/SoftBusSocketShutDown 成对使用

**问题描述**：
Socket 创建和关闭不成对，导致资源泄漏。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t CreateServer(void) {
    int32_t fd = SoftBusSocketCreate();
    if (fd < 0) {
        return SOFTBUS_ERR;
    }

    if (BindSocket(fd) != SOFTBUS_OK) {
        return SOFTBUS_ERR;  // ❌ 忘记关闭 fd
    }

    // 保存 fd 到全局变量
    g_serverFd = fd;
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t CreateServer(void) {
    int32_t fd = SoftBusSocketCreate();
    if (fd < 0) {
        HILOG_ERROR("Socket create failed");
        return SOFTBUS_SOCKET_ERR;
    }

    if (BindSocket(fd) != SOFTBUS_OK) {
        SoftBusSocketClose(fd);  // ✅ 错误时关闭
        return SOFTBUS_ERR;
    }

    // 保存 fd 到全局变量
    g_serverFd = fd;
    return SOFTBUS_OK;
}
```

**检查要点**：
- 每个 SocketCreate 必须有对应的 SocketClose
- 所有错误路径都要关闭 fd
- fd 关闭后置为 -1

---

### 规则 6.2: fd 是否正确关闭

**问题描述**：
fd 在错误路径或正常退出时未正确关闭。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessConnection(int32_t connFd) {
    char *buffer = SoftBusMalloc(BUFFER_SIZE);
    if (buffer == NULL) {
        return SOFTBUS_ERR;  // ❌ 未关闭 connFd
    }

    int32_t ret = recv(connFd, buffer, BUFFER_SIZE, 0);
    if (ret < 0) {
        SoftBusFree(buffer);
        return SOFTBUS_ERR;  // ❌ 未关闭 connFd
    }

    // 处理数据...

    SoftBusFree(buffer);
    // ❌ 忘记关闭 connFd
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ProcessConnection(int32_t connFd) {
    char *buffer = SoftBusMalloc(BUFFER_SIZE);
    if (buffer == NULL) {
        SoftBusSocketClose(connFd);  // ✅ 关闭 fd
        return SOFTBUS_ERR;
    }

    int32_t ret = recv(connFd, buffer, BUFFER_SIZE, 0);
    if (ret < 0) {
        SoftBusFree(buffer);
        SoftBusSocketClose(connFd);  // ✅ 关闭 fd
        return SOFTBUS_ERR;
    }

    // 处理数据...

    SoftBusFree(buffer);
    SoftBusSocketClose(connFd);  // ✅ 关闭 fd
    return SOFTBUS_OK;
}
```

**检查要点**：
- 函数接收的 fd 参数，如果不再使用应关闭
- 检查所有返回路径
- 注意 fd 的所有权转移

---

## 7. 内存管理检查

### 规则 7.1: 内存申请前大小合法性校验

**问题描述**：
malloc/calloc 的 size 参数未校验，可能导致分配过大或整数溢出。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessData(uint32_t count, uint32_t itemSize) {
    // ❌ 未校验大小
    uint32_t totalSize = count * itemSize;  // 可能溢出
    char *buffer = SoftBusMalloc(totalSize);
    if (buffer == NULL) {
        return SOFTBUS_ERR;
    }
    // ...
}

int32_t AllocateBuffer(uint32_t size) {
    // ❌ size 可能非常大
    return SoftBusMalloc(size);
}
```

**修复方案**：
```c
#define MAX_ALLOC_SIZE (10 * 1024 * 1024)  // 10MB

int32_t ProcessData(uint32_t count, uint32_t itemSize) {
    // ✅ 校验参数
    if (count == 0 || itemSize == 0) {
        HILOG_ERROR("Invalid count or itemSize");
        return SOFTBUS_INVALID_PARAM;
    }

    // ✅ 检查乘法溢出
    if (count > MAX_ALLOC_SIZE / itemSize) {
        HILOG_ERROR("Size overflow: count=%{public}u, itemSize=%{public}u", count, itemSize);
        return SOFTBUS_INVALID_PARAM;
    }

    uint32_t totalSize = count * itemSize;
    char *buffer = SoftBusMalloc(totalSize);
    if (buffer == NULL) {
        return SOFTBUS_ERR;
    }
    // ...
}

int32_t AllocateBuffer(uint32_t size) {
    // ✅ 限制最大分配大小
    if (size > MAX_ALLOC_SIZE) {
        HILOG_ERROR("Size too large: %{public}u", size);
        return NULL;
    }

    return SoftBusMalloc(size);
}
```

**检查要点**：
- 检查 size 是否为 0
- 检查 size 是否超过合理上限
- 检查乘法运算是否溢出
- 定义全局 MAX_ALLOC_SIZE 常量

---

### 规则 7.2: SoftBusMalloc/SoftBusCalloc 与 SoftBusFree 成对使用

**问题描述**：
malloc 和 free 不成对，导致内存泄漏。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ParseConfig(const char *jsonStr) {
    cJSON *root = cJSON_Parse(jsonStr);
    if (root == NULL) {
        return SOFTBUS_ERR;
    }

    cJSON *item = cJSON_GetObjectItem(root, "key");
    if (item == NULL) {
        // ❌ 忘记删除 root
        return SOFTBUS_ERR;
    }

    // 处理 item...

    // ❌ 忘记删除 root
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ParseConfig(const char *jsonStr) {
    cJSON *root = cJSON_Parse(jsonStr);
    if (root == NULL) {
        return SOFTBUS_ERR;
    }

    cJSON *item = cJSON_GetObjectItem(root, "key");
    if (item == NULL) {
        cJSON_Delete(root);  // ✅ 释放资源
        return SOFTBUS_ERR;
    }

    // 处理 item...

    cJSON_Delete(root);  // ✅ 释放资源
    root = NULL;  // ✅ 置空
    return SOFTBUS_OK;
}
```

**检查要点**：
- 每个 malloc 必须有对应的 free
- 检查所有返回路径
- 跨文件追踪 malloc/free 的配对

---

### 规则 7.3: new 与 delete 成对使用

**问题描述**：
C++ 的 new 和 delete 不成对，或 new[] 用 delete 删除。

**风险等级**：🔴 严重

**问题示例**：
```c++
class MessageHandler {
public:
    MessageHandler() {
        buffer_ = new char[1024];  // new[]
    }

    ~MessageHandler() {
        delete buffer_;  // ❌ 应该用 delete[]
    }

private:
    char *buffer_;
};
```

**修复方案**：
```c++
class MessageHandler {
public:
    MessageHandler() {
        buffer_ = new char[1024];
    }

    ~MessageHandler() {
        delete[] buffer_;  // ✅ 使用 delete[]
        buffer_ = nullptr;
    }

private:
    char *buffer_;
};

// 或者使用标准容器
class MessageHandler {
public:
    std::vector<char> buffer_;  // ✅ 自动管理内存
};
```

**检查要点**：
- new 配 delete，new[] 配 delete[]
- 优先使用 std::vector、std::string 等标准容器
- 使用智能指针（std::unique_ptr, std::shared_ptr）

---

### 规则 7.4: 内存申请后判空

**问题描述**：
malloc/calloc 返回值未判空就直接使用。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessData(void) {
    char *buffer = SoftBusMalloc(1024);
    // ❌ 未判空

    strcpy(buffer, "data");  // 可能崩溃
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ProcessData(void) {
    char *buffer = SoftBusMalloc(1024);
    if (buffer == NULL) {  // ✅ 判空
        HILOG_ERROR("Malloc failed");
        return SOFTBUS_MALLOC_ERR;
    }

    strcpy(buffer, "data");
    // 使用 buffer...

    SoftBusFree(buffer);
    return SOFTBUS_OK;
}
```

**检查要点**：
- 所有 malloc/calloc 结果必须判空
- new 操作符在 C++ 中抛出异常，不需要判空（但建议检查 std::bad_alloc）

---

### 规则 7.5: 全局变量释放后置空

**问题描述**：
全局变量 free/delete 后未置空，可能导致双重释放。

**风险等级**：🟡 警告

**问题示例**：
```c
static char *g_buffer = NULL;

int32_t InitBuffer(void) {
    g_buffer = SoftBusMalloc(1024);
    if (g_buffer == NULL) {
        return SOFTBUS_ERR;
    }
    return SOFTBUS_OK;
}

int32_t CleanupBuffer(void) {
    if (g_buffer != NULL) {
        SoftBusFree(g_buffer);
        // ❌ 未置空
    }
    return SOFTBUS_OK;
}

int32_t ReinitBuffer(void) {
    // g_buffer 不是 NULL，可能重复释放或使用野指针
    SoftBusFree(g_buffer);  // ❌ 可能 double free
    g_buffer = SoftBusMalloc(1024);
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
static char *g_buffer = NULL;

int32_t InitBuffer(void) {
    if (g_buffer != NULL) {  // ✅ 检查是否已初始化
        HILOG_WARN("Buffer already initialized");
        return SOFTBUS_OK;
    }

    g_buffer = SoftBusMalloc(1024);
    if (g_buffer == NULL) {
        return SOFTBUS_ERR;
    }
    return SOFTBUS_OK;
}

int32_t CleanupBuffer(void) {
    if (g_buffer != NULL) {
        SoftBusFree(g_buffer);
        g_buffer = NULL;  // ✅ 释放后置空
    }
    return SOFTBUS_OK;
}

int32_t ReinitBuffer(void) {
    CleanupBuffer();  // ✅ 先清理

    g_buffer = SoftBusMalloc(1024);
    if (g_buffer == NULL) {
        return SOFTBUS_ERR;
    }
    return SOFTBUS_OK;
}
```

**检查要点**：
- 全局变量 free/delete 后必须置空
- 重新初始化前先检查和清理
- 避免双重释放

---

### 规则 7.6: 循环体释放后置空

**问题描述**：
循环中释放资源后未置空，下次循环可能双重释放。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessMultipleItems(void) {
    char *buffer = NULL;

    for (int i = 0; i < count; i++) {
        buffer = SoftBusMalloc(1024);
        if (buffer == NULL) {
            return SOFTBUS_ERR;
        }

        // 处理数据...

        SoftBusFree(buffer);
        // ❌ 未置空，下次循环可能出错
    }

    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t ProcessMultipleItems(void) {
    char *buffer = NULL;

    for (int i = 0; i < count; i++) {
        buffer = SoftBusMalloc(1024);
        if (buffer == NULL) {
            return SOFTBUS_ERR;
        }

        // 处理数据...

        SoftBusFree(buffer);
        buffer = NULL;  // ✅ 释放后置空
    }

    return SOFTBUS_OK;
}
```

**检查要点**：
- 循环中的 free/delete 后必须置空
- 避免下次循环使用野指针

---

### 规则 7.7-7.11: 特定资源管理

**问题描述**：
特定资源（正则表达式、cJSON、JSON等）的创建和释放不成对。

**风险等级**：🔴 严重

**问题示例**：
```c
// regcomp / regfree
regex_t reg;
if (regcomp(&reg, pattern, REG_EXTENDED) != 0) {
    return SOFTBUS_ERR;
}
// 使用 reg...
// ❌ 忘记 regfree(&reg)

// cJSON_Parse / cJSON_Delete
cJSON *root = cJSON_Parse(jsonStr);
// ❌ 忘记 cJSON_Delete(root)

// JSON_PrintUnformatted / JSON_Free
char *str = JSON_PrintUnformatted(root);
// ❌ 忘记 JSON_Free(str)

// Anonymize / AnonymizeFree
char *anon = Anonymize(udid);
// ❌ 忘记 AnonymizeFree(anon)

// strdup
char *copy = strdup(original);
// ❌ 忘记 free(copy)

// realpath
char *resolved = realpath(path, NULL);
// ❌ 忘记 free(resolved)
```

**修复方案**：
```c
// regcomp / regfree
regex_t reg;
if (regcomp(&reg, pattern, REG_EXTENDED) != 0) {
    return SOFTBUS_ERR;
}
// 使用 reg...
regfree(&reg);  // ✅ 释放
memset(&reg, 0, sizeof(reg));  // ✅ 清零

// cJSON_Parse / cJSON_Delete
cJSON *root = cJSON_Parse(jsonStr);
if (root != NULL) {
    // 使用 root...
    cJSON_Delete(root);  // ✅ 释放
    root = NULL;
}

// JSON_PrintUnformatted / JSON_Free
char *str = JSON_PrintUnformatted(root);
if (str != NULL) {
    // 使用 str...
    JSON_Free(str);  // ✅ 释放
    str = NULL;
}

// Anonymize / AnonymizeFree
char *anon = Anonymize(udid);
if (anon != NULL) {
    // 使用 anon...
    AnonymizeFree(anon);  // ✅ 释放
    anon = NULL;
}

// strdup
char *copy = strdup(original);
if (copy != NULL) {
    // 使用 copy...
    free(copy);  // ✅ 释放
    copy = NULL;
}

// realpath
char *resolved = realpath(path, NULL);
if (resolved != NULL) {
    // 使用 resolved...
    free(resolved);  // ✅ 释放
    resolved = NULL;
}
```

**检查要点**：
- 每个创建函数都有对应的释放函数
- 检查函数文档，了解释放函数名称
- 使用 RAII 模式或 goto 统一清理

---

## 8. 敏感信息检查

### 规则 8.1: 禁止打印密钥、文件路径、内存地址、udidhash、设备名称、账号 id

**问题描述**：
日志中输出敏感信息，可能导致安全漏洞。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ConnectDevice(const char *networkId, const char *udid,
                      const char *key) {
    HILOG_INFO("Connecting to device:");
    HILOG_INFO("  networkId=%{public}s", networkId);  // ❌ 打印网络ID
    HILOG_INFO("  udid=%{public}s", udid);            // ❌ 打印UDID
    HILOG_INFO("  key=%{public}s", key);              // ❌ 打印密钥
    HILOG_INFO("  key addr=%{public}p", key);         // ❌ 打印地址
    return SOFTBUS_OK;
}

int32_t LoadConfig(const char *configPath) {
    HILOG_INFO("Loading config from: %{public}s", configPath);  // ❌ 打印路径
    // ...
}
```

**修复方案**：
```c
int32_t ConnectDevice(const char *networkId, const char *udid,
                      const char *key) {
    HILOG_INFO("Connecting to device:");
    HILOG_INFO("  networkId=%{private}s", networkId);  // ✅ 匿名化
    HILOG_INFO("  udid=%{private}s", udid);            // ✅ 匿名化
    // ✅ 不打印密钥
    HILOG_INFO("  key length=%{public}zu", strlen(key));
    // ...
}

int32_t LoadConfig(const char *configPath) {
    // ✅ 不打印完整路径
    const char *filename = strrchr(configPath, '/');
    if (filename != NULL) {
        filename++;  // 跳过 '/'
    } else {
        filename = configPath;
    }
    HILOG_INFO("Loading config: %{public}s", filename);
    // ...
}
```

**检查要点**：
- 禁止使用 `%{public}s` 打印敏感字符串
- 使用 `%{private}s` 匿名化
- 密钥、密码、token 绝不打印
- 文件路径只打印文件名
- 内存地址绝不打印

---

### 规则 8.2: 堆栈密钥使用后是否清零

**问题描述**：
栈上的密钥使用后未清零，可能被攻击者读取。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t EncryptData(const char *input, char *output) {
    char sessionKey[32];  // 栈上密钥

    GenerateSessionKey(sessionKey, 32);

    // 使用密钥加密...
    EncryptWithKey(input, output, sessionKey);

    // ❌ 忘记清零密钥
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t EncryptData(const char *input, char *output) {
    char sessionKey[32];

    GenerateSessionKey(sessionKey, 32);

    // 使用密钥加密...
    EncryptWithKey(input, output, sessionKey);

    // ✅ 使用后立即清零
    memset(sessionKey, 0, sizeof(sessionKey));

    return SOFTBUS_OK;
}
```

**检查要点**：
- 栈上的密钥、密码使用后必须清零
- 使用 memset_s 或类似安全函数（如果可用）
- 注意编译器优化可能移除 memset，使用 volatile 或特殊函数

---

### 规则 8.3: udid/networkid/uuid/ip/mac 等匿名化打印

**问题描述**：
设备标识符未匿名化打印，泄露用户隐私。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t OnDeviceConnected(const char *networkId, const char *udid,
                          const char *ip, const char *mac) {
    HILOG_INFO("Device connected:");
    HILOG_INFO("  networkId=%{public}s", networkId);  // ❌
    HILOG_INFO("  udid=%{public}s", udid);            // ❌
    HILOG_INFO("  ip=%{public}s", ip);                // ❌
    HILOG_INFO("  mac=%{public}s", mac);              // ❌
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t OnDeviceConnected(const char *networkId, const char *udid,
                          const char *ip, const char *mac) {
    HILOG_INFO("Device connected:");
    HILOG_INFO("  networkId=%{private}s", networkId);  // ✅ 匿名化
    HILOG_INFO("  udid=%{private}s", udid);            // ✅ 匿名化

    // ✅ IP 地址部分隐藏（只显示前两段）
    char maskedIp[32];
    MaskIpAddress(ip, maskedIp, sizeof(maskedIp));
    HILOG_INFO("  ip=%{public}s", maskedIp);

    // ✅ MAC 地址部分隐藏（只显示前半部分）
    HILOG_INFO("  mac=%{private}s", mac);  // 或者完全匿名化

    return SOFTBUS_OK;
}
```

**检查要点**：
- 所有设备标识符使用 `%{private}s`
- IP 地址可以部分隐藏（如 192.168.xxx.xxx）
- MAC 地址可以部分隐藏（如 aa:bb:cc:xx:xx:xx）
- UUID/UDID 完全匿名化

---

## 9. 整数运算检查

### 规则 9.1: 整数溢出、反转、除0风险

**问题描述**：
整数运算未检查溢出、符号反转或除零。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t AllocateBuffer(uint32_t count, uint32_t size) {
    // ❌ 可能溢出
    uint32_t total = count * size;
    return SoftBusMalloc(total);
}

int32_t CalculateOffset(int32_t base, int32_t offset) {
    // ❌ 可能反转
    int32_t result = base + offset;
    if (result < 0) {
        return SOFTBUS_ERR;
    }
    return result;
}

int32_t DivideData(int32_t a, int32_t b) {
    // ❌ 可能除零
    return a / b;
}
```

**修复方案**：
```c
int32_t AllocateBuffer(uint32_t count, uint32_t size) {
    // ✅ 检查乘法溢出
    if (count != 0 && size > UINT32_MAX / count) {
        HILOG_ERROR("Integer overflow: count=%{public}u, size=%{public}u",
                    count, size);
        return NULL;
    }
    uint32_t total = count * size;

    // ✅ 检查大小上限
    if (total > MAX_ALLOC_SIZE) {
        HILOG_ERROR("Allocation too large: %{public}u", total);
        return NULL;
    }

    return SoftBusMalloc(total);
}

int32_t CalculateOffset(int32_t base, int32_t offset) {
    // ✅ 检查加法溢出
    if ((offset > 0 && base > INT32_MAX - offset) ||
        (offset < 0 && base < INT32_MIN - offset)) {
        HILOG_ERROR("Integer overflow: base=%{public}d, offset=%{public}d",
                    base, offset);
        return SOFTBUS_ERR;
    }
    int32_t result = base + offset;

    if (result < 0) {
        return SOFTBUS_ERR;
    }
    return result;
}

int32_t DivideData(int32_t a, int32_t b) {
    // ✅ 检查除零
    if (b == 0) {
        HILOG_ERROR("Division by zero");
        return SOFTBUS_ERR;
    }

    // ✅ 检查 INT_MIN / -1 溢出
    if (a == INT32_MIN && b == -1) {
        HILOG_ERROR("Integer overflow in division");
        return SOFTBUS_ERR;
    }

    return a / b;
}
```

**检查要点**：
- 加法：检查 `a + b` 是否溢出
- 减法：检查 `a - b` 是否溢出
- 乘法：检查 `a * b` 是否溢出
- 除法：检查除数是否为 0，`INT_MIN / -1` 特殊情况
- 使用 INT_MAX、INT32_MAX 等常量

---

### 规则 9.2: 有符号整数位操作符运算

**问题描述**：
对有符号整数进行位运算（`&`, `|`, `^`, `~`, `<<`, `>>`）是未定义行为。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t SetFlag(int32_t value, int32_t flag) {
    // ❌ 对有符号整数进行位运算
    return value | flag;
}

int32_t ClearFlag(int32_t value, int32_t flag) {
    // ❌ 对有符号整数进行位运算
    return value & ~flag;
}

int32_t ShiftValue(int32_t value, int32_t shift) {
    // ❌ 对有符号整数进行移位
    return value << shift;
}
```

**修复方案**：
```c
uint32_t SetFlag(uint32_t value, uint32_t flag) {
    // ✅ 使用无符号整数
    return value | flag;
}

uint32_t ClearFlag(uint32_t value, uint32_t flag) {
    // ✅ 使用无符号整数
    return value & ~flag;
}

uint32_t ShiftValue(uint32_t value, uint32_t shift) {
    // ✅ 使用无符号整数
    if (shift >= 32) {
        return 0;
    }
    return value << shift;
}
```

**检查要点**：
- 位运算操作数应该是无符号类型
- 移位操作检查移位数量（< 32）
- 使用 `uint32_t`, `uint64_t` 等无符号类型
- 如果必须用有符号，先转换为无符号，运算后再转回

---

## 10. 循环变量检查

### 规则 10.1: 无符号数死循环

**问题描述**：
使用无符号数作为循环变量进行递减，导致死循环。

**风险等级**：🔴 严重

**问题示例**：
```c
void ProcessArray(uint32_t count) {
    // ❌ 永远不会退出（i >= 0 永远为真）
    for (uint32_t i = count; i >= 0; i--) {
        // 处理数据
    }
}

void ReverseArray(int *arr, uint32_t len) {
    // ❌ 死循环
    for (uint32_t i = len - 1; i >= 0; i--) {
        // 交换元素
    }
}
```

**修复方案**：
```c
void ProcessArray(uint32_t count) {
    // ✅ 方案1：使用有符号数
    for (int32_t i = (int32_t)count - 1; i >= 0; i--) {
        // 处理数据
    }

    // ✅ 方案2：反向递增
    for (uint32_t i = 0; i < count; i++) {
        uint32_t idx = count - 1 - i;
        // 处理 arr[idx]
    }

    // ✅ 方案3：使用 while 循环
    uint32_t i = count;
    while (i > 0) {
        i--;
        // 处理 arr[i]
    }
}
```

**检查要点**：
- 搜索 `for (uint.*i = .*; i >= 0; i--)` 模式
- 无符号数永远 >= 0
- 递减循环使用有符号数或改变循环结构

---

### 规则 10.2: 外部数据控制循环的合法性校验

**问题描述**：
循环次数由外部输入控制，未校验合法性。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t ProcessNetworkData(const char *data, uint32_t len) {
    // ❌ 直接使用外部输入作为循环次数
    uint32_t count = *(uint32_t *)data;
    for (uint32_t i = 0; i < count; i++) {
        // 处理数据
    }
}

int32_t ParseUserFile(const char *filename) {
    // ❌ 用户提供的迭代次数
    uint32_t repeatCount = GetUserRepeatCount();
    for (uint32_t i = 0; i < repeatCount; i++) {
        ProcessFile(filename);
    }
}
```

**修复方案**：
```c
#define MAX_ITERATIONS 10000

int32_t ProcessNetworkData(const char *data, uint32_t len) {
    if (len < sizeof(uint32_t)) {
        return SOFTBUS_ERR;
    }

    // ✅ 校验循环次数上限
    uint32_t count = *(uint32_t *)data;
    if (count > MAX_ITERATIONS) {
        HILOG_ERROR("Invalid iteration count: %{public}u", count);
        return SOFTBUS_INVALID_PARAM;
    }

    for (uint32_t i = 0; i < count; i++) {
        // 处理数据
    }
}

int32_t ParseUserFile(const char *filename) {
    // ✅ 限制用户提供的迭代次数
    uint32_t repeatCount = GetUserRepeatCount();
    if (repeatCount > MAX_ITERATIONS) {
        HILOG_ERROR("Invalid repeat count: %{public}u", repeatCount);
        return SOFTBUS_INVALID_PARAM;
    }

    for (uint32_t i = 0; i < repeatCount; i++) {
        ProcessFile(filename);
    }
}
```

**检查要点**：
- 所有外部输入的循环次数必须校验上限
- 定义合理的 MAX_ITERATIONS 常量
- 防止 DoS 攻击（超大循环次数）

---

## 11. 安全函数检查

### 规则 11.1: 安全函数返回值处理

**问题描述**：
安全函数（memcpy_s, strcpy_s 等）返回值未检查。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t CopyData(const char *src, char *dst, uint32_t dstSize) {
    // ❌ 未检查返回值
    memcpy_s(dst, dstSize, src, strlen(src));
    strcpy_s(dst, dstSize, src);
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
int32_t CopyData(const char *src, char *dst, uint32_t dstSize) {
    errno_t err;

    // ✅ 检查返回值
    err = memcpy_s(dst, dstSize, src, strlen(src));
    if (err != 0) {
        HILOG_ERROR("memcpy_s failed: %{public}d", err);
        return SOFTBUS_ERR;
    }

    // ✅ 检查返回值
    err = strcpy_s(dst, dstSize, src);
    if (err != 0) {
        HILOG_ERROR("strcpy_s failed: %{public}d", err);
        return SOFTBUS_ERR;
    }

    return SOFTBUS_OK;
}
```

**检查要点**：
- 所有 *_s 函数必须检查返回值
- memcpy_s, memmove_s, memset_s
- strcpy_s, strncpy_s, strcat_s
- sprintf_s, snprintf_s
- 返回值类型通常是 errno_t

---

### 规则 11.2: 目标缓冲区大小入参与实际大小一致性

**问题描述**：
缓冲区大小参数与实际大小不一致。

**风险等级**：🔴 严重

**问题示例**：
```c
#define BUFFER_SIZE 256
char g_buffer[BUFFER_SIZE];

int32_t StoreData(const char *data) {
    // ❌ 缓冲区大小不一致
    strcpy_s(g_buffer, 1024, data);  // 实际只有256字节
    return SOFTBUS_OK;
}
```

**修复方案**：
```c
#define BUFFER_SIZE 256
char g_buffer[BUFFER_SIZE];

int32_t StoreData(const char *data) {
    // ✅ 使用正确的缓冲区大小
    errno_t err = strcpy_s(g_buffer, BUFFER_SIZE, data);
    if (err != 0) {
        HILOG_ERROR("strcpy_s failed: %{public}d", err);
        return SOFTBUS_ERR;
    }
    return SOFTBUS_OK;
}

// 或者使用 sizeof
int32_t StoreData(const char *data) {
    errno_t err = strcpy_s(g_buffer, sizeof(g_buffer), data);
    if (err != 0) {
        HILOG_ERROR("strcpy_s failed: %{public}d", err);
        return SOFTBUS_ERR;
    }
    return SOFTBUS_OK;
}
```

**检查要点**：
- 缓冲区大小参数应与实际大小一致
- 优先使用 `sizeof(buffer)` 而非硬编码值
- 动态分配的内存使用实际分配大小

---

## 12. 权限校验检查

### 规则 12.1: 新增 SDK IPC 接口权限校验

**问题描述**：
新增 SDK IPC 接口未进行权限校验，可能导致未授权访问。

**风险等级**：🔴 严重

**问题示例**：
```c
int32_t DeleteDevice(const char *networkId) {
    // ❌ 未校验调用者权限
    if (networkId == NULL) {
        return SOFTBUS_INVALID_PARAM;
    }

    // 直接执行删除操作
    return RemoveDevice(networkId);
}
```

**修复方案**：
```c
int32_t DeleteDevice(const char *networkId) {
    // ✅ 校验调用者身份
    if (!CheckCallerPermission(PERMISSION_DEVICE_MANAGE)) {
        HILOG_ERROR("Permission denied: no DEVICE_MANAGE permission");
        return SOFTBUS_PERMISSION_DENIED;
    }

    if (networkId == NULL) {
        return SOFTBUS_INVALID_PARAM;
    }

    // 执行删除操作
    return RemoveDevice(networkId);
}
```

**检查要点**：
- 所有 IPC 接口必须校验权限
- 检查调用者身份和权限
- 记录权限拒绝日志
- 新增接口必须进行安全评审

---

## 13-15. 其他规则（简要说明）

由于篇幅限制，剩余规则在此简要说明。完整示例请参考 SKILL.md 文档中的"常见违规模式"部分。

### 13. 外部输入校验检查

- **路径规范化**：检查 `..`, `.`, `../` 等路径遍历字符
- **TLV 解析长度合法性**：length <= buffer 实际大小
- **源 buffer 实际大小**：拷贝时验证源缓冲区大小
- **完整校验方案**：综合校验所有外部输入

### 14. 外部数据有效性检查

- **基于外部输入的运算**：加减法、内存申请前校验
- **默认长度校验**：不使用默认长度，解析实际长度
- **TLV 格式长度校验**：验证 length 字段合法性

### 15. 常见问题检查

- **异常分支资源释放**：所有错误路径释放资源
- **宏定义资源泄漏**：CHECK_AND_RETURN_LOG_INNER 等宏
- **函数返回值一致性**：返回值类型与函数签名一致
- **格式化打印类型匹配**：使用正确的格式说明符
- **结构体字节对齐**：注意 packed 结构体

---

## 检查清单

> 📋 **快速参考**: 如需快速查阅规则索引和常见错误速查表，请查看 [主文档 - 常见错误速查表](../skill.md#常见错误速查表)

### 快速检查清单

使用以下清单快速验证代码：

- [ ] 所有返回 SOFTBUS_ERR 的地方是否可以用具体错误码
- [ ] 所有 `*ptr` 和 `ptr->` 使用前是否判空
- [ ] 所有数组访问是否验证下标范围
- [ ] 所有 Lock 是否有对应的 Unlock
- [ ] 所有 malloc 是否有对应的 free
- [ ] 所有敏感信息是否使用 `%{private}` 或不打印
- [ ] 所有循环变量类型是否正确（避免无符号递减）
- [ ] 所有外部输入是否校验合法性
- [ ] 所有安全函数返回值是否检查
- [ ] 所有 fd/socket 是否正确关闭

### 高风险代码模式

以下模式需要特别关注：

```c
// 高风险：未经校验的外部输入
arr[external_index]
char *ptr = ExternalFunc();  // 直接使用

// 高风险：资源管理
malloc  without  free
lock    without  unlock
open    without  close

// 高风险：整数运算
a + b  // 可能溢出
a * b  // 可能溢出
a / b  // 可能除零

// 高风险：类型转换
(uint32_t)signed_var  // 可能截断
(char *)raw_addr      // 可能未对齐
```

---

## 总结

本文档详细说明了软总线安全卫士的40+条安全规则。在代码审查时：

1. **使用快速参考表格**快速定位相关规则（[主文档](../skill.md)）
2. **检查常见违规模式**避免重复错误
3. **参考本文档的详细示例**理解每条规则
4. **使用检查清单**逐项验证代码

记住：**上下文分析很重要**。在报告问题时，要考虑代码的上下文，避免误报。某些情况可能有合理的理由违反规则（如：全局变量在别处初始化）。

---

## 📋 附录：参考表格

### 格式化打印类型匹配表

| 类型 | 正确格式说明符 | 常见错误 | 说明 |
|------|---------------|---------|------|
| int32_t | `%d` | 使用`%u` | 有符号32位整数 |
| uint32_t | `%u` | 使用`%d` | 无符号32位整数 |
| int64_t | `%lld` 或 `PRId64` | 使用`%d` | 有符号64位整数 |
| uint64_t | `%llu` 或 `PRIu64` | 使用`%u` | 无符号64位整数 |
| int8_t | `%hhd` | 使用`%d` | 有符号8位整数 |
| uint8_t | `%hhu` | 使用`%d` | 无符号8位整数 |
| 指针 | `%p` | 使用`0x%x` | 内存地址 |

**使用建议**：
- 优先使用 `<inttypes.h>` 中的宏（`PRId64`, `PRIu64` 等）以保证可移植性
- 指针打印使用 `%p`，不要强制转换为整数后打印
- 敏感信息使用 `%{private}s` 匿名化

### 常用安全函数列表

| 函数 | 返回值检查 | 参数要求 | 说明 |
|------|-----------|---------|------|
| `memcpy_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全内存拷贝 |
| `memmove_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全内存移动（处理重叠） |
| `memset_s` | ✅ 建议检查 | 目标缓冲区大小必须正确 | 安全内存填充 |
| `strcpy_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全字符串拷贝 |
| `strncpy_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全字符串限制拷贝 |
| `strcat_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全字符串连接 |
| `sprintf_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全格式化输出 |
| `snprintf_s` | ✅ 必须检查 | 目标缓冲区大小必须正确 | 安全限制格式化输出 |
| `SoftBusMalloc` | ✅ 必须判空 | - | 内存分配 |
| `SoftBusCalloc` | ✅ 必须判空 | - | 内存分配（清零） |
| `SoftBusMutexLock` | ✅ 必须检查返回值 | - | 加锁 |
| `SoftBusMutexInit` | ✅ 必须检查返回值 | - | 锁初始化 |

**使用建议**：
- 所有 `_s` 后缀的安全函数返回值类型为 `errno_t`，成功时返回 `0`（`EOK`）
- `memcpy_s` 等函数在运行时检查缓冲区边界，防止溢出
- `SoftBusMalloc` 失败返回 `NULL`，必须在使用前检查
- `SoftBusMutexLock` 失败可能导致死锁，必须检查返回值

### 常用错误码速查

| 错误码 | 含义 | 使用场景 |
|--------|------|---------|
| `SOFTBUS_OK` | 成功 | 操作成功返回 |
| `SOFTBUS_ERR` | ❌ 通用错误 | **禁止使用**，应使用具体错误码 |
| `SOFTBUS_INVALID_PARAM` | 参数无效 | 参数为NULL、越界等 |
| `SOFTBUS_MALLOC_ERR` | 内存分配失败 | malloc/calloc 返回NULL |
| `SOFTBUS_MEM_ERR` | 内存操作失败 | memcpy_s等失败 |
| `SOFTBUS_LOCK_ERR` | 锁操作失败 | MutexLock/Init失败 |
| `SOFTBUS_MUTEX_ERR` | 互斥锁错误 | 锁相关错误 |
| `SOFTBUS_SOCKET_ERR` | Socket错误 | socket操作失败 |
| `SOFTBUS_READ_MSG_ERR` | 读取消息失败 | IPC读取失败 |
| `SOFTBUS_PERMISSION_DENIED` | 权限拒绝 | 权限校验失败 |
| `SOFTBUS_NO_INIT` | 未初始化 | 模块未初始化 |
| `SOFTBUS_LANE_NOT_FOUND` | Lane未找到 | 特定场景错误码 |

**使用原则**：
- ✅ 返回具体的错误码，便于问题定位
- ❌ 禁止使用 `SOFTBUS_ERR` 通用错误码
- 📝 错误日志应包含具体的错误信息

---

**📖 返回主文档**: [软总线安全卫士技能说明](../skill.md)

