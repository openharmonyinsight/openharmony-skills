# GitCode MCP 平台配置文件

本目录包含了适用于不同AI平台的GitCode MCP配置文件。这些配置文件可以帮助您快速在各个平台上设置GitCode集成。

## 配置文件清单

- **Claude平台**: [claude_config.json](claude_config.json)
- **Cline平台**: [cline_config.json](cline_config.json)
- **Cursor平台**: [cursor_config.json](cursor_config.json)
- **Windsurf平台**: [windsurf_config.json](windsurf_config.json)

## 使用说明

所有配置文件都使用相同的基本结构：

```json
{
  "mcpServers": {
    "gitcode": {
      "command": "gitcode-mcp",
      "args": [],
      "env": {
        "GITCODE_TOKEN": "<您的GitCode访问令牌>",
        "GITCODE_API_URL": "https://api.gitcode.com/api/v5"
      }
    }
  }
}
```

### 使用步骤

1. 选择适合您平台的配置文件
2. 编辑文件，将`<您的GitCode访问令牌>`替换为您的实际访问令牌
3. 将配置文件保存到平台指定的配置位置

### 平台特定说明

#### Claude平台

Claude平台配置通常位于用户目录下的`.claude`文件夹：

```bash
cp claude_config.json ~/.claude/mcp_config.json
```

#### Cursor平台

Cursor平台可以在设置菜单中指定MCP配置文件：

1. 打开Cursor设置
2. 找到MCP服务器配置部分
3. 指定配置文件路径

#### Cline平台

Cline平台需要在启动时指定配置文件：

```bash
cline --mcp-config=/path/to/cline_config.json
```

#### Windsurf平台

Windsurf平台配置通常位于应用数据目录：

```bash
cp windsurf_config.json ~/.windsurf/configs/mcp.json
```

## 注意事项

- 确保您的GitCode访问令牌有足够的权限
- 配置文件中的`command`路径应该指向您已安装的`gitcode-mcp`可执行文件
- 如果您使用了自定义安装位置，请相应调整`command`的值 