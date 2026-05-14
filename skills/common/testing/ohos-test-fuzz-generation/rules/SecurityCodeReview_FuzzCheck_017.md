# 规则017: 禁止使用random等函数

**严重程度**: 中危

**问题描述**: 应该是使用data中提取变异的数据，例如`fdp.ConsumeBool()`、`fdp.ConsumeRandomLengthString(STR_LEN)`，而不是使用`random()`、`rand()`等函数。

**核心原则**:
1. 禁止使用random/rand/srand等随机函数
2. 必须使用FuzzedDataProvider提取变异数据
3. 随机函数不可重现且不受fuzz引擎控制

**错误示例**:
```cpp
// ❌ 使用random()函数
#include <cstdlib>
#include <ctime>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    srand(time(nullptr));
    int randomValue = rand();
    g_instance->SomeMethod(randomValue);
    return 0;
}
```

**正确示例**:
```cpp
// ✅ 使用FuzzedDataProvider提取变异数据
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    
    bool flag = fdp.ConsumeBool();
    int32_t value = fdp.ConsumeIntegral<int32_t>();
    std::string str = fdp.ConsumeRandomLengthString(64);
    
    g_instance->SomeMethod(flag, value, str);
    return 0;
}
```

**禁止使用的函数**:
- ❌ `rand()`, `random()`, `srand()`
- ❌ `std::random_device`, `std::mt19937`

**应该使用的方法**:
- ✅ `fdp.ConsumeBool()`
- ✅ `fdp.ConsumeIntegral<T>()`
- ✅ `fdp.ConsumeRandomLengthString(maxLength)`
- ✅ `fdp.ConsumeBytes<T>(length)`

**检查方法**: 1. 检查代码中是否使用了 `rand()`、`random()`、`srand()` 等 C 标准库随机函数
2. 检查代码中是否使用了 `std::random_device`、`std::mt19937` 等 C++ 随机库
3. 上述函数不可重现且不受 fuzz 引擎控制，应替换为 `fdp.ConsumeXxx()` 方法

**豁免场景**: 
- 无

---
