# Rule: API 分级、权限和兼容性

## Rule ID

OH-ARCH-API-LEVEL

## Applies To

- Requirement baseline
- Feature Design
- Feature Spec
- Task Spec
- AI implementation
- Design / GB 基线审查
- GC 最终验证审查

适用于新增、修改、废弃 Public API、System API、Internal API、d.ts 声明、权限、错误码、SysCap 和兼容性行为。

## Must

- 必须明确 API 级别：Public API、System API、Internal API 或模块内部接口。
- 必须说明 API 签名、参数、返回值、错误码、权限和版本引入信息。
- 新增 Public API 必须说明 SysCap、兼容性和开发者文档影响。
- System API 必须说明系统应用使用边界和权限要求。
- Internal API 必须说明调用方范围，禁止被跨子系统误用。
- API 行为变更必须说明向前/向后兼容性、迁移策略和回归场景。

## Must Not

- 禁止未经设计和评审直接新增 Public/System API。
- 禁止静默改变已有 API 默认行为。
- 禁止把内部实现细节暴露为稳定 API。
- 禁止新增无错误码、无权限说明、无版本策略的开发者可见 API。
- 禁止在不兼容变更中缺失迁移说明和旧行为回归验证。

## Evidence

- API 签名表和 d.ts/头文件路径。
- 权限、错误码、SysCap 和版本策略说明。
- API 兼容性分析和迁移说明。
- API 文档、示例代码或 CHANGELOG。
- XTS、兼容性测试或旧行为回归证据。

## Check

- 检查 API 分级是否正确。
- 检查 d.ts、权限、错误码、SysCap 是否完整。
- 检查是否影响已有 API 行为和默认值。
- 检查是否需要 API 评审、文档更新和 XTS/兼容性测试。
