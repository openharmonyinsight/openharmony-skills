# R012问题修复设计文档

## 概述

本文档描述R012问题（签名证书APL等级和app-feature配置错误）的修复流程和实现要点，用于指导AI自动执行修复。

## ⚠️ 重要提醒

**直接修改p7b文件中的字段会导致编译报错！** 必须使用签名工具重新生成p7b文件。

p7b文件是PKCS#7签名格式，包含：
- **签名数据**：JSON配置（包含apl、app-feature等）
- **加密签名**：对JSON数据的数字签名

如果直接修改JSON字段，签名会失效，导致应用无法安装和运行。

## 设计目标

1. **自动化修复**：自动检测并修复p7b文件中的apl和app-feature配置错误
2. **字段保留**：确保修复过程中保留原文件的所有字段（特别是acls字段）
3. **重新签名**：使用签名工具重新生成p7b文件（关键步骤）
4. **安全可靠**：备份原文件，支持回滚
5. **批量处理**：支持单个文件和批量修复

## 修复流程（必须严格遵循）

```
输入p7b文件
    ↓
步骤1：将p7b转化成JSON (openssl cms -verify)
    ↓
步骤2：提取关键字段
    - app-distribution-type
    - validity (not-before, not-after)
    - bundle-name
    - apl (需要修改)
    - app-feature (需要修改)
    - acls (可选，存在则提取)
    ↓
步骤3：写入UnsgnedReleasedProfileTemplate.json
    - 修改apl和app-feature为正确值
    - 保留其他字段的原始内容
    ↓
步骤4：使用hap-sign-tool.jar重新签名
    - 读取UnsgnedReleasedProfileTemplate.json
    - 生成myApplication_ohos_Provision.p7b
    ↓
步骤5：替换原文件
    - 将新生成的p7b替换到原路径（保持同名）
```

## AI执行修复的关键步骤

### 步骤1：提取JSON配置

```bash
openssl cms -verify -in <p7b文件路径> -inform DER -noverify
```

AI应解析输出获取JSON配置。

### 步骤2：问题检测

检测条件：
- `apl == "system_core"` → 需要修复
- `app-feature != "hos_normal_app"` → 需要修复

### 步骤3：修改并保留字段

⚠️ **关键：必须完整保留 distribution-certificate 字段！**

| 字段 | 操作 | 说明 |
|------|------|------|
| app-distribution-type | 保留 | 保持原值 |
| validity | 保留 | 保持原值 (not-before, not-after) |
| bundle-name | 保留 | 保持原值 |
| distribution-certificate | **必须保留** | 约800+字符，必须完整保留，否则编译报错 |
| apl | 修改 | → "normal" (或 "system_basic" 如有特定权限) |
| app-feature | 修改 | → "hos_normal_app" |
| acls | 保留 | 如存在则保留（可选字段） |

**正确处理证书的方法：**

```bash
# 使用Python脚本保留完整证书
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > original.json

python3 << 'EOF'
import json
with open('original.json', 'r') as f:
    config = json.load(f)

# 修改字段（证书自动保留）
config['bundle-info']['apl'] = 'normal'
config['bundle-info']['app-feature'] = 'hos_normal_app'

# 验证证书长度
cert = config['bundle-info'].get('distribution-certificate', '')
print(f'证书长度: {len(cert)}')
if len(cert) < 500:
    print('⚠️ 警告: 证书可能被截断！')

# 保存
with open('UnsgnedReleasedProfileTemplate.json', 'w') as f:
    json.dump(config, f, indent=4)
EOF
```

**错误处理方式（会导致编译报错）：**
```bash
# ❌ 错误：使用 cat 命令时证书可能被截断
cat > template.json << 'EOF'
{
    "bundle-info": {
        "distribution-certificate": "证书内容被截断..."
    }
}
EOF
```

### 步骤4：写入模板文件

路径：`guides/R012_p7b_signature/signature_tools/UnsgnedReleasedProfileTemplate.json`

### 步骤5：重新签名

```bash
cd guides/R012_p7b_signature/signature_tools/

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

### 步骤6：替换原文件

```bash
# 替换（保持与原文件同名）
cp guides/R012_p7b_signature/signature_tools/myApplication_ohos_Provision.p7b <原p7b文件>
```

## 批量修复流程

当需要修复多个文件时：

1. **查找所有p7b文件**
   ```bash
   find <目录> -name "*.p7b"
   ```

2. **对每个文件执行修复流程**

3. **输出修复统计**
   - 总文件数
   - 已修复数
   - 无问题数
   - 失败数

## 核心算法

### 1. 权限级别判断算法

```python
# 伪代码
function get_permission_level(permission):
    if permission in PERMISSIONS_USER_GRANT:
        return 'normal'
    elif permission in PERMISSIONS_FOR_ALL:
        return 'normal'
    elif permission in PERMISSIONS_RESTRICTED:
        return 'system_basic'
    else:
        return None  # 未知权限，需要用户确认
```

**数据来源**：
- A类权限（用户授权）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all-user.md
- B类权限（所有应用可用）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-all.md
- C类权限（受限权限）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/restricted-permissions.md
- D类权限（企业应用）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-enterprise-apps.md
- E类权限（MDM应用）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-mdm-apps.md
- F类权限（系统应用-无ACL）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-no-acl.md
- G类权限（系统应用-用户授权）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps-user.md
- H类权限（系统应用）：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/security/AccessToken/permissions-for-system-apps.md

### 2. APL和app-feature确定算法

```python
# 伪代码
function determine_apl_and_feature(permissions):
    if permissions is empty:
        return ('normal', 'hos_normal_app')
    
    max_level = 'normal'
    unknown_perms = []
    
    for perm in permissions:
        level = get_permission_level(perm)
        if level is None:
            unknown_perms.append(perm)
        elif level == 'system_basic':
            max_level = 'system_basic'
    
    return (max_level, 'hos_normal_app', unknown_perms)
```

**规则**：
- 无权限配置：`apl=normal, app-feature=hos_normal_app`
- 只有normal级别权限：`apl=normal, app-feature=hos_normal_app`
- 有system_basic级别权限：`apl=system_basic, app-feature=hos_normal_app`
- 禁止使用`system_core`级别
- **D/E类权限（企业应用）**：`app-feature=hos_system_app`（可选）
- **F/G/H类权限（系统应用）**：需要用户确认，- **未知权限**：需要用户确认后决定

**权限分类说明**：

| 权限类型 | 文档 | apl | app-feature | 说明 |
|---------|------|-----|-------------|------|
| A类 | permissions-for-all-user.md | normal | hos_normal_app | 用户授权权限 |
| B类 | permissions-for-all.md | normal | hos_normal_app | 所有应用可用权限 |
| C类 | restricted-permissions.md | system_basic | hos_normal_app | 受限权限 |
| D类 | permissions-for-enterprise-apps.md | system_basic | hos_system_app | 企业应用权限 ⭐ |
| E类 | permissions-for-mdm-apps.md | system_basic | hos_system_app | MDM应用权限 ⭐ |
| F类 | permissions-for-system-apps-no-acl.md | system_basic | hos_normal_app ⚠️ | 系统应用权限（无ACL）⚠️ |
| G类 | permissions-for-system-apps-user.md | system_basic | hos_normal_app ⚠️ | 系统应用权限（用户授权）⚠️ |
| H类 | permissions-for-system-apps.md | system_basic | hos_normal_app ⚠️ | 系统应用权限 ⚠️ |

⚠️ **重要说明**：
- D类和E类权限属于企业类应用，  - F类、G类、H类权限为系统应用权限，  - 开源仓需保证应用为普通应用，
  - 遇到F/G/H类权限时，需要用户确认后自行适配解决

⚠️ **重要说明**：
- D类和E类权限属于企业类应用，  - F类、G类、H类权限为系统应用权限
  - 开源仓需保证应用为普通应用
  - 遇到F/G/H类权限时，需要用户确认后自行适配解决

### 2.1. 企业和系统应用权限处理算法（重要！）

```python
# 伪代码
function handle_enterprise_system_permissions(enterprise_perms, system_perms, file_path):
    # 检查是否有企业应用权限（D类、E类）
    if enterprise_perms:
        print(f"\n{'='*60}")
        print(f"🏢 检测到企业应用权限 - 文件: {file_path}")
        print(f"{'='*60}")
        print(f"以下权限属于企业应用权限：")
        for perm in enterprise_perms:
            print(f"  - {perm}")
        
        print(f"\n📌 配置建议：")
        print(f"  - apl: system_basic")
        print(f"  - app-feature: hos_system_app (企业应用)")
        print(f"\n⚠️  注意：")
        print(f"  - 企业应用权限需要企业签名证书")
        print(f"  - 请确认此应用是否为企业应用")
        print(f"  - 如果是普通应用，请移除这些权限")
        
        print(f"\n请选择处理方案：")
        print(f"  1. 设置为企业应用 (app-feature=hos_system_app)")
        print(f"  2. 设置为普通应用 (app-feature=hos_normal_app，移除权限)")
        print(f"  3. 跳过此文件")
        
        choice = input(f"请选择 [1-3]: ").strip()
        
        if choice == '1':
            return ('system_basic', 'hos_system_app')
        elif choice == '2':
            return ('normal', 'hos_normal_app')
        else:
            return None
    
    # 检查是否有系统应用权限（F类、G类、H类）
    if system_perms:
        print(f"\n{'='*60}")
        print(f"⚙️  检测到系统应用权限 - 文件: {file_path}")
        print(f"{'='*60}")
        print(f"以下权限属于系统应用权限：")
        for perm in system_perms:
            print(f"  - {perm}")
        
        print(f"\n📌 配置建议：")
        print(f"  - apl: system_basic")
        print(f"  - app-feature: hos_system_app (系统应用)")
        print(f"\n⚠️  重要提醒：")
        print(f"  - 系统应用权限需要系统签名证书")
        print(f"  - 开源仓要求应用为普通应用 (app-feature=hos_normal_app)")
        print(f"  - 使用这些权限可能导致应用无法正常运行")
        print(f"  - 建议移除这些权限或确认应用场景")
        
        print(f"\n请选择处理方案：")
        print(f"  1. 设置为系统应用 (app-feature=hos_system_app，不推荐)")
        print(f"  2. 设置为普通应用 (app-feature=hos_normal_app，需移除权限)")
        print(f"  3. 跳过此文件（推荐）")
        print(f"  4. 查看权限详情")
        
        choice = input(f"请选择 [1-4]: ").strip()
        
        if choice == '1':
            print(f"⚠️  警告：开源仓不应使用系统应用配置")
            confirm = input(f"确认使用系统应用配置？(y/n): ").strip().lower()
            if confirm == 'y':
                return ('system_basic', 'hos_system_app')
            else:
                return None
        elif choice == '2':
            print(f"ℹ️  请手动移除以下权限：")
            for perm in system_perms:
                print(f"  - {perm}")
            input(f"移除完成后按回车继续...")
            return ('normal', 'hos_normal_app')
        elif choice == '4':
            open_permission_docs()
            return handle_enterprise_system_permissions([], system_perms, file_path)
        else:
            return None
    
    return None  # 无特殊权限，使用默认处理
```

**处理策略**：
1. **D类、E类权限（企业应用）**：
   - 显示企业应用权限列表
   - 提供两种选择：
     - 设置为企业应用（app-feature=hos_system_app）
     - 设置为普通应用（需移除权限）
   - 建议确认应用类型

2. **F类、G类、H类权限（系统应用）**：
   - 显示系统应用权限列表
   - 提醒开源仓要求普通应用
   - 提供四种选择：
     - 设置为系统应用（不推荐）
     - 设置为普通应用（需移除权限）
     - 跳过此文件（推荐）
     - 查看权限详情
   - 优先推荐跳过或移除权限

### 2.2. 未知权限处理算法（重要！）

```python
# 伪代码
function handle_unknown_permissions(unknown_perms, file_path, current_config):
    if unknown_perms is empty:
        return current_config  # 无未知权限，继续修复
    
    # 1. 显示未知权限信息
    print(f"\n{'='*60}")
    print(f"⚠️  发现未知权限 - 文件: {file_path}")
    print(f"{'='*60}")
    print(f"以下权限不在已知权限列表中：")
    for i, perm in enumerate(unknown_perms, 1):
        print(f"  {i}. {perm}")
    
    # 2. 显示当前配置信息
    print(f"\n当前配置：")
    print(f"  - apl: {current_config['apl']}")
    print(f"  - app-feature: {current_config['app-feature']}")
    print(f"  - acls: {current_config.get('acls', {})}")
    
    # 3. 提供参考信息
    print(f"\n📚 参考信息：")
    print(f"  - 如果这些权限是新添加的或自定义权限，请确认其级别")
    print(f"  - normal级别：适用于大多数应用权限")
    print(f"  - system_basic级别：适用于系统基础服务权限")
    print(f"  - system_core级别：禁止使用（仅系统核心服务）")
    
    # 4. 请求用户确认
    print(f"\n请确认配置方案：")
    print(f"  1. 使用 normal 级别（推荐，保守策略）")
    print(f"  2. 使用 system_basic 级别（如果权限较高）")
    print(f"  3. 跳过此文件（不修复）")
    print(f"  4. 查看权限详情（打开官方文档）")
    
    choice = input(f"\n请选择 [1-4]: ").strip()
    
    # 5. 根据用户选择处理
    switch choice:
        case '1':
            return 'normal'  # 使用normal级别
        case '2':
            return 'system_basic'  # 使用system_basic级别
        case '3':
            return None  # 跳过此文件
        case '4':
            open_permission_docs()  # 打开官方文档
            return handle_unknown_permissions(unknown_perms, file_path, current_config)  # 重新确认
        default:
            print("无效选择，使用默认值 normal")
            return 'normal'
```

**处理策略**：
1. **明确提示**：告知用户遇到未知权限
2. **提供信息**：显示当前配置和权限列表
3. **参考文档**：提供权限级别说明和官方文档链接
4. **用户选择**：让用户决定如何处理
5. **默认策略**：如果用户不确定，使用`normal`级别（保守策略）

**交互示例**：
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

📚 参考信息：
  - 如果这些权限是新添加的或自定义权限，请确认其级别
  - normal级别：适用于大多数应用权限
  - system_basic级别：适用于系统基础服务权限
  - system_core级别：禁止使用（仅系统核心服务）

请确认配置方案：
  1. 使用 normal 级别（推荐，保守策略）
  2. 使用 system_basic 级别（如果权限较高）
  3. 跳过此文件（不修复）
  4. 查看权限详情（打开官方文档）

请选择 [1-4]: 1
```

### 3. 字段保留算法（关键！）

```python
# 伪代码
function create_profile_template(config):
    # 创建基础模板
    template = {
        "version-name": config.get("version-name", "1.0.0"),
        "version-code": config.get("version-code", 1),
        "app-distribution-type": config.get("app-distribution-type", "os_integration"),
        "uuid": config.get("uuid", "..."),
        "type": config.get("type", "release"),
        "bundle-info": {
            "developer-id": config["bundle-info"]["developer-id"],
            "distribution-certificate": config["bundle-info"]["distribution-certificate"],
            "bundle-name": config["bundle-info"]["bundle-name"],
            "apl": correct_apl,  # 修改
            "app-feature": correct_feature  # 修改
        },
        "validity": config["validity"],
        "issuer": config.get("issuer", "pki_internal")
    }
    
    # 关键：保留所有原始字段
    if "permissions" in config:
        template["permissions"] = config["permissions"]
    
    if "acls" in config:
        template["acls"] = config["acls"]  # 必须保留！
    
    # 保留其他未知字段
    for key in config:
        if key not in template:
            template[key] = config[key]
    
    return template
```

## 实现要点

### 1. P7B文件解析

**使用工具**：`openssl cms -verify`

```bash
# 提取JSON配置
openssl cms -verify -in file.p7b -inform DER -noverify
```

**注意事项**：
- p7b是二进制格式，内部包含JSON配置
- 不需要完整解析证书数据
- 使用`-noverify`参数跳过证书验证

### 2. 签名工具使用

**工具路径**：`/home/xianf/master/xts_acts_wiki/signature_tools/`

**必需文件**：
- `hap-sign-tool.jar` - HAP签名工具
- `OpenHarmony.p12` - 签名密钥（密码：123456）
- `OpenHarmonyProfileRelease.pem` - 发布证书

**签名命令格式**：
```bash
java -jar hap-sign-tool.jar sign-profile \
  -mode localSign \
  -keyAlias "OpenHarmony Application Profile Release" \
  -keyPwd "123456" \
  -inFile profile.json \
  -outFile output.p7b \
  -keystoreFile OpenHarmony.p12 \
  -keystorePwd "123456" \
  -signAlg SHA256withECDSA \
  -profileCertFile OpenHarmonyProfileRelease.pem \
  -validity 365 \
  -developer-id "OpenHarmony"
```

### 3. 字段保留（最关键！）

**必须保留的字段**：
1. `acls` - ACL权限列表（最重要！）
2. `permissions` - 受限权限列表
3. `distribution-certificate` - 证书信息
4. `bundle-name` - 应用包名
5. `uuid` - 唯一标识符
6. `validity` - 有效期

**只修改的字段**：
1. `bundle-info.apl` - APL等级
2. `bundle-info.app-feature` - 应用特性

### 4. 错误处理

**需要处理的异常**：
1. p7b文件不存在或无法读取
2. JSON解析失败
3. 签名工具执行失败
4. 权限级别未知（需要用户确认）

**错误处理策略**：
- 记录详细日志
- 不中断批量处理
- 统计成功/失败数量
- 提供失败原因

### 5. 备份策略

**实现方式**：
```python
# 伪代码
if backup:
    backup_path = p7b_path.with_suffix('.p7b.backup')
    shutil.copy2(p7b_path, backup_path)
```

**备份文件命名**：`原文件名.p7b.backup`

## 命令行接口设计

### 参数设计

```
用法: fix_r012_p7b.py [files...] [options]

位置参数:
  files                 要修复的p7b文件路径（可指定多个）

可选参数:
  -h, --help            显示帮助信息
  -l FILE, --file-list FILE
                        从文本文件读取p7b文件路径列表
  --no-backup           不备份原文件
  -v, --verbose         显示详细输出
```

### 使用示例

```bash
# 修复单个文件
python3 fix_r012_p7b.py /path/to/file.p7b

# 修复多个文件
python3 fix_r012_p7b.py file1.p7b file2.p7b file3.p7b

# 从文件列表读取
python3 fix_r012_p7b.py --file-list p7b_files.txt

# 详细输出
python3 fix_r012_p7b.py -v /path/to/file.p7b

# 不备份
python3 fix_r012_p7b.py --no-backup /path/to/file.p7b
```

## 验证方法

### 1. 配置字段验证

```bash
# 查看修复后的配置
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | \
  python3 -m json.tool
```

**检查项**：
- ✅ `apl`字段值正确（normal或system_basic）
- ✅ `app-feature`字段值为`hos_normal_app`
- ✅ `acls`字段完整保留
- ✅ `permissions`字段完整保留

### 2. 字段完整性验证

```bash
# 对比修复前后的差异
diff <(openssl cms -verify -in file.p7b.backup -inform DER -noverify 2>/dev/null | \
       python3 -m json.tool) \
     <(openssl cms -verify -in file.p7b -inform DER -noverify 2>/dev/null | \
       python3 -m json.tool)
```

**预期结果**：
- 只有`apl`和`app-feature`字段发生变化
- 其他所有字段保持不变

## 常见问题处理

### Q1: 如何处理未知权限？

**方案**：
1. 记录未知权限列表
2. 在修复完成后输出提示
3. 建议用户手动确认权限级别
4. 默认使用`normal`级别（保守策略）

### Q2: 如何处理签名失败？

**方案**：
1. 检查Java环境是否正确
2. 检查签名工具路径是否正确
3. 检查密钥文件和证书是否存在
4. 记录详细错误日志

### Q3: 如何确保字段不丢失？

**方案**：
1. 使用完整的字段复制逻辑
2. 修复后立即验证字段完整性
3. 提供对比工具检查差异
4. 保留备份文件支持回滚

## 代码生成提示

当AI根据此设计文档生成代码时，应该：

1. **优先考虑字段保留**：使用通用的字段复制逻辑，不要硬编码特定字段
2. **添加详细日志**：每个关键步骤都输出日志信息
3. **完善的错误处理**：捕获所有可能的异常，提供友好的错误信息
4. **备份机制**：默认备份原文件，支持`--no-backup`参数
5. **验证机制**：修复后自动验证字段完整性
6. **批量处理**：支持单个文件和批量处理模式

## 测试用例

### 测试场景1：普通应用（无权限）

**输入**：
```json
{
  "bundle-info": {
    "apl": "system_core",
    "app-feature": "hos_system_app"
  }
}
```

**预期输出**：
```json
{
  "bundle-info": {
    "apl": "normal",
    "app-feature": "hos_normal_app"
  }
}
```

### 测试场景2：应用带ACL权限

**输入**：
```json
{
  "bundle-info": {
    "apl": "system_core",
    "app-feature": "hos_system_app"
  },
  "acls": {
    "allowed-acls": [
      "ohos.permission.VISIBLE_WINDOW_INFO"
    ]
  }
}
```

**预期输出**：
```json
{
  "bundle-info": {
    "apl": "normal",
    "app-feature": "hos_normal_app"
  },
  "acls": {
    "allowed-acls": [
      "ohos.permission.VISIBLE_WINDOW_INFO"
    ]
  }
}
```

**关键验证**：`acls`字段必须完整保留！

### 测试场景3：应用带system_basic权限

**输入**：
```json
{
  "bundle-info": {
    "apl": "system_core",
    "app-feature": "hos_system_app"
  },
  "acls": {
    "allowed-acls": [
      "ohos.permission.MANAGE_BLUETOOTH"
    ]
  }
}
```

**预期输出**：
```json
{
  "bundle-info": {
    "apl": "system_basic",
    "app-feature": "hos_normal_app"
  },
  "acls": {
    "allowed-acls": [
      "ohos.permission.MANAGE_BLUETOOTH"
    ]
  }
}
```

## 相关文档

- [R012问题修复指南](./R012_FIX_GUIDE.md)
- [R012问题历史记录](./R012_ISSUE_HISTORY.md)
- [签名工具使用指导](./signature_tools/使用指导.docx)
