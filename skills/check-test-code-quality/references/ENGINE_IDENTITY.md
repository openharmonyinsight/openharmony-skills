# 独立XTS工程识别规范

## 定义

独立XTS工程是指包含BUILD.gn文件且不包含子BUILD.gn的目录。

## 识别逻辑

1. 找到所有包含BUILD.gn的目录
2. 过滤包含子BUILD.gn的父目录（仅非group类型的父BUILD.gn）
3. 检查是否包含源代码文件（.ets, .ts, .js）
4. **重要**: group类型的BUILD.gn不作为独立工程
5. **重要**: group类型的父BUILD.gn不阻止其子目录成为独立工程（见陷阱10）

## 关键实现

完整实现代码见 [project_level_scan.md](project_level_scan.md) 中的 `find_independent_projects()` 函数。

### 判断group类型BUILD.gn

```python
def is_group_build_gn(build_gn_path):
    try:
        with open(build_gn_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return bool(re.search(r'\bgroup\s*\(', content))
    except Exception:
        return False
```

## 已知限制

1. 只判断目录是否有BUILD.gn文件，可能存在边界情况
2. 子系统-组件映射表需定期更新（R010）
3. 深层嵌套的跨文件函数调用可能无法完全检测（R004）
