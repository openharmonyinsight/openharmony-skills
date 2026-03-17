package tools

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddSearchTools 添加搜索相关工具到MCP服务器
func AddSearchTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 搜索代码
	searchCodeTool := mcp.NewTool("search_code",
		mcp.WithDescription("搜索代码"),
		mcp.WithString("query",
			mcp.Required(),
			mcp.Description("搜索关键词"),
		),
	)
	s.AddTool(searchCodeTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		query, _ := request.Params.Arguments["query"].(string)
		
		results, err := apiClient.Search.SearchCode(query)
		if err != nil {
			return nil, fmt.Errorf("搜索代码失败: %w", err)
		}
		return FormatJSONResult(results)
	})
	
	// 搜索仓库
	searchReposTool := mcp.NewTool("search_repositories",
		mcp.WithDescription("搜索仓库"),
		mcp.WithString("query",
			mcp.Required(),
			mcp.Description("搜索关键词"),
		),
	)
	s.AddTool(searchReposTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		query, _ := request.Params.Arguments["query"].(string)
		
		results, err := apiClient.Search.SearchRepositories(query)
		if err != nil {
			return nil, fmt.Errorf("搜索仓库失败: %w", err)
		}
		return FormatJSONResult(results)
	})
	
	// 搜索Issues
	searchIssuesTool := mcp.NewTool("search_issues",
		mcp.WithDescription("搜索Issues"),
		mcp.WithString("query",
			mcp.Required(),
			mcp.Description("搜索关键词"),
		),
	)
	s.AddTool(searchIssuesTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		query, _ := request.Params.Arguments["query"].(string)
		
		results, err := apiClient.Search.SearchIssues(query)
		if err != nil {
			return nil, fmt.Errorf("搜索Issues失败: %w", err)
		}
		return FormatJSONResult(results)
	})
	
	// 搜索用户
	searchUsersTool := mcp.NewTool("search_users",
		mcp.WithDescription("搜索用户"),
		mcp.WithString("query",
			mcp.Required(),
			mcp.Description("搜索关键词"),
		),
	)
	s.AddTool(searchUsersTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		query, _ := request.Params.Arguments["query"].(string)
		
		results, err := apiClient.Search.SearchUsers(query)
		if err != nil {
			return nil, fmt.Errorf("搜索用户失败: %w", err)
		}
		return FormatJSONResult(results)
	})
} 