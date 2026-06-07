# 常见问题排查指南

## 问题分类索引

- [环境配置问题](#环境配置问题)
- [编译问题](#编译问题)
- [执行问题](#执行问题)
- [报告生成问题](#报告生成问题)
- [设备连接问题](#设备连接问题)

---

## 环境配置问题

### 1. Python 版本过低

**症状**: 执行时报错 `PYTHON_VERSION_LOW`

**排查步骤**:
```bash
# 检查 Python 版本
python3 --version

# 如果版本低于 3.8，需要升级
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install python3.8

# CentOS/RHEL:
sudo yum install python38
```

**验证**:
```bash
python3 --version
# 输出应该 >= Python 3.8
```

---

### 2. 工具依赖缺失

**症状**: 执行时报错 `*_NOT_INSTALLED`

**排查步骤**:
```bash
# 检查工具是否安装
which git
which gcc
which g++
which lcov
which genhtml
which hdc

# 如果缺失，安装对应工具
# Ubuntu/Debian:
sudo apt-get install git gcc g++ lcov genhtml

# CentOS/RHEL:
sudo yum install git gcc-c++ lcov genhtml
```

**验证**:
```bash
# 检查所有工具
which git gcc g++ lcov genhtml hdc
```

---

### 3. Python 包依赖缺失

**症状**: 执行时报错 `PYTHON_DEPENDENCY_INSTALL_FAILED`

**排查步骤**:
```bash
# 检查 pip 可用性
pip3 --version

# 安装依赖
cd {SKILL_DIR}
pip3 install -r requirements.txt

# 如果安装失败，检查网络和 pip 配置
pip3 config list
```

**常见问题**:
- 网络连接失败：使用国内镜像源
- 权限不足：使用 `--user` 参数或 `sudo`
- 版本冲突：使用虚拟环境

---

## 编译问题

### 1. 预编译失败

**症状**: 执行时报错 `PRECOMPILATION_FAILED`

**排查步骤**:
```bash
# 检查编译日志
tail -100 {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log

# 检查磁盘空间
df -h

# 检查内存使用
free -h

# 清理编译缓存
rm -rf {CODE_ROOT}/out/
```

**常见原因**:
- 磁盘空间不足
- 内存不足
- 编译环境配置错误
- 代码冲突

---

### 2. gcno 文件未生成

**症状**: 执行时报错 `GCNO_FILES_NOT_FOUND`

**排查步骤**:
```bash
# 检查是否执行了 build_before_generate.py
ls {CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/part_config.json

# 如果不存在，检查编译配置
cat {CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/part_config.json

# 检查编译产物
find {CODE_ROOT}/out -name "*.gcno" | head -10
```

**解决方法**:
- 确保执行了 `build_before_generate.py`
- 检查编译命令是否包含 `--gn-args use_clang_coverage=true`
- 重新编译

---

### 3. 编译失败

**症状**: 执行时报错 `COMPILATION_FAILED`

**排查步骤**:
```bash
# 查看编译日志最后100行
tail -100 {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log

# 检查是否有编译错误
grep "error:" {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log

# 检查部件配置
cat {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build_configs/parts_info/parts_targets.json | grep {part_name}
```

**常见原因**:
- 源代码语法错误
- 依赖缺失
- 构建配置错误
- 编译器版本不兼容

---

## 执行问题

### 1. 测试执行超时

**症状**: 测试执行超过2小时

**排查步骤**:
```bash
# 检查测试是否仍在运行
ps aux | grep start.sh

# 检查设备连接状态
hdc list targets

# 检查设备内存使用
hdc shell free -h

# 检查测试日志
tail -f {CODE_ROOT}/test/testfwk/developer_test/logs/*.log
```

**解决方法**:
- 增加超时时间
- 减少测试用例数量
- 检查设备性能

---

### 2. 测试执行失败

**症状**: 执行时报错 `TEST_EXECUTION_FAILED`

**排查步骤**:
```bash
# 检查测试日志
ls {CODE_ROOT}/test/testfwk/developer_test/reports/
cat {CODE_ROOT}/test/testfwk/developer_test/reports/latest/*.log

# 检查设备连接
hdc list targets

# 检查设备日志
hdc shell dmesg | tail -50
```

**常见原因**:
- 设备断连
- 测试用例错误
- 设备资源不足
- 权限问题

---

### 3. 设备连接失败

**症状**: 执行时报错 `DEVICE_CONNECTION_FAILED`

**排查步骤**:
```bash
# 检查设备连接
hdc list targets

# 如果配置了 IP 和端口
hdc -s {ip}:{port} list targets

# 检查网络连接
ping {ip}

# 重启 hdc 服务
hdc kill
hdc start
```

**解决方法**:
- 检查网络连接
- 检查 hdc 配置
- 重启 hdc 服务
- 重新连接设备

---

## 报告生成问题

### 1. 报告未生成

**症状**: 执行时报错 `REPORT_NOT_FOUND`

**排查步骤**:
```bash
# 检查报告目录
ls -la {CODE_ROOT}/test/testfwk/developer_test/local_coverage/code_coverage/result/
ls -la {CODE_ROOT}/test/testfwk/developer_test/local_coverage/interface_coverage/result/

# 检查覆盖率数据文件
find {CODE_ROOT}/test/testfwk/developer_test/local_coverage -name "*.info"

# 检查 lcov 执行日志
```

**常见原因**:
- 测试未执行完成
- 覆盖率数据未收集
- lcov 配置错误

---

### 2. 报告移动失败

**症状**: 执行时报错 `REPORT_MOVE_FAILED`

**排查步骤**:
```bash
# 检查源报告是否存在
ls -la {CODE_ROOT}/test/testfwk/developer_test/local_coverage/code_coverage/result/

# 检查目标目录权限
ls -la {output_path}

# 检查磁盘空间
df -h

# 手动移动报告
mv {CODE_ROOT}/test/testfwk/developer_test/local_coverage/code_coverage/result/ {output_path}/code_coverage
```

**解决方法**:
- 检查目标目录权限
- 确保有足够磁盘空间
- 手动移动报告

---

### 3. 报告解析失败

**症状**: parse_coverage_report.py 执行失败

**排查步骤**:
```bash
# 手动执行解析脚本
cd {SKILL_DIR}/scripts
python3 parse_coverage_report.py --output_path {output_path} --report_type all

# 检查报告格式
file {output_path}/code_coverage/coverage/reports/cxx/html/index.html

# 检查 Python 环境
python3 --version
pip3 list | grep lxml
```

---

## 设备连接问题

### 1. 设备未找到

**症状**: 执行时报错 `DEVICE_NOT_FOUND`

**排查步骤**:
```bash
# 列出所有设备
hdc list targets

# 如果为空，检查设备连接
# 检查 USB 线连接
# 检查设备是否开机

# 如果配置了 IP 和端口，检查网络
ping {ip}
telnet {ip} {port}

# 检查 hdc 服务
hdc version
hdc start
```

---

### 2. 多设备冲突

**症状**: 检测到多个设备

**解决方法**:
- 在 `user-config.json` 中配置具体的设备信息
- 使用 `ip` 和 `port` 或 `sn` 指定设备

---

### 3. 设备连接不稳定

**症状**: 设备频繁断连

**解决方法**:
- 使用有线网络连接
- 检查网络质量
- 重启 hdc 服务
- 重新连接设备

---

## 错误恢复策略

### 快速恢复指南

| 错误类型 | 恢复方法 | 是否需要清理 | 优先级 |
|---------|---------|-------------|-------|
| 配置错误 | 修改 user-config.json 后重试 | 否 | 高 |
| 环境缺失 | 运行 pip install / apt-get | 否 | 高 |
| 编译失败 | 清理编译缓存后重试 | 是：`rm -rf out/` | 高 |
| 测试超时 | 检查设备状态，重试 | 否 | 中 |
| 报告生成失败 | 检查 lcov 数据完整性 | 是：重新生成 gcda | 高 |
| 设备连接失败 | 检查 hdc 配置，重新连接 | 否 | 高 |
| gcno 文件未生成 | 重新执行 build_before_generate.py | 否 | 中 |
| gcda 文件不匹配 | 重新编译 | 是：`rm -rf out/` | 高 |
| 磁盘空间不足 | 清理旧产物 | 是：清理报告和编译产物 | 高 |
| 内存不足 | 关闭其他进程，增加 swap | 否 | 中 |

---

### 详细恢复步骤

#### 1. 配置错误恢复

**症状**: `CONFIG_ERROR`, `USER_CONFIG_NOT_FOUND`, `CODE_ROOT_NOT_FOUND`

**恢复步骤**:
```bash
# 1. 检查配置文件
cat {SKILL_DIR}/config/user-config.json

# 2. 验证 code_root 路径
ls {code_root}
test -d {code_root} && echo "路径存在" || echo "路径不存在"

# 3. 检查必需的项目结构
test -d {code_root}/developer_test && echo "developer_test 存在" || echo "developer_test 不存在"
test -d {code_root}/xdevice && echo "xdevice 存在" || echo "xdevice 不存在"
test -d {code_root}/pr_local_coverage && echo "pr_local_coverage 存在" || echo "pr_local_coverage 不存在"

# 4. 修正配置后重试
```

**无需清理**: 配置错误不影响编译产物和报告

---

#### 2. 环境缺失恢复

**症状**: `PYTHON_VERSION_LOW`, `TOOL_NOT_INSTALLED`, `PYTHON_DEPENDENCY_INSTALL_FAILED`

**恢复步骤**:
```bash
# 1. 检查 Python 版本
python3 --version
# 如果 < 3.8，升级 Python

# 2. 安装缺失的工具
# Ubuntu/Debian:
sudo apt-get install git gcc g++ lcov genhtml

# CentOS/RHEL:
sudo yum install git gcc-c++ lcov genhtml

# 3. 安装 Python 依赖
cd {SKILL_DIR}
pip3 install -r requirements.txt

# 4. 验证安装
which git gcc g++ lcov genhtml hdc
pip3 list | grep lxml
```

**无需清理**: 环境安装不影响编译产物和报告

---

#### 3. 编译失败恢复

**症状**: `COMPILATION_FAILED`, `PRECOMPILATION_FAILED`, `BUILD_ERROR`

**恢复步骤**:
```bash
# 1. 查看编译日志
tail -100 {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log
grep "error:" {CODE_ROOT}/out/generic_generic_arm_64only/general_all_phone_standard/build.log

# 2. 检查磁盘空间
df -h

# 3. 检查内存使用
free -h

# 4. 清理编译缓存
rm -rf {CODE_ROOT}/out/

# 5. 重新编译
```

**需要清理**: 必须清理编译缓存 `rm -rf out/`

**常见原因**:
- 磁盘空间不足 → 清理空间
- 内存不足 → 增加 swap 或减少并发
- 代码冲突 → 检查代码
- 依赖缺失 → 安装依赖

---

#### 4. 测试超时恢复

**症状**: 测试执行超过2小时

**恢复步骤**:
```bash
# 1. 检查测试是否仍在运行
ps aux | grep start.sh

# 2. 检查设备连接状态
hdc list targets

# 3. 检查设备内存使用
hdc shell free -h

# 4. 查看测试日志
tail -f {CODE_ROOT}/test/testfwk/developer_test/logs/*.log

# 5. 如果测试仍在运行，等待完成
# 6. 如果测试已卡死，重试
```

**无需清理**: 测试超时不影响编译产物

**预防措施**:
- 在设备负载较低时执行测试
- 减少测试用例数量
- 增加超时时间配置

---

#### 5. 报告生成失败恢复

**症状**: `REPORT_NOT_FOUND`, `REPORT_GENERATION_FAILED`, `LCOV_ERROR`

**恢复步骤**:
```bash
# 1. 检查覆盖率数据文件
find {CODE_ROOT}/test/testfwk/developer_test/local_coverage -name "*.info"
find {CODE_ROOT}/out -name "*.gcda" | head -10

# 2. 检查 gcno 文件
find {CODE_ROOT}/out -name "*.gcno" | head -10

# 3. 检查 lcov 配置
cat /etc/lcovrc | grep lcov_branch_coverage

# 4. 如果 gcda 文件不匹配，重新生成
# 方法1: 重新执行测试
# 方法2: 重新编译

# 5. 手动执行 lcov
lcov --capture --directory {CODE_ROOT}/out --output-file coverage.info
genhtml coverage.info --output-directory html_report
```

**需要清理**: 如果 gcda/gcno 不匹配，需要重新编译 `rm -rf out/`

**常见原因**:
- gcda 文件未生成 → 重新执行测试
- gcno 文件已过时 → 重新编译
- lcov 配置错误 → 检查 /etc/lcovrc

---

#### 6. 设备连接失败恢复

**症状**: `DEVICE_CONNECTION_FAILED`, `DEVICE_NOT_FOUND`

**恢复步骤**:
```bash
# 1. 检查设备连接
hdc list targets

# 2. 如果配置了 IP 和端口
hdc -s {ip}:{port} list targets

# 3. 检查网络连接
ping {ip}

# 4. 重启 hdc 服务
hdc kill
hdc start

# 5. 重新连接设备
hdc list targets
```

**无需清理**: 设备连接问题不影响编译产物和报告

**预防措施**:
- 使用有线网络连接
- 检查网络质量
- 定期重启 hdc 服务

---

#### 7. gcno 文件未生成恢复

**症状**: `GCNO_FILES_NOT_FOUND`

**恢复步骤**:
```bash
# 1. 检查是否执行了 build_before_generate.py
ls {CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/part_config.json

# 2. 检查编译配置
cat {CODE_ROOT}/test/testfwk/developer_test/local_coverage/restore_comment/part_config.json

# 3. 检查编译产物
find {CODE_ROOT}/out -name "*.gcno" | head -10

# 4. 重新执行 build_before_generate.py
cd {CODE_ROOT}
python3 {SKILL_DIR}/scripts/build_before_generate.py
```

**无需清理**: 重新执行 build_before_generate.py 即可

---

#### 8. gcda 文件不匹配恢复

**症状**: 报告生成失败，gcda/gcno 不匹配

**恢复步骤**:
```bash
# 1. 检查 gcno 文件时间戳
find {CODE_ROOT}/out -name "*.gcno" -exec ls -l {} \;

# 2. 检查 gcda 文件时间戳
find {CODE_ROOT}/out -name "*.gcda" -exec ls -l {} \;

# 3. 清理编译缓存
rm -rf {CODE_ROOT}/out/

# 4. 重新编译
```

**需要清理**: 必须重新编译 `rm -rf out/`

**原因**: 修改 lcov 分支覆盖率参数后，gcno 文件会变化，需要重新编译

---

#### 9. 磁盘空间不足恢复

**症状**: 磁盘空间不足，编译或报告生成失败

**恢复步骤**:
```bash
# 1. 检查磁盘空间
df -h

# 2. 清理旧的编译产物
rm -rf {CODE_ROOT}/out/

# 3. 清理旧的报告
rm -rf {CODE_ROOT}/coverage_result/
rm -rf {SKILL_DIR}/coverage_report/

# 4. 清理系统缓存
sudo apt-get clean
sudo apt-get autoremove

# 5. 清理 docker 镜像（如果使用 docker）
docker system prune -a

# 6. 检查大文件
du -h --max-depth=1 / | sort -hr | head -20
```

**需要清理**: 清理旧的编译产物和报告

**预防措施**:
- 定期清理旧的编译产物和报告
- 使用独立的磁盘分区存储报告
- 监控磁盘空间使用情况

---

#### 10. 内存不足恢复

**症状**: 编译或执行时内存不足

**恢复步骤**:
```bash
# 1. 检查内存使用
free -h

# 2. 检查 swap 分区
swapon -s

# 3. 关闭不必要的进程
htop
# 或
top

# 4. 增加 swap 分区（如果需要）
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 5. 减少编译并发数
# 修改编译配置，降低并发度
```

**无需清理**: 内存问题不影响编译产物

**预防措施**:
- 配置足够的内存（至少 16GB，推荐 32GB）
- 关闭不必要的后台进程
- 减少编译并发数

---

### 恢复优先级

**高优先级（立即处理）**:
1. 配置错误
2. 环境缺失
3. 编译失败
4. 报告生成失败
5. 设备连接失败

**中优先级（有时间处理）**:
1. 测试超时
2. gcno 文件未生成
3. 内存不足

**低优先级（定期维护）**:
1. 磁盘空间不足
2. gcda 文件不匹配

---

### 自动恢复脚本

**创建恢复脚本** (`{SKILL_DIR}/scripts/recover.sh`):

```bash
#!/bin/bash

CODE_ROOT=$(cat {SKILL_DIR}/config/user-config.json | grep -oP '"code_root":\s*"\K[^"]+')
SKILL_DIR={SKILL_DIR}

echo "开始恢复..."

# 1. 检查配置
if [ ! -f "$SKILL_DIR/config/user-config.json" ]; then
    echo "错误: user-config.json 不存在"
    exit 1
fi

# 2. 检查磁盘空间
DISK_USAGE=$(df -h "$CODE_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "警告: 磁盘空间不足 ($DISK_USAGE%)"
    read -p "是否清理旧的编译产物和报告？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$CODE_ROOT/out/"
        rm -rf "$CODE_ROOT/coverage_result/"
        echo "清理完成"
    fi
fi

# 3. 检查设备连接
if ! hdc list targets | grep -q .; then
    echo "警告: 设备未连接"
    read -p "是否重试连接？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        hdc kill
        hdc start
        echo "hdc 服务已重启"
    fi
fi

echo "恢复完成"
```

---

## 获取帮助

如果以上方法都无法解决问题，请：

1. 收集错误日志：
    ```bash
    cp {output_path}/error.log /tmp/error.log
    ```

2. 收集环境信息：
    ```bash
    uname -a > /tmp/env_info.txt
    python3 --version >> /tmp/env_info.txt
    which git gcc g++ lcov genhtml hdc >> /tmp/env_info.txt
    ```

3. 查看错误码文档：`references/06-error-handler.md`

4. 联系技术支持，提供以上信息