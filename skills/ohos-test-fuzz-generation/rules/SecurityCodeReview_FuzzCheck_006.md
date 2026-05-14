# 规则006: 单文件测试接口过多

**严重程度**: 中危

**问题描述**: 单个 fuzzer 文件中测试的接口数量不应超过 10 个。接口过多会导致变异数据被分散到多个分支，每个分支获得的数据量减少，降低 fuzz 覆盖率和数据变异性。

**核心原则**:
- 单文件接口数 ≤ 10（包括 TARGET_SIZE 常量、测试函数数量、switch-case 分支数）
- 如果需要测试更多接口，应拆分为多个独立的 fuzzer 文件
- 每个文件聚焦于一个功能模块或一组紧密相关的 API

**错误示例**:
```cpp
// ❌ TARGET_SIZE 超过 10
const uint8_t DO_METHOD1 = 0;
const uint8_t DO_METHOD2 = 1;
// ... 省略中间
const uint8_t DO_METHOD15 = 14;
const uint8_t TARGET_SIZE = 15;  // 错误：超过10个

// ❌ 串行调用过多测试函数
void LLVMFuzzerTestOneInput(...) {
    DoMethod1(fdp);
    DoMethod2(fdp);
    // ... 15个调用
    DoMethod15(fdp);  // 错误：超过10个
}

// ❌ switch-case 分支过多
switch (choice) {
    case 0: ... break;
    case 1: ... break;
    // ... 15个分支
    case 14: ... break;  // 错误：超过10个
}
```

**正确示例**:
```cpp
// ✅ TARGET_SIZE ≤ 10
const uint8_t DO_SET_CONFIG = 0;
const uint8_t DO_GET_STATUS = 1;
const uint8_t DO_PROCESS_DATA = 2;
const uint8_t TARGET_SIZE = 3;  // 正确：3个接口

// ✅ 拆分为多个文件
// config_fuzzer/ → 测试配置相关接口 (5个)
// data_fuzzer/ → 测试数据处理接口 (6个)
// status_fuzzer/ → 测试状态查询接口 (4个)
```

**检查方法**: 1. 检查 `TARGET_SIZE` 常量值是否 > 10
2. 检查测试函数的串行调用数量是否 > 10
3. 检查 `switch-case` 分支数量是否 > 10
4. 检查 `if-else if` 链式调用数量是否 > 10

**豁免场景**: 
- 相关接口紧密耦合，拆分后需要大量重复初始化代码且影响测试效率

---
