# xts-generator

> **OpenHarmony XTS 测试用例通用生成模板**

## 快速开始

```bash
请使用 xts-generator 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
```

## 功能特性

- ✅ **API 定义解析** - 解析 `.d.ts` 文件，提取接口、方法、参数、返回值、错误码
- ✅ **智能测试生成** - 根据测试策略自动生成符合 XTS 规范的测试用例
- ✅ **测试设计文档生成** - 同时生成结构化的测试设计文档，包含测试场景、测试步骤、预期结果等
- ✅ **测试覆盖分析** - 分析现有测试文件，识别已覆盖和未覆盖的 API
- ✅ **代码规范检查** - 确保生成的代码符合 XTS 测试规范
- ✅ **编译问题解决** - 提供 Linux 和 Windows 双平台编译指南和问题排查方案

## 适用场景

- ✅ 为新 API 生成完整的测试套件
- ✅ 同时生成测试用例和测试设计文档
- ✅ 分析现有测试的覆盖情况
- ✅ 补充缺失的测试用例和测试设计
- ✅ 验证测试代码规范性
- ✅ 各子系统定制化测试生成

## 何时使用与何时不使用

**何时使用**：
- ✅ 需要为新 API 生成测试用例
- ✅ 需要生成测试设计文档
- ✅ 需要分析测试覆盖情况
- ✅ 需要验证测试代码规范性
- ✅ 需要批量生成测试用例

**何时不使用**：
- ❌ 需要生成非 XTS 测试
- ❌ 需要修改工程配置文件
- ❌ 需要运行测试用例
- ❌ 需要调试测试用例

## 快速使用

### 方式1：通用模板（新手）

```
请使用 xts-generator 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
```

### 方式2：子系统配置（推荐）

```
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
```

### 方式3：自定义配置（高级）

```
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: MySubsystem
自定义配置:
  Kit包: @kit.MyKit
  测试路径: test/xts/acts/mysubsystem/
  API声明: interface/sdk-js/api/@ohos.mysubsystem.d.ts

API: myAPI.method()
```

> 📖 **详细使用方式**: [docs/USAGE.md](./docs/USAGE.md)

## 最佳实践

### 生成前

- 明确生成需求（API 类型、测试类型、测试级别）
- 参考已有测试用例，分析代码风格
- 优先使用子系统配置

### 生成后

- 检查 @tc 注释块是否完整
- 检查 hypium 导入是否正确
- 检查测试用例命名是否符合规范
- 进行编译验证

## 输出验证

### 测试用例验证
- ✅ 文件命名符合规范
- ✅ @tc 注释块完整且格式正确
- ✅ hypium 导入正确
- ✅ 测试用例命名符合规范（小驼峰）
- ✅ 测试逻辑正确

### 测试设计文档验证
- ✅ 文件命名符合规范（.design.md）
- ✅ 测试场景完整
- ✅ 测试步骤清晰
- ✅ 预期结果明确
- ✅ 覆盖统计准确

## 文档

- **技能文档**: [SKILL.md](./SKILL.md) - 完整技能说明
- **使用指南**: [docs/USAGE.md](./docs/USAGE.md) - 详细使用方式
- **使用指南**: [docs/USAGE_GUIDE.md](./docs/USAGE_GUIDE.md) - 最佳实践
- **架构文档**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - 模块化架构详解
- **配置指南**: [docs/CONFIG.md](./docs/CONFIG.md) - 配置说明
- **故障排除**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) - 常见问题解决方案

## 模块架构

本技能采用四层模块化架构：

- **L1_Framework** - 框架和规范层（必须加载）
  - Hypium 框架知识
  - ArkTS 语法规范
  - XTS 测试约定

- **L2_Analysis** - 分析层（按需加载）
  - API 定义解析
  - 工程配置解析
  - 测试覆盖分析
  - 文档阅读

- **L3_Generation** - 生成层（按需加载）
  - 测试用例生成
  - 测试设计文档生成
  - 代码模板库

- **L4_Build** - 构建层（按需加载）
  - Linux/Windows 编译工作流
  - BUILD.gn 配置
  - 编译问题排查

## 示例

- [ArkUI 子系统配置](./references/subsystems/ArkUI/)
- [ArkWeb 子系统配置](./references/subsystems/ArkWeb/)
- [测试设计文档示例](./modules/L3_Generation/examples/TreeSet.test.design.md)
- [测试用例示例](./examples/Component.onClick.test.ets)

## 版本

**v1.15.0** (2026-02-12)

### 新增功能
- ✅ ArkTS 静态语言语法规范校验
- ✅ 自动语法规范检查和修复建议
- ✅ 集成 16 个 ArkTS 语言规范文件
- ✅ 详细的校验结果输出

### 架构优化
- ✅ 工作流程新增第 10 步（语法规范校验）
- ✅ 新增 arkts-static-spec 使用模式
- ✅ 优化重要注意事项，添加语法类型识别说明

## 子系统支持

| 子系统 | Kit 包 | 测试路径 | 状态 |
|--------|--------|----------|------|
| ArkUI | @kit.ArkUI | test/xts/acts/arkui/ | ✅ 完整 |
| ArkWeb | @kit.ArkWeb | test/xts/acts/arkweb/ | ✅ 完整 |
| testfwk | @kit.TestKit | test/xts/acts/testfwk/ | ✅ 完整 |
| ArkTS | @kit.ArkTS | test/xts/acts/arkts/ | ✅ 完整 |

## 触发关键词

**主要关键词**：
- `XTS`
- `测试生成`
- `用例生成`
- `测试用例`
- `测试设计`

**次要关键词**：
- `API测试`
- `测试设计文档`
- `测试覆盖分析`
- `OpenHarmony测试`

**平台关键词**：
- `OpenHarmony`
- `ArkTS`
- `ArkUI`
- `ArkWeb`

## 常见问题

### Q1: 生成的测试用例无法编译？

检查 hypium 导入是否正确，查看编译错误日志

### Q2: 测试用例命名不符合规范？

确保使用小驼峰命名（如 `onClickNormal001`），详见：[references/subsystems/_common.md](./references/subsystems/_common.md)

### Q3: 测试设计文档与测试用例不一致？

重新生成测试用例和设计文档，检查版本历史

> 📖 **详细故障排除**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 技能维护者：xts-generator Team
- 文档版本：v1.2.0
- 最后更新：2026-02-12

