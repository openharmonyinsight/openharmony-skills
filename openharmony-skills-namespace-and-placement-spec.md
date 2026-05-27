# OpenHarmony Skills 命名空间与目录放置规范

## 1. 目标

本文定义 OpenHarmony Skills 入库时的命名空间、目录结构、Skill 机器名、元数据和放置规则，用于约束 Skill 的创建、审核、发布和后续维护。

Skills 的实际创建由 Agent + skill-creator 完成。本文只规定生成后的目录与元数据要求，不规定手工创建命令。

## 2. 总体目录结构

Skills 仓库采用两大命名空间：

```text
skills/
  common/
  domain/
  README.md
```

| 目录 | 含义 |
| --- | --- |
| `common` | 公共 Skills，跨领域、跨子系统、跨团队复用 |
| `domain` | 领域 Skills，面向具体框架、子系统、技术域 |

## 3. 顶层目录结构

```text
skills/
  common/
    requirements/
    design/
    development/
    testing/
    cicd/
    troubleshooting/
    README.md

  domain/
    app-framework/
    arkruntime/
    arkui/
    arkweb/
    distributed/
    graphics/
    kernel/
    security/
    README.md

  README.md
```

`skills/README.md` 为仓库 Skills 总入口，必须说明 `common` 和 `domain` 的定位，并链接到对应目录。

## 4. `common` 目录放置规则

`common` 用于存放跨领域通用能力。

适合放入 `common` 的 Skills 包括：

1. 语言类能力，例如 C++、ArkTS、Python、Shell。
2. 通用编码规范、代码生成、代码修复能力。
3. 通用设计能力，例如 API 设计、DFX 设计、安全设计。
4. 通用测试能力，例如 UT 生成、XTS 生成、覆盖率分析。
5. 通用 CI/CD 能力，例如构建失败分析、门禁结果分析。
6. 通用问题分析能力，例如崩溃日志分析、内存问题分析、性能问题分析。

`common` 下按研发阶段组织：

```text
common/
  requirements/
  design/
  development/
  testing/
  cicd/
  troubleshooting/
```

公共 Skill 的放置规则：

```text
skills/common/<stage>/<skill-name>/
```

示例：

```text
skills/common/development/ohos-dev-cpp-coding-style/
skills/common/development/ohos-dev-arkts-syntax-checking/
skills/common/design/ohos-design-api-review/
skills/common/testing/ohos-test-ut-generation/
skills/common/cicd/ohos-ci-build-failure-analysis/
skills/common/troubleshooting/ohos-issue-crash-log-analysis/
```

## 5. `domain` 目录放置规则

`domain` 用于存放特定领域、框架、子系统相关的 Skills。

适合放入 `domain` 的 Skills 包括：

1. 强依赖某个框架、子系统或组件。
2. 只在某个领域场景下有效。
3. 需要领域专属 API、日志、工具链或评测集。
4. 不适合作为跨领域公共能力沉淀。

推荐领域目录：

```text
domain/
  app-framework/
  arkruntime/
  arkui/
  arkweb/
  distributed/
  graphics/
  kernel/
  security/
```

领域 Skill 的放置规则：

```text
skills/domain/<namespace-domain>/<stage>/<skill-name>/
```

其中 `<stage>` 必须使用完整阶段目录名：`requirements`、`design`、`development`、`testing`、`cicd`、`troubleshooting`。不得在目录中使用 Skill name 的阶段缩写，例如不得使用 `test/`、`issue/`、`dev/` 作为阶段目录。

示例：

```text
skills/domain/arkui/development/ohos-dev-arkui-component-development/
skills/domain/arkui/development/ohos-dev-arkui-state-management-v2/
skills/domain/arkui/testing/ohos-test-arkui-interaction-testing/
skills/domain/kernel/troubleshooting/ohos-issue-kernel-panic-analysis/
skills/domain/security/design/ohos-design-security-threat-modeling/
```

说明：`<namespace-domain>` 是目录命名空间，例如 `arkui`、`kernel`、`security`。Skill 机器名中的 `<domain>` 是 Skill 主题域，通常应与 `<namespace-domain>` 一致；如确需细分，必须在 README 中说明。若 `<namespace-domain>` 或 Skill 主题域包含连字符，可以在 Skill 机器名和 `metadata.domain` 中使用同一个稳定别名，例如 `graphics-3d`。

## 6. Skill 机器名命名规则

Skill 机器名统一采用：

```text
ohos-<stage>-<domain>-<capability>
```

字段说明：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `ohos` | OpenHarmony Skills 统一前缀 | 固定值 |
| `stage` | 使用阶段缩写 | `req` / `design` / `dev` / `test` / `ci` / `issue` |
| `domain` | 技术域、语言、框架、子系统或能力主题域 | `cpp` / `arkts` / `arkui` / `napi` / `dfx` |
| `capability` | 具体能力，必须使用动名词短语或名词短语，可由多个连字符分隔的词组成 | `coding-style` / `syntax-checking` / `api-review` / `log-analysis` |

解析规则：`ohos` 后的第一段是 `<stage>`；`<domain>` 与 `<capability>` 的切分以 `metadata.domain` 和 `metadata.capability` 为准。由于 `<domain>` 和 `<capability>` 都可能包含连字符，不能仅按连字符位置人工硬拆。例如 `ohos-test-graphics-3d-static-api-unit-test` 可对应 `metadata.domain = graphics-3d`、`metadata.capability = static-api-unit-test`。

命名要求：

```text
仅使用小写字母、数字、连字符
以 ohos- 开头
不使用空格、下划线、点号、斜杠
名称应稳定、清晰、可长期维护
同一仓库内 name 必须全局唯一
capability 必须是动名词短语或名词短语，不使用 `style`、`syntax`、`component`、`layout` 等单个宽泛名词
```

建议校验正则：

```text
^ohos-(req|design|dev|test|ci|issue)-[a-z0-9]+(-[a-z0-9]+)+$
```

说明：正则只校验字符形态；`<domain>` 与 `<capability>` 是否能通过 metadata 清晰切分、`capability` 是否符合动名词短语或名词短语要求，需要在入库评审中人工确认。

## 7. 阶段命名规范

目录阶段名和 `metadata.stage` 使用完整名称，Skill name 中使用阶段缩写。

| 目录阶段 | Skill name 阶段名 | 示例 |
| --- | --- | --- |
| `requirements` | `req` | `ohos-req-story-analysis` |
| `design` | `design` | `ohos-design-api-review` |
| `development` | `dev` | `ohos-dev-cpp-coding-style` |
| `testing` | `test` | `ohos-test-ut-generation` |
| `cicd` | `ci` | `ohos-ci-build-failure-analysis` |
| `troubleshooting` | `issue` | `ohos-issue-crash-log-analysis` |

注意：`test` 和 `issue` 只用于 Skill name 中的阶段缩写；目录和 `metadata.stage` 必须分别写作 `testing` 和 `troubleshooting`。

## 8. 单个 Skill 标准目录结构

每个 Skill 必须拥有独立目录。

标准结构：

```text
<skill-name>/
  SKILL.md
  README.md
  references/
  examples/
  evals/
```

推荐结构：

```text
ohos-dev-cpp-coding-style/
  SKILL.md
  README.md

  references/
    ...
  examples/
    good/
    bad/
  evals/
    prompts/
    expected/
    cases.yaml
```

| 文件 / 目录 | 是否必需 | 说明 |
| --- | --- | --- |
| `SKILL.md` | 必需 | Skill 主文件，供 Agent 加载 |
| `README.md` | 推荐 | 面向维护者的说明 |
| `references/` | 推荐 | 规范、资料、参考文档 |
| `examples/` | 推荐 | 正例、反例、修复前后样例 |
| `evals/` | 推荐 | 评测集、测试输入、期望结果 |

## 9. `SKILL.md` 元数据规范

每个 `SKILL.md` 必须包含 YAML Front Matter。

### 9.1 开放标准字段

YAML Front Matter 顶层开放标准字段只放 Agent 用于识别和触发 Skill 的字段：

| 字段 | 是否必需 | 示例 |
| --- | --- | --- |
| `name` | 必需 | `ohos-dev-cpp-coding-style` |
| `description` | 必需 | `Use when writing, reviewing, or fixing OpenHarmony C++ code to follow OpenHarmony C++ coding style.` |

顶层字段要求：

```text
name 必须与 Skill 目录名一致
description 必须说明何时触发该 Skill
OpenHarmony 入库治理、归类、版本、状态、作者等非开放标准字段不得直接放在顶层
```

### 9.2 OpenHarmony 扩展元数据

不在开放标准范围内的信息统一放入顶层 `metadata` 对象。也就是说，Front Matter 顶层允许 `name`、`description`、`metadata`；除这三个字段外，不得新增其他顶层字段。

基础格式：

```yaml
---
name: ohos-dev-cpp-coding-style
description: Use this skill when writing, reviewing, or fixing OpenHarmony C++ code to follow OpenHarmony C++ coding style.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: cpp
  capability: coding-style
  version: 0.1.0
  status: draft
  tags:
    - cpp
    - coding-style
  related-skills:
    - ohos-dev-cpp-memory-safety
---
```

公司要求的 OpenHarmony 扩展元数据：

| 字段 | 是否必需 | 示例 |
| --- | --- | --- |
| `metadata.author` | 必需 | 固定为 `openharmony` |
| `metadata.scope` | 必需 | `common` / `domain` |
| `metadata.stage` | 必需 | `development` |
| `metadata.domain` | 必需 | `cpp` |
| `metadata.capability` | 必需 | `coding-style` |
| `metadata.version` | 必需 | `0.1.0` |
| `metadata.status` | 必需 | `draft` / `trial` / `stable` / `deprecated` |

可选 OpenHarmony 扩展元数据：

| 字段 | 是否必需 | 示例 |
| --- | --- | --- |
| `metadata.tags` | 可选 | `cpp` / `coding-style` |
| `metadata.related-skills` | 可选 | `ohos-dev-cpp-memory-safety` |

与此前约定的重复关系：

| 公司 metadata 字段 | 此前约定 | 处理方式 |
| --- | --- | --- |
| `scope` | 原必需顶层字段 | 重复，迁移到 `metadata.scope` |
| `stage` | 原必需顶层字段 | 重复，迁移到 `metadata.stage` |
| `domain` | 原必需顶层字段 | 重复，迁移到 `metadata.domain` |
| `capability` | 原必需顶层字段 | 重复，迁移到 `metadata.capability` |
| `version` | 原推荐顶层字段 | 重复，迁移到 `metadata.version` |
| `status` | 原推荐顶层字段 | 重复，迁移到 `metadata.status` |
| `author` | 此前未约定 | 新增，固定为 `openharmony` |
| `tags` | 此前未约定 | 新增，可选 |
| `related-skills` | 此前未约定 | 新增，可选 |

元数据一致性要求：

```text
name 必须与 Skill 目录名一致
metadata.author 必须固定为 openharmony
metadata.scope 必须与一级命名空间一致：common 或 domain
metadata.stage 必须使用完整阶段名，并与阶段目录一致：requirements、design、development、testing、cicd、troubleshooting
metadata.domain 必须与 Skill name 中的 <domain> 字段一致
metadata.capability 必须与 Skill name 中的 <capability> 字段一致
domain scope 下，metadata.domain 默认应与 namespace-domain 一致
```

## 10. C++ 规范 Skill 落库规则

C++ 编码规范 Skill 正式命名为：

```text
ohos-dev-cpp-coding-style
```

目录位置：

```text
skills/common/development/ohos-dev-cpp-coding-style/
```

字段含义：

| 字段 | 含义 |
| --- | --- |
| `ohos` | OpenHarmony Skills |
| `dev` | development 阶段 |
| `cpp` | C++ 技术域 |
| `coding-style` | 编码规范 / 编码风格，属于名词短语 |

## 11. ArkTS 与 ArkUI 放置规则

### 11.1 ArkTS

ArkTS 属于公共语言能力，放入 `common/development`。

```text
skills/common/development/ohos-dev-arkts-syntax-checking/
skills/common/development/ohos-dev-arkts-coding-style/
```

### 11.2 ArkUI

ArkUI 属于领域框架能力，放入 `domain/arkui`。

```text
skills/domain/arkui/development/ohos-dev-arkui-component-development/
skills/domain/arkui/development/ohos-dev-arkui-state-management-v2/
skills/domain/arkui/testing/ohos-test-arkui-interaction-testing/
```

## 12. 推荐 Skill 命名示例

### `common/development`

```text
ohos-dev-cpp-coding-style
ohos-dev-cpp-memory-safety
ohos-dev-arkts-syntax-checking
ohos-dev-arkts-coding-style
ohos-dev-napi-binding
ohos-dev-hilog-usage
```

### `common/design`

```text
ohos-design-api-review
ohos-design-dfx-checking
ohos-design-security-baseline
ohos-design-testability-review
```

### `common/testing`

```text
ohos-test-ut-generation
ohos-test-xts-generation
ohos-test-coverage-analysis
ohos-test-fuzz-generation
```

### `common/cicd`

```text
ohos-ci-build-failure-analysis
ohos-ci-gate-checking
ohos-ci-log-analysis
ohos-ci-dependency-check
```

### `common/troubleshooting`

```text
ohos-issue-crash-log-analysis
ohos-issue-memory-leak-analysis
ohos-issue-performance-analysis
ohos-issue-regression-analysis
```

### `domain/arkui`

```text
ohos-dev-arkui-component-development
ohos-dev-arkui-state-management-v2
ohos-dev-arkui-layout-development
ohos-test-arkui-interaction-testing
ohos-issue-arkui-rendering
```

### `domain/security`

```text
ohos-design-security-threat-modeling
ohos-dev-security-permission-checking
ohos-test-security-fuzz-generation
ohos-issue-security-vulnerability-analysis
```

## 13. 新增 Skill 入库判断规则

### 13.1 放入 `common` 的判断

满足以下条件之一，放入 `common`：

```text
是否跨多个领域都能使用？
是否属于语言、规范、流程、工具类通用能力？
是否可以作为多个领域 Skill 的基础能力？
```

### 13.2 放入 `domain` 的判断

满足以下条件之一，放入 `domain`：

```text
是否强依赖某个框架、子系统或领域？
是否只在某个领域场景下有效？
是否需要领域专属 API、工具链、日志或评测集？
```

如同一能力既可公共复用又有领域特化版本，应采用不同 name，并在领域版本 README 中说明其与公共版本的关系。例如公共安全设计基线可命名为 `ohos-design-security-baseline`，安全领域威胁建模可命名为 `ohos-design-security-threat-modeling`。

## 14. skill-creator 生成约束

通过 Agent + skill-creator 创建 Skill 时，必须遵守以下约束：

```text
生成后的 Skill 必须位于规范目录下
生成后的 Skill 必须包含 SKILL.md
SKILL.md 中的 name 必须与目录名一致
name 必须符合 ohos-<stage>-<domain>-<capability>
capability 必须使用动名词短语或名词短语
description 必须位于 YAML Front Matter 顶层，并说明该 Skill 的触发场景
scope、stage、domain、capability、version、status、author 等非开放标准字段必须放入 metadata
metadata.author 必须固定为 openharmony
metadata.scope 必须与 common 或 domain 命名空间一致
metadata.stage 必须使用完整阶段名，并与阶段目录一致
metadata.domain、metadata.capability 必须与 name 中对应字段一致
不得使用阶段缩写作为目录名或 metadata.stage，例如 test、issue、dev
公共能力必须放入 common
领域能力必须放入 domain
```

例如：

```text
name: ohos-dev-cpp-coding-style
directory: skills/common/development/ohos-dev-cpp-coding-style/
```

其中：

```text
scope = common
stage = development
domain = cpp
capability = coding-style
```

上述字段在 `SKILL.md` 中应写为：

```text
metadata.scope = common
metadata.stage = development
metadata.domain = cpp
metadata.capability = coding-style
metadata.author = openharmony
```

## 15. 入库检查清单

每个 Skill 入库前应检查：

```text
[ ] Skill 是否有唯一 name？
[ ] Skill name 是否以 ohos- 开头？
[ ] Skill name 是否只使用小写字母、数字、连字符？
[ ] Skill name 是否符合 ohos-<stage>-<domain>-<capability>？
[ ] capability 是否使用动名词短语或名词短语？
[ ] Skill 目录名是否与 name 一致？
[ ] Skill 是否放入 common 或 domain 的正确目录？
[ ] Skill 是否放入正确阶段目录？
[ ] domain scope 下是否放入正确领域目录？
[ ] SKILL.md 是否存在？
[ ] SKILL.md 是否包含 YAML Front Matter？
[ ] YAML Front Matter 顶层是否只包含 name、description、metadata？
[ ] SKILL.md 是否包含 description？
[ ] description 是否说明何时触发该 Skill？
[ ] 非开放标准字段是否统一放入 metadata？
[ ] metadata.author 是否固定为 openharmony？
[ ] metadata.scope、metadata.stage、metadata.domain、metadata.capability 是否与目录和 name 一致？
[ ] metadata.stage 是否使用完整阶段名，而不是 test、issue、dev 等缩写？
[ ] 是否包含 README.md？
[ ] 是否根据需要包含 references、examples、evals？
```

## 16. 最终约定

当前入库规范固定为：

```text
C++ 规范 Skill name：ohos-dev-cpp-coding-style
目录位置：skills/common/development/ohos-dev-cpp-coding-style/
```

公共能力放置规则：

```text
skills/common/<stage>/<skill-name>/
```

领域能力放置规则：

```text
skills/domain/<namespace-domain>/<stage>/<skill-name>/
```

Skill name 统一遵循：

```text
ohos-<stage>-<domain>-<capability>
```

创建方式统一为：

```text
Agent + skill-creator
```

规范只约束生成结果，不提供手工创建命令。
