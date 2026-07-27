# Profile 应用纪律(共享)

> 本文件是 7 个 ohos-* 能力 skill 共享引用的 profile 加载纪律。
> **职责边界:** 只放 profile 加载/应用的共性步骤;不做 profile 选择/路由(归 `using-ohos-sdd` 元路由);不含 profile 内容(在 `profiles/`);不下沉各能力 skill 的阶段特定纪律。类比 `workflow.md` 的 shared runtime 文档,非新 skill、非元路由。

## 何时应用

- `profile` ≠ `none` **且非保留值**(custom / security-sensitive):本纪律生效,按下方「应用步骤」读 profile 正文。
- `profile` 为保留值(custom / security-sensitive):**无对应 profile 文件**,跳过「读 profile 正文」步骤;仅应用通用 OHOS SDD 流程,并在交付件标注 profile 类型(custom = 自定义约束集;security-sensitive = 安全敏感,按安全专项对待)。不读不存在的 profile 文件。
- `profile` = `none`:不应用本纪律。

## 应用步骤

1. **读命中声明**:读 `manifest.md` 的 `profile`(主类型)+ `subprofiles`(命中子 profile 数组)。
2. **读 profile 正文**(runtime 路径):
   - 主 profile:`{{ASSET_ROOT}}/profiles/<profile>/profile.md`
   - 命中的子 profile:`{{ASSET_ROOT}}/profiles/<profile>/subprofiles/<sub>.md`(逐个)
3. **应用约束**:本阶段(proposal/spec/design/plan/review)应用 profile 的「阶段补充约束」+「专项检查清单」+「专家角色」。
4. **追加检查**:在本能力 skill 的 Verification Checklist 末尾,追加 profile 的专项检查项。

## 不做

- 不自行重新选择 profile(选择归元路由;本纪律只消费已选定的命中声明)。
- 不绕开 OHOS SDD 通用流程(profile 是**补充**,不另起流程编号、不绕开硬规则)。
- profile 内容深(arkui 355 行)时,只读本阶段相关节(最小读取原则)。
