# native 模块 — 查询工具规格

Native SDK 库与 `interface/sdk_c` 源码头文件的映射。关系由 `knowledge.db` 提供，
`interface/sdk_c/` 是 `knowledge.tar.gz` 解压出的 SDK 源码，用于核对 `header_path` 指向的头文件；
它不是数据库，查询过程也不重新扫描或构建。

运行时根目录下应存在 `interface/sdk_c/`。DB 的 `header_path` 从该根目录解析；
归档中的 SDK 快照可能与扫描 revision 不同。源码缺失或路径不存在时明确报告 `SDK 源码缺失`，
不能把“没有源码可核对”说成“没有 Native SDK 头文件映射”。

## 工具清单

| 工具 | 说明 |
|------|------|
| `search_native_headers` | 模糊搜索头文件、库路径、SONAME、文件名或部件名 |
| `get_native_headers` | 按镜像库路径取全部头文件 |

---

## search_native_headers

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 子串搜索：`header_path`、`dest`、`soname`、`file_name`、`component` |
| `match_strategy` | string | | `build_gn` / `header_library` / `symbol` |
| `component` | string | | 按部件名精确过滤 |
| `limit` | int | | 默认 20，上限 100 |

**返回**

```json
{
  "results": [
    {
      "id": 1,
      "elf_module_id": 364,
      "header_path": "interface/sdk_c/third_party/openSLES/api/1.0.1/OpenSLES.h",
      "match_strategy": "build_gn",
      "soname": "libOpenSLES.so",
      "file_name": "libOpenSLES.so",
      "partition": "system",
      "component_id": 20,
      "dest": "system/lib/libOpenSLES.so",
      "component": "audio_framework"
    }
  ],
  "total": 1,
  "truncated": false
}
```

`total` 是全量匹配数，不受 `limit` 影响；`results` 是本次按 `limit` 返回的条目。
`total > len(results)` 时 `truncated=true`，即 `truncated` 表示结果被 `limit` 截断；需要完整结果时提高 `limit`。

---

## get_native_headers

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `dest` | string | ✓ | 镜像内 ELF 路径 |

**返回**

```json
{
  "dest": "system/lib/libOpenSLES.so",
  "elf_module_id": 364,
  "soname": "libOpenSLES.so",
  "file_name": "libOpenSLES.so",
  "partition": "system",
  "component": "audio_framework",
  "component_id": 20,
  "total": 3,
  "headers": [
    {
      "id": 1,
      "elf_module_id": 364,
      "header_path": "interface/sdk_c/third_party/openSLES/api/1.0.1/OpenSLES.h",
      "match_strategy": "build_gn",
      "source_url": "https://example.git/tree/<commit>/api/1.0.1/OpenSLES.h"
    }
  ]
}
```

`match_strategy` 的证据强度从高到低为 `build_gn`、`header_library`、`symbol`。
`symbol` 表示扫描时通过符号匹配建立了这条头文件→库关系，**不是可查询的符号名或完整符号图**；
当前没有独立 symbol 表。需要核对具体声明时，按 `header_path` 打开
`interface/sdk_c` 下的头文件，再到部件/子系统查询中补上下文。
`source_url` 是按仓路径和扫描提交拼出的访问 URL，未做 blob 内容比对。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | `dest` 没有 Native SDK 头文件映射 |
| `INVALID_PARAM` | `match_strategy` 非法或 `limit < 1` |
