---
rule_id: "StabilityCodeReview_ResourceManagement_003"
name: "谨慎使用static_pointer_cast"
category: "资源管理"
severity: "MEDIUM"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# 谨慎使用static_pointer_cast

## 问题描述

谨慎使用std::static_pointer_cast，子类转父类时几乎无需使用（shared_ptr支持隐式向上转换），父类转子类时必须要100%确定父类指针实际指向的是一个子类对象，否则会导致类型错误和未定义行为。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：子类转父类使用static_pointer_cast - 不必要
class Base { public: virtual ~Base() {} };
class Derived : public Base { public: void DerivedMethod() {} };

void UnnecessaryCast()
{
    std::shared_ptr<Derived> derivedPtr = std::make_shared<Derived>();
    
    // 错误：子类转父类不需要static_pointer_cast
    std::shared_ptr<Base> basePtr = std::static_pointer_cast<Base>(derivedPtr);
    
    // 正确：shared_ptr支持隐式向上转换
    std::shared_ptr<Base> basePtr2 = derivedPtr;  // 直接赋值即可
}

// 场景2：父类转子类未确认类型 - 危险
void DangerousDownCast(std::shared_ptr<Base> basePtr)
{
    // 错误：未确认basePtr实际指向Derived对象
    std::shared_ptr<Derived> derivedPtr = std::static_pointer_cast<Derived>(basePtr);
    
    // 如果basePtr实际指向其他子类，这里会导致未定义行为
    derivedPtr->DerivedMethod();  // 可能崩溃
}

// 场景3：在条件判断中静态向下转换 - 仍危险
void ConditionalDownCast(std::shared_ptr<Base> basePtr)
{
    if (basePtr) {
        // 错误：即使非空，也不保证是Derived类型
        std::shared_ptr<Derived> derivedPtr = std::static_pointer_cast<Derived>(basePtr);
        derivedPtr->DerivedMethod();
    }
}

// 场景4：链式static_pointer_cast - 更危险
class Base {};
class Middle : public Base {};
class Leaf : public Middle {};

void ChainCast(std::shared_ptr<Base> basePtr)
{
    // 错误：链式转换，每一步都有类型错误风险
    std::shared_ptr<Middle> middlePtr = std::static_pointer_cast<Middle>(basePtr);
    std::shared_ptr<Leaf> leafPtr = std::static_pointer_cast<Leaf>(middlePtr);
    
    // 如果basePtr不是Leaf类型，多层转换后崩溃
}

// 场景5：在容器遍历中误用
void ContainerCastMisuse()
{
    std::vector<std::shared_ptr<Base>> objects;
    objects.push_back(std::make_shared<Derived>());
    objects.push_back(std::make_shared<OtherDerived>());
    
    for (auto& obj : objects) {
        // 错误：假设所有对象都是Derived类型
        std::shared_ptr<Derived> derived = std::static_pointer_cast<Derived>(obj);
        derived->DerivedMethod();  // OtherDerived对象会崩溃
    }
}

// 场景6：工厂模式误用
std::shared_ptr<Base> CreateObject(int type)
{
    if (type == 1) {
        return std::make_shared<Derived>();
    } else {
        return std::make_shared<OtherDerived>();
    }
}

void FactoryCastMisuse(int type)
{
    auto obj = CreateObject(type);
    
    // 错误：未检查type，直接向下转换
    std::shared_ptr<Derived> derived = std::static_pointer_cast<Derived>(obj);
    derived->DerivedMethod();
}

// 场景7：多继承情况下的static_pointer_cast - 更复杂
class BaseA { public: virtual ~BaseA() {} };
class BaseB { public: virtual ~BaseB() {} };
class MultiDerived : public BaseA, public BaseB {};

void MultiInheritanceCast(std::shared_ptr<BaseA> baseAPtr)
{
    // 错误：多继承情况下static_pointer_cast可能导致指针偏移错误
    std::shared_ptr<BaseB> baseBPtr = std::static_pointer_cast<BaseB>(baseAPtr);
    // 即使对象是MultiDerived，这样转换可能导致错误的指针值
}

// 场景8：回调函数中误用
void CallbackCast(std::shared_ptr<Base> basePtr)
{
    auto callback = [basePtr]() {
        // 错误：回调中假设类型
        auto derived = std::static_pointer_cast<Derived>(basePtr);
        derived->DerivedMethod();
    };
    callback();
}

// 场景9：工厂返回后直接转换
class Factory {
public:
    static std::shared_ptr<Base> Create() {
        return std::make_shared<Derived>();
    }
};

void DirectCast()
{
    auto obj = Factory::Create();
    
    // 错误：即使Create返回Derived，依赖实现细节
    std::shared_ptr<Derived> derived = std::static_pointer_cast<Derived>(obj);
}
```

### ✅ 修复方案

```cpp
// 修复场景1：使用隐式向上转换
class Base { public: virtual ~Base() {} };
class Derived : public Base { public: void DerivedMethod() {} };

void UpCastCorrect()
{
    std::shared_ptr<Derived> derivedPtr = std::make_shared<Derived>();
    
    // 正确：隐式向上转换
    std::shared_ptr<Base> basePtr = derivedPtr;  // 不需要static_pointer_cast
}

// 修复场景2：使用dynamic_pointer_cast安全向下转换
void SafeDownCast(std::shared_ptr<Base> basePtr)
{
    // 正确：使用dynamic_pointer_cast检查类型
    std::shared_ptr<Derived> derivedPtr = std::dynamic_pointer_cast<Derived>(basePtr);
    
    if (derivedPtr) {
        // 类型确认后安全使用
        derivedPtr->DerivedMethod();
    } else {
        LOGE("basePtr is not a Derived object");
    }
}

// 修复场景3：添加类型标识检查
class Base {
public:
    virtual ~Base() {}
    virtual int GetType() const = 0;
};

class Derived : public Base {
public:
    int GetType() const override { return TYPE_DERIVED; }
    void DerivedMethod() {}
};

void TypeCheckDownCast(std::shared_ptr<Base> basePtr)
{
    if (basePtr && basePtr->GetType() == TYPE_DERIVED) {
        // 有类型检查后可以安全使用static_pointer_cast
        std::shared_ptr<Derived> derivedPtr = std::static_pointer_cast<Derived>(basePtr);
        derivedPtr->DerivedMethod();
    }
}

// 修复场景4：使用dynamic_pointer_cast替代链式转换
void ChainCastCorrect(std::shared_ptr<Base> basePtr)
{
    // 正确：直接dynamic_pointer_cast到目标类型
    std::shared_ptr<Leaf> leafPtr = std::dynamic_pointer_cast<Leaf>(basePtr);
    
    if (leafPtr) {
        leafPtr->LeafMethod();
    }
}

// 修复场景5：容器中逐个检查类型
void ContainerCastCorrect()
{
    std::vector<std::shared_ptr<Base>> objects;
    
    for (auto& obj : objects) {
        // 正确：逐个检查类型
        std::shared_ptr<Derived> derived = std::dynamic_pointer_cast<Derived>(obj);
        if (derived) {
            derived->DerivedMethod();
        }
    }
}

// 修复场景6：工厂模式类型检查
void FactoryCastCorrect(int type)
{
    auto obj = CreateObject(type);
    
    if (type == 1) {
        // 正确：根据type确认类型
        std::shared_ptr<Derived> derived = std::static_pointer_cast<Derived>(obj);
        derived->DerivedMethod();
    } else {
        // 处理其他类型
    }
}

// 修复场景7：多继承使用dynamic_pointer_cast
class BaseA { public: virtual ~BaseA() {} };
class BaseB { public: virtual ~BaseB() {} };
class MultiDerived : public BaseA, public BaseB {};

void MultiInheritanceCastCorrect(std::shared_ptr<BaseA> baseAPtr)
{
    // 正确：使用dynamic_pointer_cast处理多继承
    std::shared_ptr<MultiDerived> multiPtr = std::dynamic_pointer_cast<MultiDerived>(baseAPtr);
    
    if (multiPtr) {
        std::shared_ptr<BaseB> baseBPtr = multiPtr;  // 隐式转换
        baseBPtr->BaseBMethod();
    }
}

// 修复场景8：回调中类型检查
void CallbackCastCorrect(std::shared_ptr<Base> basePtr)
{
    auto callback = [basePtr]() {
        // 正确：回调中使用dynamic_pointer_cast检查
        auto derived = std::dynamic_pointer_cast<Derived>(basePtr);
        if (derived) {
            derived->DerivedMethod();
        }
    };
    callback();
}

// 修复场景9：使用模板工厂明确类型
template<typename T>
class TypedFactory {
public:
    static std::shared_ptr<T> Create() {
        return std::make_shared<T>();
    }
};

void DirectCastCorrect()
{
    // 正确：工厂直接返回具体类型
    auto derived = TypedFactory<Derived>::Create();
    derived->DerivedMethod();
}

// 修复场景10：必要时注释说明
void DocumentedCast(std::shared_ptr<Base> basePtr)
{
    // 当100%确定类型时，可以使用static_pointer_cast但需注释
    // 此处basePtr由CreateDerived函数返回，必定是Derived类型
    std::shared_ptr<Derived> derivedPtr = std::static_pointer_cast<Derived>(basePtr);
    derivedPtr->DerivedMethod();
}

// 修复场景11：最佳实践 - 避免向下转换
class Base {
public:
    virtual ~Base() {}
    virtual void Process() = 0;  // 使用虚函数代替向下转换
};

class Derived : public Base {
public:
    void Process() override { DerivedMethod(); }
private:
    void DerivedMethod() {}
};

void BestPractice(std::shared_ptr<Base> basePtr)
{
    // 正确：使用虚函数，无需向下转换
    basePtr->Process();  // 自动调用正确的实现
}
```

## 检测范围

检查以下模式：

- `std::static_pointer_cast<Derived>(basePtr)` 向下转换
- `std::static_pointer_cast<Base>(derivedPtr)` 向上转换（不必要）
- 链式static_pointer_cast调用
- 无类型检查的static_pointer_cast

## 检测要点

1. 识别`std::static_pointer_cast`调用
2. 检查是否是向上转换（子类到父类）- 不必要
3. 检查是否是向下转换（父类到子类）- 需确认类型
4. 检查是否有类型检查机制（dynamic_pointer_cast、类型标识）
5. 识别链式转换的风险

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：父类指针可能指向错误的子类类型
- **RISK_TYPE**：类型错误导致未定义行为
- **RISK_PATH**：static_pointer_cast -> 错误类型 -> 调用不存在的方法 -> 崩溃
- **IMPACT_POINT**：程序崩溃、数据损坏

## 影响分析（ImpactAnalysis）

- **Trigger**：父类指针向下转换为错误的子类类型
- **Propagation**：调用不存在的成员函数或访问错误内存
- **Consequence**：未定义行为、程序崩溃、数据损坏
- **Mitigation**：使用dynamic_pointer_cast检查类型，或使用虚函数避免转换

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 向上转换 | 目标类型是基类 | 提示不必要而非错误 |
| 有类型检查 | dynamic_cast或类型标识检查 | 不报 |
| 虚函数设计 | 使用虚函数避免转换 | 不报 |
| 文档说明 | 有注释说明100%确定类型 | 可能不报 |
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ResourceManagement_003_trigger.cpp
class Base { public: virtual ~Base() {} };
class Derived : public Base {};

void trigger_bad_1(std::shared_ptr<Base> basePtr)
{
    auto derived = std::static_pointer_cast<Derived>(basePtr);  // 应该报：向下转换无检查
}

void trigger_bad_2()
{
    auto derived = std::make_shared<Derived>();
    auto base = std::static_pointer_cast<Base>(derived);  // 应该报：向上转换不必要
}

void trigger_bad_3(std::shared_ptr<Base> basePtr)
{
    if (basePtr) {
        auto derived = std::static_pointer_cast<Derived>(basePtr);  // 应该报：仅检查非空不够
        derived->Method();
    }
}
```

### 安全用例（不应该报）

```cpp
// test_ResourceManagement_003_safe.cpp
void safe_good_1(std::shared_ptr<Base> basePtr)
{
    auto derived = std::dynamic_pointer_cast<Derived>(basePtr);  // 安全：dynamic检查
    if (derived) {
        derived->Method();
    }
}

void safe_good_2()
{
    auto derived = std::make_shared<Derived>();
    std::shared_ptr<Base> base = derived;  // 安全：隐式向上转换
}

void safe_good_3(std::shared_ptr<Base> basePtr)
{
    if (basePtr && basePtr->GetType() == TYPE_DERIVED) {  // 安全：有类型检查
        auto derived = std::static_pointer_cast<Derived>(basePtr);
        derived->Method();
    }
}

// NOPROTECT: 特殊场景
// NOPROTECT: 100%确定类型
void noprotect_case(std::shared_ptr<Base> basePtr)
{
    auto derived = std::static_pointer_cast<Derived>(basePtr);
}
```