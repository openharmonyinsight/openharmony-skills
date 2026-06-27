# ohos-design-c-api-review

鸿蒙 C API 接口设计的规范性检视技能，覆盖 `.h` 头文件中 API 函数声明、指针参数、缓冲区、注释等规范要求。

## 项目说明

由 OpenHarmony API 规范团队维护，面向 HarmonyOS C API 设计场景。技能内置 50 条规则，分为 9 大类：

| 类别 | 覆盖范围 |
|------|---------|
| 命名规范 | 函数命名、模块前缀、肯定表达式、对仗词、缩写、动词/名词词性、单复数 |
| 接口设计 | 单一职责、参数个数、可选参数、句柄设计、输出参数位置 |
| 安全 | 敏感权限、隐私数据、越权访问 |
| 异常定义 | 错误码宏、返回码枚举、错误码分段 |
| 异常实现 | 返回码校验、参数校验、错误信息 |
| 类型与数据规范 | 整数宽度、枚举类型、typedef、定长类型 |
| 注释说明 | Doxygen 完整性、参数描述、返回值描述 |
| 结构定义规范 | struct 字段顺序、内存对齐、可变性 |
| 指针规范 | `IN`/`OUT`/`INOUT` 标注、缓冲区长度、空指针检查、所有权 |

## 目录结构

```text
ohos-design-c-api-review/
├── SKILL.md              # 技能定义与全部 50 条规则
├── README.md             # 本文件
├── evals/
│   ├── evals.json        # 60 个评估用例
│   └── files/
│       ├── negative/     # 30 个违规样本（应被检出）
│       └── positive/     # 30 个合规样本（不应被误报）
└── benchmark.md          # with_skill / without_skill 评估对比报告
```

## 使用方式

将本仓库放到 opencode / Claude Code skills 路径下：

```bash
# 全局
~/.config/opencode/skills/ohos-design-c-api-review/

# 项目级
<project>/.opencode/skills/ohos-design-c-api-review/
```

触发方式（在对话中直接描述需求即可，技能会自动匹配）：

```
检视以下 C API 头文件的规范性：./sdk/c/native_buffer/native_buffer.h
审查这份 C API 接口设计：@ohos.native_buffer.h
```

输出：在 `save_dir` 目录下为每个被检文件生成 `review.md`，按规则逐条标注 `line_number`、`rule_name`、`advice`。

## 评估结果摘要

基于 `iteration-3` 的 60 个 eval（30 负向 + 30 正向）评估结果：

| 指标 | with_skill | without_skill |
|------|-----------|---------------|
| 平均通过率 | **100.0%** | 50.0% |
| 总检出数 | 204 | 90 |
| 正向用例误报 | **0** | 多处误报 |
| 问题检出倍数 | — | **2.3×** |

详细数据见 [`benchmark.md`](./benchmark.md)。
