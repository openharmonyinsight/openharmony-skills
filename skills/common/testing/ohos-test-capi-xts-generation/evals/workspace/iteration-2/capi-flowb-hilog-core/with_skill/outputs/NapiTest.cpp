#include "napi/native_api.h"
#include "hilog/log.h"

#include <cstdio>

#undef LOG_DOMAIN
#undef LOG_TAG
#define LOG_DOMAIN 0xD003200
#define LOG_TAG "testTag"

static napi_value OHLogPrintInfoLevel_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "test info message");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintDebugLevel_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_DEBUG, 0x3200, "testTag", "test debug message");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintWarnLevel_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_WARN, 0x3200, "testTag", "test warn message");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintFatalLevel_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_FATAL, 0x3200, "testTag", "test fatal message");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintDomainZero_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0, "testTag", "domain zero message");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintDomainMax_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0xFFFF, "testTag", "domain max message");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintReturnTest_napi(napi_env env, napi_callback_info info)
{
    int ret = OH_LOG_Print(LOG_APP, LOG_ERROR, 0x3200, "testTag", "return test");
    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableDebug_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableInfo_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableWarn_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableError_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableFatal_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_FATAL);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableInvalidLevel_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", (LogLevel)100);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableDomainZero_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0, "testTag", LOG_INFO);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableDomainMax_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0xFFFF, "testTag", LOG_INFO);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableReturnTrue_napi(napi_env env, napi_callback_info info)
{
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableReturnFalse_napi(napi_env env, napi_callback_info info)
{
    bool isLoggable = OH_LOG_IsLoggable(0x32000, "testTag", LOG_INFO);
    napi_value result;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelInfo_napi(napi_env env, napi_callback_info info)
{
    OH_LOG_SetMinLogLevel(LOG_INFO);
    bool debugLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    bool infoLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    napi_value result;
    if (!debugLoggable && infoLoggable) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, -1, &result);
    }
    return result;
}

static napi_value OHLogSetMinLogLevelWarn_napi(napi_env env, napi_callback_info info)
{
    OH_LOG_SetMinLogLevel(LOG_WARN);
    bool infoLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    bool warnLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN);
    napi_value result;
    if (!infoLoggable && warnLoggable) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, -1, &result);
    }
    return result;
}

static napi_value OHLogSetMinLogLevelError_napi(napi_env env, napi_callback_info info)
{
    OH_LOG_SetMinLogLevel(LOG_ERROR);
    bool warnLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN);
    bool errorLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    napi_value result;
    if (!warnLoggable && errorLoggable) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, -1, &result);
    }
    return result;
}

static napi_value OHLogSetMinLogLevelFatal_napi(napi_env env, napi_callback_info info)
{
    OH_LOG_SetMinLogLevel(LOG_FATAL);
    bool errorLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    bool fatalLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_FATAL);
    napi_value result;
    if (!errorLoggable && fatalLoggable) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, -1, &result);
    }
    return result;
}

static napi_value OHLogSetMinLogLevelDebug_napi(napi_env env, napi_callback_info info)
{
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool debugLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    napi_value result;
    if (debugLoggable) {
        napi_create_int32(env, 0, &result);
    } else {
        napi_create_int32(env, -1, &result);
    }
    return result;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"OHLogPrintInfoLevel", nullptr, OHLogPrintInfoLevel_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintDebugLevel", nullptr, OHLogPrintDebugLevel_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintWarnLevel", nullptr, OHLogPrintWarnLevel_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintFatalLevel", nullptr, OHLogPrintFatalLevel_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintDomainZero", nullptr, OHLogPrintDomainZero_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintDomainMax", nullptr, OHLogPrintDomainMax_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintReturnTest", nullptr, OHLogPrintReturnTest_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableDebug", nullptr, OHLogIsLoggableDebug_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableInfo", nullptr, OHLogIsLoggableInfo_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableWarn", nullptr, OHLogIsLoggableWarn_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableError", nullptr, OHLogIsLoggableError_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableFatal", nullptr, OHLogIsLoggableFatal_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableInvalidLevel", nullptr, OHLogIsLoggableInvalidLevel_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableDomainZero", nullptr, OHLogIsLoggableDomainZero_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableDomainMax", nullptr, OHLogIsLoggableDomainMax_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableReturnTrue", nullptr, OHLogIsLoggableReturnTrue_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogIsLoggableReturnFalse", nullptr, OHLogIsLoggableReturnFalse_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogSetMinLogLevelInfo", nullptr, OHLogSetMinLogLevelInfo_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogSetMinLogLevelWarn", nullptr, OHLogSetMinLogLevelWarn_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogSetMinLogLevelError", nullptr, OHLogSetMinLogLevelError_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogSetMinLogLevelFatal", nullptr, OHLogSetMinLogLevelFatal_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogSetMinLogLevelDebug", nullptr, OHLogSetMinLogLevelDebug_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
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
    .nm_modname = "libhilogndk",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterModule(void)
{
    napi_module_register(&demoModule);
}
