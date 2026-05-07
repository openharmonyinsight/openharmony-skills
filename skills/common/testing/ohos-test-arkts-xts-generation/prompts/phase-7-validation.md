## Phase 7: Format & Validate (MANDATORY - NEVER SKIP)

**加载模块**:
- `modules/L3_Validation/validator/format_validator.md`

此阶段分两步执行：A) 生成上下文检查（当前 skill 执行）→ B) 代码质量深度扫描（调用 check-test-code-quality）。

### 重要

此阶段是**核心强制步骤**，绝对不可跳过。跳过此阶段将导致：`as any` 类型断言在 ArkTS-Sta 下编译失败、资源泄漏导致设备内存耗尽、空 catch 块使测试永远"通过"而实际未验证、check-test-code-quality 扫描不通过则无法合入代码。

---

### 步骤 A: 生成上下文检查

使用 `validate_test_context.py` 脚本自动检查 A.1/A.2/A.3/A.7/A.8，再由模型手动检查剩余项。

#### 自动检查（脚本执行）

```bash
python {skill_root}/scripts/validate_test_context.py \
  --file {生成文件路径}.test.ets \
  --expected-module "{被测模块，如 @ohos.multimedia.media}" \
  --design-doc {设计文档路径}.design.md
```

脚本自动检查以下 5 项：

| 检查项 | 说明 | 检测方式 |
|--------|------|---------|
| A.1 许可证头 | Apache 2.0 完整头 | 匹配 `Apache License` + `Version 2.0` + `Copyright` |
| A.2 hypium 导入 | `@ohos/hypium` 包含 describe/it/expect | 正则匹配 import 语句 |
| A.3 被测模块导入 | 导入了正确的被测模块 | 匹配 `--expected-module` 参数 |
| A.7 禁止 as any | 无 `as any` 类型断言 | 正则匹配（排除注释行） |
| A.8 设计文档一致性 | 每个 `@tc.number` 在设计文档中有对应条目 | 提取所有 @tc.number 并在 design.md 中搜索 |

**处理脚本结果**：如果脚本输出 `[PASS]`，说明这 5 项全部通过；如果有 `[ISSUES]`，按报告修复后重新运行脚本。

#### 手动检查（模型执行）

以下检查项需要模型理解代码语义，无法正则匹配：

- **A.4 afterEach 资源释放**：afterEach 中释放播放器、文件描述符等资源，使用 try-catch 包裹
- **A.5 null/undefined 安全**：对象使用前先创建/初始化，文件描述符关闭前检查有效性
- **A.6 deprecated API**：不使用已废弃的 API（如 AudioPlayer→AVPlayer）
- **A.9 ArkTS 语法规范**：动态项目遵循 `references/ArkTS_Dynamic_Syntax_Rules.md`，静态项目调用 `arkts-static-spec`

---

### 步骤 B: 代码质量深度扫描（必选）

启动 subagent 调用 `check-test-code-quality` 对生成的测试文件执行深度质量扫描：

```
/check-test-code-quality {生成文件路径} --rules R002,R003,R004,R008,R009,R013,R015,R016,R018,R022,R023
```

**扫描结果处理**：

| 结果 | 处理方式 |
|------|---------|
| 0 issues | 通过，进入 Phase 8 |
| 有 issues | 自动修复所有问题 → 重新扫描 → 直到通过 |

**注意**：Phase 5 已在生成时内化了这 11 条规则约束，步骤 B 作为兜底确认。如果扫描发现问题，说明生成阶段遗漏了约束，需修复后重新扫描。

---

### 完成条件

步骤 A 和步骤 B 全部通过后，进入 Phase 8。

- [ ] 许可证头完整
- [ ] hypium 导入正确
- [ ] 被测模块导入正确
- [ ] afterEach 资源释放完整
- [ ] 无 as any 类型断言
- [ ] 设计文档一致
- [ ] ArkTS 语法规范（动态/静态）
- [ ] check-test-code-quality 扫描通过（0 issues）
