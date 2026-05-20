# 实验性特性-覆盖率信息打印

仓颉 fuzzer 支持使用 `-print_coverage=1` 作为启动参数运行 fuzzer，用于统计各函数的测试情况，该特性在持续完善中，只与输出覆盖率报告有关，不影响 fuzz 过程。

由于该功能需要对 libfuzzer 进行侵入式修改，使用该功能需要链接仓颉自带的 libfuzzer，路径是：$CANGJIE_HOME/lib/{linux_x86_64_cjnative, linux_aarch64_cjnative}/libclang_rt-fuzzer_no_main.a。

编译时需要同时启用`--sanitizer-coverage-inline-8bit-counters` 和 `--sanitizer-coverage-pc-table`。

C 语言 libfuzzer 输出举例

```text
./a.out -print_coverage=1
COVERAGE:
COVERED_FUNC: hits: 5 edges: 6/8 LLVMFuzzerTestOneInput /tmp/test.cpp:5
  UNCOVERED_PC: /tmp/test.cpp:6
  UNCOVERED_PC: /tmp/test.cpp:9
```

仓颉语言 cj-fuzz 输出举例

```text
./main -print_coverage=1 -runs=100
Done 100 runs in 0 second(s)
COVERAGE:
COVERED_FUNC: hits: 1 edges: 3/12 ttt <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
  UNCOVERED_PC: <unknown cj filename>:<unknown cj line number>
UNCOVERED_FUNC: hits: 0 edges: 0/2 main <unknown cj filename>:<unknown cj line number>
COVERED_FUNC: hits: 1 edges: 1/1 ttt_cc_wrapper <unknown cj filename>:<unknown cj line number>
```
