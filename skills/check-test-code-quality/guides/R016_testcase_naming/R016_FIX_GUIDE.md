# R016: testcase命名规范修复指南

## 问题描述

testcase名称包含特殊字符（仅允许英文字母、数字、下划线、连字符）。

常见特殊字符包括：`.`（点）、`/`（斜杠）、`&`（与号）、` `（空格）、`[`、`]`、`(`、`)`、`...`等。

## 修复规则

### 自动修复命名格式

1. **移除特殊字符**：将testcase名称中所有非`[a-zA-Z0-9_-]`的字符直接移除
2. **追加后缀**：移除特殊字符后，在名称末尾追加`Adapt` + 三位数字编号（从`001`开始）
3. **去重递增**：如果追加后缀后命名存在重复，数字递增（`001` -> `002` -> `003`...）

**格式**: `{移除特殊字符后的名称}Adapt{三位数字}`

### 数字递增规则

- 从`001`开始（三位数字补零）
- 如果`XxxAdapt001`已存在，则使用`XxxAdapt002`
- 依此类推

### 同步更新 @tc.name

**关键要求**：修改`it()`参数时，必须同步修改对应的`@tc.name`值，保持一致。

- `@tc.name`位于`it()`上方的JSDoc注释块中
- `@tc.name`的值必须与`it()`的第一个参数完全一致

## 修复示例

### 示例1: 包含`.`（点号）

**修复前**:
```javascript
/**
 * @tc.name   ArkUX_ohos.curves_customCurve_1000
 * @tc.number ArkUX_ohos.curves_customCurve_1000
 * @tc.desc   ArkUX_ohos.curves_customCurve_1000
 */
it('ArkUX_ohos.curves_customCurve_1000', Level.LEVEL0, async (done: Function) => {
```

**修复后**:
```javascript
/**
 * @tc.name   ArkUX_ohoscurves_customCurve_1000Adapt001
 * @tc.number ArkUX_ohos.curves_customCurve_1000
 * @tc.desc   ArkUX_ohos.curves_customCurve_1000
 */
it('ArkUX_ohoscurves_customCurve_1000Adapt001', Level.LEVEL0, async (done: Function) => {
```

### 示例2: 包含`&`（与号）

**修复前**:
```javascript
/**
 * @tc.name   testAlignContentCenterFlexMargin&PaddingNOSatisfy
 * @tc.number testAlignContentCenterFlexMargin&PaddingNOSatisfy
 */
it('testAlignContentCenterFlexMargin&PaddingNOSatisfy', Level.LEVEL0, async () => {
```

**修复后**:
```javascript
/**
 * @tc.name   testAlignContentCenterFlexMarginPaddingNOSatisfyAdapt001
 * @tc.number testAlignContentCenterFlexMargin&PaddingNOSatisfy
 */
it('testAlignContentCenterFlexMarginPaddingNOSatisfyAdapt001', Level.LEVEL0, async () => {
```

### 示例3: 包含`/`（斜杠）

**修复前**:
```javascript
/**
 * @tc.name   SUB_MULTIMEDIA_AUDIO_SET/GET_SPEED_0100
 * @tc.number SUB_MULTIMEDIA_AUDIO_SET/GET_SPEED_0100
 */
it('SUB_MULTIMEDIA_AUDIO_SET/GET_SPEED_0100', Level.LEVEL0, async () => {
```

**修复后**:
```javascript
/**
 * @tc.name   SUB_MULTIMEDIA_AUDIO_SETGET_SPEED_0100Adapt001
 * @tc.number SUB_MULTIMEDIA_AUDIO_SET/GET_SPEED_0100
 */
it('SUB_MULTIMEDIA_AUDIO_SETGET_SPEED_0100Adapt001', Level.LEVEL0, async () => {
```

### 示例4: 包含空格

**修复前**:
```javascript
/**
 * @tc.name    WorkSchedulerJsTest051
 */
it('  WorkSchedulerJsTest051', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
```

**修复后**:
```javascript
/**
 * @tc.name   WorkSchedulerJsTest051Adapt001
 */
it('WorkSchedulerJsTest051Adapt001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
```

### 示例5: 包含`...`（省略号）

**修复前**:
```javascript
/**
 * @tc.name   test for...in
 * @tc.number SUB_COMMONLIBRARY_ETSUTILS_ES2020NewFeatures_0010
 */
it('test for...in', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, () => {
```

**修复后**:
```javascript
/**
 * @tc.name   testforinAdapt001
 * @tc.number SUB_COMMONLIBRARY_ETSUTILS_ES2020NewFeatures_0010
 */
it('testforinAdapt001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, () => {
```

### 示例6: 去重递增

**修复前**（同一文件中多个`it()`移除特殊字符后名称相同）:
```javascript
// File A - 两个it()名称包含不同特殊字符，移除后相同
it('test.name.001', Level.LEVEL0, ...)   // 移除.后: testname001
it('test#name#001', Level.LEVEL0, ...)   // 移除#后: testname001 (重复!)
```

**修复后**:
```javascript
it('testname001Adapt001', Level.LEVEL0, ...)
it('testname001Adapt002', Level.LEVEL0, ...)
```

## 自动修复实现

### Python修复脚本

```python
import re
import os
from typing import Dict, List, Tuple, Optional, Set

def sanitize_tc_name(name: str) -> str:
    """
    移除testcase名称中的特殊字符，仅保留[a-zA-Z0-9_-]
    
    Args:
        name: 原始testcase名称
        
    Returns:
        移除特殊字符后的名称
    """
    return re.sub(r'[^a-zA-Z0-9_-]', '', name)

def find_unique_name(base_name: str, used_names: Set[str]) -> str:
    """
    为基础名称追加Adapt+数字后缀，确保唯一
    
    Args:
        base_name: 移除特殊字符后的基础名称
        used_names: 已使用的名称集合
        
    Returns:
        唯一的名称
    """
    counter = 1
    while True:
        candidate = f"{base_name}Adapt{counter:03d}"
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate
        counter += 1

def fix_r016_file(file_path: str, content: str, used_names: Optional[Set[str]] = None) -> Tuple[str, List[dict]]:
    """
    修复单个文件的R016 testcase命名问题
    
    Args:
        file_path: 文件路径
        content: 文件内容
        used_names: 已使用的名称集合（跨文件去重用），为None则创建新集合
        
    Returns:
        (修复后的内容, 修复记录列表)
        每条修复记录: {'line': int, 'old_name': str, 'new_name': str}
    """
    if used_names is None:
        used_names = set()
    
    lines = content.split('\n')
    fixes = []
    tc_name_pattern = re.compile(r"^\s*it\s*\(\s*['\"]([^'\"]+)['\"]")
    tc_name_javadoc_pattern = re.compile(r"(\*\s*@tc\.name\s+)(\S+)")
    
    # 第一遍：收集所有it()行号和原始名称
    it_entries = []
    for i, line in enumerate(lines):
        match = tc_name_pattern.search(line)
        if match:
            original_name = match.group(1)
            if not re.match(r'^[a-zA-Z0-9_-]+$', original_name):
                it_entries.append((i, original_name))
    
    if not it_entries:
        return content, []
    
    # 第二遍：为每个需要修复的it()生成新名称
    name_mapping = {}  # original_name -> new_name (file内去重)
    for line_idx, original_name in it_entries:
        base = sanitize_tc_name(original_name)
        if not base:
            base = 'unnamedTest'
        new_name = find_unique_name(base, used_names)
        name_mapping[original_name] = new_name
    
    # 第三遍：修改文件内容
    # 先收集文件中已有的所有it()名称（包括不需要修复的），用于@tc.name定位
    existing_it_names = set()
    for line in lines:
        match = tc_name_pattern.search(line)
        if match:
            existing_it_names.add(match.group(1))
    
    # 修改it()行
    for line_idx, original_name in it_entries:
        new_name = name_mapping[original_name]
        old_line = lines[line_idx]
        new_line = old_line.replace(f"'{original_name}'", f"'{new_name}'")
        if new_line == old_line:
            new_line = old_line.replace(f'"{original_name}"', f'"{new_name}"')
        if new_line != old_line:
            lines[line_idx] = new_line
            fixes.append({
                'line': line_idx + 1,
                'old_name': original_name,
                'new_name': new_name
            })
    
    # 修改@tc.name行
    # 查找每个it()上方最近的@tc.name
    for line_idx, original_name in it_entries:
        new_name = name_mapping[original_name]
        # 向上搜索@tc.name（最多搜索20行）
        for j in range(line_idx - 1, max(line_idx - 20, -1), -1):
            match = tc_name_javadoc_pattern.search(lines[j])
            if match:
                current_tc_name = match.group(2)
                if current_tc_name == original_name:
                    lines[j] = lines[j].replace(
                        f"@tc.name   {original_name}",
                        f"@tc.name   {new_name}"
                    )
                    if lines[j] == lines[j]:
                        lines[j] = lines[j].replace(
                            f"@tc.name  {original_name}",
                            f"@tc.name  {new_name}"
                        )
                    if lines[j] == lines[j]:
                        lines[j] = lines[j].replace(
                            f"@tc.name {original_name}",
                            f"@tc.name {new_name}"
                        )
                break
    
    return '\n'.join(lines), fixes

def fix_r016_directory(dir_path: str) -> Dict[str, List[dict]]:
    """
    修复目录下所有测试文件的R016问题
    
    Args:
        dir_path: 目录路径
        
    Returns:
        修复结果 {文件路径: [修复记录]}
    """
    used_names = set()
    results = {}
    
    test_extensions = ('.test.ets', '.test.ts', '.test.js')
    
    for root, dirs, files in os.walk(dir_path):
        for fname in files:
            if any(fname.endswith(ext) for ext in test_extensions):
                file_path = os.path.join(root, fname)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content, fixes = fix_r016_file(file_path, content, used_names)
                
                if fixes:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    results[file_path] = fixes
                    for fix in fixes:
                        print(f"  {file_path}:{fix['line']} "
                              f"'{fix['old_name']}' -> '{fix['new_name']}'")
    
    return results

# 使用示例
if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    results = fix_r016_directory(target)
    total = sum(len(v) for v in results.values())
    print(f"\n共修复 {len(results)} 个文件，{total} 处问题")
```

## 修复验证

修复完成后，需要验证：

1. **命名规范**: 确保新名称仅包含`[a-zA-Z0-9_-]`
2. **名称唯一**: 确保修复后无重复testcase名称
3. **@tc.name一致**: 确保`@tc.name`与`it()`第一个参数一致
4. **功能正常**: 确保测试用例仍能正常运行

### 验证命令

```bash
# 重新扫描，确认R016问题已修复
/check-test-code-quality /path/to/project --rules R016 --level warning

# 检查@tc.name与it()一致性
grep -B5 "it(" file.test.ets | grep "@tc.name"
```

## 注意事项

1. **仅修改it()和@tc.name**: 不修改`@tc.number`、`@tc.desc`等其他字段
2. **保留原始编号**: `@tc.number`字段保持不变
3. **跨文件去重**: `used_names`集合跨文件共享，确保全局唯一
4. **空名称处理**: 如果移除所有特殊字符后名称为空，使用`unnamedTest`作为基础名称
5. **备份文件**: 修复前建议备份原文件或提交代码到版本控制系统

## 相关文档

- [README.md](README.md) - 快速导航
- [../../SKILL.md](../../SKILL.md) - 完整技能说明
- [../FIX_GUIDE.md](../FIX_GUIDE.md) - 通用修复指南
