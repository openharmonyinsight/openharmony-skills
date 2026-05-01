# OpenHarmony Skills

本仓库用于集中管理 OpenHarmony 相关 Skills，约束 Skill 的目录放置、命名、元数据、评测资料和后续维护方式。

Skills 的创建统一通过 Agent + skill-creator 完成。本仓库只保存生成后的 Skill 目录、说明文档、参考资料、示例和评测集。

## 目录结构

```text
skills/
  common/
  domain/
```

| 目录 | 说明 |
| --- | --- |
| `skills/common/` | 公共 Skills，面向跨领域、跨子系统、跨团队复用的通用能力 |
| `skills/domain/` | 领域 Skills，面向具体框架、子系统或技术域的专用能力 |

`common` 按研发阶段组织，例如需求、设计、开发、测试、CI/CD 和问题分析。

`domain` 按 OpenHarmony 领域组织，例如 ArkUI、ArkWeb、ArkRuntime、Kernel、Graphics、Security 等。

## 规范文档

入库前必须遵守命名空间与目录放置规范：

[openharmony-skills-namespace-and-placement-spec.md](openharmony-skills-namespace-and-placement-spec.md)

核心约定：

```text
公共能力：skills/common/<stage>/<skill-name>/
领域能力：skills/domain/<namespace-domain>/<stage>/<skill-name>/
Skill name：ohos-<stage>-<domain>-<capability>
```

示例：

```text
skills/common/development/ohos-dev-cpp-style/
skills/domain/arkui/development/ohos-dev-arkui-component/
```

## 新增 Skill 流程

新增 Skill 时应先判断能力归属：

1. 跨领域通用能力放入 `skills/common/`。
2. 强依赖具体框架、子系统或领域工具链的能力放入 `skills/domain/`。
3. Skill 机器名必须以 `ohos-` 开头，并在仓库内全局唯一。
4. `SKILL.md` 中的 `name`、`scope`、`stage`、`domain`、`capability` 必须与目录位置和 Skill 机器名一致。

## 单个 Skill 推荐结构

```text
<skill-name>/
  SKILL.md
  README.md
  references/
  examples/
  evals/
```

`SKILL.md` 是必需文件，供 Agent 加载。`README.md`、`references/`、`examples/` 和 `evals/` 根据 Skill 复杂度补充。

## 入库检查

提交前至少确认：

```text
[ ] Skill name 是否唯一且符合 ohos-<stage>-<domain>-<capability>
[ ] Skill 目录名是否与 SKILL.md 中的 name 一致
[ ] Skill 是否放入正确的 common 或 domain 目录
[ ] SKILL.md 是否包含有效的 YAML Front Matter
[ ] description 是否说明该 Skill 的触发场景
[ ] 元数据字段是否与目录和 Skill name 一致
```
