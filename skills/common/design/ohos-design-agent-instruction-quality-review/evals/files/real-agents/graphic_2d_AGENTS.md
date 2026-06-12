# graphic_graphic_2d 指引

## 路径基准

本仓对应 OpenHarmony `foundation/graphic/graphic_2d`。
本文中的 `docs/`、`rosen/`、`frameworks/`、`interfaces/` 均为本仓相对路径。
构建命令从 OpenHarmony 源码根目录执行；引用本仓 GN target 时使用
`//foundation/graphic/graphic_2d/...` 前缀。

## 知识路由与快速入口

当前 `docs/knowledge/` 每个场景均有独立知识文档。
先按“领域缩略索引”确定方向，再到 `docs/knowledge/README.md` 查详细场景表、
锚点/搜索词、补读文档和知识文档沉淀规则，避免通读全部路由。

领域缩略索引：

| 触发词 | 先看领域 |
| --- | --- |
| build、GN、bundle、产品裁剪、preview、adapter | 构建/平台/接口 |
| main_thread、render_thread、drawable、modifier、animation | RS 管线/节点 |
| IPC、Parcel、Command、Stub、Proxy、fuzz、安全输入 | IPC/安全 |
| HWC、VSync、屏幕、dirty、HDR、UIFirst、layer、capture | RS 特性/设备 |
| LTPO、fps、DVSync、soft VSync、投票 | HGM |
| Canvas、Path、Bitmap、NDK Drawing、Texgine、WebGL | 2D/API/framework |
| profiler、trace、frame_report、ressched、graphic_test | 工具/测试 |

## 项目定位

本仓提供 Rosen 渲染框架、2D 绘制能力、显示刷新率管理和图形栈基础能力。
优先按这些目录定位问题：

- `rosen/modules/render_service_base/`：IPC 接口、节点/动画/属性基础类型、transaction。
- `rosen/modules/render_service/`：服务端渲染、主线程、渲染线程、硬件线程、合成。
- `rosen/modules/render_service_client/`：客户端 API、节点树、动画和 modifier 系统。
- `rosen/modules/2d_graphics/`：`Canvas`、`Paint`、`Path`、文本、图片和后端适配。
- `rosen/modules/hyper_graphic_manager/`：刷新率策略、投票、LTPO/LTPS、软 VSync。
- `frameworks/`：boot animation、text、OpenGL wrapper、Vulkan layers、surface image。
- `interfaces/`：`inner_api`、NAPI、CJ、ANI、Taihe、NDK/C API。
- `rosen/test/`、`test/`、`tools/`、`interfaces/*/test/`：单测、fuzz 和工具。

## 典型工作流

1. 先判断改动场景，按“知识路由与快速入口”读取文档、代码锚点和测试锚点。
2. 定位公开接口和内部实现边界；涉及 API 先看 `interfaces/`，再看实现和测试。
3. 涉及渲染链路时，按客户端节点树、transaction/IPC、服务端节点树、drawable、
   渲染线程、GPU/HWC 合成的顺序追踪数据流。
4. 小步修改，就近复用已有日志、错误码、智能指针、锁、线程投递和测试夹具。
5. 先判断是否可定位 OpenHarmony 源码根；单仓环境取消编译环节，只做可执行静态验证。
6. 完整源码环境按“构建和验证”选择最近构建或测试目标；
   涉及真实显示效果时补充设备验证结果。
7. 按“完成定义”输出结果。
8. 提交和 push 前按“提交和推送”要求完成检查。

## 构建和验证

构建命令只从 OpenHarmony 源码根目录执行。
若当前路径或父级没有 `build.sh` 和 `prebuilts/build-tools/`，视为单仓环境，取消编译环节，
改做 `git diff --check`、`rg` 路径/符号核对、JSON/YAML 检查或 BUILD target 引用检查；
不要伪造构建结论。

```sh
./build.sh --product-name <product-name> --build-target graphic_2d --ccache
prebuilts/build-tools/linux-x86/bin/ninja -C out/<product-name> \
  //foundation/graphic/graphic_2d/<path>:<target>
git diff --check
```

- `out/` 只代表已有产品输出；不能仅凭缺少 `out/` 判定为单仓。
- 产品名以已有 `out/`、当前任务说明、CI 或远程构建命令为准；`rk3568` 只是常见示例。
- 只改文档不构建，做路径、链接和空白检查即可。
- 代码改动优先构建最近 GN target；执行前确认 target 存在，并使用完整
  `//foundation/graphic/graphic_2d/...` 前缀。
- 构建失败先记录首个真实编译错误；需要设备、XTS 或显示效果验证时，在最终回复说明缺口。
- macOS 本地通常只做静态检查；编译、设备测试和 XTS 使用 Linux CI、远程构建机或明确设备环境。

## 项目约束

默认边界：

- 优先沿既有客户端、服务端和渲染端边界修改；确需跨层访问时，先说明理由、影响面和风险。
- 涉及 JS、NDK、CJ、ANI、Taihe 或 Native 公开行为时，同步检查相关入口，不只改单层绑定。
- 缺少真实设备时，可以继续推进实现、文档和静态验证；最终回复不得把设备行为、显示效果或
  性能功耗结论描述为已完整验证。
- 涉及公开 API/ABI、枚举、结构体、错误码或默认行为时，说明兼容性影响并先确认。
- 生成代码、OAT 扫描豁免产物、第三方依赖副本和 OpenHarmony `third_party/` 内容默认不改；
  任务明确要求时再处理。
- 破坏性 git/文件操作和大范围机械重构必须由用户明确要求。

需要先确认：

- 改公开 API/ABI、错误码、默认值、权限、XTS 预期或跨语言接口前。
- 改显示硬件接口、HWC、SurfaceBuffer、NativeBuffer、fence、刷新率模式或产品裁剪策略前。
- 改 Render Service 跨进程 IPC、transaction 编码、Parcel/TLV 格式或旧数据兼容前。
- 改第三方库、license、编译宏、feature flag、vendor extension 或跨仓接口前。

Agent 自主边界：

- “5 个文件”是同一用户任务或同一会话累计阈值，不是单个 commit 阈值；
  不得拆提交绕过。
- 可自主完成：文档、知识路由、注释、局部测试补充和单模块小修。
- 可自主推进但需说明风险：同一模块累计不超过 5 个文件，行为边界清晰且可验证。
- 单仓或缺少 OpenHarmony 根环境时，不因无法编译而默认阻塞；
  编译环节按“构建和验证”取消。
- 单仓可自主完成的静态验证包括 `git diff --check`、`rg` 路径/符号核对、JSON/YAML 校验、
  BUILD 引用检查和头文件依赖检索。
- 若远程 CI 或构建机入口已给出，按该入口验证并记录结果；未给出时不要臆造 CI 结论。
- 跨模块或跨仓变化、设备行为、性能功耗结论、公开 API/ABI 变化，必须先确认。

## 代码风格

优先使用仓库根目录 `.clang-format`。其当前 C++ 配置包含 `ColumnLimit: 120`、
`IndentWidth: 4`、`UseTab: Never` 和 include regroup/sort 规则。
NBNC、魔法数字等规则以本指引、评审和团队工具共同约束。

- 单行不得超过 120 字符；长字符串、函数调用和表格行都要拆分或压缩。
- 单个函数不超过 50 NBNC 行；NBNC 指非空白、非注释行。
- 除 0、1 和必要的 -1 错误返回外，不直接写魔法数字；使用 `constexpr` 或具名常量。
- 命名：类名使用项目既有 PascalCase 风格；其它命名复用附近文件风格。
- 成员变量：新代码优先使用尾部 `_`；遇到历史 `m` 前缀时保持局部一致，不做批量改名。
- 头文件：按 `.clang-format` 排序；能 forward declaration 的地方不要引入重依赖。
- 智能指针：IPC/RefBase 对象常用 `sptr<>`/`wptr<>`；内部所有权使用标准智能指针。
- 错误码：复用附近 `SUCCESS`、`ERR_*`、`HgmErrCode` 或模块既有返回约定。
- 线程异步：FFRT task、EventHandler 投递和回调生命周期必须说明线程归属，避免悬空捕获。
- 注释：只解释不显然的约束、生命周期、并发原因或兼容性原因，不写空泛描述。

## 提交和推送

若 Agent 负责 commit 或 push，先按 `docs/review-gates/README.md` 判定表确定需要的检视项
（含稳定性及安全边界场景），再到对应规范（如 `stability.md`）完成检视。
纯文档、注释、知识路由或格式调整等不涉及代码行为的任务不适用，需在最终回复说明不适用原因。
任一适用门禁失败或不可用时，不继续 push，等待人工确认。

以下为 Agent 提交约定，可能与历史人工提交风格不同；人工提交按团队现有规范执行。
提交建议使用 `git commit -s` 自动生成 `Signed-off-by`，
其姓名和邮箱来自 `git config user.name` 与 `git config user.email`，
格式类似 `Signed-off-by: zhangsan <zhangsan@huawei.com>`。
同时在 commit message 末尾额外空一行写入 `Co-Authored-By: Agent`：

```text
<type>(<scope>): <summary>

<body，可选>

Signed-off-by: <name> <email>

Co-Authored-By: Agent
```

没有明确项目要求时，`type` 优先使用 `fix`、`feat`、`refactor`、`test`、`docs`、`build`，
`scope` 使用模块名或目录名。
若关联 issue、缺陷单或需求单，在 body 中写清编号和影响范围。

## 完成定义

最终回复按任务复杂度收口，不机械打印固定清单。
不适用的构建、XTS、设备、提交项可以省略，避免把简单任务回复拉长。

轻量任务，如问答、文档删节、措辞调整或路径核对：

- 简要说明结论或改动点。
- 说明已做的静态检查；未验证时用一句话说明原因。
- 只改 1 到 2 个文档时，不必逐条展开未修改文件、XTS、设备和提交状态。

代码、接口、构建、设备或跨模块任务：

- 说明读取过的知识文档、修改文件、行为影响面和关键未改文件。
- 列出已执行的构建、单测、fuzz、XTS 或真实设备验证命令；未执行时说明原因。
- XTS 目标或真实设备验证无法确认时，列出缺口和需要人工确认的问题。
- 说明本次自主边界级别和累计改动文件数。
- 当前为单仓环境时，说明取消编译的原因和替代静态检查；
  完整 OpenHarmony 根环境时，说明使用的产品和 target。
- 涉及提交或 push 时，说明适用门禁（按 `docs/review-gates/README.md` 判定）的检视结果，
  以及 commit message 是否符合提交约定。
