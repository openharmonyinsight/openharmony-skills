# ArkUI Analysis

> 本目录存放 ArkUI 长期复用的上下文补充材料。它不替代 `profiles/arkui/profile.md` 的 gate 规则，只承载那些不该每次都默认塞进 profile 主文的背景、加载路径和验证补充。

## 读取顺序

默认不要全读。ArkUI 任务按下面顺序加载：

1. `profiles/arkui/profile.md`
2. 如命中模块类型，再读 `profiles/arkui/subprofiles/README.md` 和对应子 profile
3. 只有当任务需要更多背景时，再按需读取本目录的单篇文档

## 当前文档

| 文档 | 何时读取 | 作用 |
|---|---|---|
| [context-loading.md](context-loading.md) | 不确定该读哪些 ArkUI 上下文或需要检索策略时 | 给出 ArkUI 最小加载路径、检索流程、预算控制和按需扩展规则 |
| [asset-model.md](asset-model.md) | Define / Specify 初期需要梳理长期资产映射时 | 说明 `.codespec`、长期 `specs/`、SpecTest 资产之间的关系 |
| [gate-playbook.md](gate-playbook.md) | 执行 ArkUI gate、编写 `evidence/checks/*` 或 review gate 证据时 | 汇总 Define/Specify/Design/Plan gate 的细粒度执行规则 |
| [validation-playbook.md](validation-playbook.md) | Plan、Review、SpecTest/Host Preview 设计时 | 汇总 SpecTest 适用性、Build/Test 入口和验证分流 |

## 使用边界

- 本目录只提供可复用背景和操作补充，不单独定义 gate 结论。
- 若本目录结论与源码、Owner 结论或当前设计冲突，以当前事实为准。
- 发现这里的内容变旧时，优先回写本目录，而不是继续把长说明塞回 `profiles/arkui/profile.md`。
