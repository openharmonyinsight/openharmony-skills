# ArkTS Names, Declarations and Scopes Reference

## Simple Names

```typescript
let x: number = 42
console.log(x)  // Simple name reference
```

## Qualified Names

```typescript
// Module member access
import * as math from "./math"
math.square(5)

// Static member access
Math.PI

// Instance member access
obj.method()
```

---

## Declaration Scopes

### Module Level Scope

```typescript
// Constants/variables accessible from point of declaration
let x: number = 1
console.log(x)  // OK

export const PI: number = 3.14  // Exported, accessible in other modules
```

### Namespace Level Scope

```typescript
namespace MyNS {
  let x: number = 1      // Accessible from here to end of namespace
  export let y: number = 2  // Exported, needs namespace qualification
}

MyNS.y  // OK
// MyNS.x  // ERROR: not exported
```

### Class Level Scope

```typescript
class MyClass {
  private field: string = "private"
  public method(): string {
    return this.field  // OK: access within class
  }
}

let obj: MyClass = new MyClass()
// obj.field  // ERROR: private not accessible outside
obj.method()  // OK: public
```

### Function Level Scope

```typescript
function example(): void {
  let x: number = 1
  console.log(x)  // OK
}
// x not accessible here
```

### Block Scope

```typescript
{
  let x: number = 1
  console.log(x)  // OK
}
// x not accessible here
```

---

## Shadowing

Inner scope declarations shadow outer ones:

```typescript
let x: number = 1

{
  let x: string = "shadowed"
  console.log(x)  // "shadowed"
}

console.log(x)  // 1
```

**Parameters shadow top-level variables:**

```typescript
let x: number = 1

function foo(x: string): void {
  console.log(x)  // x is string parameter
}
```

---

## Declaration Distinguishability

Declarations must be distinguishable by **name** or **signature**:

```typescript
// OK: Different names
function foo(): void {}
function bar(): void {}

// OK: Same name, different signatures (overloading)
function process(x: number): void {}
function process(x: string): void {}

// ERROR: Same name, same signature
function duplicate(): void {}
function duplicate(): void {}  // Compile-time error
```

---

## Accessibility Rules

| Scope | Accessibility |
|-------|---------------|
| Module | From declaration point to end of module (variables/const) or entire module (other declarations) |
| Namespace | Entire namespace (variables/const from declaration point) |
| Class | Within class (private), within class and subclasses (protected), everywhere (public) |
| Function/Block | From declaration point to end of block |
