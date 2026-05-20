# 打印 fuzz 使用方法

可以使用 `-help=1` 打印帮助，`-seed=246468919` 指定随机数的种子。

运行结果如下：

```text
$ ./main -help=1

Usage:
To run fuzzing pass 0 or more directories.
program_name [-flag1=val1 [-flag2=val2 ...] ] [dir1 [dir2 ...] ]
To run individual tests without fuzzing pass 1 or more files:
program_name [-flag1=val1 [-flag2=val2 ...] ] file1 [file2 ...]
```
