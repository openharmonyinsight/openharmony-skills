package mcp

import (
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/mark3labs/mcp-go/server"

	"github.com/gitcode-org-com/gitcode-mcp/api"
	"github.com/gitcode-org-com/gitcode-mcp/config"
	"github.com/gitcode-org-com/gitcode-mcp/mcp/prompts"
	"github.com/gitcode-org-com/gitcode-mcp/mcp/tools"
)

// MCPServerOptions 服务器配置选项
type MCPServerOptions struct {
	Name         string
	Version      string
	Transport    string
	ServerPort   int
	TokenManager TokenManager
}

// TokenManager 定义令牌管理器接口
type TokenManager interface {
	GetToken() string
}

// DefaultMCPOptions 创建默认的MCP服务器选项
func DefaultMCPOptions() MCPServerOptions {
	return MCPServerOptions{
		Name:       "GitCode MCP",
		Version:    "1.0.0",
		Transport:  config.GlobalConfig.MCPTransport,
		ServerPort: config.GlobalConfig.MCPSSEPort,
	}
}

// NewMCPServer 创建并初始化MCP服务器
func NewMCPServer(options MCPServerOptions) (*server.MCPServer, error) {
	// 创建GitCode API客户端
	token := ""
	if options.TokenManager != nil {
		token = options.TokenManager.GetToken()
	}
	
	apiClient, err := api.NewGitCodeAPI(token)
	if err != nil {
		return nil, fmt.Errorf("创建API客户端失败: %w", err)
	}

	// 创建MCP服务器
	s := server.NewMCPServer(
		options.Name,
		options.Version,
	)

	// 注册所有工具
	tools.RegisterAllTools(s, apiClient)

	// 注册提示模板
	prompts.AddPrompts(s, apiClient)

	return s, nil
}

// Run 启动MCP服务器
func Run(s *server.MCPServer, options MCPServerOptions) error {
	// 根据传输方式启动服务器
	switch strings.ToLower(options.Transport) {
	case "sse":
		address := fmt.Sprintf(":%d", options.ServerPort)
		log.Printf("GitCode MCP服务器将在 http://localhost%s 上启动 (SSE模式)\n", address)
		
		// 创建SSE服务器
		sseServer := server.NewSSEServer(s)
		
		// 设置HTTP服务器
		httpServer := &http.Server{
			Addr:    address,
			Handler: sseServer,
		}
		
		// 启动HTTP服务器
		return httpServer.ListenAndServe()
	default:
		log.Println("GitCode MCP服务器已启动 (STDIO模式)")
		return server.ServeStdio(s)
	}
} 