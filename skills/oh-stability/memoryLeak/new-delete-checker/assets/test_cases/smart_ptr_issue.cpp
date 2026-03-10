// Test Case: Smart Pointer Issues
// Issue: Using RefPtr incorrectly and mixing raw pointers

#include "ace_type.h"

class MyRef : public RefBase {
public:
    MyRef() {}
    ~MyRef() {}
};

void SmartPointerIssue1() {
    // Issue 1: Using raw new with RefPtr instead of MakeRefPtr
    MyRef* rawPtr = new MyRef();
    RefPtr<MyRef> refPtr = rawPtr;  // Ownership unclear
    
    refPtr->DoSomething();
}

void SmartPointerIssue2() {
    // Issue 2: Missing MakeRefPtr usage
    RefPtr<MyRef> ptr = new MyRef();  // Should use MakeRefPtr
    ptr->DoSomething();
}

void SmartPointerIssue3() {
    // Correct usage with MakeRefPtr
    RefPtr<MyRef> ptr = AceType::MakeRefPtr<MyRef>();
    ptr->DoSomething();
}

void CircularReference() {
    class Parent : public RefBase {
    public:
        RefPtr<Child> child;
    };
    
    class Child : public RefBase {
    public:
        RefPtr<Parent> parent;  // ISSUE: Circular reference
    };
    
    RefPtr<Parent> p = AceType::MakeRefPtr<Parent>();
    RefPtr<Child> c = AceType::MakeRefPtr<Child>();
    
    p->child = c;
    c->parent = p;  // Creates circular reference
}

void BreakCircularReference() {
    class Parent : public RefBase {
    public:
        RefPtr<Child> child;
    };
    
    class Child : public RefBase {
    public:
        WeakPtr<Parent> parent;  // CORRECT: Breaks cycle
    };
    
    RefPtr<Parent> p = AceType::MakeRefPtr<Parent>();
    RefPtr<Child> c = AceType::MakeRefPtr<Child>();
    
    p->child = c;
    c->parent = p;  // No circular reference with WeakPtr
}
