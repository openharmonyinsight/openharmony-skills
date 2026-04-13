# R012: 签名证书APL等级和app-feature配置错误

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R012 |
| 问题类型 | 签名证书APL等级和app-feature配置错误 |
| 严重级别 | Critical |
| 规则复杂度 | simple |
| 扫描范围 | 所有.p7b文件（signature/*.p7b 和 根目录*.p7b） |
| testcase字段 | `-`（p7b为非测试文件，无对应it()块） |

## 问题描述

签名证书p7b文件中使用了`system_core`等级或`app-feature`字段配置错误。

- **规范要求**：
  - `apl`字段：控制应用等级，默认普通应用配置为`normal`，禁止使用`system_core`
  - `app-feature`字段：控制普通应用还是系统应用，开源仓默认为`hos_normal_app`
  - 极少数情况可以使用`system_basic`（仅限于涉及特定受限权限）
  - 高于APL等级的权限依据"权限ACL是否使能"在acls中进行权限申请

## 修复建议

使用`normal`等级，`app-feature`配置为`hos_normal_app`。修复时必须使用签名工具重新生成p7b文件（直接修改JSON会导致签名失效）。

## 权限分类标准（A-H类）

扫描R012时，必须提取p7b文件中的`acls.allowed-acls`和`permissions.restricted-permissions`字段，对涉及权限进行A-H类分类。分类结果写入Excel"修复建议"列。

| 权限类型 | 文档来源 | 正确apl | 正确app-feature | 是否需确认 | 说明 |
|---------|---------|--------|---------------|-----------|------|
| A类 | permissions-for-all-user.md | normal | hos_normal_app | 否 | 用户授权开放权限 |
| B类 | permissions-for-all.md | normal | hos_normal_app | 否 | 系统授权开放权限 |
| C类 | restricted-permissions.md | system_basic | hos_normal_app | 否 | 受限权限（通过ACL申请） |
| D类 | permissions-for-enterprise-apps.md | system_basic | hos_system_app | **是** | 企业应用权限 |
| E类 | permissions-for-mdm-apps.md | system_basic | hos_system_app | **是** | MDM应用权限 |
| F类 | permissions-for-system-apps-no-acl.md | system_basic | hos_system_app | **是** | 系统应用权限（无ACL），不推荐 |
| G类 | permissions-for-system-apps-user.md | system_basic | hos_system_app | **是** | 系统应用权限（用户授权），不推荐 |
| H类 | permissions-for-system-apps.md | system_basic | hos_system_app | **是** | 系统应用权限，不推荐 |
| 未知 | 不在上述文档中 | 需确认 | 需确认 | **是** | 新增或自定义权限 |

## Excel修复建议格式（6个场景）

### 场景1：无权限或仅A/B类权限（可自动修复）

```
当前: apl=system_core, app-feature=hos_normal_app。涉及权限: A类(ohos.permission.CAMERA), B类(ohos.permission.INTERNET)。
建议: 可自动修复。将apl改为normal, app-feature保持hos_normal_app。保留acls字段。
```

### 场景2：含C类权限（可自动修复）

```
当前: apl=system_core, app-feature=hos_normal_app。涉及权限: C类(ohos.permission.SYSTEM_FLOAT_WINDOW)。
建议: 可自动修复。将apl改为system_basic, app-feature保持hos_normal_app。必须保留acls字段: ["ohos.permission.SYSTEM_FLOAT_WINDOW"]。
```

### 场景3：含D/E类权限（需用户确认）

```
当前: apl=system_core, app-feature=hos_system_app。涉及权限: D类(ohos.permission.GET_BUNDLE_INFO_PRIVILEGED)。
建议: 【需用户确认】检测到企业应用权限(D类)。如确认为企业应用: apl=system_basic, app-feature=hos_system_app; 如为普通应用: 移除该权限后 apl=normal, app-feature=hos_normal_app。
```

### 场景4：含F/G/H类权限（需用户确认）

```
当前: apl=system_core, app-feature=hos_system_app。涉及权限: H类(ohos.permission.INSTALL_BUNDLE)。
建议: 【需用户确认】检测到系统应用权限(H类)，开源仓不推荐使用。建议移除该权限后 apl=normal, app-feature=hos_normal_app; 如必须使用，需系统签名，apl=system_basic, app-feature=hos_system_app。
```

### 场景5：含未知权限（需用户确认）

```
当前: apl=system_core, app-feature=hos_normal_app。涉及权限: 未知(ohos.permission.CUSTOM_XXX)。
建议: 【需用户确认】检测到未知权限，不在已知权限列表中。请查阅官方文档确认权限级别。默认保守策略: apl=normal, app-feature=hos_normal_app。
```

### 场景6：混合权限（需用户确认）

```
当前: apl=system_core, app-feature=hos_system_app。涉及权限: A类(ohos.permission.INTERNET), C类(ohos.permission.SYSTEM_FLOAT_WINDOW), H类(ohos.permission.INSTALL_BUNDLE)。
建议: 【需用户确认】检测到系统应用权限(H类): ohos.permission.INSTALL_BUNDLE。建议移除H类权限后，按剩余权限确定配置: C类存在需apl=system_basic, app-feature=hos_normal_app。必须保留acls字段。
```

## 扫描逻辑

### Step 1: 查找所有p7b文件

```python
import os
import subprocess
import json
import re

def find_p7b_files(scan_root):
    p7b_files = []
    for dirpath, dirnames, filenames in os.walk(scan_root):
        for fn in filenames:
            if fn.endswith('.p7b'):
                p7b_files.append(os.path.join(dirpath, fn))
    return p7b_files
```

### Step 2: 从p7b文件中提取JSON配置

p7b文件是PKCS#7签名格式，需要使用openssl提取其中的JSON数据。

```python
def extract_p7b_json(p7b_path):
    try:
        result = subprocess.run(
            ['openssl', 'cms', '-verify', '-in', p7b_path,
             '-inform', 'DER', '-noverify'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass

    try:
        with open(p7b_path, 'rb') as f:
            raw = f.read()
        text = raw.decode('utf-8', errors='ignore')
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except (json.JSONDecodeError, Exception):
        pass

    return None
```

### Step 3: 检测问题并分类权限

```python
def classify_permissions(config, permission_db):
    acls = []
    restricted = []

    acl_section = config.get('acls', {}).get('allowed-acls', [])
    if isinstance(acl_section, list):
        acls = acl_section

    perm_section = config.get('permissions', {}).get('restricted-permissions', [])
    if isinstance(perm_section, list):
        restricted = perm_section

    all_permissions = set(acls + restricted)

    classified = {}
    for perm in all_permissions:
        category = permission_db.get(perm, 'unknown')
        if category not in classified:
            classified[category] = []
        classified[category].append(perm)

    return classified
```

### Step 4: 生成修复建议

```python
def generate_suggestion(config, classified):
    bundle_info = config.get('bundle-info', {})
    current_apl = bundle_info.get('apl', 'unknown')
    current_app_feature = bundle_info.get('app-feature', 'unknown')

    all_perms_desc = []
    for cat in sorted(classified.keys()):
        perms = classified[cat]
        all_perms_desc.append(f"{cat}类({', '.join(perms)})")

    perm_summary = ', '.join(all_perms_desc) if all_perms_desc else '无'

    has_system_core = current_apl == 'system_core'
    has_wrong_feature = current_app_feature != 'hos_normal_app'

    if not has_system_core and not has_wrong_feature:
        return None

    has_confirmed_types = any(c in classified for c in ['D', 'E', 'F', 'G', 'H', 'unknown'])
    has_c_type = 'C' in classified

    if has_confirmed_types:
        confirmed_types = [c for c in ['D', 'E', 'F', 'G', 'H', 'unknown'] if c in classified]
        confirmed_perms = []
        for ct in confirmed_types:
            confirmed_perms.extend(classified[ct])

        return (
            f"当前: apl={current_apl}, app-feature={current_app_feature}。"
            f"涉及权限: {perm_summary}。\n"
            f"建议: 【需用户确认】检测到需确认的权限({', '.join(confirmed_types)}类): "
            f"{', '.join(confirmed_perms)}。"
            f"请查阅官方文档确认权限级别后修改配置。"
        )

    if has_c_type:
        acls = config.get('acls', {}).get('allowed-acls', [])
        acls_str = json.dumps(acls, ensure_ascii=False)
        return (
            f"当前: apl={current_apl}, app-feature={current_app_feature}。"
            f"涉及权限: {perm_summary}。\n"
            f"建议: 可自动修复。将apl改为system_basic, app-feature保持hos_normal_app。"
            f"必须保留acls字段: {acls_str}。"
        )

    return (
        f"当前: apl={current_apl}, app-feature={current_app_feature}。"
        f"涉及权限: {perm_summary}。\n"
        f"建议: 可自动修复。将apl改为normal, app-feature保持hos_normal_app。保留acls字段。"
    )
```

### Step 5: 生成问题报告

```python
def scan_r012(scan_root, base_dir, permission_db):
    issues = []
    p7b_files = find_p7b_files(scan_root)

    for p7b_path in p7b_files:
        config = extract_p7b_json(p7b_path)
        if not config:
            continue

        bundle_info = config.get('bundle-info', {})
        current_apl = bundle_info.get('apl', '')
        current_app_feature = bundle_info.get('app-feature', '')

        has_problem = (current_apl == 'system_core') or (current_app_feature != 'hos_normal_app')
        if not has_problem:
            continue

        classified = classify_permissions(config, permission_db)
        suggestion = generate_suggestion(config, classified)
        if not suggestion:
            continue

        rel_path = os.path.relpath(p7b_path, base_dir)

        issues.append({
            'rule': 'R012',
            'type': '签名证书APL等级和app-feature配置错误',
            'severity': 'Critical',
            'file': rel_path,
            'line': 1,
            'testcase': '-',
            'snippet': f'apl={current_apl}, app-feature={current_app_feature}',
            'suggestion': suggestion,
        })

    return issues
```

## 错误示例

```json
// 错误1：apl字段使用system_core
{
  "bundle-info": {
    "apl": "system_core",
    "app-feature": "hos_normal_app"
  }
}
```

```json
// 错误2：app-feature字段不是hos_normal_app
{
  "bundle-info": {
    "apl": "normal",
    "app-feature": "hos_system_app"
  }
}
```

## 正确示例

```json
// 正确：使用normal等级和hos_normal_app
{
  "bundle-info": {
    "apl": "normal",
    "app-feature": "hos_normal_app"
  }
}
```

```json
// 正确：特殊情况使用system_basic（仅限C类受限权限）
{
  "bundle-info": {
    "apl": "system_basic",
    "app-feature": "hos_normal_app"
  },
  "acls": {
    "allowed-acls": ["ohos.permission.MANAGE_BLUETOOTH"]
  }
}
```

## 注意事项

1. **禁止直接修改p7b文件**：p7b是PKCS#7签名格式，直接修改JSON会导致签名失效，必须使用签名工具重新生成
2. **保留所有原始字段**：修复时必须保留`acls`、`permissions`、`distribution-certificate`等所有字段
3. **权限分类是扫描的核心**：扫描时必须对权限进行A-H分类，根据分类结果生成不同的修复建议
4. **未知权限需人工确认**：不在已知列表中的权限，建议使用保守策略（normal级别）

## ⚠️ 陷阱：p7b文件是DER二进制格式，不能用json.loads()直接解析

**严重性**: 极严重，导致R012规则完全失效（100%漏检）

**问题描述**: p7b签名文件本质是DER（Distinguished Encoding Rules）二进制格式（ASN.1结构），不是纯JSON文本。文件头两个字节为`0x30 0x82`（ASN.1 SEQUENCE标记），JSON配置数据嵌入在DER二进制内容的某个位置。直接对原始字节调用`json.loads()`必定抛出`UnicodeDecodeError`或`JSONDecodeError`，如果异常被静默捕获（`except: return`），会导致**所有p7b文件全部跳过**。

**典型文件头**:
```
0x30 0x82 0x0D 0xDE 0x06 0x09 0x2A 0x86 0x48 0x86 0xF7 0x0D 0x01 0x07 0x02 ...
^-- ASN.1 SEQUENCE标记       ^-- OID: 1.2.840.113549.1.7.2 (signedData)
```

**嵌入的JSON数据在DER中的分布**（以`security/access_token/AccessTokenTest/signature/openharmony_sx.p7b`为例）:
- 位置约203字节处: `{"not-before": 1594865258, "not-after": 1689473258}`
- 位置约1191字节处: `"apl":"normal","app-feature":"hos_normal_app"`
- 位置约1245字节处: `{"allowed-acls":["ohos.permission.DISTRIBUTED_DATASYNC",...]}`
- 位置约1397字节处: `{"restricted-permissions":[]}`

**错误做法**（100%漏检）:
```python
def check_r012_wrong(p7b_path):
    raw = open(p7b_path, 'rb').read()
    data = json.loads(raw)       # ← 必定失败: UnicodeDecodeError
    # 或者:
    text = raw.decode('utf-8')   # ← 必定失败: UnicodeDecodeError (0x82不是UTF-8)
    data = json.loads(text)      # ← 同样失败
```

**正确做法**: 先用`utf-8` + `errors='replace'`容错解码二进制为字符串，再用正则直接提取关键字段（无需解析完整JSON结构）:
```python
import re

def extract_p7b_fields(p7b_path):
    """
    从DER二进制p7b文件中提取apl、app-feature等字段。
    使用正则从UTF-8容错解码的文本中提取，不依赖json.loads()。
    """
    with open(p7b_path, 'rb') as f:
        raw = f.read()

    # 容错解码：二进制中的非UTF-8字节被替换为�，但嵌入的JSON文本保持完整
    text = raw.decode('utf-8', errors='replace')

    # 直接正则提取关键字段（不依赖JSON结构层级）
    apl = ''
    app_feature = ''
    acls = []
    restricted = []

    m = re.search(r'"apl"\s*:\s*"([^"]*)"', text)
    if m:
        apl = m.group(1)

    m = re.search(r'"app-feature"\s*:\s*"([^"]*)"', text)
    if m:
        app_feature = m.group(1)

    m = re.search(r'"allowed-acls"\s*:\s*\[([^\]]*)\]', text)
    if m:
        acls = [p.strip().strip('"') for p in m.group(1).split(',') if p.strip()]

    m = re.search(r'"restricted-permissions"\s*:\s*\[([^\]]*)\]', text)
    if m:
        restricted = [p.strip().strip('"') for p in m.group(1).split(',') if p.strip()]

    return apl, app_feature, acls, restricted
```

**关键要点**:
1. `raw.decode('utf-8', errors='replace')` 而非 `raw.decode('utf-8')` — 必须容错
2. 正则提取而非`json.loads()` — 无需还原完整JSON结构，直接提取目标字段
3. `errors='replace'`不影响JSON字段值 — 非UTF-8字节（如ASN.1标签）被替换为`�`，但嵌入的ASCII/UTF-8 JSON文本保持完整

**影响**: 如果扫描脚本使用`json.loads()`解析p7b且异常被静默吞掉，R012规则将完全失效，所有p7b文件都不会被检测到。实际案例：security目录71个p7b文件中存在1个`apl=system_core`问题，但因解析失败被完全漏检。

**验证方法**: 扫描完成后，检查R012结果是否为0且p7b文件数量>0。如果p7b文件存在但R012为0，需确认解析逻辑是否正确处理了DER二进制格式。

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R012` |
| type | `签名证书APL等级和app-feature配置错误` |
| severity | `Critical` |
| file | 相对路径（如`xxx/signature/openharmony_sx.p7b`） |
| line | `1` |
| testcase | `-` |
| snippet | `apl=system_core, app-feature=hos_normal_app` |
| suggestion | 包含权限分类和具体修复建议（见6个场景格式） |

## 错误/正确示例（补充）

### 错误3：app-feature字段缺失或为空

```json
{
  "profile": {
    "apl": "normal",
    "app-feature": ""
  }
}
```

**说明**: `app-feature`字段缺失或为空同样视为配置错误，开源仓默认应为`hos_normal_app`。
