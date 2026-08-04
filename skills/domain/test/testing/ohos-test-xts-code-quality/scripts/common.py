#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""XTS Test Code Quality Scanner - Common Utilities

This module contains shared utility code used by all rule scanners:
- Subsystem mapping
- File type detection and collection
- Comment stripping
- Brace matching (string-aware)
- it()/describe() block parsing
- Independent XTS project finder
- Assertion pattern detection
- Excel report generation

NOTE: When references/subsystem_mapping.md is updated, SUBSYSTEM_MAPPING
must be synced accordingly.
"""
import os, re, sys, json, collections, logging, subprocess, shutil, threading
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook

# ======================== SUBSYSTEM MAPPING ========================
# Source: references/subsystem_mapping.md
# Sync rule: Run sync_subsystem_mapping.py when subsystem_mapping.md changes

SUBSYSTEM_MAPPING = {
    "distributeddatamgr/PasteboardPermissionTestTaiheStatic": "分布式数据", "distributeddatamgr/dataObjectEtsNoPermissions_static": "分布式数据", "security/data_identify_annoymize_service_SuccessTest": "安全", "distributeddatamgr/PasteboardNdkWithPermissionsTest": "分布式数据",
    "distributeddatamgr/PasteboardJSWithPermissionTest": "分布式数据", "distributeddatamgr/relationalstoredatagroupidtest": "分布式数据", "distributeddatamgr/RelationalStoreEtsTestStatic": "分布式数据", "graphic/acts_graphicXTSDrawingPathEffect_static": "图形图像",
    "distributeddatamgr/DataObjectNoPermissionstest": "分布式数据", "distributeddatamgr/PasteboardNoPermissionstest": "分布式数据", "distributeddatamgr/RdbWithPermisionTestStatic": "分布式数据", "distributeddatamgr/preferencesdatagroupidtest": "分布式数据",
    "distributeddatamgr/PasteboardTaiheTestStatic": "分布式数据", "multimodalinput/multimodalinput_ets_standard": "多模输入", "storage/storagedownloadcloudsyncjsteststatic": "文件管理", "distributeddatamgr/preferencesNdktestHvigor": "分布式数据",
    "graphic/acts_graphicXTSDrawingCanvas_static": "图形图像", "graphic/acts_graphicXTSDrawingRegion_static": "图形图像", "arkui/ace_c_arkui_nowear_test_api15_static": "ArkUI", "arkui/ace_c_arkui_nowear_test_api18_static": "ArkUI",
    "arkui/ace_c_arkui_nowear_test_api19_static": "ArkUI", "arkui/ace_c_arkui_nowear_test_api20_static": "ArkUI", "customization/enterprise_device_management": "定制化", "distributeddatamgr/intelligenceTest_static": "分布式数据",
    "distributeddatamgr/preferencesSendabletest": "分布式数据", "graphic/acts_graphicXTSDrawingBrush_static": "图形图像", "inputmethod/InputMethodAuthorityTestStatic": "输入法", "multimodalinput/multimodalinput_ets_hvigor": "多模输入",
    "multimodalinput/multimodalinput_ndk_hvigor": "多模输入", "resourceschedule/resourceschedule_standard": "全局资源调度", "distributeddatamgr/distributedKVStoretest": "分布式数据", "graphic/acts_graphicXTSDrawingFont_static": "图形图像",
    "graphic/acts_graphicXTSDrawingPath_static": "图形图像", "security/ActsCryptoFrameworkNapiBasicTest": "安全", "arkcompiler/arkts_ani_test_static_group1": "语言编译运行时", "arkcompiler/arkts_ani_test_static_group5": "语言编译运行时",
    "arkcompiler/arkts_module_normalized_test": "语言编译运行时", "communication/btmanager_switchoff_static": "短距", "graphic/acts_graphicXTSDrawingPen_static": "图形图像", "storage/storagesecuritylabeljsteststatic": "文件管理",
    "arkui/ace_c_accessibility_api_16_static": "ArkUI", "distributeddatamgr/KvStoreEtsTestStatic": "分布式数据", "distributeddatamgr/PasteboardTestStatic": "分布式数据", "distributeddatamgr/dataObjectEts_static": "分布式数据",
    "distributeddatamgr/pasteboard_errorcode": "分布式数据", "distributeddatamgr/preferenceEts_static": "分布式数据", "distributeddatamgr/preferencesTestApi20": "分布式数据", "inputmethod/InputMethodWindManageStatic": "输入法",
    "arkui/ace_ets_component_apilack_static": "ArkUI", "distributeddatamgr/IntelligenceApiTest": "分布式数据", "distributeddatamgr/Pasteboardjsapitest": "分布式数据", "distributeddatamgr/dataShareEts_static": "分布式数据",
    "distributeddatamgr/relationalStoretest": "分布式数据", "inputmethod/InputMethodTest_ets_static": "输入法", "storage/storagedownloadcloudsyncjstest": "文件管理", "storage/storageenvironmentjsteststatic": "文件管理",
    "arkui/ace_c_arkui_testwearcrop_static": "ArkUI", "arkui/ace_ets_component_common_attrss": "ArkUI", "distributeddatamgr/Pasteboardnapitest": "分布式数据", "distributeddatamgr/dataAbilityEtsTest": "分布式数据",
    "distributeddatamgr/preferencesEtstest": "分布式数据", "graphic/acts_graphicXTSDrawing_static": "图形图像", "inputmethod/InputMethodListTestStatic": "输入法", "communication/btmanager_errorcode401": "短距",
    "distributeddatamgr/preferencesjstest": "分布式数据", "graphic/ActsGraphicGlesExtensionTest": "图形图像", "graphic/acts_windowCompatibilityTest": "图形图像", "inputmethod/InputMethodAuthorityTest": "输入法",
    "print/PrintXtsTestNoPermissionStatic": "打印框架", "storage/storagebackupextensionjstest": "文件管理", "storage/storagefilesharejsteststatic": "文件管理", "arkui/ace_c_arkui_nowear_test_api14": "ArkUI",
    "arkui/ace_c_arkui_nowear_test_api15": "ArkUI", "arkui/ace_c_arkui_nowear_test_api18": "ArkUI", "arkui/ace_c_arkui_nowear_test_api19": "ArkUI", "arkui/ace_c_arkui_nowear_test_api20": "ArkUI",
    "arkui/ace_c_arkui_nowear_test_api21": "ArkUI", "arkui/ace_c_arkui_nowear_test_api23": "ArkUI", "arkui/ace_c_arkui_nowear_test_api24": "ArkUI", "arkui/ace_c_arkui_nowear_test_api26": "ArkUI",
    "arkui/ace_c_arkui_test_api14_static": "ArkUI", "arkui/ace_c_arkui_test_api15_static": "ArkUI", "arkui/ace_c_arkui_test_api16_static": "ArkUI", "arkui/ace_c_arkui_test_api17_static": "ArkUI",
    "arkui/ace_c_arkui_test_api18_static": "ArkUI", "arkui/ace_c_arkui_test_api19_static": "ArkUI", "arkui/ace_c_arkui_test_api20_static": "ArkUI", "distributeddatamgr/dataShare_Static": "分布式数据",
    "distributedhardware/mechanicmanager": "分布式硬件", "inputmethod/InputMethodDrawnControl": "输入法", "inputmethod/InputMethodEngineStatic": "输入法", "location/geolocation_GeocoderStatic": "位置服务",
    "location/geolocation_GeofenceStatic": "位置服务", "storage/storagefileiov9jsteststatic": "文件管理", "storage/storagepcpickerjsteststatic": "文件管理", "storage/storagestatisticsteststatic": "文件管理",
    "arkui/ace_c_arkui_test_parallelize": "ArkUI", "communication/bluetooth_ble_static": "短距", "communication/bluetooth_nop_static": "短距", "customization/config_policy_static": "定制化",
    "distributeddatamgr/dataSharejstest": "分布式数据", "storage/storagefileurijsteststatic": "文件管理", "storage/storagesecuritylabeljstest": "文件管理", "arkcompiler/arkts_ani_test_static": "语言编译运行时",
    "arkui/ActsAceEngineNDK_API20_Test": "ArkUI", "communication/bluetooth_bp_static": "短距", "communication/bluetooth_br_static": "短距", "communication/btmanager_switchoff": "短距",
    "communication/netstack_socket_nop": "短距", "communication/nfc_SecureElement_2": "短距", "distributeddatamgr/dataObjecttest": "分布式数据", "graphic/ActsGraphicVulkanNapiTest": "图形图像",
    "inputmethod/InputMethodTest_Stage": "输入法", "inputmethod/InputMethodWindManage": "输入法", "multimodalinput/input_js_standard": "多模输入", "storage/backupextensionteststatic": "文件管理",
    "storage/storageenvironmentndktest": "文件管理", "storage/storagefilemanagementtest": "文件管理", "storage/storagenopermissionjstest": "文件管理", "storage/storagepickerjsteststatic": "文件管理",
    "storage/storagestatfsjsteststatic": "文件管理", "arkui/ace_c_accessibility_api_16": "ArkUI", "arkui/ace_c_scroll_crosslanguage": "ArkUI", "arkui/ace_ets_component_advanced": "ArkUI",
    "distributeddatamgr/crossplatform": "分布式数据", "distributeddatamgr/dataShareTest": "分布式数据", "graphic/graphicDisplaySyncStatic": "图形图像", "hiviewdfx/hitracechainteststatic": "DFX",
    "hiviewdfx/hitracemeterteststatic": "DFX", "inputmethod/InputmethodTestApi20": "输入法", "location/geolocation_capi20_test": "位置服务", "storage/storageenvironmentjstest": "文件管理",
    "storage/storagefileioerrorjstest": "文件管理", "testfwk/uitest_quarantine_static": "测试子系统", "web/web_page_document_processing": "Web", "account/OsAccountTest_js_static": "账号",
    "arkui/ace_ets_component_apilack": "ArkUI", "communication/netstack_http_nop": "短距", "communication/nfc_SecureElement": "短距", "communication/wifi_ErrorCode201": "短距",
    "communication/wifi_ErrorCode401": "短距", "communication/wifi_ets_standard": "短距", "graphic/ActsGraphicNapiFontTest": "图形图像", "graphic/graphicColorSpaceStatic": "图形图像",
    "graphic/nativeDisplaySoloistNdk": "图形图像", "graphic/windowLifeCycleTestDemo": "图形图像", "hiviewdfx/apprecoveryteststatic": "DFX", "inputmethod/InputMethodListTest": "输入法",
    "inputmethod/InputMethodTest_ets": "输入法", "location/geolocation_CoreStatic": "位置服务", "location/geolocation_GnssStatic": "位置服务", "location/geolocation_capiStatic": "位置服务",
    "security/dlp_permission_service": "安全", "storage/storageclouddiskndktest": "文件管理", "storage/storagefilesharendktest": "文件管理", "storage/storagestatisticsjstest": "文件管理",
    "testfwk/uitest_errorcode_static": "测试子系统", "arkui/ace_c_arkui_test_api15XC": "ArkUI", "arkui/ace_c_arkui_testwearcrop": "ArkUI", "communication/wifi_manager_nop": "短距",
    "distributeddatamgr/kvStoretest": "分布式数据", "graphic/acts_graphicXTSDrawing": "图形图像", "graphic/graphicEffectKitStatic": "图形图像", "inputmethod/InputMethodEditBox": "输入法",
    "inputmethod/InputMethodNDKTest": "输入法", "location/geolocation_NopStatic": "位置服务", "location/geolocation_errorCode": "位置服务", "security/certificate_framework": "安全",
    "storage/storagefilesharejstest": "文件管理", "usb/usb_perstandard_ets_static": "USB服务", "arkcompiler/arkts_module_test": "语言编译运行时", "arkui/ace_c_arkui_test_api151": "ArkUI",
    "arkui/ace_c_arkui_test_static": "ArkUI", "arkui/ace_ets_component_seven": "ArkUI", "bundlemanager/bundle_standard": "包管理", "communication/netmanager_base": "短距",
    "communication/nfc_Permissions": "短距", "communication/wifi_enterprise": "短距", "graphic/graphicUiEffectStatic": "图形图像", "inputmethod/InputMethodEngine": "输入法",
    "location/geolocation_standard": "位置服务", "storage/storagefileiov9jstest": "文件管理", "storage/storagefileurindktest": "文件管理", "storage/storagepcpickerjstest": "文件管理",
    "theme/wallpaper_authority_ets": "主题", "useriam/user_auth_icon_static": "用户IAM", "arkui/ace_c_arkui_test_api13": "ArkUI", "arkui/ace_c_arkui_test_api14": "ArkUI",
    "arkui/ace_c_arkui_test_api15": "ArkUI", "arkui/ace_c_arkui_test_api16": "ArkUI", "arkui/ace_c_arkui_test_api17": "ArkUI", "arkui/ace_c_arkui_test_api18": "ArkUI",
    "arkui/ace_c_arkui_test_api19": "ArkUI", "arkui/ace_c_arkui_test_api20": "ArkUI", "arkui/ace_c_arkui_test_api21": "ArkUI", "arkui/ace_c_arkui_test_api22": "ArkUI",
    "arkui/ace_c_arkui_test_api23": "ArkUI", "arkui/ace_c_arkui_test_api24": "ArkUI", "arkui/ace_c_arkui_test_api26": "ArkUI", "communication/nfc_Controller": "短距",
    "communication/wifi_switchoff": "短距", "hiviewdfx/hitracechainjstest": "DFX", "print/print_nopermission_xts": "打印框架", "security/certificate_manager": "安全",
    "security/crypto_architecture": "安全", "storage/storagefileiondktest": "文件管理", "storage/storagefileurijstest": "文件管理", "web/application_interworking": "Web",
    "arkcompiler/ecmanewfeatures": "语言编译运行时", "communication/bluetooth_ble": "短距", "communication/bluetooth_nop": "短距", "communication/nfc_ErrorCode": "短距",
    "communication/wifi_standard": "短距", "customization/config_policy": "定制化", "distributeddatamgr/UDMFtest": "分布式数据", "graphic/graphics2DTestApi20": "图形图像",
    "graphic/nativeColorSpaceNdk": "图形图像", "hiviewdfx/hilogtsteststatic": "DFX", "print/print_errorcode_noPer": "打印框架", "security/dlp_errorcode_func": "安全",
    "security/security_component": "安全", "storage/backupextensiontest": "文件管理", "storage/storagefileiojstest": "文件管理", "storage/storagepickerjstest": "文件管理",
    "storage/storagestatfsjstest": "文件管理", "theme/screenlock_ets_static": "主题", "usb/usb_standard_ets_static": "USB服务", "account/actspermissiontest": "账号",
    "arkui/ace_js_attribute_api": "ArkUI", "commonlibrary/memory_utils": "语言编译运行时", "communication/bluetooth_bp": "短距", "communication/bluetooth_br": "短距",
    "global/global_stage_static": "全球化", "graphic/graphicDisplaySync": "图形图像", "graphic/graphicDrawingFont": "图形图像", "graphic/graphicImageStatic": "图形图像",
    "multimedia/avMusicTemplate": "视频框架", "web/web_content_processing": "Web", "ai/neural_network_runtime": "AI", "applications/settingsdata": "应用设置",
    "arkui/ace_ets_module_noui": "ArkUI", "commonlibrary/ark_runtime": "语言编译运行时", "global/global_napi_c_test": "全球化", "graphic/graphicColorSpace": "图形图像",
    "graphic/graphicTextStatic": "图形图像", "hiviewdfx/errormangertest": "DFX", "location/geolocation_capi": "位置服务", "storage/storagefilejstest": "文件管理",
    "telephony/telephonyjstest": "电话服务", "account/OsAccountTest_js": "账号", "arkui/ace_ets_xcomponent": "ArkUI", "arkui/ace_standard_video": "ArkUI",
    "commonlibrary/thirdparty": "语言编译运行时", "communication/fusion_nop": "短距", "global/i18n_stage_static": "全球化", "graphic/graphicHdrStatic": "图形图像",
    "graphic/windowPermission": "图形图像", "hiviewdfx/hiappeventtest": "DFX", "hiviewdfx/hisyseventtest": "DFX", "hiviewdfx/hitracendktest": "DFX",
    "location/geolocation_nop": "位置服务", "print/PrintXtsTestStatic": "打印框架", "security/cryptoFramework": "安全", "telephony/networkmanager": "电话服务",
    "testfwk/uitestQuarantine": "测试子系统", "testfwk/uitest_errorcode": "测试子系统", "testfwk/uitest_pc_static": "测试子系统", "validator/acts_validator": "XTS专项小组",
    "web/web_security_privacy": "Web", "ability/ability_runtime": "元能力", "arkui/ace_ets_module_ui": "ArkUI", "commonlibrary/ets_utils": "语言编译运行时",
    "global/global_idna_test": "全球化", "global/global_napi_test": "全球化", "global/i18n_util_static": "全球化", "graphic/LandscapeWindow": "图形图像",
    "graphic/displayNdkApi14": "图形图像", "graphic/graphicImageNdk": "图形图像", "graphic/graphicUiEffect": "图形图像", "graphic/nativeEffectNdk": "图形图像",
    "hiviewdfx/hicheckertest": "DFX", "time/dateTimeTestStatic": "时间时区", "usb/usb_standard_serial": "USB服务", "arkui/ace_c_arkui_test": "ArkUI",
    "arkui/ace_napi_test_es": "ArkUI", "communication/dsoftbus": "软总线", "global/resmgr_standard": "全球化", "graphic/acts_pipwindow": "图形图像",
    "graphic/displayManager": "图形图像", "graphic/graphicGLES3v2": "图形图像", "graphic/windowStageTwo": "图形图像", "graphic/windowstandard": "图形图像",
    "hiviewdfx/faultlogtest": "DFX", "multimedia/photoAccess": "相机图库框架", "testfwk/perftestStatic": "测试子系统", "time/timeauthorityTest": "时间时区",
    "useriam/user_auth_icon": "用户IAM", "web/network_management": "Web", "web/web_engine_version": "Web", "web/web_page_rendering": "Web",
    "ability/crossplatform": "元能力", "arkui/ace_ets_ux_five": "ArkUI", "graphic/nativeFontNdk": "图形图像", "graphic/nativedrawing": "图形图像",
    "hiviewdfx/bytracetest": "DFX", "hiviewdfx/hidebugtest": "DFX", "print/print_errorcode": "打印框架", "security/access_token": "安全",
    "security/dlpNDK20Test": "安全", "testfwk/perftestScene": "测试子系统", "web/web_connectNative": "Web", "arkcompiler/esmodule": "语言编译运行时",
    "arkui/ace_ets_ux_one": "ArkUI", "communication/fusion": "短距", "global/i18n_standard": "全球化", "graphic/acts_display": "图形图像",
    "graphic/graphicGLES3": "图形图像", "graphic/graphicImage": "图形图像", "graphic/nativebuffer": "图形图像", "testfwk/uitestStatic": "测试子系统",
    "theme/screenlock_ets": "主题", "usb/usb_standard_ets": "USB服务", "web/page_interaction": "Web", "account/account_ndk": "账号",
    "arkui/ace_napi_test": "ArkUI", "global/global_stage": "全球化", "graphic/component3D": "图形图像", "graphic/graphicText": "图形图像",
    "graphic/nativefence": "图形图像", "graphic/nativeimage": "图形图像", "graphic/windowStage": "图形图像", "multimedia/avsource": "视频框架",
    "security/el5filekey": "安全", "telephony/telephone": "电话服务", "testfwk/uitestScene": "测试子系统", "theme/wallpaper_ets": "主题",
    "web/web_multi_media": "Web", "web/web_switch_core": "Web", "web/web_zoom_access": "Web", "account/appaccount": "账号",
    "arkui/ace_standard": "ArkUI", "bundlemanager/zlib": "包管理", "graphic/displayNdk": "图形图像", "graphic/graphicGL4": "图形图像",
    "graphic/graphicHdr": "图形图像", "hdf/device_manager": "驱动", "web/web_life_cycle": "Web", "web/web_multimedia": "Web",
    "account/osaccount": "账号", "global/i18n_stage": "全球化", "graphic/effectKit": "图形图像", "graphic/graphic3D": "图形图像",
    "graphic/windowNdk": "图形图像", "multimedia/camera": "相机图库框架", "testfwk/uitest_pc": "测试子系统", "time/dateTimeTest": "时间时区",
    "useriam/face_auth": "用户IAM", "useriam/user_auth": "用户IAM", "hiviewdfx/hiview": "DFX", "multimedia/audio": "音频",
    "multimedia/image": "相机图库框架", "multimedia/media": "视频框架", "security/sandbox": "安全", "testfwk/perftest": "测试子系统",
    "time/timeNDKTest": "时间时区", "usb/usb_standard": "USB服务", "advertising/ads": "广告服务", "print/print_xts": "打印框架",
    "security/cipher": "安全", "web/web_storage": "Web", "ability/dmsfwk": "元能力", "security/asset": "安全",
    "testfwk/uitest": "测试子系统", "web/web_device": "Web", "graphic/webGL": "图形图像", "hdf/errorcode": "驱动",
    "hdf/selection": "驱动", "pcs/pcs_arkts": "XTS专项小组", "security/huks": "安全", "time/timeTest": "时间时区",
    "ability/form": "卡片框架", "ai/mindspore": "AI", "web/web_jump": "Web", "web/web_load": "Web",
    "pcs/pcs_ndk": "XTS专项小组", "web/web_dfx": "Web", "web/web_net": "Web", "pcs/pcs_js": "XTS专项小组",
    "ai/nncore": "AI", "hdf/base": "驱动", "hdf/hid": "驱动", "hdf/usb": "驱动",
    "web/DFX": "Web",
}
for _i in range(3, 41):
    SUBSYSTEM_MAPPING[f"communication/wifi_p{_i}p"] = "短距"

# validator子目录映射（根据pages下的子目录判断子系统）
SUBSYSTEM_MAPPING.update({
    "validator/acts_validator/entry/src/main/ets/pages/MultimodalInput": "多模输入",
    "validator/acts_validator/entry/src/main/ets/pages/Notification": "事件通知",
    "validator/acts_validator/entry/src/main/ets/pages/Experience": "XTS专项小组",
    "validator/acts_validator/entry/src/main/ets/pages/Bluetooth": "短距",
    "validator/acts_validator/entry/src/main/ets/pages/Camera": "相机图库框架",
    "validator/acts_validator/entry/src/main/ets/pages/Player": "相机图库框架",
    "validator/acts_validator/entry/src/main/ets/pages/Screen": "窗口",
    "validator/acts_validator/entry/src/main/ets/pages/Sensor": "泛Sensor",
    "validator/acts_validator/entry/src/main/ets/pages/ArkUI": "ArkUI",
    "validator/acts_validator/entry/src/main/ets/pages/Audio": "音频",
    "validator/acts_validator/entry/src/main/ets/pages/Power": "电源服务",
    "validator/acts_validator/entry/src/main/ets/pages/Wifi": "短距",
    "validator/acts_validator/entry/src/main/ets/pages/PCS": "XTS专项小组",
})

SUBSYSTEM_MAPPING.update({
    "distributedhardware": "分布式硬件", "distributeddatamgr": "分布式数据", "resourceschedule": "全局资源调度", "multimodalinput": "多模输入",
    "bundlemanager": "包管理", "commonlibrary": "语言编译运行时", "communication": "短距", "customization": "定制化",
    "officeservice": "办公服务", "applications": "应用设置", "notification": "事件通知", "advertising": "广告服务",
    "arkcompiler": "语言编译运行时", "barrierfree": "无障碍服务", "inputmethod": "输入法", "hiviewdfx": "DFX",
    "telephony": "电话服务", "validator": "XTS专项小组", "location": "位置服务", "powermgr": "电源服务",
    "security": "安全", "ability": "元能力", "account": "账号", "graphic": "图形图像",
    "request": "上传下载", "sensors": "泛Sensor", "startup": "启动子系统", "storage": "文件管理",
    "testfwk": "测试子系统", "updater": "升级子系统", "useriam": "用户IAM", "global": "全球化",
    "ostest": "应用测试", "window": "窗口", "arkui": "ArkUI", "print": "打印框架",
    "theme": "主题", "demo": "示例", "game": "游戏", "msdp": "MSDP",
    "time": "时间时区", "hdf": "驱动", "pcs": "XTS专项小组", "tee": "TEE",
    "usb": "USB服务", "web": "Web", "xts": "XTS专项小组", "ai": "AI",
})

SORTED_DIRS = sorted(SUBSYSTEM_MAPPING.keys(), key=len, reverse=True)

_DIR_SUFFIX_MAP = {}
for _d, _s in SUBSYSTEM_MAPPING.items():
    _suffix = _d.split('/')[-1] if '/' in _d else None
    if _suffix:
        if _suffix not in _DIR_SUFFIX_MAP:
            _DIR_SUFFIX_MAP[_suffix] = []
        _DIR_SUFFIX_MAP[_suffix].append((_d, _s))

_DEFAULT_SUBSYSTEM = None
_DEFAULT_SUBSYSTEM_LOCK = threading.Lock()

def set_default_subsystem(scan_root):
    global _DEFAULT_SUBSYSTEM
    if not scan_root:
        with _DEFAULT_SUBSYSTEM_LOCK:
            _DEFAULT_SUBSYSTEM = None
        return
    sr = scan_root.replace("\\", "/").rstrip("/")
    parts = sr.replace("\\", "/").split("/")
    for i in range(len(parts) - 1, -1, -1):
        candidate = "/".join(parts[i:])
        if candidate in SUBSYSTEM_MAPPING:
            with _DEFAULT_SUBSYSTEM_LOCK:
                _DEFAULT_SUBSYSTEM = SUBSYSTEM_MAPPING[candidate]
            return
        if candidate in _DIR_SUFFIX_MAP and len(_DIR_SUFFIX_MAP[candidate]) == 1:
            _DEFAULT_SUBSYSTEM = _DIR_SUFFIX_MAP[candidate][0][1]
            return
    basename = parts[-1] if parts else None
    if basename and basename in SUBSYSTEM_MAPPING:
        _DEFAULT_SUBSYSTEM = SUBSYSTEM_MAPPING[basename]
        return

def get_subsystem(file_path):
    fp = file_path.replace("\\", "/")
    for d in SORTED_DIRS:
        if fp.startswith(d + "/"):
            return SUBSYSTEM_MAPPING[d]
    first_dir = fp.split('/')[0] if '/' in fp else None
    if first_dir and first_dir in _DIR_SUFFIX_MAP:
        entries = _DIR_SUFFIX_MAP[first_dir]
        if len(entries) == 1:
            return entries[0][1]
    if _DEFAULT_SUBSYSTEM:
        return _DEFAULT_SUBSYSTEM
    return "-"

# ======================== FILE UTILITIES ========================

ALL_SOURCE_EXTS = ['.ets', '.ts', '.js']
TEST_FILE_EXTS = ['.test.ets', '.test.ts', '.test.js']

def is_test_file(filepath):
    return filepath.endswith('.test.ets') or filepath.endswith('.test.ts') or filepath.endswith('.test.js')

def collect_files(scan_root, exts):
    result = []
    for root, dirs, files in os.walk(scan_root):
        for f in files:
            for ext in exts:
                if f.endswith(ext):
                    result.append(os.path.join(root, f))
                    break
    return result

def strip_comments(line):
    idx = line.find('//')
    if idx < 0:
        return line
    in_sq = in_dq = in_bt = False
    for c in line[:idx]:
        if c == '`' and not in_sq and not in_dq: in_bt = not in_bt
        elif c == "'" and not in_dq and not in_bt: in_sq = not in_sq
        elif c == '"' and not in_sq and not in_bt: in_dq = not in_dq
    if not in_sq and not in_dq and not in_bt:
        return line[:idx]
    return line

# ======================== BRACE MATCHING ========================
# Source: references/TRAPS.md (Trap 1, Trap 1b)
# Sync rule: Update when TRAPS.md trap descriptions change

def find_matching_brace(content, start):
    depth = 0; in_s = in_d = in_bt = False; i = start
    while i < len(content):
        c = content[i]
        if c == '\\' and (in_s or in_d or in_bt): i += 2; continue
        if c == '`' and not in_s and not in_d: in_bt = not in_bt
        elif c == "'" and not in_d and not in_bt: in_s = not in_s
        elif c == '"' and not in_s and not in_bt: in_d = not in_d
        if not in_s and not in_d and not in_bt:
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: return i
        i += 1
    return -1

def find_matching_paren(content, start):
    """Find matching closing parenthesis for opening parenthesis at position start"""
    depth = 0; in_s = in_d = in_bt = False; i = start
    while i < len(content):
        c = content[i]
        if c == '\\' and (in_s or in_d or in_bt): i += 2; continue
        if c == '`' and not in_s and not in_d: in_bt = not in_bt
        elif c == "'" and not in_d and not in_bt: in_s = not in_s
        elif c == '"' and not in_s and not in_bt: in_d = not in_d
        if not in_s and not in_d and not in_bt:
            if c == '(':
                if i == start:
                    depth = 1
                else:
                    depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0: return i
        i += 1
    return -1

# ======================== IT/DESCRIBE BLOCK PARSER ========================
# it()/describe() block parsing - string-aware brace matching

def _parse_blocks(content, keyword):
    blocks = []
    lines = content.split('\n')
    pattern = re.compile(rf'\b{keyword}(?:\.only|\.skip|\.each)?\s*\(\s*[\'"](.+?)[\'"]\s*,')
    in_multi_comment = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if in_multi_comment:
            if '*/' in stripped:
                in_multi_comment = False
            continue
        
        if stripped.startswith('/*'):
            in_multi_comment = True
            if '*/' not in stripped:
                continue
        
        if stripped.startswith('//') or stripped.startswith('*'):
            continue
        
        m = pattern.search(line)
        if not m:
            continue
        name = m.group(1); start = i + 1
        bo = 0; bc = 0
        in_s = in_d = in_bt = False; found = False
        for j in range(i, len(lines)):
            text = lines[j]; k = 0
            while k < len(text):
                c = text[k]
                if c == '\\' and (in_s or in_d or in_bt): k += 2; continue
                if c == '`' and not in_s and not in_d: in_bt = not in_bt
                elif c == "'" and not in_d and not in_bt: in_s = not in_s
                elif c == '"' and not in_s and not in_bt: in_d = not in_d
                if not in_s and not in_d and not in_bt:
                    if c == '{': bo += 1; found = True
                    elif c == '}': bc += 1
                k += 1
            if found and bc >= bo and bo > 0:
                blocks.append({'name': name, 'start': start, 'end': j + 1})
                break
    return blocks

def parse_it_blocks(content):
    return _parse_blocks(content, 'it')

def parse_describe_blocks(content):
    return _parse_blocks(content, 'describe')

def find_testcase_for_line(it_blocks, line_num):
    for b in it_blocks:
        if b['start'] <= line_num <= b['end']:
            return b['name']
    return "-"

# ======================== INDEPENDENT PROJECT FINDER ========================
# Independent XTS project finder - group BUILD.gn detection

def is_group_build_gn(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return bool(re.search(r'\bgroup\s*\(', f.read()))
    except Exception as e:
        print(f"  读取BUILD.gn失败 {filepath}: {e}", file=sys.stderr)
        return False

def find_independent_projects(scan_root):
    all_bg = set()
    for root, dirs, files in os.walk(scan_root):
        if 'BUILD.gn' in files:
            all_bg.add(os.path.abspath(root))
    non_group = {d for d in all_bg if not is_group_build_gn(os.path.join(d, 'BUILD.gn'))}
    parents = set()
    for d in all_bg:
        p = os.path.dirname(d)
        while p != os.path.abspath(scan_root) and p != '/':
            if p in non_group: parents.add(d); break
            p = os.path.dirname(p)
    indep = all_bg - parents - (all_bg - non_group)
    return sorted(indep)

# ======================== ASSERTION DETECTION ========================

ASSERTION_PATTERNS = [
    re.compile(r'\bexpect\s*\('), re.compile(r'\bassertEqual\s*\('),
    re.compile(r'\bassertTrue\s*\('), re.compile(r'\bassertFalse\s*\('),
    re.compile(r'\bassertNull\s*\('), re.compile(r'\bassertFail\s*\('),
    re.compile(r'\bassertInstanceOf\s*\('), re.compile(r'\bassertContains\s*\('),
    re.compile(r'\bassertDeepEquals\s*\('), re.compile(r'\bcheckResult\s*\('),
    re.compile(r'\bassertNotEqual\s*\('), re.compile(r'\bassertUndefined\s*\('),
    re.compile(r'\bassertDefined\s*\('), re.compile(r'\bassertThrowError\s*\('),
]

def has_assertion(text):
    if not text: return False
    eff = '\n'.join(l for l in text.split('\n') if not l.strip().startswith('//'))
    return any(p.search(eff) for p in ASSERTION_PATTERNS)

def _find_try_catch(body):
    result = []; lines = body.split('\n'); i = 0
    while i < len(lines):
        s = lines[i].strip()
        if re.match(r'try\s*\{', s):
            ts = i; bc = s.count('{') - s.count('}'); j = i + 1; te = -1
            while j < len(lines) and bc > 0:
                lj = lines[j].strip()
                if re.match(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', lj): te = j; break
                bc += lj.count('{') - lj.count('}')
                if bc == 0: te = j; break
                j += 1
            if te == -1: i += 1; continue
            try_c = '\n'.join(lines[ts:te+1]); cs = -1; catch_c = ''
            if re.match(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', lines[te].strip()):
                cs = te; cbc = 1; k = cs + 1
                while k < len(lines) and cbc > 0:
                    cbc += lines[k].count('{') - lines[k].count('}'); k += 1
                catch_c = '\n'.join(lines[cs:k])
            result.append({'try_content': try_c, 'catch_content': catch_c})
            i = k if cs != -1 else te + 1
        else: i += 1
    return result

# ======================== PROJECT-LEVEL SCAN UTILITIES ========================
# Project-level duplicate detection utilities

def get_project_source_files(project_dir):
    source_files = []
    for root, dirs, files in os.walk(project_dir):
        for f in files:
            if f.endswith(('.ets', '.ts', '.js')):
                source_files.append(os.path.join(root, f))
    return source_files

def collect_attr_values(project_dir, source_files, base_dir, pattern, fcache=None):
    items = []
    for file_path in source_files:
        try:
            if fcache is not None:
                content = fcache.get(file_path)
                if content is None:
                    continue
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
        except Exception:
            continue
        for match in pattern.finditer(content):
            attr_value = match.group(2)
            if not attr_value:
                continue
            line_num = content[:match.start()].count('\n') + 1
            rel_path = os.path.relpath(file_path, base_dir)
            items.append({'value': attr_value, 'file': rel_path, 'line': line_num})
    return items

def find_duplicate_groups(items):
    value_to_occurrences = collections.defaultdict(list)
    for item in items:
        value_to_occurrences[item['value']].append(item)
    duplicates = []
    for value, occurrences in value_to_occurrences.items():
        if len(occurrences) > 1:
            first = occurrences[0]
            other_locs = [f"{occ['file']}:{occ['line']}" for occ in occurrences[1:]]
            duplicates.append({
                'value': value, 'count': len(occurrences),
                'first_file': first['file'], 'first_line': first['line'],
                'other_locations': other_locs,
            })
    return duplicates

# ======================== REPORT GENERATION ========================
# Source: references/REPORT_FORMAT.md
# Sync rule: Update when REPORT_FORMAT.md format spec changes

RULE_CATEGORIES = {
    'R001':'编码规范合规','R002':'编码规范合规','R003':'编码规范合规','R004':'编码规范合规',
    'R005':'编码规范合规','R006':'编码规范合规','R007':'编码规范合规','R008':'编码规范合规',
    'R009':'编码规范合规','R010':'编码规范合规','R011':'编码规范合规','R012':'编码规范合规',
    'R013':'编码规范合规','R014':'编码规范合规','R015':'编码规范合规','R016':'编码规范合规',
    'R017':'编码规范合规','R018':'编码规范合规','R019':'编码规范合规','R020':'编码规范合规',
    'R021':'编码规范合规','R022':'编码规范合规','R023':'编码规范合规',
    'R201':'异步/时序安全','R202':'异步/时序安全','R203':'异步/时序安全',
    'R204':'资源管理','R205':'资源管理',
    'R206':'测试设计',
}

def get_rule_category(rule_id):
    return RULE_CATEGORIES.get(rule_id, '编码规范合规')

def sanitize_text(text):
    """清洗文本中的无效字符 + 防止 Excel 公式注入

    1. 移除控制字符（ASCII 0-31，除了换行符10和制表符9）
    2. 防止 Excel 公式注入：以 = + - @ 开头的单元格会被 Excel 解释为公式，
       恶意 PR 内容（源码片段、修复建议等）可利用此执行任意公式。
       对策：在这些前导字符前加单引号前缀，使 Excel 视为纯文本。
    """
    if not text:
        return ''
    import re
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(text))
    # Excel 公式注入防护：以 = + - @ 开头时加前导单引号
    if cleaned and cleaned[0] in ('=', '+', '-', '@'):
        cleaned = "'" + cleaned
    return cleaned

def write_excel_with_bom(filepath, wb):
    wb.save(filepath)

def generate_report(all_issues, report_dir, rules_info, rule_counts):
    from config_loader import is_fixable_rule, get_fix_guide_path
    os.makedirs(report_dir, exist_ok=True)
    wb = Workbook()
    ws1 = wb.active; ws1.title = "代码质量检查报告"
    ws1.append(["问题ID","问题类别","问题类型","严重级别","可自动修复","文件路径","行号","所属用例","代码片段","修复建议","所属子系统","申请报备人","报备原因","是否报备通过"])
    for iss in all_issues:
        rid = iss.get('rule','')
        ws1.append([
            sanitize_text(rid),
            sanitize_text(iss.get('category',get_rule_category(rid))),
            sanitize_text(iss.get('type','')),
            sanitize_text(iss.get('severity','')),
            'Yes' if is_fixable_rule(rid) else 'No',
            sanitize_text(iss.get('file','')),
            iss.get('line',''),
            sanitize_text(iss.get('testcase','-')),
            sanitize_text(iss.get('snippet','')),
            sanitize_text(iss.get('suggestion','')),
            sanitize_text(iss.get('subsystem','-')),
            '', '', ''
        ])
    for col in ws1.columns:
        ml = max((len(str(c.value)) if c.value else 0) for c in col)
        ws1.column_dimensions[col[0].column_letter].width = min(ml + 2, 60)
    ws2 = wb.create_sheet("问题扫描结果汇总")
    ws2.append(["规则编号","问题类别","问题类型","严重级别","可自动修复","修复指南","问题数量"])
    for rid, rn, sev, _fn in rules_info:
        ws2.append([
            rid, get_rule_category(rid), rn, sev,
            'Yes' if is_fixable_rule(rid) else 'No',
            get_fix_guide_path(rid) if is_fixable_rule(rid) else '-',
            rule_counts.get(rid, 0) if rule_counts.get(rid, 0) > 0 else 0
        ])
    ep = os.path.join(report_dir, "XTS_代码质量检查报告.xlsx")
    write_excel_with_bom(ep, wb)
    return ep

# ======================== PERFORMANCE OPTIMIZATIONS ========================

EXCLUDED_DIRS = frozenset({
    '.git', 'node_modules', 'oh_modules', 'ohos_modules',
    'build', 'out', 'obj', 'libs', '.libs',
    'dist',
    '.idea', '.vscode', '.settings',
    'coverage', '.nyc_output', '.coverage',
    'third_party', 'prebuilts',
    '__pycache__', '.pytest_cache',
    'gen', 'gn', 'hb',
})

def collect_all_files(scan_root, extra_exclude=None):
    """Single-pass file collection with directory exclusion.

    Replaces 6 separate collect_files() calls with one os.walk.
    Automatically skips non-source directories via EXCLUDED_DIRS.

    Returns dict with keys:
        source, test, build_gn, test_json, p7b, syscap, oh_package, all_source
    """
    excluded = EXCLUDED_DIRS
    if extra_exclude:
        excluded = excluded | frozenset(extra_exclude)

    cats = {
        'source': [], 'test': [], 'build_gn': [],
        'test_json': [], 'p7b': [], 'syscap': [], 'oh_package': [],
    }

    if os.path.isfile(scan_root):
        _categorize_file(scan_root, cats)
        cats['all_source'] = cats['source'] + cats['test']
        return cats

    for root, dirs, files in os.walk(scan_root):
        dirs[:] = sorted(d for d in dirs if d not in excluded)
        for f in files:
            _categorize_file(os.path.join(root, f), cats)

    cats['all_source'] = cats['source'] + cats['test']
    return cats


def _categorize_file(fp, cats):
    """文件分类 - 支持多种命名模式"""
    f = os.path.basename(fp)
    if f == 'BUILD.gn':
        cats['build_gn'].append(fp)
    elif f == 'Test.json':
        cats['test_json'].append(fp)
    elif f.endswith('.p7b'):
        cats['p7b'].append(fp)
    elif f == 'syscap.json':
        cats['syscap'].append(fp)
    elif f == 'oh-package.json5':
        cats['oh_package'].append(fp)
    else:
        # 支持多种测试文件命名模式
        is_test_file = False
        
        # 标准模式: *.test.ets, *.test.ts, *.test.js
        if f.endswith('.test.ets') or f.endswith('.test.ts') or f.endswith('.test.js'):
            is_test_file = True
        
        # 前缀模式: test_*.ets, test_*.ts, test_*.js
        elif (f.startswith('test_') and f.endswith('.ets')) or \
             (f.startswith('test_') and f.endswith('.ts')) or \
             (f.startswith('test_') and f.endswith('.js')):
            is_test_file = True
        
        # 后缀模式: *_test.ets, *_test.ts, *_test.js
        elif (f.endswith('_test.ets')) or (f.endswith('_test.ts')) or (f.endswith('_test.js')):
            is_test_file = True
        
        if is_test_file:
            cats['test'].append(fp)
        elif f.endswith('.ets') or f.endswith('.ts') or f.endswith('.js'):
            cats['source'].append(fp)


def find_independent_projects_fast(scan_root, build_gn_files=None):
    """Optimized project finder: parallel BUILD.gn reading + short-circuit.

    Only reads first 2KB of each BUILD.gn (enough to detect group()).
    Reuses pre-collected BUILD.gn file list when available.
    """
    all_bg = set()
    if build_gn_files:
        all_bg = {os.path.dirname(os.path.abspath(f)) for f in build_gn_files}
    else:
        for root, dirs, files in os.walk(scan_root):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
            if 'BUILD.gn' in files:
                all_bg.add(os.path.abspath(root))

    if not all_bg:
        return []

    gn_paths = [os.path.join(d, 'BUILD.gn') for d in all_bg]

    def _check_group(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(4096)
            return bool(re.search(r'\bgroup\s*\(', head))
        except Exception:
            return False

    workers = min(16, max(1, len(gn_paths)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(zip(all_bg, executor.map(_check_group, gn_paths)))
    is_group = {d: g for d, g in results}

    non_group = {d for d in all_bg if not is_group[d]}
    abs_root = os.path.abspath(scan_root)
    parents = set()
    for d in all_bg:
        p = os.path.dirname(d)
        while p != abs_root and p != '/':
            if p in non_group:
                parents.add(d)
                break
            p = os.path.dirname(p)

    indep = all_bg - parents - (all_bg - non_group)
    return sorted(indep)


def find_sta_projects(scan_root, build_gn_files=None):
    """Identify XTS_Sta (Static) projects that should be excluded from test design rules.

    A project is classified as XTS_Sta if either:
    1. Its BUILD.gn uses ohos_js_app_static_suite or ohos_js_app_assist_static_suite template
    2. Its directory name ends with 'Static' or 'static'

    Returns a set of absolute directory paths that are XTS_Sta projects.
    """
    sta_projects = set()
    gn_files = build_gn_files or []
    if not gn_files:
        for root, dirs, files in os.walk(scan_root):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
            if 'BUILD.gn' in files:
                gn_files.append(os.path.join(root, 'BUILD.gn'))

    static_suite_re = re.compile(
        r'\bohos_js_app_(?:static_suite|assist_static_suite)\s*\('
    )

    for gn_path in gn_files:
        proj_dir = os.path.dirname(os.path.abspath(gn_path))
        proj_name = os.path.basename(proj_dir)

        is_sta_by_name = proj_name.endswith('Static') or proj_name.endswith('static')

        is_sta_by_template = False
        try:
            with open(gn_path, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(4096)
            is_sta_by_template = bool(static_suite_re.search(head))
        except Exception:
            pass

        if is_sta_by_name or is_sta_by_template:
            sta_projects.add(proj_dir)

    return sta_projects


def is_in_sta_project(file_path, sta_projects):
    if not sta_projects:
        return False
    abs_dir = os.path.dirname(os.path.abspath(file_path))
    if abs_dir in sta_projects:
        return True
    for sp in sta_projects:
        if abs_dir.startswith(sp + os.sep):
            return True
    return False


def grep_scan(scan_root, patterns, file_globs=None, extra_exclude=None):
    """Fast pattern scanning using ripgrep or grep.

    10-100x faster than Python for simple regex patterns.
    Falls back to grep if rg is not available.

    Args:
        scan_root: Directory to scan
        patterns: List of regex patterns
        file_globs: File glob filters (e.g. ['*.ets', '*.ts'])
        extra_exclude: Additional directory names to exclude

    Returns: list of (filepath, line_num, matched_line, pattern_index)
    """
    rg_path = shutil.which('rg')
    grep_path = shutil.which('grep')

    if not rg_path and not grep_path:
        logging.warning('grep_scan: neither rg nor grep found')
        return []

    tool = 'rg' if rg_path else 'grep'
    results = []

    excl = EXCLUDED_DIRS
    if extra_exclude:
        excl = excl | frozenset(extra_exclude)

    for idx, pattern in enumerate(patterns):
        if tool == 'rg':
            cmd = [rg_path, '-n', '--no-heading', '--binary',
                   pattern, scan_root]
            if file_globs:
                for g in file_globs:
                    cmd.extend(['--glob', g])
            for d in excl:
                cmd.extend(['--glob', f'!{d}'])
        else:
            cmd = [grep_path, '-rn', '-E', '--binary-files=without-match', pattern]
            if file_globs:
                for g in file_globs:
                    cmd.append(f'--include={g}')
            for d in excl:
                cmd.extend(['--exclude-dir', d])
            cmd.append(scan_root)

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            for line in proc.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    try:
                        results.append((parts[0], int(parts[1]), parts[2], idx))
                    except ValueError:
                        continue
        except (subprocess.TimeoutExpired, Exception) as e:
            logging.warning(f'grep_scan pattern[{idx}] failed: {e}')

    return results


# ======================== SCAN CACHE (step 3b optimization) ========================

import pickle


class FileContentCache:
    """Thread-safe file content cache.

    Avoids redundant disk reads when multiple rules scan the same files.
    Pre-load all files once, then all rules read from memory.

    Usage:
        cache = FileContentCache()
        cache.preload(file_list)           # one-time preload
        content = cache.get(filepath)      # cache hit, no disk I/O

    Performance: 5.1x speedup for 5 rules on 2000 files (3.3s -> 0.65s)
    """

    def __init__(self, max_size=80000):
        self._cache = {}
        self._max_size = max_size
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
        self._lines_cache = {}

    def get(self, filepath):
        with self._lock:
            if filepath in self._cache:
                self._hits += 1
                self._cache[filepath] = self._cache.pop(filepath)
                return self._cache[filepath]
            self._misses += 1
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            with self._lock:
                if len(self._cache) >= self._max_size:
                    oldest = list(self._cache.keys())[:self._max_size // 2]
                    for k in oldest:
                        del self._cache[k]
                self._cache[filepath] = content
            return content
        except Exception:
            return None

    def get_lines(self, filepath):
        with self._lock:
            if filepath in self._lines_cache:
                return self._lines_cache[filepath]
        content = self.get(filepath)
        if content is None:
            return []
        lines = content.split('\n')
        with self._lock:
            self._lines_cache[filepath] = lines
        return lines

    def preload(self, filepaths):
        with self._lock:
            for fp in filepaths:
                if fp not in self._cache:
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                            self._cache[fp] = f.read()
                    except Exception:
                        pass

    def stats(self):
        total = self._hits + self._misses
        rate = (self._hits / total * 100) if total > 0 else 0
        return {'hits': self._hits, 'misses': self._misses,
                'hit_rate': f'{rate:.1f}%', 'cached_files': len(self._cache)}

    def save(self, filepath):
        with self._lock:
            with open(filepath, 'wb') as f:
                pickle.dump(self._cache, f, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, filepath):
        inst = cls()
        with open(filepath, 'rb') as f:
            inst._cache = pickle.load(f)
        return inst


class BlockCache:
    """Cache for pre-parsed it()/describe() blocks.

    Multiple rules (R004,R015,R016,R018,R019,R020,R201-R206) parse it() blocks
    from the same files. Parse once, reuse across all rules.

    Usage:
        bc = BlockCache(fcache)  # fcache is FileContentCache
        blocks = bc.get_it_blocks(filepath)   # parse once, cache forever
    """

    def __init__(self, file_cache=None):
        self._it = {}
        self._describe = {}
        self._fc = file_cache
        self._lock = threading.Lock()

    def get_it_blocks(self, filepath):
        with self._lock:
            if filepath in self._it:
                return self._it[filepath]
        c = self._fc.get(filepath) if self._fc else None
        if c is None:
            return []
        blocks = parse_it_blocks(c)
        with self._lock:
            self._it[filepath] = blocks
        return blocks

    def get_describe_blocks(self, filepath):
        with self._lock:
            if filepath in self._describe:
                return self._describe[filepath]
        c = self._fc.get(filepath) if self._fc else None
        if c is None:
            return []
        blocks = parse_describe_blocks(c)
        with self._lock:
            self._describe[filepath] = blocks
        return blocks

    def preload(self, filepaths):
        for fp in filepaths:
            self.get_it_blocks(fp)
            self.get_describe_blocks(fp)


# ======================== SHARED SCANNER UTILITIES ========================
# Extracted from duplicated code across R201, R202, R203, R204, R206 scanners.
# These functions were copy-pasted identically in 5-6 scanner files.

SYNC_BUILTINS = frozenset({
    'expect', 'console', 'describe', 'it', 'beforeAll', 'beforeEach',
    'afterAll', 'afterEach', 'sleep', 'assertEqual', 'assertTrue',
    'assertFalse', 'assertContain', 'assertFail', 'assertNull',
    'assertUndefined', 'assertInstanceOf', 'assertClose', 'assertNaN',
    'assertThrowError', 'assertDeepEquals', 'assertLarger', 'assertLess',
    'mocker', 'MockKit', 'when', 'print', 'isNaN', 'parseInt', 'parseFloat',
    'String', 'Number', 'Boolean', 'Array', 'JSON', 'Math', 'Object',
})

MAX_WRAPPER_FILE_SIZE = 50 * 1024


def extract_block_body(content, start, end):
    lines = content.split('\n')
    return '\n'.join(lines[start - 1:end])


def extract_called_functions(body):
    called = set()
    # 提取直接函数调用: funcName(...)
    for match in re.finditer(r'(?:await\s+)?(\w+)\s*\(', body):
        func_name = match.group(1)
        if func_name not in SYNC_BUILTINS:
            called.add(func_name)
    
    # 提取成员方法调用: Obj.methodName(...)
    for match in re.finditer(r'(\w+)\s*\.\s*(\w+)\s*\(', body):
        obj_name = match.group(1)
        method_name = match.group(2)
        if method_name not in SYNC_BUILTINS:
            called.add(f"{obj_name}.{method_name}")
    
    return called


class FunctionDefinitionCache:
    """Cache function definitions per file to avoid repeated regex scanning.

    R201/R202 call find_function_definition() ~370K times across 17K files.
    Most calls are for the same (file, func_name) pairs. This cache indexes
    all function definitions in a file on first access.
    """

    def __init__(self, fcache=None):
        self._index = {}
        self._fc = fcache

    def get(self, file_path, func_name):
        if file_path not in self._index:
            self._build_index(file_path)
        return self._index[file_path].get(func_name)

    def get_by_content(self, content, func_name):
        content_key = (hash(content), id(content))
        if content_key not in self._index:
            self._build_index_from_content(content_key, content)
        return self._index[content_key].get(func_name)

    def _build_index(self, file_path):
        content = self._fc.get(file_path) if self._fc else None
        if content is None:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                self._index[file_path] = {}
                return
        self._build_index_from_content(file_path, content)

    def _build_index_from_content(self, key, content):
        file_funcs = {}
        _JS_KEYWORDS = frozenset({
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break',
            'continue', 'return', 'try', 'catch', 'finally', 'throw', 'new',
            'class', 'extends', 'super', 'import', 'export', 'from', 'as',
            'typeof', 'instanceof', 'in', 'of', 'delete', 'void', 'with',
        })
        for m in re.finditer(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|\w+)\s*=>\s*\{', content):
            name = m.group(1)
            if name not in file_funcs:
                brace_idx = content.index('{', m.start())
                end = find_matching_brace(content, brace_idx)
                if end > 0:
                    file_funcs[name] = content[brace_idx + 1:end]
        for m in re.finditer(r'(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{', content):
            name = m.group(1)
            if name not in file_funcs:
                brace_idx = content.index('{', m.start())
                end = find_matching_brace(content, brace_idx)
                if end > 0:
                    file_funcs[name] = content[brace_idx + 1:end]
        for m in re.finditer(r'\b([a-z_]\w*)\s*\([^)]*\)\s*\{', content):
            name = m.group(1)
            if name not in file_funcs and name not in _JS_KEYWORDS:
                brace_idx = content.index('{', m.start())
                end = find_matching_brace(content, brace_idx)
                if end > 0:
                    file_funcs[name] = content[brace_idx + 1:end]
        self._index[key] = file_funcs


def find_function_definition(content, func_name, fdef_cache=None, with_line=False):
    esc = re.escape(func_name)
    for pattern in [
        re.compile(r'(?:const|let|var)\s+' + esc + r'\s*=\s*(?:async\s+)?(?:\([^)]*\)|\w+)\s*=>\s*\{'),
        re.compile(r'(?:async\s+)?function\s+' + esc + r'\s*\([^)]*\)\s*\{'),
        re.compile(r'\b' + esc + r'\s*\([^)]*\)\s*\{'),
    ]:
        match = pattern.search(content)
        if match:
            brace_idx = content.index('{', match.start())
            func_body_end = find_matching_brace(content, brace_idx)
            if func_body_end > 0:
                func_body = content[brace_idx + 1:func_body_end]
                if with_line:
                    func_line = content[:brace_idx + 1].count('\n') + 1
                    return func_body, func_line
                return func_body
    if with_line:
        return None, None
    return None


def parse_imports(content):
    imports = {}
    # Named imports: import { A, B } from 'path'
    for match in re.finditer(r'import\s*\{([^}]+)\}\s*from\s*[\'"]([^\'"]+)[\'"]', content):
        for name in match.group(1).split(','):
            imports[name.strip()] = match.group(2)
    
    # Default imports: import X from 'path'
    for match in re.finditer(r'import\s+(\w+)\s+from\s*[\'"]([^\'"]+)[\'"]', content):
        imports[match.group(1)] = match.group(2)
    
    # Namespace imports: import * as X from 'path'
    for match in re.finditer(r'import\s+\*\s+as\s+(\w+)\s+from\s*[\'"]([^\'"]+)[\'"]', content):
        imports[match.group(1)] = match.group(2)
    
    return imports


def resolve_import_path(current_file, import_source):
    if not (import_source.startswith('./') or import_source.startswith('../')):
        return None
    base = os.path.dirname(current_file)
    resolved = os.path.normpath(os.path.join(base, import_source))
    for ext in ['.ets', '.ts', '.js', '/index.ets', '/index.ts', '/index.js']:
        candidate = resolved + ext
        if os.path.isfile(candidate):
            return candidate
    return None


def check_cross_file_wrapper(called_funcs, imports, current_file, check_fn,
                             visited=None, max_depth=2, fcache=None, fdef_cache=None):
    if visited is None:
        visited = set()
    for func_name in called_funcs:
        if func_name not in imports or func_name in visited:
            continue
        visited.add(func_name)
        source = imports[func_name]
        source_file = resolve_import_path(current_file, source)
        if not source_file:
            continue
        if fcache:
            source_content = fcache.get(source_file)
        else:
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    source_content = f.read()
            except (IOError, UnicodeDecodeError):
                continue
        if source_content is None:
            continue
        if fdef_cache:
            func_body = fdef_cache.get(source_file, func_name)
        else:
            func_body = find_function_definition(source_content, func_name)
        if func_body:
            result = check_fn(func_body, source_file, func_name)
            if result:
                return func_name, source_file, result
            if max_depth > 0:
                sub_funcs = extract_called_functions(func_body)
                sub_imports = parse_imports(source_content)
                sub_result = check_cross_file_wrapper(
                    sub_funcs, sub_imports, source_file, check_fn,
                    visited, max_depth - 1, fcache, fdef_cache
                )
                if sub_result:
                    return func_name, source_file, sub_result[2]
    return None


def find_hook_line(desc_body, hook_name):
    for i, line in enumerate(desc_body.split('\n')):
        if re.search(rf'\b{hook_name}\s*\(', line):
            return i + 1
    return 0


def find_hook_snippet(desc_body, hook_name):
    for line in desc_body.split('\n'):
        if re.search(rf'\b{hook_name}\s*\(', line):
            return line.strip()[:120]
    return ''


def extract_hook_body(desc_body, hook_name):
    hook_pattern = re.compile(rf'\b{hook_name}\s*\(')
    for i, line in enumerate(desc_body.split('\n')):
        if hook_pattern.search(line):
            full_text = '\n'.join(desc_body.split('\n')[i:])
            brace_idx = full_text.find('{')
            if brace_idx == -1:
                return None
            block_end = find_matching_brace(full_text, brace_idx)
            if block_end > 0:
                return full_text[brace_idx + 1:block_end]
    return None


def generate_html_report(all_issues, report_dir, rules_info, rule_counts, scan_meta=None, excel_path=None):
    import base64
    import json
    from config_loader import get_fixable_rules, get_fix_guide_path
    
    template_path = os.path.join(os.path.dirname(__file__), 'report_template.html')
    if not os.path.exists(template_path):
        print(f"  警告: HTML模板文件不存在: {template_path}", file=sys.stderr)
        return None
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_html = f.read()
    except Exception as e:
        print(f"  警告: 读取HTML模板失败: {e}", file=sys.stderr)
        return None
    
    rules_list = []
    for rid, rn, sev, _ in rules_info:
        rules_list.append({
            'rule': rid,
            'name': rn,
            'severity': sev,
            'category': get_rule_category(rid)
        })
    
    issues_list = []
    for iss in all_issues:
        issues_list.append({
            'rule': iss.get('rule', ''),
            'category': iss.get('category', get_rule_category(iss.get('rule', ''))),
            'type': iss.get('type', ''),
            'severity': iss.get('severity', ''),
            'file': iss.get('file', ''),
            'line': iss.get('line', ''),
            'testcase': iss.get('testcase', '-'),
            'snippet': iss.get('snippet', ''),
            'suggestion': iss.get('suggestion', ''),
            'subsystem': iss.get('subsystem', '-')
        })
    
    stats_dict = {}
    for rid, rn, sev, _ in rules_info:
        stats_dict[rid] = rule_counts.get(rid, 0)
    
    fixable_rules = list(get_fixable_rules())
    fix_guide_paths = {rid: get_fix_guide_path(rid) for rid in fixable_rules}
    
    excel_base64 = ''
    if excel_path and os.path.exists(excel_path):
        try:
            with open(excel_path, 'rb') as f:
                excel_base64 = base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"  警告: 读取Excel文件失败: {e}", file=sys.stderr)
    
    embedded_data = {
        'meta': scan_meta or {},
        'stats': stats_dict,
        'rules': rules_list,
        'issues': issues_list,
        'excel_base64': excel_base64,
        'fixable_rules': fixable_rules,
        'fix_guide_paths': fix_guide_paths,
    }
    
    data_json = json.dumps(embedded_data, ensure_ascii=False, indent=2)
    # 防止存储型 XSS：转义 </script> 标签，防止 JSON 数据中的 </script>
    # 破坏 <script> 标签边界并注入恶意脚本
    data_json = data_json.replace('</', '<\\/')
    data_json = data_json.replace('<', '\\u003c')
    final_html = template_html.replace('__DATA_PLACEHOLDER__', data_json)
    
    html_path = os.path.join(report_dir, 'XTS_代码质量检查报告.html')
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        return html_path
    except Exception as e:
        print(f"  警告: 写入HTML报告失败: {e}", file=sys.stderr)
        return None

