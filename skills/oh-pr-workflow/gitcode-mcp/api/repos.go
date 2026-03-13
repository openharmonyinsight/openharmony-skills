package api

import (
	"encoding/json"
	"fmt"
)

// Repository 表示仓库信息
type Repository struct {
	ID              json.RawMessage `json:"id"`
	Name            string          `json:"name"`
	FullName        string          `json:"full_name"`
	Owner           User            `json:"owner"`
	Private         bool            `json:"private"`
	HTMLUrl         string          `json:"html_url"`
	Description     string          `json:"description"`
	Fork            bool            `json:"fork"`
	URL             string          `json:"url"`
	DefaultBranch   string          `json:"default_branch"`
	CreatedAt       string          `json:"created_at"`
	UpdatedAt       string          `json:"updated_at"`
	StargazersCount FlexInt         `json:"stargazers_count"`
	ForksCount      FlexInt         `json:"forks_count"`
}

// User 表示用户信息
type User struct {
	ID        json.RawMessage `json:"id"`
	Username  string          `json:"username"`
	Name      string          `json:"name"`
	AvatarURL string          `json:"avatar_url"`
	Email     string          `json:"email"`
	URL       string          `json:"url"`
}

// CreateRepoOptions 表示创建仓库的参数
type CreateRepoOptions struct {
	Name        string `json:"name"`
	Description string `json:"description,omitempty"`
	Private     bool   `json:"private,omitempty"`
	AutoInit    bool   `json:"auto_init,omitempty"`
}

// ListUserRepos 列出当前用户的仓库
func (api *RepositoryAPI) ListUserRepos() ([]Repository, error) {
	path := "/user/repos"
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var repos []Repository
	if err := json.Unmarshal(resp, &repos); err != nil {
		return nil, fmt.Errorf("解析仓库列表失败: %w", err)
	}
	
	return repos, nil
}

// GetRepo 获取特定仓库的详细信息
func (api *RepositoryAPI) GetRepo(owner, repo string) (*Repository, error) {
	path := fmt.Sprintf("/repos/%s/%s", owner, repo)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var repository Repository
	if err := json.Unmarshal(resp, &repository); err != nil {
		return nil, fmt.Errorf("解析仓库详情失败: %w", err)
	}
	
	return &repository, nil
}

// CreateRepo 创建新仓库
func (api *RepositoryAPI) CreateRepo(name, description string, private bool) (*Repository, error) {
	options := CreateRepoOptions{
		Name:        name,
		Description: description,
		Private:     private,
		AutoInit:    true,
	}
	
	resp, err := api.Client.POST("/user/repos", nil, options)
	if err != nil {
		return nil, err
	}
	
	var repo Repository
	if err := json.Unmarshal(resp, &repo); err != nil {
		return nil, fmt.Errorf("解析新仓库信息失败: %w", err)
	}
	
	return &repo, nil
}

// ListReposByOrg 列出组织的仓库
func (api *RepositoryAPI) ListReposByOrg(org string) ([]Repository, error) {
	path := fmt.Sprintf("/orgs/%s/repos", org)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var repos []Repository
	if err := json.Unmarshal(resp, &repos); err != nil {
		return nil, fmt.Errorf("解析组织仓库列表失败: %w", err)
	}
	
	return repos, nil
}

// ListReposByUser 列出用户的仓库
func (api *RepositoryAPI) ListReposByUser(username string) ([]Repository, error) {
	path := fmt.Sprintf("/users/%s/repos", username)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var repos []Repository
	if err := json.Unmarshal(resp, &repos); err != nil {
		return nil, fmt.Errorf("解析用户仓库列表失败: %w", err)
	}
	
	return repos, nil
}

// DeleteRepo 删除仓库
func (api *RepositoryAPI) DeleteRepo(owner, repo string) error {
	path := fmt.Sprintf("/repos/%s/%s", owner, repo)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// UpdateRepo 更新仓库信息
func (api *RepositoryAPI) UpdateRepo(owner, repo string, options map[string]interface{}) (*Repository, error) {
	path := fmt.Sprintf("/repos/%s/%s", owner, repo)
	resp, err := api.Client.PATCH(path, nil, options)
	if err != nil {
		return nil, err
	}
	
	var repository Repository
	if err := json.Unmarshal(resp, &repository); err != nil {
		return nil, fmt.Errorf("解析更新后的仓库信息失败: %w", err)
	}
	
	return &repository, nil
}

// TransferRepo 转移仓库所有权
func (api *RepositoryAPI) TransferRepo(owner, repo, newOwner string) (*Repository, error) {
	path := fmt.Sprintf("/repos/%s/%s/transfer", owner, repo)
	body := map[string]string{
		"new_owner": newOwner,
	}
	
	resp, err := api.Client.POST(path, nil, body)
	if err != nil {
		return nil, err
	}
	
	var repository Repository
	if err := json.Unmarshal(resp, &repository); err != nil {
		return nil, fmt.Errorf("解析转移后的仓库信息失败: %w", err)
	}
	
	return &repository, nil
}

// ListStargazers 列出仓库的星标用户
func (api *RepositoryAPI) ListStargazers(owner, repo string) ([]User, error) {
	path := fmt.Sprintf("/repos/%s/%s/stargazers", owner, repo)
	resp, err := api.Client.GET(path, nil)
	if err != nil {
		return nil, err
	}
	
	var users []User
	if err := json.Unmarshal(resp, &users); err != nil {
		return nil, fmt.Errorf("解析星标用户列表失败: %w", err)
	}
	
	return users, nil
}

// StarRepo 为仓库添加星标
func (api *RepositoryAPI) StarRepo(owner, repo string) error {
	path := fmt.Sprintf("/user/starred/%s/%s", owner, repo)
	_, err := api.Client.PUT(path, nil, nil)
	return err
}

// UnstarRepo 取消仓库星标
func (api *RepositoryAPI) UnstarRepo(owner, repo string) error {
	path := fmt.Sprintf("/user/starred/%s/%s", owner, repo)
	_, err := api.Client.DELETE(path, nil)
	return err
}

// CheckIfStarred 检查当前用户是否已为仓库添加星标
func (api *RepositoryAPI) CheckIfStarred(owner, repo string) (bool, error) {
	path := fmt.Sprintf("/user/starred/%s/%s", owner, repo)
	_, err := api.Client.GET(path, nil)
	if err != nil {
		// 检查是否为404错误，如果是404表示未星标
		if apiErr, ok := err.(*APIError); ok && apiErr.Code == 404 {
			return false, nil
		}
		return false, err
	}
	
	return true, nil
} 