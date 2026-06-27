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

#include "config_parser.h"
#include <fstream>

namespace OHOS {
namespace HiviewDFX {

bool ConfigParser::LoadConfig(const std::string& filePath)
{
    if (filePath.empty()) {
        return false;
    }
    std::ifstream file(filePath);
    if (!file.is_open()) {
        return false;
    }
    std::string line;
    while (std::getline(file, line)) {
        ParseLine(line);
    }
    isLoaded_ = true;
    return true;
}

bool ConfigParser::GetSectionInfo(const std::string& sectionName, SectionInfo& info)
{
    if (sectionName.empty()) {
        return false;
    }
    if (!isLoaded_) {
        return false;
    }
    auto it = sections_.find(sectionName);
    if (it == sections_.end()) {
        return false;
    }
    info = it->second;
    return true;
}

bool ConfigParser::ResetSection(const std::string& sectionName)
{
    if (sectionName.empty()) {
        return false;
    }
    auto it = sections_.find(sectionName);
    if (it == sections_.end()) {
        return false;
    }
    sections_.erase(it);
    return true;
}

std::string ConfigParser::GetValue(const std::string& key)
{
    if (key.empty()) {
        return "";
    }
    auto it = values_.find(key);
    if (it == values_.end()) {
        return "";
    }
    return it->second;
}

int ConfigParser::GetSectionCount()
{
    return sections_.size();
}

bool ConfigParser::ParseLine(const std::string& line)
{
    if (line.empty()) {
        return false;
    }
    std::string trimmed = TrimString(line);
    if (trimmed.empty() || trimmed[0] == '#') {
        return false;
    }
    size_t pos = trimmed.find('=');
    if (pos == std::string::npos) {
        return false;
    }
    std::string key = TrimString(trimmed.substr(0, pos));
    std::string value = TrimString(trimmed.substr(pos + 1));
    values_[key] = value;
    return true;
}

std::string ConfigParser::TrimString(const std::string& str)
{
    size_t start = str.find_first_not_of(" \t");
    if (start == std::string::npos) {
        return "";
    }
    size_t end = str.find_last_not_of(" \t");
    return str.substr(start, end - start + 1);
}

} // namespace HiviewDFX
} // namespace OHOS
