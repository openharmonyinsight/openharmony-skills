## Phase 1: Config & Subsystem Determination

---

### 📚 参考文档（按需查阅）

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `references/subsystems/_common.md` | 核心配置规则、命名规范、断言方法、代码风格 | 本 Phase 必须加载 |

---

### ⚙️ 按需加载

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 用户指定了子系统 | `references/subsystems/{Subsystem}/_common.md` | 子系统特有规则 |
| 用户指定了子系统和模块 | `references/subsystems/{Subsystem}/{Module}.md` | 模块特有规则 |

---

### 🚫 Do NOT Load

```
所有 modules/L1_Analysis 模块
所有 modules/L2_Generation 模块
所有 modules/L3_Validation 模块
```

---

### 步骤

#### 0. 读取配置

读取 `{skill_root}/.oh-capi-xts-config.json` 获取 `OH_ROOT`。

- 配置文件不存在 → 提示用户设置 `OH_ROOT`，写入配置文件
- `OH_ROOT` 路径无效 → 提示用户修正

CAPI 头文件路径：`{OH_ROOT}/interface/sdk_c/`

#### 1. 确定子系统

从用户输入推断目标子系统：

| 信息来源 | 优先级 | 示例 |
|---------|--------|------|
| 用户明确指定子系统名 | 最高 | "为 multimedia 生成测试" |
| 从 .h 头文件路径推断 | 中 | `interface/sdk_c/multimedia/` → multimedia |
| 从 API 前缀推断 | 低 | `OH_NativeBundle_*` → bundlemanager |

无法确定时，询问用户。

#### 2. 确定 Flow 类型

| 优先级 | 条件 | Flow |
|--------|------|------|
| 1 | 用户明确说明"新增接口"/"新 API"/"new API" | **Flow C** |
| 2 | 用户提供了覆盖率报告（CSV/XLSX/JSON/MD） | **Flow A** |
| 3 | 以上均不满足 | **Flow C**（CAPI 无扫描工具，默认按新增接口处理） |

#### 3. 确定生成目标

| 条件 | 生成目标 | 说明 |
|------|---------|------|
| 用户指定目标测试套路径 | 补充已有工程 | 在已有工程中追加测试文件 |
| 用户指定 .h 文件 | 解析 .h 并确定目标 | 可能创建新工程或补充已有工程 |
| 用户未指定 | 询问用户 | 提供子系统支持的 API 列表供选择 |

#### 4. 输出

- 确定的子系统名称
- Flow 类型（A 或 C）
- OH_ROOT 路径
- 目标 .h 文件路径（可能多个）
- 目标测试套路径（已有工程路径 或 "新建"）
