# hb-build 工作流程详解

详细的工作流程说明、核心算法和技术实现细节。

## 目录

- [完整工作流程](#完整工作流程)
- [核心算法](#核心算法)
- [文件路径映射](#文件路径映射)
- [错误处理](#错误处理)
- [环境变量](#环境变量)

---

## 完整工作流程

### 1. 定位项目根目录

脚本首先查找包含 `build.py` 的目录（用于运行 `hb build`）：

```python
def get_project_root() -> Path:
    """获取项目根目录（包含 build.py 的目录）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / 'build.py').exists():
            return current
        current = current.parent
    return Path.cwd()
```

### 2. 检测修改的文件

使用 `git status --short` 获取修改的文件列表：

```python
def get_modified_files() -> List[str]:
    result = subprocess.run(
        ['git', 'status', '--short'],
        capture_output=True,
        text=True,
        cwd=git_root
    )
```

**自动过滤的文件**：
- `.claude/`, `.hvigor/`, `build/`, `out/`, `.git/`
- `services/dialog_ui/ams_system_dialog/.hvigor/`
- `local.properties`
- `*.md` 文档文件

### 3. 推断编译目标

根据修改的文件路径统计每个服务的命中次数：

```python
def detect_build_targets(modified_files: List[str]) -> List[Tuple[str, str]]:
    target_scores = {}

    for file_path in modified_files:
        for path_pattern, target_info in FILE_TARGET_MAP.items():
            if file_path.startswith(path_pattern):
                target_name = target_info[0]
                target_scores[target_name] = target_scores.get(target_name, 0) + 1

    # 返回所有命中过的目标，按命中次数排序
    sorted_targets = sorted(target_scores.items(), key=lambda x: x[1], reverse=True)
```

**多目标编译**：检测到多个服务有修改时，会一起编译所有目标（不是只选择修改最多的）。

**整仓编译判断**：当编译目标数量 > 5 时，自动使用整仓编译。

### 4. 构建编译命令

```python
def get_build_command(targets: List[str], build_type: str, fast_rebuild: bool) -> List[str]:
    cmd = ['hb', 'build', 'ability_runtime', build_type]

    for target in targets:
        if target != 'full':
            cmd.extend(['--build-target', target])

    if fast_rebuild:
        cmd.append('--fast-rebuild')

    return cmd
```

### 5. 执行编译并处理结果

```python
def run_build(command: List[str], retry_count: int = 0, max_retries: int = 3, auto_retry: bool = True) -> bool:
    result = subprocess.run(
        command,
        cwd=project_root,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True

    # 编译失败，分析错误并决定是否重试
    if retry_count < max_retries - 1:
        should_retry, reason = should_auto_retry(result.stdout, result.stderr)
        # ... 重试逻辑
```

---

## 核心算法

### 文件到编译目标的映射

**FILE_TARGET_MAP**：定义文件路径前缀到编译目标的映射

```python
FILE_TARGET_MAP = {
    'services/abilitymgr': ('abilityms', '...'),
    'services/appmgr': ('appms', '...'),
    'services/uripermmgr': ('libupms', '...'),
    # ...
}
```

**TARGET_NAME_TO_PATH**：目标名称到完整路径的反向索引

```python
TARGET_NAME_TO_PATH = {
    'abilityms': '//foundation/.../abilitymgr:abilityms',
    'appms': '//foundation/.../appmgr:appms',
    # ...
}
```

### 智能决策算法

```
输入: 修改文件列表
输出: 编译目标列表

1. 统计每个服务的修改文件数
2. 如果没有匹配的目标 → 返回 [('full', None)]
3. 如果目标数量 > 5 → 返回 [('full', None)]
4. 如果目标数量 > 1 → 返回所有目标（按命中次数排序）
5. 如果目标数量 = 1 → 返回单个目标
```

---

## 文件路径映射

### 映射规则

**格式**: `'路径前缀': ('目标名称', '完整构建路径')`

### 添加新服务

要支持新的编译目标：

1. 在 `FILE_TARGET_MAP` 中添加映射：
   ```python
   'services/newservice': ('newservicename', '//foundation/.../newservice:newservicename'),
   ```

2. 在 `TARGET_NAME_TO_PATH` 中添加反向索引：
   ```python
   'newservicename': '//foundation/.../newservice:newservicename',
   ```

3. 运行测试验证

---

## 错误处理

### 自动重试判断

**should_auto_retry()** 函数分析编译错误，判断是否应该自动重试：

#### 不应该自动重试的错误（需手动修复）

```python
fatal_errors = [
    r'syntax error',           # 语法错误
    r'undefined reference',    # 未定义引用
    r'error: .* was not declared',
    r'error: no matching function',
    r'error: cannot convert',  # 类型错误
    r'error: invalid conversion',
    r'error: .*: No such file or directory',  # 头文件缺失
]
```

#### 应该自动重试的错误

```python
retryable_errors = [
    r'ninja: error: rebuilding',     # 构建系统问题
    r'error: build stopped',
    r'collect2: error: ld returned', # 链接时问题
    r'error: could not create',      # 临时文件问题
    r'error: multiple rules generate', # 并发问题
    r'missing dependency',            # 依赖问题
]
```

### 重试流程

```
编译失败
  ↓
分析错误类型
  ↓
┌─────────────────────────────┐
│ 可自动重试？                │
├─────────┬───────────────────┤
│ 是      │ 否                │
│ ↓       │ ↓                 │
│ 自动重试 │ 询问用户          │
│         │ ↓                 │
│         │ 1. 按 Enter 重试  │
│         │ 2. 输入 'r' 自动  │
│         │ 3. 输入 'q' 退出  │
└─────────┴───────────────────┘
```

---

## 环境变量

脚本不依赖特定的环境变量，但以下环境会影响编译：

- `PATH`: 必须包含 `hb` 命令
- `CCACHE_DIR`: ccache 缓存目录（如果使用 ccache）
- `OUT_DIR`: 编译输出目录（OpenHarmony 构建系统使用）

---

## 扩展和定制

### 修改忽略规则

编辑 `get_modified_files()` 函数中的 `ignore_patterns` 列表：

```python
ignore_patterns = [
    '.claude/',
    '.hvigor/',
    'build/',
    # 添加更多忽略规则
]
```

### 调整智能决策阈值

修改主函数中的目标数量阈值：

```python
# 当前: 超过 5 个目标时使用整仓编译
if len(detected_targets) > 5:
    targets = ['full']

# 可以调整为其他阈值
if len(detected_targets) > 3:
    targets = ['full']
```

---

## 故障排除

### 问题: "未检测到修改的文件"

**原因**: Git 仓库中没有修改，或所有修改都被过滤了

**解决**:
- 检查 `git status` 确认有修改
- 检查修改的文件是否在忽略列表中
- 使用 `--target` 明确指定编译目标

### 问题: "无法确定编译目标"

**原因**: 修改的文件不在任何映射的路径中

**解决**:
- 检查 `FILE_TARGET_MAP` 是否包含相应的路径
- 添加新的映射规则
- 使用 `--target` 明确指定编译目标

### 问题: "hb 命令未找到"

**原因**: `hb` 不在 PATH 中

**解决**:
- 安装 OpenHarmony 构建工具
- 将 `hb` 添加到 PATH
- 或使用完整路径调用 `hb`

### 问题: 编译成功但产物找不到

**原因**: 编译输出目录配置问题

**解决**:
- 检查 `out/` 目录
- 确认 `--build-target` 参数正确
- 查看 `hb build` 的输出信息
