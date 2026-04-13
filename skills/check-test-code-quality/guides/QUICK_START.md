# 快速开始指南

> **5分钟快速上手XTS测试代码质量检查工具**

## 🎯 目标

通过本指南，您将学会：
- ✅ 基本扫描操作
- ✅ 理解扫描结果
- ✅ 修复常见问题
- ✅ 生成质量报告

## 📋 前提条件

- 已安装opencode CLI
- 有XTS测试代码需要检查
- 了解基本的命令行操作

## 🚀 第一步：基本扫描

### 扫描当前目录
```bash
/check-test-code-quality
```

**预期结果**:
```
开始扫描XTS测试代码...
扫描文件: 1,234个
发现问题: 56个

# 代码质量检查报告

## 检查结果

- 扫描文件数: 1,234
- 发现问题数: 56
...
```

### 扫描指定目录
```bash
/check-test-code-quality ability/ability_runtime/
```

## 📊 第二步：理解结果

### 问题级别

#### Critical（严重）
必须立即修复的问题，可能导致：
- ❌ 测试失败
- ❌ 测试无效
- ❌ 违反规范

#### Warning（警告）
建议修复的问题，影响：
- ⚠️ 代码质量
- ⚠️ 可维护性
- ⚠️ 规范符合度

### 常见问题类型

#### 1. R003 - 恒真断言
```typescript
// ❌ 错误
expect(true).assertTrue();

// ✅ 正确
expect(actualValue).assertTrue();
expect(result).assertEqual(expected);
```

#### 2. R002 - 错误码类型错误
```typescript
// ❌ 错误
expect(error.code).assertEqual("401");

// ✅ 正确
expect(error.code).assertEqual(401);
```

#### 3. R003 - 缺少断言
```typescript
// ❌ 错误
it('testExample', () => {
    let result = someFunction();
    // 没有断言！
});

// ✅ 正确
it('testExample', () => {
    let result = someFunction();
    expect(result).assertEqual(expectedValue);
});
```

#### 4. R006 - 设备类型差异化
```typescript
// ❌ 错误
import deviceInfo from '@ohos.deviceInfo';
if (deviceInfo.deviceType === 'phone') {
    // 设备类型判断
}

// ✅ 正确
import { canIUse } from '@kit.ArkUI';
if (canIUse('SystemCapability.ArkUI.ArkUI.Full')) {
    // 能力判断
}
```

## 🔧 第三步：修复问题

### 查看详细报告
```bash
# Excel报告会自动生成在当前目录
ls *.xlsx
# 输出: xxx_quality_report.xlsx
```

### 打开Excel报告
报告包含两个工作表：
1. **代码质量检查报告** - 详细问题列表
2. **统计摘要** - 统计信息

### 修复示例

#### 修复R002问题
```typescript
// 找到文件: test.test.ets:123
// 原代码:
expect(error.code).assertEqual("401");

// 修复后:
expect(error.code).assertEqual(401);
```

#### 修复R003问题
```typescript
// 找到文件: test.test.ets:456
// 原代码:
it('testExample', () => {
    let result = someFunction();
});

// 修复后:
it('testExample', () => {
    let result = someFunction();
    expect(result).assertEqual(expectedValue);
});
```

## 🎨 第四步：高级功能

### 扫描特定规则
```bash
# 只扫描R001, R002, R003
/check-test-code-quality --rules R001,R002,R003
```

### 跳过某些规则
```bash
# 跳过R009和R014
/check-test-code-quality --skip-rules R009,R014
```

### 指定扫描级别
```bash
# 只扫描Critical级别
/check-test-code-quality --level critical

# 只扫描Warning级别
/check-test-code-quality --level warning

# 扫描所有级别
/check-test-code-quality --level all
```

### 自动修复
```bash
# 自动修复R002问题
/check-test-code-quality --rules R002 --fix
```

## 📈 第五步：持续改进

### 建立扫描流程
```bash
# 1. 开发前扫描
/check-test-code-quality --level critical

# 2. 修复Critical问题
# ... 手动修复 ...

# 3. 完整扫描
/check-test-code-quality --level all

# 4. 修复Warning问题
# ... 手动修复 ...
```

### 集成到CI/CD
```yaml
# .github/workflows/test-quality.yml
name: Test Code Quality Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check Test Code Quality
        run: |
          /check-test-code-quality --level critical
          if [ $? -ne 0 ]; then
            echo "发现Critical级别问题，请修复后再提交"
            exit 1
          fi
```

## 🎯 最佳实践

### ✅ 推荐做法
1. **定期扫描** - 每周至少扫描一次
2. **优先修复Critical** - 先解决严重问题
3. **自动化** - 集成到CI/CD流程
4. **代码审查** - 提交前扫描
5. **持续改进** - 跟踪问题趋势

### ❌ 避免做法
1. **忽略Warning** - Warning也会影响质量
2. **批量修复** - 应该逐个理解和修复
3. **不读文档** - 理解规则才能正确修复
4. **过度依赖自动修复** - 需要人工验证

## 📚 下一步学习

### 深入了解规则
- [rules/](../rules/) - 18个独立规则实现（含示例）

### 了解实现原理
- [rules/](../rules/) - 各规则实现细节

### 参考官方规范
- [兼容性测试代码设计和编码规范2.0.md](../references/兼容性测试代码设计和编码规范2.0.md)
- [用例低级问题.md](../references/用例低级问题.md)

## ❓ 常见问题

### Q1: 扫描速度慢怎么办？
**A**: 可以只扫描Critical级别或特定规则：
```bash
/check-test-code-quality --level critical
/check-test-code-quality --rules R001,R002,R003
```

### Q2: 如何确认修复是否正确？
**A**: 重新扫描并对比结果：
```bash
# 第一次扫描
/check-test-code-quality > report1.txt

# 修复后扫描
/check-test-code-quality > report2.txt

# 对比
diff report1.txt report2.txt
```

### Q3: Excel报告在哪里？
**A**: 默认在当前目录生成：
- 单目录: `{目录名}_quality_report.xlsx`
- 多目录: `xts_quality_report_{时间戳}.xlsx`

### Q4: 如何跳过某些文件？
**A**: 使用`.gitignore`风格的配置：
```json
// skill_config.json
{
  "excluded_dirs": [
    "node_modules",
    "dist",
    "build"
  ]
}
```

### Q5: 断言方法不全怎么办？
**A**: 当前支持18种断言方法：
```javascript
assertClose, assertContain, assertEqual, assertFail,
assertFalse, assertTrue, assertInstanceOf, assertLarger,
assertLess, assertNull, assertThrowError, assertUndefined,
assertNaN, assertNegUnlimited, assertPosUnlimited, assertDeepEquals,
assertLargerOrEqual, assertLessOrEqual
```

如果使用了其他断言方法，请更新`skill_config.json`。

## 🎉 恭喜！

您已经掌握了XTS测试代码质量检查工具的基本使用！

### 下一步
- 📖 阅读详细文档: [SKILL.md](../SKILL.md)
- 🔧 学习修复指南: [guides/FIX_GUIDE.md](FIX_GUIDE.md)
- 📚 查看规则示例: [rules/](../rules/)

---

**需要帮助？**
- 📖 查看 [SKILL.md](../SKILL.md)
- 📚 查看 [规则目录](../rules/)
- 🔧 查看 [修复指南](FIX_GUIDE.md)

**最后更新**: 2026-03-09
