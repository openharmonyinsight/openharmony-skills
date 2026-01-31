# 测试执行指南

## 运行测试

上传完成后，执行以下命令运行测试：

```bash
hdc shell "chmod +x /data/test/<TARGET_NAME> && /data/test/<TARGET_NAME>"
```

## 查看实时日志

```bash
hdc shell "/data/test/<TARGET_NAME>"
```

## 清理设备测试文件

```bash
hdc shell "rm -rf /data/test/<TARGET_NAME>"
```

## 完整工作流程

当用户请求编写并运行测试时，按以下顺序自动执行：

1. **编写** - 生成或修改测试代码
2. **编译** - 执行构建命令
3. **部署** - 上传到设备
4. **运行** - 执行测试用例
5. **验证** - 检查结果，修复错误直至通过

## 禁止行为

- ❌ 不要只输出命令让用户自己执行
- ❌ 不要跳过上传步骤直接运行
- ❌ 不要假设测试文件已存在设备
- ❌ 不要改变 target 名称大小写
