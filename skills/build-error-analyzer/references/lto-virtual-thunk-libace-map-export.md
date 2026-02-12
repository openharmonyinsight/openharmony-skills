# Case 9: LTO Virtual Thunk 未定义 - libace.map 导出解决方案

**Location**: `references/lto-virtual-thunk-libace-map-export.md`

**Error signature**:
```
ld.lld: error: undefined symbol: virtual thunk to OHOS::Ace::TouchEventTarget::~TouchEventTarget()
>>> referenced by ld-temp.o
>>>               lto.tmp:(construction vtable for OHOS::Ace::TouchEventTarget-in-OHOS::Ace::V2::ListScrollBarController)
>>> referenced by ld-temp.o
>>>               lto.tmp:(construction vtable for OHOS::Ace::TouchEventTarget-in-OHOS::Ace::VerticalDragRecognizer)
```

**Context**:
- 类有虚函数并被用作基类
- 使用了前向声明优化：析构函数声明在头文件，实现在 .cpp
- 编译通过但链接时 LTO 无法找到 virtual thunk 符号

**Common misunderstanding**:
认为必须将析构函数改回 `= default` inline 定义，从而失去前向声明优化。

**Root Cause**:
当类有虚函数并作为基类被继承时：
1. LTO (Link Time Optimization) 在链接时优化虚函数表
2. 为派生类创建 **virtual thunk** 来调整 this 指针
3. 这些 virtual thunk 的符号必须在链接时可用
4. 如果析构函数不在头文件中 inline 定义，LTO 生成的 virtual thunk 符号可能不会被导出

**Correct Solution: libace.map 显式导出** ⭐

**不要回退前向声明优化！** 通过在 libace.map 中显式导出类和 virtual thunk 符号：

### Step 1: 保持头文件的前向声明优化

```cpp
// touch_event.h
#include "core/components_ng/event/target_component.h"  // ✅ 完整定义用于 RefPtr<T> 成员

namespace NG {
class TargetComponent;  // ✅ 其他类型的前向声明
}

class TouchEventTarget {
public:
    // ...
    ~TouchEventTarget() override;  // ✅ 声明（不使用 = default）
    // ...
private:
    RefPtr<NG::TargetComponent> targetComponent_;  // ✅ RefPtr 成员
};
```

### Step 2: 在 .cpp 中实现析构函数

```cpp
// touch_event.cpp
#include "core/event/touch_event.h"

TouchEventTarget::~TouchEventTarget() = default;  // ✅ 实现在 cpp
```

### Step 3: 在 libace.map 中显式导出

```map
# build/libace.map
{
  global:
    # ... 其他导出

    # ⭐ 关键：同时导出类符号和 virtual thunk
    OHOS::Ace::TouchEventTarget::*;
    virtual?thunk?to?OHOS::Ace::TouchEventTarget::*;

    # ... 其他导出
};
```

**关键点**：
- `OHOS::Ace::TouchEventTarget::*;` - 导出类的所有普通符号
- `virtual?thunk?to?OHOS::Ace::TouchEventTarget::*;` - 导出所有 virtual thunk（LTO 生成）
- 通配符 `*` 匹配所有方法，包括 virtual thunk

## Why This Works:

1. **编译阶段**：
   - 头文件使用前向声明，减少依赖
   - .cpp 文件包含完整定义并实现析构函数

2. **LTO 链接阶段**：
   - LTO 优化虚函数表，创建 virtual thunk
   - 查找 `virtual?thunk?to?OHOS::Ace::TouchEventTarget::*` 模式
   - 找到后导出这些符号到动态符号表

3. **运行时**：
   - 派生类（如 `ListScrollBarController`）的 vtable 可以正确引用 virtual thunk
   - 虚函数调用正确路由

## 关键概念：libace.map 符号导出

### libace.map 的作用

libace.map 是版本脚本，控制哪些符号从动态库导出：
- **global** 段：列出的符号将被导出
- **local** 段：未列出的符号被隐藏
- **通配符** `*`：匹配任意字符序列

### 导出模式说明

| 模式 | 作用 | 示例 |
|------|------|------|
| `ClassName::*;` | 导出类的所有公开符号 | `OHOS::Ace::TouchEventTarget::*;` |
| `virtual?thunk?to?ClassName::*;` | 导出 LTO virtual thunk | `virtual?thunk?to?OHOS::Ace::TouchEventTarget::*;` |
| `ClassName::MethodName*;` | 导出特定方法的所有重载 | `OHOS::Ace::TouchEventTarget::AttachFrameNode*;` |

### 为什么需要两个导出？

1. **`ClassName::*;`**：
   - 导出类的普通方法符号
   - 例如：`_ZN2OHOS3Ace15TouchEventTargetD1Ev`（析构函数）
   - 例如：`_ZN2OHOS3Ace15TouchEventTarget16AttachFrameNodeERKN2OHOS3Ace2NG13FrameNodeE`（方法）

2. **`virtual?thunk?to?ClassName::*;`**：
   - 导出 LTO 生成的 virtual thunk
   - 例如：`_ZTv0nN2OHOS3Ace15TouchEventTargetD1Ev`（virtual thunk 到析构函数）
   - LTO 创建这些 thunk 来调整派生类的 this 指针

## 何时使用此方案

**适用场景**：
- ✅ 类有虚函数并作为基类
- ✅ 使用了前向声明优化（析构函数不在头文件 inline）
- ✅ 链接时报错 "undefined symbol: virtual thunk to ClassName::~ClassName()"
- ✅ 使用 LTO (Link Time Optimization)

**不适用场景**：
- ❌ 类不是基类（不会被继承）
- ❌ 析构函数已经在头文件中 inline 定义
- ❌ 不使用 LTO（传统编译链接）

## 实现细节

### 完整示例

**头文件 (touch_event.h)**:
```cpp
#include "core/components_ng/event/target_component.h"

namespace NG {
class TargetComponent;
}

class ACE_FORCE_EXPORT TouchEventTarget : public Referenced {
public:
    TouchEventTarget() = default;
    ~TouchEventTarget() override;  // ✅ 声明，不在头文件实现

    void SetTargetComponent(const RefPtr<NG::TargetComponent>& targetComponent);

private:
    RefPtr<NG::TargetComponent> targetComponent_;
};
```

**实现文件 (touch_event.cpp)**:
```cpp
#include "core/event/touch_event.h"

TouchEventTarget::~TouchEventTarget() = default;  // ✅ 实现
```

**libace.map**:
```map
{
  global:
    *OHOS::Ace::NG::DragEvent::*;
    *OHOS::Ace::TouchEventTarget::*;
    virtual?thunk?to?OHOS::Ace::TouchEventTarget::*;
    // ...
};
```

## 常见错误模式

### ❌ 错误 1：只导出类符号

```map
{
  global:
    OHOS::Ace::TouchEventTarget::*;  # ❌ 只导出普通符号
    # 缺少 virtual thunk 导出
}
```

**结果**: 链接时报错 `undefined symbol: virtual thunk to...`

### ❌ 错误 2：回退前向声明优化

```cpp
// ❌ 放弃优化，将析构函数改回 inline
~TouchEventTarget() override = default;  // ❌ 在头文件中定义
```

**结果**：
- ❌ 失去前向声明优化
- ❌ 增加 target_component.h 的依赖
- ✅ 链接错误解决，但编译性能下降

### ❌ 错误 3：完全回退到完整包含

```cpp
// ❌ 最坏做法：包含完整的 target_component.h，但不需要时
#include "core/components_ng/event/target_component.h"  // ❌ 即使 RefPtr 不需要完整定义
```

## 编译性能影响

### 优化前（无前向声明）

```cpp
// touch_event.h
#include "core/components_ng/event/target_component.h"  // ❌ 完整依赖

class TouchEventTarget {
    RefPtr<NG::TargetComponent> targetComponent_;
};
```

- 所有包含 `touch_event.h` 的文件都依赖完整的 `target_component.h`
- 修改 `target_component.h` 触发大量重编译

### 优化后（前向声明 + libace.map）

```cpp
// touch_event.h
#include "core/components_ng/event/target_component.h"  // ✅ 用于 RefPtr<T> 成员

namespace NG {
class TargetComponent;  // ✅ 其他类型的前向声明
}

class TouchEventTarget {
    ~TouchEventTarget() override;  // ✅ 声明在头，实现在 cpp
    RefPtr<NG::TargetComponent> targetComponent_;
};
```

- 只在 `touch_event.cpp` 中需要完整定义
- `target_component.h` 的修改影响范围缩小
- 保持头文件轻量级

## 相关案例分析

| Case | 场景 | 解决方案 |
|------|------|----------|
| **Case 6** | RefPtr<T> 成员（有 .cpp 文件的类） | 分离特殊成员函数到 .cpp |
| **Case 8** | RefPtr<T> 成员（纯数据结构） | 添加辅助方法到新 .cpp |
| **Case 9** | 基类的虚函数 + LTO | **保持前向声明 + libace.map 导出** |

## Best Practices

### 1. 符号导出原则

当类需要显式导出时，检查以下清单：

- [ ] **普通符号导出**：添加 `ClassName::*;`
- [ ] **Virtual thunk 导出**（基类 + LTO）：添加 `virtual?thunk?to?ClassName::*;`
- [ ] **特定方法导出**（如需要）：添加 `ClassName::MethodName*;`

### 2. 前向声明优化的边界

前向声明优化适用于：
- ✅ RefPtr<T> 成员变量（需要完整类型用于构造/析构）
- ✅ 基类的虚函数（需要 libace.map 导出 virtual thunk）
- ✅ 普通指针/引用成员

前向声明优化不适用于：
- ❌ 需要在头文件中内联的函数（模板实例化等）
- ❌ 编译时常量需要在头文件定义

### 3. LTO 相关注意事项

- **LTO 会创建额外的符号**：virtual thunk、adjustor thunk 等
- **导出模式需要匹配**：`virtual?thunk?to?ClassName::*;`
- **通配符更安全**：使用 `*` 而不是列举每个方法
- **测试不同编译配置**：LTO 和非 LTO 都需要能工作

## Verification Steps:

1. **检查符号是否导出**:
```bash
# 查看 TouchEventTarget 相关符号
nm -D out/rk3568/arkui/ace_engine/libace_compatible.z.so | grep TouchEventTarget
```

2. **检查 virtual thunk 是否存在**:
```bash
# 查找 virtual thunk 符号
nm -D out/rk3568/arkui/ace_engine/libace_compatible_components.z.so | grep "ZThunk"
```

3. **验证链接成功**:
```bash
cd /home/sunfei/workspace/openHarmony
./build.sh --product-name rk3568 --build-target ace_engine
```

## Summary

**关键要点**：
1. ⭐ **保持前向声明优化**：不要因为 LTO 链接错误就回退到 inline 定义
2. ⭐ **使用 libace.map 显式导出**：添加 `virtual?thunk?to?ClassName::*;` 导出 virtual thunk
3. ⭐ **理解 LTO 的工作原理**：LTO 需要在符号表中找到 virtual thunk
4. ⭐ **区分不同场景**：普通类 vs 基类 vs 有虚函数的基类

**记住**：当遇到 "undefined symbol: virtual thunk to" 错误时，检查是否在 libace.map 中正确导出了 virtual thunk！
