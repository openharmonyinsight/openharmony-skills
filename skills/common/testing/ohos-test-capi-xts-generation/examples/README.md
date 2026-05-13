# CAPI XTS 测试用例示例

> **说明**：本目录包含 OpenHarmony CAPI (Native C API) XTS 测试的完整示例，涵盖多个核心子系统

## 目录结构

```
examples/
├── bundlemanager_examples.md      # BundleManager (包管理) 子系统示例
├── arkui_examples.md              # ArkUI (UI 框架) 子系统示例
├── ability_examples.md            # Ability (应用能力) 子系统示例
└── accessibility_examples.md     # Accessibility (辅助功能) 子系统示例
```

## 使用说明

### 1. 选择相应的子系统示例

根据您需要测试的子系统，选择对应的示例文件：

- **BundleManager**：应用安装、卸载、信息获取等包管理功能
- **ArkUI**：界面渲染、组件交互、动画等 UI 功能
- **Ability**：应用启动、生命周期、数据传递等应用能力
- **Accessibility**：朗读、缩放、颜色反转等辅助功能

### 2. 测试类型覆盖

每个子系统示例都包含以下测试类型：

#### 基础测试类型
- **PARAM 测试**：参数验证测试
- **ERROR 测试**：错误处理测试
- **RETURN 测试**：返回值验证测试
- **BOUNDARY 测试**：边界条件测试
- **MEMORY 测试**：内存管理测试

#### 高级测试类型
- **并发测试**：多线程环境下的行为测试
- **性能测试**：执行时间和资源消耗测试
- **稳定性测试**：长期运行和压力测试

### 3. 核心组件示例

每个子系统示例都提供：

#### N-API 封装示例
- 完整的 C++ N-API 实现代码
- 参数验证、类型检查、错误处理
- 内存管理最佳实践

#### ETS 测试示例
- 完整的 TypeScript 测试代码
- Hypium 测试框架使用规范
- 套件和用例组织结构

#### 断言使用示例
- 基本断言、比较断言、集合断言
- 异常断言、边界断言
- 实际应用场景示例

### 4. 代码规范遵循

所有示例都严格遵循：

#### 命名规范
- **测试套**：`Acts[子系统][模块][功能]`
- **测试用例**：`[测试类型]_[具体场景]_[预期结果]`
- **N-API 函数**：`[子系统名称]_[功能名称]`

#### 错误处理规范
- N-API 层：强制使用 `napi_throw_error`
- ETS 层：Try-Catch 包裹，详细错误信息记录

#### 日志记录规范
- 使用 hilog 进行日志输出
- 不同级别：info、error、debug、warn
- 详细的过程记录和状态跟踪

### 5. 测试执行方式

#### 命令行执行
```bash
# 执行所有测试用例
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner

# 执行指定测试套
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s class <testSuite>

# 执行指定测试用例
hdc shell aa test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s class <testSuite>#<testCase>
```

#### 开发工具执行
- 使用 DevEco Studio 进行测试执行
- 支持包级别、类级别、套级别、用例级别执行

### 6. 调试和问题排查

#### 常见调试问题
1. **N-API 函数找不到**：检查模块注册和函数名称
2. **参数类型不匹配**：验证类型检查和转换
3. **内存泄漏**：使用 valgrind 进行内存检测
4. **测试用例失败**：检查断言条件和预期值

#### 日志分析
```bash
# 过滤特定子系统的日志
hdc shell hilog | grep -E "BundleManagerTest|BundleManager"
hdc shell hilog | grep -E "ArkUITest|ArkUI"
hdc shell hilog | grep -E "AbilityTest|Ability"
hdc shell hilog | grep -E "AccessibilityTest|Accessibility"
```

### 7. 最佳实践建议

#### 开发流程
1. **需求分析**：明确测试范围和目标
2. **测试设计**：制定测试策略和计划
3. **用例编写**：遵循命名规范和代码规范
4. **测试执行**：使用合适的执行方式
5. **结果分析**：分析测试结果和覆盖率
6. **持续优化**：根据测试结果改进

#### 代码质量
1. **代码规范**：统一的代码风格和规范
2. **错误处理**：完整的错误处理机制
3. **内存管理**：正确的内存分配和释放
4. **断言完整**：全面的断言覆盖
5. **日志详细**：详细的日志记录

#### 测试维护
1. **定期更新**：根据代码变更及时更新
2. **版本控制**：使用版本控制系统管理
3. **自动化**：建立自动化测试流程
4. **文档更新**：及时更新测试文档
5. **团队协作**：建立团队协作机制

## 相关文档

- [CAPI 测试框架指南](../modules/conventions/hypium_framework_c.md) - 完整的测试框架定义和规范
- [N-API 和 ETS 公共模式](../modules/conventions/test_patterns_napi_ets.md) - N-API 封装和 ETS 测试的公共模式
- [测试生成核心](../modules/L2_Generation/test_generation_c.md) - 测试用例生成核心文档

## 兼容性

- **OpenHarmony API 版本**：API 10+
- **测试框架**：Hypium
- **开发工具**：DevEco Studio
- **测试设备**：OpenHarmony 兼容设备

## 版本信息

- **版本**：3.0.0
- **创建日期**：2026-03-06
- **更新日期**：2026-03-19
- **维护者**：OpenHarmony CAPI XTS 测试团队