// Copyright (c) 2026 Huawei Device Co., Ltd.
// VIOLATION: Rule 003 - declares FDP but never uses mutation data

#include <cstddef>
#include <cstdint>
#include <fuzzed_data_provider/fuzzed_data_provider.h>
#include "simple_class.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    ConfigManager mgr;
    mgr.SetConfig(1, "key");    // No fdp usage - fixed value
    mgr.UpdateValue(1, 1.0f);   // No fdp usage - fixed value  
    mgr.ResetSection(1);        // No fdp usage - fixed value
    return 0;
}
