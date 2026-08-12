# API 变更驱动的测试设计规则（Flow D）

> **本文件由 Phase 4 在 Flow D（API 变更驱动模式）下按需加载。**
> 数据来源：`scripts/parse_api_diff.py` 产出的 `uncovered_apis.json`，每个 API 条目附带 `change_info` 块。
> 权威依据：OpenHarmony `interface/sdk-js/build-tools/api_diff` 的 `ApiStatusCode` 枚举（21 种实际输出类型）。

---

## 一、change_info 字段说明

每个待测 API 的 `change_info` 由 `parse_api_diff.py` 自动填充：

```json
{
  "statusCode": 7,
  "change_type": "ERRORCODE_CHANGES",
  "risk_level": "MEDIUM",          // HIGH / MEDIUM / LOW
  "status_text": "错误码有变化",
  "old_message": "@throws {401,17000002,17000003}",
  "new_message": "@throws {401,17000002,17000003,17000099}",
  "raw_text": "assertComponentExist(on: On): void;",
  "incremental": {                 // 脚本已算出的增量，Phase 4 直接消费，无需重算
    "new_error_codes": ["17000099"],
    "removed_error_codes": []
  }
}
```

**Phase 4 优先使用 `incremental`**（精确的 before→after 差集）；当 `incremental` 为空或不适用时，回退到对照阅读 `old_message` / `new_message`。

---

## 二、statusCode → 测试设计动作映射

| statusCode | change_type | 风险 | Phase 4 设计动作 | 生成的测试类型 |
|-----------|-------------|------|-----------------|--------------|
| **3 / 21 / 22** | NEW_API / NEW_DTS / NEW_CLASS | 低 | **等同于 Flow C**：按完整规则生成全套 | PARAM + ERROR + RETURN（+BOUNDARY 如满足条件） |
| **6** | NEW_ERRORCODE | 中 | 为每个新增错误码生成一条独立用例（触发条件从 `@throws` / `new_message` 提取） | ERROR |
| **7** | ERRORCODE_CHANGES | 中 | 读 `incremental.new_error_codes`，每个新增码一条用例；`removed` 仅记录不生成 | ERROR |
| **10** | PERMISSION_CHANGES | 中 | 读 `incremental.new_permissions`/`removed_permissions`，补对应权限路径 | ERROR(201) + FUNCTION |
| **11** | NEW_PERMISSION | 中 | 生成「未授权→201」+「已授权→正常」两条路径 | ERROR(201) + FUNCTION |
| **12** | DELETE_PERMISSION | 中 | 删除权限后旧路径不再触发；补「无权限可正常调用」验证 | FUNCTION |
| **16** | FUNCTION_CHANGES | 高 | 读 `incremental.new_param_types`，为每个新参数类型补 PARAM 用例；返回值若变更补 RETURN | PARAM + RETURN |
| **14** | FUNCTION_TYPE_CHANGES | 高 | 类型声明变更（如泛型参数变化），对照 `old/new_message` 补兼容调用 | PARAM |
| **15** | CLASS_CHANGES | 高 | 类/枚举结构变更（枚举值增减等），对新增成员补 PARAM/RETURN | PARAM + RETURN |
| **0 / 1 / 2** | *_DELETE | 高 | **仅报告，不生成测试**（API 已不存在）。在设计文档「不生成项」章节列出原因 | — |
| **API_RENAME**（脚本识别） | — | 中 | **改名场景**：见下方「改名识别」专节。新名生成测试 + 标注旧名迁移路径；旧名不生成 | PARAM + ERROR + RETURN（按新名） |
| 4 / 5 / 8 / 9 / 13 / 18-20 | 版本/废弃/SysCap/访问级别等 | 低 | 兼容性变更，**默认不生成**；仅当 `@deprecated` 变更涉及 `@useinstead` 时补替代接口说明 | — |

---

## 三、增量消费细则（Phase 4 必读）

### 3.1 错误码增量（statusCode 6 / 7）

- **数据来源**：`incremental.new_error_codes`（已做 before/after 差集）
- **每个新错误码 → 一条独立 ERROR 用例**，禁止「codeA 或 codeB」合并断言
- **触发条件**：从 `new_message` 的 `@throws` 描述或子系统文档提取；无法确定时在设计文档标注「触发条件待确认」并降级为 RETURN 类占位
- **ArkTS-Sta 例外**：401 不单独设计（编译期拦截），仅业务码 17xxxxxx/20xxxxxx 设计

### 3.2 权限增量（statusCode 10 / 11 / 12）

- **数据来源**：`incremental.new_permissions`
- **新增权限（11）双路径**：
  1. 未授权环境调用 → 断言 `code === 201`
  2. 授权后调用 → 断言正常返回
- **权限变更（10）**：同上，对照 `new_permissions` / `removed_permissions` 分别处理
- **权限删除（12）**：补一条「原需权限现无需」的回归用例（调用成功）

### 3.3 函数签名增量（statusCode 16）

- **数据来源**：`incremental.new_param_types`（参数类型 union 新增成员）
- **每个新参数类型 → 至少一条 PARAM 用例**（正常值传入新类型）
- **返回值变更**：若 `old_message` 与 `new_message` 的返回类型不同，补 RETURN 用例验证新返回类型
- **可选参数增减**：新增可选参数补「不传该参数」的兼容用例

### 3.4 新增 API（statusCode 3 / 21 / 22）

完全复用现有 Phase 4 规则（等同 Flow C），`change_info` 仅作来源标注，不影响设计动作。

### 3.5 改名识别（API_RENAME，脚本智能配对）

api_diff 工具基于签名匹配，方法名变更时会输出「删除旧名(0) + 新增新名(3)」两条。`parse_api_diff.py` 的 `detect_renames()` 会将**同一 class 下、参数签名完全相同的 删除+新增 配对**，重新标记为 `change_type=API_RENAME`，避免误判为"真删除+从零生成"。

**识别条件**：`(class, 参数签名指纹)` 相同的 K 个删除 + K 个新增 → K 个改名。

**rename_info 字段**（配对后自动填充到 `change_info.rename_info`）：

```json
{
  "is_rename": true,
  "old_names": ["isBefore", "isAfter", "within"],
  "new_names": ["beforeComponent", "afterComponent", "withinComponent"],
  "signature": "(com: Component): On;",
  "class": "On",
  "migrate_hint": "API 改名（参数逻辑不变）：isBefore,isAfter,within → beforeComponent,afterComponent,withinComponent，现有用例可改方法名迁移"
}
```

**Phase 4 设计动作**：

| 角色 | statusCode | 处理 |
|------|-----------|------|
| 旧名条目（原 DELETE） | 0 | **不生成新测试**，在设计文档「改名迁移」章节列出：旧名 → 新名映射，提示「现有用例可改方法名迁移」 |
| 新名条目（原 NEW_API） | 3 | **按新名生成测试**（等同新增 API），但在用例「备注」列标注 `改名自 isBefore，参数逻辑相同，可参考旧用例` |

**设计文档标注要求**：Flow D 检测到改名时，文件头部「变更来源」章节追加：

```markdown
### 改名迁移清单（API_RENAME）
| 类 | 旧名 | 新名 | 参数签名 |
|----|------|------|---------|
| On | isBefore | beforeComponent | (com: Component): On |
| Driver | clickAt | clickAtWithOptions | (point: Point, options?: TouchOptions) |
> 提示：以上旧方法的现有测试用例，可通过修改方法名迁移到新方法，无需重新设计。
```

**注意**：同一组改名（如 `isBefore/isAfter/within` 签名相同）无法确定 1:1 精确对应关系，`old_names`/`new_names` 是集合形式。这不影响测试设计——参数逻辑相同，改名后测试代码结构一致，仅调用名不同。

### 3.5.1 改名迁移后的维度补全检查（强制）

> **改名迁移不是终点。** 迁移现有用例的方法名后，必须对新方法做维度补全检查——因为现有用例可能从未覆盖某些维度，迁移只是改了方法名，缺口依旧存在。

**检查步骤**（对每个改名后的新方法逐项执行）：

**步骤 A：重载变化识别（前置）**

对比变更前后的方法，确认重载关系是否被破坏：
- 旧方法是否有多个重载（同名不同签名）？
- 变更后这些重载的去向：改名 / 保留 / 合并为可选参数 / 删除？

> 重载变化直接影响后续判断：跨重载公用的用例（异常场景、可选参数默认值）在重载拆分后会失效，需按规则 3.5.3 重写。

**步骤 B：@throws 维度检查**

遍历新方法 `.d.ts` 声明的每个 `@throws` 错误码，对照迁移后的现有用例：

| 覆盖状态 | 处理 |
|---------|------|
| 已有用例覆盖该错误码 | ✅ 标记无需补 |
| 未覆盖，且触发条件可正常构造（如 null/undefined/非法参数） | 🔴 **必须补**：每个错误码至少一条独立用例 |
| 未覆盖，且触发条件特殊（见 3.5.2） | 🟡 列入检查表，标注"建议评估"，不强制补 |

**步骤 C：可选参数默认值维度检查**

若方法有 `param?: Type` 可选参数，检查是否有"不传该参数（走默认值）"的用例：

| 覆盖状态 | 处理 |
|---------|------|
| 已有"不传可选参数"的用例 | ✅ 标记无需补 |
| 未覆盖 | 🟡 **建议补**：一条不传可选参数的正常路径用例，验证默认值行为 |

**输出：改名迁移维度补全检查表**

设计文档中必须追加以下表格（每个改名方法一行）：

```markdown
### 改名迁移维度补全检查表

| 类.新方法 | @throws 错误码 | 已覆盖? | 可选参数默认值 | 已覆盖? | 重载处理 | 补全用例数 |
|----------|--------------|--------|-------------|--------|---------|-----------|
| On.beforeComponent | 17000007 | ❌ | 无可选参数 | — | 拆分(见3.5.3) | +2(null,undefined) |
| Driver.clickAtWithOptions | 17000002(特殊), 17000007 | 17000007✅ | options? | ❌ | 拆分(见3.5.3) | +2(默认值,重载重写) |
```

### 3.5.2 特殊触发条件错误码的处理策略

并非所有 `@throws` 错误码都适合在 XTS 用例中直接测试。部分错误码的触发条件需要**非典型使用环境**，直接为它们生成用例成本高且不稳定。

**判定特征**（基于错误码的**触发条件**，而非具体错误码值）：
- 需要并发调用同一 API（并发冲突类）
- 需要底层服务/驱动异常（系统级故障类）
- 需要特定硬件状态/外设状态（硬件依赖类）
- 触发条件不可稳定复现

**处理策略**：
- 维度补全检查表中**必须列出**这些错误码（不可忽略）
- 标注「触发条件特殊，建议测试团队评估是否纳入测试范围」
- **不作为强制补全项**，由具体测试团队结合子系统实际情况决定

> **注意**：以上判定基于触发条件的特征，不绑定任何特定错误码值。不同子系统的特殊错误码各不相同，需逐个分析其 `@throws` 描述的触发条件。

### 3.5.3 重载拆分/合并的公用用例重写（规则 3.5.1 步骤 A 的展开）

> **触发条件**：API 变更涉及重载关系变化（重载被拆分成独立方法、或多个方法合并为带可选参数的单方法）。

**背景**：旧 API 中，同一方法名的多个重载之间，以下场景的用例通常是**公用**的（一条用例同时覆盖多个重载）：
- 异常场景用例（传 null/undefined/非法类型 → 同一错误码）
- 可选参数不传（默认值）场景用例
- 参数边界值用例

签名变更（重载拆分/合并）后，这些公用用例会失效，需按新方法结构重写。

**重写规则**：

| 重载变化类型 | 说明 | 公用用例处理 |
|------------|------|------------|
| **拆分** | 旧多签名 → 各自独立的改名方法（如 `clickAt(point)` + `clickAt(point, options?)` → `clickAt(point)` + `clickAtWithOptions(point, options?)`） | 原公用用例按新方法名**拆分重写**，每个新方法独立覆盖异常/默认值场景 |
| **合并** | 旧多签名 → 单签名带可选参数 | 公用用例迁移后通常仍适用，但仍需按 3.5.1 步骤 B/C 校验维度 |
| **改名但签名不变** | 重载数量和签名不变，仅方法名变 | 公用用例改名迁移即可，按 3.5.1 补全缺失维度 |

**设计文档输出**：维度补全检查表的「重载处理」列标注每个方法的旧重载数 → 新重载去向 → 公用用例重写状态。

### 3.5.4 改名迁移用例的 @tc.desc 规范

- 改名迁移的用例 `@tc.desc` 必须更新为新方法名（不可保留旧名描述）
- 新增的维度补全用例（@throws / 可选参数默认值），`@tc.desc` 要标注测试维度，如：
  - `Test On.beforeComponent with null Component should report 17000007.`
  - `Test Driver.clickAtWithOptions without options (default behavior).`
- 重载重写的用例，`@tc.desc` 标注重载场景，如 `Test Driver.clickAtWithOptions (overload split from clickAt).`

---

## 四、设计文档标注要求

Flow D 产出的设计文档（`*.design.md`）须在文件头部追加「变更来源」章节：

```markdown
## 变更来源（Flow D）

> 数据源：api_diff 报告（用户提供 / 内置扫描）
> 共 N 条变更，其中：
> - 生成测试：X 条（statusCode: 3×a / 6×b / 7×c / 16×d ...）
> - 仅报告不生成：Y 条（删除类 statusCode: 0/1/2）
```

每个用例的「备注」列须标注其驱动的 `statusCode`，例如：`备注: 由错误码变更(7)驱动，新增码 17000099`。

---

## 五、与现有 Phase 4 规则的优先级

| 情形 | 优先采用 |
|------|---------|
| `change_info.incremental` 有明确增量 | **Flow D 增量规则优先**（更精确） |
| `incremental` 为空（如纯新增 API、类型结构变更） | 回退到现有 Phase 4 通用规则 |
| 删除类（0/1/2） | 不生成，仅记录 |

---

## 六、非兼容性变更识别与评审要求（⚠️ 流程合规）

> **重要**：本节定义的判定矩阵同时被 Phase 4（设计）和 Phase 11（报告）消费。
> 测试人员**不可盲目适配用例**——以下变更属于非兼容性变更，必须向开发确认是否已走**变更评审流程**（如 OpenHarmony 的 API 变更评审会）。

### 6.1 非兼容性变更判定矩阵

| change_type | statusCode | 非兼容原因 | 是否需评审 |
|-------------|-----------|-----------|-----------|
| **API_DELETE / DTS_DELETE / CLASS_DELETE** | 0 / 1 / 2 | 删除历史接口，调用方编译 break | ✅ 必须 |
| **API_RENAME**（脚本识别） | — | 接口名称变更，调用方需改名 | ✅ 必须 |
| **NEW_ERRORCODE** | 6 | 历史接口新增错误码，调用方可能触发未处理的异常分支 | ✅ 必须 |
| **ERRORCODE_CHANGES** | 7 | 同上 | ✅ 必须 |
| **NEW_PERMISSION** | 11 | 历史接口新增权限，未授权调用方突然失败 | ✅ 必须 |
| **PERMISSION_CHANGES** | 10 | 权限要求变更，调用方授权状态可能失效 | ✅ 必须 |
| **CLASS_CHANGES** | 15 | 类/枚举结构变更（枚举值增减等），影响类型契约 | ✅ 必须 |
| **FUNCTION_TYPE_CHANGES** | 14 | 类型声明变更（泛型/继承关系），影响类型契约 | ⚠️ 视情况，建议确认 |

**以下为兼容性变更（无需评审）**：NEW_API(3/21/22，纯增量)、VERSION_CHANGES(4)、DEPRECATE_CHANGES(5)、SYSCAP/访问级别/类型(8/9/13/18-20)。

> **函数签名变更(16)需人工判断**：参数类型放宽（如 `string` → `string|number`）通常兼容；参数类型收紧或个数变化则非兼容。Phase 4 对 statusCode 16 一律标注「待确认兼容性」。

### 6.2 Phase 4 设计动作（增加流程合规提示）

Flow D 检测到上述非兼容性变更时，设计文档**必须在文件头部「变更来源」章节后追加「⚠️ 非兼容性变更确认」章节**：

```markdown
### ⚠️ 非兼容性变更确认（需开发确认评审状态）

以下变更属于非兼容性变更，**测试人员不可盲目适配用例**，须向开发确认是否已走变更评审流程：

| API | 变更类型 | 非兼容原因 | 确认状态 |
|-----|---------|-----------|---------|
| On.isBefore → On.beforeComponent | API_RENAME | 接口名称变更 | ⬜ 待开发确认评审状态 |
| Driver.drag | ERRORCODE_CHANGES | 历史接口新增错误码 401 | ⬜ 待开发确认评审状态 |

> **确认流程**：向开发确认以上变更是否已提交 API 变更评审并获通过。
> - 已评审通过：测试按评审结论适配用例
> - 未评审 / 评审未通过：**暂停适配**，由开发先补齐评审流程
```

**Phase 4 对每条非兼容性变更的用例**，在「备注」列追加 `[非兼容变更] 待开发确认评审状态` 标记，Phase 11 报告中汇总。

### 6.3 判定速查（供 Phase 4 程序化判断）

```
非兼容 = change_info.change_type ∈ {
    API_DELETE, DTS_DELETE, CLASS_DELETE,
    API_RENAME,
    NEW_ERRORCODE, ERRORCODE_CHANGES,
    NEW_PERMISSION, PERMISSION_CHANGES,
    CLASS_CHANGES
}
```
