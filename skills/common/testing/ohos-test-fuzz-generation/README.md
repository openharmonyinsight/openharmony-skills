# ohos-test-fuzz-generation

OpenHarmony FUZZ 测试自动生成 Skill —— 为 C/C++ 类/API 自动生成完整的 libFuzzer 测试工程，执行 26 条安全规范审查，生成语义化种子数据。

## 这是什么

一个 opencode Agent Skill，让 AI Agent 掌握 OpenHarmony fuzz 测试领域的专家知识。激活后，Agent 能：

1. **生成完整 fuzzer 工程** — 输入一个 C++ 类名和头文件，输出 5 文件标准化项目（.cpp/.h/BUILD.gn/project.xml/corpus），无需手写
2. **审查现有 fuzzer 代码** — 按 26 条规则逐项检查，输出合规报告，支持自动修复部分违规
3. **生成语义化种子** — 基于参数类型/名称特征构造高价值初始 corpus，而非随机字节
4. **IPC stub 自动识别** — 检测 IRemoteBroker 继承时自动切换到 OnRemoteRequest stub 模式，而非普通方法调用

## 如何使用

### 安装

将本 skill 目录复制到 opencode skill 配置目录即可：

```bash
# Linux/macOS
cp -r skills/ohos-test-fuzz-generation ~/.config/opencode/skill/

# Windows
xcopy /E /I skills\ohos-test-fuzz-generation %USERPROFILE%\.config\opencode\skill\
```

### 激活

安装后无需手动调用。对话中出现关键词时自动触发：

> fuzz 测试 / 生成 fuzzer / 创建 fuzz 用例 / fuzz 规范检查 / fuzz_test / LLVMFuzzerTestOneInput / 种子数据 / corpus

### 示例对话

```
用户: 为 ConfigManager 类生成 fuzz 测试用例，头文件在 src/config_manager.h
Agent: [自动激活skill] → 解析头文件 → 生成5文件工程 → 规范审查 → 交付

用户: 检查这个 rsinterfaces_fuzzer.cpp 是否符合规范
Agent: [自动激活skill] → 26条规则审查 → 输出违规清单 → 可自动修复

用户: 为这个 fuzzer 生成语义化种子数据
Agent: [自动激活skill] → 分析参数类型 → 生成边界/特殊/业务场景种子文件
```

## 架构概览

```
用户需求
    ↓
SKILL.md（决策树 + 纯专家知识）← Agent 加载此文件获得领域知识
    ↓
6 阶段工作流
    ├─ 阶段 1 代码分析    → tools/header_parser.py
    ├─ 阶段 2 骨架生成    → templates/ (5文件模板)
    ├─ 阶段 3 实现填充    → tools/fuzz_generator.py (类型映射 + IPC检测)
    ├─ 阶段 4 种子生成    → tools/seed_generator.py
    ├─ 阶段 5 规范审查    → tools/fuzz_check.py → check_scripts/ (26规则) → rules/ (详细说明)
    └─ 阶段 6 自动修复    → tools/fuzz_check.py --fix
```

核心决策逻辑在 SKILL.md 中：类型映射决策表、IPC stub 检测规则、NEVER 列表、未知类型处理策略。工具只负责执行，策略由 Skill 驱动。

## 目录结构

```
ohos-test-fuzz-generation/
├── SKILL.md              ← Skill 定义（Agent 读取的唯一入口）
├── tools/                ← 4 个执行工具（Agent 按需调用）
│   ├── fuzz_generator.py    生成 fuzzer（TYPE_CONSUMER_MAP / ENUM_SIZE_MAP / COMPLEX_TYPE_MAP / IPC stub 检测）
│   ├── fuzz_check.py        26条规则审查 + 自动修复
│   ├── seed_generator.py    语义化种子生成
│   ├── generate_report.py   合规报告
│   └── header_parser.py     头文件解析
├── check_scripts/        ← 26条规则独立检查脚本（fuzz_check.py 调用）
├── rules/                ← 规则详细说明文档（阶段5按需加载）
├── templates/            ← 5文件工程模板（fuzz_generator.py 调用）
├── references/           ← 按需加载参考资料
│   └── rules-overview.md    规则速查表
└── evals/                ← 81个评测用例 + benchmark 结果
```

## 规则体系

26 条规则覆盖两大维度：

**代码安全（001-019）** — 参数适用性、变异数据使用、IPC stub、Driver 安全、枚举优化、类型匹配、随机函数禁用等

**文件格式（A-G）** — 头文件规范、BUILD.gn、project.xml、命名一致性、版权头等

规则速查表见 `references/rules-overview.md`（仅阶段5加载），详细说明见 `rules/SecurityCodeReview_FuzzCheck_XXX.md`。

## 评测

81 个评测用例，234 条断言，6 类全覆盖（触发/核心场景/工作流/边界/文档/禁止做法）：

| 配置 | 通过率 |
|------|:------:|
| with_skill | 100% (234/234) |
| without_skill | 27.8% (65/234) |
| **Delta** | **+72.2%** |

详见 `evals/README.md`。
