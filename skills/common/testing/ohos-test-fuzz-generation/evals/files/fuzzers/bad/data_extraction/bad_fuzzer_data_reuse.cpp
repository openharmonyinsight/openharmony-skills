// Copyright (c) 2026 Huawei Device Co., Ltd.
// VIOLATION: Rule 004 - same fdp-derived variable reused across multiple method calls

#include <cstddef>
#include <cstdint>
#include <fuzzed_data_provider/fuzzed_data_provider.h>
#include "simple_class.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    int32_t val = fdp.ConsumeIntegral<int32_t>();  // SAME val reused 3 times
    ConfigManager mgr;
    mgr.SetConfig(val, "key");       // val reused
    mgr.UpdateValue(val, 1.0f);      // val reused again
    mgr.ResetSection(val);           // val reused again
    return 0;
}
