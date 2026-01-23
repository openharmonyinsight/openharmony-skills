# XTS Test Patterns Reference

This file contains common test patterns and templates for OpenHarmony XTS test case generation.

## Table of Contents

1. [File Structure](#file-structure)
2. [Test Case Numbering](#test-case-numbering)
3. [Basic Test Template](#basic-test-template)
4. [Test Scenarios](#test-scenarios)
5. [Common Patterns](#common-patterns)

---

## File Structure

### Standard Test File Header

```typescript
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
```

### Lifecycle Hooks

```typescript
export default function moduleNameAPI() {
  describe('moduleNameAPI', () => {
    beforeAll(async (done: Function) => {
      console.info('beforeAll called');
      done();
    });

    beforeEach(async (done: Function) => {
      console.info('beforeEach called');
      done();
    });

    afterEach(async (done: Function) => {
      console.info('afterEach called');
      await sleep(SLEEP_INTERVAL_MS);
      done();
    });

    afterAll(async (done: Function) => {
      console.info('afterAll called');
      done();
    });
  });
}
```

---

## Test Case Numbering

### Format

```
SUB_{子系统缩写}_{模块名}_{方法名}_{场景}_{序号}
```

### Scenario Numbers

| Number | Scenario | Description |
|--------|----------|-------------|
| 0100 | Normal | Normal/expected call scenario (REQUIRED) |
| 0200-0299 | Exception | Null, undefined, empty values |
| 0300-0399 | Boundary | Boundary conditions |
| 0500-0899 | Optional | Optional parameter combinations |
| 0900-0999 | Enum | Enum value tests |
| 1000-1499 | Numeric | Numeric boundary tests |
| 1500-1899 | String | String tests |
| 1900-1999 | Struct | Structure parameter tests |
| 2000-2099 | File Path | File-related with path |
| 2100-2199 | File URI | File-related with URI |
| 2200-2299 | File FD | File-related with file descriptor |

### Subsystem Abbreviations

- **MM**: mechanicManager
- **DF**: data/file (filesystem)
- **NET**: network
- **WM**: windowManager
- **APP**: application

---

## Basic Test Template

### JSDoc Comments (Required)

```typescript
/**
 * @tc.number SUB_MM_ModuleName_methodName_0100
 * @tc.name SUB_MM_ModuleName_methodName_0100
 * @tc.desc Test normal call scenario for methodName
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 0
 */
```

### Test Function Structure

```typescript
it('SUB_MM_ModuleName_methodName_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  console.info("-----------------SUB_MM_ModuleName_methodName_0100 begin-----------------");
  try {
    // Test code here
    let result = moduleName.methodName(param1, param2);
    expect(result != null).assertTrue();
  } catch (error) {
    console.error('SUB_MM_ModuleName_methodName_0100 failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == 401).assertTrue();
  }
  console.info("-----------------SUB_MM_ModuleName_methodName_0100 end-----------------");
});
```

---

## Test Scenarios

### 0100 - Normal Call

```typescript
it('SUB_MM_ModuleName_methodName_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  console.info("-----------------SUB_MM_ModuleName_methodName_0100 begin-----------------");
  try {
    let callback: Callback = (data: string) => {
      console.info('callback invoked: ' + data);
    };
    let result = mechanicManager.on('attachStateChange', callback);
    expect(true).assertTrue();
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == 33300001).assertTrue();
  }
  console.info("-----------------SUB_MM_ModuleName_methodName_0100 end-----------------");
});
```

### 0200 - Null Parameter

```typescript
it('SUB_MM_ModuleName_methodName_Null_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, async () => {
  console.info("-----------------SUB_MM_ModuleName_methodName_Null_0200 begin-----------------");
  try {
    let result = moduleName.methodName(null);
    expect(false).assertFail();
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == 401).assertTrue();
  }
  console.info("-----------------SUB_MM_ModuleName_methodName_Null_0200 end-----------------");
});
```

### 0201 - Undefined Parameter

```typescript
it('SUB_MM_ModuleName_methodName_Undefined_0201', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, async () => {
  console.info("-----------------SUB_MM_ModuleName_methodName_Undefined_0201 begin-----------------");
  try {
    let result = moduleName.methodName(undefined);
    expect(false).assertFail();
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == 401).assertTrue();
  }
  console.info("-----------------SUB_MM_ModuleName_methodName_Undefined_0201 end-----------------");
});
```

### 0900 - Enum Tests

```typescript
it("SUB_MM_ModuleName_EnumTypeName_0900", TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.info("-----------------SUB_MM_ModuleName_EnumTypeName_0900 begin-----------------");
  try {
    // Access enum values
    let VALUE1: number = moduleName.EnumTypeName.VALUE1;
    let VALUE2: number = moduleName.EnumTypeName.VALUE2;
    let VALUE3: number = moduleName.EnumTypeName.VALUE3;

    // Verify enum values
    expect(VALUE1).assertEqual(0);
    expect(VALUE2).assertEqual(1);
    expect(VALUE3).assertEqual(2);
  } catch (error) {
    console.error('print failed, code is ' + error.code + ', message is ' + error.message);
    expect(false).assertFalse();
  }
  console.info("-----------------SUB_MM_ModuleName_EnumTypeName_0900 end-----------------");
});
```

### 0500-0899 - Optional Parameter Combinations

For N optional parameters, generate 2^N test cases:

```typescript
// 0500: Required params only
it('SUB_MM_ModuleName_methodName_0500', async () => {
  let result = moduleName.methodName(requiredParam);
});

// 0501: Required + optional1
it('SUB_MM_ModuleName_methodName_0501', async () => {
  let result = moduleName.methodName(requiredParam, optional1);
});

// 0502: Required + optional2
it('SUB_MM_ModuleName_methodName_0502', async () => {
  let result = moduleName.methodName(requiredParam, undefined, optional2);
});

// 0503: Required + optional1 + optional2
it('SUB_MM_ModuleName_methodName_0503', async () => {
  let result = moduleName.methodName(requiredParam, optional1, optional2);
});
```

---

## Common Patterns

### File Utility Functions (when file operations needed)

```typescript
let domain: number = 0x0000;
let tag: string = 'testTag';

async function nextFileName(testName: string): Promise<string> {
  let filesDir: string = getContext().filesDir;
  let fpath: string = filesDir + '/' + testName;
  return fpath;
}

async function prepareFile(fpath: string, content: string): Promise<boolean> {
  let file: fileio.File = fileio.createFileSync(fpath);
  let fd: number = file.fd;
  let written: number = fileio.writeSync(fd, content);
  fileio.closeSync(fd);
  return (written > 0);
}
```

### File Path Pattern (2000)

```typescript
it('SUB_DF_ModuleName_methodName_Path_2000', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  console.info("-----------------SUB_DF_ModuleName_methodName_Path_2000 begin-----------------");
  let fpath: string = await nextFileName('methodName_Path_2000');
  expect(await prepareFile(fpath, 'hello world')).assertTrue();

  try {
    let result = await moduleName.methodName(fpath);
    expect(result !== null).assertTrue();
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(false).assertFalse();
  }

  fs.unlinkSync(fpath);
  console.info("-----------------SUB_DF_ModuleName_methodName_Path_2000 end-----------------");
});
```

### File URI Pattern (2100)

```typescript
it('SUB_DF_ModuleName_methodName_URI_2100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  console.info("-----------------SUB_DF_ModuleName_methodName_URI_2100 begin-----------------");
  let fpath: string = await nextFileName('methodName_URI_2100');
  expect(await prepareFile(fpath, 'hello world')).assertTrue();

  try {
    let uri: string = fileuri.getUriFromPath(fpath);
    let result = await moduleName.methodName(uri);
    expect(result !== null).assertTrue();
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(false).assertFalse();
  }

  fs.unlinkSync(fpath);
  console.info("-----------------SUB_DF_ModuleName_methodName_URI_2100 end-----------------");
});
```

### Event Method Pattern (on/off)

```typescript
let callbackInvoked: boolean = false;

let callback: Callback = (data: string) => {
  console.info('callback invoked: ' + data);
  callbackInvoked = true;
};

let result = mechanicManager.on('attachStateChange', callback);
expect(result !== undefined).assertTrue();

// Clean up
mechanicManager.off('attachStateChange', callback);
```

### Async/Await Pattern

```typescript
it('SUB_MM_ModuleName_asyncMethod_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async () => {
  console.info("-----------------begin-----------------");
  try {
    let result: Promise<ReturnType> = await moduleName.asyncMethod(param);
    expect(result).assertEqual(expectedValue);
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == errorCode).assertTrue();
  }
  console.info("-----------------end-----------------");
});
```

### Callback Pattern

```typescript
it('SUB_MM_ModuleName_callbackMethod_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
  console.info("-----------------begin-----------------");
  try {
    moduleName.callbackMethod(param, (error: BusinessError, result: ReturnType) => {
      if (error) {
        console.error('callback failed, code is ' + error.code + ', message is ' + error.message);
        expect(false).assertFail();
        done();
        return;
      }
      expect(result !== null).assertTrue();
      done();
    });
  } catch (error) {
    console.error('failed, code is ' + error.code + ', message is ' + error.message);
    expect(error.code == errorCode).assertTrue();
    done();
  }
  console.info("-----------------end-----------------");
});
```

### Sleep Utility

```typescript
const SLEEP_INTERVAL_MS = 1000;

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Use in afterEach
afterEach(async (done: Function) => {
  console.info('afterEach called');
  await sleep(SLEEP_INTERVAL_MS);
  done();
});
```

### Module Import Pattern

```typescript
// Based on module documentation
import mechanicManager from '@ohos.mechanicManager';
import fileio from '@ohos.fileio';
import fileuri from '@ohos.file.fileuri';
import fs from '@ohos.file.fs';
```
