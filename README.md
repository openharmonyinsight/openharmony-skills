# OpenHarmony Skills

OpenHarmony 代码审查技能仓库，为 AI 助手提供结构化的代码审查指导。

## 简介

本仓库包含可重用的 OpenHarmony Skills。包括 OpenHarmony 整体可用的 Skills 和 领域总结的 Skills 

## 适用场景

## 技能列表

### openharmony-security-review

OpenHarmony C++ 系统服务安全审查技能，专注于识别以下安全风险：

- **外部输入处理** - IPC 反序列化验证、网络数据解析
- **多线程与并发** - 容器线程安全、死锁预防、TOCTOU 漏洞
- **敏感信息保护** - PII 数据脱敏、ASLR 绕过防护
- **权限验证** - 特权操作权限检查

**使用条件：**
- 审查 OpenHarmony C++ 系统服务代码（xxxService、xxxStub 实现）
- 代码处理 IPC（MessageParcel）或网络数据
- 代码存在多线程共享状态访问
- 代码执行用户数据或指针日志记录

## 如何使用

### 在 Claude Code 中使用

1. 将本仓库克隆到本地
2. 在 Claude Code 中配置技能路径
3. 当需要审查代码时，Claude 会自动调用相关技能

### 添加新Skills

1. 在 `skills/` 目录下创建新文件夹
 
[Skills文档](https://code.claude.com/docs/en/skills)

2. 建议使用 skill-creator 或者其它 skill 辅助生成 skill

## 仓库结构

```
openharmony-skills/
├── skills/                                    # 技能根目录
│   └── openharmony-security-review/          # 安全审查技能
│       └── SKILL.md                          # 技能定义文件
└── README.md                                 # 本文件
```


## 贡献

欢迎提交新的技能定义或改进现有技能。提交前请确保：

- 遵循现有的技能结构和格式
- 提供清晰的代码示例（反模式 vs 安全模式）
- 包含 DOT 图决策树
- 说明规则的原理和验证方法

## 相关资源

- [Skills文档](https://code.claude.com/docs/en/skills)

## 许可证

请查看 LICENSE 文件了解许可证信息。

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
