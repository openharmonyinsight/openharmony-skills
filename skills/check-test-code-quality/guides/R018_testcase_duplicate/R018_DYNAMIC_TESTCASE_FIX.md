# R018规则修复 - 动态拼接testcase问题

## 问题描述

### 问题1：动态拼接的testcase
- **现象**：testcase名称使用动态拼接，如 `'test' + nameA + 'IdProp'`）
- **影响**：
  1. R018重复检测无法识别动态拼接的testcase名称
  2. 修复工具无法正确替换动态拼接的字符串

### 问题2：@tc.name与it()名称不一致
- **现象**：修复后`@tc.name`与`it()`中的名称不一致
- **原因**：
  1. 修复工具只修改了`it()`中的名称，没有同步修改`@tc.name`
  2. @tc.name缺少"test"前缀
- **规范要求**：`@tc.name`必须与`it()`中的名称**完全一致**

## 修复方案

### 方案1：将动态拼接改为静态字符串

**原则**：所有testcase名称必须使用静态字符串，不允许动态拼接

**修复步骤**：
1. 找到动态拼接变量的定义（如 `nameA = 'AnimateMotion'`）
2. 计算拼接后的完整字符串
3. 将`it()`中的动态拼接替换为静态字符串
4. 同步修改`@tc.name`为相同的静态字符串

**示例**：
```javascript
// ❌ 错误 - 动态拼接
var nameA = 'AnimateMotion';
/**
 * @tc.name   test' + nameA + 'IdProp
 */
it('test' + nameA + 'IdProp', Level.LEVEL0, async function(done) { ... })

// ✅ 正确 - 静态字符串
var nameA = 'AnimateMotion';
/**
 * @tc.name   testAnimateMotionIdProp
 */
it('testAnimateMotionIdProp', Level.LEVEL0, async function(done) { ... })
```

### 方案2：@tc.name命名规范

**原则**：`@tc.name`必须与`it()`中的名称完全一致

**规则**：
- `@tc.name`的值 = `it()`第一个参数的值（静态字符串）
- 不允许动态拼接
- 不允许省略"test"前缀

**示例**：
```javascript
// ❌ 错误 - @tc.name缺少test前缀
/**
 * @tc.name   AnimateMotionIdProp
 */
it('testAnimateMotionIdProp', Level.LEVEL0, async function(done) { ... })

// ✅ 正确 - @tc.name与it()一致
/**
 * @tc.name   testAnimateMotionIdProp
 */
it('testAnimateMotionIdProp', Level.LEVEL0, async function(done) { ... })
```

## 自动修复工具

**工具名称**: R018动态拼接修复工具

**功能**：
1. 检测动态拼接的testcase
2. 解析变量定义，计算静态值
3. 替换`it()`中的动态拼接为静态字符串
4. 同步替换`@tc.name`为相同的静态字符串
5. 处理重复testcase，添加Adapt后缀

**使用方法**：
```bash
# 仅扫描
/check-test-code-quality arkui --rules R018 --dry-run

# 扫描并修复
/check-test-code-quality arkui --rules R018 --fix
```

## 验证

### 验证步骤

1. **检查动态拼接是否已消除**：
   ```bash
   /check-test-code-quality arkui --rules R018 --check-dynamic
   ```

2. **检查@tc.name与it()是否一致**：
   ```bash
   /check-test-code-quality arkui --rules R018 --check-consistency
   ```

3. **检查testcase是否重复**：
   ```bash
   /check-test-code-quality arkui --rules R018
   ```

### 预期结果

- ✅ 无动态拼接的testcase
- ✅ `@tc.name`与`it()`名称完全一致
- ✅ 无testcase重复（或已添加Adapt后缀）

## 相关文档

- [R018修复指南](R018_FIX_GUIDE.md)
- [R018动态拼接修复总结](R018_DYNAMIC_FIX_SUMMARY.md)
- [R018规则示例](../../rules/R018/SKILL.md)

- [R018实现细节](../../rules/R018/SKILL.md)

## 更新记录

- **2026-03-12**：创建文档，分析动态拼接testcase问题和@tc.name不一致问题
