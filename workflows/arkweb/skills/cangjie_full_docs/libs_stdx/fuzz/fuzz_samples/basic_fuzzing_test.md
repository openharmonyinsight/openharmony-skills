# 测试猜测字符功能

- 编写被测 API，当且仅当输入数组长度是 8、内容是 "Cangjie!" 对应的 ASCII 时抛出异常，纯随机的情况下最差需要 2<sup>64</sup> 次猜测才会触发异常。
- 创建 Fuzzer 并且调用待测 API，进入主流程。

```cangjie
// 导入依赖的类
import stdx.fuzz.fuzz.Fuzzer

main() {
    // 创建 Fuzzer 并启动 fuzz 流程
    Fuzzer(api).startFuzz()
    return 0
}


// 被测函数，在满足特定条件会抛出异常，该异常会被 Fuzzer 捕获
public func api(data: Array<UInt8>): Int32 {
    if (data.size == 8 && data[0] == b'C' && data[1] == b'a' && data[2] == b'n' && data[3] == b'g' && data[4] == b'j' &&
        data[5] == b'i' && data[6] == b'e' && data[7] == b'!') {
        throw Exception("TRAP")
    }
    return 0
}
```

> 下方的命令中的 CANGJIE_STDX_PATH 指向存放 stdx 系列的路径，例如 "./static/stdx"

Linux 的编译命令是：`cjc fuzz_main.cj -L $CANGJIE_STDX_PATH -lstdx.fuzz.fuzz --import-path $CANGJIE_STDX_PATH --link-options="--whole-archive $CANGJIE_HOME/lib/linux_x86_64_cjnative/libclang_rt.fuzzer_no_main.a -no-whole-archive -lstdc++" --sanitizer-coverage-inline-8bit-counters -lpthread`

macOS 的编译命令是：`cjc fuzz_main.cj -L $CANGJIE_STDX_PATH -lstdx.fuzz.fuzz --import-path $CANGJIE_STDX_PATH --link-options="$CANGJIE_HOME/lib/linux_x86_64_cjnative/libclang_rt.fuzzer_no_main.a -lc++" --sanitizer-coverage-inline-8bit-counters -lpthread`

释义：

- link-options 是链接时选项，fuzz 库本身依赖符号 `LLVMFuzzerRunDriver`，该符号需要开发者自行解决。
    - 仓颉语言在 $CANGJIE_HOME/lib/linux_x86_64_cjnative/libclang_rt.fuzzer_no_main.a 存放一份 **修改过** 的 libfuzzer，对标准的 libfuzzer 进行了增强，见 [实验性特性-覆盖率信息打印](./print_coverage.md)。
    - 可以使用 `find $(clang -print-runtime-dir) -name "libclang_rt.fuzzer_no_main*.a"` 寻找本地安装好的静态库文件。
- 向 Linux 编译需要使用 `whole-archive libfuzzer.a` 是因为 cjc 调用 ld 后端时，从左到右顺序是 `libfuzzer.a` 、 `libcangjie-fuzz-fuzz.a`、 libc 等基础库，该顺序会导致 `libcangjie-fuzz-fuzz.a` 依赖的 `LLVMFuzzerRunDriver` 符号未被找到。解决方案有：
    - 将 `libfuzzer.a` 放到 `libcangjie-fuzz-fuzz.a` 后面；
    - 使用 `whole-archive libfuzzer.a` 来规避符号找不到的问题。
- `-lstdc++` (Linux) / `-lc++` (macOS) 用于链接 libfuzzer 依赖的 std 库。
- `--sanitizer-coverage-inline-8bit-counters` 是 `cjc` 的编译选项，它会对当前 `package` 执行覆盖率反馈插桩，详见 cjc 编译器使用手册。
    - 其他高级的参数有：`--sanitizer-coverage-trace-compares`（提高 Fuzz 变异的效率）、`--sanitizer-coverage-pc-table`（Fuzz 结束后打印覆盖率信息）。

> **注意：**
>
> 如果您使用的 Linux 系统版本较低，可能出现 GLIBC 版本过低的链接器报错，请在 `link-options` 参数中添加 `-lpthread` 来解决此问题。

与 `libfuzzer` 体验类似，可以直接运行，数秒后（取决于 CPU 性能）可获得 crash，且输入的数据是 "Cangjie!"

运行结果如下：

```text
$ ./main
INFO: Seed: 246468919
INFO: Loaded 1 modules   (15 inline 8-bit counters): 15 [0x55bb7c76dcb0, 0x55bb7c76dcbf),
INFO: -max_len is not provided; libFuzzer will not generate inputs larger than 4096 bytes
INFO: A corpus is not provided, starting from an empty corpus
#2      INITED ft: 4 corp: 1/1b exec/s: 0 rss: 28Mb
#420    NEW    ft: 5 corp: 2/9b lim: 8 exec/s: 0 rss: 28Mb L: 8/8 MS: 3 CrossOver-InsertByte-InsertRepeatedBytes-
#1323   NEW    ft: 6 corp: 3/17b lim: 14 exec/s: 0 rss: 28Mb L: 8/8 MS: 3 InsertByte-InsertByte-CrossOver-
#131072 pulse  ft: 6 corp: 3/17b lim: 1300 exec/s: 65536 rss: 35Mb
#262144 pulse  ft: 6 corp: 3/17b lim: 2600 exec/s: 65536 rss: 41Mb
#295225 NEW    ft: 7 corp: 4/25b lim: 2930 exec/s: 73806 rss: 43Mb L: 8/8 MS: 2 ShuffleBytes-ChangeByte-
#514006 NEW    ft: 8 corp: 5/33b lim: 4096 exec/s: 73429 rss: 53Mb L: 8/8 MS: 1 ChangeByte-
#524288 pulse  ft: 8 corp: 5/33b lim: 4096 exec/s: 74898 rss: 53Mb
#1048576        pulse  ft: 8 corp: 5/33b lim: 4096 exec/s: 61680 rss: 78Mb
#1064377        NEW    ft: 9 corp: 6/41b lim: 4096 exec/s: 62610 rss: 79Mb L: 8/8 MS: 1 ChangeByte-
#1287268        NEW    ft: 10 corp: 7/49b lim: 4096 exec/s: 61298 rss: 90Mb L: 8/8 MS: 1 ChangeByte-
#2097152        pulse  ft: 10 corp: 7/49b lim: 4096 exec/s: 59918 rss: 128Mb
#2875430        NEW    ft: 11 corp: 8/57b lim: 4096 exec/s: 61179 rss: 165Mb L: 8/8 MS: 2 ChangeBinInt-ChangeByte-
#4194304        pulse  ft: 11 corp: 8/57b lim: 4096 exec/s: 59918 rss: 227Mb
#4208258        NEW    ft: 12 corp: 9/65b lim: 4096 exec/s: 60117 rss: 228Mb L: 8/8 MS: 3 CrossOver-CrossOver-ChangeBit-
[WARNING]: Detect uncatched exception, maybe caused by bugs, exit now
An exception has occurred:
Exception: TRAP
         at default.api(std/core::Array<...>)(/data/Cangjie/fuzz_main.cj:14)
         at _ZN7default3apiER_ZN8std$core5ArrayIhE_cc_wrapper(/data/Cangjie/fuzz_main.cj:0)
         at libfuzzerCallback(fuzz/fuzz/callback.cj:20)
[INFO]: data is: [67, 97, 110, 103, 106, 105, 101, 33]
[INFO]: crash file will stored with libfuzzer
==899957== ERROR: libFuzzer: fuzz target exited
SUMMARY: libFuzzer: fuzz target exited
MS: 1 ChangeByte-; base unit: 7d8b0108ce76a937161065eafcde95bbf3d47dbf
0x43,0x61,0x6e,0x67,0x6a,0x69,0x65,0x21,
Cangjie!
artifact_prefix='./'; Test unit written to ./crash-555e7af32a2ceb585cdd9ce810c4804e65d41cea
Base64: Q2FuZ2ppZSE=
```
