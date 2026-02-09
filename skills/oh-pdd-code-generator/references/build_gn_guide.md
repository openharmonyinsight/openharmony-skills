# BUILD.gn 编写指南

本文档介绍 OpenHarmony BUILD.gn 文件的编写规范。

## 基本结构

### 导入语句

```gni
import("//build/ohos.gni")
import("//build/test.gni")
import("//foundation/filemanagement/disk_management/disk_management.gni")
```

### 配置模板

```gni
config("module_config") {
  visibility = [ ":*" ]
  include_dirs = [ "include" ]
}
```

## 构建目标类型

### ohos_shared_library

动态共享库（.so 文件）

```gni
ohos_shared_library("disk_management_sa") {
  subsystem_name = "filemanagement"
  part_name = "disk_management"

  sources = [
    "src/disk_management_service.cpp",
    "src/main.cpp",
  ]

  include_dirs = [
    "include",
    "//utils/native/base/include",
  ]

  deps = [
    "//foundation/hiviewdfx/hilog/native/framework:libhilog",
  ]

  external_deps = [
    "c_utils:utils",
  ]
}
```

### ohos_static_library

静态库（.a 文件）

```gni
ohos_static_library("disk_management_utils") {
  sources = [
    "src/disk_utils.cpp",
  ]

  include_dirs = [ "include" ]
}
```

### ohos_executable

可执行文件

```gni
ohos_executable("disk_management_tool") {
  sources = [
    "src/main.cpp",
  ]

  deps = [
    ":disk_management_utils",
  ]
}
```

## 测试目标

### ohos_unittest

单元测试

```gni
ohos_unittest("disk_management_unittest") {
  subsystem_name = "filemanagement"
  part_name = "disk_management"
  test_type = "unittest"
  test_time_out = 300
  module_out_path = "filemanagement/disk_management/test/unittest"

  sources = [
    "test/disk_management_test.cpp",
  ]

  deps = [
    ":disk_management_sa",
  ]

  external_deps = [
    "googletest:gmock_main",
    "googletest:gtest_main",
  ]

  # 代码覆盖率
  cflags_cc = [ "--coverage" ]
  ldflags = [ "--coverage" ]
}
```

### ohos_fuzztest

模糊测试

```gni
ohos_fuzztest("disk_management_fuzztest") {
  module_out_path = "filemanagement/disk_management/test/fuzztest"

  sources = [
    "test/fuzztest/disk_management_fuzzer.cpp",
  ]

  deps = [
    ":disk_management_sa",
  ]
}
```

## 安全选项

### branch_protector_ret

```gni
branch_protector_ret = "pac_ret"
```

### sanitize

```gni
sanitize = {
  integer_overflow = true
  ubsan = true
  boundary_sanitize = true
  cfi = true
  cfi_cross_dso = true
  debug = false
}
```

## 条件编译

### 基于特性开关

```gni
sources = [
  "src/common.cpp",
]

if (disk_management_enable_format) {
  sources += [ "src/format_service.cpp" ]
  defines += [ "DISK_MANAGEMENT_FORMAT_ENABLE" ]
}

if (disk_management_enable_repair) {
  sources += [ "src/repair_service.cpp" ]
}
```

### 基于平台

```gni
if (is_linux) {
  sources += [ "src/linux_specific.cpp" ]
}

if (is_ohos) {
  sources += [ "src/ohos_specific.cpp" ]
}
```

## 依赖配置

### deps

内部依赖，使用标签路径

```gni
deps = [
  ":module_idl",           # 同一 BUILD.gn 内
  "//utils/native/base:utils",  # 跨模块
]
```

### external_deps

外部依赖，使用 `part_name:target_name` 格式

```gni
external_deps = [
  "c_utils:utils",
  "hilog:libhilog",
  "hitrace_native:hitrace_meter",
  "hisysevent:libhisysevent",
]
```

## 安装配置

```gni
install_images = [
  "system",
  "updater",
]

relative_install_dir = "lib"
```

## 完整示例

```gni
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0

import("//build/ohos.gni")
import("//build/test.gni")
import("//foundation/filemanagement/disk_management/disk_management.gni")

config("disk_management_config") {
  visibility = [ ":*" ]
  include_dirs = [
    "include",
    "${disk_management_path}/include",
    "//utils/native/base/include",
  ]
}

ohos_shared_library("disk_management_sa") {
  subsystem_name = "filemanagement"
  part_name = "disk_management"

  sources = [
    "src/disk_management_service.cpp",
    "src/main.cpp",
  ]

  configs = [ ":disk_management_config" ]

  defines = []

  # 条件编译
  if (disk_management_enable_format) {
    sources += [ "src/format_service.cpp" ]
    defines += [ "DISK_MANAGEMENT_FORMAT_ENABLE" ]
  }

  deps = [
    ":disk_management_idl",
    "//foundation/hiviewdfx/hilog/native/framework:libhilog",
    "//foundation/communication/ipc/interfaces/native/innerkits:ipc_core",
  ]

  external_deps = [
    "c_utils:utils",
  ]

  branch_protector_ret = "pac_ret"
  sanitize = {
    integer_overflow = true
    cfi = true
    debug = false
  }

  install_images = [ "system" ]
  relative_install_dir = "lib"
}

# 单元测试
ohos_unittest("disk_management_unittest") {
  subsystem_name = "filemanagement"
  part_name = "disk_management"
  test_type = "unittest"
  test_time_out = 300
  module_out_path = "filemanagement/disk_management/test/unittest"

  sources = [
    "test/disk_management_test.cpp",
  ]

  include_dirs = [ "include" ]

  deps = [
    ":disk_management_sa",
  ]

  external_deps = [
    "googletest:gmock_main",
    "googletest:gtest_main",
  ]

  cflags_cc = [ "--coverage" ]
  ldflags = [ "--coverage" ]
}

group("disk_management") {
  deps = [
    ":disk_management_sa",
  ]
}
```

## .gni 配置文件

### 定义路径变量

```gni
disk_management_path = "//foundation/filemanagement/disk_management"
disk_management_services_path = "${disk_management_path}/services"
disk_management_native_path = "${disk_management_services_path}/native"
```

### 定义功能开关

```gni
declare_args() {
  disk_management_enable_format = true
  disk_management_enable_repair = true
  disk_management_debug_mode = false
}
```

### 依赖判断

```gni
declare_args() {
  disk_management_rdb_enabled =
      defined(global_parts_info) &&
      defined(global_parts_info.relational_store)
}
```
