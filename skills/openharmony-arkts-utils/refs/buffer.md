# Buffer API 精简参考

> 源文档: js-apis-buffer.md (2800+ 行)

## 导入模块

```typescript
import { buffer } from '@kit.ArkTS';
```

---

## 创建 Buffer

```typescript
// 指定大小 (字节)
const buf = buffer.alloc(10);              // 填充 0
const buf = buffer.alloc(10, 0x41);        // 填充 'A'
const buf = buffer.allocUninitializedFromPool(10);  // 未初始化

// 从字符串
const buf = buffer.from("Hello", "utf-8");

// 从数组
const buf = buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]);

// 从 ArrayBuffer
const buf = buffer.from(arrayBuffer);
const buf = buffer.from(arrayBuffer, offset, length);

// 从另一个 Buffer
const buf = buffer.from(otherBuffer);

// 拼接多个 Buffer
const buf = buffer.concat([buf1, buf2], totalLength?);
```

---

## Buffer 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `length` | number | 字节长度 |
| `buffer` | ArrayBuffer | 底层 ArrayBuffer |
| `byteOffset` | number | 在 ArrayBuffer 中的偏移 |

---

## 读取方法

### 整数读取

| 方法 | 说明 | 范围 |
|------|------|------|
| `readInt8(offset)` | 有符号 8 位 | -128 ~ 127 |
| `readUInt8(offset)` | 无符号 8 位 | 0 ~ 255 |
| `readInt16BE/LE(offset)` | 有符号 16 位 | -32768 ~ 32767 |
| `readUInt16BE/LE(offset)` | 无符号 16 位 | 0 ~ 65535 |
| `readInt32BE/LE(offset)` | 有符号 32 位 | -2^31 ~ 2^31-1 |
| `readUInt32BE/LE(offset)` | 无符号 32 位 | 0 ~ 2^32-1 |
| `readBigInt64BE/LE(offset)` | 有符号 64 位 | BigInt |
| `readBigUInt64BE/LE(offset)` | 无符号 64 位 | BigInt |
| `readIntBE/LE(offset, byteLength)` | 可变长度有符号 | 1-6 字节 |
| `readUIntBE/LE(offset, byteLength)` | 可变长度无符号 | 1-6 字节 |

### 浮点数读取

| 方法 | 说明 |
|------|------|
| `readFloatBE/LE(offset)` | 32 位浮点数 |
| `readDoubleBE/LE(offset)` | 64 位浮点数 |

**BE = 大端序, LE = 小端序**

### 示例

```typescript
const buf = buffer.from([0x01, 0x02, 0x03, 0x04]);
console.info(buf.readUInt8(0));      // 1
console.info(buf.readUInt16BE(0));   // 258 (0x0102)
console.info(buf.readUInt16LE(0));   // 513 (0x0201)
console.info(buf.readUInt32BE(0));   // 16909060 (0x01020304)
```

---

## 写入方法

### 整数写入

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `writeInt8(value, offset)` | 有符号 8 位 | offset + 1 |
| `writeUInt8(value, offset)` | 无符号 8 位 | offset + 1 |
| `writeInt16BE/LE(value, offset)` | 有符号 16 位 | offset + 2 |
| `writeUInt16BE/LE(value, offset)` | 无符号 16 位 | offset + 2 |
| `writeInt32BE/LE(value, offset)` | 有符号 32 位 | offset + 4 |
| `writeUInt32BE/LE(value, offset)` | 无符号 32 位 | offset + 4 |
| `writeBigInt64BE/LE(value, offset)` | 有符号 64 位 | offset + 8 |
| `writeBigUInt64BE/LE(value, offset)` | 无符号 64 位 | offset + 8 |
| `writeIntBE/LE(value, offset, byteLength)` | 可变长度有符号 | offset + byteLength |
| `writeUIntBE/LE(value, offset, byteLength)` | 可变长度无符号 | offset + byteLength |

### 浮点数写入

| 方法 | 说明 |
|------|------|
| `writeFloatBE/LE(value, offset)` | 32 位浮点数 |
| `writeDoubleBE/LE(value, offset)` | 64 位浮点数 |

### 示例

```typescript
const buf = buffer.alloc(4);
buf.writeUInt8(0x01, 0);
buf.writeUInt8(0x02, 1);
buf.writeUInt16BE(0x0304, 2);
// buf: [0x01, 0x02, 0x03, 0x04]
```

---

## 字符串操作

### 写入字符串

```typescript
buf.write(string: string, offset?: number, length?: number, encoding?: string): number
```

### 读取为字符串

```typescript
buf.toString(encoding?: string, start?: number, end?: number): string
```

### 支持的编码

| 编码 | 说明 |
|------|------|
| `utf-8` / `utf8` | UTF-8 (默认) |
| `utf-16le` / `utf16le` | UTF-16 小端序 |
| `latin1` / `binary` | Latin-1 |
| `ascii` | ASCII |
| `base64` | Base64 |
| `base64url` | URL 安全的 Base64 |
| `hex` | 十六进制 |

### 示例

```typescript
const buf = buffer.alloc(16);
buf.write("Hello", 0, "utf-8");
console.info(buf.toString("utf-8", 0, 5));  // "Hello"

// Base64
const b64Buf = buffer.from("SGVsbG8=", "base64");
console.info(b64Buf.toString());  // "Hello"

// Hex
const hexBuf = buffer.from("48656c6c6f", "hex");
console.info(hexBuf.toString());  // "Hello"
```

---

## Buffer 操作

### 填充

```typescript
buf.fill(value: string | number | Uint8Array, offset?: number, end?: number, encoding?: string): Buffer
```

### 复制

```typescript
buf.copy(target: Buffer, targetStart?: number, sourceStart?: number, sourceEnd?: number): number
```

### 切片

```typescript
buf.slice(start?: number, end?: number): Buffer  // 返回视图 (共享内存)
buf.subarray(start?: number, end?: number): Buffer  // 同 slice
```

### 比较

```typescript
buf.compare(target: Buffer, targetStart?: number, targetEnd?: number, 
            sourceStart?: number, sourceEnd?: number): number
// 返回: -1 (小于), 0 (相等), 1 (大于)

buf.equals(otherBuffer: Buffer): boolean
```

### 查找

```typescript
buf.indexOf(value: string | number | Buffer, byteOffset?: number, encoding?: string): number
buf.lastIndexOf(value, byteOffset?, encoding?): number
buf.includes(value, byteOffset?, encoding?): boolean
```

### 交换字节序

```typescript
buf.swap16(): Buffer  // 每 2 字节交换
buf.swap32(): Buffer  // 每 4 字节交换
buf.swap64(): Buffer  // 每 8 字节交换
```

---

## 静态方法

```typescript
// 判断是否为 Buffer
buffer.isBuffer(obj: Object): boolean

// 判断编码是否支持
buffer.isEncoding(encoding: string): boolean

// 计算字符串编码后的字节长度
buffer.byteLength(string: string, encoding?: string): number

// 拼接多个 Buffer
buffer.concat(list: Buffer[] | Uint8Array[], totalLength?: number): Buffer

// 比较两个 Buffer
buffer.compare(buf1: Buffer, buf2: Buffer): number

// 转换字符串编码
buffer.transcode(source: Buffer, fromEnc: string, toEnc: string): Buffer
```

---

## 常用示例

### 读写二进制协议

```typescript
// 写入协议头
const header = buffer.alloc(8);
header.writeUInt16BE(0x1234, 0);  // 魔数
header.writeUInt16BE(1, 2);       // 版本
header.writeUInt32BE(100, 4);     // 数据长度

// 读取协议头
const magic = header.readUInt16BE(0);
const version = header.readUInt16BE(2);
const length = header.readUInt32BE(4);
```

### Base64 编解码

```typescript
// 编码
const str = "Hello, World!";
const encoded = buffer.from(str).toString("base64");
console.info(encoded);  // "SGVsbG8sIFdvcmxkIQ=="

// 解码
const decoded = buffer.from(encoded, "base64").toString("utf-8");
console.info(decoded);  // "Hello, World!"
```

### Hex 编解码

```typescript
// 编码
const data = buffer.from("Hello");
const hex = data.toString("hex");
console.info(hex);  // "48656c6c6f"

// 解码
const restored = buffer.from(hex, "hex");
console.info(restored.toString());  // "Hello"
```

### Buffer 与 ArrayBuffer 转换

```typescript
// Buffer → ArrayBuffer
const buf = buffer.from("Hello");
const arrayBuffer: ArrayBuffer = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length);

// ArrayBuffer → Buffer
const ab = new ArrayBuffer(10);
const buf2 = buffer.from(ab);
```

---

## 与 Uint8Array 关系

Buffer 继承自 Uint8Array，支持所有 Uint8Array 方法：

```typescript
const buf = buffer.from([1, 2, 3]);
buf[0] = 10;           // 索引访问
buf.forEach(x => ...); // 遍历
buf.map(x => x * 2);   // 映射 (返回 Uint8Array)
```

---

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10200001 | 参数越界 | 检查 offset 和 length |
| 10200009 | Buffer 长度错误 | 确保长度为 2/4/8 的倍数 |
| 10200013 | 只读属性 | 不要修改只读属性 |
