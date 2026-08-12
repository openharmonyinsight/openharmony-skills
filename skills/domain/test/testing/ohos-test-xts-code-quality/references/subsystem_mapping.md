# 目录-子系统映射表

扫描结果生成报告时，根据问题文件的相对路径匹配本映射表，自动填充"所属子系统"列。

## 映射规则

1. 取问题文件的相对路径（相对于扫描根目录）
2. 优先匹配双级目录（如 `ability/ability_runtime`），其次匹配单级目录（如 `advertising`）
3. 按最长前缀匹配，确保精确匹配优先于推断
4. 未匹配到则填 `-`

## 映射数据

| 目录 | 所属子系统 | 备注 |
|------|-----------|------|
| distributeddatamgr/PasteboardPermissionTestTaiheStatic | 分布式数据 |  |
| distributeddatamgr/dataObjectEtsNoPermissions_static | 分布式数据 |  |
| security/data_identify_annoymize_service_SuccessTest | 安全 |  |
| distributeddatamgr/PasteboardNdkWithPermissionsTest | 分布式数据 |  |
| distributeddatamgr/PasteboardJSWithPermissionTest | 分布式数据 |  |
| distributeddatamgr/relationalstoredatagroupidtest | 分布式数据 |  |
| distributeddatamgr/RelationalStoreEtsTestStatic | 分布式数据 |  |
| graphic/acts_graphicXTSDrawingPathEffect_static | 图形图像 |  |
| distributeddatamgr/DataObjectNoPermissionstest | 分布式数据 |  |
| distributeddatamgr/PasteboardNoPermissionstest | 分布式数据 |  |
| distributeddatamgr/RdbWithPermisionTestStatic | 分布式数据 |  |
| distributeddatamgr/preferencesdatagroupidtest | 分布式数据 |  |
| distributeddatamgr/PasteboardTaiheTestStatic | 分布式数据 |  |
| multimodalinput/multimodalinput_ets_standard | 多模输入 |  |
| storage/storagedownloadcloudsyncjsteststatic | 文件管理 |  |
| distributeddatamgr/preferencesNdktestHvigor | 分布式数据 |  |
| graphic/acts_graphicXTSDrawingCanvas_static | 图形图像 |  |
| graphic/acts_graphicXTSDrawingRegion_static | 图形图像 |  |
| arkui/ace_c_arkui_nowear_test_api15_static | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api18_static | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api19_static | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api20_static | ArkUI |  |
| customization/enterprise_device_management | 定制化 |  |
| distributeddatamgr/intelligenceTest_static | 分布式数据 |  |
| distributeddatamgr/preferencesSendabletest | 分布式数据 |  |
| graphic/acts_graphicXTSDrawingBrush_static | 图形图像 |  |
| inputmethod/InputMethodAuthorityTestStatic | 输入法 |  |
| multimodalinput/multimodalinput_ets_hvigor | 多模输入 |  |
| multimodalinput/multimodalinput_ndk_hvigor | 多模输入 |  |
| resourceschedule/resourceschedule_standard | 全局资源调度 |  |
| distributeddatamgr/distributedKVStoretest | 分布式数据 |  |
| graphic/acts_graphicXTSDrawingFont_static | 图形图像 |  |
| graphic/acts_graphicXTSDrawingPath_static | 图形图像 |  |
| security/ActsCryptoFrameworkNapiBasicTest | 安全 |  |
| arkcompiler/arkts_ani_test_static_group1 | 语言编译运行时 |  |
| arkcompiler/arkts_ani_test_static_group5 | 语言编译运行时 |  |
| arkcompiler/arkts_module_normalized_test | 语言编译运行时 |  |
| communication/btmanager_switchoff_static | 短距 |  |
| graphic/acts_graphicXTSDrawingPen_static | 图形图像 |  |
| storage/storagesecuritylabeljsteststatic | 文件管理 |  |
| arkui/ace_c_accessibility_api_16_static | ArkUI |  |
| distributeddatamgr/KvStoreEtsTestStatic | 分布式数据 |  |
| distributeddatamgr/PasteboardTestStatic | 分布式数据 |  |
| distributeddatamgr/dataObjectEts_static | 分布式数据 |  |
| distributeddatamgr/pasteboard_errorcode | 分布式数据 |  |
| distributeddatamgr/preferenceEts_static | 分布式数据 |  |
| distributeddatamgr/preferencesTestApi20 | 分布式数据 |  |
| inputmethod/InputMethodWindManageStatic | 输入法 |  |
| arkui/ace_ets_component_apilack_static | ArkUI |  |
| distributeddatamgr/IntelligenceApiTest | 分布式数据 |  |
| distributeddatamgr/Pasteboardjsapitest | 分布式数据 |  |
| distributeddatamgr/dataShareEts_static | 分布式数据 |  |
| distributeddatamgr/relationalStoretest | 分布式数据 |  |
| inputmethod/InputMethodTest_ets_static | 输入法 |  |
| storage/storagedownloadcloudsyncjstest | 文件管理 |  |
| storage/storageenvironmentjsteststatic | 文件管理 |  |
| arkui/ace_c_arkui_testwearcrop_static | ArkUI |  |
| arkui/ace_ets_component_common_attrss | ArkUI |  |
| distributeddatamgr/Pasteboardnapitest | 分布式数据 |  |
| distributeddatamgr/dataAbilityEtsTest | 分布式数据 |  |
| distributeddatamgr/preferencesEtstest | 分布式数据 |  |
| graphic/acts_graphicXTSDrawing_static | 图形图像 |  |
| inputmethod/InputMethodListTestStatic | 输入法 |  |
| communication/btmanager_errorcode401 | 短距 |  |
| distributeddatamgr/preferencesjstest | 分布式数据 |  |
| graphic/ActsGraphicGlesExtensionTest | 图形图像 |  |
| graphic/acts_windowCompatibilityTest | 图形图像 |  |
| inputmethod/InputMethodAuthorityTest | 输入法 |  |
| print/PrintXtsTestNoPermissionStatic | 打印框架 |  |
| storage/storagebackupextensionjstest | 文件管理 |  |
| storage/storagefilesharejsteststatic | 文件管理 |  |
| arkui/ace_c_arkui_nowear_test_api14 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api15 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api18 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api19 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api20 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api21 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api23 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api24 | ArkUI |  |
| arkui/ace_c_arkui_nowear_test_api26 | ArkUI |  |
| arkui/ace_c_arkui_test_api14_static | ArkUI |  |
| arkui/ace_c_arkui_test_api15_static | ArkUI |  |
| arkui/ace_c_arkui_test_api16_static | ArkUI |  |
| arkui/ace_c_arkui_test_api17_static | ArkUI |  |
| arkui/ace_c_arkui_test_api18_static | ArkUI |  |
| arkui/ace_c_arkui_test_api19_static | ArkUI |  |
| arkui/ace_c_arkui_test_api20_static | ArkUI |  |
| distributeddatamgr/dataShare_Static | 分布式数据 |  |
| distributedhardware/mechanicmanager | 分布式硬件 |  |
| inputmethod/InputMethodDrawnControl | 输入法 |  |
| inputmethod/InputMethodEngineStatic | 输入法 |  |
| location/geolocation_GeocoderStatic | 位置服务 |  |
| location/geolocation_GeofenceStatic | 位置服务 |  |
| storage/storagefileiov9jsteststatic | 文件管理 |  |
| storage/storagepcpickerjsteststatic | 文件管理 |  |
| storage/storagestatisticsteststatic | 文件管理 |  |
| arkui/ace_c_arkui_test_parallelize | ArkUI |  |
| communication/bluetooth_ble_static | 短距 |  |
| communication/bluetooth_nop_static | 短距 |  |
| customization/config_policy_static | 定制化 |  |
| distributeddatamgr/dataSharejstest | 分布式数据 |  |
| storage/storagefileurijsteststatic | 文件管理 |  |
| storage/storagesecuritylabeljstest | 文件管理 |  |
| arkcompiler/arkts_ani_test_static | 语言编译运行时 |  |
| arkui/ActsAceEngineNDK_API20_Test | ArkUI |  |
| communication/bluetooth_bp_static | 短距 |  |
| communication/bluetooth_br_static | 短距 |  |
| communication/btmanager_switchoff | 短距 |  |
| communication/netstack_socket_nop | 短距 |  |
| communication/nfc_SecureElement_2 | 短距 |  |
| distributeddatamgr/dataObjecttest | 分布式数据 |  |
| graphic/ActsGraphicVulkanNapiTest | 图形图像 |  |
| inputmethod/InputMethodTest_Stage | 输入法 |  |
| inputmethod/InputMethodWindManage | 输入法 |  |
| multimodalinput/input_js_standard | 多模输入 |  |
| storage/backupextensionteststatic | 文件管理 |  |
| storage/storageenvironmentndktest | 文件管理 |  |
| storage/storagefilemanagementtest | 文件管理 |  |
| storage/storagenopermissionjstest | 文件管理 |  |
| storage/storagepickerjsteststatic | 文件管理 |  |
| storage/storagestatfsjsteststatic | 文件管理 |  |
| arkui/ace_c_accessibility_api_16 | ArkUI |  |
| arkui/ace_c_scroll_crosslanguage | ArkUI |  |
| arkui/ace_ets_component_advanced | ArkUI |  |
| distributeddatamgr/crossplatform | 分布式数据 |  |
| distributeddatamgr/dataShareTest | 分布式数据 |  |
| graphic/graphicDisplaySyncStatic | 图形图像 |  |
| hiviewdfx/hitracechainteststatic | DFX |  |
| hiviewdfx/hitracemeterteststatic | DFX |  |
| inputmethod/InputmethodTestApi20 | 输入法 |  |
| location/geolocation_capi20_test | 位置服务 |  |
| storage/storageenvironmentjstest | 文件管理 |  |
| storage/storagefileioerrorjstest | 文件管理 |  |
| testfwk/uitest_quarantine_static | 测试子系统 |  |
| web/web_page_document_processing | Web |  |
| account/OsAccountTest_js_static | 账号 |  |
| arkui/ace_ets_component_apilack | ArkUI |  |
| communication/netstack_http_nop | 短距 |  |
| communication/nfc_SecureElement | 短距 |  |
| communication/wifi_ErrorCode201 | 短距 |  |
| communication/wifi_ErrorCode401 | 短距 |  |
| communication/wifi_ets_standard | 短距 |  |
| graphic/ActsGraphicNapiFontTest | 图形图像 |  |
| graphic/graphicColorSpaceStatic | 图形图像 |  |
| graphic/nativeDisplaySoloistNdk | 图形图像 |  |
| graphic/windowLifeCycleTestDemo | 图形图像 |  |
| hiviewdfx/apprecoveryteststatic | DFX |  |
| inputmethod/InputMethodListTest | 输入法 |  |
| inputmethod/InputMethodTest_ets | 输入法 |  |
| location/geolocation_CoreStatic | 位置服务 |  |
| location/geolocation_GnssStatic | 位置服务 |  |
| location/geolocation_capiStatic | 位置服务 |  |
| security/dlp_permission_service | 安全 |  |
| storage/storageclouddiskndktest | 文件管理 |  |
| storage/storagefilesharendktest | 文件管理 |  |
| storage/storagestatisticsjstest | 文件管理 |  |
| testfwk/uitest_errorcode_static | 测试子系统 |  |
| arkui/ace_c_arkui_test_api15XC | ArkUI |  |
| arkui/ace_c_arkui_testwearcrop | ArkUI |  |
| communication/wifi_manager_nop | 短距 |  |
| distributeddatamgr/kvStoretest | 分布式数据 |  |
| graphic/acts_graphicXTSDrawing | 图形图像 |  |
| graphic/graphicEffectKitStatic | 图形图像 |  |
| inputmethod/InputMethodEditBox | 输入法 |  |
| inputmethod/InputMethodNDKTest | 输入法 |  |
| location/geolocation_NopStatic | 位置服务 |  |
| location/geolocation_errorCode | 位置服务 |  |
| security/certificate_framework | 安全 |  |
| storage/storagefilesharejstest | 文件管理 |  |
| usb/usb_perstandard_ets_static | USB服务 |  |
| arkcompiler/arkts_module_test | 语言编译运行时 |  |
| arkui/ace_c_arkui_test_api151 | ArkUI |  |
| arkui/ace_c_arkui_test_static | ArkUI |  |
| arkui/ace_ets_component_seven | ArkUI |  |
| bundlemanager/bundle_standard | 包管理 |  |
| communication/netmanager_base | 短距 |  |
| communication/nfc_Permissions | 短距 |  |
| communication/wifi_enterprise | 短距 |  |
| graphic/graphicUiEffectStatic | 图形图像 |  |
| inputmethod/InputMethodEngine | 输入法 |  |
| location/geolocation_standard | 位置服务 |  |
| storage/storagefileiov9jstest | 文件管理 |  |
| storage/storagefileurindktest | 文件管理 |  |
| storage/storagepcpickerjstest | 文件管理 |  |
| theme/wallpaper_authority_ets | 主题 |  |
| useriam/user_auth_icon_static | 用户IAM |  |
| arkui/ace_c_arkui_test_api13 | ArkUI |  |
| arkui/ace_c_arkui_test_api14 | ArkUI |  |
| arkui/ace_c_arkui_test_api15 | ArkUI |  |
| arkui/ace_c_arkui_test_api16 | ArkUI |  |
| arkui/ace_c_arkui_test_api17 | ArkUI |  |
| arkui/ace_c_arkui_test_api18 | ArkUI |  |
| arkui/ace_c_arkui_test_api19 | ArkUI |  |
| arkui/ace_c_arkui_test_api20 | ArkUI |  |
| arkui/ace_c_arkui_test_api21 | ArkUI |  |
| arkui/ace_c_arkui_test_api22 | ArkUI |  |
| arkui/ace_c_arkui_test_api23 | ArkUI |  |
| arkui/ace_c_arkui_test_api24 | ArkUI |  |
| arkui/ace_c_arkui_test_api26 | ArkUI |  |
| communication/nfc_Controller | 短距 |  |
| communication/wifi_switchoff | 短距 |  |
| hiviewdfx/hitracechainjstest | DFX |  |
| print/print_nopermission_xts | 打印框架 |  |
| security/certificate_manager | 安全 |  |
| security/crypto_architecture | 安全 |  |
| storage/storagefileiondktest | 文件管理 |  |
| storage/storagefileurijstest | 文件管理 |  |
| web/application_interworking | Web |  |
| arkcompiler/ecmanewfeatures | 语言编译运行时 |  |
| communication/bluetooth_ble | 短距 |  |
| communication/bluetooth_nop | 短距 |  |
| communication/nfc_ErrorCode | 短距 |  |
| communication/wifi_standard | 短距 |  |
| customization/config_policy | 定制化 |  |
| distributeddatamgr/UDMFtest | 分布式数据 |  |
| graphic/graphics2DTestApi20 | 图形图像 |  |
| graphic/nativeColorSpaceNdk | 图形图像 |  |
| hiviewdfx/hilogtsteststatic | DFX |  |
| print/print_errorcode_noPer | 打印框架 |  |
| security/dlp_errorcode_func | 安全 |  |
| security/security_component | 安全 |  |
| storage/backupextensiontest | 文件管理 |  |
| storage/storagefileiojstest | 文件管理 |  |
| storage/storagepickerjstest | 文件管理 |  |
| storage/storagestatfsjstest | 文件管理 |  |
| theme/screenlock_ets_static | 主题 |  |
| usb/usb_standard_ets_static | USB服务 |  |
| account/actspermissiontest | 账号 |  |
| arkui/ace_js_attribute_api | ArkUI |  |
| commonlibrary/memory_utils | 语言编译运行时 |  |
| communication/bluetooth_bp | 短距 |  |
| communication/bluetooth_br | 短距 |  |
| global/global_stage_static | 全球化 |  |
| graphic/graphicDisplaySync | 图形图像 |  |
| graphic/graphicDrawingFont | 图形图像 |  |
| graphic/graphicImageStatic | 图形图像 |  |
| multimedia/avMusicTemplate | 视频框架 |  |
| web/web_content_processing | Web |  |
| ai/neural_network_runtime | AI |  |
| applications/settingsdata | 应用设置 |  |
| arkui/ace_ets_module_noui | ArkUI |  |
| commonlibrary/ark_runtime | 语言编译运行时 |  |
| global/global_napi_c_test | 全球化 |  |
| graphic/graphicColorSpace | 图形图像 |  |
| graphic/graphicTextStatic | 图形图像 |  |
| hiviewdfx/errormangertest | DFX |  |
| location/geolocation_capi | 位置服务 |  |
| storage/storagefilejstest | 文件管理 |  |
| telephony/telephonyjstest | 电话服务 |  |
| account/OsAccountTest_js | 账号 |  |
| arkui/ace_ets_xcomponent | ArkUI |  |
| arkui/ace_standard_video | ArkUI |  |
| commonlibrary/thirdparty | 语言编译运行时 |  |
| communication/fusion_nop | 短距 |  |
| global/i18n_stage_static | 全球化 |  |
| graphic/graphicHdrStatic | 图形图像 |  |
| graphic/windowPermission | 图形图像 |  |
| hiviewdfx/hiappeventtest | DFX |  |
| hiviewdfx/hisyseventtest | DFX |  |
| hiviewdfx/hitracendktest | DFX |  |
| location/geolocation_nop | 位置服务 |  |
| print/PrintXtsTestStatic | 打印框架 |  |
| security/cryptoFramework | 安全 |  |
| telephony/networkmanager | 电话服务 |  |
| testfwk/uitestQuarantine | 测试子系统 |  |
| testfwk/uitest_errorcode | 测试子系统 |  |
| testfwk/uitest_pc_static | 测试子系统 |  |
| validator/acts_validator | XTS专项小组 |  |
| validator/acts_validator/entry/src/main/ets/pages/ArkUI | ArkUI | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Audio | 音频 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Bluetooth | 短距 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Wifi | 短距 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Camera | 相机图库框架 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Player | 相机图库框架 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Experience | XTS专项小组 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/PCS | XTS专项小组 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/MultimodalInput | 多模输入 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Notification | 事件通知 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Power | 电源服务 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Screen | 窗口 | 根据pages子目录判断 |
| validator/acts_validator/entry/src/main/ets/pages/Sensor | 泛Sensor | 根据pages子目录判断 |
| web/web_security_privacy | Web |  |
| ability/ability_runtime | 元能力 |  |
| arkui/ace_ets_module_ui | ArkUI |  |
| commonlibrary/ets_utils | 语言编译运行时 |  |
| global/global_idna_test | 全球化 |  |
| global/global_napi_test | 全球化 |  |
| global/i18n_util_static | 全球化 |  |
| graphic/LandscapeWindow | 图形图像 |  |
| graphic/displayNdkApi14 | 图形图像 |  |
| graphic/graphicImageNdk | 图形图像 |  |
| graphic/graphicUiEffect | 图形图像 |  |
| graphic/nativeEffectNdk | 图形图像 |  |
| hiviewdfx/hicheckertest | DFX |  |
| time/dateTimeTestStatic | 时间时区 |  |
| usb/usb_standard_serial | USB服务 |  |
| communication/wifi_p10p | 短距 |  |
| communication/wifi_p11p | 短距 |  |
| communication/wifi_p12p | 短距 |  |
| communication/wifi_p13p | 短距 |  |
| communication/wifi_p14p | 短距 |  |
| communication/wifi_p15p | 短距 |  |
| communication/wifi_p16p | 短距 |  |
| communication/wifi_p17p | 短距 |  |
| communication/wifi_p18p | 短距 |  |
| communication/wifi_p19p | 短距 |  |
| communication/wifi_p20p | 短距 |  |
| communication/wifi_p21p | 短距 |  |
| communication/wifi_p22p | 短距 |  |
| communication/wifi_p23p | 短距 |  |
| communication/wifi_p24p | 短距 |  |
| communication/wifi_p25p | 短距 |  |
| communication/wifi_p26p | 短距 |  |
| communication/wifi_p27p | 短距 |  |
| communication/wifi_p28p | 短距 |  |
| communication/wifi_p29p | 短距 |  |
| communication/wifi_p30p | 短距 |  |
| communication/wifi_p31p | 短距 |  |
| communication/wifi_p32p | 短距 |  |
| communication/wifi_p33p | 短距 |  |
| communication/wifi_p34p | 短距 |  |
| communication/wifi_p35p | 短距 |  |
| communication/wifi_p36p | 短距 |  |
| communication/wifi_p37p | 短距 |  |
| communication/wifi_p38p | 短距 |  |
| communication/wifi_p39p | 短距 |  |
| communication/wifi_p40p | 短距 |  |
| arkui/ace_c_arkui_test | ArkUI |  |
| arkui/ace_napi_test_es | ArkUI |  |
| communication/dsoftbus | 软总线 |  |
| global/resmgr_standard | 全球化 |  |
| graphic/acts_pipwindow | 图形图像 |  |
| graphic/displayManager | 图形图像 |  |
| graphic/graphicGLES3v2 | 图形图像 |  |
| graphic/windowStageTwo | 图形图像 |  |
| graphic/windowstandard | 图形图像 |  |
| hiviewdfx/faultlogtest | DFX |  |
| multimedia/photoAccess | 相机图库框架 |  |
| testfwk/perftestStatic | 测试子系统 |  |
| time/timeauthorityTest | 时间时区 |  |
| useriam/user_auth_icon | 用户IAM |  |
| web/network_management | Web |  |
| web/web_engine_version | Web |  |
| web/web_page_rendering | Web |  |
| communication/wifi_p3p | 短距 |  |
| communication/wifi_p4p | 短距 |  |
| communication/wifi_p5p | 短距 |  |
| communication/wifi_p6p | 短距 |  |
| communication/wifi_p7p | 短距 |  |
| communication/wifi_p8p | 短距 |  |
| communication/wifi_p9p | 短距 |  |
| ability/crossplatform | 元能力 |  |
| arkui/ace_ets_ux_five | ArkUI |  |
| graphic/nativeFontNdk | 图形图像 |  |
| graphic/nativedrawing | 图形图像 |  |
| hiviewdfx/bytracetest | DFX |  |
| hiviewdfx/hidebugtest | DFX |  |
| print/print_errorcode | 打印框架 |  |
| security/access_token | 安全 |  |
| security/dlpNDK20Test | 安全 |  |
| testfwk/perftestScene | 测试子系统 |  |
| web/web_connectNative | Web |  |
| arkcompiler/esmodule | 语言编译运行时 |  |
| arkui/ace_ets_ux_one | ArkUI |  |
| communication/fusion | 短距 |  |
| global/i18n_standard | 全球化 |  |
| graphic/acts_display | 图形图像 |  |
| graphic/graphicGLES3 | 图形图像 |  |
| graphic/graphicImage | 图形图像 |  |
| graphic/nativebuffer | 图形图像 |  |
| testfwk/uitestStatic | 测试子系统 |  |
| theme/screenlock_ets | 主题 |  |
| usb/usb_standard_ets | USB服务 |  |
| web/page_interaction | Web |  |
| account/account_ndk | 账号 |  |
| arkui/ace_napi_test | ArkUI |  |
| global/global_stage | 全球化 |  |
| graphic/component3D | 图形图像 |  |
| graphic/graphicText | 图形图像 |  |
| graphic/nativefence | 图形图像 |  |
| graphic/nativeimage | 图形图像 |  |
| graphic/windowStage | 图形图像 |  |
| multimedia/avsource | 视频框架 |  |
| security/el5filekey | 安全 |  |
| telephony/telephone | 电话服务 |  |
| testfwk/uitestScene | 测试子系统 |  |
| theme/wallpaper_ets | 主题 |  |
| web/web_multi_media | Web |  |
| web/web_switch_core | Web |  |
| web/web_zoom_access | Web |  |
| distributedhardware | 分布式硬件 | 推断 |
| account/appaccount | 账号 |  |
| arkui/ace_standard | ArkUI |  |
| bundlemanager/zlib | 包管理 |  |
| graphic/displayNdk | 图形图像 |  |
| graphic/graphicGL4 | 图形图像 |  |
| graphic/graphicHdr | 图形图像 |  |
| hdf/device_manager | 驱动 |  |
| web/web_life_cycle | Web |  |
| web/web_multimedia | Web |  |
| distributeddatamgr | 分布式数据 | 推断 |
| account/osaccount | 账号 |  |
| global/i18n_stage | 全球化 |  |
| graphic/effectKit | 图形图像 |  |
| graphic/graphic3D | 图形图像 |  |
| graphic/windowNdk | 图形图像 |  |
| multimedia/camera | 相机图库框架 |  |
| testfwk/uitest_pc | 测试子系统 |  |
| time/dateTimeTest | 时间时区 |  |
| useriam/face_auth | 用户IAM |  |
| useriam/user_auth | 用户IAM |  |
| hiviewdfx/hiview | DFX |  |
| multimedia/audio | 音频 |  |
| multimedia/image | 相机图库框架 |  |
| multimedia/media | 视频框架 |  |
| security/sandbox | 安全 |  |
| testfwk/perftest | 测试子系统 |  |
| time/timeNDKTest | 时间时区 |  |
| usb/usb_standard | USB服务 |  |
| resourceschedule | 全局资源调度 | 推断 |
| advertising/ads | 广告服务 |  |
| print/print_xts | 打印框架 |  |
| security/cipher | 安全 |  |
| web/web_storage | Web |  |
| multimodalinput | 多模输入 | 推断 |
| ability/dmsfwk | 元能力 |  |
| security/asset | 安全 |  |
| testfwk/uitest | 测试子系统 |  |
| web/web_device | Web |  |
| graphic/webGL | 图形图像 |  |
| hdf/errorcode | 驱动 |  |
| hdf/selection | 驱动 |  |
| pcs/pcs_arkts | XTS专项小组 |  |
| security/huks | 安全 |  |
| time/timeTest | 时间时区 |  |
| bundlemanager | 包管理 | 推断 |
| commonlibrary | 语言编译运行时 | 推断 |
| communication | 短距 | 推断 |
| customization | 定制化 | 推断 |
| officeservice | 办公服务 | 推断 |
| ability/form | 卡片框架 |  |
| ai/mindspore | AI |  |
| web/web_jump | Web |  |
| web/web_load | Web |  |
| applications | 应用设置 | 推断 |
| notification | 事件通知 | 推断 |
| pcs/pcs_ndk | XTS专项小组 |  |
| web/web_dfx | Web |  |
| web/web_net | Web |  |
| advertising | 广告服务 | 推断 |
| arkcompiler | 语言编译运行时 | 推断 |
| barrierfree | 无障碍服务 | 推断 |
| inputmethod | 输入法 | 推断 |
| pcs/pcs_js | XTS专项小组 |  |
| ai/nncore | AI |  |
| hiviewdfx | DFX | 推断 |
| telephony | 电话服务 | 推断 |
| validator | XTS专项小组 | 推断 |
| hdf/base | 驱动 |  |
| location | 位置服务 | 推断 |
| powermgr | 电源服务 | 推断 |
| security | 安全 | 推断 |
| hdf/hid | 驱动 |  |
| hdf/usb | 驱动 |  |
| web/DFX | Web |  |
| ability | 元能力 | 推断 |
| account | 账号 | 推断 |
| graphic | 图形图像 | 推断 |
| request | 上传下载 | 推断 |
| sensors | 泛Sensor | 推断 |
| startup | 启动子系统 | 推断 |
| storage | 文件管理 | 推断 |
| testfwk | 测试子系统 | 推断 |
| updater | 升级子系统 | 推断 |
| useriam | 用户IAM | 推断 |
| global | 全球化 | 推断 |
| ostest | 应用测试 | 推断 |
| window | 窗口 | 推断 |
| arkui | ArkUI | 推断 |
| print | 打印框架 | 推断 |
| theme | 主题 | 推断 |
| demo | 示例 | 推断 |
| game | 游戏 | 推断 |
| msdp | MSDP | 推断 |
| time | 时间时区 | 推断 |
| hdf | 驱动 | 推断 |
| pcs | XTS专项小组 | 推断 |
| tee | TEE | 推断 |
| usb | USB服务 | 推断 |
| web | Web | 推断 |
| xts | XTS专项小组 | 推断 |
| ai | AI | 推断 |

总计: 479 条映射 (431 条精确 + 48 条推断), 50 个子系统