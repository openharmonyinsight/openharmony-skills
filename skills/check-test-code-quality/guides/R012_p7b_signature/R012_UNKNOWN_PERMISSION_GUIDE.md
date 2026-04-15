# R012问题：未知权限处理指南

## 概述

在修复R012问题时，可能会遇到未知权限（不在已知权限列表中的权限）。本文档说明如何正确处理这种情况。

## 什么是未知权限？

未知权限是指不在以下三个官方文档中的权限：
- [用户授权权限](https://gitcode.com/openharmony/docs/raw/master/zh-cn/application-dev/security/AccessToken/permissions-for-all-user.md) (A类)
- [所有应用可用权限](https://gitcode.com/openharmony/docs/raw/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md) (B类)
- [受限权限](https://gitcode.com/openharmony/docs/raw/master/zh-cn/application-dev/security/AccessToken/restricted-permissions.md) (C类)

## 未知权限的可能原因

1. **新添加的权限**：OpenHarmony新版本添加的权限，尚未更新到文档
2. **自定义权限**：应用自定义的权限
3. **企业特殊权限**：企业版应用的特殊权限
4. **权限名称变更**：权限名称已更新，但p7b文件使用旧名称
5. **文档更新延迟**：权限已存在，但文档未及时更新

## 自动修复脚本的处理流程

### 1. 检测到未知权限

```
============================================================
⚠️  发现未知权限 - 文件: ActsWindowEnterpriseTest/signature/openharmony_sx.p7b
============================================================
以下权限不在已知权限列表中：
  1. ohos.permission.CUSTOM_WINDOW_PERMISSION
  2. ohos.permission.ENTERPRISE_SPECIAL_ACCESS

当前配置：
  - apl: system_core
  - app-feature: hos_system_app
  - acls: {"allowed-acls": ["ohos.permission.CUSTOM_WINDOW_PERMISSION", ...]}
```

### 2. 提供参考信息

```
📚 参考信息：
  - 如果这些权限是新添加的或自定义权限，请确认其级别
  - normal级别：适用于大多数应用权限（推荐）
  - system_basic级别：适用于系统基础服务权限
  - system_core级别：禁止使用（仅系统核心服务）

权限级别说明：
  - normal：普通应用权限，不会影响系统和其他应用
  - system_basic：系统基础权限，需要签名证书支持
  - system_core：系统核心权限，仅限系统核心服务使用（禁止）
```

### 3. 请求用户确认

```
请确认配置方案：
  1. 使用 normal 级别（推荐，保守策略）
  2. 使用 system_basic 级别（如果权限较高）
  3. 跳过此文件（不修复）
  4. 查看权限详情（打开官方文档）

请选择 [1-4]: 
```

### 4. 根据用户选择执行

#### 选项1：使用normal级别（推荐）

**适用场景**：
- 不确定权限级别时
- 权限看起来是普通应用权限
- 保守策略，避免权限过高

**执行操作**：
```json
{
  "bundle-info": {
    "apl": "normal",
    "app-feature": "hos_normal_app"
  }
}
```

#### 选项2：使用system_basic级别

**适用场景**：
- 确认权限是系统基础服务权限
- 权限涉及系统关键功能
- 需要较高权限才能正常工作

**执行操作**：
```json
{
  "bundle-info": {
    "apl": "system_basic",
    "app-feature": "hos_normal_app"
  }
}
```

#### 选项3：跳过此文件

**适用场景**：
- 无法确认权限级别
- 需要进一步调查
- 文件不需要立即修复

**执行操作**：
- 不修改文件
- 记录到待处理列表
- 继续处理下一个文件

#### 选项4：查看权限详情

**执行操作**：
- 打开官方权限文档
- 搜索相关权限信息
- 返回重新确认

## 手动处理流程

如果自动脚本无法满足需求，可以手动处理：

### 步骤1：查阅官方文档

```bash
# 打开官方文档
xdg-open "https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md"
```

### 步骤2：搜索权限信息

在以下位置搜索：
1. OpenHarmony官方文档
2. OpenHarmony源码中的权限定义
3. 社区论坛和Issue
4. 权限管理者

### 步骤3：确认权限级别

根据权限的功能和影响范围判断：
- **normal**：不影响系统和其他应用
- **system_basic**：涉及系统关键功能
- **system_core**：仅限系统核心服务（禁止）

### 步骤4：手动修复文件

```bash
# 1. 提取配置
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json

# 2. 编辑配置文件
vim profile.json
# 修改 "apl" 字段为确认的级别

# 3. 重新签名
java -jar hap-sign-tool.jar sign-profile \
  -mode localSign \
  -keyAlias "OpenHarmony Application Profile Release" \
  -keyPwd "123456" \
  -inFile profile.json \
  -outFile openharmony_sx.p7b \
  -keystoreFile OpenHarmony.p12 \
  -keystorePwd "123456" \
  -signAlg SHA256withECDSA \
  -profileCertFile OpenHarmonyProfileRelease.pem \
  -validity 365 \
  -developer-id "OpenHarmony"
```

### 步骤5：验证修复结果

```bash
# 检查配置
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | python3 -m json.tool

# 检查acls字段
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify 2>/dev/null | \
  python3 -m json.tool | grep -A 5 "acls"
```

## 最佳实践

### 1. 优先使用保守策略

**原则**：不确定时，使用`normal`级别

**原因**：
- 避免权限过高导致安全问题
- 如果权限不足，后续可以提升
- 如果权限过高，可能导致系统风险

**示例**：
```
未知权限：ohos.permission.CUSTOM_PERMISSION
选择：1 (使用normal级别) ← 推荐
```

### 2. 记录未知权限

创建一个记录文档，记录所有未知权限：

```markdown
# 未知权限记录

## 2026-03-06
### 文件：ActsWindowEnterpriseTest/signature/openharmony_sx.p7b
- 权限：ohos.permission.CUSTOM_WINDOW_PERMISSION
- 处理方案：使用normal级别
- 确认人：张三
- 备注：企业窗口权限，使用保守策略

### 文件：ActsWindowSpecialTest/signature/openharmony_sx.p7b
- 权限：ohos.permission.SPECIAL_FEATURE
- 处理方案：使用system_basic级别
- 确认人：李四
- 备注：特殊功能权限，需要较高权限
```

### 3. 批量处理未知权限

如果多个文件有相同的未知权限：

```bash
# 1. 查找所有包含该权限的文件
grep -r "ohos.permission.CUSTOM_PERMISSION" test/xts/acts/*/signature/*.p7b

# 2. 统一处理
# 使用相同的配置方案处理所有文件

# 3. 记录处理结果
# 在文档中记录批量处理的情况
```

### 4. 验证修复效果

修复后必须验证：

1. **配置验证**
   ```bash
   # 检查apl和app-feature
   openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | \
     python3 -m json.tool | grep -E '"apl"|"app-feature"'
   ```

2. **acls字段验证**
   ```bash
   # 检查acls字段是否保留
   openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | \
     python3 -m json.tool | grep -A 5 "acls"
   ```

3. **编译验证**
   ```bash
   # 重新编译XTS测试套件
   ./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=bin,hap_dynamic
   ```

4. **运行验证**
   ```bash
   # 运行测试套件，确认权限生效
   # (如果有测试环境)
   ```

### 5. 反馈给社区

如果确认是新权限：

1. **提交Issue**
   ```
   标题：新增权限：ohos.permission.CUSTOM_PERMISSION
   内容：
   - 权限名称：ohos.permission.CUSTOM_PERMISSION
   - 权限级别：normal / system_basic
   - 使用场景：企业窗口管理
   - 确认依据：权限管理者确认
   ```

2. **提交PR**
   - 更新权限文档
   - 更新修复脚本的权限列表

## 常见问题

### Q1: 如果选择了错误的级别怎么办？

**A:** 可以重新修复：
```bash
# 1. 恢复备份
cp openharmony_sx.p7b.backup openharmony_sx.p7b

# 2. 重新运行修复脚本
python3 fix_r012_p7b.py openharmony_sx.p7b

# 3. 选择正确的级别
```

### Q2: 如何判断权限是否需要system_basic级别？

**A:** 参考以下标准：
- 是否涉及系统关键功能？
- 是否需要访问系统资源？
- 是否影响其他应用？
- 是否在受限权限列表中？

如果以上任一答案是"是"，则可能需要`system_basic`级别。

### Q3: 可以跳过所有未知权限吗？

**A:** 不推荐：
- 未知权限可能是新权限，需要确认
- 跳过可能导致权限配置错误
- 建议至少记录未知权限，后续统一处理

### Q4: 如何批量处理未知权限？

**A:** 使用批量处理脚本：
```bash
# 1. 收集所有未知权限
python3 fix_r012_p7b.py --collect-unknown test/xts/acts/*/

# 2. 统一确认处理方案
# 编辑配置文件，指定每个权限的级别

# 3. 批量修复
python3 fix_r012_p7b.py --batch-fix unknown_permissions.conf
```

## 总结

处理未知权限的关键原则：

1. ✅ **不要盲目使用默认值**：必须确认权限级别
2. ✅ **优先使用保守策略**：不确定时使用`normal`级别
3. ✅ **记录未知权限**：方便后续统一处理
4. ✅ **验证修复效果**：确保修复正确
5. ✅ **反馈给社区**：帮助完善权限列表

通过正确的处理流程，可以确保未知权限得到合理配置，避免权限问题导致的系统风险。

## 相关文档

- [R012修复指南](./R012_FIX_GUIDE.md)
- [R012修复总结](./R012_FIX_SUMMARY.md)
- [R012修复脚本设计文档](./R012_FIX_SCRIPT_DESIGN.md)
- [OpenHarmony权限管理](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/access-token.md)
