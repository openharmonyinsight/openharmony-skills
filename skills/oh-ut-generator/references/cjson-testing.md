# CJSON Testing

## Overview

The system has identified through full codebase analysis (recursively 20 levels, covering all CJSON usage in the foundation directory):

- **CJSON library widely used**: OpenHarmony project extensively uses CJSON library for JSON parsing and generation
- **Common CJSON functions**: `cJSON_Parse`, `cJSON_GetObjectItem`, `cJSON_GetStringValue`, `cJSON_Create`, `cJSON_Delete`, etc.
- **CJSON test patterns**: Including parse tests, create tests, type check tests, memory management tests, etc.

## JSON Parsing Tests

### Normal Parsing

Test `cJSON_Parse()` successfully parsing valid JSON strings:

```cpp
HWTEST_F(JsonTest, ParseJson_001, TestSize.Level1) {
    const char* jsonStr = R"({"key":"value"})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);
    EXPECT_TRUE(cJSON_IsObject(json));
    cJSON_Delete(json);
}
```

### Null Pointer Check

Test returning `nullptr` when passing `nullptr` or empty strings:

```cpp
HWTEST_F(JsonTest, ParseJson_002, TestSize.Level1) {
    cJSON* json = cJSON_Parse(nullptr);
    EXPECT_EQ(json, nullptr);

    json = cJSON_Parse("");
    EXPECT_EQ(json, nullptr);
}
```

### Invalid JSON

Test returning `nullptr` when passing invalid JSON strings:

```cpp
HWTEST_F(JsonTest, ParseJson_003, TestSize.Level1) {
    const char* invalidJson = "{invalid json}";
    cJSON* json = cJSON_Parse(invalidJson);
    EXPECT_EQ(json, nullptr);
}
```

### Memory Management

Must call `cJSON_Delete()` to free memory after successful parsing:

```cpp
HWTEST_F(JsonTest, ParseJson_001, TestSize.Level1) {
    const char* jsonStr = R"({"key":"value"})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);
    // ... test logic ...
    cJSON_Delete(json);  // Must free
}
```

## Get Object Item Tests

### Normal Get

Test `cJSON_GetObjectItem()` or `cJSON_GetObjectItemCaseSensitive()` successfully getting items:

```cpp
HWTEST_F(JsonTest, GetObjectItem_001, TestSize.Level1) {
    const char* jsonStr = R"({"name":"test","age":30})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* nameItem = cJSON_GetObjectItemCaseSensitive(json, "name");
    ASSERT_NE(nameItem, nullptr);
    EXPECT_TRUE(cJSON_IsString(nameItem));
    EXPECT_STREQ(cJSON_GetStringValue(nameItem), "test");

    cJSON* ageItem = cJSON_GetObjectItemCaseSensitive(json, "age");
    ASSERT_NE(ageItem, nullptr);
    EXPECT_TRUE(cJSON_IsNumber(ageItem));
    EXPECT_EQ(cJSON_GetNumberValue(ageItem), 30.0);

    cJSON_Delete(json);
}
```

### Non-Existent Item

Test returning `nullptr` when getting non-existent keys:

```cpp
HWTEST_F(JsonTest, GetObjectItem_002, TestSize.Level1) {
    const char* jsonStr = R"({"name":"test"})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* item = cJSON_GetObjectItemCaseSensitive(json, "nonexistent");
    EXPECT_EQ(item, nullptr);

    cJSON_Delete(json);
}
```

### Type Check

Use type checking functions:

- `cJSON_IsString()`
- `cJSON_IsNumber()`
- `cJSON_IsArray()`
- `cJSON_IsBool()`
- `cJSON_IsObject()`

```cpp
HWTEST_F(JsonTest, GetObjectItem_003, TestSize.Level1) {
    const char* jsonStr = R"({"str":"test","num":123,"bool":true,"null":null})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* strItem = cJSON_GetObjectItemCaseSensitive(json, "str");
    EXPECT_TRUE(cJSON_IsString(strItem));
    EXPECT_FALSE(cJSON_IsNumber(strItem));

    cJSON* numItem = cJSON_GetObjectItemCaseSensitive(json, "num");
    EXPECT_TRUE(cJSON_IsNumber(numItem));

    cJSON* boolItem = cJSON_GetObjectItemCaseSensitive(json, "bool");
    EXPECT_TRUE(cJSON_IsBool(boolItem));
    EXPECT_TRUE(cJSON_IsTrue(boolItem));

    cJSON* nullItem = cJSON_GetObjectItemCaseSensitive(json, "null");
    EXPECT_TRUE(cJSON_IsNull(nullItem));

    cJSON_Delete(json);
}
```

### Case Sensitivity

Distinguish between:
- `cJSON_GetObjectItem()` (case-insensitive)
- `cJSON_GetObjectItemCaseSensitive()` (case-sensitive)

## Get Array Item Tests

### Normal Get

Test `cJSON_GetArrayItem()` and `cJSON_GetArraySize()`:

```cpp
HWTEST_F(JsonTest, GetArrayItem_001, TestSize.Level1) {
    const char* jsonStr = R"([1,2,3])";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);
    EXPECT_TRUE(cJSON_IsArray(json));

    int arraySize = cJSON_GetArraySize(json);
    EXPECT_EQ(arraySize, 3);

    cJSON* item0 = cJSON_GetArrayItem(json, 0);
    ASSERT_NE(item0, nullptr);
    EXPECT_TRUE(cJSON_IsNumber(item0));
    EXPECT_EQ(cJSON_GetNumberValue(item0), 1.0);

    cJSON* itemOutOfRange = cJSON_GetArrayItem(json, 10);
    EXPECT_EQ(itemOutOfRange, nullptr);

    cJSON_Delete(json);
}
```

### Boundary Check

Test returning `nullptr` when index is out of bounds.

### Array Iteration

Use `cJSON_ArrayForEach()` to iterate arrays:

```cpp
HWTEST_F(JsonTest, ArrayForEach_001, TestSize.Level1) {
    const char* jsonStr = R"([1,2,3])";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    int count = 0;
    cJSON* item = nullptr;
    cJSON_ArrayForEach(item, json) {
        EXPECT_TRUE(cJSON_IsNumber(item));
        count++;
    }
    EXPECT_EQ(count, 3);

    cJSON_Delete(json);
}
```

## Create JSON Tests

### Create Object

Test `cJSON_CreateObject()`:

```cpp
HWTEST_F(JsonTest, CreateObject_001, TestSize.Level1) {
    cJSON* json = cJSON_CreateObject();
    ASSERT_NE(json, nullptr);

    cJSON* name = cJSON_CreateString("test");
    cJSON_AddItemToObject(json, "name", name);

    cJSON* age = cJSON_CreateNumber(30);
    cJSON_AddItemToObject(json, "age", age);

    cJSON* nameItem = cJSON_GetObjectItemCaseSensitive(json, "name");
    ASSERT_NE(nameItem, nullptr);
    EXPECT_STREQ(cJSON_GetStringValue(nameItem), "test");

    cJSON_Delete(json);
}
```

### Create Array

Test `cJSON_CreateArray()`:

```cpp
HWTEST_F(JsonTest, CreateArray_001, TestSize.Level1) {
    cJSON* json = cJSON_CreateArray();
    ASSERT_NE(json, nullptr);

    cJSON_AddItemToArray(json, cJSON_CreateNumber(1));
    cJSON_AddItemToArray(json, cJSON_CreateNumber(2));

    EXPECT_EQ(cJSON_GetArraySize(json), 2);

    cJSON_Delete(json);
}
```

### Create Values

Test value creation functions:
- `cJSON_CreateString()`
- `cJSON_CreateNumber()`
- `cJSON_CreateInt64Number()`
- `cJSON_CreateTrue()`
- `cJSON_CreateFalse()`
- `cJSON_CreateNull()`

### Memory Management

Created objects must call `cJSON_Delete()` to free.

## Get Value Tests

### String Value

```cpp
HWTEST_F(JsonTest, GetStringValue_001, TestSize.Level1) {
    const char* jsonStr = R"({"name":"test"})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* nameItem = cJSON_GetObjectItemCaseSensitive(json, "name");
    ASSERT_NE(nameItem, nullptr);

    const char* value = cJSON_GetStringValue(nameItem);
    ASSERT_NE(value, nullptr);
    EXPECT_STREQ(value, "test");

    cJSON_Delete(json);
}
```

### Number Value

```cpp
HWTEST_F(JsonTest, GetNumberValue_001, TestSize.Level1) {
    const char* jsonStr = R"({"age":30})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* ageItem = cJSON_GetObjectItemCaseSensitive(json, "age");
    ASSERT_NE(ageItem, nullptr);

    double value = cJSON_GetNumberValue(ageItem);
    EXPECT_EQ(value, 30.0);

    cJSON_Delete(json);
}
```

### Null Pointer Check

Test `cJSON_GetStringValue()` returning `nullptr` for non-string types.

### int64 Support

If `__CJSON_USE_INT64` is supported, test:
- `cJSON_GetInt64NumberValue()`
- `cJSON_CreateInt64Number()`

## Type Check Tests

### Type Judgment

Test type checking functions:
- `cJSON_IsString()`
- `cJSON_IsNumber()`
- `cJSON_IsArray()`
- `cJSON_IsBool()`
- `cJSON_IsObject()`
- `cJSON_IsNull()`

```cpp
HWTEST_F(JsonTest, TypeCheck_001, TestSize.Level1) {
    const char* jsonStr = R"({"str":"test","num":123,"bool":true,"null":null})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* strItem = cJSON_GetObjectItemCaseSensitive(json, "str");
    EXPECT_TRUE(cJSON_IsString(strItem));
    EXPECT_FALSE(cJSON_IsNumber(strItem));

    cJSON* numItem = cJSON_GetObjectItemCaseSensitive(json, "num");
    EXPECT_TRUE(cJSON_IsNumber(numItem));

    cJSON* boolItem = cJSON_GetObjectItemCaseSensitive(json, "bool");
    EXPECT_TRUE(cJSON_IsBool(boolItem));
    EXPECT_TRUE(cJSON_IsTrue(boolItem));

    cJSON* nullItem = cJSON_GetObjectItemCaseSensitive(json, "null");
    EXPECT_TRUE(cJSON_IsNull(nullItem));

    EXPECT_FALSE(cJSON_IsString(nullptr));
    EXPECT_FALSE(cJSON_IsNumber(nullptr));

    cJSON_Delete(json);
}
```

### Null Pointer Handling

Test type check functions returning `false` when passing `nullptr`.

## Delete and Modify Tests

### Delete Object

Test `cJSON_Delete()` correctly freeing memory:

```cpp
HWTEST_F(JsonTest, DeleteItem_001, TestSize.Level1) {
    const char* jsonStr = R"({"key1":"value1","key2":"value2"})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON_DeleteItemFromObjectCaseSensitive(json, "key1");

    cJSON* item1 = cJSON_GetObjectItemCaseSensitive(json, "key1");
    EXPECT_EQ(item1, nullptr);

    cJSON* item2 = cJSON_GetObjectItemCaseSensitive(json, "key2");
    ASSERT_NE(item2, nullptr);

    cJSON_Delete(json);
}
```

### Delete Item

Test `cJSON_DeleteItemFromObject()`, `cJSON_DeleteItemFromObjectCaseSensitive()`.

### Replace Item

Test `cJSON_ReplaceItemInObject()`, `cJSON_ReplaceItemInArray()`.

## Print/Serialize Tests

### Formatted Print

Test `cJSON_Print()` generating formatted JSON strings:

```cpp
HWTEST_F(JsonTest, Print_001, TestSize.Level1) {
    cJSON* json = cJSON_CreateObject();
    ASSERT_NE(json, nullptr);

    cJSON_AddItemToObject(json, "name", cJSON_CreateString("test"));

    char* printed = cJSON_Print(json);
    ASSERT_NE(printed, nullptr);
    EXPECT_NE(strstr(printed, "name"), nullptr);
    EXPECT_NE(strstr(printed, "test"), nullptr);

    cJSON_free(printed);
    cJSON_Delete(json);
}
```

### Unformatted Print

Test `cJSON_PrintUnformatted()` generating compact JSON strings:

```cpp
HWTEST_F(JsonTest, PrintUnformatted_001, TestSize.Level1) {
    cJSON* json = cJSON_CreateObject();
    ASSERT_NE(json, nullptr);

    char* printed = cJSON_PrintUnformatted(json);
    ASSERT_NE(printed, nullptr);
    EXPECT_STREQ(printed, "{}");

    cJSON_free(printed);
    cJSON_Delete(json);
}
```

### Memory Release

Printed strings must be freed using `cJSON_free()`.

### Null Pointer Handling

Test `cJSON_Print()` returning `nullptr` when `nullptr` is passed.

## Duplicate Tests

### Duplicate Object

Test `cJSON_Duplicate()`:

```cpp
HWTEST_F(JsonTest, Duplicate_001, TestSize.Level1) {
    const char* jsonStr = R"({"name":"test"})";
    cJSON* json = cJSON_Parse(jsonStr);
    ASSERT_NE(json, nullptr);

    cJSON* duplicate = cJSON_Duplicate(json, cJSON_True);
    ASSERT_NE(duplicate, nullptr);

    cJSON* nameItem = cJSON_GetObjectItemCaseSensitive(duplicate, "name");
    ASSERT_NE(nameItem, nullptr);
    EXPECT_STREQ(cJSON_GetStringValue(nameItem), "test");

    cJSON_Delete(json);
    cJSON_Delete(duplicate);
}
```

### Deep Copy vs Shallow Copy

- `cJSON_Duplicate(json, cJSON_True)`: Deep copy
- `cJSON_Duplicate(json, cJSON_False)`: Shallow copy

### Memory Management

Duplicated objects need to call `cJSON_Delete()` separately to free.

## Error Handling and Boundary Tests

### Null Pointer Parameters

Test behavior of all CJSON functions when passing `nullptr`.

### Empty String

Test handling when passing empty strings.

### Invalid JSON Format

Test various invalid JSON formats:
- Missing quotes
- Unmatched brackets
- Invalid syntax

```cpp
HWTEST_F(JsonTest, ErrorHandling_001, TestSize.Level1) {
    cJSON* json = cJSON_Parse("{invalid}");
    EXPECT_EQ(json, nullptr);

    json = cJSON_Parse("{\"key\":}");
    EXPECT_EQ(json, nullptr);

    json = cJSON_Parse("{\"key\":\"value\"");
    EXPECT_EQ(json, nullptr);
}
```

### Large JSON

Test performance when processing large JSON objects/arrays.

### Nesting Depth

Test handling of deeply nested JSON objects.

## BUILD.gN Dependencies

```gn
external_deps = [
    "c_utils:utils",
    "cjson:cjson",
    "hilog:libhilog",
    "googletest:gtest_main"
]
```

## Memory Leak Checks

### Must Free

All objects created through `cJSON_Parse()`, `cJSON_Create*()` must call `cJSON_Delete()` to free.

### Print String Release

Strings returned by `cJSON_Print()` and `cJSON_PrintUnformatted()` must be freed using `cJSON_free()`.

### Check in Tests

Use memory detection tools (Valgrind, AddressSanitizer) to verify no memory leaks:

```cpp
HWTEST_F(JsonTest, MemoryLeak_001, TestSize.Level1) {
    for (int i = 0; i < 100; i++) {
        cJSON* json = cJSON_Parse(R"({"key":"value"})");
        ASSERT_NE(json, nullptr);
        cJSON_Delete(json);  // Must free, otherwise memory leak
    }
}
```

## CJSON Test Best Practices

### ✅ Must Test

- All branches: Parse success/failure, get item exists/doesn't exist, type match/mismatch
- Memory management: Ensure all created objects are correctly freed
- Boundary conditions: Null pointers, empty strings, invalid JSON, array out of bounds
- Type checks: Verify correctness of type judgment functions
- Error handling: Handling logic for various error cases

### ❌ Forbidden

- Empty implementations: Cannot have only comments, must include complete test logic
- Ignoring memory release: Cannot only test functionality while ignoring memory management
