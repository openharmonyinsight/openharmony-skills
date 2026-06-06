## Phase 8: Build Verification

---

### 调用模式

| 模式 | 触发条件 | 与工作流模式的差异 |
|------|---------|-------------------|
| **工作流模式** | Phase 1-10 流程中，Phase 7 完成后自动进入 | phase_tracker 正常追踪前置条件 |
| **独立编译模式** | 用户直接要求编译（"编译xxx"、"重新编译"、"build"） | 跳过 phase_tracker，需自行确定 suite 名称 |

**独立编译模式**仅需额外执行以下准备（工作流模式中这些信息已在前序 Phase 中获得）：

1. 读取 `{skill_root}/.oh-xts-config.json` 获取 `OH_ROOT`
2. 从用户输入推断 suite 名称（优先级：用户指定名称 > 子系统 group 名 > BUILD.gn 提取 > 询问用户）

编译流程本身完全一致，见下方及 `build_workflow_linux.md`。

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/09_methodology/20_build_workflow_linux.md` | Linux 编译工作流（hvigor 命令、签名、编译排错） | 编译命令不确定、签名配置异常、编译错误需要排查时 |

---

### ⚙️ 按需加载（根据平台）

以下模块仅在你运行在对应平台时才需要加载：

| 平台 | 加载文件 | 说明 |
|------|---------|------|
| Windows 环境 | `{knowledge_root}/common/xts_experience/09_methodology/21_build_workflow_windows.md` | Windows 编译流程 |
| Windows + 静态编译 | `{knowledge_root}/common/xts_experience/09_methodology/23_build_workflow_windows_compile.md` | 静态编译配置 |
| Windows + UI 测试 | `{knowledge_root}/common/xts_experience/09_methodology/22_build_workflow_windows_automation.md` | UI 自动化测试 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L1_Analysis 模块（{knowledge_root}/common/xts_experience/ 下 L1_Analysis 相关内容）
所有 L2_Generation 模块（{knowledge_root}/common/xts_experience/ 下 L2_Generation 相关内容）
{knowledge_root}/common/xts_experience/ 下的 01_framework、02_arkts、03_standards、04_project、05_patterns 规范文件
```

---

### 编译流程

编译流程详见 `build_workflow_linux.md`（Linux）或 `build_workflow_windows.md`（Windows）。核心步骤：

1. **确定 suite_name**（步骤 0，必选）：
   
   > **关键**：用户提供的通常是目录名（如 `ace_ets_module_imageText_text`），但 BUILD.gn 中的 target 名（如 `ActsAceEtsModuleImageTextTextTest`）才是编译系统识别的 suite_name。**禁止直接将目录名作为 suite_name 传给编译系统。**

   **确定优先级**：
   
   | 优先级 | 来源 | 说明 |
   |--------|------|------|
   | 1 | 用户明确指定 `Acts*` 开头的名称 | 直接使用 |
   | 2 | Phase 1-7 工作流中已读取的 BUILD.gn target | 从上下文获取 |
   | 3 | 自动解析 BUILD.gn | 找到测试文件所在目录的 BUILD.gn，提取 `ohos_js_app_suite("xxx")` |
   
   **自动解析方法**（当优先级 1-2 不可用时）：
   
   ```bash
   # 方法 A: 使用 async_build.sh 内置的 resolve_suite_name（传入非 Acts 开头的名称时自动触发）
   # async_build.sh 会自动 find BUILD.gn 并 grep target 名
   
   # 方法 B: 手动从 BUILD.gn 提取（推荐，更精确）
   grep -oP 'ohos_js_app_suite\("\K[^"]+' {测试目录}/BUILD.gn
   ```

2. **预编译清理**（强制）: `{skill_root}/scripts/cleanup_group.sh {OH_ROOT} {子系统名}`
3. **SDK 缓存清理**（条件执行，见下方说明）
4. **异步编译**（推荐）: `{skill_root}/scripts/async_build.sh {OH_ROOT} {suite_name} rk3568 start`
5. **等待完成**: `{skill_root}/scripts/async_build.sh {OH_ROOT} {suite_name} rk3568 wait`
6. **验证产物**: 检查 `{OH_ROOT}/out/rk3568/suites/acts/acts/testcases/{suite_name}/{suite_name}.hap`
7. **错误处理**: 失败时分析日志并自动修复（最多 3 次重试）

> **禁止使用** `nohup ./test/xts/acts/build.sh ... &`，统一使用 `async_build.sh` 管理。

### 步骤 3：SDK 缓存清理（条件执行）

**仅当"无已有备份环境、需要原地修改 prebuilts"时执行。**

| 场景 | 是否清理 | 原因 |
|------|---------|------|
| mv 切换到已备份的 prebuilts_for_sta/dyn | **跳过** | 备份环境中的 SDK 已完整正确，直接使用 |
| 首次环境准备（无 prebuilts_for_xxx） | **执行** | 当前 prebuilts SDK 版本不对，需备份后清理以重新生成 |

```bash
# 首次静态环境准备（当前 prebuilts 为动态）
cp -r {OH_ROOT}/prebuilts {OH_ROOT}/prebuilts_for_dyn
rm -rf {OH_ROOT}/prebuilts/ohos-sdk/linux

# 或首次动态环境准备（当前 prebuilts 为静态）
cp -r {OH_ROOT}/prebuilts {OH_ROOT}/prebuilts_for_sta
rm -rf {OH_ROOT}/prebuilts/ohos-sdk/linux
```

### prebuilts 修改保护规则

当分析确定需要修改 prebuilts 中的文件时（如 SDK 声明文件缺失、hvigor 版本不匹配），必须遵循：

1. **先备份**：`cp -r {目标路径} {目标路径}.bak.$(date +%Y%m%d_%H%M%S)`
2. **再修改**：仅修改确认有问题的文件，不做大面积替换
3. **记录日志**：在 session_issues 中记录 prebuilts 修改详情（修改了什么、为什么、备份路径）

**绝对禁止**：
- `rm -rf prebuilts/` 或删除 prebuilts 下大面积内容
- 不备份直接覆盖 prebuilts 中的文件

### 编译加速技巧

当用户编译的是 group 目标而实际只需编译其中部分子工程时：

1. **备份 + 修改 group BUILD.gn**：`cp BUILD.gn BUILD.gn.bak`，注释掉不相关的 deps
2. **编译完成后恢复**: `mv BUILD.gn.bak BUILD.gn`

### 静态编译注意

- 需要 JAVA_HOME 配置
- Hvigor 版本校验（目标: `6.0.0-arkts1.2-ohosTest-*`）
- 需调用 `arkts-static-spec` 技能进行最终语法校验
