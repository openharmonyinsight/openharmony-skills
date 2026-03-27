package api

import (
	"encoding/json"
	"fmt"
	"net/url"
)

// Issue 表示Issue信息
type Issue struct {
	ID          json.RawMessage `json:"id"`
	Number      FlexInt         `json:"number"`
	Title       string          `json:"title"`
	Body        string          `json:"body"`
	State       string          `json:"state"`
	URL         string          `json:"url"`
	HTMLURL     string          `json:"html_url"`
	User        User            `json:"user"`
	CreatedAt   string          `json:"created_at"`
	UpdatedAt   string          `json:"updated_at"`
	ClosedAt    string          `json:"closed_at"`
	Labels      []Label         `json:"labels"`
	Assignees   []User          `json:"assignees"`
	Comments    FlexInt         `json:"comments"`
	PullRequest *PRRef          `json:"pull_request,omitempty"`
}

// PRRef 表示与Issue关联的PR引用
type PRRef struct {
	URL string `json:"url"`
}

// Label 表示Issue标签
type Label struct {
	ID          json.RawMessage `json:"id"`
	Name        string          `json:"name"`
	Color       string          `json:"color"`
	Description string          `json:"description"`
}

// Comment 表示Issue评论
type Comment struct {
	ID        json.RawMessage `json:"id"`
	Body      string          `json:"body"`
	User      User            `json:"user"`
	CreatedAt string          `json:"created_at"`
	UpdatedAt string          `json:"updated_at"`
}

// CreateIssueOptions 表示创建Issue的参数
type CreateIssueOptions struct {
	Title     string   `json:"title"`
	Body      string   `json:"body,omitempty"`
	Assignees []string `json:"assignees,omitempty"`
	Labels    []string `json:"labels,omitempty"`
}

// UpdateIssueOptions 表示更新Issue的参数
type UpdateIssueOptions struct {
	Title     string   `json:"title,omitempty"`
	Body      string   `json:"body,omitempty"`
	State     string   `json:"state,omitempty"`
	Assignees []string `json:"assignees,omitempty"`
	Labels    []string `json:"labels,omitempty"`
}

// ListIssues 列出仓库的Issues
func (api *IssueAPI) ListIssues(owner, repo string) ([]Issue, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues", owner, repo)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var issues []Issue
	if err := json.Unmarshal(resp, &issues); err != nil {
		return nil, fmt.Errorf("解析Issues列表失败: %w", err)
	}
	
	return issues, nil
}

// GetIssue 获取特定Issue的详细信息
func (api *IssueAPI) GetIssue(owner, repo string, issueNumber int) (*Issue, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d", owner, repo, issueNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var issue Issue
	if err := json.Unmarshal(resp, &issue); err != nil {
		return nil, fmt.Errorf("解析Issue详情失败: %w", err)
	}
	
	return &issue, nil
}

// CreateIssue 创建新Issue
func (api *IssueAPI) CreateIssue(owner, repo, title, body string) (*Issue, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues", owner, repo)
	options := CreateIssueOptions{
		Title: title,
		Body:  body,
	}
	
	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var issue Issue
	if err := json.Unmarshal(resp, &issue); err != nil {
		return nil, fmt.Errorf("解析新Issue信息失败: %w", err)
	}
	
	return &issue, nil
}

// UpdateIssue 更新Issue
func (api *IssueAPI) UpdateIssue(owner, repo string, issueNumber int, options UpdateIssueOptions) (*Issue, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d", owner, repo, issueNumber)
	resp, err := api.Client.PATCH(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var issue Issue
	if err := json.Unmarshal(resp, &issue); err != nil {
		return nil, fmt.Errorf("解析更新后的Issue信息失败: %w", err)
	}
	
	return &issue, nil
}

// CloseIssue 关闭Issue (与CLI保持一致使用state字段)
func (api *IssueAPI) CloseIssue(owner, repo string, issueNumber int) (*Issue, error) {
	return api.UpdateIssue(owner, repo, issueNumber, UpdateIssueOptions{
		State: "closed",
	})
}

// ReopenIssue 重新打开Issue
func (api *IssueAPI) ReopenIssue(owner, repo string, issueNumber int) (*Issue, error) {
	return api.UpdateIssue(owner, repo, issueNumber, UpdateIssueOptions{
		State: "open",
	})
}

// ListComments 列出Issue的评论
func (api *IssueAPI) ListComments(owner, repo string, issueNumber int) ([]Comment, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/comments", owner, repo, issueNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var comments []Comment
	if err := json.Unmarshal(resp, &comments); err != nil {
		return nil, fmt.Errorf("解析评论列表失败: %w", err)
	}
	
	return comments, nil
}

// AddComment 添加Issue评论
func (api *IssueAPI) AddComment(owner, repo string, issueNumber int, body string) (*Comment, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/comments", owner, repo, issueNumber)
	options := map[string]string{
		"body": body,
	}
	
	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var comment Comment
	if err := json.Unmarshal(resp, &comment); err != nil {
		return nil, fmt.Errorf("解析新评论信息失败: %w", err)
	}
	
	return &comment, nil
}

// EditComment 编辑Issue评论
func (api *IssueAPI) EditComment(owner, repo string, commentID int, body string) (*Comment, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/comments/%d", owner, repo, commentID)
	options := map[string]string{
		"body": body,
	}

	resp, err := api.Client.PATCH(path, nil, options)
	if err != nil {
		return nil, err
	}

	// GitCode PATCH may return empty body on success
	if len(resp) == 0 {
		return &Comment{ID: json.RawMessage(fmt.Sprintf("%d", commentID)), Body: body}, nil
	}

	var comment Comment
	if err := json.Unmarshal(resp, &comment); err != nil {
		return nil, fmt.Errorf("解析更新后的评论信息失败: %w", err)
	}

	return &comment, nil
}

// DeleteComment 删除Issue评论
func (api *IssueAPI) DeleteComment(owner, repo string, commentID int) error {
	path := fmt.Sprintf("/repos/%s/%s/issues/comments/%d", owner, repo, commentID)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// ListLabels 列出仓库的标签
func (api *IssueAPI) ListLabels(owner, repo string) ([]Label, error) {
	path := fmt.Sprintf("/repos/%s/%s/labels", owner, repo)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var labels []Label
	if err := json.Unmarshal(resp, &labels); err != nil {
		return nil, fmt.Errorf("解析标签列表失败: %w", err)
	}
	
	return labels, nil
}

// GetIssueLabels 获取Issue的标签
func (api *IssueAPI) GetIssueLabels(owner, repo string, issueNumber int) ([]Label, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/labels", owner, repo, issueNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var labels []Label
	if err := json.Unmarshal(resp, &labels); err != nil {
		return nil, fmt.Errorf("解析Issue标签失败: %w", err)
	}
	
	return labels, nil
}

// AddLabelsToIssue 为Issue添加标签
func (api *IssueAPI) AddLabelsToIssue(owner, repo string, issueNumber int, labels []string) ([]Label, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/labels", owner, repo, issueNumber)
	resp, err := api.Client.POST(path, nil, labels)
	if err != nil {
		return nil, err
	}
	
	var resultLabels []Label
	if err := json.Unmarshal(resp, &resultLabels); err != nil {
		return nil, fmt.Errorf("解析添加标签结果失败: %w", err)
	}
	
	return resultLabels, nil
}

// RemoveLabelFromIssue 从Issue移除标签
func (api *IssueAPI) RemoveLabelFromIssue(owner, repo string, issueNumber int, label string) error {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/labels/%s", owner, repo, issueNumber, url.PathEscape(label))
	_, err := api.Client.DELETE(path, nil)
	return err
}

// SearchIssues 搜索Issues
func (api *IssueAPI) SearchIssues(query string) ([]Issue, error) {
	values := url.Values{}
	values.Set("q", query)

	resp, err := api.Client.GET("/search/issues", values)
	if err != nil {
		return nil, err
	}

	// GitCode API returns array directly
	var issues []Issue
	if err := json.Unmarshal(resp, &issues); err != nil {
		return nil, fmt.Errorf("解析搜索结果失败: %w", err)
	}

	return issues, nil
}

// ListIssueReactions 列出Issue的表情回应
func (api *IssueAPI) ListIssueReactions(owner, repo string, issueNumber int) ([]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/reactions", owner, repo, issueNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}

	var reactions []interface{}
	if err := json.Unmarshal(resp, &reactions); err != nil {
		return nil, fmt.Errorf("解析Issue回应列表失败: %w", err)
	}
	return reactions, nil
}

// CreateIssueReaction 为Issue添加表情回应
func (api *IssueAPI) CreateIssueReaction(owner, repo string, issueNumber int, content string) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/issues/%d/reactions", owner, repo, issueNumber)
	body := map[string]string{"content": content}

	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}

	var reaction interface{}
	if err := json.Unmarshal(resp, &reaction); err != nil {
		return nil, fmt.Errorf("解析Issue回应失败: %w", err)
	}
	return reaction, nil
}