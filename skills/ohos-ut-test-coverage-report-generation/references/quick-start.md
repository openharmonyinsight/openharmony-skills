# 快速开始指南

## 前置条件检查

在执行覆盖率报告生成之前，请确保满足以下条件：

### 环境要求
- [ ] **操作系统**: Linux 系统
- [ ] **Python 版本**: 3.8 或更高版本
- [ ] **磁盘空间**: 至少 50GB 可用空间
- [ ] **内存**: 建议 16GB 或更多

### 工具依赖
- [ ] **hdc**: OpenHarmony 设备连接工具
- [ ] **git**: 版本控制系统
- [ ] **lcov**: 代码覆盖率工具
- [ ] **gcc/g++**: 编译器
- [ ] **genhtml**: HTML 报告生成工具
- [ ] **pip**: Python 包管理器

### 设备要求
- [ ] **设备连接**: HDC 设备已连接并可用
- [ ] **设备状态**: 设备正常运行，可执行测试

---

## 配置步骤

### 步骤1: 配置 user-config.json

在 `{SKILL_DIR}/config/user-config.json` 中配置以下信息：

```json
{
  "hdc": {
    "ip": "192.168.1.100",
    "port": "8700",
    "sn": "device_serial_number"
  },
  "code_root": "/path/to/ohos/code"
}
```

**配置说明**:
- `code_root`: OpenHarmony 代码根目录路径（必需）
- `hdc.ip`: 设备 IP 地址（可选，如果未配置则自动查找）
- `hdc.port`: HDC 端口（可选，默认 8700）
- `hdc.sn`: 设备序列号（可选，用于唯一标识设备）

### 步骤2: 检查设备连接

```bash
# 列出所有连接的设备
hdc list targets

# 如果配置了 IP 和端口
hdc -s 192.168.1.100:8700 list targets

# 如果配置了IP 、端口和序列号
hdc -s ip:port -t device_serial_number shell ls
```

### 步骤3: 配置 lcov

检查 `/etc/lcovrc` 文件中的 `lcov_branch_coverage` 设置：

```bash
# 检查当前设置
grep lcov_branch_coverage /etc/lcovrc

# 如果不存在或为 0，修改为 1
echo "lcov_branch_coverage = 1" >> /etc/lcovrc
```

---

## 执行示例

### 快速生成全量覆盖率报告

```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告"
```

执行流程将自动完成以下步骤：
1. 检查环境和配置
2. 预编译（如需要）
3. 执行 build_before_generate.py
4. 编译用例
5. 执行测试
6. 生成覆盖率报告
7. 恢复环境
8. 输出报告路径

### 快速生成增量覆盖率报告

```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告"
```

执行流程将自动完成以下步骤：
1. 检查环境和配置
2. 生成或使用提供的 diff 文件
3. 执行本地编译
4. 执行覆盖率计算
5. 生成增量覆盖率报告
6. 清理临时文件
7. 输出报告路径

---

## 常见问题

### Q1: 编译时间很长怎么办？
**A**: 可以使用 `skip_compiler: true` 参数跳过编译（前提是已经完成编译）。

### Q2: 设备连接失败怎么办？
**A**: 检查 `user-config.json` 中的 hdc 配置，确保 IP、端口和序列号正确。

### Q3: 报告生成失败怎么办？
**A**: 查看 `{OUTPUT_PATH}/error.log` 文件获取详细错误信息。

### Q4: Python 依赖包安装失败怎么办？
**A**: 检查 Python 版本是否为 3.8+，尝试使用虚拟环境或升级 pip。

### Q5: 磁盘空间不足怎么办？
**A**: 清理旧的编译产物和报告（`rm -rf out/`），预留至少 50GB 空间。

---

## 优化建议

### 环境优化
1. **使用编译缓存**: 配置 `--ccache` 参数可以显著加快编译速度
2. **使用 SSD 存储**: 提高编译和 I/O 性能
3. **配置足够的内存**: 至少 16GB，推荐 32GB
4. **使用多核 CPU**: 至少 8 核，推荐 16 核或更多

### 执行优化
1. **选择合适的覆盖率类型**: 日常开发使用增量覆盖率，定期使用全量覆盖率
2. **在设备负载较低时执行测试**: 避免在高峰期执行
3. **关闭不必要的后台进程**: 释放系统资源
4. **定期清理旧产物**: 释放磁盘空间

---

## 更多资源

- 📊 **性能说明**: 详见 `references/performance-guide.md` - 预期耗时、资源占用
- 📚 **使用示例**: 详见 `references/usage-examples.md` - 详细场景示例
- 💡 **最佳实践**: 详见 `references/best-practices.md` - 场景选择建议
- 🔧 **问题排查**: 详见 `references/troubleshooting.md` - 错误恢复策略