# 错误处理模块

## 功能

统一处理执行过程中出现的所有错误，提供用户友好的错误信息和解决方案。

## 常见场景决策树

| 场景 | 诊断步骤 | 主要工具 | Fallback | 触发条件 |
|------|---------|---------|----------|---------|
| 编译超时 | 1. 检查out/目录大小<br>2. 查看hb build日志 | bash tail -f | 清理后重试<br>跳过已编译部件 | 命令执行>2小时无输出 |
| 设备断连 | 1. hdc list targets<br>2. 检查设备电源 | bash hdc | 重新连接设备<br>降低并行度 | hdc命令超时 |
| 磁盘空间不足 | 1. df -h检查<br>2. du -sh out/定位占用 | bash df/du | 清理out/或旧报告<br>降低增量范围 | df显示<10GB可用 |

## 错误分类

### 配置错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| CONFIG_FILE_NOT_FOUND | 配置文件未找到 | user-config.json 不存在 | 检查 {SKILL_DIR}/config/user-config.json 是否存在 |
| INVALID_CONFIG_FORMAT | 配置格式错误 | user-config.json 格式不正确 | 检查 JSON 格式是否正确 |
| MISSING_CODE_ROOT | 缺少 code_root | user-config.json 中缺少 code_root 字段 | 添加 code_root 字段到配置文件 |
| INVALID_CODE_ROOT | code_root 无效 | code_root 目录不存在或不可访问 | 检查 code_root 路径是否正确且可访问 |
| PROJECT_STRUCTURE_ERROR | 项目结构错误 | 项目结构不完整 | 检查项目目录结构是否完整 |
| LCOV_CONFIG_MODIFY_FAILED | lcov配置修改失败 | 修改lcovrc配置失败 | 检查/etc/lcovrc文件权限 |
| CONFIG_MODIFY_FAILED | 配置修改失败 | 无法修改配置文件 | 恢复备份文件，检查文件权限 |

### 参数错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| PARAMETER_INVALID | 参数无效 | 必要参数缺失或格式错误 | 检查输入参数，重新提供正确参数 |
| INVALID_TASK_TYPE | 任务类型无效 | 无法识别任务类型 | 检查输入中的覆盖率类型关键词 |
| MISSING_TARGET_PARAMETER | 缺少目标参数 | 缺少必需的目标参数 | 提供子系统或部件参数 |
| MISSING_PART_FOR_INCREMENTAL | 增量模式缺少部件 | 增量覆盖率缺少部件参数 | 提供部件名称 |
| INCREMENTAL_NOT_SUPPORT_SUBSYSTEM | 增量不支持子系统 | 增量覆盖率不支持子系统级别 | 直接提供部件名称 |
| INVALID_PART_NAME | 部件名称无效 | 部件名称格式不正确 | 检查部件名称拼写 |
| SUBSYSTEM_NOT_FOUND | 子系统未找到 | 找不到指定的子系统 | 检查子系统名称拼写 |

### 环境错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| OS_NOT_SUPPORTED | 操作系统不支持 | 当前不是 Linux 系统 | 请在 Linux 系统上运行此工具 |
| PYTHON_NOT_INSTALLED | Python 未安装 | 系统未安装 Python | 安装 Python 3.8 或更高版本 |
| PYTHON_VERSION_LOW | Python 版本过低 | Python 版本低于 3.8 | 升级到 Python 3.8 或更高版本 |
| HDC_NOT_INSTALLED | hdc 未安装 | hdc 工具未安装 | 安装 hdc 工具 |
| GCC_NOT_INSTALLED | gcc 未安装 | gcc 编译器未安装 | 安装 gcc 编译器 |
| GPP_NOT_INSTALLED | g++ 未安装 | g++ 编译器未安装 | 安装 g++ 编译器 |
| LCOV_NOT_INSTALLED | lcov 未安装 | lcov 工具未安装 | 安装 lcov 工具 |
| GENHTML_NOT_INSTALLED | genhtml 未安装 | genhtml 工具未安装 | 安装 genhtml 工具 |
| GIT_NOT_INSTALLED | git 未安装 | git 工具未安装 | 安装 git 工具 |
| ADDLCOV_NOT_FOUND | addlcov 未找到 | addlcov 工具未找到 | 检查 {SKILL_DIR}/scripts/addlcov |
| INSUFFICIENT_DISK_SPACE | 磁盘空间不足 | 输出目录磁盘空间不足 | 清理磁盘空间或更换输出路径 |
| PERMISSION_DENIED | 权限不足 | 缺少必要的文件或目录权限 | 检查并设置正确的权限 |
| PROJECT_ROOT_NOT_FOUND | 项目根目录未找到 | 找不到项目根目录 | 检查 CODE_ROOT 配置 |
 | DEVICE_NOT_FOUND | 设备未找到 | hdc 设备未找到 | 检查设备连接和 hdc 配置 |
 | MULTIPLE_DEVICES_FOUND | 多设备连接 | 检测到多个设备 | 在 user-config.json 中配置 ip+port 或 sn 指定具体设备 |
 | DEVICE_CONNECTION_FAILED | 设备连接失败 | 设备连接失败 | 检查设备连接和 hdc 配置 |

### 依赖错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| SYSTEM_DEPENDENCY_INSTALL_FAILED | 系统依赖安装失败 | 系统依赖安装失败 | 检查网络连接和包管理器，重试安装 |
| PYTHON_DEPENDENCY_INSTALL_FAILED | Python 依赖安装失败 | Python 包安装失败 | 检查 pip 配置和网络连接，重试安装 |
| PIP_INSTALL_FAILED | pip安装失败 | pip包安装失败 | 检查pip配置和网络连接，重试安装 |
| PIP_NOT_AVAILABLE | pip不可用 | pip工具不可用 | 重新安装pip |
| PIP_NOT_INSTALLED | pip未安装 | pip未安装 | 安装pip工具 |
| PACKAGE_MANAGER_NOT_FOUND | 包管理器未找到 | 找不到包管理器 | 检查系统包管理器 |
| CONFLICT_ERROR | 依赖冲突 | 依赖版本冲突 | 解决依赖冲突问题 |
| NETWORK_ERROR | 网络错误 | 网络连接失败 | 检查网络连接 |

### Git 错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| GIT_DIFF_FAILED | Git diff 失败 | git diff 命令执行失败 | 检查 Git 仓库状态，确认在 Git 仓库中 |
| DIFF_FILE_EMPTY | diff 文件为空 | 生成的 diff 文件内容为空 | 检查代码变更，确认有实质性修改 |

### 预编译错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| PRECOMPILATION_FAILED | 预编译失败 | 预编译执行失败 | 检查编译环境，清理缓存后重试 |
| BUILD_GN_ONLY_FAILED | GN预编译失败 | build_system.sh --build-only-gn 执行失败 | 检查编译环境，清理缓存后重试 |
| BUILD_CONFIG_NOT_FOUND | 构建配置未找到 | 预编译后找不到构建配置 | 检查预编译结果 |

### 编译错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| BUILD_BEFORE_GENERATE_FAILED | 编译前准备失败 | build_before_generate.py 执行失败 | 检查日志文件，确认编译环境配置 |
| COMPILATION_FAILED | 编译失败 | 用例编译失败 | 检查编译日志，修复编译错误 |
| LCOV_EXCL_BR_LINE_NOT_FOUND | lcov标记未找到 | 未找到lcov分支覆盖率标记 | 检查是否执行了build_before_generate.py |
| COVERAGE_DATA_NOT_FOUND | 覆盖率数据未找到 | 未找到覆盖率数据文件 | 检查是否执行了编译和测试 |
| GCNO_FILES_NOT_FOUND | gcno 文件未找到 | 编译后未生成 gcno 文件 | 检查编译配置是否启用覆盖率 |
| ALL_PART_NOT_TEST_BUILD_TARGETS | 无测试编译目标 | 部件没有测试编译目标 | 检查部件配置，确认有测试用例 |
| LOCAL_BUILD_FAILED | 本地编译失败 | local_build 脚本执行失败 | 检查 {output}/log 目录 |

### 执行错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| TEST_EXECUTION_FAILED | 测试执行失败 | 测试用例执行失败 | 检查测试日志和设备状态 |
| PR_COVERAGE_FAILED | 覆盖率计算失败 | pr_coverage 脚本执行失败 | 检查覆盖率计算日志和变更文件列表 |
| AFTER_LCOV_FAILED | 后处理失败 | after_lcov_branch.py 执行失败 | 检查后处理日志 |
| ALL_PARTS_FAILED | 所有部件失败 | 所有部件执行失败 | 检查环境配置和依赖 |

### 报告错误

| 错误代码 | 错误名称 | 描述 | 解决方案 |
|---------|---------|------|---------|
| REPORT_NOT_FOUND | 报告未找到 | 覆盖率报告未生成 | 检查覆盖率计算过程 |
| REPORT_MOVE_FAILED | 报告移动失败 | 无法将报告移动到输出目录 | 检查输出目录权限和磁盘空间 |
| OUTPUT_DIR_CREATE_FAILED | 输出目录创建失败 | 无法创建输出目录 | 检查目录权限，手动创建目录 |

## 执行流程

```
开始
  ↓
[1] 接收错误信息
  ├── 1.1 错误代码
  ├── 1.2 错误消息
  ├── 1.3 错误上下文
  └── 1.4 错误堆栈 (可选)
  ↓
[2] 查找错误类型和解决方案
  └── 2.1 在错误分类表中查找
  ↓
[3] 生成用户友好的错误信息
  ├── 3.1 简洁的错误描述
  ├── 3.2 具体的解决方案
  ├── 3.3 相关文件路径
  └── 3.4 建议的后续操作
  ↓
[4] 记录错误日志
  ├── 4.1 记录到 {OUTPUT_PATH}/error.log
  ├── 4.2 包含完整的错误信息
  └── 4.3 包含上下文和堆栈信息
  ↓
[5] 返回错误信息给用户
  ↓
结束
```

## 错误信息格式

```
错误: {错误名称}

{错误描述}

解决方案:
{解决方案}

相关文件:
- 文件路径1
- 文件路径2

建议操作:
{建议操作}

详细日志已保存到: {OUTPUT_PATH}/error.log
```

## 使用示例

```
错误: 配置文件未找到

无法找到 user-config.json 配置文件。

解决方案:
检查 {SKILL_DIR}/config/user-config.json 是否存在，如果不存在，请创建该文件并添加必要的配置项。

相关文件:
- {SKILL_DIR}/config/user-config.json

建议操作:
1. 检查 skill 目录结构
2. 创建 config 目录
3. 创建 user-config.json 文件并填写配置

详细日志已保存到: /tmp/error.log
```

## 传入参数

从任何其他模块接收:
- `errorCode`: 错误代码
- `errorMessage`: 错误消息
- `context`: 错误上下文信息
- `stackTrace`: 错误堆栈信息 (可选)
- `skill_dir`: {SKILL_DIR}
- `output_path`: {OUTPUT_PATH}

## 错误恢复

对于可恢复的错误:
- 提供恢复步骤
- 尝试自动恢复 (如果可行)
- 记录恢复操作

对于不可恢复的错误:
- 清理临时文件
- 恢复环境到初始状态
- 终止执行流程