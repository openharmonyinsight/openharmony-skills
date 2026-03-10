---
name: cli-from-innerkits
description: Guides generating a command-line binary that wraps SA or inner_kits APIs (OpenHarmony/OHOS). Use when adding a CLI tool for a subsystem, wrapping inner_kits or IDL proxy interfaces into shell-callable commands, or when the user asks how to generate a command-line tool from existing native/SA interfaces.
---

# 从 inner_kits/SA 生成命令行工具

指导在 OpenHarmony/OHOS 工程中，将 **inner_kits 头文件中的 public 接口** 或 **SA（System Ability）的 IDL 接口** 封装成可执行命令行工具，供脚本或调试使用。

## 何时使用本 Skill

- 需要为当前子系统/仓库新增一个 **独立可执行二进制**，对外暴露已有 C++/SA 能力。
- 希望把 **bundle.json 里 inner_kits 列出的 .h 接口** 或 **IXXX.idl 定义的 SA 接口** 做成子命令（如 `get-*`、`list-*`、`set-*`）。
- 参考本仓库内 **storage_cli** 的实现方式，为其他库套用同一套模式。

## 整体流程

1. **确定接口来源**：从 bundle.json 的 `build.inner_kits` 或服务的 IDL 确定要封装的接口（.h 中的函数/类、IXXX 的 IPC 方法）。
2. **新建 CLI 目录**：在工程下建 `tools/<name>_cli/`，例如 `tools/storage_cli`。
3. **实现 main 入口**：单文件或少量 C++ 源文件，实现 `main(argc, argv)`、子命令解析、调用 proxy/API、输出结果。
4. **编写 BUILD.gn**：`ohos_executable`，依赖对应 inner_kits 的 shared_library 或 SA proxy 目标，并配好 `external_deps`（如 samgr、safwk、ipc）。
5. **（可选）接入 bundle 构建**：在 `bundle.json` 的 `build.group_type.service_group` 中追加该 executable 的 GN 路径，以便随镜像安装。

---

## 1. 目录与文件结构

```
tools/
└── <component>_cli/
    ├── BUILD.gn
    └── <component>_cli_main.cpp   # 或 main.cpp
```

- 可执行名与目录名一致即可（如 `storage_cli`），便于在 `relative_install_dir = "bin"` 下安装。

---

## 2. main 程序结构（C++）

### 2.1 必备头与命名空间

- 若封装 **SA**：需要获取 proxy，通常需要：
  - `#include <iservice_registry.h>`
  - `#include <system_ability_definition.h>`
  - 对应 SA 的 IDL 生成头（如 `istorage_manager.h`）及 Parcel 类型头（如 `bundle_stats.h`、`volume_external.h`）。
- 若封装 **仅 .h 的 C API**（如 ACL）：直接 `#include "xxx.h"`，无需 samgr。

### 2.2 获取 SA Proxy 的写法（当封装 SA 时）

```cpp
sptr<IYourInterface> GetYourProxy() {
    auto sam = SystemAbilityManagerClient::GetInstance().GetSystemAbilityManager();
    if (sam == nullptr) return nullptr;
    sptr<IRemoteObject> object = sam->GetSystemAbility(YOUR_SA_ID);  // 来自 system_ability_definition.h
    if (object == nullptr) return nullptr;
    return iface_cast<IYourInterface>(object);
}
```

- 每个子命令里：先 `GetYourProxy()`，若为 `nullptr` 则打印错误并 `return 1`；再调用 proxy 方法，根据返回码打印并 `return 0/1`。

### 2.3 子命令解析与分发

- `argv[0]` 为程序名，`argv[1]` 为子命令名，**子命令参数从 `argv[2]` 起**。
- 在 main 里：`cmd = argv[1]`，`cmdArgc = argc - 2`，`cmdArgv = (argc > 2) ? &argv[2] : nullptr`。
- 用静态表驱动分发，避免长 if-else：

```cpp
struct Command { const char *name; int (*handler)(int argc, char **argv); };
static const Command kCommands[] = {
    { "get-something", CmdGetSomething },
    { "list-items",    CmdListItems },
    // ...
};
for (const auto &c : kCommands) {
    if (strcmp(cmd, c.name) == 0) return c.handler(cmdArgc, cmdArgv);
}
```

- 每个 handler 的 **argc/argv 对应子命令参数**：即 `argv[0]` 为第一个参数（不是程序名），注意 `argv` 可能为 `nullptr`（无参数时），要先判 `argc` 和 `argv` 再访问。

### 2.4 参数与错误约定

- 在 handler 内：先检查必需参数（如 `argc < 1 || argv == nullptr`），不足则 `std::cerr` 提示并 `return 1`。
- 可选参数用 `(argc > n && argv) ? argv[n] : default_value` 或 `atoi(argv[n])` 等安全解析。
- 成功：结果打印到 `std::cout`，`return 0`；失败：错误信息到 `std::cerr`，`return 1`。
- 输出格式建议简单可解析（如 `key=value` 或每行一条），便于脚本使用。

### 2.5 类型来自 Parcel/基类时的注意点

- 若返回类型是 **继承自 Parcelable 的类**（如 `VolumeExternal : public VolumeCore`），而头文件中**子类只声明了部分 getter**，基类的 `GetId()`、`GetDiskId()` 等可能在某些构建下不可见。
- **稳妥写法**：对子类引用转成基类再调基类方法，例如：
  - `const VolumeCore &vc = static_cast<const VolumeCore &>(vol);`
  - 使用 `vc.GetId()`、`vc.GetDiskId()`、`vc.GetState()`，子类自有方法仍用 `vol.GetPath()` 等。

---

## 3. BUILD.gn 模板

- **目标类型**：`ohos_executable("your_cli")`。
- **sources**：列出 `*_main.cpp`。
- **include_dirs**：包含本仓的 service/include、common/include、以及 **inner_kits 对应 native 目录**（放 .h 的路径），若有多组 inner_kits 则多列几个。
- **deps**：  
  - 封装 SA：依赖该 SA 的 **proxy / inner_kits 库**（例如 `storage_manager_sa_proxy`），以便链接 IDL 生成代码和 Parcel 类型。  
  - 封装仅 .h 的库：依赖对应 **inner_kits 的 shared_library**（如 `storage_manager_acl`）。
- **external_deps**（按需）：  
  - 若通过 samgr 取 proxy：`safwk:system_ability_fwk`、`samgr:samgr_proxy`、`ipc:ipc_single`。  
  - 常用：`c_utils:utils`、`hilog:libhilog`。
- **part_name / subsystem_name**：与当前组件一致。
- **安装**（可选）：`install_enable = true`，`install_images = [ "system" ]`，`relative_install_dir = "bin"`。

```gn
import("//build/ohos.gni")
import("//your/product/path/your_aafwk.gni")   # 若有 path 变量

ohos_executable("your_cli") {
  sources = [ "your_cli_main.cpp" ]
  include_dirs = [
    "${your_service_path}/include",
    "${your_interface_path}/innerkits/xxx/native",
  ]
  cflags = [ "-D_FORTIFY_SOURCE=2", "-fstack-protector-strong", "-Wno-unused-parameter" ]
  defines = [ "STORAGE_LOG_TAG = \"YourCli\"", "LOG_DOMAIN = 0xD004300" ]
  deps = [
    "//path/to/innerkits/native:your_sa_proxy_or_lib",
  ]
  external_deps = [
    "c_utils:utils",
    "hilog:libhilog",
    "ipc:ipc_single",
    "safwk:system_ability_fwk",
    "samgr:samgr_proxy",
  ]
  part_name = "your_part"
  subsystem_name = "your_subsystem"
  install_enable = true
  install_images = [ "system" ]
  relative_install_dir = "bin"
}
```

---

## 4. 接入 bundle.json（可选）

若希望该可执行文件随组件一起被系统构建与镜像包含：

- 在 `bundle.json` → `component.build.group_type.service_group` 数组中追加一条：
  - `"//foundation/your_subsystem/your_component/tools/your_cli:your_cli"`
- 路径需与仓库在 full tree 中的路径一致（如 `foundation/filemanagement/storage_service/...`）。

---

## 5. 本仓库参考实现

本仓库内已有一个完整示例：

- **源码**：`tools/storage_cli/storage_cli_main.cpp`
- **构建**：`tools/storage_cli/BUILD.gn`
- **bundle 注册**：`bundle.json` 中 `service_group` 含 `//foundation/filemanagement/storage_service/tools/storage_cli:storage_cli`

该 CLI 封装了：

- **storage_manager_sa_proxy**（IStorageManager）：通过 `GetSystemAbility(STORAGE_MANAGER_MANAGER_ID)` 取 proxy，子命令包括 get-bundle-stats、get-all-volumes、get-disk-by-id、mount、format 等。
- **storage_manager_acl**（storage_acl.h）：`AclSetAccess`、`AclSetDefault` 对应子命令 acl-set-access、acl-set-default。

实现时可直接对照上述文件：main 结构、proxy 获取、表驱动子命令、argc/argv 从 `argv[2]` 起、VolumeExternal 转 VolumeCore 再调 GetDiskId 等细节。

---

## 6. 检查清单（给其他库生成 CLI 时）

- [ ] 已从 bundle.json 的 inner_kits 或 IDL 明确要封装的接口（.h 或 IXXX）。
- [ ] 已建 `tools/<name>_cli/` 且含 `BUILD.gn` 和 `*_main.cpp`。
- [ ] main 中子命令参数使用 `argv[2]...`，handler 内使用 `argv[0]` 为第一个参数并做 nullptr/argc 检查。
- [ ] 若用 SA：已实现 GetXxxProxy()，并依赖对应 sa_proxy 与 samgr/safwk/ipc。
- [ ] 若用 Parcel 派生类：基类 getter 通过 `static_cast<const Base&>(obj)` 调用，避免“没有 GetXxx”的编译错误。
- [ ] BUILD.gn 中 `part_name`/`subsystem_name` 与组件一致，需要时已加 `install_*` 和 `relative_install_dir`。
- [ ] 若需进镜像，已在 bundle.json 的 service_group 中登记该 executable 的 GN 目标。
