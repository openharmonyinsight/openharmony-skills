# Build Error Analyzer Skill

本技能帮助分析 OpenHarmony 构建错误，从 `last_error.log` 中提取错误信息，并基于错误模式和历史案例提供具体的修复建议。

## 快速开始

### 1. 提取最新的构建错误

首先，从构建日志中提取错误：

**普通产品构建**（如 rk3568）：
```bash
cd <openharmony_root>
./extract_last_error.sh out/rk3568/build.log
```

**SDK 构建**（⚠️ 特殊路径）：
```bash
cd <openharmony_root>
./extract_last_error.sh out/sdk/build.log
```

这将在构建日志所在目录创建 `last_error.log`（如 `out/rk3568/last_error.log` 或 `out/sdk/last_error.log`）。

### 2. 分析错误

使用本技能进行分析：

```
用户: "帮我分析一下构建错误"
```

或者直接：

```
用户: "分析 last_error.log"
```

本技能将：
1. 读取 `last_error.log`
2. 分类错误类型
3. 匹配历史案例
4. 提供具体的修复建议

## 错误分类

### 1. 链接错误 (SOLINK/LINK 任务)

**症状**: `ld.lld: error: undefined symbol`

**常见原因**:
- BUILD.gn 中缺少 .cpp 文件
- 符号未导出（缺少 ACE_FORCE_EXPORT）
- 符号未在 libace.map 白名单中

**参考案例**: `examples/undefined-symbol-missing-cpp.md`

### 2. 编译错误 (CXX/CC 任务)

**症状**: `error:`, `fatal error:`

**常见原因**:
- 不完整类型（缺少头文件）
- 重定义错误
- 语法错误

### 3. 构建系统错误

**症状**: Ninja 配置问题，GN 错误

**常见原因**:
- BUILD.gn 语法错误
- 缺少依赖项

## 历史案例

### 案例 1: 未定义符号 - 缺少 .cpp 文件

**文件**: `examples/undefined-symbol-missing-cpp.md`

**问题**: 头文件优化后，出现多个未定义符号错误

**解决方案**:
1. 将 .cpp 文件添加到组件 BUILD.gn
2. 添加到 frameworks/core/BUILD.gn 的 ace_core_ng_source_set
3. 使用 ACE_FORCE_EXPORT 导出跨模块符号
4. 将符号添加到 build/libace.map

**关键经验**:
- libace.z.so 只链接 ace_core_ng 库
- 新的 .cpp 必须在 ace_core_ng_source_set 中
- 跨模块符号需要导出

## 技能结构

```
build-error-analyzer/
├── SKILL.md              # 主技能定义
├── README.md             # 本文件
├── examples/             # 历史案例
│   └── undefined-symbol-missing-cpp.md
└── references/           # 参考资料
    └── (待添加)
```

## 添加新案例

当解决新的构建错误时：

1. **记录案例**:
   ```bash
   # 创建新案例文件
   vim examples/<case-name>.md
   ```

2. **包含内容**:
   - 错误签名（来自 last_error.log）
   - 根本原因分析
   - 逐步解决方案
   - 修改的文件
   - 验证命令
   - 关键经验

3. **更新 SKILL.md**:
   - 添加新案例引用
   - 如果发现新模式，更新错误模式

4. **测试技能**:
   - 提取相似模式的错误
   - 验证技能能够推荐解决方案

## 常用命令

### 提取错误

```bash
# 普通产品（从 OpenHarmony 根目录）
cd <openharmony_root>
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/rk3568/build.log

# SDK 构建（⚠️ 特殊路径：out/sdk/ 而非 out/ohos-sdk/）
foundation/arkui/ace_engine/.claude/skills/build-error-analyzer/script/extract_last_error.sh out/sdk/build.log
```

### 检查符号导出

```bash
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep SymbolName
```

### 搜索定义

```bash
grep -r "SymbolName" --include="*.h" --include="*.cpp" frameworks/
```

### 检查 BUILD.gn

```bash
grep -r "filename.cpp" frameworks/*/BUILD.gn
```

## 最佳实践

### 添加新 .cpp 文件时

1. ✅ 创建实现文件
2. ✅ 添加到组件 BUILD.gn
3. ✅ 添加到 frameworks/core/BUILD.gn 的 ace_core_ng_source_set
4. ✅ 如果跨模块使用，导出符号
5. ✅ 使用 nm -D 验证

### 优化头文件时

1. ✅ 对仅头文件常量使用 inline constexpr
2. ✅ 不要同时在 .h 和 .cpp 中定义
3. ✅ 确保在使用点可见完整类型
4. ✅ 检查 ODR 违规

### 导出符号时

1. ✅ 在头文件声明中添加 ACE_FORCE_EXPORT（不是 .cpp）
2. ✅ 将符号添加到 build/libace.map
3. ✅ 使用格式: `OHOS::Ace::NG::ClassName::MethodName*;`
4. ✅ 使用 nm -D 验证

## 相关技能

- **openharmony-build**: 构建 OpenHarmony 代码库
- **compile-analysis**: 编译性能分析

## 贡献

改进本技能：

1. 在解决不同的构建错误时添加新案例
2. 更新 SKILL.md 中的错误模式
3. 为新错误类型添加验证命令
4. 记录最佳实践和经验教训

## 版本历史

- **0.7.0** (2026-02-02): 测试链接错误支持
  - ✨ 新增测试链接错误案例分析：`test-missing-source-files.md`
  - 📝 新增 Case 7：测试中缺失源文件的通用解决方案
  - 🎯 泛化案例场景，涵盖所有缺失源文件情况（log_wrapper.cpp、string_utils.cpp 等）
  - 🌳 添加决策树帮助判断正确的解决方案
  - ⚠️ 强调只添加源文件，不修改编译标志

- **0.6.0** (2025-02-02): 新增 SDK 编译错误分析支持
  - ✨ 添加 SDK 错误触发关键词："分析SDK的编译错误"、"analyze SDK build errors"、"check SDK errors"
  - ⚠️ 特别说明：SDK 日志路径为 `out/sdk/build.log` 和 `out/sdk/last_error.log`（特殊目录）
  - 📝 更新所有路径示例，标注 SDK 的特殊目录结构
  - 🔧 优化错误提取命令，支持 SDK 路径

- **0.5.0** (2026-01-27): 模板类方法导出支持
- **0.4.0** (2026-01-27): 模板实例化类型导出支持
- **0.3.0** (2026-01-27): 符号导出最佳实践
- **0.2.0** (2026-01-27): 添加重定义错误案例
- **0.1.0** (2026-01-27): 初始版本，包含未定义符号案例研究
