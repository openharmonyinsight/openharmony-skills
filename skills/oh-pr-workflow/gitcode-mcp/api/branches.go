package api

import (
	"encoding/json"
	"fmt"
)

// Branch 表示分支信息
type Branch struct {
	Name      string     `json:"name"`
	Protected bool       `json:"protected"`
	Commit    CommitInfo `json:"commit"`
}

// CommitInfo 表示提交信息
type CommitInfo struct {
	ID        string `json:"id"`
	TreeID    string `json:"tree_id"`
	Message   string `json:"message"`
	Timestamp string `json:"timestamp"`
	URL       string `json:"url"`
	Author    Author  `json:"author"`
	Committer Author  `json:"committer"`
}

// Author 表示提交作者信息
type Author struct {
	Name  string `json:"name"`
	Email string `json:"email"`
	Date  string `json:"date"`
}

// CreateBranchOptions 表示创建分支的参数
type CreateBranchOptions struct {
	BranchName string `json:"branch_name"`
	Ref        string `json:"ref"`
}

// ListBranches 列出仓库的分支
func (api *BranchAPI) ListBranches(owner, repo string) ([]Branch, error) {
	path := fmt.Sprintf("/repos/%s/%s/branches", owner, repo)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var branches []Branch
	if err := json.Unmarshal(resp, &branches); err != nil {
		return nil, fmt.Errorf("解析分支列表失败: %w", err)
	}
	
	return branches, nil
}

// GetBranch 获取特定分支的详细信息
func (api *BranchAPI) GetBranch(owner, repo, branch string) (*Branch, error) {
	path := fmt.Sprintf("/repos/%s/%s/branches/%s", owner, repo, branch)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var branchInfo Branch
	if err := json.Unmarshal(resp, &branchInfo); err != nil {
		return nil, fmt.Errorf("解析分支详情失败: %w", err)
	}
	
	return &branchInfo, nil
}

// CreateBranch 创建新分支
func (api *BranchAPI) CreateBranch(owner, repo, branch, ref string) (*Branch, error) {
	path := fmt.Sprintf("/repos/%s/%s/branches", owner, repo)
	options := CreateBranchOptions{
		BranchName: branch,
		Ref:        ref,
	}
	
	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var branchInfo Branch
	if err := json.Unmarshal(resp, &branchInfo); err != nil {
		return nil, fmt.Errorf("解析新分支信息失败: %w", err)
	}
	
	return &branchInfo, nil
}

// DeleteBranch 删除分支
func (api *BranchAPI) DeleteBranch(owner, repo, branch string) error {
	path := fmt.Sprintf("/repos/%s/%s/branches/%s", owner, repo, branch)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// ProtectBranch 设置分支保护
func (api *BranchAPI) ProtectBranch(owner, repo, branch string, options map[string]interface{}) error {
	path := fmt.Sprintf("/repos/%s/%s/branches/%s/protection", owner, repo, branch)
	_, err := api.Client.PUT(path, nil, options)
	return err
}

// RemoveProtection 移除分支保护
func (api *BranchAPI) RemoveProtection(owner, repo, branch string) error {
	path := fmt.Sprintf("/repos/%s/%s/branches/%s/protection", owner, repo, branch)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// GetProtection 获取分支保护规则
func (api *BranchAPI) GetProtection(owner, repo, branch string) (map[string]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/branches/%s/protection", owner, repo, branch)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var protection map[string]interface{}
	if err := json.Unmarshal(resp, &protection); err != nil {
		return nil, fmt.Errorf("解析分支保护规则失败: %w", err)
	}
	
	return protection, nil
}

// IsBranchProtected 检查分支是否受保护
func (api *BranchAPI) IsBranchProtected(owner, repo, branch string) (bool, error) {
	branchInfo, err := api.GetBranch(owner, repo, branch)
	if err != nil {
		return false, err
	}
	
	return branchInfo.Protected, nil
}

// MergeBranch 合并分支
func (api *BranchAPI) MergeBranch(owner, repo, base, head string, message string) (map[string]interface{}, error) {
	path := fmt.Sprintf("/repos/%s/%s/merges", owner, repo)
	options := map[string]string{
		"base": base,
		"head": head,
	}
	
	if message != "" {
		options["commit_message"] = message
	}
	
	resp, err := api.Client.POST(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var result map[string]interface{}
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析合并结果失败: %w", err)
	}
	
	return result, nil
} 