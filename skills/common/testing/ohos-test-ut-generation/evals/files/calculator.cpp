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

#include "calculator.h"
#include <climits>
#include <sstream>

namespace OHOS {
namespace CommonLibrary {

int Calculator::Add(int a, int b)
{
    return a + b;
}

int Calculator::Subtract(int a, int b)
{
    return a - b;
}

int Calculator::Multiply(int a, int b)
{
    return a * b;
}

int Calculator::Divide(int a, int b)
{
    if (b == 0) {
        throw std::invalid_argument("Division by zero");
    }
    return a / b;
}

bool Calculator::IsValidInput(int value)
{
    if (value < 0) {
        return false;
    }
    if (value > INT_MAX / 2) {
        return false;
    }
    return true;
}

std::string Calculator::GetResultAsString(int result)
{
    if (result == 0) {
        return "zero";
    }
    std::stringstream ss;
    ss << result;
    return ss.str();
}

} // namespace CommonLibrary
} // namespace OHOS
