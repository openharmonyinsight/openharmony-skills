package tools

import (
	"context"
	"fmt"
	"strings"

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

	// 列出PR评论
	listPRCommentsTool := mcp.NewTool("list_pr_comments",
		mcp.WithDescription("列出Pull Request的评论"),
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
		mcp.WithString("comment_type",
			mcp.Description("评论类型过滤: diff_comment(行级评论) 或 pr_comment(普通评论)"),
		),
		mcp.WithNumber("per_page",
			mcp.Description("每页数量，默认30，最大100"),
		),
	)
	s.AddTool(listPRCommentsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		commentType, _ := request.Params.Arguments["comment_type"].(string)
		perPage := GetIntArg(request.Params.Arguments, "per_page")

		comments, err := apiClient.Pulls.ListPRComments(owner, repo, prNumber, commentType, perPage)
		if err != nil {
			return nil, fmt.Errorf("获取PR评论列表失败: %w", err)
		}
		return FormatJSONResult(comments)
	})

	// 删除PR评论
	deletePRCommentTool := mcp.NewTool("delete_pr_comment",
		mcp.WithDescription("删除Pull Request评论"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
		mcp.WithNumber("comment_id",
			mcp.Required(),
			mcp.Description("评论ID (note_id)"),
		),
	)
	s.AddTool(deletePRCommentTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		commentID := GetIntArg(request.Params.Arguments, "comment_id")

		err := apiClient.Pulls.DeletePRComment(owner, repo, commentID)
		if err != nil {
			return nil, fmt.Errorf("删除PR评论失败: %w", err)
		}
		return FormatJSONResult(map[string]string{"status": "deleted"})
	})

	// 创建PR评论（支持行级评论）
	createPRCommentTool := mcp.NewTool("create_pr_comment",
		mcp.WithDescription("创建Pull Request评论（支持行级评论：传入path和position）"),
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
		mcp.WithString("path",
			mcp.Description("文件路径（行级评论时必填）"),
		),
		mcp.WithNumber("position",
			mcp.Description("diff中的行号（行级评论时必填）"),
		),
	)
	s.AddTool(createPRCommentTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		body, _ := request.Params.Arguments["body"].(string)
		filePath, _ := request.Params.Arguments["path"].(string)
		position := GetIntArg(request.Params.Arguments, "position")

		comment, err := apiClient.Pulls.CreatePRComment(owner, repo, prNumber, body, filePath, position)
		if err != nil {
			return nil, fmt.Errorf("创建PR评论失败: %w", err)
		}
		return FormatJSONResult(comment)
	})

	// 更新Pull Request
	updatePRTool := mcp.NewTool("update_pull_request",
		mcp.WithDescription("更新Pull Request的标题、内容、状态或目标分支"),
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
		mcp.WithString("title",
			mcp.Description("Pull Request标题"),
		),
		mcp.WithString("body",
			mcp.Description("Pull Request内容"),
		),
		mcp.WithString("state",
			mcp.Description("Pull Request状态: open 或 closed"),
		),
		mcp.WithString("base",
			mcp.Description("目标分支"),
		),
	)
	s.AddTool(updatePRTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		title, _ := request.Params.Arguments["title"].(string)
		body, _ := request.Params.Arguments["body"].(string)
		state, _ := request.Params.Arguments["state"].(string)
		base, _ := request.Params.Arguments["base"].(string)

		pr, err := apiClient.Pulls.UpdatePullRequest(owner, repo, prNumber, api.UpdatePullRequestOptions{
			Title: title,
			Body:  body,
			State: state,
			Base:  base,
		})
		if err != nil {
			return nil, fmt.Errorf("更新Pull Request失败: %w", err)
		}
		return FormatJSONResult(pr)
	})

	// 合并Pull Request
	mergePRTool := mcp.NewTool("merge_pull_request",
		mcp.WithDescription("合并Pull Request"),
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
		mcp.WithString("merge_method",
			mcp.Description("合并方式: merge、squash 或 rebase"),
		),
		mcp.WithString("commit_title",
			mcp.Description("合并提交标题"),
		),
		mcp.WithString("commit_message",
			mcp.Description("合并提交消息"),
		),
	)
	s.AddTool(mergePRTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		mergeMethod, _ := request.Params.Arguments["merge_method"].(string)
		commitTitle, _ := request.Params.Arguments["commit_title"].(string)
		commitMessage, _ := request.Params.Arguments["commit_message"].(string)

		merged, err := apiClient.Pulls.MergePullRequest(owner, repo, prNumber, api.MergeOptions{
			MergeMethod:   mergeMethod,
			CommitTitle:   commitTitle,
			CommitMessage: commitMessage,
		})
		if err != nil {
			return nil, fmt.Errorf("合并Pull Request失败: %w", err)
		}
		return FormatJSONResult(map[string]interface{}{"merged": merged})
	})

	// 提交PR审查通过 (GitCode: POST /pulls/{n}/review)
	submitPRReviewTool := mcp.NewTool("submit_pr_review",
		mcp.WithDescription("提交Pull Request审查通过（approve）"),
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
		mcp.WithBoolean("force",
			mcp.Description("是否强制通过审查"),
		),
	)
	s.AddTool(submitPRReviewTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		force, _ := request.Params.Arguments["force"].(bool)

		result, err := apiClient.Pulls.SubmitPRReview(owner, repo, prNumber, force)
		if err != nil {
			return nil, fmt.Errorf("提交PR审查失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 提交PR测试通过 (GitCode: POST /pulls/{n}/test)
	submitPRTestTool := mcp.NewTool("submit_pr_test",
		mcp.WithDescription("标记Pull Request测试通过"),
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
		mcp.WithBoolean("force",
			mcp.Description("是否强制通过测试"),
		),
	)
	s.AddTool(submitPRTestTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		force, _ := request.Params.Arguments["force"].(bool)

		result, err := apiClient.Pulls.SubmitPRTest(owner, repo, prNumber, force)
		if err != nil {
			return nil, fmt.Errorf("提交PR测试失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 更新PR审查人员
	updatePRReviewersTool := mcp.NewTool("update_pr_reviewers",
		mcp.WithDescription("更新Pull Request的审查人员"),
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
		mcp.WithString("reviewers",
			mcp.Required(),
			mcp.Description("审查人员用户名列表，逗号分隔"),
		),
	)
	s.AddTool(updatePRReviewersTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		reviewers, _ := request.Params.Arguments["reviewers"].(string)

		result, err := apiClient.Pulls.UpdatePRReviewers(owner, repo, prNumber, reviewers)
		if err != nil {
			return nil, fmt.Errorf("更新PR审查人员失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 更新PR测试人员
	updatePRTestersTool := mcp.NewTool("update_pr_testers",
		mcp.WithDescription("更新Pull Request的测试人员"),
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
		mcp.WithString("testers",
			mcp.Required(),
			mcp.Description("测试人员用户名列表，逗号分隔"),
		),
	)
	s.AddTool(updatePRTestersTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		testers, _ := request.Params.Arguments["testers"].(string)

		result, err := apiClient.Pulls.UpdatePRTesters(owner, repo, prNumber, testers)
		if err != nil {
			return nil, fmt.Errorf("更新PR测试人员失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 更新PR标签
	updatePRLabelsTool := mcp.NewTool("update_pr_labels",
		mcp.WithDescription("添加或移除Pull Request的标签"),
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
		mcp.WithString("labels",
			mcp.Required(),
			mcp.Description("标签列表，逗号分隔"),
		),
		mcp.WithBoolean("remove",
			mcp.Description("是否为移除操作，默认false表示添加"),
		),
	)
	s.AddTool(updatePRLabelsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		labels, _ := request.Params.Arguments["labels"].(string)
		remove, _ := request.Params.Arguments["remove"].(bool)

		if remove {
			labelList := strings.Split(labels, ",")
			for _, label := range labelList {
				label = strings.TrimSpace(label)
				if label == "" {
					continue
				}
				if err := apiClient.Pulls.RemovePRLabel(owner, repo, prNumber, label); err != nil {
					return nil, fmt.Errorf("移除PR标签 %s 失败: %w", label, err)
				}
			}
			return FormatJSONResult(map[string]string{"status": "labels removed"})
		}

		result, err := apiClient.Pulls.AddPRLabels(owner, repo, prNumber, labels)
		if err != nil {
			return nil, fmt.Errorf("添加PR标签失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 关联Issue到PR
	prLinkIssuesTool := mcp.NewTool("pr_link_issues",
		mcp.WithDescription("关联或取消关联Issue到Pull Request"),
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
		mcp.WithString("issues",
			mcp.Required(),
			mcp.Description("Issue编号列表，逗号分隔"),
		),
	)
	s.AddTool(prLinkIssuesTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		issues, _ := request.Params.Arguments["issues"].(string)

		result, err := apiClient.Pulls.PRLinkIssues(owner, repo, prNumber, issues)
		if err != nil {
			return nil, fmt.Errorf("关联Issue到PR失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 列出PR操作日志
	listPROperationLogsTool := mcp.NewTool("list_pr_operation_logs",
		mcp.WithDescription("列出Pull Request的操作历史记录"),
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
	s.AddTool(listPROperationLogsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")

		logs, err := apiClient.Pulls.ListPROperationLogs(owner, repo, prNumber)
		if err != nil {
			return nil, fmt.Errorf("获取PR操作日志失败: %w", err)
		}
		return FormatJSONResult(logs)
	})

	// 列出PR表情回应
	listPRReactionsTool := mcp.NewTool("list_pr_reactions",
		mcp.WithDescription("列出Pull Request的表情回应"),
		mcp.WithString("owner", mcp.Required(), mcp.Description("仓库所有者")),
		mcp.WithString("repo", mcp.Required(), mcp.Description("仓库名称")),
		mcp.WithNumber("pull_number", mcp.Required(), mcp.Description("Pull Request编号")),
	)
	s.AddTool(listPRReactionsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")

		reactions, err := apiClient.Pulls.ListPRReactions(owner, repo, prNumber)
		if err != nil {
			return nil, fmt.Errorf("获取PR回应列表失败: %w", err)
		}
		return FormatJSONResult(reactions)
	})

	// 为PR添加表情回应
	createPRReactionTool := mcp.NewTool("create_pr_reaction",
		mcp.WithDescription("为Pull Request添加表情回应"),
		mcp.WithString("owner", mcp.Required(), mcp.Description("仓库所有者")),
		mcp.WithString("repo", mcp.Required(), mcp.Description("仓库名称")),
		mcp.WithNumber("pull_number", mcp.Required(), mcp.Description("Pull Request编号")),
		mcp.WithString("content", mcp.Required(), mcp.Description("回应类型: +1, -1, laugh, confused, heart, hooray, rocket, eyes")),
	)
	s.AddTool(createPRReactionTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		prNumber := GetIntArg(request.Params.Arguments, "pull_number")
		content, _ := request.Params.Arguments["content"].(string)

		reaction, err := apiClient.Pulls.CreatePRReaction(owner, repo, prNumber, content)
		if err != nil {
			return nil, fmt.Errorf("添加PR回应失败: %w", err)
		}
		return FormatJSONResult(reaction)
	})
}