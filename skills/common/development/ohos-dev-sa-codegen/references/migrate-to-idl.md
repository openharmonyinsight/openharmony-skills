# 模式三：非IDL化 SA 改 IDL 化迁移

## 交互式信息收集

```
question: "请提供需要迁移的非IDL SA 代码路径（含接口、Proxy、Stub 文件所在目录）"
header: "迁移源码路径"
```

## 迁移步骤

### Step 1：分析现有代码

读取以下文件提取信息：
- `I{sa_name}.h` — 提取接口方法签名和 IPC 消息码枚举
- `{sa_name}_proxy.h` / `{sa_name}_proxy.cpp` — 确认序列化方式
- `{sa_name}_stub.h` / `{sa_name}_stub.cpp` — 确认反序列化方式
- `{sa_name}.h` / `{sa_name}.cpp` — 确认 SA 类结构和注册宏
- `BUILD.gn` — 确认编译配置

### Step 2：生成 IDL 文件

根据 `I{SaName}` 接口中的纯虚函数，生成 `.idl` 文件。转换规则：

| C++ 类型 | IDL 类型 |
|----------|----------|
| `int32_t` | `int` |
| `bool` | `boolean` |
| `std::string` / `std::u16string` | `String` |
| `sptr<IRemoteObject>` | `sptr<IRemoteObject>` |
| 输出参数 `T&` | `[out] T` |
| `void` 返回 | `void` |
| `ErrCode` 返回 | 保持 `ErrCode`，由方法签名决定 |
| 自定义 sequenceable | `sequenceable` 声明 |

### Step 3：修改 BUILD.gn

参照 SKILL.md 中「IDL 化 SA 模板文件清单」中的 `services/BUILD.gn` 模板：
1. 添加 `import("//build/config/components/idl_tool/idl.gni")`
2. 添加 `idl_gen_interface` 块
3. 添加 `ohos_source_set` 分别编译 proxy 和 stub
4. 从 `ohos_shared_library` 的 `sources` 中移除手写的 `{sa_name}_proxy.cpp` 和 `{sa_name}_stub.cpp`
5. 在 `deps` 中添加 IDL 生成依赖（`:{sa_name}_proxy`、`:{sa_name}_stub`）
6. 在 `include_dirs` 中添加 `${target_gen_dir}`

### Step 4：修改 SA 类

1. SA 头文件改为继承 `SystemAbility` + `{SaName}Stub`（Stub 由 IDL 生成）
2. 添加 `#include "{sa_name}_stub.h"`（IDL 生成）
3. 移除手写的 Proxy/Stub 文件引用

### Step 5：删除手写文件

- 删除 `services/include/{sa_name}_proxy.h` 和 `services/src/{sa_name}_proxy.cpp`
- 删除 `services/include/{sa_name}_stub.h` 和 `services/src/{sa_name}_stub.cpp`
- 删除 `interfaces/I{sa_name}.h`（接口由 IDL 生成替代）

### Step 6：告知用户差异

列出：
- 已生成的 IDL 文件
- BUILD.gn 的变更点
- 需要删除的手写文件
- SA 类头文件的修改点
- IDL 生成代码与原手写代码可能存在的差异（如方法名映射、参数序列化顺序）
