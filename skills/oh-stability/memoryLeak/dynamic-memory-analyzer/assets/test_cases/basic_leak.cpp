// Test Case: Basic Memory Leak
// Issue: Missing delete in early return path

class MyClass {
public:
    MyClass() { /* ... */ }
    ~MyClass() { /* ... */ }
    void DoWork() { /* ... */ }
};

void FunctionWithLeak() {
    MyClass* ptr = new MyClass();
    
    if (CheckCondition()) {
        return;  // LEAK: ptr is not deleted
    }
    
    ptr->DoWork();
    delete ptr;  // This line is never reached if CheckCondition() is true
}

bool CheckCondition() {
    return true;
}
