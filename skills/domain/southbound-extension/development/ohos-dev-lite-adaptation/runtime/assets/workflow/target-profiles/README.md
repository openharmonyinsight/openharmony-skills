# Target Profiles（target profile 目录说明）

P2/P3 是通用的工作流阶段。target profile 选择芯片/系统特定的实现路线，不改变阶段本身。

必填字段：

- `kernel_family`：`linux` / `liteos_a` / `liteos_m` 或其他受支持值
- `driver_model`：`linux_kernel` / `linux_kernel_plus_oh_integration` / `hdf` / `iot_hal` 或其他受支持值
- `device_description`：`dts` / `hcs` / `config_struct` 或其他受支持值
- `build_integration`：目标如何进入项目构建
- `source_strategy`：`vendor` / `adapted` / `greenfield`
- `required_outputs`：P2/P3 必须产出的具体文件/目标

可选字段：

- `boot_medium` / `storage`：启动介质与 rootfs/数据介质。**双介质板两者不同**（如 SPI Nand 启动 + eMMC 放 rootfs）——`boot_medium` 决定 boot_image 构建的 BOOT_MEDIA（选错烧出 0x81），`storage` 决定 rootfs 文件系统（eMMC→ext4 / NOR→jffs2 / NAND→jffs2 或 ubifs）。与 `workflow_config.yaml` 的 `intake.boot.medium` 对账，用户确认值优先，冲突时停下问用户。
- `burn_package`（L1 烧录包策略）：`image_size_policy`（fit=镜像≤分区 / fixed=填满分区）、`boot_chain.required_inputs` + `missing_policy: BLOCKED_VENDOR_SDK`（vendor 启动链输入缺失即阻塞，禁止伪造 boot_image）、`required_artifacts`（完整包产物清单，rootfs 类型跟随介质，与 `workflow_config.yaml` 的 `burn.package.closure.required_files` 对应）。

profile 是路由数据，不是通用规则。没有 profile 时，工作流必须在 profile 选定处停下、先建 profile 再进实现（编排器 §target profile 加载规则）。
