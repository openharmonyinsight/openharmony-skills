# OpenHarmony Commit Message Format

## Format

```
type(scope): 描述（≤49字符）

Issue: https://gitcode.com/{owner}/{repo}/issues/{number}
Signed-off-by: Name <email>
Co-Authored-By: Agent
```

## Rules

- **Title line**: max 49 characters, format `type(scope): description`
- **Types**: feat / fix / docs / refactor / test / chore
- **Blank line** between title and body (mandatory)
- **Issue**: full GitCode URL, never just `#number`
- **Signed-off-by**: `Name <email>` from GitCode account
- **Co-Authored-By**: fixed string `Agent`

## Example

```
feat(sample): 新增NAPI队列示例模块

Issue: https://gitcode.com/openharmony/arkui_napi/issues/1960
Signed-off-by: zhu_heng <zhuheng12@h-partners.com>
Co-Authored-By: Agent
```

## Title Type Reference

| Type | When to use |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| refactor | Code restructuring, no behavior change |
| test | Adding or updating tests |
| chore | Build, tooling, dependencies |
