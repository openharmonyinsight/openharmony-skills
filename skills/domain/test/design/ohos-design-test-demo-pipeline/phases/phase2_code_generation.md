# 阶段 2：Demo 代码生成

## 输入
- `{输出目录}/demo_design.md`
- MCP工具（可选，由opencode自动提供；未配置时步骤3自动降级）

## 输出
- `{输出目录}/TestDemo/`（完整 ArkUI 项目目录）
- `{输出目录}/demo_code_manifest.md`（初稿，未包含编译验证结果）

> **注**：`{输出目录}/rag_demo_experience.json` 由编排器在阶段2 启动前写入（MCP 知识库查询缓存），是阶段2 的**输入**而非输出；流水线结束后由编排器统一清理（见 SKILL.md 阶段4「中间文件清理」）。

## 鸿蒙工程架构与 ArkTS 编码规范约束（强制执行）

> **本章节为所有代码生成的强制约束，生成任何文件前必须遵循。**
>
> 规范来源：
> - [OpenHarmony应用TS&JS编程指南（本地）](reference/OpenHarmony-Application-Typescript-JavaScript-coding-guide.md)
> - [构建第一个 HarmonyOS 应用（ArkTS）](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/start-with-ets-stage)
> - [工程目录结构](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-project-structure)
> - **工程模板**：`reference/template/`（已验证可编译的 HarmonyOS NEXT 标准工程，作为代码生成底座）

### 约束 1：目标平台与 API 版本

- **目标平台**：HarmonyOS NEXT（不含 Android 兼容层）
- **最低 API Version**：API 12（`compileSdkVersion` >= 12）
- **模型**：Stage 模型（禁止使用 FA 模型）
- **语言**：ArkTS（禁止使用 JS/TS 兼容写法）
- **UI 框架**：ArkUI 声明式开发范式

### 约束 2：工程目录结构与模板复制规则

**工程底座**：使用 `reference/template/` 作为基础工程，**先完整复制模板，再仅修改 `entry/src/main/` 下的源代码文件**。模板中的工程配置文件（构建脚本、包配置、Hvigor 配置、图标资源等）一律原样复制，不做任何修改。

```
TestDemo/
├── AppScope/                                    [模板复制] 整个目录
│   ├── app.json5
│   └── resources/base/element/string.json
├── entry/
│   ├── src/main/
│   │   ├── ets/
│   │   │   ├── entryability/
│   │   │   │   └── EntryAbility.ets           [模板复制] 不修改
│   │   │   ├── entrybackupability/
│   │   │   │   └── EntryBackupAbility.ets     [模板复制] 不修改
│   │   │   ├── common/                         [新增目录]
│   │   │   │   ├── Constants.ets              [生成] 控件 ID 常量
│   │   │   │   ├── Logger.ets                 [生成] 日志工具
│   │   │   │   └── ResultDisplay.ets          [生成] 结果展示组件
│   │   │   ├── model/                          [新增目录]
│   │   │   │   └── TestPoint.ets              [生成] 数据模型
│   │   │   └── pages/
│   │   │       ├── Index.ets                  [替换] 覆盖模板的 Hello World
│   │   │       ├── Page001.ets                [新增] 模块页 1
│   │   │       └── ...                        [新增] 按页面规划生成
│   │       ├── resources/
│   │       │   ├── base/
│   │       │   │   ├── element/
│   │       │   │   │   ├── color.json         [修改] 追加 PASS/FAIL/WAITING 颜色
│   │       │   │   │   ├── string.json        [修改] 追加页面标题等字符串
│   │       │   │   │   └── float.json         [模板复制] 不修改
│   │       │   │   ├── media/                  [模板复制] 整个目录（图标/启动图）
│   │       │   │   └── profile/
│   │       │   │       ├── main_pages.json    [修改] 追加页面路由
│   │       │   │       └── backup_config.json [模板复制] 不修改
│   │       │   └── dark/element/color.json    [模板复制] 不修改
│   │       └── module.json5                    [修改] 仅追加 requestPermissions
│   ├── build-profile.json5                     [模板复制] 不修改
│   ├── hvigorfile.ts                           [模板复制] 不修改
│   ├── obfuscation-rules.txt                   [模板复制] 不修改
│   └── oh-package.json5                        [模板复制] 不修改
├── build-profile.json5                          [模板复制] 不修改
├── hvigorfile.ts                                [模板复制] 不修改
├── oh-package.json5                             [模板复制] 不修改
├── code-linter.json5                            [模板复制] 不修改
├── local.properties                             [模板复制] 不修改
└── hvigor/
    └── hvigor-config.json5                      [模板复制] 不修改
```

**强制规则：**
- `[模板复制]` → 原样复制，**禁止修改**
- `[修改]` → 先复制模板版本，再**增量修改**
- `[生成]`/`[新增]`/`[替换]` → 根据设计文档生成

### 约束 3：ArkTS 命名规范

| 标识符类型 | 命名风格 | 示例 |
|-----------|---------|------|
| 类名、枚举名、命名空间名 | UpperCamelCase | `ControlIds`, `LogEntry`, `Logger` |
| 变量名、方法名、参数名 | lowerCamelCase | `resultText`, `executeApi()`, `pageId` |
| 常量名、枚举值名 | UPPER_SNAKE_CASE | `BTN_001_EXECUTE`, `MAX_USER_SIZE` |
| 布尔变量/方法 | is/has/can/should 前缀 | `isError`, `hasResult`, `isEmpty()` |
| 自定义组件名 | UpperCamelCase | `ResultDisplay`, `TestPage` |
| 文件名 | PascalCase.ets | `EntryAbility.ets`, `Constants.ets` |
| 页面文件名 | PascalCase.ets | `Index.ets`, `Page001.ets` |

**禁止事项：**
- 禁止使用单个字母或非标准缩写命名
- 禁止使用中文拼音命名
- 禁止使用否定形式的布尔变量名（如 `isNotError`）

### 约束 4：ArkTS 代码格式规范

- **缩进**：使用 2 个空格缩进，禁止使用 Tab 字符；换行缩进使用 4 个空格
- **行宽**：每行不超过 120 个字符
- **引号**：字符串统一使用单引号 `'`
- **大括号**：左大括号 `{` 与语句在同一行
- **空格**：`if`/`for`/`while`/`switch` 与 `(` 之间加空格；函数名与 `(` 不加；二元操作符前后加；逗号后加
- **变量声明**：每个语句只声明一个变量
- **条件语句**：`if`/`for`/`while`/`do` 的执行体必须使用 `{}`
- **对象字面量**：属性超过 4 个时，每个属性独占一行

### 约束 5：ArkTS 类型安全规范

- **禁止使用 `any` 类型**
- **禁止使用 `ESObject`**
- **数组类型**：统一使用 `T[]`，禁止 `Array<T>`
- **空值安全**：可能为空的值必须使用 `?.` 或 `??`
- **类型导入**：使用 `import type` 导入纯类型
- **NaN 判断**：必须使用 `Number.isNaN()`

### 约束 6：状态管理规范

**方案 A（推荐）：V2 状态管理（API 12+）**

```typescript
@ComponentV2
struct PageXXX {
  @Local inputValue1: string = ''
  @Local resultText: string = ''
  @Local statusText: string = 'WAITING'
  build() { /* ... */ }
}
```

| V2 装饰器 | 用途 | 替代的 V1 装饰器 |
|-----------|------|-----------------|
| `@ComponentV2` | 声明 V2 版本组件 | `@Component` |
| `@Local` | 组件内本地状态 | `@State` |
| `@ObservedV2` | 赋予 class 深度观测能力 | `@Observed` |
| `@Trace` | 属性级变化追踪 | — |

**方案 B（兼容）：V1 状态管理** — 适用于简单场景或需兼容旧版本。

**选择原则**：默认使用方案 A（V2），除非设计文档明确要求兼容低版本。V1/V2 装饰器不可在同一组件上混用。

### 约束 7：组件编写规范

- 每个页面必须包含 `@Entry` + `@ComponentV2`（或 `@Component`）装饰器
- 每个组件必须包含 `build()` 方法
- 所有状态变量必须有类型声明和初始值
- 类属性建议添加 `private`/`public` 修饰符

### 约束 8：API 使用规范

- 页面路由使用 `router.pushUrl()`；推荐 `Navigation` 组件
- 优先使用 ArkUI 基础组件（Column、Row、Text、Button、TextInput、List、Scroll、Grid）
- 禁止实验性 API
- 所有异步 API 调用必须 `try-catch` 包裹
- 数组遍历优先 `forEach`/`map`/`filter`
- 资源引用使用 `$r('app.string.xxx')` / `$r('app.color.xxx')`

### 约束 9：工程配置文件与模板文件

所有标注 `[模板复制]` 的文件一律从 `reference/template/` 原样复制，禁止修改。完整清单见约束2目录树中标注 `[模板复制]` 的条目。

### 约束 10：EntryAbility 与 EntryBackupAbility

从模板原样复制，禁止修改。

---

## 执行步骤

1. 读取 demo_design.md，提取页面规划、控件清单（含不重复的控件类型列表，供步骤2第一轮专项查询使用）、映射表、API 清单、系统能力清单
2. **读取 API 参考文件（按映射读取，禁止 grep 全量搜索）**

    **【禁止】使用 Grep/Glob 搜索 api-reference 目录下的所有 .json 文件。阶段1已在 demo_design.md 中建立了 `{API名称 → JSON文件名}` 映射，必须直接使用该映射。**

    **步骤 2a**：从 demo_design.md 的 API 清单表中提取所有 `{API名称 → JSON文件名}` 映射
    - 例如：`domStorageAccess → attributes-component-web.json`，`WebCookie → WebCookie.json`

    **步骤 2b**：对每个映射到的 JSON 文件，使用 Read 工具读取该文件（仅读取映射涉及的文件，不遍历目录）
    - 读取以下字段：
       - `importPath` — 正确的 import 路径
       - `methods[].name` — 方法名
       - `methods[].signature` — 方法签名
       - `methods[].params` — 参数列表
       - `methods[].description` — 方法描述
       - `methods[].examples` — **ArkUI 示例代码**（必须参考，API 用法的权威来源）
       - `methods[].htmlExamples` — HTML 示例代码
       - `syscap` — 系统能力
    - 示例代码片段格式：`// xxx.ets\n import { webview } from '@kit.ArkWeb';\n\n @Entry\n ...`
    - 用于后续代码生成时参考 `examples` 中的 ArkUI 代码模式
     - **完整模式下 api-reference 的 examples 是 API 用法的权威来源，必须严格遵循**；MCP 知识库（步骤3）提供基础组件、状态管理等通用模式的补充参考。降级模式无 examples，UI 控件生成参考编码规范 + MCP（若可用），并标注 ⚠️

     **步骤 2c（仅完整模式）**：如果 demo_design.md 中某个 API 映射缺失（JSON文件列为空或"⚠️ 未验证"）且 `reference/api-reference/{领域}/index.json` 已安装，则回退到 index.json 查找：
     - Read `reference/api-reference/{领域}/index.json`
     - 在 `modules[].files[]` 中按 `name` 字段匹配该 API
     - 找到后 Read 对应的详情 JSON 文件
     - **降级模式（index.json 未安装）**：跳过本步骤，该 API 在代码中标注 `⚠️ 无 API 参考`，最佳努力生成，返回摘要写入 `api_reference=degraded`
3. **读取 MCP 查询结果（由编排器预先执行并写入文件）**

    **MCP 查询已由编排器在启动阶段2 Agent 前完成**，结果已写入 `{输出目录}/rag_demo_experience.json`。本步骤只需读取该文件，提取可用知识。

    **步骤 3a（读取结果文件）**：使用 Read 工具读取 `{输出目录}/rag_demo_experience.json`。
    - 文件内容为 `{"status": "MCP不可用，已跳过知识库查询"}` 或 `{"status": "MCP查询失败", ...}` → MCP 不可用，标记 `MCP可用=false`，跳到步骤 4
    - 文件包含分段查询结果 → MCP 可用，标记 `MCP可用=true`，继续步骤 3b

    **步骤 3b（提取第一轮：控件专项查询结果）**：
    - 从 rag_demo_experience.json 中提取所有 `"query": "ArkUI {组件名} 组件 ..."` 的分段
    - 每个分段的 `results.items[]` 包含该组件的用法、属性、事件和代码示例
    - **用途**：直接用于步骤 7 页面代码生成时对应控件类型的 UI 声明和交互逻辑编写

    **步骤 3c（提取第二轮：通用知识查询结果）**：
    - 从 rag_demo_experience.json 中提取非控件专项的分段（如 "装饰器用法 状态管理 页面跳转"）
    - **用途**：为状态管理、页面跳转、编码规范等提供通用模式参考

    **步骤 3d（降级处理）**：MCP 不可用时：
    - 后续步骤 7 的 UI 控件生成**仅参考 api-reference 的 examples 字段和阶段2编码规范约束**
    - 自检规则 6/11 中的 MCP 相关检查项**自动标记为"跳过（MCP不可用）"**，不计为失败项
    - 返回摘要中 MCP 查询结果标注为"未执行（环境无MCP）"
4. **复制模板工程**：根据当前操作系统选择复制命令，排除 `.hvigor/`、`.idea/`、`node_modules/`、`oh_modules/`、`build/`
   - **PowerShell（Windows）**：`Copy-Item -Path 'reference/template/*' -Destination '{输出目录}/TestDemo/' -Recurse -Force -Exclude '.hvigor','.idea','node_modules','oh_modules','build'`
   - **Bash（Linux/macOS）**：`cp -r reference/template/ {输出目录}/TestDemo/ && rm -rf {输出目录}/TestDemo/.hvigor {输出目录}/TestDemo/.idea {输出目录}/TestDemo/node_modules {输出目录}/TestDemo/oh_modules {输出目录}/TestDemo/build`
   - 使用 bash 工具执行时，根据 `process.platform` 判断系统：`win32` 用 PowerShell 命令，其他用 Bash 命令
5. 在复制的工程基础上，创建新增目录：`entry/src/main/ets/common/`、`entry/src/main/ets/model/`
6. 生成通用组件：Constants.ets、Logger.ets、ResultDisplay.ets、TestPoint.ets
7. 按页面顺序逐个生成 PageXXX.ets（严格遵循代码生成规则4的模块页面代码，**API 调用严格遵循 api-reference 的 examples**）
    - **UI 控件生成**：对页面中每个控件（如 Select、Button、TextInput），若 MCP 可用，**必须参考步骤3b提取的控件专项查询结果中的代码示例和属性/事件说明**来编写 UI 声明和交互逻辑；若 MCP 不可用，参考 api-reference 的 examples 字段、阶段2编码规范约束，并结合 ArkUI 声明式语法的通用写法自行推断控件属性与事件绑定
    - **状态管理/页面跳转等通用模式**：若 MCP 可用，参考步骤3c提取的通用知识查询结果；否则参考阶段2编码规范约束（约束5-8），并结合 ArkUI 通用开发模式自行推断
8. 生成 Index.ets（替换模板版本）
9. 增量修改配置和资源文件（module.json5、main_pages.json、color.json、string.json）
10. 执行自检清单（规则 0-11，强制执行），**自检通过后使用 Glob 验证以下3个输出均已落盘**：`{输出目录}/TestDemo/`、`{输出目录}/demo_code_manifest.md`、`{输出目录}/rag_demo_experience.json`。缺失则立即补写后再继续
11. 生成 demo_code_manifest.md（初稿，编译验证结果待阶段3补充）

## 代码生成规则

### 规则 1：Constants.ets — 控件 ID 常量

```typescript
export class ControlIds {
  // PAGE-001: [页面名称]
  static readonly BTN_001_EXECUTE: string = 'btn_001_execute'
  static readonly BTN_001_RESET: string = 'btn_001_reset'
  // ... 所有控件 ID

  static getAllIds(): string[] {
    return [ControlIds.BTN_001_EXECUTE, /* ... */]
  }
}
```

### 规则 2：Logger.ets — 日志工具

```typescript
export interface LogEntry {
  timestamp: string
  pageId: string
  controlId: string
  actionType: 'input' | 'click' | 'toggle' | 'result'
  value: string
}

export class Logger {
  private static entries: LogEntry[] = []
  static logAction(pageId: string, controlId: string, actionType: string, value: string): void
  static logResult(pageId: string, controlId: string, result: string): void
  static getLogEntries(): LogEntry[]
  static clearLog(): void
  static exportLog(): string
  static getEntryCount(): number
}
```

### 规则 3：ResultDisplay.ets — 结果展示组件

```typescript
@Component
export struct ResultDisplay {
  @Prop resultText: string = ''
  @Prop statusText: string = ''  // 'PASS' | 'FAIL' | 'WAITING'
  @Prop timestamp: string = ''
  controlId: string = ''

  build() {
    Column() {
      // 状态指示（PASS=绿色, FAIL=红色, WAITING=灰色）
      // 结果文本（可滚动）
      // 时间戳
      // 复制按钮
    }
    .id(this.controlId)
  }
}
```

### 规则 4：PageXXX.ets — 模块页面代码

每个页面严格遵循以下结构，并**必须**参考阶段2步骤2读取的 API JSON `examples` 字段中的 ArkUI 示例代码来生成代码：

```typescript
// 【必须】从 API JSON 的 importPath 字段获取正确的导入路径
import { ControlIds } from '../common/Constants'
import { Logger } from '../common/Logger'
import { ResultDisplay } from '../common/ResultDisplay'
// 【必须】使用 API JSON 中记录的 importPath
import { webview } from '@kit.ArkWeb'

@Entry
@Component
struct PageXXX {
  // === 状态声明 ===
  // 【必须】参考 API examples 中的状态变量声明方式
  controller: webview.WebviewController = new webview.WebviewController()
  @State inputValue1: string = '[默认值]'
  @State resultText: string = ''
  @State statusText: string = 'WAITING'
  @State logEntries: LogEntry[] = []

  // 【必须】参考 API JSON examples 中的 ArkUI 示例代码
  // 不得随意编写未在示例中出现的 API 调用方式
  private async executeApi(): Promise<void> {
    Logger.logAction('PAGE-XXX', ControlIds.BTN_XXX_EXECUTE, 'click', '')
    try {
      // 【禁止】使用 targetApi 或其他占位符
      // 【必须】参考 API examples 中的调用模式：
      // 示例：controller.insertText(this.inputValue1)
      this.controller.insertText(this.inputValue1)
      this.resultText = 'API call successful'
      this.statusText = 'PASS'
      Logger.logResult('PAGE-XXX', ControlIds.RESULT_XXX_01, this.resultText)
    } catch (error) {
      this.resultText = `Error: ${error.code} - ${error.message}`
      this.statusText = 'FAIL'
      Logger.logResult('PAGE-XXX', ControlIds.RESULT_XXX_01, this.resultText)
    }
  }

  // === 重置方法 ===
  private reset(): void {
    this.inputValue1 = '[默认值]'
    this.resultText = ''
    this.statusText = 'WAITING'
    Logger.logAction('PAGE-XXX', ControlIds.BTN_XXX_RESET, 'click', 'reset')
  }

  build() {
    Column() {
      Text('[页面标题]').fontSize(20).fontWeight(FontWeight.Bold)
      // 【强制】如果 API 是组件属性链（如 keyboardAppearance），必须在此处包含 Web 组件和 API 调用链
      // 示例：Web({ src: $rawfile('index.html'), controller: this.controller })
      //         .keyboardAppearance(this.selectedMode)
      Scroll() {
        Column({ space: 12 }) {
          // --- 输入区域 ---
          // [为每个参数生成 TextInput / Select / Toggle]
          // --- 操作区域 ---
          Row({ space: 12 }) {
            Button('执行').id(ControlIds.BTN_XXX_EXECUTE).onClick(() => this.executeApi())
            Button('重置').id(ControlIds.BTN_XXX_RESET).onClick(() => this.reset())
          }
          // --- 结果展示区域 ---
          ResultDisplay({ resultText: this.resultText, statusText: this.statusText, controlId: ControlIds.RESULT_XXX_01 })
          // --- 日志区域 ---
          List() { /* ForEach logEntries */ }.id(ControlIds.LOG_XXX).height(200)
        }
        .padding(16)
      }
    }
    .width('100%').height('100%')
  }
}
```

**【关键】API 调用链必须出现在 build() 方法中：**
- 如果 API JSON 的 `examples` 显示的是**组件属性链调用**（如 `Web(...).keyboardAppearance(mode)`），则生成的代码**必须在 build() 方法中包含该 Web 组件和属性链**，不能仅在 executeApi() 方法中处理
- executeApi() 方法仅用于执行业务逻辑判断和日志记录
- API 调用链（Web 组件 + 属性设置）必须在 build() 中作为 UI 的一部分存在

**【强制】API 调用代码生成规则（综合）：**
- import 语句使用 API JSON 中的 `importPath`
- 组件实例化、API 调用链必须与 `examples` 一致（禁止自行推断或修改参数名/类型/顺序/值）
- **组件属性链调用**（如 `Web(...).keyboardAppearance(mode)`）必须在 `build()` 方法中存在
- **禁止省略 examples 中显式传递的可选参数**
- **参数值必须使用 examples 中的字面量**（如 `WebKeyboardAppearanceMode.DARK_IMMERSIVE`）

### 规则 5：Index.ets — 首页导航

Grid 卡片导航，每卡片显示模块名 + 测试点数，点击 `router.pushUrl` 跳转。

### 规则 6：module.json5 — 增量添加权限

先复制模板，仅在 `module` 对象中追加 `requestPermissions` 数组。

### 规则 7：main_pages.json — 追加页面路由

在模板原有 `pages/Index` 基础上追加新页面路由。

### 规则 8：资源文件增量修改

- **color.json**：追加 `result_pass`/`result_fail`/`result_waiting` 颜色
- **string.json**：追加页面标题等字符串资源

### 规则 9：TestPoint.ets — 数据模型

```typescript
export interface TestPointMapping {
  testPointId: string
  description: string
  pageId: string
  controlIds: string[]
  actionType: string
  expectedResult: string
}

export interface PageConfig {
  pageId: string
  pageName: string
  route: string
  testPointCount: number
  testPoints: TestPointMapping[]
}
```

## 自检清单（强制执行，输出前逐条验证）

### 规则 0：模板文件完整性
- diff 对比模板文件，确保未被误修改
- 检查范围：所有标注 `[模板复制]` 的文件

### 规则 1：文件完整性
- 项目结构框架中要求的所有文件均已生成

### 规则 2：控件 ID 一致性
- Constants.ets 中控件 ID 与 demo_design.md 控件清单完全一致

### 规则 3：路由注册
- main_pages.json 路由与实际页面文件一一对应

### 规则 4：权限声明
- module.json5 的 requestPermissions 覆盖 demo_design.md 中所有权限

### 规则 5：id() 修饰符
- 每个可交互 UI 控件均有 `.id(ControlIds.XXX)` 修饰符

### 规则 6：API 调用验证（合并规则6/6.1/6.2/6.3）

对每个涉及 API 的页面，逐项验证：

- [ ] import 语句与 API JSON `importPath` 一致
- [ ] 组件实例化方式与 examples 一致
- [ ] API 调用链（如 `Web(...).keyboardAppearance(mode)`）必须在 `build()` 方法中存在
- [ ] 参数名、类型、顺序、值字面量与 examples 完全一致（禁止自行推断或省略可选参数）
- [ ] 如存在 `htmlExamples`，生成对应 HTML 到 `entry/src/main/resources/rawfile/`，Web 组件使用 `$rawfile()` 引用
- [ ] 如 API JSON 无 examples，在 manifest 中标注"⚠️ 无参考示例"
- [ ] **（MCP可用时强制）如有MCP知识库查询结果，检查是否参考了通用组件/状态管理等高相关性（score≥0.5）的知识片段**
- [ ] **（MCP可用时强制）检查页面中每个 UI 控件（Select/Button/TextInput等）的声明是否参考了 rag_demo_experience.json 中对应控件类型的查询结果代码示例**（特别是 Select 组件的 options、selected、onSelect 等属性和事件）

### 规则 7：错误处理
- 所有 API 调用均在 try-catch 块中

### 规则 8：日志记录
- 所有用户操作通过 Logger.logAction 记录
- 所有 API 结果通过 Logger.logResult 记录

### 规则 9：ArkUI 语法正确性
- 每个页面文件包含 `@Entry` 和 `@ComponentV2`（或 `@Component`）
- 每个组件包含 `build()` 方法
- 所有状态变量有类型声明和初始值

### 规则 9.1：ArkTS 编码规范合规性
- 无 `any` 类型、无 `Array<T>`、无 `ESObject`
- 命名遵循约束 3、格式遵循约束 4

### 规则 9.2：HarmonyOS NEXT 工程架构合规性
- 包含 `entrybackupability` 目录、`obfuscation-rules.txt`
- module.json5 使用 HarmonyOS NEXT 格式
- 目标 API Version >= 12

### 规则 10：导航功能
- Index.ets 包含所有模块页面的导航入口
- 每个导航项使用 `router.pushUrl` 跳转到正确路由

### 规则 11：MCP 知识库参考（MCP可用时强制，含控件专项查询）
- **`{输出目录}/rag_demo_experience.json` 文件已由编排器预先写入并落盘**（使用 Glob 验证文件存在）
- **（MCP可用时强制）控件专项查询**：生成代码中的 UI 控件声明与 rag_demo_experience.json 中对应控件类型的查询结果示例一致
- **（MCP可用时强制）通用知识查询**：高相关性条目（score≥0.5）已作为通用组件/状态管理/编码规范的补充参考
- **MCP不可用时的降级处理**：rag_demo_experience.json 已由编排器写入 `{"status": "MCP不可用"}` 或 `{"status": "MCP查询失败"}`，自检项标记为"跳过"，不计为失败
- **注意**：MCP 知识库提供通用开发知识和组件用法，API 调用细节始终以 api-reference 的 examples 为准

## 确认机制

**协调器调用**：完成后返回摘要，跳过确认。
**独立调用**：完成后显示摘要（源文件数/控件ID数/权限数），使用 AskUserQuestion 询问用户确认。
- **确认完成** → 进入下一阶段
- **输入优化建议** → 增量修正、重新自检、更新 manifest、再次确认，循环直到确认完成

## 返回摘要格式
 	 
完成后请返回以下摘要信息：
- Demo 页面数：X 个
- 源文件数：X 个
- 控件 ID 数：X 个
- 权限声明项数：X 项
- **MCP知识库查询**：通用开发知识 X 条（基础组件/应用模型/编码规范/工程架构/状态管理），已写入 rag_demo_experience.json（MCP不可用时返回"未执行（环境无MCP）"）
- 自检结果：X/X 项通过
