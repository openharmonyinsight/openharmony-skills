# OpenHarmony 构建环境

## 环境架构

```mermaid
sequenceDiagram
    participant Linux as Linux环境（含Claude与OpenHarmony构建系统）
    participant HDC as HDC工具
    participant Win as Windows宿主机（运行hdc server）
    participant Dev as 鸿蒙设备

    Linux->>Linux: 修改代码（Claude直接编辑文件）
    Linux->>Linux: 执行 ./build.sh 构建OpenHarmony
    Win->>Dev: USB协议连接
    Linux-->>Linux: 直到编译成功

    Linux->>HDC: claude 执行 hdc -s xxx file send
    HDC->>Win: hdc client 推送应用/执行测试用例
    Win->>Dev: 推送应用/执行测试用例

    Dev->>Win:返回执行结果
    Win->>HDC:返回命令执行结果
    HDC->>Linux:输出给claude
```

## 关键路径

| 类型 | 路径 |
|------|------|
| 项目根目录 | `${OH_ROOT}` |
| 编译产物输出 | `${OH_OUTPUT}` |
| 设备测试路径 | `/data/test/` |

> **说明**: 具体路径值由初始化配置时设置，`${OH_ROOT}` 默认为 `/root/OpenHarmony`，`${OH_OUTPUT}` 默认为 `/root/OpenHarmony/out/rk3568/tests/`。

## 构建系统

1. **构建工具**: GN + Ninja
2. **执行环境**: Linux
3. **产品名称**: rk3568
