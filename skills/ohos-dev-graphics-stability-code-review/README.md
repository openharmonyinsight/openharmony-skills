# OpenHarmony Stability Code Review Skill Library

## 项目说明

C/C++ 稳定性代码审查框架，由 **OpenHarmony图形稳定性团队** 维护，可推广至 OH 各子系统及非 OH 部门使用。

包含 **34 条稳定性规则**，覆盖异常处理、并发稳定性、资源管理、边界条件、图形稳定性等 **5 个稳定性分类**。所有规则以 Markdown 文档形式存放于 `references/` 目录。

## 快速开始

将本仓库放到 opencode skills 路径下：

```bash
# 全局（推荐，所有项目可用）
~/.config/opencode/skills/ohos-dev-graphics-stability-code-review/

# 项目级
<project>/.opencode/skills/ohos-dev-graphics-stability-code-review/
```

然后在 opencode 对话中直接输入：

```
# 全量扫描（遍历所有规则）
稳定性全量扫描 ./rosen/
代码稳定性检视 ./src/

# 指定规则扫描（遍历指定的所有规则）
用 ExceptionHandling_001 规则检视 ./src/
用 ExceptionHandling_001,ExceptionHandling_002,BoundaryCondition_001 规则检视 ./rosen/

# 按级别过滤扫描（遍历指定级别的所有规则）
对 ./rosen/ 做稳定性扫描，只检视 HIGH 级别的规则
对 ./src/ 进行稳定性扫描，检视 CRITICAL 和 HIGH 级别规则

# 指定分类扫描（遍历该分类下的所有规则）
对 ./src/ 做稳定性扫描，只检视异常处理分类的规则
用BoundaryCondition和GraphicsStability分类的规则检视 ./rosen/
```

报告自动输出到 `./report/` 目录，包含一个 Markdown 格式的详细说明文档和一个 CSV 格式的检出问题列表

## 项目结构

```
├── README.md                      # 项目说明（本文件）
├── SKILL.md                       # skill 技能说明
├── config/
│   ├── rules.yaml                 # 规则配置
│   └── whitelist.yaml             # 白名单配置
├── references/                    # 规则参考文档（核心）和报告输出格式示例
│   ├── RULE_INDEX.md              # 规则总索引
│   ├── RULE_DEVELOPMENT_GUIDE.md  # 规则开发完整指南
│   ├── RULE_TEMPLATE.md           # 规则文档模板
│   ├── PROBLEM_TEMPLATE.md        # 检出问题格式模板
│   ├── REPORT_TEMPLATE.md         # 报告输出格式模板（Markdown格式）
│   ├── REPORT_TEMPLATE.csv        # 报告输出格式模板（CSV格式）
│   ├── ExceptionHandling/         # 异常处理 规则目录（2条）
│   ├── ConcurrencyStability/      # 并发稳定性 规则目录（1条）
│   ├── ResourceManagement/        # 资源管理 规则目录（5条）
│   ├── BoundaryCondition/         # 边界条件 规则目录（14条）
│   └── GraphicsStability/         # 图形稳定性 规则目录（12条）
└── scripts/
    └── add-rule.py                # 规则脚手架工具
```

## 核心特性

- **34条稳定性规则**：覆盖5个稳定性分类
  - 异常处理：2条（ExceptionHandling_001~002）
  - 并发稳定性：1条（ConcurrencyStability_001）
  - 资源管理：5条（ResourceManagement_001~005）
  - 边界条件：14条（BoundaryCondition_001~014）
  - 图形稳定性：12条（GraphicsStability_001~012）
- **四级严重程度**：CRITICAL（2条）/ HIGH（24条）/ MEDIUM（8条）/ LOW（0条）
  - CRITICAL：Parcel数据处理不当导致内存越界等极高风险
  - HIGH：资源泄漏、线程安全、GPU资源管理等高风险
  - MEDIUM：编码规范、类型转换、JSON处理等中等风险
- **可覆盖模块**：ArkUI、ArkWeb、内核、图形、音频、窗口、语言运行时、相机、图库、框架等 OH 核心模块
- **部门可扩展**：各部门可按业务特点添加专属规则
- **跨平台支持**：适用于 OpenHarmony 及通用 C/C++ 项目

## 文档索引

- **核心文档**：
  - [规则总索引](references/RULE_INDEX.md) - 稳定性规则的完整列表，按严重程度和分类组织
  - [规则开发指南](references/RULE_DEVELOPMENT_GUIDE.md) - 规则开发完整指南，包含开发流程、检测要点、测试验证等
  - [规则文档模板](references/RULE_TEMPLATE.md) - 标准规则文档模板，定义规则文档结构和必填字段
- **配置文件**：
  - [规则配置文件](config/rules.yaml) - 稳定性规则的配置清单，包含规则ID、路径、启用状态等
  - [白名单配置](config/whitelist.yaml) - 路径白名单配置，跳过指定目录或文件的检视
- **输出模板**：
  - [检出问题格式模板](references/PROBLEM_TEMPLATE.md) - 问题报告格式规范，包含问题描述、风险流分析、修复建议等字段
  - [报告输出格式模板(Markdown)](references/REPORT_TEMPLATE.md) - 代码检视报告的标准输出格式
  - [报告输出格式模板(CSV)](references/REPORT_TEMPLATE.csv) - 检出问题列表的标准输出格式

## 工作流程

1. **规则加载**：根据请求加载 `config/rules.yaml` 中启用的规则，读取对应的 `references/` 规则文档
2. **代码检视**：AI 模型根据规则文档中的检测要点、检测范围对代码进行检视
3. **误报过滤**：参考规则文档中的误报排除表格，跳过测试代码、白名单路径
4. **问题分析**：输出完整的问题描述、风险流分析（RiskFlow）、影响分析（ImpactAnalysis）、修复建议
5. **报告输出**：生成 Markdown 报告和 CSV 报告到 `./report/`

## 贡献者

- **维护团队**：OpenHarmony图形稳定性团队
- **贡献方式**：欢迎各 OH 子系统部门及外部开发者贡献规则，共建稳定性生态
- **联系方式**：如有问题或建议，欢迎提交 Issue 或 PR