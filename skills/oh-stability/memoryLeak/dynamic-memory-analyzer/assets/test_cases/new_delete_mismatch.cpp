// Test Case: new[] / delete mismatch
// Issue: Array allocated with new[] but freed with delete

class MyClass {
public:
    MyClass() {}
    ~MyClass() {}
};

void ArrayAllocation() {
    // Wrong: Using new[] but deleting with delete
    MyClass* arr = new MyClass[10];
    
    for (int i = 0; i < 10; i++) {
        arr[i].DoSomething();
    }
    
    delete arr;  // WRONG: Should be delete[]
}

void CorrectArrayAllocation() {
    // Correct: Using new[] with delete[]
    MyClass* arr = new MyClass[10];
    
    for (int i = 0; i < 10; i++) {
        arr[i].DoSomething();
    }
    
    delete[] arr;  // CORRECT
}
