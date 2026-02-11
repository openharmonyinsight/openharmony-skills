# 测试部署指南

## 目标路径

设备固定路径：`/data/test`

## hdc 命令

直接使用 hdc 命令部署：

```bash
# 创建目标目录
hdc -s ${WINDOWS_IP}:8710 shell "mkdir -p /data/test/"

# 部署文件
hdc -s ${WINDOWS_IP}:8710 file send <LOCAL_PATH> /data/test/

# 运行测试
hdc -s ${WINDOWS_IP}:8710 shell "chmod +x /data/test/<TARGET_NAME> && /data/test/<TARGET_NAME>"
```

**说明**: hdc client 需要通过 `-s` 参数指定网络连接的设备地址，端口固定为 8710。
