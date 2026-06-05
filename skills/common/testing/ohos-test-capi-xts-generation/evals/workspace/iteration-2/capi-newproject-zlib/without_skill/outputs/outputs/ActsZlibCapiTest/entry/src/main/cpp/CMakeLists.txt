# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");

cmake_minimum_required(VERSION 3.5.0)
project(zlibcapitest)

set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})

if(DEFINED PACKAGE_FIND_FILE)
    include(${PACKAGE_FIND_FILE})
endif()

include_directories(${NATIVERENDER_ROOT_PATH})

add_library(zlibcapitest SHARED
    NapiTest.cpp
)

target_link_libraries(zlibcapitest
    libace_napi.z.so
    libhilog_ndk.z.so
    libz.so
)
