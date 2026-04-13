# XTS测试代码质量检查 - 问题修复指南

本文档介绍如何使用自动修复脚本修复XTS测试代码质量问题。

## 概述

针对某些常见问题，工具提供了自动修复脚本。修复脚本可以：
- 从Excel报告中读取问题
- 自动修复代码中的问题
- 输出修复统计信息

## 使用方法

### 统一修复命令（推荐）

使用 `fix_issues.py` 命令进行问题修复，该命令会自动加载对应的修复脚本：

```bash
# 修复R002问题
/fix-issues multimedia_quality_report.xlsx R002

# 修复R003问题
/fix-issues code_quality_report.xlsx R003
```

**支持的规则**:
- R002 - 错误码断言必须是number类型
- 更多规则敬请期待

### 手动修复脚本

所有修复脚本位于`fixers/`目录下：

```
fixers/
├── fix_r002.py          # R002问题修复脚本
└── README.md            # 修复脚本使用指南
```

## R002问题修复

### 问题描述

`error.code`断言使用string类型

### 使用步骤

1. **运行扫描生成Excel报告**:
   ```bash
   python3 check-test-code-quality.py /path/to/code --level critical --rules R002
   ```
   这将生成一个Excel报告文件，例如：`multimedia_quality_report.xlsx`

2. **运行修复脚本**:
   ```bash
   # 推荐方式：使用统一修复命令
   /fix-issues multimedia_quality_report.xlsx R002
   
   # 或者：直接运行修复脚本
   python3 fixers/fix_r002.py /path/to/multimedia_quality_report.xlsx
   ```

3. **验证修复结果**:
   ```bash
   python3 check-test-code-quality.py /path/to/code --level critical --rules R002
   ```
   检查R002问题数量是否减少。

### 修复内容

该脚本会自动修复以下问题：

1. **直接使用string字面量**:
   - `expect(error.code).assertEqual("401")` → `expect(error.code).assertEqual(401)`
   - `expect(error.code).assertEqual('401')` → `expect(error.code).assertEqual(401)`
   - `expect(error.code == "401").assertTrue()` → `expect(error.code == 401).assertTrue()`
   - `expect(error.code === '401').assertTrue()` → `expect(error.code === 401).assertTrue()`
   - `expect(error.code === '401' || error.code === '402').assertTrue()` → `expect(error.code === 401 || error.code === 402).assertTrue()`

2. **修改变量定义**:
   - `const ERROR_PArameter = '23800151'` → `const ERROR_PArameter = 23800151`
   - `errCode: string` → `errCode: number`
   - `let errCode = '401'` → `let errCode = 401`

### 注意事项

- 修复脚本会直接修改原文件，建议在修复前提交代码到版本控制系统
- 修复后建议运行测试用例验证功能正常
- 某些复杂情况可能需要手动修复

## 完整工作流程示例

```bash
# 1. 扫描R002问题
python3 check-test-code-quality.py /path/to/code -- --rules R002

# 2. 运行修复脚本
/fix-issues /path/to/code_quality_report.xlsx R002

# 3. 验证修复结果
python3 check-test-code-quality.py /path/to/code --level critical --rules R002
```

## 问题扫描和自动修复

### 命令格式

```
/check-test-code-quality <file_or_directory> --rules <rule_id> --fix
```

### 说明

- 扫描指定路径下的指定规则问题
- 自动生成Excel报告
- 自动调用对应的修复脚本
- 自动验证修复结果

### 示例

```bash
# 扫描并修复R002问题
/check-test-code-quality /path/to/code --rules R002 --fix

# 扫描并修复R012问题
/check-test-code-quality /path/to/code --rules R012 --fix

# 扫描并修复多个规则
/check-test-code-quality /path/to/code --rules R002,R003 --fix
```

### 支持的规则

- R002 - 错误码断言必须是number类型
- R012 - 签名证书APL等级和app-feature配置错误
- R016 - testcase命名规范（移除特殊字符 + Adapt+三位数字后缀 + 同步@tc.name）
- 更多规则敬请期待

### 注意事项

- 修复脚本会直接修改原文件，建议在修复前提交代码到版本控制系统
- 修复后建议运行测试用例验证功能正常

## R012问题修复

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
       写入 guides/signature_tools/UnsgnedReleasedProfileTemplate.json
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

将提取的字段写入 `guides/signature_tools/UnsgnedReleasedProfileTemplate.json`：
- **修改** `apl` 和 `app-feature` 字段
- **保留** `app-distribution-type`、`validity`、`bundle-name`、`acls` 的内容

**步骤4：使用签名工具重新签名**
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
- 签名工具：`guides/signature_tools/`

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
