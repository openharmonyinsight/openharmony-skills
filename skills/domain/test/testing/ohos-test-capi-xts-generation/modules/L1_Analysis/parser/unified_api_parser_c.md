# 头文件解析模块

> **Purpose**: Extract OpenHarmony CAPI function signatures from `.h` header files for N-API wrapper generation

---

## Expert-Only Requirements

### OpenHarmony Header File Patterns

**OpenHarmony-specific include paths**:
```
{OH_ROOT}/interface/sdk_c/{Subsystem}/{Module}/include/{Header}.h
```

**Typical header patterns**:
- Camera: `#include <ohcamera/camera_manager.h>` (note `ohcamera/` prefix)
- HiLog: `#include <hilog/log.h>`
- BundleManager: `#include <native_interface_bundle.h>`

**Expert parsing priorities**:
1. **Function declarations** — MUST extract: return type, function name, parameters (type + name)
2. **Error code macros** — Critical for ERROR-type test generation
3. **Struct definitions** — Required for complex parameter types
4. **Enum definitions** — Map to TypeScript enums in index.d.ts

### Non-Obvious Extraction Rules

#### Rule 1: Conditional compilation directives

OpenHarmony headers use extensive `#ifdef` blocks. Extract ALL variants:

```c
#ifdef OHOS_ENABLE_CAMERA
int32_t OH_Camera_Create(Camera **camera);
#endif

#ifdef OHOS_ENABLE_VIDEORECORDER
int32_t OH_VideoRecorder_Create(VideoRecorder **recorder);
#endif
```

**Expert decision**: Generate test cases for ALL variants, not just the first one. Each `#ifdef` represents a feature gate that may be enabled in different device configurations.

#### Rule 2: Function pointer parameters

```c
typedef void (*CameraStatusCallback)(int32_t status, void *userData);
int32_t OH_Camera_SetStatusCallback(Camera *camera, CameraStatusCallback callback, void *userData);
```

**Expert handling**:
- Extract function pointer signature
- Mark as "callback" type for special N-API handling (refer to `test_patterns_napi_ets_advance.md`)
- Generate ERROR tests for null callback scenarios

#### Rule 3: Handle-specific patterns

OpenHarmony uses opaque handles extensively:

```c
typedef struct Camera Camera;
int32_t OH_Camera_Create(Camera **camera);  // Note: double pointer
```

**Expert handling**:
- Detect `struct TypeName` followed by `TypeName **outParam` pattern
- Mark as "handle allocation" — requires special N-API test pattern
- Generate MEMORY tests for handle lifecycle

#### Rule 4: Attribute annotations

```c
__attribute__((visibility("default"))) int32_t OH_Camera_Start(Camera *camera);
```

**Expert decision**: Ignore visibility attributes for test generation. Focus only on function signature.

#### Rule 5: Bitmask parameter patterns

```c
#define OH_CAMERA_FEATURE_PREVIEW  (1 << 0)
#define OH_CAMERA_FEATURE_VIDEO    (1 << 1)
int32_t OH_Camera_EnableFeature(Camera *camera, uint32_t features);
```

**Expert handling**: Extract all bitmask macros and generate PARAM tests for individual bits and combinations.

#### Rule 6: Variadic functions

```c
int32_t OH_Log_Print(int32_t type, const char *format, ...);
```

**Expert handling**: Skip variadic functions for N-API wrapping. They require `va_list` handling which is error-prone. Log these as "requires manual implementation."

### API Information Structure

Output this exact JSON format:

```json
{
  "function_name": "OH_Camera_Create",
  "return_type": "int32_t",
  "return_meaning": "error code: 0 = success, others = failure",
  "parameters": [
    {
      "name": "camera",
      "type": "Camera **",
      "direction": "out",
      "is_handle": true,
      "requires_allocation": true
    }
  ],
  "macros": [
    {"name": "OH_CAMERA_SUCCESS", "value": "0"},
    {"name": "OH_CAMERA_ERROR_INVALID_PARAM", "value": "-1"}
  ],
  "test_requirements": {
    "param_tests": ["null pointer", "valid pointer"],
    "error_tests": ["OH_CAMERA_ERROR_INVALID_PARAM"],
    "memory_tests": ["handle allocation", "handle release"]
  }
}
```

### Common Edge Cases

#### Edge Case 1: Incomplete type definitions

```c
typedef struct Camera Camera;  // Forward declaration only
```

**Expert handling**: Mark as `is_opaque = true`. Don't generate tests that access struct fields directly. Test only through function interfaces.

#### Edge Case 2: Anonymous enums

```c
enum {
    CAMERA_STATUS_UNKNOWN = 0,
    CAMERA_STATUS_ACTIVE = 1
};
```

**Expert handling**: Extract as named enum by prefix:
```json
{
  "enum_name": "CameraStatus",
  "values": [
    {"name": "UNKNOWN", "value": "0"},
    {"name": "ACTIVE", "value": "1"}
  ]
}
```

#### Edge Case 3: Macro type aliases

```c
#define CAMERA_HANDLE void*
```

**Expert handling**: Expand macro and record mapping. Generate TypeScript as:
```typescript
export type CameraHandle = number;
```

#### Edge Case 4: Nested pointer types

```c
int32_t OH_Camera_GetFrame(Camera *camera, uint8_t **frameData, uint32_t *dataSize);
```

**Expert handling**:
- Detect `uint8_t **frameData` (double pointer) → mark as output buffer
- Detect `uint32_t *dataSize` (single pointer) → mark as output size
- Generate memory test for buffer allocation/deallocation

#### Edge Case 5: Const correctness in function signatures

```c
int32_t OH_Camera_SetConfig(Camera *camera, const CameraConfig *config);
```

**Expert handling**: The `const` qualifier is important for TypeScript interface generation:
```typescript
interface CameraConfig { /* ... */ }
export const OH_Camera_SetConfig: (camera: CameraHandle, config: CameraConfig) => number;
```
Note: Input parameters with `const` should be read-only in test cases.

### Parameter Type Mapping

| C Type | TypeScript Type | Special Handling |
|---------|-----------------|------------------|
| `int32_t` | `number` | — |
| `uint32_t` | `number` | Bitmask: generate combination tests |
| `char*` / `const char*` | `string` | Null check required |
| `void*` | `number` (as handle) | Handle lifecycle tests |
| `struct Name*` | `NameHandle` (custom type) | Forward declaration tests |
| `enum Name` | `Name` (enum) | Extract all values |
| `CallbackType*` | `(args: any[]) => void` | N-API async handling |

### Macro Definition Extraction

#### Constant macros (for error codes)

```c
#define OH_CAMERA_SUCCESS 0
#define OH_CAMERA_ERROR_INVALID_PARAM (-1)
#define OH_CAMERA_ERROR_NO_MEMORY (-2)
```

**Expert handling**: Extract as test error codes:
```json
{
  "error_codes": [
    {"name": "SUCCESS", "value": 0},
    {"name": "ERROR_INVALID_PARAM", "value": -1},
    {"name": "ERROR_NO_MEMORY", "value": -2}
  ]
}
```

Generate ERROR test cases for each non-zero error code.

#### Feature macros (conditional compilation)

```c
#ifdef OHOS_FEATURE_CAMERA_CAPTURE
int32_t OH_Camera_Capture(Camera *camera);
#endif
```

**Expert handling**: Record feature dependency:
```json
{
  "function_name": "OH_Camera_Capture",
  "feature_flag": "OHOS_FEATURE_CAMERA_CAPTURE",
  "requires_condition": true
}
```

### Documentation Comment Extraction

OpenHarmony headers may contain documentation comments:

```c
/**
 * @brief Create a camera instance
 * @param camera Output parameter for camera instance
 * @return 0 on success, error code on failure
 */
int32_t OH_Camera_Create(Camera **camera);
```

**Expert handling**: Extract and include in test description:
```json
{
  "function_name": "OH_Camera_Create",
  "brief": "Create a camera instance",
  "param_docs": {
    "camera": "Output parameter for camera instance"
  },
  "return_doc": "0 on success, error code on failure"
}
```

Use this documentation in `@tc.desc` field of generated test cases.

### Output Format Summary

After parsing a header file, output:

```markdown
## Header File Analysis Results

**File**: `{OH_ROOT}/interface/sdk_c/camera_framework/camera.h`

### Extracted Functions: N

| Function | Return Type | Parameters | Test Types Required |
|-----------|--------------|-------------|---------------------|
| OH_Camera_Create | int32_t | Camera ** | PARAM, ERROR, MEMORY |
| OH_Camera_Start | int32_t | Camera * | PARAM, ERROR |
| ... | ... | ... | ... |

### Extracted Macros: N

| Macro Name | Value | Type |
|------------|--------|------|
| OH_CAMERA_SUCCESS | 0 | Error Code |
| OH_CAMERA_ERROR_INVALID_PARAM | -1 | Error Code |
| ... | ... | ... |

### Complex Types: N

| Type Name | Definition | Opaque? |
|------------|-------------|----------|
| Camera | struct Camera | Yes |
| CameraConfig | ... | No |
| ... | ... | ... |

### Conditional Variants: N

| Feature Flag | Functions |
|--------------|-----------|
| OHOS_ENABLE_CAMERA_CAPTURE | OH_Camera_Capture, ... |
| OHOS_ENABLE_CAMERA_PREVIEW | OH_Camera_StartPreview, ... |
| ... | ... |

---
```

---

## Testing Coverage Analysis

### Existing Test File Scanning

Scan existing test files and extract:

1. **Test case list** — test case ID, name, description
2. **Covered APIs** — API name, covered parameter combinations, covered test scenarios
3. **Code style** — indentation, naming conventions, comment style

### Coverage Gap Analysis

Compare extracted API list with covered APIs and generate:

```markdown
## Coverage Analysis Report

### API Coverage

| API | Total Functions | Covered | Uncovered | Coverage % |
|-----|----------------|-----------|------------|-------------|
| Camera | 20 | 15 | 5 | 75% |

### Missing Tests

#### OH_Camera_Create
- [ ] PARAM test: null pointer
- [ ] PARAM test: valid pointer
- [ ] ERROR test: OH_CAMERA_ERROR_NO_MEMORY
- [ ] MEMORY test: handle allocation

#### OH_Camera_SetConfig
- [ ] PARAM test: invalid config structure
- [ ] ERROR test: OH_CAMERA_ERROR_INVALID_PARAM
- [ ] BOUNDARY test: config size limits

### Test Style Summary

- Indentation: 4 spaces
- Naming: camelCase for test functions
- Comments: `/* @tc.name: */` format
```

### Flow A (Coverage-Report-Driven) — Style Scan Only

When user provides coverage report:
1. Parse the report to extract missing test items
2. Scan existing test files for code style ONLY (naming patterns, comment style, test structure)
3. Generate tests directly per report's missing items
4. Do NOT re-analyze existing coverage

### Flow B (Standard Process) — Full Coverage

When no coverage report:
1. Scan all existing test files
2. Analyze method/param/error-code coverage
3. Generate gap report
4. Prefer supplementing existing project > creating new project

---

**版本**: 2.0.0
**更新日期**: 2026-05-12
