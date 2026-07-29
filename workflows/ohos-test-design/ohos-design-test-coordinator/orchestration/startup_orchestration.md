# 启动编排：领域选择与确认（协调器执行步骤）

> 本文件为 ohos-design-test-coordinator 启动阶段的协调器操作细节。SKILL.md「启动流程」仅保留决策树与 AskUserQuestion 配置表；本文件承载领域选择的操作步骤与路径约定。
> **职责边界**：`orchestration/` = 协调器自己执行的步骤；`rules/` = spawn 出去的 Agent 按需 Read 的规则。

## 领域选择与确认

选择②时，由用户选择领域：

**步骤1：AskUserQuestion选择领域**

通用经验库固定加载全部（general/下三层知识目录，无需用户确认）。用户从以下领域列表中选择：

```
可选择的领域：
- ArkUI（组件、动画、生命周期）
- ArkWeb（加载、导航）
- 元能力（生命周期、权限）
- 包管理（安装卸载、权限、应用管理）
```

| 选项 | 说明 |
|------|------|
| ① 选择领域 | 从领域列表中选择领域（ArkUI/ArkWeb/元能力/包管理等） |
| ② 仅使用通用经验库 | 不加载领域经验库，仅通用固定加载 |
| ③ 自定义路径 | 用户输入自定义经验库路径 |

**步骤2：进入Phase1**

确认后，知识库范围确定：
- 领域路径：`domain/{领域}/` 下三层知识目录（domain-knowledge/、test-experience/、case-refinement/）
- 通用路径：`general/` 下三层知识目录
- 检索路径：`experience_library/domain/{领域}/{知识层级}/**/*.md` + `experience_library/general/{知识层级}/**/*.md`
- AI通过各知识层级目录下的index.md索引文件定位相关条目

**检索路径限定（强制执行）**：各阶段仅读取对应知识层级目录，详见 `rules/knowledge_usage_guide.md` 层级隔离规则。
