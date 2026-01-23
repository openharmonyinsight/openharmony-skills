# XTS Test Constraints and Coding Standards

This file contains strict constraints and coding standards that MUST be followed when generating OpenHarmony XTS test cases.

## Table of Contents

1. [Type Safety](#type-safety)
2. [Error Handling](#error-handling)
3. [Code Style](#code-style)
4. [Forbidden Patterns](#forbidden-patterns)
5. [Test Framework Requirements](#test-framework-requirements)

---

## Type Safety

### Strict Type Declarations Required

All variables MUST have explicit type annotations:

```typescript
// CORRECT
let result: string = moduleName.methodName();
let callback: Callback = (data: string) => { console.info(data); };
let config: ConfigType = { property: 'value' };

// WRONG - No type annotation
let result = moduleName.methodName();
let callback = (data) => { console.info(data); };
```

### Forbidden Type Annotations

**NEVER use `any` or `unknown` types:**

```typescript
// FORBIDDEN
let data: any = result;
let params: unknown[] = [];

// REQUIRED - Use specific types
let data: string = result;
let params: string[] = [];
```

**NEVER use type assertions with `as any`:**

```typescript
// FORBIDDEN
let value = result as any;
let config = params as any;

// REQUIRED - Use proper types or type guards
let value: string = result as string;
let config: ConfigType = params as ConfigType;
```

### Import Type Patterns

```typescript
// For API modules, use the documented import
import mechanicManager from '@ohos.mechanicManager';
import fileio from '@ohos.fileio';

// For interfaces/types if exposed
import { ModuleName, InterfaceType } from '@ohos.moduleName';
```

---

## Error Handling

### Single Error Code Assertion

**Each test case may ONLY assert ONE error code:**

```typescript
// CORRECT
try {
  methodName(invalidParam);
  expect(false).assertFail();
} catch (error) {
  expect(error.code == 401).assertTrue();
}

// FORBIDDEN - Multiple error codes with ||
try {
  methodName(invalidParam);
  expect(false).assertFail();
} catch (error) {
  expect(error.code == 401 || error.code == 402).assertTrue(); // WRONG!
}

// FORBIDDEN - Multiple error codes with &&
expect(error.code == 401 && error.message == 'error message').assertTrue();
```

### Error Object Access

```typescript
// Access error properties
catch (error) {
  console.error('failed, code is ' + error.code + ', message is ' + error.message);
  expect(error.code == 401).assertTrue();
}

// Correct error logging patterns:
console.error('failed, code is ' + error.code + ', message is ' + error.message);
console.error(`failed, code is ${error.code}, message is ${error.message}`);
console.error(JSON.stringify(error, ['code', 'message']));
```

### Expected Error Scenarios

For tests expecting errors, use `assertFail()`:

```typescript
try {
  methodName(null); // Should throw
  expect(false).assertFail(); // Should not reach here
} catch (error) {
  expect(error.code == 401).assertTrue(); // Expected error
}
```

### No Error Expected Pattern

For tests expecting success, use success assertions:

```typescript
try {
  let result = methodName(validParam);
  expect(result != null).assertTrue(); // or assertEqual, etc.
} catch (error) {
  console.error('unexpected error, code is ' + error.code + ', message is ' + error.message);
  expect(error.code == expectedErrorCode).assertTrue();
}
```

---

## Code Style

### English Only

**All comments and logs MUST be in English:**

```typescript
// CORRECT
console.info('test start');
console.info('callback invoked');
/**
 * @tc.desc Test normal call scenario
 */

// WRONG
console.info('测试开始');
console.info('回调被调用');
/**
 * @tc.desc 测试正常调用场景
 */
```

### Console Log Format

Use standard log format with test number delimiters:

```typescript
console.info("-----------------SUB_MM_ModuleName_methodName_0100 begin-----------------");
// test code
console.info("-----------------SUB_MM_ModuleName_methodName_0100 end-----------------");
```

### Error Log Format

```typescript
console.error('SUB_MM_ModuleName_methodName_0100 failed, code is ' + error.code + ', message is ' + error.message);
```

---

## Forbidden Patterns

### Type Assertions

```typescript
// FORBIDDEN
as any
as unknown
let x: any;
let x: unknown;

// Use proper types instead
as string
as Callback
let x: string;
```

### Multiple Error Codes

```typescript
// FORBIDDEN
expect(error.code == 401 || error.code == 402).assertTrue();
expect(error.code == 401 && error.code == 402).assertTrue();

// Create separate test cases for each error code
```

### Missing Type Annotations

```typescript
// FORBIDDEN
let result = methodName();
let callback = (data) => console.log(data);

// REQUIRED
let result: ReturnType = methodName();
let callback: CallbackType = (data: DataType) => console.log(data);
```

### Missing Done Callback

Lifecycle hooks MUST use `done` callback:

```typescript
// REQUIRED
beforeAll(async (done: Function) => {
  console.info('beforeAll called');
  done();
});

// FORBIDDEN - Missing done
beforeAll(async () => {
  console.info('beforeAll called');
});
```

---

## Test Framework Requirements

### Hypium Imports

```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
```

### Test Decorators

```typescript
// Standard test case
it('testNumber', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  // test code
});

// Test with done callback
it('testNumber', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
  // test code
  done();
});
```

### Test Types

- `TestType.FUNCTION` - Function tests
- `TestType.PERFORMANCE` - Performance tests

### Test Sizes

- `Size.SMALLTEST` - Small tests (< 1s)
- `Size.MEDIUMTEST` - Medium tests (1-10s)
- `Size.LARGETEST` - Large tests (> 10s)

### Test Levels

- `Level.LEVEL0` - Basic smoke tests
- `Level.LEVEL1` - Basic functionality
- `Level.LEVEL2` - Edge cases
- `Level.LEVEL3` - Comprehensive tests
- `Level.LEVEL4` - Stress tests

---

## API Method Patterns

### Event Methods (on/off)

Event methods require special handling:

```typescript
// Register event
let callback: Callback = (data: DataType) => {
  console.info('event received: ' + JSON.stringify(data));
};
mechanicManager.on('eventType', callback);

// Unregister event (cleanup)
mechanicManager.off('eventType', callback);
```

### Async Methods

```typescript
// Use await for promises
let result: ReturnType = await moduleName.asyncMethod(param);

// Or handle promise rejection
moduleName.asyncMethod(param).then((result: ReturnType) => {
  expect(result != null).assertTrue();
}).catch((error: BusinessError) => {
  expect(error.code == errorCode).assertTrue();
});
```

### Callback Methods

```typescript
moduleName.callbackMethod(param, (error: BusinessError, result: ReturnType) => {
  if (error) {
    console.error('callback error: ' + error.message);
    expect(false).assertFail();
    done();
    return;
  }
  expect(result != null).assertTrue();
  done();
});
```

---

## File Naming and Organization

### Output File Names

- Format: `{ModuleName}.test.ets`
- Examples: `MechanicManager.test.ets`, `FileSystem.test.ets`

### Output Directory

```
{projectRoot}/entry/src/ohosTest/ets/test/
```

### Module Name Mapping

| API Module | Test File | Subsystem |
|------------|-----------|-----------|
| @ohos.mechanicManager | MechanicManager.test.ets | MM |
| @ohos.file.fs | FileSystem.test.ets | DF |
| @ohos.net.http | Http.test.ets | NET |

---

## Common Error Codes

| Code | Description |
|------|-------------|
| 401 | Parameter error |
| 202 | Permission denied |
| 33300001 | Operation failed |
| 13900001 | Parameter check failed |

When generating error tests, use appropriate error codes from the API documentation.
