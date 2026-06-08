---
name: ohos-dev-mmi-device-test-harness
description: Use when building or running multimodal input system tests on a real DAYU200 device. Covers NativeToken permission setup, server-side bypass, test binary compile/deploy/run pipeline, phase-based hidumper capture, device discovery polling, and dump field reference.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: device-test-harness
  version: 0.2.0
  status: draft
  tags:
    - multimodalinput
    - device-testing
    - hidumper
    - nativetoken
  related-skills:
    - ohos-dev-mmi-wms-dms-simulation
    - ohos-dev-mmi-uinput-virtual-device
---

# 多模输入真机测试脚手架

在 DAYU200 (RK3568) 真机上运行多模输入子系统测试二进制的完整基础设施。

## When to Use

- 新建多模输入系统测试二进制时，需要权限获取、编译部署、dump 捕获等基础能力
- 已有测试需要在真机上运行和验证
- 需要理解 hidumper dump 输出的含义

## 跳板机环境变量

设备通过 Windows 跳板机连接（hdc 运行在 Windows 上）。所有命令使用环境变量避免硬编码凭据：

```bash
# 设置一次，全 session 复用（根据实际环境替换占位符）
export DEVICE="<device_serial>"                    # hdc 设备序列号
export WIN_SSH="sshpass -p <pwd> ssh -o StrictHostKeyChecking=no -p <port> <user>@<host>"
export WIN_SCP="sshpass -p <pwd> scp -P <port>"
export WIN_SCP_DST="<user>@<host>:Desktop"         # SCP 目标（跳板机桌面）
export WIN_HOME='C:\Users\<user>'                  # Windows 用户主目录
export HDC="hdc -t $DEVICE"
```

后续文档中的 `$WIN_SSH`、`$WIN_SCP`、`$WIN_SCP_DST`、`$WIN_HOME`、`$HDC` 均引用这些变量。

## 权限获取

测试进程调用 InputManager IPC 需要系统权限：

```cpp
#include "accesstoken_kit.h"
#include "nativetoken_kit.h"
#include "token_setproc.h"

static void InitNativeToken() {
    const char *perms[] = {
        "ohos.permission.INPUT_DEVICE_CONFIGURATOR",
        "ohos.permission.INPUT_MONITORING",
    };
    NativeTokenInfoParams info = {
        .dcapsNum = 0,
        .permsNum = sizeof(perms) / sizeof(perms[0]),
        .aclsNum = 0,
        .dcaps = nullptr,
        .perms = perms,
        .acls = nullptr,
        .processName = "YourTestName",
        .aplStr = "system_basic",
    };
    uint64_t tokenId = GetAccessTokenId(&info);
    SetSelfTokenID(tokenId);
    OHOS::Security::AccessToken::AccessTokenKit::ReloadNativeTokenInfo();
}
```

**必须在 main() 最开始、其他 InputManager 调用之前执行。**

权限列表按测试需要调整：
- `INPUT_DEVICE_CONFIGURATOR` — 设备绑定/解绑
- `INPUT_MONITORING` — 事件监听

## Server 端绕过

测试进程不是 WMS/DMS 进程，server 端会校验调用方 token 类型。需要临时修改 3 个位置：

### 1. OnDisplayInfo — 允许测试进程调 UpdateDisplayInfo

**文件**: `service/message_handle/src/server_msg_handler.cpp`

```cpp
int32_t ServerMsgHandler::OnDisplayInfo(SessionPtr sess, NetPacket &pkt) {
    // [TEST BYPASS] 原代码校验 tokenType == TOKEN_NATIVE
    // 测试时注释掉该检查，允许所有 token 类型
}
```

### 2. OnWindowGroupInfo — 允许测试进程调 UpdateWindowInfo

**文件**: `service/message_handle/src/server_msg_handler.cpp`

```cpp
int32_t ServerMsgHandler::OnWindowGroupInfo(SessionPtr sess, NetPacket &pkt) {
    // [TEST BYPASS] 同上
}
```

### 3. CheckBindDevicePermission — 允许测试进程绑定设备

**文件**: `service/module_loader/src/mmi_service.cpp`

```cpp
// [TEST BYPASS] 直接 return RET_OK
// 原代码: 校验 INPUT_DEVICE_CONFIGURATOR 权限
```

### 部署绕过后的 .so

```bash
# 备份原始 .so
$WIN_SSH "$HDC shell mount -o rw,remount /"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-server.z.so /system/lib/libmmi-server.z.so.bak"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-service.z.so /system/lib/libmmi-service.z.so.bak"

# 推送修改后的 .so（从编译产物）
$WIN_SCP libmmi-server.z.so "$WIN_SCP_DST/libmmi-server.z.so"
$WIN_SSH "$HDC file send $WIN_HOME\\Desktop\\libmmi-server.z.so /system/lib/libmmi-server.z.so"
$WIN_SCP libmmi-service.z.so "$WIN_SCP_DST/libmmi-service.z.so"
$WIN_SSH "$HDC file send $WIN_HOME\\Desktop\\libmmi-service.z.so /system/lib/libmmi-service.z.so"

# 重启 multimodalinput 服务
$WIN_SSH "$HDC shell kill \$(pidof multimodalinput)"
```

**注意**：.so 在 `/system/lib/`，不是 `/system/lib/platformsdk/` 或 `/system/lib/chipset-pub-sdk/`。

### 还原

```bash
$WIN_SSH "$HDC shell mount -o rw,remount /"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-server.z.so.bak /system/lib/libmmi-server.z.so"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-service.z.so.bak /system/lib/libmmi-service.z.so"
$WIN_SSH "$HDC shell kill \$(pidof multimodalinput)"
```

**测试完成后必须还原。** 绕过会降低系统安全性。

## 编译部署流水线

### 编译

测试二进制通过 `compile_test.py` 编译（使用 OpenHarmony 工具链交叉编译）：

```bash
cd /srv/workspace/<oh_root>
python3 /tmp/compile_test.py
```

`compile_test.py` 的关键配置：
- `SOURCE` — 测试 .cpp 源文件路径
- `BUILD_DIR` — `<oh_root>/code/out/rk3568`
- `OUTPUT_DIR` — 编译产物子目录（如 `multimodalinput/input`）
- 产物位于 `$BUILD_DIR/$OUTPUT_DIR/<target_name>`

### 部署到设备

```bash
BINARY="<oh_root>/code/out/rk3568/<output_dir>/<target>"

# 1. SCP 到 Windows 跳板机桌面
$WIN_SCP "$BINARY" "$WIN_SCP_DST/<target>"

# 2. hdc 推送到设备
$WIN_SSH "$HDC file send $WIN_HOME\\Desktop\\<target> /data/local/tmp/<target>"
```

**路径注意**：hdc 在 Windows 上运行，`file send` 的源路径是 Windows 路径（`C:\\...`）。

### 运行

```bash
$WIN_SSH "$HDC shell chmod 755 /data/local/tmp/<target>"
$WIN_SSH "$HDC shell /data/local/tmp/<target>"
```

**hdc shell 引号陷阱**：不要在 hdc shell 后用单引号包裹命令（`hdc shell 'cmd1 && cmd2'`），会报 `no closing quote`。拆成多条 hdc 命令。

## Phase-Based Dump 捕获

### 原理

测试二进制通过写 phase 文件通知外部脚本当前阶段，外部脚本检测到新 phase 后执行 hidumper 捕获。

### C++ 端 — DumpPhase()

```cpp
static void DumpG(const char *label)
{
    std::cout << "\n===== " << label << " =====" << std::endl;
    std::cout.flush();
    FILE *f = fopen("/data/local/tmp/dual_group_phase.txt", "w");
    if (f) { fprintf(f, "%s\n", label); fclose(f); }
    std::this_thread::sleep_for(std::chrono::seconds(3));  // 等外部脚本捕获
}
```

3 秒 sleep 是关键 — 外部脚本 1 秒轮询一次，需要留出足够时间。

### Shell 端 — 后台捕获脚本

```bash
#!/system/bin/sh
DUMP=/data/local/tmp/dump.txt
PHASE=/data/local/tmp/dual_group_phase.txt
TEST=/data/local/tmp/<test_binary>
rm -f "$DUMP" "$PHASE"
chmod 755 "$TEST"
$TEST &
PID=$!
LAST=""
while kill -0 $PID 2>/dev/null; do
    if [ -f "$PHASE" ]; then
        CUR=$(cat "$PHASE" 2>/dev/null)
        if [ "$CUR" != "$LAST" ] && [ -n "$CUR" ]; then
            echo "===== DUMP: $CUR =====" >> "$DUMP"
            hidumper -s MultimodalInput -a '-G' >> "$DUMP" 2>&1
            LAST="$CUR"
        fi
    fi
    sleep 1
done
wait $PID 2>/dev/null
echo "TEST_DONE" >> "$DUMP"
```

**关键**：PHASE 文件路径必须与 C++ 端一致。之前出过 `phase.txt` vs `dual_group_phase.txt` 不匹配导致整个 dump 为空的 bug。

### 拉取 dump 到本地

```bash
$WIN_SSH "$HDC file recv /data/local/tmp/dump.txt $WIN_HOME\\Desktop\\dump.txt"
$WIN_SCP "$WIN_SCP_DST/../Desktop/dump.txt" /tmp/dump.txt
```

## 设备发现轮询

uinput `UI_DEV_CREATE` 后设备需要被 libinput 扫描到才能通过 InputManager 发现。轮询模式：

```cpp
static int FindDevice(const std::string &targetName) {
    std::mutex mtx;
    std::condition_variable cv;
    int foundId = -1;
    for (int attempt = 0; attempt < 30 && foundId < 0; ++attempt) {
        bool done = false;
        InputManager::GetInstance()->GetDeviceIds([&](std::vector<int32_t> &ids) {
            for (auto id : ids) {
                InputManager::GetInstance()->GetDevice(id,
                    [&](std::shared_ptr<InputDevice> dev) {
                        if (dev && dev->GetName() == targetName) {
                            foundId = id;
                        }
                    });
            }
            std::lock_guard<std::mutex> lock(mtx);
            done = true;
            cv.notify_one();
        });
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait_for(lock, std::chrono::milliseconds(500), [&] { return done; });
        if (foundId >= 0) break;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
    return foundId;
}
```

最多等 15 秒（30 次 x 500ms）。实测通常 1-3 秒内发现。

## hidumper Dump 字段参考

`hidumper -s MultimodalInput -a '-G'` 输出的关键段落：

| 段落 | 字段 | 含义 |
|------|------|------|
| **RuntimeBindings** | `deviceId=N displayId=N groupId=N` | HID 设备绑定关系 |
| **DisplayGroups** | `groupId displays mainDisplayId focusWindowId` | 显示组配置（focusWindowId 对 MAIN_GROUPID 显示为 -1 是正常的） |
| **PointerStateByGroup** | `cursorPos mouseLocation captureMode` | 每组光标位置和捕获模式 |
| **KeyboardStateByGroup** | `focusWindowId` + 按键状态 | 每组键盘状态 |
| **SequenceSnapshots** | 类型(POINTER/KEY) group targetWindow | 最近事件序列记录（可能为空，有 TTL） |
| **SoftCursorRS** | `displayId cursorPos direction drawFlag` | 软光标渲染状态 |
| **PointerStyleByWindow** | `pid windowId groupId style(id/size/color)` | 每窗口光标样式 |
| **PointerDrawingRS → Display Info** | 显示器属性表 | 已注册的显示器列表 |
| **PointerDrawingRS → Cursor Info** | `windowId lastPhysicalX/Y` | 当前光标命中的窗口 ID（hit-test 结果） |

### 解读要点

- `DisplayGroups.focusWindowId=-1` 对 MAIN_GROUPID 是正常的 — dump 读的是 `displayGroupInfoMap_`，MAIN_GROUPID 的焦点从 `UpdateWindowInfo` 传入，存在别处
- `Cursor Info.windowId` 反映光标物理位置命中的最高 zOrder 窗口，不是焦点窗口
- `SequenceSnapshots` 可能为空 — 条目有 TTL 或被清理，dump 时机要紧跟事件注入
- `RuntimeBindings` 为 `(empty)` 表示无设备绑定

## SELinux 注意

真机默认 SELinux Enforcing，测试前需要临时关闭：

```bash
$WIN_SSH "$HDC shell setenforce 0"   # Permissive
# 测试完成后还原：
$WIN_SSH "$HDC shell setenforce 1"   # Enforcing
```

不关闭 SELinux 时，`/dev/uinput` 访问和部分 IPC 会被拒绝。

## GN 构建目标配置

测试二进制的 `BUILD.gn` 配置要点：

```gn
ohos_executable("dual_group_interleave_test") {
  sources = [ "dual_group_interleave_test.cpp" ]
  deps = [
    "//foundation/multimodalinput/input/frameworks/proxy:libmmi-client",
    "//base/security/access_token/interfaces/innerkits/nativetoken:libnativetoken",
    "//base/security/access_token/interfaces/innerkits/accesstoken:libaccesstoken_sdk",
    "//base/security/access_token/interfaces/innerkits/token_setproc:libtoken_setproc",
  ]
  external_deps = [ "input:libmmi-client" ]
  testonly = true      # 测试专用，不参与正式构建
  part_name = "input"
  subsystem_name = "multimodalinput"
}
```

`testonly = true` 确保不会被正式产品构建拉入。

## 完整执行顺序

```
准备阶段：
  1. 修改 server 端绕过 → 编译 .so → 部署到设备 → 重启服务
  2. SELinux permissive

测试阶段：
  3. 编译测试二进制 (compile_test.py)
  4. 部署后台 dump 脚本 + 测试二进制到设备
  5. 运行后台 dump 脚本（启动测试 + hidumper 捕获）
  6. 拉取 dump 文件到本地分析

还原阶段：
  7. 还原 server 端 .so（从 .bak）
  8. SELinux enforcing
  9. 验证还原：重启服务 + 确认正常功能
```

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| Phase 文件路径不匹配 | dump 全程为空 | C++ 写的路径和 shell 读的路径必须完全一致 |
| hdc shell 用单引号包裹多命令 | `no closing quote` 错误 | 拆成多条独立 hdc 命令 |
| .so 推到错误路径 | 服务加载旧 .so，绕过不生效 | 路径是 `/system/lib/`，不是 platformsdk/ 或 chipset-pub-sdk/ |
| 忘记 mount -o rw,remount / | file send 到 /system/ 失败 | 先 remount |
| DumpG sleep 太短 | 外部脚本来不及捕获 | 至少 3 秒（脚本 1 秒轮询一次） |
| 忘记 testonly=true | 正式构建报错或拉入测试代码 | BUILD.gn 中加 testonly=true |
| 忘记还原 server 绕过 | 安全风险 | 测试完必须从 .bak 还原 |
| SELinux 未关闭 | uinput/IPC 被拒绝，报权限错误 | `setenforce 0` |
| InitNativeToken 放在 InputManager 调用之后 | 权限检查失败 | 必须在 main() 最开始调用 |
