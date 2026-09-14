# ohos-ci-lite-deploy-burn evals

4 个评估用例，判据全部来自 iter07（Hi3516CV610 L1 烧录实战）/ iter12（Hi3861 L0 端到端实战）沉淀进 SKILL.md 的真实数据，非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `remote_build_artifact_download_flow` | 远程编译产物下载流程（Phase 1→2） | SSH 模式阶段串联 + config 变量映射 + Local 模式裁剪 | iter12 编译链路（wifiiot_hispark_pegasus 产物路径）+ SKILL.md Phase 1/2 |
| `l1_burn_package_and_medium_mismatch` | L1 烧录包（boot_image+env+uImage+rootfs+xml 分区表）+ 介质错配诊断 | L0/L1 烧录路由 + iter07 介质错配实战回溯 | 实测案例：`no find spi` + `Invalid spi flash block size` |
| `test_run_log_capture_and_passfail_stats` | 测试运行 + 日志抓取（AT 静默降级 + PASS/FAIL 统计） | burn_one.py WAKE_MAGIC 唤醒/降级链 + XTS 结束标志 + 握手码定性 | SKILL.md「自动上板跑 test」能力 1-4 + iter12 |
| `map_analysis_artifacts` | MAP 分析产物（analyze/compare） | map_analyzer.py 双模式用法 + .map 来源 | tools/map_analyzer.py（skill 自带资产，ohos-test-lite-adapt-verify 调用） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：
- L0/L1 烧录机制区分（基线常拿 HiBurn 流程答 L1 问题）
- 介质错配根因判定（基线倾向查串口/线缆，想不到 getinfo 确认介质）
- WAKE_MAGIC/降级链（基线不知道 HiBurn 烧后 AT 静默的机制，只会让用户重新上电试）
- 0xC35A69A6 定性（基线倾向当校验失败，换文件重烧）
- map_analyzer 工具存在性（基线不知道 skill 自带工具，倾向手写脚本解析 map）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **L0/L1 路由正确率**：with skill 先判级别再选工具/包格式；基线混用两套机制
2. **实战症状命中率**：介质错配 / 0xC35A69A6 / pagesize 8192 等 iter07/12 症状，with skill 直接按症状表定位；基线逐个盲试
3. **工具复用率**：with skill 用自带 burn_one.py / map_analyzer.py / 设备 profile；基线倾向现写脚本或让用户手动 GUI 操作
4. **终点纪律**：with skill 推进到板上 test PASS 才停；基线常停在"编译过/能烧"的中间态
