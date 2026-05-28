# 模式一：生成 IDL 化 SA 框架代码

## 交互式信息收集

**核心原则：所有必填字段必须由用户明确提供，禁止使用默认值或占位值。**

SA 代码生成的必填字段清单（共 10 项）：

| # | 字段 | 变量名 | 格式要求 | 示例 |
|---|------|--------|----------|------|
| 1 | SA 类名 | `{SaName}` | PascalCase | `ListenAbility` |
| 2 | SA ID | `{SA_ID}` | 纯数字，需申请分配 | `1499` |
| 3 | 进程名 | `{process_name}` | 小写下划线 | `listen_test` |
| 4 | 子系统名 | `{subsystem_name}` | 小写 | `systemabilitymgr` |
| 5 | 部件名 | `{part_name}` | 小写下划线 | `safwk` |
| 6 | 启动方式 | `{runOnCreate}` | true/false | `false` |
| 7 | 分布式支持 | `{distributed}` | true/false | `false` |
| 8 | HiLog domain | `{log_domain}` | 格式 `0xD00XXXX` | `0xD003F00` |
| 9 | 接口方法 | — | C++ 方法签名列表 | `int32_t AddVolume(int32_t volume);` |
| 10 | 代码生成路径 | — | 目录路径 | `./demo-sa` |

### 信息收集流程

**首轮提问：一次性请求用户提供所有必填信息**

```
question: "请提供以下 SA 必填信息（可一次性提供多项，未提供的字段将逐一追问）：
  1. SA 类名（PascalCase，如 ListenAbility）
  2. SA ID（纯数字，需向系统服务管理责任田同事申请分配）
  3. SA 运行进程名（如 listen_test）
  4. 所属子系统名（如 systemabilitymgr）
  5. 所属部件名（如 safwk）
  6. 启动方式：true（常驻启动）或 false（按需启动）
  7. 是否支持分布式：true 或 false
  8. HiLog domain（格式 0xD00XXXX，如 0xD003F00）
  9. 接口方法签名列表（如 int32_t AddVolume(int32_t volume);）
  10. 代码生成目标路径"
header: "SA 必填信息"
```

**用户回答后，逐一校验缺失字段并追问：**

对用户未提供的每个必填字段，使用 `question` 工具逐项追问。**不使用任何默认值或占位值填充。** 每个追问必须说明字段用途，帮助用户理解其重要性。

```
# SA ID 缺失时
question: "SA ID 是 SA 注册的唯一标识，需向系统服务管理责任田同事申请分配。
  请提供已分配的 SA ID（纯数字，如 1499）。如果尚未申请，请先完成 SA ID 申请。"
header: "SA ID（必填）"

# 进程名缺失时
question: "请提供 SA 运行的进程名（如 listen_test）。该进程名用于 CFG 配置和 SA Profile。"
header: "进程名（必填）"

# 子系统名缺失时
question: "请提供 SA 所属子系统名（如 systemabilitymgr）。用于 BUILD.gn 和 SA Profile 配置。"
header: "子系统名（必填）"

# 部件名缺失时
question: "请提供 SA 所属部件名（如 safwk）。用于 BUILD.gn 和 SA Profile 配置。"
header: "部件名（必填）"

# 启动方式缺失时
question: "请选择 SA 启动方式"
header: "启动方式（必填）"
options:
  - label: "true（常驻启动）"
    description: "进程启动时即创建 SA，CFG 中 ondemand 为 false"
  - label: "false（按需启动）"
    description: "首次访问时才创建 SA，CFG 中 ondemand 为 true"

# 分布式支持缺失时
question: "请选择 SA 是否支持分布式"
header: "分布式支持（必填）"
options:
  - label: "false（不支持）"
    description: "SA 仅在本地设备运行"
  - label: "true（支持）"
    description: "SA 支持跨设备分布式调用"

# HiLog domain 缺失时
question: "请提供 HiLog domain ID（格式 0xD00XXXX，如 0xD003F00）。
  该 ID 用于 SA 日志输出，需确保不与已有 SA 的 domain 冲突。"
header: "HiLog domain（必填）"

# 接口方法缺失时
question: "请提供 SA 对外暴露的接口方法签名列表。格式示例：
  int32_t AddVolume(int32_t volume);
  int32_t GetData(int32_t input, double& output);
  void SetStatus(bool status);"
header: "接口方法（必填）"

# 代码生成路径缺失时
question: "请提供代码生成的目标目录路径（如 ./demo-sa）"
header: "生成路径（必填）"
```

### 信息完整性校验

**生成代码前，必须确认全部 10 项必填字段已收集完毕。** 校验规则：

1. 逐项检查必填字段清单，确认每项非空、非占位值
2. SA ID 必须为正整数（> 0），不接受 0 或负数
3. SA 类名必须符合 PascalCase 格式
4. HiLog domain 必须符合 `0xD00XXXX` 格式
5. 接口方法签名必须至少包含一个方法
6. 如果有任何字段缺失或格式不正确，**不允许开始代码生成**，继续追问直到信息完整

```
# 校验不通过时
"以下必填信息尚未提供：[列出缺失字段]。请补充后将继续代码生成。"
```

## 信息收集完成后：生成代码

**必须先 Read `references/idl-sa-templates.md`**，然后根据用户提供的变量做替换，严格遵循模板的结构和风格生成代码。不要凭记忆生成。

**CFG ondemand 规则**：当 `runOnCreate=true` 时，`ondemand=false`；当 `runOnCreate=false` 时，`ondemand=true`。

## 生成完成后的提示

告诉用户：
1. 列出所有生成的文件及其用途
2. 标记需要手动补充的 TODO 项（接口方法实现逻辑）
3. 提醒需要在子系统根 BUILD.gn 中添加 `{sa_name}` 编译依赖
4. 提醒 SA ID 需要上库（修改 `system_ability_definition.h` 和 `dump_utils.cpp`）
5. 提醒 Selinux 规则需要配置
