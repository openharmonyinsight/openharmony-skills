# 使用 DataProvider 功能进行测试

除了使用字节流对 API 进行测试的方法之外，fuzz 包提供了 FuzzDataProvider 类，用于更友好地从变异的数据源产生仓颉的标准数据类型，方便对 API 进行测试。

```cangjie
public func api2(dp: FuzzDataProvider): Int32 {
    if(dp.consumeBool() && dp.consumeByte() == b'A' && dp.consumeUint32() == 0xdeadbeef){
        throw Exception("TRAP")
    }
    return 0
}
```

此案例中，开启 `--sanitizer-coverage-trace-compares` 可有效提高 fuzz 效率。

DataProvider 模式下，无法直观地判断各个 API 返回值分别是什么，因此提供了 Fuzzer.enableDebugDataProvider() 和 `DebugDataProvider`，在 `startFuzz` 前调用 `enableDebugDataProvider()` 即可令本次 fuzz 每次调用 `consumeXXX` 时打印日志。

例如，上文代码触发异常后，添加 `enableDebugDataProvider` 重新编译，效果如下。

```cangjie
import stdx.fuzz.fuzz.*

main() {
    let fuzzer = Fuzzer(api2)
    fuzzer.enableDebugDataProvider()
    fuzzer.startFuzz()
    return 0
}
```

运行结果如下：

```text
./main crash-d7ece8e77ff25769a5d55eb8d3093d4bace78e1b
Running: crash-d7ece8e77ff25769a5d55eb8d3093d4bace78e1b
[DEBUG] consumeBool return true
[DEBUG] consumeByte return 65
[DEBUG] consumeUInt32 return 3735928559
[WARNING]: Detect uncatched exception, maybe caused by bugs, exit now
An exception has occurred:
Exception: TRAP
         at default.api2(fuzz/fuzz::FuzzDataProvider)(/tmp/test.cj:12)
         at _ZN7default4api2EC_ZN9fuzz$fuzz16FuzzDataProviderE_cc_wrapper(/tmp/test.cj:0)
         at libfuzzerCallback(fuzz/fuzz/callback.cj:0)
[INFO]: data is: [191, 65, 239, 190, 173, 222]
```
