# 使用方式详解

> **xts-generator** - 完整使用指南

## 目录

- [一、概述](#一概述)
- [二、使用方式](#二使用方式)
- [三、使用场景](#三使用场景)
- [四、最佳实践](#四最佳实践)
- [五、常见问题](#五常见问题)

---

## 一、概述

xts-generator 提供 3 种使用方式，从简单到复杂，满足不同用户的需求。

### 1.1 使用方式对比

| 使用方式 | 适用场景 | 优点 | 缺点 |
|---------|---------|------|------|
| **方式1：通用模板** | 新手、简单任务 | 简单直接、无需配置 | 无法利用子系统特有规则 |
| **方式2：子系统配置** | 推荐方式、大多数任务 | 利用子系统特有规则、规范统一 | 需要子系统配置文件 |
| **方式3：自定义配置** | 高级用户、特殊需求 | 最大灵活性、完全自定义 | 需要详细配置 |

### 1.2 选择建议

**如果你是新手** → 使用方式1（通用模板）

**如果你熟悉流程** → 使用方式2（子系统配置）【推荐】

**如果你有特殊需求** → 使用方式3（自定义配置）

---

## 二、使用方式

### 方式1：通用模板（推荐新手）

#### 2.1.1 适用场景

- ✅ 新手首次使用
- ✅ 子系统没有配置文件
- ✅ 快速生成测试用例
- ✅ 简单的 API 测试

#### 2.1.2 使用格式

```markdown
请使用 xts-generator 为以下 API 生成测试用例：

子系统: {子系统名称}
API: {API名称}
定义文件: {API声明文件路径}
```

#### 2.1.3 使用示例

**示例1：为 ArkUI Component 生成测试**

```markdown
请使用 xts-generator 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
定义文件: interface/sdk-js/api/@ohos.arkui.d.ts
```

**示例2：为 Audio 模块生成测试**

```markdown
请使用 xts-generator 为以下 API 生成测试用例：

子系统: Multimedia
API: AudioRenderer.create()
定义文件: interface/sdk-js/api/@ohos.multimedia.audio.d.ts
```

**示例3：为 Web 模块生成测试**

```markdown
请使用 xts-generator 为以下 API 生成测试用例：

子系统: ArkWeb
API: Web.runJavaScript()
定义文件: interface/sdk-js/api/@ohos.web.webview.d.ts
```

#### 2.1.4 优缺点

**优点**:
- ✅ 简单直接，无需了解配置系统
- ✅ 适合快速生成测试用例
- ✅ 适合新手入门

**缺点**:
- ❌ 无法利用子系统特有规则
- ❌ 生成的测试用例可能不够优化
- ❌ 需要手动提供 API 声明文件路径

#### 2.1.5 输出说明

使用通用模板时，技能会：
1. 使用通用配置（`references/subsystems/_common.md`）
2. 根据通用规则生成测试用例
3. 应用通用的代码模板
4. **同步生成测试设计文档**：在生成测试用例的同时，生成对应的测试设计文档（`{测试文件名}.design.md`）
   - 包含所有测试场景的详细说明
   - 包含测试步骤和预期结果
   - 包含测试覆盖分析
   - 包含测试环境要求和注意事项

---

### 方式2：子系统配置（推荐）

#### 2.2.1 适用场景

- ✅ 大多数测试生成任务【推荐】
- ✅ 子系统已有配置文件
- ✅ 需要利用子系统特有规则
- ✅ 需要生成符合子系统规范的测试用例

#### 2.2.2 使用格式

```markdown
请使用 xts-generator 为 {子系统名称} 子系统生成测试用例：

子系统: {子系统名称}
配置文件: {配置文件路径}
API: {API名称}
```

#### 2.2.3 使用示例

**示例1：使用 ArkUI 子系统配置**

```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
```

**示例2：使用 ArkWeb 子系统配置**

```markdown
请使用 xts-generator 为 ArkWeb 子系统生成测试用例：

子系统: ArkWeb
配置文件: references/subsystems/ArkWeb/_common.md
API: Web.runJavaScript()
```

**示例3：使用 ArkTS 子系统配置（特殊规则）**

```markdown
请使用 xts-generator 为 ArkTS 子系统生成测试用例：

子系统: ArkTS
配置文件: references/subsystems/ArkTS/_common.md
API: ArkTS 特有语法
```

**说明**: ArkTS 子系统有特殊规则（string 空字符串是合法参数），使用子系统配置可以自动应用这些规则。

#### 2.2.4 配置文件查找

技能会按以下顺序查找配置文件：

1. **用户指定的路径**（如果明确指定）
2. **默认路径**: `references/subsystems/{子系统名称}/_common.md`
3. **通用配置**: `references/subsystems/_common.md`（兜底）

**示例**:
```
子系统: ArkUI

// 技能会查找：
// 1. references/subsystems/ArkUI/_common.md（找到）
// 2. references/subsystems/_common.md（未找到，使用通用配置）
```

#### 2.2.5 优缺点

**优点**:
- ✅ 利用子系统特有规则
- ✅ 生成的测试用例更符合子系统规范
- ✅ 自动应用子系统的特殊规则
- ✅ 配置可重用，提高一致性

**缺点**:
- ❌ 需要子系统配置文件
- ❌ 首次创建配置文件需要一定工作量

#### 2.2.6 输出说明

使用子系统配置时，技能会：
1. 加载通用配置（`references/subsystems/_common.md`）
2. 加载子系统配置（`references/subsystems/{子系统}/_common.md`）
3. 应用子系统特有规则
4. 应用子系统特有代码模板
5. 生成符合子系统规范的测试用例
6. **同步生成测试设计文档**：在生成测试用例的同时，生成对应的测试设计文档（`{测试文件名}.design.md`）
   - 包含所有测试场景的详细说明
   - 包含测试步骤和预期结果
   - 包含测试覆盖分析
   - 包含测试环境要求和注意事项

---

### 方式3：自定义配置

#### 2.3.1 适用场景

- ✅ 高级用户
- ✅ 子系统没有配置文件且不想创建
- ✅ 有特殊的测试需求
- ✅ 需要完全自定义测试生成过程

#### 2.3.2 使用格式

```markdown
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: {子系统名称}
自定义配置:
  Kit包: @kit.{KitName}
  测试路径: {测试路径}
  API声明: {API声明文件路径}
  {其他配置项}

API: {API名称}
```

#### 2.3.3 使用示例

**示例1：自定义测试路径**

```markdown
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: CustomSubsystem
自定义配置:
  Kit包: @kit.CustomKit
  测试路径: test/xts/acts/custom/
  API声明: interface/sdk-js/api/@ohos.custom.d.ts

API: customAPI.method()
```

**示例2：自定义测试规则**

```markdown
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: MySubsystem
自定义配置:
  Kit包: @kit.MyKit
  测试路径: test/xts/acts/mysubsystem/
  API声明: interface/sdk-js/api/@ohos.mysubsystem.d.ts
  特殊规则:
    - string 空字符串是合法参数
    - number 负数会抛出 401

API: myAPI.method()
```

**示例3：完全自定义**

```markdown
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: NewSubsystem
自定义配置:
  Kit包: @kit.NewKit
  测试路径: test/xts/acts/new/
  API声明: interface/sdk-js/api/@ohos.new.d.ts
  测试级别: Level2
  测试类型: Function | Reliability
  代码模板: |
    import { describe, it, expect } from '@ohos/hypium';
    export default function testSuite() {
      describe('My Test', () => {
        it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
          // Test code
        });
      });
    }

API: newAPI.method()
```

#### 2.3.4 自定义配置项

| 配置项 | 类型 | 说明 | 必需 |
|-------|------|------|------|
| `Kit包` | string | 子系统的 Kit 包名 | ✅ |
| `测试路径` | string | 测试用例的存放路径 | ✅ |
| `API声明` | string | API 声明文件的路径 | ✅ |
| `测试级别` | string | 默认测试级别（Level0-Level4） | ❌ |
| `测试类型` | string | 默认测试类型 | ❌ |
| `特殊规则` | list | 子系统特有的测试规则 | ❌ |
| `代码模板` | string | 自定义代码模板 | ❌ |

#### 2.3.5 优缺点

**优点**:
- ✅ 最大灵活性
- ✅ 完全自定义
- ✅ 不需要创建配置文件
- ✅ 适合特殊需求

**缺点**:
- ❌ 配置较为复杂
- ❌ 每次使用都需要指定配置
- ❌ 无法复用配置

#### 2.3.6 输出说明

使用自定义配置时，技能会：
1. 加载通用配置（`references/subsystems/_common.md`）
2. 应用用户指定的自定义配置（覆盖通用配置）
3. 根据自定义配置生成测试用例
4. 应用自定义的代码模板（如果提供）
5. **同步生成测试设计文档**：在生成测试用例的同时，生成对应的测试设计文档（`{测试文件名}.design.md`）
   - 包含所有测试场景的详细说明
   - 包含测试步骤和预期结果
   - 包含测试覆盖分析
   - 包含测试环境要求和注意事项

---

## 三、使用场景

### 3.1 场景1：为新 API 生成测试

**需求**: 为新增的 API 生成完整的测试套件

**推荐方式**: 方式2（子系统配置）

**示例**:
```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onAppear()

要求:
- 生成参数测试
- 生成错误码测试
- 生成返回值测试
```

### 3.2 场景2：补充缺失的测试用例

**需求**: 分析现有测试覆盖情况，补充缺失的测试用例

**推荐方式**: 方式2（子系统配置）+ 覆盖分析

**示例**:
```markdown
请使用 xts-generator 分析 ArkUI 子系统的测试覆盖情况：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
测试套路径: test/xts/acts/arkui/uitest/

要求:
- 分析哪些 API 还没有测试覆盖
- 为未覆盖的 API 生成测试用例
- 输出测试覆盖统计
```

### 3.3 场景3：验证测试代码规范性

**需求**: 检查现有测试代码是否符合 XTS 规范

**推荐方式**: 方式2（子系统配置）+ 规范检查

**示例**:
```markdown
请使用 xts-generator 检查以下测试文件是否符合规范：

测试文件: test/xts/acts/arkui/uitest/Component.test.ets
子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md

要求:
- 检查 @tc 注释块是否完整
- 检查 hypium 导入是否正确
- 检查测试用例命名是否符合规范
- 检查代码风格是否一致
```

### 3.4 场景4：批量生成测试用例

**需求**: 为多个 API 批量生成测试用例

**推荐方式**: 方式2（子系统配置）+ 列表

**示例**:
```markdown
请使用 xts-generator 为以下 API 批量生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md

API 列表:
1. Component.onClick()
2. Component.onAppear()
3. Component.onDisAppear()

要求:
- 为每个 API 生成完整的测试套件
- 统一生成到一个测试文件
```

### 3.5 场景5：为特殊子系统生成测试

**需求**: 为有特殊规则的子系统生成测试用例

**推荐方式**: 方式2（子系统配置）或 方式3（自定义配置）

**示例** (ArkTS 子系统):
```markdown
请使用 xts-generator 为 ArkTS 子系统生成测试用例：

子系统: ArkTS
配置文件: references/subsystems/ArkTS/_common.md
API: ArkTS 特有语法

说明: ArkTS 子系统有特殊规则，string 空字符串是合法参数，不会抛出 401
```

### 3.6 场景6：修复测试用例

**需求**: 修复不符合规范的测试用例

**推荐方式**: 方式2（子系统配置）+ 修复

**示例**:
```markdown
请使用 xts-generator 修复以下测试用例：

测试文件: test/xts/acts/arkui/uitest/Component.test.ets
子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md

问题:
- @tc 注释块不完整
- 测试用例命名使用大写下划线
- 第二个参数使用 0

要求:
- 补充完整的 @tc 注释块
- 修改测试用例命名为小驼峰
- 修改第二个参数为完整格式
```

### 3.7 场景7：生成测试用例和测试设计文档

**需求**: 同时生成测试用例和对应的测试设计文档

**推荐方式**: 方式2（子系统配置）

**说明**: 从 v1.14.0 开始，xts-generator 会自动在生成测试用例的同时生成对应的测试设计文档

**示例**:
```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()

要求:
- 生成完整的测试用例
- 自动生成测试设计文档
```

**输出结果**:
- 测试文件: `test/xts/acts/arkui/uitest/Component.onClick.test.ets`
- 测试设计文档: `test/xts/acts/arkui/uitest/Component.onClick.test.design.md`

**测试设计文档内容**:
- 测试概述（测试对象、测试目标）
- 测试场景设计（所有场景的详细说明）
- 测试覆盖分析（覆盖统计）
- 测试依赖关系
- 测试环境要求
- 注意事项
- 变更记录

---

## 四、最佳实践

### 4.1 使用方式选择

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| 新手首次使用 | 方式1 | 简单直接，无需配置 |
| 大多数任务 | 方式2 | 利用子系统特有规则，规范统一 |
| 特殊需求 | 方式3 | 最大灵活性，完全自定义 |
| 子系统有配置文件 | 方式2 | 直接使用配置，提高效率 |
| 子系统无配置文件 | 方式1 或 方式3 | 根据是否需要自定义选择 |

### 4.2 配置文件管理

#### 创建子系统配置文件

**何时创建**:
- ✅ 需要多次为同一子系统生成测试用例
- ✅ 子系统有特殊的测试规则
- ✅ 子系统包含多个模块

**创建方法**: 参考 [CONFIG.md](./CONFIG.md) 的"创建新子系统配置"章节

#### 维护配置文件

**版本管理**:
- 每次修改都更新版本号和日期
- 在版本历史中记录修改内容

**定期审查**:
- 每月审查一次配置文件
- 根据实际使用情况优化配置

### 4.3 测试用例生成

#### 明确生成需求

**生成前明确**:
- 需要生成哪些 API 的测试用例？
- 需要生成哪些类型的测试？（参数测试、错误码测试、返回值测试）
- 测试级别是什么？（Level0-Level4）
- 是否需要分析测试覆盖情况？

**示例**:
```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()

要求:
- 生成参数测试（正常值、边界值）
- 生成错误码测试（401, 202, 201）
- 测试级别: Level3
- 测试类型: Function
```

#### 参考已有用例

**生成前参考**:
- 查看测试套中已有的测试用例
- 分析代码风格和规范
- 确保新生成的用例与已有用例一致

**示例**:
```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
已有用例路径: test/xts/acts/arkui/uitest/

要求:
- 参考已有用例的代码风格
- 保持代码风格一致
```

### 4.4 输出验证

#### 编译验证

**生成后必须编译**:
- 检测运行环境（Linux/Windows）
- 根据环境选择编译方案
- 执行编译命令
- 处理编译错误

**Linux 环境**:
```bash
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=test_name
```

**Windows 环境**:
```bash
hvigorw.bat --mode module -p product=default assembleHap
```

#### 代码审查

**生成后审查**:
- ✅ 检查 @tc 注释块是否完整
- ✅ 检查 hypium 导入是否正确
- ✅ 检查测试用例命名是否符合规范
- ✅ 检查代码风格是否一致
- ✅ 检查测试逻辑是否正确

---

## 五、常见问题

### Q1: 哪种使用方式最好？

**A**: 没有绝对的"最好"，只有"最适合"：

- **新手**：推荐方式1（通用模板）
- **大多数情况**：推荐方式2（子系统配置）【推荐】
- **特殊需求**：推荐方式3（自定义配置）

**建议**：如果子系统有配置文件，优先使用方式2。

### Q2: 如何指定测试套路径？

**A**: 在使用方式中添加"测试套路径"参数：

```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
测试套路径: test/xts/acts/arkui/uitest/
```

### Q3: 如何分析测试覆盖情况？

**A**: 添加"测试覆盖分析"要求：

```markdown
请使用 xts-generator 分析 ArkUI 子系统的测试覆盖情况：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
测试套路径: test/xts/acts/arkui/uitest/

要求:
- 分析测试覆盖情况
- 输出测试覆盖统计
- 输出覆盖率对比
```

### Q4: 如何修复已有测试用例？

**A**: 指定测试文件和修复要求：

```markdown
请使用 xts-generator 修复以下测试用例：

测试文件: test/xts/acts/arkui/uitest/Component.test.ets
子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md

问题:
- @tc 注释块不完整
- 测试用例命名不符合规范

要求:
- 修复所有问题
- 保持测试逻辑不变
```

### Q5: 如何为多个 API 批量生成测试用例？

**A**: 提供 API 列表：

```markdown
请使用 xts-generator 为以下 API 批量生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md

API 列表:
1. Component.onClick()
2. Component.onAppear()
3. Component.onDisAppear()

要求:
- 为每个 API 生成完整的测试套件
- 统一生成到一个测试文件
```

### Q6: 生成的测试用例在哪里？

**A**: 取决于你的测试套路径：

- **默认路径**: `test/xts/acts/{子系统}/{测试套}/`
- **指定路径**: 使用时指定的"测试套路径"

**示例**:
```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
测试套路径: test/xts/acts/arkui/uitest/  // 测试用例将生成到这里
```

### Q7: 如何指定测试级别和测试类型？

**A**: 在使用方式中添加"测试级别"和"测试类型"参数：

```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
测试级别: Level3  // Level0, Level1, Level2, Level3, Level4
测试类型: Function  // Function, Performance, Reliability, Security
```

### Q8: 如何指定生成哪些类型的测试？

**A**: 在"要求"中明确说明：

```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()

要求:
- 生成参数测试（正常值、边界值、空值）
- 生成错误码测试（401, 202, 201）
- 生成返回值测试
```

### Q9: 如何确保生成的测试用例符合规范？

**A**:

1. **使用子系统配置**（方式2）：自动应用子系统特有规则
2. **参考已有用例**：指定"已有用例路径"，让技能参考
3. **编译验证**：生成后必须编译，检查是否有错误
4. **代码审查**：生成后审查代码，确保符合规范

**示例**:
```markdown
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
已有用例路径: test/xts/acts/arkui/uitest/

要求:
- 参考已有用例的代码风格
- 确保符合 XTS 规范
- 生成后进行编译验证
```

### Q10: 如果子系统没有配置文件怎么办？

**A**: 有两种选择：

**选项1：使用通用模板（方式1）**
```markdown
请使用 xts-generator 为以下 API 生成测试用例：

子系统: NewSubsystem
API: newAPI.method()
定义文件: interface/sdk-js/api/@ohos.newsubsystem.d.ts
```

**选项2：使用自定义配置（方式3）**
```markdown
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: NewSubsystem
自定义配置:
  Kit包: @kit.NewKit
  测试路径: test/xts/acts/newsubsystem/
  API声明: interface/sdk-js/api/@ohos.newsubsystem.d.ts

API: newAPI.method()
```

**选项3：创建子系统配置文件**（推荐长期使用）
参考 [CONFIG.md](./CONFIG.md) 的"创建新子系统配置"章节

---

## 附录

### A. 快速参考

#### 使用方式对比

| 使用方式 | 适用场景 | 配置需求 | 灵活性 |
|---------|---------|---------|-------|
| **方式1：通用模板** | 新手、简单任务 | 无 | 低 |
| **方式2：子系统配置** | 大多数任务 | 子系统配置文件 | 中 |
| **方式3：自定义配置** | 高级用户、特殊需求 | 每次使用时指定 | 高 |

#### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `子系统` | 子系统名称 | `ArkUI`, `ArkWeb`, `Multimedia` |
| `配置文件` | 配置文件路径 | `references/subsystems/ArkUI/_common.md` |
| `API` | API 名称 | `Component.onClick()` |
| `定义文件` | API 声明文件 | `interface/sdk-js/api/@ohos.arkui.d.ts` |
| `测试套路径` | 测试套路径 | `test/xts/acts/arkui/uitest/` |
| `测试级别` | 测试级别 | `Level0`, `Level1`, `Level2`, `Level3`, `Level4` |
| `测试类型` | 测试类型 | `Function`, `Performance`, `Reliability`, `Security` |
| **测试设计文档** | **测试设计文档生成（v1.14.0+ 自动生成）** | **自动生成 `{测试文件名}.design.md`** |

### B. 示例模板

#### 模板1：简单测试生成

```markdown
请使用 xts-generator 为以下 API 生成测试用例：

子系统: {子系统名称}
API: {API名称}
定义文件: {API声明文件路径}
```

#### 模板2：使用子系统配置

```markdown
请使用 xts-generator 为 {子系统名称} 子系统生成测试用例：

子系统: {子系统名称}
配置文件: references/subsystems/{子系统名称}/_common.md
API: {API名称}
```

#### 模板3：自定义配置

```markdown
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: {子系统名称}
自定义配置:
  Kit包: @kit.{KitName}
  测试路径: {测试路径}
  API声明: {API声明文件路径}

API: {API名称}
```

#### 模板4：完整需求

```markdown
请使用 xts-generator 为 {子系统名称} 子系统生成测试用例：

子系统: {子系统名称}
配置文件: references/subsystems/{子系统名称}/_common.md
API: {API名称}
测试套路径: {测试套路径}
已有用例路径: {已有用例路径}

要求:
- 生成参数测试（正常值、边界值）
- 生成错误码测试（401, 202, 201）
- 测试级别: Level3
- 测试类型: Function
- 参考已有用例的代码风格
- 生成后进行编译验证
- 输出测试覆盖统计
```

---

## 版本更新记录

### v1.14.0 (2026-02-10)

**新增功能**：
- ✅ 测试设计文档自动生成
  - 在生成测试用例的同时自动生成对应的测试设计文档
  - 测试设计文档命名：`{测试文件名}.design.md`
  - 包含测试概述、测试场景设计、测试覆盖分析等完整内容

**使用说明**：
- 测试设计文档生成是自动的，无需额外配置
- 测试设计文档与测试用例保持同步更新
- 详见：`modules/L3_Generation/design_doc_generator.md`

---

**文档版本**: 1.1.0
**创建日期**: 2026-02-05
**最后更新**: 2026-02-10
**维护者**: xts-generator Team
