---
name: openharmony-ut
description: |
  Automate OpenHarmony unit test and fuzz test workflows including
  test generation, compilation via WSL, deployment to devices, and execution.
  Use when writing, building, or running UT/FuzzTest for OpenHarmony projects.
allowed-tools: Bash, Read, Edit, Write
---

# OpenHarmony UT 自动化

## 快速命令

### 编译测试
```bash
wsl bash -c "cd /root/OpenHarmony/ && ./build.sh --product-name=rk3568 --build-target <TARGET_NAME>"
```

### 部署到设备
```bash
python .claude/skills/openharmony-ut/scripts/deploy_oh_test.py <TARGET_NAME>
```

### 运行测试
```bash
hdc shell "chmod +x /data/test/<TARGET_NAME> && /data/test/<TARGET_NAME>"
```

## 自动化流程

当用户请求编写并运行测试时，按以下顺序自动执行：

1. **编写** - 生成测试代码，命名必须与 build target 一致
2. **编译** - 执行构建，修改代码后使用 `--fast-rebuild`
3. **部署** - 使用脚本上传到设备 `/data/test/`
4. **运行** - 执行测试并返回结果
5. **修复** - 如失败则修复错误直到通过

## 关键规则

- **命名**: 测试名必须与 BUILD.gn target 一致（如 `LnnNetBuilderFuzzTest`）
- **位置**: 放在对应模块的 tests 目录下
- **风格**: 遵循 OpenHarmony HWTEST_F 规范，不使用 GoogleTest main
- **禁魔数**: 所有常量必须有命名

## 详细文档

- [environment.md](references/environment.md) - 构建环境架构和路径说明
- [test-generation.md](references/test-generation.md) - 测试编写规范
- [build-guide.md](references/build-guide.md) - 编译命令和产物说明
- [deployment.md](references/deployment.md) - 部署步骤详解
- [execution.md](references/execution.md) - 测试执行和故障排除
