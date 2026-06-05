## Phase 5B: UiTest 测试代码生成（UI 类用例）

**前置条件**：Phase 4 设计文档已生成，且包含控件 ID 清单附录。

**与 Phase 5A 的执行关系**：
- **代码生成可并行**：UiTest 测试代码生成（Phase 5B）与 Demo 代码生成（Phase 5A Step 1a/1b）可并行，因为两者均从 Phase 4 设计文档的控件 ID 清单读取，无串行依赖
- **编译阶段**：Demo 和 UiTest 测试代码一起进入编译——同 HAP 模式作为同一编译单元；辅助包模式通过编译 group 将测试套和 Demo 辅助包作为整体编译

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

**加载模块**:
- `{knowledge_root}/common/xts_experience/09_methodology/14_uitest_templates.md`
- `{knowledge_root}/common/xts_experience/09_methodology/16_quality_constraints.md`
- `{knowledge_root}/common/xts_experience/01_framework/02_uitest_framework.md`
- `{knowledge_root}/common/xts_experience/05_patterns/01_demo_uitest_contract.md`

---

### 生成范围

仅生成 Step 0 分类为 UI 类的测试用例。每个 UI 类用例通过 UiTest 框架操作 Demo 界面完成验证。

### 生成流程

1. **读取设计文档控件 ID 清单附录**：
   - 提取所有控件 ID、类型、所在页面、关联测试用例
   - 提取页面规划（页面 ID → 路由路径）

2. **按页面分组 UI 类用例**：
   - 同一页面的用例归入同一个 describe 块
   - 每个页面对应一个 `Utils.pushPage()` 导航

3. **按测试场景选择模板**：
   - 加载 `{knowledge_root}/common/xts_experience/09_methodology/14_uitest_templates.md`
   - 根据用例的控件操作序列匹配对应模板

4. **生成 UiTest 测试代码**：
   - 从设计文档读取控件 ID，填入 `ON.id()` 引用
   - 从设计文档读取参数值，填入 `setText()` 调用
   - 从设计文档读取预期 UI 结果，填入断言

5. **生成测试文件**：
   - 文件命名：`{ModuleName}Ui.test.ets`（与 Demo 页面对应）
   - 文件包含 Apache 2.0 许可证头
   - 文件包含标准 `@tc` 注解块

### 测试场景模板匹配

| 控件操作序列特征 | 匹配模板 | 说明 |
|----------------|---------|------|
| input.setText → btn.click → result.getProperty | 标准模式 | 最常见：输入参数 → 执行 → 查看结果 |
| select.click → option.click → btn.click → result.getProperty | Select 模式 | 选择参数 → 执行 → 查看结果 |
| toggle.click → result.getProperty | Toggle 模式 | 切换开关 → 查看结果 |
| component.getProperty（无操作） | 只读模式 | 直接读取组件属性 |
| input.setText(无效值) → btn.click → status.getProperty('FAIL') | 错误场景 | 输入无效参数 → 验证错误状态 |

### @tc 注解块格式

```typescript
/**
 * @tc.number {用例编号}
 * @tc.name {用例名}
 * @tc.desc {用例描述}
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level {n}
 * @tc.require
 * @tc.precondition 已安装 Demo HAP，已导航到 {页面名称}
 * @tc.step {从设计文档的控件操作序列生成}\n2. 等待 UI 更新\n3. 读取结果区域
 * @tc.expected {从设计文档的预期 UI 结果生成}
 */
```

### 控件 ID 使用约束

1. **ID 必须来源于设计文档**：`ON.id('xxx')` 中的 `xxx` 必须在设计文档的控件 ID 清单附录中存在
2. **禁止猜测 ID**：不存在的控件 ID 会导致 `waitForComponent` 返回 null，测试必然失败
3. **页面路由对应**：`Utils.pushPage('pages/Page001')` 中的路由必须与设计文档的页面规划一致
4. **操作顺序对应**：UiTest 的操作步骤必须与设计文档的控件操作序列一致

### 输出

**UiTest 测试代码文件**：`{ModuleName}Ui.test.ets`

- 完整的 ArkTS UiTest 测试代码
- 符合 Hypium 框架规范 + UiTest 框架规范
- 包含标准 `@tc` 注解块
- 每个测试用例对应设计文档中的一个 UI 类用例条目

### 代码质量约束

生成的代码必须满足 `quality_constraints.md` 中的全部规则（R002-R029），确保天然通过 check-test-code-quality 扫描。特别关注：
- 每条 `waitForComponent` 返回后必须判空
- 禁止使用 `as any`
- Driver 在 `beforeAll` 中创建，禁止在 `it` 中重复创建
- 异步操作必须 `await`
