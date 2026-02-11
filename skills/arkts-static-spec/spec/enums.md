# ArkTS Enumerations Reference

## Enum Declaration

### Numeric Enum (default)

```typescript
enum Direction {
  North,  // 0
  South,  // 1
  East,   // 2
  West    // 3
}

let dir: Direction = Direction.North
console.log(dir)  // 0
console.log(Direction[dir])  // "North"
```

### String Enum

```typescript
enum Color {
  Red = "red",
  Green = "green",
  Blue = "blue"
}

let c: Color = Color.Red
console.log(c)  // "red"
```

### Explicit Numeric Values

```typescript
enum Priority {
  Low = 1,
  Medium = 5,
  High = 10
}
```

### Computed Values

```typescript
enum Size {
  Small = 1,
  Medium = Small * 2,
  Large = Medium * 2
}
```

---

## Enum with Explicit Type

```typescript
enum StatusCode: number {
  OK = 200,
  NotFound = 404
}

enum Message: string {
  Hello = "hi",
  Bye = "goodbye"
}
```

---

## Enum Usage

```typescript
enum Day {
  Monday,
  Tuesday,
  Wednesday,
  Thursday,
  Friday
}

function isWeekend(day: Day): boolean {
  return day === Day.Saturday || day === Day.Sunday
}
```

---

## Key Rules

1. **Const enums**: Not supported

2. **Enum members**: Must be constant values

3. **Type inference**: Enum type inferred from base type

4. **String conversion**: String enums convert to `string` type

5. **Numeric conversion**: Numeric enums convert to base numeric type
