package api

import (
	"encoding/json"
	"fmt"
)

// AuthenticatedUser represents the currently authenticated user
type AuthenticatedUser struct {
	ID    json.RawMessage `json:"id"`
	Login string          `json:"login"`
	Name  string          `json:"name"`
	Email string          `json:"email"`
}

// GetAuthenticatedUser returns the current token owner's info
func (c *GitCodeAPI) GetAuthenticatedUser() (*AuthenticatedUser, error) {
	resp, err := c.GET("/user", nil)
	if err != nil {
		return nil, err
	}

	var user AuthenticatedUser
	if err := json.Unmarshal(resp, &user); err != nil {
		return nil, fmt.Errorf("解析用户信息失败: %w", err)
	}

	return &user, nil
}
