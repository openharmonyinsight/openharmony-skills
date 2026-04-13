# R012问题修复指南

## 问题描述

R012规则检查签名证书p7b文件中的APL等级和app-feature配置错误。

**规范要求：**
- **app-feature字段**: 控制普通应用还是系统应用，开源仓默认为普通应用，因此`app-feature`字段默认配置为`hos_normal_app`
- **apl字段**: 控制应用等级，默认普通应用apl等级配置为`normal`
- 禁止使用`system_core`等级
- 极少数情况可以使用`system_basic`（仅限于涉及特定权限）
- 高于APL等级的权限依据"权限ACL是否使能"在acls中进行权限申请

## ⚠️ 重要提醒

**直接修改p7b文件中的字段会导致编译报错！** 必须使用签名工具重新生成p7b文件。

p7b文件是PKCS#7签名格式，包含：
- **签名数据**：JSON配置（包含apl、app-feature等）
- **加密签名**：对JSON数据的数字签名

如果直接修改JSON字段，签名会失效，导致应用无法安装和运行。

## 修复方法一：AI自动修复（推荐）

当用户请求修复R012问题时，AI应按照以下流程自动执行修复：

### 修复流程图

```
输入p7b文件路径
       ↓
步骤1：提取JSON配置 (openssl cms -verify)
       ↓
步骤2：检测问题
       - 检查 apl == "system_core" ?
       - 检查 app-feature != "hos_normal_app" ?
       ↓
步骤3：提取关键字段并修改
       - 保留: app-distribution-type, validity, bundle-name, acls
       - 修改: apl → "normal", app-feature → "hos_normal_app"
       ↓
步骤4：写入模板文件
       - 写入 guides/signature_tools/UnsgnedReleasedProfileTemplate.json
       ↓
步骤5：重新签名
       - 使用 hap-sign-tool.jar 生成新的p7b文件
       ↓
步骤6：替换原文件
       - 备份原文件为 .p7b.backup
       - 替换为新生成的p7b文件
```

### AI执行修复的关键命令

**步骤1：提取JSON配置**
```bash
openssl cms -verify -in <p7b文件路径> -inform DER -noverify
```

**步骤2：问题检测逻辑**
- 如果 `apl == "system_core"` → 需要修复
- 如果 `app-feature != "hos_normal_app"` → 需要修复

**步骤3：需要保留和修改的字段**

| 字段 | 操作 | 说明 |
|------|------|------|
| app-distribution-type | 保留 | 保持原值 |
| validity | 保留 | 保持原值 (not-before, not-after) |
| bundle-name | 保留 | 保持原值 |
| apl | 修改 | → "normal" (或 "system_basic" 如有特定权限) |
| app-feature | 修改 | → "hos_normal_app" |
| acls | 保留 | 如存在则保留（可选字段） |

**步骤4：写入模板文件**
- 路径：`guides/signature_tools/UnsgnedReleasedProfileTemplate.json`
- 使用JSON格式写入修改后的完整配置

**步骤5：重新签名命令**
```bash
cd guides/signature_tools/

java -jar hap-sign-tool.jar sign-profile \
  -mode "localSign" \
  -keyAlias "OpenHarmony Application Profile Release" \
  -keyPwd "123456" \
  -inFile "UnsgnedReleasedProfileTemplate.json" \
  -outFile "myApplication_ohos_Provision.p7b" \
  -keystoreFile "OpenHarmony.p12" \
  -keystorePwd "123456" \
  -signAlg "SHA256withECDSA" \
  -profileCertFile "OpenHarmonyProfileRelease.pem" \
  -validity "365" \
  -developer-id "ohosdeveloper"
```

**步骤6：替换原文件**
```bash
# 替换（保持与原文件同名）
cp guides/signature_tools/myApplication_ohos_Provision.p7b <原p7b文件>
```

### 验证修复结果

```bash
# 检查修复后的配置
openssl cms -verify -in <p7b文件> -inform DER -noverify | python3 -m json.tool
```

确认：
- ✅ apl = "normal" 或 "system_basic"
- ✅ app-feature = "hos_normal_app"
- ✅ acls字段已保留（如果原来存在）

### 批量修复

当需要修复多个文件时，AI应：
1. 查找所有.p7b文件：`find <目录> -name "*.p7b"`
2. 对每个文件执行上述修复流程
3. 输出修复统计（总数、已修复、无问题、失败）

## 修复方法二：手动修复

### 修复步骤（必须严格按顺序执行）

### 步骤1：将p7b文件转化成JSON文件

```bash
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json
```

### 步骤2：提取JSON文件中的关键字段

需要提取的字段（注：acls是可选字段，不存在则不需要提取）：

```json
{
    "app-distribution-type": "XXXXXX",
    "validity": {
        "not-before": XXXXX,
        "not-after": XXXXX
    },
    "bundle-info": {
        "bundle-name": "XXXXX",
        "apl": "XXXXX",
        "app-feature": "XXXXX"
    },
    "acls": {
        "allowed-acls": ["XXXXX"]
    }
}
```

### 步骤3：修改UnsgnedReleasedProfileTemplate.json

将提取的字段写入 `guides/signature_tools/UnsgnedReleasedProfileTemplate.json`：

- **修改** `apl` 和 `app-feature` 字段为正确值
- **保留** `app-distribution-type`、`validity`、`bundle-name`、`acls` 的原始内容

示例：
```json
{
    "version-name": "1.0.0",
    "version-code": 1,
    "app-distribution-type": "os_integration",
    "uuid": "5027b99e-5f9e-465d-9508-a9e0134ffe18",
    "validity": {
        "not-before": 1594865258,
        "not-after": 1689473258
    },
    "type": "release",
    "bundle-info": {
        "developer-id": "OpenHarmony",
        "distribution-certificate": "...",
        "bundle-name": "ohos.example.test",
        "apl": "normal",
        "app-feature": "hos_normal_app"
    },
    "permissions": {
        "restricted-permissions": []
    },
    "issuer": "pki_internal"
}
```

### 步骤4：使用签名工具重新签名

```bash
cd guides/signature_tools/

java -jar hap-sign-tool.jar sign-profile \
  -mode "localSign" \
  -keyAlias "OpenHarmony Application Profile Release" \
  -keyPwd "123456" \
  -inFile "UnsgnedReleasedProfileTemplate.json" \
  -outFile "myApplication_ohos_Provision.p7b" \
  -keystoreFile "OpenHarmony.p12" \
  -keystorePwd "123456" \
  -signAlg "SHA256withECDSA" \
  -profileCertFile "OpenHarmonyProfileRelease.pem" \
  -validity "365" \
  -developer-id "ohosdeveloper"
```

### 步骤5：替换原文件

```bash
# 备份原文件
cp openharmony_sx.p7b openharmony_sx.p7b.backup

# 替换（保持与原文件同名）
cp myApplication_ohos_Provision.p7b openharmony_sx.p7b
```

## 修复流程

### 1. 权限分类判断

根据p7b文件中配置的权限，判断正确的apl和app-feature值：

#### A类：用户授权权限（normal级别）
权限在文档A中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all-user.md`

**配置：** `apl="normal"`, `app-feature="hos_normal_app"`

#### B类：所有应用可用权限（normal级别）
权限在文档B中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md`

**配置：** `apl="normal"`, `app-feature="hos_normal_app"`

#### C类：受限权限（system_basic级别）
权限在文档C中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/restricted-permissions.md`

**配置：** `apl="system_basic"`, `app-feature="hos_normal_app"`

#### D类：企业应用权限（system_basic级别）⭐ NEW
权限在文档D中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-enterprise-apps.md`

**配置：** `apl="system_basic"`, `app-feature="hos_system_app"`（企业应用）

**说明**：D类权限属于企业类应用，可设置app-feature为hos_system_app

#### E类：MDM应用权限（system_basic级别）⭐ NEW
权限在文档E中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-mdm-apps.md`

**配置：** `apl="system_basic"`, `app-feature="hos_system_app"`（企业应用）

**说明**：E类权限属于MDM（移动设备管理）应用，可设置app-feature为hos_system_app

#### F类：系统应用权限-无ACL（system_basic级别）⚠️ NEW
权限在文档F中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-no-acl.md`

**配置：** 需用户确认
- **推荐配置**：移除这些权限，使用 `apl="normal"`, `app-feature="hos_normal_app"`
- **可选配置**：`apl="system_basic"`, `app-feature="hos_system_app"`（但开源仓不推荐）

**说明**：⚠️ F类权限为系统应用权限，需要系统签名。开源仓要求普通应用，建议移除这些权限。

#### G类：系统应用权限-用户授权（system_basic级别）⚠️ NEW
权限在文档G中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-user.md`

**配置：** 需用户确认
- **推荐配置**：移除这些权限，使用 `apl="normal"`, `app-feature="hos_normal_app"`
- **可选配置**：`apl="system_basic"`, `app-feature="hos_system_app"`（但开源仓不推荐）

**说明**：⚠️ G类权限为系统应用权限，需要系统签名。开源仓要求普通应用，建议移除这些权限。

#### H类：系统应用权限（system_basic级别）⚠️ NEW
权限在文档H中：`https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps.md`

**配置：** 需用户确认
- **推荐配置**：移除这些权限，使用 `apl="normal"`, `app-feature="hos_normal_app"`
- **可选配置**：`apl="system_basic"`, `app-feature="hos_system_app"`（但开源仓不推荐）

**说明**：⚠️ H类权限为系统应用权限，需要系统签名。开源仓要求普通应用，建议移除这些权限。

#### 未知权限
如果权限不在上述文档中，需要手动确认权限级别。

### 2. 自动修复工具

#### 概述

AI会根据设计文档自动生成R012修复脚本。

**设计文档位置**：`R012_FIX_SCRIPT_DESIGN.md`

**生成流程**：
1. AI读取设计文档
2. 理解架构设计和算法逻辑
3. 根据当前环境生成定制化代码
4. 自动验证生成结果

**生成的脚本特性**：
- ✅ 自动提取p7b文件中的JSON配置
- ✅ 根据权限列表自动判断正确的apl和app-feature值
- ✅ **自动保留acls字段**（ACL权限列表）
- ✅ **自动保留所有原始字段**（permissions、distribution-certificate等）
- ✅ 使用签名工具重新生成p7b文件
- ✅ 支持批量修复

#### 使用示例

AI生成的修复脚本通常支持以下用法：

AI生成的修复脚本通常支持以下用法：

```bash
# 修复单个p7b文件
python3 fix_r012_p7b.py /path/to/file.p7b

# 修复多个p7b文件
python3 fix_r012_p7b.py file1.p7b file2.p7b file3.p7b

# 从文本文件读取路径列表
python3 fix_r012_p7b.py --file-list p7b_files.txt

# 详细输出模式
python3 fix_r012_p7b.py -v /path/to/file.p7b

# 不备份原文件
python3 fix_r012_p7b.py --no-backup /path/to/file.p7b
```

#### 参数说明

| 参数 | 说明 |
|------|------|
| `files` | 要修复的p7b文件路径（可指定多个） |
| `--file-list`, `-l` | 从文本文件读取p7b文件路径列表 |
| `--no-backup` | 不备份原文件（默认会备份为.p7b.backup） |
| `--verbose`, `-v` | 显示详细输出信息 |

#### 修复示例

**示例1：修复单个文件**
```bash
$ python3 fix_r012_p7b.py test/xts/acts/camera/camera_hap_test/signature/openharmony_sx.p7b -v

============================================================
处理文件: test/xts/acts/camera/camera_hap_test/signature/openharmony_sx.p7b
[R012修复] 当前配置: apl=system_core, app-feature=hos_system_app
[R012修复] 正确配置: apl=normal, app-feature=hos_normal_app
[R012修复] 已备份原文件到: openharmony_sx.p7b.backup
[R012修复] 执行签名命令: java -jar hap-sign-tool.jar sign-profile ...
[R012修复] 成功生成签名文件: temp_profile.p7b
[R012修复] 成功修复文件: test/xts/acts/camera/camera_hap_test/signature/openharmony_sx.p7b
```

**示例2：批量修复**
```bash
$ python3 fix_r012_p7b.py --file-list p7b_issues.txt

============================================================
修复完成
  成功: 15
  失败: 0
  
发现的未知权限:
  - ohos.permission.CUSTOM_PERMISSION_1
  - ohos.permission.CUSTOM_PERMISSION_2
```

### 3. 手动修复步骤

如果自动修复失败或存在未知权限，可以手动修复：

#### 步骤1：提取p7b文件中的JSON配置
```bash
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json
```

#### 步骤2：修改配置文件
编辑`profile.json`文件，修改以下字段：
```json
{
  "bundle-info": {
    "apl": "normal",  // 或 "system_basic"
    "app-feature": "hos_normal_app"
  }
}
```

**重要**：保留原文件中的所有字段，特别是：
- `acls` 字段（ACL权限列表）
- `permissions` 字段（受限权限列表）
- `distribution-certificate` 字段（证书信息）
- 其他所有自定义字段

#### 步骤3：重新签名生成p7b文件
```bash
cd signature_tools/
java -jar hap-sign-tool.jar sign-profile \
  -mode "localSign" \
  -keyAlias "OpenHarmony Application Profile Release" \
  -keyPwd "123456" \
  -inFile "profile.json" \
  -outFile "openharmony_sx.p7b" \
  -keystoreFile "OpenHarmony.p12" \
  -keystorePwd "123456" \
  -signAlg "SHA256withECDSA" \
  -profileCertFile "OpenHarmonyProfileRelease.pem" \
  -validity "365" \
  -developer-id "OpenHarmony"
```

#### 步骤4：替换原文件
将新生成的p7b文件替换到原路径。

## 权限分类参考

### 常见normal级别权限
- `ohos.permission.INTERNET` - 网络访问
- `ohos.permission.GET_NETWORK_INFO` - 获取网络信息
- `ohos.permission.CAMERA` - 相机（用户授权）
- `ohos.permission.MICROPHONE` - 麦克风（用户授权）
- `ohos.permission.LOCATION` - 位置（用户授权）
- `ohos.permission.READ_MEDIA` - 读取媒体文件（用户授权）

### 常见system_basic级别权限
- `ohos.permission.MANAGE_BLUETOOTH` - 管理蓝牙
- `ohos.permission.INSTALL_BUNDLE` - 安装应用
- `ohos.permission.MANAGE_SETTINGS` - 管理设置
- `ohos.permission.GRANT_SENSITIVE_PERMISSIONS` - 授予敏感权限

## 常见问题

### Q1: 如何确认权限级别？
**A:** 参考以下三个官方文档：
- [用户授权权限](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all-user.md)
- [所有应用可用权限](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md)
- [受限权限](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/restricted-permissions.md)

### Q2: 修复后还是报R012错误？
**A:** 可能的原因：
1. p7b文件没有正确替换到原路径
2. 权限级别判断错误，需要手动确认
3. 存在多个p7b文件，需要全部修复

### Q3: 出现未知权限怎么办？
**A:** 按以下步骤处理：

#### 自动修复脚本的处理流程

当修复脚本遇到未知权限时，会：

1. **暂停修复并提示用户**
   ```
   ============================================================
   ⚠️  发现未知权限 - 文件: xxx/signature/openharmony_sx.p7b
   ============================================================
   以下权限不在已知权限列表中：
     1. ohos.permission.CUSTOM_PERMISSION
   
   当前配置：
     - apl: system_core
     - app-feature: hos_system_app
     - acls: {"allowed-acls": [...]}
   ```

2. **提供参考信息**
   ```
   📚 参考信息：
     - 如果这些权限是新添加的或自定义权限，请确认其级别
     - normal级别：适用于大多数应用权限
     - system_basic级别：适用于系统基础服务权限
     - system_core级别：禁止使用（仅系统核心服务）
   ```

3. **请求用户确认**
   ```
   请确认配置方案：
     1. 使用 normal 级别（推荐，保守策略）
     2. 使用 system_basic 级别（如果权限较高）
     3. 跳过此文件（不修复）
     4. 查看权限详情（打开官方文档）
   
   请选择 [1-4]:
   ```

4. **根据用户选择执行**
   - **选择1**：使用`normal`级别（保守策略，推荐）
   - **选择2**：使用`system_basic`级别（如果确认权限较高）
   - **选择3**：跳过此文件，不进行修复
   - **选择4**：打开官方文档查看权限详情

#### 手动处理步骤

如果选择跳过自动修复，可以手动处理：

1. **查阅官方文档确认权限**
   - [用户授权权限](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all-user.md)
   - [所有应用可用权限](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md)
   - [受限权限](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/restricted-permissions.md)

2. **联系权限管理者**
   - 如果是新权限，联系权限管理者确认级别
   - 提供权限名称和使用场景

3. **临时使用保守策略**
   - 如果无法确认，使用`normal`级别
   - 后续可以根据实际情况调整

4. **手动修复文件**
   ```bash
   # 1. 提取配置
   openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json
   
   # 2. 编辑配置文件
   vim profile.json
   # 修改 "apl" 字段为确认的级别
   
   # 3. 重新签名
   java -jar hap-sign-tool.jar sign-profile ...
   ```

#### 最佳实践

1. **优先使用保守策略**

### Q4: 编译报错 "Common name of certificate is empty!"？
**A:** 这是签名配置问题，profile文件中的证书信息为空或被截断。

**错误信息：**
```
ERROR: 11015004 Verify profile failed
Error Message: Common name of certificate is empty!
```

**原因：**
1. `distribution-certificate` 字段在写入模板文件时被截断
2. 证书内容包含大量换行符(`\n`)，在命令行中直接写入时处理不当

**解决方案：**

1. **验证证书字段是否完整**
   ```bash
   openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | python3 -c "
   import sys, json
   config = json.load(sys.stdin)
   cert = config.get('bundle-info', {}).get('distribution-certificate', '')
   print(f'证书长度: {len(cert)}')
   if len(cert) < 500:
       print('⚠️ 证书可能被截断！')
   "
   ```

2. **使用 HEREDOC 格式写入完整配置**
   ```bash
   cat > UnsgnedReleasedProfileTemplate.json << 'ENDOFFILE'
   {
       "version-name": "1.0.0",
       ...
       "bundle-info": {
           "distribution-certificate": "-----BEGIN CERTIFICATE-----\n完整证书内容...\n-----END CERTIFICATE-----\n",
           ...
       }
   }
   ENDOFFILE
   ```

3. **使用 Python 脚本正确处理 JSON**
   ```bash
   # 提取原始配置
   openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > original.json
   
   # 使用Python修改并保留完整证书
   python3 << 'EOF'
   import json
   with open('original.json', 'r') as f:
       config = json.load(f)
   
   # 修改字段
   config['bundle-info']['apl'] = 'normal'
   config['bundle-info']['app-feature'] = 'hos_normal_app'
   
   # 保存（证书自动保留）
   with open('UnsgnedReleasedProfileTemplate.json', 'w') as f:
       json.dump(config, f, indent=4)
   EOF
   ```

**注意事项：**
- ⚠️ 证书内容约 800+ 字符，必须完整保留
- ⚠️ 使用 `'ENDOFFILE'`（带引号）避免 shell 解释变量
- ⚠️ 修复后验证证书长度是否正确
   - 不确定时，使用`normal`级别
   - 宁可保守，不可激进

2. **记录未知权限**
   - 将未知权限记录到文档中
   - 后续可以批量处理

3. **验证修复结果**
   - 修复后验证权限是否生效
   - 重新编译测试套件确认

4. **反馈给社区**
   - 如果发现新权限，反馈给OpenHarmony社区
   - 帮助完善权限列表

### Q3.5: 遇到企业应用权限（D类、E类）怎么办？ ⭐ NEW
**A:** 企业应用权限需要特别处理：

#### 权限类型
- **D类**：企业应用权限 - [文档](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-enterprise-apps.md)
- **E类**：MDM应用权限 - [文档](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-mdm-apps.md)

#### 处理流程

修复脚本会自动检测企业应用权限：

```
============================================================
🏢 检测到企业应用权限 - 文件: xxx/signature/openharmony_sx.p7b
============================================================
以下权限属于企业应用权限：
  - ohos.permission.ENTERPRISE_MANAGE_SETTINGS
  - ohos.permission.MDM_ADMIN

📚 参考信息：
  - 这些权限需要企业应用签名
  - app-feature需要设置为hos_system_app
  - 请确认此应用是否为企业应用

请选择处理方案：
  1. 设置为企业应用（app-feature=hos_system_app，apl=system_basic）
  2. 设置为普通应用（需移除企业权限，推荐）
  3. 跳过此文件（不修复）

请选择 [1-3]: 
```

#### 处理建议

1. **确认应用类型**
   - 如果是企业内部应用：选择方案1
   - 如果是开源仓测试应用：选择方案2（推荐）

2. **开源仓推荐配置**
   ```json
   {
     "bundle-info": {
       "apl": "normal",
       "app-feature": "hos_normal_app"
     }
   }
   ```
   并移除企业应用权限

3. **企业应用配置**
   ```json
   {
     "bundle-info": {
       "apl": "system_basic",
       "app-feature": "hos_system_app"
     }
   }
   ```

### Q3.6: 遇到系统应用权限（F类、G类、H类）怎么办？ ⭐ NEW
**A:** 系统应用权限需要特别处理：

#### 权限类型
- **F类**：系统应用权限（无ACL） - [文档](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-no-acl.md)
- **G类**：系统应用权限（用户授权） - [文档](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-user.md)
- **H类**：系统应用权限 - [文档](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps.md)

#### 处理流程

修复脚本会自动检测系统应用权限：

```
============================================================
⚙️  检测到系统应用权限 - 文件: xxx/signature/openharmony_sx.p7b
============================================================
以下权限属于系统应用权限：
  - ohos.permission.SYSTEM_DIALOG
  - ohos.permission.SET_TIME

📚 参考信息：
  - 这些权限需要系统应用签名
  - app-feature需要设置为hos_system_app
  - ⚠️ 但开源仓要求应用为普通应用（hos_normal_app）
  - 建议移除这些权限或跳过此文件

请选择处理方案：
  1. 设置为系统应用（不推荐，app-feature=hos_system_app）
  2. 设置为普通应用并移除系统权限（推荐）
  3. 跳过此文件（推荐）
  4. 查看权限详情（打开官方文档）

请选择 [1-4]:
```

#### 处理建议

1. **开源仓强烈建议**
   - ⚠️ **不要使用系统应用权限**
   - 选择方案2或方案3（推荐）

2. **推荐配置**
   ```json
   {
     "bundle-info": {
       "apl": "normal",
       "app-feature": "hos_normal_app"
     }
   }
   ```
   并移除系统应用权限

3. **如果必须使用系统权限**
   - 需要系统签名证书
   - app-feature必须设置为`hos_system_app`
   - 但这不符合开源仓规范

4. **最佳实践**
   - 重新评估是否真的需要这些权限
   - 考虑使用替代方案
   - 或者联系架构师讨论解决方案

#### 权限分类总结表

| 权限类型 | apl | app-feature | 开源仓推荐 | 说明 |
|---------|-----|-------------|-----------|------|
| A类 | normal | hos_normal_app | ✅ 推荐 | 用户授权权限 |
| B类 | normal | hos_normal_app | ✅ 推荐 | 所有应用可用 |
| C类 | system_basic | hos_normal_app | ✅ 推荐 | 受限权限 |
| D类 | system_basic | hos_system_app | ⚠️ 需确认 | 企业应用权限 |
| E类 | system_basic | hos_system_app | ⚠️ 需确认 | MDM应用权限 |
| F类 | system_basic | hos_system_app | ❌ 不推荐 | 系统应用权限（无ACL） |
| G类 | system_basic | hos_system_app | ❌ 不推荐 | 系统应用权限（用户授权） |
| H类 | system_basic | hos_system_app | ❌ 不推荐 | 系统应用权限 |

### Q4: 签名工具报错？
**A:** 检查以下内容：
1. Java环境是否正确安装
2. hap-sign-tool.jar路径是否正确
3. OpenHarmony.p12和OpenHarmonyProfileRelease.pem文件是否存在
4. 密码是否正确（默认：123456）

### Q5: 修复后acls字段丢失？
**A:** 这是一个已知问题，已在修复脚本中解决：
- **问题原因**：早期版本的修复脚本在重新生成p7b文件时，没有保留原文件中的acls字段
- **影响**：导致配置了ACL权限的应用在修复后丢失权限配置
- **解决方案**：已更新`fix_r012_p7b.py`脚本，现在会自动保留原文件中的所有字段，包括：
  - `acls` 字段（ACL权限列表）
  - `permissions` 字段（受限权限列表）
  - 其他所有自定义字段
- **验证方法**：修复后使用以下命令检查acls字段是否保留：
  ```bash
  openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | python3 -m json.tool | grep -A 5 "acls"
  ```

### Q6: 如何验证修复是否成功？
**A:** 按以下步骤验证：
1. **检查配置字段**：
   ```bash
   openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | python3 -m json.tool
   ```
   确认输出中包含正确的apl和app-feature值，且acls字段已保留

2. **检查文件完整性**：
   ```bash
   # 对比修复前后的字段差异
   diff <(openssl cms -verify -in openharmony_sx.p7b.backup -inform DER -noverify 2>/dev/null | python3 -m json.tool) \
        <(openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify 2>/dev/null | python3 -m json.tool)
   ```
   应该只有apl和app-feature字段发生变化，其他字段保持不变

3. **重新运行质量检查**：
   ```bash
   python3 check_test_code_quality.py test/xts/acts/your_subsystem/
   ```
   确认R012问题已解决

## 相关文档

- [OpenHarmony权限管理](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/access-token.md)
- [应用权限列表](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md)
- [签名工具使用指导](../signature_tools/使用指导.docx)

## 技术支持

如有问题，请联系：
- 邮件：xts@openharmony.io
- Issue：https://gitee.com/openharmony/xts_acts/issues
