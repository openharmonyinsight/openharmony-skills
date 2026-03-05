# Fix Recommendations

## 1. Basic Pairing Fixes

### Array Mismatch
```cpp
// ❌ Wrong
MyClass* arr = new MyClass[10];
delete arr;

// ✅ Correct
MyClass* arr = new MyClass[10];
delete[] arr;
```

### Multiple new, Single delete
```cpp
// ❌ Wrong
void Function() {
    MyClass* ptr1 = new MyClass();
    MyClass* ptr2 = new MyClass();
    delete ptr1;  // ptr2 leaked
}

// ✅ Correct
void Function() {
    auto ptr1 = std::make_unique<MyClass>();
    auto ptr2 = std::make_unique<MyClass>();
}
```

## 2. Smart Pointer Fixes

### Raw Pointer with RefPtr
```cpp
// ❌ Wrong
MyClass* ptr = new MyClass();
RefPtr<MyClass> refPtr = ptr;  // Ownership unclear

// ✅ Correct
RefPtr<MyRef> refPtr = AceType::MakeRefPtr<MyClass>();
```

### Missing MakeRefPtr
```cpp
// ❌ Wrong
RefPtr<MyClass> ptr = new MyClass();

// ✅ Correct
RefPtr<MyClass> ptr = AceType::MakeRefPtr<MyClass>();
```

## 3. Exception Safety Fixes

### Exception Path Leak
```cpp
// ❌ Wrong
void Function() {
    MyClass* ptr = new MyClass();
    MayThrowException();  // If throws, ptr leaks
    delete ptr;
}

// ✅ Correct (RAII)
void Function() {
    auto ptr = std::make_unique<MyClass>();
    MayThrowException();  // Auto-cleanup
}

// ✅ Correct (Manual)
void Function() {
    MyClass* ptr = new MyClass();
    try {
        MayThrowException();
    } catch (...) {
        delete ptr;
        throw;
    }
    delete ptr;
}
```

## 4. Register/Unregister Fixes

### Exception Path Missing Unregister
```cpp
// ❌ Wrong
void Function() {
    Register();
    MayThrowException();  // Unregister not called
    Unregister();
}

// ✅ Correct (RAII)
class ResourceGuard {
public:
    ResourceGuard() { Register(); }
    ~ResourceGuard() { Unregister(); }
};

void Function() {
    ResourceGuard guard;  // Auto-unregister
    MayThrowException();
}
```

### Duplicate Register
```cpp
// ❌ Wrong
void Function() {
    Register();  // Old registration leaked
    Register();
}

// ✅ Correct
void Function() {
    if (IsRegistered()) {
        Unregister();
    }
    Register();
}
```

## 5. Lifecycle Binding Fixes

### Circular Reference
```cpp
// ❌ Wrong
class Child {
public:
    void SetParent(Parent* parent) {
        parent_ = parent;  // Circular reference
    }
private:
    RefPtr<Parent> parent_;
};

// ✅ Correct
class Child {
public:
    void SetParent(const WeakPtr<Parent>& parent) {
        parent_ = parent;  // Weak reference
    }
private:
    WeakPtr<Parent> parent_;
};
```

### Parent Destructor Missing Cleanup
```cpp
// ❌ Wrong
class Parent {
public:
    void AddChild(Child* child) {
        children_.push_back(child);
    }
    // Destructor missing - children leaked
private:
    std::vector<Child*> children_;
};

// ✅ Correct
class Parent {
public:
    void AddChild(Child* child) {
        children_.push_back(child);
    }
    ~Parent() {
        for (auto* child : children_) {
            delete child;
        }
        children_.clear();
    }
private:
    std::vector<Child*> children_;
};
```

## 6. Assignment Update Fixes

### Exception-Unsafe Assignment
```cpp
// ❌ Wrong
void SetValue() {
    delete ptr_;  // If new throws, ptr_ is deleted
    ptr_ = new Resource();  // May throw
}

// ✅ Correct
void SetValue() {
    Resource* newPtr = new Resource();
    delete ptr_;
    ptr_ = newPtr;
}

// ✅ Correct (Smart Pointer)
void SetValue() {
    ptr_ = AceType::MakeRefPtr<Resource>();  // Auto-managed
}
```

### Self-Assignment
```cpp
// ❌ Wrong
void SetValue(Resource* ptr) {
    delete ptr_;
    ptr_ = new Resource(*ptr);  // If ptr == ptr_, we deleted it
}

// ✅ Correct
void SetValue(Resource* ptr) {
    if (ptr_ == ptr) {
        return;
    }
    delete ptr_;
    ptr_ = new Resource(*ptr);
}
```

## 7. Function Return Fixes

### Early Return Leak
```cpp
// ❌ Wrong
void Function() {
    MyClass* ptr = new MyClass();
    if (CheckCondition()) {
        return;  // ptr leaked
    }
    delete ptr;
}

// ✅ Correct (RAII)
void Function() {
    auto ptr = std::make_unique<MyClass>();
    if (CheckCondition()) {
        return;  // Auto-cleanup
    }
}

// ✅ Correct (Manual)
void Function() {
    MyClass* ptr = new MyClass();
    if (CheckCondition()) {
        delete ptr;
        return;
    }
    delete ptr;
}
```

### Multiple Return Paths
```cpp
// ❌ Wrong
void Function(bool flag1, bool flag2) {
    MyClass* ptr = new MyClass();
    if (flag1) {
        delete ptr;
        return;
    }
    if (flag2) {
        return;  // ptr leaked
    }
    delete ptr;
}

// ✅ Correct
void Function(bool flag1, bool flag2) {
    auto ptr = std::make_unique<MyClass>();
    if (flag1) {
        return;
    }
    if (flag2) {
        return;
    }
}
```

## 8. Container Pointer Fixes

### Container Cleanup Missing
```cpp
// ❌ Wrong
class MyClass {
public:
    void AddItem(Item* item) {
        items_.push_back(item);
    }
    // Destructor missing - items leaked
private:
    std::vector<Item*> items_;
};

// ✅ Correct
class MyClass {
public:
    void AddItem(Item* item) {
        items_.push_back(item);
    }
    ~MyClass() {
        for (auto* item : items_) {
            delete item;
        }
        items_.clear();
    }
private:
    std::vector<Item*> items_;
};

// ✅ Correct (Smart Pointers)
class MyClass {
public:
    void AddItem(Item* item) {
        items_.push_back(AceType::MakeRefPtr<Item>(item));
    }
private:
    std::vector<RefPtr<Item>> items_;
};
```

## 9. nullptr Handling Fixes

### Unnecessary nullptr Check
```cpp
// ❌ Wrong (Unnecessary)
void Function() {
    MyClass* ptr = nullptr;
    if (ptr != nullptr) {  // Unnecessary
        delete ptr;
    }
}

// ✅ Correct
void Function() {
    MyClass* ptr = nullptr;
    delete ptr;  // Safe by C++ standard
}
```

### new(std::nothrow) Usage
```cpp
// ❌ Wrong
void Function() {
    MyClass* ptr = new(std::nothrow) MyClass();
    if (ptr == nullptr) {
        return;
    }
    // ... use ptr
    delete ptr;  // Must delete even if nullptr
}

// ✅ Correct
void Function() {
    MyClass* ptr = new(std::nothrow) MyClass();
    if (ptr == nullptr) {
        return;
    }
    // ... use ptr
    delete ptr;  // Safe even if nullptr
}
```

## 10. Third-party Library Fixes

### Rosen Pointer Ownership
```cpp
// ⚠️ Caution: Rosen pointers may have specific ownership
// Always check Rosen documentation

// Example: Rosen::WindowOption
sptr<Rosen::WindowOption> option = new Rosen::WindowOption();
// sptr manages ownership - no manual delete needed
```

### Skia Pointer Ownership
```cpp
// ⚠️ Caution: Skia objects may have specific ownership
// Always check Skia documentation

// Example: SkCanvas
std::unique_ptr<SkCanvas> canvas = SkCanvas::MakeDirect(...);
// unique_ptr manages ownership
```
