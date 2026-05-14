/*
 * Copyright (c) {YEAR} Huawei Device Co., Ltd.
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

#include "{FUZZER_NAME}.h"

#include <fuzzer/FuzzedDataProvider.h>

#include {TARGET_HEADER}

namespace OHOS {
namespace {NAMESPACE} {

{GLOBAL_INSTANCE_DECL}

namespace {

{METHOD_CONSTANTS}

{METHOD_FUNCTIONS}

} // namespace

} // namespace {NAMESPACE}
} // namespace OHOS

extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)
{
{LLVM_FUZZER_INIT_BODY}
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
{NULL_CHECK_GLOBAL}

    FuzzedDataProvider fdp(data, size);

    uint8_t tarPos = fdp.ConsumeIntegral<uint8_t>() % OHOS::{NAMESPACE}::TARGET_SIZE;
    switch (tarPos) {
{SWITCH_CASES}
        default:
            return -1;
    }
    return 0;
}