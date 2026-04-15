# R011: testsuite重复修复指南

## 问题描述

一个独立XTS工程下不允许describe命名重复。

## 修复规则

### 自动修复命名格式

在重复的testsuite名称后追加驼峰式`Adapt`+三位数字编号。

**格式**: `{原testsuite名称}Adapt{三位数字}`

### 数字递增规则

- 从001开始
- 如果`XxxAdapt001`已存在，则使用`XxxAdapt002`
- 依此类推

### 保留首个原则

保留第一个出现的testsuite名称不变，只修改后续重复的。

## 修复示例

### 示例1: 基本修复

**修复前**:
```javascript
// File1.test.js
describe("TransientTaskJsTest", function () {
  // 测试代码
});

// File2.test.js (重复)
describe("TransientTaskJsTest", function () {  // ✗ 错误：与File1.test.js重复
  // 测试代码
});
```

**修复后**:
```javascript
// File1.test.js (保持不变)
describe("TransientTaskJsTest", function () {
  // 测试代码
});

// File2.test.js (已修复)
describe("TransientTaskJsTestAdapt001", function () {  // ✓ 正确：名称唯一
  // 测试代码
});
```

### 示例2: 多个重复的情况

**修复前**:
```javascript
// File1.test.js
describe("ContinuousTaskJsTest", function () {
  // 测试代码
});

// File2.test.js (重复)
describe("ContinuousTaskJsTest", function () {  // ✗ 错误：重复
  // 测试代码
});

// File3.test.js (重复)
describe("ContinuousTaskJsTest", function () {  // ✗ 错误：重复
  // 测试代码
});
```

**修复后**:
```javascript
// File1.test.js (保持不变 - 首个)
describe("ContinuousTaskJsTest", function () {
  // 测试代码
});

// File2.test.js (已修复)
describe("ContinuousTaskJsTestAdapt001", function () {  // ✓ 正确
  // 测试代码
});

// File3.test.js (已修复)
describe("ContinuousTaskJsTestAdapt002", function () {  // ✓ 正确
  // 测试代码
});
```

## 自动修复实现

### Python修复脚本

```python
import re
import os
from typing import Dict, List, Tuple, Optional

def fix_r011_testsuite_duplicate(
    file_path: str, 
    content: str, 
    existing_names: Dict[str, str]
) -> Tuple[str, Optional[str]]:
    """
    修复单个文件的R011 testsuite重复问题
    
    Args:
        file_path: 文件路径
        content: 文件内容
        existing_names: 已存在的testsuite名称 {name: file_path}
    
    Returns:
        (修复后的内容, 新的testsuite名称)，如果没有修改则返回 (原内容, None)
    """
    pattern = r'(describe\s*\(\s*["\'])([^"\']+)(["\'])'
    
    def replace_func(match):
        prefix = match.group(1)  # describe(" 或 describe('
        original_name = match.group(2)  # testsuite名称
        suffix = match.group(3)  # " 或 '
        
        if original_name not in existing_names:
            # 首次出现，记录但不修改
            existing_names[original_name] = file_path
            return match.group(0)
        
        # 已存在重复，需要重命名
        counter = 1
        while True:
            new_name = f"{original_name}Adapt{counter:03d}"
            if new_name not in existing_names:
                existing_names[new_name] = file_path
                return f"{prefix}{new_name}{suffix}"
            counter += 1
    
    new_content = re.sub(pattern, replace_func, content)
    
    if new_content != content:
        # 提取新的testsuite名称
        new_match = re.search(pattern, new_content)
        if new_match:
            return new_content, new_match.group(2)
    
    return content, None

def fix_r011_in_project(project_dir: str, test_files: List[str]) -> Dict[str, str]:
    """
    修复整个项目的R011问题
    
    Args:
        project_dir: 项目目录
        test_files: 测试文件列表（相对路径）
    
    Returns:
        修复结果 {文件路径: 新testsuite名称}
    """
    existing_names: Dict[str, str] = {}
    fix_results: Dict[str, str] = {}
    
    for file_path in test_files:
        full_path = os.path.join(project_dir, file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, new_name = fix_r011_testsuite_duplicate(
            file_path, content, existing_names
        )
        
        if new_content != content and new_name:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fix_results[file_path] = new_name
            print(f"已修复: {file_path} -> {new_name}")
    
    return fix_results

# 使用示例
if __name__ == "__main__":
    project_dir = "/path/to/project"
    test_files = [
        "test/File1.test.js",
        "test/File2.test.js",
        "test/File3.test.js",
    ]
    
    results = fix_r011_in_project(project_dir, test_files)
    print(f"\n共修复 {len(results)} 个文件")
```

## 修复验证

修复完成后，需要验证：

1. **名称唯一性**: 确保同一独立工程内所有describe名称唯一
2. **命名规范**: 确保新名称符合`{原名}Adapt{三位数字}`格式
3. **功能正常**: 确保测试用例仍能正常运行

### 验证命令

```bash
# 重新扫描，确认R011问题已修复
/check-test-code-quality /path/to/project --rules R011
```

## 注意事项

1. **保留首个**: 第一个出现的testsuite名称保持不变
2. **跨工程不检测**: 不同独立工程之间的同名testsuite不视为重复
3. **动态字符串**: 包含变量拼接的testsuite名称不进行重复检查
4. **备份文件**: 修复前建议备份原文件

## 相关文档

- [README.md](README.md) - 快速导航
- [../../SKILL.md](../../SKILL.md) - 完整技能说明
- [../../rules/R011/SKILL.md](../../rules/R011/SKILL.md) - R011规则示例和实现
- [../FIX_GUIDE.md](../FIX_GUIDE.md) - 通用修复指南
