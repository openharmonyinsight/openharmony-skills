# 增量覆盖率执行模块

## 功能

执行增量覆盖率测试流程，针对部件级别的代码变更生成覆盖率报告。本模块是 AI 执行指南，提供详细的、可执行的步骤让 AI 自主完成增量覆盖率流程。

## Anti-Patterns - 绝对禁止事项

NEVER 做以下操作，否则会导致测试无法编译、运行：

| 禁止项                                          | 原因                                                | 正确做法                                            |
| -------------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| **NEVER 中断或轮询长时间运行的命令**    | 必须使用 timeout 并等待自然完成 | 禁止主动中断或轮询检查命令状态，让 timeout 机制处理超时    |
| **NEVER 在编译过程中跳过验证**    | 必须验证每个步骤的输出 | 编译和执行每个步骤后必须验证结果，确保成功后再继续下一步    |

## 执行流程

```
传入参数
  ↓
[全局初始化]
├── 创建 {OUTPUT_PATH} 目录（如果不存在）
└── 初始化成功/失败列表
  ↓
[对每个 part_name 执行完整流程]
├── 1.1 确认 diff 文件路径（每个部件独立）
├── 1.2 验证 diff 文件是否存在且非空（每个部件独立）
├── 1.3 自动生成 diff 文件（每个部件独立，1.3.1预编译只执行一次）
├── 1.4 执行 local_build 编译产物（每个部件独立）
├── 1.5 检查编译产物是否生成（每个部件独立）
├── 2.1 检查参数,拼接完整命令（每个部件独立）
├── 2.2 执行 pr_coverage 主流程（每个部件独立）
├── 2.3 检查覆盖率报告是否生成（每个部件独立）
├── 3.1 定位生成的增量覆盖率报告（每个部件独立）
├── 3.3 移动报告到 {OUTPUT_PATH}/{part_name}_incremental_coverage_report/（每个部件独立）
└── [记录执行状态]（成功/失败）
  ↓
[全局结果汇总]
├── 统计成功和失败的部件
└── 生成报告路径列表（文本格式）
  ↓
[恢复环境]
├── 4.1 清理临时编译产物（所有部件执行完）
├── 4.2 清理临时覆盖率文件（所有部件执行完）
└── 4.3 恢复工作目录
  ↓
[清理临时文件]
├── 5.1 删除编译临时文件（所有部件执行完）
├── 5.2 删除覆盖率临时文件（所有部件执行完）
└── 5.3 删除其他中间产物（所有部件执行完）
  ↓
结束
```

## 传入参数

从 01-config-checker.md 接收（完整配置）：
- `skill_dir`: {SKILL_DIR}
- `code_root`: {CODE_ROOT}
- `taskType`: 任务类型
- `userInput.parameters`: 用户参数
  - `part_name_list`: 部件名称列表 (必需，增量不支持子系统级别)
  - `diffPath`: diff 文件路径 (可选，不传入则自行解析)
  - `output_path`: 报告输出路径
- `config.deviceInfo`: 设备配置信息（完整）
  - `ip`: hdc 连接 IP
  - `port`: hdc 连接端口
  - `sn`: 设备序列号
  - `connected`: 设备连接状态
  - `validated`: 验证状态

## 使用脚本

- `{SKILL_DIR}/scripts/pr_local_coverage/local_build/local_build.py` - 本地编译脚本（每个部件独立执行）
  - 功能: 执行增量覆盖率编译，收集编译产物
  - 参数: {CODE_ROOT} {part_name} {diff_file}
  - 产物: {CODE_ROOT}/out/coverage.tar.lz4
  - 待后续完善具体实现细节
- `{SKILL_DIR}/scripts/pr_local_coverage/pr_coverage/pr_coverage.py` - 覆盖率计算脚本（每个部件独立执行）
  - 功能: 执行增量覆盖率计算，生成报告
  - 参数: {CODE_ROOT} {part_name} {output_path}
  - 报告路径: {SKILL_DIR}/scripts/pr_local_coverage/pr_coverage/output/output_YYYYMMDDHHMM/{part_name}/report/diff_html/
  - 待后续完善具体实现细节


## 详细步骤说明

### [全局初始化]

#### 初始化执行环境
- **目标路径**: `{OUTPUT_PATH}` (从 userInput.parameters.output_path 获取)
- **命令**: 
  ```bash
  mkdir -p {OUTPUT_PATH}
  ```
- **验证**: 
  ```bash
  ls -la {OUTPUT_PATH}
  ```
- **失败处理**: 目录创建失败 → 调用 06-error-handler.md 返回 `OUTPUT_DIR_CREATE_FAILED` 错误

#### 初始化执行状态记录
- **成功列表**: `success_parts = []`
- **失败列表**: `failed_parts = []`
- **作用**: 记录每个部件的执行状态，最终汇总结果

### [对每个 part_name 执行完整流程]

#### 1.1 确认 diff 文件路径

##### 单部件场景
- **条件判断**: 检查 `part_name_list` 是否只有一个部件
- **用户提供了 diff_file**:
  - **路径**: `{diffPath}` (从 userInput.parameters.diffPath 获取)
  - **验证**: 检查文件是否存在，文件不存在 → 执行 1.3 自动生成 diff 文件

##### 多部件场景
- **条件判断**: 检查 `part_name_list` 是否包含多个部件
- **处理逻辑**: 默认没有diff文件，为每个部件执行 1.3 自动生成 diff 文件的逻辑

#### 1.2 验证 diff 文件是否存在且非空

##### 检查 diff 文件是否存在
- **操作**: 使用 `ls -la` 命令检查文件是否存在
- **命令**: `ls -la {diff_file_path}`
- **判断**: 
  - 文件存在 → 继续检查是否为空
  - 文件不存在 → 执行 1.3 自动生成 diff 文件

##### 检查 diff 文件是否为空
- **操作**: 检查文件大小是否为 0
- **命令**: `wc -l {diff_file_path}`
- **判断**: 
  - 文件非空 → 直接执行 1.4 执行 local_build 编译
  - 文件为空 → 执行 1.3 自动生成 diff 文件

#### 1.3 自动生成 diff 文件

##### 1.3.1 预编译生成 parts_path_info.json（仅执行一次）
- **检查是否已进行预编译**: 检查编译产物 `{CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build_configs`是否存在
- **预编译执行条件**: 
  - 第一次执行时检查
  - 如果不存在则执行预编译
  - 如果已存在则跳过（避免重复执行）
  - **不存在则执行下列步骤**:
    1. 执行下列命令，进行预编译
      ```bash
      cd {CODE_ROOT}
      ./build_system.sh --abi-type generic_generic_arm_64only --device-type general_all_phone_standard --ccache --build-target hmos_make_test --build-only-gn --build-variant root
      ```

    2. 检查编译是否成功,失败则中断流程 → 调用06-error-handler.md返回`BUILD_GN_ONLY_FAILED`错误;
    3. 再次检查编译产物,失败则中断流程 → 调用06-error-handler.md返回`BUILD_CONFIG_NOT_FOUND`错误;
  - **存在则继续后续流程**:

##### 1.3.2 解析部件名对应的路径
- **操作**: 读取 parts_path_info.json 文件
- **路径**: `{CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build_configs/parts_info/parts_path_info.json`
- **解析步骤**:
  1. 使用 JSON 解析器读取文件
  2. 查找 part_name 对应的条目
  3. 提取路径信息
- **示例格式**:
  ```json
  {
    "ability_base": "founction/ability/ability_base",
    "ability_runtime": "founction/ability/ability_runtime",
    ...
  }
  ```

  -其中: ability_base 对应的 code_path 为 `founction/ability/ability_base`;ability_runtime 对应的code_path为 `founction/ability/ability_runtime`
- **失败处理**: part_name 不存在 → 调用 06-error-handler.md 返回 `PART_PATH_NOT_FOUND` 错误

##### 1.3.3 解析代码目录绝对路径
- **操作**: 拼接路径，构建完整的代码绝对路径
- **路径**: `{CODE_ROOT}/{code_path}`
- **示例**: `founction/ability/ability_base` → `{CODE_ROOT}/founction/ability/ability_base`
- **验证**: 检查目录是否存在
- **失败处理**: code_path 不存在 → 调用 06-error-handler.md 返回 `CODE_PATH_NOT_FOUND` 错误

##### 1.3.4 进入代码目录绝对路径并生成 diff 文件
- **工作目录**: `{CODE_ROOT}/{code_path}`
- **命令**: 
  ```bash
  cd {CODE_ROOT}/{code_path}
  git add -N .
  git diff > {part_name}_diff.txt
  git reset
  ```
- **参数说明**:
  - `{CODE_ROOT}/{code_path}`: 代码绝对路径
  - `{part_name}`: 部件名
  - `git reset`: 恢复本地git记录
- **验证**: 检查 diff 文件是否生成成功
- **失败处理**: 调用 06-error-handler.md 返回 `GIT_DIFF_FAILED` 错误
- **注意，多部件名需按如下要求进行**: 
  - 预编译只进行一次，在第一个 part_name 生成diff文件时执行
  - 每个part_name 在自己的部件目录下生成独立的 diff 文件

##### 1.3.5 检查生成结果
- **操作**: 验证 diff 文件是否生成且非空
- **命令**: `wc -l {diff_file_path}`
- **判断**: 
  - 行数 > 0 → 生成成功
  - 行数 = 0 → 生成失败
- **失败处理**: 调用 06-error-handler.md 返回 `DIFF_FILE_EMPTY` 错误

#### 1.4 执行 local_build 编译产物

##### 构建编译命令
- **工作目录**: `{SKILL_DIR}/scripts/pr_local_coverage/local_build`
- **基础命令**: `python local_build.py {CODE_ROOT} {part_name} {diff_file}`
- **参数说明**:
  - `{CODE_ROOT}`: 代码根目录 (从传入参数获取)
  - `{part_name}`: 部件名称
  - `{diff_file}`: diff 文件路径 (从 入参 或 1.3 获取)
- **完整命令示例**:
  ```bash
  cd {SKILL_DIR}/scripts/pr_local_coverage/local_build
  chmod +x *
  python local_build.py /xxx/xxx/code ability_base /home/user/skill/scripts/pr_local_coverage/local_build/ability_base_diff.txt
  ```

##### 执行编译命令
- **工作目录**: `{SKILL_DIR}/scripts/pr_local_coverage/local_build`
- **超时**: 3小时 (根据编译规模调整)
- **执行**: 同步执行编译命令，等待自然完成
- **禁止**: 禁止主动中断或轮询检查命令状态
- **超时处理**: 使用 timeout 机制处理超时

#### 1.5 检查编译产物是否生成
- **检查路径**: `{CODE_ROOT}/out/coverage.tar.lz4`
- **验证内容**:
  1. 目录是否存在
  2. 编译产物是否存在
- **验证命令**: `ls -la {CODE_ROOT}/out/coverage.tar.lz4`
- **失败处理**: 
  - 编译产物缺失，将{SKILL_DIR}/scripts/pr_local_coverage/local_build/log 目录移动到{output}目录
  - 将 `{part_name}` 添加到 `failed_parts` 列表，记录错误 `LOCAL_BUILD_FAILED`
  - 继续执行下一个部件（不中断整体流程）

#### 2.1 检查参数,拼接完整命令（每个部件独立）
- **必要参数检查**:
  - `skill_dir`: {SKILL_DIR}
  - `code_root`: {CODE_ROOT}
  - `part_name`: 单个部件名称
  - `output_path`: 报告输出路径
- **参数验证**: 确保所有必要参数都已提供且有效
- **失败处理**: 参数缺失或无效 → 调用 06-error-handler.md 返回 `PARAMETER_INVALID` 错误

#### 2.2 执行覆盖率流程脚本（每个部件独立）
- **工作目录**: `{SKILL_DIR}/scripts/pr_local_coverage/pr_coverage/`
- **基础命令**: `python pr_coverage.py {CODE_ROOT} {part_name} {output_path}`
- **参数说明**:
  - `{CODE_ROOT}`: 代码根目录
  - `{part_name}`: 单个部件名称（不是列表）
  - `{output_path}`: 报告输出路径
- **完整命令示例**:
  ```bash
  cd {SKILL_DIR}/scripts/pr_local_coverage/pr_coverage/
  python pr_coverage.py /home/user/code ability_base /home/user/output
  ```
- **超时**: 2小时
- **执行**: 后台执行脚本，等待自然完成
- **禁止**: 禁止主动中断或轮询检查命令状态
- **日志记录**: 记录执行日志，便于问题排查
- **注意**: 此脚本待后续完善具体实现细节

#### 2.3 检查覆盖率报告是否生成（每个部件独立）
- **报告位置**: 定位最新的 `output_YYYYMMDDHHMM` 目录中的部件报告
  ```bash
  cd {SKILL_DIR}/scripts/pr_local_coverage/pr_coverage/output
  latest_output=$(ls -td output_* | head -1)
  report_path="${latest_output}/{part_name}/report/diff_html/"
  ```
- **检查内容**:
  1. report_path 目录是否存在
  2. index.html 文件是否存在
  3. 报告文件是否完整可读
- **检查命令**: `ls -la ${report_path}/index.html`
- **验证**: 尝试打开 HTML 文件，确认格式正确
- **失败处理**: 
  - 报告不存在或不完整 → 将 `{part_name}` 添加到 `failed_parts` 列表，记录错误 `PR_COVERAGE_FAILED`
  - 继续执行下一个部件（不中断整体流程）

#### 3.1 定位生成的增量覆盖率报告（每个部件独立）
- **定位方法**: 查找最新的 `output_YYYYMMDDHHMM` 目录
  ```bash
  cd {SKILL_DIR}/scripts/pr_local_coverage/pr_coverage/output
  latest_output=$(ls -td output_* | head -1)
  report_source="${latest_output}/{part_name}/report/diff_html/"
  ```
- **确认操作**: 
  1. 检查报告目录是否存在
  2. 检查关键文件是否存在 (index.html, css, js 等)
  3. 验证报告内容完整性
- **失败处理**: 
  - 报告未找到 → 将 `{part_name}` 添加到 `failed_parts` 列表，记录错误 `REPORT_NOT_FOUND`
  - 继续执行下一个部件（不中断整体流程）

#### 3.3 移动报告到 {OUTPUT_PATH}（每个部件独立）
- **目标路径**: `{OUTPUT_PATH}/{part_name}_incremental_coverage_report/`
- **命令**: 
  ```bash
  mv {report_source} {OUTPUT_PATH}/{part_name}_incremental_coverage_report/
  ```
- **验证**: 
  ```bash
  ls -la {OUTPUT_PATH}/{part_name}_incremental_coverage_report/
  ```
- **确认**: 检查报告文件是否成功移动到目标位置
- **成功处理**: 将 `{part_name}: {OUTPUT_PATH}/{part_name}_incremental_coverage_report/` 添加到 `success_parts` 列表
- **失败处理**: 
  - 移动失败 → 将 `{part_name}` 添加到 `failed_parts` 列表，记录错误 `REPORT_MOVE_FAILED`
  - 检查磁盘空间、目标目录权限、源路径是否存在
  - 继续执行下一个部件（不中断整体流程）

### [全局结果汇总]

#### 统计执行结果
- **成功数量**: `len(success_parts)`
- **失败数量**: `len(failed_parts)`

#### 生成报告路径列表（文本格式）
- **所有部件成功时**:
  ```
  ## 覆盖率报告生成完成
  
  成功生成的报告 (N个):
  - {part_name1}: {OUTPUT_PATH}/{part_name1}_incremental_coverage_report/
  - {part_name2}: {OUTPUT_PATH}/{part_name2}_incremental_coverage_report/
  ...
  ```
- **部分部件失败时**:
  ```
  ## 覆盖率报告生成完成（部分成功）
  
  成功生成的报告 (N个):
  - {part_name1}: {OUTPUT_PATH}/{part_name1}_incremental_coverage_report/
  - {part_name2}: {OUTPUT_PATH}/{part_name2}_incremental_coverage_report/
  ...
  
  执行失败的部件 (M个):
  - {part_name3}: {错误信息}
  - {part_name4}: {错误信息}
  ...
  ```
- **所有部件失败时**:
  ```
  ## 覆盖率报告生成失败
  
  执行失败的部件 (N个):
  - {part_name1}: {错误信息}
  - {part_name2}: {错误信息}
  ...
  ```

### [4] 恢复环境（所有部件执行完）

#### 4.1 清理临时编译产物
- **清理路径**: `{CODE_ROOT}/out/pr_coverage_out/`
- **命令**: 
  ```bash
  rm -rf {CODE_ROOT}/out/pr_coverage_out/
  ```
- **验证**: 
  ```bash
  ls -la {CODE_ROOT}/out/ | grep pr_coverage_out
  ```
- **失败处理**: 清理失败时记录日志，但不影响主流程

#### 4.2 清理临时覆盖率文件
- **清理路径**: `{SKILL_DIR}/scripts/pr_local_coverage/local_build/log/`
- **命令**: 
  ```bash
  rm -rf {SKILL_DIR}/scripts/pr_local_coverage/local_build/log/
  ```
- **验证**: 确认日志目录已清理
- **失败处理**: 清理失败时记录日志，但不影响主流程

#### 4.3 恢复工作目录
- **操作**: 切换回代码根目录
- **命令**: 
  ```bash
  cd {CODE_ROOT}
  ```
- **验证**: 
  ```bash
  pwd
  ```
- **确认**: 确认当前工作目录为 {CODE_ROOT}

### [5] 清理临时文件（所有部件执行完）

#### 5.1 删除编译临时文件
- **操作**: 删除临时编译过程中生成的文件
- **命令**: 
  ```bash
  find {CODE_ROOT}/out -name "*.tmp" -delete
  ```
- **验证**: 确认临时文件已删除
- **失败处理**: 删除失败时记录日志，但不影响主流程

#### 5.2 删除覆盖率临时文件
- **操作**: 删除覆盖率计算过程中的临时文件
- **命令**: 
  ```bash
  find {output_path} -name "*.tmp" -delete
  ```
- **验证**: 确认临时文件已删除
- **失败处理**: 删除失败时记录日志，但不影响主流程

#### 5.3 删除其他中间产物
- **操作**: 删除其他临时文件和目录
- **命令**: 
  ```bash
  find {SKILL_DIR}/scripts/pr_local_coverage -name "*.log" -delete
  ```
- **验证**: 确认临时文件已删除
- **失败处理**: 删除失败时记录日志，但不影响主流程

## 输出

### 单部件场景
- 报告路径: {OUTPUT_PATH}/{part_name}_incremental_coverage_report/index.html
- 增量覆盖率报告目录: {OUTPUT_PATH}/{part_name}_incremental_coverage_report/
- 报告内容包括:
  - 代码覆盖率详情
  - 增量变更覆盖率
  - 覆盖率统计图表
  - 未覆盖代码行标识

### 多部件场景
报告路径列表（文本格式）：
- {part_name1}: {OUTPUT_PATH}/{part_name1}_incremental_coverage_report/
- {part_name2}: {OUTPUT_PATH}/{part_name2}_incremental_coverage_report/
- ...

每个报告目录包含：
- 代码覆盖率详情
- 增量变更覆盖率
- 覆盖率统计图表
- 未覆盖代码行标识

### 执行结果汇总格式
所有部件成功时：
```
## 覆盖率报告生成完成

成功生成的报告 (N个):
- {part_name1}: {OUTPUT_PATH}/{part_name1}_incremental_coverage_report/
- {part_name2}: {OUTPUT_PATH}/{part_name2}_incremental_coverage_report/
...
```

部分部件失败时：
```
## 覆盖率报告生成完成（部分成功）

成功生成的报告 (N个):
- {part_name1}: {OUTPUT_PATH}/{part_name1}_incremental_coverage_report/
- {part_name2}: {OUTPUT_PATH}/{part_name2}_incremental_coverage_report/
...

执行失败的部件 (M个):
- {part_name3}: {错误信息}
- {part_name4}: {错误信息}
...
```

所有部件失败时：
```
## 覆盖率报告生成失败

执行失败的部件 (N个):
- {part_name1}: {错误信息}
- {part_name2}: {错误信息}
...
```

## 错误处理

### 错误类型及处理

| 错误代码 | 错误名称 | 触发条件 | 恢复策略 |
|---------|---------|---------|---------|
| `BUILD_GN_ONLY_FAILED` | 预编译失败 | build_system.sh --build-only-gn 执行失败 | 检查编译环境，清理缓存后重试 |
| `BUILD_CONFIG_NOT_FOUND` | 构建配置未找到 | 预编译后找不到构建配置 | 检查预编译结果 |
| `PART_PATH_NOT_FOUND` | 部件路径未找到 | parts_path_info.json 中找不到部件路径 | 检查部件名称拼写，确认部件存在 |
| `CODE_PATH_NOT_FOUND` | 代码路径未找到 | code_path 目录不存在 | 检查代码仓库结构 |
| `GIT_DIFF_FAILED` | Git diff 失败 | git diff 命令执行失败 | 检查 Git 仓库状态，确认在 Git 仓库中 |
| `DIFF_FILE_EMPTY` | diff 文件为空 | 生成的 diff 文件内容为空 | 检查代码变更，确认有实质性修改 |
| `LOCAL_BUILD_FAILED` | 本地编译失败 | local_build 编译产物未生成 | 检查编译日志，修复编译错误 |
| `PARAMETER_INVALID` | 参数无效 | 必要参数缺失或格式错误 | 检查输入参数，重新提供正确参数 |
| `PR_COVERAGE_FAILED` | 覆盖率计算失败 | pr_coverage 脚本执行失败 | 检查脚本日志，修复执行环境 |
| `REPORT_NOT_FOUND` | 报告未找到 | 覆盖率报告未生成 | 检查覆盖率计算过程 |
| `OUTPUT_DIR_CREATE_FAILED` | 输出目录创建失败 | 无法创建输出目录 | 检查目录权限，手动创建目录 |
| `REPORT_MOVE_FAILED` | 报告移动失败 | 无法移动报告到目标目录 | 检查磁盘空间和目标目录权限 |
| `ALL_PARTS_FAILED` | 所有部件失败 | 所有部件执行失败 | 检查环境配置和依赖 |

### 错误恢复策略

1. **单部件失败处理**: 单个部件失败时记录错误信息，继续执行下一个部件，不中断整体流程
2. **所有部件失败处理**: 所有部件都失败时返回 `ALL_PARTS_FAILED` 错误
3. **部分成功处理**: 部分部件成功时返回汇总结果，标记成功和失败的部件
4. **环境恢复**: 所有部件执行完后统一清理临时文件、恢复工作目录
5. **日志记录**: 记录详细的错误日志和上下文信息，便于问题排查
6. **用户提示**: 提供用户友好的错误信息和解决方案

### 多部件执行失败示例

**场景1: 部分部件失败**
```
执行: ability_base → 成功
执行: ability_runtime → 失败 (LOCAL_BUILD_FAILED)
执行: ability_tools → 成功

结果: 
成功生成的报告 (2个):
- ability_base: {OUTPUT_PATH}/ability_base_incremental_coverage_report/
- ability_tools: {OUTPUT_PATH}/ability_tools_incremental_coverage_report/

执行失败的部件 (1个):
- ability_runtime: LOCAL_BUILD_FAILED
```

**场景2: 所有部件失败**
```
执行: ability_base → 失败 (PR_COVERAGE_FAILED)
执行: ability_runtime → 失败 (LOCAL_BUILD_FAILED)

结果: 
## 覆盖率报告生成失败

执行失败的部件 (2个):
- ability_base: PR_COVERAGE_FAILED
- ability_runtime: LOCAL_BUILD_FAILED
```

## 注意事项

### diff 文件处理注意事项

1. **路径处理**: diff 文件路径使用绝对路径，避免相对路径问题
2. **编码格式**: diff 文件必须是 UTF-8 编码，避免中文乱码
3. **文件大小**: 确保 diff 文件不为空，否则跳过编译
4. **独立生成**: 每个部件在各自代码目录下生成独立的 diff 文件
5. **预编译优化**: 预编译只执行一次，在第一个部件执行时进行

### 编译注意事项

1. **超时设置**: 编译超时设置为 3 小时，根据实际编译规模调整
2. **依次执行**: 多部件时依次编译，避免并发冲突
3. **产物验证**: 每次编译后验证产物完整性，确保后续流程正常
4. **缓存使用**: 启用 ccache 加速编译，提高编译效率
5. **失败处理**: 单个部件编译失败时记录日志，继续执行下一个部件

### 超时处理注意事项

1. **预编译超时**: 30 分钟，生成构建配置（只执行一次）
2. **diff 生成超时**: 5 分钟，Git diff 操作
3. **编译超时**: 3 小时，完整的编译流程
4. **覆盖率计算超时**: 2 小时，生成覆盖率报告
5. **自然等待**: 所有命令必须等待自然完成，禁止主动中断

### 清理策略注意事项

1. **统一清理**: 按照方案B，所有部件执行完后再统一清理
2. **失败容忍**: 清理失败时记录日志，但不影响主流程
3. **路径验证**: 清理前验证路径存在，避免删除错误文件
4. **权限检查**: 确保有足够的权限执行删除操作

### 多部件处理注意事项

1. **独立执行**: 每个部件独立执行完整的覆盖率生成流程
2. **执行顺序**: 依次执行每个部件，避免并发冲突
3. **失败容忍**: 单个部件失败不影响其他部件执行
4. **结果汇总**: 所有部件执行完后统一汇总结果
5. **报告命名**: 使用 `{part_name}_incremental_coverage_report` 避免冲突
6. **预编译优化**: 预编译只在第一个部件时执行一次
7. **清理策略**: 所有部件执行完后再统一清理临时文件

### 部件级别限制

1. **不支持子系统**: 增量覆盖率只支持部件级别，不支持子系统级别
2. **必需参数**: part_name 必须提供，不能为空
3. **多部件支持**: 支持多个部件同时计算增量覆盖率
4. **部件验证**: 确保部件名称在项目中存在

### 路径处理注意事项

1. **占位符使用**: 严格使用 {SKILL_DIR}、{CODE_ROOT} 等占位符
2. **路径分隔符**: 使用 `/` 作为路径分隔符，避免 Windows 路径问题
3. **路径验证**: 所有路径在使用前验证存在性和可访问性
4. **相对路径**: 避免使用相对路径，使用绝对路径确保一致性

### pr_coverage 执行注意事项

1. **单部件执行**: 每个部件独立执行 pr_coverage 脚本
2. **参数传递**: 只传入单个部件名，不传入部件列表
3. **output目录**: 确保执行前 output 目录为空，避免路径冲突
4. **报告定位**: 通过查找最新的 `output_YYYYMMDDHHMM` 目录定位报告
5. **报告结构**: 报告路径为 `output_YYYYMMDDHHMM/{part_name}/report/diff_html/`

### 报告移动注意事项

1. **独立目录**: 每个部件报告移动到独立的 `{part_name}_incremental_coverage_report` 目录
2. **路径验证**: 移动前验证源路径和目标路径
3. **磁盘空间**: 检查目标目录磁盘空间
4. **权限检查**: 确保有足够的权限执行移动操作