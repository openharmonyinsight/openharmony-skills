# R018 动态拼接testcase修复总结

## 修复时间
2026-03-12

## 问题描述

在R018规则（testcase重复）修复过程中，发现以下问题：

### 问题1：动态拼接的testcase
- **现象**：testcase名称使用动态拼接，如 `'test' + nameA + 'IdProp'`
- **原因**：开发者为了复用变量，使用了字符串拼接
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

### 1. 技术方案

#### 变量提取
- 支持单行变量定义：`var nameA = 'AnimateMotion';`
- 支持多行变量定义：
  ```javascript
  var name = 'textPath',
      nameA = 'TextPath',
      labelName = 'textPath';
  ```

#### 变量替换
- 按变量名长度降序排序，避免先匹配短变量名导致长变量名匹配错误
- 使用词边界确保精确匹配变量名

#### 一致性修复
- @tc.name必须与it()第一个参数完全一致（包括test前缀）
- 去除前导/尾随空格

### 2. 修复工具

**工具名称**: R018动态拼接修复工具

**功能**：
1. 检测动态拼接的testcase
2. 解析变量定义，计算静态值
3. 替换`it()`中的动态拼接为静态字符串
4. 同步替换`@tc.name`为相同的静态字符串
5. 处理@tc.name与it()不一致的情况

**使用方法**：
```bash
# 扫描并修复
/check-test-code-quality arkui --rules R018 --fix

# 仅扫描不修复
/check-test-code-quality arkui --rules R018 --dry-run
```

## 修复结果

### arkui目录
- **扫描文件数**：16,904 个测试文件
- **发现动态拼接**：440 个
- **修复问题**：641 个（440动态拼接 + 201 @tc.name不一致）

### 验证结果
- ✅ 动态拼接testcase：0个
- ✅ testcase重复：0个
- ⚠️ @tc.name与it()不一致：431个（主要是多行it()导致的配对问题）

## 示例

### 修复前
```javascript
var nameA = 'AnimateMotion';

/**
 * @tc.name   AnimateMotionIdProp
 * @tc.number SUB_ACE_BASIC_COMPONENT_JS_API_0100
 */
it('test' + nameA + 'IdProp', Level.LEVEL0, async function(done) { ... })
```

### 修复后
```javascript
var nameA = 'AnimateMotion';

/**
 * @tc.name   testAnimateMotionIdProp
 * @tc.number SUB_ACE_BASIC_COMPONENT_JS_API_0100
 */
it('testAnimateMotionIdProp', Level.LEVEL0, async function(done) { ... })
```

## 注意事项

1. **多行it()**：当前工具不支持多行it()的检测，需要后续优化
2. **模板字符串**：不支持模板字符串（`` `test${nameA}IdProp` ``）
3. **复杂拼接**：不支持复杂的字符串拼接（如函数调用、三元表达式等）

## 相关文档

- [R018动态拼接修复技术说明](R018_DYNAMIC_TESTCASE_FIX.md)
- [R018规则示例](../../rules/R018/SKILL.md)
- [R018修复指南](R018_FIX_GUIDE.md)

## 更新记录

- **2026-03-12**：完成arkui目录的动态拼接testcase修复
