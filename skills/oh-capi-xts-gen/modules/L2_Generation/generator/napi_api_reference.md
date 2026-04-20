# N-API 常用 API 参考

> **N-API 常用 API 参考** - 详细的 N-API 常用 API 参考文档，包含参数获取、类型转换、错误处理等

## 概述

本文档提供了 N-API 开发中常用的 API 参考，包括参数获取、类型转换、错误处理、数组操作等。这些 API 是开发 N-API 封装时最常用的基础 API。

## 参数获取和类型检查

### 1. 获取回调信息

```cpp
/**
 * @brief 获取回调信息
 * @param env N-API 环境句柄
 * @param cbinfo 回调信息
 * @param argc 参数数量指针
 * @param argv 参数数组指针
 * @param this_arg this 对象指针
 * @param data 用户数据指针
 * @return napi_status 状态码
 */
napi_status napi_get_cb_info(
    napi_env env,
    napi_callback_info cbinfo,
    size_t* argc,
    napi_value* argv,
    napi_value* this_arg,
    void** data
);
```

**使用示例**：
```cpp
size_t argc = 2;
napi_value args[2];
napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Failed to get callback info");
    return nullptr;
}
```

### 2. 获取值类型

```cpp
/**
 * @brief 获取值的类型
 * @param env N-API 环境句柄
 * @param value 要检查的值
 * @param result 类型指针
 * @return napi_status 状态码
 */
napi_status napi_typeof(
    napi_env env,
    napi_value value,
    napi_valuetype* result
);
```

**使用示例**：
```cpp
napi_valuetype valuetype;
napi_status status = napi_typeof(env, args[0], &valuetype);
if (status != napi_ok || valuetype != napi_string) {
    napi_throw_error(env, nullptr, "Argument must be a string");
    return nullptr;
}
```

**napi_valuetype 枚举**：
```cpp
typedef enum {
    napi_undefined,
    napi_null,
    napi_boolean,
    napi_number,
    napi_string,
    napi_symbol,
    napi_object,
    napi_function,
    napi_external,
    napi_bigint
} napi_valuetype;
```

## napi_value 类型转换

### 1. 字符串转换

#### 获取字符串长度和内容

```cpp
/**
 * @brief 获取 UTF-8 字符串长度
 * @param env N-API 环境句柄
 * @param value 字符串值
 * @param bufsize 缓冲区大小
 * @param result 字符串长度
 * @return napi_status 状态码
 */
napi_status napi_get_value_string_utf8(
    napi_env env,
    napi_value value,
    char* buf,
    size_t bufsize,
    size_t* result
);
```

**使用示例**：
```cpp
// 获取字符串长度
size_t strLen;
napi_status status = napi_get_value_string_utf8(env, args[0], NULL, 0, &strLen);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Failed to get string length");
    return nullptr;
}

// 分配内存
char* param = (char*)malloc(strLen + 1);
if (param == NULL) {
    napi_throw_error(env, nullptr, "Memory allocation failed");
    return nullptr;
}

// 获取字符串内容
status = napi_get_value_string_utf8(env, args[0], param, strLen + 1, NULL);
if (status != napi_ok) {
    free(param);
    napi_throw_error(env, nullptr, "Failed to get string value");
    return nullptr;
}
```

#### 创建字符串

```cpp
/**
 * @brief 创建 UTF-8 字符串
 * @param env N-API 环境句柄
 * @param str 字符串内容
 * @param length 字符串长度
 * @param result 字符串值
 * @return napi_status 状态码
 */
napi_status napi_create_string_utf8(
    napi_env env,
    const char* str,
    size_t length,
    napi_value* result
);
```

**使用示例**：
```cpp
napi_value napiString;
napi_status status = napi_create_string_utf8(env, "Hello World", NAPI_AUTO_LENGTH, &napiString);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Failed to create string");
    return nullptr;
}
```

### 2. 数值转换

#### 整数类型转换

```cpp
/**
 * @brief 获取 int32 值
 * @param env N-API 环境句柄
 * @param value 数值值
 * @param result int32 结果
 * @return napi_status 状态码
 */
napi_status napi_get_value_int32(
    napi_env env,
    napi_value value,
    int32_t* result
);

/**
 * @brief 创建 int32 值
 * @param env N-API 环境句柄
 * @param value int32 值
 * @param result 数值值
 * @return napi_status 状态码
 */
napi_status napi_create_int32(
    napi_env env,
    int32_t value,
    napi_value* result
);

/**
 * @brief 获取 uint32 值
 * @param env N-API 环境句柄
 * @param value 数值值
 * @param result uint32 结果
 * @return napi_status 状态码
 */
napi_status napi_get_value_uint32(
    napi_env env,
    napi_value value,
    uint32_t* result
);

/**
 * @brief 创建 uint32 值
 * @param env N-API 环境句柄
 * @param value uint32 值
 * @param result 数值值
 * @return napi_status 状态码
 */
napi_status napi_create_uint32(
    napi_env env,
    uint32_t value,
    napi_value* result
);

/**
 * @brief 获取 int64 值
 * @param env N-API 环境句柄
 * @param value 数值值
 * @param result int64 结果
 * @return napi_status 状态码
 */
napi_status napi_get_value_int64(
    napi_env env,
    napi_value value,
    int64_t* result
);

/**
 * @brief 获取 double 值
 * @param env N-API 环境句柄
 * @param value 数值值
 * @param result double 结果
 * @return napi_status 状态码
 */
napi_status napi_get_value_double(
    napi_env env,
    napi_value value,
    double* result
);

/**
 * @brief 创建 double 值
 * @param env N-API 环境句柄
 * @param value double 值
 * @param result 数值值
 * @return napi_status 状态码
 */
napi_status napi_create_double(
    napi_env env,
    double value,
    napi_value* result
);
```

**使用示例**：
```cpp
// 获取 int32 值
int32_t intValue;
napi_status status = napi_get_value_int32(env, args[0], &intValue);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Invalid integer value");
    return nullptr;
}

// 创建 int32 值
napi_value napiResult;
napi_create_int32(env, intValue, &napiResult);
```

### 3. 布尔类型转换

```cpp
/**
 * @brief 获取布尔值
 * @param env N-API 环境句柄
 * @param value 布尔值
 * @param result 布尔结果
 * @return napi_status 状态码
 */
napi_status napi_get_value_bool(
    napi_env env,
    napi_value value,
    bool* result
);

/**
 * @brief 创建布尔值
 * @param env N-API 环境句柄
 * @param value 布尔值
 * @param result 布尔值
 * @return napi_status 状态码
 */
napi_status napi_get_boolean(
    napi_env env,
    bool value,
    napi_value* result
);
```

**使用示例**：
```cpp
// 获取布尔值
bool boolValue;
napi_status status = napi_get_value_bool(env, args[0], &boolValue);
if (status != napi_ok) {
    napi_throw_error(env, nullptr, "Invalid boolean value");
    return nullptr;
}

// 创建布尔值
napi_value napiResult;
napi_get_boolean(env, boolValue, &napiResult);
```

## 对象和数组操作

### 1. 对象操作

```cpp
/**
 * @brief 创建对象
 * @param env N-API 环境句柄
 * @param result 对象值
 * @return napi_status 状态码
 */
napi_status napi_create_object(
    napi_env env,
    napi_value* result
);

/**
 * @brief 设置对象属性
 * @param env N-API 环境句柄
 * @param object 对象
 * @param key 属性键
 * @param value 属性值
 * @return napi_status 状态码
 */
napi_status napi_set_named_property(
    napi_env env,
    napi_value object,
    const char* key,
    napi_value value
);

/**
 * @brief 获取对象属性
 * @param env N-API 环境句柄
 * @param object 对象
 * @param key 属性键
 * @param value 属性值
 * @return napi_status 状态码
 */
napi_status napi_get_named_property(
    napi_env env,
    napi_value object,
    const char* key,
    napi_value* value
);

/**
 * @brief 删除对象属性
 * @param env N-API 环境句柄
 * @param object 对象
 * @param key 属性键
 * @param result 是否成功
 * @return napi_status 状态码
 */
napi_status napi_delete_property(
    napi_env env,
    napi_value object,
    napi_value key,
    bool* result
);
```

**使用示例**：
```cpp
// 创建对象
napi_value napiObject;
napi_create_object(env, &napiObject);

// 设置属性
napi_value stringValue;
napi_create_string_utf8(env, "test", NAPI_AUTO_LENGTH, &stringValue);
napi_set_named_property(env, napiObject, "name", stringValue);

// 获取属性
napi_value getValue;
napi_get_named_property(env, napiObject, "name", &getValue);
```

### 2. 数组操作

```cpp
/**
 * @brief 创建数组
 * @param env N-API 环境句柄
 * @param length 数组长度
 * @param result 数组值
 * @return napi_status 状态码
 */
napi_status napi_create_array_with_length(
    napi_env env,
    size_t length,
    napi_value* result
);

/**
 * @brief 创建数组（推荐使用）
 * @param env N-API 环境句柄
 * @param result 数组值
 * @return napi_status 状态码
 */
napi_status napi_create_array(
    napi_env env,
    napi_value* result
);

/**
 * @brief 设置数组元素
 * @param env N-API 环境句柄
 * @param array 数组
 * @param index 索引
 * @param value 元素值
 * @return napi_status 状态码
 */
napi_status napi_set_element(
    napi_env env,
    napi_value array,
    uint32_t index,
    napi_value value
);

/**
 * @brief 获取数组元素
 * @param env N-API 环境句柄
 * @param array 数组
 * @param index 索引
 * @param value 元素值
 * @return napi_status 状态码
 */
napi_status napi_get_element(
    napi_env env,
    napi_value array,
    uint32_t index,
    napi_value* value
);

/**
 * @brief 获取数组长度
 * @param env N-API 环境句柄
 * @param array 数组
 * @param result 数组长度
 * @return napi_status 状态码
 */
napi_status napi_get_array_length(
    napi_env env,
    napi_value array,
    uint32_t* result
);
```

**使用示例**：
```cpp
// 创建数组
napi_value napiArray;
napi_create_array(env, &napiArray);

// 添加元素
napi_value element1;
napi_create_int32(env, 1, &element1);
napi_set_element(env, napiArray, 0, element1);

napi_value element2;
napi_create_int32(env, 2, &element2);
napi_set_element(env, napiArray, 1, element2);

// 获取数组长度
uint32_t arrayLength;
napi_get_array_length(env, napiArray, &arrayLength);
```

## 错误处理

### 1. 抛出异常

```cpp
/**
 * @brief 抛出错误异常
 * @param env N-API 环境句柄
 * @param code 错误码（可以为 nullptr）
 * @param msg 错误信息
 * @return napi_status 状态码
 */
napi_status napi_throw_error(
    napi_env env,
    const char* code,
    const char* msg
);

/**
 * @brief 抛出类型错误异常
 * @param env N-API 环境句柄
 * @param code 错误码（可以为 nullptr）
 * @param msg 错误信息
 * @return napi_status 状态码
 */
napi_status napi_throw_type_error(
    napi_env env,
    const char* code,
    const char* msg
);

/**
 * @brief 抛出范围错误异常
 * @param env N-API 环境句柄
 * @param code 错误码（可以为 nullptr）
 * @param msg 错误信息
 * @return napi_status 状态码
 */
napi_status napi_throw_range_error(
    napi_env env,
    const char* code,
    const char* msg
);
```

**使用示例**：
```cpp
// 简单错误抛出
napi_throw_error(env, nullptr, "Operation failed");

// 带错误码的错误抛出
napi_throw_error(env, "INVALID_ARGUMENT", "Invalid argument provided");

// 类型错误抛出
napi_throw_type_error(env, "TYPE_ERROR", "Expected string but got number");
```

### 2. 获取异常信息

```cpp
/**
 * @brief 获取异常信息
 * @param env N-API 环境句柄
 * @param result 异常信息
 * @return napi_status 状态码
 */
napi_status napi_get_and_clear_last_error(
    napi_env env,
    const napi_extended_error_info** result
);
```

### 3. 创建特殊值

```cpp
/**
 * @brief 获取 null 值
 * @param env N-API 环境句柄
 * @param result null 值
 * @return napi_status 状态码
 */
napi_status napi_get_null(
    napi_env env,
    napi_value* result
);

/**
 * @brief 获取 undefined 值
 * @param env N-API 环境句柄
 * @param result undefined 值
 * @return napi_status 状态码
 */
napi_status napi_get_undefined(
    napi_env env,
    napi_value* result
);
```

## 模块操作

### 1. 模块定义

```cpp
/**
 * @brief N-API 模块定义
 */
typedef struct {
    int nm_version;              // 版本号
    unsigned int nm_flags;       // 标志位
    const char* nm_filename;      // 文件名
    napi_module_init_func nm_register_func; // 注册函数
    const char* nm_modname;      // 模块名
    void* nm_priv;               // 私有数据
    void reserved[4];            // 保留字段
} napi_module;

/**
 * @brief N-API 模块初始化函数类型
 */
typedef napi_value (*napi_module_init_func)(napi_env env, napi_value exports);
```

**使用示例**：
```cpp
// 模块定义
static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "demo",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

// 模块注册
extern "C" __attribute__((constructor)) void RegisterDemoModule(void) {
    napi_module_register(&demoModule);
}
```

### 2. 模块初始化

```cpp
/**
 * @brief 模块初始化函数
 * @param env N-API 环境句柄
 * @param exports 导出对象
 * @return napi_value 导出对象
 */
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"function1", nullptr, Function1, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"function2", nullptr, Function2, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

## 内存管理

### 1. 内存分配

```cpp
/**
 * @brief 分配内存
 * @param size 分配大小
 * @return 分配的内存指针
 */
void* malloc(size_t size);

/**
 * @brief 释放内存
 * @param ptr 要释放的内存指针
 */
void free(void* ptr);
```

**使用示例**：
```cpp
// 分配内存
char* buffer = (char*)malloc(256);
if (buffer == NULL) {
    napi_throw_error(env, nullptr, "Memory allocation failed");
    return nullptr;
}

// 使用内存
strcpy(buffer, "Hello World");

// 释放内存
free(buffer);
```

### 2. 字符串复制

```cpp
/**
 * @brief 安全字符串复制
 * @param dest 目标字符串
 * @param src 源字符串
 * @param size 目标缓冲区大小
 * @return 目标字符串指针
 */
char* strcpy_s(char* dest, size_t size, const char* src);
```

## 实用工具函数

### 1. 工具函数模板

```cpp
// 字符串参数处理工具函数
static napi_value ProcessStringParam(napi_env env, napi_value arg)
{
    // 获取字符串长度
    napi_status status = napi_get_value_string_utf8(env, arg, NULL, 0, NULL);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get string length");
        return nullptr;
    }

    // 分配内存
    size_t strLen;
    status = napi_get_value_string_utf8(env, arg, NULL, 0, &strLen);
    char* param = (char*)malloc(strLen + 1);
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    // 获取字符串内容
    status = napi_get_value_string_utf8(env, arg, param, strLen + 1, NULL);
    if (status != napi_ok) {
        free(param);
        napi_throw_error(env, nullptr, "Failed to get string value");
        return nullptr;
    }

    // 使用参数...
    char* result = ProcessFunction(param);
    free(param);

    // 返回结果
    napi_value napiResult;
    napi_create_string_utf8(env, result, NAPI_AUTO_LENGTH, &napiResult);
    free(result);
    return napiResult;
}

// 数值参数处理工具函数
static napi_value ProcessIntParam(napi_env env, napi_value arg)
{
    int32_t value;
    napi_status status = napi_get_value_int32(env, arg, &value);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Invalid integer value");
        return nullptr;
    }

    // 调用函数
    int result = ProcessFunction(value);

    // 返回结果
    napi_value napiResult;
    napi_create_int32(env, result, &napiResult);
    return napiResult;
}

// 布尔参数处理工具函数
static napi_value ProcessBoolParam(napi_env env, napi_value arg)
{
    bool value;
    napi_status status = napi_get_value_bool(env, arg, &value);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Invalid boolean value");
        return nullptr;
    }

    // 调用函数
    bool result = ProcessFunction(value);

    // 返回结果
    napi_value napiResult;
    napi_get_boolean(env, result, &napiResult);
    return napiResult;
}
```

### 2. 错误处理工具函数

```cpp
// 简单错误处理
static napi_value SimpleErrorTest(napi_env env, napi_callback_info info)
{
    [返回类型] result = [API名称]([参数]);
    
    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }
    
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}

// 多错误码处理
static napi_value MultiErrorCodeTest(napi_env env, napi_callback_info info)
{
    [返回类型] result = [API名称]([参数]);
    
    switch (result) {
        case [错误码1]:
            napi_throw_error(env, "[错误码1]", "[错误信息1]");
            return nullptr;
        case [错误码2]:
            napi_throw_error(env, "[错误码2]", "[错误信息2]");
            return nullptr;
        case [错误码3]:
            napi_throw_error(env, "[错误码3]", "[错误信息3]");
            return nullptr;
        default:
            break;
    }
    
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

## 最佳实践

### 1. 参数验证

```cpp
// 参数验证模式
static napi_value ParamValidation(napi_env env, napi_callback_info info)
{
    size_t argc = [参数数量];
    napi_value args[argc];
    napi_status status;

    // 获取参数
    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < [最小参数数量]) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 类型检查
    for (size_t i = 0; i < argc; i++) {
        napi_valuetype valuetype;
        status = napi_typeof(env, args[i], &valuetype);
        if (status != napi_ok || valuetype != napi_[参数类型]) {
            napi_throw_error(env, nullptr, "Argument must be [参数类型]");
            return nullptr;
        }
    }

    // 继续处理...
    return nullptr;
}
```

### 2. 内存管理

```cpp
// 内存管理模式
static napi_value MemoryManagement(napi_env env, napi_callback_info info)
{
    char* param = (char*)malloc(256);
    if (param == NULL) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    // 使用参数
    strcpy(param, "[测试数据]");
    [返回类型] result = [API名称](param);
    free(param);

    if (result == [错误码]) {
        napi_throw_error(env, nullptr, "Operation failed");
        return nullptr;
    }

    // 返回结果
    napi_value napiResult;
    napi_create_[type](env, result, &napiResult);
    return napiResult;
}
```

### 3. 错误处理

```cpp
// 错误处理模式
static napi_value ErrorHandling(napi_env env, napi_callback_info info)
{
    try {
        [返回类型] result = [API名称]([参数]);
        
        if (result == [错误码1]) {
            napi_throw_error(env, "[错误码1]", "[错误信息1]");
            return nullptr;
        }
        
        napi_value napiResult;
        napi_create_[type](env, result, &napiResult);
        return napiResult;
    } catch (const std::exception& e) {
        napi_throw_error(env, nullptr, e.what());
        return nullptr;
    }
}
```

---

**版本**: 1.0.0
**创建日期**: 2026-03-10
**兼容性**: OpenHarmony API 10+