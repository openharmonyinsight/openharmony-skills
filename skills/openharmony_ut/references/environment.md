# OpenHarmony 构建环境

## 环境架构

```mermaid
sequenceDiagram
    participant Win as Windows本地电脑（运行Claude）
    participant WSL as WSL环境(含OpenHarmony构建系统)
    participant HDC as HDC工具
    participant Dev as 鸿蒙设备

    Win-->>WSL: 同步代码文件修改内容
    WSL->>Win: 读取代码（Windows映射目录）
    Win->>WSL: wsl bash -c "cd /root/OpenHarmony && ./build.sh ..."
    WSL->>WSL: 执行OpenHarmony构建(build.sh)
    WSL-->>Win: 输出编译结果

    Win->>HDC: hdc install / hdc shell aa test ...
    HDC->>Dev: 推送应用/执行测试用例
    Dev-->>HDC: 返回测试日志/结果
    HDC-->>Win: 输出测试结果
```

## 关键路径

| 类型 | 路径 |
|------|------|
| WSL 源码根目录 | `/root/OpenHarmony/` |
| Windows 映射路径 | `\\wsl.localhost\Ubuntu-20.04\root\OpenHarmony` |
| 编译产物输出 | `/root/OpenHarmony/out/rk3568/tests/` |
| 设备测试路径 | `/data/test/` |

## 构建系统

- **构建工具**: GN + Ninja
- **执行环境**: 必须通过 WSL
- **产品名称**: rk3568
