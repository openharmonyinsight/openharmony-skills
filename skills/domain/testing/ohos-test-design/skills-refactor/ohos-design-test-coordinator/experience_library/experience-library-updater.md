---
name: experience-library-updater
description: 经验库配置更新工具。扫描经验库目录下所有md文件（包括index），重新编号排序，更新文件汇总信息，并自动更新 config.yaml 配置文件。当用户需要更新经验库配置、同步经验库文件变更、或提及 update config.yaml / sync experience library / 经验库配置更新时使用。
---

# experience-library-updater

> 经验库配置更新工具

## 使用方法

prompt：执行 experience_library/experience-library-updater.md，更新 experience_library/config.yaml

## 功能说明

本 skill 用于自动更新经验库的配置和文件结构，主要功能包括：
1. 扫描 `domain/` 和 `general/` 目录下的所有 `.md` 文件（包括 index.md）
2. 按层级结构对文件中的条目重新编号
3. 更新每个文件开头的汇总信息表
4. 更新 config.yaml 配置文件

## 工作流程

### 第一步：扫描经验库目录结构

使用 Glob 工具扫描以下目录的所有 `.md` 文件（包括 index.md）：
- `{experience_library_root}/domain/**/*.md` - 领域特定知识
- `{experience_library_root}/general/**/*.md` - 通用知识

**重要**：必须包含 index.md 文件，它们也需要编号和汇总信息

### 第二步：按层级结构排序文件

根据文件路径的层级结构，对文件进行排序：

**排序规则**：
1. 按领域分组：ArkUI, Ability, ArkWeb, BundleManager, 安全...
2. 按知识层分组：domain-knowledge, test-experience, case-refinement
3. 按子目录层级排序：同一层级下，index.md 排在最前，其他文件按字母顺序
4. 文件内部条目按出现顺序编号

**排序示例**：
```
domain/ArkUI/
  domain-knowledge/
    index.md                           (第一优先)
    animation/animation.md             (第二优先)
    animation/transition/transition.md (第三优先)
    ...
  test-experience/
    index.md
    animation/animation.md
    ...
```

### 第三步：条目ID重新编号

对每个文件中的条目ID进行重新编号，确保全局唯一且符合层级结构。

**编号格式**：

| 知识层 | 格式 | 示例 |
|--------|------|------|
| 领域知识 (DK) | `DK-{领域缩写}-{子分类缩写}-{序号}` | `DK-UI-ANM-001`（领域知识-ArkUI-animation-001） |
| 测试经验 (TE) | `TE-{领域缩写}-{子分类缩写}-{序号}` | `TE-BMS-APP-001`（测试经验-BundleManager-application-001） |
| 用例细化 (CR) | `CR-{领域缩写}-{子分类缩写}-{序号}` | `CR-UI-ANM-001`（用例细化-ArkUI-animation-001） |
| 通用知识 (GK) | `GK-{分类缩写}-{序号}` | `GK-DFP-001`（通用知识-defect-patterns-001） |

**领域缩写对照表**：ArkUI→UI、BundleManager→BMS、Ability→ABY、ArkWeb→WEB、安全→SEC

**子分类缩写对照表**：animation→ANM、transition→TRN、component→CMP、button→BTN、image→IMG、list→LST、lifecycle→LIF、state-restore→STR、application→APP、install→INS、uninstall→UNS、permission→PRM、driver-app→DRV、entry→ENT、feature→FTR、shared→SHD、atomic-service→ATS

**通用知识分类缩写**：`DFP`(defect-patterns)、`NFN`(non-functional)

**编号逻辑**：
1. 从文件路径提取领域缩写和子分类缩写
2. 按照文件在排序后的位置，从 001 开始顺序编号
3. 同一文件内的条目按出现顺序编号
4. 跨文件但同一子分类的条目继续递增编号

**示例**：
```
文件1: domain/ArkUI/domain-knowledge/animation/animation.md
  条目1: DK-UI-ANM-001: 动画-中断恢复一致性

文件2: domain/ArkUI/domain-knowledge/animation/transition/transition.md
  条目1: DK-UI-TRN-001: 转场-反向动画一致性
  条目2: DK-UI-TRN-002: 转场-动画状态残留
```

### 第四步：更新文件汇总信息表

每个 md 文件开头都有汇总信息表，需要更新。

**普通文件格式**：
```markdown
# {标题}（{知识层}/domain/{领域}/{子分类}）

> {路径} 分类{知识层中文名}

| 字段 | 值 |
|-----|-----|
| 版本 | v1.0 |
| 条目总数 | {实际条目数} |
| 更新时间 | {当前日期 YYYY-MM-DD} |
| 知识层级 | {知识层中文名} |
| 适用领域 | {领域路径} |

---
```

**index.md 特殊格式**：
```markdown
# {领域名}（{知识层}/domain/{领域}）

> {知识层}/domain/{领域} 索引文件

| 字段 | 值 |
|-----|-----|
| 版本 | v1.0 |
| 子分类数 | {子分类数量} |
| 条目总数 | {该领域该知识层的总条目数} |
| 更新时间 | {当前日期 YYYY-MM-DD} |
| 知识层级 | {知识层中文名} |

---

## 子分类列表

{列出所有子分类，包括路径和条目数}

{test-experience 层列出测试场景；case-refinement 层列出细化场景}
```

**更新步骤**：
1. 读取文件内容
2. 统计文件中的条目数量（`## XX-XXX-NNN:` 格式）
3. 获取当前日期
4. 替换汇总信息表中的相关字段
5. 保持其他内容不变

### 第五步：提取条目信息并更新 config.yaml

对于每个文件，提取以下信息：

1. **条目ID、标题和行号**：
   - 收集文件中所有 `## XX-XX-XXX-NNN:` 格式的条目标题（更新编号后的）
   - 提取每个条目的标题文本（冒号后的内容）
   - 记录每个条目标题所在的行号

2. **相对路径**：相对于 `{experience_library_root}` 的路径

3. **摘要格式规则**：
   - 如果文件只有1个条目，使用该条目标题作为摘要
   - 如果文件有多个条目，用 `/` 分隔所有标题
   - 禁止省略（如"等N个"），必须列出所有条目标题

4. **行号格式规则**：
   - 每个条目都有对应的行号
   - 多个条目时，行号用逗号分隔
   - 行号与摘要中的条目一一对应，顺序相同

### 第六步：更新 config.yaml

根据收集的信息，更新 config.yaml 文件：

```yaml
domains:
  {DomainName}:
    display_name: "{显示名称}"
    keywords: [{keyword1}, {keyword2}]
    knowledge_layers:
      {layer-name}:
        display_name: "{中文显示名}"
        files:
          - path: "relative/path/file.md + 行号1,行号2,...,行号N"
            summary: "条目1标题/条目2标题/..."

general_knowledge_layers:
  {layer-name}:
    display_name: "{中文显示名}"
    files:
      - path: "relative/path/file.md + 行号1,行号2,...,行号N"
        summary: "条目1标题/条目2标题/..."
```

**更新规则**：
1. 保持 config.yaml 中的 `knowledge_layers_meta` 和 `output` 部分不变
2. 保持每个领域的 `display_name` 和 `keywords` 不变
3. 只更新 `files` 列表，根据实际扫描结果添加/删除/更新条目
4. 路径格式：从领域或通用目录开始
5. index.md 文件也要记录在 config.yaml 中

### 第七步：验证配置

更新完成后，使用 Read 工具重新读取 config.yaml，验证：
1. YAML 语法正确
2. 所有列出的文件都存在
3. 行号数量 = 条目数量
4. 行号顺序与摘要顺序一致
5. 条目ID编号符合规范且全局唯一
6. 所有文件的汇总信息表已更新

### 第八步：清理临时文件（必须）

在 skill 执行过程中生成的临时文件必须在结束时自动清理。

**NEVER约束**（强制执行）：
- NEVER 清理 experience_library 下的 md 文件——避免误删有效文件

**需要清理的临时文件模式**：`*.py`（Python脚本）、`*.json`（JSON临时数据）、`*_temp.*`（含 temp）、`*_cache.*`（含 cache）

**清理范围**：经验库根目录（`{experience_library_root}`）、用户工作目录、临时目录

**清理时机**：skill 执行完成后立即执行清理，在输出最终报告前完成

## 注意事项

1. **必须处理 index.md**：index.md 也要包含在扫描和更新范围内；需统计子分类和总条目数；config.yaml 中也要记录其信息
2. **编号全局唯一性**：同一领域、同一知识层、同一子分类下的条目ID必须连续且唯一；不同文件但相同子分类的条目ID应继续递增；编号从 001 开始，三位数字
3. **汇总信息准确性**：条目总数必须与实际条目数一致；更新时间使用当前日期；适用领域路径必须准确
4. **文件路径格式**：使用相对于经验库根目录的相对路径；保持与 config.yaml 现有格式一致
5. **行号对应关系**：每个条目都有对应的行号；多个条目时行号用逗号分隔；行号数量 = 条目数量；行号顺序 = 摘要中的条目顺序

## 工具调用顺序

```
1. Glob 扫描 domain/**/*.md（包括 index.md）
2. Glob 扫描 general/**/*.md（包括 index.md）
3. Read 读取每个 md 文件（可并行）：提取条目ID和标题、记录行号、统计条目数
4. 对条目ID重新编号（如需要）
5. Edit 更新每个文件的汇总信息表
6. Read 读取 config.yaml
7. Edit 更新 config.yaml
8. Read 验证更新后的 config.yaml
9. Bash 清理临时文件
```

## 输出报告

更新完成后输出报告，包含以下统计：

- **文件扫描**：领域数量、扫描文件总数（按知识层分类：领域知识/测试经验/用例细化/通用知识）
- **条目编号**：重新编号条目数、编号冲突修复数、编号格式修正数
- **汇总信息更新**：更新文件数、更新条目总数、更新时间同步数
- **config.yaml 更新**：新增/更新/删除文件记录数、总条目数
- **验证结果**：YAML 语法、文件存在性、行号对应、条目ID唯一性
- **临时文件清理**：清理的文件类型与数量

## 错误处理

遇到以下情况应报告错误并跳过该文件：
1. 文件格式不符合规范（缺少汇总信息表）
2. 条目ID格式错误（无法解析领域/子分类）
3. 文件路径无法解析（无法确定领域/知识层）
4. 编号冲突且无法自动解决

对于可自动修复的问题（如编号不连续、汇总信息不准确），应自动修复并记录。
