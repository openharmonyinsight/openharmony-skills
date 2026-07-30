# 源码路径定位（手动回退流程）

> 本文档是 `modules/L0_PreAnalysis/FailureAndSource.md` Step 2.5 的详细回退流程。
> **优先使用自动脚本**：`python3 scripts/locate_xts_source.py --testcase <用例名> --root <OH_ROOT>`（自动推断根/源码路径）。
> 脚本定位失败时，按下述手动流程回退。

## 目标

基于 BUILD.gn 中 `hap_name` 字段精准定位测试套件源码目录，避免 find 盲搜导致 static/non-static 版本混淆。

## 源码根路径解析优先级（从高到低）

1. **用户本次输入提供的源码路径**（最高）— AI 先检查用户输入
2. **配置文件 OH_ROOT**（`.xts-analysis-config.json`）— 用户未提供时回退
3. **AI 主动提示用户提供**（最低）— 均无时提示

> 详细说明见 [config.md](../docs/config.md)

**输入**：日志目录名（hap_name）+ OH_ROOT（按上述优先级链解析）
**输出**：测试套件目录路径 + 定位方法（hap_name / test_template / bundle_name）

## 2.5.1 提取 hap_name（强制）

**方法1（优先）**：从日志目录名提取
```bash
# 日志目录结构示例
# /home/xianf/copy/20260706/log/ActsAceCArkUI16Test/
#                                            └───── hap_name

hap_name=$(basename <日志目录>)   # 输出: ActsAceCArkUI16Test
```

**方法2（备用）**：从 bundle name 推断（hap_name 缺失时）
```bash
# 从 module_run.log 提取 bundle name
grep "Obtain the app name" module_run.log | grep -oE "com\.openharmony\.[a-z_]+"

# 示例: com.openharmony.arkui_capi_xts_api16
# 推断 hap_name（去除 static 后缀）
hap_name=$(infer_hap_from_bundle $bundle_name)
```

## 2.5.2 搜索 BUILD.gn 文件

```bash
# 在 OH_ROOT/test/xts/acts 下搜索所有 BUILD.gn
find $OH_ROOT/test/xts/acts -name "BUILD.gn" -type f

# 示例输出：
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16/BUILD.gn
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16_static/BUILD.gn
```

## 2.5.3 匹配 hap_name 字段（优先级①）

**优先级①**：hap_name 字段匹配（精准定位）

```bash
# 搜索包含 hap_name 字段的 BUILD.gn
grep -r "hap_name = \"$hap_name\"" $OH_ROOT/test/xts/acts --include="BUILD.gn"

# 示例输出：
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16/BUILD.gn:hap_name = "ActsAceCArkUI16Test"

test_suite_dir=$(dirname <匹配的BUILD.gn路径>)
echo "✅ 定位成功（hap_name匹配）: $test_suite_dir"
```

**解析 BUILD.gn 示例**：
```gn
ohos_js_app_suite("ActsAceCArkUI16Test") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsAceCArkUI16Test"      ← ✅ 匹配此字段
  part_name = "ace_engine"
  subsystem_name = "arkui"
  deps = [ ":ActsAceCArkUI16" ]
}
```

## 2.5.4 匹配测试模板 target（优先级②，hap_name 缺失时备用）

**支持的测试模板类型**（基于 XTS 源码统计，按使用频率排序）：

| 模板类型 | 使用次数 | 是否含 hap_name | 说明 |
|---------|---------|---------------|------|
| `ohos_js_app_suite` | 1893 | ✅ 是 | JS 应用测试套件（主要） |
| `ohos_js_app_static_suite` | 1140 | ✅ 是 | JS 应用静态测试套件 |
| `ohos_app_assist_suite` | 1007 | ✅ 是 | 应用辅助测试套件 |
| `ohos_moduletest_suite` | 359 | ❌ 否 | 模块测试套件（无 hap_name） |
| `ohos_js_hap_suite` | 13 | ✅ 是 | JS HAP 测试套件 |
| `ohos_js_app_assist_static_suite` | 9 | ✅ 是 | JS 应用辅助静态套件 |
| `ohos_test_suite` | 4 | ❌ 否 | 通用测试套件（无 hap_name） |
| `ohos_hap_assist_suite` | 2 | ✅ 是 | HAP 辅助测试套件 |
| `ohos_sh_assist_suite` | 1 | ❌ 否 | Shell 辅助测试套件（无 hap_name） |

```bash
# hap_name 未找到时，搜索测试模板 target（支持 9 种模板类型）
grep -rE "(ohos_js_app_suite|ohos_js_app_static_suite|ohos_app_assist_suite|ohos_moduletest_suite|ohos_js_hap_suite|ohos_js_app_assist_static_suite|ohos_test_suite|ohos_hap_assist_suite|ohos_sh_assist_suite)\(\"$hap_name\"\)" $OH_ROOT/test/xts/acts --include="BUILD.gn"

# 示例输出：
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16/BUILD.gn:ohos_js_app_suite("ActsAceCArkUI16Test")
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16_static/BUILD.gn:ohos_js_app_static_suite("ActsAceCArkUI16StaticTest")

test_suite_dir=$(dirname <匹配的BUILD.gn路径>)
echo "✅ 定位成功（测试模板匹配）: $test_suite_dir"
```

## 2.5.5 验证源码路径结构

**非 static 版本**（正确结构）：
```
ace_c_arkui_test_api16/
├── entry/
│   └── src/
│       ├── main/
│       │   └── ets/
│       │       └── pages/                    ← 页面代码（应用层）
│       └── ohosTest/                         ← 测试代码目录
│           └── ets/
│               ├── test/                     ← 测试代码（测试层）
│               │   └── textArea/
│               │       └── TextAreaLetterSpacing.test.ets  ← ✅ 正确
│               └── MainAbility/
│                   └── pages/                ← 测试页面代码
```

**static 版本**（备用结构）：
```
ace_c_arkui_test_api16_static/
├── entry/
│   └── src/
│       └── main/                             ← 注意：无 ohosTest 目录
│           ├── ets/
│           │   └── pages/                    ← 页面代码
│           └── src/                          ← 额外的 src 层
│               └── test/                     ← 测试代码
│                   └── textArea/
│                       └── TextAreaLetterSpacing.test.ets
```

**验证命令**：
```bash
# 优先查找 ohosTest 路径
ohosTest_path="$test_suite_dir/entry/src/ohosTest/ets/test"

if [ -d "$ohosTest_path" ]; then
    echo "✅ 非 static 版本，测试代码路径: $ohosTest_path"
    source_structure="ohosTest"
else
    # 回退查找 static 路径
    static_path="$test_suite_dir/entry/src/main/src/test"
    if [ -d "$static_path" ]; then
        echo "⚠️ static 版本，测试代码路径: $static_path"
        source_structure="static"
    else
        echo "❌ 源码路径结构异常"
        source_structure="invalid"
    fi
fi
```

## 输出示例

```
Step 2.5：源码路径定位
hap_name: ActsAceCArkUI16Test
定位方法: hap_name 字段匹配
测试套件目录: /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16
源码结构: ohosTest（非 static 版本）
```

## OH_ROOT 未配置时的处理

```
Step 2.5：源码路径定位
⚠️ OH_ROOT 未配置
→ 必须提示用户提供源码路径（不可静默跳过）
→ 用户拒绝提供后，降级为 L1 报告，标题显著标注"⚠️ 无源码分析（L1 降级）"
```

---

**来源**：从 `modules/L0_PreAnalysis/FailureAndSource.md` Step 2.5 下沉（2026-07-14 精简）。
