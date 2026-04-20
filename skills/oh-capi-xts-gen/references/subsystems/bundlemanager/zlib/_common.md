# Zlib 模块 CAPI 配置

## 一、模块基础信息

- **模块名称**: Zlib
- **模块描述**: Zlib 数据压缩库
- **子系统**: BundleManager
- **API 语言**: C（通过 N-API 封装供 ETS/ArkTS 测试）
- **测试路径**: `test/xts/acts/bundlemanager/zlib/`

## 二、模块功能概述

Zlib 是一个通用的数据压缩库，提供内存中压缩和解压缩数据的能力。

### 2.1 支持的压缩算法

- **Deflate 算法**: 唯一支持的压缩方法
- **压缩级别**: 0-9（0=无压缩，1=最快，9=最高压缩，-1=默认）
- **压缩策略**:
  - Z_DEFAULT_STRATEGY (0): 默认策略
  - Z_FILTERED (1): 过滤后数据
  - Z_HUFFMAN_ONLY (2): 仅 Huffman 编码
  - Z_RLE (3): RLE 编码
  - Z_FIXED (4): 固定代码

### 2.2 支持的数据格式

- **zlib 格式**: 默认格式（RFC 1950）
- **gzip 格式**: 文件压缩格式（RFC 1952）
- **raw deflate**: 无头部和尾部

### 2.3 Flush 参数

- Z_NO_FLUSH (0): 不刷新
- Z_PARTIAL_FLUSH (1): 部分刷新
- Z_SYNC_FLUSH (2): 同步刷新
- Z_FULL_FLUSH (3): 完全刷新
- Z_FINISH (4): 完成压缩/解压缩
- Z_BLOCK (5): 块刷新
- Z_TREES (6): 树刷新

## 三、头文件路径

### 3.1 主要头文件

```c
#include "zlib.h"
#include "napi/native_api.h"
```

### 3.2 头文件位置（相对于 {OH_ROOT}/interface/sdk_c）

```
{OH_ROOT}/interface/sdk_c/third_party/zlib/zlib.h
```

### 3.3 头文件依赖

```
zlib.h 依赖于:
- zconf.h: 平台相关配置
```

## 四、API 列表

### 4.1 核心压缩/解压缩 API

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `compress` | 单步压缩数据 | int | zlib.h |
| `compress2` | 单步压缩数据（可指定压缩级别） | int | zlib.h |
| `compressBound` | 计算压缩后最大长度 | uLong | zlib.h |
| `uncompress` | 单步解压缩数据 | int | zlib.h |
| `uncompress2` | 单步解压缩数据（返回实际长度） | int | zlib.h |

### 4.2 Deflate 流 API

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `deflateInit` | 初始化 deflate 流 | int | zlib.h |
| `deflateInit2` | 初始化 deflate 流（可自定义） | int | zlib.h |
| `deflate` | 压缩数据块 | int | zlib.h |
| `deflateEnd` | 结束 deflate 流 | int | zlib.h |
| `deflateReset` | 重置 deflate 流 | int | zlib.h |
| `deflateResetKeep` | 重置 deflate 流（保留压缩参数） | int | zlib.h |
| `deflateParams` | 动态更新压缩参数 | int | zlib.h |
| `deflateTune` | 调整内部压缩参数 | int | zlib.h |
| `deflateBound` | 计算压缩后最大长度 | uLong | zlib.h |
| `deflatePending` | 获取待处理的数据量 | int | zlib.h |
| `deflatePrime` | 插入位到输出流 | int | zlib.h |
| `deflateSetHeader` | 设置 gzip 头部信息 | int | zlib.h |
| `deflateSetDictionary` | 设置预计算字典 | int | zlib.h |
| `deflateGetDictionary` | 获取字典 | int | zlib.h |
| `deflateCopy` | 复制 deflate 流 | int | zlib.h |

### 4.3 Inflate 流 API

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `inflateInit` | 初始化 inflate 流 | int | zlib.h |
| `inflateInit2` | 初始化 inflate 流（可自定义） | int | zlib.h |
| `inflate` | 解压缩数据块 | int | zlib.h |
| `inflateEnd` | 结束 inflate 流 | int | zlib.h |
| `inflateReset` | 重置 inflate 流 | int | zlib.h |
| `inflateReset2` | 重置 inflate 流（可更改窗口） | int | zlib.h |
| `inflateSync` | 同步到刷新点 | int | zlib.h |
| `inflatePrime` | 插入位到输入流 | int | zlib.h |
| `inflateGetHeader` | 获取 gzip 头部信息 | int | zlib.h |
| `inflateSetDictionary` | 设置字典 | int | zlib.h |
| `inflateGetDictionary` | 获取字典 | int | zlib.h |
| `inflateCopy` | 复制 inflate 流 | int | zlib.h |
| `inflateMark` | 标记当前流位置 | long | zlib.h |

### 4.4 InflateBack API（回调式解压）

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `inflateBackInit` | 初始化 inflateBack 流 | int | zlib.h |
| `inflateBack` | 使用回调解压数据 | int | zlib.h |
| `inflateBackEnd` | 结束 inflateBack 流 | int | zlib.h |

### 4.5 校验和 API

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `crc32` | 计算 CRC-32 校验和 | uLong | zlib.h |
| `crc32_z` | 计算 CRC-32 校验和（支持大缓冲区） | uLong | zlib.h |
| `crc32_combine` | 合并两个 CRC-32 值 | uLong | zlib.h |
| `crc32_combine_op` | 合并两个 CRC-32 值（带操作） | uLong | zlib.h |
| `adler32` | 计算 Adler-32 校验和 | uLong | zlib.h |
| `adler32_z` | 计算 Adler-32 校验和（支持大缓冲区） | uLong | zlib.h |
| `adler32_combine` | 合并两个 Adler-32 值 | uLong | zlib.h |

### 4.6 工具 API

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `zlibVersion` | 返回 zlib 版本字符串 | const char* | zlib.h |
| `zlibCompileFlags` | 返回编译时选项标志 | uLong | zlib.h |

### 4.7 Gzip 文件 API（不常用，可省略）

| 函数名 | 功能 | 返回值 | 头文件 |
|--------|------|--------|--------|
| `gzopen` | 打开 gzip 文件 | gzFile | zlib.h |
| `gzdopen` | 从文件描述符打开 gzip | gzFile | zlib.h |
| `gzclose` | 关闭 gzip 文件 | int | zlib.h |
| `gzread` | 从 gzip 文件读取 | int | zlib.h |
| `gzwrite` | 写入 gzip 文件 | int | zlib.h |
| `gzprintf` | 格式化写入 gzip 文件 | int | zlib.h |
| `gzseek` | 定位到指定位置 | z_off_t | zlib.h |
| `gztell` | 获取当前位置 | z_off_t | zlib.h |
| `gzflush` | 刷新 gzip 文件 | int | zlib.h |

## 五、错误码枚举

| 错误码 | 值 | 说明 |
|--------|------|------|
| `Z_OK` | 0 | 成功 |
| `Z_STREAM_END` | 1 | 流结束 |
| `Z_NEED_DICT` | 2 | 需要字典 |
| `Z_ERRNO` | -1 | 系统错误 |
| `Z_STREAM_ERROR` | -2 | 流状态错误 |
| `Z_DATA_ERROR` | -3 | 数据错误 |
| `Z_MEM_ERROR` | -4 | 内存错误 |
| `Z_BUF_ERROR` | -5 | 缓冲区错误 |
| `Z_VERSION_ERROR` | -6 | 版本错误 |

## 六、N-API 封装规范

### 6.1 数据类型转换

#### ArrayBuffer 处理

```cpp
// 辅助函数：获取 ArrayBuffer 数据
static bool GetArrayBufferData(napi_env env, napi_value arrayBuffer, void** data, size_t* byteLength)
{
    void* bufferData = nullptr;
    napi_status status = napi_get_arraybuffer_info(env, arrayBuffer, &bufferData, byteLength);
    if (status != napi_ok || bufferData == nullptr) {
        return false;
    }

    *data = bufferData;
    return true;
}

// 辅助函数：创建 ArrayBuffer 副本
static napi_value CreateArrayBufferCopy(napi_env env, void* data, size_t length)
{
    napi_value result;
    void* buffer = nullptr;
    napi_status status = napi_create_arraybuffer(env, length, &buffer, &result);
    if (status != napi_ok || buffer == nullptr) {
        return nullptr;
    }
    memcpy(buffer, data, length);
    return result;
}
```

#### 字符串处理

```cpp
// 从 ArrayBuffer 创建字符串（用于文本数据）
static napi_value ArrayBufferToString(napi_env env, napi_value arrayBuffer)
{
    void* data = nullptr;
    size_t length = 0;
    if (!GetArrayBufferData(env, arrayBuffer, &data, &length)) {
        return nullptr;
    }

    napi_value result;
    napi_create_string_utf8(env, (const char*)data, length, &result);
    return result;
}
```

### 6.2 压缩函数封装模板

#### compress 函数封装

```cpp
/**
 * @tc.name: SUB_ZLIB_Compress_PARAM_001
 * @tc.desc: 测试 compress 函数，正常数据压缩
 * @tc.type: FUNC
 */
static napi_value Compress_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected ArrayBuffer.");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_object) {
        napi_throw_error(env, nullptr, "Argument must be an ArrayBuffer");
        return nullptr;
    }

    bool isArrayBuffer;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "Argument must be an ArrayBuffer");
        return nullptr;
    }

    void* sourceData = nullptr;
    size_t sourceLen = 0;
    if (!GetArrayBufferData(env, args[0], &sourceData, &sourceLen)) {
        napi_throw_error(env, nullptr, "Failed to get source buffer data");
        return nullptr;
    }

    uLong compressedLen = compressBound(sourceLen);
    Bytef* compressed = (Bytef*)malloc(compressedLen);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed for compressed data");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef*)sourceData, sourceLen);

    napi_value result;
    if (ret == Z_OK) {
        result = CreateArrayBufferCopy(env, compressed, compressedLen);
    } else {
        napi_value error = CreateError(env, ret, "Compression failed");
        napi_throw(env, error);
        result = nullptr;
    }

    free(compressed);
    return result;
}
```

#### compress2 函数封装

```cpp
/**
 * @tc.name: SUB_ZLIB_Compress2_PARAM_001
 * @tc.desc: 测试 compress2 函数，带压缩级别的数据压缩
 * @tc.type: FUNC
 */
static napi_value Compress2_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected (ArrayBuffer, level).");
        return nullptr;
    }

    // 验证第一个参数为 ArrayBuffer
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_object) {
        napi_throw_error(env, nullptr, "First argument must be an ArrayBuffer");
        return nullptr;
    }

    bool isArrayBuffer;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "First argument must be an ArrayBuffer");
        return nullptr;
    }

    // 验证第二个参数为数字
    status = napi_typeof(env, args[1], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Second argument must be a number (compression level)");
        return nullptr;
    }

    int32_t level;
    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get compression level");
        return nullptr;
    }

    // 验证压缩级别
    if (!CheckCompressLevel(level)) {
        napi_throw_error(env, nullptr, "Invalid compression level. Must be -1 or between 0 and 9.");
        return nullptr;
    }

    void* sourceData = nullptr;
    size_t sourceLen = 0;
    if (!GetArrayBufferData(env, args[0], &sourceData, &sourceLen)) {
        napi_throw_error(env, nullptr, "Failed to get source buffer data");
        return nullptr;
    }

    uLong compressedLen = compressBound(sourceLen);
    Bytef* compressed = (Bytef*)malloc(compressedLen);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = compress2(compressed, &compressedLen, (const Bytef*)sourceData, sourceLen, level);

    napi_value result;
    if (ret == Z_OK) {
        result = CreateArrayBufferCopy(env, compressed, compressedLen);
    } else {
        napi_value error = CreateError(env, ret, "Compression failed");
        napi_throw(env, error);
        result = nullptr;
    }

    free(compressed);
    return result;
}
```

### 6.3 Deflate 流函数封装模板

#### deflateInit 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_DeflateInit_PARAM_001
 * @tc.desc: 测试 deflateInit 函数，初始化 deflate 流
 * @tc.type: FUNC
 */
static napi_value DeflateInit_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected compression level (number).");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument must be a number");
        return nullptr;
    }

    int32_t level;
    status = napi_get_value_int32(env, args[0], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get compression level");
        return nullptr;
    }

    if (!CheckCompressLevel(level)) {
        napi_throw_error(env, nullptr, "Invalid compression level");
        return nullptr;
    }

    // 分配 deflate 流
    z_streamp strm = (z_streamp)malloc(sizeof(z_stream));
    if (strm == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate deflate stream");
        return nullptr;
    }

    // 初始化 deflate 流
    memset(strm, 0, sizeof(z_stream));
    int ret = deflateInit(strm, level);

    napi_value result;
    napi_create_int32(env, ret, &result);

    if (ret != Z_OK) {
        free(strm);
    }

    return result;
}
```

#### deflate 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_Deflate_PARAM_001
 * @tc.desc: 测试 deflate 函数，压缩数据块
 * @tc.type: FUNC
 */
static napi_value Deflate_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected (ArrayBuffer, flush).");
        return nullptr;
    }

    // 验证第一个参数为 ArrayBuffer
    void* sourceData = nullptr;
    size_t sourceLen = 0;
    if (!GetArrayBufferData(env, args[0], &sourceData, &sourceLen)) {
        napi_throw_error(env, nullptr, "Failed to get source buffer data");
        return nullptr;
    }

    // 验证第二个参数为 flush 值
    napi_valuetype valuetype;
    status = napi_typeof(env, args[1], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Second argument must be a number (flush value)");
        return nullptr;
    }

    int32_t flush;
    status = napi_get_value_int32(env, args[1], &flush);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get flush value");
        return nullptr;
    }

    // 验证 flush 值
    if (flush < Z_NO_FLUSH || flush > Z_TREES) {
        napi_throw_error(env, nullptr, "Invalid flush value");
        return nullptr;
    }

    // 准备输出缓冲区
    uLong compressedLen = compressBound(sourceLen);
    Bytef* compressed = (Bytef*)malloc(compressedLen);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    // 设置 deflate 流（使用全局流）
    global_strm->next_in = (const Bytef*)sourceData;
    global_strm->avail_in = sourceLen;
    global_strm->next_out = compressed;
    global_strm->avail_out = compressedLen;

    // 调用 deflate
    int ret = deflate(global_strm, flush);

    napi_value result;
    if (ret >= 0) {
        // 返回压缩后的 ArrayBuffer
        size_t actualLen = compressedLen - global_strm->avail_out;
        result = CreateArrayBufferCopy(env, compressed, actualLen);
    } else {
        napi_value error = CreateError(env, ret, "Deflate failed");
        napi_throw(env, error);
        result = nullptr;
    }

    free(compressed);
    return result;
}
```

### 6.4 Inflate 流函数封装模板

#### inflateInit 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_InflateInit_PARAM_001
 * @tc.desc: 测试 inflateInit 函数，初始化 inflate 流
 * @tc.type: FUNC
 */
static napi_value InflateInit_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_status status = napi_get_cb_info(env, info, &argc, nullptr, nullptr, nullptr);

    // 分配 inflate 流
    z_streamp strm = (z_streamp)malloc(sizeof(z_stream));
    if (strm == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate inflate stream");
        return nullptr;
    }

    // 初始化 inflate 流
    memset(strm, 0, sizeof(z_stream));
    int ret = inflateInit(strm);

    napi_value result;
    napi_create_int32(env, ret, &result);

    if (ret != Z_OK) {
        free(strm);
    }

    return result;
}
```

### 6.5 校验和函数封装模板

#### crc32 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_Crc32_PARAM_001
 * @tc.desc: 测试 crc32 函数，计算 CRC-32 校验和
 * @tc.type: FUNC
 */
static napi_value Crc32_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected (crc, ArrayBuffer).");
        return nullptr;
    }

    // 获取 crc 参数
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "First argument must be a number (crc value)");
        return nullptr;
    }

    uint32_t crc;
    status = napi_get_value_uint32(env, args[0], &crc);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get crc value");
        return nullptr;
    }

    // 获取 ArrayBuffer
    void* data = nullptr;
    size_t len = 0;
    if (!GetArrayBufferData(env, args[1], &data, &len)) {
        napi_throw_error(env, nullptr, "Failed to get buffer data");
        return nullptr;
    }

    // 计算 CRC-32
    uLong resultCrc = crc32(crc, (const Bytef*)data, len);

    // 返回结果
    napi_value result;
    napi_create_uint32(env, resultCrc, &result);
    return result;
}
```

#### adler32 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_Adler32_PARAM_001
 * @tc.desc: 测试 adler32 函数，计算 Adler-32 校验和
 * @tc.type: FUNC
 */
static napi_value Adler32_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected (adler, ArrayBuffer).");
        return nullptr;
    }

    // 获取 adler 参数
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "First argument must be a number (adler value)");
        return nullptr;
    }

    uint32_t adler;
    status = napi_get_value_uint32(env, args[0], &adler);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get adler value");
        return nullptr;
    }

    // 获取 ArrayBuffer
    void* data = nullptr;
    size_t len = 0;
    if (!GetArrayBufferData(env, args[1], &data, &len)) {
        napi_throw_error(env, nullptr, "Failed to get buffer data");
        return nullptr;
    }

    // 计算 Adler-32
    uLong resultAdler = adler32(adler, (const Bytef*)data, len);

    // 返回结果
    napi_value result;
    napi_create_uint32(env, resultAdler, &result);
    return result;
}
```

### 6.6 工具函数封装模板

#### zlibVersion 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_ZlibVersion_RETURN_001
 * @tc.desc: 测试 zlibVersion 函数，返回 zlib 版本字符串
 * @tc.type: FUNC
 */
static napi_value ZlibVersion_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 0;
    napi_status status = napi_get_cb_info(env, info, &argc, nullptr, nullptr, nullptr);

    const char* version = zlibVersion();
    if (version == nullptr) {
        napi_throw_error(env, nullptr, "Failed to get zlib version");
        return nullptr;
    }

    napi_value result;
    napi_create_string_utf8(env, version, strlen(version), &result);
    return result;
}
```

#### compressBound 封装

```cpp
/**
 * @tc.name: SUB_ZLIB_CompressBound_PARAM_001
 * @tc.desc: 测试 compressBound 函数，计算压缩后最大长度
 * @tc.type: FUNC
 */
static napi_value CompressBound_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected source length (number).");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument must be a number");
        return nullptr;
    }

    int64_t sourceLen;
    status = napi_get_value_int64(env, args[0], &sourceLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get source length");
        return nullptr;
    }

    uLong bound = compressBound(sourceLen);

    napi_value result;
    napi_create_uint32(env, bound, &result);
    return result;
}
```

## 七、ETS/ArkTS 测试用例模板

### 7.1 压缩测试模板

```typescript
/**
 * @tc.name: SUB_ZLIB_Compress_PARAM_001
 * @tc.desc: 测试 compress 函数，正常数据压缩
 * @tc.type: FUNC
 */
it('Compress_NormalData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================Compress_NormalData start==================");
    try {
        // 准备测试数据
        const testData: string = "Hello, zlib! This is a test string for compress.";
        const textEncoder: util.TextEncoder = new util.TextEncoder();
        const arrayBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;

        // 调用 N-API 函数
        const compressed: ArrayBuffer = testNapi.compress(arrayBuffer);

        // 验证结果
        expect(compressed.byteLength).assertLarger(0);
        expect(compressed.byteLength).assertLess(arrayBuffer.byteLength);

        hilog.info(domain, tag, `Compressed size: ${compressed.byteLength}, Original size: ${arrayBuffer.byteLength}`);
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `Compress_NormalData error: errCode:${code} message:${errMsg}`);
        expect.fail(`Test should not throw error but got: ${errMsg}`);
    }
    done();
    hilog.info(domain, tag, "==================Compress_NormalData end==================");
});
```

### 7.2 解压缩测试模板

```typescript
/**
 * @tc.name: SUB_ZLIB_Uncompress_PARAM_001
 * @tc.desc: 测试 uncompress 函数，正常数据解压缩
 * @tc.type: FUNC
 */
it('Uncompress_NormalData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================Uncompress_NormalData start==================");
    try {
        // 准备原始数据
        const originalData: string = "Hello, zlib! This is a test string for uncompress.";
        const textEncoder: util.TextEncoder = new util.TextEncoder();
        const originalBuffer: ArrayBuffer = textEncoder.encodeInto(originalData).buffer;

        // 压缩数据
        const compressed: ArrayBuffer = testNapi.compress(originalBuffer);

        // 解压缩数据
        const decompressed: ArrayBuffer = testNapi.uncompress(compressed, originalBuffer.byteLength);

        // 验证结果
        expect(decompressed.byteLength).assertEqual(originalBuffer.byteLength);

        // 比较数据内容
        const decompressedArray: Uint8Array = new Uint8Array(decompressed);
        const originalArray: Uint8Array = new Uint8Array(originalBuffer);
        for (let i = 0; i < decompressedArray.length; i++) {
            expect(decompressedArray[i]).assertEqual(originalArray[i]);
        }

        hilog.info(domain, tag, `Decompressed size: ${decompressed.byteLength}`);
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `Uncompress_NormalData error: errCode:${code} message:${errMsg}`);
        expect.fail(`Test should not throw error but got: ${errMsg}`);
    }
    done();
    hilog.info(domain, tag, "==================Uncompress_NormalData end==================");
});
```

### 7.3 Deflate 流测试模板

```typescript
/**
 * @tc.name: SUB_ZLIB_Deflate_PARAM_001
 * @tc.desc: 测试 deflate 函数，压缩数据块
 * @tc.type: FUNC
 */
it('Deflate_DataBlock', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================Deflate_DataBlock start==================");
    try {
        // 准备测试数据
        const testData: string = "Hello, zlib! This is a test string for deflate.";
        const textEncoder: util.TextEncoder = new util.TextEncoder();
        const arrayBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;
        const level: number = 6;

        // 初始化 deflate 流
        const initResult: number = testNapi.deflateInit(level);
        expect(initResult).assertEqual(0);

        // 压缩数据
        const compressed: ArrayBuffer = testNapi.deflate(arrayBuffer, Z_FINISH);

        // 验证结果
        expect(compressed.byteLength).assertLarger(0);
        expect(compressed.byteLength).assertLess(arrayBuffer.byteLength);

        // 结束 deflate 流
        const endResult: number = testNapi.deflateEnd();
        expect(endResult).assertEqual(0);

        hilog.info(domain, tag, `Deflate compressed size: ${compressed.byteLength}`);
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `Deflate_DataBlock error: errCode:${code} message:${errMsg}`);
        expect.fail(`Test should not throw error but got: ${errMsg}`);
    }
    done();
    hilog.info(domain, tag, "==================Deflate_DataBlock end==================");
});
```

### 7.4 校验和测试模板

```typescript
/**
 * @tc.name: SUB_ZLIB_Crc32_PARAM_001
 * @tc.desc: 测试 crc32 函数，计算 CRC-32 校验和
 * @tc.type: FUNC
 */
it('Crc32_NormalData', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0, async (done: Function) => {
    hilog.info(domain, tag, "==================Crc32_NormalData start==================");
    try {
        // 准备测试数据
        const testData: string = "Hello, zlib! This is a test string for crc32.";
        const textEncoder: util.TextEncoder = new util.TextEncoder();
        const arrayBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;

        // 计算 CRC-32
        const crc: number = testNapi.crc32(0, arrayBuffer);

        // 验证结果
        expect(crc).assertLarger(0);

        hilog.info(domain, tag, `CRC-32 value: ${crc}`);
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `Crc32_NormalData error: errCode:${code} message:${errMsg}`);
        expect.fail(`Test should not throw error but got: ${errMsg}`);
    }
    done();
    hilog.info(domain, tag, "==================Crc32_NormalData end==================");
});
```

### 7.5 错误码测试模板

```typescript
/**
 * @tc.name: SUB_ZLIB_Compress2_ERROR_001
 * @tc.desc: 测试 compress2 函数，无效压缩级别
 * @tc.type: FUNC
 */
it('Compress2_InvalidLevel', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL2, async (done: Function) => {
    hilog.info(domain, tag, "==================Compress2_InvalidLevel start==================");
    try {
        // 准备测试数据
        const testData: string = "Hello, zlib!";
        const textEncoder: util.TextEncoder = new util.TextEncoder();
        const arrayBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;

        // 使用无效的压缩级别
        const invalidLevel: number = 999;
        const result: number = testNapi.compress2InvalidLevel(arrayBuffer, invalidLevel);

        // 验证返回错误码
        expect(result).assertEqual(-2); // Z_STREAM_ERROR

        hilog.info(domain, tag, `Compress2 invalid level result: ${result}`);
    } catch (err) {
        let errMsg = (err as BusinessError).message;
        let code = (err as BusinessError).code;
        hilog.error(domain, tag, `Compress2_InvalidLevel error: errCode:${code} message:${errMsg}`);
        expect.fail(`Test should not throw error but got: ${errMsg}`);
    }
    done();
    hilog.info(domain, tag, "==================Compress2_InvalidLevel end==================");
});
```

## 八、测试覆盖要求

### 8.1 核心 API 测试

- ✅ 测试 `compress` 正常数据、空数据、大数据
- ✅ 测试 `compress2` 不同压缩级别（0-9、-1）
- ✅ 测试 `compressBound` 各种数据大小
- ✅ 测试 `uncompress` 正常数据、边界数据
- ✅ 测试 `crc32` 不同数据
- ✅ 测试 `adler32` 不同数据
- ✅ 测试 `zlibVersion` 返回值格式

### 8.2 Deflate 流 API 测试

- ✅ 测试 `deflateInit` 不同压缩级别
- ✅ 测试 `deflate` 不同 flush 值
- ✅ 测试 `deflateEnd` 正常和未初始化情况
- ✅ 测试 `deflateReset` 正常和未初始化情况
- ✅ 测试 `deflateResetKeep` 正常情况
- ✅ 测试 `deflateParams` 动态更新参数
- ✅ 测试 `deflateBound` 各种数据大小

### 8.3 Inflate 流 API 测试

- ✅ 测试 `inflateInit` 正常初始化
- ✅ 测试 `inflate` 不同 flush 值
- ✅ 测试 `inflateEnd` 正常和未初始化情况
- ✅ 测试 `inflateReset` 正常和未初始化情况

### 8.4 错误码覆盖

- ✅ 覆盖所有错误码：Z_OK, Z_STREAM_ERROR, Z_DATA_ERROR, Z_MEM_ERROR, Z_BUF_ERROR
- ✅ 测试空指针参数
- ✅ 测试无效参数值

### 8.5 返回值覆盖

- ✅ 压缩级别：覆盖 -1, 0, 1-9
- ✅ Flush 值：覆盖 0-6
- ✅ 错误码：覆盖所有错误码
- ✅ 校验和：验证计算正确性

## 九、参考文档

### 9.1 Zlib 官方文档

- **Zlib 官方文档**: https://zlib.net/manual.html
- **RFC 1950 (zlib format)**: https://www.rfc-editor.org/rfc/rfc1950
- **RFC 1951 (deflate format)**: https://www.rfc-editor.org/rfc/rfc1951
- **RFC 1952 (gzip format)**: https://www.rfc-editor.org/rfc/rfc1952

### 9.2 OpenHarmony 文档

- **Zlib C API 参考**: `{OH_ROOT}/docs/zh-cn/application-dev/reference/native-lib/zlib.md`
- **错误码参考**: `{OH_ROOT}/docs/zh-cn/application-dev/reference/apis-basic-services-kit/errorcode-zlib.md`
- **N-API 开发指南**: `{OH_ROOT}/docs/zh-cn/application-dev/napi/ndk-development-overview.md`

### 9.3 历史测试用例参考

- **参考测试套**: `{OH_ROOT}/test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/`
- **N-API 封装**: `entry/src/main/cpp/NapiTest.cpp`
- **ETS 测试**: `entry/src/ohosTest/ets/test/*.test.ets`

## 十、测试用例命名规范

### 10.1 测试用例编号格式

```
SUB_ZLIB_[API名称]_[类型]_[序号]
```

### 10.2 编号示例

```
SUB_ZLIB_Compress_PARAM_001
SUB_ZLIB_Compress2_PARAM_001
SUB_ZLIB_Uncompress_PARAM_001
SUB_ZLIB_Deflate_PARAM_001
SUB_ZLIB_Crc32_PARAM_001
SUB_ZLIB_Adler32_PARAM_001
```

### 10.3 ETS 测试用例名称

```
格式：[API名]_[场景描述]
示例：Compress_NormalData, Compress2_DifferentLevels, Uncompress_RoundTrip
```

## 十一、配置文件更新要求

> 📋 **通用校验流程参考**：[modules/L2_Generation/verification_common.md](../../../../modules/L2_Generation/verification_common.md)
>
> 本节仅提供 Zlib 模块特有的配置要求，通用校验流程请查看上述链接。

### 11.1 syscap.json 更新要求

> ⚠️ **重要：新增 Zlib 模块测试用例时，必须更新 syscap.json！
>
> 在 `entry/src/main/syscap.json` 中添加 Zlib 系统能力声明。

#### Zlib 系统能力标识

```json
{
    "devices": {
        "general": [],
        "custom": [
            {
                "xts": [
                    "SystemCapability.BundleManager.Zlib"
                ]
            }
        ]
    }
}
```

#### 验证命令

```bash
# 检查 syscap.json 是否包含 Zlib 系统能力
grep "SystemCapability.BundleManager.Zlib" entry/src/main/syscap.json
```

### 11.2 hap 包名对应要求

> ⚠️ **重要：BUILD.gn 和 Test.json 中的 hap 包名必须对应！
>
> 详细的 hap 包名对应校验请参考 [通用校验模块](../../../../modules/L2_Generation/verification_common.md#232-配置文件参数检查)

#### Zlib 测试套命名示例

| 配置文件 | 字段 | Zlib 测试套示例 |
|---------|------|-------------------|
| BUILD.gn | `hap_name` | `ActsZlibCapiApiTest` |
| Test.json | `test-file-name` | `ActsZlibCapiApiTest.hap` |
| Test.json | `bundle-name` | `com.acts.zlib.napitest` |

### 11.3 三步同步校验要求

> 📋 **详细校验流程**：[通用校验模块 - 三重Napi校验](../../../../modules/L2_Generation/verification_common.md#一三重napi校验)

新增 Zlib 模块测试用例完成后，必须执行三步同步校验：

1. **N-API 函数注册**：确保所有 Zlib N-API 封装函数都在 `Init` 函数中注册
2. **TypeScript 接口声明**：确保所有函数都在 `types/libentry/index.d.ts` 中声明
3. **ETS 测试接口使用**：确保 ETS 测试中使用的接口都有对应的 N-API 实现

### 11.4 编译前工程结构校验

> 📋 **详细校验流程**：[通用校验模块 - 编译前工程结构校验](../../../../modules/L2_Generation/verification_common.md#二编译前工程结构校验)

编译前必须执行工程结构校验，确保：
- 所有必需文件存在
- 配置参数正确
- hap 包名对应

---

**版本**: 1.3.0
**创建日期**: 2026-03-24
**更新日期**: 2026-03-24
**兼容性**: OpenHarmony API 10+
**基于测试用例**: ActsZlibCapiApiTest (N-API 封装）
