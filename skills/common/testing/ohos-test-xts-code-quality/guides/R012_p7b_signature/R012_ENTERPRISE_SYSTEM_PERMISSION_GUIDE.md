# R012问题：企业和系统应用权限处理指南

## 概述

本文档专门说明如何处理D类（企业应用权限）、E类（MDM应用权限）和F/G/H类（系统应用权限）。

## 权限分类

### D类：企业应用权限

**文档**：[permissions-for-enterprise-apps.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-enterprise-apps.md)

**特点**：
- 属于企业应用专用权限
- 需要企业签名证书
- app-feature可设置为`hos_system_app`

**示例权限**：
- `ohos.permission.ENTERPRISE_MANAGE_SETTINGS`
- `ohos.permission.ENTERPRISE_SET_NETWORK`
- `ohos.permission.ENTERPRISE_GET_NETWORK`

**配置方案**：
```json
{
  "bundle-info": {
    "apl": "system_basic",
    "app-feature": "hos_system_app"  // 企业应用
  }
}
```

**处理建议**：
- ✅ 如果是企业应用，可以保留权限
- ⚠️ 需要确认是否有企业签名证书
- ❓ 如果是普通应用，需要移除这些权限

### E类：MDM应用权限

**文档**：[permissions-for-mdm-apps.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-mdm-apps.md)

**特点**：
- MDM（移动设备管理）专用权限
- 用于设备管理场景
- app-feature可设置为`hos_system_app`

**示例权限**：
- `ohos.permission.MDM_ADMIN`
- `ohos.permission.MDM_DEVICE_SETTINGS`
- `ohos.permission.MDM_APPLICATION_MANAGEMENT`

**配置方案**：
```json
{
  "bundle-info": {
    "apl": "system_basic",
    "app-feature": "hos_system_app"  // MDM应用
  }
}
```

**处理建议**：
- ✅ 如果是MDM应用，可以保留权限
- ⚠️ 需要确认是否有MDM签名证书
- ❓ 如果是普通应用，需要移除这些权限

### F类：系统应用权限（无ACL）

**文档**：[permissions-for-system-apps-no-acl.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-no-acl.md)

**特点**：
- 系统应用专用权限（无需ACL）
- 需要系统签名
- app-feature必须为`hos_system_app`
- **开源仓不推荐使用** ⚠️

**示例权限**：
- `ohos.permission.GET_BUNDLE_INFO_PRIVILEGED`
- `ohos.permission.INSTALL_BUNDLE`
- `ohos.permission.MANAGE_LOCAL_ACCOUNTS`

**处理建议**：
- ❌ 开源仓不推荐使用
- ✅ 建议移除这些权限
- ⚠️ 如果必须使用，需要系统签名

### G类：系统应用权限（用户授权）

**文档**：[permissions-for-system-apps-user.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-user.md)

**特点**：
- 系统应用专用权限（用户授权）
- 需要用户授权和系统签名
- app-feature必须为`hos_system_app`
- **开源仓不推荐使用** ⚠️

**示例权限**：
- `ohos.permission.MANAGE_SECURE_SETTINGS`
- `ohos.permission.SET_UNREMOVABLE_NOTIFICATION`

**处理建议**：
- ❌ 开源仓不推荐使用
- ✅ 建议移除这些权限
- ⚠️ 如果必须使用，需要系统签名

### H类：系统应用权限

**文档**：[permissions-for-system-apps.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps.md)

**特点**：
- 系统应用专用权限
- 需要系统签名证书
- app-feature必须为`hos_system_app`
- **开源仓不推荐使用** ⚠️

**示例权限**：
- `ohos.permission.CONNECT_IME_ABILITY`
- `ohos.permission.CONNECT_IVI_ABILITY`

**处理建议**：
- ❌ 开源仓不推荐使用
- ✅ 建议移除这些权限
- ⚠️ 如果必须使用，需要系统签名

## 自动处理流程

### 1. 检测到企业应用权限（D类、E类）

```
============================================================
🏢 检测到企业应用权限 - 文件: xxx/signature/openharmony_sx.p7b
============================================================
以下权限属于企业应用权限：
  - ohos.permission.ENTERPRISE_MANAGE_SETTINGS
  - ohos.permission.MDM_ADMIN

📚 参考信息：
  - 这些权限需要企业签名证书
  - app-feature需要设置为 hos_system_app
  - 如果是普通应用，需要移除这些权限

请选择处理方案：
  1. 设置为企业应用（保留权限，app-feature=hos_system_app）
  2. 设置为普通应用（移除权限，app-feature=hos_normal_app）
  3. 跳过此文件（不修复）
  4. 查看权限详情（打开官方文档）

请选择 [1-4]:
```

### 2. 检测到系统应用权限（F类、G类、H类）

```
============================================================
⚙️  检测到系统应用权限 - 文件: xxx/signature/openharmony_sx.p7b
============================================================
以下权限属于系统应用权限：
  - ohos.permission.GET_BUNDLE_INFO_PRIVILEGED
  - ohos.permission.INSTALL_BUNDLE

📚 参考信息：
  - 这些权限需要系统签名证书
  - app-feature需要设置为 hos_system_app
  - 开源仓要求应用为普通应用（app-feature=hos_normal_app）
  - 使用这些权限会导致应用无法正常运行

⚠️  重要提醒：
  - 开源仓不推荐使用系统应用权限
  - 建议移除这些权限
  - 或者联系架构师讨论解决方案

请选择处理方案：
  1. 设置为系统应用（不推荐，app-feature=hos_system_app）
  2. 设置为普通应用（需移除权限，app-feature=hos_normal_app）【推荐】
  3. 跳过此文件（不修复）【推荐】
  4. 查看权限详情（打开官方文档）

请选择 [1-4]:
```

## 手动处理方法

### 企业应用权限处理

#### 方案1：保留企业应用权限

```bash
# 1. 提取配置
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json

# 2. 编辑配置文件
vim profile.json
# 修改：
#   "apl": "system_basic"
#   "app-feature": "hos_system_app"

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
  -validity 365
```

#### 方案2：移除企业应用权限

```bash
# 1. 提取配置
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json

# 2. 编辑配置文件
vim profile.json
# 修改：
#   "apl": "normal"
#   "app-feature": "hos_normal_app"
#   删除企业权限相关的acls

# 3. 重新签名（同上）
```

### 系统应用权限处理

#### 推荐方案：移除系统应用权限

```bash
# 1. 提取配置
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json

# 2. 编辑配置文件
vim profile.json
# 修改：
#   "apl": "normal"  # 或 system_basic（如果有其他权限）
#   "app-feature": "hos_normal_app"
#   删除系统权限相关的acls

# 3. 重新签名（同上）
```

## 权限分类决策树

```
检测到权限
    ↓
判断权限类型
    ├─ A/B类 → apl=normal, app-feature=hos_normal_app
    ├─ C类 → apl=system_basic, app-feature=hos_normal_app
    ├─ D/E类 → 企业应用权限 ⚠️
    │   ├─ 确认为企业应用 → apl=system_basic, app-feature=hos_system_app
    │   └─ 普通应用 → 移除权限, apl=normal, app-feature=hos_normal_app
    ├─ F/G/H类 → 系统应用权限 ⚠️
    │   ├─ 推荐方案 → 移除权限, apl=normal, app-feature=hos_normal_app
    │   └─ 特殊情况 → 联系架构师
    └─ 未知权限 → 需要用户确认
```

## 权限分类总结表

| 权限类型 | 文档 | apl | app-feature | 开源仓推荐 | 处理难度 |
|---------|------|-----|-------------|-----------|---------|
| A类 | permissions-for-all-user.md | normal | hos_normal_app | ✅ 推荐 | 简单 |
| B类 | permissions-for-all.md | normal | hos_normal_app | ✅ 推荐 | 简单 |
| C类 | restricted-permissions.md | system_basic | hos_normal_app | ✅ 推荐 | 简单 |
| D类 | permissions-for-enterprise-apps.md | system_basic | hos_system_app | ⚠️ 需确认 | 中等 |
| E类 | permissions-for-mdm-apps.md | system_basic | hos_system_app | ⚠️ 需确认 | 中等 |
| F类 | permissions-for-system-apps-no-acl.md | system_basic | hos_system_app | ❌ 不推荐 | 困难 |
| G类 | permissions-for-system-apps-user.md | system_basic | hos_system_app | ❌ 不推荐 | 困难 |
| H类 | permissions-for-system-apps.md | system_basic | hos_system_app | ❌ 不推荐 | 困难 |

## 常见问题

### Q1: 为什么开源仓不推荐使用F/G/H类权限？

**A:** 原因如下：
1. **签名要求**：需要系统签名证书，开源仓通常使用普通签名
2. **应用类型**：需要系统应用（app-feature=hos_system_app），开源仓要求普通应用
3. **功能限制**：这些权限涉及系统核心功能，普通应用不应使用
4. **兼容性**：可能导致应用在某些设备上无法正常运行

### Q2: 如果测试用例必须使用F/G/H类权限怎么办？

**A:** 建议按以下步骤处理：
1. **重新评估需求**：确认是否真的需要这些权限
2. **寻找替代方案**：查看是否有普通权限可以替代
3. **联系架构师**：讨论特殊处理方案
4. **临时跳过**：暂时跳过该测试用例，等待官方解决方案

### Q3: D类和E类权限可以用于开源仓吗？

**A:** 可以，但需要满足条件：
1. **应用类型**：确认应用为企业应用或MDM应用
2. **签名证书**：需要相应的企业签名证书
3. **配置正确**：app-feature设置为`hos_system_app`
4. **功能验证**：确保应用功能正常

### Q4: 如何判断应用是企业应用还是普通应用？

**A:** 判断标准：
1. **应用场景**：
   - 企业应用：企业内部管理、设备管控
   - MDM应用：移动设备管理
   - 普通应用：通用功能

2. **权限需求**：
   - 需要D/E类权限 → 可能是企业应用
   - 只需要A/B/C类权限 → 普通应用

3. **签名证书**：
   - 有企业签名证书 → 企业应用
   - 普通签名证书 → 普通应用

## 最佳实践

### 1. 优先使用A/B/C类权限
- ✅ 这些权限适用于开源仓
- ✅ 配置简单，无需特殊处理
- ✅ 兼容性好

### 2. 谨慎使用D/E类权限
- ⚠️ 确认应用类型
- ⚠️ 确认有企业签名证书
- ⚠️ 配置正确的app-feature

### 3. 避免使用F/G/H类权限
- ❌ 开源仓不推荐
- ❌ 需要系统签名
- ❌ 可能导致兼容性问题

### 4. 及时沟通
- 💬 遇到问题及时反馈
- 💬 联系架构师讨论方案
- 💬 记录处理过程

## 相关文档

- [R012修复指南](./R012_FIX_GUIDE.md)
- [R012修复总结](./R012_FIX_SUMMARY.md)
- [R012修复脚本设计文档](./R012_FIX_SCRIPT_DESIGN.md)
- [R012未知权限处理指南](./R012_UNKNOWN_PERMISSION_GUIDE.md)
