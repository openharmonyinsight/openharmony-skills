---
rule_id: "StabilityCodeReview_GraphicsStability_011"
name: "Vulkan信号量导出fd生命周期管理"
category: "图形稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# Vulkan信号量导出fd生命周期管理

## 问题描述

使用GetFenceFdFromSemaphore、vkGetSemaphoreFdKHR等接口从vulkan信号量中导出fd后,fd由调用方负责关闭。**最佳实践是**在判断fd合法后,**立刻**(无任何中间代码)用sptr<SyncFence>智能指针包裹,由该智能指针接管fd生命周期,在智能指针释放时会自动关闭fd。**注意:强调"立刻"二字,意味着在fd导出后、判断合法后,必须立即创建智能指针,中间不能有任何其他代码语句,以确保fd在任何代码路径下都不会泄漏。**若实在无法使用SyncFence类型,须非常谨慎处理每一处函数/作用域出口,确保手动释放fd,避免fd泄漏。

## 检测示例

### 错误示例

```cpp
// 错误示例1:导出fd后未关闭
void ProcessVulkanSemaphore(VkSemaphore semaphore)
{
    int fd = GetFenceFdFromSemaphore(semaphore);
    if (fd < 0) {
        return;  // 错误:fd未关闭
    }
    // 使用fd...
    // 错误:函数结束时fd未关闭
}

// 错误示例2:多个退出路径遗漏关闭
int ExportAndUseFd(VkSemaphore sem)
{
    int fd = vkGetSemaphoreFdKHR(device, sem, &info);
    if (fd < 0) {
        return -1;
    }
    
    if (!CheckCondition()) {
        return -2;  // 错误:fd未关闭
    }
    
    if (!ProcessFd(fd)) {
        return -3;  // 错误:fd未关闭
    }
    
    close(fd);
    return 0;
}

// 错误示例3:异常分支fd泄漏
void HandleSemaphore(VkSemaphore sem)
{
    int fd = GetFenceFdFromSemaphore(sem);
    
    auto result = DoSomething(fd);
    if (!result) {
        LOGE("Operation failed");
        return;  // 错误:fd泄漏
    }
    
    close(fd);
}

// 错误示例4:导出fd后未立刻用智能指针管理
void DelayedFenceWrap(VkSemaphore sem)
{
    int fd = GetFenceFdFromSemaphore(sem);
    if (fd < 0) {
        return;
    }
    
    // 错误:在创建智能指针之前插入了其他代码
    DoSomeOtherWork();  // 如果这里抛异常或出错,fd会泄漏
    
    // 虽然后续使用了智能指针,但不是"立刻"创建
    sptr<SyncFence> fence = new SyncFence(fd);
}
```

### 正确示例

```cpp
// 正确示例1:使用SyncFence智能指针管理fd生命周期
void ProcessVulkanSemaphore(VkSemaphore semaphore)
{
    int fd = GetFenceFdFromSemaphore(semaphore);
    if (fd < 0) {
        LOGE("GetFenceFdFromSemaphore failed, fd=%{public}d", fd);
        return;
    }
    
    // 正确:判断fd合法后,立刻(无中间代码)使用sptr<SyncFence>智能指针管理fd
    sptr<SyncFence> fence = new SyncFence(fd);
    // fd现在由fence管理,无需手动close
}

// 正确示例2:所有退出路径都正确关闭fd
int ExportAndUseFd(VkSemaphore sem)
{
    int fd = vkGetSemaphoreFdKHR(device, sem, &info);
    if (fd < 0) {
        LOGE("vkGetSemaphoreFdKHR failed, fd=%{public}d", fd);
        return -1;
    }
    
    // 正确:使用RAII方式管理fd
    auto fdGuard = [](int* fd) { if (*fd >= 0) close(*fd); };
    std::unique_ptr<int, decltype(fdGuard)> fdHolder(&fd, fdGuard);
    
    if (!CheckCondition()) {
        return -2;  // fd会自动关闭
    }
    
    if (!ProcessFd(fd)) {
        return -3;  // fd会自动关闭
    }
    
    return 0;
}

// 正确示例3:使用SyncFence统一管理
void HandleSemaphore(VkSemaphore sem)
{
    int fd = GetFenceFdFromSemaphore(sem);
    if (fd < 0) {
        LOGE("GetFenceFdFromSemaphore failed, fd=%{public}d", fd);
        return;
    }
    
    // 正确:判断fd合法后,立刻(无中间代码)智能指针接管生命周期
    sptr<SyncFence> fence = new SyncFence(fd);
    
    auto result = DoSomething(fd);
    if (!result) {
        LOGE("Operation failed");
        return;  // 正确:fence析构时自动关闭fd
    }
}
```

## 检测范围

检查以下API/函数/模式:

- `GetFenceFdFromSemaphore()`、`vkGetSemaphoreFdKHR()`
- `GetSemaphoreFd()`、`ImportSemaphoreFdKHR()`
- 所有从Vulkan信号量导出fd的接口

## 检测要点

1. 识别从Vulkan信号量导出fd的调用
2. **检查导出的fd是否在判断合法后立刻(无中间代码)被SyncFence智能指针管理**
   - **关键检测点:** 从fd导出到创建智能指针之间,是否存在其他代码语句
   - **违规示例:** fd导出 → 判断合法 → 中间有其他代码 → 创建智能指针 (应报错)
   - **合规示例:** fd导出 → 判断合法 → 立即创建智能指针 (正确)
3. 若未使用智能指针,检查所有退出路径是否都正确关闭fd
4. 重点关注异常分支、提前返回、错误处理等场景
5. **特别强调:** "立刻"意味着在获取有效fd后,下一行代码就应该创建智能指针,不允许在中间插入任何业务逻辑代码

## 风险流分析(RiskFlow)

- **RISK_SOURCE**: 从Vulkan信号量导出fd后未**立刻**用智能指针管理生命周期
- **RISK_TYPE**: 文件描述符泄漏
- **RISK_PATH**: fd导出 → 未**立刻**用智能指针管理 → 中间代码异常 → fd泄漏累积
- **IMPACT_POINT**: 系统fd资源耗尽,导致无法打开新文件/设备

## 影响分析(ImpactAnalysis)

- **Trigger**: 调用GetFenceFdFromSemaphore等接口导出fd
- **Propagation**: fd未**立刻**用智能指针管理,判断合法和创建智能指针之间插入其他代码,异常分支遗漏关闭
- **Consequence**: fd泄漏累积,系统资源耗尽,程序崩溃或功能异常
- **Mitigation**: 在判断fd合法后**立刻**(无任何中间代码)用sptr<SyncFence>智能指针管理fd生命周期

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| fd立即传递给其他函数管理 | fd作为参数传递给接管函数 | 不报 |
| 使用RAII类管理fd | unique_ptr/shared_ptr/sptr包裹 | 不报(但需检查是否**立刻**创建) |
| 有明确的close调用 | 所有退出路径都有close(fd) | 不报 |
| fd所有权转移 | 有注释说明fd所有权转移 | 不报 |

**注意:** 即使使用了智能指针管理,如果在判断fd合法后到创建智能指针之间插入了其他代码语句,仍应报错,因为这违反了"立刻"的要求。

## 测试用例

### 触发用例(应该报)

```cpp
// test_StabilityCodeReview_GraphicsStability_011_trigger.cpp
void TriggerFdLeak(VkSemaphore semaphore)
{
    int fd = GetFenceFdFromSemaphore(semaphore);
    if (fd < 0) {
        return;  // 应该报:未使用智能指针,异常分支未关闭fd
    }
    
    // 使用fd...
    // 应该报:函数结束未关闭fd
}
```

### 安全用例(不应该报)

```cpp
// test_StabilityCodeReview_GraphicsStability_011_safe.cpp
void SafeFdManagement(VkSemaphore semaphore)
{
    int fd = GetFenceFdFromSemaphore(semaphore);
    if (fd < 0) {
        LOGE("GetFenceFdFromSemaphore failed, fd=%{public}d", fd);
        return;  // 不报:fd无效,打印日志后返回
    }
    
    // 不报:判断fd合法后,立刻(无中间代码)使用智能指针管理fd
    sptr<SyncFence> fence = new SyncFence(fd);
    // fd由fence管理,自动关闭
}
```