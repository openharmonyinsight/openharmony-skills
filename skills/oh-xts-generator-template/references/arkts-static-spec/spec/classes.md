# ArkTS Classes Reference

## Table of Contents
1. [Class Declaration](#class-declaration)
2. [Access Modifiers](#access-modifiers)
3. [Constructors](#constructors)
4. [Fields](#fields)
5. [Methods](#methods)
6. [Inheritance](#inheritance)
7. [Abstract Classes](#abstract-classes)
8. [Static Members](#static-members)
9. [Getters and Setters](#getters-and-setters)

---

## Class Declaration

```typescript
class MyClass {
  // fields
  private field: string

  // constructor
  constructor(field: string) {
    this.field = field
  }

  // methods
  public method(): string {
    return this.field
  }
}
```

---

## Access Modifiers

| Modifier | Class | Subclass | Outside |
|----------|-------|----------|---------|
| `public` (default) | ✓ | ✓ | ✓ |
| `private` | ✓ | ✗ | ✗ |
| `protected` | ✓ | ✓ | ✗ |
| `readonly` | ✓ | ✓ | ✓ (read-only) |
| `static` | ✓ | ✓ | ✓ (class-level) |

```typescript
class Example {
  public publicField: string = "public"
  private privateField: string = "private"
  protected protectedField: string = "protected"
  readonly readonlyField: string = "readonly"

  static staticField: string = "static"
}
```

---

## Constructors

### Primary Constructor

```typescript
class Person {
  constructor(private name: string, public age: number) {}
}
```

### Overloaded Constructors

```typescript
class Point {
  constructor(x: number, y: number)
  constructor(coord: [number, number])
  constructor(xOrCoord: number | [number, number], y?: number) {
    // Implementation
  }
}
```

---

## Fields

### Field Declaration

```typescript
class Example {
  // With explicit type
  field1: string

  // With initializer
  field2: number = 42

  // Readonly
  readonly field3: string = "immutable"

  // Static
  static field4: boolean = true
}
```

### Field Initialization Order

1. Default values apply
2. Field initializers execute in declaration order
3. Constructor body executes

```typescript
class Order {
  let a: int = 1      // 1st
  let b: int = 2      // 2nd

  constructor() {
    console.log(this.a, this.b)  // 3rd
  }
}
```

---

## Methods

### Instance Methods

```typescript
class Calculator {
  public add(a: number, b: number): number {
    return a + b
  }
}
```

### Static Methods

```typescript
class MathUtil {
  public static square(n: number): number {
    return n * n
  }
}

MathUtil.square(5)  // 25
```

### Methods Returning `this`

```typescript
class Builder {
  public setName(name: string): this {
    // ...
    return this
  }

  public setAge(age: number): this {
    // ...
    return this
  }
}
```

### Method Overloading

```typescript
class Greeter {
  greet(name: string): string
  greet(names: string[]): string
  greet(nameOrNames: string | string[]): string {
    if (typeof nameOrNames === "string") {
      return `Hello, ${nameOrNames}!`
    }
    return `Hello, ${nameOrNames.join(", ")}!`
  }
}
```

---

## Inheritance

### Extending a Class

```typescript
class Animal {
  constructor(protected name: string) {}

  public speak(): string {
    return `${this.name} makes a sound`
  }
}

class Dog extends Animal {
  constructor(name: string) {
    super(name)  // Must call super()
  }

  public speak(): string {
    return `${this.name} barks`  // Override
  }
}
```

### Using `super`

```typescript
class Child extends Parent {
  method(): void {
    super.method()  // Call parent method
  }

  constructor(x: number) {
    super(x)  // Call parent constructor
  }
}
```

### Method Override

```typescript
class Parent {
  public method(): string {
    return "parent"
  }
}

class Child extends Parent {
  public override method(): string {  // 'override' keyword
    return super.method() + " overridden"
  }
}
```

---

## Abstract Classes

```typescript
abstract class Shape {
  abstract area(): number  // Must be implemented by subclasses

  public describe(): string {
    return `Area: ${this.area()}`
  }
}

class Circle extends Shape {
  constructor(private radius: number) {
    super()
  }

  public area(): number {
    return Math.PI * this.radius * this.radius
  }
}
```

---

## Static Members

```typescript
class Counter {
  private static count: number = 0

  public static increment(): void {
    Counter.count++
  }

  public static getCount(): number {
    return Counter.count
  }
}
```

---

## Getters and Setters

```typescript
class Person {
  private _name: string = ""

  get name(): string {
    return this._name
  }

  set name(value: string) {
    if (value.length > 0) {
      this._name = value
    }
  }
}

let p = new Person()
p.name = "Alice"  // setter
console.log(p.name)  // getter
```

---

## Initializer Blocks

```typescript
class Example {
  private field: string

  // Static initializer
  static {
    console.log("Class loaded")
  }

  // Instance initializer
  {
    this.field = "initialized"
    console.log("Instance created")
  }
}
```

---

## Key Rules

1. **Constructor requirement**: If a constructor is explicitly defined, all subclass constructors must call `super()`

2. **Field initialization**: Fields must be initialized before use (default value, initializer, or in constructor)

3. **Override requirement**: Use `override` keyword when overriding parent methods

4. **Abstract methods**: Abstract classes cannot be instantiated; abstract methods must be implemented by subclasses

5. **Static inheritance**: Static members are not inherited; they belong to the class that declares them
