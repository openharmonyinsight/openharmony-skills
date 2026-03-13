package prompts

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddPrompts 添加提示模板到MCP服务器
func AddPrompts(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 创建Issue提示
	s.AddPrompt(mcp.NewPrompt("create_issue",
		mcp.WithPromptDescription("生成创建Issue的提示文本"),
		mcp.WithArgument("owner",
			mcp.ArgumentDescription("仓库所有者"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("repo",
			mcp.ArgumentDescription("仓库名称"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("title",
			mcp.ArgumentDescription("Issue标题"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("body",
			mcp.ArgumentDescription("Issue内容"),
		),
	), func(ctx context.Context, request mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
		owner := request.Params.Arguments["owner"]
		repo := request.Params.Arguments["repo"]
		title := request.Params.Arguments["title"]
		body := request.Params.Arguments["body"]
		
		promptText := fmt.Sprintf(`在 %s/%s 仓库中创建一个新Issue：

标题：%s

内容：%s`, owner, repo, title, body)
		
		return mcp.NewGetPromptResult(
			"创建 Issue 的提示",
			[]mcp.PromptMessage{
				mcp.NewPromptMessage(
					mcp.RoleAssistant,
					mcp.NewTextContent(promptText),
				),
			},
		), nil
	})
	
	// 创建Pull Request提示
	s.AddPrompt(mcp.NewPrompt("create_pull_request",
		mcp.WithPromptDescription("生成创建Pull Request的提示文本"),
		mcp.WithArgument("owner",
			mcp.ArgumentDescription("仓库所有者"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("repo",
			mcp.ArgumentDescription("仓库名称"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("title",
			mcp.ArgumentDescription("PR标题"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("head",
			mcp.ArgumentDescription("源分支"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("base",
			mcp.ArgumentDescription("目标分支"),
			mcp.RequiredArgument(),
		),
		mcp.WithArgument("body",
			mcp.ArgumentDescription("PR内容"),
		),
	), func(ctx context.Context, request mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
		owner := request.Params.Arguments["owner"]
		repo := request.Params.Arguments["repo"]
		title := request.Params.Arguments["title"]
		head := request.Params.Arguments["head"]
		base := request.Params.Arguments["base"]
		body := request.Params.Arguments["body"]
		
		promptText := fmt.Sprintf(`在 %s/%s 仓库中创建一个新Pull Request：

标题：%s

从分支 %s 到 %s

内容：%s`, owner, repo, title, head, base, body)
		
		return mcp.NewGetPromptResult(
			"创建 Pull Request 的提示",
			[]mcp.PromptMessage{
				mcp.NewPromptMessage(
					mcp.RoleAssistant,
					mcp.NewTextContent(promptText),
				),
			},
		), nil
	})
	
	// 搜索代码提示
	s.AddPrompt(mcp.NewPrompt("search_code",
		mcp.WithPromptDescription("生成搜索代码的提示文本"),
		mcp.WithArgument("query",
			mcp.ArgumentDescription("搜索关键词"),
			mcp.RequiredArgument(),
		),
	), func(ctx context.Context, request mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
		query := request.Params.Arguments["query"]
		
		promptText := fmt.Sprintf(`搜索代码：%s

请提供相关代码段及其所在的文件和仓库信息。`, query)
		
		return mcp.NewGetPromptResult(
			"搜索代码的提示",
			[]mcp.PromptMessage{
				mcp.NewPromptMessage(
					mcp.RoleAssistant,
					mcp.NewTextContent(promptText),
				),
			},
		), nil
	})
} 