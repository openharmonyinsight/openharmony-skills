package tools

import (
	"github.com/mark3labs/mcp-go/server"
	
	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// RegisterAllTools 注册所有工具到MCP服务器
func RegisterAllTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	// 注册仓库相关工具
	AddRepositoryTools(s, apiClient)
	
	// 注册分支相关工具
	AddBranchTools(s, apiClient)
	
	// 注册Issue相关工具
	AddIssueTools(s, apiClient)
	
	// 注册Pull Request相关工具
	AddPullRequestTools(s, apiClient)
	
	// 注册搜索相关工具
	AddSearchTools(s, apiClient)

	// 注册用户相关工具
	AddUserTools(s, apiClient)
} 