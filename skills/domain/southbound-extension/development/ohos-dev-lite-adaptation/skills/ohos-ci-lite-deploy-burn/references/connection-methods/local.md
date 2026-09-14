# 本地构建连接方式

> **适用场景**: OpenHarmony 源码就在本地（WSL2 / Git Bash / 本地 Linux VM）
> **优势**: 零延迟、无需网络、调试最方便
> **限制**: 需要本地有完整的 OH 编译工具链（GCC + Python 3.8+ + Ninja）

## 配置

`config.json` 中 `connection.method = "local"` 时：

```json
{
  "connection": {
    "method": "local",
    "local": {
      "code_dir": "C:/path/to/openharmony"
    }
  }
}
```

| 字段 | 必填 | 说明 |
|------|:----:|------|
| `code_dir` | ✅ | 本地 OH 源码根目录的绝对路径 |

## 命令模板

| 操作 | 命令模板 |
|------|---------|
| **执行命令** | `cd ${CODE_DIR} && <CMD>` (PowerShell) 或 `bash -c 'cd $CODE_DIR && <CMD>'` |
| **文件操作** | 直接用 Read/Write/Edit 工具，无需 SCP |

## 与 SSH 模式的差异

| 能力 | SSH | Local |
|------|-----|-------|
| 远程编译 | ✅ Phase 1 | ✅ 直接执行 build.sh |
| 产物下载 | ✅ Phase 2 (SCP) | ✅ 已在本地，无需下载 |
| 烧录 | ✅ Phase 3 (COM) | ✅ Phase 3 (COM) — 相同 |
| MAP 分析 | ✅ Phase 5 | ✅ Phase 5 — 相同 |
| 免密配置 | ❌ 需要一次配置 | ✅ 不需要 |
| 编译速度 | 取决于服务器性能 | 取决于本机性能 |

## WSL2 注意事项

如果源码在 WSL2 内：
- `code_dir` 填 WSL 路径：`/home/user/openharmony`
- 执行命令通过 `wsl -e bash -c '<CMD>'`
- 文件访问通过 `\\wsl$\Ubuntu-xx\home\user\...` 或 `wsl cat /path/to/file`
