# 规则A: 头文件格式规范

**严重程度**: 中危

**问题描述**: FUZZ测试的头文件必须遵循特定格式规范，包括完整的版权声明、正确的头文件保护、必需的系统头文件（`<cstdint>`、`<unistd.h>`、`<climits>`、`<cstdio>`、`<cstdlib>`、`<fcntl.h>`）以及`FUZZ_PROJECT_NAME`宏定义。格式不规范会导致编译失败或fuzz引擎无法正确识别项目。

**核心原则**:
1. 头文件必须包含完整的版权声明
2. 必须使用#ifndef/#define/#endif保护
3. 必须包含6个必需系统头文件

**错误示例**:
```cpp
// ❌ 缺少系统头文件和FUZZ_PROJECT_NAME
#ifndef FUZZER_H
#define FUZZER_H
#include <iostream>
#endif
```

**正确示例**:
```cpp
// ✅ 完整的头文件
#ifndef FUZZER_NAME_FUZZER_H
#define FUZZER_NAME_FUZZER_H

#include <cstdint>
#include <unistd.h>
#include <climits>
#include <cstdio>
#include <cstdlib>
#include <fcntl.h>

#define FUZZ_PROJECT_NAME "SetScreenInfo_fuzzer"

#endif
```

**检查方法**:
1. 检查文件开头是否有版权声明
2. 检查是否使用 `#ifndef/#define/#endif` 头文件保护
3. 检查是否包含全部6个必需系统头文件
4. 检查是否定义了 `FUZZ_PROJECT_NAME` 宏
5. 检查 `FUZZ_PROJECT_NAME` 值与目录名是否一致
6. 检查是否有命名空间定义（应无）

**豁免场景**: 
- 无

---
