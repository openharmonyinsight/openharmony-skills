# hb-build 参考文档

详细的 API 参考、配置说明和技术实现细节。

## 目录

- [命令行参数](#命令行参数)
- [配置文件](#配置文件)
- [核心算法](#核心算法)
- [文件路径映射](#文件路径映射)
- [错误处理](#错误处理)
- [环境变量](#环境变量)
- [故障排除](#故障排除)

---

## 命令行参数

### 完整参数列表

```bash
python3 scripts/helper.py [OPTIONS]
```

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--target` | string | 否 | `auto` | 编译目标 |
| `--type` | string | 否 | `-i` | 编译类型（`-i` 功能代码 / `-t` 测试套） |
| `--fast` | flag | 否 | `false` | 启用快速编译（添加 `--fast-rebuild`） |
| `--max-retries` | integer | 否 | `3` | 编译失败后的最大重试次数 |
| `--auto-retry` | flag | 否 | `false` | 启用自动重试模式 |
| `--help` | flag | 否 | - | 显示帮助信息 |

### --target 参数详解

#### auto (默认)
自动根据修改的文件推断编译目标。推断规则：
- 统计每个服务目录下修改的文件数量
- 选择修改文件最多的服务作为编译目标
- 如果无法确定，默认编译全仓

```bash
hb-build --target auto
# 等同于
hb-build
```

#### full
编译整个 ability_runtime 组件（包括所有服务和模块）。

```bash
hb-build --target full
```

**注意**: 全仓编译耗时较长（可能超过 10 分钟）。

#### 单个服务目标
编译指定的服务 SO 文件。

```bash
# UriPermissionManager
hb-build --target libupms

# AbilityManagerService
hb-build --target abilityms

# AppManagerService
hb-build --target appms
```

---

## 配置文件

### FILE_TARGET_MAP

文件路径到编译目标的映射，定义在 `scripts/helper.py` 中：

```python
FILE_TARGET_MAP = {
    'services/abilitymgr': ('abilityms', '//foundation/ability/ability_runtime/services/abilitymgr:abilityms'),
    'services/appmgr': ('appms', '//foundation/ability/ability_runtime/services/appmgr:appms'),
    'services/uripermmgr': ('libupms', '//foundation/ability/ability_runtime/services/uripermmgr:libupms'),
    'services/dataobsmgr': ('dataobsms', '//foundation/ability/ability_runtime/services/dataobsmgr:dataobsms'),
    'services/quickfixmgr': ('quickfixmgr', '//foundation/ability/ability_runtime/services/quickfixmgr:quickfixmgr'),
}
```

**格式**: `'路径前缀': ('目标名称', '完整构建路径')`

**添加新服务**:
1. 在 `FILE_TARGET_MAP` 中添加映射
2. 在 `TARGET_NAME_TO_PATH` 中添加反向索引
3. 运行测试验证

### TARGET_NAME_TO_PATH

目标名称到完整路径的反向索引：

```python
TARGET_NAME_TO_PATH = {
    'abilityms': '//foundation/ability/ability_runtime/services/abilitymgr:abilityms',
    'appms': '//foundation/ability/ability_runtime/services/appmgr:appms',
    'libupms': '//foundation/ability/ability_runtime/services/uripermmgr:libupms',
    'dataobsms': '//foundation/ability/ability_runtime/services/dataobsmgr:dataobsms',
    'quickfixmgr': '//foundation/ability/ability_runtime/services/quickfixmgr:quickfixmgr',
}
```

---

## 核心算法

### 文件检测算法

```python
def get_modified_files() -> List[str]:
    """获取修改的文件列表"""

    # 1. 运行 git status --short
    result = subprocess.run(['git', 'status', '--short'], ...)

    # 2. 解析输出
    for line in result.stdout:
        parts = line.strip().split()
        if len(parts) >= 2:
            file_path = parts[1]

            # 3. 过滤不需要编译的文件
            if any(pattern in file_path for pattern in IGNORE_PATTERNS):
                continue

            # 4. 计算相对路径
            rel_path = Path(file_path).relative_to(art_root)
            modified.append(rel_path)

    return modified
```

**忽略的文件模式**:
- `.claude/` - Skill 配置目录
- `.hvigor/` - 构建工具目录
- `build/` - 构建产物
- `local.properties` - 本地配置
- `out/` - 输出目录
- `.git/` - Git 目录

### 目标推断算法

```python
def detect_build_targets(modified_files: List[str]) -> List[Tuple[str, str]]:
    """根据修改的文件推断编译目标（支持多个目标）"""

    # 1. 统计每个目标的命中次数
    target_scores = {}
    for file_path in modified_files:
        for path_pattern, target_info in FILE_TARGET_MAP.items():
            if file_path.startswith(path_pattern):
                target_name = target_info[0]
                target_scores[target_name] = target_scores.get(target_name, 0) + 1

    # 2. 返回所有命中过的目标，按命中次数排序
    if not target_scores:
        return [('full', None)]  # 无法确定，编译全仓

    sorted_targets = sorted(target_scores.items(), key=lambda x: x[1], reverse=True)

    # 3. 构建返回列表
    targets = []
    for target_name, score in sorted_targets:
        target_full_path = TARGET_NAME_TO_PATH.get(target_name)
        targets.append((target_name, target_full_path))

    return targets
```

**示例 1: 单个服务修改**:
```
修改文件:
  - services/uripermmgr/src/libupms/batch_uri.cpp
  - services/uripermmgr/src/libupms/uri_permission_manager_service.cpp

推断结果: [('libupms', '//.../libupms')]
```

**示例 2: 多个服务修改**:
```
修改文件:
  - services/uripermmgr/src/libupms/batch_uri.cpp
  - services/abilitymgr/src/ability_manager/ability_manager_client.cpp
  - services/appmgr/src/app_manager/app_manager_service.cpp

推断结果: [
  ('libupms', '//.../libupms'),
  ('abilityms', '//.../abilityms'),
  ('appms', '//.../appms')
]
```

**示例 3: 目标数量 > 5，使用整仓编译**:
```
修改文件涉及 6 个或更多服务
推断结果: [('full', None)]  # 自动使用整仓编译
```

### 编译命令构建

```python
def get_build_command(target: str, target_full_path: str, build_type: str, fast_rebuild: bool) -> List[str]:
    """构建编译命令"""

    cmd = ['hb', 'build', 'ability_runtime', build_type]

    if target != 'full':
        if target_full_path:
            cmd.extend(['--build-target', target_full_path])
        else:
            cmd.extend(['--build-target', target])

    if fast_rebuild:
        cmd.append('--fast-rebuild')

    return cmd
```

**生成命令示例**:
```bash
# 单个目标
hb build ability_runtime -i --build-target //foundation/ability/ability_runtime/services/uripermmgr:libupms

# 全仓编译
hb build ability_runtime -i

# 快速编译
hb build ability_runtime -i --build-target //foundation/ability/ability_runtime/services/uripermmgr:libupms --fast-rebuild
```

---

## 文件路径映射

### 项目目录结构

```
<project_root>/                               # 项目根目录（包含 build.py）
├── build.py                                  # 构建入口
├── out/                                      # 编译产物
└── foundation/ability/ability_runtime/       # ability_runtime 组件（当前工作目录）
    ├── interfaces/                           # 接口定义
    ├── services/                             # 服务实现
    │   ├── abilitymgr/                       # AbilityManagerService
    │   ├── appmgr/                           # AppManagerService
    │   ├── uripermmgr/                       # UriPermissionManager
    │   ├── dataobsmgr/                       # DataObserverManager
    │   └── quickfixmgr/                      # QuickFix Manager
    └── .git/                                 # Git 仓库根目录
```

**说明**：
- `<project_root>` - 包含 `build.py` 的目录，通常为代码仓库的根目录
- 当前工作目录通常位于 `foundation/ability/ability_runtime/`

### 路径检测函数

```python
def get_project_root() -> Path:
    """获取项目根目录（包含 build.py 的目录）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / 'build.py').exists():
            return current
        current = current.parent
    return Path.cwd()

def get_git_root() -> Path:
    """获取 Git 仓库根目录（包含 .git 的目录）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / '.git').exists():
            return current
        current = current.parent
    return Path.cwd()

def get_ability_runtime_root() -> Path:
    """获取 ability_runtime 组件根目录"""
    project_root = get_project_root()
    art_path = project_root / 'foundation' / 'ability' / 'ability_runtime'
    if art_path.exists():
        return art_path
    # 向上查找
    current = Path.cwd()
    while current != current.parent:
        if (current / 'services' / 'abilitymgr').exists():
            return current
        current = current.parent
    return Path.cwd()
```

---

## 错误处理

### 编译错误解析

```python
def parse_compiler_errors(output: str) -> List[str]:
    """解析编译器错误信息"""

    errors = []
    error_pattern = r'^([^:]+):(\d+):(\d+):\s*error:\s*(.+)$'

    for line in output.split('\n'):
        match = re.match(error_pattern, line.strip())
        if match:
            file_path = match.group(1)
            line_num = match.group(2)
            error_msg = match.group(4)
            errors.append(f"{file_path}:{line_num} - {error_msg}")

    return errors
```

**匹配示例**:
```
<project_root>/foundation/ability/ability_runtime/services/uripermmgr/src/libupms/batch_uri.cpp:123:45: error: undefined reference to 'some_function'

解析结果:
  文件: <project_root>/foundation/ability/ability_runtime/services/uripermmgr/src/libupms/batch_uri.cpp
  行号: 123
  列号: 45
  错误: undefined reference to 'some_function'
```

### 重试机制

```python
def should_auto_retry(output: str, stderr: str) -> Tuple[bool, str]:
    """
    分析编译错误，判断是否应该自动重试
    返回: (是否应该重试, 原因)
    """
    combined_output = output + stderr

    # 不应该自动重试的错误类型
    fatal_errors = [
        r'syntax error',
        r'undefined reference',
        r'error: .* was not declared',
        r'error: no matching function',
        r'error: cannot convert',
        r'error: invalid conversion',
        r'error: .*: No such file or directory',
        r'fatal error: .*: No such file',
    ]

    # 应该自动重试的错误类型
    retryable_errors = [
        r'ninja: error: rebuilding',
        r'error: build stopped',
        r'collect2: error: ld returned',
        r'error: could not create',
        r'error: unable to open',
        r'error: multiple rules generate',
        r'missing dependency',
    ]

    for pattern in fatal_errors:
        if re.search(pattern, combined_output, re.IGNORECASE):
            return False, f"发现需要手动修复的错误: {pattern}"

    for pattern in retryable_errors:
        if re.search(pattern, combined_output, re.IGNORECASE):
            return True, f"发现可重试的错误: {pattern}"

    return False, "未知错误类型"

def run_build(command: List[str], retry_count: int = 0,
              max_retries: int = 3, auto_retry: bool = True) -> bool:
    """执行编译命令，支持自动重试"""

    result = subprocess.run(command, ...)

    if result.returncode == 0:
        return True

    # 编译失败，分析错误
    should_retry, reason = should_auto_retry(result.stdout, result.stderr)

    if auto_retry and should_retry:
        # 自动重试
        print_warning(f"✓ {reason}")
        print_warning(f"⚠ 自动重试中... ({max_retries - retry_count - 1} 次剩余)")
        time.sleep(2)
        return run_build(command, retry_count + 1, max_retries, auto_retry)
    else:
        # 需要手动确认
        print_warning(f"\n原因: {reason}")
        print_info("您可以：")
        print_info("  1. 手动修复代码后，按 Enter 继续重试")
        print_info("  2. 输入 'r' 开启自动重试模式")
        print_info("  3. 输入 'q' 或 'quit' 退出")

        user_input = input("\n您的选择 [Enter/r/q]: ").strip().lower()

        if user_input == 'r':
            return run_build(command, retry_count + 1, max_retries, auto_retry=True)
        elif user_input not in ['q', 'quit']:
            return run_build(command, retry_count + 1, max_retries, auto_retry)

        return False
```

**自动重试的错误类型**:
- 构建系统临时问题（如 ninja 重建）
- 链接时偶尔出现的错误
- 临时文件访问问题
- 并发构建问题

**需手动修复的错误类型**:
- 语法错误
- 未定义引用
- 类型转换错误
- 头文件缺失

---

## 环境变量

脚本不依赖特定的环境变量，但以下环境变量可能影响编译过程：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `PATH` | 可执行文件搜索路径 | 系统默认 |
| `HOME` | 用户主目录 | 系统默认 |
| `PWD` | 当前工作目录 | 系统检测 |

---

## 故障排除

### 问题 1: 检测不到修改的文件

**症状**:
```
[WARNING] 未检测到修改的文件，默认编译 ability_runtime
[INFO] 编译目标: full (全仓编译)
```

**原因**:
- 不在 Git 仓库中
- 文件未修改或未暂存
- 路径过滤规则错误

**解决方案**:
```bash
# 1. 检查 Git 状态
git status --short

# 2. 确认在正确的目录
pwd  # 应该显示 .../foundation/ability/ability_runtime

# 3. 检查文件是否被忽略
git status --ignored
```

### 问题 2: 编译目标未找到

**症状**:
```
Exception: Error: The build target xxx was not found in the build configuration of bundle.json.
If you really want to specify this target for building, please use the full path.
```

**原因**:
- 使用了简短目标名而非完整路径
- bundle.json 中未定义该目标

**解决方案**:
```bash
# 使用完整路径
hb-build --target //foundation/ability/ability_runtime/services/uripermmgr:libupms

# 或检查 bundle.json 中的可用目标
grep -A 50 '"sub_component"' bundle.json
```

### 问题 3: hb 命令未找到

**症状**:
```
/bin/bash: hb: command not found
```

**原因**:
- OpenHarmony 构建工具未安装
- PATH 环境变量未配置

**解决方案**:
```bash
# 1. 检查 hb 是否安装
which hb

# 2. 添加到 PATH
export PATH=$PATH:/path/to/hb

# 3. 或使用完整路径
/path/to/hb build ability_runtime
```

### 问题 4: 编译超时或卡住

**症状**:
编译进程长时间无输出

**原因**:
- 网络问题（下载依赖）
- 资源不足（内存/CPU）
- 编译缓存损坏

**解决方案**:
```bash
# 1. 检查进程状态
ps aux | grep -E "hb|hpm|ninja"

# 2. 清理缓存
rm -rf out/standard/.ninja_log
rm -rf out/standard/build.ninja

# 3. 重新编译
hb-build --clean-build
```

### 问题 5: 权限错误

**症状**:
```
Permission denied: <project_root>/out/standard/...
```

**原因**:
- 输出目录权限不足
- 磁盘空间不足

**解决方案**:
```bash
# 1. 检查权限
ls -ld out/standard

# 2. 修改权限
chmod -R u+w out/standard

# 3. 检查磁盘空间
df -h out
```

---

## 附录

### A. 完整的编译命令示例

```bash
# 1. 自动检测并编译
python3 scripts/helper.py --target auto

# 2. 编译特定服务（快速模式）
python3 scripts/helper.py --target libupms --fast

# 3. 编译测试套
python3 scripts/helper.py --target full --type -t

# 4. 自定义重试次数
python3 scripts/helper.py --target abilityms --max-retries 5
```

### B. 输出文件位置

```
编译产物:
  <project_root>/out/standard/ability/ability_runtime/
  ├── libupms.z.so
  ├── libabilityms.z.so
  ├── libappms.z.so
  └── ...

日志文件:
  <project_root>/out/standard/build.log
  <project_root>/out/standard/.ninja_log
```

**说明**：`<project_root>` 为包含 `build.py` 的目录（通常为代码仓库根目录）。从 ability_runtime 目录执行时，可以使用相对路径 `../out/standard/`

### C. 相关链接

- [OpenHarmony 独立编译指南](https://gitee.com/csliutt-private/component_indep_build/blob/master/cases/case19.md)
- [hb 构建工具文档](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/quick-start/building-the-first-app.md)
- [Claude Code Skills 指南](https://code.claude.com/docs/zh-CN/skills)
