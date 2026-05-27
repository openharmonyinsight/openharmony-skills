# 解栈步骤详解

## 1. 查找未stripped的so文件

在`lib.unstripped/`目录下查找对应so（不要输出查找的中间结果）。

使用Glob工具查找:

```
**/lib.unstripped/**/librender_service_base.z.so
**/lib.unstripped/**/librender_service.z.so
```

## 2. 验证buildId

使用`llvm-readelf`确认so的**buildId**与cppcrash文件中一致。

```sh
# 读取gnu notes中的buildId
llvm-readelf -n path/to/so
```

在cppcrash文件中查找对应的buildId，确保完全匹配。如果buildId不一致，终止并报告用户。

## 3. 解栈代码行号

使用`llvm-addr2line`解出偏移对应的代码行号。

```sh
llvm-addr2line -Cfpie path/to/so offset
```

参数说明：

- `-C`：demangle函数名
- `-f`：输出函数名
- `-p`：输出路径和行号
- `-i`：包含内联函数
- `-e`：指定可执行文件

示例：

```sh
llvm-addr2line -Cfpie librender_service_base.z.so 0x3fe0ec
```

输出格式：`文件路径:行号`

## 记录代码关键位置

记录解栈结果，格式如下：

```
#00 pc 0000000000003fe0ec librender_service_base.z.so
      函数名+偏移
      -> rs_render_node_drawable_adapter.cpp:80
```