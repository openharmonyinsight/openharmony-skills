# 线程安全审查详细检查清单

本文档提供系统化的线程安全问题检查流程，用于审查 OpenHarmony C++ 系统服务代码。

## 完整检查流程

### 第一阶段：代码理解（5分钟）

1. **识别线程模型**
   - [ ] 确认代码运行在哪些线程
   - [ ] 识别线程创建点（pthread、std::thread、EventHandler等）
   - [ ] 绘制线程交互图

2. **识别共享状态**
   - [ ] 列出所有成员变量
   - [ ] 标记可能被多线程访问的变量
   - [ ] 识别跨线程传递的对象

3. **识别同步机制**
   - [ ] 列出所有使用的同步原语（mutex、rwlock、atomic等）
   - [ ] 标记每个锁保护的资源

### 第二阶段：详细检查（15分钟）

#### A. 数据竞争检查

**A1. 非原子共享变量**
```cpp
// 检查清单：
// □ 所有非原子成员变量
// □ 静态/全局变量
// □ 裸指针和引用
```

**检查步骤**：
1. 遍历所有成员变量声明
2. 对每个非原子类型，询问：
   - 是否可能被多个线程访问？
   - 是否有锁保护？
   - 锁的范围是否足够？

**常见错误模式**：
```cpp
// ❌ 错误
class Service {
    int counter_;  // 无保护
    void Increment() { counter_++; }
};

// ✓ 正确
class Service {
    std::mutex mutex_;
    int counter_;
    void Increment() {
        std::lock_guard<std::mutex> lock(mutex_);
        counter_++;
    }
};
```

**A2. STL容器使用**
```cpp
// 检查清单：
// □ std::vector, std::map 等容器的并发访问
// □ 迭代器失效问题
// □ size() 与实际访问的原子性
```

**A3. 智能指针**
```cpp
// 检查清单：
// □ shared_ptr 的引用计数是否线程安全（是）
// □ shared_ptr 指向对象的访问是否线程安全（否）
// □ weak_ptr::lock() 的返回值检查
```

#### B. 锁使用审查

**B1. RAII使用**
```cpp
// 检查清单：
// □ 所有锁都使用 lock_guard/unique_lock
// □ 没有手动 lock/unlock
// □ 异常安全性

// ❌ 危险
mutex_.lock();
// 如果抛异常，锁永远持有
DoSomething();
mutex_.unlock();

// ✓ 正确
std::lock_guard<std::mutex> lock(mutex_);
DoSomething();
// 自动释放
```

**B2. 锁粒度**
```cpp
// 检查清单：
// □ 锁的范围尽可能小
// □ 避免在持有锁时进行I/O操作
// □ 避免在持有锁时调用未知代码

// ❌ 锁粒度过大
{
    std::lock_guard<std::mutex> lock(mutex_);
    LoadDataFromNetwork();  // 耗时I/O
    ProcessData();          // 复杂计算
    SaveData();             // 更多I/O
}

// ✓ 正确：缩小锁范围
auto data = GetData();
{
    std::lock_guard<std::mutex> lock(mutex_);
    data_.push_back(data);
}
ProcessData();
```

**B3. 多锁顺序**
```cpp
// 检查清单：
// □ 所有代码路径获取多个锁的顺序一致
// □ 使用 std::lock() 避免死锁
// □ 考虑使用层级锁（hierarchical mutex）

// ❌ 死锁风险
void MethodA() {
    std::lock_guard<std::mutex> lock1(mutex1_);
    std::lock_guard<std::mutex> lock2(mutex2_);
}

void MethodB() {
    std::lock_guard<std::mutex> lock2(mutex2_);  // 顺序不同！
    std::lock_guard<std::mutex> lock1(mutex1_);
}

// ✓ 正确
void SafeLock() {
    std::lock(mutex1_, mutex2_);  // 同时避免死锁
    std::lock_guard<std::mutex> lock1(mutex1_, std::adopt_lock);
    std::lock_guard<std::mutex> lock2(mutex2_, std::adopt_lock);
}
```

**B4. 递归锁检查**
```cpp
// 检查清单：
// □ 同一线程是否递归获取锁
// □ 是否可以重新设计避免递归
// □ 如需递归，显式使用 recursive_mutex

// 检查方法：搜索同一锁的嵌套使用
void Outer() {
    std::lock_guard<std::mutex> lock(mutex_);
    Inner();  // Inner() 也获取 mutex_？
}

void Inner() {
    std::lock_guard<std::mutex> lock(mutex_);
    // ...
}
```

#### C. 临界区完整性

**C1. 检查-竞态模式**
```cpp
// 检查清单：
// □ if (检查) { 操作 } 模式
// □ 检查和操作是否在同一临界区

// ❌ Check-Then-Race
if (ptr != nullptr) {        // 线程A检查
    // 上下文切换
    ptr->Method();            // 线程A使用，可能已释放
}

// ✓ 正确
{
    std::lock_guard<std::mutex> lock(mutex_);
    if (ptr != nullptr) {
        ptr->Method();
    }
}
```

**C2. 复合操作原子性**
```cpp
// 检查清单：
// □ 多步操作是否需要原子性
// □ 不变量（invariant）的维护

// ❌ 非原子复合操作
void AddItem(Item item) {
    std::lock_guard<std::mutex> lock(mutex_);
    items_.push_back(item);
    // 锁释放
    count_++;  // 与 items_ 状态不一致
}

// ✓ 正确
void AddItem(Item item) {
    std::lock_guard<std::mutex> lock(mutex_);
    items_.push_back(item);
    count_++;
}
```

#### D. 条件变量使用

**D1. 虚假唤醒**
```cpp
// 检查清单：
// □ wait() 必须在循环中或使用谓词

// ❌ 危险
cv_.wait(lock);

// ✓ 正确：使用谓词
cv_.wait(lock, [this] { return ready_; });

// 或使用循环
while (!ready_) {
    cv_.wait(lock);
}
```

**D2. 通知时机**
```cpp
// 检查清单：
// □ notify 必须在持有锁时调用
// □ 条件设置在 notify 之前

// ❌ 错误顺序
ready_ = true;
cv_.notify_one();
// 如果 wait 还没开始，通知丢失

// ✓ 正确
{
    std::lock_guard<std::mutex> lock(mutex_);
    ready_ = true;
    cv_.notify_one();  // 持有锁时通知
}
```

#### E. OpenHarmony特定检查

**E1. EventHandler**
```cpp
// 检查清单：
// □ ProcessEvent 可能在多线程调用
// □ 事件处理中的操作是否线程安全
// □ SendEvent/PostEvent 的正确使用

class MyHandler : public OHOS::EventHandler {
    void ProcessEvent(const OHOS::InnerEvent::Pointer& event) override {
        // ❌ 未考虑线程安全
        count_++;

        // ✓ 正确
        {
            std::lock_guard<std::mutex> lock(mutex_);
            count_++;
        }
    }
private:
    int count_;
    std::mutex mutex_;
};
```

**E2. Binder回调线程**
```cpp
// 检查清单：
// □ DeathRecipient 在Binder线程调用
// □ 回调是否需要调度到业务线程

class MyDeathRecipient : public OHOS::IRemoteObject::DeathRecipient {
    void OnRemoteDied(const OHOS::wptr<OHOS::IRemoteObject>& object) override {
        // ❌ 直接访问业务对象（可能线程不安全）
        service_->Cleanup();

        // ✓ 正确：调度到业务线程
        handler_->PostTask([] { service_->Cleanup(); });
    }
};
```

**E3. 单例模式**
```cpp
// 检查清单：
// □ 懒加载单例是否线程安全
// □ 推荐使用C++11魔法静态

// ❌ 不安全
static Service* GetInstance() {
    static Service* instance = nullptr;
    if (!instance) {  // 数据竞争
        instance = new Service();
    }
    return instance;
}

// ✓ 正确：C++11保证线程安全
static Service& GetInstance() {
    static Service instance;  // 魔法静态
    return instance;
}
```

**E4. DelayedSingleton**
```cpp
// OpenHarmony常用的单例模板
// 检查清单：
// □ DelayedSingleton::GetInstance() 的线程安全
// □ 第一次调用的线程安全性
```

### 第三阶段：安全性评估（5分钟）

#### F. 死锁风险评估

**F1. 资源依赖图**
```
检查步骤：
1. 绘制锁获取关系图
2. 检查是否有循环依赖
3. 评估跨模块调用的锁依赖
```

**F2. 超时机制**
```cpp
// 检查清单：
// □ 是否有超时保护
// □ 使用 unique_lock::try_lock_for()

if (lock.try_lock_for(std::chrono::seconds(1))) {
    // 获取成功
} else {
    // 超时处理
}
```

#### G. 性能影响评估

```cpp
// 检查清单：
// □ 锁竞争是否会影响性能
// □ 是否可以使用读写锁优化
// □ 是否可以使用无锁算法（atomic）
```

## 问题严重程度判定

### 严重（Critical）
- 明确的数据竞争，100%会导致崩溃
- 死锁风险，高概率触发
- 内存安全相关（UAF、双释等）

### 高（High）
- 概率性数据竞争
- 可能的性能瓶颈
- 复杂场景下的死锁风险

### 中（Medium）
- 边界条件下的竞态
- 代码可维护性问题
- 缺少文档说明的复杂同步逻辑

### 低（Low）
- 潜在的优化空间
- 代码风格问题
- 防御性编程建议

## 审查报告模板

```markdown
# 线程安全审查报告

## 基本信息
- **审查对象**: `文件路径`
- **审查人**: `姓名`
- **审查日期**: `日期`

## 线程模型分析
1. **主要线程**: 列出涉及的线程
2. **共享状态**: 列出共享的数据
3. **同步机制**: 列出使用的锁和同步原语

## 发现的问题

### [严重] 问题标题
- **位置**: `文件:行号`
- **违反规则**: 规则X
- **问题描述**: 详细说明
- **修复建议**: 代码示例

## 总体评估
- **风险等级**: 高/中/低
- **关键建议**:
  1. ...
  2. ...
  3. ...
```

## 常见反模式库

### 反模式1：双重检查锁定（错误的）
```cpp
// ❌ C++11之前的问题模式
static Singleton* GetInstance() {
    static Singleton* instance = nullptr;
    if (!instance) {  // 第一次检查
        std::lock_guard<std::mutex> lock(mutex_);
        if (!instance) {  // 第二次检查
            instance = new Singleton();
        }
    }
    return instance;
}

// ✓ C++11正确做法：使用魔法静态
static Singleton& GetInstance() {
    static Singleton instance;
    return instance;
}
```

### 反模式2：在析构函数中加锁
```cpp
// ❌ 危险：可能导致死锁
~Service() {
    std::lock_guard<std::mutex> lock(mutex_);
    // 如果其他线程正在使用这个对象
}

// 建议：析构函数不应加锁，对象销毁前确保无其他使用者
```

### 反模式3：锁中调用回调
```cpp
// ❌ 危险：回调中可能获取其他锁
void Process() {
    std::lock_guard<std::mutex> lock(mutex_);
    callback_();  // 未知代码，可能死锁
}

// ✓ 正确：先复制回调，释放锁后调用
auto callback = callback_;
{
    std::lock_guard<std::mutex> lock(mutex_);
    callback = callback_;
}
callback();
```

## 工具辅助

建议使用以下工具辅助审查：
- ThreadSanitizer (TSan): 运行时检测数据竞争
- Clang Static Analyzer: 静态分析
- Coverity: 商业静态分析工具
- Valgrind/Helgrind: 内存和线程分析

注意：工具不能替代人工审查，只能作为补充。
