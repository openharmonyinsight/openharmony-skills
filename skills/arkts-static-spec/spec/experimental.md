# ArkTS Experimental Features Reference

## Fixed-Size Arrays (FixedArray<T>)

### Syntax

```typescript
let chars: FixedArray<string> = ['a', 'b', 'c']
let nums: FixedArray<number> = [1, 2, 3]
```

### Characteristics

- **Fixed length**: Set once at runtime, cannot be changed
- **Better performance**: Optimized compared to resizable arrays
- **No methods**: Unlike `Array<T>`, FixedArray has no methods (push, pop, etc.)
- **Type incompatible**: `FixedArray<T>` and `Array<T>` are not compatible

### Creation Methods

**Array literal:**

```typescript
let a: FixedArray<number> = [1, 2, 3]
a[1] = 7                    // Modify element
let y = a[2]                // Access element
let count = a.length        // Get length
// y = a[3]                 // Runtime error: out of bounds
```

**Constructors:**

```typescript
// Using default value
let a = new FixedArray<number>(3)        // [0.0, 0.0, 0.0]

// Fill with specified value
let b = new FixedArray<string>(3, "a")   // ["a", "a", "a"]

// Generate with function
let c = new FixedArray<int>(3, (inx: int) => 3 - inx)  // [3, 2, 1]
```

### Type Incompatibility

```typescript
function foo(a: FixedArray<number>, b: Array<number>) {
  a = b  // ERROR: cannot assign Array to FixedArray
  b = a  // ERROR: cannot assign FixedArray to Array
}
```

**Status:** Partly implemented (`frontend_status: Partly`)

---

## Character Type (char)

### Syntax

```typescript
// Character literal with 'c' prefix (REQUIRED)
let ch: char = c'A'

// Using constructor
let a_char = new char
a_char = c'B'

// Escape sequences
let newline: char = c'\n'
let hex: char = c'\x7F'
let unicode: char = c'\u0000'
```

**Important:** Character literals MUST use the `c'...'` syntax. Using regular string literals like `'A'` is **incorrect**.

```typescript
// ❌ WRONG - This will cause compile error
let ch: char = 'A'

// ✅ CORRECT
let ch: char = c'A'
```

### Characteristics

- **32-bit Unicode code points**: Values from U+0000 to U+10FFFF
- **Class type**: `char` is a class type, subtype of `Object`
- **No relational operators**: Cannot use `<`, `>`, `<=`, `>=` with char
- **Equality only**: `==`, `===`, `!=`, `!==` supported

### Equality Operators

```typescript
let a0 = new char
let a1 = new char
a0 = c'a'
a1 = c'a'

console.log(a0 == a1)   // true
console.log(a0 === a1)  // true

// ❌ ERROR: Relational operators not supported
a0 < a1  // Compile-time error

// ❌ ERROR: Cannot compare char with number
let x: number = 1
a0 == x  // Compile-time error
```

**Status:** Partly implemented (`frontend_status: Partly`)

---

## Function Overloading

```typescript
function process(x: number): string
function process(x: string): number
function process(x: number | string): string | number {
  if (typeof x === "number") {
    return x.toString()
  }
  return parseInt(x, 10)
}
```

**Status:** Partly implemented

---

## Native Functions

```typescript
native function nativeApi(): void
```

**Rules:**
- Cannot have body
- Implemented in native code

---

## For-Of Explicit Type Annotation

```typescript
for (let element: number of [1, 2, 3]) {
  console.log(element)
}
```

**Status:** Experimental

---

## Readonly Parameters

```typescript
function foo(arr: readonly number[]): void {
  console.log(arr[0])  // OK
  arr[0] = 5  // ERROR: readonly
}
```

---

## Important Notes

1. **Experimental features** may change or be removed
2. **Compiler support** varies by feature
3. **Check `frontend_status`** in specification for implementation status
4. **FixedArray<T>** requires concrete type `T` (not type parameter)
