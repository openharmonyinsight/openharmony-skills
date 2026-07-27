# Rule: 部件和构建系统

## Rule ID

OH-ARCH-COMPONENT-BUILD

## Applies To

- Feature Design
- Feature Spec
- Task Spec
- AI implementation
- Design / GB 基线审查
- GC 代码质量审查

适用于新增或修改 BUILD.gn、bundle.json、编译 target、部件依赖、SysCap 声明和跨仓构建路径。

## Must

- 必须说明新增或修改的 BUILD.gn、target 类型、sources、deps 和被上层 group 引用方式。
- 必须遵循最小依赖原则，只声明当前模块确实需要的依赖。
- 修改 bundle.json 时必须说明 component、subsystem、deps、features、syscap 影响。
- 必须确保新增依赖方向符合分层架构和子系统边界规则。
- 必须记录本地构建、GN 检查或等效验证命令和结果。
- 新增 Public API 或设备能力时必须评估 SysCap 声明。

## Must Not

- 禁止为了编译通过添加不必要的全局 deps。
- 禁止在 bundle.json 中引入循环依赖。
- 禁止跨部件直接依赖未公开内部 target。
- 禁止新增 target 后不接入构建入口或缺失验证命令。
- 禁止修改 SysCap、component 或 deps 后不说明兼容性和裁剪影响。

## Evidence

- BUILD.gn 变更说明。
- bundle.json 变更说明。
- 新增 target、sources、deps 和上层引用路径。
- 构建命令、日志或报告。
- SysCap 和部件裁剪影响分析。

## Check

- 检查 target 是否被正确引用。
- 检查 deps 是否最小且方向合法。
- 检查 bundle.json 是否完整、无循环、不越界。
- 检查构建验证是否覆盖受影响目标。
