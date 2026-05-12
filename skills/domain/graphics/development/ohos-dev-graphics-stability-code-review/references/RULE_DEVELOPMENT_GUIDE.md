# 规则开发指南

## 核心流程

```
定义规则需求 → 创建规则文档 → 更新配置 → 测试验证 → 持续改进
```

---

## 第一步：定义规则需求

明确以下信息：

- **规则 ID**: `StabilityCodeReview_XXX_YYY`（XXX为分类英文缩写，YYY为序号）
- **规则名称**: 一句话描述稳定性问题，简洁明确
- **分类**: 异常处理/并发稳定性/资源管理/边界条件/图形稳定性
- **严重程度**: CRITICAL/HIGH/MEDIUM/LOW（详见下方严重程度定义）
- **检测需求**: 详细描述要检测的稳定性风险场景，包括：
  - 问题触发条件
  - 影响范围
  - 实际项目中的常见错误模式
  - 参考的实际代码函数/类名/常量值

### 严重程度定义

| 等级 | 定义 | 适用场景 | 典型后果 |
|------|------|----------|----------|
| **CRITICAL** | 极高风险，可能导致系统崩溃、安全漏洞，必须立即修复 | Parcel数据安全风险、内存越界访问、数组越界 | 程序崩溃（SIGSEGV）、安全漏洞、内存损坏、未定义行为 |
| **HIGH** | 高风险，可能导致服务中断、资源耗尽、严重稳定性问题 | 内存泄漏、资源泄漏、GPU资源管理问题、引用计数错误、反序列化内存泄漏、JSON解析安全风险 | OOM、资源耗尽、服务中断、性能严重退化、GPU崩溃 |
| **MEDIUM** | 中等风险，可能导致功能异常、数据错误，但不直接导致崩溃 | 编码规范违规、类型转换问题、JSON处理不当、异常处理机制、数据成员未初始化 | 功能异常、数据错误、性能轻微退化、未定义值 |
| **LOW** | 低风险，代码质量问题，建议改进 | 编码风格问题、性能优化建议、可维护性问题 | 代码可读性差、维护成本高 |

---

## 第二步：创建规则文档

在 `references/分类名称/` 目录下创建规则文档：

```
references/BoundaryCondition/StabilityCodeReview_BoundaryCondition_XXX.md
```

按 [RULE_TEMPLATE.md](RULE_TEMPLATE.md) 格式编写文档，必须包含以下章节：

### 1. 基本信息（YAML Front Matter）

```yaml
---
rule_id: "StabilityCodeReview_BoundaryCondition_XXX"
name: "规则名称"
category: "边界条件"
severity: "CRITICAL"  # 根据风险等级选择
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---
```

### 2. 问题描述

**要求**：
- 第一句话描述问题及其危害（必须）
- 可选补充详细背景说明（如OpenHarmony特定要求）
- 可选补充实际项目中的常见错误模式

**示例**：
```markdown
## 问题描述

从Parcel中读取的数据不可信，不能直接作为循环或递归的条件，必须进行上限保护处理。恶意构造的Parcel数据可能包含超大数值，导致死循环、栈溢出或拒绝服务攻击。

OpenHarmony禁止使用C++异常处理机制（try/catch/throw）。异常处理机制会引入运行时开销和代码膨胀，影响系统稳定性和性能。
```

### 3. 检测示例

**必须包含5-10个问题场景**：

- 每个场景用注释标注具体问题
- 覆盖常见变体和实际代码模式
- 使用实际项目中的函数名、常量值增强真实性

**示例结构**：
```cpp
// ❌ 问题代码
// 场景1：{具体问题描述，如"Parcel数据直接作为循环条件"}
void ReadDataFromParcel(Parcel& parcel)
{
    int count = parcel.ReadInt32();  // 不可信数据
    for (int i = 0; i < count; i++) {  // 危险：count可能为超大值
        ProcessItem(parcel);
    }
}

// 场景2：{具体问题描述}
// 场景3：{具体问题描述}
// ...提供5-10个场景
```

**必须包含5-10个修复方案**：

- 包括最佳实践、RAII模式
- 参考实际代码中的标准写法
- 使用真实函数名、日志函数、常量值

**示例结构**：
```cpp
// ✅ 修复方案
// 修复场景1：{修复方法说明，如"添加上限保护"}
constexpr int MAX_ITEM_COUNT = 1000;  // 实际项目中常用的常量值

void ReadDataFromParcel(Parcel& parcel)
{
    int count = parcel.ReadInt32();
    if (count < 0 || count > MAX_ITEM_COUNT) {  // 安全：有上限保护
        ROSEN_LOGE("Invalid count: %d", count);  // 实际项目使用的日志函数
        return;
    }
    for (int i = 0; i < count; i++) {
        ProcessItem(parcel);
    }
}

// 修复场景2：使用RAII模式（推荐）
// 修复场景3：使用智能指针
// ...提供5-10个修复方案
```

### 4. 检测范围

**要求**：
- 清晰列出要检查的目标（API、函数、模式）
- 编号列表，便于理解
- 具体到函数名、关键字、模式

**示例**：
```markdown
## 检测范围

检查以下模式：

1. 从Parcel读取数据后直接用于`for`循环
2. 从Parcel读取数据后直接用于`while`循环
3. 从Parcel读取数据后直接用于递归终止条件
4. 从Parcel读取数据后用于嵌套循环控制
5. Parcel.ReadInt32/ReadInt64/ReadUint32/ReadUint64等读取函数
```

### 5. 检测要点

**必须包含**：
- 基本检测步骤（5条）
- 误报排除方法

**可选扩展章节**（根据规则特点添加）：

#### 最佳实践说明

针对复杂技术点提供最佳实践：

- **推荐方式1**：说明适用场景和示例
- **推荐方式2**：说明适用场景和示例

**示例**（BoundaryCondition_001）：
```markdown
### 动态上限vs常量上限

实际代码中常用两种上限保护方式：

- **动态上限**：使用Parcel.GetReadableBytes()获取实际可读大小
  - 示例：`if (len > readableSize || len > payload_.max_size())`
  - 适用场景：数据大小可变、需要精确控制
  
- **常量上限**：使用constexpr定义固定上限
  - 示例：`constexpr int MAX_ITEM_COUNT = 1000;`
  - 适用场景：固定大小限制、简单场景
```

#### 实际代码参考

引用实际项目中的具体元素：

- **实际常量值**：MAX_NESTING_DEPTH = 800
- **实际函数名**：RSCanvasDrawingRenderNodeDrawable::CreateGpuSurface
- **实际日志函数**：ROSEN_LOGE(), RS_LOGE()
- **实际项目路径**：rosen/modules/render_service/

**示例**（BoundaryCondition_001）：
```markdown
### 动态上限vs常量上限

实际代码中常用两种上限保护方式：

- **动态上限**：使用Parcel.GetReadableBytes()获取实际可读大小
  - 示例：`if (len > readableSize || len > payload_.max_size())`
  - 适用场景：数据大小可变、需要精确控制
  
- **常量上限**：使用constexpr定义固定上限
  - 示例：`constexpr int MAX_ITEM_COUNT = 1000;`
  - 适用场景：固定大小限制、简单场景
```

#### 特殊技术说明

针对复杂技术提供详细说明：

- **Parcel数据处理规范**（边界条件）
- **GPU资源管理**（图形稳定性）
- **C++11/20特性**（容器find、初始化）
- **JSON处理安全**（边界条件）
- **VulkanCleanupHelper引用计数**（图形稳定性）

**示例**（BoundaryCondition_007）：
```markdown
### Parcel序列化与反序列化匹配检查

#### 序列化顺序必须与反序列化顺序完全一致

- **基本原则**：WriteXXX和ReadXXX必须严格对应
  - 类型匹配：WriteInt32必须对应ReadInt32
  - 数量匹配：序列化N个对象，反序列化也必须N个
  - 顺序匹配：先序列化的数据必须先反序列化
  
- **常见错误**：
  - 类型不匹配：WriteInt32后使用ReadInt64
  - 顺序错乱：先WriteString后WriteInt32，但反序列化顺序相反
  - 数量不匹配：序列化3个对象，反序列化只读2个
```

#### 分类处理策略

针对不同场景提供不同处理方式：

**示例**（GraphicsStability_005）：
```markdown
### GPU操作线程限制

根据线程职责选择不同的操作策略：

- **RS主线程**：禁止执行任何GPU Context操作
  - 禁止：MakeFromBackendTexture、DeleteVkImage等
  - 允许：abandonedContext()、purgeCache()等特殊清理操作
  
- **RSUniRenderThread**：可以执行GPU操作
  - 允许：创建Surface、释放Image、GetBackendTexture等
  - 注意：必须在正确的线程执行
  
- **线程检测方法**：
  - 检查调用函数是否在RSMainThread::Process()中
  - 检查是否有OHOS::Rosen::RSMainThread标识
```

### 6. 风险流分析（RiskFlow）

**必须包含完整的风险流**：

```markdown
- RISK_SOURCE: {具体到代码元素，如"Parcel读取的不可信数据"}
- RISK_TYPE: {具体风险类型，如"边界条件缺失、空指针解引用"}
- RISK_PATH: {完整传播路径，如"不可信数据 -> 循环条件 -> 无限循环/栈溢出"}
- IMPACT_POINT: {最终影响，如"系统资源耗尽、拒绝服务"}
```

**要求**：
- 具体到代码元素（函数、API、变量）
- 描述完整的传播路径
- 说明最终影响系统稳定性的点

### 7. 影响分析（ImpactAnalysis）

**必须包含完整的影响分析**：

```markdown
- Trigger: {具体触发条件，如"使用Parcel数据作为循环条件"}
- Propagation: {具体传播方式，如"恶意构造超大数值导致无限循环"}
- Consequence: {具体后果，如"CPU资源耗尽、栈溢出、系统崩溃"}
- Mitigation: {具体缓解方案，如"添加数值上限检查，限制循环次数"}
```

**要求**：
- 触发条件要具体（什么代码、什么数据）
- 传播方式要说明机制
- 后果要具体（崩溃、资源耗尽、性能下降等）
- 缓解方案要具体可行

### 8. 误报排除

**必须包含误报排除表格**：

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有安全防护 | {具体识别方法} | 不报 |
| 使用最佳实践 | {具体识别方法} | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录 | 自动跳过 |

**要求**：
- 至少包含NOPROTECT、第三方库、测试代码的排除
- 针对规则特点添加具体的误报场景
- 识别特征要明确（注释、路径、代码模式）

### 9. 测试用例

**触发用例要求**：
- 提供5-10个触发用例
- 覆盖典型错误模式和边界情况
- 每个用例用注释标注应该触发的原因

**安全用例要求**：
- 提供5-10个安全用例
- 覆盖正确做法和误报排除场景
- 包含NOPROTECT标记的用例
- 包含最佳实践的用例

---

## 第三步：更新配置

在 `config/rules.yaml` 中添加规则配置：

```yaml
边界条件:
  name: 边界条件
  description: 检测边界条件处理不当导致的稳定性风险
  enabled: true
  rules:
    StabilityCodeReview_BoundaryCondition_XXX:
      enabled: true
      id: StabilityCodeReview_BoundaryCondition_XXX
      name: Parcel数据不可作为循环条件
      severity: HIGH  # 根据实际严重程度设置
      description: Parcel数据不可信，不能直接作为循环条件
      reference: 边界条件/StabilityCodeReview_BoundaryCondition_XXX.md
```

---

## 第四步：更新文档

新增规则后，需同步更新以下文档：

- **README.md**：更新规则总数和分类统计
- **SKILL.md**：更新"核心概念-稳定性分类"表格中的规则数量
- **references/RULE_INDEX.md**：添加新规则到规则索引

---

## 第五步：验证规则有效性

使用 Agent 检视代码验证规则有效性：

1. 选择包含目标问题模式的代码文件或目录
2. 使用新增规则对代码进行检视
3. 验证规则是否能准确检出问题
4. 检查是否存在误报或漏报
5. 根据验证结果优化规则文档

---

## 第六步：持续改进

根据实际使用反馈持续改进：

1. 收集误报案例，完善误报排除表格
2. 收集漏报案例，扩展检测范围和要点
3. 更新实际代码参考，增强真实性
4. 补充新发现的错误模式和修复方案

---

## 规则编写最佳实践

### 1. 代码示例质量

**问题代码要求**：
- 每个场景用注释标注具体问题（`// 错误：xxx` 或 `// 危险：xxx`）
- 使用实际项目中的函数名、类名（如Parcel、Drawing::Surface）
- 覆盖常见变体和实际错误模式
- 提供5-10个场景，全面覆盖问题

**修复方案要求**：
- 参考实际项目中的标准写法
- 使用真实的常量值（如MAX_NESTING_DEPTH = 800）
- 使用真实的日志函数（如ROSEN_LOGE()）
- 包含RAII、智能指针等最佳实践
- 提供5-10个修复方案

### 2. 检测要点深度

**基本检测步骤**：
- 如何识别目标代码模式
- 如何检查问题
- 如何判断风险
- 如何排除误报
- 特殊情况处理

**扩展说明章节**（根据规则特点添加）：
- 最佳实践说明（memory_order、thread_local等）
- 实际代码参考（函数名、常量值、项目路径）
- 特殊技术说明（C++11/20特性、POD类型等）
- 分类处理策略（不同场景不同处理）

### 3. 风险流和影响分析

**风险流要求**：
- RISK_SOURCE具体到代码元素（函数、API、变量）
- RISK_TYPE使用标准术语（空指针解引用、UAF、数据竞争等）
- RISK_PATH描述完整传播路径
- IMPACT_POINT说明最终影响

**影响分析要求**：
- Trigger具体触发条件
- Propagation传播机制
- Consequence具体后果（崩溃、OOM等）
- Mitigation具体缓解方案

### 4. 误报排除完善

**必须包含的排除场景**：
- NOPROTECT标记
- 第三方库路径
- 测试代码路径
- 已有安全防护

**规则特有的排除场景**：
- 使用最佳实践（智能指针、RAII等）
- 使用新特性（C++11/20）
- 特殊业务场景

### 5. 实际性增强

**引用实际项目元素**：
- 实际函数名：RSCanvasDrawingRenderNodeDrawable::CreateGpuSurface
- 实际类名：NativeBufferUtils::VulkanCleanupHelper
- 实际常量：MAX_NESTING_DEPTH, RECORD_CMD_MAX_DEPTH
- 实际日志：ROSEN_LOGE(), RS_LOGE()
- 实际项目路径：rosen/modules/render_service/

**参考实际代码模式**：
- Marshalling/Unmarshalling深度检查模式
- Visitor模式替代传统递归
- memory_order精确控制
- 动态上限vs常量上限

---

## 分类规则编写要点

### 异常处理 (ExceptionHandling)

**特点**：
- OpenHarmony禁止异常处理机制
- 使用错误码返回值替代
- 需说明编码规范要求

**检测重点**：
- try/catch/throw关键字检测
- 错误码返回值使用模式
- 异常分支处理正确性

### 并发稳定性 (ConcurrencyStability)

**特点**：
- 线程安全、数据竞争、竞态条件
- RenderNodeDrawable全局变量写入风险
- 需要说明thread_local最佳实践

**扩展说明**：
- thread_local最佳实践
- 全局变量线程安全处理
- RenderNodeDrawable线程限制

### 资源管理 (ResourceManagement)

**特点**：
- 内存泄漏、资源泄漏
- 反序列化、动态库加载
- 需要强调RAII、智能指针

**最佳实践**：
- 使用std::unique_ptr、std::shared_ptr
- 使用std::make_unique、std::make_shared
- 构造函数初始化列表
- 异常分支清理

### 边界条件 (BoundaryCondition)

**特点**：
- Parcel数据安全、不可信数据
- 容器find未检查、数组越界
- 动态上限vs常量上限

**扩展说明**：
- 动态上限vs常量上限（GetReadableBytes() vs constexpr）
- 实际常量值（MAX_ITEM_COUNT = 1000）
- contains()替代find()（C++20）
- 链式find逐层检查

### 图形稳定性 (GraphicsStability)

**特点**：
- GPU资源管理、引用计数
- VulkanCleanupHelper、VkImage
- 线程角色混乱

**扩展说明**：
- VulkanCleanupHelper引用计数管理（首次vs后续）
- DeleteVkImage函数指针
- GPU资源UAF风险
- RS主线程限制

---

## 规则文档完整性检查清单

创建规则文档后，使用以下清单验证完整性：

### 基本信息检查
- [ ] YAML Front Matter包含所有必需字段
- [ ] 规则ID格式正确（StabilityCodeReview_XXX_YYY）
- [ ] 严重程度根据风险等级正确设置
- [ ] 分类正确

### 问题描述检查
- [ ] 第一句话描述问题及危害
- [ ] 可选补充详细背景说明
- [ ] 可选补充实际项目常见错误模式

### 检测示例检查
- [ ] 问题代码包含5-10个场景
- [ ] 每个场景用注释标注具体问题
- [ ] 使用实际项目函数名、类名
- [ ] 修复方案包含5-10个方案
- [ ] 参考实际项目标准写法
- [ ] 包含RAII、智能指针等最佳实践

### 检测范围检查
- [ ] 清晰列出检测目标（编号列表）
- [ ] 具体到函数名、关键字、模式

### 检测要点检查
- [ ] 包含基本检测步骤（5条）
- [ ] 包含误报排除方法
- [ ] 根据规则特点添加扩展说明章节：
  - [ ] 最佳实践说明（memory_order、thread_local等）
  - [ ] 实际代码参考（函数名、常量值）
  - [ ] 特殊技术说明（C++11/20特性等）
  - [ ] 分类处理策略

### 风险流和影响分析检查
- [ ] RiskFlow包含4个必需字段
- [ ] 具体到代码元素，描述完整路径
- [ ] ImpactAnalysis包含4个必需字段
- [ ] 触发条件、传播机制、后果、缓解方案具体

### 误报排除检查
- [ ] 包含误报排除表格
- [ ] 至少包含NOPROTECT、第三方库、测试代码
- [ ] 针对规则特点添加具体误报场景
- [ ] 识别特征明确

### 测试用例检查
- [ ] 触发用例包含5-10个
- [ ] 覆盖典型错误模式和边界情况
- [ ] 安全用例包含5-10个
- [ ] 覆盖正确做法和误报排除
- [ ] 包含NOPROTECT标记用例
- [ ] 包含最佳实践用例

---

## 规则编写常见问题

### 问题1：代码示例不够实际

**解决方案**：
- 参考实际项目代码，使用真实的函数名、类名
- 使用实际项目中的常量值（MAX_NESTING_DEPTH = 800）
- 使用实际项目的日志函数（ROSEN_LOGE()）
- 添加"实际代码参考"章节

### 问题2：检测要点不够深入

**解决方案**：
- 根据规则特点添加扩展说明章节
- 详细说明技术细节（memory_order、thread_local等）
- 提供分类处理策略
- 说明最佳实践模式

### 问题3：风险流不够具体

**解决方案**：
- RISK_SOURCE具体到代码元素（函数、API、变量）
- RISK_TYPE使用标准术语
- RISK_PATH描述完整传播路径，不跳过中间步骤
- IMPACT_POINT说明最终影响（崩溃、OOM等）

### 问题4：误报排除不够完善

**解决方案**：
- 至少包含NOPROTECT、第三方库、测试代码
- 添加规则特有的误报场景
- 明确识别特征（注释、路径、代码模式）
- 使用表格形式，便于AI理解

### 问题5：缺少最佳实践说明

**解决方案**：
- 添加"最佳实践说明"章节
- 说明推荐方式和适用场景
- 提供代码片段示例
- 说明性能、安全性等方面的考虑

---

## 规则文档模板使用指南

### 必需章节（不可省略）

1. YAML Front Matter
2. 问题描述（至少一句话）
3. 检测示例（至少5个问题场景+5个修复方案）
4. 检测范围
5. 检测要点（至少5条）
6. 风险流分析
7. 影响分析
8. 误报排除表格
9. 测试用例（至少5个触发+5个安全）

### 可选章节（根据规则特点添加）

1. 问题描述中的详细背景说明
2. 检测要点中的扩展说明章节：
   - 最佳实践说明
   - 实际代码参考
   - 特殊技术说明
   - 分类处理策略
3. 更多的代码示例场景（10+）

### 建议的代码示例数量

- **简单规则**：5个问题场景 + 5个修复方案
- **复杂规则**：10个问题场景 + 10个修复方案
- **涉及多场景的规则**：覆盖所有主要场景，每个场景至少1个示例

---

## 总结

编写高质量规则文档的关键：

1. **实际性**：使用真实的项目函数名、常量值、日志函数
2. **完整性**：包含所有必需章节，不省略关键信息
3. **深度性**：添加扩展说明章节，详细说明技术细节
4. **准确性**：风险流和影响分析具体到代码元素
5. **全面性**：提供足够的代码示例（5-10个场景）
6. **实用性**：包含最佳实践、误报排除、测试用例

遵循本指南，创建的规则文档将：
- 帮助AI模型准确识别问题
- 提供明确的修复指导
- 减少误报和漏报
- 提高稳定性检测质量