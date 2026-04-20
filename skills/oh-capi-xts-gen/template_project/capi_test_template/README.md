# CAPI 测试套模板工程

## 概述

这是一个干净的 OpenHarmony CAPI 测试套模板工程，已删除所有包管理相关的业务代码，保留了完整的工程结构和配置文件。

## 模板位置

```
.opencode/skills/oh-capi-xts-gen/template_project/capi_test_template/
```

## 使用方法

### 1. 复制模板工程

```bash
# 设置变量
SUBSYSTEM="your_subsystem"  # 例如: bundlemanager, ability, arkui
TEST_SUITE_NAME="your_test_suite_name"  # 例如: actscapitest
OH_ROOT="/path/to/openharmony"

# 复制模板
cp -r .opencode/skills/oh-capi-xts-gen/template_project/capi_test_template \
  ${OH_ROOT}/test/xts/acts/${SUBSYSTEM}/${TEST_SUITE_NAME}
```

### 2. 修改配置文件

需要修改以下文件中的测试套名称和相关信息：

| 文件 | 需要修改的内容 |
|------|---------------|
| `BUILD.gn` | 测试套名称、hap_name、part_name、subsystem_name |
| `Test.json` | bundle-name、test-file-name |
| `AppScope/app.json5` | bundleName |
| `entry/src/main/module.json5` | module 信息 |

### 3. 实现 CAPI 测试

#### 步骤 3.1: 添加 CAPI 头文件

在 `entry/src/main/cpp/NapiTest.cpp` 中：

```cpp
// TODO: 添加实际的 CAPI 头文件
#include "your_capi_header.h"  // 例如: #include "arkui/native_interface_arkui.h"
```

#### 步骤 3.2: 实现 N-API 封装函数

替换 `YourCAPIFunction_napi` 为实际的函数：

```cpp
static napi_value YourCAPIFunction_napi(napi_env env, napi_callback_info info)
{
    // 1. 参数提取和验证
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    // 2. 参数类型检查
    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_string) {
        napi_throw_error(env, nullptr, "Argument must be a string");
        return nullptr;
    }

    // 3. 从 napi_value 提取参数值
    char param[256] = {0};
    size_t strLen;
    status = napi_get_value_string_utf8(env, args[0], param, sizeof(param) - 1, &strLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get parameter value");
        return nullptr;
    }

    // 4. 调用实际的 CAPI 函数
    int result = YourCAPIFunction(param);
    
    // 5. 构造返回值
    napi_value returnValue;
    napi_create_int32(env, result, &returnValue);
    
    return returnValue;
}
```

#### 步骤 3.3: 注册 N-API 函数

在 `Init` 函数中：

```cpp
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        { "yourCAPIFunction", nullptr, YourCAPIFunction_napi, nullptr, nullptr, nullptr, napi_default, nullptr }
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

#### 步骤 3.4: 添加 TypeScript 声明

在 `entry/src/main/cpp/types/libentry/index.d.ts` 中：

```typescript
export const yourCAPIFunction: (param: string) => number;
```

#### 步骤 3.5: 编写测试用例

在 `entry/src/ohosTest/ets/test/Ability.test.ets` 中：

```typescript
it('SUB_YourAPI_Example_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, (done: Function) => {
    try {
        const result = testNapi.yourCAPIFunction("test_param");
        expect(result).assertEqual(expectedValue);
        done();
    } catch (err) {
        hilog.error(DOMAIN, TAG, `Test case failed: ${JSON.stringify(err)}`);
        expect().assertFail();
        done();
    }
});
```

### 4. 上层 BUILD.gn 注册

在上层目录的 BUILD.gn 中：

```gn
group("your_subsystem") {
  testonly = true
  if (is_standard_system) {
    deps = [
      "your_test_suite_name:YourTestSuite",
    ]
  }
}
```

### 5. 验证和编译

```bash
# 验证工程结构
bash .opencode/skills/oh-capi-xts-gen/scripts/check_test_suite_structure.sh \
  ${OH_ROOT}/test/xts/acts/${SUBSYSTEM}/${TEST_SUITE_NAME}

# 编译测试套
cd ${OH_ROOT}
./build.sh --product-name rk3568 --build-target ${TEST_SUITE_NAME}
```

## 目录结构

```
capi_test_template/
├── BUILD.gn                           # 测试套编译配置
├── Test.json                          # 测试配置文件
├── signature/                          # 签名证书
│   └── openharmony.p7b
├── hvigor/                             # Hvigor 配置
│   └── hvigor-config.json5
├── hvigorfile.ts                       # Hvigor 构建脚本
├── build-profile.json5                 # 构建配置
├── oh-package.json5                    # 包配置
├── AppScope/                            # 应用级配置
│   ├── app.json5
│   └── resources/
└── entry/                              # 主模块
    ├── src/
    │   ├── main/
    │   │   ├── cpp/
    │   │   │   ├── NapiTest.cpp          # N-API 封装实现（模板）
    │   │   │   ├── CMakeLists.txt       # CMake 配置
    │   │   │   └── types/
    │   │   │       └── libentry/
    │   │   │           ├── index.d.ts      # TypeScript 声明（模板）
    │   │   │           └── oh-package.json5
    │   │   ├── ets/
    │   │   │   ├── entryability/
    │   │   │   │   └── EntryAbility.ts
    │   │   │   └── pages/
    │   │   │       └── Index.ets
    │   │   ├── resources/
    │   │   └── module.json5
    │   └── ohosTest/
    │       ├── ets/
    │       │   ├── test/
    │       │   │   ├── Ability.test.ets   # 测试用例（模板）
    │       │   │   └── List.test.ets     # 测试套注册
    │       │   ├── testability/
    │       │   └── testrunner/
    │       └── module.json5
    ├── build-profile.json5
    └── oh-package.json5
```

## 注意事项

1. **包名唯一性**: 确保 bundleName 在整个系统中唯一
2. **测试套命名**: 遵循 `[子系统][功能]Test` 的命名规范
3. **签名文件**: 使用正确的签名文件（从其他测试套复制）
4. **上层注册**: 不要忘记在上层 BUILD.gn 中注册测试套
5. **TypeScript 声明**: 确保所有 N-API 函数都有对应的 TypeScript 声明

## 参考文档

- [工程配置模板](../../modules/L2_Generation/project_config_templates.md)
- [测试用例生成](../../modules/L2_Generation/test_generation_c.md)
- [测试套结构检查](../../scripts/check_test_suite_structure.sh)
