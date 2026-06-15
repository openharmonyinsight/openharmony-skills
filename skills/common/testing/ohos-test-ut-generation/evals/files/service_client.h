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

#ifndef SERVICE_CLIENT_H
#define SERVICE_CLIENT_H

#include <string>
#include <vector>
#include <memory>

namespace OHOS {
namespace Telephony {

class INetworkService {
public:
    virtual ~INetworkService() = default;
    virtual bool Connect(const std::string& host, int port) = 0;
    virtual void Disconnect() = 0;
    virtual int SendData(const std::vector<uint8_t>& data) = 0;
    virtual std::vector<uint8_t> ReceiveData(int maxBytes) = 0;
    virtual bool IsConnected() = 0;
};

class ServiceClient {
public:
    explicit ServiceClient(std::shared_ptr<INetworkService> service);
    ~ServiceClient() = default;

    bool EstablishConnection(const std::string& host, int port);
    void CloseConnection();
    int TransmitData(const std::vector<uint8_t>& payload);
    std::vector<uint8_t> FetchData(int requestedBytes);
    bool CheckConnectionStatus();
    std::string GetLastError();

private:
    std::shared_ptr<INetworkService> service_;
    std::string lastError_;
    bool isConnected_ = false;
};

} // namespace Telephony
} // namespace OHOS

#endif // SERVICE_CLIENT_H
