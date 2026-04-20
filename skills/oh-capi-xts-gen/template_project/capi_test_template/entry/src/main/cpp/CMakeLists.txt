# the minimum version of CMake.
cmake_minimum_required(VERSION 3.4.1)
project({PROJECT_NAME})

set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})

include_directories(${NATIVERENDER_ROOT_PATH}
                    ${NATIVERENDER_ROOT_PATH}/include)

add_library(entry SHARED NapiTest.cpp)
target_link_libraries(entry PUBLIC libace_napi.z.so)
target_link_libraries(entry PUBLIC {NDK_LIB_NAME})
target_link_libraries(entry PUBLIC libc++.a)
