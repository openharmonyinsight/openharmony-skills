# L1 init.cfg 参考（hi3516cv610 类 18 services 基线）

> 来源：`20260720 L0 session & L1 conf/conf.txt`（L1 18 services init.cfg 完整提炼）。
> 用途：hi3516cv610 类 L1（LiteOS-A / Linux）适配时，作 init.cfg 模板基线。新板子把 18 个 service 的 path/uid/gid 按实际产物核对，pre-init 的目录与权限照搬。
> 与 `04-build-verify` Step 4.5 配套：rootfs 启动项五件套（B6）+ param 三件套（B7）+ importance:0 防 reboot loop（B8）+ 命令支持集（B15，见 SKILL.md）。

## init.cfg 结构总览

init.cfg 由三部分组成：`jobs`（pre-init / init / post-init 三个 job）+ `services`（18 个 service）。

```
jobs:
  pre-init   ← 目录创建 + 节点权限 + LD_LIBRARY_PATH/LD_PRELOAD
  init       ← /data 目录树 + start 全部 service（17 个）
  post-init  ← start iotc_service（1 个，依赖前序 service 就绪）
services:    ← 18 个 service 定义（path/uid/gid/importance/caps）
```

## pre-init job（目录 + 节点权限 + 环境变量）

pre-init 必须按序做五件事（B6 启动项五件套）：① mount proc/sysfs ② mount cgroup ③ mount binder（见 SKILL.md Step 4.5）④ 建存储目录 + 设权限 ⑤ 设 LD 环境变量。本节是 ④⑤ 的基线目录清单。

### 存储目录创建 + 权限（照搬基线）

| 目录 | 权限 | owner | 用途 |
|---|---|---|---|
| `/storage/data` | 0755 | — | 主数据根 |
| `/storage/data/log` | 0755 | 4:4 | 日志根（hilog uid 4） |
| `/storage/maindata` | 0700 | 12:12 | huks 主数据 |
| `/storage/maindata/hks_client` | 0700 | 12:12 | hks 客户端 |
| `/storage/maindata/hks_client/info` | 0700 | 12:12 | hks info |
| `/storage/maindata/hks_client/key` | 0700 | 12:12 | hks key |
| `/storage/data/dsoftbus` | 0750 | 19:7 | softbus 数据 |
| `/storage/data/device_attest` | 0755 | 20:20 | 设备认证 |
| `/storage/deviceauth` | 0700 | 19:7 | deviceauth |
| `/storage/deviceauth/account` | 0700 | 19:7 | deviceauth account |
| `/storage/data/system` | — | — | 系统数据 |
| `/storage/data/system/param` | 0755 | — | 系统参数 |
| `/storage/data/timertask` | 0755 | 7:7 | 定时任务 |
| `/userdata` | 0777 | — | 用户数据根 |
| `/userdata/photo` | 0777 | — | 照片 |
| `/userdata/thumb` | 0777 | — | 缩略图 |
| `/userdata/video` | 0777 | — | 视频 |
| `/data` | — | — | 数据根（init job 详建子树） |

### /dev 节点权限（照搬基线）

| 节点 | 权限/owner | 说明 |
|---|---|---|
| `/dev/binder` | `chmod 0666` | binder IPC，0666 全开（见 B6：binderfs 禁用时由 devtmpfs 建） |
| `/dev/hilog` | `chown 4 4` | hilog 设备，owner uid 4（hilog） |
| `/dev/hwlog_exception` | `chown 4 4` | 硬件异常日志，owner uid 4 |
| `/dev/hdf/hdfwifi` | `chmod 0666` | HDF wifi 设备节点 |

### 环境变量（pre-init 末尾必设）

```
export LD_LIBRARY_PATH /storage/app/libs:/usr/lib
export LD_PRELOAD /usr/lib/libdfx_signalhandler.so
```

- `LD_LIBRARY_PATH`：app 库目录 + 系统库目录
- `LD_PRELOAD`：dfx 信号处理器（崩溃捕获）

> ⚠️ 命令支持集（B15）：OH init 只支持 `mount/mkdir/chmod/chown/start/exec/export`，**不支持 mknod**。需要 mknod 时用 `exec /bin/busybox mknod ...` 绕。见 `base/startup/init/services/init/init_common_cmds.c`。

## init job（/data 目录树 + start 17 services）

init job 先建 `/data` 目录树（faultlog / misc / service / el1 / public / wifi / database 等，权限多为 0771/0770，owner 11:11 或 system），再 `exec /bin/hks_compatibility_bin`，最后依次 `start` 17 个 service。

### /data 目录树要点

- `/data` → `chown root root` + `chmod 0771`
- `/data/log` + `/data/log/faultlog/{temp,debug}` → system:4，0775/0750/0770
- `/data/misc` → 01771 11:11
- `/data/service/el1/public/wifi/{sockets,wpa_supplicant,dhcp}` → 0770 11:11
- `/data/service/el1/public/database/{dtbhardware_manager_service,distributeddata}/...` → 0770 11:11（含 key/meta/kvdb/backup 子树）
- `/storage/data/service/el1/public/huks_service/{maindata,bakdata}` → 0711 12:12

### service 启动顺序（init job 的 start 序列）

```
start ueventd            ← 先起 ueventd（建 /dev 节点）
start shell
start apphilogcat
start foundation         ← importance:1（稳态值，bring-up 期改 0，见 B8）
start appspawn
start wms_server
start bundle_daemon
start media_server
start deviceauth_service
start softbus_server
start devicemanagerservice
start wifi_manager_service
start wifi_hal_service
start faultloggerd
start devattest_service
start huks_server
```

## post-init job

```
start iotc_service       ← 依赖前序 service 就绪，故放 post-init
```

## services（18 个 service 定义基线）

> bring-up 期（B8）：所有 service `importance` 设 `0` + 去掉 `critical` 数组，防 service 退出 → init ReapService → reboot loop。稳定后恢复稳态值（watchdog_service=-20，foundation=1）。

| # | name | path | uid | gid | importance | caps | once | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | shell | `/sbin/getty -n -l /bin/sh -L 115200 ttyS000 vt100` | 0 | 0 | 0 | [4294967295] | 0 | 串口 shell |
| 2 | huks_server | `/bin/huks_server` | 0 | 12 | 0 | [23] | 0 | 密钥服务 |
| 3 | iotc_service | `/bin/iotc_service` | 0 | 0 | 0 | [] | 0 | IoT 连接（post-init 起） |
| 4 | foundation | `/bin/foundation` | 7 | 7 | **1** | [23] | 0 | 系统服务框架（稳态 importance=1，bring-up 期 0） |
| 5 | appspawn | `/bin/appspawn` | 1 | 1 | 0 | [2,6,7,8,11,17,23,24] | 0 | 应用孵化 |
| 6 | apphilogcat | `/bin/apphilogcat` | 4 | 4 | 0 | [] | 1 | 应用日志 |
| 7 | media_server | `/bin/media_server` | 0 | 0 | 0 | [] | 1 | 媒体 |
| 8 | wms_server | `/bin/wms_server` | 10 | 10 | 0 | [1,23] | 1 | 窗口管理 |
| 9 | bundle_daemon | `/bin/bundle_daemon` | 8 | 8 | 0 | [0,1,23] | 0 | 包管理 |
| 10 | hiview | `/bin/hiview` | 4 | 4 | 0 | [] | 1 | 日志视图 |
| 11 | deviceauth_service | `/bin/deviceauth_service` | 0 | 7 | 0 | [23] | 0 | 设备认证 |
| 12 | softbus_server | `/bin/softbus_server` | 0 | 7 | 0 | [23] | 0 | 软总线 |
| 13 | devicemanagerservice | `/bin/devicemanagerservice` | 0 | 7 | 0 | [] | 0 | 设备管理 |
| 14 | watchdog_service | `/bin/watchdog_service 10 2` | watchdog | watchdog | **-20** | [] | 0 | 看门狗（稳态 -20，bring-up 期 0；内核须先适配 watchdog 驱动见 prefer-driver-adaptation） |
| 15 | ueventd | `/bin/ueventd_linux` | ueventd | ueventd | 0 | [DAC_OVERRIDE,MKNOD,CHOWN,FOWNER] | 0 | 设备节点（含 socket；**critical 数组 bring-up 期去掉**） |
| 16 | wifi_manager_service | `/bin/wifi_manager_service` | 11 | 11 | 0 | [4294967295] | 0 | wifi 管理 |
| 17 | wifi_hal_service | `/bin/wifi_hal_service` | 11 | 11 | 0 | [4294967295] | 0 | wifi HAL |
| 18 | faultloggerd | `/bin/faultloggerd` | faultloggerd | system,4,faultloggerd | 0 | [CAP_KILL] | 0 | 故障日志（含 3 个 socket） |
| — | devattest_service | `/bin/devattest_service` | 20 | 20 | 0 | [23] | 1 | 设备 attest（init job 起，once=1） |

> 注：上表 18 项为 conf.txt 原始 services 数组（devattest_service 单列）。`once=1` 表示起一次即退（不重启）；`once=0` 表示常驻（退出会被重启/触发 ReapService）。`caps` 数字为 Linux capability bit。

### 特殊 service 字段

- **ueventd**：带 `socket`（AF_NETLINK ueventd）+ `critical: [0,15,5]` + `ondemand: true`。★ bring-up 期去掉 `critical` 数组（B8）。
- **faultloggerd**：带 3 个 `socket`（faultloggerd.server / faultloggerd.crash.server / faultloggerd.sdkdump.server，均 AF_UNIX SOCK_STREAM，permissions 0666）。
- **watchdog_service**：`uid/gid` 用名字（`watchdog`）非数字，path 带参数 `10 2`。
- **ueventd/faultloggerd**：`uid/gid` 用名字（`ueventd` / `faultloggerd` / `system`），需 `/etc/passwd` 有对应条目。

## 配套检查（与 SKILL.md 联动）

- **B6 启动项五件套**：pre-init 前补 mount proc/sysfs/cgroup/binder（本表不含，见 SKILL.md Step 4.5）。
- **B7 param 三件套**：rootfs 必有 `/system/etc/param/ohos_const/ohos.para` + `/system/etc/param/ohos.para` + `ohos.para.dac` + `/vendor/etc/param/vendor.para`，否则 softbus/deviceauth/huks 起不来（见 SKILL.md Step 4.5）。
- **B8 importance:0**：bring-up 期全改 0 + 去 critical，稳定后恢复 watchdog=-20/foundation=1（见 SKILL.md Step 4.5 + ohos-issue-lite-diagnose）。
- **B15 命令支持集**：init 不支持 mknod，用 `exec /bin/busybox mknod` 绕（见 SKILL.md）。

## hi3516cv610 bring-up 场景语料（L1 小型系统实测）

> 以下为 hi3516cv610 小型系统（L1）bring-up 期 init.cfg / rootfs 相关的具体场景案例。通用方法见各 SKILL.md 正文，本节是 hi3516cv610 实例。

### 场景 1：softbus_server 是 foundation 硬依赖（删了 → foundation RPC death loop）

hi3516cv610 L1 小型系统的 `foundation` 链接 `libdmslite` → `libdmslite` 又依赖 `libsoftbus_client`。即 `foundation` → `libdmslite` → `libsoftbus_client` → `softbus_server`（运行时 RPC 依赖）。

**实测教训**：bring-up 期 `softbus_server` 起不来，想"先删 softbus_server 减负" → 删后 `foundation` 启动即崩：`EPIPE -32` ×9478 次（RPC 对端没了）→ 板子挂死。

**结论**：`softbus_server` 是 `foundation` 的硬依赖，不能删。删 service 前必查 .so 依赖闭包（见 `04-build-verify` B8.2 删服务前依赖审计）：
```bash
readelf -d <rootfs>/bin/foundation | grep NEEDED    # 含 libdmslite
readelf -d <rootfs>/lib/libdmslite.so | grep NEEDED  # 含 libsoftbus_client
# softbus_server 是 libsoftbus_client 的运行时对端 → 删 softbus_server → foundation RPC 断 → EPIPE death loop
```

### 场景 2：11 服务 importance 全 0 清单（hi3516cv610 bring-up 期）

hi3516cv610 init.cfg bring-up 期所有 service 设 `importance: 0` + 去 `critical` 数组，防 reboot loop（见 `04-build-verify` B8）。bring-up 期全 0 清单：

| service | path | bring-up importance | 稳态恢复值 | 备注 |
|---|---|:---:|:---:|---|
| foundation | /bin/foundation | 0 | **1** | 核心 SA，稳态恢复 1（uid 须 0） |
| huks_server | /bin/huks_server | 0 | 0 | uid 须 0（SCHED_RR） |
| softbus_server | /bin/softbus_server | 0 | 0 | foundation 硬依赖（见场景 1） |
| watchdog_service | /bin/watchdog_service 10 2 | 0 | **-20** | 高优先级，稳态恢复 -20（内核须先适配 watchdog 驱动） |
| ueventd | /bin/ueventd_linux | 0 | 0 | 去 critical 数组（bring-up） |
| appspawn | /bin/appspawn | 0 | 0 | uid 须 0 |
| bundle_daemon | /bin/bundle_daemon | 0 | 0 | uid 须 0 |
| hiview | /bin/hiview | 0 | 0 | 日志 |
| apphilogcat | /bin/apphilogcat | 0 | 0 | 日志 |
| deviceauth_service | /bin/deviceauth_service | 0 | 0 | 设备认证 |
| devattest_service | /bin/devattest_service | 0 | 0 | 设备 attest（init job 起，once=1） |

> 稳态恢复时机 + 验证见 `04-build-verify` B8.1。恢复后必跑 XTS 核心用例 + 多次启动确认不回归 reboot loop。

### 场景 3：XTS 386→426 迭代案例（hi3516cv610）

hi3516cv610 XTS 从 386/426 迭代到 426/426 全过：

- **HUKS 0/40 → 40/40**：回溯 samgr_lite `NO_TASK` 同步分发（见 `diagnostic-cases.md` OH002）+ engine .so（OH003）+ uid（OH004）+ binder EACCES（OH005）。4 个子问题逐个修，HUKS 从 0 到 40。
- **deviceattest 0/3 → 3/3**：回溯 deviceattest 依赖链（见场景 4）。

迭代方法见 `{{ASSET_ROOT}}/workflow/steps/05-test-gen/SKILL.md` Step 3.5（XTS fail 分类回溯表）。

### 场景 4：deviceattest 适配要点（hi3516cv610）

`devattest_service` 依赖链：`device_auth` + `huks_server` + `/storage/deviceauth`。起不来常见原因与 HUKS 同链路：

1. **huks_server 没起 / 没发布 feature** → deviceattest 调 HUKS 失败（与 OH002 同根因：samgr_lite NO_TASK）
2. **device_auth .so 缺失** → 链接失败（与 OH003 同类：.so 没打进 rootfs/lib）
3. **`/storage/deviceauth` 目录/文件缺** → 认证数据读写失败（rootfs 目录树要建）
4. **uid 非 root** → 权限不足（与 OH004 同类：核心 SA uid 须 0）

**修复**：huks_server 修通（NO_TASK + uid + engine .so）后 deviceattest 自然通（同链路）。补 device_auth .so + 建 /storage/deviceauth 目录。

### 场景 5：samgr_lite NO_TASK 具体修法（hi3516cv610，对应 fault-knowledge-base §7.4 通用模式的实例）

OH samgr_lite 源码（hi3516cv610 L1 小型系统）的具体修法（对应 `fault-knowledge-base.md` §7.4 通用模式"服务注册 OK 但不分发"）：

1. **`GetTaskConfig` 的 `taskFlags`**：`SINGLE_TASK` → `NO_TASK`(0xFF)
   - `SINGLE_TASK`：异步排队模式，消息进队列需消费者线程 dispatch
   - `NO_TASK`：同步分发模式，注册时立即执行初始化和分发
2. **`AddTaskPool` 的 `NO_TASK` case**：走同步分发路径（不创建独立任务线程，在注册调用栈内直接 dispatch）
3. **构造器 `Init()` 只注册不做重活**：重活（`DEFAULT_Initialize` 等）放分发触发，构造器只做 `SAMGR_AddRouter` / `RegisterServiceApi` 等元信息登记

**验证**：改 NO_TASK 后加打印确认 `DEFAULT_Initialize` 被进入（之前从未进入）→ feature 发布 → 客户端 `GetFeatureApi` 成功。完整诊断链见 `diagnostic-cases.md` OH002。

> memory：`samgr-lite-no-task-sync-dispatch`（samgr_lite 服务 GetTaskConfig 用 SINGLE_TASK→异步排队不消费→DEFAULT_Initialize 永不执行；改 NO_TASK 走同步分发）。
