# 依赖安装模块

## 功能

根据02-env-checker.md记录的依赖安装情况，安装缺失的依赖，验证安装结果。安装失败则中断报错。

## 职责

- **读取JSON状态**: 读取02传入的完整依赖检查JSON
- **基于状态安装**: 严格根据02的JSON中 `installed` 字段决定安装
- **只安装缺失的**: 只安装 `installed === false` 的依赖
- **不重复安装**: 不重复安装 `installed === true` 的依赖
- **不额外安装**: 不安装不在JSON中的依赖
- **失败则中断**: 任何安装失败都中断流程并报错

## 执行流程

```
开始
  ↓
[1] 读取02传入的JSON
  ├── 1.1 读取完整的依赖检查结果JSON
  ├── 1.2 验证JSON格式和结构
  ├── 1.3 遍历JSON中的所有依赖
  │     ├── tools.lcov.installed === false? → 加入安装列表
  │     ├── tools.dos2unix.installed === false? → 加入安装列表
  │     ├── pythonPackages.*.installed === false? → 加入安装列表
  │     ├── tools.git、tools.hdc → 跳过
  │     ├── tools.addlcov → 从本地提供
  │     └── tools.pip.installed === false? → 加入安装列表
  ├── 1.4 生成待安装列表（只包含installed=false的依赖）
  └── 1.5 如果待安装列表为空 → 跳到[5]验证
  ↓
[2] 安装缺失的系统依赖（基于JSON）
  ├── 2.1 优先安装pip（如果需要）
  │     ├── 检查tools.pip.installed
  │     ├── 如果false → 安装pip
  │     │     ├── 使用apt-get: sudo apt-get install python3-pip
  │     │     └── 或使用yum: sudo yum install python3-pip
  │     └── 如果安装失败 → 调用06-error-handler.md中断报错
  ├── 2.2 使用包管理器安装其他依赖（apt-get或yum）
  │     ├── 2.2.1 更新包列表
  │     ├── 2.2.2 只安装JSON中installed=false的系统依赖（排除pip）
  │     └── 2.2.3 验证每个依赖安装结果
  └── 2.3 如果任何一个安装失败 → 调用06-error-handler.md中断报错
  ↓
[3] 安装缺失的Python包（基于JSON）
  ├── 3.1 检查pip是否可用（如果不可用则中断）
  ├── 3.2 使用pip安装缺失的Python包
  │     ├── 3.2.1 升级pip（如果可用）
  │     ├── 3.2.2 只安装JSON中installed=false的Python包
  │     └── 3.2.3 验证每个包安装结果
  └── 3.3 如果任何一个安装失败 → 调用06-error-handler.md中断报错
  ↓
[4] 提供本地工具（addlcov）
  ├── 4.1 检查{SKILL_DIR}/scripts/addlcov是否存在
  ├── 4.2 如果存在 → 检查可执行性，设置权限
  └── 4.3 如果不存在 → 中断报错
  ↓
[5] 验证最终安装状态
  ├── 5.1 重新检查JSON中标记为需要安装的依赖
  ├── 5.2 确认所有installed=false的依赖都已安装
  └── 5.3 如果有未安装的依赖 → 中断报错
  ↓
[6] 返回依赖安装状态
  ↓
结束
```

## 传入参数

从 02-env-checker.md 接收完整的依赖检查结果JSON:

```json
{
  "skill_dir": "SKILL所在目录路径",
  "code_root": "代码根目录路径",
  "output_path": "报告输出目录",
  "tools": {
    "pip": {
      "installed": true/false,
      "version": "x.x.x",
      "path": "/path/to/pip"
    },
    "git": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "lcov": {
      "installed": true/false,
      "version": "x.x.x",
      "path": "/path/to/lcov"
    },
    "addlcov": {
      "installed": true/false,
      "local_available": true/false,
      "system_available": true/false,
      "local_path": "{SKILL_DIR}/scripts/addlcov",
      "version": "x.x.x"
    },
    "dos2unix": {
      "installed": true/false,
      "version": "x.x.x",
      "path": "/path/to/dos2unix"
    },
    "hdc": {
      "installed": true/false,
      "version": "x.x.x",
      "path": "/path/to/hdc"
    }
  },
  "pythonPackages": {
    "lxml": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "selectolax": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "CppHeaderParser": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "requests": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "pyserial": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "paramiko": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "rsa": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "lz4": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "json5": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "beautifulsoup4": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "PyYAML": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "redis": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "pycryptodome": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "esdk-obs-python": {
      "installed": true/false,
      "version": "x.x.x"
    },
    "chardet": {
      "installed": true/false,
      "version": "x.x.x"
    }
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
  }
}
```

**关键说明**:
1. 只安装 `installed === false` 的依赖
2. 不重复安装 `installed === true` 的依赖
3. 不安装不在JSON中的依赖
4. 严格基于02的检查结果
5. 不尝试安装 git、pip、hdc（即使installed=false）

## 传出参数

传递给覆盖率执行模块:
- `isAllInstalled`: 所有依赖是否已安装 (true/false)
- `dependencies`: 依赖安装状态
  - `system`: 系统依赖安装状态
    - `lcov`: lcov 安装状态和版本
    - `genhtml`: genhtml 安装状态和版本
    - `dos2unix`: dos2unix 安装状态和版本
    - `gcc`: gcc 安装状态和版本
    - `g++`: g++ 安装状态和版本
    - `make`: make 安装状态和版本
    - `cmake`: cmake 安装状态和版本
    - `python3-dev`: python3-dev 安装状态和版本
  - `python`: Python 包依赖安装状态
    - `lxml`: lxml 安装状态和版本
    - `selectolax`: selectolax 安装状态和版本
    - `CppHeaderParser`: CppHeaderParser 安装状态和版本
    - `requests`: requests 安装状态和版本
    - `pyserial`: pyserial 安装状态和版本
    - `paramiko`: paramiko 安装状态和版本
    - `rsa`: rsa 安装状态和版本
    - `lz4`: lz4 安装状态和版本
    - `json5`: json5 安装状态和版本
    - `beautifulsoup4`: beautifulsoup4 安装状态和版本
    - `PyYAML`: PyYAML 安装状态和版本
    - `redis`: redis 安装状态和版本
    - `pycryptodome`: pycryptodome 安装状态和版本
    - `esdk-obs-python`: esdk-obs-python 安装状态和版本
    - `chardet`: chardet 安装状态和版本

## 02与03的数据驱动接口

### 数据流

1. **02 → 03**: 传递完整的依赖检查JSON
   - 包含所有依赖的 `installed` 状态
   - 03只读取，不修改02的检查逻辑

2. **03 → 04/05**: 传递安装完成后的状态
   - 确认所有必需依赖都已安装
   - 不再传递详细的依赖状态

### 数据驱动原则

1. **完全依赖02的检查结果**
   - 03不进行任何依赖检查
   - 03完全基于02的JSON决定安装行为

2. **精确控制安装范围**
   ```javascript
   // 03只执行以下逻辑
   if (dependency.installed === false) {
     install(dependency);
   }
   ```

3. **避免过度安装**
   - 不重新安装已安装的依赖
   - 不安装不在JSON中的依赖
   - 不安装明确跳过的依赖（git、pip、hdc）

4. **失败则终止**
   - 任何一个依赖安装失败就中断
   - 不允许部分安装
   - 确保所有需要的依赖都可用

### JSON字段映射

| JSON字段 | 03行为 | 说明 |
|---------|--------|------|
| `tools.pip.installed` | false→优先安装, true→跳过 | Python包管理器 |
| `tools.lcov.installed` | false→安装, true→跳过 | 覆盖率工具 |
| `tools.dos2unix.installed` | false→安装, true→跳过 | 文本转换工具 |
| `tools.git.installed` | 无论真假都跳过 | 不安装git |
| `tools.addlcov.installed` | 从本地提供 | 本地工具 |
| `tools.hdc.installed` | 跳过（02已验证） | 必须存在 |
| `pythonPackages.*.installed` | false→安装, true→跳过 | Python包 |

## 配置文件

使用以下配置文件:
- `{SKILL_DIR}/config/dependencies.txt` - 系统依赖列表（备用）
- `{SKILL_DIR}/config/requirements.txt` - Python 依赖列表（备用）

**重要**: 优先使用02传入的JSON，配置文件仅作为备用参考。

### dependencies.txt 格式示例
```
# 覆盖率工具
lcov
genhtml

# 文本处理工具
dos2unix

# 编译工具
gcc
g++
make
cmake

# Python 开发工具
python3-dev
```

### requirements.txt 格式示例
```
# XML/HTML 解析
lxml>=4.6.0
selectolax>=0.2.0

# C++ 头文件解析
CppHeaderParser

# HTTP 请求
requests>=2.25.0

# 串口通信
pyserial>=3.3

# SSH 协议支持
paramiko>=2.7.0
rsa>=4.7

# 压缩
lz4>=4.0.0

# JSON 解析
json5>=0.9.0

# HTML/XML 解析
beautifulsoup4>=4.9.0

# YAML 解析
PyYAML>=5.4.0

# Redis 客户端
redis>=3.5.0

# 加密库
pycryptodome>=3.10.0

# OBS 存储 SDK
esdk-obs-python>=3.20.0

# 字符编码检测
chardet>=4.0.0
```

## 详细步骤说明

### [1] 分析02传递的依赖状态

#### 1.1 读取02的检查结果
- 从传入参数中获取完整的依赖检查JSON
- 验证JSON结构是否正确
- 记录所有依赖的安装状态

#### 1.2 识别需要安装的系统依赖
遍历 `tools` 对象，根据 `installed` 字段识别需要安装的依赖：
```javascript
const toInstallSystem = [];
if (!tools.lcov.installed) toInstallSystem.push('lcov');
if (!tools.dos2unix.installed) toInstallSystem.push('dos2unix');
// 注意：git和pip不在此列表中，即使installed=false也不安装
// addlcov从本地提供，不在此列表中
// hdc已在02中验证，不在此列表中
```

#### 1.3 识别需要安装的Python包
遍历 `pythonPackages` 对象，根据 `installed` 字段识别需要安装的包：
```javascript
const toInstallPython = [];
for (const [pkg, info] of Object.entries(pythonPackages)) {
  if (!info.installed) toInstallPython.push(pkg);
}
```

#### 1.4 识别需要提供的本地工具
- 检查 `tools.addlcov.local_available` 或 `system_available`
- 如果需要使用addlcov但不可用，从本地提供

#### 1.5 识别跳过的依赖
以下依赖即使 `installed === false` 也不安装：
- `tools.git.installed === false` → 跳过（02已根据任务类型处理）
- `tools.hdc.installed === false` → 跳过（02已验证）

注意：pip需要安装，不在跳过列表中。

#### 1.6 如果没有需要安装的依赖
- 如果 `toInstallSystem.length === 0` 且 `toInstallPython.length === 0`
- 直接跳转到 [5] 验证最终状态

### [2] 安装缺失的系统依赖

#### 2.1 优先安装pip（如果需要）
- **检查状态**: 查看 `tools.pip.installed`
- **如果 `tools.pip.installed === false`**:
  - **apt-get**: `sudo apt-get install python3-pip`
  - **yum**: `sudo yum install python3-pip`
  - **验证**: 执行 `pip --version` 确认安装成功
  - **失败处理**: 调用06-error-handler.md返回`PIP_INSTALL_FAILED`错误，中断流程
- **如果 `tools.pip.installed === true`**:
  - 跳过pip安装

#### 2.2 检测包管理器
- 执行 `which apt-get` → 成功则使用apt-get
- 执行 `which yum` → 成功则使用yum
- 都不成功 → 调用06-error-handler.md中断报错

##### 2.2.2 更新包列表
- **apt-get**: `sudo apt-get update`
- **yum**: `sudo yum makecache`

##### 2.2.2 安装缺失的系统依赖（排除pip）
使用步骤1.2生成的列表，只安装 `installed === false` 的系统依赖：
```bash
# apt-get（不包括pip，因为已单独处理）
sudo apt-get install -y lcov dos2unix

# yum（不包括pip，因为已单独处理）
sudo yum install -y lcov dos2unix
```

**注意**: 
- 不重复安装 `installed === true` 的依赖
- 不安装不在JSON中的依赖
- 不安装git、addlcov、hdc
- pip已在2.1中单独处理

##### 2.2.4 验证每个依赖安装结果
对每个安装的依赖执行验证命令：
- 检查命令是否存在：`which lcov`
- 检查版本信息：`lcov --version`

#### 2.3 安装失败处理
- 如果任何一个依赖安装失败：
  - 记录失败包名称和错误信息
  - 调用06-error-handler.md返回`SYSTEM_DEPENDENCY_INSTALL_FAILED`错误
  - **中断流程**

### [3] 安装缺失的Python包

#### 3.1 检查pip是否可用
- 执行 `python -m pip --version` 或 `pip --version`
- 如果不可用：
  - 调用06-error-handler.md返回`PIP_NOT_AVAILABLE`错误
  - **中断流程**

#### 3.2 使用pip安装缺失的Python包

##### 3.2.1 升级pip
- 执行 `python -m pip install --upgrade pip`
- 如果失败，记录警告继续执行

##### 3.2.2 安装缺失的Python包
使用步骤1.3生成的列表，只安装 `installed === false` 的包：
```bash
# 只安装02检查未安装的包
python -m pip install lxml selectolax CppHeaderParser requests pyserial paramiko rsa lz4 json5 beautifulsoup4 PyYAML redis pycryptodome esdk-obs-python chardet
```

**注意**: 
- 不重复安装 `installed === true` 的包
- 不安装不在JSON中的包

##### 3.2.3 验证每个包安装结果
对每个安装的包执行验证：
- 执行 `pip show <package_name>`
- 检查返回结果是否包含版本信息

#### 3.3 安装失败处理
- 如果任何一个包安装失败：
  - 记录失败包名称和错误信息
  - 调用06-error-handler.md返回`PYTHON_DEPENDENCY_INSTALL_FAILED`错误
  - **中断流程**

### [4] 提供本地工具（addlcov）

#### 4.1 检查本地addlcov
- 检查路径：`{SKILL_DIR}/scripts/addlcov`
- 根据 `tools.addlcov.local_available` 判断

#### 4.2 将其复制到默认命令行目录中
- 命令
  ```bash
  sudo cp {SKILL_DIR}/scripts/addlcov /usr/bin/addlcov
  sudo chmod +x /usr/bin/addlcov
  ```

#### 4.3 处理不可用情况
- 如果本地不存在且系统也不可用：
  - 记录错误信息
  - 调用06-error-handler.md返回`ADDLCOV_NOT_FOUND`错误
  - **中断流程**

### [5] 验证最终安装状态

#### 5.1 重新检查所有依赖
使用与02相同的方法重新检查：
- 只检查步骤1.2和1.3中标记为需要安装的依赖
- 不重新检查已经标记为 `installed === true` 的依赖

#### 5.2 确认所有需要安装的依赖都已安装
- 对比步骤1.2和1.3的待安装列表
- 确认所有项都已安装成功

#### 5.3 处理未安装的依赖
- 如果有未安装的依赖：
  - 记录哪些依赖未安装
  - 调用06-error-handler.md返回相关错误
  - **中断流程**

- 如果所有依赖都已安装：
  - 设置 `isAllInstalled = true`
  - 继续下一步
- **文件路径**: `{SKILL_DIR}/config/dependencies.txt`
- **读取方法**: 逐行读取，跳过空行和以 `#` 开头的注释行
- **处理**: 将依赖名称存储到列表中

#### 1.2 使用包管理器安装
##### 1.2.1 检测包管理器
- **检测命令**:
  - 执行 `which apt-get`，如果成功 → 使用 apt-get
  - 执行 `which yum`，如果成功 → 使用 yum
  - 都不成功 → 调用 06-error-handler.md 返回 `PACKAGE_MANAGER_NOT_FOUND` 错误

##### 1.2.2 更新包列表 (apt-get)
- **命令**: `sudo apt-get update`
- **说明**: 更新包索引，确保获取最新的包信息
- **检查 permissions.sudo_available**:
  - 如果为 true: 使用 `sudo apt-get update`
  - 如果为 false: 使用 `apt-get update`，如果失败则提示用户需要手动更新
- **如果更新失败**: 记录警告，继续尝试安装

##### 1.2.3 安装依赖包
**apt-get 命令**:
```bash
sudo apt-get install -y lcov genhtml dos2unix gcc g++ make cmake python3-dev
```

**yum 命令**:
```bash
sudo yum install -y lcov dos2unix gcc gcc-c++ make cmake python3-devel
```

**安装步骤**:
1. 将所有依赖名称连接成一个字符串，用空格分隔
2. 构建安装命令
3. 执行安装命令
4. 检查返回码
5. 如果返回码 != 0:
   - 分析错误信息
   - 调用 06-error-handler.md 返回 `SYSTEM_DEPENDENCY_INSTALL_FAILED` 错误
   - 传入失败包名称和错误信息

##### 1.2.4 验证安装结果
**验证方法**:
```bash
# lcov
which lcov
lcov --version

# genhtml
which genhtml
genhtml --version

# dos2unix
which dos2unix
dos2unix --version

# gcc
which gcc
gcc --version

# g++
which g++
g++ --version

# make
which make
make --version

# cmake
which cmake
cmake --version

# python3-dev
dpkg -l python3-dev  # apt-get
rpm -qa python3-devel  # yum
```

**验证步骤**:
1. 对每个依赖执行验证命令
2. 检查命令是否执行成功
3. 记录安装状态和版本信息

### [2] 安装 Python 包依赖

#### 2.1 读取 Python 依赖列表
- **文件路径**: `{SKILL_DIR}/config/requirements.txt`
- **读取方法**: 逐行读取，跳过空行和以 `#` 开头的注释行
- **处理**: 将依赖名称和版本要求存储到列表中

#### 3.2 使用 pip 安装 Python 包

##### 3.2.1 检查 pip 是否可用
- **检查命令**: `python -m pip --version` 或 `pip --version`
- **如果 pip 不可用**:
  - 调用 06-error-handler.md 返回 `PIP_NOT_AVAILABLE` 错误
  - 中断流程
  - 提示用户手动安装 pip
- **错误代码**: `PIP_NOT_AVAILABLE`（中断）

##### 3.2.2 升级 pip
- **命令**: `python -m pip install --upgrade pip` 或 `python3 -m pip install --upgrade pip`
- **说明**: 确保 pip 是最新版本，避免安装问题
- **如果升级失败**: 记录警告，继续安装

##### 2.2.2 安装依赖包
**安装命令**:
```bash
python -m pip install -r {SKILL_DIR}/config/requirements.txt
```

**安装步骤**:
1. 切换到 {SKILL_DIR} 目录
2. 执行 pip install 命令
3. 监控安装进度
4. 捕获安装输出
5. 检查返回码
6. 如果返回码 != 0:
   - 分析错误信息
   - 尝试逐个安装失败的包
   - 如果单个包安装失败，记录该包但继续安装其他包
   - 调用 06-error-handler.md 返回 `PYTHON_DEPENDENCY_INSTALL_FAILED` 错误
   - 传入失败包名称和错误信息

##### 2.2.3 验证安装结果
**验证方法**:
```bash
# 对每个包执行
pip show <package_name>
```

**验证步骤**:
1. 对每个依赖执行 `pip show` 命令
2. 检查命令是否执行成功
3. 解析版本信息
4. 比较版本是否符合 requirements.txt 中的要求
5. 记录安装状态和版本信息

### [3] 处理 addlcov

- **命令**: `which addlcov` 和 `addlcov --version`
- **如果找到**: 记录版本信息
- **如果不存在**: 记录错误信息，调用06-error-handler.md返回`ADDLCOV_NOT_FOUND`错误
- **中断流程**


### [4] 验证安装结果

#### 4.1 重新检查系统依赖
- 使用与 02-env-checker.md 相同的检查方法
- 对所有系统依赖进行检查
- 记录最终状态

#### 4.2 重新检查 Python 包
- 使用 `pip show` 对所有 Python 包进行检查
- 记录最终状态

#### 4.3 返回部分安装状态
- 如果有未安装的依赖:
  - 设置 `isAllInstalled = false`
  - 在 `dependencies` 对象中标记哪些依赖未安装
  - 提供用户友好的消息说明哪些依赖缺失
- 如果所有依赖都已安装:
  - 设置 `isAllInstalled = true`

### [5] 返回依赖安装状态

返回包含以下信息的对象:
```json
{
  "isAllInstalled": true,
  "dependencies": {
    "system": {
      "lcov": {
        "installed": true,
        "version": "1.14",
        "path": "/usr/bin/lcov"
      },
      "genhtml": {
        "installed": true,
        "version": "1.14",
        "path": "/usr/bin/genhtml"
      },
      "dos2unix": {
        "installed": true,
        "version": "7.4.0",
        "path": "/usr/bin/dos2unix"
      },
      "gcc": {
        "installed": true,
        "version": "9.3.0",
        "path": "/usr/bin/gcc"
      },
      "g++": {
        "installed": true,
        "version": "9.3.0",
        "path": "/usr/bin/g++"
      },
      "make": {
        "installed": true,
        "version": "4.2.1",
        "path": "/usr/bin/make"
      },
      "cmake": {
        "installed": true,
        "version": "3.16.3",
        "path": "/usr/bin/cmake"
      },
      "python3-dev": {
        "installed": true,
        "version": "3.8.5",
        "path": "/usr/include/python3.8"
      }
    },
    "python": {
      "lxml": {
        "installed": true,
        "version": "4.6.3"
      },
      "selectolax": {
        "installed": true,
        "version": "0.2.6"
      },
      "CppHeaderParser": {
        "installed": true,
        "version": "2.7.4"
      },
      "requests": {
        "installed": true,
        "version": "2.25.1"
      },
      "pyserial": {
        "installed": true,
        "version": "3.4"
      },
      "paramiko": {
        "installed": true,
        "version": "2.7.2"
      },
      "rsa": {
        "installed": true,
        "version": "4.7"
      },
      "lz4": {
        "installed": true,
        "version": "4.0.2"
      },
      "json5": {
        "installed": true,
        "version": "0.9.5"
      },
      "beautifulsoup4": {
        "installed": true,
        "version": "4.9.3"
      },
      "PyYAML": {
        "installed": true,
        "version": "5.4.1"
      },
      "redis": {
        "installed": true,
        "version": "3.5.3"
      },
      "pycryptodome": {
        "installed": true,
        "version": "3.10.1"
      },
      "esdk-obs-python": {
        "installed": true,
        "version": "3.20.5"
      },
      "chardet": {
        "installed": true,
        "version": "4.0.0"
      }
    },
    "addlcov": {
      "installed": true,
      "path": "{SKILL_DIR}/scripts/addlcov",
      "version": "1.0.0"
    }
  },
  "missing": [],
  "warnings": []
}
```

## 依赖安装策略

### 不安装的依赖（跳过）
- **git**: 不安装，跳过

### 本地提供的依赖（不安装）
- **addlcov**: 从 skill 脚本目录提供，不安装

### 需要安装的系统依赖（安装失败则中断）
- **pip**: 包下载工具，如果缺失则安装
- **lcov**: 覆盖率工具，如果缺失则安装
- **genhtml**: 覆盖率报告生成工具，如果缺失则安装
- **dos2unix**: 文件格式转换工具，如果缺失则安装
- **gcc**: C 编译器，如果缺失则安装
- **g++**: C++ 编译器，如果缺失则安装
- **make**: 构建工具，如果缺失则安装
- **cmake**: 构建工具，如果缺失则安装
- **python3-dev**: Python 开发头文件，如果缺失则安装

### 需要安装的 Python 包（安装失败则中断）
- **lxml**: XML 解析
- **selectolax**: HTML 解析
- **CppHeaderParser**: C++ 头文件解析
- **requests**: HTTP 请求
- **pyserial**: 串口通信
- **paramiko**: SSH 协议支持
- **rsa**: 加密库
- **lz4**: 压缩库
- **json5**: JSON 解析
- **beautifulsoup4**: HTML/XML 解析
- **PyYAML**: YAML 解析
- **redis**: Redis 客户端
- **pycryptodome**: 加密库
- **esdk-obs-python**: OBS 存储 SDK
- **chardet**: 字符编码检测

## 错误处理

### pip 不可用错误（中断）
- **错误代码**: `PIP_NOT_AVAILABLE`
- **触发条件**: 需要使用 pip 但 pip 不可用
- **处理**: 调用 06-error-handler.md，中断流程

### 系统依赖安装失败（中断）
- **错误代码**: `SYSTEM_DEPENDENCY_INSTALL_FAILED`
- **触发条件**: 系统依赖安装失败
- **处理**: 调用 06-error-handler.md，中断流程
- **传递信息**: 失败的依赖名称和错误信息

### Python 包安装失败（中断）
- **错误代码**: `PYTHON_DEPENDENCY_INSTALL_FAILED`
- **触发条件**: Python 包安装失败
- **处理**: 调用 06-error-handler.md，中断流程
- **传递信息**: 失败的包名称和错误信息

### 其他错误（中断）
- **错误代码**: `PACKAGE_MANAGER_NOT_FOUND` - 包管理器未找到
- **错误代码**: `PERMISSION_DENIED` - 权限不足
- **错误代码**: `NETWORK_ERROR` - 网络错误导致安装失败
- **错误代码**: `CONFLICT_ERROR` - 包冲突导致安装失败
- **错误代码**: `ADDLCOV_NOT_FOUND` - addlcov移动失败且系统不存在该工具

**错误处理原则**:
1. 任何安装失败都中断流程
2. 不记录部分安装状态，确保所有必需依赖都已安装
3. 提供详细的错误信息和解决方案

## 错误恢复策略

### 系统依赖安装失败
1. 记录失败的包名称
2. 尝试单独安装失败的包
3. 如果仍然失败，中断流程并提示用户手动安装

### Python 包安装失败
1. 尝试使用 `--user` 参数安装到用户目录
2. 尝试使用 `--ignore-installed` 参数覆盖已安装的包
3. 如果仍然失败，中断流程并提示用户使用虚拟环境

### 网络错误
1. 尝试使用国内镜像源
2. 增加重试次数
3. 如果仍然失败，中断流程并提示用户检查网络连接

## 注意事项

### 数据驱动原则

1. **严格基于02的JSON**:
   - 只安装JSON中 `installed === false` 的依赖
   - 不重复安装 `installed === true` 的依赖
   - 不安装不在JSON中的依赖
   - 不进行任何额外的依赖检查

2. **不进行假设**:
   - 不假设某个依赖已安装
   - 不假设某个依赖未安装
   - 完全依赖02的检查结果

3. **安装行为**:
   - `tools.pip.installed === false` → 优先安装
   - `tools.lcov.installed === false` → 安装
   - `tools.dos2unix.installed === false` → 安装
   - `pythonPackages.*.installed === false` → 安装
   - 其他情况 → 不安装

### 02和03的职责分工

**02-env-checker.md**:
- 职责：只负责检查，不安装
- 行为：检查所有依赖和工具的安装情况
- 输出：完整的依赖状态JSON
- 中断：致命错误（OS不支持、Python问题、HDC缺失等）直接中断

**03-dependency-installer.md**:
- 职责：根据02的JSON安装缺失依赖
- 行为：读取JSON，只安装 `installed === false` 的依赖
- 输出：所有必需依赖都已安装
- 中断：任何安装失败都中断流程

### 特殊依赖的处理

#### pip
- **02行为**: 检查pip是否安装，记录状态（警告级别）
- **03行为**: 如果未安装则优先安装，安装失败则中断报错
- **原因**: pip用于安装Python包，必须确保可用

#### git
- **02行为**: 检查git是否安装，记录状态（增量任务时中断）
- **03行为**: 不安装git，直接跳过
- **原因**: git不是必需依赖，02已根据任务类型处理

#### addlcov
- **02行为**: 检查本地和系统是否有addlcov，记录状态
- **03行为**: 从本地`{SKILL_DIR}/scripts/addlcov`提供，不安装
- **原因**: addlcov是skill自带的工具

#### hdc
- **02行为**: 检查hdc是否安装，如果未安装则立即中断
- **03行为**: 不处理hdc（02已确保它存在）
- **原因**: hdc是核心工具，必须在安装前就存在

### 安装策略

1. **按需安装**:
   - 只安装JSON中 `installed === false` 的依赖
   - 不重复安装已存在的依赖
   - 不尝试安装标记为不安装的依赖

2. **安装失败即中断**:
   - 任何依赖安装失败都中断流程
   - 不允许部分安装
   - 确保所有必需依赖都已安装

3. **使用包管理器**:
   - 系统依赖：使用apt-get或yum
   - Python包：使用pip

4. **验证安装结果**:
   - 每个依赖安装后立即验证
   - 确认命令可执行
   - 确认版本正确
