# ohos-dev-kernel-node-adapt evals

4 个评估用例，判据全部来自本 skill 自身方法论（SKILL.md Step 1-5 + 各 playbook，iter07 hi3516cv610 实战提炼），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `watchdog_devnode_defconfig_dts` | 缺 /dev/watchdog → reboot loop | defconfig 开 CONFIG + DTS 加节点完整链路 + 反 rootfs 绕过 | SKILL.md Step 2/3 + watchdog-adapter-playbook（CONFIG_WATCHDOG+DW_WATCHDOG / snps,dw-wdt / 0x11030000） |
| `spi_nand_dual_side_id_table` | SPI Nand 颗粒 probe 失败（-19） | ID 表两侧补条目 + runtime print 权威 | Step 4 + spi-nand-id-table-playbook（0xe5 0xf1 / raw/fmc100 vs fmc100 两侧独立） |
| `binder_32bit_config_arrangement` | binder ioctl -22 EINVAL ×400 / samgr boot step -9 | 32 位小系统 binder CONFIG 安排 + BINDER_IPC_32BIT | Step 2 CONFIG 表 + binder-adapter-playbook（OH001 案例） |
| `full_audit_not_single_fix` | 只报了一个节点缺失 | 全量缺口审计（不只修当前报错那个） | Step 1 方法论 + config-devnode-map（iter07 教训） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条布尔判定。全部用例 expectations 全过 = 通过。

**without skill（基线）**：同一 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]`。预期基线弱项：
- ID 表两侧补条目意识（基线常只补内核侧或只补一侧）
- BINDER_IPC_32BIT 32 位对齐（基线常只开 CONFIG 不加位宽宏，-22 不解）
- 全量审计（基线常跟着当前报错修一个）
- rootfs 绕过倾向（基线可能建议删 service 绕过而非驱动适配）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。
