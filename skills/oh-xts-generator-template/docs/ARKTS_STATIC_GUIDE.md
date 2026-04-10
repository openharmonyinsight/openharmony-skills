# ArkTS 静态语言语法规范校验指南

> 本文档提供 ArkTS 静态语言语法规范的完整校验指南，包括语法特性、类型强校验规则和测试用例生成要求。

## 概述

ArkTS 静态语法是 OpenHarmony 提供的强类型语言规范，与传统的 ArkTS 动态语法有以下主要区别：

- **编译时类型检查**：启用严格的编译时类型检查
- **类型强校验**：类型错误在编译阶段暴露，而非运行时抛出 401 错误
- **禁止隐式转换**：所有类型必须有显式声明
- **字段必须初始化**：所有字段必须在声明时初始化

## 🔧 语法规范校验方式

在进行 ArkTS 静态语言语法规范校验时，**必须调用专门的 `arkts-static-spec` 技能**：

### 基本使用方式
```bash
请使用 arkts-static-spec 进行语法规范校验：
- 语法规则检查
- 类型系统验证
- 编译问题分析
- TypeScript 迁移指导
```

### 重要原则
- 严格遵守 `arkts-static-spec` 技能的使用原则
- 所有回答必须基于该技能的官方规范文档
- 不添加文档之外的假设或推断
- 将 ArkTS 视为独立的静态语言，不是 TypeScript 的超集

## 类型强校验特性

### 1. 编译时类型检查

```typescript
// 动态语法 - 运行时 401 错误
it('should throw 401 for invalid parameter', () => {
  expect(() => {
    apiCall(invalidTypeParam); // 运行时抛出 401
  }).toThrowError('401');
});

// 静态语法 - 编译时错误
// 以下代码将无法通过编译
apiCall(invalidTypeParam); // 编译错误：类型不匹配
```

### 2. 入参类型不匹配处理

- **动态语法**：运行时抛出 401 错误码
- **静态语法**：编译时直接报错，无法通过编译

### 3. 类型推断禁用

- 不允许隐式类型推断
- 所有类型必须显式声明
- 禁止使用 any 类型

## 测试用例生成要求

### 1. 严格类型匹配

所有参数类型必须与 `.d.ts` 声明完全一致，不允许类型转换或隐式匹配。

### 2. 错误处理策略

由于类型错误在编译阶段暴露，不需要设计运行时 401 错误码测试。重点测试：

- 有效类型范围内的边界值
- 类型兼容性（允许的显式转换）
- 类型约束（泛型类型参数）

### 3. 边界值测试

重点测试有效类型范围内的边界值，而非无效类型：

```typescript
// 推荐：测试有效边界值
it('should handle maximum valid value', () => {
  const maxValue = Number.MAX_SAFE_INTEGER;
  expect(apiCall(maxValue)).toBe(expectedResult);
});

// 不推荐：测试无效类型（无法编译）
// it('should throw error for invalid type', () => {
//   expect(() => apiCall("invalid")).toThrow();
// });
```

### 4. 类型转换测试

如需类型转换，必须使用显式的类型转换语法：

```typescript
// 推荐：显式类型转换
const result = apiCall(param as TargetType);

// 不推荐：隐式类型转换（编译错误）
const result = apiCall(param); // 类型不匹配
```

## 规范文档参考

详细的 ArkTS 静态语言语法规范请参考：

- [类型系统](../references/arkts-static-spec/spec/types.md)
- [类和接口](../references/arkts-static-spec/spec/classes.md)
- [表达式](../references/arkts-static-spec/spec/expressions.md)
- [语句](../references/arkts-static-spec/spec/statements.md)
- [泛型](../references/arkts-static-spec/spec/generics.md)
- [注解](../references/arkts-static-spec/spec/annotations.md)

## 编译环境配置

### Windows 环境

Windows 环境下编译静态测试套需要：

1. 配置 JAVA_HOME 环境变量
2. 使用 `hvigorw.bat` 编译
3. 确保工程类型为静态语法

详细步骤请参考 [Windows 静态编译流程](../modules/L4_Build/build_workflow_windows.md#arkts-静态-xts-编译)

### Linux 环境

Linux 环境下编译静态测试套需要：

1. 确认 BUILD.gn 中使用 `ohos_js_app_static_suite()`
2. 添加 `xts_suitetype=hap_static` 编译参数
3. 可能需要替换 hvigor 工具版本

详细步骤请参考 [Linux 静态测试套编译](../modules/L4_Build/linux_compile_static_suite.md)

## 与动态语法的区别对比

| 特性 | 动态语法 | 静态语法 |
|------|---------|---------|
| 类型检查 | 运行时 | 编译时 |
| 错误处理 | 抛出 401 错误码 | 编译失败 |
| 类型推断 | 支持 | 禁止 |
| any 类型 | 允许 | 禁止 |
| 字段初始化 | 可选 | 必需 |
| 显式转换 | 可选 | 推荐 |

## 最佳实践

1. **始终使用显式类型声明**
2. **避免依赖类型推断**
3. **充分利用编译时类型检查**
4. **关注类型兼容性而非错误码**
5. **使用泛型提高代码复用性**