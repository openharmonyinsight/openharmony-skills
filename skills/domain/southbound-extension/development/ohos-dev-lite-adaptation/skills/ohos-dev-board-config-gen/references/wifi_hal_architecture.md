# WiFi HAL 架构参考 (Hi3861V100 / OH Lite)

> **来源**: Ground Truth `device/soc/hisilicon/hi3861v100/hi3861_adapter/hals/communication/wifi_lite/wifiservice/source/wifi_device.c`
> **用途**: P3 driver-dev 阶段生成 WiFi HAL 时的架构指南
> **版本**: Iteration 02 提取 | GT 代码量: **993 行** | 复杂度: **HIGH**

---

## 1. 为什么 WiFi HAL 特殊

| 维度 | 简单驱动 (GPIO/I2C/PWM/UART) | WiFi HAL |
|------|-------------------------------|---------|
| 代码行数 | 30-80 行 | **993 行** |
| 函数数量 | 3-8 个 | **30+ 个** |
| 内部状态 | 无 (无状态) | **7 个全局状态变量** |
| 异步处理 | 同步调用 | **事件回调 + 状态机** |
| 外部依赖 | 单个 SDK 头文件 | **LWIP + WPA + HisiWiFi + FS + utils** |

**Iteration 01 结果**: 再生版仅 177 行，覆盖率 **0%**。缺失的核心是整个事件分发基础设施。

---

## 2. 分层架构

```
┌──────────────────────────────────────────────────────┐
│ Layer 1: Public OH WiFi HAL API                       │
│ WifiConnect / WifiDisconnect / WifiScan / ...        │
│ (wifi_device.h 定义的接口)                            │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│ Layer 2: Connection State Machine                     │
│ g_wifiStaStatus / g_connectState / g_networkId       │
│ STA_NOT_ACTIVE → ACTIVE → CONNECTING → CONNECTED      │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│ Layer 3: Event Dispatch System (核心复杂度所在)         │
│ HisiEvent → DispatchEvent() → User Callback           │
│ ~200 行代码                                           │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│ Layer 4: Network Config Persistence                   │
│ WriteNetworkConfig / ReadNetworkConfig               │
│ Flash 文件系统存储 SSID/PSK                           │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│ Layer 5: IP/DNS Post-Connect Setup                    │
│ StaSetLocaladdr / StaSetDNSServer / StaSetNetConfig   │
│ LWIP netifapi + dns API                               │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│ Layer 6: Hisilicon WiFi Driver API                    │
│ hi_wifi_connect / hi_wifi_scan / hi_wifi_start/stop   │
│ hi_wifi_register_event_callback                      │
└──────────────────────────────────────────────────────┘
```

---

## 3. 全局状态变量

```c
// === STA (Station) 模式状态 ===
static int g_wifiStaStatus = WIFI_STA_NOT_ACTIVE;    // STA 激活状态
static int g_connectState = WIFI_STATE_NOT_AVAILABLE; // 连接状态
static int g_networkId = -1;                          // 当前配置 ID

// === 配置存储 ===
static WifiDeviceConfig g_wifiConfigs[WIFI_MAX_CONFIG_SIZE]; // 已保存的配置
static bool g_networkConfigReadFlag = false;          // 配置是否已加载
static int g_isNetworkConfigExist = WIFI_FILE_UNEXIST; // 配置文件是否存在

// === 事件回调 ===
static WifiEvent* g_wifiEvents[WIFI_MAX_EVENT_SIZE] = {0}; // 用户注册的回调
```

### 状态转换图

```
              ┌─────────────────┐
              │ WIFI_STA_NOT_   │ ← 初始状态 / 断开
              │     ACTIVE      │
              └────────┬────────┘
                       │ WifiStartSta / Activate
                       ↓
              ┌─────────────────┐
              │  WIFI_STA_      │ ← 可扫描
              │     ACTIVE      │
              └────────┬────────┘
                       │ WifiConnect (发起连接)
                       ↓
              ┌─────────────────┐
              │ WIFI_STA_       │ ← 正在连接
              │   CONNECTING    │
              └────────┬────────┘
                       │ 连接成功 (DispatchStaConnectEvent)
                  ┌────┴────┐
                  ↓         ↓
    ┌───────────────┐  ┌───────────────┐
    │WIFI_STA_      │  │WIFI_STA_      │ ← 断开
    │  CONNECTED    │  │ DISCONNECTED  │
    └───────────────┘  └───────────────┘
```

---

## 4. 事件分发系统（最关键的部分）

### 4.1 双层事件模型

OH WiFi 使用**两层事件结构**：

```c
// 层 A: Hisilicon 原始事件 (来自 Hi3861 WiFi 驱动)
typedef struct {
    int event;              // 事件类型 (HI_WIFI_EVENT_*)
    void *data;            // 事件数据 (scan result, assoc req 等)
    size_t data_length;
} hi_wifi_event;

// 层 B: OH 标准化事件 (传递给应用)
typedef struct {
    int eventId;            // WIFI_SCAN_DONE / WIFI_CONNECTED / ...
    void *data;
    size_t data_length;
    const char *ifName;    // 接口名 ("wlan0")
} WifiEvent;
```

### 4.2 回调注册链

```
App 调用 WifiRegisterEventCallback(&event_cb)
    ↓
存储到 g_wifiEvents[] 数组
    ↓
RegisterHisiCallback()
    ↓
hi_wifi_register_event_callback(HiWifiWpaEventCb)
    ↓
[异步] Hi3861 WiFi 硬件产生事件
    ↓
HiWifiWpaEventCb(hisiEvent) 被调用
    ↓
DispatchEvent(hisiEvent, &ohEvent)
    ↓
根据 hisiEvent->event 类型分发:
  ├── HI_WIFI_EVENT_SCAN_DONE → DispatchScanStateChangeEvent()
  ├── HI_WIFI_EVENT_CONNECTED → DispatchConnectEvent() → DispatchStaConnectEvent()
  ├── HI_WIFI_EVENT_DISCONNECTED → DispatchDisconnectEvent()
  ├── HI_WIFI_EVENT_ASSOC_FAIL → DispatchAssocFailEvent()
  └── ... 其他事件
    ↓
遍历 g_wifiEvents[], 匹配 eventId → 调用用户回调
    ↓
应用的 OnWifiScanStateChanged / OnWifiConnectionChanged 被执行
```

### 4.3 关键分发函数签名

```c
// 入口: Hisilicon WPA 事件回调
static void HiWifiWpaEventCb(const hi_wifi_event *hisiEvent);

// 一级分发: HisiEvent → OHEvent
static void DispatchEvent(const hi_wifi_event* hisiEvent, const WifiEvent* hosEvent);

// 二级分发: 具体事件处理
static void DispatchScanStateChangeEvent(const hi_wifi_event*, const WifiEvent*);
static void DispatchConnectEvent(const hi_wifi_event*, const WifiEvent*);
static void DispatchStaConnectEvent(const hi_wifi_event*, const WifiEvent*);
static void DispatchApStartEvent(const WifiEvent*);

// 注册
static void RegisterHisiCallback(void);
```

### 4.4 估计代码量分配

| 功能模块 | GT 行数 | 最小可工作行数 | 说明 |
|---------|---------|--------------|------|
| 事件分发 (Layer 3) | ~200 | ~120 | 可简化错误路径 |
| 公共 API (Layer 1) | ~250 | ~150 | 保留所有接口签名 |
| 状态管理 (Layer 2) | ~100 | ~60 | 简化状态检查 |
| 配置持久化 (Layer 4) | ~80 | ~50 | 基础读写即可 |
| IP/DNS 设置 (Layer 5) | ~80 | ~50 | DHCP + static |
| Scan 实现 | ~140 | ~80 | 类型转换 + 异步结果 |
| STA Connect | ~120 | ~80 | 认证类型处理 |
| **总计** | **~970** | **~590** | 目标: ≥60% 架构覆盖 |

---

## 5. 公共 API 完整列表

### 5.1 STA 模式 API

| 函数 | 返回值 | 功能 | 复杂度 |
|------|--------|------|--------|
| `WifiEnableClient(void)` | WifiErrorCode | 启动 STA 模式 | 中 |
| `WifiDisableClient(void)` | WifiErrorCode | 停止 STA 模式 | 中 |
| `WifiConnect(const WifiDeviceConfig*)` | WifiErrorCode | 连接指定 AP | 高 |
| `WifiDisconnect(void)` | WifiErrorCode | 断开当前连接 | 低 |
| `WifiScan(void)` | WifiErrorCode | 触发扫描 | 中 |
| `WifiGetLinkedInfo(WifiLinkedInfo*)` | WifiErrorCode | 获取连接信息 | 低 |
| `IsWifiActive(void)` | int | 检查 WiFi 是否激活 | 低 |
| `WifiRegisterEventCallback(const WifiEvent*)` | WifiErrorCode | 注册事件回调 | 低 |
| `WifiUnregisterEventCallback(const WifiEvent*)` | WifiErrorCode | 注销回调 | 低 |

### 5.2 SoftAP 模式 API

| 函数 | 返回值 | 功能 |
|------|--------|------|
| `WifiHotspotConfig(HotspotConfig*)` | WifiErrorCode | 配置 SoftAP |
| `WifiStartHotspot(void)` | WifiErrorCode | 启动 SoftAP |
| `WifiStopHotspot(void)` | WifiErrorCode | 停止 SoftAP |

### 5.3 辅助函数 (static)

| 函数 | 功能 |
|------|------|
| `IsFileExist(path)` | 检查文件是否存在 |
| `WriteNetworkConfig(buf, len)` | 写入网络配置到 flash |
| `ReadNetworkConfig(buf, len)` | 从 flash 读取网络配置 |
| `ScanTypeSwitch(type)` | OH 扫描类型 → Hisi 扫描类型 |
| `GetLocalWifiIp(ip)` | 获取本机 IP 地址 |
| `StaSetLocaladdr(netif, gw, ip, mask)` | 配置接口 IP |
| `StaSetDNSServer(switcher)` | 配置 DNS |
| `StaSetWifiNetConfig(switcher)` | 启用/禁用 DHCP |

---

## 6. 头文件依赖

```c
// OH WiFi 接口
#include "wifi_device.h"

// 安全/标准库
#include <securec.h>
#include <stdio.h>
#include <stdlib.h>

// LWIP 网络栈 (IP/DNS/DHCP)
#include "lwip/if_api.h"
#include "lwip/netifapi.h"
#include "lwip/dns.h"

// 项目内部
#include "wifi_device_util.h"      // 工具函数
#include "wifi_hotspot_config.h"    // SoftAP 配置
#include "utils_file.h"             // 文件 I/O 工具
```

---

## 7. 相关文件清单

```
hals/communication/wifi_lite/
├── wifiservice/source/
│   ├── wifi_device.c         ← ★ 主文件 (993行)
│   ├── wifi_device_util.c    辅助工具函数
│   ├── wifi_device_util.h    辅助工具声明
│   └── wifi_hotspot.c        SoftAP 实现
├── wifiaware/source/
│   └── hal_wifiaware.c       WiFi Aware (返回 NOT_SUPPORTED)
└── BUILD.gn                   编译入口
```

---

## 8. 生成时策略

### 策略 A: 最小可行 (MVP) — 目标 ~400 行

生成以下内容：
1. ✅ 所有公共 API 函数签名（stub 或简单实现）
2. ✅ 全局状态变量声明
3. ✅ 基础事件分发框架（单级，不分 Hisi/OH 两层）
4. ✅ WifiConnect/WifiDisconnect/WifiScan 的基础实现
5. ❌ 不实现：配置持久化、IP/DNS 后设置、SoftAP
6. ❌ 不实现：完整的两层事件模型

### 策略 B: 完整架构 — 目标 ~700 行

在 MVP 基础上增加：
7. ✅ 双层事件分发 (HiWifiWpaEventCb → DispatchEvent → user cb)
8. ✅ 配置持久化 (WriteNetworkConfig / ReadNetworkConfig)
9. ✅ IP/DNS 后连接设置
10. ✅ SoftAP 基础实现
11. ⚠️ 简化错误处理路径

### 推荐: 先策略 A 通过 L3 验证，再迭代到策略 B

---

## 9. 与其他 HAL 的差异总结

| 特征 | GPIO/I2C/PWM/UART | WiFi HAL |
|------|-------------------|---------|
| 模式 | 1:1 委托 (`GpioX → hi_gpio_x`) | **状态机 + 事件驱动** |
| 内部状态 | 无 | **7 个全局变量** |
| 异步 | 无 (同步返回) | **扫描/连接均为异步** |
| 回调 | 无 | **必需 (g_wifiEvents[])** |
| 外部依赖 | 1 个 SDK 头 | **7+ 头文件 (LWIP/WPA/utils)** |
| 生成难度 | 低 (模板化) | **高 (需要架构理解)** |
