# Authoritative Source Rule / 权威数据源与来源引用

## 1. 唯一权威：interface_sdk-js

**公共接口定义以 `interface_sdk-js` 为唯一权威**：https://gitcode.com/openharmony/interface_sdk-js （`api/` 下 `.d.ts` / `.static.d.ets`）。渲染文档（含 `@since`/单位/废弃）：`docs.openharmony.cn` 与 gitee `openharmony/docs` 的 `zh-cn/application-dev/reference/apis-arkui/arkui-ts/*.md`。

> ace_engine 内部 `.d.ts` / C++（`frameworks/.../index.d.ts`、`interfaces/inner_api/ace_kit/...`）属于前端桥接或实现内部，**仅作实现对照，不得作公共能力、字段、行为或 availability 结论**。内部符号与公共接口不一致时，以锁定版本的 `interface_sdk-js` 为准；无法消解则记录冲突并标 `待核`。

## 2. 取数命令（按可用性）
1. `oh-gc search code "<符号>"`（gitcode 仓库内检索；端点偶尔不可用→兜底）。
2. 工作目录可写时，检出锁定分支到任务缓存目录，不要写入用户项目：

   ```powershell
   git clone --depth 1 --branch <LOCKED_BRANCH> https://gitcode.com/openharmony/interface_sdk-js.git <TASK_CACHE>/interface_sdk-js
   git -C <TASK_CACHE>/interface_sdk-js rev-parse HEAD
   rg -n "<SYMBOL>|<RELATED_TYPE>" <TASK_CACHE>/interface_sdk-js/api
   ```

3. 无法检出时使用 gitcode / gitee raw `.d.ts`；记录完整 URL、分支和响应状态。
4. 再兜底到 `docs.openharmony.cn` / gitee docs raw（含 `@since`/单位/废弃）。

命中入口符号后，继续检索其参数、返回值和继承链引用的公共类型。例如事件接口继续追踪 event/object/history 类型，组件继续追踪 item/group/controller/options，不能只摘入口签名。

## 3. 平台版本基线（必须锁定并记录）

每次分析在 Initial Checks 锁定并**显式记录**以下基线，禁止混用未发布 ArkUI API 与不同平台版本：

| 平台 | 记录项 |
|---|---|
| ArkUI | API/SDK Version 或分支（如 API 12 / master）；查询日期 |
| Android | API Level + Jetpack Compose 版本（如 API 34 / Compose BOM 2024.x） |
| iOS/iPadOS | 系统版本（如 iOS 17）；查询日期 |

## 4. 来源引用格式（每项实质性断言必须可追溯）

规格速览 / 能力矩阵 / 关键差异 / 迁移结论中，**每项实质性断言**关联 `Source ID`（`S1`、`S2`…），并在附录来源表中记录。Fact 与 Claim 的推荐显示语法为 `[A-01][S1]`、`[CL-01][S1][S2]`。来源表字段只以 `evidence-ledger.md` 的 canonical Source Record 为准；本文件补充以下取值要求：

| 列 | 说明 |
|---|---|
| Source ID | `S1`、`S2`…；同一交付内唯一 |
| 平台 | ArkUI / Android / iOS |
| API 或符号 | 如 `List.cachedCount`、`LazyColumn`、`UITableViewDataSource` |
| 证据类型 | 使用 `evidence-ledger.md` 的 `API Reference`、`Guide`、`Sample`、`Source` 或 `Discovery` |
| 证据等级 | 按证据类型填写 E1、E2、E3、E4 或 E5 |
| 来源 | 官方文档 URL 或仓库文件路径（含 `file:line`） |
| 目标版本 / availability | `@since` / API Level / iOS availability |
| 查询日期 | YYYY-MM-DD |
| 章节 | 文档章节或锚点 |
| Applies to | 该来源实际支撑的一个或多个 Capability ID |

规则：
- 分析推论只进入 Claim Ledger，并关联支撑它的 Fact/Source；不得把 `inference` 写入来源表的 Evidence type。
- 只使用 `S<n>` 作为来源标识，不再混用数字 `[n]`；正文引用的每个 Source ID 都必须在同一交付的来源表定义。
- **缺失 / 独有 / 优于**类结论须列出**完成双向检索**的来源（即在两方平台都查过、确认存在/不存在）。
- 无充分来源支撑的断言标 **`待核`**，**不得进入确定性结论**。
- 先按 `evidence-ledger.md` 建立 Fact ID，再由 Fact ID 形成 Claim ID；不要只在附录放一组宽泛来源而不说明具体支撑关系。
- 仓库来源优先记录精确文件路径和行号；在线文档记录稳定 URL、章节和查询日期。

## 5. 冲突与回退

- `interface_sdk-js` 与渲染文档不一致时，先核对分支、API 版本和生成时间；无法消解则建立 Conflict Log 并标 `待核`。
- gitcode 检索不可用时，依次使用 raw `.d.ts`、gitee 官方镜像和 `docs.openharmony.cn`。
- 声称“官方源不可访问”前，至少记录一次仓库检出或 raw 请求的实际错误；只因搜索工具失败不能跳过 git clone/raw 回退。
- 只找到 ace_engine 内部定义时，不得据此补齐公共字段或 availability。

## 6. 领域事实动态取证

本 Skill 不内置某一 API 类别的字段速查表或固定事实样例。每次分析都应根据 Analysis Brief 锁定的版本，从 `interface_sdk-js` 和 Android/iOS 官方文档重新提取领域事实。报告结构以 `assets/report-template.md` 为准；eval 中的具体事实只用于锁定版本下的回归测试，不能替代正式取证。
