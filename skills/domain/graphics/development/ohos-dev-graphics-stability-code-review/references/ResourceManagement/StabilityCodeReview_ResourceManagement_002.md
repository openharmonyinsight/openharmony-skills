---
rule_id: "StabilityCodeReview_ResourceManagement_002"
name: "dlopen需配对dlclose"
category: "资源管理"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# dlopen需配对dlclose

## 问题描述

使用dlopen动态加载共享库函数后，需要使用dlclose进行关闭，否则存在资源泄露。未关闭的动态库会占用系统资源，多次加载但不关闭会导致资源累积，影响系统稳定性。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：dlopen后未dlclose
void LoadAndCallFunction()
{
    void* handle = dlopen("libplugin.so", RTLD_NOW);
    if (handle == nullptr) {
        LOGE("dlopen failed: %s", dlerror());
        return;
    }
    
    void* func = dlsym(handle, "plugin_func");
    if (func == nullptr) {
        LOGE("dlsym failed: %s", dlerror());
        return;  // 错误：handle未关闭
    }
    
    ((void(*)())func)();
    // 错误：函数执行后handle未关闭
}

// 场景2：异常分支未关闭
typedef int (*PluginFunc)(int);

int CallPlugin(const char* libPath, int param)
{
    void* handle = dlopen(libPath, RTLD_NOW);
    if (!handle) {
        return -1;  // 正确：dlopen失败无需关闭
    }
    
    PluginFunc func = (PluginFunc)dlsym(handle, "process");
    if (!func) {
        LOGE("dlsym failed");
        return -1;  // 错误：handle未关闭
    }
    
    int result = func(param);
    if (result < 0) {
        LOGE("Plugin execution failed");
        return -1;  // 错误：handle未关闭
    }
    
    return result;  // 错误：handle未关闭
}

// 场景3：多次dlopen未配对关闭
class PluginManager {
private:
    std::vector<void*> handles_;
    
public:
    bool LoadPlugins(const std::vector<std::string>& paths) {
        for (const auto& path : paths) {
            void* handle = dlopen(path.c_str(), RTLD_NOW);
            if (handle) {
                handles_.push_back(handle);
            }
            // 错误：即使失败，已加载的handles未在析构时关闭
        }
        return !handles_.empty();
    }
    
    // 错误：缺少析构函数关闭handles
};

// 场景4：全局变量持有handle未关闭
void* g_pluginHandle = nullptr;

bool InitPlugin()
{
    g_pluginHandle = dlopen("libservice.so", RTLD_NOW);
    if (!g_pluginHandle) {
        return false;
    }
    return true;
    // 错误：全局handle从未关闭
}

// 场景5：循环中dlopen未关闭
void ProcessMultiplePlugins(const std::vector<std::string>& paths)
{
    for (const auto& path : paths) {
        void* handle = dlopen(path.c_str(), RTLD_NOW);
        if (handle) {
            void* func = dlsym(handle, "execute");
            if (func) {
                ((void(*)())func)();
            }
            // 错误：每次循环handle未关闭
        }
    }
}

// 场景6：条件分支未关闭
void LoadPluginWithOptions(const char* path, bool useLazy)
{
    int flags = useLazy ? RTLD_LAZY : RTLD_NOW;
    void* handle = dlopen(path, flags);
    if (!handle) {
        return;
    }
    
    if (useLazy) {
        // 懒加载场景
        void* func = dlsym(handle, "lazy_init");
        if (!func) {
            return;  // 错误：handle未关闭
        }
        ((void(*)())func)();
    } else {
        // 立即加载场景
        void* func = dlsym(handle, "init");
        ((void(*)())func)();
        // 错误：handle未关闭
    }
}
```

### ✅ 修复方案

```cpp
// 修复场景1：正确配对dlclose
void LoadAndCallFunction()
{
    void* handle = dlopen("libplugin.so", RTLD_NOW);
    if (handle == nullptr) {
        LOGE("dlopen failed: %s", dlerror());
        return;
    }
    
    void* func = dlsym(handle, "plugin_func");
    if (func == nullptr) {
        LOGE("dlsym failed: %s", dlerror());
        dlclose(handle);  // 正确：dlsym失败时关闭
        return;
    }
    
    ((void(*)())func)();
    dlclose(handle);  // 正确：函数执行后关闭
}

// 修复场景2：所有分支正确关闭
typedef int (*PluginFunc)(int);

int CallPlugin(const char* libPath, int param)
{
    void* handle = dlopen(libPath, RTLD_NOW);
    if (!handle) {
        return -1;
    }
    
    PluginFunc func = (PluginFunc)dlsym(handle, "process");
    if (!func) {
        LOGE("dlsym failed");
        dlclose(handle);  // 正确：dlsym失败时关闭
        return -1;
    }
    
    int result = func(param);
    dlclose(handle);  // 正确：执行完成后关闭
    
    if (result < 0) {
        LOGE("Plugin execution failed");
        return -1;
    }
    
    return result;
}

// 修复场景3：RAII封装管理
class DlHandle {
private:
    void* handle_;
    
public:
    explicit DlHandle(const char* path, int flags = RTLD_NOW)
        : handle_(dlopen(path, flags)) {}
    
    ~DlHandle() {
        if (handle_) {
            dlclose(handle_);
        }
    }
    
    bool IsValid() const { return handle_ != nullptr; }
    void* Get() const { return handle_; }
    void* Sym(const char* name) const { return dlsym(handle_, name); }
    
    DlHandle(const DlHandle&) = delete;
    DlHandle& operator=(const DlHandle&) = delete;
};

void UsePluginRAII()
{
    DlHandle handle("libplugin.so");
    if (!handle.IsValid()) {
        LOGE("dlopen failed");
        return;  // 自动关闭
    }
    
    auto func = handle.Sym("plugin_func");
    if (func) {
        ((void(*)())func)();
    }
    // 自动关闭
}

// 修复场景4：PluginManager正确析构
class PluginManager {
private:
    std::vector<void*> handles_;
    
public:
    ~PluginManager() {
        for (void* handle : handles_) {
            if (handle) {
                dlclose(handle);
            }
        }
    }
    
    bool LoadPlugins(const std::vector<std::string>& paths) {
        for (const auto& path : paths) {
            void* handle = dlopen(path.c_str(), RTLD_NOW);
            if (handle) {
                handles_.push_back(handle);
            }
        }
        return !handles_.empty();
    }
};

// 修复场景5：全局变量使用RAII或提供清理函数
class GlobalPluginHandle {
private:
    void* handle_;
    
public:
    GlobalPluginHandle() : handle_(nullptr) {}
    
    ~GlobalPluginHandle() {
        Close();
    }
    
    bool Open(const char* path) {
        Close();  // 先关闭之前的
        handle_ = dlopen(path, RTLD_NOW);
        return handle_ != nullptr;
    }
    
    void Close() {
        if (handle_) {
            dlclose(handle_);
            handle_ = nullptr;
        }
    }
    
    void* Get() { return handle_; }
};

GlobalPluginHandle g_pluginHandle;

bool InitPlugin()
{
    return g_pluginHandle.Open("libservice.so");
}

// 修复场景6：循环中每次关闭
void ProcessMultiplePlugins(const std::vector<std::string>& paths)
{
    for (const auto& path : paths) {
        void* handle = dlopen(path.c_str(), RTLD_NOW);
        if (handle) {
            void* func = dlsym(handle, "execute");
            if (func) {
                ((void(*)())func)();
            }
            dlclose(handle);  // 正确：每次循环都关闭
        }
    }
}

// 修复场景7：使用goto统一清理
void LoadPluginWithOptionsGoto(const char* path, bool useLazy)
{
    void* handle = nullptr;
    
    int flags = useLazy ? RTLD_LAZY : RTLD_NOW;
    handle = dlopen(path, flags);
    if (!handle) {
        goto cleanup;
    }
    
    if (useLazy) {
        void* func = dlsym(handle, "lazy_init");
        if (!func) {
            goto cleanup;
        }
        ((void(*)())func)();
    } else {
        void* func = dlsym(handle, "init");
        ((void(*)())func)();
    }
    
cleanup:
    if (handle) {
        dlclose(handle);
    }
}
```

## 检测范围

检查以下API调用：

- `dlopen()` 动态库加载
- `dlclose()` 动态库关闭
- `dlsym()` 符号查找

## 检测要点

1. 检测`dlopen`调用并记录handle变量
2. 追踪handle变量的生命周期
3. 检查函数结束时是否有对应的`dlclose`
4. 检查所有异常返回分支是否有`dlclose`
5. 排除使用RAII封装类的情况

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：dlopen打开的动态库handle
- **RISK_TYPE**：动态库资源泄露
- **RISK_PATH**：dlopen -> 未dlclose -> handle泄露 -> 系统资源占用
- **IMPACT_POINT**：系统资源耗尽、内存增长

## 影响分析（ImpactAnalysis）

- **Trigger**：使用dlopen加载动态库但未配对dlclose
- **Propagation**：多次加载累积，系统资源持续占用
- **Consequence**：内存增长、文件描述符泄漏、系统不稳定
- **Mitigation**：确保dlopen/dlclose配对使用，或使用RAII封装

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 有dlclose配对 | 存在dlclose调用 | 不报 |
| RAII封装 | DlHandle/ScopeDl类 | 不报 |
| 全局管理类 | 有析构函数管理 | 不报 |
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ResourceManagement_002_trigger.cpp
void trigger_bad_1()
{
    void* handle = dlopen("lib.so", RTLD_NOW);  // 应该报：无dlclose
    if (!handle) return;
    
    auto func = dlsym(handle, "func");
    if (func) ((void(*)())func)();
}

int trigger_bad_2(const char* path)
{
    void* h = dlopen(path, RTLD_LAZY);
    if (!h) return -1;
    
    if (!dlsym(h, "entry")) {
        return -1;  // 应该报：异常返回未dlclose
    }
    return 0;  // 应该报：正常返回也未dlclose
}
```

### 安全用例（不应该报）

```cpp
// test_ResourceManagement_002_safe.cpp
void safe_good_1()
{
    void* handle = dlopen("lib.so", RTLD_NOW);
    if (!handle) return;
    
    auto func = dlsym(handle, "func");
    if (func) ((void(*)())func)();
    
    dlclose(handle);  // 安全：有dlclose
}

void safe_good_2()
{
    DlHandle handle("lib.so");  // 安全：RAII封装
    if (!handle.IsValid()) return;
    
    auto func = handle.Sym("func");
    if (func) ((void(*)())func)();
    // 自动关闭
}

// NOPROTECT: 特殊场景
// NOPROTECT: 长期持有的插件handle
void* g_handle = dlopen("lib.so", RTLD_NOW);
```