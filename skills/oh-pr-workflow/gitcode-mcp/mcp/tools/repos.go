package tools

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddRepositoryTools 添加仓库相关工具到MCP服务器
func AddRepositoryTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 列出用户仓库
	listReposTool := mcp.NewTool("list_repositories",
		mcp.WithDescription("列出当前用户的仓库"),
	)
	s.AddTool(listReposTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		repos, err := apiClient.Repos.ListUserRepos()
		if err != nil {
			return nil, fmt.Errorf("获取仓库列表失败: %w", err)
		}
		return FormatJSONResult(repos)
	})
	
	// 获取仓库
	getRepoTool := mcp.NewTool("get_repository",
		mcp.WithDescription("获取特定仓库的详细信息"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
	)
	s.AddTool(getRepoTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		
		repository, err := apiClient.Repos.GetRepo(owner, repo)
		if err != nil {
			return nil, fmt.Errorf("获取仓库详情失败: %w", err)
		}
		return FormatJSONResult(repository)
	})
	
	// 创建仓库
	createRepoTool := mcp.NewTool("create_repository",
		mcp.WithDescription("创建新仓库"),
		mcp.WithString("name",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithString("description",
			mcp.Description("仓库描述"),
		),
		mcp.WithBoolean("private",
			mcp.Description("是否为私有仓库"),
		),
	)
	s.AddTool(createRepoTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		name, _ := request.Params.Arguments["name"].(string)
		description, _ := request.Params.Arguments["description"].(string)
		private, _ := request.Params.Arguments["private"].(bool)
		
		repo, err := apiClient.Repos.CreateRepo(name, description, private)
		if err != nil {
			return nil, fmt.Errorf("创建仓库失败: %w", err)
		}
		return FormatJSONResult(repo)
	})
} 