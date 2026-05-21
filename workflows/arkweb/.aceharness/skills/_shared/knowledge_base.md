# Chromium 开发导航（任务→文档映射）

> 集成自 chromium_agents/prompts/knowledge_base.md，适配 OpenHarmony/ArkWeb 场景。
> AI Agent 在处理 Chromium 相关任务时，**必须先查阅相关文档**，不可仅凭通用知识回答。

## 核心原则：先查文档，再回答

Chromium 代码库庞大且高度专业化。在回答任何 Chromium 相关问题前，必须先查阅相关文档：
- 官方文档：chromium_src 仓库的 `docs/` 目录（183+ md 文件）
- 知识库索引：通过 `oh-chromium-knowledge` 的 routing_table 定位代码路径
- 本地文档：`{DOCS_REPO}/analysis/` 下的历史分析报告

## 任务→文档映射

### 进程间通信 / IPC

**任务涉及进程间通信（Browser ↔ Renderer ↔ GPU）**
→ 找 `.mojom` 文件，理解数据结构和方法定义
→ 查阅 `docs/mojo_and_services.md`
→ 参考 `oh-chromium-knowledge/routing_table.json` 中 Mojo 相关路径

### 线程和异步

**涉及线程、TaskRunner、序列**
→ 查阅 `docs/threading_and_tasks.md`
→ 使用 `base::TaskRunner` + `base::BindOnce/BindRepeating`

### 回调

**涉及 base::Callback / base::OnceCallback / base::RepeatingCallback**
→ 查阅 `docs/callback.md`

### Blink 渲染引擎

**涉及 third_party/blink/renderer/ 代码修改**
→ **必须使用 WTF 容器**（`blink::Vector`、`blink::String`）和 **Oilpan GC**（`Member<>`、`WeakMember<>`、`Persistent<>`）
→ **禁止使用 STL 容器或大部分 base/ 等价物**
→ 参考 `oh-chromium-knowledge/repos/chromium_src/modules/blink.json`

### 页面渲染

**涉及 HTML/CSS/DOM/布局/绘制/合成**
→ 查阅 `docs/how_cc_works.md`（合成器）
→ 参考 routing_table 中"页面渲染"条目
→ 关键目录：`third_party/blink/renderer/core/{html,css,dom,layout,paint}/`

### 导航和加载

**涉及 URL 加载、导航、页面生命周期**
→ 查阅 `docs/navigation.md`、`docs/navigation_concepts.md`
→ 关键目录：`content/browser/frame_host/`、`third_party/blink/renderer/core/loader/`

### 焦点/输入/IME

**涉及键盘输入、焦点管理、IME**
→ 参考 routing_table 中"焦点管理"、"键盘输入与编辑"条目
→ 关键目录：`third_party/blink/renderer/core/input/`、`content/browser/input/`

### 滚动

**涉及滚动、惯性、自定义滚动条**
→ 参考 routing_table 中"滚动"条目
→ 关键目录：`third_party/blink/renderer/core/scroll/`

### GPU/图形

**涉及 GPU、WebGL、Vulkan、合成**
→ 查阅 `docs/gpu/` 目录下的 15 个文档
→ 关键目录：`gpu/`、`third_party/blink/renderer/platform/graphics/`

### 安全

**涉及沙箱、权限、CORS、CSP**
→ 查阅 `docs/security/` 目录下的 42 个文档
→ 关键目录：`content/browser/sandbox*.h`

### OHOS 适配

**涉及 OHOS 适配、NWeb、ArkWeb**
→ 参考 `oh-chromium-knowledge/repos/chromium_src/arkweb_adapter/ohos_dirs.json`（43 个目录）
→ 参考 `oh-chromium-knowledge/repos/chromium_src/arkweb_adapter/nweb_service.json`（NWeb API 映射）
→ 关键目录：`ohos/`、`ohos_nweb/`、`ohos_nweb_ex/`

### 构建

**涉及 BUILD.gn、Ninja、编译配置**
→ 查阅 `docs/modules.md`、`docs/component_build.md`
→ GN 依赖检查：`gn desc <out_dir> //target deps`

### 测试

**涉及单元测试、browser test**
→ 查阅 `docs/testing/` 目录下的 38 个文档

## 调试速查

| 错误 | 排查步骤 |
|------|---------|
| header not found | 1. 检查 BUILD.gn 的 deps 2. 检查 #include 路径 3. `gn gen` 重建 4. `gn desc` 确认依赖 |
| linker error | 检查 deps 中是否有提供符号的 target |
| visibility error | 在依赖的 BUILD.gn 中添加 visibility |
| 运行时调试 | `docs/debugging.md`，检查命令行 flags |
