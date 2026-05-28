# SA 开发专家判断与反模式

## IDL 化 vs 非IDL 化 选择标准

| 维度 | IDL 化（推荐） | 非IDL 化 |
|------|---------------|----------|
| 代码量 | 少，Proxy/Stub 自动生成 | 多，手写序列化/反序列化 |
| 出错概率 | 低，工具保证一致性 | 高，手写容易漏字段或顺序错误 |
| 维护成本 | 低，新增接口只改 .idl | 高，需同步改接口/Proxy/Stub 三处 |
| 适用场景 | 新 SA 开发、长期维护的 SA | 历史遗留 SA、有特殊序列化需求 |
| 性能差异 | 无实质差异 | 无实质差异 |

**默认推荐 IDL 化**。仅当存在以下情况时考虑非IDL：
- 需要兼容已有二进制接口（无法改 IDL 重新生成）
- 需要自定义序列化逻辑（如自定义Parcel读写）
- 迁移过程中作为中间态

## NEVER 列表（绝对禁止）

### 代码生成

- **NEVER** 对必填字段使用默认值或占位值（如 SA ID = 0、进程名 = "placeholder"）
- **NEVER** 在未读取模板文件的情况下凭记忆生成代码
- **NEVER** 跳过信息完整性校验直接生成代码
- **NEVER** 修改模板的结构和模式，只做变量替换

### IPC 安全

- **NEVER** 在 Stub 中不校验 `ReadInterfaceToken` 就处理请求
- **NEVER** 忽略 `MessageParcel::Read*` 的返回值——每个参数读取前必须校验成功
- **NEVER** 在 Proxy 中不检查 `Remote()` 是否为 nullptr
- **NEVER** 在 Proxy 中不检查 `SendRequest` 返回值

### SA 注册

- **NEVER** 在 `OnStart` 中执行耗时操作（影响同进程其他 SA 启动）
- **NEVER** 在构造函数中执行耗时操作（影响 dlopen 耗时）
- **NEVER** 在 `Publish(this)` 之前执行需要 SA 已可用的操作
- **NEVER** 在 App 进程中注册 SA（仅 native 进程可注册）

### 配置一致性

- **NEVER** 让 SA Profile JSON 中的 `name` 与代码注册的 SA ID 不一致
- **NEVER** 让 CFG 进程名与 SA Profile 的 `process` 字段不一致
- **NEVER** 让非IDL模式 Proxy 和 Stub 的消息码枚举值不一致

### 符号导出（version_script）

- **NEVER** 让 SA so 库导出内部实现符号——必须通过 version_script 控制符号可见性
- **NEVER** 在 SA 的 `ohos_shared_library` 中遗漏 `shlib_type = "sa"` 或自定义 `version_script`

## version_script 与符号导出

### 为什么需要 version_script

SA 以 `.so` 形式被 `sa_main` 进程加载。如果不控制符号导出，所有内部符号都会暴露在进程符号表中，可能导致：
- 符号冲突（多个 SA 定义同名内部函数）
- ABI 不稳定（内部实现变更影响外部）
- 安全风险（内部函数可被外部调用）

### 推荐方式：使用 shlib_type

在 `ohos_shared_library` 中设置 `shlib_type = "sa"`，构建系统会自动应用默认的 `singleton.versionscript`：

```gn
ohos_shared_library("demo_service") {
  sources = [...]
  shlib_type = "sa"  # 自动应用默认 version_script
  part_name = "safwk"
  subsystem_name = "systemabilitymgr"
}
```

默认 `singleton.versionscript` 仅导出 SA 注册所需的符号（`*delegator_E`、`*instance_E`、`*mutex_E`），隐藏其他所有符号。

### 自定义 version_script

当需要导出额外符号（如给其他模块调用的 C 接口）时，编写 `.map` 文件：

```
{
  global:
    extern "C++" {
      "OHOS::Demo::IDemoService::*";
    };
    extern "C" {
      "OH_DemoService_GetInstance";
    };
  local:
    *;
};
```

在 BUILD.gn 中引用：

```gn
ohos_shared_library("demo_service") {
  sources = [...]
  version_script = "demo_service.map"
  part_name = "safwk"
  subsystem_name = "systemabilitymgr"
}
```

### .map 文件格式说明

| 段 | 作用 |
|---|------|
| `global:` | 列出需要导出的符号，支持通配符 |
| `extern "C++"` | C++ 符号（需要 mangled 名称或通配符） |
| `extern "C"` | C 符号（原始函数名） |
| `local: *;` | 隐藏所有未在 global 中列出的符号 |

### 模板 BUILD.gn 注意事项

生成代码时，`services/BUILD.gn` 中的 `ohos_shared_library` 应包含 `shlib_type = "sa"`，确保符号隔离。IDL 和非IDL 模式均适用。

## 常见失败模式

### SA 无法启动

| 现象 | 根因 | 解决 |
|------|------|------|
| 进程未拉起 | CFG 路径错误或未 push 到设备 | 检查 CFG `path` 字段，确保使用 `/system/bin/sa_main` |
| 进程启动但 SA 未注册 | Profile JSON 未安装或 `libpath` 错误 | 检查 so 路径和 sa_profile BUILD.gn |
| SA 注册失败 | Selinux 权限不足 | 检查 selinux 规则是否配置 `add` 权限 |
| `OnStart` 超时 | `OnStart` 中有耗时操作 | 将耗时操作移到独立线程 |

### IPC 调用失败

| 现象 | 根因 | 解决 |
|------|------|------|
| `GetSystemAbility` 返回 nullptr | SA ID 未上库或 SA 未注册 | 检查 `system_ability_definition.h` |
| `SendRequest` 返回错误 | 消息码不匹配或序列化错误 | 检查 Proxy/Stub 消息码一致性 |
| 数据读取崩溃 | `Read*` 返回值未校验 | 添加读取校验 |
| `ReadInterfaceToken` 不匹配 | Proxy 和 Stub 的 descriptor 不一致 | 检查 `DECLARE_INTERFACE_DESCRIPTOR` |

### 编译失败

| 现象 | 根因 | 解决 |
|------|------|------|
| 找不到 IDL 生成的头文件 | `include_dirs` 缺少 `${target_gen_dir}` | 在 BUILD.gn 中添加 |
| 重复定义符号 | 手写和 IDL 生成的 Proxy/Stub 同时存在 | 移除手写文件 |
| SA Profile 编译失败 | JSON 文件名与 BUILD.gn 引用不一致 | 统一文件名 |

## 生成后验证最小命令

```bash
# 编译验证
./build.sh --product-name rk3568 --cache --build-target {sa_name}

# 部署验证
hdc file send {process_name}.cfg /system/etc/init/
hdc file send {process_name}.json /system/profile/
hdc shell reboot

# 状态验证
hdc shell ps -A | grep {process_name}
hdc shell hidumper -ls
```

**验证失败时的处理路径**：
1. 编译失败 → 根据错误日志修复代码 → 重新编译
2. 进程未启动 → 检查 CFG 路径和权限 → 重新部署
3. SA 未注册 → 检查 Profile 和 Selinux → 查看日志 `hilog | grep {sa_name}`
4. IPC 调用失败 → 检查消息码和序列化 → 用 hidumper 确认 SA 状态
