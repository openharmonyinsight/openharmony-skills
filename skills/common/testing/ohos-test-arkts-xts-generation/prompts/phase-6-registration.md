## Phase 6: Register Test Suites

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/04_project/02_ets_version_naming.md` | ETS 版本命名规范（目录名、文件名、Dynamic/Static/Interop 差异） | 不确定目录命名规则、需要确认版本后缀时 |

---

### ⚙️ 按需加载

本 Phase 不需要额外加载模块。

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有模块（仅执行 register_test.py 脚本和检查操作）
```

---

### 条件

仅当新增了测试文件时需要执行此阶段。

---

### 6.0 注册前检查

使用 `register_test.py` 前，先验证工程配置文件一致性：

| 检查项 | 文件 | 规则 | 错误后果 |
|--------|------|------|---------|
| BUILD.gn 模板函数 | BUILD.gn | 1.1→`ohos_js_app_suite`，1.2→`ohos_js_app_static_suite` | 模板函数错误 → 编译环境版本错 → 编译失败 |
| BUILD.gn test_hap | BUILD.gn | `test_hap` 字段必须注释掉 | ohosTest 不可用，未注释 → 编译报错 |
| BUILD.gn part_name | BUILD.gn | 必须与实际组件名一致 | 不一致 → 编译失败 |
| BUILD.gn subsystem_name | BUILD.gn | 必须与实际子系统名一致 | 不一致 → 编译失败 |
| Test.json module-name | Test.json | 固定值 `"entry"` | 其他值 → 测试运行器找不到模块 |
| Test.json test-file-name | Test.json | 必须与 BUILD.gn 的 `hap_name` 完全一致 | 不一致 → 测试套件注册失败 |
| hap_name 命名 | BUILD.gn | 遵循 ets_version_naming.md §二的矩阵 | 不合规 → CodeCheck 门禁拦截 PR |
| bundleName | app.json5 | 禁止 `com.example.helloworld` | 使用默认值 → 门禁拦截 |
| 目录名 | 工程目录 | 遵循 ets_version_naming.md §二 | 不合规 → 门禁拦截 |

---

### 6.1 注册测试用例到 List.test.ets

使用 `register_test.py` 脚本自动注册：

```bash
python {skill_root}/scripts/register_test.py \
  --list-file {测试套目录}/List.test.ets \
  --new-file {测试套目录}/{NewModule}.test.ets
```

脚本自动完成：
- 按字母顺序插入 import 语句（字母序确保多个开发者并行添加测试时不产生合并冲突，且保证文件内容确定性）
- 在 `testsuite()` 函数中插入调用

如需预览（不写入文件）：
```bash
python {skill_root}/scripts/register_test.py \
  --list-file {测试套目录}/List.test.ets \
  --new-file {测试套目录}/{NewModule}.test.ets \
  --dry-run
```

---

### 6.2 注册 Demo 页面到 main_pages.json（关键步骤）

> **⚠️ 遗漏此步骤会导致 Phase 9 测试执行全部失败！**
>
> 根因：测试用例通过 `router.pushUrl/replaceUrl` 跳转到 Demo 页面，如果 Demo 页面未注册到 `main_pages.json`，路由会报 `can't find this page` 错误，导致用例失败（Empty Text / error in beforeEach）。

**对于每个新增的 Demo 页面文件（`MainAbility/pages/**/*.ets`），必须检查并注册到路由配置文件**。

#### 步骤 1：识别新增的 Demo 页面

从 Phase 5 生成的文件清单中，筛选出 `MainAbility/pages/` 下的 `.ets` 文件：

```bash
# 假设新增文件记录在 generated_files.json 中
# 或直接检查 Demo 页面目录
ls {测试套目录}/entry/src/main/ets/MainAbility/pages/{子目录}/
```

#### 步骤 2：计算页面路由路径

路由路径格式：`MainAbility/pages/{子目录}/{PageName}`（不含 `.ets` 后缀）

例如：
- 文件：`MainAbility/pages/Text/TextFontFeature.ets`
- 路由：`MainAbility/pages/Text/TextFontFeature`

#### 步骤 3：检查 main_pages.json 是否已包含

```bash
MAIN_PAGES="{测试套目录}/entry/src/main/resources/base/profile/main_pages.json"
```

检查新增页面的路由是否已存在：
```bash
grep "MainAbility/pages/Text/TextFontFeature" "$MAIN_PAGES"
```

#### 步骤 4：注册缺失的路由

将缺失的路由添加到 `main_pages.json` 的 `"src"` 数组末尾（在 `]` 之前），保持 JSON 格式合法：

- 在最后一个已有条目后添加逗号
- 按页面所在的子目录分组排列（如所有 `Text/` 页面放在一起）
- 缩进使用 8 个空格（与已有条目一致）

**示例**：新增 2 个 Demo 页面
```json
        "MainAbility/pages/Text/TextExistingPage",
        "MainAbility/pages/Text/TextFontFeature",
        "MainAbility/pages/Text/TextIncrementalUpdatePolicy"
    ]
}
```

#### 步骤 5：验证注册正确性

```bash
# 验证 JSON 格式合法
python3 -c "import json; json.load(open('$MAIN_PAGES')); print('✅ JSON valid')"

# 验证所有 Demo 页面都已注册
for page in {新增页面列表}; do
    if grep -q "$page" "$MAIN_PAGES"; then
        echo "✅ $page registered"
    else
        echo "❌ $page MISSING"
    fi
done
```

---

### 6.3 注意事项

- 如果 `List.test.ets` 不存在，跳过步骤 6.1
- 不要修改 `List.test.ets` 中已有的内容
- **禁止跳过步骤 6.2**——Demo 页面注册遗漏是测试执行失败的最常见原因之一
- 同一个 `main_pages.json` 被所有测试共享，添加新路由时不要删除已有条目

### 常见注册失败排查

#### 测试注册失败
- **症状**：测试文件存在但不被执行
- **根因**：未在 List.test.ets 中注册新测试文件
- **修复**：使用 `scripts/register_test.py` 注册
