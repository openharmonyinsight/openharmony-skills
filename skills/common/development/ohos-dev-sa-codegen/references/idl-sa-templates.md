# IDL 化 SA 代码模板

生成代码时**必须严格参照以下模板结构和风格**，根据用户提供的变量做替换。不要凭记忆或经验生成代码——始终以本文件中的模板为准。

变量定义和派生规则详见 `references/variable-reference.md`。

## 模板文件清单

| # | 生成目标路径 | 说明 |
|---|-------------|------|
| 1 | `BUILD.gn` | 根 group() 汇总 |
| 2 | `interfaces/I{SaName}.idl` | IDL 接口定义 |
| 3 | `services/include/{sa_name}.h` | SA 服务端头文件 |
| 4 | `services/src/{sa_name}.cpp` | SA 服务端实现 |
| 5 | `services/BUILD.gn` | idl_gen_interface + source_set + shared_library |
| 6 | `sa_profile/{sa_id}.json` | SA Profile |
| 7 | `sa_profile/BUILD.gn` | ohos_sa_profile |
| 8 | `etc/{process_name}.cfg` | CFG 进程配置 |
| 9 | `etc/BUILD.gn` | ohos_prebuilt_etc |

---

## 1. 根 BUILD.gn

生成目标：`BUILD.gn`

```gn
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import("//build/ohos.gni")

group("{sa_name}") {
  deps = [
    "services:{sa_name}",
    "etc:{sa_name}_etc",
    "sa_profile:{sa_name}_sa_profile",
  ]
}
```

---

## 2. IDL 接口定义

生成目标：`interfaces/I{SaName}.idl`

```idl
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

interface OHOS.I{SaName} {
   void MethodName([in] int paramA, [in] int paramB, [out] int result);
}
```

**IDL 语法规则**（用于将 C++ 方法签名转为 IDL 声明）：
- 接口声明：`interface OHOS.I{SaName} { ... }`
- 方法声明：`void MethodName([in] type param, [out] type param)`
- 输入参数标注 `[in]`，输出参数标注 `[out]`
- C++ 类型映射：`int32_t` → `int`，`bool` → `boolean`，`std::string` → `String`

---

## 3. SA 服务端头文件

生成目标：`services/include/{sa_name}.h`

```cpp
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

#ifndef {HEADER_GUARD}
#define {HEADER_GUARD}

#include "{sa_name}_stub.h"
#include "system_ability.h"

namespace OHOS {

class {SaName} : public SystemAbility, public {SaName}Stub {
    DECLARE_SYSTEM_ABILITY({SaName});

public:
    {SaName}(int32_t saId, bool runOnCreate);
    ~{SaName}();

    // 接口方法 override 声明（根据 IDL 生成）
    ErrCode MethodName(int32_t paramA, int32_t paramB, int32_t& result) override;
protected:
    void OnStart() override;
    void OnStop() override;
};
}

#endif // {HEADER_GUARD}
```

---

## 4. SA 服务端实现

生成目标：`services/src/{sa_name}.cpp`

```cpp
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

#include "{sa_name}.h"

#include "iremote_object.h"
#include "system_ability_definition.h"

using namespace OHOS;

REGISTER_SYSTEM_ABILITY_BY_ID({SaName}, {SA_ID}, {runOnCreate});

{SaName}::{SaName}(int32_t saId, bool runOnCreate) : SystemAbility(saId, runOnCreate)
{
}

{SaName}::~{SaName}()
{
}

// TODO: 实现接口方法逻辑
ErrCode {SaName}::MethodName(int32_t paramA, int32_t paramB, int32_t& result)
{
    return ERR_OK;
}

void {SaName}::OnStart()
{
    Publish(this);
}

void {SaName}::OnStop()
{
}
```

---

## 5. services/BUILD.gn

生成目标：`services/BUILD.gn`

```gn
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import("//build/config/components/idl_tool/idl.gni")

idl_gen_interface("{sa_name}_interface") {
  src_idl = rebase_path("../interfaces/I{SaName}.idl")
  log_domainid = "{log_domain}"
  log_tag = "{SaName}"
}

config("{sa_name}_config") {
  visibility = [ ":*" ]
  include_dirs = [
    "include",
    "${target_gen_dir}",
  ]
}

ohos_source_set("{sa_name}_proxy") {
  output_values = get_target_outputs(":{sa_name}_interface")
  sources = filter_include(output_values,
                            [
                              "*_proxy.cpp",
                              "*_client.cpp"
                            ])
  public_configs = [":{sa_name}_config"]
  deps = [ ":{sa_name}_interface" ]
  external_deps = [
    "c_utils:utils",
    "hilog:libhilog",
    "ipc:ipc_single",
    "samgr:samgr_proxy",
  ]
  part_name = "{part_name}"
  subsystem_name = "{subsystem_name}"
}

ohos_source_set("{sa_name}_stub") {
  output_values = get_target_outputs(":{sa_name}_interface")
  sources = filter_include(output_values, [ "*_stub.cpp" ])
  public_configs = [":{sa_name}_config"]
  deps = [ ":{sa_name}_interface" ]
  external_deps = [
    "c_utils:utils",
    "hilog:libhilog",
    "ipc:ipc_single",
  ]
  part_name = "{part_name}"
  subsystem_name = "{subsystem_name}"
}

ohos_shared_library("{sa_name}") {
  sources = [ "src/{sa_name}.cpp" ]

  public_configs = [":{sa_name}_config"]

  deps = [
    ":{sa_name}_proxy",
    ":{sa_name}_stub",
    "../../interfaces/innerkits/safwk:system_ability_fwk",
  ]

  external_deps = [
    "c_utils:utils",
    "hilog:libhilog",
    "ipc:ipc_single",
    "samgr:samgr_proxy",
  ]

  part_name = "{part_name}"
  subsystem_name = "{subsystem_name}"
  shlib_type = "sa"
}
```

---

## 6. SA Profile JSON

生成目标：`sa_profile/{sa_id}.json`

```json
{
    "process": "{process_name}",
    "systemability": [
        {
            "name": {SA_ID},
            "libpath": "lib{sa_name}.z.so",
            "run-on-create": {runOnCreate},
            "distributed": {distributed},
            "dump-level": 1
        }
    ]
}
```

---

## 7. sa_profile/BUILD.gn

生成目标：`sa_profile/BUILD.gn`

```gn
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import("//build/ohos/sa_profile/sa_profile.gni")

ohos_sa_profile("{sa_name}_sa_profile") {
  sources = [ "{sa_id}.json" ]
  part_name = "{part_name}"
}
```

---

## 8. CFG 进程配置

生成目标：`etc/{process_name}.cfg`

**CFG ondemand 规则**：当 `runOnCreate=true` 时，`ondemand=false`；当 `runOnCreate=false` 时，`ondemand=true`。

```json
{
    "services" : [{
            "name" : "{process_name}",
            "path" : ["/system/bin/sa_main", "/system/profile/{process_name}.json"],
            "ondemand" : {ondemand},
            "uid" : "system",
            "gid" : ["system", "shell"],
            "secon" : "u:r:{process_name}:s0"
        }
    ]
}
```

---

## 9. etc/BUILD.gn

生成目标：`etc/BUILD.gn`

```gn
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import("//build/ohos.gni")

ohos_prebuilt_etc("{sa_name}_etc") {
  source = "{process_name}.cfg"
  relative_install_dir = "init"
  part_name = "{part_name}"
  subsystem_name = "{subsystem_name}"
}
```
