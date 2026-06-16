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

#include "data_processor.h"
#include <climits>

namespace OHOS {
namespace Utils {

ProcessResult DataProcessor::ProcessString(const std::string& input)
{
    if (input.empty()) {
        lastError_ = "Empty input string";
        return RESULT_INVALID_INPUT;
    }
    if (input.size() > INT_MAX) {
        lastError_ = "Input too long";
        return RESULT_INVALID_INPUT;
    }
    isProcessing_ = true;
    processedCount_++;
    isProcessing_ = false;
    return RESULT_SUCCESS;
}

ProcessResult DataProcessor::ProcessBuffer(const std::vector<uint8_t>& buffer, int maxSize)
{
    if (buffer.empty()) {
        lastError_ = "Empty buffer";
        return RESULT_INVALID_INPUT;
    }
    if (maxSize <= 0) {
        lastError_ = "Invalid max size";
        return RESULT_INVALID_INPUT;
    }
    if (buffer.size() > maxSize) {
        lastError_ = "Buffer exceeds max size";
        return RESULT_PROCESS_ERROR;
    }
    isProcessing_ = true;
    processedCount_++;
    isProcessing_ = false;
    return RESULT_SUCCESS;
}

bool DataProcessor::SetConfig(const std::string& key, const std::string& value)
{
    if (key.empty()) {
        return false;
    }
    config_[key] = value;
    return true;
}

std::string DataProcessor::GetConfig(const std::string& key)
{
    if (key.empty()) {
        return "";
    }
    auto it = config_.find(key);
    if (it == config_.end()) {
        return "";
    }
    return it->second;
}

int DataProcessor::GetProcessedCount()
{
    return processedCount_;
}

bool DataProcessor::ResetState()
{
    processedCount_ = 0;
    config_.clear();
    lastError_ = "";
    isProcessing_ = false;
    return true;
}

std::string DataProcessor::GetStatusReport()
{
    if (isProcessing_) {
        return "processing";
    }
    if (processedCount_ == 0) {
        return "idle";
    }
    return "completed:" + std::to_string(processedCount_);
}

} // namespace Utils
} // namespace OHOS
