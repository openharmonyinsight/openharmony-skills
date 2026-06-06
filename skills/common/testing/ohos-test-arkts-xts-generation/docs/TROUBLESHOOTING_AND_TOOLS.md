# 故障排除与覆盖率工具

> 常见问题解答 + APICoverageDetector 工具详解

## 目录

- [一、常见问题](#一常见问题)
- [二、APICoverageDetector 工具详解](#二apicoveragedetector-工具详解)

---

## 一、常见问题

### Q1: 生成的测试用例无法编译

**可能原因**：hypium 导入不正确 / ArkTS 语法类型不匹配 / 测试文件路径错误 / @tc 注释块格式错误

**解决方案**：

1. 检查 hypium 导入：
   ```typescript
   import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
   ```

2. 检查 ArkTS 语法类型匹配：读取 `build-profile.json5` 中 `arkTSVersion` 字段，确保工程类型与 API 类型兼容

3. 检查测试文件路径：
   - ArkTS 动态测试套（arkts-dyn）：`entry/src/ohosTest/ets/test/`
   - ArkTS 静态测试套（arkts-sta）：`entry/src/main/src/test/`

4. 检查 @tc 注释块格式：
   ```typescript
   /**
    * @tc.name onClickNormal001
    * @tc.number SUB_ARKUI_COMPONENT_ONCLICK_PARAM_001
    * @tc.desc 测试 Component 的 onClick 方法 - 正常点击场景.
    * @tc.type FUNCTION
    * @tc.size MEDIUMTEST
    * @tc.level LEVEL3
    */
   ```

5. 查看编译错误日志：参考 `modules/L3_Validation/builder/build_troubleshooting.md`

---

### Q2: 测试用例命名不符合规范

**解决方案**：

1. 使用小驼峰命名（camelCase）：`onClickNormal001` ✅ / `ON_CLICK_NORMAL_001` ❌
2. 确保 @tc.name 与 it() 第一个参数完全一致
3. 参考命名规范：`references/subsystems/_common.md`

---

### Q3: 测试设计文档与测试用例不一致

**解决方案**：重新生成测试用例和设计文档确保同步；检查设计文档版本号是否递增；参考 `modules/L2_Generation/generator/design_doc_generator.md`

---

### Q4: Linux 环境编译失败

**可能原因**：使用了 `hvigorw` 命令（不适用于 Linux） / 编译环境未正确配置 / BUILD.gn 编译目标识别错误

**解决方案**：

1. 必须使用 `build.sh` 脚本编译：`./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=test_name`
2. 参考环境准备：`modules/L3_Validation/builder/build_workflow_linux.md`
3. 预编译清理：`rm -rf build && rm -rf out`
4. 查看编译错误日志：`modules/L3_Validation/builder/build_troubleshooting.md`

---

### Q5: 测试用例执行失败

**解决方案**：检查测试逻辑 / 前置条件（权限、网络、设备状态） / 测试数据 / 依赖资源是否准备好

---

### Q6: 子系统配置文件未找到

**解决方案**：

1. 确保配置文件路径正确：`references/subsystems/{子系统名称}/_common.md`（区分大小写）
2. 如不存在，使用通用配置：`references/subsystems/_common.md`

---

### Q7: 测试覆盖率分析不准确

**解决方案**：确保测试文件扫描完整（指定正确测试路径） / 检查 API 定义解析（读取正确的 .d.ts 文件） / 确保测试用例编号格式规范：`SUB_[子系统]_[模块]_[API]_[类型]_[序号]`

---

### Q8: ArkTS 静态语法校验问题

**解决方案**：

1. 确认项目配置了 `arkTSVersion: 1.2`
2. 调用 `arkts-static-spec` 技能进行语法规范校验（Phase 7 步骤 A 自动触发）
3. 严格遵循该技能的规范，不添加文档之外的假设

---

### Q9: 如何调用 arkts-static-spec 技能

在 Phase 7 步骤 A 中自动触发（仅 ArkTS-Sta 项目）。也可手动调用：

```
请使用 arkts-static-spec 进行语法规范校验：
- 语法规则检查
- 类型系统验证
- 编译问题分析
```

**注意**：不要在本技能中重复实现静态语法检查功能。

---

### Q10: 为什么格式化和验证步骤经常被漏掉？

**根因**：

1. 长流程中 Phase 7 不够突出，缺乏强制性标记
2. 用户误以为"编译验证"会自动发现所有问题
3. 缺乏自动化检查点（Phase Tracker 已解决）

**解决方案**（已实施）：

- Phase 7 标记为**不可跳过**（`phase_tracker.py` 强制检查）
- SKILL.md Anti-Patterns 中明确"NEVER 跳过 Phase 7"
- Phase 7 分两步：步骤 A（`validate_test_context.py` 自动检查 5/9 项）+ 步骤 B（`check-test-code-quality` 11 条规则）

**正确流程**：生成测试用例 → 注册测试套 → **Phase 7 格式验证（不可跳过）** → 编译验证

| 对比项 | Phase 7 格式验证 | Phase 8 编译验证 |
|--------|----------------|----------------|
| 检查内容 | 语法规范、命名规范、@tc 注解、断言方法、资源释放 | 编译环境、编译目标、依赖关系 |
| 可跳过 | ❌ | ❌ |
| 依赖关系 | Phase 8 的前置条件 | Phase 7 的后置步骤 |

---

## 二、APICoverageDetector 工具详解

### 概述

APICoverageDetector 是 OpenHarmony 官方的 API 覆盖率扫描工具，本技能通过异步封装（`scripts/async_coverage_scan.py`）集成于 Phase 2（初始扫描）和 Phase 10（覆盖率验证）。

### 平台支持

| 环境 | 是否可用 | 路径示例 | 说明 |
|------|---------|---------|------|
| Windows 原生 | 可用 | `D:\APICoverageDetector` | 直接运行 |
| WSL | 可用 | `/mnt/d/APICoverageDetector` | 通过 WSL 路径映射调用 .exe |
| Linux 计算云/远程服务器 | **不可用** | — | 只能提供已有扫描结果或跳过 |

### 路径配置

从 `.oh-xts-config.json` 的 `scan_tool_root` 字段读取。路径不存在时向用户提供选项：
1. 更新 APICoverageDetector 路径
2. 提供已有的覆盖率扫描结果（CSV/XLSX 文件）
3. 跳过覆盖率扫描

**路径建议**：推荐放在磁盘根目录（如 `D:\APICoverageDetector`），避免 Windows 260 字符路径限制导致扫描失败（XTS 测试工程目录层级通常很深）。

### 主要组件

- `APICoverageDetector_ArkTS.bat`: ArkTS 覆盖率扫描脚本
- `APICoverageDetector_C.bat`: C/C++ 覆盖率扫描脚本
- `arkts_entrance/`: ArkTS 静态检查工具包

### 输出位置

- 扫描结果：`{scan_tool_root}/results/`
- 覆盖率数据：`{skill_root}/.coverage_data/`
- 未覆盖 API 列表：`{skill_root}/.coverage_data/uncovered_apis.json`

### 异步扫描工具

基本命令：

```bash
# 启动异步扫描
python scripts/async_coverage_scan.py start

# 查看扫描状态
python scripts/async_coverage_scan.py status

# 获取扫描结果
python scripts/async_coverage_scan.py results

# 停止扫描
python scripts/async_coverage_scan.py stop
```

### 扫描阶段（10 步）

1. `(1/10) count工具` — 统计工具
2. `(2/10) metrics工具` — 指标工具
3. `(3/10) 检查metrics工具结果` — 检查结果
4. `(4/10) 扫描覆盖率` — 扫描覆盖率
5. `(5/10) 汇总覆盖率信息` — 汇总信息
6. `(6/10) 统计覆盖度` — 统计覆盖度
7. `(7/10) 检查参数规格` — 检查参数
8. `(8/10) 检查错误码` — 检查错误码
9. `(9/10) 检查返回值` — 检查返回值
10. `(10/10) 格式化输出` — 格式化输出

### 状态说明

| 状态 | 描述 | 处理方式 |
|------|------|----------|
| `idle` | 空闲状态 | 可以启动新扫描 |
| `running` | 扫描中 | 可以监控进度 |
| `completed` | 扫描完成 | 可以获取结果 |
| `failed` | 扫描失败 | 检查错误信息 |

### 结果文件

```
APICoverageDetector/results/
├── open_source/sdk_result.xlsx
├── dynamic/sdk_result.xlsx
└── static/sdk_result.xlsx
```

### 故障排除

| 问题 | 解决方法 |
|------|---------|
| 扫描启动失败 | 检查配置文件路径、测试用例路径、可执行文件是否存在 |
| 进度更新异常 | 检查日志文件权限和是否存在 |
| 扫描长时间无响应 | 检查进程状态、查看日志文件、必要时手动停止 |

调试命令：

```bash
python scripts/async_coverage_scan.py status    # 查看状态
python scripts/async_coverage_scan.py results   # 查看结果
tail -f APICoverageDetector/log/arkts_runner.log  # 检查日志
```

---

### 获取帮助

- [Prompt 模板与使用场景](./USAGE_AND_WORKFLOW.md)
- [安装与配置](./SETUP_AND_CONFIG.md)
- 编译相关问题：`modules/L3_Validation/`
- 测试生成相关问题：`modules/L2_Generation/`
- 分析相关问题：`modules/L1_Analysis/`
- 通用配置：`references/subsystems/_common.md`
