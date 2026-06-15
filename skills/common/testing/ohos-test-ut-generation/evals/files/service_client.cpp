/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
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

#include "service_client.h"

namespace OHOS {
namespace Telephony {

ServiceClient::ServiceClient(std::shared_ptr<INetworkService> service) : service_(service)
{
    if (service_ == nullptr) {
        lastError_ = "Service is null";
    }
}

bool ServiceClient::EstablishConnection(const std::string& host, int port)
{
    if (service_ == nullptr) {
        lastError_ = "Service is null";
        return false;
    }
    if (host.empty()) {
        lastError_ = "Host is empty";
        return false;
    }
    if (port <= 0 || port > 65535) {
        lastError_ = "Invalid port";
        return false;
    }
    bool result = service_->Connect(host, port);
    if (result) {
        isConnected_ = true;
    } else {
        lastError_ = "Connection failed";
    }
    return result;
}

void ServiceClient::CloseConnection()
{
    if (service_ != nullptr && isConnected_) {
        service_->Disconnect();
        isConnected_ = false;
    }
}

int ServiceClient::TransmitData(const std::vector<uint8_t>& payload)
{
    if (service_ == nullptr) {
        lastError_ = "Service is null";
        return -1;
    }
    if (!isConnected_) {
        lastError_ = "Not connected";
        return -1;
    }
    if (payload.empty()) {
        lastError_ = "Empty payload";
        return -1;
    }
    return service_->SendData(payload);
}

std::vector<uint8_t> ServiceClient::FetchData(int requestedBytes)
{
    if (service_ == nullptr) {
        lastError_ = "Service is null";
        return {};
    }
    if (!isConnected_) {
        lastError_ = "Not connected";
        return {};
    }
    if (requestedBytes <= 0) {
        lastError_ = "Invalid bytes request";
        return {};
    }
    return service_->ReceiveData(requestedBytes);
}

bool ServiceClient::CheckConnectionStatus()
{
    if (service_ == nullptr) {
        return false;
    }
    isConnected_ = service_->IsConnected();
    return isConnected_;
}

std::string ServiceClient::GetLastError()
{
    return lastError_;
}

} // namespace Telephony
} // namespace OHOS
