# OpenHarmony Profiles

> 本目录定义子系统和专项 profile。Profile 是对 4 阶段主流程的补充约束，不替代复杂度分级。

## 作用

Profile 用来表达不同子系统的差异化约束，例如：

- 哪些 N/A 维度要重点确认
- Phase 2/3 规格说明与设计应优先读取哪些上下文来源
- 审查阶段应重点检查哪些风险
- 哪些 expert / reviewer 角色需要参与
- 最终交付前应补哪些专项验证
- 是否支持 Spec for Validation，以及对应的输出格式、专项分析和审批规则

## 与复杂度分级的关系

- **复杂度**（简单/标准/复杂/关键）：决定流程裁剪强度、审批严格度
- **profile**：决定子系统或专项约束

两者正交，不互相替代。

## 目录结构

> **迁移完成**：旧 5 文件碎片（checklist.md, experts.md, rules.md, context-sources.md）已合并到单一 `profile.md`。碎片文件已移除，新 profile 只需一个 `profile.md`。

```text
profiles/
├── README.md
├── _template/
│   └── profile.md              # 新模板（单文件，含全部内容）
├── arkweb/
│   └── profile.md
├── arkui/
│   ├── profile.md
│   ├── templates/
│   │   └── spec-for-validation.md  # ArkUI 详细 2D/NFR/2C 格式覆盖
│   └── subprofiles/
│       ├── README.md
│       ├── component.md
│       ├── capi.md
│       ├── sdk-api.md
│       └── render.md
├── arkgraphic/
│   └── profile.md
└── arkdata/
    └── profile.md
```

## 使用方式

1. 先按源仓 `docs/02-分级流程指南.md` 选择复杂度级别。
2. 再判断是否需要子系统 profile。
3. 如需 profile，把 profile 名写入业务仓 `manifest.md`。
4. 各阶段先读取 `profile.md`，再按需读取子 profile 与 `context-engine/analysis/<profile>/` 中的补充文档。
5. 如 Profile 声明 `spec_for_validation`，开发者可在 spec/design Approved 后显式生成 Profile 格式的 `spec-for-validation.md`。

## Profile 编写指南

### 何时创建新 profile

- 同一子系统已有 **3+ 次独立需求**进入 SDD 流程，且每次都追加相似的专项检查项 → 值得沉淀为 profile
- 单次需求涉及的子系统尚无 profile，但审查中反复出现子系统特有的坑 → 可以提前创建
- 不要为尚未实际接触过的子系统预建 profile——没有真实需求驱动的 profile 容易写出脱离实际的检查项

### 如何创建

1. 复制 `_template/profile.md` 到 `子系统名/profile.md`
2. 填写"基本信息"和"阶段补充约束"两个核心节
3. 其余章节按实际需要补齐，不要填占位符
4. PR 提交，附上创建依据（如"基于 X 个已完成需求的审查经验沉淀"）

### 填写深浅

- 先用已有需求的**真实检查项和审查经验**填充，不要凭空设计"完美 profile"
- 每条检查项应能追溯到具体需求或审查记录
- profile 随实践持续迭代，不要求一次性写全

## Profile 命中与加载机制(P5)

两维度命中(正交):

- **仓间(repo)→ 主 profile**:读 `git remote get-url origin` → `basename` 去 `.git` → 仓名;扫各 profile 的 `repos` 字段命中主类型。平台无关(gitcode/gitee/github/ssh 均可)。
- **仓内(path)→ 子 profile**:扫本次变更文件路径 → 匹配 `subprofiles/<sub>.md` 的 `applies_to` glob → 命中子 profile(可多个)。

frontmatter 一律用缩进 block seq(`- item`),**不用内联数组** `[a, b]`(CLI YAML parser 不解析 flow style)。

仓名提取(纯 shell):

```sh
url="$(git remote get-url origin 2>/dev/null || true)"
repo="$(basename "${url%.git}")"
```

### source vs runtime 路径

| 角色 | 主 profile | 子 profile | Profile 模板 |
|---|---|---|---|
| source(本目录) | `<name>/profile.md` | `<name>/subprofiles/<sub>.md` | 全局默认 `../templates/spec-for-validation.md`；可选 `<name>/templates/*` 覆盖 |
| runtime(`{{ASSET_ROOT}}/profiles/`) | `<name>/profile.md` | `<name>/subprofiles/<sub>.md` | 全局默认 `{{ASSET_ROOT}}/templates/spec-for-validation.md`；可选 `<name>/templates/*` 覆盖 |

### 可选 Spec for Validation 声明

支持测试输入旁路的 Profile 在 frontmatter 中声明：

```yaml
spec_for_validation:
  title: <输出文档标题>
  adapter: <adapter-name> # 可选
  template_override: templates/spec-for-validation.md # 可选
  playbook: analysis/<profile>/spec-for-validation.md
  analysis:
    - id: <stable-id>
      title: <分析区标题>
      items:
        - <验证分析项>
```

- 默认使用公共 `openharmony/templates/spec-for-validation.md`，公共层负责生命周期、通用投影、渲染、检查和证据生成。
- `title` 定义输出文档标题；`analysis` 以声明方式追加 Profile 专项分析区和检查项。
- `adapter` 对应 `ohos_sdd_spec_for_validation_<adapter>.py`，仅在需要特殊投影或领域过滤规则时声明，不应重复公共流程逻辑。
- `template_override` 相对当前 Profile 目录解析，仅在默认格式无法满足该 Profile 时使用。
- `playbook` 描述测试人员输入的填写规则和缺口回流方式。
- 未声明 `spec_for_validation` 的 Profile 不支持该旁路，CLI 应明确拒绝，不回退到其他 Profile 格式。

### 软规范

profile schema 推荐节(基本信息 / 阶段补充约束 / 专项检查清单):缺则 `ohos-sdd validate` **warn 不 fail**。新 profile 按本机制扩充即可,不必一次填满。

### 与打包目录的关系

- `openharmony/profiles/`：社区版，面向贡献者阅读和编辑
- `{{ASSET_ROOT}}/profiles/`：运行时版本，由打包工具从本目录生成，供 Agent 执行
- 修改本目录后重新运行 `bash packaging/build.sh` 即可刷新运行时 profile

## 当前状态

- 当前已提供：`arkweb`、`arkui`、`arkgraphic`、`arkdata`
- 后续候选：`security-sensitive`

## 最小读取原则

- `profile.md` 是门禁和专项约束真相源，默认必读
- `subprofiles/` 只在命中模块类型时读取
- `context-engine/analysis/<profile>/` 只在需要更多背景、验证路径或长期资产说明时读取
- 不要为了“更全面”默认全读整个 profile 目录

## 最低约束

所有 profile 都必须遵守：

1. 不另起流程编号体系
2. 不绕开"计划未通过前不得修改生产代码"的硬规则
3. 不用 profile 替代 `manifest.md` 的单一事实源角色
4. 与当前事实冲突时，以源码、官方文档和 Owner 结论为准
