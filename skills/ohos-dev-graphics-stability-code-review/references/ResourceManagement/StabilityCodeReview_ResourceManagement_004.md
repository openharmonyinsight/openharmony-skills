---
rule_id: "StabilityCodeReview_ResourceManagement_004"
name: "文件描述符泄漏"
category: "资源管理"
severity: "HIGH"
language: ["cpp", "c", "c++"]
author: "OH-Department7 Stability Team"
---

# 文件描述符泄漏

## 问题描述

文件描述符fd资源需要确保申请和释放一一对应。遗漏释放会造成fd泄露，重复释放会造成double free。文件描述符是操作系统的重要资源，每个进程可打开的文件描述符数量有限，泄漏会导致进程无法打开新文件。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：异常分支fd泄漏
int read_config(const char* path) {
    int fd = open(path, O_RDONLY);  // 打开文件描述符
    if (fd < 0) {
        return -1;
    }
    
    char buf[1024];
    ssize_t n = read(fd, buf, sizeof(buf));
    if (n < 0) {
        return -1;  // 错误：fd泄漏
    }
    
    // 处理数据...
    close(fd);
    return 0;
}

// 场景2：多分支fd泄漏
int process_file(const char* path, int mode) {
    int fd = open(path, mode);
    if (fd < 0) {
        return -1;
    }
    
    if (mode == O_RDONLY) {
        char buf[100];
        if (read(fd, buf, sizeof(buf)) < 0) {
            return -1;  // 错误：fd泄漏
        }
    } else if (mode == O_WRONLY) {
        char data[] = "hello";
        if (write(fd, data, sizeof(data)) < 0) {
            return -1;  // 错误：fd泄漏
        }
    } else {
        return -1;  // 错误：fd泄漏
    }
    
    close(fd);
    return 0;
}

// 场景3：socket fd泄漏
int connect_server(const char* host, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return -1;
    }
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, host, &addr.sin_addr);
    
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        return -1;  // 错误：sock泄漏
    }
    
    return sock;  // 调用者需要关闭
}

// 场景4：double close
void process_data(int fd) {
    char buf[100];
    read(fd, buf, sizeof(buf));
    close(fd);
    // ... 一些代码
    close(fd);  // 错误：double close!
}

// 场景5：pipe fd泄漏
int create_pipe(int* read_fd, int* write_fd) {
    int fds[2];
    if (pipe(fds) < 0) {
        return -1;
    }
    
    *read_fd = fds[0];
    *write_fd = fds[1];
    
    if (*read_fd < 0) {
        return -1;  // 错误：fds[0]和fds[1]都泄漏
    }
    
    return 0;
}
```

### ✅ 修复方案

```cpp
// 修复场景1：使用RAII封装
class FdGuard {
public:
    explicit FdGuard(int fd) : fd_(fd) {}
    ~FdGuard() { if (fd_ >= 0) close(fd_); }
    int get() const { return fd_; }
    int release() { int tmp = fd_; fd_ = -1; return tmp; }
private:
    int fd_;
};

int read_config(const char* path) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) {
        return -1;
    }
    FdGuard guard(fd);  // RAII管理
    
    char buf[1024];
    ssize_t n = read(guard.get(), buf, sizeof(buf));
    if (n < 0) {
        return -1;  // FdGuard自动关闭
    }
    
    return 0;
}

// 修复场景2：统一清理
int process_file(const char* path, int mode) {
    int fd = open(path, mode);
    if (fd < 0) {
        return -1;
    }
    
    int ret = -1;
    
    if (mode == O_RDONLY) {
        char buf[100];
        if (read(fd, buf, sizeof(buf)) >= 0) {
            ret = 0;
        }
    } else if (mode == O_WRONLY) {
        char data[] = "hello";
        if (write(fd, data, sizeof(data)) >= 0) {
            ret = 0;
        }
    }
    
    close(fd);  // 统一清理
    return ret;
}

// 修复场景3：使用unique_fd
using unique_fd = std::unique_ptr<int, decltype(&close_fd)>;

int safe_connect(const char* host, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return -1;
    }
    
    unique_fd fd_ptr(sock, close_fd);
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, host, &addr.sin_addr);
    
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        return -1;  // unique_fd自动关闭
    }
    
    return fd_ptr.release();  // 转移所有权
}

// 修复场景4：避免double close
void process_data(int fd) {
    char buf[100];
    read(fd, buf, sizeof(buf));
    close(fd);
    fd = -1;  // 设为无效值，防止误用
    // ... 一些代码
    // 不再调用close(fd)
}

// 修复场景5：pipe正确处理
int create_pipe(int* read_fd, int* write_fd) {
    int fds[2];
    if (pipe(fds) < 0) {
        return -1;
    }
    
    *read_fd = fds[0];
    *write_fd = fds[1];
    
    // 检查有效性
    if (*read_fd < 0 || *write_fd < 0) {
        close(fds[0]);
        close(fds[1]);
        return -1;
    }
    
    return 0;
}

// 修复场景6：goto统一清理（C风格）
int read_file_goto(const char* path, char* buf, size_t size) {
    int fd = -1;
    ssize_t n = -1;
    
    fd = open(path, O_RDONLY);
    if (fd < 0) {
        goto error;
    }
    
    n = read(fd, buf, size);
    if (n < 0) {
        goto error;
    }
    
    close(fd);
    return 0;
    
error:
    if (fd >= 0) {
        close(fd);
    }
    return -1;
}
```

## 检测范围

检查以下模式：

- `open/openat/socket/accept/creat` 打开的fd
- `pipe/pipe2` 创建的管道fd
- `epoll_create/epoll_create1` 创建的epoll fd
- `inotify_init/signalfd/timerfd_create/eventfd` 等特殊fd
- 异常分支未关闭fd
- 重复关闭同一个fd

### OpenHarmony特有fd类型

OpenHarmony系统中有以下特殊的文件描述符类型：

- **Ashmem fd**：匿名共享内存文件描述符
  - 创建：`AshmemCreate()` 或通过Parcel传递
  - 释放：需要调用专门的释放函数，不是简单的close
  - 示例：`int ashmemFd = AshmemCreate("name", size);`

- **Parcel fd**：IPC数据传输中的文件描述符
  - 通过Parcel传递的fd，所有权可能转移
  - 接收方需要明确是否负责关闭
  - 示例：`int fd = parcel.ReadFileDescriptor();`

- **socketpair fd**：用于IPC通信的socket对
  - 创建：`socketpair()`，返回两个fd
  - 注意两个fd都需要正确管理
  - 示例：`int fds[2]; socketpair(AF_UNIX, SOCK_STREAM, 0, fds);`

- **SyncFence fd**：图形系统同步栅栏
  - 通常通过sptr<SyncFence>管理，fd封装在对象内
  - 不应直接操作内部的fd
  - 示例：`sptr<SyncFence> fence = new SyncFence(fd);`

### 实际代码示例（从graphic_graphic_2d）

```cpp
// 示例1：使用RAII管理dlopen handle
void LoadAndUseLibrary() {
    void* handle = dlopen("libname.so", RTLD_NOW);
    if (!handle) {
        ROSEN_LOGE("dlopen failed");
        return;
    }
    
    // 使用库函数
    auto func = dlsym(handle, "function_name");
    if (!func) {
        dlclose(handle);  // 异常分支正确关闭
        ROSEN_LOGE("dlsym failed");
        return;
    }
    
    // 正常使用
    dlclose(handle);  // 正常关闭
}

// 示例2：socketpair的正确管理
bool CreateCommunicationChannel(int& readFd, int& writeFd) {
    int fds[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, fds) < 0) {
        ROSEN_LOGE("socketpair failed");
        return false;
    }
    
    readFd = fds[0];
    writeFd = fds[1];
    
    // 如果后续操作失败，需要关闭两个fd
    if (!SetupChannel(fds[0], fds[1])) {
        close(fds[0]);
        close(fds[1]);
        return false;
    }
    
    return true;  // 调用者负责关闭readFd和writeFd
}

// 示例3：Ashmem fd管理
void UseAshmem() {
    int ashmemFd = AshmemCreate("shared_memory", 4096);
    if (ashmemFd < 0) {
        ROSEN_LOGE("AshmemCreate failed");
        return;
    }
    
    void* addr = mmap(nullptr, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, ashmemFd, 0);
    if (addr == MAP_FAILED) {
        close(ashmemFd);  // mmap失败，关闭fd
        ROSEN_LOGE("mmap failed");
        return;
    }
    
    // 使用共享内存
    munmap(addr, 4096);
    close(ashmemFd);  // 使用完成，关闭fd
}
```

## 检测要点

1. 识别fd申请操作（open, socket, pipe等）
2. 追踪fd变量到函数结束
3. 检查异常返回分支是否关闭fd
4. 检查是否存在double close
5. 排除使用RAII封装的情况

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：打开的文件描述符fd
- **RISK_TYPE**：资源泄漏/双重释放
- **RISK_PATH**：open -> 异常返回 -> 未close -> fd泄漏 或 close -> close -> double free
- **IMPACT_POINT**：系统资源耗尽、进程崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**：异常分支返回时未关闭fd，或同一fd被关闭两次
- **Propagation**：文件描述符泄漏累积，或无效内存访问
- **Consequence**：进程无法打开新文件、系统资源耗尽、程序崩溃
- **Mitigation**：使用RAII封装（FdGuard/unique_fd）或确保所有分支都调用close

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 使用RAII封装 | FdGuard/unique_fd/AutoCloseFd | 不报 |
| 有close释放 | 异常分支前有close调用 | 不报 |
| fd作为返回值 | return fd变量 | 不报 |
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ResourceManagement_004_trigger.cpp
int trigger_bad_1(const char* path) {
    int fd = open(path, O_RDONLY);  // 应该报：fd泄漏
    if (fd < 0) return -1;
    char buf[100];
    if (read(fd, buf, sizeof(buf)) < 0) {
        return -1;  // fd泄漏
    }
    close(fd);
    return 0;
}

int trigger_bad_2(const char* host, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);  // 应该报：sock泄漏
    if (sock < 0) return -1;
    struct sockaddr_in addr;
    // ...
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        return -1;  // sock泄漏
    }
    return sock;
}

void trigger_bad_3(int fd) {
    close(fd);
    close(fd);  // 应该报：double close
}
```

### 安全用例（不应该报）

```cpp
// test_ResourceManagement_004_safe.cpp
int safe_good_1(const char* path) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    FdGuard guard(fd);  // 安全：RAII管理
    char buf[100];
    if (read(guard.get(), buf, sizeof(buf)) < 0) {
        return -1;
    }
    return 0;
}

int safe_good_2(const char* path) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    char buf[100];
    if (read(fd, buf, sizeof(buf)) < 0) {
        close(fd);  // 安全：手动关闭
        return -1;
    }
    close(fd);
    return 0;
}

// NOPROTECT: 测试代码
int noprotect_case(const char* path) {
    int fd = open(path, O_RDONLY);
    if (read(fd, nullptr, 0) < 0) {
        return -1;
    }
    close(fd);
    return 0;
}
```