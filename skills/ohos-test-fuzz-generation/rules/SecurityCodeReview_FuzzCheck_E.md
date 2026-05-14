# 规则E: 头文件包含规范

**严重程度**: 中危

**问题描述**: FUZZ测试的.cpp文件必须正确包含所有必要的头文件，包括自身头文件（文件名必须与.cpp一致，使用双引号）、被测API头文件、参数类型头文件（结构体/类、回调函数、容器、智能指针等）以及标准库头文件。头文件包含不规范会导致编译失败。

**核心原则**:
1. .cpp必须包含对应的.h头文件
2. 项目头文件必须使用双引号
3. 必须包含所有必要的头文件

**错误示例**:
```cpp
// AnimationCommand_fuzzer2.cpp
#include "AnimationCommand_fuzzer2a.h"  // 错误：自身头文件名不匹配
#include <fuzzed_data_provider.h>         // 错误：应该用双引号 "

// 缺少被测类的头文件
// 缺少参数类型的结构体头文件
void DoTest(FuzzedDataProvider& fdp)
{
    RSScreenModeInfo info;  // 错误：缺少 rsscreen_mode_info.h，编译失败
    g_manager->SetModeInfo(info);
}
```

**正确示例**:
```cpp
// AnimationCommand_fuzzer2.cpp
#include "AnimationCommand_fuzzer2.h"   // ✅ 自身头文件名一致
#include "fuzzed_data_provider.h"         // ✅ 使用双引号
#include "screen_manager.h"               // ✅ 被测 API 头文件
#include "rsscreen_mode_info.h"           // ✅ 参数类型头文件
#include <vector>                          // ✅ 容器头文件
#include <memory>                          // ✅ 智能指针头文件
```

**检查方法**:
1. 检查自身头文件名是否与.cpp文件名一致
2. 检查项目头文件是否使用双引号而非尖括号
3. 检查是否包含被测API所在类的头文件
4. 检查是否包含参数类型对应的头文件
5. 尝试编译验证是否有缺失的头文件

**豁免场景**: 
- 无

---
