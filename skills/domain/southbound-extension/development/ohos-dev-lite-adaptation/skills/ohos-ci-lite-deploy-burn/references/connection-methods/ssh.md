# SSH 连接方式（推荐）

> **适用场景**: 远程 Linux 服务器上存放 OpenHarmony 源码，本地 Windows/macOS 做 Agent 运行环境
> **优势**: 安全（免密登录一次配置后无需密码）、通用（所有 OH Lite 编译环境都是 Linux）、支持流水线全阶段

## 配置要求

`config.json` 中 `connection.method = "ssh"` 时需填写：

```json
{
  "connection": {
    "method": "ssh",
    "ssh": {
      "host": "192.0.2.10",
      "port": 22,
      "user": "root",
      "identity_file": "~/.ssh/id_ed25519"
    }
  }
}
```

| 字段 | 必填 | 说明 | 示例 |
|------|:----:|------|------|
| `host` | ✅ | 服务器 IP 或域名 | `192.0.2.10` |
| `port` | ✅ | SSH 端口 | `22`（或自定义端口） |
| `user` | ✅ | SSH 登录用户 | `root` |
| `identity_file` | ⚠️ 推荐 | 私钥文件路径（不填则用密码） | `~/.ssh/id_ed25519` |

## 免密登录配置

首次运行 Phase 0 时自动完成：
1. 检测是否已可免密连接
2. 若不可 → 生成/使用已有密钥对 → 推送公钥到服务器
3. 验证免密生效

**手动配置（可选提前做）**:
```bash
# 本地生成密钥（如果没有）
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

# 复制公钥到服务器
ssh-copy-id -p <PORT> <USER>@<HOST>
```

## 命令模板

SSH 连接方式下，以下变量由 config.json 自动填充：

| 操作 | 命令模板 | 变量来源 |
|------|---------|---------|
| **远程执行** | `ssh -p ${PORT} -i ${IDENTITY} ${USER}@${HOST} "<CMD>"` | connection.ssh.* |
| **下载文件** | `scp -P ${PORT} -i ${IDENTITY} ${USER}@${HOST}:${REMOTE_PATH} ${LOCAL_PATH}` | 同上 |
| **上传文件** | `scp -P ${PORT} -i ${IDENTITY} ${LOCAL_PATH} ${USER}@${HOST}:${REMOTE_PATH}` | 同上 |

## PowerShell 特殊处理

Windows PowerShell 中执行 SSH 命令时需注意：
- `$env:CI='true'` 前缀：部分 CI 环境需要此变量才能正常执行 ssh
- `&&` 链接不支持：用 `; if ($?) { }` 替代
- 路径中的 `\` 需要转义或用 `/`
