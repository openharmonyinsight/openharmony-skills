# 文档阅读器

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载
> - 适用范围：文档阅读和分析
> - 依赖：无

---

## 一、模块概述

文档阅读器用于阅读和分析 OpenHarmony 官方文档，包括 API Reference、开发指南、测试指南等，为测试用例生成提供准确的参考信息。

---

## 二、文档位置

### 2.1 API Reference（API 参考）

```
位置: docs/zh-cn/application-dev/reference/

按子系统组织：
- apis-arkdata/    # 数据相关 API
- apis-network/    # 网络相关 API
- apis-file/       # 文件相关 API
- apis-ui/         # UI 相关 API
- ...
```

### 2.2 开发指南

```
位置: docs/zh-cn/application-dev/[子系统名]/

示例：
- ui/              # UI 开发指南
- database/        # 数据库开发指南
- network/         # 网络开发指南
- security/        # 安全开发指南
```

### 2.3 测试指南

```
位置: docs/zh-cn/application-dev/application-test/

关键文档：
- unittest-guidelines.md     # 单元测试指南
- uitest-guidelines.md       # UI 测试指南
- perftest-guideline.md      # 性能测试指南
- wukong-guidelines.md       # Wukong 测试框架指南
```

---

## 三、API Reference 阅读策略

### 3.1 查找目标 API 文档

```bash
# 方法1：按模块名搜索
find docs/ -name "*util*" -type f

# 方法2：按 API 名称搜索
grep -r "TreeSet" docs/zh-cn/application-dev/reference/

# 方法3：按子系统搜索
ls docs/zh-cn/application-dev/reference/apis-arkdata/
```

### 3.2 API 文档结构

典型的 API Reference 文档结构：

```markdown
# [API 名称]

## 简介
[功能概述]

## 模块
[导入方式]

## 子系统
[所属子系统]

## 系统要求
[最低系统版本]

## 接口说明

### [方法/属性名称]

[功能描述]

**参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ... | ... | ... | ... |

**返回值**：
| 类型 | 说明 |
|------|------|
| ... | ... |

**错误码**：
| 错误码 | 说明 |
|--------|------|
| 401 | 参数无效 |
| ... | ... |

**示例**：
```ts
// 示例代码
```
```

### 3.3 提取关键信息

从 API Reference 中提取：

1. **API 功能说明**：理解 API 的用途
2. **参数详细说明**：参数的含义、取值范围、约束条件
3. **错误码含义**：每个错误码的触发条件和处理建议
4. **使用示例**：官方提供的代码示例和最佳实践
5. **版本要求**：API 的版本限制、兼容性说明
6. **依赖关系**：与其他 API 或模块的关系

---

## 四、开发指南阅读策略

### 4.1 查找子系统开发指南

```bash
# 查找所有子系统目录
ls docs/zh-cn/application-dev/

# 常见子系统
ui/          # UI 组件
database/    # 数据存储
network/     # 网络通信
security/    # 安全能力
dfx/         # 诊断与调试
```

### 4.2 开发指南内容

开发指南通常包含：

1. **概述**：子系统的功能、架构、使用场景
2. **开发流程**：如何使用该子系统进行开发
3. **API 使用指导**：子系统内 API 的使用方法和注意事项
4. **示例代码**：完整的使用示例和代码片段
5. **常见问题**：开发过程中的常见问题和解决方案

---

## 五、测试指南阅读策略

### 5.1 单元测试指南

文件：`unittest-guidelines.md`

关键内容：
- 测试框架使用方法
- 测试用例编写规范
- 测试最佳实践
- 常见问题解决方案

### 5.2 UI 测试指南

文件：`uitest-guidelines.md`

关键内容：
- UiTest 框架使用
- 组件测试方法
- 事件测试方法
- 页面跳转测试

---

## 六、文档使用流程

### 6.1 完整流程

```
输入：API 名称
  ↓
步骤1：解析 .d.ts 文件
  - 获取接口定义、方法签名、参数类型
  ↓
步骤2：查找 API Reference 文档
  - 获取 API 详细说明、参数约束、错误码
  ↓
步骤3：查阅测试指南
  - 获取测试用例编写规范
  ↓
步骤4：综合信息生成测试用例
  - 结合 .d.ts 类型定义
  - 参考 API Reference 功能说明
  - 遵循测试指南规范
```

### 6.2 冲突处理

当 `.d.ts` 定义和 `docs` 文档描述存在冲突时：

1. **向用户确认**：不应自行推测或假定哪个来源更准确
2. **记录差异**：明确指出冲突点
3. **等待确认**：在用户明确指示之前，暂停生成

---

## 七、文档信息提取模板

### 7.1 API 信息提取

```markdown
# API 信息提取表

## 基本信息
- API 名称:
- 子系统:
- 模块:
- Kit:

## 功能说明
- 功能描述:
- 使用场景:
- 版本要求:

## 接口定义
- 方法名:
- 参数列表:
  - 参数名: 类型 | 约束 | 必填/可选
- 返回值类型:
- 是否异步:

## 错误码
- 错误码: 触发条件
- ...

## 使用示例
[官方示例代码]

## 注意事项
- 特殊约束:
- 兼容性问题:
- 已知限制:
```

---

## 八、快速参考

### 8.1 文档查找命令

```bash
# 查找 API 文档
find docs/zh-cn/application-dev/reference/ -name "*[API名称]*"

# 查找子系统指南
ls docs/zh-cn/application-dev/ | grep [子系统名]

# 搜索特定内容
grep -r "[关键词]" docs/zh-cn/application-dev/
```

### 8.2 常用文档路径

```
# API Reference
docs/zh-cn/application-dev/reference/apis-arkdata/js-apis-util.md
docs/zh-cn/application-dev/reference/apis-network/js-apis-http.md

# 开发指南
docs/zh-cn/application-dev/ui/
docs/zh-cn/application-dev/database/

# 测试指南
docs/zh-cn/application-dev/application-test/unittest-guidelines.md
docs/zh-cn/application-dev/application-test/uitest-guidelines.md
```
