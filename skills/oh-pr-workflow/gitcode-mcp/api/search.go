package api

import (
	"encoding/json"
	"fmt"
	"net/url"
)

// SearchResult 表示通用搜索结果
type SearchResult struct {
	TotalCount int             `json:"total_count"`
	Items      json.RawMessage `json:"items"`
}

// CodeSearchResult 表示代码搜索结果
type CodeSearchResult struct {
	TotalCount int         `json:"total_count"`
	Items      []CodeMatch `json:"items"`
}

// CodeMatch 表示代码匹配
type CodeMatch struct {
	Name        string     `json:"name"`
	Path        string     `json:"path"`
	HTMLURL     string     `json:"html_url"`
	Repository  Repository `json:"repository"`
	Score       float64    `json:"score"`
	TextMatches []TextMatch `json:"text_matches"`
}

// TextMatch 表示文本匹配
type TextMatch struct {
	Fragment  string `json:"fragment"`
	Matches   []MatchInfo `json:"matches"`
}

// MatchInfo 表示匹配信息
type MatchInfo struct {
	Text     string `json:"text"`
	Indices  []int  `json:"indices"`
}

// SearchCode 搜索代码
func (api *SearchAPI) SearchCode(query string) (*CodeSearchResult, error) {
	values := url.Values{}
	values.Set("q", query)
	
	resp, err := api.Client.GET("/search/code", values)
	if err != nil {
		return nil, err
	}
	
	var result CodeSearchResult
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析代码搜索结果失败: %w", err)
	}
	
	return &result, nil
}

// SearchRepositories 搜索仓库
func (api *SearchAPI) SearchRepositories(query string) ([]Repository, error) {
	values := url.Values{}
	values.Set("q", query)
	
	resp, err := api.Client.GET("/search/repositories", values)
	if err != nil {
		return nil, err
	}
	
	var result struct {
		TotalCount int          `json:"total_count"`
		Items      []Repository `json:"items"`
	}
	
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析仓库搜索结果失败: %w", err)
	}
	
	return result.Items, nil
}

// SearchIssues 搜索Issues
func (api *SearchAPI) SearchIssues(query string) ([]Issue, error) {
	values := url.Values{}
	values.Set("q", query)
	
	resp, err := api.Client.GET("/search/issues", values)
	if err != nil {
		return nil, err
	}
	
	var result struct {
		TotalCount int     `json:"total_count"`
		Items      []Issue `json:"items"`
	}
	
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析Issues搜索结果失败: %w", err)
	}
	
	return result.Items, nil
}

// SearchUsers 搜索用户
func (api *SearchAPI) SearchUsers(query string) ([]User, error) {
	values := url.Values{}
	values.Set("q", query)
	
	resp, err := api.Client.GET("/search/users", values)
	if err != nil {
		return nil, err
	}
	
	var result struct {
		TotalCount int    `json:"total_count"`
		Items      []User `json:"items"`
	}
	
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析用户搜索结果失败: %w", err)
	}
	
	return result.Items, nil
}

// SearchCommits 搜索提交
func (api *SearchAPI) SearchCommits(query string) ([]interface{}, error) {
	values := url.Values{}
	values.Set("q", query)
	
	resp, err := api.Client.GET("/search/commits", values)
	if err != nil {
		return nil, err
	}
	
	var result struct {
		TotalCount int           `json:"total_count"`
		Items      []interface{} `json:"items"`
	}
	
	if err := json.Unmarshal(resp, &result); err != nil {
		return nil, fmt.Errorf("解析提交搜索结果失败: %w", err)
	}
	
	return result.Items, nil
}

// SearchLabels 搜索标签
func (api *SearchAPI) SearchLabels(owner, repo, query string) ([]Label, error) {
	path := fmt.Sprintf("/repos/%s/%s/labels", owner, repo)
	values := url.Values{}
	
	if query != "" {
		values.Set("q", query)
	}
	
	resp, err := api.Client.GET(path, values)
	if err != nil {
		return nil, err
	}
	
	var labels []Label
	if err := json.Unmarshal(resp, &labels); err != nil {
		return nil, fmt.Errorf("解析标签搜索结果失败: %w", err)
	}
	
	return labels, nil
} 