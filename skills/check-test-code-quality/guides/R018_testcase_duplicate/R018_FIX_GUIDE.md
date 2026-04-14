# R018 testcase重复修复指南

## 问题描述

一个describe下不允许testcase（@tc.name）重复。

## 修复规则

1. **命名格式**: `{原testcase名称}Adapt{三位数字}`
2. **数字递增规则**: 从001开始
3. **示例**:
    - 添加Adapt001后缀
    - 如果已有则使用002
4. **保留首个**: 保留第一个出现的testcase名称不变
5. **同步更新**: **必须同步更新** `@tc.name` 注释，保持与testcase名称一致

## 修复示例

```javascript
// 错误 - 编号格式不正确
it('File_Document_Choose_001adapt1', Level.LEVEL0, ...)

// 正确 - 使用Adapt
it('File_Document_Choose_001Adapt001', Level.LEVEL0, ...)
```

## 动态拼接testcase修复

### 问题说明

动态拼接的testcase无法被正确识别和修复。

### 修复方案

将动态拼接改为静态字符串，同步修改@tc.name，保持与it()名称一致（包括test前缀）。

### 修复规则

1. **禁止动态拼接**: 所有testcase名称必须使用静态字符串
2. **@tc.name必须一致**: @tc.name的值必须与it()第一个参数完全一致（包括test前缀）
3. **计算静态值**: 解析变量定义，计算拼接后的完整字符串
4. **处理重复**: 如果存在重复，在静态字符串后追加Adapt后缀
5. **@tc.name同步**: 添加相同的adapt后缀

### 修复示例

```javascript
// 错误 - 动态拼接
var nameA = 'AnimateMotion';
/**
 * @tc.name   AnimateMotionIdProp
 * @tc.number SUB_ACE_BASIC_COMPONENT_JS_API_0100
 */
it('test' + nameA + 'IdProp', Level.LEVEL0, async function(done) { ... })

// 正确 - 静态字符串
var nameA = 'AnimateMotion';
/**
 * @tc.name   testAnimateMotionIdProp
 * @tc.number SUB_ACE_BASIC_COMPONENT_JS_API_0100
 */
it('testAnimateMotionIdProp', Level.LEVEL0, async function(done) { ... })
```

## 验证方法

1. **检查动态拼接**
```bash
grep -r " + nameA + " --include="*.test.js" arkui/
```
2. **检查@tc.name与it()一致性**
```bash
/check-test-code-quality arkui --rules R018 --check-consistency
```
3. **检查testcase重复**
```bash
/check-test-code-quality arkui --rules R018
```

预期结果：无输出

## 技术实现细节

1. **变量提取**: 支持单行和多行变量定义
2. **变量替换**: 按变量名长度降序排序，避免先匹配短变量名导致长变量名匹配错误
3. **@tc.name一致性**: @tc.name的值必须与it()第一个参数完全一致

## 注意事项

1. **多行it()**: 当前工具不支持多行it()的检测
2. **模板字符串**: 不支持模板字符串
3. **复杂拼接**: 不支持复杂的字符串拼接

## 相关文档

- [R018动态拼接修复技术说明](R018_DYNAMIC_TESTCASE_FIX.md)
- [R018动态拼接修复总结](R018_DYNAMIC_FIX_SUMMARY.md)
