# xts-generator 故障排除

> **xts-generator** - 常见问题解决方案

## 目录

- [Q1: 生成的测试用例无法编译](#q1-生成的测试用例无法编译)
- [Q2: 测试用例命名不符合规范](#q2-测试用例命名不符合规范)
- [Q3: 测试设计文档与测试用例不一致](#q3-测试设计文档与测试用例不一致)
- [Q4: Linux 环境编译失败](#q4-linux-环境编译失败)
- [Q5: 测试用例执行失败](#q5-测试用例执行失败)
- [Q6: 子系统配置文件未找到](#q6-子系统配置文件未找到)
- [Q7: 测试覆盖率分析不准确](#q7-测试覆盖率分析不准确)
- [获取帮助](#获取帮助)

---

## Q1: 生成的测试用例无法编译

### 可能原因

1. hypium 导入不正确
2. ArkTS 语法类型不匹配
3. 测试文件路径错误
4. @tc 注释块格式错误

### 解决方案

1. **检查 hypium 导入是否正确**：
   ```typescript
   import { describe, it, expect } from '@ohos/hypium';
   import { TestType, Level, Size } from '@ohos/hypium';
   ```

2. **检查 ArkTS 语法类型是否匹配**：
   - 读取 `.d.ts` 文件中的 `@since` 标签
   - 读取 `build-profile.json5` 中的 `arkTSVersion` 字段
   - 确保工程类型与 API 类型兼容

3. **检查测试文件路径**：
   - 确保测试文件路径在 `entry/src/ohosTest/ets/test/` 目录下
   - 确保文件命名符合规范

4. **检查 @tc 注释块格式**：
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

5. **查看编译错误日志**：
   - 参考 `modules/L4_Build/linux_compile_troubleshooting.md`

---

## Q2: 测试用例命名不符合规范

### 可能原因

1. 使用了大写下划线命名
2. 包含特殊标点符号
3. @tc.name 与 it() 第一个参数不一致

### 解决方案

1. **确保使用小驼峰命名（camelCase）**：
   - ✅ 正确示例：`onClickNormal001`
   - ✅ 正确示例：`uitestOnText401`
   - ❌ 错误示例：`ON_CLICK_NORMAL_001`
   - ❌ 错误示例：`test[MethodName].Param.0001`

2. **确保 @tc.name 与 it() 第一个参数完全一致**：
   ```typescript
   /**
    * @tc.name onClickNormal001
    */
   it('onClickNormal001', Level.LEVEL3, () => {
     // 测试代码
   });
   ```

3. **参考命名规范**：
   - 查看 `references/subsystems/_common.md` 的命名规范章节

---

## Q3: 测试设计文档与测试用例不一致

### 可能原因

1. 测试用例修改后未同步更新设计文档
2. 设计文档版本号未递增
3. 变更记录未更新

### 解决方案

1. **重新生成测试用例和设计文档**，确保同步

2. **检查设计文档的版本历史**，确保版本号递增：
   ```markdown
   | 版本 | 日期 | 变更内容 | 作者 |
   |------|------|---------|------|
   | 1.0 | 2026-02-10 | 初始版本 | xts-generator |
   | 1.1 | 2026-02-11 | 修改场景3的预期结果 | User |
   ```

3. **更新变更记录**，记录修改内容

4. **参考更新机制**：
   - 查看 `modules/L3_Generation/design_doc_generator.md`

---

## Q4: Linux 环境编译失败

### 可能原因

1. 使用了 `hvigorw` 命令（不适用于 Linux）
2. 编译环境未正确配置
3. BUILD.gn 配置错误
4. 预编译清理不彻底

### 解决方案

1. **必须使用 `build.sh` 脚本编译**，不要使用 `hvigorw`：
   ```bash
   ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=test_name
   ```

2. **检查编译环境配置**：
   - 参考环境准备指南：`modules/L4_Build/linux_compile_env_setup.md`
   - 确保工具链安装正确
   - 确保 SDK 下载完整

3. **检查 BUILD.gn 配置**：
   - 参考配置指南：`modules/L4_Build/build_gn_config.md`
   - 确保测试套名称正确
   - 确保源文件路径正确

4. **执行预编译清理**：
   ```bash
   rm -rf build
   rm -rf out
   ```
   - 参考清理指南：`modules/L4_Build/linux_prebuild_cleanup.md`

5. **查看编译错误日志**：
   - 参考问题排查指南：`modules/L4_Build/linux_compile_troubleshooting.md`

---

## Q5: 测试用例执行失败

### 可能原因

1. 测试逻辑错误
2. 前置条件未满足
3. 测试数据不正确
4. 依赖的资源未准备好

### 解决方案

1. **检查测试逻辑是否正确**

2. **检查前置条件是否满足**：
   - 权限配置
   - 网络环境
   - 设备状态

3. **检查测试数据是否正确**

4. **确保依赖的资源已准备好**

5. **使用 hypium 框架的调试功能**进行调试

---

## Q6: 子系统配置文件未找到

### 可能原因

1. 配置文件路径错误
2. 子系统名称拼写错误
3. 配置文件不存在

### 解决方案

1. **确保配置文件路径正确**：
   ```
   references/subsystems/{子系统名称}/_common.md
   ```

2. **确保子系统名称拼写正确**（区分大小写）

3. **如果子系统配置不存在，使用通用配置**：
   ```
   references/subsystems/_common.md
   ```

4. **参考现有子系统配置示例**：
   - ArkUI: `references/subsystems/ArkUI/_common.md`
   - ArkWeb: `references/subsystems/ArkWeb/_common.md`

---

## Q7: 测试覆盖率分析不准确

### 可能原因

1. 测试文件扫描不完整
2. API 定义解析错误
3. 测试用例命名不规范
4. 未覆盖的 API 未识别

### 解决方案

1. **确保测试文件扫描完整**，指定正确的测试路径

2. **检查 API 定义解析是否正确**，确保读取了正确的 `.d.ts` 文件

3. **确保测试用例命名符合规范**：
   ```
   SUB_[子系统]_[模块]_[API]_[类型]_[序号]
   ```

4. **手动检查未覆盖的 API**，补充测试用例

---

## 获取帮助

如果以上解决方案无法解决问题：

### 1. 查看详细文档

- [使用指南](./USAGE_GUIDE.md)
- [架构文档](./ARCHITECTURE.md)
- [配置指南](./CONFIG.md)

### 2. 查看模块文档

- [L4_Build](../modules/L4_Build/) - 编译相关问题
- [L3_Generation](../modules/L3_Generation/) - 测试生成相关问题
- [L2_Analysis](../modules/L2_Analysis/) - 分析相关问题

### 3. 查看参考配置

- [通用配置](../references/subsystems/_common.md)
- [子系统配置](../references/subsystems/)

### 4. 联系支持

- 技能维护者：xts-generator Team
- 文档版本：v1.0.0

---

**文档版本**: 1.0.0
**创建日期**: 2026-02-10
**最后更新**: 2026-02-10
**维护者**: xts-generator Team
