// Copyright (c) 2026 Huawei Device Co., Ltd.
// VIOLATION: Rule 014 - uses fixed/hardcoded parameters instead of fdp-derived values

#include <cstddef>
#include <cstdint>
#include <fuzzed_data_provider/fuzzed_data_provider.h>
#include "simple_class.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    ConfigManager mgr;
    mgr.SetConfig(42, "default_key");    // FIXED: hardcoded 42 and "default_key"
    mgr.UpdateValue(0, 3.14f);           // FIXED: hardcoded 0 and 3.14f
    mgr.ResetSection(1);                 // FIXED: hardcoded 1
    mgr.MergeConfig("/etc/config", 100); // FIXED: hardcoded path and count
    mgr.QueryValue("test");              // FIXED: hardcoded "test"
    return 0;
}
