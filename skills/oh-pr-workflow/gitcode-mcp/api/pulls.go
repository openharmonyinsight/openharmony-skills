package api

import (
	"encoding/json"
	"fmt"
	"net/url"
	"strings"
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

// SubmitPRReview 提交PR审查通过 (GitCode: POST /pulls/{n}/review)
func (api *PullRequestAPI) SubmitPRReview(owner, repo string, pullNumber int, force bool) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/review", owner, repo, pullNumber)
	body := map[string]interface{}{
		"force": force,
	}

	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析审查结果失败: %w", err)
	}

	return result, nil
}

// SubmitPRTest 提交PR测试通过 (GitCode: POST /pulls/{n}/test)
func (api *PullRequestAPI) SubmitPRTest(owner, repo string, pullNumber int, force bool) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/test", owner, repo, pullNumber)
	body := map[string]interface{}{
		"force": force,
	}

	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析测试结果失败: %w", err)
	}

	return result, nil
}

func mapToValues(m map[string]string) url.Values {
	v := url.Values{}
	for key, val := range m {
		v.Set(key, val)
	}
	return v
}

// DiffPosition 表示diff评论的位置信息
type DiffPosition struct {
	StartNewLine int `json:"start_new_line,omitempty"`
	EndNewLine   int `json:"end_new_line,omitempty"`
	StartOldLine int `json:"start_old_line,omitempty"`
	EndOldLine   int `json:"end_old_line,omitempty"`
}

// PRComment 表示PR评论（包含diff评论的完整字段）
type PRComment struct {
	ID           json.RawMessage `json:"id"`
	DiscussionID string          `json:"discussion_id,omitempty"`
	Body         string          `json:"body"`
	CreatedAt    string          `json:"created_at"`
	UpdatedAt    string          `json:"updated_at"`
	User         User            `json:"user"`
	CommentType  string          `json:"comment_type,omitempty"`
	Resolved     *bool           `json:"resolved,omitempty"`
	DiffPosition *DiffPosition   `json:"diff_position,omitempty"`
	Reply        []PRComment     `json:"reply,omitempty"`
}

// ListPRComments 列出PR的评论（支持comment_type过滤和per_page参数）
func (api *PullRequestAPI) ListPRComments(owner, repo string, pullNumber int, commentType string, perPage int) ([]PRComment, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/comments", owner, repo, pullNumber)
	params := make(map[string]string)
	if perPage > 0 {
		params["per_page"] = fmt.Sprintf("%d", perPage)
	}

	resp, err := api.Client.GET(path, mapToValues(params))
	if err != nil {
		return nil, err
	}

	var comments []PRComment
	if err := json.Unmarshal(resp, &comments); err != nil {
		return nil, fmt.Errorf("解析PR评论列表失败: %w", err)
	}

	// 客户端过滤 comment_type（API 不一定支持该参数）
	if commentType != "" {
		var filtered []PRComment
		for _, c := range comments {
			if c.CommentType == commentType {
				filtered = append(filtered, c)
			}
		}
		return filtered, nil
	}

	return comments, nil
}

// DeletePRComment 删除PR评论
func (api *PullRequestAPI) DeletePRComment(owner, repo string, commentID int) error {
	path := fmt.Sprintf("/repos/%s/%s/pulls/comments/%d", owner, repo, commentID)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// CreatePRComment 创建PR评论（支持行级评论：传入 filePath 和 position）
func (api *PullRequestAPI) CreatePRComment(owner, repo string, pullNumber int, body, filePath string, position int) (*PRComment, error) {
	apiPath := fmt.Sprintf("/repos/%s/%s/pulls/%d/comments", owner, repo, pullNumber)
	options := map[string]interface{}{
		"body": body,
	}
	if filePath != "" {
		options["path"] = filePath
	}
	if position > 0 {
		options["position"] = position
	}

	resp, err := api.Client.POST(apiPath, nil, options)
	if err != nil {
		return nil, err
	}

	var comment PRComment
	if err := json.Unmarshal(resp, &comment); err != nil {
		return nil, fmt.Errorf("解析PR评论失败: %w", err)
	}

	return &comment, nil
}

// ListPRReactions 列出PR的表情回应
func (api *PullRequestAPI) ListPRReactions(owner, repo string, pullNumber int) ([]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/reactions", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}

	var reactions []interface{}
	if err := json.Unmarshal(resp, &reactions); err != nil {
		return nil, fmt.Errorf("解析PR回应列表失败: %w", err)
	}
	return reactions, nil
}

// CreatePRReaction 为PR添加表情回应
func (api *PullRequestAPI) CreatePRReaction(owner, repo string, pullNumber int, content string) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/reactions", owner, repo, pullNumber)
	body := map[string]string{"content": content}

	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}

	var reaction interface{}
	if err := json.Unmarshal(resp, &reaction); err != nil {
		return nil, fmt.Errorf("解析PR回应失败: %w", err)
	}
	return reaction, nil
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

// UpdatePRReviewers 分配PR审查人员 (GitCode: POST /pulls/{n}/reviewers)
func (api *PullRequestAPI) UpdatePRReviewers(owner, repo string, pullNumber int, reviewers string) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/reviewers", owner, repo, pullNumber)
	reviewerList := strings.Split(reviewers, ",")
	for i := range reviewerList {
		reviewerList[i] = strings.TrimSpace(reviewerList[i])
	}
	body := map[string]interface{}{
		"reviewers": reviewerList,
	}

	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析更新审查人员结果失败: %w", err)
	}

	return result, nil
}

// UpdatePRTesters 分配PR测试人员 (GitCode: POST /pulls/{n}/testers)
func (api *PullRequestAPI) UpdatePRTesters(owner, repo string, pullNumber int, testers string) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/testers", owner, repo, pullNumber)
	testerList := strings.Split(testers, ",")
	for i := range testerList {
		testerList[i] = strings.TrimSpace(testerList[i])
	}
	body := map[string]interface{}{
		"testers": testerList,
	}

	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析更新测试人员结果失败: %w", err)
	}

	return result, nil
}

// AddPRLabels 为PR添加标签
func (api *PullRequestAPI) AddPRLabels(owner, repo string, pullNumber int, labels string) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/labels", owner, repo, pullNumber)
	labelList := strings.Split(labels, ",")
	for i := range labelList {
		labelList[i] = strings.TrimSpace(labelList[i])
	}

	resp, err := api.Client.POST(path, nil, labelList)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析添加标签结果失败: %w", err)
	}

	return result, nil
}

// RemovePRLabel 移除PR的单个标签
func (api *PullRequestAPI) RemovePRLabel(owner, repo string, pullNumber int, label string) error {
	label = strings.TrimSpace(label)
	encodedLabel := url.PathEscape(label)
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/labels/%s", owner, repo, pullNumber, encodedLabel)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// PRLinkIssues 关联/取消关联Issue到PR
func (api *PullRequestAPI) PRLinkIssues(owner, repo string, pullNumber int, issues string) (interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d", owner, repo, pullNumber)
	body := map[string]interface{}{
		"issue_nums": issues,
	}

	resp, err := api.Client.PATCH(path, nil, body)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析关联Issue结果失败: %w", err)
	}

	return result, nil
}

// ListPROperationLogs 列出PR的操作日志
func (api *PullRequestAPI) ListPROperationLogs(owner, repo string, pullNumber int) ([]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/pulls/%d/operate_logs", owner, repo, pullNumber)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}

	var logs []interface{}
	if err := json.Unmarshal(resp, &logs); err != nil {
		return nil, fmt.Errorf("解析PR操作日志失败: %w", err)
	}

	return logs, nil
} 