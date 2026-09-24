> **Scope**: 编译错误速查表（hb 装配 / GN / Ninja / 链接阶段常见错误）
> **When**: 用户粘贴编译报错信息时，用 Grep 搜索本文件匹配错误
> **Size**: ~200 lines
> **Grep 用法**: `Grep references/error-cheatsheet.md "<错误关键词>"`

---

## 0. 快速分诊表（症状 → 根因 → 去哪查）

用户粘贴报错时，先按"症状"定位再跳到对应小节看修复；关键词明确时也可直接 Grep。

| 症状 | 最可能根因 | 跳到 |
|------|-----------|------|
| hb 提示 product not found / 列出产品无目标 | config.json 缺失 / product_name 不匹配 / 目录名 ≠ device_company+board | hb 装配 → product not found |
| gn gen 报 no such target / Can't find target | ohos.build module_list 指向不存在的 group | hb 装配 → no such target |
| gn gen 报 Can't load input file | import() 的 .gni 路径错 | GN → Can't load input file |
| 编译期 No such file xxx.h | include_dirs 缺路径 | Ninja → No such file |
| 链接 undefined reference to xxx | sources/deps 缺符号实现 | 链接 → undefined reference |
| 链接 region overflowed / will not fit | 代码或数据超 Flash/RAM | 链接 → overflowed |
| 启动即 Hard Fault / 中断不触发 | linker.ld 内存映射 / 向量表位置 / startup | 链接 → Hard Fault / vectors |
| 架构相关链接异常（乱码符号 / ABI 报错） | march/mabi 三处不一致（RISC-V 误用 -mcpu） | config-gni-guide → march/mabi 一致性 |

---

## hb 装配/产品发现阶段错误

执行 `./build.sh --product <product_name>` 时，hb 先发现产品、装配子系统/部件依赖图，再进入 gn gen。此阶段错误多源于 config.json / ohos.build / 目录约定不一致。

### **product not found** / **product** / **no such product** / **unknown product**

**错误消息**: `product "<name>" not found` 或 hb 列出可用产品后无目标产品。

**原因**: hb 找不到产品定义。mini(L0 轻量)/small(L1 小型) 产品由 `vendor/<device_company>/<board>/config.json` 定位。

**修复**:
1. 确认 `vendor/<device_company>/<board>/config.json` 存在，目录名 = `device_company` + `board`
2. 确认 config.json 的 `product_name` 与 `--product` 参数完全一致（含大小写）
3. 确认 `device_company`/`board` 字段与目录路径 `vendor/<device_company>/<board>/` 一致
4. mini/small 产品**不要**放 `productdefine/common/products/`（那是 standard）

### **no such target** / **target** / **module_list**

**错误消息**: `ERROR: Can't find target //vendor/<dc>/<board>:<board>` 或 `no such target`。

**原因**: `ohos.build` 的 `module_list` 指向的 target 在对应 BUILD.gn 中不存在。

**修复**:
1. 检查 `vendor/<dc>/<board>/ohos.build` 的 `module_list`，格式 `//vendor/<dc>/<board>:<target>`
2. 确认 `vendor/<dc>/<board>/BUILD.gn` 中定义了同名 target（`group("<target>")`），target 名 == module_list 冒号后的部分
3. 确认 ohos.build 的 part/subsystem 名 == `product_` + config.json 的 `product_name`

### **device_build_path** / **board build path** / **missing board**

**错误消息**: 找不到 board 构建入口，或 `device_build_path` 相关报错。

**原因**: config.json 的 `device_build_path` 指向的目录不存在 BUILD.gn。

**修复**:
1. 确认 config.json `device_build_path`（如 `device/board/hisilicon/hispark_pegasus`）目录存在
2. 该目录下必须有 Board 级 `BUILD.gn`（含 `group("<board>")`）
3. `device_build_path` 用相对源码根的路径，**不带** `//` 前缀

### **product_adapter_dir** / **adapter dir** / **hals**

**错误消息**: `product_adapter_dir` 路径缺失或 HAL 适配找不到。

**原因**: config.json 的 `product_adapter_dir` 指向的 `hals/` 目录不存在。

**修复**:
1. 确认 `vendor/<dc>/<board>/hals/` 目录存在且含 BUILD.gn
2. `product_adapter_dir` 用 `//` 开头绝对路径，如 `//vendor/hisilicon/hispark_pegasus/hals`

---

## GN 阶段错误

### **Can't load input file** / **import** / **load**

**错误消息**: `Can't load input file "xxx.gni"` 或 `Import "xxx" failed`
**原因**: import() 路径错误或文件不存在
**修复**:
1. 确认路径以 `//` 开头（绝对路径）或相对当前文件目录
2. 验证目标文件确实存在于指定路径
3. 检查路径中是否有拼写错误（区分大小写）

### **Dependency cycle** / **cycle** / **circular**

**错误消息**: `Dependency cycle detected`
**原因**: 配置文件互相 import 或 deps 形成循环引用
**修复**:
1. 找出循环路径（GN 会打印完整循环链）
2. 重构配置，将共用变量提取到独立文件
3. 使用 `import` 替代双向 deps

### **Expected a newline** / **newline** / **eof** / **syntax**

**错误消息**: `ERROR Expected a newline or eof`
**原因**: GN 文件语法格式问题——通常是文件末尾缺少空行、多余字符或括号不匹配
**修复**:
1. 运行 `gn format <file>` 自动格式化
2. 检查文件末尾是否有空行
3. 检查括号和引号是否成对

### **Expected string** / **type** / **Expected**

**错误消息**: `Expected string but got int` 或类似类型错误
**原因**: 变量赋值类型不匹配（如应为字符串但赋了整数）
**修复**:
1. 检查变量赋值，确保类型正确
2. 字符串需要双引号包裹：`board_cpu = "cortex-m4"`

### **Undefined variable** / **variable** / **not defined**

**错误消息**: `Undefined variable "xxx"` 或 `Variable "xxx" not defined`
**原因**: 变量在使用前未定义或未通过 import 导入
**修复**:
1. 检查 import 语句，确认包含该变量定义的 .gni 文件已导入
2. 确认变量名拼写正确（GN 区分大小写）
3. 如果变量可选，使用 `defined()` 检查：`if (!defined(board_opt_flags)) { board_opt_flags = [] }`

---

## Ninja 编译阶段错误

### **fatal error** / **No such file** / **header** / **include**

**错误消息**: `fatal error: xxx.h: No such file or directory`
**原因**: include_dirs 配置不完整，缺少头文件搜索路径
**修复**:
1. 确定缺失头文件所在的目录
2. 在 BUILD.gn 的 `include_dirs` 中添加该路径
3. 如果使用 SoC SDK，确认 `board_include_dirs` 包含 SDK 头文件路径
4. 路径使用 `//` 前缀表示源码根目录

### **misaligned** / **alignment** / **pointer dereference**

**错误消息**: `misaligned pointer dereference`
**原因**: 数据结构内存对齐不正确
**修复**:
1. 使用 `__attribute__((aligned(N)))` 指定对齐
2. 检查 `#pragma pack` 是否正确使用
3. 检查 DMA 缓冲区是否对齐到要求边界

### **multiple definition** / **redefinition** / **redefined**

**错误消息**: `multiple definition of 'xxx'`
**原因**: 同一符号在多个源文件中定义（非声明）
**修复**:
1. 将定义改为 `extern` 声明，仅在一个 .c 文件中保留定义
2. 检查是否在头文件中意外写了函数实现（应只写声明）
3. 检查 deps 中是否重复引入了同一库

### **undefined reference** / **reference** / **undefined**

**错误消息**: `undefined reference to 'xxx'` 或 `ld: symbol 'xxx' not found`
**原因**: 链接时找不到符号定义——缺少源文件或库
**修复**:
1. 确认包含该符号实现的源文件在 `sources` 列表中
2. 在 `deps` 中添加提供该符号的库或模块
3. 常见缺失符号及来源：
   - `printf`/`memcpy` → 需链接 C 库（检查 toolchain 配置）
   - `Reset_Handler` → 启动代码 startup.S 未链接
   - `LOS_TaskCreate` → 需 deps `//kernel/liteos_m/kernel:modules`

### **undeclared** / **implicit declaration** / **warning**

**错误消息**: `warning: implicit declaration of function 'xxx'`（配合 `-Werror` 变为错误）
**原因**: 函数使用前未声明，通常是缺少对应头文件的 include
**修复**:
1. 添加 `#include` 对应的头文件
2. 确认头文件在 include_dirs 中可找到

---

## 链接阶段错误

### **Hard Fault** / **hard fault** / **crash** / **boot**

**错误消息**: 运行时 Hard Fault（启动后立即崩溃）
**原因**: 内存映射错误、向量表位置不对、时钟未初始化
**修复**:
1. 检查 linker.ld 的 MEMORY 区域地址与芯片手册一致
2. 确认 `.vectors` 段位于 Flash 起始地址
3. 检查 startup.S 中的时钟初始化代码
4. 使用调试器查看 Hard Fault 的 PC 和 LR 寄存器定位崩溃点

### **region overflowed** / **overflowed** / **overflow** / **will not fit**

**错误消息**: `region 'RAM' overflowed by N bytes` 或 `section .text will not fit in region 'FLASH'`
**原因**: 代码或数据超出 Flash/RAM 容量
**修复**:
1. **代码溢出 Flash**：
   - 启用 LTO（Link-Time Optimization）：在 ldflags 加 `-flto`
   - 使用 `-Os` 或 `-Oz` 优化等级
   - 裁剪未使用的功能模块
   - 检查是否有大型调试信息未移除
2. **数据溢出 RAM**：
   - 减小缓冲区大小
   - 减少全局/静态变量
   - 减小栈和堆大小
   - 使用 `arm-none-eabi-size` 检查各段大小

### **Reset_Handler** / **entry point** / **startup**

**错误消息**: `undefined reference to 'Reset_Handler'` 或 `cannot find entry point`
**原因**: 启动代码（startup.S）未被链接或入口符号名不匹配
**修复**:
1. 确认 startup.S 在 BUILD.gn 的 sources 中
2. 检查 ENTRY() 指定的入口函数名与 startup.S 中定义的一致
3. ARM Cortex-M 通常是 `ENTRY(Reset_Handler)` 或 `ENTRY(g_bootVectors)`
4. RISC-V 通常是 `ENTRY(_start)`

### **vector table** / **vectors** / **vectors section**

**错误消息**: 启动后 Hard Fault 或中断不触发
**原因**: 向量表不在 Flash 起始位置，或偏移不正确
**修复**:
1. 检查 linker.ld 中 `.vectors` 段是否在 SECTIONS 的最前面
2. 确认 `KEEP(*(.vectors))` 保留向量表不被 gc-sections 移除
3. 验证向量表大小 = (中断数量 + 16) × 4 字节

### **BSS** / **bss** / **uninitialized**

**错误消息**: 全局变量值异常（未正确清零）
**原因**: BSS 段未正确清零或 BSS 地址不对
**修复**:
1. 检查 startup.S 中的 BSS 清零逻辑（通常用 `__bss_start` 和 `__bss_end`）
2. 确认 linker.ld 中 BSS 段的 `__bss_start` 和 `__bss_end` 符号定义正确

### **stack** / **stack overflow** / **Stack**

**错误消息**: 运行时 Hard Fault（函数调用时崩溃）
**原因**: 栈空间不足——递归过深、局部变量过大或中断嵌套
**修复**:
1. 增大 linker.ld 中的 `__stack_size`（默认 4KB → 尝试 8KB）
2. 减少深层递归，改为迭代
3. 将大型局部数组改为 static 或全局变量
4. 检查中断嵌套是否导致栈溢出
