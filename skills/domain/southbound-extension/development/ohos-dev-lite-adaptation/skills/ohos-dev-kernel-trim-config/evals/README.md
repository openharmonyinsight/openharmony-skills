# ohos-dev-kernel-trim-config evals

5 个评估用例，判据全部来自 SR-06 交付件真实验证数据（自验证说明.md iter09 🟡→iter10 ✅ + compile-verification/compile-verify-report.md 源码级核实 + iter10_reverify/output/trim-plan.md 实测方案），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `l0_hi3861_ram_budget_trim_plan` | L0 裁剪方案生成（RAM 预算分级 + 逐类决策） | 总 SRAM 扣厂商组件后分级 + 最小集保留 + 关调测类 + 实例上限下调 + 20% 裕量 + 运行期风险标注 | SR-06 iter10 ✅ 实测方案（TSK 32→15 / SEM 100→32 / MUX 64→24 / QUEUE 64→16 / SWTMR 80→16） |
| `cpup_disable_must_be_explicit_no` | 关闭宏的正确方式 | 注释掉 #define → 未定义符号编译错；必须显式 `#define ... NO` | compile-verify-report §3.3 实测挖出的真错误（trim-plan §4 原写法会编译错） |
| `pmp_lazy_macro_no_savings` | 惰性宏识别 | PMP/Track/FPB 类宏关闭不省资源，禁止计入节省合计（防虚报） | SR-06 iter09 深审翻车点（PMP 虚报 ~800B ROM）+ iter10 修正 + compile-verify Track/FPB 惰性核实 |
| `queue_limit_lowering_vs_disable` | 限额下调 vs 组件关闭 | LIMIT 下调只缩池，不触发组件关闭类 #error；运行期耗尽风险另评 | compile-verify-report §2.1 #9（QUEUE_LIMIT 64→16 不触发 los_config.h:421） |
| `error_guard_source_verification_over_docs` | #error 守卫以源码实读为准 | 不信文档/记忆引用的守卫文本；真实依赖方向相反的案例 | compile-verify-report §3.1/§3.2：文档所述 `#error "cpup need support task monitor"` 实不存在，CPUP 包在 TSK_MONITOR==YES 守卫内 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：

- RAM 分级判定（基线常拿总 SRAM 352KB 直接归 256~512KB 级，不知扣 WiFi 协议栈）
- 注释掉 vs 显式 NO（基线大概率认可注释掉这种"直觉写法"——这正是 SR-06 真实翻车点）
- 惰性宏不虚报（基线倾向接受"关宏=省资源"的表面账）
- 限额下调 vs 关闭区分（基线可能误判触发 #error 或忽略运行期耗尽风险）
- 守卫文本溯源（基线倾向直接采信文档里的 #error 引用）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **分级正确率**：with skill 用内核可用 RAM（扣协议栈）分级；基线用总 SRAM
2. **关闭方式正确率**：with skill 100% 显式 `#define ... NO`；基线高概率给注释掉写法（编译错）
3. **虚报拦截**：惰性宏场景 with skill 节省标 0/TODO；基线计入合计虚报
4. **依赖判定**：限额下调用例 with skill 精确区分"缩池"与"关组件"；基线易混淆
5. **证据纪律**：守卫验证 with skill 要求源码实读；基线直接信题面/文档
