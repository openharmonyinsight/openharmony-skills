# ZlibCompressTest.test.ets 测试设计文档

## 接口 1: compress

### 基本信息
- **头文件**: `third_party/zlib/zlib.h`
- **函数签名**: `int compress(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen)`
- **返回值**: Z_OK (0) 成功, Z_MEM_ERROR (-4) 内存不足, Z_BUF_ERROR (-5) 输出缓冲区不够
- **错误码**: Z_OK (0), Z_MEM_ERROR (-4), Z_BUF_ERROR (-5)

### 测试用例 1: SUB_ZLIB_Compress_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_Compress_PARAM_001 |
| 用例名 | compress正常数据压缩 |
| N-API 函数名 | compressNormalData |
| 预置条件 | 准备有效字符串数据的 ArrayBuffer |
| 测试步骤 | 1. 将字符串 "Hello, zlib!" 编码为 ArrayBuffer<br>2. 调用 testNapi.compressNormalData(arrayBuffer)<br>3. 获取返回的压缩后 ArrayBuffer |
| 预期结果 | 返回的 ArrayBuffer 长度 > 0 且 < 原始数据长度 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 2: SUB_ZLIB_Compress_PARAM_002

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_Compress_PARAM_002 |
| 用例名 | compress空数据压缩 |
| N-API 函数名 | compressEmptyData |
| 预置条件 | 准备空 ArrayBuffer (长度为0) |
| 测试步骤 | 1. 创建空 ArrayBuffer<br>2. 调用 testNapi.compressEmptyData(emptyBuffer)<br>3. 获取返回值 |
| 预期结果 | 返回 Z_OK (0)，压缩后数据长度 <= compressBound(0) |
| 场景 | 边界场景 |
| 类型 | PARAM |
| 级别 | P1 |
| 依赖关系 | 无 |

### 测试用例 3: SUB_ZLIB_Compress_ERROR_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_Compress_ERROR_001 |
| 用例名 | compress输出缓冲区不足 |
| N-API 函数名 | compressBufError |
| 预置条件 | 准备有效数据和极小的输出缓冲区 |
| 测试步骤 | 1. 创建较大数据 ArrayBuffer<br>2. 调用 testNapi.compressBufError(arrayBuffer)，内部设置极小输出缓冲区<br>3. 捕获异常 |
| 预期结果 | C API 返回 Z_BUF_ERROR (-5)，N-API 层抛出异常 |
| 场景 | 异常场景 |
| 类型 | ERROR |
| 级别 | P2 |
| 依赖关系 | 无 |

---

## 接口 2: uncompress

### 基本信息
- **头文件**: `third_party/zlib/zlib.h`
- **函数签名**: `int uncompress(Bytef *dest, uLongf *destLen, const Bytef *source, uLong sourceLen)`
- **返回值**: Z_OK (0) 成功, Z_MEM_ERROR (-4) 内存不足, Z_BUF_ERROR (-5) 输出缓冲区不够, Z_DATA_ERROR (-3) 数据损坏
- **错误码**: Z_OK (0), Z_MEM_ERROR (-4), Z_BUF_ERROR (-5), Z_DATA_ERROR (-3)

### 测试用例 4: SUB_ZLIB_Uncompress_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_Uncompress_PARAM_001 |
| 用例名 | uncompress正常数据解压完整往返 |
| N-API 函数名 | uncompressRoundTrip |
| 预置条件 | 准备原始数据并先通过 compress 压缩 |
| 测试步骤 | 1. 编码字符串为 ArrayBuffer<br>2. 调用 testNapi.compressNormalData(arrayBuffer) 获取压缩数据<br>3. 调用 testNapi.uncompressRoundTrip(compressedBuffer, originalLength)<br>4. 逐字节比较解压后数据与原始数据 |
| 预期结果 | 解压后数据长度 == 原始数据长度，且每个字节完全一致 |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 依赖 compress 函数 |

### 测试用例 5: SUB_ZLIB_Uncompress_ERROR_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_Uncompress_ERROR_001 |
| 用例名 | uncompress损坏数据解压 |
| N-API 函数名 | uncompressCorruptData |
| 预置条件 | 准备一段随机损坏的压缩数据 |
| 测试步骤 | 1. 创建包含随机字节的 ArrayBuffer<br>2. 调用 testNapi.uncompressCorruptData(corruptBuffer, 1024)<br>3. 捕获异常 |
| 预期结果 | C API 返回 Z_DATA_ERROR (-3)，N-API 层抛出异常 |
| 场景 | 异常场景 |
| 类型 | ERROR |
| 级别 | P2 |
| 依赖关系 | 无 |

---

## 接口 3: compressBound

### 基本信息
- **头文件**: `third_party/zlib/zlib.h`
- **函数签名**: `uLong compressBound(uLong sourceLen)`
- **返回值**: 压缩后数据的最大可能长度 (uLong)
- **错误码**: 无错误码，始终成功

### 测试用例 6: SUB_ZLIB_CompressBound_RETURN_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_CompressBound_RETURN_001 |
| 用例名 | compressBound正常数据大小 |
| N-API 函数名 | compressBoundNormalSize |
| 预置条件 | 准备有效数据大小值 |
| 测试步骤 | 1. 调用 testNapi.compressBoundNormalSize(100)<br>2. 获取返回值 bound |
| 预期结果 | bound > 100 且 bound >= sourceLen (返回值不小于输入值) |
| 场景 | 正常场景 |
| 类型 | RETURN |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 7: SUB_ZLIB_CompressBound_BOUNDARY_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ZLIB_CompressBound_BOUNDARY_001 |
| 用例名 | compressBound零长度 |
| N-API 函数名 | compressBoundZeroLength |
| 预置条件 | 无 |
| 测试步骤 | 1. 调用 testNapi.compressBoundZeroLength()<br>2. 获取返回值 bound |
| 预期结果 | bound > 0 (即使源长度为 0，返回值也大于 0，因为压缩有头部开销) |
| 场景 | 边界场景 |
| 类型 | BOUNDARY |
| 级别 | P1 |
| 依赖关系 | 无 |

---

## 覆盖率统计

| API | PARAM | ERROR | RETURN | BOUNDARY | 合计 |
|-----|-------|-------|--------|----------|------|
| compress | 2 | 1 | 0 | 0 | 3 |
| uncompress | 1 | 1 | 0 | 0 | 2 |
| compressBound | 0 | 0 | 1 | 1 | 2 |
| **合计** | **3** | **2** | **1** | **1** | **7** |
