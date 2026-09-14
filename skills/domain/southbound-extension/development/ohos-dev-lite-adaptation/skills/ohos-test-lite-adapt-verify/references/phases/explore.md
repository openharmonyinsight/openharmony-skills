# 阶段 1 · explore — 探索（量基线）

**前置**：已完成 init（连接配置可用、设备 profile 已选定、`xts_test/` 目录已建）。

**约定路径**：

- ohos-ci-lite-deploy-burn：`skills/ohos-ci-lite-deploy-burn/`
- 设备 profile：`ohos-ci-lite-deploy-burn/references/devices/<chip>.json`
- 产物：`xts_test/reports/baseline_map.md`、`xts_test/reports/arch.md`
- 硬件上限：从设备 profile 的 `hardware.ram_size` / `hardware.flash_size` 读取

## 执行步骤

### 1. 量基线 RAM/ROM

1. 读取 `ohos-ci-lite-deploy-burn/config.json` 取连接参数和路径
2. 读取设备 profile 确认硬件上限（RAM / Flash）
3. 触发全量编译（firmware 模式）：
   - 调用 `ohos-ci-lite-deploy-burn` Phase 1（编译）
   - build_mode 由设备 profile 的 `build_modes.firmware` 决定
4. 下载编译产物（含 .map 文件）：
   - 调用 `ohos-ci-lite-deploy-burn` Phase 2（下载）
5. 分析 MAP 文件：
   ```bash
   python skills/ohos-ci-lite-deploy-burn/tools/map_analyzer.py analyze \
     <下载到的.map文件路径>
   ```
6. 把基线数字写入 `xts_test/reports/baseline_map.md`：
   - RAM：已用 / 上限 / 占比 %
   - Flash (ROM)：已用 / 上限 / 占比 %
   - Top N 最大段 / 最大符号
   - 编译时间、固件大小等辅助信息

> 此文件是后续 MAP 对比的"黄金基线"。**不可覆盖**，除非用户明确要求重新量测。

### 2. 探架构

1. 通过配置的连接方式访问代码仓（SSH / Local / Custom），读取用户指定的模块代码
2. 梳理以下内容并记录：
   - **对外接口**：模块暴露的 API / 头文件 / 服务接口
   - **关键调用路径**：数据流 / 控制流的主要路径
   - **内存占用大户**：大表 / 大 buffer / 重复代码 / 未裁剪特性
   - **依赖关系**：与其他模块的耦合点
3. 产出架构图（mermaid 优先，次选文字层级图）写入 `xts_test/reports/arch.md`：
   - 标注模块边界和接口
   - 标注疑似可优化点及对应代码位置
   - 标注内存占用热点

**探索范围由用户指定**。若用户未指定，默认探索全量固件的高层架构。

### 3. 识别优化/验证点（初稿）

基于基线数字 + 架构图，输出优化/验证初稿：

常见方向（不限于此）：
- 裁剪未用特性 / 死代码消除
- 压缩只读数据表（常量合并、字符串去重）
- Buffer 复用 / 内存池优化
- 日志级别裁剪
- 未使用符号清理
- 编译器优化选项调优（-Os vs -O2 vs -Oz）

将初稿存入 `xts_test/reports/explore_draft.md`。

> 若有 openspec 可用，可调用其 explore 能力增强分析深度。但 **openspec 不是必须的**，
> 手动分析同样有效。

### 4. 阶段收尾

确认清单：
- [ ] `xts_test/reports/baseline_map.md` 含完整基线 RAM/ROM 数字（含硬件上限）
- [ ] `xts_test/reports/arch.md` 含架构图与疑似优化/验证点
- [ ] `xts_test/reports/explore_draft.md` 含优化/验证初稿

回显基线数据摘要，提示用户下一阶段（analyze，见 `references/phases/analyze.md`）。
