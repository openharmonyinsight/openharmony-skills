# Refactoring Large Functions

Guidance for breaking down oversized C/C++ functions into maintainable units.

## Decomposition Strategies

### 1. Extract by Responsibility

Identify distinct logical responsibilities within the function:

```cpp
// BEFORE: 200+ lines doing initialization, processing, and cleanup
void ProcessData(Input* input) {
    // 50 lines: validate input
    // 80 lines: transform data
    // 40 lines: write results
    // 30 lines: cleanup
}

// AFTER: Delegated to focused functions
void ProcessData(Input* input) {
    ValidateInput(input);
    auto transformed = TransformData(input);
    WriteResults(transformed);
}
```

### 2. Extract Loops into Functions

Long loops often contain logic that can be extracted:

```cpp
// BEFORE
for (auto& item : items) {
    // 20 lines of processing per item
}

// AFTER
for (auto& item : items) {
    ProcessItem(item);  // Single responsibility
}
```

### 3. Extract Conditional Branches

Deep conditionals with substantial bodies are extraction candidates:

```cpp
// BEFORE
if (type == TypeA) {
    // 30 lines for TypeA handling
} else if (type == TypeB) {
    // 25 lines for TypeB handling
}

// AFTER
if (type == TypeA) {
    HandleTypeA(item);
} else if (type == TypeB) {
    HandleTypeB(item);
}
```

### 4. Strategy Pattern for Variant Behavior

When conditions select between behaviors, use polymorphism:

```cpp
// BEFORE: Function with many type-based conditionals
void Process(Item* item) {
    if (item->type == A) { /* ... */ }
    else if (item->type == B) { /* ... */ }
    // ... 10 more types
}

// AFTER: Virtual dispatch
struct ItemProcessor {
    virtual void Process(Item* item) = 0;
};
```

## Naming Guidelines

Extracted functions should clearly describe **what** they do:

| Poor Name | Better Name | Why |
|-----------|-------------|-----|
| `process()` | `validateAndNormalizeInput()` | Describes outcome |
| `handleStuff()` | `convertUnitsAndScale()` | Specific |
| `doWork()` | `serializeToJson()` | Clear purpose |

## When NOT to Extract

Don't extract if:
- The extracted function would only be called once and isn't independently meaningful
- It would require passing 5+ parameters (consider grouping related data)
- It would make the code harder to follow due to indirection

## Helper Detection Heuristics

When reading a large function, look for:
- Comments describing what a section does → extraction candidate
- Repeated code patterns → extract to function
- Deep nesting (3+ levels) → extract condition body
- Variables scoped to a small region → could be function-local

## Validation After Refactoring

After splitting, verify:
1. Each function has a single clear purpose
2. The original function reads like a high-level summary
3. No functions exceed your size threshold
4. Tests still pass (or are easier to write)
