# BUILD.gn Rules

## Overview

This document specifies the BUILD.gn configuration rules for OpenHarmony unit tests.

## BUILD.gn Target Configuration

### ohos_unittest Target

```gn
ohos_unittest("{CamelCase}Test") {
    module_out_path = "subsystem/module"
    branch_protector_ret = "pac_ret"
    sanitize = {
        integer_overflow = true
        cfi = true
        cfi_cross_dso = true
        debug = false
        blocklist = "${project_path}/cfi_blocklist.txt"
    }
    sources = ["test_file.cpp"]
    include_dirs = ["//include/path"]
    deps = [":source_target"]
    external_deps = [
        "hilog:libhilog",
        "c_utils:utils",
        "googletest:gtest_main"
    ]
    defines = ["private=public"]
    use_exceptions = true
}
```

### Copyright Header

```gn
# Copyright (c) 2025 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

## Configuration Matching Requirements

The system automatically extracts the source file's BUILD.gn configuration. When generating UT test BUILD.gn:

### deps Matching

- Must include all deps of the source file target
- Tests usually need the same dependencies as source
- Example:

```gn
# If source file target has:
deps = [ ":source_target" ]

# UT test should also include:
deps = [ ":source_target" ]
```

### external_deps Matching

- Must include all external_deps of the source file target
- Must include googletest:gtest_main for test framework
- Example:

```gn
# If source file target has:
external_deps = [ "hilog:libhilog", "c_utils:utils" ]

# UT test should include:
external_deps = [
    "hilog:libhilog",
    "c_utils:utils",
    "googletest:gtest_main"  # Additional for testing
]
```

### include_dirs Matching

- Must include all include_dirs of the source file target
- Add "mock" directory if mock is needed
- Use relative paths (//subsystem/module/...) or variable references (${xxx_path})
- Example:

```gn
# If source file target has:
include_dirs = [ "//foundation/xxx/include" ]

# UT test should include:
include_dirs = [
    "//foundation/xxx/include",
    "mock"  # Additional if mock needed
]
```

### defines Matching

- If source file target has defines, UT test should include the same defines
- Add "private=public", "protected=public" if needed to access private/protected members
- Example:

```gn
# If source file target has:
defines = [ "FEATURE_ENABLED" ]

# UT test should include:
defines = [
    "FEATURE_ENABLED",
    "private=public"  # Additional to access private members
]
```

### module_out_path Matching

- Must reuse source file GN's module_out_path
- Maintains consistency with project structure
- Example:

```gn
# If source file target has:
module_out_path = "foundation/communication/tests"

# UT test should also include:
module_out_path = "foundation/communication/tests"
```

### use_exceptions Matching

- If source file target has use_exceptions, UT test should also include it
- Example:

```gn
# If source file target has:
use_exceptions = true

# UT test should also include:
use_exceptions = true
```

## sources Array Format Requirements

### Alphabetical Sorting

- All entries in sources array must be sorted alphabetically by filename
- Ignore path prefix when sorting (case-insensitive)
- Example:

```gn
# CORRECT: Alphabetically sorted
sources = [
    "a_test.cpp",
    "b_test.cpp",
    "c_test.cpp"
]

# WRONG: Not alphabetically sorted
sources = [
    "c_test.cpp",
    "a_test.cpp",
    "b_test.cpp"
]
```

### Insert at Correct Position

If existing BUILD.gn has sources array, new files must be inserted at correct alphabetical position:

```gn
# Existing: ["a_file.cpp", "c_file.cpp"]
# Insert "b_file.cpp" at correct position:
sources = [
    "a_file.cpp",
    "b_file.cpp",  # Inserted here
    "c_file.cpp"
]
```

### Variable Reference Format Support

Support variable reference format:

```gn
sources = [
    "${xxx_path}/file.cpp",
    "${xxx_path}/path/file.cpp"
]
```

### Maintain Original Format

If existing sources use variable references, new entries should maintain same format:

```gn
# If existing sources use variable references:
sources = ["${path}/a_file.cpp", "${path}/c_file.cpp"]

# New entry should also use variable reference:
sources = ["${path}/a_file.cpp", "${path}/b_file.cpp", "${path}/c_file.cpp"]
```

### Support += Append Format

If existing BUILD.gn uses sources += [...] format, new files should be added to first sources = [...] array:

```gn
# If BUILD.gn has:
sources += ["new_file.cpp"]

# New file should be added to first sources array alphabetically:
sources = ["a_file.cpp", "b_file.cpp", "c_file.cpp"]
# NOT: sources += ["b_file.cpp"]
```

## group("unittest") Configuration

### Must Live in Same BUILD.gn

```gn
group("unittest") {
    testonly = true
    deps = [ ":{CamelCase}Test" ]
}
```

### Alphabetical Sorting

deps array must be alphabetically sorted:

```gn
# CORRECT: Alphabetically sorted
group("unittest") {
    testonly = true
    deps = [
        ":ATest",
        ":BTest",
        ":CTest"
    ]
}
```

### If Group Already Exists

Only need to append new target in deps, maintaining alphabetical sorting:

```gn
# Existing:
group("unittest") {
    testonly = true
    deps = [ ":ATest", ":CTest" ]
}

# Add new BTest:
group("unittest") {
    testonly = true
    deps = [ ":ATest", ":BTest", ":CTest" ]  # Inserted alphabetically
}
```

## Creating New BUILD.gn

If directory lacks BUILD.gn, create one following template:

### Parent Directory BUILD.gn

```gn
import("//build/test.gni")
group("unittest") {
    testonly = true
    deps = [ "unittest:unittest" ]
}
```

### Test Directory BUILD.gn

Then define ohos_unittest target in test/unittest/BUILD.gn:

```gn
ohos_unittest("{CamelCase}Test") {
    # Target configuration
}
```

## C Language Source Files

For C source files (.c):

- Generated test files are still .cpp (C++ test files)
- Use googletest:gtest_main dependency (same as C++ tests)
- No Unity/CUnit dependencies needed
- Wrap C functions with extern "C":

```cpp
extern "C" {
#include "original_header.h"
}
```

## External Dependencies

### Minimum Required

Always include at least:

```gn
external_deps = [
    "hilog:libhilog",
    "c_utils:utils",
    "googletest:gtest_main"
]
```

### Domain-Specific Dependencies

Add based on source file dependencies:

- IPC: `ipc:ipc_core`
- Ability: `ability_base:ability_base`
- Access Token: `access_token:libaccesstoken_sdk`
- And more based on actual source dependencies

### NDK Module Dependencies

For NDK interface testing:

```gn
external_deps = [
    "pasteboard:pasteboard_ndk",
    "preferences:preferences_ndk",
    "hilog:libhilog",
    "googletest:gtest_main"
]
```

## GN Integration Steps

### 1. Inspect Existing Test BUILD.gn

Check "test/unittest" or sibling directory for existing BUILD.gn:

- Append new test/mock source files to sources array (alphabetically sorted)
- Check existing sources sorting, ensure new files maintain alphabetical order
- If sources uses variable references, maintain same format
- Add missing include_dirs/deps/external_deps without overwriting existing config

### 2. Create New BUILD.gn If Missing

If "unittest" directory lacks BUILD.gn:

- Create new file following template
- Ensure reuse of existing path variables (like '${xxx_path}')

### 3. Update Parent BUILD.gn

Update or create parent "test/BUILD.gn":

- If group("unittest") exists, append new target in deps (alphabetically sorted)
- If not exists, create group with new target

### 4. Register with Repository-Level Groups

If project uses higher-level group (like bundle.json level):

- Document how to register new target at repository level

## Output Format

### Provide Clear Suggestions

- Provide BUILD.gn modification suggestions or patch snippets
- Maintain original indentation/order/alphabetical sorting
- Clearly indicate "insert alphabetically" rather than "append to end" or "replace"

### Example Patch Suggestion

```diff
diff --git a/test/unittest/BUILD.gn b/test/unittest/BUILD.gn
index 1234567..abcdefg 100644
--- a/test/unittest/BUILD.gn
+++ b/test/unittest/BUILD.gn
@@ -10,10 +10,11 @@ ohos_unittest("ServiceTest") {
     module_out_path = "foundation/module/tests"
     sources = [
-        "a_test.cpp",
         "c_test.cpp"
+        "a_test.cpp",
+        "b_test.cpp",  # Insert alphabetically
+        "c_test.cpp"
     ]
     ...
 }
```

## BUILD.gn Best Practices

### ✅ Recommended

- Alphabetically sort sources and deps arrays
- Match source file's GN configuration
- Use relative paths or variable references
- Include all necessary dependencies
- Add "private=public" to access private members
- Reuse existing path variables

### ❌ Forbidden

- Use absolute paths in include_dirs
- Append new files to end without sorting
- Overwrite existing configuration
- Skip adding required dependencies
- Forget to add googletest:gtest_main
