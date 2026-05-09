# 规则019: 全局变量初始化检查

**严重程度**: 中危

**问题描述**: FUZZ测试中的全局指针或全局对象未正确初始化，可能导致空指针解引用、未定义行为或测试无效。

**核心原则**:
1. 全局指针必须在 `LLVMFuzzerInitialize` 中初始化为有效对象
2. 禁止使用未初始化的全局指针进行API调用
3. 优先使用单例模式（`Class::GetInstance()`）获取实例
4. 避免使用裸指针，建议使用智能指针或引用

**错误示例**:
```cpp
// 错误1: 全局指针未在LLVMFuzzerInitialize中初始化
RSScreenManager* g_manager = nullptr;

extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
    // 忘记初始化 g_manager
    return 0;
}

void DoTest(FuzzedDataProvider& fdp)
{
    g_manager->SomeMethod();  // 空指针解引用！
}

// 错误2: 初始化为nullptr但未重新赋值
RSScreenManager* g_manager = nullptr;

extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
    g_manager = nullptr;  // 仍然是nullptr
    return 0;
}
```

**正确示例**:
```cpp
// 正确1: 使用单例模式初始化
RSScreenManager* g_manager = nullptr;

extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
    g_manager = &RSScreenManager::GetInstance();
    return 0;
}

// 正确2: 使用new创建对象（需确保释放）
RSScreenManager* g_manager = nullptr;

extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
    g_manager = new RSScreenManager();
    return 0;
}

// 正确3: 使用智能指针（推荐）
std::shared_ptr<RSScreenManager> g_manager;

extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
    g_manager = std::make_shared<RSScreenManager>();
    return 0;
}
```

**检查方法**: 1. 检查全局指针是否声明为 `nullptr`
2. 检查 `LLVMFuzzerInitialize` 函数是否存在
3. 检查全局指针是否在 `LLVMFuzzerInitialize` 中被赋值为有效对象
4. 检查赋值模式是否为 `&Class::GetInstance()`、`new Class()` 或有效对象地址

**豁免场景**: 
- 全局变量是基本类型（int、bool等）且有初始值
- 全局变量在 `LLVMFuzzerTestOneInput` 中首次使用前被初始化
- 全局变量是常量（const）

---
