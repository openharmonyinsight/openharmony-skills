# hilog 驱动适配 playbook

> 缺 `/dev/hilog` → `apphilogcat: hilog fd failed No such file or directory` → hilog/hiview 起不来。来源：hi3516cv610 实战。hilog 是「驱动有但节点不自动建」的典型——驱动适配（开 CONFIG）+ pre-init mknod 缺一不可。

## 症状

```
apphilogcat: hilog fd failed No such file or directory    ← /dev/hilog 不存在
```
hilog/hiview/apphilogcat 起不来。

## 根因

OH hilog 驱动（`drivers/staging/hilog`）注册字符设备但**不调 `device_create`** → devtmpfs 不会自动建 `/dev/hilog`。即使 `CONFIG_HILOG` 开了驱动编入内核，`/dev/hilog` 也不会自动出现，必须在 init.cfg pre-init 手动 mknod。

## 适配操作

### 1. defconfig 开 CONFIG

```
CONFIG_STAGING=y          # hilog 在 drivers/staging 下
CONFIG_HILOG=y            # OH hilog 驱动
```

### 2. init.cfg pre-init 手动 mknod（关键）

hilog 驱动不 `device_create` → 必须在 init.cfg pre-init 用 busybox mknod 建节点：

```json
// init.cfg pre-init jobs
"exec /bin/busybox mknod /dev/hilog c 245 0",
"chmod 0666 /dev/hilog"
```

**三个陷阱**：

| 陷阱 | 正确做法 |
|------|---------|
| 用 OH init 原生 `mknod` 命令 | OH init **不支持原生 mknod**（init.cfg 的 `exec` 走 OH init 内置命令集，无 mknod）。必须 `exec /bin/busybox mknod`（busybox 进 rootfs） |
| 猜 major 设备号 | major **245** = `drivers/staging/hilog/hilog.c` 的 `HILOGDEV_MAJOR`，核对源码确认；或 `cat /proc/devices` 查 hilog 实际注册的主号（驱动 `alloc_chrdev_region` 动态分配时每次可能不同，别猜） |
| 不放开权限 | 必须 `chmod 0666`——hilog 需用户态进程（apphilogcat 等）读写，不放开权限起不来 |

### 3. 重编 + 烧后验证

```bash
ls /dev/hilog             # 节点出现
cat /proc/devices | grep hilog   # 核对 major 号
```
apphilogcat 不再 `fd failed`，hilog/hiview 起来。

## 原则

- **hilog 是「驱动有但节点不自动建」典型**：开 CONFIG（驱动编入）+ pre-init mknod（建节点）缺一不可。别以为开了 CONFIG 就有节点。
- **OH init 无 mknod 命令**：要用 `exec /bin/busybox mknod`，别裸 `mknod`。关联 `../ohos-issue-lite-diagnose/references/fault-knowledge-base.md` §7.1（mknod 陷阱）。
- **major 号从源码/`/proc/devices` 查**：别猜，动态分配的主号每次可能不同。

## 关联

- `{{ASSET_ROOT}}/workflow/steps/03-driver-device/SKILL.md` §hilog 驱动适配 + mknod 陷阱
- `../ohos-issue-lite-diagnose/references/fault-knowledge-base.md` §7.1 设备节点 mknod 陷阱
- `config-devnode-map.md`（hilog 行：CONFIG_HILOG → /dev/hilog → hilog/hiview 依赖）
