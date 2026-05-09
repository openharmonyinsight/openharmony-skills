# ohos-dev-napi-module

OpenHarmony NAPI 模块开发技能，用于指导开发者创建 OpenHarmony 原生模块，重点覆盖模块注册、初始化、BUILD.gn 配置、扩展 API 使用、异步工作模式等关键流程，并详细说明与 Node.js N-API 的行为差异。

## 放置说明

该技能属于跨子系统复用的开发阶段 NAPI 模块开发能力，放置在：

```text
skills/common/development/ohos-dev-napi-module/
```

该技能不放入 `domain/napi`。`domain/napi` 用于 NAPI 子系统内部实现、测试框架等领域专属技能。

命名字段对应关系：

| 字段 | 值 |
| --- | --- |
| scope | common |
| stage | development |
| domain | napi |
| capability | module |

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 指导开发者编写 OpenHarmony NAPI 模块时使用的主路由文件 |
| `references/` | 按 API 行为差异、扩展 API、辅助宏、构建配置、异步工作模式拆分的按需加载资料 |
| `README.md` | 面向维护者的放置、命名和文件说明 |