# repos 模块 — 查询工具规格

代码仓查找、列表与 git 访问 URL 构建。repos 是归属链的根，每个部件通过 `repo_id` 关联到一个仓。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_repo` | 按仓名精确查找 |
| `list_repos` | 列出所有仓，含部件计数 |
| `git_url` | 工作区路径/GN label → git 仓访问 URL |

---

## get_repo

按仓名精确查找，返回仓的 git 元数据、部件计数与仓根 URL。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `name` | string | ✓ | 仓名（manifest 的 name 属性，如 `ability_ability_runtime`） |

**返回**

```json
{
  "id": 3,
  "name": "ability_ability_runtime",
  "path": "foundation/ability/ability_runtime",
  "remote": "origin",
  "remote_url": "https://gitcode.com/openharmony/ability_ability_runtime.git",
  "revision": "refs/heads/master",
  "groups": "default",
  "clone_depth": 1,
  "head_commit": "abc123def456...",
  "component_count": 1,
  "url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123def456"
}
```

`path` 是工作区内相对路径。`head_commit` 是当前 HEAD commit SHA。`component_count` 是该仓下的部件数（`components.repo_id` 关联统计）。`url` 是仓根访问 URL，`ref` 优先用 `head_commit`（扫描时的确切状态），无则退回 `revision`（分支名，会随时间漂移）。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 仓名不存在 |
| `NO_SESSION` | 未建立会话 |

---

## list_repos

列出所有仓，按仓名排序，每个仓附部件计数与仓根 URL。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `limit` | int | | 返回上限，默认 50，上限 200 |

**返回**

```json
{
  "repos": [
    {
      "id": 3,
      "name": "ability_ability_runtime",
      "path": "foundation/ability/ability_runtime",
      "remote_url": "https://gitcode.com/openharmony/ability_ability_runtime.git",
      "head_commit": "abc123d",
      "component_count": 1,
      "url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d"
    }
  ],
  "total": 38
}
```

`head_commit` 截断为前 7 位（git short format），完整 SHA 用 `get_repo`。

---

## git_url

给定工作区相对路径或 GN label，构建对应文件的 git 仓访问 URL。这是 Agent 从数据跳转到源码的通用桥梁。

**URL 构建逻辑**

1. **输入识别**：路径以 `//` 开头 → GN label（`//path:target`），取 `:` 前的目录部分 + `/BUILD.gn`；否则视为文件路径
2. **仓匹配**：按最长路径前缀匹配 `repos.path`（如 `foundation/ability/ability_runtime` 匹配路径 `foundation/ability/ability_runtime/bundle.json`）
3. **仓内相对路径**：strip 仓 path 前缀，得到仓内文件路径（如 `bundle.json`）
4. **ref 选择**：优先 `head_commit`（扫描时确切状态），无则退回 `revision`（分支名）
5. **URL 拼接**：`{remote_url去掉.git}/tree/{ref}/{仓内路径}`，GitLab 系多一段 `/-/`
6. **行号锚点**：有 `line` 参数时追加 `#L{line}`

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `path` | string | ✓ | 工作区相对文件路径（如 `foundation/ability/ability_runtime/bundle.json`）或 GN label（如 `//foundation/ability/ability_runtime:ability_runtime`） |
| `line` | int | | 行号，追加 `#L{line}` 锚点 |

**返回**

```json
{
  "url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/bundle.json",
  "repo": "ability_ability_runtime",
  "ref": "abc123def456...",
  "file_path": "bundle.json",
  "exact": true
}
```

`file_path` 是仓内相对路径（已 strip 仓 path 前缀）。`exact` 为 true 表示用 `head_commit`（扫描时确切状态），false 表示用 `revision`（分支名，会漂移）。

GN label 示例：`//foundation/ability/ability_runtime:ability_runtime` → `file_path` 为 `BUILD.gn`，URL 指向该目录的 BUILD.gn 文件（目标定义的推荐猜测，不排除来自 .gni import）。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 路径不属于任何已扫描的仓 |
| `NO_REF` | 仓无 `head_commit` 也无 `revision`，无法构建 URL |
| `NO_SESSION` | 未建立会话 |
