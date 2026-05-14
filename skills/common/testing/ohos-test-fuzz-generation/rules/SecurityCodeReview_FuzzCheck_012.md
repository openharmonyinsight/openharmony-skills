# 规则012: 目标API内部分支覆盖不足

**严重程度**: 中危

**问题描述**: 编写 fuzz 用例时，应深入分析目标 API 的内部实现逻辑，识别所有关键分支点（参数校验、状态判断、边界处理、前置条件、异常路径等）。如果构造的用例数据不合理，fuzz 引擎产生的变异输入会被前置校验拦截，永远无法触及核心业务逻辑，导致 fuzz 测试形同虚设。本规则专注于**分支覆盖不足**的问题，不检测空容器/空指针构造（由规则005负责）。常见分支拦截场景包括：参数范围校验、状态依赖校验、组合条件校验、特殊值处理、固定参数导致只覆盖特定分支。

**核心原则**:
1. 必须覆盖目标API的所有分支
2. 避免只覆盖空值校验分支
3. 构造有效数据以测试核心业务逻辑

**错误示例**:
```cpp
// ❌ 场景1: 参数范围过小，永远触发非法参数分支
void DoSetMode(FuzzedDataProvider& fdp)
{
    uint32_t mode = 9999;  // 业务只支持 0-5
    g_instance->SetMode(mode);
    // 目标 API 内部: if (mode > MODE_MAX) return ERR_INVALID_MODE;
    // 永远无法测试 mode 设置的核心逻辑
}

// ❌ 场景2: 未构造前置依赖状态
void DoProcessData(FuzzedDataProvider& fdp)
{
    uint32_t dataId = fdp.ConsumeIntegral<uint32_t>();
    g_instance->ProcessData(dataId);
    // 目标 API 内部: if (!IsDataLoaded(dataId)) return ERR_NOT_FOUND;
    // 需要先调用 LoadData 才能走到 ProcessData 的核心逻辑
}

// ❌ 场景3: 未考虑组合条件，永远走错误分支
void DoSetResolution(FuzzedDataProvider& fdp)
{
    uint32_t width = 100;
    uint32_t height = 10000;  // width < height 违反业务约束
    g_instance->SetResolution(width, height);
    // 目标 API 内部: if (width > height) return ERR_INVALID_RATIO;
    // 永远无法测试分辨率设置的核心逻辑
}
```

**正确示例**:
```cpp
// ✅ 场景1: 让 mode 覆盖合法值和非法值
void DoSetMode(FuzzedDataProvider& fdp)
{
    // 50% 概率产生合法值(0-5)，50% 概率产生非法值(6-255)
    uint8_t mode = fdp.ConsumeIntegral<uint8_t>();
    g_instance->SetMode(mode);
    // 合法值走: 模式设置成功分支
    // 非法值走: 参数校验失败分支
}

// ✅ 场景2: 先构造前置依赖，再调用目标 API
void DoProcessData(FuzzedDataProvider& fdp)
{
    // 先加载数据，构造前置条件
    uint32_t dataId = fdp.ConsumeIntegral<uint32_t>();
    std::vector<uint8_t> data = fdp.ConsumeBytes<uint8_t>(fdp.ConsumeIntegral<uint8_t>());
    g_instance->LoadData(dataId, data);
    
    // 再调用需要依赖的接口
    g_instance->ProcessData(dataId);
    // 现在可以覆盖: 数据不存在分支、数据存在但无效分支、正常处理分支
}

// ✅ 场景3: 考虑组合条件，构造合法参数组合
void DoSetResolution(FuzzedDataProvider& fdp)
{
    // 确保 width <= height 满足业务约束
    uint32_t width = fdp.ConsumeIntegral<uint16_t>() + 1;   // 1-65536
    uint32_t height = width + fdp.ConsumeIntegral<uint16_t>();  // height >= width
    g_instance->SetResolution(width, height);
    // 覆盖: 参数非法分支(概率低)、正常设置分支、边界值处理分支
}
```

**深度分析示例**:

假设目标 API 内部实现如下：
```cpp
int32_t ProcessImage(const ImageBuffer& buffer, uint32_t width, uint32_t height, PixelFormat format)
{
    // 分支1: 空指针校验
    if (buffer.data == nullptr || buffer.size == 0) {
        return ERR_INVALID_BUFFER;
    }
    
    // 分支2: 尺寸范围校验
    if (width == 0 || height == 0 || width > MAX_WIDTH || height > MAX_HEIGHT) {
        return ERR_INVALID_SIZE;
    }
    
    // 分支3: 宽高比例校验
    if (width * height > MAX_PIXELS) {
        return ERR_TOO_LARGE;
    }
    
    // 分支4: 格式校验
    if (format != RGBA && format != RGB && format != GRAY) {
        return ERR_INVALID_FORMAT;
    }
    
    // 分支5: 缓冲区大小校验
    uint32_t expectedSize = width * height * GetPixelSize(format);
    if (buffer.size < expectedSize) {
        return ERR_BUFFER_TOO_SMALL;
    }
    
    // 核心逻辑（我们希望 fuzz 能走到这里）
    return ProcessImageData(buffer.data, width, height, format);
}
```

对应的 fuzz 用例应构造：
```cpp
void DoProcessImage(FuzzedDataProvider& fdp)
{
    // 构造非空 buffer（避免分支1）
    uint32_t bufferSize = fdp.ConsumeIntegral<uint16_t>() + 100;  // 至少100字节
    auto bufferData = fdp.ConsumeBytes<uint8_t>(bufferSize);
    ImageBuffer buffer{bufferData.data(), bufferSize};
    
    // 构造合法尺寸（避免分支2）
    uint32_t width = fdp.ConsumeIntegral<uint8_t>() + 1;   // 1-256，在范围内
    uint32_t height = fdp.ConsumeIntegral<uint8_t>() + 1;  // 1-256，在范围内
    
    // 确保不超出最大像素（避免分支3）
    // width * height <= 256*256 = 65536，通常小于 MAX_PIXELS
    
    // 构造合法格式（避免分支4）
    // 50% 概率合法格式，50% 概率非法格式
    uint8_t formatRaw = fdp.ConsumeIntegral<uint8_t>();
    PixelFormat format = (formatRaw < 3) ? 
        static_cast<PixelFormat>(formatRaw) : static_cast<PixelFormat>(formatRaw);
    
    // 调用目标 API
    g_instance->ProcessImage(buffer, width, height, format);
    
    // 覆盖情况:
    // - 小概率: buffer 为空（分支1）
    // - 小概率: 尺寸为0（分支2）
    // - 小概率: 格式非法（分支4）
    // - 大概率: 走到核心逻辑
}
```

**检查方法**:
1. **阅读源码**: 仔细阅读目标 API 的实现代码，识别所有 if/return 分支点
2. **识别拦截点**: 标记所有可能导致提前返回的校验（空指针、范围、状态、权限等）
3. **构造绕过数据**: 设计用例使 fuzz 引擎能产生通过校验的变异数据
4. **平衡覆盖率**: 确保既覆盖正常路径，也覆盖异常路径，但核心逻辑要有足够概率被触发
5. **验证覆盖率**: 使用覆盖率工具验证 fuzz 是否走到了目标分支，如果某个分支始终未触发，调整用例构造

**豁免场景**: 
- 测试目标就是前置校验逻辑本身
- 无法构造绕过数据（如硬编码的系统限制）

---
