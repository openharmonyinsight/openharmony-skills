# watchdog 驱动适配 playbook

> 缺 `/dev/watchdog` → OH `watchdog_service` open 失败退出 → init `ReapService` 见 IMPORTANT 进程退出 → `reboot(RB_AUTOBOOT)` 软重启 loop。这是 bring-up 高频卡点。来源：hi3516cv610 实战。

## 症状

- 烧录启动后板子反复重启（reboot loop）。
- 串口看到 `watchdog_service` 退出 + init `ReapService` + `reboot(RB_AUTOBOOT)`。
- `ls /dev/watchdog` 不存在。

## 根因

内核没编 watchdog 驱动——defconfig 没开 `CONFIG_WATCHDOG`/`CONFIG_DW_WATCHDOG`，或 DTS 没 wdt 节点 / `status="disabled"`。`/dev/watchdog` 缺 → `watchdog_service` open 失败 → init 见服务退出软重启。

## 标准操作（按序）

### 1. 查 defconfig

在芯片 defconfig（如 `arch/arm/configs/hi3516cv610_defconfig`）开：

```
CONFIG_WATCHDOG=y
CONFIG_DW_WATCHDOG=y        # Synopsys DesignWare WDT（hi3516cv610 用 dw wdt）
```

没开就开。其他 SoC 按实际 wdt IP 选对应 CONFIG（如 `CONFIG_ARM_SP805_WATCHDOG`、`CONFIG_STM32_WATCHDOG` 等），别一律套 `DW_WATCHDOG`。

### 2. 查 DTS

watchdog 节点（hi3516cv610 实例 `wdg@0x11030000`）要含 `compatible = "snps,dw-wdt"` + `clocks` + `status = "okay"`：

```dts
/* arch/arm/boot/dts/hi3516cv610.dtsi */
wdg0: wdg@0x11030000 {
    compatible = "snps,dw-wdt";
    reg = <0x11030000 0x1000>;
    interrupts = <GIC_SPI 32 IRQ_TYPE_LEVEL_HIGH>;
    clocks = <&crg_ctrl HI3516_WDG_CLK>;
    status = "okay";              /* ← 缺节点或 status="disabled" 都要加/改 */
};
```

- `compatible` 必须与驱动 `.of_match_table` 匹配（dw wdt = `snps,dw-wdt`）。
- `reg` 基地址查 SoC TRM（HiSilicon NDA），**查不到别猜地址**，报 blocker。
- `clocks` 要给对 wdt 时钟，否则喂狗/超时计数不对。

### 3. 重编 zImage + dtbs

DTS 改了必走 `make dtbs` 重编设备树：

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-ohos- hi3516cv610_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-ohos- dtbs
make ARCH=arm CROSS_COMPILE=arm-linux-ohos- zImage
```

uImage 按内核重编后必走 FIT 重做（见 `{{ASSET_ROOT}}/workflow/steps/02-kernel-port`「内核重编后 uImage 必走 FIT」）。

### 4. 烧后验证

```bash
ls /dev/watchdog          # 节点出现
```

`watchdog_service` 不再 open 失败退出 → init 不再 reboot loop。

## 原则

- **优先驱动适配，别只靠 rootfs 绕过**：缺 `/dev/watchdog` 优先开 CONFIG + DTS + 重编，不要只在 rootfs 删 `watchdog_service`（绕过是权宜，标注技术债）。关联 memory `prefer-driver-adaptation-over-rootfs-bypass`。
- **全量审计**：缺 `/dev/watchdog` 时同步把 init.cfg pre-init 的 chmod/chown 路径 + service 依赖的其他 `/dev` 节点（binder/hilog/ttyS/cgroup）也查一遍，别等下一个报错。完整映射见 `config-devnode-map.md`。
- **改 uImage 记 changelog**：重编 uImage 烧录后立即更新 `CHANGES_*.md`（md5 + 改动 + 根因），关联 memory `update-changelog-after-burnfile-change`。

## 关联

- `{{ASSET_ROOT}}/workflow/steps/03-driver-device/SKILL.md` §watchdog 驱动适配标准操作 + 驱动适配审计清单
- `../ohos-issue-lite-diagnose/references/diagnostic-cases.md` §8（hi3516cv610 烧录全程含 watchdog）
- memory `prefer-driver-adaptation-over-rootfs-bypass`
