# 规则009: FUZZ Driver引入bug

**严重程度**: 中危

**问题描述**: 用例代码书写错误可能引入多种安全问题，这些问题往往不是被测目标 API 的缺陷，而是 FUZZ Driver 自身构造数据或边界条件时引入的，会干扰 fuzz 结果的有效性，甚至掩盖真正的漏洞。主要包括：

- **内存安全类**：堆溢出、栈溢出、缓冲区溢出、数组越界访问、非法内存访问、空指针解引用、use-after-free
- **资源管理类**：内存泄漏（new/delete、malloc/free 不匹配）、文件句柄泄漏、死锁
- **逻辑安全类**：整数溢出/下溢、除零、类型混淆、越界偏移量计算
- **构造合理性问题**：分配超大内存导致卡住、创建未初始化的对象、资源未释放

**核心原则**:
1. FUZZ Driver代码必须保证内存安全
2. 避免堆溢出、栈溢出、数组越界等漏洞
3. 正确处理资源分配和释放

**错误示例**:
```cpp
// ❌ 长度判断错误导致堆溢出
void DoReadData(FuzzedDataProvider& fdp)
{
    uint32_t bufferSize = fdp.ConsumeIntegral<uint32_t>();
    // 业务要求：bufferSize >= 2*sizeof(int32_t)
    if (bufferSize < 8) {
        return;  // 错误：判断了8字节，但后面读了3个int32（12字节）
    }

    // 读取3个int32_t（需要12字节，但只判断了8字节）
    int32_t value1 = fdp.ConsumeIntegral<int32_t>();
    int32_t value2 = fdp.ConsumeIntegral<int32_t>();
    int32_t value3 = fdp.ConsumeIntegral<int32_t>();  // 可能堆溢出
    g_instance->ProcessData(value1, value2, value3);
}

// ❌ 数组越界访问
void DoProcessArray(FuzzedDataProvider& fdp)
{
    int32_t index = fdp.ConsumeIntegral<int32_t>();
    int32_t values[10];
    values[index] = fdp.ConsumeIntegral<int32_t>();  // index 未做范围校验，可能越界
}

// ❌ 空指针解引用
void DoSetCallback(FuzzedDataProvider& fdp)
{
    void* ptr = nullptr;
    g_instance->RegisterCallback(ptr);  // 某些实现未做空指针保护，触发崩溃
}

// ❌ 整数下溢导致超大内存分配
void DoAllocBuffer(FuzzedDataProvider& fdp)
{
    size_t len = fdp.ConsumeIntegral<uint8_t>();
    size_t extra = 16;
    size_t total = len - extra;  // len < 16 时发生下溢，分配超大内存
    auto buffer = std::make_unique<uint8_t[]>(total);
}

// ❌ 内存泄漏（new 后未 delete）
void DoCreateObject(FuzzedDataProvider& fdp)
{
    MyObject* obj = new MyObject(fdp.ConsumeIntegral<int32_t>());
    g_instance->UseObject(obj);
    // 错误：未 delete obj，内存泄漏
}

// ❌ 分配超大内存导致卡住
void DoAllocHugeBuffer(FuzzedDataProvider& fdp)
{
    uint32_t size = fdp.ConsumeIntegral<uint32_t>();
    // 错误：未限制 size 范围，可能分配超大内存导致卡住
    auto buffer = std::make_unique<uint8_t[]>(size);
    g_instance->ProcessBuffer(buffer.get(), size);
}

// ❌ 使用未初始化的指针
void DoProcessData(FuzzedDataProvider& fdp)
{
    int32_t* data;  // 错误：未初始化
    g_instance->ProcessData(data);  // 未定义行为
}
```

**正确示例**:
```cpp
// ✅ 正确的长度判断
void DoReadData(FuzzedDataProvider& fdp)
{
    uint32_t bufferSize = fdp.ConsumeIntegral<uint32_t>();
    // 业务要求：bufferSize >= 3*sizeof(int32_t) = 12
    if (bufferSize < 12) {
        return;
    }

    int32_t value1 = fdp.ConsumeIntegral<int32_t>();
    int32_t value2 = fdp.ConsumeIntegral<int32_t>();
    int32_t value3 = fdp.ConsumeIntegral<int32_t>();
    g_instance->ProcessData(value1, value2, value3);
}

// ✅ 数组索引做范围校验
void DoProcessArray(FuzzedDataProvider& fdp)
{
    int32_t index = fdp.ConsumeIntegral<int32_t>();
    if (index < 0 || index >= 10) {
        return;
    }
    int32_t values[10];
    values[index] = fdp.ConsumeIntegral<int32_t>();
}

// ✅ 避免空指针传入
void DoSetCallback(FuzzedDataProvider& fdp)
{
    auto callback = [](int x) { (void)x; };
    g_instance->RegisterCallback(callback);
}

// ✅ 防止整数下溢
void DoAllocBuffer(FuzzedDataProvider& fdp)
{
    size_t len = fdp.ConsumeIntegral<uint8_t>();
    size_t extra = 16;
    if (len < extra) {
        return;
    }
    size_t total = len - extra;
    auto buffer = std::make_unique<uint8_t[]>(total);
}

// ✅ 使用智能指针避免内存泄漏
void DoCreateObject(FuzzedDataProvider& fdp)
{
    auto obj = std::make_unique<MyObject>(fdp.ConsumeIntegral<int32_t>());
    g_instance->UseObject(obj.get());
    // 智能指针自动释放，无内存泄漏
}

// ✅ 限制内存分配大小
void DoAllocHugeBuffer(FuzzedDataProvider& fdp)
{
    uint32_t size = fdp.ConsumeIntegral<uint32_t>() % 65536;  // 限制最大64KB
    auto buffer = std::make_unique<uint8_t[]>(size);
    g_instance->ProcessBuffer(buffer.get(), size);
}

// ✅ 初始化指针
void DoProcessData(FuzzedDataProvider& fdp)
{
    auto data = std::make_unique<int32_t>(fdp.ConsumeIntegral<int32_t>());
    g_instance->ProcessData(data.get());
}
```

**检查方法**:
1. 检查 buffer 大小判断与实际读取/写入的字节数是否匹配
2. 检查数组索引、循环边界是否做了范围校验
3. 检查指针在使用前是否已合理构造或做空指针保护
4. 检查整数运算（尤其是减法、乘法）是否存在溢出/下溢风险
5. 检查资源分配后是否有对应的释放逻辑（new/delete、malloc/free 匹配）
6. 检查内存分配是否做了大小限制，避免分配超大内存
7. 检查指针和对象是否已初始化，避免使用未初始化的值

**豁免场景**: 
- 无（fuzz driver自身引入的bug必须修复）

---
