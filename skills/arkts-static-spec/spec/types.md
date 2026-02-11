# ArkTS Type System Reference

## Table of Contents
1. [Type Categories](#type-categories)
2. [Predefined Types](#predefined-types)
3. [User-Defined Types](#user-defined-types)
4. [Special Types](#special-types)
5. [Union Types](#union-types)
6. [Intersection Types](#intersection-types)
7. [Array Types](#array-types)
8. [Type Relationships](#type-relationships)

---

## Type Categories

ArkTS types are divided into:

- **Predefined types**: Built-in types provided by the language
- **User-defined types**: Classes, interfaces, enums, type aliases
- **Special types**: void, null, undefined, any, unknown, never

---

## Predefined Types

### Numeric Types

| Type | Description | Size | Range |
|------|-------------|------|-------|
| `byte` | 8-bit signed integer | 8 bits | -128 to 127 |
| `short` | 16-bit signed integer | 16 bits | -32,768 to 32,767 |
| `int` | 32-bit signed integer | 32 bits | -2³¹ to 2³¹-1 |
| `long` | 64-bit signed integer | 64 bits | -2⁶³ to 2⁶³-1 |
| `float` | 32-bit floating point | 32 bits | IEEE 754 |
| `double` | 64-bit floating point | 64 bits | IEEE 754 |
| `number` | Alias for `double` | 64 bits | IEEE 754 |
| `bigint` | Arbitrary precision integer | unlimited | N/A |

**Integer literals** default to `int` if value fits, otherwise `long`:

```typescript
let a: int = 42              // OK
let b: int = 0x7FFF_FFFF     // OK (max int)
let c: long = 0x8000_0000    // Needs long
```

**Float literals** require `f` suffix for `float` type:

```typescript
let pi: double = 3.14159     // double
let e: float = 2.718f        // float
```

### Boolean Type

```typescript
let flag: boolean = true
```

### String Type

```typescript
let name: string = "ArkTS"
let multiline: string = `Line 1
Line 2`
```

### Character Type (Experimental)

```typescript
let ch: char = c'A'  // Note: 'c' prefix is required
```

**Important:** Character literals MUST use `c'...'` syntax. Regular string literals like `'A'` cannot be used with char type.

```typescript
// ✅ Correct
let ch: char = c'A'

// ❌ Wrong - compile error
let ch: char = 'A'

// Other escape sequences
let newline: char = c'\n'
let tab: char = c'\t'
let hex: char = c'\x7F'
let unicode: char = c'\u0000'
```

---

## Special Types

### void

Used for functions that return no value:

```typescript
function log(message: string): void {
  console.log(message)
}
```

### null

Represents a null reference:

```typescript
let nullable: string | null = null
```

### undefined

Represents undefined value:

```typescript
let optional: string | undefined = undefined
```

### any

Top type, can hold any value (not recommended):

```typescript
let data: any = 42  // Avoid using any
```

### unknown

Type-safe alternative to `any`:

```typescript
function process(value: unknown) {
  if (typeof value === "string") {
    console.log(value.toUpperCase())  // Type narrowing
  }
}
```

### never

Bottom type, for functions that never return:

```typescript
function throwError(message: string): never {
  throw new Error(message)
}
```

---

## Union Types

Combine multiple types with `|`:

```typescript
let value: number | string
value = 42         // OK
value = "hello"    // OK
```

Union type normalization removes duplicates and subtypes:

```typescript
type T = number | int        // Normalizes to: number
type U = string | string     // Normalizes to: string
```

---

## Intersection Types

Combine multiple types with `&`:

```typescript
type Named = { name: string }
type Aged = { age: number }

type Person = Named & Aged

let person: Person = { name: "Alice", age: 30 }
```

---

## Array Types

### Dynamic Arrays (Resizable)

```typescript
let numbers: number[] = [1, 2, 3]
let strings: Array<string> = ["a", "b", "c"]
numbers.push(4)  // Can add elements
```

### Fixed-Size Arrays (Experimental)

**Note:** `FixedArray<T>` is an experimental feature with better performance but fixed length.

```typescript
let chars: FixedArray<string> = ['a', 'b', 'c']
let nums: FixedArray<number> = [1, 2, 3]

// Access elements
chars[0] = 'x'  // OK: modify element
let len = chars.length  // OK: get length

// No methods available
// chars.push('d')  // ERROR: FixedArray has no methods
```

**FixedArray constructors:**

```typescript
// Using default values
let a = new FixedArray<number>(3)        // [0.0, 0.0, 0.0]

// Fill with specified value
let b = new FixedArray<string>(3, "a")   // ["a", "a", "a"]

// Generate with function
let c = new FixedArray<int>(3, (inx: int) => 3 - inx)  // [3, 2, 1]
```

**Important:** `FixedArray<T>` and `Array<T>` are incompatible types.

### Tuple Types

```typescript
let tuple: [number, string] = [42, "hello"]
let triple: [number, number, number] = [1, 2, 3]
```

### Readonly Arrays

```typescript
function sum(arr: readonly number[]) {
  console.log(arr[0])   // OK: read
  arr[0] = 5            // ERROR: cannot modify
}
```

---

## Type Relationships

### Subtyping

```typescript
let num: number = 42    // OK: int is subtype of number
let intVal: int = num   // ERROR: requires explicit conversion
```

### Assignability

A type `S` is assignable to type `T` if:
- `S` is a subtype of `T`, OR
- `S` can be implicitly converted to `T`

### Widening Numeric Conversions

Smaller numeric types can widen to larger ones:

```typescript
let b: byte = 1
let i: int = b      // byte widens to int
let l: long = i     // int widens to long
let d: double = l   // long widens to double
```

---

## Type Inference

### From Initializer

```typescript
let x = 42              // Type inferred as: int
let y = 3.14            // Type inferred as: double
let s = "hello"         // Type inferred as: string
```

### Literal Type Widening

```typescript
const a = 1             // Type: 1 (literal type)
let b = 2               // Type: int (widened from literal)
```

---

## Default Values

| Type | Default Value |
|------|--------------|
| Numeric types | 0 |
| boolean | false |
| string | "" (empty string) |
| class/interface | null |

Variables without explicit initializers use default values:

```typescript
let x: int                // Initialized to 0
let s: string             // Initialized to ""
let obj: MyClass | null   // Initialized to null
```
