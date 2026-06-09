# 配置检查模块

## 功能

检查项目配置、用户输入参数和配置文件是否合理、完整、正确。

## 执行流程

```
开始
  ↓
[1] 获取基础变量
  ├── 1.1 向上查找SKILL.md, 获取 SKILL_DIR
  ├── 1.2 检查 {SKILL_DIR}/config/user-config.json 是否存在
  ├── 1.3 读取 {SKILL_DIR}/config/user-config.json
  ├── 1.4 获取 CODE_ROOT
  └── 1.5 验证 CODE_ROOT 目录和 build_system.sh
  ↓
[2] 项目结构检查
  ├── 2.1 检查 {CODE_ROOT}/test/testfwk/developer_test 是否存在
  ├── 2.2 检查 {CODE_ROOT}/test/testfwk/xdevice 是否存在
  └── 2.3 检查 {SKILL_DIR}/script/pr_local_coverage 是否存在
  ↓
[3] 用户输入参数检查
  ├── 3.1 识别任务类型 (全量/增量)
  ├── 3.2 解析验证全量覆盖率参数
  ├── 3.3 解析验证增量覆盖率参数
  └── 3.4 解析 output 参数
  ↓
[4] 配置文件检查
  ├── 4.1 验证 hdc 配置格式和内容
  └── 4.2 检查 /etc/lcovrc 中的 lcov_branch_coverage 是否为1
  ↓
[5] 部件名称解析
  ├── 5.1 如果用户提供的是 subsystem_name 且未提供 part_name 时 (全量)
  └── 5.2 如果用户提供了多个 part_name (用逗号分隔)
  ↓
[6] 设备连接配置检查
  ├── 6.1 情况1：没有配置 ip 和 port
  ├── 6.2 情况2：配置了 ip 和 port，但没有配置 sn
  └── 6.3 情况3：配置了 ip、port 和 sn
  ↓
[7] 返回配置和参数信息   
  ↓
结束
```

## 传入参数

从主入口 (SKILL.md) 接收:
- `userInput`: 用户输入的原始参数对象
  - `coverage_type`: 覆盖率类型 ("full_coverage" 或 "incremental_coverage")
  - `subsystem`: 子系统名称 (可选，仅全量覆盖率支持)
  - `part`: 部件名称 (可选，增量必须填写)
  - `module`: 模块名称 (可选，仅全量覆盖率支持)
  - `testsuite`: 测试套名称 (可选，仅全量覆盖率支持)
  - `testcase`: 测试用例名称 (可选，仅全量覆盖率支持)
  - `diffPath`: diff文件路径 (可选，仅增量覆盖率支持)
  - `output_path`: 报告输出路径 (可选)
  - `skip_compiler`: 是否跳过编译 (可选，仅全量覆盖率支持，默认false)

## 传出参数

传递给后续模块:
- `skill_dir`: {SKILL_DIR} - skill 所在目录
- `code_root`: {CODE_ROOT} - 代码根目录
- `userInput.parameters.*`: 用户解析的参数 (subsystem、part、module、testcase、diff、output_path、skip_compiler)
- `config.deviceInfo`: 设备配置信息（完整）
  - `ip`: hdc 连接 IP
  - `port`: hdc 连接端口
  - `sn`: 设备序列号
  - `connected`: 设备连接状态
  - `validated`: 验证状态
- `taskType`: 任务类型 ("full_coverage" 或 "incremental_coverage")
- `part_name_list`: 部件名称列表
- `output_path`: 最终的报告输出路径

## 检查项详细说明

### [1] 获取基础变量

#### 1.1 向上查找 SKILL.md
- 从当前目录开始，逐级向上查找 SKILL.md 文件
- 找到后记录其所在目录为 SKILL_DIR
- 如果找到多个 SKILL.md，使用最上层的一个
- **目的**: 确定skill所在目录，用于后续路径解析

#### 1.2 检查 user-config.json
- 检查路径: `{SKILL_DIR}/config/user-config.json`
- 如果文件不存在 → 调用 06-error-handler.md 返回 `CONFIG_FILE_NOT_FOUND` 错误
- **目的**: 确保配置文件存在，避免后续步骤因配置缺失而失败

#### 1.3 读取 user-config.json
- 使用 JSON 解析器读取配置文件
- 验证 JSON 格式是否正确
- 如果格式错误 → 调用 06-error-handler.md 返回 `INVALID_CONFIG_FORMAT` 错误
- **目的**: 确保配置文件格式正确，可以正确解析

#### 1.4 获取 CODE_ROOT
- 从 user-config.json 中读取 `code_root` 字段
- 如果字段不存在 → 调用 06-error-handler.md 返回 `MISSING_CODE_ROOT` 错误
- 如果字段为空 → 调用 06-error-handler.md 返回 `MISSING_CODE_ROOT` 错误
- **目的**: 获取代码根目录，这是后续所有操作的基础路径

#### 1.5 验证 CODE_ROOT
- 检查 {CODE_ROOT} 目录是否存在
- 检查 {CODE_ROOT}/build_system.sh 是否存在
- 如果目录或文件不存在 → 调用 06-error-handler.md 返回 `INVALID_CODE_ROOT` 错误
- **目的**: 验证代码根目录的可用性和完整性

### [2] 项目结构检查

#### 2.1 检查 developer_test
- 路径: `{CODE_ROOT}/test/testfwk/developer_test`
- 如果不存在 → 调用 06-error-handler.md 返回 `PROJECT_STRUCTURE_ERROR` 错误
- **目的**: 验证全量覆盖率测试框架目录存在

#### 2.2 检查 xdevice
- 路径: `{CODE_ROOT}/test/testfwk/xdevice`
- 如果不存在 → 调用 06-error-handler.md 返回 `PROJECT_STRUCTURE_ERROR` 错误
- **目的**: 验证测试执行设备框架目录存在

#### 2.3 检查 pr_local_coverage
- 路径: `{SKILL_DIR}/scripts/pr_local_coverage`
- 如果不存在 → 调用 06-error-handler.md 返回 `PROJECT_STRUCTURE_ERROR` 错误
- **目的**: 验证增量覆盖率脚本目录存在

### [3] 用户输入参数检查

#### 3.1 识别任务类型
- 根据用户输入中的关键词识别任务类型
- 关键词匹配规则:
  - 全量覆盖率: 匹配 "全量"、"full"、"complete" 等字样
  - 增量覆盖率: 匹配 "增量"、"incremental"、"diff" 等字样
- 如果无法识别 → 调用 06-error-handler.md 返回 `INVALID_TASK_TYPE` 错误
- **目的**: 确定使用全量还是增量覆盖率流程

#### 3.2 解析验证全量覆盖率参数
参数解析规则:
- 子系统: 匹配 '对?(\w+)子系统' 或 '?(\w+)子系统' 或 '子系统(\w+)'
- 部件: 匹配 '对?(\w+(?:,\s*\w+)*)部件' 或 '(\w+(?:,\s*\w+)*)部件' 或 '部件(\w+(?:,\s*\w+)*)'
- 模块: 匹配 '?(\w+)模块' 或 '模块(\w+)'
- 测试套: 匹配 '?(\w+)测试套' 或 '测试套(\w+)'
- 用例: 匹配 '?(\w+)用例' 或 '用例(\w+)'

验证规则:
- **必需参数验证**:
  - subsystem、part、part_name_list 三个必须至少有一个不为空
  - 如果三个都为空 → 调用 06-error-handler.md 返回 `MISSING_TARGET_PARAMETER` 错误
- **参数优先级**:
  - 如果提供了 part → 使用 part，忽略 subsystem
  - 如果未提供 part 但提供了 subsystem → 需要解析子系统获取部件列表
  - part 可以是单个部件或多个部件（逗号分隔）
- **可选参数**:
  - module、testsuite、testcase 为可选参数
  - skip_compiler 为可选参数，默认 false

#### 3.3 解析验证增量覆盖率参数
参数解析规则:
- 部件: 同 3.2 中的部件匹配规则
- diffPath: 匹配文件路径格式

验证规则:
- **必需参数验证**:
  - part 必须有数据（不能为空）
  - 如果 part 为空 → 调用 06-error-handler.md 返回 `MISSING_PART_FOR_INCREMENTAL` 错误
- **不支持子系统**:
  - 如果用户提供了 subsystem → 调用 06-error-handler.md 返回 `INCREMENTAL_NOT_SUPPORT_SUBSYSTEM` 错误
  - 增量覆盖率不支持子系统级别，必须提供部件名称
- **可选参数**:
  - diffPath 为可选参数，不提供则自行解析
  - module、testsuite、testcase 为可选参数

#### 3.4 解析验证 output_path 参数
- 匹配规则: 用户给出将报告输出到xxx目录下
- 如果用户未提供 → 使用默认值: `{CODE_ROOT}/coverage_result`
- 如果用户提供 → 验证路径格式是否存在且可读写 → 不存则创建、不可读写则赋予权限

### [4] 配置文件检查

#### 4.1 验证 hdc 配置
从 user-config.json 中读取 hdc 配置:
- `ip`: hdc 连接 IP 地址 (可选)
- `port`: hdc 连接端口 (可选)
- `sn`: 设备序列号 (可选)

验证规则:
- 如果配置了 ip 和 port，格式必须正确
- 如果配置了 sn，格式必须正确

#### 4.2 检查 /etc/lcovrc
- 读取 /etc/lcovrc 文件
- 查找 lcov_branch_coverage 配置项
- 如果 lcov_branch_coverage=1 → 无需修改
- 如果 lcov_branch_coverage=0 或不存在 → 修改为 lcov_branch_coverage=1
- 验证修改是否成功
- 如果修改失败 → 调用 06-error-handler.md 返回 `LCOV_CONFIG_MODIFY_FAILED` 错误
- **目的**: 确保启用分支覆盖率统计，保证报告完整性

### [5] 部件名称解析

#### 5.1 通过子系统解析部件 (仅全量)
- 前提条件: 用户提供了 subsystem_name 且未提供 part_name
- 执行步骤:
  1. 预编译生成 subsystem_parts.json 文件
     ```bash
     cd {CODE_ROOT}
     ./build_system.sh --abi-type generic_generic_arm_64only --device-type general_all_phone_standard --ccache --build-target hmos_make_test --build-only-gn --build-variant root
     ```

  2. 读取 subsystem_parts.json 文件
     - 路径: `{CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build_configs/parts_info/subsystem_parts.json`
     - **目的**: 获取子系统与部件的映射关系
  3. 查找对应的 subsystem_name
  4. 提取部件列表到 part_name_list
- 示例：
  - subsystem_name为 `ability`
  - subsystem_parts.json中的 ability的格式为
  ```json
  "ability": [
    "dmsfwk_lite",
    "ability_base",
    "ability_runtime",
    ...
  ],
  ...
  ```

  - 提取后part_name_list的值则为：`["dmsfwk_lite", "ability_base", "ability_runtime", ... ]`
- 如果预编译失败 → 调用 06-error-handler.md 返回 `PRECOMPILATION_FAILED` 错误
- 如果找不到 subsystem_name → 调用 06-error-handler.md 返回 `SUBSYSTEM_NOT_FOUND` 错误
- **目的**: 将子系统名称转换为部件列表，便于后续处理

#### 5.2 解析多部件

- 前提条件: 用户提供了 part_name（可以是单个或多个，多个用逗号分隔）
- 执行步骤:
  1. 检查 part 字符串是否包含逗号
  2. 如果包含逗号（多个部件）:
     - 将逗号分隔的字符串拆分成数组
     - 去除每个部件名称的空白字符
  3. 如果不包含逗号（单个部件）:
     - 将单个部件名放入只包含一个元素的数组
  4. 验证部件名称格式
  5. 生成 part_name_list
- 如果部件名称格式不正确 → 调用 06-error-handler.md 返回 `INVALID_PART_NAME` 错误

### [6] 设备连接配置检查

#### 6.1 读取 hdc 配置
- **配置内容**: ip、port、sn
- **读取位置**: `{SKILL_DIR}/config/user-config.json`

#### 6.2 情况1：没有配置 ip 和 port
- **前提条件**: config.deviceInfo 中 ip 和 port 都为空
- **检查步骤**:
  1. 执行 `hdc list targets` 命令
  2. 分析返回结果
- **如果返回 `[Empty]`**:
  - 调用 06-error-handler.md 返回 `DEVICE_NOT_FOUND` 错误
  - 提示用户连接设备或检查 hdc 配置
- **如果返回多行**:
  - 调用 06-error-handler.md 返回 `MULTIPLE_DEVICES_FOUND` 错误
  - 提示用户有多个设备，需要在配置中指定具体设备（ip+port 或 sn）
- **如果返回单行**:
  - 解析返回的设备信息
  - 提取并设置 sn、ip、port
  - 验证连接：执行 `hdc shell echo "connected"`
  - 如果验证成功，更新 config.deviceInfo 对象:
    ```json
    {
      "ip": "提取的IP",
      "port": "提取的端口",
      "sn": "提取的序列号",
      "connected": true,
      "validated": true
    }
    ```
  - 如果验证失败 → 调用 06-error-handler.md 返回 `DEVICE_CONNECTION_FAILED` 错误
- **错误代码**: `DEVICE_NOT_FOUND`, `MULTIPLE_DEVICES_FOUND`, `DEVICE_CONNECTION_FAILED`

#### 6.3 情况2：配置了 IP 和端口
- **前提条件**: config.deviceInfo 中 ip 和 port 有值，sn 为空
- **检查步骤**:
  1. 执行 `hdc -s <ip>:<port> shell echo "connected"` 验证连接
  2. 检查命令返回码和输出
- **如果返回码为 0 且输出包含 "connected"**:
  - 设备连接成功
  - 更新 config.deviceInfo 对象:
    ```json
    {
      "ip": "配置的IP",
      "port": "配置的端口",
      "connected": true,
      "validated": true
    }
    ```
- **如果验证失败**:
  - 调用 06-error-handler.md 返回 `DEVICE_CONNECTION_FAILED` 错误
  - 提示用户检查 IP、端口配置和 hdc 配置
- **错误代码**: `DEVICE_CONNECTION_FAILED`

#### 6.4 情况3：配置了 IP 、端口 和 sn号
- **前提条件**: config.deviceInfo 中 ip 、 port 和sn 都
- **检查步骤**:
  1. 执行 `hdc -s <ip>:<port> -t <sn> shell echo "connected"` 验证连接
  2. 检查命令返回码和输出
- **如果返回码为 0 且输出包含 "connected"**:
  - 设备连接成功
  - 更新 config.deviceInfo 对象:
    ```json
    {
      "ip": "配置的IP",
      "port": "配置的端口",
      "connected": true,
      "validated": true
    }
    ```
- **如果验证失败**:
  - 调用 06-error-handler.md 返回 `DEVICE_CONNECTION_FAILED` 错误
  - 提示用户检查 IP、端口配置和 hdc 配置
- **错误代码**: `DEVICE_CONNECTION_FAILED`

### [7] 返回配置和参数信息

返回包含以下信息的对象:
```json
{
  "skill_dir": "SKILL所在目录路径",
  "code_root": "代码根目录路径",
  "userInput": {
    "parameters": {
      "subsystem": "子系统名称 (如果有)",
      "part": "部件名称 (如果有)",
      "part_name_list": ["部件1", "部件2", ...],
      "module": "模块名称 (如果有)",
      "testsuite": "测试套名称 (如果有)",
      "testcase": "测试用例名称 (如果有)",
      "diffPath": "diff文件路径 (如果有)",
      "output_path": "报告输出路径",
      "skip_compiler": "是否跳过编译"
    }
  },
  "config": {
    "deviceInfo": {
      "ip": "hdc连接IP",
      "port": "hdc连接端口",
      "sn": "设备序列号"
    }
  },
  "taskType": "full_coverage 或 incremental_coverage",
  "output_path": "最终报告输出路径"
}
```

**参数验证规则**:
- 全量模式: `subsystem`、`part`、`part_name_list` 三个至少一个不为空
  - 如果只提供了 `subsystem` → 需要解析生成 `part_name_list`
  - 如果提供了 `part` → 可以是单个或多个（逗号分隔），解析为 `part_name_list`
  - 如果同时提供了 `subsystem` 和 `part` → 使用 `part`，忽略 `subsystem`
- 增量模式: `part` 必须有数据（不能为空）
  - `part` 不能为空，不支持子系统级别
  - 如果提供了 `subsystem` → 报错 `INCREMENTAL_NOT_SUPPORT_SUBSYSTEM`
- 其他参数为可选

## 配置文件格式

### user-config.json 格式
```json
{
  "hdc": {
    "ip": "192.168.1.100",
    "port": "8700",
    "sn": "device_serial_number"
  },
  "code_root": "/path/to/code/root"
}
```

配置字段说明:
- `code_root` (必需): 代码根目录路径
- `hdc` (必需): hdc 设备连接配置
  - `ip` (可选): 设备 IP 地址
  - `port` (可选): 设备端口
  - `sn` (可选): 设备序列号

## 错误处理

任何步骤失败时:
- 调用 06-error-handler.md
- 传入错误类型和相关上下文信息
- 终止执行流程

错误类型包括:
- `CONFIG_FILE_NOT_FOUND` - 配置文件未找到
- `INVALID_CONFIG_FORMAT` - 配置格式错误
- `MISSING_CODE_ROOT` - 缺少 code_root
- `INVALID_CODE_ROOT` - code_root 无效
- `PROJECT_STRUCTURE_ERROR` - 项目结构错误
- `INVALID_TASK_TYPE` - 无效的任务类型
- `MISSING_TARGET_PARAMETER` - 缺少目标参数（全量模式下 subsystem、part、part_name_list 都为空）
- `MISSING_PART_FOR_INCREMENTAL` - 增量模式下缺少部件参数
- `INCREMENTAL_NOT_SUPPORT_SUBSYSTEM` - 增量覆盖率不支持子系统级别
- `LCOV_CONFIG_MODIFY_FAILED` - lcov 配置修改失败
- `PRECOMPILATION_FAILED` - 预编译失败
- `SUBSYSTEM_NOT_FOUND` - 子系统未找到
- `INVALID_PART_NAME` - 无效的部件名称
- `DEVICE_NOT_FOUND` - 设备未找到
- `DEVICE_CONNECTION_FAILED` - 设备连接失败