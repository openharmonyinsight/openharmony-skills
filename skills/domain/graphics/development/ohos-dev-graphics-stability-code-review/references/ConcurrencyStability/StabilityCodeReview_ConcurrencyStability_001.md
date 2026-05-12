---
rule_id: "StabilityCodeReview_ConcurrencyStability_001"
name: "RenderNodeDrawable全局变量写入问题"
category: "并发稳定性"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# RenderNodeDrawable全局变量写入问题

## 问题描述

RenderNodeDrawable是渲染系统中的关键组件，在多线程渲染场景下，应避免写入全局变量。若必须使用全局变量，则应加锁保护避免并发问题。渲染线程可能并发执行，对全局变量的无锁写入会导致数据竞争、渲染异常、画面闪烁等严重问题。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：RenderNodeDrawable中写入全局变量
class RenderNodeDrawable {
public:
    void Draw() {
        g_renderCount++;  // 危险：多线程并发写入全局计数
        ProcessDraw();
    }
private:
    void ProcessDraw() {
        g_currentDrawable = this;  // 危险：多线程并发设置全局指针
    }
};

// 错误示例2：修改全局容器
class RenderNodeDrawable {
public:
    void Draw() {
        g_drawableList.push_back(this);  // 危险：多线程并发push
        Render();
    }
    
    void Clear() {
        g_drawableList.clear();  // 危险：多线程并发clear
    }
};

// 错误示例3：写入静态成员变量
class RenderNodeDrawable {
public:
    static int s_totalNodes;
    
    void Draw() {
        s_totalNodes++;  // 危险：多线程并发修改静态成员
    }
};

// 错误示例4：全局缓存写入
class RenderNodeDrawable {
public:
    void Draw() {
        g_cache[key] = value;  // 危险：多线程并发写入全局缓存
        UseCache();
    }
};

// 错误示例5：回调中写入全局状态
class RenderNodeDrawable {
public:
    void OnRenderComplete() {
        g_lastRenderTime = GetCurrentTime();  // 危险：回调可能并发执行
        g_renderStatus = "completed";  // 危险：多线程并发写入
    }
};

// 错误示例6：全局资源池修改
class RenderNodeDrawable {
public:
    void AllocateResource() {
        g_resourcePool.erase(id);  // 危险：多线程并发erase
        allocated_ = true;
    }
};
```

### ✅ 修复方案

```cpp
// 正确示例1：使用成员变量替代全局变量
class RenderNodeDrawable {
public:
    void Draw() {
        renderCount_++;  // 安全：使用成员变量
        ProcessDraw();
    }
private:
    int renderCount_ = 0;  // 每个实例独立计数
};

// 正确示例2：使用mutex保护全局变量
class RenderNodeDrawable {
public:
    void Draw() {
        {
            std::lock_guard<std::mutex> lock(g_renderMutex);
            g_renderCount++;  // 安全：有锁保护
        }
        ProcessDraw();
    }
};

// 正确示例3：使用atomic计数器
std::atomic<int> g_atomicRenderCount{0};

class RenderNodeDrawable {
public:
    void Draw() {
        g_atomicRenderCount.fetch_add(1, std::memory_order_relaxed);  // 安全：atomic操作
        ProcessDraw();
    }
};

// 正确示例4：使用thread_local变量
thread_local int t_localCounter = 0;

class RenderNodeDrawable {
public:
    void Draw() {
        t_localCounter++;  // 安全：thread_local变量
        ProcessDraw();
    }
};

// 正确示例5：使用线程安全容器
class RenderNodeDrawable {
public:
    void Draw() {
        std::lock_guard<std::mutex> lock(g_listMutex);
        g_drawableList.push_back(this);  // 安全：有锁保护
        Render();
    }
};

// 正确示例6：使用局部变量和返回值
class RenderNodeDrawable {
public:
    RenderStats GetStats() const {
        return stats_;  // 安全：返回局部状态
    }
private:
    RenderStats stats_;  // 成员变量，线程安全
};

// 正确示例7：避免全局状态，使用参数传递
class RenderNodeDrawable {
public:
    void Draw(RenderContext& context) {
        context.nodeCount++;  // 安全：context由调用者管理
        ProcessDraw(context);
    }
};

// 正确示例8：静态atomic成员是线程安全的
class RenderNodeDrawable {
public:
    static inline std::atomic<int> totalProcessedNodeCount_{0};
    
    static void TotalProcessedNodeCountInc()
    {
        totalProcessedNodeCount_++;  // 安全：静态atomic成员，无需额外锁
    }
    
    static int GetTotalProcessedNodeCount()
    {
        return totalProcessedNodeCount_.load();
    }
};

// 正确示例9：静态成员使用mutex保护
class RenderNodeDrawable {
public:
    static inline std::mutex drawingCacheInfoMutex_;
    static inline std::unordered_map<NodeId, std::pair<RectI, int32_t>> drawingCacheInfos_;
    
    void UpdateCacheInfo(NodeId id, const RectI& rect)
    {
        std::lock_guard<std::mutex> lock(drawingCacheInfoMutex_);
        drawingCacheInfos_[id] = {rect, 0};  // 安全：静态mutex保护静态数据
    }
};

// 正确示例10：thread_local静态成员，每个线程独立
class RenderNodeDrawable {
public:
    static thread_local bool isOpDropped_;
    static thread_local bool occlusionCullingEnabled_;
    static thread_local inline int processedNodeCount_ = 0;
    
    void Draw() {
        processedNodeCount_++;  // 安全：thread_local，每个渲染线程独立计数
        isOpDropped_ = false;  // 安全：thread_local
        ProcessDraw();
    }
};
```

## 检测范围

检查以下场景：

1. RenderNodeDrawable类中写入全局变量(g_开头)
2. RenderNodeDrawable类中写入静态成员变量(s_开头)
3. RenderNodeDrawable修改全局容器
4. 渲染回调函数中写入全局状态
5. RenderNodeDrawable::Draw等渲染函数中的全局写入

## 检测要点

1. 识别RenderNodeDrawable类/结构体
2. 检测全局变量写入（g_变量赋值、++等）
3. 检测静态成员变量写入
4. 检测全局容器修改操作
5. 检查是否有mutex保护

### 静态成员变量处理方式

静态成员变量需要与全局变量同等对待，根据类型选择保护策略：

- **静态atomic成员**：线程安全，无需额外锁
  ```cpp
  static inline std::atomic<int> totalProcessedNodeCount_{0};
  totalProcessedNodeCount_++;  // 安全
  ```

- **静态普通成员**：需要静态mutex保护
  ```cpp
  static inline std::mutex drawingCacheInfoMutex_;
  static inline std::unordered_map<NodeId, ...> drawingCacheInfos_;
  // 使用静态mutex保护静态数据
  ```

- **thread_local静态成员**：每个线程独立，无需同步
  ```cpp
  static thread_local int processedNodeCount_ = 0;
  processedNodeCount_++;  // 安全，每个线程独立
  ```

### thread_local作为最佳实践

thread_local在渲染系统中的典型应用：

- **渲染线程独立状态**：
  - 每个渲染线程的计数器
  - 渲染线程的配置标志
  - 性能追踪的临时数据

- **优势**：
  - 完全避免同步开销
  - 性能与普通变量相同
  - 适用于高频访问的数据

- **适用数据类型**：
  - bool：状态标志（如isOpDropped_）
  - int：计数器（如processedNodeCount_）
  - 复杂类型：线程独立的缓存

### 场景分类细化

- **实例成员**：默认线程安全（单线程访问该实例）
- **静态atomic成员**：线程安全，无需额外保护
- **静态普通成员**：需要静态mutex保护
- **thread_local静态成员**：每个线程独立，无需同步
- **全局变量**：需要全局mutex保护或使用atomic

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: RenderNodeDrawable中写入全局变量
- **RISK_TYPE**: 并发风险、数据竞争
- **RISK_PATH**: 多线程并发写入全局变量 -> 数据竞争 -> 渲染状态不一致
- **IMPACT_POINT**: 渲染错误、画面闪烁、程序崩溃

## 影响分析（ImpactAnalysis）

- **Trigger**: 多个渲染线程同时写入全局变量
- **Propagation**: 数据竞争导致状态不一致
- **Consequence**: 渲染错误、画面闪烁、程序崩溃
- **Mitigation**: 使用mutex保护，或改用thread_local/成员变量

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有锁保护 | 存在 lock_guard 等 | 不报 |
| 使用atomic | 变量类型为 std::atomic | 不报 |
| thread_local | thread_local 关键字 | 不报 |
| 只读全局变量 | 仅读取，不写入 | 不报 |
| 单线程场景 | 明确注释说明单线程 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
class RenderNodeDrawable {
public:
    void Draw() {
        g_renderCount++;  // 应该报：全局变量无锁写入
    }
    
    void Process() {
        g_drawableList.push_back(this);  // 应该报：全局容器无锁修改
    }
    
    static int s_totalNodes;
    void Count() {
        s_totalNodes++;  // 应该报：静态成员无锁写入
    }
};

int g_renderCount = 0;
std::vector<RenderNodeDrawable*> g_drawableList;
```

### 安全用例（不应该报）

```cpp
std::atomic<int> g_atomicRenderCount{0};

class RenderNodeDrawable {
public:
    void Draw() {
        g_atomicRenderCount++;  // 安全：使用atomic
    }
};

class RenderNodeDrawable {
public:
    void Draw() {
        std::lock_guard<std::mutex> lock(g_mutex);
        g_renderCount++;  // 安全：有锁保护
    }
};

thread_local int t_localCounter = 0;
class RenderNodeDrawable {
public:
    void Draw() {
        t_localCounter++;  // 安全：thread_local
    }
};

class RenderNodeDrawable {
public:
    void Draw() {
        renderCount_++;  // 安全：成员变量
    }
private:
    int renderCount_ = 0;
};

// NOPROTECT: 单线程渲染
void InitGlobal() {
    g_renderCount = 0;  // 不报：明确标记单线程
}
```