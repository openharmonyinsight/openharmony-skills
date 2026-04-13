# 目录-子系统映射表

本文件定义了 xts_acts 目录下各子目录与所属子系统的对应关系。
扫描结果生成报告时，根据问题文件的相对路径匹配本映射表，自动填充"所属子系统"列。

## 映射规则

1. 取问题文件的相对路径（相对于扫描根目录）
2. 依次尝试从最长目录前缀到最短前缀进行匹配
3. 匹配成功则填入对应子系统名称
4. 未匹配到则填 `-`

## 映射数据

| 目录 | 所属子系统 |
|------|-----------|
| ability/ability_runtime | 元能力 |
| ability/crossplatform | 元能力 |
| ability/form | 卡片框架 |
| account | 账号 |
| ai | AI |
| applications/settingsdata | 应用设置 |
| arkcompiler | 语言编译运行时 |
| arkui | ArkUI |
| bundlemanager | 包管理 |
| commonlibrary | 语言编译运行时 |
| communication/bluetooth_ble | 短距 |
| communication/bluetooth_bp | 短距 |
| communication/bluetooth_br | 短距 |
| communication/bluetooth_nop | 短距 |
| communication/btmanager_errorcode401 | 短距 |
| communication/btmanager_switchoff | 短距 |
| communication/dsoftbus | 软总线 |
| communication/netmanager_base | 短距 |
| communication/nfc_Controller | 短距 |
| communication/nfc_ErrorCode | 短距 |
| communication/nfc_Permissions | 短距 |
| communication/nfc_SecureElement | 短距 |
| communication/nfc_SecureElement_2 | 短距 |
| communication/wifi_ErrorCode201 | 短距 |
| communication/wifi_ErrorCode401 | 短距 |
| communication/wifi_enterprise | 短距 |
| communication/wifi_ets_standard | 短距 |
| communication/wifi_manager_nop | 短距 |
| communication/wifi_p10p | 短距 |
| communication/wifi_p11p | 短距 |
| communication/wifi_p12p | 短距 |
| communication/wifi_p13p | 短距 |
| communication/wifi_p14p | 短距 |
| communication/wifi_p15p | 短距 |
| communication/wifi_p16p | 短距 |
| communication/wifi_p17p | 短距 |
| communication/wifi_p18p | 短距 |
| communication/wifi_p19p | 短距 |
| communication/wifi_p2p | 短距 |
| communication/wifi_p20p | 短距 |
| communication/wifi_p21p | 短距 |
| communication/wifi_p22p | 短距 |
| communication/wifi_p23p | 短距 |
| communication/wifi_p24p | 短距 |
| communication/wifi_p25p | 短距 |
| communication/wifi_p26p | 短距 |
| communication/wifi_p27p | 短距 |
| communication/wifi_p28p | 短距 |
| communication/wifi_p29p | 短距 |
| communication/wifi_p3p | 短距 |
| communication/wifi_p30p | 短距 |
| communication/wifi_p31p | 短距 |
| communication/wifi_p32p | 短距 |
| communication/wifi_p33p | 短距 |
| communication/wifi_p34p | 短距 |
| communication/wifi_p35p | 短距 |
| communication/wifi_p36p | 短距 |
| communication/wifi_p37p | 短距 |
| communication/wifi_p38p | 短距 |
| communication/wifi_p39p | 短距 |
| communication/wifi_p3p | 短距 |
| communication/wifi_p40p | 短距 |
| communication/wifi_p41p | 短距 |
| communication/wifi_p4p | 短距 |
| communication/wifi_p5p | 短距 |
| communication/wifi_p6p | 短距 |
| communication/wifi_p7p | 短距 |
| communication/wifi_p8p | 短距 |
| communication/wifi_p9p | 短距 |
| communication/wifi_standard | 短距 |
| customization | 定制化 |
| distributeddatamgr | 分布式数据 |
| global | 全球化 |
| graphic | 图形图像 |
| hdf | 驱动 |
| hiviewdfx | DFX |
| inputmethod | 输入法 |
| location | 位置服务 |
| multimedia/audio | 音频 |
| multimedia/avsource | 视频框架 |
| multimedia/camera | 相机图库框架 |
| multimedia/image | 相机图库框架 |
| multimedia/media | 视频框架 |
| multimedia/photoAccess | 相机图库框架 |
| multimodalinput | 多模输入 |
| pcs | XTS专项小组 |
| print | 打印框架 |
| resourceschedule | 全局资源调度 |
| security | 安全 |
| security/certificate_manager | 安全 |
| storage | 文件管理 |
| telephony | 电话服务 |
| testfwk | 测试子系统 |
| theme | 主题 |
| time | 时间时区 |
| usb | USB服务 |
| useriam | 用户IAM |
| validator/acts_validator/entry/src/main/ets/pages/PCS | XTS专项小组 |
| web | Web |

## 使用方法

```python
SUBSYSTEM_MAPPING = {
    "ability/ability_runtime": "元能力",
    "ability/crossplatform": "元能力",
    "ability/form": "卡片框架",
    "account": "账号",
    "ai": "AI",
    "applications/settingsdata": "应用设置",
    "arkcompiler": "语言编译运行时",
    "arkui": "ArkUI",
    "bundlemanager": "包管理",
    "commonlibrary": "语言编译运行时",
    "communication/bluetooth_ble": "短距",
    "communication/bluetooth_bp": "短距",
    "communication/bluetooth_br": "短距",
    "communication/bluetooth_nop": "短距",
    "communication/btmanager_errorcode401": "短距",
    "communication/btmanager_switchoff": "短距",
    "communication/dsoftbus": "软总线",
    "communication/netmanager_base": "短距",
    "communication/nfc_Controller": "短距",
    "communication/nfc_ErrorCode": "短距",
    "communication/nfc_Permissions": "短距",
    "communication/nfc_SecureElement": "短距",
    "communication/nfc_SecureElement_2": "短距",
    "communication/wifi_ErrorCode201": "短距",
    "communication/wifi_ErrorCode401": "短距",
    "communication/wifi_enterprise": "短距",
    "communication/wifi_ets_standard": "短距",
    "communication/wifi_manager_nop": "短距",
    "communication/wifi_p10p": "短距",
    "communication/wifi_p11p": "短距",
    "communication/wifi_p12p": "短距",
    "communication/wifi_p13p": "短距",
    "communication/wifi_p14p": "短距",
    "communication/wifi_p15p": "短距",
    "communication/wifi_p16p": "短距",
    "communication/wifi_p17p": "短距",
    "communication/wifi_p18p": "短距",
    "communication/wifi_p19p": "短距",
    "communication/wifi_p2p": "短距",
    "communication/wifi_p20p": "短距",
    "communication/wifi_p21p": "短距",
    "communication/wifi_p22p": "短距",
    "communication/wifi_p23p": "短距",
    "communication/wifi_p24p": "短距",
    "communication/wifi_p25p": "短距",
    "communication/wifi_p26p": "短距",
    "communication/wifi_p27p": "短距",
    "communication/wifi_p28p": "短距",
    "communication/wifi_p29p": "短距",
    "communication/wifi_p3p": "短距",
    "communication/wifi_p30p": "短距",
    "communication/wifi_p31p": "短距",
    "communication/wifi_p32p": "短距",
    "communication/wifi_p33p": "短距",
    "communication/wifi_p34p": "短距",
    "communication/wifi_p35p": "短距",
    "communication/wifi_p36p": "短距",
    "communication/wifi_p37p": "短距",
    "communication/wifi_p38p": "短距",
    "communication/wifi_p39p": "短距",
    "communication/wifi_p3p": "短距",
    "communication/wifi_p40p": "短距",
    "communication/wifi_p41p": "短距",
    "communication/wifi_p4p": "短距",
    "communication/wifi_p5p": "短距",
    "communication/wifi_p6p": "短距",
    "communication/wifi_p7p": "短距",
    "communication/wifi_p8p": "短距",
    "communication/wifi_p9p": "短距",
    "communication/wifi_standard": "短距",
    "customization": "定制化",
    "distributeddatamgr": "分布式数据",
    "global": "全球化",
    "graphic": "图形图像",
    "hdf": "驱动",
    "hiviewdfx": "DFX",
    "inputmethod": "输入法",
    "location": "位置服务",
    "multimedia/audio": "音频",
    "multimedia/avsource": "视频框架",
    "multimedia/camera": "相机图库框架",
    "multimedia/image": "相机图库框架",
    "multimedia/media": "视频框架",
    "multimedia/photoAccess": "相机图库框架",
    "multimodalinput": "多模输入",
    "pcs": "XTS专项小组",
    "print": "打印框架",
    "resourceschedule": "全局资源调度",
    "security": "安全",
    "security/certificate_manager": "安全",
    "storage": "文件管理",
    "telephony": "电话服务",
    "testfwk": "测试子系统",
    "theme": "主题",
    "time": "时间时区",
    "usb": "USB服务",
    "useriam": "用户IAM",
    "validator/acts_validator/entry/src/main/ets/pages/PCS": "XTS专项小组",
    "web": "Web",
}

# 按目录长度降序排列，优先匹配最长前缀
SORTED_DIRS = sorted(SUBSYSTEM_MAPPING.keys(), key=len, reverse=True)

def get_subsystem(file_path: str) -> str:
    """
    根据文件相对路径查找所属子系统

    Args:
        file_path: 文件相对路径（如 'ability/ability_runtime/xxx.test.ets'）

    Returns:
        所属子系统名称，未匹配到返回 '-'
    """
    file_path = file_path.replace("\\", "/")
    for dir_prefix in SORTED_DIRS:
        if file_path.startswith(dir_prefix + "/") or file_path.startswith(dir_prefix + "\\"):
            return SUBSYSTEM_MAPPING[dir_prefix]
    return "-"
```

## 数据来源

- 源文件: `/home/xianf/copy/所属子系统.xlsx`
- 更新日期: 2026-04-07
- 总目录数: 98
