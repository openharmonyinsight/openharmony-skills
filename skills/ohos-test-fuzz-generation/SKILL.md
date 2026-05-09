---
name: ohos-test-fuzz-generation
description: >
  为 C/C++ 项目自动生成 FUZZ 测试用例、执行安全规范审查、生成语义化种子数据（corpus）。支持 LLVM libFuzzer 框架，兼容 OpenHarmony、Linux、Android 等构建系统。

  **必须激活场景**：
  - 用户提及 "fuzz 测试"、"生成 fuzzer"、"创建 fuzz 用例"、"fuzz 规范检查"、"fuzz_test"、"LLVMFuzzerTestOneInput"
  - 需要为类/API 编写 FUZZ 测试
  - 需要生成或验证 FUZZ 种子数据
  - 需要检查 FUZZ 代码是否符合安全编码规范

  **能力**：代码分析 → 用例生成 → 种子构造 → 26条规则合规审查 → 自动修复 → 报告生成。
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: fuzz
  capability: test-generation
  version: 0.1.0
  status: draft
  tags:
    - fuzz
    - testing
    - security
    - c++
---

# FUZZ 测试生成引擎

## 核心工作流

```
用户输入需求
      ↓
[决策点] 用户意图是什么？
    ├─ 给类名要求生成测试 → 进入完整工作流
    ├─ 给现有文件要求检查 → 跳至阶段 5（规范审查）
    ├─ 要求生成种子 → 跳至阶段 4（种子语义生成）
    └─ 要求生成报告 → 跳至阶段 5 后生成报告
      ↓
[阶段 1] 代码分析 —— 解析目标 API 类结构、方法签名、参数类型
      ↓
[阶段 2] 骨架生成 —— 创建 5 文件标准化工程（.cpp/.h/BUILD.gn/project.xml/corpus）
      ↓
[阶段 3] 实现填充 —— 模板替换为实际 API 调用与数据构造逻辑
      ↓
[阶段 4] 种子语义生成 —— 基于参数类型/名称特征生成高价值初始 corpus
      ↓
[阶段 5] 规范审查 —— 26 条规则逐一验证，输出合规报告
    **加载触发**：仅加载违规规则的 rules/SecurityCodeReview_FuzzCheck_XXX.md
    **必须加载**：规则 005 详细说明（复杂参数构造，误报高发区）
    **不要加载**：未违规规则
      ↓
[阶段 6] 自动修复 —— 可自动修复规则执行修复（最多 3 轮）
      ↓
交付生成文件 + 审查报告 + 人工确认项清单
```

**异常处理决策树**：
- 阶段 1 解析失败（找不到类/头文件）→ 检查类名拼写 → 提供头文件路径 → 手动解析
- 阶段 5 发现不可自动修复违规 → 输出人工修复指南 → 标记 BLOCK → 跳过修复
- 阶段 6 修复 3 轮后仍失败 → 停止修复 → 输出剩余违规清单 → 建议人工审查

## 工具入口

| 工具 | 用途 | 命令示例 |
|------|------|----------|
| `tools/fuzz_generator.py` | 生成 FUZZ 测试用例 | `python tools/fuzz_generator.py --class RSInterfaces` |
| `tools/fuzz_check.py` | 规范审查（26 条规则） | `python tools/fuzz_check.py --fix` |
| `tools/seed_generator.py` | 生成语义化种子 | `python tools/seed_generator.py --api ProcessImage` |
| `tools/generate_report.py` | 生成合规报告 | `python tools/generate_report.py` |

## 关键决策

### 生成测试前的自检问题

开始生成前，先确认：
1. **目标 API 是否有参数？** 无参数 → 拒绝生成，建议单元测试（规则 001）
2. **是 IPC 接口吗？** 继承 `IRemoteBroker` 或方法名含 `OnRemoteRequest` → 必须通过 stub 测试（规则 007）
3. **单文件接口数量？** >10 个 → 拆分为多个 fuzzer（规则 006）
4. **参数是否全为输出类型？** 非 const 引用/指针 → 跳过，无需 fuzz 输入

### 类型映射决策

| 类型类别 | 消费代码 | 说明 |
|----------|----------|------|
| 标识符类型（大驼峰非枚举） | `fdp.ConsumeIntegral<uint64_t>()` | 如 `ScreenId`/`NodeId`，底层是 `uint64_t` typedef |
| 进程/用户标识 | `fdp.ConsumeIntegral<uint32_t>()` | 如 `ProcessId`/`Uid` |
| 文件描述符 | `fdp.ConsumeIntegral<int32_t>()` | 如 `Fd` |
| 枚举类型 | `static_cast<EnumType>(fdp.ConsumeIntegral<uint8_t>() % ENUM_SIZE)` | **必须用 uint8_t**（规则 013） |
| 字符串 | `fdp.ConsumeRandomLengthString(256)` | 限制最大长度防止内存爆炸 |
| 容器 | 先消费长度 `uint8_t count = fdp.ConsumeIntegral<uint8_t>() % 32`，再循环消费 | 适用于 `std::vector<T>` |

**关键区分**：大驼峰命名不一定是枚举，可能是 typedef 别名。必须检查 `ENUM_SIZE_MAP` 确认是否为枚举。

**未知类型处理策略**：
- 类型在 `TYPE_CONSUMER_MAP` 中 → 直接使用映射
- 类型不在映射中但为大驼峰 → 检查 `ENUM_SIZE_MAP` → 是枚举则 `uint8_t % ENUM_SIZE`
- 类型不在映射中且非大驼峰 → 检查是否为 `std::vector<T>` → 是则循环消费
- 以上都不匹配 → **必须加载** `tools/fuzz_generator.py` 查看 `COMPLEX_TYPE_MAP` 或构造自定义消费逻辑

### NEVER 列表

- **NEVER** 使用 `rand()` / `random()` —— 不可重现，丧失覆盖率追踪意义（规则 017）
- **NEVER** 将 `size` 参数当作变异数据传入 API —— fuzz 引擎无法有效变异长度（规则 010）
- **NEVER** 直接解引用 `data` 指针 —— 可能包含非法地址，100% 触发 SIGSEGV（规则 018）
- **NEVER** 使用未初始化全局指针 —— fuzz 引擎会误判为稳定崩溃而停止探索（规则 019）
- **NEVER** 对无参数 API 生成 FUZZ —— 覆盖率永远为 0（规则 001）
- **NEVER** 单文件测试超过 10 个接口 —— 变异预算不足，覆盖率下降（规则 006）
- **NEVER** 使用 `auto` 声明 fuzz 变量 —— 无法人工验证类型匹配性（规则 016）
- **NEVER** 跳过 Verify 循环 —— 无法发现状态机相关 bug（资源泄漏、顺序依赖）
- **NEVER** 对枚举使用 `uint32_t` —— 1 字节变异效率远高于 4 字节（规则 013）

## 规范审查规则速查

### 代码安全规范（001–019）

| 规则 | 严重度 | 规则名称 | 自动检查 | 自动修复 |
|------|--------|----------|----------|----------|
| 001 | 🔴 高危 | 目标 API FUZZ 适用性评估（无参数/仅固定参数） | ✅ | ❌ |
| 002 | 🔴 高危 | 关键有参 API 覆盖完整性检查 | ✅ | ❌ |
| 003 | 🔴 高危 | 变异数据使用检测（FuzzedDataProvider 提取验证） | ✅ | ❌ |
| 004 | 🟡 中危 | 变异数据复用检测（同一变量多接口调用） | ✅ | ❌ |
| 005 | 🔴 高危 | 复杂参数构造合理性（结构体/指针/回调/容器） | ✅ | ❌ |
| 006 | 🟡 中危 | 单文件接口数量限制（超过 10 个告警） | ✅ | ❌ |
| 007 | 🔴 高危 | IPC 接口测试规范（必须通过 OnRemoteRequest 测试 stub） | ✅ | ❌ |
| 008 | 🟡 中危 | 种子合理构造（corpus 目录、种子文件大小和格式） | ✅ | ❌ |
| 009 | 🔴 高危 | FUZZ Driver 安全性（堆溢出/内存泄漏/整数溢出等 10 项检测） | ✅ | ❌ |
| 010 | 🔴 高危 | size 参数误用检测（禁止将 size 当作变异数据） | ✅ | ❌ |
| 011 | 🔴 高危 | 系统安全准入条件（权限/UID/Capability 等） | ⚠️ 部分 | ❌ 需人工 |
| 012 | 🔴 高危 | 目标 API 内部分支覆盖率评估 | ⚠️ 部分 | ❌ 需人工 |
| 013 | 🟡 中危 | 枚举值构造优化（优先 uint8_t 而非 uint32_t） | ✅ | ❌ |
| 014 | 🔴 高危 | 固定参数使用检测（可豁免场景识别） | ✅ | ❌ |
| 015 | 🔴 高危 | 中间产物合法性验证（编解码/序列化/加密等） | ⚠️ 部分 | ❌ 需人工 |
| 016 | 🔴 高危 | 数据类型匹配性（字节宽度/符号性/类型类别） | ✅ | ❌ |
| 017 | 🔴 高危 | 随机函数禁用检测（禁止 random/rand，强制使用 FDP） | ✅ | ✅ |
| 018 | 🔴 高危 | data 指针直接使用检测（禁止解引用/强转/当字符串使用） | ✅ | ❌ |
| 019 | 🔴 高危 | 全局变量初始化检查（禁止未初始化全局指针） | ✅ | ✅ |

### 文件格式规范（A–G）

| 规则 | 规则名称 | 自动检查 | 自动修复 |
|------|----------|----------|----------|
| A | 头文件规范（保护宏、系统头文件、FUZZ_PROJECT_NAME） | ✅ | ❌ |
| B | BUILD.gn 规范（ohos_fuzztest()、fuzz_config_file 路径、group("fuzztest")） | ✅ | ❌ |
| C | project.xml 规范（XML 声明、根元素 fuzz_config、必需配置项） | ✅ | ❌ |
| D | 目录名/文件名一致性（XxxXxx_fuzzer 格式） | ✅ | ❌ |
| E | .cpp 文件头文件完整性（自身头文件名一致且可编译） | ✅ | ❌ |
| F | 版权头规范（`Copyright (c) <year> Huawei Device Co., Ltd.`） | ✅ | ✅ |
| G | BUILD.gn 目标命名规范（XxxXxxFuzzTest，驼峰式 + FuzzTest 后缀） | ✅ | ❌ |

> **详细规则说明、正误示例和豁免条件**见 `rules/` 目录下的独立 Markdown 文件。
> **自动修复说明**：标注 ✅ 的规则支持 `fuzz_check.py --fix` 自动修复（当前支持规则 017/019/F）；标注 ⚠️ 的规则需要人工审查确认。

## References

**根据任务按需加载：**

- **`rules/SecurityCodeReview_FuzzCheck_XXX.md`** — 违规规则详细说明（正误示例 + 豁免条件）
  - **加载时机**：阶段 5 规范审查发现违规时
  - **不要加载**：未违规规则

- **`rules/SecurityCodeReview_FuzzCheck_005.md`** — 复杂参数构造规则详解
  - **加载时机**：涉及结构体/指针/回调/容器参数时
  - **原因**：规则 005 是误报高发区，需仔细核对豁免条件

- **`tools/fuzz_generator.py`** — 用例生成器源码
  - **加载时机**：需要了解生成逻辑或自定义类型映射时
  - **关键查看**：`TYPE_CONSUMER_MAP`、`ENUM_SIZE_MAP`、`COMPLEX_TYPE_MAP`

- **`templates/fuzzer.cpp`** — 代码生成模板
  - **加载时机**：需要自定义 fuzzer 代码结构时
  - **不要加载**：正常使用生成器时
