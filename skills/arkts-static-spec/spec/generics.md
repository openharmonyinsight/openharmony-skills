# ArkTS Generics Reference

## Generic Declaration

```typescript
// Generic function
function identity<T>(value: T): T {
  return value
}

// Generic class
class Box<T> {
  private value: T

  constructor(value: T) {
    this.value = value
  }

  public get(): T {
    return this.value
  }
}
```

---

## Type Parameters

### Syntax

```typescript
function func<T>() {}
class Class<T, U>() {}
type Alias<T> = {}
```

### Constraints

```typescript
// Upper bound constraint
function process<T extends Number>(value: T): number {
  return value.valueOf()
}

// Multiple constraints
interface A { methodA(): void }
interface B { methodB(): void }

function combine<T extends A & B>(obj: T): void {
  obj.methodA()
  obj.methodB()
}
```

---

## Generic Classes

```typescript
class Container<T> {
  private items: T[] = []

  public add(item: T): void {
    this.items.push(item)
  }

  public get(index: number): T {
    return this.items[index]
  }
}

// Usage
let numbers: Container<number> = new Container<number>()
numbers.add(42)
```

---

## Generic Interfaces

```typescript
interface Repository<T> {
  findById(id: number): T | null
  save(entity: T): void
}

class UserRepository implements Repository<User> {
  findById(id: number): User | null { /* ... */ }
  save(user: User): void { /* ... */ }
}
```

---

## Type Parameter Defaults

```typescript
function create<T = string>(value?: T): T {
  return value as T
}

create()        // Type: string
create(42)      // Type: number
```

---

## Variance

**Invariant by default** (for mutable generics):

```typescript
class Box<T> {
  private value: T

  constructor(value: T) {
    this.value = value
  }
}

let boxString: Box<string> = new Box<string>("hello")
let boxObject: Box<Object> = boxString  // ERROR: invariant
```

---

## Wildcards

Using union types for flexibility:

```typescript
function process(box: Box<string | number>): void {
  // Can accept Box<string> or Box<number>
}
```

---

## Type Inference

```typescript
// Generic type inference
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second]
}

let result = pair(1, "hello")  // Types inferred as: [number, string]
```

---

## Generic Methods in Non-Generic Classes

```typescript
class Util {
  static identity<T>(value: T): T {
    return value
  }
}

let x: number = Util.identity<number>(42)
let y: string = Util.identity("hello")  // Type inferred
```

---

## Key Rules

1. **Type parameter scope**: Class type parameters don't apply to static members

2. **Constraint syntax**: Use `extends` for upper bounds

3. **Default values**: Type parameters can have default types

4. **Inference**: Generic types are often inferred from arguments

5. **Variance**: Most generic types are invariant for safety
