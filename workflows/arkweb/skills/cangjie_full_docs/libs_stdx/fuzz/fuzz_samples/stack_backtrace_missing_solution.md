# 栈回溯缺失的处理方案

当前在启动 fuzz 时默认会有这三条 WARNING，因为当前 cj-fuzz 没有对它们进行实现。

```text
WARNING: Failed to find function "__sanitizer_acquire_crash_state".
WARNING: Failed to find function "__sanitizer_print_stack_trace".
WARNING: Failed to find function "__sanitizer_set_death_callback".
```

在 fuzz 过程中，可能会因为以下 3 种情况而结束 fuzz 流程：

1. 抛出异常
2. 超时
3. 在 C 代码中 crash

其中“抛出异常”的情况，fuzz 框架对异常进行捕获后会打印栈回溯，不会造成栈回溯缺失的现象。

“超时”和“在 C 代码中 crash”实际是在 native 代码中触发了 SIGNAL，不属于仓颉异常，因此会造成栈回溯的缺失。

libfuzzer 会尝试使用 `__sanitizer_acquire_crash_state`、`__sanitizer_print_stack_trace`、`__sanitizer_set_death_callback` 等函数处理异常情况，其中 `__sanitizer_print_stack_trace` 会打印栈回溯，目前成熟的实现在 `llvm` `compiler-rt` 中的 `asan` 等模块中。

因此，建议的解决方案是在链接时额外加入如下的静态库文件和链接选项，释义如下：

```/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.a -lgcc_s --eh-frame-hdr```

- `/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.a` 因为该 .a 文件实现了 `__sanitizer_print_stack_trace`，出于方便就直接用它；
- `-lgcc_s` 栈回溯依赖 gcc_s；
- `--eh-frame-hdr` ld 链接时生成 eh_frame_hdr 节，帮助完成栈回溯。

可选的环境变量：`ASAN_SYMBOLIZER_PATH=$CANGJIE_HOME/third_party/llvm/bin/llvm-symbolizer`，可能在某些情况下有用。

最终会得到两套栈回溯，一套是 Exception.printStackTrace，一套是 `__sanitizer_print_stack_trace`，内容如下：

```text
[WARNING]: Detect uncatched exception, maybe caused by bugs, exit now
An exception has occurred:
Exception: TRAP!
         at default.ttt(std/core::Array<...>)(/data/cangjie/libs/fuzz/ci_fuzzer0.cj:11)
         at _ZN7default3tttER_ZN8std$core5ArrayIhE_cc_wrapper(/data/cangjie/libs/fuzz/ci_fuzzer0.cj:0)
         at libfuzzerCallback(/data/cangjie/libs/fuzz/fuzz/callback.cj:34)
[INFO]: data is: [0, 202, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
[INFO]: crash file will stored with libfuzzer
==425243== ERROR: libFuzzer: fuzz target exited
    #0 0x563a233fadf1 in __sanitizer_print_stack_trace (/data/cangjie/libs/fuzz/main+0x280df1)
    #1 0x563a2337c0b8 in fuzzer::PrintStackTrace() (/data/cangjie/libs/fuzz/main+0x2020b8)
    #2 0x563a2338726c in fuzzer::Fuzzer::ExitCallback() (/data/cangjie/libs/fuzz/main+0x20d26c)
    #3 0x7f485cf36494 in __run_exit_handlers stdlib/exit.c:113:8
    #4 0x7f485cf3660f in exit stdlib/exit.c:143:3
    #5 0x563a23224e68 in libfuzzerCallback$real /data/cangjie/libs/fuzz/fuzz/callback.cj:62:18
    #6 0x7f485d22718b in CJ_MCC_N2CStub (/data/cangjie/output/runtime/lib/linux_x86_64_cjnative/libcangjie-runtime.so+0x2718b)
    #7 0x563a2322fc26 in libfuzzerCallback /data/cangjie/libs/fuzz/fuzz/callback.cj:20
    #8 0x563a23387883 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) (/data/cangjie/libs/fuzz/main+0x20d883)
    #9 0x563a2338a3f9 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long, bool, fuzzer::InputInfo*, bool, bool*) (/data/cangjie/libs/fuzz/main+0x2103f9)
    #10 0x563a23387e49 in fuzzer::Fuzzer::MutateAndTestOne() (/data/cangjie/libs/fuzz/main+0x20de49)
    #11 0x563a2338a2b5 in fuzzer::Fuzzer::Loop(std::vector<fuzzer::SizedFile, std::allocator<fuzzer::SizedFile>>&) (/data/cangjie/libs/fuzz/main+0x2102b5)
    #12 0x563a23377a12 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) (/data/cangjie/libs/fuzz/main+0x1fda12)
    #13 0x563a231ad2b6 in fuzz_fake$fuzz::Fuzzer::startFuzz() /data/cangjie/libs/fuzz/fuzz/fuzzer.cj:200:13
    #14 0x563a23405fad in default::main() /data/cangjie/libs/fuzz/ci_fuzzer0.cj:5:5
    #15 0x563a23405fe7 in user.main /data/cangjie/libs/fuzz/<stdin>
    #16 0x563a234060e1 in cj_entry$ (/data/cangjie/libs/fuzz/main+0x28c0e1)
    #17 0x7f485d227220  (/data/cangjie/output/runtime/lib/linux_x86_64_cjnative/libcangjie-runtime.so+0x27220)
    #18 0x7f485d223898  (/data/cangjie/output/runtime/lib/linux_x86_64_cjnative/libcangjie-runtime.so+0x23898)
    #19 0x7f485d2607b9 in CJ_CJThreadEntry (/data/cangjie/output/runtime/lib/linux_x86_64_cjnative/libcangjie-runtime.so+0x607b9)
```
