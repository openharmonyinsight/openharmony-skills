# ArkTS Modules Reference

## Import/Export

### Named Exports

```typescript
// math.ets
export const PI: number = 3.14159
export function square(n: number): number { return n * n }
export class Calculator {}
```

```typescript
// main.ets
import { PI, square, Calculator } from "./math"
```

### Default Exports

```typescript
// utils.ets
export default function log(msg: string): void {
  console.log(msg)
}
```

```typescript
// main.ets
import log from "./utils"
```

### Namespace Import

```typescript
import * as math from "./math"
math.PI
math.square(5)
```

### Re-exports

```typescript
export { PI, square } from "./math"
export { default as log } from "./utils"
```

---

## Namespaces

```typescript
namespace MyNamespace {
  export const value: number = 42

  export function func(): void {
    console.log(value)
  }

  // Nested namespace
  export namespace Inner {
    export const nested: string = "nested"
  }
}

// Usage
MyNamespace.func()
MyNamespace.Inner.nested
```

---

## Ambient Declarations

```typescript
// Declare external module
declare module "external-lib" {
  export function externalApi(): string
}

// Declare ambient variable
declare const globalConfig: Config

// Declare ambient function
declare function nativeFunction(): void
```
