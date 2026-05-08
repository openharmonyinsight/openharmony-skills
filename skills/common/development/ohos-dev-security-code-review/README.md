# ohos-dev-security-code-review

OpenHarmony 通用开发阶段安全代码审查技能，用于审查 C++ 系统服务代码中的安全风险，重点覆盖 IPC 反序列化、并发共享状态、敏感信息日志和权限校验。

## 放置说明

该技能属于跨子系统复用的开发阶段安全代码审查能力，放置在：

```text
skills/common/development/ohos-dev-security-code-review/
```

该技能不放入 `domain/security`。`domain/security` 用于 SELinux、安全子系统、安全业务等领域专属技能。

命名字段对应关系：

| 字段 | 值 |
| --- | --- |
| scope | common |
| stage | development |
| domain | security |
| capability | code-review |

## 迁移来源

该技能从 `main` 分支的旧路径迁移而来：

```text
skills/openharmony-security-review/SKILL.md
```

迁移后按仓库命名空间与目录放置规范重命名为 `ohos-dev-security-code-review`。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 审查 OpenHarmony C++ 系统服务安全风险时使用的主路由文件 |
| `references/` | 按 IPC 输入校验、并发、隐私日志、权限校验、System Ability 信任边界拆分的按需加载资料 |
| `README.md` | 面向维护者的放置、命名和迁移说明 |
