# Test

测试领域相关技能，按研发阶段组织为设计、测试执行、问题分析三个方向。

## 阶段导航

| 阶段 | 目录 | 说明 |
|------|------|------|
| 设计 | [design/](design/) | 测试用例设计、测试策略制定、测试设计文档生成 |
| 测试执行 | [testing/](testing/) | XTS 测试用例生成、编译验证、覆盖率分析 |
| 问题分析 | [troubleshooting/](troubleshooting/) | 测试日志定界、崩溃栈分析、问题归属判定 |

## Skills

### testing/

- [ohos-test-arkts-xts-generation](testing/ohos-test-arkts-xts-generation/) — ArkTS XTS 测试用例生成器，解析 .d.ts 生成 Hypium 测试用例，支持 5 种 Flow（A/B/C/D/E）模式、ArkTS-Dyn/Sta 双语法、覆盖率分析与编译验证。
- [ohos-test-capi-xts-generation](testing/ohos-test-capi-xts-generation/) — CAPI XTS 测试用例生成器，解析 .h 头文件生成 N-API 封装与 ArkTS 测试代码，支持三重校验与编译验证。

### troubleshooting/

- [ohos-issue-xts-log-analysis](troubleshooting/ohos-issue-xts-log-analysis/) — XTS 测试日志定界分析，支持多形态识别、时间窗切片、源码→领域证据链追溯、崩溃栈解析。

### design/

（暂无技能，后续将新增测试设计相关技能，详见 [design/README.md](design/README.md)。）
