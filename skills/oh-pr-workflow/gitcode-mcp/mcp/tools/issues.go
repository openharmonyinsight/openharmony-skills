package tools

import (
	"context"
	"fmt"
	"strings"

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

	// 更新Issue
	updateIssueTool := mcp.NewTool("update_issue",
		mcp.WithDescription("更新Issue（标题、内容、状态、指派人、标签）"),
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
		mcp.WithString("title",
			mcp.Description("Issue标题"),
		),
		mcp.WithString("body",
			mcp.Description("Issue内容"),
		),
		mcp.WithString("state",
			mcp.Description("Issue状态（open/closed/progressing）"),
		),
	)
	s.AddTool(updateIssueTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")
		title, _ := request.Params.Arguments["title"].(string)
		body, _ := request.Params.Arguments["body"].(string)
		state, _ := request.Params.Arguments["state"].(string)

		issue, err := apiClient.Issues.UpdateIssue(owner, repo, issueNumber, api.UpdateIssueOptions{
			Title: title,
			Body:  body,
			State: state,
		})
		if err != nil {
			return nil, fmt.Errorf("更新Issue失败: %w", err)
		}
		return FormatJSONResult(issue)
	})

	// 关闭Issue
	closeIssueTool := mcp.NewTool("close_issue",
		mcp.WithDescription("关闭Issue"),
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
	s.AddTool(closeIssueTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")

		issue, err := apiClient.Issues.CloseIssue(owner, repo, issueNumber)
		if err != nil {
			return nil, fmt.Errorf("关闭Issue失败: %w", err)
		}
		return FormatJSONResult(issue)
	})

	// 重新打开Issue
	reopenIssueTool := mcp.NewTool("reopen_issue",
		mcp.WithDescription("重新打开已关闭的Issue"),
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
	s.AddTool(reopenIssueTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")

		issue, err := apiClient.Issues.ReopenIssue(owner, repo, issueNumber)
		if err != nil {
			return nil, fmt.Errorf("重新打开Issue失败: %w", err)
		}
		return FormatJSONResult(issue)
	})

	// 添加Issue评论
	addCommentTool := mcp.NewTool("add_issue_comment",
		mcp.WithDescription("为Issue添加评论"),
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
		mcp.WithString("body",
			mcp.Required(),
			mcp.Description("评论内容"),
		),
	)
	s.AddTool(addCommentTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")
		body, _ := request.Params.Arguments["body"].(string)

		comment, err := apiClient.Issues.AddComment(owner, repo, issueNumber, body)
		if err != nil {
			return nil, fmt.Errorf("添加评论失败: %w", err)
		}
		return FormatJSONResult(comment)
	})

	// 列出Issue评论
	listCommentsTool := mcp.NewTool("list_issue_comments",
		mcp.WithDescription("列出Issue的评论"),
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
	s.AddTool(listCommentsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")

		comments, err := apiClient.Issues.ListComments(owner, repo, issueNumber)
		if err != nil {
			return nil, fmt.Errorf("获取评论列表失败: %w", err)
		}
		return FormatJSONResult(comments)
	})

	// 编辑Issue评论
	editCommentTool := mcp.NewTool("edit_issue_comment",
		mcp.WithDescription("编辑Issue评论"),
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
			mcp.Description("评论ID"),
		),
		mcp.WithString("body",
			mcp.Required(),
			mcp.Description("评论内容"),
		),
	)
	s.AddTool(editCommentTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		commentID := GetIntArg(request.Params.Arguments, "comment_id")
		body, _ := request.Params.Arguments["body"].(string)

		comment, err := apiClient.Issues.EditComment(owner, repo, commentID, body)
		if err != nil {
			return nil, fmt.Errorf("编辑评论失败: %w", err)
		}
		return FormatJSONResult(comment)
	})

	// 删除Issue评论
	deleteCommentTool := mcp.NewTool("delete_issue_comment",
		mcp.WithDescription("删除Issue评论"),
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
			mcp.Description("评论ID"),
		),
	)
	s.AddTool(deleteCommentTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		commentID := GetIntArg(request.Params.Arguments, "comment_id")

		err := apiClient.Issues.DeleteComment(owner, repo, commentID)
		if err != nil {
			return nil, fmt.Errorf("删除评论失败: %w", err)
		}
		return FormatJSONResult(map[string]string{"status": "deleted"})
	})

	// 列出仓库标签
	listLabelsTool := mcp.NewTool("list_labels",
		mcp.WithDescription("列出仓库的标签"),
		mcp.WithString("owner",
			mcp.Required(),
			mcp.Description("仓库所有者"),
		),
		mcp.WithString("repo",
			mcp.Required(),
			mcp.Description("仓库名称"),
		),
	)
	s.AddTool(listLabelsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)

		labels, err := apiClient.Issues.ListLabels(owner, repo)
		if err != nil {
			return nil, fmt.Errorf("获取标签列表失败: %w", err)
		}
		return FormatJSONResult(labels)
	})

	// 为Issue添加标签
	addLabelsTool := mcp.NewTool("add_issue_labels",
		mcp.WithDescription("为Issue添加标签"),
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
		mcp.WithString("labels",
			mcp.Required(),
			mcp.Description("标签名称，多个标签用逗号分隔"),
		),
	)
	s.AddTool(addLabelsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")
		labels, _ := request.Params.Arguments["labels"].(string)

		labelList := strings.Split(labels, ",")
		for i, l := range labelList {
			labelList[i] = strings.TrimSpace(l)
		}

		result, err := apiClient.Issues.AddLabelsToIssue(owner, repo, issueNumber, labelList)
		if err != nil {
			return nil, fmt.Errorf("添加标签失败: %w", err)
		}
		return FormatJSONResult(result)
	})

	// 从Issue移除标签
	removeLabelTool := mcp.NewTool("remove_issue_label",
		mcp.WithDescription("从Issue移除标签"),
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
		mcp.WithString("label",
			mcp.Required(),
			mcp.Description("标签名称"),
		),
	)
	s.AddTool(removeLabelTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")
		label, _ := request.Params.Arguments["label"].(string)

		err := apiClient.Issues.RemoveLabelFromIssue(owner, repo, issueNumber, label)
		if err != nil {
			return nil, fmt.Errorf("移除标签失败: %w", err)
		}
		return FormatJSONResult(map[string]string{"status": "removed"})
	})

	// 列出Issue表情回应
	listIssueReactionsTool := mcp.NewTool("list_issue_reactions",
		mcp.WithDescription("列出Issue的表情回应"),
		mcp.WithString("owner", mcp.Required(), mcp.Description("仓库所有者")),
		mcp.WithString("repo", mcp.Required(), mcp.Description("仓库名称")),
		mcp.WithNumber("issue_number", mcp.Required(), mcp.Description("Issue编号")),
	)
	s.AddTool(listIssueReactionsTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")

		reactions, err := apiClient.Issues.ListIssueReactions(owner, repo, issueNumber)
		if err != nil {
			return nil, fmt.Errorf("获取Issue回应列表失败: %w", err)
		}
		return FormatJSONResult(reactions)
	})

	// 为Issue添加表情回应
	createIssueReactionTool := mcp.NewTool("create_issue_reaction",
		mcp.WithDescription("为Issue添加表情回应"),
		mcp.WithString("owner", mcp.Required(), mcp.Description("仓库所有者")),
		mcp.WithString("repo", mcp.Required(), mcp.Description("仓库名称")),
		mcp.WithNumber("issue_number", mcp.Required(), mcp.Description("Issue编号")),
		mcp.WithString("content", mcp.Required(), mcp.Description("回应类型: +1, -1, laugh, confused, heart, hooray, rocket, eyes")),
	)
	s.AddTool(createIssueReactionTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		owner, _ := request.Params.Arguments["owner"].(string)
		repo, _ := request.Params.Arguments["repo"].(string)
		issueNumber := GetIntArg(request.Params.Arguments, "issue_number")
		content, _ := request.Params.Arguments["content"].(string)

		reaction, err := apiClient.Issues.CreateIssueReaction(owner, repo, issueNumber, content)
		if err != nil {
			return nil, fmt.Errorf("添加Issue回应失败: %w", err)
		}
		return FormatJSONResult(reaction)
	})
}