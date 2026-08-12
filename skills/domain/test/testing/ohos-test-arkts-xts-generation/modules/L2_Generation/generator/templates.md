# 代码模板库

> **模块信息**
> - 层级：L2_Generation
> - 优先级：按需加载
> - 适用范围：测试代码文件级模板（文件头、完整文件结构、模板变量）
> - 依赖：conventions
> - 相关：参数/返回值/边界值测试模板见 `param_test.md`；错误码测试模板见 `error_test.md`；UiTest 模板见 `uitest_templates.md`

---

## 一、模板概述

本模块提供测试代码的**文件级模板**，包括许可证头部和完整测试文件结构。各类型测试用例的代码模板（参数测试、错误码测试、返回值测试、边界值测试、异步测试、801 防护）分别由 `param_test.md` 和 `error_test.md` 提供。

---

## 二、测试文件头模板

### 2.1 Apache 2.0 许可证头部

```typescript
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
```

---

## 三、完整测试文件模板

### 3.1 API 测试文件

```typescript
// ... Apache 2.0 license header (see §2.1) ...

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
import {APIName} from '@kit.BaseKitName'; // 根据实际模块修改

export default function APINameTest() {
  describe('APINameParameterTest', () => {
    // 参数测试用例（模板见 param_test.md §二）
  });

  describe('APINameErrorCodeTest', () => {
    // 错误码测试用例（模板见 error_test.md §三）
  });

  describe('APINameReturnValueTest', () => {
    // 返回值测试用例（模板见 param_test.md §三）
  });
}
```

---

## 九、模板变量说明

> **重要说明**：
> - `{Code}` 和 `{expectedErrorCode}` 必须从 API 的 `@throws` 标记中提取
> - 不同 API 的错误码可能不同，不能假设所有参数错误都抛出 401
> - 错误码参考：通用错误码（`docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`）和子系统特有错误码（`docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md`）
