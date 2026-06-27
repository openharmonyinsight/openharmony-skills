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

#ifndef CONFIG_PARSER_H
#define CONFIG_PARSER_H

#include <string>
#include <map>
#include <vector>

namespace OHOS {
namespace HiviewDFX {

struct SectionInfo {
    std::string name;
    int offset;
    int length;
};

class ConfigParser {
public:
    ConfigParser() = default;
    ~ConfigParser() = default;

    bool LoadConfig(const std::string& filePath);
    bool GetSectionInfo(const std::string& sectionName, SectionInfo& info);
    bool ResetSection(const std::string& sectionName);
    std::string GetValue(const std::string& key);
    int GetSectionCount();

private:
    bool ParseLine(const std::string& line);
    std::string TrimString(const std::string& str);
    std::map<std::string, SectionInfo> sections_;
    std::map<std::string, std::string> values_;
    bool isLoaded_ = false;
};

} // namespace HiviewDFX
} // namespace OHOS

#endif // CONFIG_PARSER_H
