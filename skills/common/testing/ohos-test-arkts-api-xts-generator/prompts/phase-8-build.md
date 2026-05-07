## Phase 8: Build Verification

**加载模块**: 根据运行环境选择
- Linux: `modules/L3_Validation/builder/build_workflow_linux.md`
- Windows: `modules/L3_Validation/builder/build_workflow_windows.md`

### Linux 环境

1. **编译工具**: `./test/xts/acts/build.sh`（禁止使用 `hvigorw`）
2. **异步编译（推荐）**: `scripts/async_build.sh`
3. **预编译清理（强制）**: `scripts/cleanup_group.sh`
4. **错误自动处理**: 语法错误自动修复（最多 3 次重试），配置错误需用户确认

### Windows 环境

根据关键词自动选择：
- **动态编译（默认）**: DevEco Studio IDE 或 `hvigorw.bat`
- **静态编译**: 当提到 `arkts-sta`、`ArkTS静态` 等关键词时启用

### 静态编译注意

- 需要 JAVA_HOME 配置
- Hvigor 版本校验（目标: `6.0.0-arkts1.2-ohosTest-*`）
- 需调用 `arkts-static-spec` 技能进行最终语法校验
