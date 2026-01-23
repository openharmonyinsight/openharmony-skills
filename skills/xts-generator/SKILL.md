---
name: xts-generator
description: Generate OpenHarmony XTS (Compatibility Test Suite) test cases from API documentation. Use when generating or modifying XTS test files (.ets) for OpenHarmony API testing, including: (1) Creating new test files from API documentation, (2) Adding test cases for new methods, (3) Generating tests for enum types, (4) Creating optional parameter combination tests, (5) Writing exception/boundary test cases. This skill enforces strict type safety (no `any`/`unknown`), proper error handling (single error code assertions), and Hypium test framework conventions.
---

# XTS Test Case Generator

Generate OpenHarmony XTS test cases following strict coding standards and test patterns.

## Quick Reference

When generating XTS test cases, consult these references:

- **[Test Patterns & Templates](references/xts-patterns.md)** - File structure, test scenarios, code templates
- **[Constraints & Standards](references/xts-constraints.md)** - Type safety rules, error handling, forbidden patterns

## Test File Generation Process

### 1. Parse API Documentation

From Markdown API documentation (js-apis-{module}.md), extract:
- Module name and import statement
- Method signatures with parameters
- Return types and error codes
- Enum definitions
- Permissions required
- Example code patterns

### 2. Generate Test Cases

For each API method, generate test cases following these scenarios:

| Scenario | Number | Description |
|----------|--------|-------------|
| Normal | `0100` | Required - Normal/expected call |
| Null | `0200` | Exception - null parameter |
| Undefined | `0201` | Exception - undefined parameter |
| Optional combos | `0500+` | For N optional params, generate 2^N tests |
| Enum | `0900+` | One test per enum type |
| File path | `2000+` | For file APIs with path parameter |
| File URI | `2100+` | For file APIs with URI parameter |

### 3. Test Case Number Format

```
SUB_{子系统缩写}_{模块名}_{方法名}_{场景}_{序号}
```

Examples:
- `SUB_MM_MechanicManager_on_0100` - Normal call
- `SUB_MM_MechanicManager_on_Null_0200` - Null parameter
- `SUB_MM_MechanicManager_EnumType_0900` - Enum test

## Critical Constraints

### Type Safety (Strict)

```typescript
// CORRECT - Explicit types
let result: string = methodName(param);
let callback: Callback = (data: DataType) => { };

// FORBIDDEN
let result = methodName(param);           // No type
let data: any = result;                   // any type
let value: unknown = param;               // unknown type
let x = result as any;                    // as any
```

### Error Handling (Single Error Code)

```typescript
// CORRECT - One error code only
catch (error) {
  expect(error.code == 401).assertTrue();
}

// FORBIDDEN - Multiple error codes
expect(error.code == 401 || error.code == 402).assertTrue();
expect(error.code == 401 && error.code == 402).assertTrue();
```

### English Only

All comments, logs, and JSDoc must be in English.

## Common Test Template

```typescript
/**
 * @tc.number SUB_MM_ModuleName_methodName_0100
 * @tc.name SUB_MM_ModuleName_methodName_0100
 * @tc.desc Test normal call scenario for methodName
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 0
 */
it('SUB_MM_ModuleName_methodName_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  console.info("-----------------SUB_MM_ModuleName_methodName_0100 begin-----------------");
  try {
    let result: ReturnType = moduleName.methodName(param1, param2);
    expect(result != null).assertTrue();
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == errorCode).assertTrue();
  }
  console.info("-----------------SUB_MM_ModuleName_methodName_0100 end-----------------");
});
```

## When to Use References

### Read xts-patterns.md for:
- Complete file structure templates
- Lifecycle hook implementations
- File operation utilities (nextFileName, prepareFile)
- Specific test scenario patterns (0100, 0200, 0900, 2000, 2100)
- Event method patterns (on/off)
- Async/callback patterns

### Read xts-constraints.md for:
- Type safety rules and forbidden patterns
- Error handling standards
- Code style requirements
- Test framework requirements (Hypium)
- Common error codes
- File naming conventions

## Input Types

### From API Documentation
- Method definitions with signatures
- Parameter types and names
- Return type descriptions
- Error code lists
- Enum definitions
- Example code blocks

### Test Requirements
- Subsystem abbreviation (MM, DF, NET, etc.)
- Module name
- Test scenarios to cover
- File paths for file-related APIs

## Output

Generated `.ets` test file with:
- Proper copyright header
- Hypium framework imports
- Complete lifecycle hooks
- Numbered test cases for each scenario
- Type-safe code with no `any`/`unknown`
- Proper error handling with single error codes
- English-only comments and logs
