## Phase 7: Build Verification

---

### 调用模式

| 模式 | 触发条件 | 与工作流模式的差异 |
|------|---------|-------------------|
| **工作流模式** | Phase 1-6 流程中，Phase 6 完成后自动进入 | 正常流程 |
| **独立编译模式** | 用户直接要求编译（"编译xxx"、"重新编译"、"build"） | 跳过 Phase 1-6，需自行确定 suite 路径 |

**独立编译模式**仅需额外执行以下准备：

1. 读取 `{skill_root}/.oh-capi-xts-config.json` 获取 `OH_ROOT`
2. 从用户输入推断目标测试套路径（优先级：用户指定路径 > 子系统目录名 > 询问用户）

编译流程本身完全一致。

---

### 📚 参考文档（按需查阅）

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `modules/L3_Validation/builder/build_workflow_c.md` | CAPI 编译工作流（build.sh 命令、签名、编译排错、BUILD.gn 类型详解） | 编译流程细节不明确时参考 |
| 编译/运行错误排查 | `references/error_handling.md` | 编译失败时加载 |

---

### ⚙️ 按需加载

| 平台/任务 | 加载文件 | 说明 |
|----------|---------|------|
| Linux 环境配置 | `modules/L3_Validation/builder/linux_compile_env_setup_c.md` | Linux 编译环境搭建 |

---

### 🚫 Do NOT Load

```
所有 modules/L1_Analysis 模块
所有 modules/L2_Generation 模块
```

---

### 编译流程

编译流程详见 `modules/L3_Validation/builder/build_workflow_c.md`。核心步骤：

1. **环境检查**：确认 OH_ROOT、编译工具链（hvigor）、签名文件可用
2. **清理旧残留**：
   ```bash
   bash {skill_root}/scripts/cleanup_group.sh ${TARGET_PATH}
   ```
3. **异步编译**：
   ```bash
   bash {skill_root}/scripts/async_build.sh ${TARGET_PATH}
   ```
4. **监控编译状态**：
   ```bash
   python {skill_root}/scripts/async_build_manager.py status
   ```
5. **检查编译结果**：确认 `.hap` 文件生成

### 编译失败处理

加载 `references/error_handling.md`，按错误分级处理：

| 错误级别 | 处理策略 | 最大重试 |
|---------|---------|---------|
| Level 1（语法错误、类型不匹配） | 自动修复后重新编译 | 3 次 |
| Level 2（链接错误、NAPI 注册错误） | 自动修复后重新编译 | 3 次 |
| Level 3（配置错误） | 展示错误信息，等待用户确认 | 1 次 |
| Level 4（环境错误） | 终止，提示修正环境 | 0 次 |

3 次重试后仍失败 → 提交给用户确认。

### 结果判定

| 结果 | 操作 |
|------|------|
| 编译成功 | Phase 7 完成 |
| 自动修复后编译成功 | Phase 7 完成，记录修复内容 |
| 重试耗尽 | 展示错误日志，等待用户确认 |
