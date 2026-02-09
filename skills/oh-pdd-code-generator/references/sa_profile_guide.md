# SA Profile 配置指南

本文档介绍 OpenHarmony System Ability (SA) 配置文件的编写规范。

## SA 配置文件 (5001.json)

### 文件位置

```
services/native/5001.json
```

### 基本结构

```json
{
  "sa-id": 5001,
  "sa-name": "disk_management",
  "run-on-create": true,
  "auto-start": true,
  "start-mode": "boot",
  "process": "disk_management_service",
  "dump-level": "control",
  "critical": [1, 4, 240],
  "permission": [],
  "jobs": [],
  "seon": [],
  "libpath": "libdisk_management_sa.z.so"
}
```

## 字段说明

### sa-id (必需)

System Ability 的唯一标识符

| SA ID 范围 | 类别 |
|-----------|------|
| 1000-1999 | 基础服务 |
| 4000-4999 | 数据存储 |
| 5000-5999 | 文件管理 |
| 6000-6999 | 多媒体 |
| 7000-7999 | 图形 |
| 8000-8999 | AI |

```json
"sa-id": 5001
```

### sa-name (必需)

SA 的名称，需与进程名相关

```json
"sa-name": "disk_management"
```

### run-on-create (可选)

是否在 SA 加载时立即运行

```json
"run-on-create": true
```

### auto-start (可选)

是否自动启动

```json
"auto-start": true
```

### start-mode (可选)

启动模式

| 值 | 说明 |
|----|------|
| boot | 开机启动 |
| condition | 条件启动 |
| on-demand | 按需启动 |

```json
"start-mode": "boot"
```

### process (必需)

运行的进程名

```json
"process": "disk_management_service"
```

### dump-level (可选)

dump 命令支持级别

| 值 | 说明 |
|----|------|
| control | 控制 |
| info | 信息 |
| full | 完整 |

```json
"dump-level": "control"
```

### critical (可选)

关键服务重启配置

```json
"critical": [1, 4, 240]
```

格式: `[启动优先级, 最小运行次数, 重启等待时间]`

### permission (可选)

需要的权限列表

```json
"permission": [
  "ohos.permission.STORAGE_MANAGER",
  "ohos.permission.WRITE_USER_STORAGE"
]
```

### jobs (可选)

启动任务

```json
"jobs": [
  {
    "name": "boot",
    "value": "start"
  }
]
```

### seon (可选)

系统启动时运行的服务

```json
"seon": ["disk_management_service"]
```

### libpath (必需)

共享库路径

```json
"libpath": "libdisk_management_sa.z.so"
```

## Init 配置文件 (disk_management.cfg)

### 文件位置

```
services/native/disk_management.cfg
```

### 基本结构

```json
{
  "services": [{
    "name": "disk_management_service",
    "path": [
      "/system/bin/sa_main",
      "/system/profile/disk_management/5001.json"
    ],
    "critical": [1, 4, 240],
    "uid": "root",
    "gid": ["root", "system"],
    "start-mode": "boot",
    "writepid": [
      "/dev/cpuset/foreground/tasks"
    ]
  }]
}
```

## 字段说明

### name (必需)

服务名称，需与 SA 配置中的 process 一致

### path (必需)

启动命令和参数

```json
"path": [
  "/system/bin/sa_main",
  "/system/profile/disk_management/5001.json"
]
```

### uid (可选)

运行用户 ID

```json
"uid": "root"
```

### gid (可选)

运行组 ID 列表

```json
"gid": ["root", "system"]
```

### writepid (可选)

PID 文件写入位置

```json
"writepid": ["/dev/cpuset/foreground/tasks"]
```

## 完整示例

### SA 配置 (5001.json)

```json
{
  "sa-id": 5001,
  "sa-name": "disk_management",
  "run-on-create": true,
  "auto-start": true,
  "start-mode": "boot",
  "process": "disk_management_service",
  "dump-level": "control",
  "critical": [1, 4, 240],
  "permission": [
    "ohos.permission.STORAGE_MANAGER"
  ],
  "jobs": [
    {
      "name": "boot",
      "value": "start"
    }
  ],
  "seon": ["disk_management_service"],
  "libpath": "libdisk_management_sa.z.so"
}
```

### Init 配置 (disk_management.cfg)

```json
{
  "services": [{
    "name": "disk_management_service",
    "path": [
      "/system/bin/sa_main",
      "/system/profile/disk_management/5001.json"
    ],
    "critical": [1, 4, 240],
    "uid": "root",
    "gid": ["root", "system"],
    "start-mode": "boot",
    "writepid": [
      "/dev/cpuset/foreground/tasks"
    ]
  }]
}
```

## BUILD.gn 配置

```gni
ohos_sa_profile("disk_management_sa_profile") {
  sources = [ "${disk_management_native_path}/5001.json" ]
  part_name = "disk_management"
}

ohos_prebuilt_etc("disk_management_cfg") {
  source = "${disk_management_native_path}/disk_management.cfg"
  relative_install_dir = "init"
  part_name = "disk_management"
  subsystem_name = "filemanagement"
}
```

## 常见错误

### 错误 1：sa-id 重复

同一系统中 sa-id 不能重复

### 错误 2：进程名不匹配

`process` 字段必须与 init 配置中的 `name` 一致

### 错误 3：libpath 错误

库文件名必须以 `.z.so` 结尾

### 错误 4：路径格式

使用正斜杠 `/`，不要使用反斜杠 `\`
