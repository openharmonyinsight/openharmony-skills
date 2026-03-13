package mcp

import (
	"os"
	"sync"

	"github.com/gitcode-org-com/gitcode-mcp/config"
)

// ConfigTokenManager 基于配置的令牌管理器
type ConfigTokenManager struct {
	mu    sync.RWMutex
	token string
}

// NewConfigTokenManager 创建基于配置的令牌管理器
func NewConfigTokenManager() *ConfigTokenManager {
	return &ConfigTokenManager{
		token: config.GlobalConfig.GitCodeToken,
	}
}

// GetToken 获取令牌
func (m *ConfigTokenManager) GetToken() string {
	m.mu.RLock()
	defer m.mu.RUnlock()
	
	// 优先使用环境变量中的令牌
	if envToken := os.Getenv("GITCODE_TOKEN"); envToken != "" {
		return envToken
	}
	
	return m.token
}

// SetToken 设置令牌
func (m *ConfigTokenManager) SetToken(token string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	
	m.token = token
} 