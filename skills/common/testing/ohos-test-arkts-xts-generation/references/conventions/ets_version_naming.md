# ETS 版本命名规范

> **模块信息**
> - 层级：conventions（跨层共享）
> - 优先级：Phase 5/6 必须加载
> - 适用范围：ArkTS 1.1/1.2/Interop 三种 ETS 版本的命名
> - 依赖：无
> - 来源：xts_acts 仓库 README_note.md

---

## 一、三种 ETS 版本类型

| 版本 | 别名 | 判断依据 |
|------|------|---------|
| ArkTS 1.1 | 动态 / Dyn | build-profile.json5 中无 arkTSVersion 或值非 "1.2" |
| ArkTS 1.2 | 静态 / Static | build-profile.json5 中 arkTSVersion = "1.2" |
| Interop | 互操作 | 两种语法共存的工程 |

---

## 二、命名差异矩阵

> **来源**: xts_acts README_note.md §5/§7/§8/§9

### 2.1 目录名

> 注意：目录名中的 `[Static]` `[static]` `[Interop]` `[interop]` 是**字面量字符**，必须包含在目录名中。

| 版本 | 示例1 | 示例2 | 示例3 |
|------|-------|-------|-------|
| 1.1 | ActsAmsUsersThirdTest | ace_web_page_saving_dev_three | actscreatemodulecontexttest |
| 1.2 | ActsAmsUsersThirdTest[Static] | ace_web_page_saving_dev_three_[static] | actscreatemodulecontexttest[static] |
| Interop | ActsAmsUsersThirdTest[Interop] | ace_web_page_saving_dev_three_[interop] | actscreatemodulecontexttest[interop] |

> **存疑**: 示例1 用大写 `[Static]`，示例2/3 用小写 `[static]`。源文件未明确是否区分大小写，建议按子系统已有目录风格统一。

### 2.2 bundleName

| 版本 | 格式 | 示例 |
|------|------|------|
| 1.1 | `com.open.harmony.acts{xxx}` | com.open.harmony.actsacewebpagesavtest |
| 1.2 | `com.open.harmony.acts{xxx}.static` | com.open.harmony.actsacewebpagesavtest.static |
| Interop | `com.open.harmony.acts{xxx}.interop` | com.open.harmony.actsacewebpagesavtest.interop |

**禁止使用** `com.example.helloworld`（会被门禁拦截）。

### 2.3 hap_name / targetname

| 版本 | 格式 | 示例 |
|------|------|------|
| 1.1 | `ActsXxxTest` | ActsFaMyApplication1Test |
| 1.2 | `ActsXxxStaticTest` | ActsFaMyApplication1StaticTest |
| Interop | `ActsXxxInteropTest` | ActsFaMyApplication1InteropTest |

### 2.4 用例名

| 版本 | 格式 | 示例 |
|------|------|------|
| 1.1 | `xxx_{scenario}_0100` | abilityConstant_WindowMode_static_0100 |
| 1.2 | `xxx_{scenario}_static_0100` | abilityConstant_WindowMode_static_static_0100 |
| Interop | `xxx_{scenario}_interop_0100` | abilityConstant_WindowMode_static_interop_0100 |

> **存疑**: 源文件中 interop 行标注为 1.2 列，可能是原文笔误，interop 应属于互操作列。

---

## 三、门禁陷阱（CodeCheck）

### 3.1 hap_name 中 Static 的位置

CodeCheck 门禁使用 `Acts.*Test` 正则校验 hap_name。

- **正确**: `ActsFaMyApplication1StaticTest` — Static 在 `Test` 之前
- **错误**: `ActsFaMyApplication1TestStatic` — Static 在末尾，不匹配 `Acts.*Test`，会被门禁拦截

### 3.2 BUILD.gn 模板函数必须匹配 ETS 版本

| 版本 | BUILD.gn 模板函数 |
|------|-----------------|
| 1.1 | `ohos_js_app_suite("Name")` 或 `ohos_js_hap_suite("Name")` |
| 1.2 | `ohos_js_app_static_suite("Name")` |

**错误后果**: 1.2 工程使用 `ohos_js_app_suite` → 编译环境按 1.1 编译 → 静态语法测试用例全部编译失败。

### 3.3 BUILD.gn test_hap 字段

当前 ohosTest 不可用，BUILD.gn 中 `test_hap` 字段**必须注释掉**。

### 3.4 part_name 和 subsystem_name

BUILD.gn 中 `part_name` 和 `subsystem_name` 必须与实际子系统/组件名一致，不能随意填写。

---

## 四、Test.json 约束

| 字段 | 规则 | 错误后果 |
|------|------|---------|
| `module-name` | 固定值 `"entry"` | 其他值 → 测试运行器找不到模块 → 用例不执行 |
| `test-file-name` | 必须与 BUILD.gn 的 `hap_name` 完全一致 | 不一致 → 测试套件注册失败 |

---

## 五、syscap.json

只需填写被测 API 的**最小 syscap**，不是全部 syscap。

示例：测试 `@ohos.app.ability.Want` 的 `bundleName` 属性：
```json
{
  "syscap": ["SystemCapability.Ability.AbilityBase"]
}
```

> **注意**: 工程中使用 syscap.json 时，module.json5 中有对应字段需修改（具体修改内容见 xts_acts 仓库 README_note.md §3 配图）。
