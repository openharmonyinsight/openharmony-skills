# Authoritative Source Rule / 权威数据源与来源引用

## 1. 唯一权威：interface_sdk-js

**公共接口定义以 `interface_sdk-js` 为唯一权威**：https://gitcode.com/openharmony/interface_sdk-js （`api/` 下 `.d.ts` / `.static.d.ets`）。渲染文档（含 `@since`/单位/废弃）：`docs.openharmony.cn` 与 gitee `openharmony/docs` 的 `zh-cn/application-dev/reference/apis-arkui/arkui-ts/*.md`。

> ace_engine 内部 `.d.ts` / C++（`frameworks/.../index.d.ts`、`interfaces/inner_api/ace_kit/...`）是前端桥接/实现内部，**仅作实现对照，不得作公共能力结论**。实测反例：触摸坐标单位是 **vp**（非内部常见的 px）；`screenX/Y` 自 API 10 **废弃**；公共压力字段叫 **`pressure`**（非内部 `force`）；`sourceTool`/`tiltX` 在**事件级** BaseEvent（非触点级）；左右手是 **`hand`**（非 `operatingHand`）。

## 2. 取数命令（按可用性）
1. `oh-gc search code "<符号>"`（gitcode 仓库内检索；端点偶尔不可用→兜底）。
2. gitcode / gitee raw `.d.ts`。
3. 兜底：`docs.openharmony.cn` / gitee docs raw（含 `@since`/单位/废弃）。

## 3. 平台版本基线（必须锁定并记录）

每次分析在 Initial Checks 锁定并**显式记录**以下基线，禁止混用未发布 ArkUI API 与不同平台版本：

| 平台 | 记录项 |
|---|---|
| ArkUI | API/SDK Version 或分支（如 API 12 / master）；查询日期 |
| Android | API Level + Jetpack Compose 版本（如 API 34 / Compose BOM 2024.x） |
| iOS/iPadOS | 系统版本（如 iOS 17）；查询日期 |

## 4. 来源引用格式（每项实质性断言必须可追溯）

规格速览 / 能力矩阵 / 关键差异 / 迁移结论中，**每项实质性断言**关联来源编号 `[n]`，并在附录来源表中记录：

| 列 | 说明 |
|---|---|
| 编号 | `[1]`、`[2]`… |
| 平台 | ArkUI / Android / iOS |
| API 或符号 | 如 `TouchEvent`、`MotionEvent.getActionMasked`、`UIEvent.coalescedTouches` |
| 证据类型 | 官方直接证据 / 分析推论 |
| 来源 | 官方文档 URL 或仓库文件路径（含 `file:line`） |
| 目标版本 / availability | `@since` / API Level / iOS availability |
| 查询日期 | YYYY-MM-DD |
| 章节 | 文档章节或锚点 |

规则：
- **区分官方证据 vs 推论**：推论须注明依据。
- **缺失 / 独有 / 优于**类结论须列出**完成双向检索**的来源（即在两方平台都查过、确认存在/不存在）。
- 无充分来源支撑的断言标 **`待核`**，**不得进入确定性结论**。

## 5. 触摸/指针专项规格（按需）
ArkUI onTouch 的逐字段校准规格已移至 `input-event-spec.md`，**仅在分析触摸/指针输入时按需加载**，避免其固定字段（单位/触点归属）污染通用流程与其它领域。
