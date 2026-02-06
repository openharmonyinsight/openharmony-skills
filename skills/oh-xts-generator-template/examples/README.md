# 子系统配置示例

> **oh-xts-generator-template 子系统配置示例集合**

## 示例列表

### 1. ArkTS 子系统

**文件**: [arkts_subsystem.md](./arkts_subsystem.md)

**说明**: ArkTS（ArkUI编程语言）子系统配置

**关键特性**:
- 包含 ArkTS 编译错误级别规则（70+ 条规则）
- 明确 ArkTS 不支持的语法特性
- ArkTS 特有测试规则和代码模板

**参考**: `references/subsystems/ArkTS/_common.md`

### 2. ArkUI 子系统

**文件**: [arkui_subsystem.md](./arkui_subsystem.md)

**说明**: ArkUI（UI框架）子系统配置

**关键特性**:
- API Kit 映射: @kit.ArkUI
- 测试路径: test/xts/acts/arkui/
- 模块映射: Component, Animator, Router

**参考**: `references/subsystems/ArkUI/_common.md`

### 3. ArkWeb 子系统

**文件**: [arkweb_subsystem.md](./arkweb_subsystem.md)

**说明**: ArkWeb（Web组件）子系统配置

**关键特性**:
- API Kit 映射: @kit.ArkWeb
- 测试路径: test/xts/acts/arkweb/
- 模块映射: Web, WebViewController

**参考**: `references/subsystems/ArkWeb/_common.md`

## 如何使用这些示例

### 方式1: 参考示例创建新子系统配置

1. 查看最接近的子系统配置
2. 复制其结构
3. 根据你的子系统特性修改配置

### 方式2: 直接使用子系统配置

在调用技能时指定配置文件：

```
请使用 oh-xts-generator-template 生成测试用例：

子系统: MySubsystem
配置文件: references/subsystems/MySubsystem/_common.md
API: myAPI.method()
```

### 方式3: 学习配置模式

查看各个子系统的配置示例，学习如何：
- 组织配置结构
- 定义测试规则
- 创建代码模板
- 处理特殊情况

## 配置模板

### 子系统通用配置模板

```markdown
# {子系统名称} 子系统通用配置

> **子系统信息**
> - 名称: {子系统英文名}
> - Kit包: @kit.{KitName}
> - 测试路径: test/xts/acts/{子系统}/
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、子系统通用配置

### 1.1 API Kit 映射
### 1.2 测试路径规范
### 1.3 模块映射配置

## 二、子系统通用测试规则

## 三、已知问题和注意事项

## 四、参考示例
```

## 配置最佳实践

1. **保持结构一致**: 遵循统一的配置结构
2. **明确特殊规则**: 在配置中明确子系统的特殊规则
3. **提供示例**: 包含具体的配置和使用示例
4. **版本管理**: 在文件头部记录版本和更新日期

## 相关文档

- **通用配置**: [references/subsystems/_common.md](../references/subsystems/_common.md)
- **主技能文件**: [../SKILL.md](../SKILL.md)
- **架构文档**: [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)
