# ohos-dev-hal-skeleton-gen evals

5 个评估用例，判据全部来自 SR-02 交付件真实验证数据（自验证说明.md：iter09 深审两硬错误 → iter10 未闭合 → b21588f 修后 ✅ + iter12 板上 27/27 PASS；iter10_skill-reverify-fix/ 的 gpio_config.hcs、device_info.hcs.gpio.fragment 实例），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `l1_gpio_driver_skeleton_hdf` | L1 GPIO 驱动骨架生成（PL061，SDK 无 GPIO API） | HdfDriverEntry 结构 + 寄存器直写路线 + IRQ 从 HCS 读入 + HCS 三段链对齐 + hdf_driver 模板 | b21588f 修后产出（irqStart=55、match_attr hisi_hi3516cv610_gpio 两侧相等） |
| `irq_gic_plus32_conversion` | IRQ +32 GIC 换算 | DTS SPI 号 ≠ Linux virq；23→55 换算与后果 | iter09 深审硬错误①（irqStart=23 翻车，真值 55）+ dv300 irqStart=48 佐证 |
| `missing_device_info_counterpart` | match_attr 无对端 → .ko 加载但 Bind/Init 不被调用 | 运行时绑定链诊断（编译器查不出）+ 真产出对端而非文档化 | iter09 深审硬错误② + iter10 "只文档化未产出对端=未修复" 实测 |
| `l0_iot_hal_route_no_hdf` | L0 路线选择 | L0 = IoT 子系统（GpioOperations），非 HDF；调 SDK 函数路线；lite_component | 验收判据 2 + iter12 端到端（IoTGpio* 接口板上 27/27 PASS） |
| `l1_bare_register_access_antipattern` | 反模式：L1 裸指针寄存器直写 + 硬编码基址 | OSAL 封装要求 + 基址从 HCS 读入 | 禁止项「L1 直接操作寄存器」+ b21588f 修后 OSAL/DRS 实证 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：

- IRQ +32 换算（基线大概率把 DTS SPI 号 23 原样填入——iter09 新手执行者实测翻车点）
- device_info.hcs 对端必须真产出（基线常只说明"应改 device_info.hcs"而不产出——实测未闭合模式）
- L0/L1 框架区分（基线可能给 L0 生成 HDF 代码或给 L1 用裸 CMSIS 访问）
- match_attr 三段链（基线只查字符串相等，不查 deviceNode 实例级配对）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **IRQ 正确率**：with skill 100% 填 55（+32 换算）；基线高概率填 23（原始 SPI 号）
2. **对端产出率**：with skill 必产出 device_info.hcs 对端片段；基线常停留在文档建议层
3. **路线正确性**：L0/L1 场景 with skill 框架不混用；基线易混（L0 出 HDF / L1 裸寄存器）
4. **溯源纪律**：寄存器参数 with skill 从 chip_spec/HCS 取并可追溯；基线常直接编进 .c
