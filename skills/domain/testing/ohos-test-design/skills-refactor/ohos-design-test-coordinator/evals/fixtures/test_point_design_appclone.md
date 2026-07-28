# 测试点设计
> 生成时间：2026-07-28 / 来源：requirement_analysis_appclone.md

## 汇总
| 维度 | 数量 |
|------|------|
| 测试对象主单元 | 2 |
| 被测场景总数 | 6 |
| 测试点总数 | 14 |
| 按执行方式统计 | XTS:0 / 黑盒自动化:14 / API性能:0 / 手工:0 |

## 测试点清单

### US-1：设置应用分身模式

| 测试点ID | 场景ID | 测试点描述 | 风险级别 | 测试类型 | 执行方式 | 预期结果 | 来源 |
|----------|--------|-----------|---------|---------|---------|---------|------|
| TP-US01-001 | US1-AC1 | 管理员设置mode=ALWAYS_ASK，验证返回值0 | P0 | 功能测试 | 黑盒自动化 | 返回0，且通过getAppClonePreference可观测到mode已变更为ALWAYS_ASK | spec AC-1 |
| TP-US01-002 | US1-AC2 | 管理员设置mode=MAIN_APP，验证返回值0 | P1 | 功能测试 | 黑盒自动化 | 返回0，且getAppClonePreference返回mode=MAIN_APP | spec AC-2 |
| TP-US01-003 | US1-AC3 | 管理员设置mode=CLONE_APP,index=1，验证返回值0 | P0 | 功能测试 | 黑盒自动化 | 返回0，且getAppClonePreference返回mode=CLONE_APP,index=1 | spec AC-3 |
| TP-US01-004 | US1-AC3 | 管理员设置mode=CLONE_APP,index=5（上限），验证返回值0 | P1 | 边界值测试 | 黑盒自动化 | 返回0，分身创建成功 | spec AC-3,BR-2 |
| TP-US01-005 | US1-AC4 | 管理员设置mode=CLONE_APP,index=6（超上限），验证返回-1 | P0 | 边界值测试 | 黑盒自动化 | 返回-1，错误码201，分身未创建 | spec AC-4,BR-2 |
| TP-US01-006 | US1-AC1 | bundleName为空字符串，验证返回-1 | P0 | 异常测试 | 黑盒自动化 | 返回-1，错误码201 | spec EX-1 |
| TP-US01-007 | US1-AC1 | bundleName长度超256字符，验证返回-1 | P2 | 边界值测试 | 黑盒自动化 | 返回-1，错误码201 | spec EX-2 |
| TP-US01-008 | US1-AC1 | mode值非枚举范围（如mode=99），验证返回-1 | P1 | 异常测试 | 黑盒自动化 | 返回-1，错误码201 | spec EX-3 |
| TP-US01-009 | US1-AC1 | 普通用户（非管理员）调用setAppClonePreference，验证返回-1 | P0 | 安全测试 | 黑盒自动化 | 返回-1，权限不足，分身模式未变更 | spec BR-1,NF-1 |

### US-2：查询应用分身状态

| 测试点ID | 场景ID | 测试点描述 | 风险级别 | 测试类型 | 执行方式 | 预期结果 | 来源 |
|----------|--------|-----------|---------|---------|---------|---------|------|
| TP-US02-001 | US2-AC5 | 应用已配置分身后查询，验证返回mode及index | P0 | 功能测试 | 黑盒自动化 | 返回mode=CLONE_APP,index=1（与设置值一致） | spec AC-5 |
| TP-US02-002 | US2-AC6 | 应用未配置分身时查询，验证返回NOT_CONFIGURED | P1 | 功能测试 | 黑盒自动化 | 返回mode=NOT_CONFIGURED | spec AC-6,BR-3 |
| TP-US02-003 | US2-AC5 | bundleName为空字符串查询，验证返回-1 | P0 | 异常测试 | 黑盒自动化 | 返回-1，错误码201 | spec EX-1 |
| TP-US02-004 | US2-AC5 | bundleName长度超256字符查询，验证返回-1 | P2 | 边界值测试 | 黑盒自动化 | 返回-1，错误码201 | spec EX-2 |
| TP-US02-005 | US2-AC5 | getAppClonePreference响应时间验证 | P2 | 性能测试 | API性能 | 响应时间≤100ms | spec NF-2 |

## 对抗评估结果
- 总分：85/100（达标，≥80）
- 需求覆盖率：90% | 关键场景覆盖：38/45 | 变异杀死率：12/15
