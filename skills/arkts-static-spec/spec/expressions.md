# ArkTS Expressions Reference

## Operator Precedence (Highest to Lowest)

| Precedence | Operators | Association |
|------------|-----------|-------------|
| 1 | `x.y`, `x[y]`, `x[y]`, `x()`, `x?.y`, `x?.[y]`, `x?.()`, `new X()`, `x++`, `x--` | Left-to-Right |
| 2 | `++x`, `--x`, `+x`, `-x`, `~x`, `!x`, `typeof x`, `void x`, `await x` | Right-to-Left |
| 3 | `**` | Right-to-Left |
| 4 | `*`, `/`, `%` | Left-to-Right |
| 5 | `+`, `-` | Left-to-Right |
| 6 | `<<`, `>>`, `>>>` | Left-to-Right |
| 7 | `<`, `>`, `<=`, `>=`, `in`, `instanceof` | Left-to-Right |
| 8 | `==`, `!=`, `===`, `!==` | Left-to-Right |
| 9 | `&` | Left-to-Right |
| 10 | `^` | Left-to-Right |
| 11 | `\|` | Left-to-Right |
| 12 | `&&` | Left-to-Right |
| 13 | `\|\|` | Left-to-Right |
| 14 | `??` | Left-to-Right |
| 15 | `? :` (ternary) | Right-to-Left |
| 16 | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `>>>=`, `&=`, `^=`, `\|=`, `**=` | Right-to-Left |
| 17 | `yield`, `yield*` | Right-to-Left |

---

## Primary Expressions

### Literals

```typescript
42                  // Integer literal
3.14                // Float literal
"hello"             // String literal
true                // Boolean literal
null                // Null literal
undefined           // Undefined literal
```

### This Expression

```typescript
class Example {
  private field: string = "value"

  method(): string {
    return this.field  // 'this' refers to current instance
  }
}
```

### Super Expression

```typescript
class Child extends Parent {
  method(): void {
    super.method()  // Call parent method
  }
}
```

### Identifier

```typescript
let x: number = 42
console.log(x)  // 'x' is an identifier expression
```

---

## Unary Expressions

### Increment/Decrement

```typescript
let x: number = 5
x++       // Post-increment: returns 5, then x becomes 6
++x       // Pre-increment: x becomes 6, then returns 6
x--       // Post-decrement: returns 6, then x becomes 5
--x       // Pre-decrement: x becomes 5, then returns 5
```

### Arithmetic Unary

```typescript
let x: number = -5
let y: number = +x      // y = -5
let z: number = -x      // z = 5
```

### Logical Not

```typescript
let flag: boolean = true
let result: boolean = !flag  // result = false
```

### Bitwise Not

```typescript
let x: number = 5   // binary: 101
let y: number = ~x  // binary: ~101 = ...11111010 (two's complement)
```

### Typeof

```typescript
let x: number = 42
console.log(typeof x)  // "number"
console.log(typeof "hello")  // "string"
```

---

## Binary Expressions

### Arithmetic Operators

```typescript
let a: number = 10, b: number = 3

a + b     // Addition: 13
a - b     // Subtraction: 7
a * b     // Multiplication: 30
a / b     // Division: 3.333...
a % b     // Modulo: 1
a ** b    // Exponentiation: 1000
```

### Comparison Operators

```typescript
let a: number = 5, b: number = 10

a < b     // Less than: true
a <= b    // Less than or equal: true
a > b     // Greater than: false
a >= b    // Greater than or equal: false
```

### Equality Operators

```typescript
5 == 5        // Equal: true
5 != 5         // Not equal: false
5 === 5        // Strict equal: true
5 !== 5        // Strict not equal: false
```

### Logical Operators

```typescript
let a: boolean = true, b: boolean = false

a && b    // Logical AND: false
a || b    // Logical OR: true
!a        // Logical NOT: false
```

### Bitwise Operators

```typescript
let a: number = 5  // 101
let b: number = 3  // 011

a & b     // AND: 001 (1)
a | b     // OR: 111 (7)
a ^ b     // XOR: 110 (6)
a << 1    // Left shift: 1010 (10)
a >> 1    // Right shift: 10 (2)
a >>> 1   // Unsigned right shift: 10 (2)
```

---

## Conditional Expression

```typescript
let condition: boolean = true
let result: string = condition ? "yes" : "no"  // "yes"
```

### Type Inference in Ternary

```typescript
function cond(): boolean { return Math.random() < 0.5 }

let a = cond() ? 1 : 2              // Type: int (compile-time unknown, same type)
let b = cond() ? 3 : 3.14           // Type: int | double
let c = cond() ? "one" : "two"      // Type: string
let d = cond() ? 1 : "one"          // Type: int | string
```

---

## Assignment Expression

```typescript
let x: number = 5

x = 10           // Simple assignment
x += 5           // Addition assignment: x = x + 5
x -= 3           // Subtraction assignment: x = x - 3
x *= 2           // Multiplication assignment
x /= 4           // Division assignment
x %= 3           // Modulo assignment
```

---

## Spread Expression

### Spread in Array Literals

```typescript
let arr1: number[] = [1, 2, 3]
let arr2: number[] = [...arr1, 4, 5]  // [1, 2, 3, 4, 5]
```

### Spread in Function Calls

```typescript
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0)
}

let nums: number[] = [1, 2, 3]
sum(...nums)  // Equivalent to: sum(1, 2, 3)
```

---

## Optional Chaining

```typescript
interface User {
  address?: {
    city?: string
  }
}

let user: User | null = null
let city: string | undefined = user?.address?.city  // undefined
```

---

## Nullish Coalescing

```typescript
let value: string | null = null
let result: string = value ?? "default"  // "default"
```

---

## Function Call Expression

```typescript
function greet(name: string, greeting: string = "Hello"): string {
  return `${greeting}, ${name}!`
}

greet("Alice")           // "Hello, Alice!"
greet("Bob", "Hi")       // "Hi, Bob!"
```

---

## Method Call Expression

```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b
  }
}

let calc: Calculator = new Calculator()
calc.add(5, 3)  // 8
```

---

## Lambda Expressions (Arrow Functions)

```typescript
// Basic syntax
let add = (a: number, b: number): number => a + b

// Single parameter (parentheses optional)
let square = (x: number): number => x * x

// No parameters
let getRandom = (): number => Math.random()

// Block body
let complex = (x: number): number => {
  let result: number = x * 2
  return result + 1
}
```

---

## instanceof Expression

```typescript
class Animal {}
class Dog extends Animal {}

let pet: Animal = new Dog()

console.log(pet instanceof Dog)    // true
console.log(pet instanceof Animal) // true
console.log(pet instanceof Object) // true
```

---

## as Expression (Type Assertion)

```typescript
let value: unknown = "hello"

// Type assertion
let str: string = value as string

// Non-null assertion
let nullable: string | null = "value"
let nonNull: string = nullable!  // Assert not null
```

---

## Key Expression Rules

1. **Operator precedence**: Determines evaluation order; use parentheses to override

2. **Type checking**: All expressions are type-checked at compile time

3. **Short-circuit evaluation**: `&&` and `||` operators evaluate operands lazily

4. **Nullish coalescing**: `??` only triggers on `null` or `undefined`, not other falsy values

5. **Optional chaining**: `?.` short-circuits if the left operand is `null` or `undefined`
