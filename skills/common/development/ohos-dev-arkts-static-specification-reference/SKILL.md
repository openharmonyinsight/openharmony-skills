---
name: ohos-dev-arkts-static-specification-reference
description: "ArkTS static language specification reference for OpenHarmony. Use this skill when reading or writing ArkTS (.ets), explaining ArkTS type-system and static-semantics rules (Any type, nullish types, enum, cast expression, subtyping, assignability, compile-time error, async/await, generic constraint, concurrency), validating code against the ArkTS spec, investigating ArkTS compile-time behavior, or comparing ArkTS with TypeScript migration guidance."
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: arkts
  capability: static-specification-reference
  version: 0.1.0
  status: draft
  tags:
    - arkts
    - static-spec
    - specification-reference
    - type-system
    - typescript-migration
---

# ArkTS Static Language Specification

ArkTS 静态语言规范与 TypeScript 迁移参考。

## Rules

1. 只依据本 skill 目录下的 `spec/` 和 `cookbook/` 文档回答。
2. 不补充文档外规则，不按 TypeScript 习惯补全 ArkTS 语义。不假设 ArkTS 支持 TypeScript 的动态特性。
3. 文档未明确说明时，必须直接标注：
   `⚠️ skill 文档未明确说明，待使用者自行确认`
4. 涉及语义、类型、语法、约束、编译期行为时，优先查 `spec/`；尤其优先考虑 `semantics.md`、`types.md`、`expressions.md`、`classes.md`。
5. 涉及 TS 到 ArkTS 的支持性、迁移方式、兼容性差异时，优先查 `cookbook/`。
6. 回答优先给结论，再给依据文件名，最后给必要限制。对 TS 不支持写法，优先给出显式、静态、可编译的改写方案。
7. 若用户给出代码，先对照 NEVER 列表逐条检查，再指出违反的 ArkTS 规则，最后给最小修正方案。

## NEVER

- **NEVER** 将 ArkTS `Any` 与 TypeScript `any` 混淆 — ArkTS `Any` 是预定义 nullish 类型，所有类型的超类型，无方法无字段（spec/types.md）
- **NEVER** 假设 `number` 类型语义 — ArkTS 有独立数值体系 byte/short/int/long/float/double，`number` 仅限互操作场景（spec/types.md）
- **NEVER** 将 TS 的 `1/2 = 0.5` 推广到 ArkTS — ArkTS 整数除法 `int(1)/int(2) = 0`（spec/expressions.md）
- **NEVER** 混淆 `null` 和 `undefined` — ArkTS 中 `void` ≡ `undefined`，`null` 是独立类型且不推荐使用（spec/types.md）
- **NEVER** 将 nullish 类型赋值给 `Object` — `T | undefined` 不兼容 `Object`，是 compile-time error（spec/types.md Nullish Types）
- **NEVER** 猜测规范未定义的行为 — 必须输出 `⚠️ skill 文档未明确说明，待使用者自行确认`
- **NEVER** 用 TypeScript 装饰器语义解释 ArkTS 注解 — ArkTS 注解有独立的编译期处理规则（spec/annotations.md）
- **NEVER** 假设 `as` cast 一定成功 — 非字面量 cast 走 Runtime Checking 路径，类型不匹配时抛出 `ClassCastError`（spec/expressions.md）
- **NEVER** 忽略泛型约束默认值 — 无显式约束的泛型参数默认 `extends Any`，导致不兼容 `Object` 且无方法可用（spec/generics.md）
- **NEVER** 假设 enum 底层类型是 `number` — ArkTS enum 基类型为 `int` 或 `string`，混合初始化器类型导致 compile-time error（spec/enums.md）
- **NEVER** 混用 FixedArray 与 ResizableArray — 两者不可互赋值（not assignable to each other），且 FixedArray 无方法（spec/types.md）

## Problem Diagnosis

**先判断问题类型，再选择路径：**

| 问题类型 | 特征 | 入口 |
|---------|------|------|
| 规范查询 | "X 的语义是什么""ArkTS 是否支持 Y" | 直接走下方 Diagnosis 定位文件 |
| 代码诊断 | "这段代码为什么报错""编译失败原因" | 先对照 NEVER 列表逐条排查，再走 Diagnosis |

收到 ArkTS 相关问题后，按以下优先级快速定位：

1. **是否涉及类型兼容 / 赋值失败？** → 先查 nullish 规则（`spec/types.md`），再查子类型/赋值兼容（`spec/semantics.md`），最后查泛型默认约束（`spec/generics.md`）
2. **是否涉及表达式求值 / 运算结果不符合预期？** → 查数值体系与运算符语义（`spec/expressions.md`），注意整数除法截断、cast 的 Runtime Checking 路径
3. **是否涉及声明 / 作用域 / 可见性？** → 查名字解析（`spec/names.md`）和模块系统（`spec/modules.md`）
4. **是否从 TypeScript 迁移？** → 先查迁移概览（`cookbook/index.md`），再按具体语法查 recipes（`cookbook/cookbook-recipes.md`），最后对照行为差异（`cookbook/cookbook-compatibility.md`）
5. **是否涉及类 / 接口继承关系？** → 查类声明（`spec/classes.md`）和接口（`spec/interfaces.md`），注意 override 合法性在 `spec/semantics.md`

若以上路径均未命中，按以下顺序 fallback：
1. 用 `compile-time error` 或关键类型名在所有文件中 `Grep` 定位。
2. 若 Grep 也未命中，依次 `Read` `spec/semantics.md` 前 100 行（总览）和 `spec/types.md` 前 100 行，找到最接近的章节作为起点。
3. 若仍无结果，输出 `⚠️ skill 文档未明确说明，待使用者自行确认`。

## Routing

- 类型、类型关系、默认值、nullish、数组、tuple：`spec/types.md`
- 声明、作用域、名字解析、type alias：`spec/names.md`
- 泛型、泛型约束、泛型推断：`spec/generics.md`
- 转换、赋值上下文、数值转换：`spec/conversions.md`
- 表达式、运算符、instanceof、调用：`spec/expressions.md`
- 语句、控制流、循环、return：`spec/statements.md`
- 类、字段、方法、构造器、继承、override：`spec/classes.md`
- 接口、实现关系、接口成员：`spec/interfaces.md`
- 枚举：`spec/enums.md`
- 错误处理、throw、try：`spec/errors.md`
- 模块、import/export、namespace：`spec/modules.md`
- ambient / declare：`spec/ambients.md`
- 子类型、assignability、overload、override 合法性、类型推断规则：`spec/semantics.md`
- 并发、async/await、TaskPool、worker：`spec/concurrency.md`
- 标准库签名：`spec/stdlib.md`
- 实验特性：`spec/experimental.md`
- 运行时、二进制表示相关：`spec/runtime.md`, `spec/binary_compatibility.md`
- 语法归类、语法入口：`spec/grammar.md`
- 构建系统、导入解析、可见性：`spec/build_system.md`
- TS 迁移概览：`cookbook/index.md`
- 具体迁移规则：`cookbook/cookbook-recipes.md`
- TS 与 ArkTS 行为差异：`cookbook/cookbook-compatibility.md`

## Loading Strategy

### 大文件检索（>1500 行）

| 文件 | 行数 | 检索方法 |
|------|------|---------|
| expressions.md | ~5500 | 用关键词搜索 section 标题，不要全读 |
| semantics.md | ~2650 | 同上 |
| experimental.md | ~2470 | 同上 |
| classes.md | ~2180 | 同上 |
| types.md | ~2270 | 同上 |

具体方法：先 `Grep` 关键词定位 section，再用 `Read` 按行号范围读取。

### Do NOT Load

- 回答纯 ArkTS 静态规范问题 → 不要加载 `cookbook/`
- 回答 TS→ArkTS 迁移问题 → 不要加载 `spec/runtime.md`, `spec/build_system.md`, `spec/implementation.md`, `spec/binary_compatibility.md`
- `spec/grammar.md`（12行）和 `spec/stdlib.md`（17行）几乎无内容，不要作为主要依据

### 常见关键词分布

| 搜索关键词 | 主要分布文件（按命中数排序） |
|-----------|--------------------------|
| `compile-time error` (376处) | expressions(100), classes(57), experimental(47), types(21), semantics(33), modules(26), names(19), statements(16), annotations(15) |
| `Any` (83处) | types(20), experimental(47), statements(16), expressions(13), semantics(8) |
| `subtype` / `supertype` | semantics, types, generics, classes |
| `assignable` / `assignability` | semantics, types, conversions, generics |

## Working Style

处理问题时按下面顺序：

1. 先判断问题属于 `spec` 还是 `cookbook`。
2. 只打开必要文件，不通读整个目录。
3. **MANDATORY**：优先读取最直接相关的 1 到 2 个文件；不足时再扩展。对 >1500 行的文件必须先用 `Grep` 定位再按行号范围 `Read`，禁止全读。
4. 若多个文件可能冲突，优先采用更直接回答该问题的章节。
5. 回答时注明依据文件名。
6. 若文档没有直接结论，不推断，直接输出固定提示。

### 跨文件查询策略

当问题同时涉及多个规范域时，按优先级读取：

| 问题特征 | 主文件 | 补充文件 |
|---------|--------|---------|
| 类型 + 表达式（如 cast、运算） | `expressions.md` | `types.md` |
| 类型 + 赋值兼容 | `semantics.md` | `types.md`, `conversions.md` |
| 类 + 接口实现 | `classes.md` | `interfaces.md`, `semantics.md` |
| 泛型 + 类型推断 | `generics.md` | `semantics.md` |
| 迁移 + 行为差异 | `cookbook-recipes.md` | `cookbook-compatibility.md` |
