package tools

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"

	"github.com/gitcode-org-com/gitcode-mcp/api"
)

// AddUserTools adds user-related tools to the MCP server
func AddUserTools(s *server.MCPServer, apiClient *api.GitCodeAPI) {
	getUserTool := mcp.NewTool("get_authenticated_user",
		mcp.WithDescription("获取当前认证用户信息（登录名、姓名、邮箱）"),
	)
	s.AddTool(getUserTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		user, err := apiClient.GetAuthenticatedUser()
		if err != nil {
			return nil, fmt.Errorf("获取用户信息失败: %w", err)
		}
		return FormatJSONResult(user)
	})
}
