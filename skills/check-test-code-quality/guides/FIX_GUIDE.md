# XTS测试代码质量检查 - 问题修复指南

本文档介绍如何修复XTS测试代码质量问题。当用户使用 `--fix` 参数时，按对应修复指南执行自动修复。

## 支持自动修复的规则

| 规则 | 修复指南 | 修复内容 |
|------|---------|---------|
| R008 | `guides/R008_testcase_format/R008_FIX_GUIDE.md` | @tc.xxx冒号改空格、删除多余空行 |
| R011 | `guides/R011_testsuite_duplicate/R011_FIX_GUIDE.md` | describe名称追加Adapt后缀 |
| R012 | `guides/R012_p7b_signature/R012_FIX_GUIDE.md` | p7b签名证书重新生成（需hap-sign-tool.jar） |
| R014 | `guides/R014_hap_naming/R014_HAP_NAMING_GUIDE.md` | BUILD.gn hap命名修正+Test.json同步 |
| R016 | `guides/R016_testcase_naming/R016_FIX_GUIDE.md` | 特殊字符移除+Adapt后缀+同步@tc.name |
| R018 | `guides/R018_testcase_duplicate/R018_FIX_GUIDE.md` | testcase名称去重+Adapt后缀+同步@tc.name |

## 使用方法

### 问题描述

签名证书p7b文件中使用了`system_core`等级或`app-feature`字段配置错误

### ⚠️ 重要提醒

**直接修改p7b文件中的字段会导致编译报错！** 必须使用签名工具重新生成p7b文件。

### 修复方法一：AI自动修复（推荐）

当用户请求修复R012问题时（如 `/check-test-code-quality /path --rules R012 --fix`），AI应自动执行以下流程：

```
步骤1：提取JSON配置
       openssl cms -verify -in <p7b文件> -inform DER -noverify
       ↓
步骤2：检测问题
       - apl == "system_core" ?
       - app-feature != "hos_normal_app" ?
       ↓
步骤3：修改并保留字段
       - 保留: app-distribution-type, validity, bundle-name, acls
       - 修改: apl → "normal", app-feature → "hos_normal_app"
       ↓
步骤4：写入模板文件
       写入 guides/R012_p7b_signature/signature_tools/UnsgnedReleasedProfileTemplate.json
       ↓
步骤5：重新签名
       java -jar hap-sign-tool.jar sign-profile ...
       ↓
步骤6：替换原文件
       备份为 .p7b.backup，替换为新生成的p7b
```

**关键命令：**
```bash
# 重新签名
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

详细修复指南请参考：`guides/R012_p7b_signature/R012_FIX_GUIDE.md`

### 修复方法二：手动修复

#### 修复步骤（必须严格按顺序执行）

**步骤1：将p7b文件转化成JSON文件**
```bash
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > profile.json
```

**步骤2：提取JSON文件中的关键字段**

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

**步骤3：修改UnsgnedReleasedProfileTemplate.json**

将提取的字段写入 `guides/R012_p7b_signature/signature_tools/UnsgnedReleasedProfileTemplate.json`：
- **修改** `apl` 和 `app-feature` 字段
- **保留** `app-distribution-type`、`validity`、`bundle-name`、`acls` 的内容

**步骤4：使用签名工具重新签名**
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

**步骤5：替换原文件**
```bash
# 替换（保持与原文件同名）
cp myApplication_ohos_Provision.p7b openharmony_sx.p7b
```

### 规范要求

- **app-feature字段**: 必须配置为 `hos_normal_app`（开源仓默认为普通应用）
- **apl字段**: 默认配置为 `normal`，特定权限场景可使用 `system_basic`
- **禁止使用** `system_core` 等级

### 验证修复结果

```bash
# 检查配置字段
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify | python3 -m json.tool
```

### 常见问题

**Q: 直接修改p7b文件后编译报错？**
A: p7b是PKCS#7签名格式，直接修改JSON会导致签名失效。必须使用签名工具重新生成。

**Q: 修复后acls字段丢失？**
A: 确保在步骤3中保留原文件的acls字段内容

**Q: 编译报错 "Common name of certificate is empty!"？**
A: 这是证书字段被截断导致的。解决方案：
```bash
# 使用Python脚本保留完整证书
openssl cms -verify -in openharmony_sx.p7b -inform DER -noverify > original.json

python3 << 'EOF'
import json
with open('original.json', 'r') as f:
    config = json.load(f)
config['bundle-info']['apl'] = 'normal'
config['bundle-info']['app-feature'] = 'hos_normal_app'
with open('UnsgnedReleasedProfileTemplate.json', 'w') as f:
    json.dump(config, f, indent=4)
EOF

# 验证证书长度（应 > 800）
python3 -c "import json; c=json.load(open('UnsgnedReleasedProfileTemplate.json')); print(f'证书长度: {len(c[\"bundle-info\"][\"distribution-certificate\"])}')"
```

## 更多信息

更多详细信息请参考：
- R012详细修复指南：`guides/R012_p7b_signature/R012_FIX_GUIDE.md`
- R012设计文档：`guides/R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md`
- R016修复指南：`guides/R016_testcase_naming/R016_FIX_GUIDE.md`
- 签名工具：`guides/R012_p7b_signature/signature_tools/`

## R016问题修复

### 问题描述

testcase名称包含特殊字符（仅允许英文字母、数字、下划线、连字符）。

### 修复规则

1. **移除特殊字符**：将testcase名称中所有非`[a-zA-Z0-9_-]`的字符直接移除
2. **追加后缀**：移除后追加`Adapt`+三位数字后缀（从`001`开始）
3. **去重递增**：如果追加后命名存在重复，数字递增（`001` -> `002` -> `003`...）
4. **同步@tc.name**：修改`it()`参数时，必须同步修改对应的`@tc.name`值

### 修复示例

```javascript
// 修复前
/**
 * @tc.name   ArkUX_ohos.curves_customCurve_1000
 * @tc.number ArkUX_ohos.curves_customCurve_1000
 */
it('ArkUX_ohos.curves_customCurve_1000', Level.LEVEL0, async (done: Function) => {

// 修复后
/**
 * @tc.name   ArkUX_ohoscurves_customCurve_1000Adapt001
 * @tc.number ArkUX_ohos.curves_customCurve_1000
 */
it('ArkUX_ohoscurves_customCurve_1000Adapt001', Level.LEVEL0, async (done: Function) => {
```

### 注意事项

- 仅修改`it()`和`@tc.name`，不修改`@tc.number`、`@tc.desc`等其他字段
- `used_names`集合跨文件共享，确保全局唯一
- 修复前建议备份原文件或提交代码到版本控制系统

详细修复指南请参考：`guides/R016_testcase_naming/R016_FIX_GUIDE.md`

## R008问题修复

### 问题描述

用例声明格式不规范，主要包括@tc.xxx参数使用冒号分隔符、文档注释后多余空行等。

详细修复指南请参考：`guides/R008_testcase_format/R008_FIX_GUIDE.md`

## R011问题修复

### 问题描述

同一独立XTS工程内testsuite（describe）名称重复。

详细修复指南请参考：`guides/R011_testsuite_duplicate/R011_FIX_GUIDE.md`

## R014问题修复

### 问题描述

测试HAP命名不符合规范。

详细修复指南请参考：`guides/R014_hap_naming/R014_HAP_NAMING_GUIDE.md`

## 更多信息

- R012详细修复指南：`guides/R012_p7b_signature/R012_FIX_GUIDE.md`
- R012设计文档：`guides/R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md`
- R016修复指南：`guides/R016_testcase_naming/R016_FIX_GUIDE.md`
- 签名工具：`guides/R012_p7b_signature/signature_tools/`
