# OpenHarmony CAPI XTS 测试框架指南

> **文档目的**：定义 OpenHarmony CAPI (Native C API) XTS 测试的基础框架、规范和标准，为 N-API 测试提供理论基础

> 📖 **相关文档**：
> - [N-API 和 ETS 公共模式](./test_patterns_napi_ets.md) - N-API 封装和 ETS 测试的公共模式定义
> - [N-API 和 ETS 高级模式](./test_patterns_napi_ets_advance.md) - N-API 和 ETS 测试的高级模式和特殊场景
> - [测试生成核心](../L2_Generation/test_generation_c.md) - 测试用例生成核心文档
> - [子系统测试示例](../examples/) - 各子系统的完整测试用例示例和实现

## 一、CAPI 测试基础

### 1.1 为什么 CAPI 测试重要

- **系统基础**：CAPI 是 OpenHarmony 系统的基础接口，测试确保系统稳定
- **性能关键**：CAPI 直接影响系统性能和资源消耗
- **跨语言集成**：支持 C 与 ArkTS/JavaScript 的无缝集成
- **测试标准化**：XTS (eXtensive Test Suite) 是 OpenHarmony 的标准测试套件
- **质量保证**：确保 CAPI 接口的正确性和一致性

### 1.2 CAPI 测试特点

| 特点 | 说明 | 子系统示例 |
|------|------|-----------|
| **N-API 封装** | CAPI 通过 N-API 封装供 ETS 调用 | BundleManager, ArkUI, Ability |
| **内存管理** | 手动内存管理，需要测试内存分配和释放 | 系统级 API，文件操作 API |
| **类型转换** | C 类型与 ArkTS 类型之间的转换 | 数据类型 API，序列化 API |
| **错误处理** | 统一的错误码和异常处理机制 | 所有子系统 API |
| **性能敏感** | 需要测试性能和资源消耗 | 图形 API，媒体 API |
| **并发安全** | 需要测试多线程环境下的安全性 | 网络 API，数据库 API |

## 二、CAPI 测试架构

### 2.1 测试架构总览

OpenHarmony CAPI 测试采用标准的 XTS 架构：

```
XTS 测试架构
├── 应用测试层 (ArkTS/JavaScript) - 用户应用测试
├── 框架测试层 (Hypium) - 统一测试框架
├── N-API 封装层 (C/C++ ↔ ArkTS) - 跨语言接口
├── CAPI 原生层 (C/C++ API) - 系统原生接口
└── 系统服务层 (System Services) - 系统服务能力
```

### 2.2 Hypium 测试框架

#### 2.2.1 Hypium 框架概述

**Hypium** 是 OpenHarmony 的官方单元测试框架，提供全面的测试执行能力：

- **基础流程支持**：支持同步和异步测试用例执行
- **丰富的断言库**：25+ 断言方法，支持各种数据类型和场景
- **Mock 能力**：函数级 Mock，支持参数匹配和调用验证
- **数据驱动**：参数化测试，支持不同数据集
- **高级特性**：测试筛选、随机执行、压力测试、超时控制

#### 2.2.2 Hypium 核心组件

| 组件 | 功能 | 说明 | 使用示例 |
|------|------|------|----------|
| **describe** | 定义测试套 | 组织相关的测试用例 | `describe('ActsBundleManagerTest', () => {` |
| **it** | 定义测试用例 | 单个测试场景的实现 | `it('Install_Success', 0, () => {` |
| **expect** | 断言库 | 验证测试结果是否符合预期 | `expect(result).assertEqual(0);` |
| **beforeAll/afterAll** | 套件级钩子 | 在所有测试用例前后执行 | `beforeAll(() => { setup(); });` |
| **beforeEach/afterEach** | 用例级钩子 | 在每个测试用例前后执行 | `beforeEach(() => { init(); });` |
| **MockKit** | Mock 框架 | 函数 Mock 和验证 | `let mocker = new MockKit();` |

#### 2.2.3 Hypium 测试配置

**测试类型（TestType）**：
- `FUNCTION` - 功能测试
- `PERFORMANCE` - 性能测试
- `POWER` - 功耗测试
- `RELIABILITY` - 可靠性测试
- `SECURITY` - 安全测试
- `GLOBAL` - 全局测试
- `COMPATIBILITY` - 兼容性测试

**测试规模（Size）**：
- `SMALLTEST` - 小规模测试
- `MEDIUMTEST` - 中规模测试
- `LARGETEST` - 大规模测试

**测试级别（Level）**：
- `LEVEL0` - `LEVEL4` - 不同级别的测试

### 2.3 CAPI 测试方式

#### 2.3.1 CAPI 测试方式对比

OpenHarmony CAPI 支持两种测试方式：

| 方式 | 名称 | 说明 | 推荐度 |
|------|------|------|--------|
| **方式1** | Native C 测试 | 使用 gtest/HWTEST_F 直接测试 C 函数 | ❌ 不推荐 |
| **方式2** | N-API 封装测试 | 将 C 函数封装为 N-API 供 ETS 测试 | ✅ 强制推荐 |

#### 2.3.2 方式1：Native C 测试（已淘汰）

**特点**：
- 使用 gtest/HWTEST_F 测试框架
- 直接测试 C 函数
- 测试文件：`.cpp` 文件
- ❌ **不再推荐使用**

#### 2.3.3 方式2：N-API 封装测试（⭐ 必需使用）

**特点**：
- 将 C 函数封装为 N-API (napi_value、napi_env) 接口
- 封装函数返回 `napi_value` 类型供 ETS/ArkTS 测试调用
- 测试文件：`NapiTest.cpp` + `*.test.ets`
- ✅ **新生成测试用例必须使用此方式**

**优势**：
- ✅ **符合标准架构**：符合 OpenHarmony 标准系统的测试架构
- ✅ **跨语言集成**：支持 C 语言与 ArkTS 的无缝集成
- ✅ **自动化支持**：便于测试自动化和覆盖率统计
- ✅ **开发体验**：使用 Hypium 框架，开发体验一致
- ✅ **调试支持**：支持 ETS 环境下的调试和日志

## 三、测试类型定义

### 3.1 基本测试类型

#### 3.1.1 PARAM 测试（参数测试）

**定义**：测试 API 在不同参数情况下的行为

**测试场景**：
- 正常参数值
- 边界参数值（最大值、最小值）
- 特殊参数值（null、空字符串、0）
- 无效参数值

**关键点**：
- 参数类型验证
- 参数范围检查
- 参数组合测试

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 参数测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#1-参数测试)
- **ArkUI 参数测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#1-参数测试)
- **Ability 参数测试**：[examples/ability_examples.md](../examples/ability_examples.md#2-参数测试)
- **Accessibility 参数测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#2-功能测试)

> **提示**：每个子系统示例都包含完整的测试代码、N-API 封装和 ETS 测试实现。

#### 3.1.2 ERROR 测试（错误测试）

**定义**：测试 API 在错误情况下的异常处理

**测试场景**：
- 错误码返回
- 异常抛出
- 边界条件错误
- 系统级错误

**关键点**：
- 错误码覆盖
- 异常信息验证
- 错误恢复机制

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 错误测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#2-错误测试)
- **ArkUI 错误测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#2-错误测试)
- **Ability 错误测试**：[examples/ability_examples.md](../examples/ability_examples.md#3-错误测试)
- **Accessibility 错误测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#4-错误处理测试)

> **提示**：错误处理是测试的重要部分，确保所有可能的错误情况都被覆盖。

#### 3.1.3 RETURN 测试（返回值测试）

**定义**：测试 API 返回值的正确性

**测试场景**：
- 正常返回值
- 枚举值覆盖
- 布尔值覆盖（true/false）
- 复杂对象返回

**关键点**：
- 返回值类型验证
- 返回值内容验证
- 返回值一致性检查

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 返回值测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#3-返回值测试)
- **ArkUI 返回值测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#3-返回值测试)
- **Ability 返回值测试**：[examples/ability_examples.md](../examples/ability_examples.md#1-基础功能测试)
- **Accessibility 返回值测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#1-基础功能测试)

> **提示**：返回值测试确保 API 的行为符合预期，是功能正确性的重要保证。

#### 3.1.4 BOUNDARY 测试（边界测试）

**定义**：测试 API 在边界值和极限情况下的行为

**测试场景**：
- 最大值/最小值
- 空指针/空字符串
- 数组越界
- 时间边界

**关键点**：
- 边界值验证
- 极限情况处理
- 稳定性测试

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 边界测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#4-边界测试)
- **ArkUI 边界测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#4-边界测试)
- **Ability 边界测试**：[examples/ability_examples.md](../examples/ability_examples.md#3-边界测试)
- **Accessibility 边界测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#3-边界测试)

> **提示**：边界测试确保 API 在极限情况下的稳定性，是测试中非常重要的一环。

#### 3.1.5 MEMORY 测试（内存测试）

**定义**：测试 API 的内存管理和内存泄漏

**测试场景**：
- 内存分配/释放
- 内存泄漏检测
- 内存越界访问
- 大内存处理

**关键点**：
- 内存管理验证
- 泄漏检测
- 性能影响

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 内存测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#5-内存测试)
- **ArkUI 内存测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#5-内存测试)
- **Ability 内存测试**：[examples/ability_examples.md](../examples/ability_examples.md#5-内存管理测试)
- **Accessibility 内存测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#5-内存管理测试)

> **提示**：内存泄漏检测是 CAPI 测试中的重要环节，应结合 valgrind 等工具进行验证。

### 3.2 高级测试类型

#### 3.2.1 并发测试

**定义**：测试 API 在并发环境下的行为

**测试场景**：
- 多线程调用
- 异步操作
- 竞态条件
- 死锁检测

**子系统示例**：
```typescript
// BundleManager 并发测试
it('BundleManager_Concurrent_Access', TestType.FUNCTION | Size.LARGETEST | Level.LEVEL2,
  async (done: Function) => {
  try {
    const promises = [];
    const concurrentCount = 10;
    
    // 并发安装测试
    for (let i = 0; i < concurrentCount; i++) {
      let promise = new Promise((resolve) => {
        setTimeout(() => {
          let result = testNapi.BundleManager_Install('com.example.app');
          expect(result).assertEqual(0);
          resolve();
        }, Math.random() * 1000);
      });
      promises.push(promise);
    }
    
    await Promise.all(promises);
    hilog.info(DOMAIN, 'BundleManagerTest', 'Concurrent test passed');
    done();
  } catch (err) {
    let errMsg = (err as BusinessError).message;
    hilog.error(DOMAIN, 'BundleManagerTest', `Concurrent test failed: ${errMsg}`);
    done();
  }
})
```

#### 3.2.2 性能测试

**定义**：测试 API 的性能表现

**测试场景**：
- 执行时间测量
- 资源消耗统计
- 吞吐量测试
- 响应时间测试

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 性能测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#7-性能测试)
- **ArkUI 性能测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#6-性能测试)
- **Ability 性能测试**：[examples/ability_examples.md](../examples/ability_examples.md#6-性能测试)
- **Accessibility 性能测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#6-性能测试)

#### 3.2.3 稳定性测试

**定义**：测试 API 的长期稳定性

**测试场景**：
- 长时间运行
- 压力测试
- 异常恢复
- 内存压力测试

**子系统示例**：
详细的子系统测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 稳定性测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#8-稳定性测试)
- **ArkUI 稳定性测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#13-稳定性测试)
- **Ability 稳定性测试**：[examples/ability_examples.md](../examples/ability_examples.md#13-稳定性测试)
- **Accessibility 稳定性测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#13-稳定性测试)

> **提示**：性能和稳定性测试确保 API 在高负载和长期运行环境下的可靠性。

## 四、测试规范和最佳实践

### 4.1 命名规范

#### 4.1.1 测试套命名

**格式**：`Acts[子系统][模块][功能]`

**示例**：
- `ActsBundleManagerInstallTest` - BundleManager 安装测试
- `ActsArkUIComponentTest` - ArkUI 组件测试
- `ActsAbilityStartTest` - Ability 启动测试

**子系统参考**：
| 子系统 | 测试套名称示例 | 说明 |
|--------|---------------|------|
| BundleManager | `ActsBundleManagerInstallTest` | 包管理安装测试套 |
| ArkUI | `ActsArkUIComponentTest` | ArkUI 组件测试套 |
| Ability | `ActsAbilityStartTest` | Ability 启动测试套 |
| Accessibility | `ActsAccessibilityTest` | 辅助功能测试套 |

#### 4.1.2 测试用例命名

**格式**：`[测试类型]_[具体场景]_[预期结果]`

**示例**：
- `Normal_BasicFunction_Success` - 正常场景基础功能成功
- `Error_InvalidParameter_Fail` - 错误场景无效参数失败
- `Boundary_MaxValue_Success` - 边界场景最大值成功
- `Memory_NoLeak_Success` - 内存场景无泄漏成功

**子系统示例**：
```typescript
// BundleManager 命名示例
it('BundleManager_Install_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done) => {``})
it('BundleManager_Install_InvalidParam_Fail', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1, async (done) => {`})
it('BundleManager_Uninstall_Boundary_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done) => {`})

// ArkUI 命名示例
it('ArkUI_Render_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done) => {`})
it('ArkUI_Click_InvalidComponent_Fail', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1, async (done) => {`})
it('ArkUI_SetText_Boundary_Success', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (done) => {`})
```

#### 4.1.3 N-API 函数命名

**格式**：`[子系统名称]_[功能名称]`

**示例**：
```cpp
// N-API 函数命名
static napi_value BundleManager_Install(napi_env env, napi_callback_info info);
static napi_value BundleManager_Uninstall(napi_env env, napi_callback_info info);
static napi_value ArkUI_Render(napi_env env, napi_callback_info info);
static napi_value ArkUI_Click(napi_env env, napi_callback_info info);
```

### 4.2 代码规范

#### 4.2.1 N-API 封装规范

**基本原则**：
- 使用 `napi_throw_error` 抛出异常（强制要求）
- 确保内存分配和释放配对
- 参数类型验证完整
- 错误处理全面

**N-API 封装示例**：
详细的 N-API 封装示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager N-API 封装**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#9-n-api-封装示例)
- **ArkUI N-API 封装**：[examples/arkui_examples.md](../examples/arkui_examples.md#7-n-api-封装示例)
- **Ability N-API 封装**：[examples/ability_examples.md](../examples/ability_examples.md#8-n-api-封装示例)
- **Accessibility N-API 封装**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#8-n-api-封装示例)

> **提示**：N-API 封装应遵循统一的错误处理规范，强制使用 `napi_throw_error` 抛出异常。

#### 4.2.2 ETS 测试代码规范

**基本原则**：
- 使用 Try-Catch 包裹异常
- 使用 `expect` 进行断言
- 记录详细的测试日志
- 处理异步操作

**ETS 测试示例**：
详细的 ETS 测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager ETS 测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#10-ets-测试示例)
- **ArkUI ETS 测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#8-ets-测试示例)
- **Ability ETS 测试**：[examples/ability_examples.md](../examples/ability_examples.md#9-ets-测试示例)
- **Accessibility ETS 测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#9-ets-测试示例)

> **提示**：ETS 测试应使用 Try-Catch 包裹异常，使用 `expect` 进行断言，记录详细的测试日志。

### 4.3 断言使用规范

#### 4.3.1 基本断言

| 断言方法 | 用途 | 子系统示例 |
|---------|------|----------|
| `assertEqual` | 值相等 | `expect(result).assertEqual(0)` |
| `assertTrue` | 布尔为真 | `expect(flag).assertTrue()` |
| `assertFalse` | 布尔为假 | `expect(isInvalid).assertFalse()` |
| `assertNull` | 值为 null | `expect(value).assertNull()` |
| `assertUndefined` | 值为 undefined | `expect(result).assertUndefined()` |
| `assertNotNull` | 值不为 null | `expect(result).assertNotNull()` |

**子系统示例**：
详细的断言使用示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 断言示例**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#11-断言示例)
- **ArkUI 断言示例**：[examples/arkui_examples.md](../examples/arkui_examples.md#9-断言示例)
- **Ability 断言示例**：[examples/ability_examples.md](../examples/ability_examples.md#10-断言示例)
- **Accessibility 断言示例**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#10-断言示例)

#### 断言使用规范

| 断言方法 | 用途 | 子系统示例 |
|---------|------|----------|
| `assertEqual` | 值相等 | `expect(result).assertEqual(0)` |
| `assertTrue` | 布尔为真 | `expect(flag).assertTrue()` |
| `assertFalse` | 布尔为假 | `expect(isInvalid).assertFalse()` |
| `assertNull` | 值为 null | `expect(value).assertNull()` |
| `assertUndefined` | 值为 undefined | `expect(result).assertUndefined()` |
| `assertNotNull` | 值不为 null | `expect(result).assertNotNull()` |
| `assertLarger` | 大于 | `expect(version1).assertLarger(version2)` |
| `assertLess` | 小于 | `expect(count).assertLess(100)` |
| `assertContain` | 包含元素 | `expect(array).assertContain(item)` |
| `assertDeepEquals` | 深度相等 | `expect(obj1).assertDeepEquals(obj2)` |

> **提示**：断言应覆盖所有关键业务逻辑，确保测试的全面性。

#### 4.3.2 比较断言

| 断言方法 | 用途 | 子系统示例 |
|---------|------|----------|
| `assertLarger` | 大于 | `expect(version1).assertLarger(version2)` |
| `assertLess` | 小于 | `expect(count).assertLess(100)` |
| `assertLargerOrEqual` | 大于等于 | `expect(size).assertLargerOrEqual(minSize)` |
| `assertLessOrEqual` | 小于等于 | `expect(load).assertLessOrEqual(maxLoad)` |
| `assertClose` | 接近（误差范围内） | `expect(value).assertClose(expected, 0.01)` |

**子系统示例**：
```typescript
// BundleManager 比较断言
it('BundleManager_CompareVersion', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let version1 = testNapi.BundleManager_GetVersion('app1');
      let version2 = testNapi.BundleManager_GetVersion('app2');
      
      expect(version1).assertLarger(version2); // 版本 1 大于版本 2
      
      let appSize = testNapi.BundleManager_GetSize('com.example.app');
      expect(appSize).assertLess(100 * 1024 * 1024); // 应用大小小于 100MB
      
      done();
    } catch (err) {
      done();
    }
  })

// ArkUI 比较断言
it('ArkUI_PerformanceCheck', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let startTime = performance.now();
      testNapi.ArkUI_Render('componentId');
      let endTime = performance.now();
      
      expect(endTime - startTime).assertLess(100); // 渲染时间小于 100ms
      
      let fps = testNapi.ArkUI_GetFPS();
      expect(fps).assertLargerOrEqual(60); // FPS 大于等于 60
      
      done();
    } catch (err) {
      done();
    }
  })
```

#### 4.3.3 集合断言

| 断言方法 | 用途 | 子系统示例 |
|---------|------|----------|
| `assertContain` | 包含元素 | `expect(array).assertContain(item)` |
| `assertDeepEquals` | 深度相等 | `expect(obj1).assertDeepEquals(obj2)` |

**子系统示例**：
```typescript
// BundleManager 集合断言
it('BundleManager_GetList', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let appList = testNapi.BundleManager_GetInstalledApps();
      expect(appList).assertNotNull();
      
      // 断言应用列表包含预期应用
      expect(appList).assertContain('com.example.app');
      expect(appList).assertContain('com.system.settings');
      
      done();
    } catch (err) {
      done();
    }
  })

// ArkUI 集合断言
it('ArkUI_ComponentProperties', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      let expectedProps = {
        visible: true,
        enabled: true,
        text: 'Hello World'
      };
      
      let actualProps = testNapi.ArkUI_GetProps('componentId');
      expect(actualProps).assertDeepEquals(expectedProps);
      
      done();
    } catch (err) {
      done();
    }
  })
```

#### 4.3.4 异常断言

| 断言方法 | 用途 | 子系统示例 |
|---------|------|----------|
| `assertThrowError` | 抛出异常 | `expect(() => func()).assertThrowError('error')` |
| `assertPromiseIsRejected` | Promise 被拒绝 | `await expect(promise).assertPromiseIsRejected()` |

**子系统示例**：
```typescript
// BundleManager 异常断言
it('BundleManager_ThrowError', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      // 测试空参数抛出异常
      let result = testNapi.BundleManager_Install('');
      expect(result).assertNotEqual(0); // 断言失败返回
      
      // 测试不存在的应用抛出异常
      let uninstallResult = testNapi.BundleManager_Uninstall('nonexistent.app');
      expect(uninstallResult).assertNotEqual(0);
      
      done();
    } catch (err) {
      // 预期会有 BusinessError 异常
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      expect(code).assertEqual('ERROR_CODE');
      done();
    }
  })

// ArkUI 异常断言
it('ArkUI_ThrowError', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
  async (done: Function) => {
    try {
      // 测试无效组件 ID 抛出异常
      let result = testNapi.ArkUI_Render('invalid.component.id');
      expect(result).assertFalse();
      
      // 测试重复渲染抛出异常
      let renderResult = testNapi.ArkUI_Render('componentId');
      expect(renderResult).assertFalse(); // 第二次渲染应该失败
      
      done();
    } catch (err) {
      let errMsg = (err as BusinessError).message;
      let code = (err as BusinessError).code;
      expect(code).assertEqual('ERROR_CODE');
      done();
    }
  })
```

### 4.4 错误处理规范

#### 4.4.1 N-API 层错误处理

**基本原则**：
- 使用 `napi_throw_error` 抛出异常（强制要求）
- 包含错误码和错误信息
- 确保资源正确释放

**子系统示例**：
详细的错误处理示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager N-API 错误处理**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#12-napi-错误处理)
- **ArkUI N-API 错误处理**：[examples/arkui_examples.md](../examples/arkui_examples.md#11-napi-错误处理)
- **Ability N-API 错误处理**：[examples/ability_examples.md](../examples/ability_examples.md#11-napi-错误处理)
- **Accessibility N-API 错误处理**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#11-napi-错误处理)

#### 4.4.2 ETS 层错误处理

**基本原则**：
- 使用 Try-Catch 捕获异常
- 记录详细的错误信息
- 断言错误码

**子系统示例**：
详细的 ETS 错误处理示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager ETS 错误处理**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#12-错误处理)
- **ArkUI ETS 错误处理**：[examples/arkui_examples.md](../examples/arkui_examples.md#12-错误处理)
- **Ability ETS 错误处理**：[examples/ability_examples.md](../examples/ability_examples.md#11-错误处理)
- **Accessibility ETS 错误处理**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#11-错误处理)

> **提示**：错误处理应完整覆盖所有可能的错误场景，包括参数验证、系统级错误和异常情况。

### 4.5 日志记录规范

#### 4.5.1 日志级别

| 级别 | 用途 | 使用场景|
|------|------|----------|
| `hilog.info` | 正常信息 | 测试开始、成功完成 |
| `hilog.error` | 错误信息 | 测试失败、异常情况 |
| `hilog.debug` | 调试信息 | 详细的过程信息 |
| `hilog.warn` | 警告信息 | 边界情况、潜在问题 |

#### 4.5.2 日志格式

**子系统示例**：
详细的日志记录示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 日志示例**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#13-日志记录示例)
- **ArkUI 日志示例**：[examples/arkui_examples.md](../examples/arkui_examples.md#12-日志记录示例)
- **Ability 日志示例**：[examples/ability_examples.md](../examples/ability_examples.md#12-日志记录示例)
- **Accessibility 日志示例**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#12-日志记录示例)

> **提示**：日志记录应遵循分级原则，使用合适的日志级别记录关键信息，便于调试和问题排查。

## 五、测试执行和调试

### 5.1 测试执行方式

#### 5.1.1 命令行执行

**基本命令**：
```bash
# 执行所有测试用例
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner

# 执行指定测试套
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s class <testSuite>

# 执行指定测试用例
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s class <testSuite>#<testCase>
```

**子系统示例**：
```bash
# BundleManager 测试执行
hdc shell aa test -b com.example.bundlemanger.test -m entry -s unittest OpenHarmonyTestRunner -s class ActsBundleManagerInstallTest

# ArkUI 测试执行
hdc shell aa test -b com.example.arkui.test -m entry -s unittest OpenHarmonyTestRunner -s class ActsArkUIComponentTest
```

**高级选项**：
```bash
# 设置超时时间
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s timeout 15000

# 遇错即停模式
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s breakOnError true

# 随机执行
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s random true

# 压力测试
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s stress 1000

# 按测试级别筛选
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s level 0

# 按测试规模筛选
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s size small
```

#### 5.1.2 DevEco Studio 执行

**执行方式**：
- 测试包级别执行
- 测试类级别执行
- 测试套级别执行
- 测试用例级别执行

### 5.2 测试结果查看

#### 5.2.1 日志输出格式

**测试开始**：
```
OHOS_REPORT_STATUS: class=ActsBundleManagerInstallTest
OHOS_REPORT_STATUS: current=1
OHOS_REPORT_STATUS: id=JS
OHOS_REPORT_STATUS: numtests=447
OHOS_REPORT_STATUS: stream=
OHOS_REPORT_STATUS: test=BundleManager_Install_Success
OHOS_REPORT_STATUS_CODE: 1
```

**测试成功**：
```
OHOS_REPORT_STATUS: class=ActsBundleManagerInstallTest
OHOS_REPORT_STATUS: current=1
OHOS_REPORT_STATUS: id=JS
OHOS_REPORT_STATUS: numtests=447
OHOS_REPORT_STATUS: stream=
OHOS_REPORT_STATUS: test=BundleManager_Install_Success
OHOS_REPORT_STATUS_CODE: 0
OHOS_REPORT_STATUS: consuming=4
```

**测试失败**：
```
OHOS_REPORT_STATUS: class=ActsBundleManagerInstallTest
OHOS_REPORT_STATUS: current=1
OHOS_REPORT_STATUS: id=JS
OHOS_REPORT_STATUS: numtests=447
OHOS_REPORT_STATUS: stream=Test failed assertion error
OHOS_REPORT_STATUS: test=BundleManager_Install_Success
OHOS_REPORT_STATUS_CODE: -1
```

#### 5.2.2 最终结果汇总

```bash
OHOS_REPORT_RESULT: stream=Tests run: 447, Failure: 0, Error: 1, Pass: 201, Ignore: 245
OHOS_REPORT_CODE: 0
```

### 5.3 测试调试技巧

#### 5.3.1 常见调试问题

**问题1：N-API 函数找不到**
- 检查模块注册是否正确
- 验证函数名称是否匹配
- 确认库文件路径正确

**问题2：参数类型不匹配**
- 检查 `napi_get_value_*` 的类型是否正确
- 验证参数是否为预期的类型
- 使用 `napi_typeof` 进行类型检查

**问题3：内存泄漏**
- 使用 `valgrind` 进行内存检测
- 确保所有 `malloc` 都有对应的 `free`
- 检查 N-API 引用管理

**问题4：测试用例失败**
- 检查断言条件是否正确
- 验证预期值和实际值
- 查看详细的错误信息

#### 5.3.2 调试工具

**日志分析**：
```bash
hdc shell hilog | grep BundleManagerTest
hdc shell hilog | grep ArkUITest
```

**子系统日志示例**：
```bash
# BundleManager 日志过滤
hdc shell hilog | grep -E "BundleManagerTest|BundleManager"

# ArkUI 日志过滤
hdc shell hilog | grep -E "ArkUITest|ArkUI"
```

## 六、测试覆盖和性能

### 6.1 测试覆盖率

#### 6.1.1 覆盖率类型

| 类型 | 说明 | 子系统示例 |
|------|------|----------|
| **代码覆盖率** | 代码行被执行的比例 | BundleManager 核心功能 ≥ 90% |
| **分支覆盖率** | 代码分支被执行的比例 | ArkUI 渲染路径 ≥ 80% |
| **函数覆盖率** | 函数被调用的比例 | CAPI 函数覆盖率 ≥ 85% |
| **参数覆盖率** | 参数组合被测试的比例 | API 参数组合覆盖率 ≥ 75% |

#### 6.1.2 覆盖率标准

**子系统覆盖率标准**：

| 子系统 | 代码覆盖率 | 分支覆盖率 | 函数覆盖率 |
|--------|-----------|-----------|-----------|
| BundleManager | ≥ 90% | ≥ 80% | ≥ 85% |
| ArkUI | ≥ 85% | ≥ 75% | ≥ 80% |
| Ability | ≥ 90% | ≥ 80% | ≥ 85% |
| Accessibility | ≥ 80% | ≥ 70% | ≥ 75% |

### 6.2 性能测试

#### 6.2.1 性能指标

| 指标 | 说明 | 子系统示例 |
|------|------|----------|
| **响应时间** | 函数执行时间 | BundleManager 安装时间 < 5s |
| **内存使用** | 内存消耗量 | ArkUI 组件渲染内存 < 50MB |
| **CPU 使用率** | CPU 占用率 | Ability 启动 CPU < 30% |
| **吞吐量** | 单位时间处理请求数 | API 调用吞吐量 > 100/s |

#### 6.2.2 性能测试示例

**子系统性能测试**：
详细的性能测试示例请参考 [examples/](../examples/) 目录中的具体实现：

- **BundleManager 性能测试**：[examples/bundlemanager_examples.md](../examples/bundlemanager_examples.md#7-性能测试)
- **ArkUI 性能测试**：[examples/arkui_examples.md](../examples/arkui_examples.md#6-性能测试)
- **Ability 性能测试**：[examples/ability_examples.md](../examples/ability_examples.md#6-性能测试)
- **Accessibility 性能测试**：[examples/accessibility_examples.md](../examples/accessibility_examples.md#6-性能测试)

> **提示**：性能测试应关注执行时间、内存消耗、CPU 使用率和吞吐量等关键指标。

---

## 七、最佳实践总结

### 7.1 开发流程最佳实践

1. **需求分析**：明确测试范围和测试目标
2. **测试设计**：制定测试策略和测试计划
3. **用例编写**：遵循命名规范和代码规范
4. **测试执行**：使用合适的执行方式和参数
5. **结果分析**：分析测试结果和覆盖率
6. **持续优化**：根据测试结果持续改进

### 7.2 代码质量最佳实践

1. **代码规范**：遵循统一的代码风格和规范
2. **错误处理**：完整的错误处理机制（N-API 使用 `napi_throw_error`）
3. **内存管理**：正确的内存分配和释放
4. **断言完整**：全面的断言覆盖
5. **日志详细**：详细的日志记录

### 7.3 测试维护最佳实践

1. **定期更新**：根据代码变更及时更新测试用例
2. **版本控制**：使用版本控制系统管理测试代码
3. **自动化**：建立自动化测试流程
4. **文档更新**：及时更新测试文档
5. **团队协作**：建立团队协作机制

---

**版本**: 3.0.0  
**创建日期**: 2026-03-06  
**更新日期**: 2026-03-19  
**兼容性**: OpenHarmony API 10+
