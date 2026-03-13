package config

import (
	"sync"
	"time"
)

// 缓存项结构体
type CacheItem struct {
	Value      interface{} // 缓存的值
	Expiration time.Time   // 过期时间
}

// 缓存管理器
type CacheManager struct {
	mu    sync.RWMutex          // 读写锁
	items map[string]*CacheItem // 缓存项映射
	ttl   time.Duration         // 默认TTL
}

// 创建新的缓存管理器
func NewCacheManager() *CacheManager {
	// 使用5分钟的固定TTL
	cacheTTL := 5 * time.Minute
	
	return &CacheManager{
		items: make(map[string]*CacheItem),
		ttl:   cacheTTL,
	}
}

// 设置缓存项
func (c *CacheManager) Set(key string, value interface{}) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	expiration := time.Now().Add(c.ttl)
	item := &CacheItem{
		Value:      value,
		Expiration: expiration,
	}
	
	// 添加新的缓存项
	c.items[key] = item
}

// 获取缓存项
func (c *CacheManager) Get(key string) (interface{}, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	
	item, found := c.items[key]
	if !found {
		return nil, false
	}
	
	// 如果已过期，则返回未找到
	if time.Now().After(item.Expiration) {
		return nil, false
	}
	
	return item.Value, true
}

// 删除缓存项
func (c *CacheManager) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	delete(c.items, key)
}

// 清空所有缓存项
func (c *CacheManager) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	c.items = make(map[string]*CacheItem)
}

// 全局缓存管理器实例
var GlobalCache *CacheManager

// 初始化缓存管理器
func InitCache() {
	GlobalCache = NewCacheManager()
} 