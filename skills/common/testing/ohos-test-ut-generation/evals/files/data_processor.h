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

#ifndef DATA_PROCESSOR_H
#define DATA_PROCESSOR_H

#include <string>
#include <vector>
#include <map>
#include <memory>

namespace OHOS {
namespace Utils {

enum ProcessResult {
    RESULT_SUCCESS = 0,
    RESULT_INVALID_INPUT = 1,
    RESULT_PROCESS_ERROR = 2,
    RESULT_TIMEOUT = 3,
};

class DataProcessor {
public:
    DataProcessor() = default;
    ~DataProcessor() = default;

    ProcessResult ProcessString(const std::string& input);
    ProcessResult ProcessBuffer(const std::vector<uint8_t>& buffer, int maxSize);
    bool SetConfig(const std::string& key, const std::string& value);
    std::string GetConfig(const std::string& key);
    int GetProcessedCount();
    bool ResetState();
    std::string GetStatusReport();

private:
    std::map<std::string, std::string> config_;
    int processedCount_ = 0;
    bool isProcessing_ = false;
    std::string lastError_;
};

} // namespace Utils
} // namespace OHOS

#endif // DATA_PROCESSOR_H
