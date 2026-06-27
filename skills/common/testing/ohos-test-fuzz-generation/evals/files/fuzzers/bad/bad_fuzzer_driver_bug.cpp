// Copyright (c) 2026 Huawei Device Co., Ltd.
// VIOLATION: Rule 009 - driver/helper code introduces bugs (overflow, OOM, leak)

#include <cstddef>
#include <cstdint>
#include <fuzzed_data_provider/fuzzed_data_provider.h>
#include "simple_class.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    int32_t count = fdp.ConsumeIntegral<int32_t>();
    if (count < 0) { count = -count; }    // BUG: INT32_MIN → INT32_MIN (overflow)
    int32_t *buf = new int32_t[count];      // BUG: count can be huge → OOM
    for (int32_t i = 0; i < count; i++) {
        buf[i] = fdp.ConsumeIntegral<int32_t>();  // BUG: reads beyond data if count > remaining
    }
    ConfigManager mgr;
    if (count > 0) {
        mgr.SetConfig(buf[0], "key");
    }
    // BUG: no delete[] buf → memory leak
    return 0;
}
