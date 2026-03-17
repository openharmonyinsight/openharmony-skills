package tools

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddPullRequestTools 添加Pull Request相关工具到MCP服务器
func AddPullRequestTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 列出Pull Requests
	listPRsTool := mcp.NewTool("list_pull_requests",
		mcp.WithDescription("列出仓库的Pull Requests"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
	)
	s.AddTool(listPRsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		
		prs, err := apiClient.Pulls.ListPullRequests(owner, repo)
		if err != nil {
			return nil, fmt.Errorf("获取Pull Requests列表失败: %w", err)
		}
		return FormatJSONResult(prs)
	})
	
	// 获取Pull Request
	getPRTool := mcp.NewTool("get_pull_request",
		mcp.WithDescription("获取特定Pull Request的详细信息"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithNumber("pull_number",
			mcp.Required(),
			mcp.Description("Pull Request编号"),
		),
	)
	s.AddTool(getPRTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")

		pr, err := apiClient.Pulls.GetPullRequest(owner, repo, prNumber)
		if err != nil {
			return nil, fmt.Errorf("获取Pull Request详情失败: %w", err)
		}
		return FormatJSONResult(pr)
	})
	
	// 创建Pull Request
	createPRTool := mcp.NewTool("create_pull_request",
		mcp.WithDescription("创建新Pull Request"),
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
			mcp.Description("Pull Request标题"),
		),
		mcp.WithString("head",
			mcp.Required(),
			mcp.Description("源分支"),
		),
		mcp.WithString("base",
			mcp.Required(),
			mcp.Description("目标分支"),
		),
		mcp.WithString("body",
			mcp.Description("Pull Request内容"),
		),
	)
	s.AddTool(createPRTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		title, _ := request.Params.Arguments["title"].(string)
		head, _ := request.Params.Arguments["head"].(string)
		base, _ := request.Params.Arguments["base"].(string)
		body, _ := request.Params.Arguments["body"].(string)
		
		pr, err := apiClient.Pulls.CreatePullRequest(owner, repo, title, head, base, body)
		if err != nil {
			return nil, fmt.Errorf("创建Pull Request失败: %w", err)
		}
		return FormatJSONResult(pr)
	})

	// 列出PR的提交
	listPRCommitsTool := mcp.NewTool("list_pr_commits",
		mcp.WithDescription("列出Pull Request包含的提交"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithNumber("pull_number",
			mcp.Required(),
			mcp.Description("Pull Request编号"),
		),
	)
	s.AddTool(listPRCommitsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")

		commits, err := apiClient.Pulls.ListCommits(owner, repo, prNumber)
		if err != nil {
			return nil, fmt.Errorf("获取PR提交列表失败: %w", err)
		}
		return FormatJSONResult(commits)
	})

	// 列出PR的变更文件
	listPRFilesTool := mcp.NewTool("list_pr_files",
		mcp.WithDescription("列出Pull Request包含的变更文件"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithNumber("pull_number",
			mcp.Required(),
			mcp.Description("Pull Request编号"),
		),
	)
	s.AddTool(listPRFilesTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")

		files, err := apiClient.Pulls.ListFiles(owner, repo, prNumber)
		if err != nil {
			return nil, fmt.Errorf("获取PR变更文件失败: %w", err)
		}
		return FormatJSONResult(files)
	})

	// 创建PR评论
	createPRCommentTool := mcp.NewTool("create_pr_comment",
		mcp.WithDescription("创建Pull Request评论"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithNumber("pull_number",
			mcp.Required(),
			mcp.Description("Pull Request编号"),
		),
		mcp.WithString("body",
			mcp.Required(),
			mcp.Description("评论内容"),
		),
	)
	s.AddTool(createPRCommentTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		body, _ := request.Params.Arguments["body"].(string)

		comment, err := apiClient.Pulls.CreatePRComment(owner, repo, prNumber, body)
		if err != nil {
			return nil, fmt.Errorf("创建PR评论失败: %w", err)
		}
		return FormatJSONResult(comment)
	})
} 