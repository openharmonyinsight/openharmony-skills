# ArkTS Error Handling Reference

## Error Class

```typescript
class Error {
  constructor(message?: string)
  name: string
  message: string
  stack?: string
}
```

---

## throw Statement

```typescript
class CustomError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "CustomError"
  }
}

function divide(a: number, b: number): number {
  if (b === 0) {
    throw new CustomError("Division by zero")
  }
  return a / b
}
```

**Requirement:** Thrown expression must be assignable to `Error`

---

## try-catch-finally

```typescript
try {
  // Code that may throw
  riskyOperation()
} catch (e: Error) {
  // Handle error
  console.log(e.message)
} finally {
  // Cleanup (always runs)
  cleanup()
}
```

---

## Catch Clause

```typescript
// Simple catch
try {
  throw new Error("error")
} catch (e: Error) {
  console.log(e.message)
}
```

**Catch variable type:** Always `Error`

---

## Finally Clause

```typescript
function process(): void {
  let resource: Resource | null = null

  try {
    resource = acquireResource()
    // Use resource
  } finally {
    // Always cleanup, even if error thrown
    if (resource !== null) {
      resource.release()
    }
  }
}
```

---

## Execution Flow

| Scenario | Flow |
|----------|------|
| No error | try → finally |
| Error, catch present | try → catch → finally |
| Error, no catch | Error propagates, finally executes |

---

## User-Defined Errors

```typescript
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message)
    this.name = "ValidationError"
  }
}

function validate(value: string): void {
  if (value.length === 0) {
    throw new ValidationError("value", "Cannot be empty")
  }
}
```

---

## Uncaught Errors

If an error is not caught, `UncaughtExceptionError` is thrown and the program may terminate.
