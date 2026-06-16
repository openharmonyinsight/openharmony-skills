/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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

#include <cstddef>
#include <cstdint>
#include <parcel.h>
#include <securec.h>

#include <iremote_stub.h>
#include "message_option.h"
#include "message_parcel.h"
#include "marshalling_helper.h"
#include "window.h"
#include "window_agent.h"
#include "window_impl.h"
#include "window_manager.h"
#include "windowstubget_fuzzer.h"

using namespace OHOS::Rosen;

namespace OHOS {
namespace {
constexpr size_t DATA_MIN_SIZE = 2;
}

bool DoSomethingInterestingWithMyAPI(const uint8_t* data, size_t size)
{
    if (data == nullptr || size < DATA_MIN_SIZE) {
        return false;
    }
    
    MessageParcel parcel;
    MessageParcel reply;
    MessageOption option;

    parcel.WriteInterfaceToken(WindowStub::GetDescriptor());
    parcel.WriteBuffer(data, size);

    sptr<WindowOption> windowOption = new(std::nothrow)WindowOption();
    if (windowOption == nullptr) {
        return false;
    }
    sptr<WindowImpl> window = new(std::nothrow)WindowImpl(windowOption);
    if (window == nullptr) {
        return false;
    }
    sptr<WindowAgent> windowStub = new(std::nothrow)WindowAgent(window);
    if (windowStub == nullptr) {
        return false;
    }
    parcel.RewindRead(0);
    windowStub->OnRemoteRequest(static_cast<uint32_t>(IWindow::WindowMessage::TRANS_ID_GET_WINDOW_PROPERTY),
        parcel, reply, option);
    parcel.RewindRead(0);
    windowStub->OnRemoteRequest(static_cast<uint32_t>(IWindow::WindowMessage::TRANS_ID_DUMP_INFO),
        parcel, reply, option);
    parcel.RewindRead(0);
    windowStub->OnRemoteRequest(static_cast<uint32_t>(IWindow::WindowMessage::TRANS_ID_RESTORE_SPLIT_WINDOW_MODE),
        parcel, reply, option);
    parcel.RewindRead(0);
    windowStub->OnRemoteRequest(static_cast<uint32_t>(IWindow::WindowMessage::TRANS_ID_CONSUME_KEY_EVENT),
        parcel, reply, option);
    return true;
}
} // namespace.OHOS

/* Fuzzer entry point */
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    /* Run your code on data */
    OHOS::DoSomethingInterestingWithMyAPI(data, size);
    return 0;
}
