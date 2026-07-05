# 状态管理 V1→V2 迁移 Skill 设计方案

> 分析日期: 2026-06-06
> 目标: 提供 V1→V2 状态管理迁移的 Claude Code Skill

## 一、核心判断

**纯 Markdown 不够，需要 Markdown + 代码脚本。**

| 环节 | 需要脚本原因 |
|------|-------------|
| 组件依赖链追踪 | 需解析 .ets 文件的 import/调用关系，构建父子组件树，识别 @State→@Link 等状态传递 |
| API 版本检测 | 需从 build-profile.json5 / app.json5 精确提取 compatibleSdkVersion |
| 迁移范围确定 | 给定单个组件，自动找出所有有数据交互的上下游组件 |
| V1/V2 混用校验 | 迁移后验证是否违反混用约束（如 @Observed 和 @ObservedV2 不能共存） |

代码转换本身（装饰器替换、状态变量改写）由 Claude 完成，比 codemod 更可靠。

## 二、Skill 架构

```
v1-v2-migration/
├── SKILL.md                          # 主 skill 定义
├── scripts/                          # 确定性分析脚本
│   ├── component_analyzer.py         # 组件分析：装饰器、状态变量、输入输出
│   ├── dependency_tracer.py          # 依赖追踪：父子组件链
│   ├── api_version_checker.py        # API 版本检测
│   └── mixing_validator.py           # V1/V2 混用校验
├── references/                       # 迁移文档（精简版）
│   ├── decorator-mapping.md          # 装饰器映射表
│   ├── class-migration.md            # 数据对象迁移规则
│   ├── app-state-migration.md        # 应用级状态迁移
│   ├── mixing-rules.md               # V1/V2 混用规则
│   ├── rendering-migration.md        # 渲染控制迁移
│   └── advanced-topics.md            # animateTo、内置对象迁移
├── examples/                         # 迁移前后对照示例
└── templates/                        # 迁移代码模板
```

## 三、工作流

```
用户调用 /v1-v2-migrate [target]
  → api_version_checker (检测API版本)
  → 确定迁移范围 (整仓 or 单组件+依赖链)
  → 生成迁移计划 (展示给用户确认)
  → Claude 执行代码改写
  → mixing_validator (迁移后校验)
  → 生成迁移报告
```

## 四、迁移文档源

从 `docs/zh-cn/application-dev/ui/state-management/` 提取，核心文档 11 份：

- arkts-v1-v2-migration.md (总览与装饰器映射表)
- arkts-v1-v2-migration-inner-component.md (组件级状态变量)
- arkts-v1-v2-migration-inner-class.md (数据对象 @Observed→@ObservedV2)
- arkts-v1-v2-migration-application.md (LocalStorage/AppStorage/PersistentStorage)
- arkts-v1-v2-migration-reusable.md (@Reusable→@ReusableV2)
- arkts-v1-v2-migration-rendering-control-repeat.md (ForEach→Repeat)
- arkts-v1-v2-migration-inner-object.md (内置对象)
- arkts-v1-v2-migration-animateTo.md (animateTo)
- arkts-v1-v2-update-difference.md (更新机制差异)
- arkts-v1-v2-mixusage-before-api-version.md (API<19混用规则)
- arkts-v1-v2-mixusage.md (API>=19混用规则)

## 五、装饰器映射核心表

| V1 | V2 | 关键差异 |
|----|-----|---------|
| @Component | @ComponentV2 | 容器装饰器 |
| @State | @Local / @Param | @Local 不可外部初始化；@Param 可 |
| @Prop | @Param | V2 @Param 是引用非深拷贝 |
| @Link | @Param + @Event | 需手动回调模式实现双向 |
| @Observed + @ObjectLink | @ObservedV2 + @Trace | V2 深度观测无需子组件分解 |
| @Track | @Trace | 直接替换 |
| @Provide/@Consume | @Provider/@Consumer | V2 需 `()` 语法，alias 为唯一匹配键 |
| @Watch | @Monitor | V2 异步，支持多变量监听 |
| $$ 绑定 | !! 绑定 | 语法替换 |
| LocalStorage | @ObservedV2/@Trace 单例 | 跨页面用 import/export |
| AppStorage | AppStorageV2.connect() | 跨 Ability 共享 |
| PersistentStorage | PersistenceV2 | 自动持久化 @Trace 属性 |
| ForEach | Repeat (全量模式) | 替代 ForEach 和 LazyForEach |
| LazyForEach | Repeat + .virtualScroll() | 内置懒加载 |

## 六、实施阶段

| 阶段 | 内容 | 预估 |
|------|------|------|
| P1 | references/ — 6 份参考文档 | 1-2 天 |
| P2 | component_analyzer.py + dependency_tracer.py | 2-3 天 |
| P3 | api_version_checker.py + mixing_validator.py | 1 天 |
| P4 | examples/ — 5 组前后对照 | 1-2 天 |
| P5 | SKILL.md — 主 skill 文件 | 2-3 天 |
| P6 | templates/ — 3 个模板 | 0.5 天 |
| P7 | 端到端测试 | 2-3 天 |
| P8 | 打包交付 | 1 天 |

## 七、交付形式

独立 skill 包 → 放入项目 `.claude/skills/` 即可使用。脚本仅用 Python 标准库，无外部依赖。
