# ArkTS Statements Reference

## Statement Types

| Statement | Description |
|-----------|-------------|
| Expression Statement | Expression followed by semicolon |
| Block | `{ ... }` - sequence of statements |
| if-else | Conditional execution |
| while, do-while | Loops |
| for, for-of | Iteration |
| break, continue | Loop control |
| return | Function return |
| switch | Multi-way branch |
| throw | Exception throwing |
| try-catch-finally | Exception handling |

---

## if Statement

```typescript
// Basic if
if (condition) {
  // code
}

// if-else
if (condition) {
  // code
} else {
  // code
}

// if-else if-else
if (condition1) {
  // code
} else if (condition2) {
  // code
} else {
  // code
}
```

**Rules:**
- Expression must be `boolean` type
- `else` matches the nearest preceding `if`

---

## while and do-while Statements

```typescript
// while loop
let i: number = 0
while (i < 10) {
  console.log(i)
  i++
}

// do-while loop
let j: number = 0
do {
  console.log(j)
  j++
} while (j < 10)
```

---

## for Statement

```typescript
// Standard for loop
for (let i: int = 0; i < 10; i++) {
  console.log(i)
}

// Using existing variable
let k: int
for (k = 1; k < 10; k++) {
  console.log(k)
}

// Multiple initializers/updaters
for (let i: int = 0, j: int = 10; i < j; i++, j--) {
  console.log(i, j)
}
```

**Scope:** Variable declared in `forInit` has loop scope

---

## for-of Statement

```typescript
// Array iteration
let numbers: number[] = [1, 2, 3]
for (const num of numbers) {
  console.log(num)
}

// String iteration
for (const ch of "hello") {
  console.log(ch)
}

// With explicit type
for (let num: number of [1, 2, 3]) {
  console.log(num)
}
```

---

## break Statement

```typescript
// Without label
while (true) {
  break  // Exit innermost loop
}

// With label
outer: for (let i: int = 0; i < 10; i++) {
  for (let j: int = 0; j < 10; j++) {
    if (condition) {
      break outer  // Exit outer loop
    }
  }
}
```

---

## continue Statement

```typescript
// Without label
for (let i: int = 0; i < 10; i++) {
  if (i % 2 === 0) {
    continue  // Skip even numbers
  }
  console.log(i)
}

// With label
outer: for (let i: int = 0; i < 10; i++) {
  for (let j: int = 0; j < 10; j++) {
    if (condition) {
      continue outer  // Continue outer loop
    }
  }
}
```

---

## return Statement

```typescript
// With value
function add(a: number, b: number): number {
  return a + b
}

// Without value (void function)
function log(message: string): void {
  console.log(message)
  return
}

// In constructor
class Example {
  constructor() {
    return  // Valid
  }
}
```

---

## switch Statement

```typescript
let value: string = "B"

switch (value) {
  case "A":
    console.log("A")
    break
  case "B":
    console.log("B")
    break  // Without break, execution falls through
  case "C":
    console.log("C")
    break
  default:
    console.log("Other")
}
```

**Rules:**
- Case expressions must match switch expression type
- Fallthrough: execution continues without `break`
- Optional `default` clause

---

## throw Statement

```typescript
class CustomError extends Error {
  constructor(message: string) {
    super(message)
  }
}

function divide(a: number, b: number): number {
  if (b === 0) {
    throw new CustomError("Division by zero")
  }
  return a / b
}
```

**Requirement:** Expression must be assignable to `Error` type

---

## try-catch-finally Statement

```typescript
// try-catch
try {
  // code that may throw
} catch (e: Error) {
  // handle error
}

// try-finally
try {
  // code
} finally {
  // cleanup (always runs)
}

// try-catch-finally
try {
  // code
} catch (e: Error) {
  // handle error
} finally {
  // cleanup (always runs)
}
```

**Execution flow:**

1. No error: `try` → `finally`
2. Error with catch: `try` → `catch` → `finally`
3. Error without catch: error propagates, `finally` executes

---

## Block Statement

```typescript
{
  let x: number = 1
  console.log(x)
}
// x is not accessible here
```

**Scope:** Creates block scope for `let` and `const` declarations

---

## Local Declarations

```typescript
// let (mutable)
let x: number = 1
x = 2  // OK

// const (immutable)
const y: number = 1
// y = 2  // ERROR: cannot reassign const

// Type inference
let z = 3.14  // Type inferred as double
```

---

## Labeled Statements

```typescript
outer: for (let i: int = 0; i < 10; i++) {
  inner: for (let j: int = 0; j < 10; j++) {
    if (condition) {
      break outer
      continue inner
    }
  }
}
```

**Labels:** Can be used with `break` and `continue`
