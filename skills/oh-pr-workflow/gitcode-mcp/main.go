package main

import (
	"log"
	
	"github.com/joho/godotenv"
	
	"github.com/gitcode-org-com/gitcode-mcp/config"
	"github.com/gitcode-org-com/gitcode-mcp/mcp"
)

func init() {
	// 只加载.env文件
	err := godotenv.Load()
	if err != nil {
		log.Println("未找到.env文件，将使用环境变量或默认配置")
	}

	// 初始化配置
	if err := config.Init(); err != nil {
		log.Printf("初始化配置失败: %v，将使用默认配置\n", err)
	}

	// 初始化缓存
	config.InitCache()
}

func main() {
	log.Println("正在启动GitCode MCP服务器...")
	
	// 创建令牌管理器
	tokenManager := mcp.NewConfigTokenManager()
	
	// 获取默认配置选项
	options := mcp.DefaultMCPOptions()
	options.TokenManager = tokenManager
	
	// 创建并初始化MCP服务器
	server, err := mcp.NewMCPServer(options)
	if err != nil {
		log.Fatalf("初始化MCP服务器失败: %v", err)
	}
	
	// 启动服务器
	if err := mcp.Run(server, options); err != nil {
		log.Fatalf("启动MCP服务器失败: %v", err)
	}
} 