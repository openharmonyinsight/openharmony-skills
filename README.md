# OpenHarmony Skills

OpenHarmony Skills 仓库用于集中管理面向 OpenHarmony / HarmonyOS 开发、审查、构建、测试、问题分析和提交流程的可复用 Skill 定义，供 AI 助手按场景调用。

本仓库主分支当前采用扁平目录结构：每个可安装 Skill 放在 `skills/<skill-name>/` 下。Skill 的目录分层不强制与 `release` 分支一致，但上库命名、目录名和文件命名要求必须与 `release` 分支规范保持一致。历史存量 Skill 在迁移完成前可能保留旧名，新上库或重构改造时按新规范执行。

## 当前 Skill 列表

以下列表来自 `skills/*/SKILL.md` 顶层 Skill 目录。嵌套在 `rules/`、`references/` 等目录中的辅助 Skill 不作为主列表项统计。

```text
afwk-hb-build
ai-feedback-collector
ai-feedback-collector-zh
ai-generated-business-code-review
ai-generated-ut-code-review
android-to-harmonyos-migration-workflow
api-doc-checker
appmgr-api-generator
arkts-sta-playground
arkts-static-spec
arkui-api-design
arkui-menu-debug
arkuix-module-adapter
arkweb-app-debug
arkweb-build
arkweb-thread-safety-review
audio_pr_create
build-error-analyzer
check-test-code-quality
code-checker
code-problem-analyzer
compile-analysis
comprehensive-code-review
cpp-core-guidelines-review
cpp-include-sorter
create-pr
dsoftbus-security
ets-runtime-dev
generate-interface-uml
gitcode-cli
gitcode-pr
glslviewer-shader-debug
graphic-2d-PR
graphic-2d-format
harmonyos-ai-agent-skill
harmonyos-autotest
header-optimization
log-coverage-analyzer
oh-add-memory-trace-tags
oh-arkruntime-interop-promise
oh-arkruntime-taskpool-dependency-analysis
oh-arkruntime-thread-safety-audit
oh-capi-xts-gen
oh-distributed-security-design-review
oh-docs-check-zh-cn
oh-graphic-gitcode-pr-creator
oh-interfaces-ipc-to-service
oh-memory-leak-detection
oh-pdd-code-generator
oh-pdd-design-doc-generator
oh-pdd-prd-analysis
oh-pr-workflow
oh-precommit-codecheck
oh-ut-generator
oh-xts-build-run
oh-xts-generator-template
ohos-app-build-debug
ohos-dev-graphics-pixel-tests-generator
ohos-dev-graphics-stability-code-review
ohos-dev-graphics3d-combined-postprocess
ohos-issue-graphics-cppcrash-analysis
ohos-issue-graphics-sysfreeze-analysis
ohos-test-fuzz-generation
ohos-test-graphics3d-static-api-unit-test
ohos-test-ut-generation
ohos-ut-test-coverage-report-generation
openharmony-arkts-layer
openharmony-build
openharmony-ci
openharmony-cpp
openharmony-download
openharmony-security-review
openharmony-ut
review-gitcode-pr
xts-generator
```

## 适用场景

- OpenHarmony C++ / ArkTS / ArkUI 代码开发与审查
- 系统服务、安全、并发、内存问题分析
- 编译、构建、CI、日志和错误定位
- API 文档检查、设计文档生成、PRD 分析
- 自动化测试、XTS 测试生成与执行
- GitCode / PR / Issue 工作流处理
- 图形、ArkWeb、ArkRuntime、应用迁移、运行时等专项场景

## 使用方式

安装整个仓库：

```bash
npx skills add openharmonyinsight/openharmony-skills
```

安装单个 Skill：

```bash
npx skills add openharmonyinsight/openharmony-skills --skill <skill_name>
```

其中 `<skill_name>` 替换为 `skills/` 目录下的具体技能名，例如 `openharmony-security-review`。

## 仓库结构

主分支当前结构：

```text
openharmony-skills/
├── skills/
│   ├── <skill-name>/
│   │   ├── SKILL.md
│   │   ├── README.md        # 可选
│   │   ├── references/      # 可选
│   │   ├── examples/        # 可选
│   │   └── evals/           # 入库要求
│   └── ...
└── README.md
```

`release` 分支采用 `skills/common/<stage>/<skill-name>/` 和 `skills/domain/<namespace-domain>/<stage>/<skill-name>/` 的分层目录。主分支不要求按该目录分层放置，但新增、迁移或改造 Skill 时，命名和文件要求沿用 `release` 分支规范。

## 命名与文件要求

新增、迁移或改造 Skill 时，推荐使用 `skill-creator` 生成初稿，并遵守以下规则：

- Skill 机器名采用 `ohos-<stage>-<domain>-<capability>`。
- 机器名只使用小写字母、数字和连字符，不使用空格、下划线、点号或斜杠。
- `<stage>` 使用阶段缩写：`req`、`design`、`dev`、`test`、`ci`、`issue`。
- 如未来需要按阶段建目录，目录阶段名使用完整名称：`requirements`、`design`、`development`、`testing`、`cicd`、`troubleshooting`；主分支当前不要求创建这些阶段目录。
- `<domain>` 表示技术域、语言、框架、子系统或能力主题域，例如 `cpp`、`arkts`、`arkui`、`graphics-3d`。
- `<capability>` 必须是动名词短语或名词短语，避免使用过宽泛的单个名词。
- Skill 目录名必须与 `SKILL.md` Front Matter 中的 `name` 一致。
- `SKILL.md` 必须存在，并包含有效 YAML Front Matter。
- `SKILL.md` 顶层 Front Matter 必须包含 `name` 和 `description`，`description` 必须说明触发场景。
- 入库治理字段建议放入 `metadata`，不要散落为额外顶层字段。

推荐的单个 Skill 目录结构：

```text
<skill-name>/
  SKILL.md
  README.md
  references/
  examples/
  evals/
```

## 入库要求

提交新的 Skill 或对现有 Skill 做较大改造前，必须满足以下要求：

1. 使用 `skills-judge` 对 Skill 进行设计质量评分，结果达到 B 级或以上。
2. 具备 eval 用例，测试输入、预期结果和评估方式应随 Skill 一起提交。
3. `with skill` 评估必须全部通过。
4. 同时运行 `with skill` 和 `without skill` 评估，用于证明 Skill 相比基线的效果提升。
5. 上传 `with skill` 和 `without skill` 的最终评估报告，报告中应包含用例结果、通过情况和关键差异。

## 入库检查清单

```text
[ ] Skill name 是否全局唯一？
[ ] Skill name 是否符合 ohos-<stage>-<domain>-<capability>？
[ ] capability 是否使用动名词短语或名词短语？
[ ] Skill 目录名是否与 SKILL.md 中的 name 一致？
[ ] SKILL.md 是否包含有效 YAML Front Matter？
[ ] description 是否说明该 Skill 的触发场景？
[ ] 是否包含 eval 用例？
[ ] with skill 评估是否全部通过？
[ ] 是否上传 with skill 和 without skill 最终评估报告？
[ ] skills-judge 评分是否达到 B 级或以上？
```

## 贡献

欢迎提交新的 Skill 定义或改进现有 Skill。提交前请确保命名、文件结构、评估材料和入库报告完整，避免只提交 `SKILL.md` 而缺少验证证据。

## 许可证

请查看 LICENSE 文件了解许可证信息。
