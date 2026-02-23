# HarmonyOS 自动化测试 Skill

将自然语言测试需求转换为可执行的 Hypium 测试用例，实现 HarmonyOS 应用的自动化测试。

## 功能特性

- **自然语言转代码**: 将中文测试步骤自动转换为 Hypium Python 测试代码
- **逐步调试**: 严格的单步调试机制，确保每一步都经过验证
- **智能控件定位**: 优先使用控件定位器（text/type/key），坐标定位作为备选方案
- **自动环境检测**: 检测 HDC、Hypium、设备连接状态
- **控件树分析**: 自动导出和分析设备控件树
- **AI 视觉识别**: 当控件树无法定位时，支持截图 + AI 分析
- **完整测试报告**: 生成 HTML/XML/JSON 格式的测试报告

## 前置要求

- **HDC 工具**: 已安装并配置到 PATH
- **Hypium 框架**: 版本 >= 6.0.7.210
- **HarmonyOS 设备**: 已通过 USB 连接并授权调试

安装 Hypium:
```bash
pip3 install hypium
```

## 快速开始

### 基本用法

创建一个包含测试步骤的 Markdown 文件，然后调用 skill:

```bash
/harmonyos-autotest @your_test_steps.md
```

### 示例：设置显示和亮度测试

**输入文件** (`test.md`):

```markdown
## 操作步骤
1.打开设置；
2.搜索"显示和亮度"，点击搜索；
3.并打开搜索到的"显示和亮度"页面；
4.将"显示模式"调整成"深色"；
5.将"自动调节"上方的滑动条向右滑动至最大；
6.将"自动调节"右侧的按钮关闭；
7.向下滑动屏幕，将屏幕滑到底部；
```

**执行命令**:
```bash
/harmonyos-autotest @test.md
```

**生成的测试代码** (`Example.py`):

```python
#!/usr/bin/env python
# coding: utf-8
from devicetest.core.test_case import TestCase, Step
from hypium import *
from hypium.model.basic_data_type import UiParam
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
        Step('2.打开设置')
        self.driver.start_app(package_name="com.huawei.hmos.settings")
        time.sleep(3)

        Step('3.点击搜索输入框')
        self.driver.touch(BY.key("__SearchField__homPageSearchInput"))
        time.sleep(3)

        Step('4.输入搜索内容')
        self.driver.input_text(BY.type("SearchField"), "显示和亮度")
        time.sleep(3)

        Step('5.按回车执行搜索')
        self.driver.press_key(KeyCode.ENTER)
        time.sleep(3)

        Step('6.点击搜索结果')
        self.driver.touch((721, 481))
        time.sleep(3)

        Step('7.选择深色模式')
        self.driver.touch(BY.text("深色, tab_unlock"))
        time.sleep(3)

        Step('8.滑动亮度条至最大')
        self.driver.slide((200, 2103), (1100, 2103))
        time.sleep(3)

        Step('9.关闭自动调节开关')
        self.driver.touch(BY.key("automatic_adjust_toggle"))
        time.sleep(3)

        Step('10.向下滑动屏幕到底部')
        self.driver.swipe(UiParam.UP, distance=80)
        time.sleep(3)

    def teardown(self):
        Step('11.清理环境')
        self.driver.stop_app("com.huawei.hmos.settings")
```

## 工作流程

```
用户输入自然语言测试需求
         │
         ▼
┌─────────────────────┐
│  1. 创建项目目录     │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  2. 步骤解析         │  解析测试步骤为 JSON
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  3. 环境检测         │  HDC/Hypium/设备
└─────────────────────┘
         │ (失败则终止)
         ▼
┌─────────────────────┐
│  4. 创建测试工程     │
└─────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│              5. 循环: 对每个测试步骤 (逐步调试)               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ a. 控件解析: 导出控件树，定位目标控件                   │  │
│  │ b. 编写代码: 生成测试代码                               │  │
│  │ c. 执行调试: 运行测试工程                               │  │
│  │ d. 人为确认: 等待用户确认步骤执行正确                   │  │
│  │ e. 注释代码: 将已确认的步骤代码注释掉                   │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│  6. 端到端测试       │  执行完整测试
└─────────────────────┘
         │
         ▼
    输出测试报告
```

## 项目结构

生成的测试项目结构:

```
projects/{app}_{feature}_{timestamp}/
├── config/
│   └── user_config.xml          # 设备和环境配置
├── testcases/
│   ├── Example.py               # 测试用例 Python 文件
│   └── Example.json             # 测试用例配置文件
├── aw/
│   └── Utils.py                 # 工具函数
├── resource/
│   └── images/                  # 图片资源
├── output/
│   ├── controls/                # 控件树快照
│   ├── screenshots/             # 测试截图
│   ├── reports/                 # 测试报告
│   ├── logs/                    # 测试日志
│   └── temp/                    # 临时文件
├── main.py                      # 测试入口
└── requirements.txt             # Python 依赖
```

## 支持的操作

| 操作类型 | 关键词 | 示例 |
|---------|--------|------|
| 点击 | 点击、单击、按下 | `点击"确定"按钮` |
| 输入 | 输入、填写、设置 | `输入"Hello"` |
| 滑动 | 滑动、滚动、拖动 | `向下滑动屏幕` |
| 长按 | 长按 | `长按图标` |
| 双击 | 双击 | `双击图片` |
| 按键 | 按键 | `按回车` |

## 常见应用包名

| 应用 | 包名 |
|------|------|
| 设置 | com.huawei.hmos.settings |
| 今日头条 | com.ss.android.article.news |
| 微信 | com.tencent.mm |
| 美团 | com.sankuai.hmeituan |
| 滴滴出行 | com.sdu.didi.hmos.psnger |

## 控件定位优先级

```
1. BY.text("文本")      # 优先使用
2. BY.key("key值")
3. BY.id("id值")
4. BY.type("类型")
5. 坐标 (x, y)          # 备选方案
```

## 搜索操作规范

搜索操作必须按照三步流程执行:

```
1. 点击搜索输入框 (触发键盘)
2. 输入搜索内容
3. 点击搜索按钮或按回车
```

## 调试原则

1. **每次只调试一个步骤**
2. **已确认的步骤必须注释**
3. **后续步骤必须注释**
4. **调试期间注释 setup/teardown**
5. **端到端测试前恢复所有注释**

## 输出示例

```json
{
  "success": true,
  "test_name": "设置_显示和亮度测试",
  "project_path": "./projects/settings_display_brightness_20260223_170221",
  "testcase_path": "./projects/.../testcases/Example.py",
  "execution_summary": {
    "total_steps": 10,
    "passed": 10,
    "failed": 0
  },
  "report_path": "./projects/.../reports/summary_report.html"
}
```

## Skill 文件结构

```
harmonyos-autotest/
├── SKILL.md                     # [核心] Skill 定义文件，包含完整的工作流程和规则
├── README.md                    # 本文档
│
├── assets/                      # 资源文件
│   └── HypiumProjectTemplate/   # Hypium 测试项目模板
│       ├── config/
│       │   └── user_config.xml      # 设备配置模板
│       ├── testcases/
│       │   ├── Example.py           # 测试用例模板
│       │   └── Example.json         # 测试配置模板
│       ├── aw/
│       │   └── Utils.py             # 工具函数模板
│       ├── resource/images/         # 图片资源目录
│       └── main.py                  # 测试入口模板
│
├── references/                  # 参考文档（Agent 执行时读取）
│   ├── step-parser.md           # 步骤解析：将自然语言转为 JSON
│   ├── control-parser.md        # 控件解析：导出和分析控件树
│   ├── environment.md           # 环境检测：HDC/Hypium/设备状态
│   ├── operation.md             # 操作执行：UI 操作 API 用法
│   ├── debug.md                 # 调试指南：单步调试和错误处理
│   ├── testcase-writer.md       # 用例编写：生成测试代码规范
│   ├── control-visual-guide.md  # 控件识别：无文字控件的视觉识别
│   ├── project-template.md      # 项目模板：Hypium 项目结构说明
│   ├── hypium_api.md            # API 参考：完整 Hypium API 文档
│   └── hypium测试工程指导.pdf    # 官方工程指导文档
│
└── scripts/                     # 辅助脚本
    ├── create_project.py        # 创建新的测试项目
    ├── check_environment.py     # 检测环境是否就绪
    ├── dump_controls.py         # 导出设备控件树
    └── run_test.py              # 运行测试用例
```

### 核心文件说明

#### SKILL.md
Skill 的核心定义文件，包含：
- 完整的工作流程（6 个步骤）
- 核心原则（严格单步调试）
- 搜索操作规范（三步流程）
- 控件定位优先级
- 测试代码示例
- 常见应用包名

#### references/ 参考文档

| 文件 | 用途 | 使用时机 |
|------|------|---------|
| `step-parser.md` | 解析自然语言测试步骤为 JSON 格式 | 步骤 2: 步骤解析 |
| `control-parser.md` | 导出控件树、定位目标控件 | 步骤 5a: 控件解析 |
| `environment.md` | 检测 HDC、Hypium、设备状态 | 步骤 3: 环境检测 |
| `operation.md` | UI 操作 API 使用方法 | 步骤 5b: 编写代码 |
| `debug.md` | 单步调试流程、错误分类、修正策略 | 步骤 5c: 执行调试 |
| `testcase-writer.md` | 生成测试用例代码规范 | 步骤 5b: 编写代码 |
| `control-visual-guide.md` | 点赞、收藏、分享等无文字控件识别 | 控件树无法定位时 |
| `project-template.md` | Hypium 项目结构和配置说明 | 步骤 4: 创建工程 |
| `hypium_api.md` | 完整的 Hypium API 参考 | 查询 API 用法 |

#### scripts/ 辅助脚本

| 脚本 | 用法 | 说明 |
|------|------|------|
| `create_project.py` | `python create_project.py <app> <feature>` | 创建测试项目目录结构 |
| `check_environment.py` | `python check_environment.py` | 检测 HDC/Hypium/设备状态 |
| `dump_controls.py` | `python dump_controls.py [output_dir]` | 导出当前页面控件树 |
| `run_test.py` | `python run_test.py [test_name]` | 运行指定测试用例 |

#### assets/HypiumProjectTemplate/ 项目模板

用于快速创建新的测试项目，包含：
- `config/user_config.xml` - 设备和环境配置
- `testcases/Example.py` - 测试用例模板
- `testcases/Example.json` - 测试配置模板
- `aw/Utils.py` - 常用工具函数
- `main.py` - 测试入口文件

### Agent 执行流程与文件读取

Agent 在执行测试时会按以下顺序读取参考文档：

```
步骤 2: 步骤解析
  └── 读取 references/step-parser.md

步骤 3: 环境检测
  └── 读取 references/environment.md

步骤 4: 创建测试工程
  └── 读取 references/project-template.md

步骤 5: 逐步调试（每个步骤）
  ├── 读取 references/control-parser.md  (控件解析)
  ├── 读取 references/debug.md           (修正策略)
  ├── 读取 references/testcase-writer.md (编写代码)
  └── 读取 references/operation.md       (API 用法)
```

## 注意事项

- 每个操作后都会自动添加 `time.sleep(3)` 等待
- 启动应用后必须等待 3 秒
- 控件定位优先使用 `BY.text()`、`BY.type()`、`BY.key()`
- 坐标定位是备选方案，仅在控件无可用属性时使用
- 支持中英文混合输入

## 许可证

MIT License
