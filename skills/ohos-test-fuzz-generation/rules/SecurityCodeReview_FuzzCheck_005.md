# 规则005: 复杂参数未合理构造

**严重程度**: 中危

**问题描述**: 实际业务 API 中，入参很少是基础数据类型（`int`, `string`, `bool` 等），绝大多数是**复杂类型**：结构体、类对象、智能指针、回调函数、容器、枚举组合等。如果直接传递 `nullptr`、默认构造的空对象或未初始化的内存，会被业务代码的前置校验拦截，导致无法测试真正的业务逻辑。构造复杂参数时应先查看 API 头文件和类型定义，追踪参数类型的完整定义（字段、构造函数、约束条件），查看 TDD 单元测试了解如何构造该对象，并查看业务代码的校验逻辑了解哪些字段是必需的。

**核心原则**:
1. **必须查看参数定义**：通过头文件或源码找到参数类型的完整定义（字段、构造函数、约束条件）
2. **必须用 FuzzedDataProvider 填充**：所有可变字段都应从 `fdp` 提取数据，而非硬编码
3. **必须构造有意义的对象**：确保对象能通过业务校验，进入核心逻辑

**错误示例**:
```cpp
// ❌ 默认构造，所有字段都是 0 或默认值
void DoSetScreenModeInfo(FuzzedDataProvider& fdp)
{
    ScreenId id = fdp.ConsumeIntegral<uint64_t>();
    RSScreenModeInfo info;  // 错误：所有字段都是默认值，可能被拦截
    g_screenManager->SetScreenModeInfo(id, info);
}

// ❌ 智能指针直接赋值为 nullptr
void DoCreateObject(FuzzedDataProvider& fdp)
{
    uint32_t id = fdp.ConsumeIntegral<uint32_t>();
    std::shared_ptr<MyObject> obj = nullptr;  // 错误！
    g_manager->CreateObject(id, obj);
}

// ❌ 空容器会被拦截或走空逻辑分支
void DoSetBlackList(FuzzedDataProvider& fdp)
{
    uint32_t id = fdp.ConsumeIntegral<uint32_t>();
    std::vector<uint64_t> blacklist;  // 错误：空列表
    g_manager->SetBlackList(id, blacklist);
}
```

**正确示例**:
```cpp
// ✅ 从 fdp 提取数据填充每个字段
void DoSetScreenModeInfo(FuzzedDataProvider& fdp)
{
    ScreenId id = fdp.ConsumeIntegral<uint64_t>();
    RSScreenModeInfo info;
    info.SetScreenWidth(fdp.ConsumeIntegral<int32_t>());
    info.SetScreenHeight(fdp.ConsumeIntegral<int32_t>());
    info.SetScreenRefreshRate(fdp.ConsumeIntegral<uint32_t>());
    info.SetScreenModeId(fdp.ConsumeIntegral<int32_t>());
    // 如果还有更多字段，继续填充...
    g_screenManager->SetScreenModeInfo(id, info);
}

// ✅ 用 make_shared 构造，并填充对象字段
void DoCreateObject(FuzzedDataProvider& fdp)
{
    uint32_t id = fdp.ConsumeIntegral<uint32_t>();
    auto obj = std::make_shared<MyObject>(
        fdp.ConsumeIntegral<int32_t>(),      // 构造函数参数1
        fdp.ConsumeRandomLengthString(32)    // 构造函数参数2
    );
    // 如果对象还有 setter 方法，继续填充
    obj->SetProperty(fdp.ConsumeIntegral<uint32_t>());
    g_manager->CreateObject(id, obj);
}

// ✅ 构造变长容器，元素数量从 fdp 提取
void DoSetBlackList(FuzzedDataProvider& fdp)
{
    uint32_t id = fdp.ConsumeIntegral<uint32_t>();
    std::vector<uint64_t> blacklist;
    size_t count = fdp.ConsumeIntegral<uint8_t>() % 10;  // 0-9 个元素
    for (size_t i = 0; i < count; i++) {
        blacklist.push_back(fdp.ConsumeIntegral<uint64_t>());
    }
    g_manager->SetBlackList(id, blacklist);
}

// ✅ 多重嵌套类型：层层拆解，从内到外逐级构造
void DoSetComplexData(FuzzedDataProvider& fdp)
{
    auto dataList = std::make_shared<std::vector<DataItem>>();
    
    size_t count = fdp.ConsumeIntegral<uint8_t>() % 5;
    for (size_t i = 0; i < count; i++) {
        DataItem item;
        item.id = fdp.ConsumeIntegral<uint32_t>();
        item.name = fdp.ConsumeRandomLengthString(32);
        item.value = fdp.ConsumeIntegral<float>();
        dataList->push_back(item);
    }
    
    g_manager->SetComplexData(dataList);
}
```

**检查方法**:
1. 检查智能指针是否直接赋值为 nullptr 而未构造有效对象
2. 检查结构体/类是否默认构造后未用 fdp 填充字段
3. 检查容器是否为空且未填充元素
4. 检查 C 风格指针是否为 nullptr 并传给接口

**豁免场景**: 
- API明确要求传递nullptr（如解绑、清空操作）
- 默认构造对象有合法语义（如默认配置）
- 空容器有业务意义（如清空列表）

---
