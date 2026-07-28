# Zlib 模块配置

本目录包含 Zlib 数据压缩库模块的 CAPI XTS 测试用例生成配置。

## 模块概述

- **模块名称**: Zlib
- **功能描述**: Zlib 数据压缩库，提供内存中压缩和解压缩数据的能力
- **子系统**: BundleManager
- **测试方式**: N-API 封装测试（方式2）

## 配置文件

- **_common.md**: Zlib 模块的通用配置，包含 API 列表、N-API 封装规范、测试用例模板等

## API 分类

### 核心 API

- `compress`: 单步压缩数据
- `compress2`: 单步压缩数据（可指定压缩级别）
- `compressBound`: 计算压缩后最大长度
- `uncompress`: 单步解压缩数据
- `uncompress2`: 单步解压缩数据（返回实际长度）

### Deflate 流 API

- `deflateInit`, `deflateInit2`: 初始化 deflate 流
- `deflate`: 压缩数据块
- `deflateEnd`: 结束 deflate 流
- `deflateReset`, `deflateResetKeep`: 重置 deflate 流
- `deflateParams`: 动态更新压缩参数
- `deflateTune`: 调整内部压缩参数
- `deflatePending`: 获取待处理的数据量
- `deflatePrime`: 插入位到输出流
- `deflateSetHeader`: 设置 gzip 头部信息
- `deflateSetDictionary`, `deflateGetDictionary`: 字典管理
- `deflateCopy`: 复制 deflate 流

### Inflate 流 API

- `inflateInit`, `inflateInit2`: 初始化 inflate 流
- `inflate`: 解压缩数据块
- `inflateEnd`: 结束 inflate 流
- `inflateReset`, `inflateReset2`: 重置 inflate 流
- `inflateSync`: 同步到刷新点
- `inflatePrime`: 插入位到输入流
- `inflateGetHeader`: 获取 gzip 头部信息
- `inflateSetDictionary`, `inflateGetDictionary`: 字典管理
- `inflateCopy`: 复制 inflate 流
- `inflateMark`: 标记当前流位置

### InflateBack API（回调式解压）

- `inflateBackInit`: 初始化 inflateBack 流
- `inflateBack`: 使用回调解压数据
- `inflateBackEnd`: 结束 inflateBack 流

### 校验和 API

- `crc32`, `crc32_z`: 计算 CRC-32 校验和
- `crc32_combine`, `crc32_combine_op`: 合并 CRC-32 值
- `adler32`, `adler32_z`: 计算 Adler-32 校验和
- `adler32_combine`: 合并 Adler-32 值

### 工具 API

- `zlibVersion`: 返回 zlib 版本字符串
- `zlibCompileFlags`: 返回编译时选项标志

## 测试覆盖要求

### 核心 API 测试

- ✅ 测试 `compress` 正常数据、空数据、大数据
- ✅ 测试 `compress2` 不同压缩级别（0-9、-1）
- ✅ 测试 `compressBound` 各种数据大小
- ✅ 测试 `uncompress` 正常数据、边界数据
- ✅ 测试 `crc32` 不同数据
- ✅ 测试 `adler32` 不同数据
- ✅ 测试 `zlibVersion` 返回值格式

### Deflate 流 API 测试

- ✅ 测试 `deflateInit` 不同压缩级别
- ✅ 测试 `deflate` 不同 flush 值
- ✅ 测试 `deflateEnd` 正常和未初始化情况
- ✅ 测试 `deflateReset` 正常和未初始化情况
- ✅ 测试 `deflateResetKeep` 正常情况
- ✅ 测试 `deflateParams` 动态更新参数
- ✅ 测试 `deflateBound` 各种数据大小

### Inflate 流 API 测试

- ✅ 测试 `inflateInit` 正常初始化
- ✅ 测试 `inflate` 不同 flush 值
- ✅ 测试 `inflateEnd` 正常和未初始化情况
- ✅ 测试 `inflateReset` 正常和未初始化情况

### 错误码覆盖

- ✅ 覆盖所有错误码：Z_OK, Z_STREAM_ERROR, Z_DATA_ERROR, Z_MEM_ERROR, Z_BUF_ERROR
- ✅ 测试空指针参数
- ✅ 测试无效参数值

### 返回值覆盖

- ✅ 压缩级别：覆盖 -1, 0, 1-9
- ✅ Flush 值：覆盖 0-6
- ✅ 错误码：覆盖所有错误码
- ✅ 校验和：验证计算正确性

## 参考文档

- **Zlib 官方文档**: https://zlib.net/manual.html
- **RFC 1950 (zlib format)**: https://www.rfc-editor.org/rfc/rfc1950
- **RFC 1951 (deflate format)**: https://www.rfc-editor.org/rfc/rfc1951
- **RFC 1952 (gzip format)**: https://www.rfc-editor.org/rfc/rfc1952
- **OpenHarmony Zlib 文档**: `{OH_ROOT}/docs/zh-cn/application-dev/reference/native-lib/zlib.md`
- **历史测试用例**: `{OH_ROOT}/test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/`

## N-API 封装特点

Zlib 模块的 N-API 封装具有以下特点：

1. **ArrayBuffer 处理**: 压缩/解压缩函数使用 ArrayBuffer 传输二进制数据
2. **流状态管理**: Deflate/Inflate API 需要维护流状态
3. **内存管理**: 需要手动管理 zlib 分配的内存
4. **错误码转换**: zlib 错误码需要转换为 N-API 异常

## 测试用例命名规范

```
SUB_ZLIB_[API名称]_[类型]_[序号]
```

示例：
- `SUB_ZLIB_Compress_PARAM_001`
- `SUB_ZLIB_Compress2_PARAM_001`
- `SUB_ZLIB_Uncompress_PARAM_001`
- `SUB_ZLIB_Deflate_PARAM_001`
- `SUB_ZLIB_Crc32_PARAM_001`

---

**版本**: 1.0.0
**创建日期**: 2026-03-24
**更新日期**: 2026-03-24
**兼容性**: OpenHarmony API 10+
