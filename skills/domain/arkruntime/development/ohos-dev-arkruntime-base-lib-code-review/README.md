# ohos-dev-arkruntime-base-lib-code-review

基础库仓库 C/C++/ArkTS 代码变更审查 Skill。

## 适用仓库

| 仓库名称 | Gitcode 地址 |
|---|---|
| arkcompiler_runtime_core | https://gitcode.com/openharmony/arkcompiler_runtime_core |
| third_party_musl | https://gitcode.com/openharmony/third_party_musl |
| commonlibrary_c_utils | https://gitcode.com/openharmony/commonlibrary_c_utils |

其他仓库也可使用本 Skill 进行审查，但不会执行仓库专属的领域知识检查。

## 审查流程

1. 拉取 PR 分支
2. AI 通用代码审查
3. 语言补充知识审查（C/C++ 检查清单 8 项）
4. 仓库专属知识审查（musl 导出符号兼容性等）
5. 输出结构化审查报告

## 目录结构

```
ohos-dev-arkruntime-base-lib-code-review/
├── SKILL.md
├── README.md
├── references/
│   └── c-cpp-checklist-details.md
└── evals/
    ├── evals.json
    └── files/
```
