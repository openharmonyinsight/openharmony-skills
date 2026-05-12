---
rule_id: "StabilityCodeReview_BoundaryCondition_004"
name: "容器size增长的对外接口应限制上限"
category: "边界条件"
severity: "HIGH"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 容器size增长的对外接口应限制上限

## 问题描述

会导致容器size增大的对外接口，应该限制容器size的上限，防止外部恶意攻击申请过大内存。外部输入可能包含恶意构造的数据，导致容器无限增长，造成内存耗尽或拒绝服务。

## 检测示例

### ❌ 问题代码

```cpp
// 错误示例1：push_back无限制
class DataProcessor {
private:
    std::vector<int> data_;
public:
    void AddData(int value) {
        data_.push_back(value);  // 危险：无大小限制
    }
};

// 错误示例2：从外部数据源批量添加
class MessageHandler {
private:
    std::vector<Message> messages_;
public:
    void AddMessages(const std::vector<Message>& msgs) {
        for (const auto& msg : msgs) {
            messages_.push_back(msg);  // 危险：无大小限制
        }
    }
};

// 错误示例3：insert操作无限制
class ConnectionManager {
private:
    std::set<Connection*> connections_;
public:
    void AddConnection(Connection* conn) {
        connections_.insert(conn);  // 危险：无大小限制
    }
};

// 错误示例4：从Parcel读取无限制
class DataManager {
private:
    std::vector<std::string> items_;
public:
    void ReadFromParcel(Parcel& parcel) {
        int count = parcel.ReadInt32();
        for (int i = 0; i < count; i++) {
            items_.push_back(parcel.ReadString());  // 危险：count和items_都无限制
        }
    }
};

// 错误示例5：map插入无限制
class CacheManager {
private:
    std::map<int, Data> cache_;
public:
    void Insert(int key, const Data& data) {
        cache_[key] = data;  // 危险：无大小限制
    }
};

// 错误示例6：链表无限制增长
class EventQueue {
private:
    std::list<Event> events_;
public:
    void PushEvent(const Event& event) {
        events_.push_back(event);  // 危险：无大小限制
    }
};
```

### ✅ 修复方案

```cpp
// 正确示例1：添加容量限制
class DataProcessor {
private:
    std::vector<int> data_;
    static constexpr size_t MAX_DATA_SIZE = 10000;
    
public:
    bool AddData(int value) {
        if (data_.size() >= MAX_DATA_SIZE) {
            LOGE("Data size exceeded limit: %zu", MAX_DATA_SIZE);
            return false;
        }
        data_.push_back(value);
        return true;
    }
};

// 正确示例2：批量添加时检查总大小
class MessageHandler {
private:
    std::vector<Message> messages_;
    static constexpr size_t MAX_MESSAGES = 5000;
    
public:
    bool AddMessages(const std::vector<Message>& msgs) {
        if (messages_.size() + msgs.size() > MAX_MESSAGES) {
            LOGE("Message count exceeded limit");
            return false;
        }
        for (const auto& msg : msgs) {
            messages_.push_back(msg);
        }
        return true;
    }
};

// 正确示例3：连接数限制
class ConnectionManager {
private:
    std::set<Connection*> connections_;
    static constexpr size_t MAX_CONNECTIONS = 1000;
    
public:
    bool AddConnection(Connection* conn) {
        if (connections_.size() >= MAX_CONNECTIONS) {
            LOGE("Connection count exceeded limit: %zu", MAX_CONNECTIONS);
            return false;
        }
        auto result = connections_.insert(conn);
        if (!result.second) {
            LOGE("Connection already exists");
            return false;
        }
        return true;
    }
};

// 正确示例4：安全的Parcel读取
class DataManager {
private:
    std::vector<std::string> items_;
    static constexpr size_t MAX_ITEMS = 1000;
    static constexpr size_t MAX_ITEM_COUNT = 100;
    
public:
    bool ReadFromParcel(Parcel& parcel) {
        int count = parcel.ReadInt32();
        if (count < 0 || static_cast<size_t>(count) > MAX_ITEM_COUNT) {
            LOGE("Invalid count: %d", count);
            return false;
        }
        if (items_.size() + count > MAX_ITEMS) {
            LOGE("Items size exceeded limit");
            return false;
        }
        for (int i = 0; i < count; i++) {
            items_.push_back(parcel.ReadString());
        }
        return true;
    }
};

// 正确示例5：缓存大小限制
class CacheManager {
private:
    std::map<int, Data> cache_;
    static constexpr size_t MAX_CACHE_SIZE = 10000;
    
public:
    bool Insert(int key, const Data& data) {
        if (cache_.size() >= MAX_CACHE_SIZE) {
            // 可选：淘汰策略
            EvictOldest();
        }
        if (cache_.size() >= MAX_CACHE_SIZE) {
            LOGE("Cache is full");
            return false;
        }
        cache_[key] = data;
        return true;
    }
    
private:
    void EvictOldest() {
        if (!cache_.empty()) {
            cache_.erase(cache_.begin());
        }
    }
};

// 正确示例6：事件队列大小限制
class EventQueue {
private:
    std::list<Event> events_;
    static constexpr size_t MAX_QUEUE_SIZE = 10000;
    
public:
    bool PushEvent(const Event& event) {
        if (events_.size() >= MAX_QUEUE_SIZE) {
            LOGE("Event queue is full, dropping oldest event");
            events_.pop_front();
        }
        events_.push_back(event);
        return true;
    }
    
    bool PushEventNoDrop(const Event& event) {
        if (events_.size() >= MAX_QUEUE_SIZE) {
            LOGE("Event queue is full");
            return false;
        }
        events_.push_back(event);
        return true;
    }
};
```

## 检测范围

检查以下模式：

1. 公共接口中的`push_back/push_front/insert/emplace`
2. 公共接口中的容器扩展操作
3. 公共接口从外部数据源添加元素
4. 公共接口处理批量数据

## 检测要点

1. 识别`public`成员函数中的容器操作
2. 检测`push_back`, `push_front`, `insert`, `emplace`等操作
3. 检查是否进行了大小限制
4. 识别`std::vector`, `std::list`, `std::map`, `std::set`, `std::deque`等容器
5. 排除NOPROTECT标记的代码

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: 外部输入数据
- **RISK_TYPE**: 容器大小无限制
- **RISK_PATH**: 外部数据 -> 容器增长 -> 内存耗尽
- **IMPACT_POINT**: 系统资源耗尽、拒绝服务

## 影响分析（ImpactAnalysis）

- **Trigger**: 对外接口未限制容器大小增长
- **Propagation**: 恶意大量调用导致容器无限增长
- **Consequence**: 内存耗尽、程序崩溃、系统不稳定
- **Mitigation**: 添加容器大小上限检查，实现淘汰策略

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT 标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有大小检查 | 存在 size() 比较或容量检查 | 不报 |
| 私有成员函数 | 标记为 private/protected | 不报 |
| 内部工具类 | 明确标记为内部使用 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_BoundaryCondition_004_trigger.cpp
class TriggerBad1 {
    std::vector<int> data_;
public:
    void AddData(int value) {
        data_.push_back(value);  // 应该报：无大小限制
    }
};

class TriggerBad2 {
    std::map<int, std::string> cache_;
public:
    void Insert(int key, const std::string& value) {
        cache_[key] = value;  // 应该报：无大小限制
    }
};

class TriggerBad3 {
    std::list<Event> events_;
public:
    void PushEvent(const Event& event) {
        events_.push_back(event);  // 应该报：无大小限制
    }
};

class TriggerBad4 {
    std::set<int> ids_;
public:
    void AddId(int id) {
        ids_.insert(id);  // 应该报：无大小限制
    }
};
```

### 安全用例（不应该报）

```cpp
// test_BoundaryCondition_004_safe.cpp
class SafeGood1 {
    std::vector<int> data_;
    static constexpr size_t MAX_SIZE = 1000;
public:
    bool AddData(int value) {
        if (data_.size() >= MAX_SIZE) {  // 安全：有大小限制
            return false;
        }
        data_.push_back(value);
        return true;
    }
};

class SafeGood2 {
    std::vector<int> data_;
public:
    void AddData(int value) {
        if (data_.capacity() > data_.size()) {  // 安全：有容量检查
            data_.push_back(value);
        }
    }
};

class SafeGood3 {
    std::vector<int> data_;
public:
    void ClearAndAdd(int value) {  // 安全：先清空
        data_.clear();
        data_.push_back(value);
    }
};

// NOPROTECT: 内部使用，数据量可控
class NoprotectCase {
    std::vector<int> data_;
public:
    void AddData(int value) {
        data_.push_back(value);
    }
};
```