Skill 1: ohos-test-arkts-xts-generation

  优化点 1.1：Phase 0-11 流程过重，冷启动成本高

  12-Phase完整流程在简单场景下（如"给这2个API补充测试"）显得过重。用户需经历配置加载→覆盖率扫描→API解析→设计→生成→注册→验证→编译→执行→覆盖率对比→输出，即使仅需生成2个测试用例。

  建议：
  - 增加 Quick Mode：当目标API ≤ 5 个时，合并 Phase 2-4（扫描+解析+设计→一步完成），跳过 Phase 9/10（设备执行+覆盖率对比），直接输出结果
  - 在 SKILL.md 入口判定中增加 Quick Mode 分支

  优化点 1.2：模块懒加载规则分散，执行时上下文膨胀

  "仅加载当前阶段需要的模块"原则正确，但加载规则分散在每个Phase的prompt文件中。Agent需先读取prompt文件才能知道加载什么，而prompt文件本身也可能很长。

  建议：
  - 在 SKILL.md 或独立文件 modules/LOAD_MAP.md 中提供 Phase→Module 映射总表，Agent一次性读取即可知道每个Phase该加载什么，无需逐个打开prompt文件查找

  优化点 1.3：knowledge_root 降级路径映射复杂

  外部知识库 → 内部降级路径的映射关系（09_methodology/01~07 → L1_Analysis/）在 system.md 中硬编码，且降级模式下子系统特定知识不可用，但这个限制没有在 Phase 流程中体现为具体的行为差异。

  建议：
  - 降级模式下，在 Phase 1 输出中明确标注 MODE: degraded，后续Phase遇到子系统特定决策时主动提醒用户"降级模式下使用通用规则，结果可能不够精确"
  - 将路径映射关系提取到配置文件中，而非硬编码在 system.md

  优化点 1.4：Anti-Patterns 数量过多（16条），优先级不明

  16条 NEVER 规则覆盖了从"不使用未声明接口"到"不延迟创建session_issues日志"等不同严重级别，但缺乏优先级区分。Agent执行时难以判断哪些是硬性阻断、哪些是建议性约束。

  建议：
  - 分为 P0-Block（违反则不可继续，如使用未声明接口）、P1-Warning（违反会降低质量，如延迟记录issue）、P2-Advisory（最佳实践）
  - 在每条NEVER前标注级别
  
  Skill 2: ohos-test-capi-xts-generation

  优化点 2.1：缺少覆盖率扫描能力，默认Flow C过于粗暴

  CAPI 无 APICoverageDetector，默认走 Flow C（全部按新增接口处理）。这意味着无法识别已有测试覆盖了哪些API，可能生成重复测试。

  建议：
  - 增加 轻量级覆盖率检测：通过 grep -r 扫描已有 .test.ets 中的 SUB_* 编号和API调用，构建简易覆盖映射，至少避免生成完全重复的用例
  - 或复用 ArkTS XTS 的 extract_uncovered.py 脚本（需适配 .h 解析）

  优化点 2.2：N-API 三重校验仅靠Shell脚本，跨平台兼容性差

  verify_napi_triple.sh、auto_fix_napi_triple.sh、check_test_suite_structure.sh 都是Bash脚本，在Windows原生环境下无法直接运行（需WSL）。

  建议：
  - 将核心校验逻辑用 Python 重写（参考 ArkTS XTS 的 validate_test_context.py 和 phase_tracker.py），Shell脚本作为可选入口
  - 或在 SKILL.md 中明确标注 Windows 环境下的替代方案

  优化点 2.3：Thinking Framework 位置不当

  "Before You Generate" Thinking Framework（C API特性分析、N-API封装决策树、用例数量估算）内容非常有价值，但放在 SKILL.md 中仅作为参考。Agent在Phase 5生成时可能不会重新加载SKILL.md。

  建议：
  - 将 Thinking Framework 提取到 modules/L2_Generation/generator/napi_decision_framework.md，在 Phase 5 prompt 中标记为 MANDATORY 加载

  优化点 2.4：模板工程路径硬编码

  template_project/capi_test_template/ 路径在多处硬编码引用，且 SKILL.md 中"NEVER 创建新工程时不从模板复制"规则依赖此路径存在。

  建议：
  - 模板路径放入配置文件，启动时验证路径有效性
  - 增加模板完整性校验（检查 CMakeLists.txt、module.json5、Test.json 等关键文件是否存在）