# ArkTS Type Conversions Reference

## Conversion Contexts

### Assignment-like Contexts

- Variable declarations
- Const declarations
- Field declarations
- Assignments
- Function/method arguments
- Return statements
- Array/object literals

```typescript
let x: number = 42        // Assignment context
const s: string = "text"  // Constant declaration
function foo(p: number) {} // Parameter context
```

---

## Implicit Conversions

### Widening Numeric Conversions

Smaller numeric types automatically widen to larger types:

```typescript
let b: byte = 1
let s: short = b      // byte → short
let i: int = s        // short → int
let l: long = i       // int → long
let d: double = l     // long → double
```

**Conversion table:**

| From | To |
|------|-----|
| byte | short, int, long, float, double |
| short | int, long, float, double |
| int | long, float, double |
| long | float, double |
| float | double |

---

### Numeric Casting Conversions

Use standard library methods for explicit casting:

```typescript
let d: double = 3.14
let i: int = d.toInt()      // Explicit double → int

let l: long = 123456789
let s: short = l.toShort()  // Explicit long → short
```

**Rules:**
- Floating to integer: rounds toward zero
- NaN → 0
- Infinity → max/min representable value
- Larger to smaller integer: truncates bits

---

## String Conversion

In string concatenation context:

```typescript
console.log("Value: " + 42)        // "Value: 42"
console.log("Value: " + true)      // "Value: true"
console.log("Value: " + null)      // "Value: null"
```

---

## Forbidden Conversions

Some conversions are **not allowed** and cause compile-time errors:

```typescript
// No implicit narrowing
let i: int = 100
let b: byte = i  // ERROR: int → byte not allowed

// No user-defined type conversions
class A {}
class B {}
let a: A = new A()
let b: B = a  // ERROR: different types
```

---

## Assignability

Expression type `S` is assignable to type `T` if:

1. `S` is a subtype of `T`, OR
2. `S` can be implicitly converted to `T`, OR
3. Both are reference types and `S` implements `T`

```typescript
let num: number = 42       // OK: int is subtype of number
let obj: Object = "string"  // OK: string is subtype of Object
```
