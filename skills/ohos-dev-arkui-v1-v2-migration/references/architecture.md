# V1→V2 状态管理迁移 Skill 架构与工作流程

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    SKILL.md (AI 驱动)                      │
│                                                          │
│  Phase 0 确认目标 → Phase 1 分析 → Phase 2 规划           │
│  → Phase 3 执行改写 → Phase 4 验证                        │
│                                                          │
│  Claude 负责：决策、改写代码、向用户确认                     │
└──────────┬──────────┬──────────┬──────────┬──────────────┘
           │          │          │          │
           ▼          ▼          ▼          ▼
  ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐
  │ component  │ │dependency│ │  api_ver  │ │   mixing      │
  │ _analyzer  │ │ _tracer  │ │ _checker  │ │  _validator   │
  │            │ │          │ │           │ │               │
  │ 组件结构    │ │ 依赖链    │ │ API版本   │ │ V1/V2混用     │
  │ 状态变量    │ │ 传递类型  │ │ 混用规则  │ │ 合规校验      │
  │ API调用    │ │ must迁移  │ │ strict/   │ │ violations   │
  │ key追踪    │ │          │ │ relaxed   │ │ warnings     │
  └─────┬──────┘ └────┬─────┘ └───────────┘ └──────┬───────┘
        │              │                         │
        └──────────────┴─────────────────────────┘
                        │
                  只读分析，不修改任何文件
```

**设计原则**：Python 脚本负责「分析」（结构化数据提取、规则校验），Claude 负责「决策和改写」。脚本输出 JSON，Claude 读取后结合 `references/` 文档指导用户完成迁移。

---

## 二、Skill 五阶段工作流与脚本调用关系

### Phase 0：确认迁移目标

```
用户输入工程路径（无指定组件）
         │
         ▼
python3 component_analyzer.py <工程路径> --scan-v1
         │
         ▼
输出 JSON:
{
  "v1Components": [...],        // 所有 V1 组件列表
  "stateApiCalls": [...],       // 所有状态管理 API 调用
  "stateApiByKey": {            // 按 key 分组的状态 API 分析
    "PropA": {
      "decoratorUsage": [...],  // 哪些 V1 组件通过装饰器使用该 key
      "apiCalls": [...],        // 该 key 的所有 API 调用（标注文件类型）
      "v1CallsSafeToRemove": false,
      "removableV1Calls": []
    }
  },
  "instruction": "请先向用户确认要迁移以上哪个组件..."
}
         │
         ▼
Claude 将 V1 组件列表展示给用户，等待用户指定组件名
```

### Phase 1：分析（4个脚本依次运行）

```
Step 1.1  API 版本检测
──────────────────────
python3 api_version_checker.py <项目目录> --json

输出:
{
  "compatibleApiVersion": 12,
  "apiLevel": "pre19",           // or "post19"
  "mixingRules": "strict",       // or "relaxed"
  "availableApis": []            // API>=19 时有 enableV2Compatibility 等
}

决策点:
  strict → 复杂类型不能跨 V1/V2，需桥接模式
  relaxed → 可用 UIUtils.enableV2Compatibility()


Step 1.2  目标组件分析
──────────────────────
python3 component_analyzer.py <目标文件或目录> --json

输出:
{
  "file": "xxx.ets",
  "fileType": "ets",
  "components": [{
    "name": "MyComp",
    "version": "V1",
    "stateVariables": [...],
    "usedComponents": ["ChildA", "ChildB"],
    "rendering": { "hasForEach": true, ... },
    "appState": { "hasAppStorage": true, ... },
    "storageKeyTraces": [...]       // Storage key → API 调用追踪
  }],
  "classes": [...],
  "stateApiCalls": [...]
}


Step 1.3  依赖链追踪
──────────────────────
python3 dependency_tracer.py <组件名> <项目目录> --json

输出:
{
  "targetComponent": "MyComp",
  "migrationScope": {
    "mustMigrate": ["MyComp", "ChildA"],
    "reasons": {
      "MyComp->ChildA": "val: state_variable_ref (this.data)"
    }
  },
  "dependencyGraph": { ... }
}

决策点:
  mustMigrate 只有 1 个 → 可独立迁移
  mustMigrate 有多个 → 联合迁移或桥接模式


Step 1.4  混用校验（迁移前）
──────────────────────
python3 mixing_validator.py <项目目录> --json

输出:
{
  "violations": [...],    // 编译/运行时会出错的混用问题
  "warnings": [...],      // 可能存在风险的场景
  "suggestions": [...],   // 可用的兼容性 API 建议
  "summary": { "isCompliant": false }
}
```

### Phase 2：规划

Claude 综合以上 4 个脚本的输出，向用户报告迁移范围和策略：
- **独立迁移**：目标组件无外部数据交互
- **联合迁移**：目标与父/子组件有复杂类型传递
- **桥接模式**：API < 19 时 V1 传 @Observed class 给 V2

### Phase 3：执行迁移

Claude 按照 `references/` 文档中的规则逐步改写代码。不调用 Python 脚本，纯 AI 改写。

### Phase 4：验证

```
python3 mixing_validator.py <项目目录> --json --target <组件名>
         │
         ▼
确认 summary.isCompliant == true
逐项检查清单（组件装饰器、状态变量、渲染控制、应用级状态...）
```

---

## 三、Python 脚本处理流程详解

### 3.1 component_analyzer.py — 组件结构与状态 API 分析

**职责**：扫描 `.ets`/`.ts` 文件，提取组件结构、状态变量、状态管理 API 调用，并进行 Storage key 跨文件追踪。

#### 处理流程

```
输入: 文件路径或目录路径
      │
      ▼
 ┌─────────────────────────────────────┐
 │  文件遍历                            │
 │  analyze_directory()                 │
 │  ├─ glob("**/*.ets", "**/*.ts")      │
 │  ├─ 跳过 .d.ts 声明文件              │
 │  └─ 对每个文件调用 analyze_file()    │
 └─────────────┬───────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────┐
 │  单文件分析                          │
 │  analyze_file(filepath)             │
 │  ├─ extract_components()            │  ← 提取组件结构
 │  ├─ extract_classes()               │  ← 提取 @Observed 类
 │  ├─ extract_state_api_calls()       │  ← 扫描状态管理 API
 │  └─ 返回 {components, classes,      │
 │           stateApiCalls, fileType}  │
 └─────────────┬───────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────┐
 │  跨文件追踪                          │
 │  trace_storage_keys(results)        │
 │  └─ 组件 @StorageLink('key')        │
 │     → 找出所有 AppStorage.xxx('key') │
 │     → 标注文件类型 (ts/ets)          │
 └─────────────┬───────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────┐
 │  按 key 分组（--scan-v1 模式）       │
 │  build_state_api_key_map(results)   │
 │  ├─ 收集每个 key 的                  │
 │  │   decoratorUsage (V1装饰器引用)   │
 │  │   apiCalls (API调用站点)          │
 │  ├─ 判断 v1CallsSafeToRemove:       │
 │  │   decoratorUsage 为空 → True     │
 │  │   (所有V1组件已迁移,可删V1 API)   │
 │  └─ 填充 removableV1Calls           │
 └─────────────────────────────────────┘
```

#### 核心函数详解

**`extract_components(content, filepath)`**
- 正则匹配 `@Component/@ComponentV2 ... struct XXX`
- 大括号匹配提取 struct body（`extract_brace_block`）
- 向前回溯 500 字符检测 `@Entry`、`@Reusable`
- 对 body 调用 `extract_state_variables`、`extract_child_components` 等

**`extract_state_variables(body)`**
- 逐行扫描，收集连续的装饰器行
- 解析 `decorator varName: Type = value` 声明
- 分类 primary decorator（V1/V2 状态装饰器）和 auxiliary decorators（@Watch 等）
- 对 `@StorageLink('PropA')` 等提取 key 参数

**`extract_state_api_calls(content, filepath)`** — 6 轮扫描

| 扫描轮次 | 目标 | 示例 |
|---------|------|------|
| 1 | V1 静态 API | `AppStorage.setOrCreate('key', val)` |
| 2 | V2 静态 API | `AppStorageV2.connect(Type, 'key', ...)` |
| 3 | LocalStorage 实例方法 | `myLS.setOrCreate('key', val)` |
| 4 | 构造函数 + getShared | `new LocalStorage({...})` |
| 5 | 批量属性方法 | `PersistentStorage.persistProps([...])` |
| 6 | 废弃 PascalCase API | `AppStorage.SetOrCreate(...)` |

每条记录包含：`class`、`method`、`key`、`line`、`raw`、`version`、`deprecated`

**`build_state_api_key_map(results)`** — 迁移决策的关键

```
遍历所有文件的 stateApiCalls 和 components
                │
                ▼
        按 key 分组
                │
   ┌────────────┼────────────┐
   ▼            ▼            ▼
decoratorUsage  apiCalls   安全判断
(V1装饰器)     (API调用)    │
   │            │           ▼
   │            │    v1CallsSafeToRemove
   │            │    ├─ decoratorUsage 非空 → False
   │            │    │  (V1组件仍在用，V1 API 不能删)
   │            │    └─ decoratorUsage 为空 → True
   │            │       (已全迁到V2，可清理V1 API)
   │            │
   │            └─ 每条标注 fileType (ts/ets)
   │               和 version (V1/V2)
   │
   └─ 记录 component、variable、decorator、file
```

#### V1/V2 API 覆盖范围

| API 类 | 类名 | 方法 |
|--------|------|------|
| V1 静态 | AppStorage | setOrCreate, set, get, link, setAndLink, prop, setAndProp, ref, setAndRef, has, delete, keys, clear, size |
| V1 静态 | PersistentStorage | persistProp, deleteProp, keys |
| V1 静态 | Environment | envProp, keys |
| V1 实例 | LocalStorage | setOrCreate, set, get, link, setAndLink, prop, setAndProp, ref, setAndRef, has, delete, keys, size, clear |
| V1 废弃 | AppStorage | Link, SetAndLink, Prop, SetAndProp, Has, Get, Set, SetOrCreate, Delete, Keys, Clear, IsMutable, Size |
| V1 废弃 | PersistentStorage | PersistProp, PersistProps, DeleteProp, Keys |
| V1 废弃 | Environment | EnvProp, EnvProps, Keys |
| V2 静态 | AppStorageV2 | connect, remove, keys |
| V2 静态 | PersistenceV2 | connect, globalConnect, save, notifyOnError |
| V2 静态 | UIUtils | makeObserved, enableV2Compatibility, makeV1Observed, applySync, flushUpdates, flushUIUpdates, getTarget, getLifecycle, canBeObserved, makeBinding, addMonitor, clearMonitor, getCustomComponentContext |

---

### 3.2 dependency_tracer.py — 组件依赖链追踪

**职责**：从目标组件出发，沿父子关系双向追踪数据流，确定必须联合迁移的组件范围。

#### 处理流程

```
输入: 目标组件名 + 项目目录
      │
      ▼
 ┌─────────────────────────────────────────┐
 │  1. 定位目标组件定义                      │
 │  find_component_definition()            │
 │  ├─ glob("**/*.ets") 逐文件扫描          │
 │  ├─ re_search_component() 快速预过滤     │
 │  │  (struct XXX 声明是否存在)            │
 │  └─ analyze_file() 提取完整组件信息       │
 └─────────────┬───────────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────────┐
 │  2. 判断是否需要追踪                      │
 │  hasInput=false && hasOutput=false       │
 │  → 无外部数据交互，独立迁移，跳过追踪      │
 │  hasInput || hasOutput                   │
 │  → 需要双向追踪                          │
 └─────────────┬───────────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────────┐
 │  3. DFS 递归追踪 (max_depth=5)           │
 │                                         │
 │  向下追踪 (direction='down'):            │
 │  ├─ 遍历 comp['usedComponents']          │
 │  ├─ analyze_state_passing(parent, child) │
 │  │  ├─ 正则提取 Child({ param: expr })   │
 │  │  └─ classify_passage_type(expr):      │
 │  │     ├─ two_way_binding  ($$/!!)       │
 │  │     ├─ state_variable_ref (this.xxx)  │
 │  │     ├─ new_instance      (new Xxx)    │
 │  │     ├─ callback          (() =>...)   │
 │  │     ├─ literal           (42/'str')   │
 │  │     ├─ function_call     (fn())       │
 │  │     └─ expression        (其他)       │
 │  ├─ passage 为 state_variable_ref        │
 │  │  或 two_way_binding → 加入 mustMigrate│
 │  └─ 递归进入子组件继续追踪                │
 │                                         │
 │  向上追踪 (direction='up'):              │
 │  ├─ find_component_usages() 找父组件     │
 │  │  └─ 哪些组件的 usedComponents 包含目标  │
 │  ├─ 同样 analyze_state_passing 分析      │
 │  └─ 递归进入父组件继续追踪                │
 │                                         │
 │  循环检测: visited set 记录已访问组件      │
 └─────────────┬───────────────────────────┘
               │
               ▼
 输出:
 {
   "migrationScope": {
     "mustMigrate": ["CompA", "CompB", "CompC"],
     "reasons": {
       "CompA->CompB": "data: state_variable_ref (this.model)",
       "CompB->CompC": "val: two_way_binding ($$this.val)"
     }
   },
   "dependencyGraph": {
     "CompA": { "children": ["CompB"], "stateFlow": [...] }
   }
 }
```

**mustMigrate 判定规则**（满足任一即加入必须迁移列表）：
- `two_way_binding`（`$$` / `!!` / `$var`）：V2 无双向绑定等价物，双方必须一起改写；
- `state_variable_ref`（`this.xxx`，含嵌套 `this.x.y.z`）且**根变量**为**复杂类型**（`@Observed` class / Array / Map / Set / Date）：复杂类型不能跨 V1/V2 边界。嵌套访问按根变量（`this.<root>`）的类型判定。

**不构成强制依赖**（仅记入 `mayNeedMigration` 或忽略）：
- `state_variable_ref` 但根变量是**简单类型**（number / string / boolean）：可自由跨 V1/V2 → 记入 `mayNeedMigration`（可选）；
- `literal` / `callback` / `new_instance` / `function_call` / `expression`：忽略。

类型复杂度通过 `component_analyzer` 已计算的 `isSimpleType` / `isClassType` / `isBuiltinType` 判定；引用无法解析时保守地视为复杂类型（不漏报）。

---

### 3.3 api_version_checker.py — API 版本检测

**职责**：读取项目配置文件，确定 API 版本，输出混用规则类型（strict/relaxed）。

#### 处理流程

```
输入: 项目根目录
      │
      ▼
 ┌─────────────────────────────────────────┐
 │  1. 定位配置文件                          │
 │  find_config_files()                    │
 │  ├─ build-profile.json5 (项目根)         │
 │  ├─ AppScope/app.json5                  │
 │  └─ **/src/main/module.json5 (所有模块)  │
 └─────────────┬───────────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────────┐
 │  2. 解析 JSON5 文件                      │
 │  parse_json5()                          │
 │  ├─ strip_json5_comments()              │
 │  │  ├─ 去除 // 行注释                    │
 │  │  └─ 去除尾逗号                        │
 │  └─ json.loads()                        │
 └─────────────┬───────────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────────┐
 │  3. 提取 API 版本号                      │
 │                                         │
 │  build-profile.json5:                   │
 │    app.products[0].compatibleSdkVersion │
 │                                         │
 │  app.json5:                             │
 │    app.minAPIVersion                    │
 │                                         │
 │  module.json5:                          │
 │    module.minAPIVersion                 │
 │    module.distro.minAPIVersion (回退)    │
 │                                         │
 │  parse_api_version() 处理多种格式:        │
 │    24 / "24" / "6.1.1(24)" / "API 24"  │
 └─────────────┬───────────────────────────┘
               │
               ▼
 ┌─────────────────────────────────────────┐
 │  4. 取最低版本 + 判定规则                 │
 │                                         │
 │  compatibleApiVersion = min(             │
 │    build-profile, app, all_modules)     │
 │                                         │
 │  >= 19 → relaxed (enableV2Compatibility) │
 │  <  19 → strict  (桥接模式)              │
 └─────────────────────────────────────────┘
```

**关键阈值**：`API_VERSION_THRESHOLD = 19`。API 19 引入了 `UIUtils.enableV2Compatibility()` 和 `UIUtils.makeV1Observed()`，放宽了 V1/V2 之间的数据传递限制。

---

### 3.4 mixing_validator.py — V1/V2 混用合规校验

**职责**：检查项目中 V1/V2 组件间的数据传递是否符合混用规则，输出违规/警告/建议。

#### 处理流程

```
输入: 项目目录 [+ 可选目标组件名]
      │
      ▼
 ┌───────────────────────────────────────────────┐
 │  1. 获取 API 版本                              │
 │  detect_api_version() → api_level: pre19/post19│
 └─────────────┬─────────────────────────────────┘
               │
               ▼
 ┌───────────────────────────────────────────────┐
 │  2. 扫描所有组件                               │
 │  analyze_directory() → 组件列表 + 元数据        │
 │  构建 name→component 查找表                    │
 └─────────────┬─────────────────────────────────┘
               │
               ▼
 ┌───────────────────────────────────────────────┐
 │  3. 三轮校验                                   │
 │                                               │
 │  Pass 1: _check_cross_component_passing()     │
 │  ├─ 遍历所有 V1-V2 或 V2-V1 父子对             │
 │  ├─ 提取实参传递表达式                         │
 │  ├─ 按 API 版本应用方向性规则:                  │
 │  │                                            │
 │  │  V1→V2 (API<19, strict):                   │
 │  │  ├─ @Observed class → ERROR (需桥接)       │
 │  │  ├─ Array/Map/Set/Date → ERROR             │
 │  │  └─ 子组件非@Param接收 → ERROR              │
 │  │                                            │
 │  │  V1→V2 (API>=19, relaxed):                 │
 │  │  ├─ 复杂类型 → SUGGEST enableV2Compat     │
 │  │  └─ 内置类型 → SUGGEST makeV1Observed      │
 │  │                                            │
 │  │  V2→V1 (所有版本):                          │
 │  │  ├─ @Link 接收 → ERROR                     │
 │  │  ├─ @ObjectLink/@StorageLink 接收 → ERROR  │
 │  │  ├─ Array/Set/Map/Date (API<19) → ERROR    │
 │  │  └─ Function (API<19) → WARNING            │
 │  │                                            │
 │  │  双向绑定:                                   │
 │  │  └─ $$ / !! 跨 V1/V2 → ERROR               │
 │  │                                            │
 │  Pass 2: _check_bridge_pattern_need()         │
 │  └─ API<19 且 V1 传 class 给 V2 → 建议桥接    │
 │                                               │
 │  Pass 3: _check_multiple_decorators()         │
 │  └─ 同一变量多个主装饰器 → ERROR               │
 └─────────────┬─────────────────────────────────┘
               │
               ▼
 输出:
 {
   "violations": [{ "type": "...", "component": "...", "message": "..." }],
   "warnings": [...],
   "suggestions": [...],
   "summary": {
     "totalViolations": 0,
     "totalWarnings": 1,
     "isCompliant": true
   },
   "interactions": {
     "V1Parent(V1)->V2Child(V2)": { "direction": "V1->V2" }
   }
 }
```

---

## 四、脚本间数据流

```
                    ┌──────────────────┐
                    │ .ets / .ts 源文件 │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     component_analyzer   api_version    (源文件直接
     (组件/API/Key分析)   _checker       读取分析)
              │              │
              │              │
              ▼              │
     ┌────────────────┐     │
     │ analyze_file() │     │
     │ 返回:          │     │
     │  components    │     │
     │  classes       │     │
     │  stateApiCalls │     │
     └───┬────┬───────┘     │
         │    │             │
    ┌────┘    └──────┐      │
    ▼                ▼      ▼
dependency_      mixing_validator
tracer           ├─ 复用 component_analyzer
├─ import        │   的 analyze_file/analyze_directory
│  analyze_file  ├─ import api_version_checker
│  read_file     │   的 detect_api_version
│  等            └─ 输出 violations/warnings/suggestions
└─ DFS 追踪
   mustMigrate
```

**import 关系**：

```
dependency_tracer ──imports──→ component_analyzer
                              (analyze_file, read_file,
                               extract_components, V1_DECORATORS, ...)

mixing_validator ──imports──→ component_analyzer
                              (analyze_file, analyze_directory,
                               normalize_decorator, V1_DECORATORS, ...)

mixing_validator ──imports──→ api_version_checker
                              (detect_api_version)

api_version_checker ──→ 无外部依赖（独立运行）
```

---

## 五、Storage Key 追踪机制

这是迁移应用级状态的关键能力。以一个真实场景说明：

```
场景: 组件 MyComp 使用 @StorageLink('PropA'), 需要迁移

1. component_analyzer 扫描所有文件:
   - MyComp.ets:  @StorageLink('PropA') count: number
   - model.ts:    AppStorage.setOrCreate('PropA', 42)
   - service.ts:  AppStorage.get('PropA')
   - Other.ets:   @StorageProp('PropA') display: number

2. build_state_api_key_map 按 key='PropA' 分组:
   decoratorUsage: [
     { component: 'MyComp',  decorator: '@StorageLink' },   ← 要迁移
     { component: 'Other',   decorator: '@StorageProp' },    ← 未迁移
   ]
   apiCalls: [
     { class: 'AppStorage', method: 'setOrCreate', file: 'model.ts',  fileType: 'ts' },
     { class: 'AppStorage', method: 'get',         file: 'service.ts', fileType: 'ts' },
   ]
   v1CallsSafeToRemove: false    ← Other 还在用 @StorageProp
   removableV1Calls: []          ← 不能删 V1 API

3. 迁移 MyComp 时:
   - MyComp.ets: @StorageLink('PropA') → AppStorageV2.connect(CountStorage, 'PropA', ...)
   - model.ts:   新增 AppStorageV2.connect(...)   ← 只新增，不删 V1
   - service.ts: 不动（PropA 的 get 调用保留）

4. 迁移 Other 后再次扫描:
   decoratorUsage: []                          ← 无 V1 组件使用了
   v1CallsSafeToRemove: true
   removableV1Calls: [
     { class: 'AppStorage', method: 'setOrCreate', file: 'model.ts', line: 10 },
     { class: 'AppStorage', method: 'get',         file: 'service.ts', line: 5 },
   ]
   → 此时才可安全删除 V1 API 调用
```

---

## 七、完整示例：输入源码 → 脚本输出解析

以下使用 `examples/localstorage/` 真实示例，展示源码如何被各脚本解析。

### 7.1 输入源码（before.ets 节选）

```typescript
// === EntryAbility.ets — 初始化状态 ===
let storage: LocalStorage = LocalStorage.GetShared()

PersistentStorage.persistProp('fontSize', 16)         // ← V1 PersistentStorage API
PersistentStorage.persistProp('language', 'zh-CN')    // ← V1 PersistentStorage API
PersistentStorage.persistProp('notifications', true)  // ← V1 PersistentStorage API

AppStorage.setOrCreate('appThemeColor', '#4CAF50')    // ← V1 AppStorage API, key='appThemeColor'
AppStorage.setOrCreate('launchCount', 0)               // ← V1 AppStorage API, key='launchCount'

storage.setOrCreate('themeColor', '#4CAF50')           // ← LocalStorage 实例方法, key='themeColor'

// === MainPage — V1 组件，单向读取 ===
@Entry(localStorage)
@Component
struct MainPage {
  @LocalStorageProp('themeColor') localThemeColor: string = '#4CAF50'  // ← key='themeColor'
  @StorageProp('appThemeColor') globalThemeColor: string = '#4CAF50'   // ← key='appThemeColor'
  @StorageProp('launchCount') launchCount: number = 0                  // ← key='launchCount'
  @StorageProp('fontSize') fontSize: number = 16                       // ← key='fontSize'
  @StorageProp('language') language: string = 'zh-CN'                  // ← key='language'
  @State username: string = 'Alice'

  aboutToAppear() {
    let count = AppStorage.get<number>('launchCount') ?? 0             // ← V1 AppStorage API
    AppStorage.setOrCreate('launchCount', count + 1)                   // ← V1 AppStorage API
  }
}

// === SettingsPage — V1 组件，双向同步 ===
@Entry(settingsStorage)
@Component
struct SettingsPage {
  @LocalStorageLink('themeColor') localThemeColor: string = '#4CAF50'  // ← key='themeColor', 双向
  @StorageLink('appThemeColor') globalThemeColor: string = '#4CAF50'   // ← key='appThemeColor', 双向
  @StorageLink('fontSize') fontSize: number = 16                       // ← key='fontSize', 双向
  @StorageLink('language') language: string = 'zh-CN'                  // ← key='language', 双向
  @StorageLink('notifications') notifications: boolean = true          // ← key='notifications', 双向
}
```

### 7.2 Phase 0 输出：`component_analyzer.py --scan-v1`

```json
{
  "projectDir": "examples/localstorage",
  "totalV1Components": 2,
  "v1Components": [
    {
      "name": "MainPage",
      "file": "before.ets",
      "isEntry": true,
      "stateVariables": [
        "@LocalStorageProp localThemeColor: string",
        "@StorageProp globalThemeColor: string",
        "@StorageProp launchCount: number",
        "@StorageProp fontSize: number",
        "@StorageProp language: string",
        "@State username: string"
      ],
      "storageKeyTraces": [
        {
          "variable": "localThemeColor",
          "decorator": "@LocalStorageProp",
          "key": "themeColor",
          "decoratorFile": "before.ets",
          "decoratorFileType": "ets",
          "apiCalls": [
            {
              "class": "LocalStorage instance (storage)",
              "method": "setOrCreate",
              "key": "themeColor",
              "line": 25,
              "raw": "storage.setOrCreate('themeColor', '#4CAF50')",
              "file": "before.ets",
              "fileType": "ets",
              "version": "V1",
              "deprecated": false
            }
          ]
        }
      ]
    },
    {
      "name": "SettingsPage",
      "file": "before.ets",
      "isEntry": true,
      "stateVariables": [
        "@LocalStorageLink localThemeColor: string",
        "@StorageLink globalThemeColor: string",
        "@StorageLink fontSize: number",
        "@StorageLink language: string",
        "@StorageLink notifications: boolean"
      ],
      "storageKeyTraces": [
        {
          "variable": "localThemeColor",
          "decorator": "@LocalStorageLink",
          "key": "themeColor",
          "decoratorFile": "before.ets",
          "decoratorFileType": "ets",
          "apiCalls": [
            {
              "class": "LocalStorage instance (storage)",
              "method": "setOrCreate",
              "key": "themeColor",
              "line": 25,
              "raw": "storage.setOrCreate('themeColor', '#4CAF50')",
              "file": "before.ets",
              "fileType": "ets",
              "version": "V1",
              "deprecated": false
            }
          ]
        }
      ]
    }
  ],
  "stateApiCalls": [
    {
      "class": "AppStorage",
      "method": "setOrCreate",
      "key": "appThemeColor",
      "line": 21,
      "raw": "AppStorage.setOrCreate('appThemeColor', '#4CAF50')",
      "version": "V1",
      "file": "before.ets"
    },
    {
      "class": "AppStorage",
      "method": "setOrCreate",
      "key": "launchCount",
      "line": 22,
      "raw": "AppStorage.setOrCreate('launchCount', 0)",
      "version": "V1",
      "file": "before.ets"
    },
    {
      "class": "PersistentStorage",
      "method": "persistProp",
      "key": "fontSize",
      "line": 16,
      "raw": "PersistentStorage.persistProp('fontSize', 16)",
      "version": "V1",
      "file": "before.ets"
    },
    {
      "class": "LocalStorage",
      "method": "GetShared",
      "key": null,
      "line": 11,
      "raw": "LocalStorage.GetShared()",
      "version": "V1",
      "deprecated": true,
      "file": "before.ets"
    }
  ],
  "stateApiByKey": { ... },    // ← 详见下方 7.3 节
  "instruction": "请先向用户确认要迁移以上哪个组件，不得跳过此步骤。..."
}
```

**解析要点**：
- 两个 V1 组件，都有 `@Entry` 装饰器
- MainPage 用 `@StorageProp`（单向）和 `@LocalStorageProp`（单向）
- SettingsPage 用 `@StorageLink`（双向）和 `@LocalStorageLink`（双向）
- 同一个 key `appThemeColor` 被 `@StorageProp` 和 `@StorageLink` 同时使用
- 每个组件的 `storageKeyTraces` 直接关联了装饰器 key 与对应的 API 调用站点
- `stateApiCalls` 中 `LocalStorage.GetShared()` 标记了 `deprecated: true`

### 7.3 `stateApiByKey` 详解 — 按 key 分组的状态 API 分析

以 `appThemeColor` 和 `fontSize` 两个 key 为例：

#### key = `'appThemeColor'`

```json
{
  "appThemeColor": {
    "decoratorUsage": [
      {
        "component": "MainPage",
        "variable": "globalThemeColor",
        "decorator": "@StorageProp",        // MainPage 单向读取
        "file": "before.ets",
        "fileType": "ets"
      },
      {
        "component": "SettingsPage",
        "variable": "globalThemeColor",
        "decorator": "@StorageLink",        // SettingsPage 双向同步
        "file": "before.ets",
        "fileType": "ets"
      }
    ],
    "apiCalls": [
      {
        "class": "AppStorage",              // V1 静态 API
        "method": "setOrCreate",
        "file": "before.ets",
        "fileType": "ets",                  // 文件类型标记
        "line": 21,
        "raw": "AppStorage.setOrCreate('appThemeColor', '#4CAF50')",
        "version": "V1",
        "deprecated": false
      }
    ],
    "v1CallsSafeToRemove": false,           // ← 2个V1组件仍在用，不能删
    "removableV1Calls": []                  // ← 空列表
  }
}
```

**迁移决策**：
- `decoratorUsage` 有 2 条 → MainPage 和 SettingsPage 都在用 → `v1CallsSafeToRemove: false`
- 迁移 MainPage 时：只新增 `AppStorageV2.connect()`，**不删除** `AppStorage.setOrCreate('appThemeColor', ...)`
- 迁移 SettingsPage 后再次扫描 → `decoratorUsage` 变为空 → `v1CallsSafeToRemove: true` → 此时才可删除 V1 API

#### key = `'fontSize'`

```json
{
  "fontSize": {
    "decoratorUsage": [
      {
        "component": "MainPage",
        "variable": "fontSize",
        "decorator": "@StorageProp",
        "file": "before.ets",
        "fileType": "ets"
      },
      {
        "component": "SettingsPage",
        "variable": "fontSize",
        "decorator": "@StorageLink",
        "file": "before.ets",
        "fileType": "ets"
      }
    ],
    "apiCalls": [
      {
        "class": "PersistentStorage",       // 注意：是 PersistentStorage，不是 AppStorage
        "method": "persistProp",
        "file": "before.ets",
        "fileType": "ets",
        "line": 16,
        "raw": "PersistentStorage.persistProp('fontSize', 16)",
        "version": "V1",
        "deprecated": false
      }
    ],
    "v1CallsSafeToRemove": false,
    "removableV1Calls": []
  }
}
```

**迁移决策**：
- `PersistentStorage.persistProp` → V2 对应 `PersistenceV2.globalConnect()`
- 同样需要等两个组件都迁移后才能删除 `persistProp` 调用

#### key = `'appSettings'`（after.ets 中 V2 新增的 key）

```json
{
  "appSettings": {
    "decoratorUsage": [],                   // ← 无 V1 装饰器引用
    "apiCalls": [
      {
        "class": "AppStorageV2",            // V2 API
        "method": "connect",
        "file": "after.ets",
        "fileType": "ets",
        "line": 61,
        "raw": "AppStorageV2.connect(AppSettings, 'appSettings', ()",
        "version": "V2",                    // ← 标记为 V2
        "deprecated": false
      },
      {
        "class": "PersistenceV2",           // V2 API
        "method": "globalConnect",
        "file": "after.ets",
        "fileType": "ets",
        "line": 66,
        "raw": "PersistenceV2.globalConnect({ type: AppSettings, key: 'appSettings', ... })",
        "version": "V2",
        "deprecated": false
      }
    ],
    "v1CallsSafeToRemove": false,           // ← False 因为没有 V1 API 可删
    "removableV1Calls": []
  }
}
```

**解析**：这是一个纯 V2 的 key，没有 V1 装饰器引用，也没有 V1 API 调用。`v1CallsSafeToRemove` 为 `false` 是因为根本没有需要移除的 V1 调用。

### 7.4 Phase 1.2 输出：`component_analyzer.py --json`（单文件详细分析）

以 MainPage 组件为例：

```json
{
  "file": "before.ets",
  "fileType": "ets",
  "components": [
    {
      "name": "MainPage",
      "file": "before.ets",
      "version": "V1",
      "decorator": "@Component",
      "isEntry": true,
      "isReusable": false,
      "hasInput": false,
      "hasOutput": false,
      "stateVariables": [
        {
          "name": "localThemeColor",
          "decorator": "@LocalStorageProp",
          "decoratorArg": "themeColor",         // ← Storage key 参数
          "auxDecorators": [],
          "type": "string",
          "isSimpleType": true,
          "isBuiltinType": false,
          "isClassType": false,
          "hasDefaultValue": true,
          "hasExternalInit": false
        },
        {
          "name": "globalThemeColor",
          "decorator": "@StorageProp",
          "decoratorArg": "appThemeColor",       // ← Storage key 参数
          "auxDecorators": [],
          "type": "string",
          "isSimpleType": true,
          "isBuiltinType": false,
          "isClassType": false,
          "hasDefaultValue": true,
          "hasExternalInit": false
        },
        {
          "name": "username",
          "decorator": "@State",                 // ← 普通 @State，无 Storage key
          "decoratorArg": null,
          "auxDecorators": [],
          "type": "string",
          "isSimpleType": true,
          "isBuiltinType": false,
          "isClassType": false,
          "hasDefaultValue": true,
          "hasExternalInit": false
        }
      ],
      "inputs": [],
      "outputs": [],
      "usedComponents": [],                      // 无自定义子组件
      "rendering": {
        "hasForEach": false,
        "hasLazyForEach": false,
        "hasRepeat": false,
        "hasVirtualScroll": false
      },
      "appState": {
        "hasLocalStorage": true,                 // ← 检测到 LocalStorage 使用
        "hasAppStorage": true,                   // ← 检测到 AppStorage 使用
        "hasPersistentStorage": true,            // ← 检测到 PersistentStorage 使用
        "hasEnvironment": false,
        "hasAnimateTo": false
      },
      "storageKeyTraces": [
        {
          "variable": "launchCount",
          "decorator": "@StorageProp",
          "key": "launchCount",
          "decoratorFile": "before.ets",
          "decoratorFileType": "ets",
          "apiCalls": [
            {
              "class": "AppStorage",
              "method": "setOrCreate",
              "key": "launchCount",
              "line": 22,
              "raw": "AppStorage.setOrCreate('launchCount', 0)",
              "file": "before.ets",
              "fileType": "ets",
              "version": "V1",
              "deprecated": false
            },
            {
              "class": "AppStorage",
              "method": "setOrCreate",
              "key": "launchCount",
              "line": 53,
              "raw": "AppStorage.setOrCreate('launchCount', count + 1)",
              "file": "before.ets",
              "fileType": "ets",
              "version": "V1",
              "deprecated": false
            }
          ]
        }
      ]
    }
  ],
  "classes": [],
  "stateApiCalls": [
    {
      "class": "AppStorage",
      "method": "setOrCreate",
      "key": "appThemeColor",
      "line": 21,
      "raw": "AppStorage.setOrCreate('appThemeColor', '#4CAF50')",
      "version": "V1",
      "file": "before.ets"
    },
    {
      "class": "LocalStorage instance (storage)",    // ← 区分实例方法 vs 静态方法
      "method": "setOrCreate",
      "key": "themeColor",
      "line": 25,
      "raw": "storage.setOrCreate('themeColor', '#4CAF50')",
      "version": "V1",
      "file": "before.ets"
    },
    {
      "class": "LocalStorage",
      "method": "GetShared",
      "key": null,
      "line": 11,
      "raw": "LocalStorage.GetShared()",
      "version": "V1",
      "deprecated": true                            // ← 检测到废弃 API
    }
  ]
}
```

**解析要点**：

| 字段 | 含义 | 迁移影响 |
|------|------|---------|
| `decoratorArg: "themeColor"` | 该变量绑定的 Storage key | 迁移时需找到对应 key 的 V2 替代 |
| `auxDecorators: []` | 附加装饰器（如 @Watch） | 多装饰器场景需同时处理 |
| `hasDefaultValue: true` | 变量有默认值 | 影响迁移时是否需要 @Once |
| `storageKeyTraces[].apiCalls` | 该 key 对应的所有 API 调用点 | 迁移时需逐一处理 |
| `apiCalls[].fileType: "ets"` | 调用所在文件类型 | .ts 文件中的调用可能是 model/service 层 |
| `deprecated: true` | 废弃 API（如 `GetShared`） | 迁移时优先处理 |
| `hasLocalStorage: true` | 组件使用了 LocalStorage | 迁移到 V2 时需改为 @ObservedV2 单例 |

### 7.5 迁移过程中的状态变化演示

假设先迁移 MainPage，保留 SettingsPage 不动：

```
迁移前 (before.ets):
┌─────────────────────────────────────────────────────┐
│ MainPage    @StorageProp('appThemeColor')  ← V1     │
│ SettingsPage @StorageLink('appThemeColor') ← V1     │
│ AppStorage.setOrCreate('appThemeColor', ...)  ← V1 │
│                                                     │
│ stateApiByKey['appThemeColor']:                     │
│   decoratorUsage: [MainPage, SettingsPage]          │
│   v1CallsSafeToRemove: false  ← 不能删 V1 API      │
└─────────────────────────────────────────────────────┘

迁移 MainPage 后 (MainPage → V2):
┌─────────────────────────────────────────────────────┐
│ MainPage    AppStorageV2.connect(...'appThemeColor') ← V2 新增
│ SettingsPage @StorageLink('appThemeColor')           ← V1 保留
│ AppStorage.setOrCreate('appThemeColor', ...)         ← V1 保留
│                                                     │
│ stateApiByKey['appThemeColor']:                     │
│   decoratorUsage: [SettingsPage]           ← 减少到1 │
│   v1CallsSafeToRemove: false  ← SettingsPage 还在用 │
└─────────────────────────────────────────────────────┘

迁移 SettingsPage 后 (全部 → V2):
┌─────────────────────────────────────────────────────┐
│ MainPage    AppStorageV2.connect(...)        ← V2    │
│ SettingsPage PersistenceV2.globalConnect(...)← V2    │
│ AppStorage.setOrCreate('appThemeColor', ...) ← 可删  │
│                                                     │
│ stateApiByKey['appThemeColor']:                     │
│   decoratorUsage: []                       ← 清空   │
│   v1CallsSafeToRemove: true                ← 可以删  │
│   removableV1Calls: [                       ← 列出   │
│     AppStorage.setOrCreate line:21                   │
│   ]                                                  │
└─────────────────────────────────────────────────────┘
```

---

## 八、对比示例：独立组件 vs 有父子依赖的组件

### 例 A：独立组件（无输入输出，无依赖链）

#### A.1 源码

```typescript
// simple-component/before.ets

@Entry
@Component
struct CounterPage {                              // ← hasInput: false, hasOutput: true
  @State count: number = 0                       // ← 简单类型 @State
  @State message: string = 'Hello V1'
  @State step: number = 1

  build() {
    Column({ space: 10 }) {
      Text(this.message)
        .fontSize(24)
      Text(`Count: ${this.count}`)
      CountDisplay({ currentCount: this.count, step: this.step })  // ← 传递 this.xxx
      Row({ space: 10 }) {
        Button('Reset').onClick(() => { this.count = 0 })
        Button(`+${this.step}`).onClick(() => { this.count += this.step })
      }
    }
    .width('100%').height('100%')
  }
}

@Component
struct CountDisplay {                             // ← hasInput: true (@Prop)
  @Prop currentCount: number = 0
  @Prop step: number = 1

  build() {
    Column({ space: 5 }) {
      Text(`Current: ${this.currentCount}`)
      Text(`Step: ${this.step}`)
    }
  }
}
```

#### A.2 `component_analyzer.py --json` 输出

```json
[
  {
    "file": "before.ets",
    "fileType": "ets",
    "components": [
      {
        "name": "CounterPage",
        "file": "before.ets",
        "version": "V1",
        "decorator": "@Component",
        "isEntry": true,
        "isReusable": false,
        "hasInput": false,                      // ← 无外部输入
        "hasOutput": true,                      // ← hasOutput: 有 usedComponents
        "stateVariables": [
          { "name": "count",   "decorator": "@State", "decoratorArg": null, "auxDecorators": [],
            "type": "number", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false },
          { "name": "message", "decorator": "@State", "decoratorArg": null, "auxDecorators": [],
            "type": "string", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false },
          { "name": "step",    "decorator": "@State", "decoratorArg": null, "auxDecorators": [],
            "type": "number", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false }
        ],
        "inputs": [],
        "outputs": [],
        "usedComponents": ["CountDisplay"],     // ← 引用了子组件
        "rendering": { "hasForEach": false, "hasLazyForEach": false, "hasRepeat": false, "hasVirtualScroll": false },
        "appState": {                           // ← 无应用级状态
          "hasLocalStorage": false, "hasAppStorage": false,
          "hasPersistentStorage": false, "hasEnvironment": false, "hasAnimateTo": false
        }
      },
      {
        "name": "CountDisplay",
        "file": "before.ets",
        "version": "V1",
        "decorator": "@Component",
        "isEntry": false,
        "isReusable": false,
        "hasInput": true,                       // ← @Prop 算输入
        "hasOutput": false,
        "inputs": ["currentCount", "step"],     // ← 两个 @Prop 参数
        "outputs": [],
        "stateVariables": [
          { "name": "currentCount", "decorator": "@Prop", "decoratorArg": null, "auxDecorators": [],
            "type": "number", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false },
          { "name": "step",         "decorator": "@Prop", "decoratorArg": null, "auxDecorators": [],
            "type": "number", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false }
        ],
        "usedComponents": []
      }
    ],
    "classes": [],
    "stateApiCalls": []                         // ← 无状态管理 API 调用
  }
]
```

#### A.3 `dependency_tracer.py CounterPage <项目目录> --json` 输出

```json
{
  "targetComponent": "CounterPage",
  "projectDir": "examples/localstorage",
  "migrationScope": {
    "mustMigrate": [
      "CounterPage"                            // ← 只有自身
    ],
    "mayNeedMigration": [
      "CountDisplay"                           // ← 简单类型引用，可选（不强制联合迁移）
    ],
    "reasons": {},                              // ← 空的，无强依赖
    "components": {
      "CounterPage": {
        "name": "CounterPage",
        "file": "before.ets",
        "version": "V1",
        "hasInput": false,
        "hasOutput": true,
        "stateVariables": [...]
      }
    }
  },
  "dependencyGraph": {}                        // ← 空图
}
```

**解读**：
- CounterPage `hasInput=false`，传递给子组件的是简单类型（`this.count`、`this.step`）
- 简单类型的 `state_variable_ref` 不构成强制依赖（不需要联合迁移 CountDisplay），仅记入 `mayNeedMigration`
- 迁移策略：**独立迁移**，`@State → @Local`，直接替换

**迁移路径**：
```
CounterPage:
  @Component   → @ComponentV2
  @State count → @Local count
  @State step  → @Local step

CountDisplay（可暂不迁移）:
  @Prop → @Param（简单类型可跨 V1/V2 传递）
```

> **注意**：简单类型的 `state_variable_ref` 传递（如 `this.count`、`this.step`）
> 不构成强制联合迁移依赖。只有复杂类型（@Observed class）的传递才需要联合迁移。

---

### 例 B：有父子依赖的组件（@Link 双向绑定 → 必须联合迁移）

#### B.1 源码

```typescript
// component-with-props/before.ets

@Entry
@Component
struct SettingsPage {                              // ← hasInput: false, hasOutput: true
  @State username: string = 'Alice'
  @State fontSize: number = 16
  @Provide('themeColor') themeColor: string = '#4CAF50'
  @State showAdvanced: boolean = false

  build() {
    Column({ space: 15 }) {
      Text('Settings')
        .fontSize(24)
        .fontColor(this.themeColor)

      // $$ 双向绑定
      TextInput({ placeholder: 'Username', text: $$this.username })
        .width('80%')
        .fontSize(this.fontSize)

      Text(`Hello, ${this.username}`)
        .fontSize(this.fontSize)

      // @Link 双向同步 fontSize
      FontSizeAdjuster({ size: $fontSize })        // ← $fontSize = @Link 引用

      // @Consume 跨层级
      ThemeToggle()

      Button(this.showAdvanced ? 'Hide Advanced' : 'Show Advanced')
        .onClick(() => { this.showAdvanced = !this.showAdvanced })

      if (this.showAdvanced) {
        AdvancedSettings({ username: $username })   // ← $username = @Link 引用
      }
    }
    .width('100%').height('100%').padding(20)
  }
}

@Component
struct FontSizeAdjuster {                          // ← hasInput: true (@Link)
  @Link size: number                               // ← 双向绑定，修改会同步回父组件
  @Watch('onSizeChange') private prevSize: number = 0

  onSizeChange() { console.info(`FontSize changed to ${this.size}`) }

  build() {
    Row({ space: 10 }) {
      Button('-').onClick(() => { this.size = Math.max(12, this.size - 2) })
      Text(`${this.size}`).fontSize(16)
      Button('+').onClick(() => { this.size = Math.min(32, this.size + 2) })
    }
  }
}

@Component
struct ThemeToggle {
  @Consume('themeColor') themeColor: string        // ← 跨层级获取 @Provide

  build() {
    Row({ space: 10 }) {
      Text('Theme:').fontSize(16)
      Button('Green').onClick(() => { this.themeColor = '#4CAF50' })
      Button('Blue').onClick(() =>  { this.themeColor = '#2196F3' })
    }
  }
}

@Component
struct AdvancedSettings {                          // ← hasInput: true (@Link)
  @Link username: string                           // ← 双向绑定
  build() {
    Column({ space: 10 }) {
      Text('Advanced').fontSize(18)
      TextInput({ placeholder: 'Edit username', text: $$this.username })
        .width('80%')
    }
  }
}
```

#### B.2 `component_analyzer.py --json` 输出

```json
[
  {
    "file": "before.ets",
    "fileType": "ets",
    "components": [
      {
        "name": "SettingsPage",
        "file": "before.ets",
        "version": "V1",
        "decorator": "@Component",
        "isEntry": true,
        "isReusable": false,
        "hasInput": false,
        "hasOutput": true,                       // ← hasOutput: 有 usedComponents
        "inputs": [],
        "outputs": [],
        "stateVariables": [
          { "name": "username",     "decorator": "@State",   "decoratorArg": null, "auxDecorators": [],
            "type": "string",  "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false },
          { "name": "fontSize",     "decorator": "@State",   "decoratorArg": null, "auxDecorators": [],
            "type": "number",  "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false },
          { "name": "themeColor",   "decorator": "@Provide", "decoratorArg": "themeColor", "auxDecorators": [],
            "type": "string",  "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false },
          { "name": "showAdvanced", "decorator": "@State",   "decoratorArg": null, "auxDecorators": [],
            "type": "boolean", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false }
        ],
        "usedComponents": [
          "AdvancedSettings",                    // ← 3 个子组件
          "FontSizeAdjuster",
          "ThemeToggle"
        ],
        "rendering": { "hasForEach": false, "hasLazyForEach": false, "hasRepeat": false, "hasVirtualScroll": false },
        "appState": {
          "hasLocalStorage": false, "hasAppStorage": false,
          "hasPersistentStorage": false, "hasEnvironment": false, "hasAnimateTo": false
        }
      },
      {
        "name": "FontSizeAdjuster",
        "file": "before.ets",
        "version": "V1",
        "decorator": "@Component",
        "isEntry": false,
        "isReusable": false,
        "hasInput": true,                        // ← @Link 算输入
        "hasOutput": false,
        "inputs": ["size"],
        "outputs": [],
        "stateVariables": [
          { "name": "size",     "decorator": "@Link",  "decoratorArg": null, "auxDecorators": [],
            "type": "number", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": false, "hasExternalInit": false },
          { "name": "prevSize", "decorator": "@Watch", "decoratorArg": "onSizeChange", "auxDecorators": [],
            "type": "number", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": true, "hasExternalInit": false }
        ],
        "usedComponents": []
      },
      {
        "name": "ThemeToggle",
        "file": "before.ets",
        "version": "V1",
        "decorator": "@Component",
        "isEntry": false,
        "isReusable": false,
        "hasInput": false,
        "hasOutput": false,
        "stateVariables": [
          { "name": "themeColor", "decorator": "@Consume", "decoratorArg": "themeColor", "auxDecorators": [],
            "type": "string", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": false, "hasExternalInit": false }
        ],
        "usedComponents": []
      },
      {
        "name": "AdvancedSettings",
        "file": "before.ets",
        "version": "V1",
        "decorator": "@Component",
        "isEntry": false,
        "isReusable": false,
        "hasInput": true,                        // ← @Link 算输入
        "hasOutput": false,
        "inputs": ["username"],
        "outputs": [],
        "stateVariables": [
          { "name": "username", "decorator": "@Link", "decoratorArg": null, "auxDecorators": [],
            "type": "string", "isSimpleType": true, "isBuiltinType": false, "isClassType": false,
            "hasDefaultValue": false, "hasExternalInit": false }
        ],
        "usedComponents": []
      }
    ],
    "classes": [],
    "stateApiCalls": []                         // ← 无 Storage 相关 API
  }
]
```

#### B.3 `dependency_tracer.py FontSizeAdjuster <项目目录> --json` 输出

追踪 FontSizeAdjuster（它有 `@Link` 输入），向上找到父组件 SettingsPage：

```json
{
  "targetComponent": "FontSizeAdjuster",
  "projectDir": "examples/component-with-props",
  "migrationScope": {
    "mustMigrate": [
      "FontSizeAdjuster",                       // ← 目标组件自身
      "SettingsPage"                            // ← 父组件必须一起迁移!
    ],
    "mayNeedMigration": [],
    "reasons": {
      "SettingsPage->FontSizeAdjuster": {
        "direction": "parent->child",
        "passages": [
          {
            "childParam": "size",
            "parentExpression": "this.fontSize",
            "passageType": "state_variable_ref"  // ← 引用了父组件的 @State 变量
          }
        ],
        "summary": "size: state_variable_ref (this.fontSize)"
      }
    },
    "components": {
      "FontSizeAdjuster": {
        "name": "FontSizeAdjuster",
        "file": "before.ets",
        "version": "V1",
        "hasInput": true,
        "hasOutput": false,
        "stateVariables": [...]
      },
      "SettingsPage": {
        "name": "SettingsPage",
        "file": "before.ets",
        "version": "V1",
        "hasInput": false,
        "hasOutput": true,
        "stateVariables": [...]
      }
    }
  },
  "dependencyGraph": {
    "SettingsPage": {
      "children": ["FontSizeAdjuster"],
      "stateFlow": [
        "size: state_variable_ref (this.fontSize)"
      ]
    }
  }
}
```

**解读**：
- FontSizeAdjuster 的 `@Link size` 接收了 `$fontSize`（即 `this.fontSize` 的引用）→ 分类为 `state_variable_ref`
- `state_variable_ref` 是强依赖 → 父组件 SettingsPage 被加入 `mustMigrate`
- `callback` 类型不构成强制依赖（只是普通回调）

**迁移策略**：**联合迁移** SettingsPage + FontSizeAdjuster

**迁移路径**：
```
SettingsPage:
  @Component                → @ComponentV2
  @State username           → @Local username
  @State fontSize           → @Local fontSize
  @Provide('themeColor')    → @Provider('themeColor')
  $$this.username           → this.username!!

FontSizeAdjuster:
  @Component                → @ComponentV2
  @Link size                → @Param size + @Event setSize
  @Watch('onSizeChange')    → @Monitor('size')

调用方式:
  V1: FontSizeAdjuster({ size: $fontSize })
  V2: FontSizeAdjuster({ size: this.fontSize, onSizeChange: (v: number) => this.fontSize = v })
```

---

### 例 A vs 例 B 对比总结

| 维度 | 例 A：CounterPage | 例 B：FontSizeAdjuster + SettingsPage |
|------|-------------------|---------------------------------------|
| **component_analyzer 输出** | `hasInput: false, hasOutput: true`，3 个 `@State`，`usedComponents: ["CountDisplay"]` | `hasInput: true, hasOutput: true`，`@Link size`，父组件有 `@State` + `@Provide` |
| **stateApiCalls** | `[]`（无 Storage API） | `[]`（无 Storage API） |
| **dependency_tracer** | `mustMigrate: [自身]`，`reasons: {}` | `mustMigrate: [FontSizeAdjuster, SettingsPage]`，`passageType: "state_variable_ref"` |
| **迁移策略** | 独立迁移 | 联合迁移 |
| **复杂度** | `@State → @Local`，直接替换 | `@Link → @Param + @Event`，需改写调用方式 |
| **风险** | 低，无跨组件状态耦合 | 中，父→子数据流需要重新设计 |

---

## 九、目录结构与文件清单

```
v1-v2-migration/
├── SKILL.md                              # Skill 主文件（五阶段工作流）
├── scripts/
│   ├── component_analyzer.py             # 组件分析 + 状态API扫描 + Key追踪
│   ├── dependency_tracer.py              # 依赖链追踪 + mustMigrate判定
│   ├── api_version_checker.py            # API版本检测 + strict/relaxed判定
│   └── mixing_validator.py              # V1/V2混用规则校验
├── references/
│   ├── decorator-mapping.md             # 装饰器完整映射表
│   ├── class-migration.md               # @Observed→@ObservedV2
│   ├── app-state-migration.md           # LocalStorage/AppStorage/PersistentStorage→V2
│   ├── mixing-rules.md                  # V1/V2混用规则 + 桥接模式
│   ├── rendering-migration.md           # ForEach/LazyForEach→Repeat
│   └── advanced-topics.md               # makeObserved/animateTo
├── examples/
│   ├── simple-component/                # @State→@Local
│   ├── component-with-props/            # @Link→@Param+@Event
│   ├── observed-class/                  # @Observed→@ObservedV2
│   ├── localstorage/                    # LocalStorage/AppStorage→V2
│   └── partial-migration/              # V1/V2共存 + 桥接
└── templates/
    ├── component-v2-template.ets        # V2组件结构模板（10种模式）
    ├── observedV2-class-template.ets    # @ObservedV2数据对象模板（6种模式）
    └── bridge-pattern-template.ets      # 桥接模式模板（3种方案）
```
