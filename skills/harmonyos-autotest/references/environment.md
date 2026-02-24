# 环境检测指南

检测 HarmonyOS 自动化测试环境是否就绪。

## 检测步骤

### 1. 检测 HDC 工具

```bash
hdc version
```
- 确认 HDC 已安装且可执行
- 记录版本号

### 2. 检测 Hypium 框架

```bash
pip3 show hypium
```
- 确认版本 >= 6.0.7.210
- 如未安装，提示安装命令: `pip3 install hypium`

### 3. 检测设备连接

```bash
hdc list targets
```
- 列出所有已连接设备
- 检查设备状态是否为 connected

### 4. 检测应用安装状态（可选）

```bash
hdc shell bm dump -n {package_name}
```
- 确认目标应用是否已安装

## 输出格式

```json
{
  "is_ready": true|false,
  "checks": {
    "hdc": {"installed": true|false, "version": "x.x.x", "error": "..."},
    "hypium": {"installed": true|false, "version": "x.x.x", "min_required": "6.0.7.210"},
    "devices": [{"sn": "device_sn", "status": "connected|offline|unauthorized"}],
    "app": {"checked": true|false, "installed": true|false, "package_name": "com.example.app"}
  },
  "recommendations": ["list of recommendations if is_ready is false"]
}
```

## 错误处理

| 问题 | 处理方式 |
|------|---------|
| HDC 未安装 | 提示下载和配置方法 |
| Hypium 未安装 | 提供 `pip3 install hypium` 命令 |
| 设备未连接 | 提示检查 USB 连接和网络adb |
| 设备未授权 | 提示在设备上确认授权弹窗 |
