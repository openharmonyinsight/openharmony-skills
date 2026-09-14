# ohos-dev-board-config-gen evals

5 个评估用例，判据全部来自 SR-03 交付件真实验证数据（自验证说明.md：iter09 深审三阻断 / iter10 HCS 回归 / b21588f 修后 match_attr 16 对严格相等 + 寄存器中断与 DTS 零不一致 + 11 HCS 全量补齐），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `match_attr_pairing_uart_config_hcs` | match_attr 配对生成（device_info.hcs ↔ *_config.hcs） | deviceMatchAttr 与 match_attr 逐字符严格相等 + regBase/irqNum 按给定规格 | SR-03 b21588f：match_attr 16 对严格相等实测 |
| `defconfig_dependency_chain_check` | defconfig 依赖链完整性 | depends on 链断裂识别（编译器不报错但静默不生效）+ 对照官方金标准 | SR-03 iter09 深审真编译阻断（缺 MFD_BSP_FMC / PM） |
| `hex_legality_0x3516CV610` | hex 值合法性 | 大写 V 非法十六进制识别 + 全小写修正 | SR-03 iter09 翻车点（0x3516CV610 C 编译错误） |
| `l0_vs_l1_file_set_hcs_completeness` | L0/L1 文件清单差异 + L1 HCS 必生成 | 系统级别判定 → 文件集正确；漏 HCS 根因解释 | SR-03 iter10 回归根因（L1 漏 11 HCS → 所有 HDF 驱动加载失败） |
| `riscv_march_mabi_no_mcpu` | RISC-V 架构变量 | board_arch/board_cpu/cflags 正确 + RISC-V 不用 -mcpu | SKILL/config-gni-guide 规则 + Hi3861 实测 board_arch=rv32imac |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：

- match_attr 严格相等意识（基线常改名/改大小写"美化"字符串，不知静默加载失败后果）
- depends on 链检查（基线常只看 CONFIG 名存在与否，识别不出依赖断裂与"静默不生效"）
- L1 HCS 文件清单（基线常漏 HCS，或不知道 hdf.hcs/device_info.hcs/*_config.hcs 三层结构）
- hex 合法性细节（基线可能只说"格式问题"定位不到 V 字符）
- RISC-V 不用 -mcpu（基线倾向照抄 ARM 模板带 -mcpu）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **配对正确率**：with skill 的 match_attr 100% 与 deviceMatchAttr 逐字符相等；基线易出现自造命名
2. **依赖链盲区**：depends on 断裂用例，with skill 能指出"编译过但功能不进固件"；基线常误判"编译能过=没问题"
3. **HCS 完整性**：L1 场景 with skill 必产出 11 HCS 清单；基线大概率复现 iter10 式漏 HCS 回归
4. **架构差异化**：RISC-V 场景 with skill 不带 -mcpu；基线常混入 -mcpu=cortex-m4 类错误
