# ArkTS Standard Library Reference

## Global Objects

### console

```typescript
console.log(...args: any[]): void
console.error(...args: any[]): void
console.warn(...args: any[]): void
console.info(...args: any[]): void
```

### Math

```typescript
Math.abs(x: number): number
Math.ceil(x: number): number
Math.floor(x: number): number
Math.round(x: number): number
Math.max(...values: number[]): number
Math.min(...values: number[]): number
Math.pow(x: number, y: number): number
Math.sqrt(x: number): number
Math.random(): number
Math.sin(x: number): number
Math.cos(x: number): number
// ... and more
```

### JSON

```typescript
JSON.stringify(value: any): string
JSON.parse(text: string): any
```

---

## Common Types

### Array

```typescript
class Array<T> {
  length: number

  push(...items: T[]): number
  pop(): T | undefined
  shift(): T | undefined
  unshift(...items: T[]): number
  slice(start?: number, end?: number): T[]
  splice(start: number, deleteCount?: number): T[]
  indexOf(element: T): number
  includes(element: T): boolean
  forEach(callbackfn: (value: T, index: number) => void): void
  map<U>(callbackfn: (value: T, index: number) => U): U[]
  filter(callbackfn: (value: T) => boolean): T[]
  reduce(callbackfn: (acc: T, value: T) => T): T
  // ... and more
}
```

### Map

```typescript
class Map<K, V> {
  set(key: K, value: V): this
  get(key: K): V | undefined
  has(key: K): boolean
  delete(key: K): boolean
  clear(): void
  entries(): IterableIterator<[K, V]>
  keys(): IterableIterator<K>
  values(): IterableIterator<V>
  size: number
}
```

### Set

```typescript
class Set<T> {
  add(value: T): this
  has(value: T): boolean
  delete(value: T): boolean
  clear(): void
  values(): IterableIterator<T>
  size: number
}
```

---

## Date

```typescript
class Date {
  constructor()
  constructor(value: number | string)
  constructor(year: number, month: number, date?: number, ...)

  getTime(): number
  setDate(date: number): number
  setMonth(month: number): number
  setFullYear(year: number): number
  // ... and more
}
```

---

## String Methods

```typescript
interface String {
  length: number
  charAt(pos: number): string
  substring(start: number, end?: number): string
  slice(start?: number, end?: number): string
  toUpperCase(): string
  toLowerCase(): string
  trim(): string
  split(separator: string | RegExp): string[]
  indexOf(searchString: string): number
  includes(searchString: string): boolean
  replace(searchValue: string | RegExp, replaceValue: string): string
  match(regexp: string | RegExp): RegExpMatchArray | null
  // ... and more
}
```

---

## Promise

See [concurrency.md](concurrency.md) for details.
