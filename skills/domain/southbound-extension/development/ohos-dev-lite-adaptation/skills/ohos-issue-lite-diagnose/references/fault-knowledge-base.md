# 故障知识库

> 本文件是 OpenHarmony Lite（L0/L1）芯片适配全链路故障知识库，覆盖编译、链接、启动、驱动、运行时五大类故障。每条知识包含错误模式、根因分析、修复方案和预防措施。

---

## 1. 编译错误 (Compilation Errors)

编译错误是Lite芯片适配中最先遇到、也是最高频的问题类型，约占所有适配问题的40%。

### 1.1 头文件缺失

**错误模式**: `fatal error: xxx.h: No such file or directory`

**常见场景与修复**:

| 缺失头文件 | 原因 | 修复方案 |
|-----------|------|---------|
| `cmsis_os2.h` | CMSIS头文件路径未配置 | BUILD.gn添加 `"//kernel/liteos_m/kal/cmsis/CMSIS/RTOS2/Include"` |
| `iot_gpio.h` | IoT外设驱动组件未启用 | product.json的subsystems中添加gpio组件 |
| `gpio_if.h` | HAL头文件路径缺失 | BUILD.gn添加 `"//drivers/lite/include"` |
| `los_task.h` | LiteOS-M内核头文件路径缺失 | BUILD.gn添加 `"//kernel/liteos_m/kernel/include"` |
| `iot_wifi.h` | WiFi组件未在product.json中启用 | subsystems中添加wifi组件 |
| `stm32f4xx_hal_spi.h` | Kconfig中SPI平台驱动未开启 | menuconfig中启用SPI Platform Driver |

**通用排查步骤**:
1. 在代码库中搜索该头文件的实际位置
2. 确认BUILD.gn中的include_dirs是否包含该路径
3. 确认Kconfig中是否需要开启对应功能
4. 确认product.json中是否需要添加对应子系统

### 1.2 宏/类型未定义

**错误模式**: `error: 'XXX_TYPE' undeclared`

**常见原因**:
- Kconfig选项未开启导致条件编译排除了相关定义
- CMSIS/HAL版本变更导致类型名改变
- 缺少必要的头文件包含

**修复方案**:
```yaml
- error_id: ARM-GCC-IMPLICIT-FUNCTION-DECLARATION
  compiler: [arm-none-eabi-gcc, riscv32-unknown-elf-gcc]
  severity: error (when -Werror)
  pattern: "implicit declaration of function '{func_name}'"
  category: header_missing
  root_causes:
    - cause: "缺少包含{func_name}声明的头文件"
      probability: 0.60
      fix: "添加 #include <对应头文件>"
    - cause: "CMSIS头文件路径变更"
      probability: 0.25
      fix: "更新include_dirs中的CMSIS路径"
    - cause: "Kconfig选项未开启导致条件编译排除"
      probability: 0.15
      fix: "在Kconfig/menuconfig中开启对应选项"
  lite_context:
    common_headers:
      "IoSetFunc": "<iot_io.h>"
      "GpioOpen": "<gpio_if.h>"
      "osThreadNew": "<cmsis_os2.h>"
      "LOS_TaskCreate": "<los_task.h>"
      "IotWifiInit": "<iot_wifi.h>"
```

### 1.3 arm-gcc/riscv-gcc兼容性

**常见问题**:
- 不同GCC版本的编译选项差异
- `-Werror`将警告升级为错误
- RISC-V GCC与ARM GCC的内联汇编语法差异

### 1.4 GN/build_lite配置错误

**错误模式**: `ERROR at //BUILD.gn:xx: Undefined identifier`

**排查步骤**:
1. 检查GN语法是否正确
2. 确认引用的.gni文件路径存在
3. 确认变量在使用前已定义
4. 检查import语句的路径

### 1.5 Kconfig依赖不满足

**错误模式**: 某些功能需要的Kconfig选项未开启，导致条件编译排除了关键代码

**排查方法**:
```bash
# 使用menuconfig查看和修改Kconfig
make menuconfig
# 或在build_lite中
python build/lite/build.py product=xxx --gn-args loSCFG_xxx=true
```

---

## 2. 链接错误 (Linker Errors)

### 2.1 未定义符号

**错误模式**: `undefined reference to 'xxx'`

**根因**: 缺少库文件或链接顺序错误

**修复方案**:
1. 搜索符号定义所在的源文件
2. 在BUILD.gn的deps中添加对应的库
3. 确认链接顺序（被依赖的库放在后面）

### 2.2 RAM段溢出

**错误模式**: `region 'RAM' overflowed by N bytes`

**这是Lite系统最常见的链接错误**。MCU RAM极其有限（128KB~数百KB），启用WiFi/BLE等协议栈后很容易溢出。

**诊断步骤**:
1. 分析.map文件找出RAM占用Top模块
2. 计算各组件的RAM开销

**修复方案（按效果排序）**:
```
1. 移除不需要的组件（如不需要BLE则移除 -60KB）
2. 减缓冲池大小（如WiFi: WLAN_MEM_POOL_SIZE 64K→48K）
3. 启用LTO: cflags += ["-flto"]
4. 使用-nano-specs减小newlib体积
5. 减小堆栈大小（基于栈分析结果）
6. 将只读数据移至Flash (.rodata)
7. 裁剪Kconfig中的非必要功能
```

### 2.3 Flash溢出

**错误模式**: `region 'FLASH' overflowed by N bytes`

**修复方案**:
```
1. 启用-Os优化
2. 启用LTO (-flto)
3. 移除未使用的代码和库
4. 使用-nano-specs
5. 减少printf格式化字符串
6. 将大常量表压缩或移到外部存储
```

### 2.4 重复定义

**错误模式**: `multiple definition of 'xxx'`

**修复方案**:
- 使用`__attribute__((weak))`标记弱符号
- 合并重复的模块
- 检查是否有同一源文件被多次编译

### 2.5 C/C++链接不匹配

**错误模式**: C++调用C库时名称修饰不一致

**修复方案**: 在C头文件中添加`extern "C"`包裹

---

## 3. LiteOS-M 启动失败

### 3.1 启动失败决策树

```
LiteOS-M启动失败
├── 完全无输出
│   ├── 启动代码未执行 → 检查镜像烧录是否正确、复位向量地址
│   ├── 时钟配置错误 → 检查SystemClock_Config、外部晶振连接
│   ├── 堆栈指针错误 → 检查startup.s中SP初始值
│   └── 串口引脚/波特率错误 → 确认TX引脚复用、波特率匹配
├── 部分输出后停止
│   ├── 内存区域配置错误 → 检查LD脚本中RAM/FLASH地址与实际一致
│   ├── 中断控制器初始化失败 → 检查NVIC/PLIC配置
│   ├── 堆初始化失败 → 检查HEAP大小不超过可用RAM
│   └── 内核对象初始化失败 → 检查Kconfig配置完整性
└── 内核init成功但任务不运行
    ├── 任务栈溢出 → 增大栈大小
    ├── 任务优先级问题 → 检查优先级配置
    ├── 调度器未启动 → 检查LOS_Start()是否被调用
    └── 硬件定时器未配置 → 检查SysTick/Tick Timer配置
```

### 3.2 完全无输出的排查流程

1. **确认硬件连接**: JTAG/SWD能否连接到芯片？
2. **确认固件烧录**: Flash内容是否正确？向量表是否在正确地址？
3. **检查VTOR**: SCB->VTOR是否与链接脚本中FLASH ORIGIN一致？
4. **检查时钟**: HSE/HSI是否正常？PLL配置是否正确？
5. **检查串口**: TX/RX引脚是否正确？AF模式是否配置？波特率是否匹配？
6. **检查启动代码**: SP初始值是否指向有效RAM区域？

### 3.3 HardFault快速诊断

#### ARM Cortex-M CFSR位域解析

```yaml
hardfault_diagnosis:
  cfsr_bits:
    IBUSERR:
      bit: 0
      meaning: "指令总线错误"
      causes: ["跳转到无效地址", "Flash读取错误"]
    PRECISERR:
      bit: 1
      meaning: "精确数据总线错误"
      causes: ["访问无效外设地址", "外设时钟未使能"]
      check_bfar: true
    IMPRECISERR:
      bit: 2
      meaning: "非精确数据总线错误"
      causes: ["写缓冲中的错误", "PC不一定指向出错指令"]
    UNSTKERR:
      bit: 3
      meaning: "出栈错误"
      causes: ["栈指针被破坏", "异常返回时栈不可访问"]
    STKERR:
      bit: 4
      meaning: "入栈错误"
      causes: ["栈溢出", "异常入口时栈空间不足"]
    BFARVALID:
      bit: 7
      meaning: "BFAR寄存器包含有效故障地址"
      
  quick_diagnosis:
    - condition: "CFSR.STKERR == 1"
      diagnosis: "栈溢出 - 增大任务栈或减小程序栈使用"
    - condition: "CFSR.PRECISERR == 1 && BFAR != 0"
      diagnosis: "访问地址{BFAR}无效 - 检查外设地址映射和时钟使能"
    - condition: "CFSR.IBUSERR == 1"
      diagnosis: "指令获取失败 - 检查Flash内容、跳转目标"
    - condition: "CFSR.UNDEFINSTR == 1"
      diagnosis: "未定义指令 - 检查代码完整性、函数指针有效性、FPU是否启用"
    - condition: "CFSR.DIVBYZERO == 1"
      diagnosis: "除零错误 - 检查除法运算前的除数校验"
```

#### HardFault串口输出模板

```c
/* Fault Handler - 通过串口输出Fault信息 */
void HardFault_Handler(void) {
    uint32_t cfsr = SCB->CFSR;
    uint32_t hfsr = SCB->HFSR;
    uint32_t bfar = SCB->BFAR;
    uint32_t msp = __get_MSP();
    uint32_t psp = __get_PSP();
    
    printf("\n=== HardFault Handler ===\n");
    printf("CFSR:  0x%08X\n", cfsr);
    printf("HFSR:  0x%08X\n", hfsr);
    if (cfsr & 0x80) {  /* BFARVALID */
        printf("BFAR:  0x%08X\n", bfar);
    }
    printf("MSP:   0x%08X\n", msp);
    printf("PSP:   0x%08X\n", psp);
    printf("=========================\n");
    
    while (1);  /* 停在此处等待JTAG调试 */
}
```

---

## 4. IoT子系统组件问题（L0特有）

> ⚠️ **关键区别**：L0不使用HDF框架，因此不存在"HDF驱动加载失败"的问题。L0的问题集中在IoT外设组件注册和HAL接口实现上。

### 4.1 组件注册失败

**日志模式**: `[ERROR] xxx component register failed, ret=N`

**排查步骤**:
1. 检查组件名是否重复
2. 检查方法表(Method结构体)是否完整
3. 追溯HAL层Init函数返回值
4. 检查外设时钟是否使能

### 4.2 HAL接口返回错误

**排查步骤**:
1. 确认HAL层实现的参数校验逻辑
2. 检查硬件是否就绪（时钟、引脚复用）
3. 对比芯片规格书确认寄存器操作正确性

### 4.3 CMSIS接口不兼容

**症状**: CMSIS API调用返回osError

**排查**: 对照CMSIS-RTOS2标准检查实现是否符合规范

---

## 5. 运行时异常 (Runtime Faults)

### 5.1 异常类型速查表

| 异常类型 | ARM表现 | RISC-V表现 | 典型原因 | 调试方法 |
|---------|--------|-----------|---------|---------|
| **HardFault** | HardFault_Handler触发 | Trap异常 | 非法指令、未对齐访问、权限违规 | JTAG/SWD查看寄存器+CFSR |
| **栈溢出** | MSP/PSP超出范围 | SP超出范围 | 局部变量过大、递归过深、ISR嵌套 | 栈水位标记+栈分析 |
| **内存不足** | malloc返回NULL | malloc返回NULL | 堆耗尽、内存泄漏 | 堆统计+map文件分析 |
| **看门狗复位** | 系统突然重启 | 系统突然重启 | 程序跑飞、死循环无喂狗 | 看门狗日志+GPIO翻转 |
| **BusFault** | BusFault_Handler | Bus Error | 访问无效地址、外设时钟未开 | JTAG查看BFAR寄存器 |
| **UsageFault** | UsageFault_Handler | Illegal Instruction | 除零、未定义指令 | JTAG查看UFSR寄存器 |

### 5.2 栈溢出专项诊断

**检测方法**:
1. 编译时添加`-fstack-usage`生成.su文件
2. 对比每个函数的栈使用量与任务栈大小
3. 运行时使用栈水位标记(Stack Watermark)检测

**修复方案**:
- 增大任务栈大小（Kconfig或TSK_INIT_PARAM_S.uwStackSize）
- 将大数组改为静态分配(`static`)
- 消除递归调用
- ISR中使用最小化局部变量

### 5.3 看门狗复位诊断

**排查步骤**:
1. 确认复位原因是看门狗（查看复位原因寄存器）
2. 检查看门狗超时时间设置
3. 在主循环和长耗时操作中添加GPIO翻转标记
4. 定位无喂狗的时间窗口
5. 添加喂狗操作或调整超时时间

### 5.4 内存泄漏诊断

**方法**:
- 定期打印堆空闲大小(`LOS_MemFreeSizeGet`)
- 使用堆统计工具追踪分配/释放配对
- 分析长时间运行后的堆使用趋势

### 5.5 LiteOS-M 内核堆内存配置宏速查（⚠️ L0 专属，非所有场合适用）

> **⚠️ 适用范围声明**：本节宏是 **L0（LiteOS-M）内核堆内存配置宏**，**仅 L0 适配（Hi3861 等 MCU 级芯片）时适用**。L1（LiteOS-A / Linux）内核堆配置**不同**——Linux 用 memblock/bootmem，LiteOS-A 用 `LOSCFG_MEM_*` 系列，本节宏不适用 L1。诊断前先按 `ohos-dev-soc-spec-parse` 的 L0/L1 分流确认系统类型，别把 L0 宏套到 L1。

**三个核心宏**：

| 宏 | 含义 | 配置示例 |
|---|---|---|
| `LOSCFG_SYS_EXTERNAL_HEAP` | 内核堆是否由外部提供。`=y`：用户指定地址/大小；`=n`：内核自动从 RAM 分配 | `LOSCFG_SYS_EXTERNAL_HEAP=y` |
| `LOSCFG_SYS_HEAP_ADDR` | 堆起始地址（`EXTERNAL_HEAP=y` 时生效） | `LOSCFG_SYS_HEAP_ADDR=0x20000000` |
| `LOSCFG_SYS_HEAP_SIZE` | 堆大小（`EXTERNAL_HEAP=y` 时生效） | `LOSCFG_SYS_HEAP_SIZE=0x10000` |

**配错症状链**：

```
地址/大小不对
  → 内核堆挂载到错误位置
  → 踩内存 / 访问越界
  → HardFault（栈溢出样表现，见 §5.2）/ 数据损坏 / 随机崩溃
```

**诊断要点**：
- 怀疑堆配置问题时，先核对 `LOSCFG_SYS_HEAP_ADDR` + `LOSCFG_SYS_HEAP_SIZE` 与链接脚本（LD）中 RAM 区域是否一致
- `EXTERNAL_HEAP=n` 时内核自动分配，不需手填地址/大小；`EXTERNAL_HEAP=y` 时三个宏必须配套且地址落在可用 RAM 内
- 配错常表现为"启动初期看似正常，运行一段时间后随机崩溃"——区别于栈溢出（有明确溢出函数）

**来源**：官方 `porting-chip-faqs`（LiteOS-M 芯片移植 FAQ）——
`https://gitee.com/openharmony/docs/raw/master/zh-cn/device-dev/porting/porting-chip-faqs.md`

---

## 6. 性能与功耗问题

### 6.1 中断延迟过高

**分析方法**: GPIO翻转计时、逻辑分析仪
**优化方向**: ISR最小化、减少临界区长度、优化中断优先级

### 6.2 功耗异常

**排查步骤**:
1. 逐个禁用外设，定位电流消耗源
2. 检查低功耗模式下各外设时钟是否关闭
3. 检查GPIO引脚是否配置为模拟模式（最低漏电）
4. 确认唤醒源配置正确

### 6.3 Flash磨损

**预防**: 写入计数、扇区分布分析、磨损均衡算法

### 6.4 启动速度慢

**优化**: GPIO标记+示波器测量、并行化初始化、延迟初始化非必要外设

---

## 7. OHOS init / 服务启动故障（L1 小型系统特有，实测 Hi3516CV610 实战）

> 芯片适配过烧录/内核启动关后，会卡在 OHOS init（samgr/foundation/各 service 启动）。这类问题报错日志在 user 态而非内核，常表现为 service 反复重启 + `samgr` boot step 超时。以下知识来自 hi3516cv610 小型系统（L1）rootfs 起来后的 init 阶段。配套真实案例见 `references/diagnostic-cases.md` §9。

### 7.1 设备节点 mknod 陷阱 — 驱动未 device_create → /dev/xxx 不自动建

**错误模式**：
```
apphilogcat: hilog fd failed No such file or directory    ← /dev/hilog 不存在
（或某 service: open /dev/xxx failed No such file or directory）
```

**根因**：L1 驱动若不在 init/probe 时调用 `device_create()`（或对应 misc device 注册），`/dev/<node>` 不会自动创建。OH init 起来后 user 态 service open `/dev/xxx` → `No such file`。典型：hilog 驱动只注册了 file_operations 但没 `device_create`，`/dev/hilog` 缺失，apphilogcat 起来 open 失败。

**修复方案**：OH init 没有 `mknod` 命令（不是 busybox init），不能靠 init 脚本 `mknod`。两条路：
1. **改驱动**（根治）：在 hilog/对应驱动 init 时补 `device_create()`（或 `misc_register` 让 udev/devtmpfs 自动建节点）。需改内核/vendor 驱动源码重编。
2. **init.cfg 手动 mknod**（绕过，应急）：在 `init.cfg` 的 early 阶段用 busybox mknod：
   ```json
   // system/etc/init.cfg  jobs → "pre-init" 或 "early-init" 阶段
   { "name": "exec /bin/busybox mknod /dev/hilog c 245 0", ... }
   ```
   主次设备号（`245 0`）按该驱动在内核注册的 `alloc_chrdev_region` 实际分配值填（`cat /proc/devices` 查 hilog 的主号）。

**教训**：
- ① **`/dev/xxx No such file` + 驱动已编译进内核 → 优先查驱动有没有 `device_create`**。OH init 无 mknod 命令，节点不自动建就不会有。
- ② **OH init 无 mknod 命令**——不能像 busybox init 那样在 init 脚本里裸 `mknod`，要用 `exec /bin/busybox mknod`（busybox 进 rootfs）。
- ③ **应急 mknod 的主次设备号要从 `/proc/devices` 查实际分配值**——别猜，驱动 `alloc_chrdev_region` 动态分配的主号每次可能不同。

### 7.2 链接错误 — musl ld 用错版本 → 全 service `Error relocating: __fd_chk: symbol not found`

**错误模式**：rootfs 起来，每个 service 一启动就报：
```
CANNOT LINK EXECUTABLE "foundation": Error relocating: __fd_chk: symbol not found
CANNOT LINK EXECUTABLE "appspawn": Error relocating: __fd_chk: symbol not found
...（几乎全 service 都报）
```

**根因**：rootfs 里的动态链接器 `ld-musl-arm.so.1` 用了**独立/错误版本**（如 prebuilts 下的独立 musl ld），与 OH sysroot 的 `libc.so` 不配套——独立版 ld 缺 `__fd_chk` 符号（musl 某些版本的 fd 安全检查符号），而 OH sysroot libc.so 里有引用。ld 与 libc 版本不匹配 → `__fd_chk` 找不到 → 所有链接 musl 的 service 都起不来。

**修复方案**：rootfs 的 `ld-musl-arm.so.1` 必须用 **OH sysroot 的 libc.so 拷贝**（ld 和 libc 是同一个 musl 构建，符号配套），不能用 prebuilts 独立版：
```bash
# 从 OH sysroot 拷 musl libc.so 作为 rootfs 的 ld-musl-arm.so.1
cp <oh_sysroot>/lib/libc.so  <rootfs>/lib/ld-musl-arm.so.1
# （OH musl 的 libc.so 同时承担 ld 角色，软链或拷贝均可，关键是同一构建产物）
```

**教训**：
- ① **全 service 集中报某个符号 not found（如 `__fd_chk`）→ 优先怀疑 rootfs 动态链接器/libc 用错版本**，不是单个 service 的问题。集中报错 = 公共依赖（ld/libc）错。
- ② **musl 的 ld 和 libc 必须配套（同一 sysroot 同一构建）**——ld-musl-arm.so.1 不能用 prebuilts 独立版凑，必须从 OH sysroot 拷 libc.so。`__fd_chk` / `__memset_chk` 等 chk 符号是 musl 版本敏感的。
- ③ **鉴别**：单个 service 报符号缺失 → 那个 service 缺 lib；几乎全 service 报同一符号缺失 → ld/libc 用错版本。

### 7.3 颗粒规格查不到时 — runtime 证据优先于缺 datasheet

**错误模式**：板载 SPI Nand / SPI Nor 颗粒无 datasheet（或 datasheet 查不到 page/OOB/容量），驱动适配时不知道填什么规格参数 → 容易猜地址/规格 → 烧上去 pagesize 错 / probe 失败。

**根因**：颗粒 datasheet 不公开 / 拿不到 / 型号对不上时，没法定规格参数。

**修复方案**：**以能跑的 bin 的 runtime print 为权威**，别猜：
1. 找一个在该颗粒上**能正常跑**的 u-boot / 内核 bin（厂商 SDK / 参考板 / 同颗粒别的板子）。
2. 烧上去启动，看 runtime 打印的颗粒规格（如 `Page:2KB OOB:128B` / `spi nand id: 0xe5 0xf1` / `pagesize 2048 oobsize 128`）。
3. 以 runtime print 的实际值为权威填进 ID 表 / 驱动参数。datasheet 查不到就别查了，runtime 实测 > datasheet（datasheet 也可能印错/版本不符）。

**教训**：
- ① **datasheet 查不到时，以能跑的 bin 的 runtime print 为权威**——别猜地址/规格，别用"应该是 2KB"这种推断。
- ② **runtime print 是颗粒规格的 ground truth**——`Page:2KB OOB:128B` 这种打印是驱动实测读寄存器/ID 出来的，比 datasheet 更可信。
- ③ **关联**：见 `references/diagnostic-cases.md` §8 案例BG003（DS35Q1GB ID 表）—— 颗粒 ID + 规格（2KB page/128B OOB）也是从 uboot 启动早期 `spi nand id: 0xe5 0xf1` print 抓的，不是猜的。配套 `skills/ohos-dev-soc-spec-parse/SKILL.md`「颗粒规格 runtime 证据优先」小节。

### 7.4 服务注册 OK 但不分发 — 任务分发配置错（注册成功≠功能可用）

**错误模式**：
```
某服务日志显示注册成功（RegisterServiceApi 返回 OK / SAMGR_AddRouter 成功）
但功能不工作：GetFeatureApi 重试 N 秒后超时返回 -2
或：服务的初始化函数（DEFAULT_Initialize 等）从未被调用
现象：注册链路全 OK，但下游永远拿不到 feature / 服务初始化不执行
```

**根因**：服务注册成功只是把"服务元信息"登记进 samgr，**真正执行服务初始化/分发请求需要任务（task）来消费消息队列**。如果该服务的 `GetTaskConfig` 配置成异步排队模式（如某些 samgr_lite 实现的 `SINGLE_TASK`：消息进队列但无消费者线程去 dispatch），则：
- 注册 OK（元信息登记成功）
- 但 `DEFAULT_Initialize` / `Receive` 等需要任务驱动的函数**永不执行**（队列里堆着消息没人取）
- 下游 `GetFeatureApi` 等不到 feature 发布 → 重试超时 → 返回 -2（超时错误码）

**通用判别**：
1. 注册链路全 OK（RegisterServiceApi/SAMGR_AddRouter 返回成功）但功能不工作 → **别只查注册链，查任务分发配置**
2. 服务的初始化函数从未被调用（加打印确认）→ 任务没被 dispatch
3. 查该服务的 `GetTaskConfig` / task 配置：是同步分发（立即执行）还是异步排队（需消费者线程）？异步模式如果没起消费者线程 → 队列堆消息无人取 → 初始化不执行

**修复方向**（通用）：
- 把该服务的任务分发配置从"异步排队无消费者"改成"同步分发"（注册时立即执行初始化/分发），或确保异步模式有消费者线程在跑
- 具体改法依框架实现而定（如某 samgr_lite 实现把 `taskFlags` 从 `SINGLE_TASK` 改成 `NO_TASK` 走同步分发）

**教训**：
- ① **注册 OK ≠ 功能可用**——注册只是登记元信息，功能可用需要任务分发驱动初始化和请求处理。注册链全通但功能不工作 → 查任务分发配置。
- ② **服务初始化函数从未被调用 → 优先查任务分发**（加打印确认初始化函数有没有被进入，没被进入 = 任务没 dispatch 到它）。
- ③ **异步队列模式必须有消费者**——`SINGLE_TASK` 类配置如果没起消费线程，队列里消息永远堆着不处理。
- ④ **关联**：配套真实案例见 `references/diagnostic-cases.md` §9（某 samgr_lite `NO_TASK` 同步分发案例——注册 OK 但 `DEFAULT_Initialize` 永不执行，改任务分发配置后功能通）。
