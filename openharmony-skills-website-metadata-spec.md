# OpenHarmony Skills 网站展示元数据规范

## 1. 目标

本文定义 OpenHarmony Skills 在网站上结构化展示时使用的数据记录方式、字段模型、生成产物和后续工作流程。

核心目标：

```text
SKILL.md 继续服务 Agent 触发和执行
skill.info.yaml 服务网站展示、搜索、筛选和人类阅读
dist/skills.catalog.json 服务网站列表页、搜索页和筛选页
dist/skills/<skill-id>.json 服务网站详情页
```

不得把 `SKILL.md` 正文作为网站展示信息的直接来源。`SKILL.md` 是 Agent 执行指令，包含触发、流程、禁止事项、按需加载规则等内容，不适合作为面向用户的能力介绍。

## 2. 信息分层

每个 Skill 的信息分为三层：

| 层级 | 文件 | 使用方 | 定位 |
| --- | --- | --- | --- |
| Agent 执行层 | `SKILL.md` | Agent / Skill 运行时 | 触发和执行指令 |
| 网站展示源数据层 | `skill.info.yaml` | 网站生成脚本 / 人类维护者 | 结构化能力介绍和使用说明 |
| 网站生成产物层 | `dist/skills.catalog.json`、`dist/skills/<skill-id>.json` | 网站前端 | 列表、搜索、筛选和详情展示 |

`SKILL.md` 与 `skill.info.yaml` 都位于单个 Skill 目录下。`dist/` 是生成产物目录，不作为人工维护入口。

## 3. 单个 Skill 目录要求

在现有标准目录结构基础上，推荐新增 `skill.info.yaml`：

```text
<skill-name>/
  SKILL.md
  skill.info.yaml
  README.md
  references/
  examples/
  evals/
```

其中：

| 文件 | 是否必需 | 说明 |
| --- | --- | --- |
| `SKILL.md` | 必需 | Agent 加载的 Skill 主文件 |
| `skill.info.yaml` | 推荐，网站展示时必需 | 网站展示、搜索、筛选和详情页的源数据 |
| `README.md` | 推荐 | 面向维护者的补充说明 |

## 4. `skill.info.yaml` 字段模型

### 4.1 基础示例

```yaml
schemaVersion: 1

id: ohos-issue-graphics-cppcrash-analysis
title: 图形 cppcrash 崩溃分析
summary: 分析 OpenHarmony 图形模块 native 崩溃日志，定位崩溃根因并给出修复建议。

category:
  scope: domain
  namespace: graphics
  stage: troubleshooting
  domain: graphics
  capability: cppcrash-analysis

status:
  maturity: trial
  version: 0.1.0
  owner: openharmony

tags:
  - graphics
  - cppcrash
  - native-crash
  - troubleshooting

audience:
  - 图形子系统开发者
  - 崩溃问题定位人员
  - 值班问题分析人员

useCases:
  - title: 分析 SIGSEGV / SIGABRT 崩溃
    description: 根据 cppcrash、符号表和源码定位崩溃点。
  - title: 识别 Use-After-Free 或内存踩踏
    description: 结合地址模式、调用栈和源码进行数据流追踪。

whenToUse:
  - 图形模块发生 native cppcrash
  - 日志中包含 SIGSEGV、SIGABRT、cfi_slowpath_comm 等信号
  - 需要结合符号表和源码定位崩溃根因

whenNotToUse:
  - 纯 ArkTS / JS 层崩溃
  - 没有 cppcrash 日志
  - 没有匹配版本的符号表

inputs:
  required:
    - cppcrash 日志文件
    - 对应版本源码目录
    - lib.unstripped 符号表目录
  optional:
    - 相关 issue 背景
    - 复现步骤
    - 关联提交记录

outputs:
  - 崩溃根因分析报告
  - 精确代码位置
  - 修复建议
  - 进一步排查方向

quickStart:
  steps:
    - 准备 cppcrash 日志、源码目录和 lib.unstripped 目录。
    - 在问题描述中说明崩溃进程、复现背景和相关模块。
    - 请求 Agent 使用该 Skill 分析崩溃根因。
  examplePrompt: |
    请使用 ohos-issue-graphics-cppcrash-analysis 分析这个 cppcrash，
    日志在 crash.log，源码在 code/，符号表在 lib.unstripped/。

related:
  skills: []
  docs:
    - title: 解栈说明
      path: references/stack-unwinding.md
```

### 4.2 字段说明

| 字段 | 是否必需 | 说明 |
| --- | --- | --- |
| `schemaVersion` | 必需 | 当前固定为 `1` |
| `id` | 必需 | Skill 机器名，必须与目录名和 `SKILL.md` 的 `name` 一致 |
| `title` | 必需 | 网站展示标题，使用面向用户的中文短标题 |
| `summary` | 必需 | 一句话说明 Skill 能力，建议 30 到 80 个中文字符 |
| `category.scope` | 必需 | `common` 或 `domain` |
| `category.namespace` | 必需 | 所在命名空间目录。`common` 可使用阶段或主题，`domain` 使用领域目录名 |
| `category.stage` | 必需 | 完整阶段名：`requirements`、`design`、`development`、`testing`、`cicd`、`troubleshooting` |
| `category.domain` | 必需 | Skill 主题域，必须与 `SKILL.md` 的 `metadata.domain` 一致 |
| `category.capability` | 必需 | 具体能力，必须与 `SKILL.md` 的 `metadata.capability` 一致 |
| `status.maturity` | 必需 | `draft`、`trial`、`stable` 或 `deprecated` |
| `status.version` | 必需 | Skill 版本，必须与 `SKILL.md` 的 `metadata.version` 一致 |
| `status.owner` | 必需 | 当前固定为 `openharmony` |
| `tags` | 推荐 | 搜索、过滤和相关推荐使用 |
| `audience` | 推荐 | 适用用户角色 |
| `useCases` | 推荐 | 典型使用场景 |
| `whenToUse` | 必需 | 适用条件，帮助用户判断是否该用 |
| `whenNotToUse` | 推荐 | 不适用条件，降低误用 |
| `inputs.required` | 推荐 | 使用前必须准备的信息或文件 |
| `inputs.optional` | 可选 | 有助于提升效果的补充信息 |
| `outputs` | 推荐 | 使用后预期产出 |
| `quickStart.steps` | 推荐 | 简单使用步骤 |
| `quickStart.examplePrompt` | 推荐 | 可直接复制修改的示例 Prompt |
| `related.skills` | 可选 | 相关 Skill 的 `id` |
| `related.docs` | 可选 | 相关文档链接，路径相对当前 Skill 目录 |

## 5. 网站页面展示字段

### 5.1 列表页和搜索页

列表页、搜索页和筛选页需要快速回答“这个 Skill 是否相关”。建议展示：

```text
title
summary
status.maturity
status.version
category.scope
category.namespace
category.stage
category.domain
tags
audience
whenToUse
inputs.required
outputs
```

列表页不展示完整 `quickStart`、`useCases.description` 和 `related.docs`，避免卡片过重。

### 5.2 详情页

详情页需要回答“这个 Skill 能做什么、什么时候用、怎么用、需要准备什么”。建议展示：

```text
title
summary
category
status
tags
audience
useCases
whenToUse
whenNotToUse
inputs
outputs
quickStart
related
source path
```

详情页可以提供跳转到 `SKILL.md` 和 `README.md` 的入口，但不默认展开 `SKILL.md` 正文。

## 6. 生成产物

### 6.1 `dist/skills.catalog.json`

`skills.catalog.json` 是网站列表、搜索和筛选的索引文件。它应包含足够多的摘要字段，但不包含完整详情。

示例：

```json
{
  "schemaVersion": 1,
  "generatedAt": "2026-05-27T00:00:00Z",
  "skills": [
    {
      "id": "ohos-issue-graphics-cppcrash-analysis",
      "title": "图形 cppcrash 崩溃分析",
      "summary": "分析 OpenHarmony 图形模块 native 崩溃日志，定位崩溃根因并给出修复建议。",
      "scope": "domain",
      "namespace": "graphics",
      "stage": "troubleshooting",
      "domain": "graphics",
      "capability": "cppcrash-analysis",
      "status": "trial",
      "version": "0.1.0",
      "tags": [
        "graphics",
        "cppcrash",
        "native-crash",
        "troubleshooting"
      ],
      "audience": [
        "图形子系统开发者",
        "崩溃问题定位人员"
      ],
      "whenToUse": [
        "图形模块发生 native cppcrash",
        "需要结合符号表和源码定位崩溃根因"
      ],
      "inputs": [
        "cppcrash 日志文件",
        "对应版本源码目录",
        "lib.unstripped 符号表目录"
      ],
      "outputs": [
        "崩溃根因分析报告",
        "精确代码位置",
        "修复建议"
      ],
      "path": "skills/domain/graphics/troubleshooting/ohos-issue-graphics-cppcrash-analysis",
      "detailPath": "dist/skills/ohos-issue-graphics-cppcrash-analysis.json"
    }
  ]
}
```

### 6.2 `dist/skills/<skill-id>.json`

详情页 JSON 由 `skill.info.yaml` 生成，保留完整字段，并补充源文件路径。

示例：

```json
{
  "schemaVersion": 1,
  "id": "ohos-issue-graphics-cppcrash-analysis",
  "title": "图形 cppcrash 崩溃分析",
  "summary": "分析 OpenHarmony 图形模块 native 崩溃日志，定位崩溃根因并给出修复建议。",
  "category": {
    "scope": "domain",
    "namespace": "graphics",
    "stage": "troubleshooting",
    "domain": "graphics",
    "capability": "cppcrash-analysis"
  },
  "status": {
    "maturity": "trial",
    "version": "0.1.0",
    "owner": "openharmony"
  },
  "source": {
    "skillDir": "skills/domain/graphics/troubleshooting/ohos-issue-graphics-cppcrash-analysis",
    "skillFile": "skills/domain/graphics/troubleshooting/ohos-issue-graphics-cppcrash-analysis/SKILL.md",
    "infoFile": "skills/domain/graphics/troubleshooting/ohos-issue-graphics-cppcrash-analysis/skill.info.yaml"
  }
}
```

## 7. 首版信息提取流程

后续需要先用 Agent 从现有 `SKILL.md` 和 `README.md` 中提取一版 `skill.info.yaml`。建议流程如下：

1. 扫描所有包含 `SKILL.md` 的 Skill 目录。
2. 读取 `SKILL.md` YAML Front Matter，提取 `name`、`description` 和 `metadata`。
3. 读取 `SKILL.md` 正文中的以下结构化信息：
   - 解决的问题
   - 输入
   - 输出
   - 不适用情形
   - 触发信号
   - 典型流程
   - 参考资料
4. 若存在 `README.md`，优先补充面向人类用户的说明。
5. 生成首版 `skill.info.yaml`。
6. 标记提取不确定项，避免 Agent 伪造信息。
7. 由维护者人工 review 和修订。

Agent 提取时必须遵守：

```text
不得编造 SKILL.md 或 README.md 中没有依据的能力
不得把 Agent 内部执行禁令原样搬到网站展示文案
不得把长流程完整塞进 summary 或列表页字段
不确定字段可以留空或写入 extractionNotes
面向用户的 title、summary、whenToUse 应使用自然中文
```

可选增加临时字段：

```yaml
extractionNotes:
  confidence: medium
  missing:
    - audience
    - quickStart.examplePrompt
  comments:
    - README.md 不存在，quickStart 根据 SKILL.md 输入输出推导，需要人工确认。
```

`extractionNotes` 只用于首版治理，不建议进入网站详情页展示。

## 8. 网站生成流程

网站生成分为三个阶段：

### 8.1 校验阶段

生成前校验：

```text
skill.info.yaml 是否存在且 YAML 可解析
id 是否与目录名一致
id 是否与 SKILL.md front matter 的 name 一致
category.scope 是否与目录一级命名空间一致
category.stage 是否与阶段目录一致
category.domain 是否与 SKILL.md metadata.domain 一致
category.capability 是否与 SKILL.md metadata.capability 一致
status.version 是否与 SKILL.md metadata.version 一致
status.maturity 是否与 SKILL.md metadata.status 一致
related.skills 中的 Skill id 是否存在
related.docs 中的相对路径是否存在
```

### 8.2 构建阶段

构建脚本读取所有 `skill.info.yaml`，生成：

```text
dist/skills.catalog.json
dist/skills/<skill-id>.json
```

构建脚本不应从 `SKILL.md` 正文生成网站展示文案，只能使用 `SKILL.md` front matter 做一致性校验。

### 8.3 网站消费阶段

网站前端使用：

```text
dist/skills.catalog.json 渲染首页、列表页、搜索页和筛选页
dist/skills/<skill-id>.json 渲染详情页
```

网站可以提供 `SKILL.md`、`README.md` 和源码目录链接，但默认展示应来自生成后的 JSON。

## 9. 后续工作拆分

### 9.1 第一阶段：补充展示元数据

目标：为现有 Skill 生成首版 `skill.info.yaml`。

建议任务：

```text
编写提取 Prompt 或 Agent 工作流
批量扫描现有 Skill 目录
为每个 Skill 生成 skill.info.yaml
保留 extractionNotes
人工 review 重点 Skill
```

完成标准：

```text
每个需要上站展示的 Skill 都有 skill.info.yaml
核心字段 id、title、summary、category、status、whenToUse 可用
不确定项已在 extractionNotes 中标记
```

### 9.2 第二阶段：实现校验和生成脚本

目标：把 `skill.info.yaml` 转换成网站可消费的 JSON。

建议任务：

```text
实现 YAML 解析和字段校验
实现 SKILL.md front matter 一致性校验
实现 related.skills 和 related.docs 校验
生成 dist/skills.catalog.json
生成 dist/skills/<skill-id>.json
接入 CI 或本地检查命令
```

完成标准：

```text
校验失败时能指出具体 Skill、字段和原因
生成产物稳定、可重复
dist/skills.catalog.json 可直接被网站列表页消费
```

### 9.3 第三阶段：实现网站展示

目标：基于生成产物实现网站页面。

建议页面：

```text
首页：按 common / domain、stage、热门标签展示入口
列表页：支持 scope、namespace、stage、status、tag 筛选
搜索页：搜索 title、summary、tags、whenToUse、outputs
详情页：展示能力介绍、适用场景、输入输出、快速开始、相关 Skill 和文档
```

完成标准：

```text
用户可以在不阅读 SKILL.md 的情况下判断 Skill 是否适用
用户可以通过详情页知道如何准备输入和如何发起使用
列表页卡片信息足够判断相关性但不过载
```

## 10. 与命名空间规范的关系

本文不替代 `openharmony-skills-namespace-and-placement-spec.md`。

两份规范的关系：

```text
命名空间与目录放置规范：约束 Skill 如何命名、放在哪里、SKILL.md 元数据如何写
网站展示元数据规范：约束 Skill 如何被网站结构化展示、如何生成网站数据
```

当两者涉及同一字段时，以 `SKILL.md` 的开放标准字段和 OpenHarmony 扩展元数据作为治理事实源，`skill.info.yaml` 必须与其保持一致。
