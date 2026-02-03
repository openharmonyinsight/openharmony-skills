# 测试部署指南

## 目标路径

设备固定路径：`/data/test`

## 方法一：自动化部署脚本（推荐）

使用项目提供的 `deploy_oh_test.py` 脚本一键部署：

```bash
python .claude/skills/openharmony-ut/scripts/deploy_oh_test.py <TARGET_NAME>
```

可选参数：
```bash
python .claude/skills/openharmony-ut/scripts/deploy_oh_test.py <TARGET_NAME> --wsl-distro Ubuntu-22.04
```

脚本自动处理：
1. 在 WSL 中查找编译产物
2. 转换 Linux 路径为 Windows WSL 路径
3. 通过 hdc 发送到设备

## 方法二：手动部署（备用）

### 步骤 1：创建设备目录
```bash
hdc shell "mkdir -p /data/test"
```

### 步骤 2：在 WSL 中查找编译产物
```bash
wsl bash -c "cd /root/OpenHarmony/out/rk3568/tests/ && find . -name <TARGET_NAME> | xargs realpath"
```

### 步骤 3：路径转换

Linux 路径转换为 Windows WSL 路径格式：

| Linux | Windows |
|-------|---------|
| `/root/OpenHarmony/out/rk3568/tests/xxx/test` | `\\wsl.localhost\Ubuntu-20.04\root\OpenHarmony\out\rk3568\tests\xxx\test` |

### 步骤 4：上传到设备
```bash
hdc file send <LOCAL_TEST_PATH> /data/test
```
