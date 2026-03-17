package tools

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddIssueTools 添加Issue相关工具到MCP服务器
func AddIssueTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 列出Issues
	listIssuesTool := mcp.NewTool("list_issues",
		mcp.WithDescription("列出仓库的Issues"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
	)
	s.AddTool(listIssuesTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		
		issues, err := apiClient.Issues.ListIssues(owner, repo)
		if err != nil {
			return nil, fmt.Errorf("获取Issues列表失败: %w", err)
		}
		return FormatJSONResult(issues)
	})
	
	// 获取Issue
	getIssueTool := mcp.NewTool("get_issue",
		mcp.WithDescription("获取特定Issue的详细信息"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithNumber("issue_number",
			mcp.Required(),
			mcp.Description("Issue编号"),
		),
	)
	s.AddTool(getIssueTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")

		issue, err := apiClient.Issues.GetIssue(owner, repo, issueNumber)
		if err != nil {
			return nil, fmt.Errorf("获取Issue详情失败: %w", err)
		}
		return FormatJSONResult(issue)
	})
	
	// 创建Issue
	createIssueTool := mcp.NewTool("create_issue",
		mcp.WithDescription("创建新Issue"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithString("title",
			mcp.Required(),
			mcp.Description("Issue标题"),
		),
		mcp.WithString("body",
			mcp.Description("Issue内容"),
		),
	)
	s.AddTool(createIssueTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		title, _ := request.Params.Arguments["title"].(string)
		body, _ := request.Params.Arguments["body"].(string)
		
		issue, err := apiClient.Issues.CreateIssue(owner, repo, title, body)
		if err != nil {
			return nil, fmt.Errorf("创建Issue失败: %w", err)
		}
		return FormatJSONResult(issue)
	})
} 