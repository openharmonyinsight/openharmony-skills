# 使用 FakeCoverage 避免 DataProvider 模式下 Fuzz 异常终止

在链接了 libfuzzer <= 14 的情况下，且处于 DataProvider 模式下，遇到了类似如下的错误，可能需要阅读此章节：

```text
ERROR: no interesting inputs were found. Is the code instrumented for coverage? Exiting.
```

[libfuzzer 15](https://github.com/llvm/llvm-project/commit/92fb310151d2b1e349695fc0f1c5d5d50afb3b52) 起，修复了该 feature，即使初始化时拒绝了输入，也不会停止执行。

**注意：请确认被测试的库确实被插入了覆盖率反馈，因为在没有覆盖率反馈插桩的情况下，也会出现该错误！**

当前 fuzz 后端对接到了 libfuzzer，而 libfuzzer 在启动时会先输入空字节流、再输入仅包含一个 `'\n'` 的字节流对待测函数进行试探，在两轮结束后检测覆盖率是否新增。在 DataProvider 模式下，如果先消耗数据，再调用待测库的 API，会导致消耗数据时长度不足而提前返回，从而 libfuzzer 认为覆盖率信息为零。

例如下方代码，会触发该错误

触发的代码：

```cangjie
// main.cj
import stdx.fuzz.fuzz.*

main() {
    let f = Fuzzer(api)
    f.disableFakeCoverage()
    f.startFuzz()
    return 0
}

// fuzz_target.cj, with sancov
public func api(dp: FuzzDataProvider): Int32 {
    if (dp.consumeBool() && dp.consumeBool()) {
        throw Exception("TRAP!")
    }
    return 0
}
```

运行结果如下：

```text
...
ERROR: no interesting inputs were found. Is the code instrumented for coverage? Exiting.
...
```

因此，需要使用 Fake Coverage 创建虚假的覆盖率信息，让 libfuzzer 在初始化期间认为待测模块确实被插桩，等到 DataProvider 收集到足够数据后，再进行有效的 fuzz 测试。该模式被称为 Fake Coverage 模式。

将上文的 `disableFakeCoverage()` 替换为 `enableFakeCoverage()` 即可继续运行，最终触发 TRAP。

此外，除了使用 Fake Coverage 模式，还可以在测试用例中主动调用待测函数的某些不重要的 API 来将覆盖率信息传递给 libfuzzer，也能起到让 fuzz 继续下去的作用。

```cangjie
// main.cj
import stdx.fuzz.fuzz.*

main() {
    let f = Fuzzer(api)
    f.enableFakeCoverage()
    f.startFuzz()
    return 0
}

// fuzz_target.cj, with sancov
public func api(dp: FuzzDataProvider): Int32 {
    if (dp.consumeBool() && dp.consumeBool()) {
        throw Exception("TRAP!")
    }
    return 0
}
```

运行结果如下：

```text
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 3187548846
INFO: Loaded 2 modules   (8 inline 8-bit counters): 7 [0x55bf83ea8790, 0x55bf83ea8797), 1 [0x55bf83e97b00, 0x55bf83e97b01),
INFO: -max_len is not provided; libFuzzer will not generate inputs larger than 4096 bytes
INFO: A corpus is not provided, starting from an empty corpus
#2      INITED ft: 5 corp: 1/1b exec/s: 0 rss: 33Mb
#9      NEW    ft: 6 corp: 2/2b lim: 4 exec/s: 0 rss: 33Mb L: 1/1 MS: 2 CopyPart-ChangeByte-
[WARNING]: Detect uncatched exception, maybe caused by bugs, exit now
An exception has occurred:
Exception: TRAP!
...
...
```
