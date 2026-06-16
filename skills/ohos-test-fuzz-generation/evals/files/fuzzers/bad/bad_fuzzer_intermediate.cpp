// Copyright (c) 2026 Huawei Device Co., Ltd.
// VIOLATION: Rule 015 - unnecessary intermediate encode/decode before API call

#include <cstddef>
#include <cstdint>
#include <string>
#include <fuzzed_data_provider/fuzzed_data_provider.h>
#include "simple_class.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    FuzzedDataProvider fdp(data, size);
    int32_t rawId = fdp.ConsumeIntegral<int32_t>();
    std::string encoded = std::to_string(rawId);    // INTERMEDIATE: encode to string
    int32_t sectionId = std::stoi(encoded);          // INTERMEDIATE: decode back to int
    ConfigManager mgr;
    mgr.SetConfig(sectionId, "key");                 // Should use rawId directly from fdp
    return 0;
}
