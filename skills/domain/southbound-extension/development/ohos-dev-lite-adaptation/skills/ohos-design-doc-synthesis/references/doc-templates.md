# 文档模板骨架 — ohos-design-doc-synthesis

> 本文件定义 ohos-design-doc-synthesis skill 三种 deliverable 的章节模板骨架。**模板用占位符 `${...}`，出稿时由 Step 3 填入项目实际数据（非占位符）**。占位符未填 = 文档未完成，标 WIP 不交付。术语遵循 ohos-design-ref-retrieval `references/terminology.md`。

---

## §1 芯片适配手册模板

> 交付物 ①：项目专属芯片适配手册。从 P1~P5 产出填实际数据。

```markdown
> **文档类型**: 芯片适配手册
> **文档版本**: ${VERSION}
> **适配版本**: OpenHarmony Lite ${OHOS_VERSION}
> **系统级别**: ${L0 轻量系统 (Mini System) / L1 小型系统 (Small System)}
> **芯片型号**: ${CHIP_NAME}
> **数据来源**: chip_spec.json (P1) / 内核 defconfig (P2) / 驱动清单+HCS (P3) / build 配置 (P4) / XTS+DECISIONS.md (P5)
> **生成 skill**: ohos-design-doc-synthesis ${VERSION}

## 1. 概述
### 1.1 芯片简介
${CHIP_NAME} 是 ${VENDOR} 的 ${CPU_ARCH} 芯片，${功能能力（WiFi/视频/通用）}。
<!-- 数据来源: chip_spec.json metadata -->

### 1.2 核心规格表
| 项目 | 规格 | 数据来源 |
|------|------|---------|
| CPU | ${cpu.coreType} | chip_spec.json |
| 主频 | ${cpu.freq} | chip_spec.json |
| RAM | ${RAM_SIZE} | chip_spec.json memoryMap |
| Flash | ${FLASH_SIZE} | chip_spec.json memoryMap |
| DDR 变体 | ${ddrVariant.variantSuffix} ${ddrVariant.ddrType} ${ddrVariant.ddrCapacity} | chip_spec.json ddrVariant |
| 系统级别 | ${L0/L1} | chip_spec.json |
| 内核 | ${LiteOS-M/LiteOS-A/Linux(L1-Linux)} | — |

### 1.3 适配范围
${适配范围：哪些外设/功能纳入本次适配}

## 2. 环境搭建
### 2.1 工具链
${工具链版本 + 安装命令}
<!-- 数据来源: build 配置 P4 -->

### 2.2 源码同步
${源码同步命令}

### 2.3 编译验证
${编译命令 + 期望产物}

## 3. 内核移植
### 3.1 Kconfig 适配链
${关键 Kconfig 项 + 取值}
<!-- 数据来源: 内核 defconfig P2 -->

### 3.2 启动配置
${启动参数 + 关键宏（如 BINDER_IPC_32BIT=1）}
<!-- 数据来源: 内核 defconfig P2 -->

### 3.3 C 库适配
${musl/newlib 适配 + ld-musl-arm.so.1 来源（OH sysroot libc.so）}

## 4. 驱动开发
<!-- L0: IoT 外设驱动子系统；L1: 精简版 HDF + HCS -->
### 4.1 驱动框架
${L0 IoT 外设驱动子系统 / L1 精简版 HDF + HCS 说明}

### 4.2 外设支持矩阵
| 外设 | 驱动状态 | 验证状态 | 备注 |
|------|---------|:------:|------|
| GPIO | ${已适配/未适配} | ${✅/⚠️/❌} | ${备注} |
| UART | ... | ... | ... |
| I2C | ... | ... | ... |
<!-- 数据来源: 驱动清单 P3 + XTS P5 -->

### 4.3 HCS 配置（仅 L1）
${HCS 配置示例 + match_attr 配对}

## 5. 编译构建
### 5.1 config.gni / BUILD.gn
${关键配置项}
<!-- 数据来源: build 配置 P4 -->

### 5.2 链接脚本
${内存布局：Flash/RAM 地址范围}
<!-- 数据来源: linker.ld P4 -->

### 5.3 config.json
${产品配置}

## 6. 烧录运行
### 6.1 烧录工具配置
${烧录工具 + 命令 + 分区表}
<!-- 数据来源: build 配置 P4 -->

### 6.2 串口输出
${期望启动日志关键阶段}

### 6.3 功能验证
${功能验证清单 + 结果}

## 7. 验证状态
### 7.1 功能模块验证矩阵
| 模块 | XTS 结果 | 实测状态 | 备注 |
|------|---------|:------:|------|
| ${模块} | ${通过/失败/未测} | ${✅/⚠️/❌} | ${备注} |
<!-- 数据来源: XTS P5 -->

### 7.2 XTS 测试结果
${XTS 通过率 + 失败项}

## 8. 已知问题
### 8.1 适配踩坑
${坑 + 解决方案}
<!-- 数据来源: DECISIONS.md P5 -->

### 8.2 决策记录
${关键决策（A1~A6）+ 理由}
<!-- 数据来源: DECISIONS.md P5 -->

## 9. 参考资料
- 官方文档: ${链接}
- 芯片 Datasheet: ${来源}
- 社区资源: ${链接}
- 关联 skill 产出: chip_spec.json / 内核 defconfig / 驱动清单 / build 配置 / XTS 报告 / DECISIONS.md
```

---

## §2 API 参考文档模板

> 交付物 ②：项目专属 API 参考文档。从驱动清单 + HCS 填实际接口。

```markdown
> **文档类型**: API 参考文档
> **文档版本**: ${VERSION}
> **适配版本**: OpenHarmony Lite ${OHOS_VERSION}
> **系统级别**: ${L0 轻量系统 (Mini System) / L1 小型系统 (Small System)}
> **芯片型号**: ${CHIP_NAME}
> **数据来源**: 驱动清单+HCS (P3) / chip_spec.json (P1)
> **生成 skill**: ohos-design-doc-synthesis ${VERSION}

## 1. API 概览
### 1.1 外设 API 列表
| 外设 | 头文件 | API 数 | 验证状态 |
|------|--------|:-----:|:------:|
| GPIO | ${iot_gpio.h / hdf_gpio.h} | ${N} | ${✅/⚠️/❌} |
| UART | ... | ... | ... |
<!-- 数据来源: 驱动清单 P3 -->

### 1.2 驱动框架
${L0: IoT 外设驱动子系统（操作函数表 GpioOperations 等）；L1: 精简版 HDF（HdfDriverEntry + HCS 绑定）}

## 2. 各外设 API
<!-- 每个外设一节，从驱动实现 + HCS 填实际接口 -->

### 2.1 GPIO
#### 2.1.1 GpioInit
```c
${函数签名}
```
- **参数**: ${参数说明}
- **返回值**: ${返回码 + 含义}
- **示例**: ${代码示例}
- **注意事项**: ${ISR 安全/线程安全/硬件依赖}
<!-- 数据来源: 驱动实现 P3 -->

#### 2.1.2 GpioSetDir
...（同上格式）

### 2.2 UART
...（同 GPIO 格式）

## 3. HAL 接口
<!-- L0: 操作函数表；L1: HDF Method -->
### 3.1 操作函数表（L0）
| 接口 | 实现函数 | 说明 |
|------|---------|------|
| ${GpioMethod.xxx} | ${实现函数名} | ${说明} |
<!-- 数据来源: 驱动清单 P3 -->

### 3.2 HDF Method（L1）
| Method | 实现函数 | HCS match_attr |
|--------|---------|---------------|
| ${Method 名} | ${实现函数名} | ${HCS 配对} |

## 4. 错误码
| 错误码 | 含义 | 排查 |
|--------|------|------|
| ${码} | ${含义} | ${排查方向} |
<!-- 数据来源: 驱动实现 P3 -->

## 5. 兼容性
### 5.1 L0/L1 跨系统差异
${同一外设在 L0（IoT 外设 API）vs L1（HDF API）的差异}
<!-- 数据来源: chip_spec.json 系统级别 + 驱动清单 -->

### 5.2 CMSIS / OSAL
${L0 CMSIS 合规 / L1 OSAL 接口使用说明}
```

---

## §3 移植指南模板

> 交付物 ③：项目专属移植指南。从 P1~P5 产出填实际流程。L0/L1 共用章节框架，差异在内核/驱动框架。

```markdown
> **文档类型**: 移植指南
> **文档版本**: ${VERSION}
> **适配版本**: OpenHarmony Lite ${OHOS_VERSION}
> **系统级别**: ${L0 轻量系统 (Mini System) / L1 小型系统 (Small System)}
> **芯片型号**: ${CHIP_NAME}
> **数据来源**: chip_spec.json (P1) / 内核 defconfig (P2) / 驱动清单+HCS (P3) / build 配置 (P4) / XTS+DECISIONS.md (P5)
> **生成 skill**: ohos-design-doc-synthesis ${VERSION}

## 1. 移植前置
### 1.1 芯片选型评估
${CHIP_NAME} 适配 ${OH_VERSION} 可行性评估。
<!-- 数据来源: chip_spec.json P1 -->

### 1.2 系统级别判定
${L0/L1 判定依据：有 MMU → L1；无 MMU → L0。本芯片 = ${L0/L1}}
<!-- 数据来源: chip_spec.json cpu.mmu -->

### 1.3 功能能力判定
${WiFi/视频/通用 + DDR 变体（如适用）}
<!-- 数据来源: chip_spec.json + ddr-variant-guide -->

## 2. 内核移植步骤
### 2.1 Kconfig 适配
${步骤 + 关键 Kconfig 项}
<!-- 数据来源: 内核 defconfig P2 -->

### 2.2 启动代码
${启动代码适配 + 关键宏（如 BINDER_IPC_32BIT=1，见 ohos-issue-lite-diagnose 案例OH001）}

### 2.3 C 库适配
${musl ld = OH sysroot libc.so 拷贝（见 ohos-issue-lite-diagnose fault-knowledge-base §7.2）}

## 3. 驱动移植步骤
### 3.1 L0 IoT 外设驱动子系统移植
<!-- 仅 L0 -->
${操作函数表注册流程 + 各外设 HAL 实现}

### 3.2 L1 精简版 HDF + HCS 移植
<!-- 仅 L1 -->
${HdfDriverEntry + HCS 绑定流程 + match_attr 配对}

### 3.3 外设移植清单
| 外设 | 移植步骤 | 验证状态 |
|------|---------|:------:|
| ${外设} | ${步骤摘要} | ${✅/⚠️/❌} |
<!-- 数据来源: 驱动清单 P3 + XTS P5 -->

## 4. 构建配置步骤
### 4.1 config.gni / BUILD.gn
${配置流程 + 关键项}
<!-- 数据来源: build 配置 P4 -->

### 4.2 链接脚本
${内存布局配置流程}
<!-- 数据来源: linker.ld P4 -->

### 4.3 config.json
${产品配置流程}

## 5. 烧录验证步骤
### 5.1 烧录
${烧录工具 + 分区表 + 命令}
<!-- 数据来源: build 配置 P4 -->

### 5.2 串口验证
${期望启动日志 + 关键阶段 checkpoint}
<!-- 卡某阶段 → 走 ohos-issue-lite-diagnose add-debug-prints 标准步骤 -->

### 5.3 XTS 验证
${XTS 运行 + 结果判读}
<!-- 数据来源: XTS P5 -->

## 6. 常见问题
### 6.1 移植踩坑
| 现象 | 根因 | 解决 | 关联 |
|------|------|------|------|
| ${现象} | ${根因} | ${解决} | ${ohos-issue-lite-diagnose 案例编号} |
<!-- 数据来源: DECISIONS.md P5 + ohos-issue-lite-diagnose 案例 -->
<!-- 例: binder ioctl -22 → BINDER_IPC_32BIT → 案例OH001 -->

### 6.2 决策记录
${关键决策（A1~A6）+ 理由 + 替代方案}
<!-- 数据来源: DECISIONS.md P5 -->

## 7. 参考案例
### 7.1 同系芯片适配案例
${同系芯片（如 hispark_taurus_cv610）适配案例引用}
<!-- 数据来源: ohos-design-ref-retrieval 检索 adaptation-cases/ -->

### 7.2 官方移植指南
${官方移植指南链接（L0 13 篇 / L1 7 篇）}
<!-- 数据来源: ohos-design-ref-retrieval 检索 porting-guides/ -->
```

---

## 填充逻辑速查

> 模板占位符 → 从哪个上游产出取哪个字段。

| 模板占位符 | 上游产出 | 字段/位置 |
|-----------|---------|----------|
| `${CHIP_NAME}` / `${VENDOR}` / `${CPU_ARCH}` | chip_spec.json (P1) | metadata.chipName / vendor / architecture |
| `${RAM_SIZE}` / `${FLASH_SIZE}` | chip_spec.json (P1) | memoryMap[] |
| `${ddrVariant.*}` | chip_spec.json (P1) | ddrVariant |
| `${L0/L1}` | chip_spec.json (P1) | metadata.targetSystemLevel |
| 内核 Kconfig 项 / 关键宏 | 内核 defconfig (P2) | defconfig 实际取值 |
| 外设 API 列表 / 操作函数表 | 驱动清单 + HCS (P3) | driver list / HCS |
| config.gni / linker.ld / config.json | build 配置 (P4) | 实际配置文件 |
| 功能验证状态 ✅/⚠️/❌ | XTS + DECISIONS.md (P5) | XTS 结果 + DECISIONS 决策 |
| 已知问题 / 踩坑 | DECISIONS.md (P5) | 决策记录 + ohos-issue-lite-diagnose 案例引用 |
| 参考案例 / 官方指南 | ohos-design-ref-retrieval 检索 | adaptation-cases/ / porting-guides/ |

> **规则**：占位符在 docDataPool 里有值 → 填实际值 + 标数据来源；无值 → 标 WIP + 列「待 P? 产出后填」，**不编造**。
