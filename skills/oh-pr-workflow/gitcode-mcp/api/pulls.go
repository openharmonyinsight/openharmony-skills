package api

import (
	"encoding/json"
	"fmt"
)

// PullRequest 表示Pull Request信息
type PullRequest struct {
	ID              json.RawMessage `json:"id"`
	Number          FlexInt         `json:"number"`
	Title           string     `json:"title"`
	Body            string     `json:"body"`
	State           string     `json:"state"`
	URL             string     `json:"url"`
	HTMLURL         string     `json:"html_url"`
	User            User       `json:"user"`
	CreatedAt       string     `json:"created_at"`
	UpdatedAt       string     `json:"updated_at"`
	ClosedAt        string     `json:"closed_at"`
	MergedAt        string     `json:"merged_at"`
	MergeCommitSha  string     `json:"merge_commit_sha"`
	Assignees       []User     `json:"assignees"`
	RequestedReviewers []User  `json:"requested_reviewers"`
	Labels          []Label    `json:"labels"`
	Base            PRBranch   `json:"base"`
	Head            PRBranch   `json:"head"`
	Merged          bool       `json:"merged"`
	Mergeable       bool       `json:"mergeable"`
	Rebaseable      bool       `json:"rebaseable"`
	Comments        FlexInt    `json:"comments"`
	Commits         FlexInt    `json:"commits"`
	Additions       FlexInt    `json:"additions"`
	Deletions       FlexInt    `json:"deletions"`
	ChangedFiles    FlexInt    `json:"changed_files"`
}

// PRBranch 表示PR分支信息
type PRBranch struct {
	Label string `json:"label"`
	Ref   string `json:"ref"`
	SHA   string `json:"sha"`
	User  User   `json:"user"`
	Repo  Repository `json:"repo"`
}

// CreatePullRequestOptions 表示创建PR的参数
type CreatePullRequestOptions struct {
	Title               string   `json:"title"`
	Body                string   `json:"body,omitempty"`
	Head                string   `json:"head"`
	Base                string   `json:"base"`
	Draft               bool     `json:"draft,omitempty"`
	MaintainerCanModify bool     `json:"maintainer_can_modify,omitempty"`
}

// UpdatePullRequestOptions 表示更新PR的参数
type UpdatePullRequestOptions struct {
	Title   string `json:"title,omitempty"`
	Body    string `json:"body,omitempty"`
	State   string `json:"state,omitempty"`
	Base    string `json:"base,omitempty"`
}

// MergeOptions 表示合并PR的参数
type MergeOptions struct {
	CommitTitle       string `json:"commit_title,omitempty"`
	CommitMessage     string `json:"commit_message,omitempty"`
	SHA               string `json:"sha,omitempty"`
	MergeMethod       string `json:"merge_method,omitempty"`
	DeleteBranchAfter bool   `json:"delete_branch_after,omitempty"`
}

// ListPullRequests 列出仓库的Pull Requests
func (api *PullRequestAPI) ListPullRequests(owner, repo string) ([]PullRequest, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls", owner, repo)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var pulls []PullRequest
	if err := json.Unmarshal(resp, &pulls); err != nil {
		return nil, fmt.Errorf("解析Pull Requests列表失败: %w", err)
	}
	
	return pulls, nil
}

// GetPullRequest 获取特定Pull Request的详细信息
func (api *PullRequestAPI) GetPullRequest(owner, repo string, pullNumber int) (*PullRequest, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var pull PullRequest
	if err := json.Unmarshal(resp, &pull); err != nil {
		return nil, fmt.Errorf("解析Pull Request详情失败: %w", err)
	}
	
	return &pull, nil
}

// CreatePullRequest 创建新Pull Request
func (api *PullRequestAPI) CreatePullRequest(owner, repo, title, head, base, body string) (*PullRequest, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls", owner, repo)
	options := CreatePullRequestOptions{
		Title: title,
		Head:  head,
		Base:  base,
		Body:  body,
	}
	
	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var pull PullRequest
	if err := json.Unmarshal(resp, &pull); err != nil {
		return nil, fmt.Errorf("解析新Pull Request信息失败: %w", err)
	}
	
	return &pull, nil
}

// UpdatePullRequest 更新Pull Request
func (api *PullRequestAPI) UpdatePullRequest(owner, repo string, pullNumber int, options UpdatePullRequestOptions) (*PullRequest, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d", owner, repo, pullNumber)
	resp, err := api.Client.PATCH(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var pull PullRequest
	if err := json.Unmarshal(resp, &pull); err != nil {
		return nil, fmt.Errorf("解析更新后的Pull Request信息失败: %w", err)
	}
	
	return &pull, nil
}

// ClosePullRequest 关闭Pull Request
func (api *PullRequestAPI) ClosePullRequest(owner, repo string, pullNumber int) (*PullRequest, error) {
	return api.UpdatePullRequest(owner, repo, pullNumber, UpdatePullRequestOptions{
		State: "closed",
	})
}

// MergePullRequest 合并Pull Request
func (api *PullRequestAPI) MergePullRequest(owner, repo string, pullNumber int, options MergeOptions) (bool, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/merge", owner, repo, pullNumber)
	resp, err := api.Client.PUT(path, nil, options)
	if err != nil {
		return false, err
	}
	
	var result struct {
		Merged  bool   `json:"merged"`
		Message string `json:"message"`
	}
	
	if err := json.Unmarshal(resp, &result); err != nil {
		return false, fmt.Errorf("解析合并结果失败: %w", err)
	}
	
	return result.Merged, nil
}

// ListPRReviews 列出PR的代码审查
func (api *PullRequestAPI) ListPRReviews(owner, repo string, pullNumber int) ([]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/reviews", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var reviews []interface{}
	if err := json.Unmarshal(resp, &reviews); err != nil {
		return nil, fmt.Errorf("解析代码审查列表失败: %w", err)
	}
	
	return reviews, nil
}

// CreatePRReview 创建PR代码审查
func (api *PullRequestAPI) CreatePRReview(owner, repo string, pullNumber int, body, event string, comments []interface{}) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/reviews", owner, repo, pullNumber)
	options := map[string]interface{}{
		"body":     body,
		"event":    event,
		"comments": comments,
	}
	
	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var review interface{}
	if err := json.Unmarshal(resp, &review); err != nil {
		return nil, fmt.Errorf("解析新代码审查信息失败: %w", err)
	}
	
	return review, nil
}

// ListPRComments 列出PR的评论
func (api *PullRequestAPI) ListPRComments(owner, repo string, pullNumber int) ([]Comment, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/comments", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var comments []Comment
	if err := json.Unmarshal(resp, &comments); err != nil {
		return nil, fmt.Errorf("解析PR评论列表失败: %w", err)
	}
	
	return comments, nil
}

// CreatePRComment 创建PR评论
func (api *PullRequestAPI) CreatePRComment(owner, repo string, pullNumber int, body string) (*Comment, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/comments", owner, repo, pullNumber)
	options := map[string]string{
		"body": body,
	}

	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}

	var comment Comment
	if err := json.Unmarshal(resp, &comment); err != nil {
		return nil, fmt.Errorf("解析PR评论失败: %w", err)
	}

	return &comment, nil
}

// IsPRMergeable 检查PR是否可合并
func (api *PullRequestAPI) IsPRMergeable(owner, repo string, pullNumber int) (bool, error) {
	pr, err := api.GetPullRequest(owner, repo, pullNumber)
	if err != nil {
		return false, err
	}
	
	return pr.Mergeable, nil
}

// ListFiles 列出PR包含的文件
func (api *PullRequestAPI) ListFiles(owner, repo string, pullNumber int) ([]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/files", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var files []interface{}
	if err := json.Unmarshal(resp, &files); err != nil {
		return nil, fmt.Errorf("解析PR文件列表失败: %w", err)
	}
	
	return files, nil
}

// ListCommits 列出PR包含的提交
func (api *PullRequestAPI) ListCommits(owner, repo string, pullNumber int) ([]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/commits", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var commits []interface{}
	if err := json.Unmarshal(resp, &commits); err != nil {
		return nil, fmt.Errorf("解析PR提交列表失败: %w", err)
	}
	
	return commits, nil
} 