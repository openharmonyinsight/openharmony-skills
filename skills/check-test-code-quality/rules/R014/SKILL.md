# R014: 测试HAP命名不规范

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R014 |
| 问题类型 | 测试HAP命名不规范 |
| 严重级别 | Critical |
| 规则复杂度 | simple |
| 扫描范围 | BUILD.gn文件中的ohos_js_app_suite、ohos_js_app_static_suite、ohos_moduletest_suite模板 |
| testcase字段 | `-`（BUILD.gn为非测试文件，无对应it()块） |

## 问题描述

测试HAP命名不符合规范要求。hap包命名采用大驼峰方式。

## 命名规范

| 模板类型 | 检测目标 | 命名规范 | 正确示例 |
|---------|---------|---------|---------|
| `ohos_js_app_suite` | `hap_name` | 以`Acts`开头（A大写），以`Test`结尾（T大写） | `ActsAbilityTest` |
| `ohos_js_app_static_suite` | `hap_name` | 以`Acts`开头（A大写），以`StaticTest`结尾（S、T大写） | `ActsAbilityStaticTest` |
| `ohos_moduletest_suite` | 模板名称`XXXX` | 以`Acts`开头（A大写），以`Test`结尾（T大写） | `ActsModuleTest` |

## 修复规则

### ohos_js_app_suite / ohos_js_app_static_suite

**只修改`hap_name`，不修改target名称。** target名称与上层BUILD.gn中deps字段的引用保持一致，与hap_name无直接关系。

### ohos_moduletest_suite

**必须修改target名称。** ohos_moduletest_suite没有hap_name字段，target名称就是输出文件名。

## 特殊排除

名称中包含`validator`的不视为问题（如`ActsValidatorTest`是合法的）。

## 扫描逻辑

### Step 1: 状态机方法解析BUILD.gn模板

使用状态机方法解析BUILD.gn文件，识别三种模板类型并提取对应的检测目标。

```python
import re
import os

TEMPLATE_TYPES = {
    'ohos_js_app_suite': {
        'pattern': re.compile(r'ohos_js_app_suite\s*\(\s*["\']([^"\']+)["\']'),
        'check_field': 'hap_name',
        'must_start': 'Acts',
        'must_end': 'Test',
    },
    'ohos_js_app_static_suite': {
        'pattern': re.compile(r'ohos_js_app_static_suite\s*\(\s*["\']([^"\']+)["\']'),
        'check_field': 'hap_name',
        'must_start': 'Acts',
        'must_end': 'StaticTest',
    },
    'ohos_moduletest_suite': {
        'pattern': re.compile(r'ohos_moduletest_suite\s*\(\s*["\']([^"\']+)["\']'),
        'check_field': 'target_name',
        'must_start': 'Acts',
        'must_end': 'Test',
    },
}

HAP_NAME_PATTERN = re.compile(r'hap_name\s*=\s*["\']([^"\']+)["\']')
```

### Step 2: 状态机解析模板块

对BUILD.gn文件进行逐行扫描，使用状态机跟踪当前所在的模板块。

```python
def parse_build_gn_templates(content):
    templates = []
    lines = content.split('\n')

    state = 'IDLE'
    current_template = None
    brace_depth = 0
    template_start_line = 0

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        if state == 'IDLE':
            for tname, tinfo in TEMPLATE_TYPES.items():
                match = tinfo['pattern'].search(line)
                if match:
                    target_name = match.group(1)
                    current_template = {
                        'type': tname,
                        'target_name': target_name,
                        'target_line': line_num,
                        'hap_name': None,
                        'hap_name_line': 0,
                    }
                    state = 'IN_TEMPLATE'
                    template_start_line = line_num
                    brace_depth = line.count('{') - line.count('}')
                    break

        elif state == 'IN_TEMPLATE':
            brace_depth += line.count('{') - line.count('}')

            hap_match = HAP_NAME_PATTERN.search(line)
            if hap_match:
                current_template['hap_name'] = hap_match.group(1)
                current_template['hap_name_line'] = line_num

            if brace_depth <= 0:
                templates.append(current_template)
                current_template = None
                state = 'IDLE'

    return templates
```

### Step 3: 验证命名规范

```python
def validate_naming(template):
    tname = template['type']
    tinfo = TEMPLATE_TYPES[tname]

    if tinfo['check_field'] == 'hap_name':
        name = template['hap_name']
        report_line = template['hap_name_line']
    else:
        name = template['target_name']
        report_line = template['target_line']

    if not name:
        return None

    if 'validator' in name.lower():
        return None

    must_start = tinfo['must_start']
    must_end = tinfo['must_end']

    starts_ok = name.startswith(must_start)
    ends_ok = name.endswith(must_end)

    if starts_ok and ends_ok:
        return None

    errors = []
    if not starts_ok:
        errors.append(f'不以"{must_start}"开头')
    if not ends_ok:
        errors.append(f'不以"{must_end}"结尾')

    return {
        'name': name,
        'line': report_line,
        'errors': errors,
        'template_type': tname,
        'check_field': tinfo['check_field'],
    }
```

### Step 4: 生成修复建议

```python
def generate_fix_suggestion(template, validation):
    name = validation['name']
    tname = validation['template_type']
    check_field = validation['check_field']
    tinfo = TEMPLATE_TYPES[tname]
    errors = validation['errors']

    must_start = tinfo['must_start']
    must_end = tinfo['must_end']

    fixed_name = name
    if not fixed_name.startswith(must_start):
        fixed_name = must_start + fixed_name[0].upper() + fixed_name[1:]
    if not fixed_name.endswith(must_end):
        fixed_name = fixed_name + 'Adapt001' + must_end

    if check_field == 'hap_name':
        target_info = f"target名称 \"{template['target_name']}\" 保持不变，只修改hap_name"
    else:
        target_info = f"target名称 \"{template['target_name']}\" 需要修改为 \"{fixed_name}\""

    return (
        f"{check_field} \"{name}\" 不符合规范：{', '.join(errors)}。"
        f"修复: {check_field}改为 \"{fixed_name}\"。{target_info}。"
    )
```

### Step 5: 生成问题报告

```python
def scan_r014(scan_root, base_dir):
    issues = []

    for dirpath, dirnames, filenames in os.walk(scan_root):
        if 'BUILD.gn' not in filenames:
            continue

        build_gn_path = os.path.join(dirpath, 'BUILD.gn')

        with open(build_gn_path, 'r', encoding='utf-8') as f:
            content = f.read()

        templates = parse_build_gn_templates(content)

        for template in templates:
            validation = validate_naming(template)
            if validation is None:
                continue

            rel_path = os.path.relpath(build_gn_path, base_dir)
            suggestion = generate_fix_suggestion(template, validation)

            if validation['check_field'] == 'hap_name':
                snippet = f'hap_name = "{validation["name"]}"'
            else:
                snippet = f'{template["type"]}("{validation["name"]}")'

            issues.append({
                'rule': 'R014',
                'type': '测试HAP命名不规范',
                'severity': 'Critical',
                'file': rel_path,
                'line': validation['line'],
                'testcase': '-',
                'snippet': snippet,
                'suggestion': suggestion,
            })

    return issues
```

## 错误示例

### 错误1：ohos_js_app_suite - hap_name不以Acts开头，不以Test结尾

```python
ohos_js_app_suite("mytest") {        # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "actsability"            # ✗ 错误：不以Acts开头，不以Test结尾
}
```

### 错误2：ohos_js_app_static_suite - hap_name不以StaticTest结尾

```python
ohos_js_app_static_suite("statictest") {  # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsTestSuite"          # ✗ 错误：不以StaticTest结尾
}
```

### 错误3：ohos_moduletest_suite - target名称不以Acts开头

```python
# ohos_moduletest_suite没有hap_name字段，target名称就是输出文件名
ohos_moduletest_suite("mymoduletest") {   # ✗ 错误：不以Acts开头，不以Test结尾
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
}
```

### 错误4：大小写不符合规范

```python
ohos_js_app_suite("test2") {
  hap_name = "actsTest"               # ✗ 错误：A应该大写
}

ohos_js_app_static_suite("test3") {
  hap_name = "Actsstatictest"         # ✗ 错误：S、T应该大写
}
```

## 正确示例

### 正确1：ohos_js_app_suite

```python
# target名称与hap_name可以不同，修复时只修改hap_name
ohos_js_app_suite("mytest") {             # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsAbilityAdapt001Test"    # ✓ 正确：以Acts开头，以Test结尾
}
```

### 正确2：ohos_js_app_static_suite

```python
ohos_js_app_static_suite("statictest") {  # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsAbilityAdapt001StaticTest"  # ✓ 正确：以Acts开头，以StaticTest结尾
}
```

### 正确3：ohos_moduletest_suite

```python
# ohos_moduletest_suite没有hap_name字段，target名称需要符合规范
ohos_moduletest_suite("ActsMyModuleAdapt001Test") {  # ✓ 正确
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
}
```

### 特殊排除：validator

```python
ohos_js_app_suite("valtest") {
  hap_name = "ActsValidatorTest"       # ✓ 不是问题：包含validator
}
```

## 完整修复示例（含BUILD.gn上下文）

### 修复1：ohos_js_app_suite（只修改hap_name）

修复前:
```python
# BUILD.gn
ohos_js_app_suite("mytest") {        # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "actsability"           # ✗ 不符合规范
}

# Test.json
{
  "test-file-name": ["actsability.hap"]
}
```

修复后:
```python
# BUILD.gn
ohos_js_app_suite("mytest") {        # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsAbilityAdapt001Test"  # ✓ 只修改hap_name
}

# Test.json
{
  "test-file-name": ["ActsAbilityAdapt001Test.hap"]
}
```

### 修复2：ohos_moduletest_suite（修改target名称）

修复前:
```python
# BUILD.gn
ohos_moduletest_suite("mymoduletest") {  # ✗ 不符合规范
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
}

# Test.json
{
  "kits": [{
    "push": ["mymoduletest->/data/local/tmp/mymoduletest"]
  }],
  "driver": {
    "module-name": "mymoduletest"
  }
}
```

修复后:
```python
# BUILD.gn
ohos_moduletest_suite("ActsMyModuleAdapt001Test") {  # ✓ 修改target名称
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
}

# Test.json
{
  "kits": [{
    "push": ["ActsMyModuleAdapt001Test->/data/local/tmp/ActsMyModuleAdapt001Test"]
  }],
  "driver": {
    "module-name": "ActsMyModuleAdapt001Test"
  }
}
```

## 注意事项

1. **修复ohos_js_app_suite/ohos_js_app_static_suite时，绝对不能修改target名称**，只修改hap_name
2. **修复ohos_moduletest_suite时，必须修改target名称**，因为没有hap_name字段
3. 修复BUILD.gn后，需同步修改Test.json中的文件名引用（如`test-file-name`、`push`路径、`module-name`等）
4. 包含`validator`的hap名称不视为问题
5. 状态机方法能正确处理嵌套的BUILD.gn结构（如模板内的if/else块）

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R014` |
| type | `测试HAP命名不规范` |
| severity | `Critical` |
| file | 相对路径（如`xxx/BUILD.gn`） |
| line | hap_name或target名称所在行号 |
| testcase | `-` |
| snippet | `hap_name = "xxx"` 或 `ohos_moduletest_suite("xxx")` |
| suggestion | hap_name "xxx" 不符合规范：不以"Acts"开头, 不以"Test"结尾。修复: hap_name改为 "ActsXxxAdapt001Test"。target名称 "yyy" 保持不变，只修改hap_name。 |

## 错误/正确示例（补充）

### 错误5：命名不以Acts开头

```python
ohos_js_app_suite("test1") {         # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "MyTest"  # ✗ 错误：不以Acts开头
}
```

## 实现细节

### 额外正确/错误格式示例

**ohos_js_app_suite模板 - 正确格式**:
- `ActsAbilityTest` - 以Acts开头，Test结尾
- `ActsWindowManagerTest` - 以Acts开头，Test结尾

**ohos_js_app_static_suite模板 - 正确格式**:
- `ActsAbilityStaticTest` - 以Acts开头，StaticTest结尾
- `ActsNotificationThirdPartyWatchPermissionStaticTest` - 以Acts开头，StaticTest结尾

**ohos_moduletest_suite模板 - 正确格式**:
- `ActsModuleTest` - 以Acts开头，Test结尾
- `ActsAbilityTest` - 以Acts开头，Test结尾

**错误格式**:
- `actsStartSelfUIAbilityStaticTest` - 首字母小写（错误）
- `ActsAbility` - 缺少Test/StaticTest结尾（错误）
- `AbilityTest` - 缺少Acts开头（错误）
- `ActsStatictest` - T未大写（错误）
