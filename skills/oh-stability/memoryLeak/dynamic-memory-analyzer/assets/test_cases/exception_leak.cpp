// Test Case: Exception Safety
// Issue: Memory leak when exception is thrown

class MyClass {
public:
    MyClass() {}
    ~MyClass() {}
    void DoWork() {}
};

void MayThrowException() {
    if (ShouldThrow()) {
        throw std::runtime_error("Something went wrong");
    }
}

bool ShouldThrow() {
    return true;
}

void ExceptionUnsafeFunction() {
    MyClass* ptr = new MyClass();
    
    try {
        MayThrowException();  // If this throws, ptr leaks
        ptr->DoWork();
    } catch (const std::exception& e) {
        // ptr is not deleted here - LEAK
        throw;
    }
    
    delete ptr;
}

void ExceptionSafeWithRAII() {
    auto ptr = std::make_unique<MyClass>();
    
    MayThrowException();  // Safe: auto cleanup on exception
    ptr->DoWork();
}

void ExceptionSafeWithManualCleanup() {
    MyClass* ptr = new MyClass();
    
    try {
        MayThrowException();
        ptr->DoWork();
    } catch (...) {
        delete ptr;  // Manual cleanup before rethrowing
        throw;
    }
    
    delete ptr;
}

void RegisterWithoutRAII() {
    Register();
    
    try {
        MayThrowException();  // If throws, Unregister not called
    } catch (...) {
        throw;
    }
    
    Unregister();
}

class ResourceGuard {
public:
    ResourceGuard() { Register(); }
    ~ResourceGuard() { Unregister(); }
};

void RegisterWithRAII() {
    ResourceGuard guard;  // RAII ensures cleanup
    
    MayThrowException();  // Safe: Unregister called automatically
}
