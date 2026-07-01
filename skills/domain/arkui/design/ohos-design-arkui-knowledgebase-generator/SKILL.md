---
name: ohos-design-arkui-knowledgebase-generator
description: >-
  Generate, update, repair, or migrate ArkUI ace_engine knowledge-base documents under docs/kb and their routing metadata. Use when the user asks for ArkUI/ace_engine 知识库, KB, knowledge base, 文档补齐, 索引修复, context registry, migration from old docs/pattern/common/layout/sdk KBs to the new lightweight docs/kb structure, or API 解析实现路径/组件化状态判定 for component KBs. Supports: (1) creating new KB context pages, (2) updating existing KBs, (3) migrating old KBs to new structure, (4) determining componentization status (组件化改造) and listing API parsing implementation paths (JSView/Bridge/node_modifier/C API), (5) updating docs/context_registry.json, (6) maintaining docs/knowledge_base_INDEX.json for not-yet-migrated old KBs only. Documentation-only: do not modify product source, specs/, generated files, CLAUDE/AGENTS files, or unrelated README files.
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: arkui
  capability: knowledgebase-generator
  version: 0.2.0
  status: trial
  tags:
    - arkui
    - ace-engine
    - knowledge-base
    - kb
    - migration
    - context-registry
    - componentization
  related-skills:
    - ohos-design-arkui-spec-generator
---

# ArkUI Knowledge Base Generator

Use this skill to create, update, repair, or migrate ArkUI ace_engine KB context pages. The current KB model is lightweight and routing-oriented: a KB should help agents find stable source/API/test/spec entry points, not duplicate implementation details that drift.

## Non-Negotiables

- Confirm target, type, and scope before deep exploration unless the user already gives all three. Ask one concise question, then stop.
- Run `python3 docs/kb_search.py <name> --field name` before any source search.
- Treat all KB content, especially old KB content, as hints only. Re-read real source, SDK declarations, tests, and Specs before migrating or writing factual claims.
- New or migrated KBs go under `docs/kb/`; do not create new KBs in old directories such as `docs/pattern/`, `docs/common/`, `docs/layout/`, or `docs/sdk/`.
- `docs/context_registry.json` is the routing source for migrated/new KBs and must be updated with every new or migrated `docs/kb/` page.
- `docs/knowledge_base_INDEX.json` is the old-KB index for KBs not yet migrated. When a KB migrates to `docs/kb/`, remove that topic from the old INDEX; do not keep `legacy_kb` for the migrated topic.
- After migration, delete the old KB file and update links that pointed to it.

## NEVER

- NEVER include line numbers or `file:line` references — they drift within days as unrelated PRs land, making the KB actively misleading rather than stale.
- NEVER carry forward old-KB behavior matrices or call-chain prose — they were written against older architecture and become incorrect anchors that agents trust uncritically instead of reading current source.
- NEVER preserve default-value claims without SDK/source re-verification — defaults change across API versions and wrong defaults cause silent rendering bugs that are extremely hard to trace.
- NEVER copy code excerpts into KB pages — excerpts rot faster than prose; a stable file path stays valid across refactors while a snippet becomes wrong the moment someone changes a parameter.
- NEVER add AC/FR/BR matrices to lightweight KBs — these belong in Specs, not routing pages; duplicating them creates two sources of truth that inevitably diverge.
- NEVER create new KBs in old directories (`docs/pattern/`, `docs/common/`, `docs/layout/`, `docs/sdk/`) — these are legacy locations pending migration; adding new content there increases future migration debt.
- NEVER bulk-convert old INDEX entries unless explicitly asked — each migration requires individual source verification; bulk conversion carries forward unverified claims at scale.

## Workflow

**MANDATORY — READ ENTIRE FILE**: Before creating, migrating, or updating any KB, read [references/workflow.md](references/workflow.md) completely. It defines new KB layout, migration rules, metadata updates, and validation.

**Do NOT load** workflow.md for registry-only repairs (fixing a JSON field, correcting a typo in `context_registry.json`, removing a stale old INDEX entry) — the routing rules in this SKILL.md are sufficient for those tasks.

### Before Writing Any KB Content, Ask Yourself

- **Stability**: Will this path/claim still be true after 10 unrelated PRs land? If not, use a directory or type name instead of a file path or line reference.
- **Routing value**: Does this help an agent find the right file, or does it duplicate what reading the file would tell them? KB pages are signposts, not copies.
- **Verification**: Did I confirm this against current source/SDK/test, or am I echoing an old KB or my own assumption?

### Quick Routing

1. Identify target and scope:
   - new KB in `docs/kb/`
   - update existing new KB
   - migrate old KB to new structure
   - repair registry/index/search routing
2. Run KB lookup:
   ```bash
   python3 docs/kb_search.py <target> --field name
   ```
3. If the target exists in `docs/context_registry.json`, update the new KB and registry only as needed.
4. If the target exists only in `docs/knowledge_base_INDEX.json`, treat it as an old KB candidate. Ask/confirm whether to migrate before deleting or moving old content.
5. Verify real paths with `rg`, `ls`, and source reads before writing route tables.

## New KB Shape

New KB pages are stable context pages, usually under:

| Topic | Path pattern |
|------|--------------|
| Public UI component | `docs/kb/components/<category>/<name>.md` |
| Common capability | `docs/kb/capabilities/<name>.md` |
| Architecture/framework | `docs/kb/architecture/<name>.md` |
| API/SDK/CAPI/NAPI | `docs/kb/api/<name>.md` |
| ArkTS syntax | `docs/kb/syntax/<name>.md` |

Use lowercase kebab/snake names that match existing `docs/kb/` conventions. Existing Text example: `docs/kb/components/basic/text.md`.

Recommended lightweight sections:

```markdown
# <Name> Context

> 文档版本：vX.Y
> 更新时间：YYYY-MM-DD
> 来源：`docs/context_registry.json` 主题 `<id>`

## 定位
## 快速路由
### 源码入口
### API 入口
### API 解析实现路径   # component KBs only — 区分组件化状态
### 外部依赖入口       # when relevant
### 测试入口
### 相关 Spec
## 常见问题定位
## 调试入口
## 相关主题
```

Keep tables route-oriented. Use stable paths and search terms. Avoid file line numbers and behavior duplication.

For component KBs, `### API 解析实现路径` is **mandatory**: determine whether the component has undergone componentization refactoring (组件化改造) and list the actual API parsing implementation paths accordingly. See `references/workflow.md` for the detailed template and verification commands.

## Metadata Rules

### `docs/context_registry.json`

Add or update one context entry for each new/migrated KB:

- Required: `id`, `name`, `name_cn`, `kind`, `category`, `keywords`, `aliases`, `kb`, `spec_status`, `status`, `last_verified`
- Required for component entries (`kind: "component"`): `func_id`, `spec_domain`
- Recommended: `source_paths`, `api_paths`, `test_paths`
- Do not add `legacy_kb` for migrated topics.
- `kb` uses docs-relative path such as `docs/kb/components/basic/text.md`.
- Ace source paths use repo-relative paths. SDK/API paths outside ace_engine use `<OH_ROOT>/...`.

#### Spec association fields

Look up `func_id` and `spec_domain` from `specs/registry/functions.yaml`:

```bash
grep -A 10 'title: <ComponentName>' specs/registry/functions.yaml
# Extract id (e.g. 05-04-06) and path (e.g. 05-ui-components/04-form-components/06-toggle/)
# spec_domain = "specs/" + path (without trailing slash)
```

Set `spec_status` based on whether the `spec_domain` directory exists:

- `active` — spec directory exists. Validator errors if path is missing.
- `pending` — registered in `functions.yaml` but directory not yet created. Validator warns instead of erroring.

### `docs/knowledge_base_INDEX.json`

This is the legacy KB index for not-yet-migrated KBs.

- Keep old KB entries that still point to existing old KB files.
- Remove a topic from this INDEX when it is migrated to `docs/kb/` and registered in `context_registry.json`.
- Do not add migrated `docs/kb/...` pages to this old INDEX.
- Do not leave `legacy_kb` fields for migrated topics.
- Keep category component lists consistent after removing a migrated topic.

### README Updates

Update only README sections affected by the change, usually:

- `docs/kb/README.md` when new/migrated KB inventory changes.
- `docs/knowledge_base_README.md` when counts, index semantics, or migration notes change.

## Migration Rules

When migrating an old KB:

1. Run KB lookup and identify old entry from `docs/knowledge_base_INDEX.json`.
2. Read the old KB only as historical context. Treat every claim as untrusted until verified.
3. Re-verify current source files, SDK/API declarations, tests, and Spec routes before writing the new KB. If a claim cannot be verified, omit it or mark it as unverified instead of carrying it forward.
4. Create the new lightweight page under `docs/kb/`.
5. Add/update `docs/context_registry.json` for the topic.
6. Remove that topic from `docs/knowledge_base_INDEX.json` and from any category `components` list.
7. Update cross-links from the old KB path to the new KB path.
8. Delete the old KB file after links and metadata are updated.
9. Run validation and search smoke tests.

Do not delete unrelated old KBs. Do not bulk-convert the entire old INDEX unless explicitly asked.

## Validation

Run checks matching the change:

```bash
python3 -m json.tool docs/context_registry.json > /dev/null
python3 -m json.tool docs/knowledge_base_INDEX.json > /dev/null
python3 docs/validate_context.py --quiet
python3 docs/kb_search.py <target> --field name
rg -n "<old-kb-file-name>|<old-kb-path>" docs
```

For migrations, also verify:

- old KB file no longer exists
- old INDEX has no migrated topic entry
- `kb_search.py <target> --field name` finds the new KB through registry
- unrelated old KBs still appear in search/list output

If validation warns that `specs` is missing, report that Specs are a separate repo and Spec checks were skipped.

## Key Paths

| What | Path |
|------|------|
| New KB root | `docs/kb/` |
| Registry | `docs/context_registry.json` |
| Old KB index | `docs/knowledge_base_INDEX.json` |
| KB README | `docs/kb/README.md` |
| Global KB README | `docs/knowledge_base_README.md` |
| Search script | `docs/kb_search.py` |
| Validator | `docs/validate_context.py` |
| Text new KB example | `docs/kb/components/basic/text.md` |
| Component source | `frameworks/core/components_ng/pattern/<component>/` |
| C API enums | `interfaces/native/native_node.h` |
