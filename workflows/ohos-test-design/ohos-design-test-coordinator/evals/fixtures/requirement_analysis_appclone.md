# 需求分析报告
> 生成时间：2026-07-28 / 需求文档名：requirement_appclone.md

## 1. 需求概述
- 需求名称：应用分身功能
- 业务目标：为 HarmonyOS NEXT 提供应用分身能力，允许为同一应用创建多个独立分身实例，数据隔离
- 拆分策略声明：用户故事格式（spec格式信号命中3项，分支A）
- 变更范围概要：测试对象主单元2个（US-1, US-2） + 回归对象领域0个 + 文档验证类US: US-3，Phase4统一生成资料用例
- 主单元索引：
  - US-1 设置应用分身模式 | 测试对象
  - US-2 查询应用分身状态 | 测试对象

## 2. 共享规格资源

### 2.1 输入条件规格表
| 条件ID | 条件名称 | 数据类型 | 取值范围 | 必填/可选 | 枚举值 | 默认值 | 条件类型 | 来源章节 |
|--------|---------|---------|---------|----------|--------|--------|---------|---------|
| COND-001 | bundleName | string | 非空，长度1-256 | 必填 | - | - | 直接参数 | §2 API/US-1,US-2 |
| COND-002 | mode | CloneMode | NOT_CONFIGURED/ALWAYS_ASK/MAIN_APP/CLONE_APP | 必填 | 0,1,2,3 | - | 直接参数 | §2 API/US-1 |
| COND-003 | index | number | 1-5 | 可选 | - | - | 直接参数 | §2 API/US-1 |
| COND-004 | 调用者角色 | enum | administrator/普通用户 | 必填 | - | 普通用户 | 上下文条件 | §4 BR-1 |
| COND-005 | 分身数量上限 | number | 5 | - | - | 5 | 上下文条件 | §4 BR-2 |

### 2.2 输入条件耦合分析+验证映射

#### US-1 设置应用分身模式
**正交判定**：非正交
**判定依据**：mode=CLONE_APP 时需要 index，且 index 受分身数量上限约束；其他 mode 值不需要 index，此部分为正交子路径。

**耦合路径说明**：
输出"返回0，分身创建成功"需要同时满足：COND-002=CLONE_APP + COND-003在1-5范围内 + COND-004=administrator
输出"返回-1，超限"仅需：COND-003>5 且 COND-002=CLONE_APP
输出"返回-1，参数错误"仅需：COND-001非法 或 COND-002非法（与其他条件取值无关，此部分正交）

**耦合性质**：混合型（错误路径正交，成功路径非正交）

##### 组合真值表（非正交路径）
| COND-002(mode) | COND-003(index) | COND-004(角色) | 输出 | 关联AC | VM ID | 路径类型 |
|---------------|----------------|---------------|------|--------|-------|---------|
| ALWAYS_ASK | * | administrator | 返回0，模式设为始终询问 | AC-1 | VM-001 | 成功路径 |
| MAIN_APP | * | administrator | 返回0，模式设为主应用 | AC-2 | VM-002 | 成功路径 |
| CLONE_APP | 1 | administrator | 返回0，创建第1个分身 | AC-3 | VM-003 | 成功路径（多条件耦合） |
| CLONE_APP | 6 | administrator | 返回-1，超过上限 | AC-4 | VM-004 | 错误路径 |
| * | * | 普通用户 | 返回-1，权限不足 | - | VM-005 | 错误路径（COND-004正交） |

##### 正交子路径（可独立表述的部分）
| 条件 | 取值 | 独立影响 | 正交范围 |
|------|------|---------|---------|
| COND-001 | 空字符串/超256 | 返回-1，错误码201 | 任何其他条件取值下均独立生效 |
| COND-002 | 非枚举值 | 返回-1，错误码201 | 任何其他条件取值下均独立生效 |

#### US-2 查询应用分身状态
**正交判定**：正交
**判定依据**：bundleName 合法性独立决定查询结果，不依赖其他条件取值。

##### COND-001(bundleName) → 独立影响路径
| 取值类别 | 具体取值 | 对输出的影响 | 关联AC | VM ID | 来源 |
|---------|---------|------------|--------|-------|------|
| 合法值 | 非空1-256 | 返回mode及index（如已设置） | AC-5 | VM-006 | §2 AC-5 |
| 非法值 | 空字符串 | 返回-1，错误码201 | AC-5 | VM-007 | §5 EX-1 |

### 2.3 SDK API信息（含inner接口过滤说明）
| 接口ID | 接口名称 | 接口类型(public) | 入参格式 | 参数说明 | 错误码 | 来源章节 |
|--------|---------|----------------|---------|---------|--------|---------|
| API-001 | setAppClonePreference | public | (bundleName: string, preference: {mode: CloneMode, index?: number}) | bundleName:应用包名; mode:分身模式; index:分身序号 | 0,-1,201 | §2 API/US-1 |
| API-002 | getAppClonePreference | public | (bundleName: string) | bundleName:应用包名 | 0,-1,201 | §2 API/US-2 |

> 删除Inner接口数：1（getAppCloneInfo，@internal标记，未输出到§2.3）
> 删除参数数：0（getAppCloneInfo 的 bundleName 参数未提取到§2.1）

### 2.4 可测试性手段信息
| 手段ID | 手段类型 | 触发方式 | 用途 | 来源章节 |
|--------|---------|---------|------|---------|
| TM-001 | 辅助API测试桩 | 调用 setAppClonePreference | 触发US-1被测对象 | §6 |
| TM-002 | 辅助API测试桩 | 调用 getAppClonePreference | 触发US-2被测对象 | §6 |

### 2.5 全局非功能性需求
| 需求ID | 类别 | 描述 | 指标 | 关联主单元 | 来源章节 |
|--------|------|------|------|-----------|---------|
| NF-1 | 安全 | 仅授权管理员可修改分身配置 | administrator角色 | US-1 | §7 |
| NF-2 | 性能 | getAppClonePreference响应时间 | ≤100ms | US-2 | §7 |

## 3. US-1：设置应用分身模式

### 3.1 描述
- 业务目标：设置应用的分身模式，控制是否可创建分身实例
- 测试策略标识：测试对象（spec标注变更内容）
- 外部入口：TM-001（辅助API测试桩）→ 被测对象 setAppClonePreference

### 3.2 资源关联
- 涉及条件：COND-001(bundleName, 非空≤256), COND-002(mode, 枚举0-3), COND-003(index, 1-5可选), COND-004(角色, administrator), COND-005(上限, 5)
- 关联规则：BR-1(跨US:↔US-2), BR-2(跨US:↔US-2), EX-1, EX-2, EX-3, EX-4
- 涉及手段：TM-001(辅助API测试桩)

### 3.3 被测场景表
| 场景ID | 关联AC | WHEN（触发条件） | THEN（预期输出） | 来源 |
|--------|--------|-----------------|-----------------|------|
| US1-AC1 | AC-1 | 调用setAppClonePreference(bundleName,{mode:ALWAYS_ASK}) | 返回0，分身模式设为始终询问 | §2 AC-1 |
| US1-AC2 | AC-2 | 调用setAppClonePreference(bundleName,{mode:MAIN_APP}) | 返回0，分身模式设为主应用 | §2 AC-2 |
| US1-AC3 | AC-3 | 调用setAppClonePreference(bundleName,{mode:CLONE_APP,index:1}) | 返回0，创建第1个分身 | §2 AC-3 |
| US1-AC4 | AC-4 | 调用setAppClonePreference(bundleName,{mode:CLONE_APP,index:6}) | 返回-1，超过分身数量上限(5) | §2 AC-4 |

### 3.4 输入→输出映射
（见§2.2 组合真值表，US-1为非正交，已穷举关键组合路径）

### 3.5 待确认项
| 待确认ID | 缺口类型 | 问题描述 | 价值说明 |
|----------|---------|---------|---------|
| 无 | - | - | - |

## 4. US-2：查询应用分身状态

### 4.1 描述
- 业务目标：查询应用的分身配置状态
- 测试策略标识：测试对象（spec标注变更内容）
- 外部入口：TM-002（辅助API测试桩）→ 被测对象 getAppClonePreference

### 4.2 资源关联
- 涉及条件：COND-001(bundleName, 非空≤256)
- 关联规则：BR-3(默认行为), EX-1, EX-2
- 涉及手段：TM-002(辅助API测试桩)

### 4.3 被测场景表
| 场景ID | 关联AC | WHEN（触发条件） | THEN（预期输出） | 来源 |
|--------|--------|-----------------|-----------------|------|
| US2-AC5 | AC-5 | 调用getAppClonePreference(bundleName)，应用已配置 | 返回mode及index（如已设置） | §2 AC-5 |
| US2-AC6 | AC-6 | 调用getAppClonePreference(bundleName)，应用未配置 | 返回mode:NOT_CONFIGURED | §2 AC-6 |

## 5. 自检结果
- 24/24项通过（通用检查项24项 + 分支A附加4项）
- Inner接口过滤：已删除1个（getAppCloneInfo），§2.1无InnerApi参数
- 零推导验证：通过，所有场景均来自原文档明确描述
- 正交判定：US-1(非正交/混合型) + US-2(正交)
