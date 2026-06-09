# 环境检查模块
## 功能

检查执行环境是否完整，包括依赖、工具版本、权限和磁盘空间，并记录所有依赖的安装情况，传递给后续模块。

## 职责

- **只负责检查**: 检查所有依赖和工具的安装情况
- **不负责安装**: 不尝试安装任何依赖
- **记录状态**: 将所有依赖的安装情况记录并传递给03
- **选择性中断**: 只有HDC等致命错误才中断，其他错误只记录不中断
## 执行流程

```
开始
  ↓
[1] 操作系统环境检查
  └── 1.1 检查操作系统类型（仅支持 Linux）
       └── 如果不是 Linux → 调用 06-error-handler.md 返回 OS_NOT_SUPPORTED 错误（中断）
  ↓
[2] Python 环境检查
  └── 2.1 检查 Python 版本是否 >= 3.8
       ├── 如果未安装 → 调用 06-error-handler.md 返回 PYTHON_NOT_INSTALLED 错误（中断）
       ├── 如果版本 < 3.8 → 调用 06-error-handler.md 返回 PYTHON_VERSION_LOW 错误（中断）
       └── 如果版本满足 → 记录版本信息（不中断）
  ↓
[3] 工具依赖检查（只检查，不安装）
  ├── 3.1 检查 pip → 记录安装状态（不中断）
  ├── 3.2 检查 git → 记录安装状态（如果是增量任务,则中断）
  ├── 3.3 检查 lcov → 记录安装状态（不中断，03负责安装）
  ├── 3.4 检查 addlcov → 记录安装状态（不中断，03从本地提供）
  ├── 3.5 检查 dos2unix → 记录安装状态（不中断，03负责安装）
  └── 3.6 检查 hdc → 检查安装情况（未安装则中断）
  ↓
[4] Python 包依赖检查（只检查，不安装）
  └── 4.1-4.15 检查所有Python包 → 记录安装状态（不中断，03负责安装）
  ↓
[5] 项目根目录验证
  ├── 5.1 检查 {CODE_ROOT}/build_system.sh 是否存在
  └── 5.2 如果未找到 → 调用 06-error-handler.md 返回 PROJECT_ROOT_NOT_FOUND 错误（中断）
  ↓
[6] 权限检查
  ├── 6.1-6.4 检查各目录权限 → 记录权限状态（不中断，记录警告）
  ↓
[7] 磁盘空间检查
  └── 7.1 检查可用空间（全量≥50GB，增量≥20GB）→ 记录空间状态（不中断，记录警告）
  ↓
[8] 返回环境状态（包括所有依赖的安装情况）
  ↓
结束
```

## 输入
从 `01-config-checker.md` 获取：
- `skill_dir`: SKILL_DIR （skill 所在目录）
- `code_root`: CODE_ROOT （代码根目录）
- `output_path`: output_path （报告输出目录）
- `taskType`: 任务类型 ("full_coverage" 或 "incremental_coverage")
- `config.deviceInfo`: 设备配置信息（完整，来自01的验证结果）
  - `ip`: hdc 连接 IP
  - `port`: hdc 连接端口
  - `sn`: 设备序列号
  - `connected`: 设备连接状态
  - `validated`: 验证状态

## 检查项详细说明

### [1] 操作系统环境检查

#### 1.1 检查操作系统类型
- **命令**: `uname -s`
- **预期结果**: `Linux`
- **如果返回值不是 `Linux`**:
  - 调用 06-error-handler.md 返回 `OS_NOT_SUPPORTED` 错误
  - 当前 skill 只支持 Linux 环境
- **错误代码**: `OS_NOT_SUPPORTED`

### [2] Python 环境检查

#### 2.1 检查 Python 版本
- **命令**: `python --version` 或 `python3 --version`
- **最低版本**: 3.8.0
- **检查步骤**:
  1. 执行 `python --version`，如果失败则执行 `python3 --version`
  2. 如果命令执行失败（未安装）:
     - 调用 06-error-handler.md 返回 `PYTHON_NOT_INSTALLED` 错误（中断）
  3. 解析返回的版本号，提取主版本号和次版本号
  4. 比较版本号是否 >= 3.8.0
  5. 如果版本不满足:
     - 调用 06-error-handler.md 返回 `PYTHON_VERSION_LOW` 错误（中断）
  6. 如果版本满足:
     - 记录版本信息到返回的状态中
- **记录内容**（仅在Python已安装且版本满足时记录）:
  ```json
  "python": {
    "installed": true,
    "version": "3.8.x",
    "satisfied": true
  }
  ```
- **错误处理**: 
  - Python未安装 → 立即中断，返回 `PYTHON_NOT_INSTALLED`
  - Python版本过低 → 立即中断，返回 `PYTHON_VERSION_LOW`

### [3] 工具依赖检查

所有工具只检查安装情况，记录状态，不尝试安装，不中断流程。

#### 3.1 检查 pip 是否安装
- **命令**: `pip --version` 或 `pip3 --version`
- **说明**: 依赖下载工具
- **检查步骤**:
  1. 执行检查命令
  2. 解析版本信息（如果安装）
  3. 记录安装状态和版本
- **记录内容**:
  ```json
  "pip": {
    "installed": true/false,
    "version": "x.x.x",
    "path": "/path/to/pip"
  }
  ```
- **03处理**: 不安装，如果后续使用出错则中断报错

#### 3.2 检查 git 是否安装
- **命令**: `git --version`
- **说明**: git工具
- **检查步骤**:
  1. 执行检查命令
  2. 解析版本信息（如果安装）
  3. 记录安装状态和版本
  4. **根据任务类型决定是否中断**:
     - 如果 `taskType === "incremental_coverage"` 且 `git` 未安装:
       - 调用 06-error-handler.md 返回 `GIT_NOT_INSTALLED` 错误（中断）
       - 提示用户安装 git 以支持增量覆盖率功能
     - 如果 `taskType === "full_coverage"` 或 `git` 已安装:
       - 记录状态，不中断流程
- **记录内容**:
  ```json
  "git": {
    "installed": true/false,
    "version": "x.x.x"
  }
  ```
- **03处理**: 不安装，直接跳过
- **错误处理**: 
  - 增量任务且git未安装 → 立即中断
  - 全量任务或git已安装 → 记录状态继续

#### 3.3 检查 lcov 是否安装
- **命令**: `lcov --version`
- **说明**: 覆盖率工具
- **检查步骤**:
  1. 执行检查命令
  2. 解析版本信息（如果安装）
  3. 记录安装状态和版本
- **记录内容**:
  ```json
  "lcov": {
    "installed": true/false,
    "version": "x.x.x",
    "path": "/path/to/lcov"
  }
  ```
- **03处理**: 如果未安装则安装，安装失败则中断报错

#### 3.4 检查 addlcov 是否安装
- **命令**: `addlcov --version`
- **说明**: 增量覆盖率工具（本地提供）
- **检查步骤**:
  1. 检查 `{SKILL_DIR}/scripts/addlcov` 是否存在
  2. 如果存在，检查是否可执行
  3. 如果不存在，检查系统是否已安装 addlcov
  4. 记录所有发现的情况
- **记录内容**:
  ```json
  "addlcov": {
    "installed": true/false,
    "local_available": true/false,
    "system_available": true/false,
    "local_path": "{SKILL_DIR}/scripts/addlcov",
    "version": "x.x.x"
  }
  ```
- **03处理**: 从本地 skill 脚本目录提供，不安装

#### 3.5 检查 dos2unix 是否安装
- **命令**: `dos2unix --version`
- **说明**: 文件格式转换工具
- **检查步骤**:
  1. 执行检查命令
  2. 解析版本信息（如果安装）
  3. 记录安装状态和版本
- **记录内容**:
  ```json
  "dos2unix": {
    "installed": true/false,
    "version": "x.x.x",
    "path": "/path/to/dos2unix"
  }
  ```
- **03处理**: 如果未安装则安装，安装失败则中断报错

#### 3.6 检查 hdc 是否安装
- **命令**: `hdc --version`
- **说明**: 设备连接工具
- **检查步骤**:
  1. 执行检查命令
  2. 解析版本信息（如果安装）
  3. 记录安装状态和版本
  4. 如果未安装，中断流程并调用错误处理
- **记录内容**:
  ```json
  "hdc": {
    "installed": true/false,
    "version": "x.x.x",
    "path": "/path/to/hdc"
  }
  ```
- **如果未安装**:
  - 立即中断流程
  - 调用 06-error-handler.md 返回 `HDC_NOT_INSTALLED` 错误
- **03处理**: hdc 必须在安装前检查，如果缺失立即中断

### [4] Python 包依赖检查

所有Python包只检查安装情况，记录状态，不尝试安装，不中断流程。

#### Python包检查列表

| 包名 | 检查命令 | 最低版本 | 03处理 |
|-----|---------|---------|--------|
| lxml | `pip show lxml` | - | 未安装则安装，失败中断 |
| selectolax | `pip show selectolax` | - | 未安装则安装，失败中断 |
| CppHeaderParser | `pip show CppHeaderParser` | - | 未安装则安装，失败中断 |
| requests | `pip show requests` | - | 未安装则安装，失败中断 |
| pyserial | `pip show pyserial` | 3.3 | 未安装则安装，失败中断 |
| paramiko | `pip show paramiko` | - | 未安装则安装，失败中断 |
| rsa | `pip show rsa` | - | 未安装则安装，失败中断 |
| lz4 | `pip show lz4` | - | 未安装则安装，失败中断 |
| json5 | `pip show json5` | - | 未安装则安装，失败中断 |
| beautifulsoup4 | `pip show beautifulsoup4` | - | 未安装则安装，失败中断 |
| PyYAML | `pip show PyYAML` | - | 未安装则安装，失败中断 |
| redis | `pip show redis` | - | 未安装则安装，失败中断 |
| pycryptodome | `pip show pycryptodome` | - | 未安装则安装，失败中断 |
| esdk-obs-python | `pip show esdk-obs-python` | - | 未安装则安装，失败中断 |
| chardet | `pip show chardet` | - | 未安装则安装，失败中断 |

**检查步骤**:
1. 使用 `pip show <package_name>` 检查每个包是否已安装
2. 如果需要检查版本，使用 `pip show <package_name> | grep Version` 解析版本号
3. 记录每个包的安装状态和版本信息
4. 不因为包未安装而中断流程

**记录内容**:
```json
"pythonPackages": {
  "lxml": {
    "installed": true/false,
    "version": "x.x.x"
  },
  "selectolax": {
    "installed": true/false,
    "version": "x.x.x"
  },
  // ... 其他包
}
```

### [5] 项目根目录验证

#### 5.1 从当前目录向上递归查找 build_system.sh
- **检查路径**: `{CODE_ROOT}/build_system.sh`
- **检查步骤**:
  1. 检查 {CODE_ROOT} 目录是否存在
  2. 检查 {CODE_ROOT}/build_system.sh 是否存在
- **如果未找到**:
  - 调用 06-error-handler.md 返回 `PROJECT_ROOT_NOT_FOUND` 错误
  - 提示用户确认 code_root 配置是否正确
- **错误代码**: `PROJECT_ROOT_NOT_FOUND`

### [6] 权限检查

#### 6.1 检查项目目录可读
- **检查路径**: `{CODE_ROOT}`
- **检查方法**: 使用 `os.access(path, os.R_OK)` 或 `ls -la {CODE_ROOT}`
- **如果不可读**:
  - 调用 06-error-handler.md 返回 `PERMISSION_DENIED` 错误
  - 提示用户检查目录权限
- **错误代码**: `PERMISSION_DENIED`

#### 6.2 检查 developer_test 目录可读
- **检查路径**: `{CODE_ROOT}/test/testfwk/developer_test`
- **检查方法**: 使用 `os.access(path, os.R_OK)` 或 `ls -la {CODE_ROOT}/test/testfwk/developer_test`
- **如果不可读**:
  - 调用 06-error-handler.md 返回 `PERMISSION_DENIED` 错误
  - 提示用户检查目录权限
- **错误代码**: `PERMISSION_DENIED`

#### 6.3 检查报告输出目录可写
- **检查路径**: `{output_path}`
- **检查方法**: 
  - 使用 `os.access(path, os.W_OK)`
  - 尝试创建测试文件 `{output_path}/.test_write`
  - 删除测试文件
- **如果不可写**:
  - 调用 06-error-handler.md 返回 `PERMISSION_DENIED` 错误
  - 提示用户检查目录权限或更换输出路径
- **错误代码**: `PERMISSION_DENIED`

#### 6.4 检查依赖安装权限 (sudo 权限)
- **检查方法**: 执行 `sudo -n true` 命令
- **如果失败**:
  - 记录警告信息，不中断流程
  - 提示用户可能需要手动安装某些系统依赖
  - 在依赖安装模块中尝试不使用 sudo 安装

### [7] 磁盘空间检查

#### 8.1 检查可用空间
- **检查路径**: `{CODE_ROOT}` 所在的文件系统
- **最低要求**: 至少 15GB 可用空间
- **检查步骤**:
  1. 执行 `df -k {CODE_ROOT}` 命令
  2. 解析输出，获取 Available 列的值
  3. 比较可用空间是否 >= 16GB (16384 MB = 16777216 KB)
- **如果空间不足**:
  - 调用 06-error-handler.md 返回 `INSUFFICIENT_DISK_SPACE` 错误
  - 提示用户清理磁盘空间或更换输出路径
- **错误代码**: `INSUFFICIENT_DISK_SPACE`

### [8] 返回环境状态

返回包含以下信息的对象:
```json
{
  "os": {
    "type": "Linux",
    "supported": true
  },
  "python": {
    "version": "3.8.x",
    "supported": true
  },
  "tools": {
    "pip": {
      "installed": true,
      "version": "x.x.x"
    },
    "git": {
      "installed": false,
      "version": null
    },
    "lcov": {
      "installed": true,
      "version": "x.x.x"
    },
    "addlcov": {
      "installed": false,
      "version": null,
      "path": "{SKILL_DIR}/scripts/addlcov"
    },
    "dos2unix": {
      "installed": true,
      "version": "x.x.x"
    },
    "hdc": {
      "installed": true,
      "version": "x.x.x"
    }
  },
  "pythonPackages": {
    "lxml": {
      "installed": true,
      "version": "x.x.x"
    },
    "selectolax": {
      "installed": false,
      "version": null
    },
    // ... 其他包的状态
  },
  "permissions": {
    "project_readable": true,
    "developer_test_readable": true,
    "output_writable": true,
    "sudo_available": false
  },
  "disk": {
    "available": "50GB",
    "sufficient": true
  },
  "overall": "ready"  // "ready", "warning", "error"
}
```

## 错误处理

### 立即中断的错误（02中直接中断）
以下情况需要立即中断流程，调用06-error-handler.md：
- `OS_NOT_SUPPORTED` - 操作系统不支持（非Linux）
- `PYTHON_NOT_INSTALLED` - Python未安装（必须在执行前检查）
- `PYTHON_VERSION_LOW` - Python版本过低（< 3.8.0）
- `HDC_NOT_INSTALLED` - hdc未安装（必须在安装前检查）
- `PROJECT_ROOT_NOT_FOUND` - 项目根目录未找到
- `GIT_NOT_INSTALLED` - git未安装（仅在增量任务时中断）

### 条件中断的错误（根据任务类型决定）
以下情况根据任务类型决定是否中断：
- `GIT_NOT_INSTALLED` - git未安装
  - **增量任务（taskType === "incremental_coverage"）**: 立即中断流程，调用06-error-handler.md
  - **全量任务（taskType === "full_coverage"）**: 只记录警告，不中断流程

### 记录状态不中断（传递给03处理）
以下情况只记录状态，不中断流程，将状态传递给03进行安装：
- 所有系统依赖（lcov、dos2unix等）的安装状态
- 所有Python包的安装状态
- 磁盘空间是否足够
- 各种权限状态

### 警告信息（03不处理）
以下情况记录警告，03不处理：
- `PIP_NOT_INSTALLED` - pip未安装（03不安装，使用时出错再报错）
- `GIT_NOT_INSTALLED` - git未安装（仅全量任务时为警告，增量任务时已中断）
- `ADDLCOV_NOT_FOUND` - addlcov未找到（03从本地提供）

**02的工作原则**:
1. **只检查不安装**: 检查所有依赖和工具的安装情况
2. **记录状态**: 将所有检查结果记录并传递给03
3. **选择性中断**: 致命错误（如OS不支持、Python问题、HDC缺失、增量任务下git缺失等）才中断，其他只记录状态
4. **不做假设**: 不假设任何依赖已安装或可安装

**必须立即中断检查的项目**（不传递给03）:
- 操作系统类型（必须为Linux）
- Python环境（必须已安装且版本 >= 3.8.0）
- HDC工具（必须已安装）
- 项目根目录（必须存在）
- 设备连接（必须可用）
- Git工具（仅在增量任务时必须）

**传递给03的信息结构**:
```json
{
  "skill_dir": "SKILL所在目录路径",
  "code_root": "代码根目录路径",
  "output_path": "报告输出目录",
  "taskType": "任务类型",
  "os": { /* 操作系统信息 */ },
  "python": { /* Python版本和状态 */ },
  "tools": {
    "pip": { installed, version },
    "git": { installed, version },
    "lcov": { installed, version },
    "addlcov": { installed, local_available, system_available },
    "dos2unix": { installed, version },
    "hdc": { installed, version }
  },
  "pythonPackages": {
    "lxml": { installed, version },
    "selectolax": { installed, version },
    // ... 其他包
  },
  "permissions": { /* 权限状态 */ },
  "disk": { /* 磁盘空间状态 */ }
}
```
