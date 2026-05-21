# SKILL.md — oh-chromium-knowledge

> OpenHarmony Chromium 知识库 Skill
> 供 AI 辅助设计工作流（arkweb-sdd）的 code-analysis、architect 等 skill 调用

## 元信息

- **知识库仓库**: `zhufenghao/oh-chromium-knowledge` (GitCode 公开)
- **数据来源组织**: `openharmony-tpc` (14 个 Chromium 相关仓库)
- **Chromium 版本**: M144 (144.0.7559.59)
- **适用场景**: ArkWeb 代码分析、方案设计、代码审查、版本升级评估

---

## 1. 知识库读取协议

### 1.1 GitCode API 访问

```
BASE_URL = "https://gitcode.com/api/v5/repos/zhufenghao/oh-chromium-knowledge/contents"
AUTH = "PRIVATE-TOKEN: <TOKEN>"（优先 GITCODE_TOKEN，回退 GITLAB_TOKEN）
```

**读取文件（返回 base64 编码内容）**：
```bash
curl -sL "${BASE_URL}/{path}?ref=master" \
  -H "PRIVATE-TOKEN: ${GITCODE_TOKEN:-${GITLAB_TOKEN}}" \
  | jq -r '.content' | base64 -d
```

**获取目录列表**：
```bash
curl -sL "${BASE_URL}/{path}?ref=master" \
  -H "PRIVATE-TOKEN: ${GITCODE_TOKEN:-${GITLAB_TOKEN}}"
```

**响应格式**（单文件）：
```json
{
  "name": "index.json",
  "path": "index.json",
  "sha": "abc123...",
  "content": "eyJ...base64...",
  "encoding": "base64"
}
```

**Token 获取：优先环境变量 `GITCODE_TOKEN`，回退 `GITLAB_TOKEN`，或从 `.env` 文件读取

### 1.2 Agent 必须遵守的读取顺序

```
Step 1: index.json                     ← 全局路由入口（必须先读）
Step 2: search/by_feature.json         ← 按功能需求快速定位
Step 3: search/by_module.json          ← 按模块定位
Step 4: repos/{repo}/meta.json         ← 仓库元信息（1-2个）
Step 5: repos/{repo}/architecture.md   ← 架构文档（1-2个）
Step 6: repos/chromium_src/arkweb_adapter/routing_table.json  ← 代码路径映射
Step 7: skills/（按需）                  ← 领域开发指南
Step 8: cross_repo/（按需）              ← 跨仓依赖分析
```

### 1.3 禁止事项

- ❌ **不要批量扫描** — 不要一次性读取所有 repos/ 下的文件
- ❌ **不要批量读取 search/** — 不要把所有搜索索引全部加载
- ❌ **不要自己拼路径** — 文件路径必须从 index.json 或 search/ 索引中获取
- ❌ **不要把知识库当源码** — 知识库仅作索引参考，具体实现请查看实际代码仓库
- ❌ **不要跳过 Step 1** — 必须先读 index.json 了解全局结构

---

## 2. 快速检索路由

### 2.1 按需求类型 → 推荐文件

| 需求类型 | 首选文件 | 次选文件 |
|---------|---------|---------|
| 页面渲染/布局/CSS | `repos/chromium_src/modules/blink.json` | `repos/chromium_src/modules/gpu_cc_skia.json` |
| 文本选择/复制 | `routing_table.json` → "文本选择" | `modules/blink.json` → editing |
| 滚动（含过滚动） | `routing_table.json` → "滚动" | `modules/blink.json` → scroll |
| 焦点管理/Tab 导航 | `routing_table.json` → "焦点管理" | `modules/blink.json` → dom |
| 键盘输入/IME | `routing_table.json` → "输入与编辑" | `modules/blink.json` → editing |
| 表单交互/验证 | `routing_table.json` → "表单验证" | `modules/blink.json` → html |
| 触摸/手势 | `routing_table.json` → "触摸手势" | `modules/blink.json` → events |
| 右键菜单 | `routing_table.json` → "右键菜单" | — |
| 拖拽 | `routing_table.json` → "拖拽" | — |
| 视频/音频播放 | `routing_table.json` → "视频播放" | `modules/media.json` |
| 网络请求/缓存 | `routing_table.json` → "网络请求" | `modules/net.json` |
| Canvas/WebGL/WebGPU | `routing_table.json` → "Canvas 绘图" | `modules/gpu_cc_skia.json` |
| PDF 查看 | `routing_table.json` → "PDF 查看" | `repos/.../pdfium/architecture.md` |
| WebRTC 通话 | `routing_table.json` → "实时通信" | `repos/.../webrtc/architecture.md` |
| 多进程/IPC | `modules/content.json` | `modules/mojo.json` |
| OHOS 适配开发 | `ohos_dirs.json` + `ohos-adapter-guide.md` | `nweb_service.json` |
| 构建系统 | `build/gn_ninja.md` | `build/ohos_build_flags.json` |
| 版本升级 | `cross_repo/upgrade_paths.json` | `cross_repo/dependency_graph.json` |
| W3C AI API | `upgrade_paths.json` → arkweb_exclusive | `architecture.md` |

> `routing_table.json` 完整路径: `repos/chromium_src/arkweb_adapter/routing_table.json`

### 2.2 按 Chromium 模块 → 对应索引

| 模块 | 索引文件 |
|------|---------|
| Content Layer | `repos/chromium_src/modules/content.json` |
| Blink | `repos/chromium_src/modules/blink.json` |
| Mojo IPC | `repos/chromium_src/modules/mojo.json` |
| GPU/CC/Skia | `repos/chromium_src/modules/gpu_cc_skia.json` |
| 网络栈 | `repos/chromium_src/modules/net.json` |
| 媒体 | `repos/chromium_src/modules/media.json` |
| base/ 基础库 | `repos/chromium_src/modules/base.json` |
| V8 | `repos/chromium_v8/architecture.md` |
| CEF | `repos/chromium_cef/architecture.md` + `api_mapping.json` |

### 2.3 按仓库 → 对应文件

| 仓库 | meta | architecture | 额外文件 |
|------|------|-------------|---------|
| chromium_src | ✅ | ✅ | arkweb_adapter/, modules/, build/, chromium_rules.json |
| chromium_cef | ✅ | ✅ | api_mapping.json |
| chromium_third_party | ✅ | — | key_deps.json |
| chromium_chrome | ✅ | ✅ | — |
| chromium_v8 | ✅ | ✅ | — |
| 其他 9 个 | ✅ | ✅ | — |

---

## 3. 与其他 Skill 的集成方式

### 3.1 code-analysis skill 调用

**场景**: 分析 ArkWeb 特定功能的代码实现

```
code-analysis skill:
  1. 读取本知识库的 routing_table.json，确定代码路径
  2. 使用代码路径在 chromium_src 仓库中定位具体代码
  3. 结合 architecture.md 理解架构上下文
  4. 参考 chromium_rules.json 确保代码符合规范
  5. 如涉及 OHOS 适配，参考 ohos_dirs.json 和 ohos-adapter-guide.md
```

### 3.2 architect skill 调用

**场景**: 设计 ArkWeb 新功能方案

```
architect skill:
  1. 读取 arkweb_stack.json 理解完整技术栈
  2. 读取 dependency_graph.json 理解仓库间依赖
  3. 读取对应模块的 architecture.md 理解现有架构
  4. 参考 routing_table.json 中类似功能的实现模式
  5. 参考 upgrade_paths.json 了解版本演进方向
```

### 3.3 Subagent 调用示例

**在 subagent 场景中获取上下文**：

```
# 伪代码 — subagent 获取知识库上下文

1. 读取 index.json → 获取全局结构
2. 根据任务类型选择检索路径:
   - 功能开发 → search/by_feature.json
   - 模块分析 → search/by_module.json
   - 适配开发 → search/by_ohos_adapter.json
3. 读取 1-2 个相关文件获取具体信息
4. 在代码分析/方案设计中引用知识库信息
```

### 3.4 API 调用示例（Python）

```python
import base64, json, urllib.request

TOKEN = "your_gitlab_token"
BASE = "https://gitcode.com/api/v5/repos/zhufenghao/oh-chromium-knowledge/contents"

def read_kb_file(path: str, ref: str = "master") -> dict:
    """读取知识库文件"""
    url = f"{BASE}/{path}?ref={ref}"
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": TOKEN})
    resp = json.loads(urllib.request.urlopen(req).read())
    content = base64.b64decode(resp["content"]).decode("utf-8")
    return json.loads(content) if path.endswith(".json") else content

# 1. 读取全局路由
index = read_kb_file("index.json")

# 2. 按功能检索
features = read_kb_file("search/by_feature.json")
# 找到"滚动"相关文件
scroll_files = [f for f in features["features"] if f["name"] == "滚动"][0]["files"]

# 3. 读取路由表
routing = read_kb_file("repos/chromium_src/arkweb_adapter/routing_table.json")
scroll_paths = routing["routing"]["滚动"]["chromium_paths"]
```

---

## 4. 知识库维护

### 4.1 更新索引

**手动更新**:
1. 修改本地 `/root/oh-chromium-knowledge/` 中的文件
2. 通过 Git push 或 API 推送到 GitCode

**API 更新（单文件）**:
```bash
# 1. 获取当前文件 SHA
curl -sL "${BASE_URL}/{path}?ref=master" -H "PRIVATE-TOKEN: ${TOKEN}" | jq '.sha'

# 2. 更新文件
curl -X PUT "${BASE_URL}/{path}?ref=master" \
  -H "PRIVATE-TOKEN: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "update {path}",
    "content": "'"$(base64 -w0 file.json)"'",
    "sha": "{current_sha}"
  }'
```

### 4.2 新仓库入库流程

1. 在 `repos/` 下新建仓库目录
2. 创建 `meta.json`（从 GitCode API 获取仓库信息）
3. 创建 `architecture.md`（编写架构概述）
4. 更新 `index.json` 的 `repo_index` 和 `repositories`
5. 更新 `cross_repo/dependency_graph.json`（如有依赖关系）
6. 更新 `search/by_module.json`（添加新模块条目）
7. 提交推送

### 4.3 版本升级后更新

Chromium 版本升级后需要更新：
1. `repos/chromium_src/meta.json` — 版本号
2. `cross_repo/upgrade_paths.json` — 添加新升级路径
3. `repos/chromium_src/architecture.md` — 新特性和不兼容变更
4. `repos/chromium_src/arkweb_adapter/routing_table.json` — 新增/变更的代码路径
5. `search/by_feature.json` — 新增功能特性条目

---

## 5. 覆盖范围

### 5.1 14 个入库仓库

| 梯队 | 数量 | 说明 |
|------|------|------|
| 核心 (Tier 1) | 6 | chromium_src, chromium_cef, chromium_third_party, chromium_chrome, chromium_v8, chromium_third_party_skia |
| 子系统 (Tier 2) | 7 | ffmpeg, angle, devtools_frontend, webrtc, blink_webtests, dawn, pdfium |
| 归档 (Tier 3) | 1 | chromium_arkweb |

### 5.2 知识深度

| 仓库 | meta | architecture | 详细索引 | 模块拆分 | 路由表 |
|------|------|-------------|---------|---------|--------|
| chromium_src | ✅ | ✅ | ✅ | ✅ 7个模块+17个组件 | ✅ 29个需求类型 |
| chromium_cef | ✅ | ✅ | ✅ API映射 | — | — |
| chromium_third_party | ✅ | — | ✅ 22条依赖清单 | — | — |
| 其他 11 个 | ✅ | ✅（80-208行） | — | — | — |

### 5.3 不在覆盖范围内

- Chromium 上游原版代码（仅覆盖 OHOS 适配分支）
- ArkUI 框架层（ace_engine）的内部实现
- web_webview 的完整 API 文档（参考 oh_component_knowledge）
- 实际源码内容（知识库仅提供索引和架构描述）
