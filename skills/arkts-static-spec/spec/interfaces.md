# ArkTS Interfaces Reference

## Interface Declaration

```typescript
interface Drawable {
  draw(): void
}
```

---

## Interface Properties

```typescript
interface Point {
  x: number
  y: number
  readonly name: string  // Readonly property
}
```

---

## Interface Methods

```typescript
interface Calculator {
  add(a: number, b: number): number
  subtract(a: number, b: number): number
}
```

---

## Implementing Interfaces

```typescript
interface Drawable {
  draw(): void
}

class Circle implements Drawable {
  public draw(): void {
    console.log("Drawing circle")
  }
}
```

**Multiple interfaces:**

```typescript
interface Readable {
  read(): string
}

interface Writable {
  write(data: string): void
}

class File implements Readable, Writable {
  public read(): string { /* ... */ }
  public write(data: string): void { /* ... */ }
}
```

---

## Interface Inheritance

```typescript
interface Shape {
  area(): number
}

interface ColoredShape extends Shape {
  color: string
}

// Must implement both methods
class Circle implements ColoredShape {
  color: string = "red"

  area(): number {
    return Math.PI * 10 * 10
  }
}
```

**Multiple inheritance:**

```typescript
interface A { methodA(): void }
interface B { methodB(): void }

interface C extends A, B {
  methodC(): void
}
```

---

## Default Access

All interface members are `public` by default (access modifiers not needed).

---

## Optional Properties

```typescript
interface Config {
  required: string
  optional?: number  // Optional property
}

function useConfig(config: Config): void {
  console.log(config.required)
  if (config.optional !== undefined) {
    console.log(config.optional)
  }
}
```

---

## Key Differences from Classes

| Feature | Interface | Class |
|---------|-----------|-------|
| Instantiation | No | Yes |
| Implementation | No | Yes |
| Multiple inheritance | Yes | No |
| Access modifiers | No (public only) | Yes |
| Constructors | No | Yes |

---

## Structural Typing

ArkTS uses **nominal typing** for classes but supports interface implementation:

```typescript
interface Named {
  name: string
}

class Person {
  constructor(public name: string) {}
}

// Requires explicit 'implements'
class Employee implements Named {
  name: string = "John"
}
```
