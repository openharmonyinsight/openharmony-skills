// Eval file for rule: 存根/空方法实现检测
// 正例1：纯虚函数声明（接口定义）
class Subscriber {
public:
    virtual void OnStateChanged(const StateData& data) = 0;  // OK: pure virtual
};

// 正例2：虚析构函数（标准模式）
class Manager {
public:
    virtual ~Manager() {}  // OK: standard pattern for virtual destructors
};

// 正例3：默认实现，子类可以重写
void OnStateChanged(const StateData& data) {
    // Default: do nothing, subclasses can override
}

// 正例4：空构造函数
class MyClass {
public:
    MyClass() {}  // OK: default constructor
};

// 正例5：参数标记为 maybe_unused
int32_t CallbackEnter([[maybe_unused]] uint32_t code) {
    // Some implementations may need this, others don't
    return ERR_OK;  // OK: marked as maybe_unused
}

// 正例6：条件处理，有实际实现逻辑
int32_t ProcessOptionalFeature(const OptionalFeature& feature) {
    if (!feature.isEnabled()) {
        return ERR_OK;  // OK: feature is optional, skipping is valid
    }
    return ProcessFeature(feature);
}
