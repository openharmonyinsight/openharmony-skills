# stdx.compress.zlib

## 功能介绍

compress 提供压缩解压功能。

压缩是指用更少的比特表示数据，以便更高效地存储和传输数据。在实际应用中，压缩广泛应用于文件压缩、网页压缩、数据库备份等。

压缩功能的实现依赖于压缩算法，主流的压缩算法有 deflate、lz77、lzw 等，这些算法可以将数据中的冗余信息去除或者替换成更紧凑的表示形式，从而实现数据压缩的目的。目前使用 deflate 算法。

基于 deflate 压缩算法，给压缩后数据加上首部和尾部，可封装成不同格式的压缩文件，如 deflate-raw（无封装）、gzip、zip、png 等。其中 zip 可用于多个文件的压缩和打包，gzip 仅包含一个压缩文件。目前支持的数据格式有 deflate-raw 和 gzip，暂不支持文件打包功能。

此外，支持设置压缩级别，更高的压缩级别对应着更高的压缩率和更慢的压缩速度，反之，更低的压缩级别对应着更低的压缩率和更快的压缩速度。

特别地，zlib 指的是压缩功能的一个实现库，zlib 包实现了 deflate 算法，并支持 deflate-raw 和 gzip 压缩格式。

本包基于开源库 zlib，使用 deflate 算法，支持 deflate-raw 和 gzip 数据格式，支持快速、默认、高压缩率三种压缩等级，压缩速度依次下降，压缩率依次提升。

本包提供流式压缩和解压功能，即支持从输入流读取数据，将其压缩或解压，并写入字节数组，或从字节数组中读取数据，将其压缩或解压，并写入输出流。

> **说明：**
>
> 本包暂不支持文件打包功能。

## API 列表

### 类

|                 类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [CompressInputStream](./zlib_package_api/zlib_package_classes.md#class-compressinputstream) | 压缩输入流。    |
| [CompressOutputStream](./zlib_package_api/zlib_package_classes.md#class-compressoutputstream) | 压缩输出流。       |
| [DecompressInputStream](./zlib_package_api/zlib_package_classes.md#class-decompressinputstream) | 解压输入流。    |
| [DecompressOutputStream](./zlib_package_api/zlib_package_classes.md#class-decompressoutputstream) | 解压输出流。      |

### 枚举

|                 枚举名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [CompressLevel](./zlib_package_api/zlib_package_enums.md#enum-compresslevel) | 压缩等级。      |
| [WrapType](./zlib_package_api/zlib_package_enums.md#enum-wraptype) | 压缩数据格式。    |

### 异常类

|                 异常类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [ZlibException](./zlib_package_api/zlib_package_exceptions.md#class-zlibexception) | `zlib` 包的异常类。      |
