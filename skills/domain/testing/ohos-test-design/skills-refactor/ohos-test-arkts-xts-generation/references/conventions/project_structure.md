# XTS 测试工程结构规范

> **模块信息**
> - 层级：conventions（跨层共享）
> - 优先级：按需加载（Phase 1 配置加载时参考）
> - 适用范围：Stage 模式 ArkTS XTS 测试工程
> - 依赖：ets_version_naming.md
> - 来源：xts_acts 仓库 README_zh.md、README_xts1.2.md

---

## 一、Stage 模式标准工程结构

```
{TestSuite}/
├── BUILD.gn                    # 编译配置（模板函数必须匹配 ETS 版本）
├── Test.json                   # 测试资源配置
├── signature/
│   └── openharmony_sx.p7b      # 签名文件
├── syscap.json                 # 被测 API 最小 syscap
├── hypium/                     # 本地编译用，上库时删除
├── AppScope/
│   ├── app.json5               # bundleName（禁止 com.example.helloworld）
│   └── resources/
└── entry/
    └── src/main/
        ├── ets/
        │   ├── test/           # 测试代码目录
        │   │   ├── List.test.ets
        │   │   └── *.test.ets
        │   ├── MainAbility/    # 应用入口
        │   ├── TestAbility/    # 测试框架入口
        │   ├── Application/
        │   │   └── AbilityStage.ts
        │   └── TestRunner/
        │       └── OpenHarmonyTestRunner.js
        ├── resources/
        └── module.json5
```

---

## 二、配置文件关联规则

| 文件 | 字段 | 关联 | 规则 |
|------|------|------|------|
| BUILD.gn | `hap_name` | → Test.json `test-file-name` | 必须完全一致 |
| BUILD.gn | `subsystem_name` | → 子系统实际名称 | 必须一致 |
| BUILD.gn | `part_name` | → 组件实际名称 | 必须一致 |
| BUILD.gn | 模板函数 | → ETS 版本 | 1.1→`ohos_js_app_suite`，1.2→`ohos_js_app_static_suite` |
| Test.json | `module-name` | — | 固定值 `"entry"` |
| Test.json | `test-file-name` | → BUILD.gn `hap_name` | 必须完全一致 |
| app.json5 | `bundleName` | — | `com.open.harmony.xxx` 格式，禁止 `com.example.helloworld` |

---

## 三、BUILD.gn 完整模板（Stage 模式）

### 3.1 ArkTS-Dyn（1.1）

```python
import("//test/xts/tools/build/suite.gni")

ohos_js_hap_suite("ActsXxxTest") {
  hap_profile = "/src/main/module.json"
  js_build_mode = "debug"
  deps = [
    ":xxx_js_assets",
    ":xxx_resources",
  ]
  ets2abc = true
  certificate_profile = "signature/openharmony_sx.p7b"
  hap_name = "ActsXxxTest"
  subsystem_name = "{subsystem}"
  part_name = "{part}"
}
```

### 3.2 ArkTS-Sta（1.2）

```python
import("//test/xts/tools/build/suite.gni")

ohos_js_app_static_suite("ActsXxxStaticTest") {
  hap_profile = "/src/main/module.json"
  js_build_mode = "debug"
  deps = [
    ":xxx_js_assets",
    ":xxx_resources",
  ]
  ets2abc = true
  certificate_profile = "signature/openharmony_sx.p7b"
  hap_name = "ActsXxxStaticTest"
  subsystem_name = "{subsystem}"
  part_name = "{part}"
}
```

---

## 四、syscap.json

只需填写被测 API 的**最小 syscap**，不是全部。

示例：测试 `@ohos.app.ability.Want` 的 `bundleName` 属性：
```json
{
  "devices": [{ "type": "device", "label": "phone" }],
  "syscap": ["SystemCapability.Ability.AbilityBase"]
}
```

> **注意**: 使用 syscap.json 时，module.json5 中有对应字段需修改（具体见 xts_acts 仓库 README_note.md §3 配图）。

---

## 五、签名文件

- 获取方式：https://gitcode.com/openharmony/xts_acts/wiki/XTS签名
- 存放位置：`signature/openharmony_sx.p7b`

---

## 六、hypium 文件夹

- 本地编译验证时需要（静态版获取地址：https://gitcode.com/openharmony/xts_tools/tree/OpenHarmony_feature_20250328/hypium_static）
- git push 上库前**必须删除**
