# 编译优化策略

本文档提供减少编译时间和优化依赖关系的具体策略。

## 常见编译性能问题

### 1. 过度包含（Over-inclusion）

**症状**：
- 编译时间长（>15 秒）
- 依赖树有很多分支（宽度 > 10）
- 许多不相关的头文件被包含

**示例**：

```cpp
//不好：frame_widget.cpp 包含了不必要的头文件
#include "base/log.h"
#include "utils/time_utils.h"  // 实际上没用到
#include "network/http_client.h"  // 实际上没用到
#include "render/canvas.h"
#include "core/animation.h"  // 实际上没用到
#include "components/frame_widget.h"
```

**解决方案**：

1. 移除未使用的包含
2. 使用工具检测未使用的包含
3. 使用前置声明替代完整包含

```cpp
// 好：只包含必要的头文件
#include "components/frame_widget.h"
#include "render/canvas.h"

// 对其他类使用前置声明
class HttpClient;
class Animation;
```

### 2. 深层依赖链

**症状**：
- 依赖树深度 > 7 层
- 修改一个小头文件导致大量重编译
- 编译时间随包含深度指数增长

**示例**：

```
file.cpp
  └── header1.h
      └── header2.h
          └── header3.h
              └── header4.h
                  └── header5.h
                      └── header6.h
                          └── header7.h
                              └── header8.h
```

**解决方案**：

1. **减少中间层次**：合并相关的头文件
2. **使用接口类**：通过接口解耦实现
3. **依赖注入**：通过参数传递而非包含

```cpp
// 不好：深层依赖
// A.h -> B.h -> C.h -> D.h -> E.h

// 好：使用接口解耦
// A.h -> IInterface.h (接口)
// A.cpp -> B.h (实现)
```

### 3. 模板实例化过多

**症状**：
- 编译时间特别长（>30 秒）
- 内存使用很高（>800 MB）
- .ii 文件非常大（>100 MB）

**示例**：

```cpp
// 不好：模板在头文件中实例化
template<typename T>
class Container {
    // 复杂的实现...
};

// 每个包含这个头文件的文件都会实例化模板
#include "container.h"
```

**解决方案**：

1. **显式实例化**：在 .cpp 文件中实例化模板
2. **类型擦除**：使用基类指针代替模板
3. **extern template**：声明模板实例化

```cpp
// container.h
template<typename T> class Container { ... };
extern template class Container<MyType>;  // 声明

// container.cpp
template class Container<MyType>;  // 显式实例化

// user.cpp
#include "container.h"
// 不会重新实例化 Container<MyType>
```

### 4. 循环依赖

**症状**：
- 编译错误："incomplete type"
- 头文件必须按特定顺序包含
- 依赖树中有循环路径

**示例**：

```cpp
// A.h
#include "B.h"
class A { B* b; };

// B.h
#include "A.h"
class B { A* a; };  // 循环依赖！
```

**解决方案**：

1. **前置声明**：打破循环
2. **接口分离**：抽取公共接口
3. **PIMPL 模式**：隐藏实现细节

```cpp
// A.h
class B;  // 前置声明
class A { B* b; };

// B.h
class A;  // 前置声明
class B { A* a; };

// A.cpp
#include "B.h"  // 在实现文件中完整包含
```

## 优化技术

### 前置声明（Forward Declaration）

**原则**：尽可能使用前置声明而不是完整包含

**何时使用前置声明**：
- 指针或引用
- 函数参数或返回值
- 类成员指针

```cpp
// 不好
#include "MyClass.h"
class Container {
    MyClass* ptr;
    void func(MyClass* obj);
};

// 好
class MyClass;  // 前置声明
class Container {
    MyClass* ptr;
    void func(MyClass* obj);
};
```

**何时必须包含**：
- 继承关系
- 成员变量（非指针）
- 模板参数

### PIMPL 模式

**用途**：隐藏实现细节，减少编译依赖

**示例**：

```cpp
// MyWidget.h
class MyWidget {
public:
    MyWidget();
    ~MyWidget();
    void doSomething();

private:
    class Impl;  // 前置声明
    Impl* pImpl;  // 指向实现
};

// MyWidget.cpp
#include "MyWidget.h"
#include "PrivateHeader.h"  // 只在实现中包含

class MyWidget::Impl {
    // 实现细节
    void detailedOperation() { ... }
};

MyWidget::MyWidget() : pImpl(new Impl) {}
MyWidget::~MyWidget() { delete pImpl; }
void MyWidget::doSomething() {
    pImpl->detailedOperation();
}
```

**优势**：
- 头文件不包含实现细节
- 修改实现不触发客户端重编译
- 减少头文件依赖

### 预编译头文件（PCH）

**用途**：对稳定依赖使用预编译头

**OpenHarmony 中的使用**：

```cpp
// precompile.h
// 包含所有稳定、常用的系统头文件
#include <memory>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <functional>
// ... 其他标准库头文件
```

**配置 PCH**：

在 BUILD.gn 中：
```gn
config("precompile_config") {
  precompiled_header = "precompile.h"
  precompiled_source = "precompile.cc"
}
```

### Include Guards 和 Pragma Once

**用途**：防止重复包含

```cpp
// 方法 1: Include guards
#ifndef MY_HEADER_H
#define MY_HEADER_H

// 内容...

#endif  // MY_HEADER_H

// 方法 2: Pragma once（推荐）
#pragma once

// 内容...
```

**OpenHarmony 推荐使用**：`#pragma once`

### 减少头文件包含

**策略 1：在 .cpp 中包含**

```cpp
// MyWidget.h
class MyWidget {
    void paint();
};

// MyWidget.cpp
#include "MyWidget.h"
#include "render/canvas.h"  // 只在实现中包含
#include "utils/painter.h"

void MyWidget::paint() {
    Canvas canvas;
    Painter painter(canvas);
    // ...
}
```

**策略 2：使用依赖注入**

```cpp
// 不好：直接依赖
class Database {
    Connection* conn;
};

// 好：注入依赖
class Database {
    Database(Connection* c) : conn(c) {}
    Connection* conn;
};
```

## 重构策略

### 识别热点文件

**方法 1：使用编译分析**

```bash
# 分析多个文件，找出编译最慢的
for file in framework/core/**/*.cpp; do
  ./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$file" 2>&1 | \
    grep "编译时间"
done | sort -t: -k2 -nr | head -20
```

**方法 2：从构建日志提取**

```bash
# 查看 ninja 构建日志
grep "CXX" out/rk3568/.ninja_log | \
  awk '{print $1, $2}' | \
  sort -nr | \
  head -20
```

### 重构步骤

**步骤 1：测量基线**

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp > baseline.txt
```

**步骤 2：分析依赖**

```bash
# 查看依赖树深度和宽度
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py \
  out/rk3568/obj/.../frame_node.ii
```

**步骤 3：应用优化**

根据分析结果应用相应优化：
- 移除未使用的包含
- 使用前置声明
- 应用 PIMPL 模式
- 拆分大文件

**步骤 4：验证改进**

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp > optimized.txt

diff baseline.txt optimized.txt
```

**步骤 5：回归测试**

确保优化没有破坏功能：
```bash
./build.sh --product-name rk3568 --build-target ace_engine_test
```

## 常见反模式

### 反模式 1：万能头文件

**问题**：创建包含一切的"common.h"

```cpp
// 不好
// common.h
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include "utils/a.h"
#include "utils/b.h"
#include "utils/c.h"
// ... 100+ 包含
```

**后果**：
- 包含 common.h 会拖入大量依赖
- 任何依赖变化都会触发重编译

**解决**：按需包含

### 反模式 2：内联一切

**问题**：在头文件中实现所有函数

```cpp
// 不好
// MyWidget.h
class MyWidget {
public:
    void func1() { /* 复杂实现 */ }
    void func2() { /* 复杂实现 */ }
    void func3() { /* 复杂实现 */ }
};
```

**后果**：
- 增加编译时间
- 增加头文件大小
- 可能导致代码膨胀

**解决**：在 .cpp 中实现

### 反模式 3：过度使用模板

**问题**：对所有东西使用模板

```cpp
// 不好：不需要模板的地方使用模板
template<typename T>
class Logger {
    void log(T message) { std::cout << message; }
};
```

**解决**：只在必要时使用模板

```cpp
// 好：使用多态或类型擦除
class Logger {
public:
    virtual void log(const std::string& message) = 0;
};
```

## 工具辅助

### 使用 include-what-you-use

```bash
# 安装
sudo apt install iwyu

# 分析
include-what-you-use \
  -I/path/to/includes \
  frameworks/core/components_ng/base/frame_node.cpp
```

### 使用 CPath

```bash
# 分析包含关系
path picker --file frame_node.cpp
```

### 使用 Clang-Tidy

```bash
# 检查现代 C++ 用法和潜在问题
clang-tidy \
  -checks='modernize-*' \
  frameworks/core/components_ng/base/frame_node.cpp \
  -- -I/path/to/includes
```

## 测量影响

### 量化改进

创建脚本跟踪改进：

```bash
#!/bin/bash
# track_improvements.sh

FILE="$1"
ITERATION="$2"

./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$FILE" | \
  grep -E "编译时间|峰值内存" | \
  tee -a improvements_${ITERATION}.log
```

使用方法：

```bash
# 基线
track_improvements.sh frame_node.cpp baseline

# 第一次优化后
track_improvements.sh frame_node.cpp v1

# 第二次优化后
track_improvements.sh frame_node.cpp v2

# 对比
diff improvements_baseline.log improvements_v2.log
```

## OpenHarmony 特定考虑

### ACE Engine 结构

了解 ACE Engine 的组件依赖：
- `frameworks/core/components_ng/` - 核心组件
- `frameworks/bridge/` - 前端桥接
- `frameworks/base/` - 基础工具

### GN 构建系统优化

在 BUILD.gn 中优化依赖：

```gn
# 减少公开依赖
source_set("my_component") {
  sources = [ "my_component.cpp" ]
  deps = [
    ":private_dependency",  # 私有依赖
  ]
  public_deps = [
    "//public/interface",   # 只暴露必要的公开接口
  ]
}
```

### 分层编译

利用 OpenHarmony 的分层架构：
- 基础层优先编译
- 使用预编译库
- 最小化跨层依赖
