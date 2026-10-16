# 通用故障模式库（鸿蒙）——索引

分析时必须对照本库逐类扫描，避免遗漏。库按 18 个大类拆分为独立文件，**只读取与被分析模块相关的类别**，不必全量加载；18 类为大体量压测素材，仅在稳定性/压测场景按路由加载。

**两级加载**：每类配一个触发索引 `triggers/NN-xxx.md`（每条目一行：ID / 故障模式 / 触发条件）。先读触发索引做扫描判定；条目触发条件命中后，再到该类文件 `NN-xxx.md` 读取对应 `### ID` 条目详情（未命中的条目不加载详情）。跳过触发索引直读类文件全文视为路由违规。

各分类文件不再重复本行（本索引是五要素的唯一定义处）。每条模式包含【典型原因】【典型影响】【故障注入】【日志/Trace】【消减建议】五要素。分析时将模式实例化为被分析对象的具体故障模式（标注代码位置或设计环节）；被代码证据排除的模式不列出。

## 编号规则

- 每个文件内条目使用独立前缀，全局唯一，格式为 `前缀-序号`（如 F-01、AF-12、NET-02a）。
- 带字母后缀（如 HW-01a、P-03b）表示该大类下的子条目；`##` 为章节/条目组标题，`###` 为具体故障模式条目。
- 输出 FMEA 表格时，在"故障原因"列尾注记本库编号（如 `（库依据：I-03）`）便于追溯。

## 文件索引

| 文件 | 类别 | 适用场景 | 条目前缀与范围 |
|---|---|---|---|
| [01-data-file.md](01-data-file.md) | 数据文件故障模式 | 涉及文件读写的模块（配置、缓存、日志、持久化） | F-01 ~ F-08（F-01 含常见损坏与异常类型清单：文件不存在、0 字节、没权限、数据只有一半、畸形内容、fd 误用、fd 超限；F-01a 掉电窗口专项；F-06a fd 误用） |
| [02-database.md](02-database.md) | 数据库故障模式 | 使用 RDB/Preferences/KV 存储的模块，含主备双库场景 | D-01 ~ D-11（D-01a 数据库文件损坏，D-09 主备其一损坏，D-10 主备同时损坏，D-11 未持锁访问） |
| [03-ipc.md](03-ipc.md) | IPC 故障模式 | 跨进程通信、SystemAbility 服务、SA 客户端、接口契约与消息流控 | I-01 ~ I-16 |
| [04-ffrt.md](04-ffrt.md) | FFRT 故障模式 | 使用 FFRT 任务调度的模块 | R-01 ~ R-07 |
| [05-libc.md](05-libc.md) | libc / libc++ 故障模式 | Native C/C++ 代码、NDK 动态库 | C-01 ~ C-10 |
| [06-memory-resource-leak.md](06-memory-resource-leak.md) | 内存与资源泄漏故障模式 | 缓存、长驻服务、Ashmem、RefBase 对象 | M-01 ~ M-05 |
| [07-thread-concurrency.md](07-thread-concurrency.md) | 线程与并发故障模式 | 自建线程/线程池、锁与同步原语、Timer、事件循环 | T-01 ~ T-06 |
| [08-napi-arkts.md](08-napi-arkts.md) | NAPI / ArkTS 边界故障模式 | NAPI 中间件、ArkTS 状态管理、XComponent | N-01 ~ N-10 |
| [09-appfreeze.md](09-appfreeze.md) | 主线程卡死 / AppFreeze 故障模式 | UI 进程、主线程同步等待、跨线程互锁 | A-01 ~ A-05 |
| [10-cutils-parcel.md](10-cutils-parcel.md) | C-Utils / Parcel 组件使用陷阱 | 使用 c_utils 组件（SafeMap、Parcel、Timer 等）的 Native 模块 | U-01 ~ U-05 |
| [11-high-risk-operations.md](11-high-risk-operations.md) | 高危操作故障模式 | **所有模块必扫**：进程自杀/杀进程/跨模块删数据/直操作他模块数据库/跨模块释放内存等非配对操作 | H-01 ~ H-08 |
| [12-app-framework.md](12-app-framework.md) | 应用框架与业务可靠性故障模式 | UIAbility/ServiceExtensionAbility/DataShare 生命周期、公共事件、窗口与输入事件、Binder、事件队列、方舟 GC、通知、多实例、USB 配件 | AF-01 ~ AF-36 |
| [13-version-compatibility.md](13-version-compatibility.md) | 版本配套可靠性故障模式 | OTA、跨设备协同、多模块版本兼容性 | V-01 ~ V-06 |
| [14-hardware-driver.md](14-hardware-driver.md) | 硬件与驱动故障模式 | CPU/GPU/TP/内存/存储硬件故障、底层存储视角数据库故障、驱动加载与运行异常 | HW-01a ~ HW-06b，DRV-01 ~ DRV-09 |
| [15-process-fault.md](15-process-fault.md) | 进程与线程故障模式 | 进程崩溃/挂死/异常状态、线程故障、资源耗尽、Binder 与 Socket 通道异常 | P-01a ~ P-05d |
| [16-network-distributed.md](16-network-distributed.md) | 网络与分布式故障模式 | 近场/远场通信（BLE、WiFi P2P、丢包错包）、分布式发现连接/传输/同步/组网、虚拟设备 | NET-01a ~ NET-02i，CS-01a ~ CS-05f，DS-01a ~ DS-07b |
| [17-virtualization.md](17-virtualization.md) | 虚拟化故障模式 | 虚拟机/容器异常、共享内存、vNotify 通道、Host/Guest 时钟与中断 | VM-01a ~ VM-06e |
| [18-system-stability.md](18-system-stability.md) | 系统稳定性与压力故障模式 | 内核/调度/中断、文件系统极限、媒体压力、休眠唤醒、折叠开合、设备组网、老化压测 | S-01a ~ S-13e |

> 原语料中的 19（API 接口可靠性）/ 20（业务域数据文件可靠性）/ 21（业务域故障注入与边界值测试设计）三类为业务域绑定素材，对 OpenHarmony 平台级 FMEA 无参考价值，已剔除（2026-09-26 维护者决策）。13 类中的业务域版本配套专项（V-07~V-36，取自原 22 类素材）与 18 类中的 S-14 业务稳定性（S-14a~o）同属业务域绑定素材，已一并剔除（2026-09-29），13 类仅保留 V-01~V-06 通用模式、18 类保留 S-01~S-13。

## 加载路由

类文件加载路由以 `odk-fmea` SKILL.md「通用故障模式库」一节为唯一定义处（按模块类别选择类文件；任何模块必扫 11；18 类仅稳定性/压测场景加载）。非代码输入的选类补充：设计文档按模块功能映射对应类别逐条推演；问题列表按根因反查对应类别横向扫描。

## 扩展来源

上游取材 gitcode.com/stesen1/harmonyos-fmea 工程文档集，仅作同步源，无需外部资源可达。01~05、11 为 ODK 自建；06~10 取自鸿蒙稳定性开发文档集；12~18 取自业务可靠性/稳定性测试设计文档集。语料内部代号（如 `rphone`）的语义与替换见 fault-injection.md 补充手段表。
