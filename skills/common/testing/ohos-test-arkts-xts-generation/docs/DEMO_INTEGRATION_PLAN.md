# Demo Pipeline 整合方案：嵌入 XTS 生成流水线 Phase 5

## 1. 背景与目标

### 1.1 当前 Phase 5 现状

当前 Phase 5（Generate Test Cases）仅生成 XTS 测试用例代码（`.test.ets`），测试方式为纯代码调用被测 API + 断言。对于需要 UI 交互验证的测试点（如 ArkUI 组件属性、事件响应），缺少可交互的被测应用界面。

### 1.2 整合目标

将 `demo-pipeline` 技能整合进 Phase 5，使其能够：

- 根据设计文档中的 UI 类测试点，生成可交互的 Demo 被测应用（HAP）
- Demo 内部调用被测 API 并将结果映射到 UI 控件展示
- XTS 测试代码通过 UiTest 框架（Driver/ON/Component）操作 Demo 界面完成验证

### 1.3 配合关系

```
Demo 应用（被测 HAP）                     XTS 测试代码
┌───────────────────────────┐            ┌──────────────────────────────┐
│ 内部调用被测 API           │            │ import {Driver, ON}          │
│ 将参数/结果映射到 UI 控件  │            │   from '@ohos.UiTest'        │
│ 所有控件带 id() 修饰符     │ ◄──契约──► │ driver.findComponent(        │
│                            │  控件ID    │   ON.id('btn_001_execute'))  │
│ Button('执行')             │  一致      │ component.click()            │
│   .id('btn_001_execute')   │            │ component.getProperty('text')│
│                            │            │ expect(text).assertEqual(…)  │
│ Text(result)               │            │                              │
│   .id('result_001_01')     │            │ driver.findComponent(        │
│                            │            │   ON.id('result_001_01'))    │
└───────────────────────────┘            └──────────────────────────────┘
```

**核心原则**：Demo 提供可交互的 UI 界面，UiTest 通过界面交互（点击、输入、读取结果）触发和验证测试点。Demo 内部的 API 调用对 UiTest 透明。

---

## 2. 整合后的 Phase 5 结构

### 2.1 Phase 5 总体流程

```
Phase 4 设计文档 (.design.md，含控件ID清单附录)
         │
         ▼
Phase 5: Generate Test Cases & Demo
  │
  ├─ Step 0: 测试用例分类
  │     将设计文档中的用例分为 UI 类和非 UI 类
  │
  ├─ Step 1: [子流程A] Demo 应用生成（仅存在 UI 类用例时执行）
  │     ├─ 1a: Demo UI 设计（读取设计文档中的控件ID清单）
  │     ├─ 1b: Demo 代码生成
  │     └─ 1c: Demo 编译验证
  │     输出: TestDemo/
  │
  ├─ Step 2: [子流程B] XTS 测试代码生成（与 Step 1 可并行）
  │     ├─ 2a: 非 UI 类用例 → 生成直接 API 调用测试
  │     └─ 2b: UI 类用例 → 读取设计文档中的控件ID清单，生成 UiTest 测试
  │     输出: {Module}.test.ets
  │
  └─ Step 3: 输出汇总
        输出: 文件清单
```

### 2.2 执行顺序约束

```
Phase 4 设计文档（含控件ID清单附录）
         │
         ├────→ Step 1: Demo 生成（读取控件ID清单）
         │
         └────→ Step 2: 测试代码生成（读取控件ID清单）
                    ├─ 2a: 不依赖控件ID
                    └─ 2b: 从设计文档读取控件ID
```

**Step 1（代码生成）和 Step 2（测试代码生成）可并行**：控件 ID 在 Phase 4 设计文档中已预定义，Demo 代码生成和 UiTest 测试代码生成均从设计文档读取，无串行依赖。

**编译阶段**：Demo 和 UiTest 测试代码一起进入编译——同 HAP 模式下作为同一编译单元；辅助包模式下通过编译 group 将测试套和 Demo 辅助包作为整体编译。

---

## 3. Phase 4 扩展：控件 ID 清单附录

### 3.1 设计文档格式扩展

Phase 4 在生成设计文档时，对 UI 类用例追加控件规划字段：

```markdown
### 测试用例 1: SUB_ARKUI_XXX_EVENT_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_ARKUI_XXX_EVENT_001 |
| 用例名 | 组件属性正常值测试 |
| ... | ...（原有字段不变） |
| 执行方式 | UI |
| 页面 | PAGE-001 |
| 控件操作序列 | input_001_value.setText('200') → btn_001_execute.click() → result_001_01.getProperty('text') |
| 预期 UI 结果 | result_001_01 显示 '200.00vp'，status_001_01 显示 'PASS' |
```

### 3.2 控件 ID 清单附录

设计文档末尾追加控件 ID 清单，作为 Demo 生成和 UiTest 代码生成的**共享契约**：

```markdown
## 附录：控件 ID 清单

### 控件总表

| 控件 ID | 类型 | 所在页面 | 标签 | 默认值 | 关联测试用例 |
|---------|------|---------|------|--------|-------------|
| input_001_value | TextInput | PAGE-001 | 参数输入 | '' | SUB_ARKUI_XXX_EVENT_001 |
| btn_001_execute | Button | PAGE-001 | 执行 | — | SUB_ARKUI_XXX_EVENT_001 |
| btn_001_reset | Button | PAGE-001 | 重置 | — | SUB_ARKUI_XXX_EVENT_001 |
| result_001_01 | Text | PAGE-001 | 结果展示 | '' | SUB_ARKUI_XXX_EVENT_001 |
| status_001_01 | Text | PAGE-001 | 状态指示 | 'WAITING' | SUB_ARKUI_XXX_EVENT_001 |

### 页面规划

| 页面ID | 页面名称 | 路由路径 | 涉及API | 控件数 |
|--------|---------|---------|--------|--------|
| PAGE-001 | 属性测试页 | pages/Page001 | setWidth | 5 |

### 控件 ID 命名规范

```
{type}_{page_seq}_{semantic_name}
type: btn | input | textarea | toggle | select | result | status | log
page_seq: 3 位零填充页面序号
例: btn_001_execute, input_001_value, result_001_01
```
```

### 3.3 控件 ID 的作用

| 消费方 | 读取内容 | 用途 |
|--------|---------|------|
| Demo 生成（Step 1） | 控件 ID + 类型 + 标签 + 页面规划 | 生成 ArkUI 页面代码，控件带 `.id()` |
| UiTest 生成（Step 2b） | 控件 ID + 关联测试用例 + 操作序列 | 生成 `ON.id()` 引用和界面交互代码 |

---

## 4. Step 0: 测试用例分类

### 4.1 分类规则

读取 Phase 4 设计文档，按以下规则将测试用例分为 UI 类和非 UI 类：

| 分类 | 条件 | 测试方式 |
|------|------|---------|
| **UI 类** | 测试类型为 `EVENT`，或涉及组件属性/界面交互/页面跳转的用例 | Demo + UiTest |
| **非 UI 类** | 测试类型为 `PARAM`/`ERROR`/`RETURN`/`BOUNDARY`，且不涉及 UI 交互 | 直接 API 调用 |

### 4.2 子系统维度判断

| 子系统 | 默认分类策略 |
|--------|-------------|
| ArkUI | 大部分用例为 UI 类（组件属性、事件、布局） |
| ArkWeb | Web 组件属性/事件为 UI 类，webview API 为非 UI 类 |
| ability | 页面跳转/生命周期为 UI 类，纯 Ability API 为非 UI 类 |
| 其他 | 默认为非 UI 类，除非用例显式涉及 UI 交互 |

### 4.3 分类结果输出

```markdown
## 测试用例分类结果

### UI 类用例（需要 Demo）
| 用例编号 | 用例名 | 类型 | 涉及 API |
|----------|--------|------|---------|

### 非 UI 类用例（纯代码测试）
| 用例编号 | 用例名 | 类型 | 涉及 API |
|----------|--------|------|---------|

### 统计
- UI 类：X 个 | 非 UI 类：X 个
```

**若所有用例均为非 UI 类**，跳过 Step 1（Demo 生成），直接进入 Step 2a。

---

## 5. Step 1: Demo 应用生成

### 4.1 输入

从 XTS 流水线已有产物中提取，适配为 demo-pipeline 所需格式：

| Demo Pipeline 所需输入 | 来源 | 适配方式 |
|----------------------|------|---------|
| `demo_test_points.md` | Step 0 分类的 UI 类用例 | **新增适配转换**（见 4.2） |
| 控件 ID 清单 | Phase 4 设计文档附录 | **直接读取**（Phase 4 已预定义） |
| 领域选择 | Phase 1 子系统配置 | **子系统 → 领域映射**（见 4.3） |
| API 参考 JSON | Phase 3 的 UnifiedAPIInfo | **共享**（需确保 api-reference 覆盖） |
| 需求分析报告 | 用户提供（可选） | 直接传递 |
| 语法类型 | Phase 7 确定 | 传递 ArkTS-Dyn/ArkTS-Sta |

### 4.2 设计文档 → 测试点转换适配

将 Phase 4 的 `.design.md` 中 UI 类用例转换为 demo-pipeline 的 `demo_test_points.md` 格式。

**转换映射表**：

| .design.md 字段 | demo_test_points.md 字段 | 转换规则 |
|-----------------|------------------------|---------|
| 用例编号 | 测试点ID | 直接映射 |
| 用例名 | 描述 | 直接映射 |
| 类型 | 技术类型 | PARAM/ERROR/RETURN/BOUNDARY/EVENT 直接映射 |
| 级别 | 优先级 | P0/P1/P2 直接映射 |
| 测试步骤 | 操作步骤 | **关键转换**：代码步骤 → 用户操作描述（见下方） |
| 预期结果 | 预期结果 | **关键转换**：代码断言 → 可观察 UI 行为（见下方） |

**操作步骤转换示例**：

```
设计文档（代码步骤）：
  1. 调用 component.setWidth(200)
  2. 验证 width 属性值为 '200.00vp'

转换后（用户操作）：
  1. 在输入框输入宽度值 200
  2. 点击"执行"按钮
  3. 查看结果区域显示的宽度值
```

**预期结果转换示例**：

```
设计文档（代码断言）：
  expect(width).assertEqual('200.00vp')

转换后（可观察 UI 行为）：
  结果区域显示 '200.00vp'，状态为 PASS
```

### 4.3 子系统 → 领域映射

| XTS 子系统 | demo-pipeline 领域 | domains.yaml key |
|-----------|-------------------|-----------------|
| ArkUI | ArkUI | `ArkUI` |
| arkweb | ArkWeb | `ArkWeb` |
| ability | 元能力 | `元能力` |
| bundlemanager | 包管理 | `包管理` |
| testfwk | — | 不生成 Demo（测试框架无 UI 场景） |
| 其他 | — | 需在 domains.yaml 中新增 |

**未覆盖的子系统**：需在 demo-pipeline 的 `reference/domains.yaml` 和 `reference/api-reference/` 中补充对应领域的配置和 API 参考文件。

### 4.4 执行 demo-pipeline 三个阶段

调用 demo-pipeline 技能，依次执行：

| 子阶段 | demo-pipeline 阶段 | 输出 |
|--------|-------------------|------|
| 1a | 阶段1：Demo UI 设计 | `demo_design.md` |
| 1b | 阶段2：代码生成 | `TestDemo/` 工程 + `demo_code_manifest.md` |
| 1c | 阶段3：编译验证 | 编译通过/失败的 Demo HAP |

### 4.5 Step 1 输出产物

| 产物 | 路径 | 用途 |
|------|------|------|
| Demo 工程 | `{输出目录}/TestDemo/` | 被测 HAP，需安装到设备 |
| Demo 设计文档 | `{输出目录}/demo_design.md` | 页面结构参考 |
| 编译状态 | `demo_code_manifest.md` 中记录 | Phase 8 编译验证参考 |

---

## 6. Step 2: XTS 测试代码生成

### 5.1 Step 2a：非 UI 类用例（不依赖 Demo）

与当前 Phase 5 逻辑完全相同，生成直接 API 调用式测试：

```typescript
import {describe, it, expect} from '@ohos/hypium';
import {APIName} from '@kit.XXXKit';

it('testMethodParam001', Level.LEVEL1, () => {
  let result = apiObject.methodName(validParam);
  expect(result).assertEqual(expectedValue);
});
```

### 5.2 Step 2b：UI 类用例（从设计文档读取控件 ID）

**前置条件**：Phase 4 设计文档已包含控件 ID 清单附录。

**核心流程**：

1. **读取设计文档中的控件 ID 清单附录**：获取所有控件 ID 常量及关联测试用例
2. **读取页面路由**：从设计文档中获取页面规划（PAGE-xxx → 路由路径）
3. **按测试用例生成 UiTest 代码**：
   - 每个用例通过 `ON.id()` 定位设计文档中预定义的控件
   - 通过 `component.click()`/`component.setText()` 触发界面交互
   - 通过 `component.getProperty('text')` 读取结果区域
   - 断言结果是否符合设计文档预期

**UiTest 测试代码模板**：

```typescript
import {describe, beforeAll, it, expect, Level} from '@ohos/hypium';
import {Driver, ON} from '@ohos.UiTest';
import Utils from '../common/Utils';

export default function DemoUiTest() {
  let driver: Driver;

  beforeAll(async (done: Function) => {
    await Utils.pushPage('pages/Page001', done);
    await Utils.sleep(1000);
    driver = await Driver.create();
    await Utils.sleep(1000);
    done();
  });

  describe('XXX_UiTest', () => {
    /**
     * @tc.number SUB_ARKUI_XXX_EVENT_001
     * @tc.name 组件属性正常值测试
     * ...
     */
    it('testComponentProp001', Level.LEVEL1, async (done: Function) => {
      // 1. 定位输入控件，输入参数
      const input = await driver.waitForComponent(ON.id('input_001_value'), 2000);
      if (input) {
        await input.setText('200');
      } else {
        expect().assertFail();
        done();
        return;
      }
      await Utils.sleep(500);

      // 2. 点击执行按钮
      const btn = await driver.waitForComponent(ON.id('btn_001_execute'), 2000);
      if (btn) {
        await btn.click();
      } else {
        expect().assertFail();
        done();
        return;
      }
      await Utils.sleep(500);

      // 3. 读取结果区域
      const result = await driver.waitForComponent(ON.id('result_001_01'), 2000);
      if (result) {
        const text = await result.getProperty('text');
        expect(text).assertEqual('200.00vp');
      } else {
        expect().assertFail();
      }

      done();
    });
  });
}
```

### 5.3 控件 ID 使用约束

| 约束 | 说明 |
|------|------|
| **ID 必须来源于设计文档** | `ON.id('xxx')` 中的 `xxx` 必须在设计文档的控件 ID 清单附录中存在 |
| **禁止猜测 ID** | 不存在的控件 ID 会导致 `waitForComponent` 返回 null，测试必然失败 |
| **页面路由对应** | `Utils.pushPage('pages/Page001')` 中的路由必须与设计文档的页面规划一致 |
| **操作顺序对应** | UiTest 的操作步骤必须与 Demo 的操作模式（PM-XXX）一致 |

---

## 7. Step 3: 输出汇总

### 6.1 输出文件清单

```
{输出目录}/
├── TestDemo/                          # Demo 被测应用工程
│   ├── entry/src/main/ets/
│   │   ├── common/Constants.ets       # 控件 ID 定义（与设计文档一致）
│   │   ├── common/Logger.ets
│   │   ├── common/ResultDisplay.ets
│   │   ├── model/TestPoint.ets
│   │   └── pages/
│   │       ├── Index.ets              # Demo 首页
│   │       ├── Page001.ets            # 模块页
│   │       └── ...
│   └── ...
├── demo_design.md                     # Demo UI 设计文档
├── demo_code_manifest.md              # Demo 代码清单（含编译状态）
├── {Module}.test.design.md            # 设计文档（含控件ID清单附录）
├── {Module}_api.test.ets              # 非 UI 类测试代码
└── {Module}_ui.test.ets               # UI 类测试代码（UiTest）
```

---

## 8. 后续 Phase 适配

### 7.1 Phase 6: 注册测试套

- `{Module}_api.test.ets` → 注册到原测试套目录
- `{Module}_ui.test.ets` → 注册到测试套目录，**同时需将 Demo HAP 配置到 Test.json 的 kits 中**

```json
{
  "kits": [
    {
      "test-file-name": ["TestDemo.hap"],
      "type": "AppInstallKit",
      "cleanup-apps": true
    }
  ]
}
```

### 7.2 Phase 7: 格式与验证

**新增检查项**：

| 检查项 | 说明 |
|--------|------|
| 控件 ID 一致性 | 设计文档控件 ID 清单 ↔ Demo `Constants.ets` ↔ UiTest 代码 `ON.id()` 三方一致 |
| 页面路由一致性 | 设计文档页面规划 ↔ Demo `main_pages.json` ↔ UiTest `Utils.pushPage()` 三方一致 |
| Demo 编译状态 | Demo 已通过编译（检查 `demo_code_manifest.md`），未编译的 Demo 对应的 UiTest 用例标记为"待验证" |

### 7.3 Phase 8: 编译验证

- Demo 编译：已在 Step 1c 完成
- 测试代码编译：原有流程不变
- 需额外检查：UiTest 测试代码能否正确引用 Demo 的页面路由

### 7.4 Phase 9: 覆盖率验证

不变。Demo 不影响 API 覆盖率统计。

### 7.5 Phase 10: 输出结果

**扩展输出**：

```
## 生成结果

### Demo 应用
- TestDemo/（X 个页面，X 个控件）
- 编译状态：BUILD SUCCESSFUL / FAILED

### 测试代码
- {Module}_api.test.ets（X 个非 UI 用例）
- {Module}_ui.test.ets（X 个 UI 用例）

### 控件 ID 映射
- 映射表见 demo_code_manifest.md
```

---

## 9. 需要新增/修改的文件

### 8.1 新增文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `prompts/phase-5-demo-generation.md` | XTS 技能 | Step 0 + Step 1 的详细指令（分类 + Demo 生成） |
| `prompts/phase-5-uitest-generation.md` | XTS 技能 | Step 2b 的 UiTest 测试代码生成指令 |
| `modules/L2_Generation/generator/demo_testpoint_adapter.md` | XTS 技能 | .design.md → demo_test_points.md 转换规则 |
| `modules/L2_Generation/generator/uitest_templates.md` | XTS 技能 | 基于 Demo 控件 ID 的 UiTest 测试模板 |
| `references/conventions/demo_uitest_contract.md` | XTS 技能 | Demo 控件 ID 与 UiTest 的契约规范 |

### 8.2 修改文件

| 文件 | 修改内容 |
|------|---------|
| `SKILL.md` | Phase 5 描述更新为双通道生成（Demo + 测试代码），新增模块加载映射 |
| `prompts/phase-4-design.md` | UI 类用例新增控件操作序列、页面、预期 UI 结果字段；新增控件 ID 清单附录输出 |
| `prompts/phase-5-generation.md` | 重构为 Step 2a（非 UI 类）的逻辑，移除 UI 类用例生成 |
| `prompts/phase-7-validation.md` | 新增控件 ID 存在性（设计文档 vs Demo Constants.ets 一致性）、页面路由一致性检查项 |
| `prompts/phase-10-output.md` | 新增 Demo 产物输出 |

### 8.3 demo-pipeline 侧修改

| 修改内容 | 说明 |
|---------|------|
| `reference/domains.yaml` | 补充更多子系统对应的领域映射 |
| `reference/api-reference/` | 补充 API JSON 文件，与 XTS 的 `.d.ts` 覆盖范围对齐 |

---

## 10. SKILL.md 模块加载映射更新

Phase 5 的新模块加载映射：

| Phase | Always Load | Conditionally Load |
|-------|-------------|-------------------|
| 4 | `modules/L2_Generation/generator/design_doc_generator.md` | `modules/L2_Generation/generator/demo_testpoint_adapter.md`（当存在 UI 类用例时，用于生成控件ID清单附录） |
| 5 (Step 2a) | `modules/L2_Generation/generator/test_generator.md`, `templates.md`, `quality_constraints.md` | 同现有 Phase 5 |
| 5 (Step 1, Demo) | `demo-pipeline/phases/phase1_ui_design.md`, `phase2_code_generation.md`, `phase3_compile_verify.md` | `demo-pipeline/reference/api-reference/{领域}/*.json` |
| 5 (Step 2b, UiTest) | `modules/L2_Generation/generator/uitest_templates.md`, `references/conventions/uitest_framework.md`, `references/conventions/demo_uitest_contract.md` | — |

---

## 11. 批量模式适配

当 Phase 3-5 处于批量模式时：

| 批量模式行为 | 说明 |
|-------------|------|
| Step 0 分类 | 仅对当前批次 ≤10 个 API 的用例分类 |
| Step 1 Demo 生成 | 仅生成当前批次涉及的页面（增量追加到已有 Demo 工程） |
| Step 2 测试代码 | 仅生成当前批次的测试用例 |

**增量 Demo 生成约束**：
- 新页面追加到已有 `TestDemo/` 工程
- `Constants.ets` 追加新控件 ID（不覆盖已有）
- `main_pages.json` 追加新路由
- `Index.ets` 追加新导航卡片

---

## 12. 执行约束

1. **控件 ID 由设计文档定义**：控件 ID 在 Phase 4 设计文档中预定义（附录：控件 ID 清单），Demo 生成和 UiTest 代码生成均从设计文档读取，两者可并行
2. **Demo 编译通过才能使用 UiTest 代码**：若 Step 1c Demo 编译失败（且非 SDK 缺失），对应 UiTest 测试代码标记为"待 Demo 修复后补充"
3. **SDK 缺失处理**：沿用 demo-pipeline 的 SDK 缺失暂停策略，询问用户是否替换 SDK 或跳过
4. **无 UI 类用例时跳过 Demo**：若 Step 0 分类后无 UI 类用例，直接走 Step 2a，不触发 demo-pipeline
5. **Demo 编译超 5 轮失败**：回退到设计阶段重新评估 API 选型，沿用 demo-pipeline 现有策略
