# 迁移规划方法

## 规划原则

### 1. 自底向上迁移

按依赖顺序从底层到上层迁移：

```
第1层: 数据层 (models, entities, dto)
    ↓
第2层: 数据访问层 (database, network, storage)
    ↓
第3层: 业务逻辑层 (helpers, utils, services)
    ↓
第4层: UI适配层 (adapters, viewholders)
    ↓
第5层: UI层 (fragments, activities)
```

### 2. 模块划分

每个迁移模块约 **5000 行代码**，包含：

- 完整的功能单元
- 相关的依赖文件
- 可独立编译验证

### 3. 风险评估

按以下因素评估迁移风险：

| 风险因素 | 低风险 | 高风险 |
|---------|--------|--------|
| 代码行数 | <500 | >2000 |
| 依赖复杂度 | 少量依赖 | 大量循环依赖 |
| 使用框架 | 标准 Android API | 第三方库 |
| 业务复杂度 | 工具类 | 核心业务逻辑 |

## 规划步骤

### 步骤 1: 依赖分析

运行分析脚本生成依赖图：

```bash
python scripts/analyze.py <source-path> --output dependencies.json
```

### 步骤 2: 识别模块

根据包结构和依赖关系划分模块：

```
com.example.gallery/
├── models/           → 模块1: 数据模型
├── database/         → 模块2: 数据库层
├── helpers/          → 模块3: 工具类
├── adapters/         → 模块4: 适配器
├── fragments/        → 模块5: UI片段
└── activities/       → 模块6: Activity
```

### 步骤 3: 确定优先级

**高优先级**（先迁移）：
- 数据模型 (models)
- 基础工具类 (helpers)
- 数据库操作 (database)

**中优先级**：
- 业务服务 (services)
- 适配器 (adapters)

**低优先级**（后迁移）：
- UI 组件 (fragments, activities)

### 步骤 4: 生成任务清单

为每个模块创建任务卡片：

```markdown
## 模块: models

**优先级**: 高
**预估工时**: 4小时
**依赖**: 无
**文件数**: 15

### 任务清单
- [ ] Medium.kt → Medium.ets
- [ ] Directory.kt → Directory.ets
- [ ] ...

### 验证标准
- [ ] 编译无错误
- [ ] 类型定义正确
- [ ] 导出语句正确
```

## 模块迁移示例

### 示例 1: models 模块

**源文件**：
```
models/Medium.kt (120行)
models/Directory.kt (80行)
models/Favorite.kt (60行)
...
```

**迁移策略**：
1. 先迁移数据类定义
2. 添加必要的导入
3. 转换类型注解
4. 验证编译

### 示例 2: database 模块

**依赖**: models 模块

**迁移策略**：
1. 等待 models 模块完成
2. 迁移 Room 实体定义
3. 转换 DAO 接口
4. 转换数据库操作

### 示例 3: adapters 模块

**依赖**: models 模块

**迁移策略**：
1. 迁移数据类为 DataSource
2. 转换 ViewHolder 为 ListItem
3. 使用 LazyForEach 替代 RecyclerView

## 并行迁移策略

当有多个开发者时，可以并行迁移独立模块：

```
开发者A: models + database
开发者B: helpers + services
开发者C: adapters
```

**注意**：必须先完成低层模块，才能迁移依赖它的上层模块。

## 持续集成

每个模块迁移完成后：

1. **编译验证**：确保编译无错误
2. **语法检查**：运行 `scripts/validate.py`
3. **代码审查**：检查转换质量
4. **单元测试**：验证功能正确性

## 迁移追踪

使用表格追踪进度：

| 模块 | 状态 | 负责人 | 开始日期 | 完成日期 | 问题 |
|------|------|--------|----------|----------|------|
| models | ✅ 完成 | A | 01-01 | 01-02 | - |
| database | 🔄 进行中 | A | 01-03 | - | API映射问题 |
| helpers | ⏳ 待开始 | B | - | - | - |
| services | ⏳ 待开始 | B | - | - | - |
| adapters | ⏳ 待开始 | C | - | - | - |
| fragments | ⏳ 待开始 | C | - | - | - |
| activities | ⏳ 待开始 | C | - | - | - |

状态标识：
- ✅ 完成
- 🔄 进行中
- ⏳ 待开始
- ❌ 有问题
