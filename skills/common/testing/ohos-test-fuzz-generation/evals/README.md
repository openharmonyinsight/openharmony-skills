# ohos-test-fuzz-generation 测试用例说明

## 概述

本测试套件包含 **81个测试用例**，234条断言，覆盖 fuzz 测试生成技能的触发检测、核心场景、工作流、边界情况、文档使用和禁止做法。真实 OpenHarmony 代码覆盖 graphic_2d、surface、3D、WM、effect/compositor 五个仓。配置文件覆盖 BUILD.gn、project.xml、fuzzer header 三种格式。

## 评测结果 (81-case Benchmark)

| Configuration | Pass Rate | Assertions | Details |
|---------------|:---------:|:----------:|---------|
| **with_skill** | **100%** | 234/234 | All 234 assertions passed (iteration 5, live evaluation) |
| **without_skill** | **27.8%** | 65/234 | 169 failed — systematic domain errors |
| **Delta** | **+72.2%** | — | Exceeds ≥30-50% target |

### Per-Category Results

| Category | Evals | With-Skill | Without-Skill | Delta |
|----------|:-----:|:----------:|:------------:|:-----:|
| trigger | 15 | 100% | 40% | +60% |
| core_scenario | 42 | 100% | 31.6% | +68.4% |
| workflow | 4 | 100% | 12.5% | +87.5% |
| edge_case | 7 | 100% | 31.8% | +68.2% |
| documentation | 3 | 100% | 12.5% | +87.5% |
| forbidden | 10 | 100% | 0% | +100% |

### Skill-judge 分数

118/120 (98.3%, Grade A)

### Fixture Coverage

| Type | Total | Real OHOS | Synthetic | Real Ratio |
|------|:-----:|:---------:|:---------:|:----------:|
| Headers | 14 | 7 | 7 | 50% |
| Fuzzers | 21 | 6 | 15 | 28.6% |
| Configs | 6 | 0 | 6 | — |
| **Total** | **41** | **13** | **28** | **31.7%** |

Real OHOS domains: graphic_2d (rs_interfaces, rsanimationcommand, rsmemorymanager), surface (ibuffer_producer, nativewindow), 3D (i_engine), WM (idisplay_manager_agent, windowstubget), effect (shader_effect, ge_kawase_blur)

## 测试分类

### 1. 技能触发测试 (15个, IDs 1-15)
- 应触发 (9个): fuzz/fuzzer/fuzz_test/LLVMFuzzerTestOneInput/*_fuzzer.cpp/fuzztest/种子/报告
- 不触发 (6个): 单元测试/集成测试/bug修复/性能测试/通用review/API设计

### 2. 核心场景测试 (42个, IDs 16-28, 51-60, 61-64, 65-69, 70-74, 75-76, 77-81)
- 合成生成 (5): simple/ipc/complex/enum/no_param
- 合成检查 (8): good/rand/data_ptr/size/uninit/auto/ipc_proxy/enum_uint32
- 真实OHOS生成 (8): IPC stub/HDI screen/sptr complex/no param/callback/check/baseline
- 真实OHOS检查 (5): animation command/kawase blur/nativewindow/windowstub/memory manager
- 配置格式检查 (6): project_xml bad/good + fuzzer_header bad/good + BUILD_gn bad/good
- 新规则检查 (5): fixed_params(014)/unused_mutation(003)/data_reuse(004)/intermediate(015)/driver_bug(009)
- 真实OHOS新域生成 (5): surface IPC/3D engine/WM display/effect shader/composer callback
- good fuzzer检查 (2): ipc stub/singleton

### 3. 工作流测试 (4个, IDs 29-32)

### 4. 边界情况测试 (7个, IDs 33-39)

### 5. 文档使用测试 (3个, IDs 40-42)

### 6. 禁止做法测试 (10个, IDs 43-50, 57-58)

## 测试文件

### headers/ (14 files)
- Synthetic (7): simple_class.h / ipc_class.h / complex_param_class.h / all_output_params_class.h / enum_class.h / no_param_class.h / many_methods_class.h
- Real OHOS (7): 2d/(2 files) + 3d/(1) + composer/(1) + effect/(1) + surface/(1) + wm/(1)

### fuzzers/ (21 files)
- Good (3): good_fuzzer / good_fuzzer_ipc_stub / good_fuzzer_singleton
- Bad synthetic (12): data_extraction/(6 files) + bad_fuzzer_auto / bad_fuzzer_driver_bug / bad_fuzzer_enum_uint32 / bad_fuzzer_intermediate / bad_fuzzer_ipc_proxy / bad_fuzzer_uninit_global
- Real OHOS (6): 2d/(3 files) + effect/(1) + surface/(1) + wm/(1)

### configs/ (6 files)
- build_gn/ (2): build_gn_good.gn / build_gn_bad.gn
- project_xml/ (2): project_xml_good.xml / project_xml_bad.xml
- fuzzer_header/ (2): fuzzer_header_good.h / fuzzer_header_bad.h



## 文件说明

- **evals.json** — 81个测试定义（纯定义，不含结果），version 3.0
- **README.md** — 测试套件说明和评测结果汇总
- **files/** — 测试 fixture 文件（headers/fuzzers/configs）
- **agent-skill-eval-2026-06-15/** — 历史迭代 benchmark（iteration 1-5），iteration 5 为最终结果

## 版本历史

- v1.0 (2026-06-14): 50合成测试
- v1.1 (2026-06-14): +8真实OHOS, 8-case基线
- v1.2 (2026-06-15): +2 BUILD.gn, 60-case基线, delta +71.5%
- v2.0 (2026-06-15): +21 evals(IDs 61-81), +5真实fuzzer, +5真实header(surface/3D/WM/effect/composer), +4 config fixture(project.xml/fuzzer .h), +5 bad fuzzer(003/004/009/014/015), 81-case全量评测, with_skill 100%(234/234), without_skill 32.5%(76/234), delta +67.5%
- v3.0 (2026-06-15): Iteration 5 live evaluation, 12 fixes applied (IPC stub detection, self-check enforcement, COMPLEX_TYPE_MAP aggregate init, ENUM_SIZE_MAP expansion, fixture fix), with_skill 100%(234/234), without_skill 27.8%(65/234), delta +72.2%
