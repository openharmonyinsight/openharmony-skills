package api

import (
	"bytes"
	"crypto/md5"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"time"
	
	"github.com/gitcode-org-com/gitcode-mcp/config"
)

// 错误类型
var (
	ErrAuthFailed      = errors.New("认证失败")
	ErrPermissionDenied = errors.New("权限不足")
	ErrNotFound        = errors.New("资源不存在")
	ErrValidation      = errors.New("参数验证失败")
	ErrRateLimit       = errors.New("API请求频率限制")
	ErrServer          = errors.New("服务器错误")
	ErrUnknown         = errors.New("未知错误")
)

// APIError 表示API错误
type APIError struct {
	Code    int    // HTTP状态码
	Message string // 错误信息
	Err     error  // 底层错误
}

// Error 实现Error接口
func (e *APIError) Error() string {
	return fmt.Sprintf("API错误 [%d]: %s - %v", e.Code, e.Message, e.Err)
}

// Unwrap 返回底层错误
func (e *APIError) Unwrap() error {
	return e.Err
}

// GitCodeAPI 表示GitCode API客户端
type GitCodeAPI struct {
	Token       string
	BaseURL     string
	Timeout     time.Duration
	HTTPClient  *http.Client
	
	// API子模块
	Repos      *RepositoryAPI
	Branches   *BranchAPI
	Issues     *IssueAPI
	Pulls      *PullRequestAPI
	Search     *SearchAPI
}

// NewGitCodeAPI 创建一个新的GitCode API客户端
func NewGitCodeAPI(token string) (*GitCodeAPI, error) {
	// 如果未提供token，则使用配置中的token
	if token == "" {
		token = config.GlobalConfig.GitCodeToken
		if token == "" {
			return nil, errors.New("GitCode令牌未提供。请设置GITCODE_TOKEN环境变量或在初始化时提供token参数")
		}
	}
	
	timeout := time.Duration(config.GlobalConfig.APITimeout) * time.Second
	baseURL := config.GlobalConfig.GitCodeAPIURL
	
	client := &GitCodeAPI{
		Token:      token,
		BaseURL:    baseURL,
		Timeout:    timeout,
		HTTPClient: &http.Client{
			Timeout: timeout,
		},
	}
	
	// 初始化API子模块
	client.Repos = NewRepositoryAPI(client)
	client.Branches = NewBranchAPI(client)
	client.Issues = NewIssueAPI(client)
	client.Pulls = NewPullRequestAPI(client)
	client.Search = NewSearchAPI(client)
	
	return client, nil
}

// buildURL 构建完整的API URL
func (c *GitCodeAPI) buildURL(path string, params url.Values) string {
	u := fmt.Sprintf("%s%s", c.BaseURL, path)
	
	if params != nil && len(params) > 0 {
		u = fmt.Sprintf("%s?%s", u, params.Encode())
	}
	
	return u
}

// 生成缓存键
func (c *GitCodeAPI) generateCacheKey(method, url string, body interface{}) string {
	// 创建唯一的缓存键
	key := fmt.Sprintf("%s:%s", method, url)
	
	// 如果有请求体，将其添加到键中
	if body != nil {
		jsonData, err := json.Marshal(body)
		if err == nil {
			hash := md5.Sum(jsonData)
			key = fmt.Sprintf("%s:%x", key, hash)
		}
	}
	return key
}

// Request 发送API请求
func (c *GitCodeAPI) Request(method, path string, params url.Values, body interface{}) ([]byte, error) {
	url := c.buildURL(path, params)
	
	// 对于GET请求，尝试从缓存获取
	cacheKey := c.generateCacheKey(method, url, body)
	if method == "GET" {
		if cachedData, found := config.GlobalCache.Get(cacheKey); found {
			log.Printf("从缓存获取: %s %s", method, url)
			return cachedData.([]byte), nil
		}
	}
	
	var bodyReader io.Reader
	if body != nil {
		jsonData, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("序列化请求体失败: %w", err)
		}
		bodyReader = bytes.NewBuffer(jsonData)
	}
	
	req, err := http.NewRequest(method, url, bodyReader)
	if err != nil {
		return nil, fmt.Errorf("创建请求失败: %w", err)
	}
	
	// 设置请求头
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.Token))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", "GitCode-MCP-Go-Client/1.0.0")
	
	log.Printf("API请求: %s %s", method, url)
	
	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("HTTP请求失败: %w", err)
	}
	defer resp.Body.Close()
	
	// 读取响应体
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("读取响应体失败: %w", err)
	}
	
	// 处理响应状态码
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		// 对于GET请求，缓存响应
		if method == "GET" {
			config.GlobalCache.Set(cacheKey, respBody)
		}
		return respBody, nil
	}
	
	// 解析错误信息
	var errorMessage string
	var errorResponse map[string]interface{}
	if err := json.Unmarshal(respBody, &errorResponse); err == nil {
		if msg, ok := errorResponse["message"].(string); ok {
			errorMessage = msg
		} else {
			errorMessage = string(respBody)
		}
	} else {
		errorMessage = string(respBody)
	}
	
	// 根据状态码创建特定错误
	var apiErr *APIError
	switch resp.StatusCode {
	case http.StatusUnauthorized: // 401
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrAuthFailed}
	case http.StatusForbidden: // 403
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrPermissionDenied}
	case http.StatusNotFound: // 404
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrNotFound}
	case http.StatusUnprocessableEntity: // 422
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrValidation}
	case http.StatusTooManyRequests: // 429
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrRateLimit}
	case http.StatusInternalServerError, http.StatusBadGateway, http.StatusServiceUnavailable: // 500, 502, 503
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrServer}
	default:
		apiErr = &APIError{Code: resp.StatusCode, Message: errorMessage, Err: ErrUnknown}
	}
	
	return nil, apiErr
}

// GET 发送GET请求
func (c *GitCodeAPI) GET(path string, params url.Values) ([]byte, error) {
	return c.Request("GET", path, params, nil)
}

// POST 发送POST请求
func (c *GitCodeAPI) POST(path string, params url.Values, body interface{}) ([]byte, error) {
	return c.Request("POST", path, params, body)
}

// PUT 发送PUT请求
func (c *GitCodeAPI) PUT(path string, params url.Values, body interface{}) ([]byte, error) {
	return c.Request("PUT", path, params, body)
}

// DELETE 发送DELETE请求
func (c *GitCodeAPI) DELETE(path string, params url.Values) ([]byte, error) {
	return c.Request("DELETE", path, params, nil)
}

// PATCH 发送PATCH请求
func (c *GitCodeAPI) PATCH(path string, params url.Values, body interface{}) ([]byte, error) {
	return c.Request("PATCH", path, params, body)
}

// BaseAPI 所有API模块的基类
type BaseAPI struct {
	Client *GitCodeAPI
}

// 各API子模块的前向声明
type RepositoryAPI struct {
	BaseAPI
}

type BranchAPI struct {
	BaseAPI
}

type IssueAPI struct {
	BaseAPI
}

type PullRequestAPI struct {
	BaseAPI
}

type SearchAPI struct {
	BaseAPI
}

// 创建各API子模块的实例
func NewRepositoryAPI(client *GitCodeAPI) *RepositoryAPI {
	return &RepositoryAPI{BaseAPI{Client: client}}
}

func NewBranchAPI(client *GitCodeAPI) *BranchAPI {
	return &BranchAPI{BaseAPI{Client: client}}
}

func NewIssueAPI(client *GitCodeAPI) *IssueAPI {
	return &IssueAPI{BaseAPI{Client: client}}
}

func NewPullRequestAPI(client *GitCodeAPI) *PullRequestAPI {
	return &PullRequestAPI{BaseAPI{Client: client}}
}

func NewSearchAPI(client *GitCodeAPI) *SearchAPI {
	return &SearchAPI{BaseAPI{Client: client}}
} 