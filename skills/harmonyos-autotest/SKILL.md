---
name: harmonyos-autotest
description: Complete HarmonyOS automated testing workflow orchestrator. Converts natural language test requirements to executable Hypium test cases through step parsing, environment checking, project creation, control parsing, operation execution, debugging, and test case writing. Use when user wants to run complete automated test workflow, create HarmonyOS test projects, or mentions HarmonyOS测试, 自动化测试, run test, execute test. Trigger keywords: harmonyos test, 自动化测试, run test, test workflow, 完整测试流程, hypium, 创建测试工程.
---

# HarmonyOS 自动化测试

协调完整的 HarmonyOS 自动化测试工作流程，将自然语言测试需求转换为可执行的 Hypium 测试用例。

## 核心原则：严格单步调试

> **绝对禁止将多个步骤合并调试！每次只调试一个步骤！**

1. **已确认通过的步骤**：必须**全部注释**
2. **当前调试的步骤**：**只有一个未注释**
3. **后续待调试步骤**：必须**全部注释**
4. **调试期间注释 setup/teardown**：调试过程中必须**注释掉 setup 和 teardown 函数**，否则每次调试都会回到桌面和关闭应用，导致无法连续调试
5. **端到端测试前恢复**：所有步骤调试完成后，**先取消 setup/teardown 的注释，再取消所有步骤的注释**，然后执行端到端测试

## ⚠️ 搜索操作规范（必须遵守）

> **搜索操作必须严格按照三步流程执行！禁止直接点击搜索按钮！**

### 搜索操作的正确流程

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: 点击搜索输入框                                      │
│  - 目的：触发输入框获取焦点，显示键盘                          │
│  - 控件类型：SearchField、TextInput、TextField               │
│  - 定位方式：BY.type("SearchField") 或 BY.key("search_*")    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 2: 输入搜索内容                                        │
│  - 使用 input_text_on_current_cursor() 或 input_text()       │
│  - 等待输入完成                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 3: 点击搜索按钮或按回车执行搜索                         │
│  - 点击搜索按钮：BY.text("搜索")                              │
│  - 或按回车：KeyCode.ENTER                                    │
└─────────────────────────────────────────────────────────────┘
```

### 错误示例 ❌

```python
# 错误：直接点击搜索按钮，没有先点击输入框
self.driver.touch(BY.text("搜索"))  # ❌ 输入框没有焦点，无法输入
self.driver.input_text("周黑鸭")    # ❌ 输入失败
```

### 正确示例 ✅

```python
# 正确：先点击输入框，再输入，最后搜索
self.driver.touch(BY.type("SearchField"))  # ✅ 点击输入框获取焦点
time.sleep(3)
self.driver.input_text_on_current_cursor("周黑鸭")  # ✅ 输入内容
time.sleep(3)
self.driver.press_key(KeyCode.ENTER)  # ✅ 按回车搜索
```

### 搜索输入框识别要点

| 控件类型 | 说明 | 定位方式 |
|---------|------|---------|
| SearchField | 专用搜索输入框 | `BY.type("SearchField")` |
| TextInput | 通用文本输入框 | `BY.type("TextInput")` |
| TextField | 文本字段 | `BY.type("TextField")` |
| 带提示文字的输入框 | 显示"请输入"、"搜索"等提示 | 通过坐标定位 |

**注意**：搜索输入框通常**没有明显的"搜索"文本**，需要通过类型（type）或key来识别！

## ⚠️ 控件定位优先级（必须遵守）

> **优先使用控件定位器，坐标定位是备选方案！**

### 控件定位的优先级顺序

```
┌─────────────────────────────────────────────────────────────┐
│  优先级 1: BY.text() - 通过文本内容定位                      │
│  适用于：按钮、菜单项、标签等有明确文字的控件                 │
│  示例：BY.text("确定"), BY.text("设置")                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  优先级 2: BY.type() - 通过控件类型定位                      │
│  适用于：特定类型的控件（按钮、输入框、开关等）               │
│  示例：BY.type("Button"), BY.type("Toggle"), BY.type("Slider")│
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  优先级 3: BY.key() - 通过控件key属性定位                    │
│  适用于：有唯一key标识的控件                                  │
│  示例：BY.key("search_input"), BY.key("btn_submit")          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  优先级 4: BY.id() - 通过控件id定位                          │
│  适用于：有唯一id的控件                                       │
│  示例：BY.id("com.example:id/button")                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  优先级 5: 组合定位器 - 多属性组合                           │
│  适用于：单一属性无法唯一确定时                               │
│  示例：BY.text("确定").type("Button")                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  备选方案: 坐标定位 touch((x, y))                            │
│  仅在以下情况使用：                                           │
│  - 控件树中无法找到任何可用的定位属性                         │
│  - 控件是纯图形/图标，无文字、type、key等属性                 │
│  - 控件定位器反复失败后的最后手段                             │
└─────────────────────────────────────────────────────────────┘
```

### 为什么优先使用控件定位器？

| 优势 | 说明 |
|------|------|
| **稳定性** | 控件属性通常不会因屏幕分辨率变化而改变 |
| **可维护性** | 代码更易读，`BY.text("确定")` 比 `(658, 483)` 更易理解 |
| **适应性** | 自动适应不同设备尺寸和布局变化 |
| **调试性** | 失败时错误信息更明确 |

### 错误示例 ❌

```python
# 错误：优先使用坐标
self.driver.touch((658, 483))  # ❌ 代码不可读，不稳定

# 错误：控件有text属性却用坐标
# 控件树显示: type="Button", text="确定", clickable=true
self.driver.touch((577, 227))  # ❌ 应该用 BY.text("确定")
```

### 正确示例 ✅

```python
# 正确：优先使用控件定位器
self.driver.touch(BY.text("确定"))           # ✅ 通过文本定位
self.driver.touch(BY.type("Toggle"))         # ✅ 通过类型定位
self.driver.touch(BY.key("btn_submit"))      # ✅ 通过key定位

# 仅在无法找到定位属性时才使用坐标
# 控件树显示: type="Image", text="", key="", clickable=true
self.driver.touch((658, 483))  # ✅ 纯图标控件，无可用属性，坐标是备选
```

### 控件树分析要点

分析控件树时，**必须首先记录以下属性**：

1. **text**: 控件显示的文本内容
2. **type**: 控件类型（Button, Toggle, Slider, Text, Image等）
3. **key**: 控件的key属性
4. **id**: 控件的id属性
5. **clickable**: 是否可点击

只有当以上属性都无法用于定位时，才记录 **center坐标** 作为备选。

## 工作流程

```
用户输入自然语言测试需求
         │
         ▼
┌─────────────────────┐
│  1. 创建项目目录     │  创建统一的项目根目录
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  2. 步骤解析         │  解析测试步骤为 JSON，参考references/step-parser.md
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  3. 环境检测         │  检测环境是否就绪，参考references/environment.md
└─────────────────────┘
         │ (失败则终止)
         ▼
┌─────────────────────┐
│  4. 创建测试工程     │  创建测试项目结构，参考references/project-template.md
└─────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│              5. 循环: 对每个测试步骤 (逐步调试)               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ⚠️ 每步必须先读取对应参考文档！                        │  │
│  │                                                        │  │
│  │ a. 控件解析:                                           │  │
│  │    ① 读取 references/control-parser.md                 │  │
│  │    ② 读取 references/debug.md (修正策略)               │  │
│  │    ③ 导出控件树，**优先查找控件的text/type/key属性**   │  │
│  │    ④ **仅在无可用属性时**才使用坐标作为备选            │  │
│  │    ⑤ 若控件树完全无法定位 → 截图 + AI分析              │  │
│  │                                                        │  │
│  │ b. 编写代码:                                           │  │
│  │    ① 读取 references/testcase-writer.md                │  │
│  │    ② 读取 references/operation.md (API用法)            │  │
│  │    ③ 结合操作方式编写测试代码                          │  │
│  │                                                        │  │
│  │ c. 执行调试: 运行测试工程，验证当前步骤是否成功        │  │
│  │ d. 人为确认: 等待用户确认步骤执行正确                  │  │
│  │ e. 注释代码: 将已确认的步骤代码注释掉                  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│  6. 端到端测试       │  去掉注释，执行完整测试
└─────────────────────┘
         │
         ▼
    输出测试报告
```

## 可用脚本

| 脚本 | 用法 | 说明 |
|------|------|------|
| `scripts/create_project.py` | `python create_project.py <app> <feature>` | 创建测试项目 |
| `scripts/check_environment.py` | `python check_environment.py` | 检测环境状态 |
| `scripts/dump_controls.py` | `python dump_controls.py [output_dir]` | 导出控件树 |
| `scripts/run_test.py` | `python run_test.py [test_name]` | 运行测试用例 |

## 详细指南

| 功能 | 文档 | 说明 |
|------|------|------|
| 步骤解析 | [step-parser.md](references/step-parser.md) | 解析自然语言为JSON格式 |
| 控件解析 | [control-parser.md](references/control-parser.md) | 导出和分析控件树 |
| 环境检测 | [environment.md](references/environment.md) | 检测HDC/Hypium/设备状态 |
| 操作执行 | [operation.md](references/operation.md) | UI操作API使用 |
| 调试指南 | [debug.md](references/debug.md) | 单步调试和错误分析 |
| 用例编写 | [testcase-writer.md](references/testcase-writer.md) | 生成测试用例代码 |
| 控件识别 | [control-visual-guide.md](references/control-visual-guide.md) | 无文字控件视觉识别 |
| 项目模板 | [project-template.md](references/project-template.md) | Hypium项目结构 |
| API文档 | [hypium_api.md](references/hypium_api.md) | 完整Hypium API参考 |
| 工程指导 | [hypium测试工程指导.pdf](references/hypium测试工程指导.pdf) | 官方Hypium工程指导 |

## 执行步骤

### 1. 创建项目目录

在当前工作目录下创建 projects 根目录和项目：

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROJECT_NAME="{app_name}_{test_feature}_${TIMESTAMP}"
PROJECT_ROOT="./projects/${PROJECT_NAME}"

mkdir -p "${PROJECT_ROOT}"/{config,testcases,aw,resource/images,output/{controls,screenshots,reports,logs,temp}}
export HARMONYOS_PROJECT_ROOT="$(cd ${PROJECT_ROOT} && pwd)"
```

### 2. 步骤解析

> ⚠️ **必须先读取 [references/step-parser.md](references/step-parser.md)**

将自然语言测试步骤解析为结构化JSON。

### 3. 环境检测

> ⚠️ **必须先读取 [references/environment.md](references/environment.md)**

检测 HDC、Hypium、设备连接状态。

### 4. 创建测试工程

> ⚠️ **必须先读取 [references/project-template.md](references/project-template.md)**

基于模板创建测试项目。

### 5. 逐步调试

> ⚠️ **每步调试前必须先读取对应参考文档！**
>
> - 控件解析: 读取 `references/control-parser.md` 和 `references/debug.md`
> - 编写代码: 读取 `references/testcase-writer.md` 和 `references/operation.md`
> - 控件树无法定位时: 使用截图+AI分析 (见 `references/debug.md` 策略3)

对每个测试步骤执行调试循环：

```bash
# 进入项目目录
cd {PROJECT_ROOT}

# 执行测试
xdevice run -l Example -ta agent_mode:bin;screenshot:true
```

### 6. 端到端测试

```bash
# 强制关闭应用
hdc shell aa force-stop {package_name}

# 去掉所有注释

# 执行完整测试
xdevice run -l Example -ta agent_mode:bin
```

## 测试代码示例

### 调试期间的状态（setup/teardown 已注释）

```python
from devicetest.core.test_case import TestCase, Step
from hypium import *
import time


class Example(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        TestCase.__init__(self, self.TAG, controllers)
        self.driver = UiDriver(self.device1)

    # 调试期间注释掉 setup，避免每次回到桌面
    # def setup(self):
    #     Step('1.回到桌面')
    #     self.driver.swipe_to_home()
    #     time.sleep(3)

    def process(self):
        # Step 1: 启动应用（已确认，注释掉）
        # Step('1.启动应用')
        # self.driver.start_app(package_name="com.example.app")
        # time.sleep(3)

        # Step 2: 点击按钮（当前调试步骤，未注释）
        Step('2.点击按钮')
        self.driver.touch(BY.text("按钮"))
        time.sleep(3)

        # Step 3: 后续步骤（全部注释）
        # Step('3.输入文本')
        # self.driver.input_text("测试内容")
        # time.sleep(3)

    # 调试期间注释掉 teardown，避免每次关闭应用
    # def teardown(self):
    #     Step('4.清理环境')
    #     self.driver.stop_app("com.example.app")
```

### 端到端测试前的状态（所有注释已取消）

```python
from devicetest.core.test_case import TestCase, Step
from hypium import *
import time


class Example(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        TestCase.__init__(self, self.TAG, controllers)
        self.driver = UiDriver(self.device1)

    def setup(self):
        Step('1.回到桌面')
        self.driver.swipe_to_home()
        time.sleep(3)

    def process(self):
        Step('2.启动应用')
        self.driver.start_app(package_name="com.example.app")
        time.sleep(3)  # 启动后必须等待3秒

        Step('3.点击按钮')
        self.driver.touch(BY.text("按钮"))
        time.sleep(3)

    def teardown(self):
        Step('4.清理环境')
        self.driver.stop_app("com.example.app")
```

## 常见应用包名

| 应用 | 包名 |
|------|------|
| 设置 | com.huawei.hmos.settings |
| 今日头条 | com.ss.android.article.news |
| 微信 | com.tencent.mm |
| 美团 | com.sankuai.hmeituan |
| 滴滴出行 | com.sdu.didi.hmos.psnger |

## 输出结果

```json
{
  "success": true,
  "test_name": "测试名称",
  "project_path": "{PROJECT_ROOT}",
  "testcase_path": "{PROJECT_ROOT}/testcases/Example.py",
  "execution_summary": {
    "total_steps": 5,
    "passed": 5,
    "failed": 0
  },
  "report_path": "{PROJECT_ROOT}/output/reports/test_report.md"
}
```

## 使用示例

### 示例 1: 完整测试流程（逐步调试）

**用户输入**:
```
测试设置显示和亮度功能：
1. 启动设置
2. 点击搜索框
3. 输入"显示和亮度"
4. 点击搜索结果
5. 设置深色模式
```

**Agent 执行**:
```
1. 创建项目目录
2. 解析测试步骤为 JSON
3. 检测环境
4. 创建测试工程

=== 开始逐步调试 ===

--- 步骤 1: 启动设置应用 ---
[直接执行] driver.start_app(package_name="com.huawei.hmos.settings")
[debug] 执行测试... 成功

请确认: 应用是否正确启动？(ok/失败)
> ok

[注释步骤 1 代码]

--- 步骤 2: 点击搜索框 ---
[control-parser] 导出设置页控件树
[testcase-writer] 编写点击搜索框代码
[debug] 执行测试... 成功

请确认: 搜索框是否被点击？(ok/失败)
> ok

[注释步骤 2 代码]

... (继续步骤 3-5)

=== 所有步骤调试完成 ===

=== 端到端测试 ===
[强制关闭应用] hdc shell aa force-stop com.huawei.hmos.settings
[去掉所有注释]
[执行完整测试]
[生成测试报告]
```

### 示例 2: 调试失败重新尝试

```
--- 步骤 3: 输入搜索词 ---
[control-parser] 导出控件树
[testcase-writer] 编写输入代码
[debug] 执行测试... 失败: 控件未找到

[debug] 分析: 定位器 BY.key('search_input') 未找到
[debug] 尝试备用定位器: BY.type('SearchField')
[testcase-writer] 更新代码
[debug] 重新执行... 成功

请确认: 是否正确输入了搜索词？(ok/失败)
```

## 配置

默认配置:
```yaml
# ~/.harmonyos-test/config.yaml
defaults:
  device_sn: auto  # 自动选择第一个设备
  timeout: 30000   # 默认超时 30 秒
  retry: 2         # 失败重试 2 次
  output_dir: ./output

apps:
  settings: com.huawei.hmos.settings
  toutiao: com.ss.android.article.news
  wechat: com.tencent.mm
  meituan: com.sankuai.hmeituan
```

## 注意事项

- **逐步调试**: 每步都需要人为确认后才能继续
- **注释机制**: 已确认的步骤会被注释，确保下次只执行新步骤
- **调试期间注释 setup/teardown**: 调试过程中必须注释掉 setup 和 teardown 函数，否则每次调试都会回到桌面和关闭应用，无法连续调试
- **端到端测试前恢复**: 所有步骤调试完成后，先取消 setup/teardown 的注释，再取消所有步骤的注释
- **执行调试前必须进入项目目录**: 每次运行 `xdevice` 前，必须先 `cd {PROJECT_ROOT}`
- **端到端测试前必须关闭应用**: 使用 `hdc shell aa force-stop {package_name}` 强制关闭应用
- **启动应用优化**: 启动应用步骤直接使用 `driver.start_app()`，不需要导出控件树
- **⚠️ 控件定位优先级**: **优先使用 `BY.text()`, `BY.type()`, `BY.key()` 等控件定位器**，坐标 `touch((x,y))` 是备选方案，仅在控件无可用属性时使用
- **⚠️ 搜索操作必须三步走**: 1.先点击搜索输入框 → 2.输入内容 → 3.点击搜索按钮或回车。**禁止直接点击搜索按钮！**
- **搜索输入框识别**: 通过 `BY.type("SearchField/TextInput")` 或 `BY.key()` 定位，不要用 `BY.text("搜索")`
- 支持中英文混合输入
- 自动处理控件定位失败
- 沉淀调试规则供后续使用
