# ets_runtime 编译、测试、运行参考

> **读者**：Planner（编译验证）、Worker（编写测试用例）
> **按需读取**：读取 `SKILL_ROOT/ets_runtime.md`（`SKILL_ROOT` 为 Planner 注入的技能根路径）

## 目录

- [路径约定](#路径约定)
- [1. GN 构建（完整构建系统）](#1-gn-构建完整构建系统)
- [2. 直接用二进制运行 JS/TS（不走 GN）](#2-直接用二进制运行-jsts不走-gn)
- [3. TS 测试用例编写](#3-ts-测试用例编写)
- [4. Planner 编译验证流程](#4-planner-编译验证流程)

---

## 路径约定

以下用 `OHOS_ROOT` 表示包含 `ark.py` 的根目录（ets_runtime 往上两级），`OUT` 表示 `${OHOS_ROOT}/out/x64.debug`。

**二进制位置**：

| 工具 | 路径 |
|------|------|
| es2abc | `$OUT/arkcompiler/ets_frontend/es2abc` |
| ark_js_vm | `$OUT/arkcompiler/ets_runtime/ark_js_vm` |
| ark_aot_compiler | `$OUT/arkcompiler/ets_runtime/ark_aot_compiler` |

---

## 1. GN 构建（完整构建系统）

### 构建命令

```bash
cd ${OHOS_ROOT} && python3 ark.py x64.debug              # 全量构建
cd ${OHOS_ROOT} && python3 ark.py x64.debug {target}      # 单个 target
```

### GN Target 命名规则

target 名 = `{test_name}{Mode}Action`：

| Mode | 含义 | 示例 |
|------|------|------|
| `Jit` | JIT 模式执行 | `divJitAction` |
| `Aot` | AOT 编译+执行 | `divAotAction` |
| `AotCompile` | 仅 AOT 编译（不执行） | `divAotCompileAction` |
| （无后缀） | 取决于 BUILD.gn 中的模板 | `divAction` |

`test_name` 对应 `test/{aottest,jittest,moduletest,deopttest}/` 下的目录名。

### 常用命令

```bash
# 单个 JIT 测试
cd ${OHOS_ROOT} && python3 ark.py x64.debug divJitAction

# 单个 AOT 测试
cd ${OHOS_ROOT} && python3 ark.py x64.debug divAotAction

# 直接 ninja
ninja -C ${OHOS_ROOT}/out/x64.debug divJitAction
```

---

## 2. 直接用二进制运行 JS/TS（不走 GN）

适合快速验证逻辑，不需要完整构建流程。

### 设置库路径（一次性）

```bash
export LD_LIBRARY_PATH="\
$OUT/arkcompiler/ets_runtime:\
$OUT/thirdparty/icu:\
$OUT/thirdparty/zlib:\
$OUT/hiviewdfx/hilog:\
$OUT/thirdparty/bounds_checking_function:\
$OUT/resourceschedule/frame_aware_sched:\
$OUT/hmosbundlemanager/zlib_override:\
${OHOS_ROOT}/prebuilts/clang/ohos/linux-x86_64/llvm/lib"
```

### 编译 TS → ABC

```bash
$OUT/arkcompiler/ets_frontend/es2abc \
    --output test.abc --extension ts --module --merge-abc test.ts
```

### 运行模式

**解释器模式（C++ 解释器）**：
```bash
$OUT/arkcompiler/ets_runtime/ark_js_vm \
    --asm-interpreter=false \
    --entry-point=test test.abc
```

**ASM 解释器模式**：
```bash
$OUT/arkcompiler/ets_runtime/ark_js_vm \
    --asm-interpreter=true \
    --entry-point=test test.abc
```

**JIT 模式**：
```bash
$OUT/arkcompiler/ets_runtime/ark_js_vm \
    --asm-interpreter=true \
    --compiler-enable-jit=true \
    --compiler-jit-hotness-threshold=5 \
    --compiler-enable-litecg=true \
    --enable-force-gc=false \
    --entry-point=test test.abc
```

**注意**：`--entry-point` 的值 = ABC 文件名（不含 `.abc` 后缀）。

### ark_js_vm 关键 Flag

| Flag | 默认 | 说明 |
|------|------|------|
| `--asm-interpreter` | `false` | ASM 解释器（汇编加速，生产默认开启） |
| `--compiler-enable-jit` | `false` | JIT 总开关 |
| `--compiler-jit-hotness-threshold` | `2` | 函数调用几次后触发 JIT |
| `--compiler-enable-osr` | `false` | On-Stack Replacement（长循环内触发编译） |
| `--compiler-enable-litecg` | — | 轻量代码生成器 |
| `--enable-force-gc` | — | 强制 GC（测试中常设 false 避免干扰） |

### TS 中可用的 JIT 调试 API

```typescript
ArkTools.jitCompileAsync(func);                // 异步触发 JIT 编译
var ret = ArkTools.waitJitCompileFinish(func); // 等待完成，返回 true/false
```

---

## 3. TS 测试用例编写

ets_runtime 的 TS 测试是**端到端输出比对**：`.ts` → `es2abc` → `.abc` → `ark_js_vm` → 比对 `expect_output.txt`。

### 目录结构

每个测试用例是一个独立目录：

```
test/{aottest,jittest,moduletest,deopttest}/{test_name}/
├── BUILD.gn            # GN 构建定义（必须）
├── {test_name}.ts      # TypeScript 源码（必须）
└── expect_output.txt   # 预期输出（必须，前 13 行为版权头会被跳过）
```

### TS 测试文件写法

不使用任何测试框架，直接用 `print()` 输出结果：

```typescript
declare function print(arg:any):string;

function foo(a: number, b: number) { return a + b; }
print(foo(1, 2));       // → 3
print(foo(-1, 1));      // → 0
print(foo(0, 0));       // → 0
```

### expect_output.txt

前 13 行是版权头（被测试框架跳过），第 14 行起为预期输出：

```
Copyright (c) 20XX Huawei Device Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
3
0
0
```

### BUILD.gn 模板

根据测试类型选择对应模板（定义在 `test/test_helper.gni`）：

**JIT 测试**：
```gn
import("//arkcompiler/ets_runtime/test/test_helper.gni")

host_jit_test_action("test_name") {
}
```

**AOT 测试**：
```gn
import("//arkcompiler/ets_runtime/test/test_helper.gni")

host_aot_test_action("test_name") {
}
```

**Module 测试**：
```gn
import("//arkcompiler/ets_runtime/test/test_helper.gni")

host_moduletest_action("test_name") {
}
```

模板会自动查找同目录下的 `{test_name}.ts` 和 `expect_output.txt`。

### 注册到上级 BUILD.gn

新建测试目录后，必须在上级 `BUILD.gn` 中添加子目录引用：

```gn
# test/jittest/BUILD.gn
group("ark_jit_ts_test") {
  ...
  deps += [ "test_name:test_nameJitAction" ]
}
```

---

## 4. Planner 编译验证流程

> **读者**：Planner（步骤 5 编译验证时参考此章节）

### 自动检测工作目录

- **如果在 ets_runtime 目录下**（路径包含 `arkcompiler/ets_runtime`）：
  1. 令 `OHOS_ROOT` 为 ets_runtime 往上两级目录（即包含 `ark.py` 的目录）
  2. 根据 Plan 中的测试用例名，组装具体的编译命令（参照上方 GN Target 命名规则）
  3. **检查是否涉及 stub 文件修改**：`git diff --name-only` 中是否包含 `stub` 关键路径
     - **不涉及 stub**：命令追加 `--gn-args="skip_gen_stub=true"` 加速编译
     - **涉及 stub**：不添加该参数，正常编译
  4. **直接执行**编译命令，将对应 Task 的 Status 改为 `building`

- **否则（非 ets_runtime 项目）**：将对应 Task 的 Status 改为 `blocked`，Reason 写 `not an ets_runtime repo, build command unknown`，向用户询问编译命令，拿到后继续执行

### 编译失败处理

编译失败 → 将对应 Task 的 Status 改为 `build_failed`，Reason 写编译错误摘要，将错误信息附给 Worker，重新派发修复。
