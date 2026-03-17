package tools

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddBranchTools 添加分支相关工具到MCP服务器
func AddBranchTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 列出分支
	listBranchesTool := mcp.NewTool("list_branches",
		mcp.WithDescription("列出仓库的分支"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
	)
	s.AddTool(listBranchesTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		
		branches, err := apiClient.Branches.ListBranches(owner, repo)
		if err != nil {
			return nil, fmt.Errorf("获取分支列表失败: %w", err)
		}
		return FormatJSONResult(branches)
	})
	
	// 获取分支
	getBranchTool := mcp.NewTool("get_branch",
		mcp.WithDescription("获取特定分支的详细信息"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithString("branch",
			mcp.Required(),
			mcp.Description("分支名称"),
		),
	)
	s.AddTool(getBranchTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		branch, _ := request.Params.Arguments["branch"].(string)
		
		branchInfo, err := apiClient.Branches.GetBranch(owner, repo, branch)
		if err != nil {
			return nil, fmt.Errorf("获取分支详情失败: %w", err)
		}
		return FormatJSONResult(branchInfo)
	})
	
	// 创建分支
	createBranchTool := mcp.NewTool("create_branch",
		mcp.WithDescription("创建新分支"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithString("branch",
			mcp.Required(),
			mcp.Description("新分支名称"),
		),
		mcp.WithString("ref",
			mcp.Required(),
			mcp.Description("基于的引用 (通常为另一个分支名或提交SHA)"),
		),
	)
	s.AddTool(createBranchTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		branch, _ := request.Params.Arguments["branch"].(string)
		ref, _ := request.Params.Arguments["ref"].(string)
		
		branchInfo, err := apiClient.Branches.CreateBranch(owner, repo, branch, ref)
		if err != nil {
			return nil, fmt.Errorf("创建分支失败: %w", err)
		}
		return FormatJSONResult(branchInfo)
	})
} 