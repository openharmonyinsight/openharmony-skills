# Pattern Detection Rules

## 1. Basic Pairing Issues

### Detection
```bash
# new[] with delete
grep -rn "new \[" frameworks/ --include="*.cpp" | while read line; do
    file=$(echo $line | cut -d: -f1)
    line_num=$(echo $line | cut -d: -f2)
    # Check if delete is used nearby
    sed -n "${line_num},+10p" $file | grep -q "delete " && echo "Potential issue: $file:$line_num"
done

# Multiple new with single delete
awk '/new / {count++} /delete / {count--; if (count < 0) print FILENAME":"NR":"$0}' frameworks/**/*.cpp
```

### Example
```cpp
// ❌ Wrong
MyClass* arr = new MyClass[10];
delete arr;  // Should be delete[]

// ✅ Correct
MyClass* arr = new MyClass[10];
delete[] arr;
```

## 2. Smart Pointer Issues

### Detection
```bash
# Raw pointer delete with RefPtr nearby
grep -rn "delete " frameworks/ --include="*.cpp" | while read line; do
    file=$(echo $line | cut -d: -f1)
    line_num=$(echo $line | cut -d: -f2)
    # Check if RefPtr is used in same function
    sed -n "1,${line_num}p" $file | grep -q "RefPtr" && echo "Potential issue: $file:$line_num"
done

# Missing MakeRefPtr
grep -rn "RefPtr.*new" frameworks/ --include="*.cpp"
```

### Example
```cpp
// ❌ Wrong
MyClass* ptr = new MyClass();
RefPtr<MyClass> refPtr = ptr;  // Ownership unclear

// ✅ Correct
RefPtr<MyClass> refPtr = AceType::MakeRefPtr<MyClass>();
```

## 3. Exception Safety Issues

### Detection
```bash
# new followed by potential throw
grep -rn "new " frameworks/ --include="*.cpp" | while read line; do
    file=$(echo $line | cut -d: -f1)
    line_num=$(echo $line | cut -d: -f2)
    # Check next 5 lines for throw or function calls
    sed -n "${line_num},+5p" $file | grep -E "(throw|MayThrow|ThrowError)" && echo "Potential issue: $file:$line_num"
done
```

### Example
```cpp
// ❌ Wrong
void Function() {
    MyClass* ptr = new MyClass();
    MayThrowException();  // If throws, ptr leaks
    delete ptr;
}

// ✅ Correct
void Function() {
    auto ptr = std::make_unique<MyClass>();
    MayThrowException();  // Auto-cleanup
}
```

## 4. Register/Unregister Issues

### Detection
```bash
# Register without Unregister
grep -rn "Register" frameworks/ --include="*.cpp" | while read line; do
    file=$(echo $line | cut -d: -f1)
    func=$(echo $line | grep -o "Register[^()]*")
    # Check for matching Unregister
    grep -q "Unregister.*${func#Register}" $file || echo "Missing Unregister: $file"
done
```

### Example
```cpp
// ❌ Wrong
void Function() {
    Register();
    MayThrowException();  // Unregister not called
    Unregister();
}

// ✅ Correct
void Function() {
    ResourceGuard guard;  // RAII
    MayThrowException();  // Auto-unregister
}
```

## 5. Lifecycle Binding Issues

### Detection
```bash
# Potential circular references
grep -rn "RefPtr<.*>" frameworks/ --include="*.h" | grep -v "WeakPtr" | while read line; do
    file=$(echo $line | cut -d: -f1)
    class_name=$(echo $line | grep -o "RefPtr<[^>]*>" | sed 's/RefPtr<//;s/>//')
    # Check if class has back reference
    grep -q "$class_name" $file && echo "Potential cycle: $file"
done
```

### Example
```cpp
// ❌ Wrong
class Child {
    RefPtrPtr<Parent> parent_;  // Cycle
};

// ✅ Correct
class Child {
    WeakPtr<Parent> parent_;  // Break cycle
};
```

## 6. Assignment Update Issues

### Detection
```bash
# ptr_ = new without delete ptr_
grep -rn "ptr_ = new" frameworks/ --include="*.cpp" | while read line; do
    file=$(echo $line | cut -d: -f1)
    line_num=$(echo $line | cut -d: -f2)
    # Check previous lines for delete
    sed -n "1,${line_num}p" $file | tail -5 | grep -q "delete ptr_" || echo "Potential leak: $file:$line_num"
done
```

### Example
```cpp
// ❌ Wrong
void SetValue() {
    ptr_ = new Resource();  // Old ptr_ leaked
}

// ✅ Correct
void SetValue() {
    Resource* newPtr = new Resource();
    delete ptr_;
    ptr_ = newPtr;
}
```

## 7. Function Return Issues

### Detection
```bash
# Multiple return paths with new
awk '/^[a-zA-Z].*\(.*\)/ {p=1; fname=$0} p && /new / {has_new=1} p && /return/ {c++} c>2 && /^}/ {print FILENAME":"NR" - "fname; c=0; p=0}' frameworks/**/*.cpp
```

### Example
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

## 8. Container Pointer Fixes

### Container Cleanup Missing
```cpp
//`

### Example
```cpp
// ❌ Wrong
void Function() {
    MyClass* ptr = new MyClass();
    if (condition) {
        return;  // ptr leaked
    }
    delete ptr;
}

// ✅ Correct
void Function() {
    auto ptr = std::make_unique<MyClass>();
    if (condition) {
        return;  // Auto-cleanup
    }
}
```
