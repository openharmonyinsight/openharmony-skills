# Rules

本目录存放 kit 的校验规则和约束。按类别分目录：

| 目录 | 用途 | 状态 |
|------|------|------|
| `delivery/` | 交付件结构规则（ID 格式、元数据、校验清单） | Phase 1 |
| `agent/` | Agent 运行时行为规则（上下文经济性、subagent 纪律） | Phase 1 |
| `architecture/` | 架构约束规则（模块边界、API 层级、组件依赖） | Phase 2+ |
| `coding/` | 编码规范规则（命名、错误处理、日志、测试） | Phase 2+ |
| `profile/` | 子系统 profile 专属约束 | Phase 2+ |

## 新增规则

1. 在对应目录下创建 `.md` 文件
2. 每条规则包含：规则 ID、适用范围、检查内容、通过条件
3. 校验清单 (`delivery/validation-checklist.md`) 中引用新规则 ID
