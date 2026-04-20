/*
 * Copyright (C) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "napi/native_api.h"
#include <cstdlib>

/**
 * N-API 封装函数示例
 * 
 * @param env N-API 环境
 * @param info 回调信息
 * @return napi_value 返回值
 */
static napi_value YourCAPIFunction_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string");
        return nullptr;
    }

    char param[256] = {0};
    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], param, sizeof(param) - 1, &strLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get parameter value");
        return nullptr;
    }

    // TODO: 调用实际的 CAPI 函数
    // int result = YourCAPIFunction(param);
    
    napi_value result;
    napi_create_int32(env, 0, &result);
    
    return result;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        // TODO: 注册实际的 N-API 函数
        { "yourCAPIFunction", nullptr, YourCAPIFunction_napi, nullptr, nullptr, nullptr, napi_default, nullptr }
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "entry",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterEntryModule(void)
{
    napi_module_register(&demoModule);
}
