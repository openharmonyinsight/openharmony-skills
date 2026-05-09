# 规则002: 关键API需要FUZZ覆盖

**严重程度**: 中危

**问题描述**: 有参数的API/接口必须进行FUZZ覆盖，以确保参数的健壮性。

**核心原则**:
1. 所有有参public API都应被FUZZ覆盖
2. 关键业务逻辑API必须包含在测试范围内
3. 遗漏API会导致安全漏洞无法被发现

**错误示例**:
```cpp
// ❌ 只覆盖了部分有参数的API，遗漏了 SetScreenBacklight
const uint8_t DO_SET_SCREEN_POWER_STATUS = 0;
const uint8_t TARGET_SIZE = 1;

void DoSetScreenPowerStatus(FuzzedDataProvider& fdp)
{
    ScreenId id = fdp.ConsumeIntegral<uint64_t>();
    ScreenPowerStatus status = static_cast<ScreenPowerStatus>(fdp.ConsumeIntegral<uint32_t>());
    g_rsInterfaces->SetScreenPowerStatus(id, status);
}

// SetScreenBacklight(ScreenId id, uint32_t level) 未测试
```

**正确示例**:
```cpp
// ✅ 覆盖所有有参数的API
const uint8_t DO_SET_SCREEN_POWER_STATUS = 0;
const uint8_t DO_SET_SCREEN_BACKLIGHT = 1;
const uint8_t TARGET_SIZE = 2;

void DoSetScreenPowerStatus(FuzzedDataProvider& fdp)
{
    ScreenId id = fdp.ConsumeIntegral<uint64_t>();
    ScreenPowerStatus status = static_cast<ScreenPowerStatus>(fdp.ConsumeIntegral<uint32_t>());
    g_rsInterfaces->SetScreenPowerStatus(id, status);
}

void DoSetScreenBacklight(FuzzedDataProvider& fdp)
{
    ScreenId id = fdp.ConsumeIntegral<uint64_t>();
    uint32_t level = fdp.ConsumeIntegral<uint32_t>();
    g_rsInterfaces->SetScreenBacklight(id, level);
}
```

**检查方法**:
1. 对比目标类的所有public API
2. 确保所有有参数API都被FUZZ测试覆盖

**豁免场景**: 
- 内部使用API（private/protected成员）
- 已在其他fuzzer中覆盖的API
- 废弃API（标记为deprecated）

---
