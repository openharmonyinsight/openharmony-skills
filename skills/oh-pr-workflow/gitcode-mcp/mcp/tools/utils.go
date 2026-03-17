package tools

import (
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/mark3labs/mcp-go/mcp"
)

// GetIntArg extracts an integer argument from MCP request.
// Handles both float64 (JSON number) and string types,
// since Claude Code may pass numbers as either type.
func GetIntArg(args map[string]interface{}, key string) int {
	val, ok := args[key]
	if !ok {
		return 0
	}
	switch v := val.(type) {
	case float64:
		return int(v)
	case string:
		n, err := strconv.Atoi(v)
		if err != nil {
			return 0
		}
		return n
	case json.Number:
		n, err := v.Int64()
		if err != nil {
			return 0
		}
		return int(n)
	default:
		return 0
	}
}

// FormatJSONResult 将数据格式化为JSON结果
func FormatJSONResult(data interface{}) (*mcp.CallToolResult, error) {
	// 将数据转换为JSON字符串
	jsonBytes, err := json.Marshal(data)
	if err != nil {
		return nil, fmt.Errorf("JSON编码失败: %w", err)
	}
	
	// 使用 NewToolResultText 创建结果
	return mcp.NewToolResultText(string(jsonBytes)), nil
} 