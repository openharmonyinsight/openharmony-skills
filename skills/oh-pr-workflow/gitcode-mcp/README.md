# GitCode MCP Go Server

这是GitCode MCP服务器的Go语言实现版本，提供了GitCode API的标准MCP接口封装。

## 功能特点

- 完整支持GitCode API的主要功能
- 基于标准MCP协议实现，使用mark3labs/mcp-go SDK
- 支持STDIO和SSE两种传输方式
- 轻量级，响应速度快
- 并发处理能力强，适合高负载场景
- 模块化的代码结构，便于扩展和维护

## 安装要求

- Go 1.16+
- 网络连接以访问GitCode API

## 环境变量配置

项目使用`.env`文件来管理环境变量。您可以复制`.env.example`文件并重命名为`.env`，然后设置以下环境变量：

```
# GitCode API配置
GITCODE_TOKEN=<您的GitCode访问令牌>
GITCODE_API_URL=https://api.gitcode.com/api/v5
```

## 安装说明

### 方法一：使用安装脚本（推荐）

```bash
# 克隆仓库
git clone https://github.com/gitcode-org-com/gitcode-mcp.git
cd gitcode-mcp

# 运行安装脚本
./install.sh
```

安装脚本会：
1. 编译项目生成可执行文件
2. 创建配置目录 `~/.gitcode_mcp`
3. 复制配置文件到配置目录
4. 提示输入您的GitCode访问令牌
5. 将可执行文件安装到系统路径（需要管理员权限）或用户目录

安装完成后，您可以在任何位置运行 `gitcode-mcp` 命令。

### 方法二：使用 Go Install

```bash
# 安装最新版本
go install github.com/gitcode-org-com/gitcode-mcp@latest
```

使用 Go Install 安装后，程序会被安装到 `$GOPATH/bin` 目录下。请确保该目录已添加到您的 PATH 环境变量中。

## 快速开始

1. 运行MCP服务器

```bash
gitcode-mcp
```

2. 配置AI平台

   项目docs目录下提供了各平台的配置文件参考：
   - Claude平台: `claude_config.json`
   - Cline平台: `cline_config.json`
   - Cursor平台: `cursor_config.json`
   - Windsurf平台: `windsurf_config.json`

## MCP工具清单

GitCode MCP提供以下工具：

| 工具名称 | 描述 | 参数 |
|---------|------|-----|
| list_repositories | 列出当前用户的仓库 | 无 |
| get_repository | 获取特定仓库的详细信息 | owner, repo |
| create_repository | 创建新仓库 | name, description?, private? |
| list_branches | 列出仓库的分支 | owner, repo |
| get_branch | 获取特定分支的详细信息 | owner, repo, branch |
| create_branch | 创建新分支 | owner, repo, branch, ref |
| list_issues | 列出仓库的Issues | owner, repo |
| get_issue | 获取特定Issue的详细信息 | owner, repo, issue_number |
| create_issue | 创建新Issue | owner, repo, title, body? |
| list_pull_requests | 列出仓库的Pull Requests | owner, repo |
| get_pull_request | 获取特定Pull Request的详细信息 | owner, repo, pull_number |
| create_pull_request | 创建新Pull Request | owner, repo, title, head, base, body? |
| search_code | 搜索代码 | query |
| search_repositories | 搜索仓库 | query |
| search_issues | 搜索Issues | query |
| search_users | 搜索用户 | query |

## 许可证

该项目采用MIT许可证。详情请参阅LICENSE文件。

