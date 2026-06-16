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

#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <string>
#include <stdexcept>

namespace OHOS {
namespace CommonLibrary {

class Calculator {
public:
    Calculator() = default;
    ~Calculator() = default;

    int Add(int a, int b);
    int Subtract(int a, int b);
    int Multiply(int a, int b);
    int Divide(int a, int b);
    bool IsValidInput(int value);
    std::string GetResultAsString(int result);
};

} // namespace CommonLibrary
} // namespace OHOS

#endif // CALCULATOR_H
