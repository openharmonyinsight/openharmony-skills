# SOLID Principles Code Review Guide

## Overview

SOLID is a mnemonic acronym for five design principles intended to make software designs more understandable, flexible, and maintainable.

---

## S - Single Responsibility Principle (SRP)

**A class should have one, and only one, reason to change.**

### What It Means

Each class should have only one job or responsibility. If a class has more than one reason to change, it violates SRP.

### Detection

**Red Flags:**
- Class has many methods (>20)
- Methods do very different things
- Changing one feature requires understanding whole class
- Class name is vague (Manager, Handler, Processor)

### Examples

**❌ VIOLATION:**
```cpp
class MenuManager {
public:
    // Business logic
    void ShowMenu();
    void HideMenu();
    void AddMenuItem();

    // Rendering
    void DrawBackground();
    void DrawBorder();
    void DrawText();

    // Event handling
    void OnClick();
    void OnHover();
    void OnKeyPress();

    // Persistence
    void SaveToDatabase();
    void LoadFromDatabase();

    // Networking
    void SendOverNetwork();
    void ReceiveFromNetwork();

    // Multiple reasons to change!
};
```

**✅ CORRECT:**
```cpp
// Separate responsibilities
class MenuPattern {
public:
    void ShowMenu();
    void HideMenu();
    void AddMenuItem();
};

class MenuRenderer {
public:
    void DrawBackground();
    void DrawBorder();
    void DrawText();
};

class MenuEventHandler {
public:
    void OnClick();
    void OnHover();
    void OnKeyPress();
};

class MenuStorage {
public:
    void SaveToDatabase();
    void LoadFromDatabase();
};

class MenuNetwork {
public:
    void SendOverNetwork();
    void ReceiveFromNetwork();
};
```

### Refactoring

**Extract Class:** Pull out related methods into a separate class.

```cpp
// Before: One class doing everything
class MenuPattern {
    void Layout();
    void Render();
    void SaveState();
    void HandleEvents();
};

// After: Separate classes
class MenuPattern { void Layout(); };
class MenuRenderer { void Render(); };
class MenuStorage { void SaveState(); };
class MenuEventHandler { void HandleEvents(); };
```

### Severity

**🟠 HIGH** - Violations lead to:
- Hard to maintain code
- Unexpected side effects
- Difficult testing

---

## O - Open/Closed Principle (OCP)

**Software entities should be open for extension, but closed for modification.**

### What It Means

You should be able to extend a class's behavior without modifying it. Use abstraction (interfaces, abstract classes) to achieve this.

### Detection

**Red Flags:**
- Adding new feature requires modifying existing code
- Many if/else or switch statements checking types
- Frequent modifications to stable code

### Examples

**❌ VIOLATION:**
```cpp
class MenuProcessor {
public:
    void ProcessMenu(MenuType type) {
        switch (type) {
            case MenuType::CONTEXT:
                ProcessContextMenu();
                break;
            case MenuType::DROPDOWN:
                ProcessDropdownMenu();
                break;
            case MenuType::POPUP:
                ProcessPopupMenu();
                break;
            // Adding new type requires modifying this!
            default:
                break;
        }
    }

private:
    void ProcessContextMenu() { /* ... */ }
    void ProcessDropdownMenu() { /* ... */ }
    void ProcessPopupMenu() { /* ... */ }
};
```

**✅ CORRECT:**
```cpp
// Abstract base
class MenuProcessor {
public:
    virtual ~MenuProcessor() = default;
    virtual void Process() = 0;
};

// Concrete implementations
class ContextMenuProcessor : public MenuProcessor {
public:
    void Process() override {
        // Context menu specific processing
    }
};

class DropdownMenuProcessor : public MenuProcessor {
public:
    void Process() override {
        // Dropdown menu specific processing
    }
};

// Factory for creation
class MenuProcessorFactory {
public:
    static std::unique_ptr<MenuProcessor> Create(MenuType type) {
        switch (type) {
            case MenuType::CONTEXT:
                return std::make_unique<ContextMenuProcessor>();
            case MenuType::DROPDOWN:
                return std::make_unique<DropdownMenuProcessor>();
        }
    }
};

// Adding new type: just add new class, no modification needed!
class PopupMenuProcessor : public MenuProcessor {
public:
    void Process() override { /* ... */ }
};
```

### Refactoring

**Replace Conditional with Polymorphism:**

```cpp
// Before: Switch on type
void Draw(Component* comp) {
    switch (comp->type) {
        case BUTTON: DrawButton(comp); break;
        case TEXT: DrawText(comp); break;
    }
}

// After: Polymorphism
class Component {
public:
    virtual void Draw() = 0;
};

class Button : public Component {
public:
    void Draw() override { DrawButton(); }
};

class Text : public Component {
public:
    void Draw() override { DrawText(); }
};
```

### Severity

**🟠 HIGH** - Violations lead to:
- Bugs in existing code when adding features
- Difficult to maintain
- High regression risk

---

## L - Liskov Substitution Principle (LSP)

**Subtypes must be substitutable for their base types.**

### What It Means

If class B is a subtype of class A, then you should be able to replace A with B without breaking the program. Derived classes must honor the contract of their base classes.

### Detection

**Red Flags:**
- Derived class throws exception for methods base doesn't
- Derived class returns null when base doesn't
- Derived class has weaker preconditions or stronger postconditions
- Client code checks type before using

### Examples

**❌ VIOLATION 1: Changing Behavior**
```cpp
class Bird {
public:
    virtual void Fly() {
        // All birds can fly
    }
};

class Penguin : public Bird {
public:
    void Fly() override {
        // Penguins can't fly!
        throw std::runtime_error("Penguins can't fly!");
    }
};

// Client code breaks
void MakeBirdFly(Bird* bird) {
    bird->Fly();  // Crashes for Penguin!
}
```

**✅ CORRECT:**
```cpp
// Restructure hierarchy
class Bird {
public:
    virtual void Move() = 0;
};

class FlyingBird : public Bird {
public:
    void Move() override { Fly(); }
    void Fly() { /* ... */ }
};

class FlightlessBird : public Bird {
public:
    void Move() override { Swim(); }
    void Swim() { /* ... */ }
};

class Eagle : public FlyingBird { /* ... */ };
class Penguin : public FlightlessBird { /* ... */ };
```

**❌ VIOLATION 2: Returning Null**
```cpp
class Menu {
public:
    virtual MenuItem& GetItem(int index) {
        return items_.at(index);  // Throws if out of bounds
    }
};

class LazyMenu : public Menu {
public:
    MenuItem& GetItem(int index) override {
        if (index >= items_.size()) {
            static MenuItem empty;  // Returns reference to empty!
            return empty;
        }
        return items_.at(index);
    }
};

// Different behavior breaks LSP
```

**✅ CORRECT:**
```cpp
// Use optionals or exceptions consistently
class Menu {
public:
    virtual std::optional<MenuItem*> GetItem(int index) = 0;
};

class LazyMenu : public Menu {
public:
    std::optional<MenuItem*> GetItem(int index) override {
        if (index >= items_.size()) return std::nullopt;
        return &items_.at(index);
    }
};
```

### Refactoring

**Restructure Inheritance Hierarchy:**
- Move common behavior to base
- Create separate branches for incompatible behaviors
- Use interfaces instead of inheritance when appropriate

### Severity

**🟡 MEDIUM** - Violations lead to:
- Subtle bugs
- Unexpected behavior
- Need for type checking

---

## I - Interface Segregation Principle (ISP)

**Clients should not be forced to depend on interfaces they don't use.**

### What It Means

Interfaces should be focused and specific. Fat interfaces force clients to implement methods they don't need.

### Detection

**Red Flags:**
- Classes with empty method implementations (just to satisfy interface)
- Interfaces with many methods (>10)
- Clients throw "not implemented" exceptions

### Examples

**❌ VIOLATION:**
```cpp
// Fat interface
class Component {
public:
    virtual void Render() = 0;
    virtual void HandleClick() = 0;
    virtual void HandleKeyPress() = 0;
    virtual void HandleHover() = 0;
    virtual void Animate() = 0;
    virtual void Serialize() = 0;
    virtual void Deserialize() = 0;
};

// Forced to implement everything
class Label : public Component {
public:
    void Render() override { /* ... */ }
    void HandleClick() override { /* ... */ }

    // But these don't make sense for Label!
    void HandleKeyPress() override {
        // Empty - label doesn't handle keys
    }
    void HandleHover() override {
        // Empty - label doesn't handle hover
    }
    void Animate() override {
        // Empty - labels don't animate
    }
    void Serialize() override { /* ... */ }
    void Deserialize() override { /* ... */ }
};
```

**✅ CORRECT:**
```cpp
// Segregated interfaces
class Renderable {
public:
    virtual void Render() = 0;
};

class Clickable {
public:
    virtual void OnClick() = 0;
};

class Animatable {
public:
    virtual void Animate() = 0;
};

class Serializable {
public:
    virtual void Serialize() = 0;
    virtual void Deserialize() = 0;
};

// Label implements only what it needs
class Label : public Renderable, public Serializable {
public:
    void Render() override { /* ... */ }
    void Serialize() override { /* ... */ }
    void Deserialize() override { /* ... */ }
};

class Button : public Renderable, public Clickable, public Animatable, public Serializable {
public:
    void Render() override { /* ... */ }
    void OnClick() override { /* ... */ }
    void Animate() override { /* ... */ }
    void Serialize() override { /* ... */ }
    void Deserialize() override { /* ... */ }
};
```

### Refactoring

**Split Interface:**
```cpp
// Before: One big interface
class Menu {
public:
    virtual void Show() = 0;
    virtual void Hide() = 0;
    virtual void AddItem() = 0;
    virtual void RemoveItem() = 0;
    virtual void Save() = 0;
    virtual void Load() = 0;
};

// After: Multiple focused interfaces
class MenuVisibility {
public:
    virtual void Show() = 0;
    virtual void Hide() = 0;
};

class MenuItems {
public:
    virtual void AddItem() = 0;
    virtual void RemoveItem() = 0;
};

class MenuPersistence {
public:
    virtual void Save() = 0;
    virtual void Load() = 0;
};
```

### Severity

**🟡 MEDIUM** - Violations lead to:
- Empty method implementations
- Coupling to unused functionality
- Confusing interfaces

---

## D - Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions.**

### What It Means

High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces). Abstractions should not depend on details; details should depend on abstractions.

### Detection

**Red Flags:**
- High-level classes directly create low-level objects
- Hard-coded dependencies
- Cannot swap implementations without changing code
- Difficult to test (can't inject mocks)

### Examples

**❌ VIOLATION:**
```cpp
// High-level module depends on low-level details
class MenuPattern {
private:
    SQLiteDatabase database_;  // Concrete dependency!
    FileLogger logger_;        // Concrete dependency!

public:
    MenuPattern() : database_("menu.db"), logger_("menu.log") {}

    void SaveState() {
        database_.Execute("INSERT INTO menu ...");
    }

    void LogAction(const std::string& action) {
        logger_.Write(action);
    }
};

// Hard to test, hard to change implementations
```

**✅ CORRECT:**
```cpp
// Depend on abstractions
class IDatabase {
public:
    virtual ~IDatabase() = default;
    virtual void Execute(const std::string& sql) = 0;
};

class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void Write(const std::string& message) = 0;
};

class MenuPattern {
private:
    std::shared_ptr<IDatabase> database_;  // Abstract dependency!
    std::shared_ptr<ILogger> logger_;      // Abstract dependency!

public:
    MenuPattern(std::shared_ptr<IDatabase> db,
                std::shared_ptr<ILogger> logger)
        : database_(db), logger_(logger) {}

    void SaveState() {
        database_->Execute("INSERT INTO menu ...");
    }

    void LogAction(const std::string& action) {
        logger_->Write(action);
    }
};

// Concrete implementations
class SQLiteDatabase : public IDatabase {
public:
    void Execute(const std::string& sql) override {
        // SQLite-specific implementation
    }
};

class FileLogger : public ILogger {
public:
    void Write(const std::string& message) override {
        // File-specific implementation
    }
};

// Easy to test with mocks
class MockDatabase : public IDatabase {
public:
    void Execute(const std::string& sql) override {
        calls_.push_back(sql);
    }
    std::vector<std::string> calls_;
};

TEST(MenuPatternTest, SaveState) {
    auto mock_db = std::make_shared<MockDatabase>();
    auto mock_logger = std::make_shared<MockLogger>();
    MenuPattern menu(mock_db, mock_logger);

    menu.SaveState();

    ASSERT_EQ(mock_db->calls_.size(), 1);
}
```

### Refactoring

**Dependency Injection:**

```cpp
// Before: Hard-coded dependency
class MenuPattern {
    FileLogger logger_;
public:
    MenuPattern() : logger_("menu.log") {}
};

// After: Injected dependency
class MenuPattern {
    std::shared_ptr<ILogger> logger_;
public:
    MenuPattern(std::shared_ptr<ILogger> logger) : logger_(logger) {}
};
```

### Severity

**🟠 HIGH** - Violations lead to:
- Hard to test
- Tight coupling
- Inflexible design
- Difficult to swap implementations

---

## SOLID Summary Table

| Principle | Key Idea | Violation Signs | Refactoring | Severity |
|-----------|----------|-----------------|-------------|----------|
| **SRP** | One responsibility per class | Class does many things | Extract Class | 🟠 HIGH |
| **OCP** | Open for extension, closed for modification | Adding features requires changing existing code | Replace Conditional with Polymorphism | 🟠 HIGH |
| **LSP** | Subtypes must be substitutable | Derived class changes behavior | Restructure hierarchy | 🟡 MEDIUM |
| **ISP** | Focused interfaces | Fat interfaces, empty methods | Split Interface | 🟡 MEDIUM |
| **DIP** | Depend on abstractions | Hard-coded dependencies | Dependency Injection | 🟠 HIGH |

---

## SOLID Violation Detection Checklist

**Single Responsibility:**
- [ ] Class has >20 methods
- [ ] Methods do unrelated things
- [ ] Class name is vague (Manager, Handler, Processor)
- [ ] Multiple reasons to change

**Open/Closed:**
- [ ] Adding feature requires modifying stable code
- [ ] Switch/if-else chains on type
- [ ] Frequently modified code

**Liskov Substitution:**
- [ ] Derived throws exception base doesn't
- [ ] Derived returns null when base doesn't
- [ ] Client checks type before using

**Interface Segregation:**
- [ ] Interfaces with >10 methods
- [ ] Empty method implementations
- [ ] "Not implemented" exceptions

**Dependency Inversion:**
- [ ] Direct creation of low-level objects
- [ ] Hard-coded dependencies
- [ ] Can't inject mocks for testing

---

## Quick Refactoring Guide

**SRP:**
```cpp
// Before
class BigClass {
    void DoA();
    void DoB();
    void DoC();
};

// After
class ClassA { void DoA(); };
class ClassB { void DoB(); };
class ClassC { void DoC(); };
```

**OCP:**
```cpp
// Before
void Process(int type) {
    if (type == 1) DoA();
    else if (type == 2) DoB();
}

// After
class Processor {
    virtual void Process() = 0;
};
class ProcessorA : Processor { void Process() override { DoA(); } };
class ProcessorB : Processor { void Process() override { DoB(); } };
```

**LSP:**
```cpp
// Before
class Base { void Method(); };
class Derived : Base { void Method() override { throw; } };

// After
class Base { void Method(); };
class ValidDerived : Base { void Method() override { /* valid */ } };
```

**ISP:**
```cpp
// Before
interface BigInterface {
    void MethodA();
    void MethodB();
    void MethodC();
}

// After
interface InterfaceA { void MethodA(); };
interface InterfaceB { void MethodB(); };
interface InterfaceC { void MethodC(); };
```

**DIP:**
```cpp
// Before
class HighLevel {
    LowLevel dep_;
};

// After
class HighLevel {
    Interface dep_;
};
```

---

## Testing for SOLID Compliance

**SRP Test:** Can you describe class responsibility in one sentence?

**OCP Test:** Can you add a new feature by only adding new code (not modifying existing)?

**LSP Test:** Can you substitute derived class anywhere base is used without breaking?

**ISP Test:** Does every interface method make sense for all implementers?

**DIP Test:** Can you easily swap dependencies (especially for testing)?

---

## Common Mistakes

1. **"SRP means small classes"** - No, SRP means one responsibility
2. **"OCP means never modify code"** - No, OCP means stable abstractions
3. **"LSP is just about inheritance"** - No, LSP is about behavioral contracts
4. **"ISP means many small interfaces"** - No, ISP means focused, client-specific interfaces
5. **"DIP means no dependencies"** - No, DIP means depend on abstractions, not concretions
