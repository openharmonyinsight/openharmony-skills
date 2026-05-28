# 模式四：修改已有 SA 代码

## 交互式信息收集

```
questions:
  - question: "请描述需要修改的内容"
    header: "修改需求"
    options:
      - label: "添加新的接口方法"
        description: "在 SA 中新增对外的接口"
      - label: "修改已有接口实现"
        description: "修改已有方法的逻辑"
      - label: "修改 SA 配置"
        description: "调整 profile、cfg、BUILD.gn 等配置"
      - label: "添加 SA 依赖监听"
        description: "监听其他 SA 的上下线状态"
      - label: "其他修改"
        description: "描述具体的修改需求"
```

## 根据修改类型执行

### 添加新接口方法

**对于 IDL 化 SA**：
1. 在 `.idl` 文件中添加新方法声明
2. 在 SA 类中添加新方法的 override 实现
3. Proxy/Stub 由 IDL 工具自动重新生成，无需手动修改
4. 通知用户重新编译即可

**对于非IDL 化 SA**：
1. 在 `interfaces/I{sa_name}.h` 中：
   - 在 `I{SaName}IpcCode` 枚举中添加新消息码
   - 添加新的纯虚函数声明
2. 在 `services/include/{sa_name}_proxy.h` 中：
   - 添加新方法的 override 声明
3. 在 `services/src/{sa_name}_proxy.cpp` 中：
   - 实现新方法（WriteInterfaceToken → Write入参 → SendRequest(使用枚举) → Read出参）
4. 在 `services/src/{sa_name}_stub.cpp` 中：
   - 在 `OnRemoteRequest` 的 switch 中添加新 case（使用枚举）
5. 在 SA 类 `{sa_name}.h/.cpp` 中：
   - 声明并实现新方法

### 修改 SA 配置

根据需求修改对应的 profile JSON / cfg / BUILD.gn 文件，参照对应模式的模板格式。

### 添加 SA 依赖监听

在 SA 类的 `OnStart()` 中添加 `AddSystemAbilityListener(TARGET_SA_ID);`，
并实现 `OnAddSystemAbility` / `OnRemoveSystemAbility` 回调。
