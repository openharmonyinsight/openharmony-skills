# CONFIG → /dev 节点 → OH service 依赖映射表

> bring-up 缺 `/dev` 节点审计速查：哪个 CONFIG 出哪个 `/dev` 节点，哪个 OH service 依赖它，缺了什么症状。来源：hi3516cv610 实战 + `{{ASSET_ROOT}}/workflow/steps/03-driver-device/SKILL.md` 驱动适配审计清单。

## 映射表

| `/dev` 节点 | 依赖的内核驱动/CONFIG | DTS 节点 | OH service 依赖 | 缺失后果（症状） | 适配 playbook |
|---|---|---|---|---|---|
| `/dev/watchdog` | `CONFIG_WATCHDOG` + `CONFIG_DW_WATCHDOG`（dw wdt） | wdt 节点 `compatible="snps,dw-wdt"` + `clocks` + `status="okay"` | `watchdog_service` | watchdog_service open 失败退出 → init `ReapService` → `reboot(RB_AUTOBOOT)` 软重启 loop（典型 bring-up 卡点） | `watchdog-adapter-playbook.md` |
| `/dev/binder`、`/dev/hwbinder`、`/dev/vndbinder` | `CONFIG_ANDROID` + `CONFIG_ANDROID_BINDER_IPC` + 32位加 `BINDER_IPC_32BIT` + 关 BINDERFS | （misc_register/devtmpfs 自动建，无 DTS 节点） | samgr / foundation / 各 sa | 32位错配：`binder ioctl -22 EINVAL` ×400 + samgr `boot step -9` 卡死，各 service 起不来 | `binder-adapter-playbook.md` |
| `/dev/hilog` | `CONFIG_HILOG` + `CONFIG_STAGING` | （驱动不 device_create，需手动 mknod） | hilog / hiview / apphilogcat | `apphilogcat: hilog fd failed No such file` → hilog/hiview 起不来 | `hilog-adapter-playbook.md` |
| `/dev/ttyS*` | UART 驱动 CONFIG（如 `CONFIG_SERIAL_8250` / 厂商 UART） | uart 节点 `compatible` + `interrupts` + `clocks` + `status` | getty / 串口 console | 串口 console / getty 起不来 | （DTS 节点规范见 03-driver-device） |
| cgroup 相关 | `CONFIG_CGROUPS` + `CONFIG_CGROUP_FREEZER`（+ 其他子系统 cgroup） | （内核挂载，无 DTS 节点） | 部分 service（依赖 cgroup 资源隔离） | 部分 service 依赖 cgroup 起不来 | （defconfig 开 CONFIG） |
| SPI Nand 颗粒（mtdblock） | SPI Nand 驱动 + **ID 表两侧补条目** | （fmc 节点） | UBI / rootfs | uboot `pagesize 8192` BUG / 内核 `bsp_spi_nand_probe error -19` → UBI/rootfs 起不来 | `spi-nand-id-table-playbook.md` |
| SPI Nor 颗粒（mtdblock） | SPI Nor 驱动 + **ID 表两侧补条目** | （fmc 节点） | jffs2 / rootfs | 颗粒 probe 失败 → rootfs 起不来 | `spi-nand-id-table-playbook.md` §SPI Nor 同理 |

## 审计流程（Step 1 全量审计）

1. **列需求**：把 OH `init.cfg` pre-init 的 `chmod`/`chown` 路径 + 各 service 依赖的 `/dev` 节点列出来。
   - 典型 pre-init job：`chmod 0666 /dev/binder`、`chown 4 4 /dev/hilog`、`mkdir /storage/data/dsoftbus`、`chmod 0666 /dev/hdf/hdfwifi` 等。
   - 典型 service 依赖：`watchdog_service` → `/dev/watchdog`；samgr/foundation → `/dev/binder`；hiview/apphilogcat → `/dev/hilog`；getty → `/dev/ttyS*`。
2. **逐个对内核配置找缺口**：每个 `/dev` 节点按上表查 defconfig（CONFIG 开没开）+ DTS（节点在不在、`status` 是不是 `"okay"`）+ ID 表（颗粒在不在表）。
3. **全量列出缺口**：把全部缺的驱动一次性列出来，别只修当前报错那个（实测教训——缺 watchdog 修完，binder/hilog 又报）。

## 常见 init.cfg pre-init job 参考（hi3516 linux L1）

> pre-init 必须先做，否则 service 起不来：

```
chmod 0666 /dev/binder
chown 4 4 /dev/hilog
exec /bin/busybox mknod /dev/hilog c 245 0      # hilog 驱动不 device_create
chmod 0666 /dev/hilog
mkdir /storage/data/dsoftbus
mkdir /storage/maindata/hks_client/{info,key}
mkdir /storage/deviceauth
chmod 0666 /dev/hdf/hdfwifi
export LD_LIBRARY_PATH /storage/app/libs
export LD_PRELOAD /usr/lib/libdfx_signalhandler.so
```

## 原则

- **全量审计**：缺一个 `/dev` 节点时把全部节点查一遍，避免一个个报错才发现。关联 memory `prefer-driver-adaptation-over-rootfs-bypass`。
- **优先驱动适配**：缺节点优先开 CONFIG + DTS + ID 表 + 重编，不靠 rootfs 绕过。
- **hilog 类「驱动有但节点不自动建」**：开 CONFIG 仍要 pre-init mknod（驱动不 `device_create`）。
- **OH init 无 mknod**：用 `exec /bin/busybox mknod`，major 号从 `/proc/devices` 查实际值。

## 关联

- `{{ASSET_ROOT}}/workflow/steps/03-driver-device/SKILL.md` §驱动适配审计清单 + §L1 子系统选配 init 配置步骤（标准该起的进程表）
- 各 playbook（watchdog / hilog / binder / spi-nand-id-table）
- memory `prefer-driver-adaptation-over-rootfs-bypass`
