package config

import (
	"fmt"
	"log"
	"os"
	"strconv"
)

// 配置结构体
type Config struct {
	// GitCode API配置
	GitCodeToken  string // GitCode API访问令牌
	GitCodeAPIURL string // GitCode API基础URL
	APITimeout    int    // API请求超时时间（秒）

	// MCP配置
	MCPTransport string // MCP传输方式 (stdio或sse)
	MCPSSEPort   int    // SSE服务器端口
}

// 默认配置值
var defaultConfig = Config{
	GitCodeAPIURL: "https://api.gitcode.com/api/v5",
	MCPTransport:  "stdio",
	MCPSSEPort:    8000,
	APITimeout:    30,
}

// 全局配置实例
var GlobalConfig Config

// 初始化配置
func Init() error {
	// 默认使用默认配置
	GlobalConfig = defaultConfig

	// 从环境变量读取配置，如果未设置，使用默认值
	if token := os.Getenv("GITCODE_TOKEN"); token != "" {
		GlobalConfig.GitCodeToken = token
	}

	if apiURL := os.Getenv("GITCODE_API_URL"); apiURL != "" {
		GlobalConfig.GitCodeAPIURL = apiURL
	}

	if transport := os.Getenv("MCP_TRANSPORT"); transport != "" {
		GlobalConfig.MCPTransport = transport
	}

	if ssePort := os.Getenv("MCP_SSE_PORT"); ssePort != "" {
		if port, err := strconv.Atoi(ssePort); err == nil {
			GlobalConfig.MCPSSEPort = port
		}
	}
	
	if apiTimeout := os.Getenv("API_TIMEOUT"); apiTimeout != "" {
		if timeout, err := strconv.Atoi(apiTimeout); err == nil {
			GlobalConfig.APITimeout = timeout
		}
	}

	// 验证配置
	return validateConfig()
}

// 验证配置
func validateConfig() error {
	// 验证GitCode API令牌
	if GlobalConfig.GitCodeToken == "" {
		log.Println("警告: 未设置GitCode API令牌，某些功能可能无法正常工作")
	}

	// 验证SSE服务器端口范围
	if GlobalConfig.MCPTransport == "sse" && (GlobalConfig.MCPSSEPort <= 0 || GlobalConfig.MCPSSEPort > 65535) {
		return fmt.Errorf("SSE服务器端口配置无效: %d，有效范围为1-65535", GlobalConfig.MCPSSEPort)
	}

	return nil
} 