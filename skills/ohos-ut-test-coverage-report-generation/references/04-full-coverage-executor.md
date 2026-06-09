# 全量覆盖率执行模块

## 功能

执行全量覆盖率测试流程，支持针对 子系统、 部件、 模块、 测试套或测试用例生成覆盖率报告。 本模块是 AI 执行指南，提供详细的、可执行的步骤让 AI 自主完成全量覆盖率流程。


## Anti-Patterns - 绝对禁止事项

NEVER 做以下操作，否则会导致测试无法编译、运行：

| 禁止项                                          | 原因                                                | 正确做法                                            |
| -------------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| **NEVER 自由修改测试命令参数** | 必须严格按入参拼接命令            | 禁止添加、修改或省略任何命令参数，严格按照用户输入和规则构建 |
| **NEVER 中断或轮询长时间运行的命令**    | 必须使用timeout并等待自然完成 | 禁止主动中断或轮询检查命令状态，让timeout机制处理超时    |



## 执行流程

```
读取输入
  ↓
[1] 修改 user_config.xml 配置文件
  ├── 1.1 读取 {CODE_ROOT}/test/testfwk/developer_test/user_config.xml 文件
  ├── 1.2 更新设备信息(ip、port、sn)，保存修改
  └── 1.3 检查修改结果，如果修改失败 → 调用 06-error-handler.md 返回 CONFIG_MODIFY_FAILED 错误
  ↓
[2] 检查是否需要编译
  ├── 2.1 如果 skip_compiler = true → 跳转到 `3.3 检查 gcno 文件是否生成`
  └── 2.2 如果 skip_compiler = false → 继续
  ↓
[3] 执行编译流程
  ├── 3.1 预编译代码
  ├── 3.2 进入 `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment`目录， 执行 build_before_generate.py
  │  └── 如果执行失败 → 调用 06-error-handler.md 返回 BUILD_BEFORE_GENERATE_FAILED 错误
   ├── 3.3 编译用例
   │  ├── 3.3.1 构建编译命令
   │  ├── 3.3.2 执行编译命令（设置超时时间2小时）
   │  └── 3.3.3 验证编译结果
   │     ├── 如果编译失败 → 执行以下错误诊断和恢复流程：
   │     │   1. **分析错误类型**:
   │     │      ```bash
   │     │      # 查看编译日志最后100行
   │     │      tail -100 {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log
   │     │      
   │     │      # 搜索错误信息
   │     │      grep -i "error:" {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log | head -20
   │     │      ```
   │     │   2. **判断错误原因**:
   │     │      - **磁盘空间不足**: 检查 `df -h`，如果 <10GB 可用空间 → 清理空间后重试
   │     │      - **内存不足**: 检查 `free -h`，如果可用内存 <4GB → 增加 swap 或减少并发
   │     │      - **语法错误**: 检查源代码，修复语法错误
   │     │      - **依赖缺失**: 检查编译日志，安装缺失的依赖
   │     │      - **权限问题**: 检查文件权限，设置正确的权限
   │     │   3. **执行恢复**:
   │     │      ```bash
   │     │      # 清理编译缓存
   │     │      rm -rf {CODE_ROOT}/out/
   │     │      
   │     │      # 重新执行编译命令
   │     │      [重新执行 3.3.2 的编译命令]
   │     │      ```
   │     │   4. **如果仍然失败**:
   │     │      → 调用 06-error-handler.md 返回 `COMPILATION_FAILED` 错误
   │     │      → 提供编译日志路径供用户排查
  └── 3.4 检查 gcno 文件是否生成
     ├── 3.4.1 检查是否执行了 build_before_generate.py 脚本
     ├── 3.4.2 执行 {SKILL_DIR}/scripts/check_gcno_files.py 脚本,检查是否插桩成功
     └── 如果未生成 → 调用 06-error-handler.md 返回 GCNO_FILES_NOT_FOUND 错误
  ↓
[4] 启动框架并执行命令
  ├── 4.1 构建 run -t 测试命令
  │  ├── 4.1.1 根据输入参数构建命令
  │  └── 4.1.2 构建完整命令
  ├── 4.2 接受 4.1 传入的完整测试命令，在后台执行测试 (设置超时时间2小时)
  └── 4.3 检查覆盖率报告是否生成，如果不存在覆盖率报告 → 调用 06-error-handler.md 返回 REPORT_NOT_FOUND 错误
  ↓
[5] 执行 after_lcov_branch.py
  ├── 5.1 进入 `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment`目录
  ├── 5.2 检查是否需要执行 after_lcov_branch.py，如果需要则执行 after_lcov_branch.py
  └── 5.3 如果需要执行但是执行失败 → 调用 06-error-handler.md 返回 AFTER_LCOV_FAILED 错误
  ↓
[6] 移动报告到输出目录
  ├── 6.1 定位生成的覆盖率报告
  ├── 6.2 移动报告到 {OUTPUT_PATH}
  └── 6.3 如果移动失败 → 调用 06-error-handler.md 返回 REPORT_MOVE_FAILED 错误
  ↓
[7] 解析报告
  ↓
[8] 清理环境
  ├── 8.1 删除原始测试报告目录
  ├── 8.2 清理编译产物(可选，默认不删除) 
  └── 8.3 验证删除结果 
  ↓
结束
```

## 传入参数

从 01-config-checker.md 接收（完整配置）：
- `skill_dir`: {SKILL_DIR}
- `code_root`: {CODE_ROOT}
- `taskType`: 任务类型
- `userInput.parameters`: 用户参数
  - `part_name_list`: 部件名称列表（必需）
  - `module`: 模块名称 (可选)
  - `testsuite`: 测试套名称 (可选)
  - `testcase`: 测试用例名称 (可选)
  - `skip_compiler`: 是否跳过编译 (默认false)
  - `output_path`: 报告输出路径
- `config.deviceInfo`: 设备配置信息（完整）
  - `ip`: hdc 连接 IP
  - `port`: hdc 连接端口
  - `sn`: 设备序列号
  - `connected`: 设备连接状态
  - `validated`: 验证状态

## 使用脚本

- `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/build_before_generate.py` - 编译前准备
- `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/after_lcov_branch.py` - 恢复源码
- `{SKILL_DIR}/scripts/parse_coverage_report.py` - 解析报告
- `{SKILL_DIR}/scripts/check_gcno_files.py` - 检查是否插桩成功

## 详细步骤说明

### [1] 修改 user_config.xml 配置文件

#### 1.1 读取配置文件
- **路径**: `{CODE_ROOT}/test/testfwk/developer_test/user_config.xml`
- **操作**: 使用 JSON 解析器读取配置文件
- **备份**: 在修改前创建备份文件 `user_config.xml.backup`

#### 1.2 更新设备信息
- **更新字段**: 在user_config.xml中查找以下类似代码段
- **步骤**:
  1. 找到 `<device type="usb-hdc" label="ohos">` 节点
  2. 更新 `<info>`标签的属性：
      - `ip`: hdc 连接 IP
      - `port`: hdc 连接端口
      - `sn`: 设备序列号
  ```xml
  <environment>
    <!-- reserved field, configure devices that support HDC connection -->
    <device type="usb-hdc" label="ohos">
      <info ip="" port="" sn="" alias="" />
    </device>
  ```
- **验证**: 确保所有必需的设备信息都已填写
- **保存**: 将修改后的配置保存到原文件

#### 1.3 检查修改结果
- **验证**: 重新读取文件，验证修改是否成功
- **失败处理**: 如果修改失败，调用 06-error-handler.md 返回 `CONFIG_MODIFY_FAILED` 错误

### [2] 检查是否需要编译

#### 2.1 判断 skip_compiler 参数
- **如果 skip_compiler = true**: 跳转到 [3.4] 检查 gcno 文件是否生成
- **如果 skip_compiler = false**: 继续执行 [3] 编译流程

### [3] 执行编译流程

#### 3.1 执行预编译
- **检查是否已进行预编译**: 检查编译产物 `{CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build_configs`是否存在
  - **不存在则执行下列步骤**:
    1. 执行下列命令，进行预编译
      ```bash
      cd {CODE_ROOT}
      ./build_system.sh --abi-type generic_generic_arm_64only --device-type general_all_phone_standard --ccache --build-target hmos_make_test --build-only-gn --build-variant root
      ```

    2. 检查编译是否成功,失败则中断流程 → 调用06-error-handler.md返回`BUILD_GN_ONLY_FAILED`错误;
    3. 再次检查编译产物,失败则中断流程 → 调用06-error-handler.md返回`BUILD_CONFIG_NOT_FOUND`错误;
  - **存在则继续后续流程**:
#### 3.2 执行 build_before_generate.py
- **工作目录**: `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment`
- **命令**
  ```bash
  printf "run -tp {part1} {part2} ... \nexit\n" | python build_before_generate.py
  ```
- **参数说明**: `{part1} {part2} ... ` 用户传入的部件名列表(从`part_name_list或part获取`)
- **示例**: 
  ```bash
  printf "run -tp ability_base ability_runtime ability_tools \nexit\n" | python build_before_generate.py
  ```
- **验证结果**: 编译前准备工作，设置编译环境
- **超时**: 5分钟
- **失败处理**: 如果执行失败，调用 06-error-handler.md 返回 `BUILD_BEFORE_GENERATE_FAILED` 错误

#### 3.3 编译用例

##### 3.3.1 构建编译命令
**基础命令**: `./build_system.sh --abi-type generic_generic_arm_64only --device-type general_all_phone_standard --ccache --build-target {build_target}  --build-variant root --gn-args use_clang_coverage=true` (命令参数不可缺失)

**必需参数**:
- `--abi-type`: 架构类型，强制选择 `generic_generic_arm_64only`
- `--device-type`: 设备类型，强制选择 `general_all_phone_standard`
- `--ccache`: 启用编译缓存
- `--build-target`: 构建目标,需要按如下步骤解析：
  1. 解析用户传输的part_name: 根据传入的参数，从part或part_name_list解析出part_name列表;
  2. 解析part_name列表对应的编译目标列表：根据part_name列表，从预编译结果中解析出 `{build_target}`;
    -**步骤**：
      1. 读取预编译生成的 `{CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build_configs/parts_info/parts_targets.json`;
      2. 对于part_name列表的每一个参数:
        - 在 parts_targets.json 中查找对应的 part_name
        - 读取part_name对应的test字段的值
        - 从读取的值中提取编译目标: 去掉后缀 `(//build/toolchain/ohos:ohos_clang_arm64)` 和前缀 `//`
        - 示例： parts_targets.json中 `ability_base`的格式入下:

        ```json
          "ability_base": {
            "inner_kits": "//out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_base:ability_base_inner_kits(//build/toolchain/ohos:ohos_clang_arm64)",
            "part": "//out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_base:ability_base(//build/toolchain/ohos:ohos_clang_arm64)",,
            "test": "//out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_base:ability_base_test(//build/toolchain/ohos:ohos_clang_arm64)",
          }
        ```

        提前后的编译目标则为 `out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_base:ability_base_test`
        - 如果不存在test字段，则省略这个part_name,如果都不存在，则中断流程，调用 06-error-handler.md 返回 `ALL_PART_NOT_TEST_BUILD_TARGETS` 错误
        - 如果存在多个part_name,将所有解析出的编译目标用空格拼接
          -示例：
            - part_name列表为 ability_base,ability_runtime;
            - 则 `{build_target}` 为 `out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_base:ability_base_test out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_runtime:ability_runtime_test`
- `--gn-args use_clang_coverage=true`: 启动覆盖率插桩

**完整命令示例**:
```bash
./build_system.sh --abi-type generic_generic_arm_64only --device-type general_all_phone_standard --ccache --build-target out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_base:ability_base_test out/generic_generic_arm_64only/general_all_phone_standard/build_configs/ability/ability_runtime:ability_runtime_test  --build-variant root --gn-args use_clang_coverage=true
```

**命令拼接规则**:
1. 严格基于用户输入参数构建
2. 不得添加、修改或省略任何参数
3. 参数顺序不影响功能，但建议按推荐顺序

##### 3.3.2 执行编译命令
- **工作目录**: `{CODE_ROOT}`
- **超时**: 3小时（根据编译规模调整）
- **执行**: 同步执行编译命令，等待自然完成
- **禁止**: 禁止主动中断或轮询检查命令状态，让 timeout 机制自然处理超时
- **超时处理**: 使用 timeout 机制处理超时
- **目的**: 确保编译过程完整执行，避免人为中断导致的不完整状态

##### 3.3.3 验证编译结果
- **检查编译日志**: 读取编译日志(路径为 `{CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log`)的最后100行内容，如果存在报错则走失败处理
- **检查编译产物**: 检查测试用例是否编译成功
- **失败处理**: 如果编译失败，中断流程，调用 06-error-handler.md 返回 `COMPILATION_FAILED` 错误

#### 3.4 检查 gcno 文件是否生成
- **操作**: 验证编译产物是否存在覆盖率数据文件 (按部件级细化检查)
- **步骤**: 

#### 3.4.1 **检查是否执行了 build_before_generate.py 脚本**
    - **检查方式**:
      - 查询 `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/part_config.json`是否存在
      - 存在则继续流程
      - 不存在则中断流程，调用 06-error-handler.md 返回 `LCOV_EXCL_BR_LINE_NOT_FOUND` 错误
    - **目的**: 确保编译前准备工作已完成，源码已正确标记
  3.4.2 **执行 {SKILL_DIR}/scripts/check_gcno_files.py 脚本,检查是否插桩成功**
    - **执行命令**
      ```bash
      cd {SKILL_DIR}/scripts && python3 check_gcno_files.py --code_root {CODE_ROOT} --part {part_name_list}
      ```
    - 判断执行结果，失败则中断流程，调用 06-error-handler.md 返回 `COVERAGE_DATA_NOT_FOUND` 错误

### [4] 启动框架并执行命令

#### 4.1 构建 run -t 测试命令

##### 4.1.1 根据输入参数构建命令
**基础命令格式**: `run -t UT -tp <part> -tm <module> -ts <testsuite> -tc <testcase> -cov coverage`

- **参数说明**:
  -  `-t UT `: 测试类型，必填，必选UT;
  -  `-tp <part> `: 部件名，必填，多个部件时部件名中间用空格隔开 即 `-tp part1 part2`;
  -  `-tm <module>`: 模块名，可选，填写入参{module};
  -  `-ts <testsuite>`: 测试套名，可选，填写入参{testsuite};
  -  `-tc <testcase>`: 测试用例名，可选，填写入参{testcase};
  -  `-cov coverage`: 开启覆盖率模式，必填，**不可省略**;

##### 4.1.2 构建完整命令
**操作**: 将cd命令、产品形态序号、run命令拼接成完整命令，准备传递给包装脚本
**命令格式**: 
```base
  cd {CODE_ROOT}/test/testfwk/developer_test && printf \"2\\n{test_command}\\nquit\\n\" | ./start.sh
```
**参数说明**:
  - `{CODE_ROOT}`: 代码根目录
  - `2`: 产品形态选择
  - `test_command`: 4.1.1中拼接的 run -t 命令
  - `quit`: 退出命令行
  - 注意： 命令中的 `\\n`表示换行符, `\"` 表示转义的双引号



#### 4.2 执行测试
- **执行命令**:4.1创建的 FULL_COMMAND
- **注意事项**:必须设置超时时间(2小时),中间不能主动中断
- **后台执行**: 使用后台进程执行测试
- **禁止**: 禁止主动中断或轮询检查命令状态，让 timeout 机制自然处理超时
- **错误处理**: 测试执行失败,直接执行[5] 执行 after_lcov_branch.py，执行完成[5] 执行 after_lcov_branch.py后直接中断流程，调用 06-error-handler.md 返回 `TEST_EXECUTION_FAILED` 错误
- **目的**: 确保测试完整执行，获取准确的覆盖率数据

#### 4.3 检查覆盖率报告是否生成
- **报告位置**: 
  - 代码覆盖率主页面文件位置：`{CODE_ROOT}/test/testfwk/developer_test/local_coverage/code_coverage/result/coverage/reports/cxx/html/index.html`
  - 接口覆盖率主页面文件位置：`{CODE_ROOT}/test/testfwk/developer_test/local_coverage/interface_coverage/result/coverage/interface_kits/ohos_interfaceCoverage.html`
- **检查内容**: 查找两个报告是否存在
- **失败处理**: 如果都不存在，调用 06-error-handler.md 返回 `REPORT_NOT_FOUND` 错误

### [5] 执行 after_lcov_branch.py

#### 5.1 进入工作目录
- **目录**: `{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment`

#### 5.2 检查是否需要执行
- **检查条件**: 检查`{CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/part_config.json`是否存在
- **判断**: 如果存在则需要执行，否则不执行

#### 5.3 执行恢复脚本
- **命令**: `python after_lcov_branch.py`
- **功能**: 恢复源码文件，清理覆盖率编译标记
- **超时**: 5分钟
- **失败处理**: 如果执行失败，调用 06-error-handler.md 返回 `AFTER_LCOV_FAILED` 错误

### [6] 移动报告到输出目录

#### 6.1 定位生成的覆盖率报告
- **源路径**: 
  - 代码覆盖率报告目录：`{CODE_ROOT}/test/testfwk/developer_test/local_coverage/code_coverage/result/`
  - 接口覆盖率报告目录：`{CODE_ROOT}/test/testfwk/developer_test/local_coverage/interface_coverage/result/`
- **确认**: 验证报告文件存在

#### 6.2 移动报告
- **目标路径**: `{output_path}`
- **操作**: 创建目标目录（如果不存在），移动报告文件
- **命令**:
  ```bash
  # 移动代码覆盖率报告
  mv {CODE_ROOT}/test/testfwk/developer_test/local_coverage/code_coverage/result/ {output_path}/code_coverage
  # 移动接口覆盖率报告
  cp -r {CODE_ROOT}/test/testfwk/developer_test/local_coverage/interface_coverage/result/ {output_path}/interface_coverage
  ```
- **验证**: 确认报告已成功移动到目标位置

#### 6.3 处理移动失败
- **失败处理**: 如果移动失败，检查原因，尝试解决，无法解决时中断流程,调用 06-error-handler.md 返回 `REPORT_MOVE_FAILED` 错误
- **原因检查**: 检查磁盘空间、目标目录权限

### [7] 解析报告
- **操作**：使用 parse_coverage_report.py 解析报告
- **脚本路径**: `{SKILL_DIR}/scripts/parse_coverage_report.py`
- **命令**:

  ```bash
  cd {SKILL_DIR}/scripts
  python parse_coverage_report.py --output_path {output_path} --report_type all
  ret=$?
  ```

-**将报告解析结果和报告地址提供给用户**
-**错误处理**: 如果解析失败，则只告诉用户报告地址
- **功能**: 解析 HTML 报告，提取覆盖率数据

### [8] 清理环境

#### 8.1 删除原始测试报告目录
- **目录**: `{CODE_ROOT}/test/testfwk/developer_test/reports`
- **操作**: 删除原始测试用例报告目录
- **命令**: `rm -rf {CODE_ROOT}/test/testfwk/developer_test/reports`

#### 8.2 清理编译产物(可选，默认不删除，根据用户说明确认是否删除)
- **操作**: 清理编译产物
- **命令**: `rm -rf {CODE_ROOT}/out/`

#### 8.3 验证是否清理成功 (可选)
- **条件**: 根据用户需求决定是否清理
- **清理内容**: 编译生成的二进制文件、中间文件
- **建议**: 通常保留编译产物，方便后续调试


## 错误处理

### 错误类型及处理

| 错误代码 | 错误名称 | 触发条件 | 恢复策略 |
|---------|---------|---------|---------|
| `CONFIG_MODIFY_FAILED` | 配置文件修改失败 | 无法修改或保存 user_config.xml | 恢复备份文件 |
| `BUILD_BEFORE_GENERATE_FAILED` | 编译前准备失败 | build_before_generate.py 执行失败 | 尝试恢复环境 |
| `COMPILATION_FAILED` | 编译失败 | 编译命令返回非0 | 记录日志，清理临时文件 |
| `GCNO_FILES_NOT_FOUND` | gcno文件未找到 | 编译后未生成gcno文件 | 检查编译配置 |
| `TEST_EXECUTION_FAILED` | 测试执行失败 | 测试命令执行失败 | 检查设备连接 |
| `REPORT_NOT_FOUND` | 报告未找到 | 测试后未生成覆盖率报告 | 检查测试输出 |
| `AFTER_LCOV_FAILED` | 后处理失败 | after_lcov_branch.py 执行失败 | 尝试手动恢复源码 |
| `REPORT_MOVE_FAILED` | 报告移动失败 | 无法移动报告到输出目录 | 检查目标目录权限 |

### 错误恢复策略

1. **配置文件恢复**: 任何修改配置文件前先备份，失败时恢复备份
2. **环境清理**: 失败时尝试清理临时文件、恢复环境
3. **日志记录**: 记录详细的错误日志和上下文信息
4. **用户提示**: 提供用户友好的错误信息和解决方案

## 注意事项

### 命令构建规则

1. **严格按入参**: 严格基于用户输入和规则构建命令
2. **禁止随意修改**: 禁止添加、修改或省略任何命令参数
3. **参数验证**: 验证所有参数的格式和有效性
4. **特殊字符处理**: 正确处理参数中的特殊字符

### 超时处理

1. **编译超时**: 设置合理的超时时间（1-2小时）
2. **测试超时**: 设置测试执行超时（2小时）
3. **自然等待**: 等待命令自然完成，禁止主动中断

### 设备连接

1. **连接验证**: 执行前验证设备连接
2. **连接监控**: 执行过程中监控连接状态
3. **重连机制**: 连接断开时尝试重连

### 资源管理

1. **磁盘空间**: 执行前检查可用磁盘空间
2. **内存使用**: 监控内存使用情况
3. **进程管理**: 清理僵尸进程

### 路径处理

1. **路径验证**: 验证所有路径的正确性和可访问性
2. **路径转换**: 正确处理相对路径和绝对路径
3. **路径分隔符**: 使用正确的路径分隔符（`/`）

## 参数构建规则总结

### run.py 命令构建

```python
# 基础命令
command_parts = ["python", "run.py"]

# 添加部件参数（必需）
for part in part_name_list:
    command_parts.extend(["-t", part])

# 添加模块参数（可选）
if module:
    command_parts.extend(["-m", module])

# 添加测试套参数（可选）
if testsuite:
    command_parts.extend(["-ts", testsuite])

# 添加测试用例参数（可选）
if testcase:
    command_parts.extend(["-tc", testcase])

# 构建完整命令
command = " ".join(command_parts)
```

### build_system.sh 命令构建

```python
# 基础命令
command_parts = [
    "./build_system.sh",
    "--abi-type", "generic_generic_arm_64only",
    "--device-type", "general_all_phone_standard",
    "--ccache",
    "--build-target", "hmos_make_test"
]

# 添加部件参数
for part in part_name_list:
    command_parts.extend(["--build-part", part])

# 添加模块参数（可选）
if module:
    command_parts.extend(["--build-module", module])

# 添加测试套参数（可选）
if testsuite:
    command_parts.extend(["--build-testsuite", testsuite])

# 添加测试用例参数（可选）
if testcase:
    command_parts.extend(["--build-testcase", testcase])

# 构建完整命令
command = " ".join(command_parts)
```