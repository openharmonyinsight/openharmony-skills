# Ability子系统配置

> **Ability子系统** - 元能力特有规则

## 基础信息

**子系统名称**：Ability（元能力）

**源码路径**：`test/xts/acts/ability`

---

## domain映射

### 元能力 domain

| 模块 | domain | 标签 | 说明 |
|------|--------|------|------|
| AAFwk | C0013xx | AAFwk | Ability Framework |
| AMS | C0013xx | AMS | Ability Manager Service |

### 日志过滤domain

**常用domain**：
- C001300：AAFwk核心
- C001301：AMS管理
- C0013xx：元能力相关

---

## 关键字规则

### 定界规则

**元能力相关关键字**：

| 关键字 | 领域 | 问题类型 | 解决方案 |
|--------|------|----------|----------|
| App died | 元能力 | 应用闪退 | 检查应用启动流程，验证Ability生命周期 |
| Ability not found | 元能力 | Ability未找到 | 检查Ability配置，验证bundleName |
| startAbility failed | 元能力 | 启动失败 | 检查Want参数，验证目标Ability是否存在 |
| Ability timeout | 元能力 | 启动超时 | 检查Ability启动耗时，分析性能问题 |

---

## SO库归属

### 元能力相关SO库

| SO库名 | 子系统 | 说明 |
|--------|--------|------|
| libability_runtime.z.so | 元能力 | Ability Runtime |
| libapp_manager.z.so | 元能力 | App Manager |

---

## 源码路径映射

### Ability源码结构

```
test/xts/acts/ability/
├── ability_runtime/
│   └─ AbilityRuntime.test.ets
├── ability_base/
│   └─ AbilityBase.test.ets
└── ability_manager/
    └─ AbilityManager.test.ets
```

---

## 特殊规则

### 元能力特有分析规则

**规则1**：Ability生命周期分析
- 检测 Ability 状态转换（onCreate/onStart/onStop）
- 分析生命周期调用顺序

**规则2**：Want参数分析
- 提取 Want 参数（bundleName/abilityName/moduleName）
- 验证目标Ability是否存在

**规则3**：进程状态分析
- 检测进程启动/退出
- 分析进程崩溃原因

---

## 配置优先级

**Ability子系统配置**：
```
Ability模块配置 > Ability子系统配置 > 核心配置
```

---

**更新时间**：2026-07-03  
**适用范围**：Ability子系统测试问题分析