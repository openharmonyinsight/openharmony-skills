# 仓颉鸿蒙项目模板文件

本文档包含仓颉鸿蒙项目的所有模板文件内容。

## 目录

1. [根目录文件](#根目录文件)
   - [.gitignore](#gitignore)
   - [build-profile.json5](#build-profilejson5)
   - [code-linter.json5](#code-linterjson5)
   - [hvigorfile.ts](#hvigorfilets)
   - [oh-package.json5](#oh-packagejson5)
2. [AppScope 目录](#appscope-目录)
   - [app.json5](#appjson5)
3. [entry 模块](#entry-模块)
   - [entry/build-profile.json5](#entrybuild-profilejson5)
   - [entry/hvigorfile.ts](#entryhvigorfilets)
   - [entry/oh-package.json5](#entryoh-packagejson5)
   - [entry/cjpm.toml](#entrycjpmtoml)
   - [entry/cjpm.lock](#entrycjmplock)
   - [entry/src/main/module.json5](#entrysrcmainmodulejson5)
4. [仓颉源码](#仓颉源码)
   - [ability_stage.cj](#ability_stagecj)
   - [index.cj](#indexcj)
   - [main_ability.cj](#main_abilitycj)
5. [测试模块配置](#测试模块配置)
   - [entry/src/ohosTest/cangjie/cjpm.toml](#entrysrcohosTestcangjiecjpmtoml)
   - [entry/src/test/cangjie/cjpm.toml](#entrysrctestcangjiecjpmtoml)
6. [资源文件](#资源文件)
   - [string.json](#stringjson)
   - [color.json](#colorjson)
   - [main_pages.json](#main_pagesjson)
   - [layered_image.json](#layered_imagejson)
7. [Hvigor 配置](#hvigor-配置)
   - [hvigor-config.json5](#hvigor-configjson5)

---

## 根目录文件

### .gitignore

```gitignore
/node_modules
/oh_modules
/local.properties
/.idea
**/build
/.hvigor
.cxx
/.clangd
/.clang-format
/.clang-tidy
**/.test
/.appanalyzer
```

### build-profile.json5

**说明**：项目级构建配置文件。

**需要替换**：无需替换，但需确保 `modules` 中的 `name` 与模块目录名一致。

```json5
{
  "app": {
    "signingConfigs": [],
    "products": [
      {
        "name": "default",
        "signingConfig": "default",
        "targetSdkVersion": "6.0.2(22)",
        "compatibleSdkVersion": "6.0.2(22)",
        "runtimeOS": "HarmonyOS",
        "buildOption": {
          "strictMode": {
            "caseSensitiveCheck": true,
            "useNormalizedOHMUrl": true
          }
        }
      }
    ],
    "buildModeSet": [
      {
        "name": "debug",
      },
      {
        "name": "release"
      }
    ]
  },
  "modules": [
    {
      "name": "entry",
      "srcPath": "./entry",
      "targets": [
        {
          "name": "default",
          "applyToProducts": [
            "default"
          ]
        }
      ]
    }
  ]
}
```

### code-linter.json5

**说明**：代码检查配置文件。

```json5
{
  "files": [
    "**/*.ets",
    "**/*.cj"
  ],
  "ignore": [
    "**/src/ohosTest/**/*",
    "**/src/test/**/*",
    "**/src/mock/**/*",
    "**/node_modules/**/*",
    "**/oh_modules/**/*",
    "**/build/**/*",
    "**/.preview/**/*"
  ],
  "ruleSet": [
    "plugin:@performance/recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@security/no-unsafe-aes": "error",
    "@security/no-unsafe-hash": "error",
    "@security/no-unsafe-mac": "warn",
    "@security/no-unsafe-dh": "error",
    "@security/no-unsafe-dsa": "error",
    "@security/no-unsafe-ecdsa": "error",
    "@security/no-unsafe-rsa-encrypt": "error",
    "@security/no-unsafe-rsa-sign": "error",
    "@security/no-unsafe-rsa-key": "error",
    "@security/no-unsafe-dsa-key": "error",
    "@security/no-unsafe-dh-key": "error",
    "@security/no-unsafe-3des": "error"
  }
}
```

### hvigorfile.ts

**说明**：项目级 Hvigor 构建脚本。

```typescript
import { appTasks } from '@ohos/hvigor-ohos-plugin';

export default {
  system: appTasks, /* Built-in plugin of Hvigor. It cannot be modified. */
  plugins: []       /* Custom plugin to extend the functionality of Hvigor. */
}
```

### oh-package.json5

**说明**：项目依赖配置文件。

```json5
{
  "modelVersion": "6.0.2",
  "description": "Please describe the basic information.",
  "dependencies": {
  },
  "devDependencies": {
    "@ohos/hypium": "1.0.25",
    "@ohos/hamock": "1.0.0"
  }
}
```

---

## AppScope 目录

### app.json5

**说明**：应用全局配置文件，定义应用的基本信息。

**需要替换**：
- `bundleName`: 替换为用户指定的包名，如 `com.mycompany.myapp`
- `vendor`: 替换为开发者/公司名称

```json5
{
  "app": {
    "bundleName": "com.example.myapplication",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:layered_image",
    "label": "$string:app_name"
  }
}
```

---

## entry 模块

### entry/build-profile.json5

**说明**：模块级构建配置文件。

```json5
{
  "apiType": "stageMode",
  "buildOption": {
    "cangjieOptions": {
      "path": "./cjpm.toml"
    },
    "nativeLib": {
      "filter": {
        "enableOverride": true
      }
    }
  },
  "buildOptionSet": [
  ],
  "targets": [
    {
      "name": "default"
    }
  ]
}
```

### entry/hvigorfile.ts

**说明**：模块级 Hvigor 构建脚本。

```typescript
import { hapTasks } from '@ohos/hvigor-ohos-plugin';

export default {
  system: hapTasks, /* Built-in plugin of Hvigor. It cannot be modified. */
  plugins: []       /* Custom plugin to extend the functionality of Hvigor. */
}
```

### entry/oh-package.json5

**说明**：模块依赖配置文件。

```json5
{
  "name": "entry",
  "version": "1.0.0",
  "description": "Please describe the basic information.",
  "main": "",
  "author": "",
  "license": "",
  "dependencies": {}
}
```

### entry/cjpm.toml

**路径**：`entry/cjpm.toml`

**说明**：仓颉包管理配置文件，定义仓颉编译选项、目标平台配置等。

**需要替换**：`name` 字段可保持 `ohos_app_cangjie_entry` 不变。

**重要**：文件中的环境变量（如 `${DEVECO_CANGJIE_HOME}`、`${DEVECO_OH_NATIVE_HOME}` 等）由构建脚本自动注入，无需手动设置。

```toml
[package]
  cjc-version = "1.1.0"
  compile-option = "--dy-std --cfg=\"${COMPILE_CONDITION_ENTRY}\""
  description = "CangjieUI Application"
  link-option = ""
  name = "ohos_app_cangjie_entry"
  output-type = "dynamic"
  src-dir = "./src/main/cangjie"
  target-dir = ""
  version = "1.0.0"
  package-configuration = {}
  scripts = {}

[profile]
  [profile.build]
    incremental = true
    lto = ""
    [profile.build.combined]
      ohos_app_cangjie_entry = "dynamic"
  [profile.customized-option]
    debug = "-g -Woff all -Won apilevel-check"
    release = "--fast-math -O2 -s -Woff all -Won apilevel-check"
  [profile.test]

[target.aarch64-linux-ohos]
  compile-option = "-B \"${DEVECO_CANGJIE_HOME}/build-tools/third_party/llvm/bin\" -B \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/aarch64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/aarch64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/clang/15.0.4/lib/aarch64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/aarch64-linux-ohos\" --sysroot \"${DEVECO_OH_NATIVE_HOME}/sysroot\""
[target.aarch64-linux-ohos.bin-dependencies]
  path-option = ["${AARCH64_LIBS}", "${AARCH64_MACRO_LIBS}", "${AARCH64_KIT_LIBS}"]
  package-option = {}

[target.x86_64-linux-ohos]
  compile-option = "-B \"${DEVECO_CANGJIE_HOME}/build-tools/third_party/llvm/bin\" -B \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/x86_64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/x86_64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/clang/15.0.4/lib/x86_64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/x86_64-linux-ohos\" --sysroot \"${DEVECO_OH_NATIVE_HOME}/sysroot\""
[target.x86_64-linux-ohos.bin-dependencies]
  path-option = ["${X86_64_OHOS_LIBS}", "${X86_64_OHOS_MACRO_LIBS}", "${X86_64_OHOS_KIT_LIBS}"]

[target.x86_64-unknown-windows-gnu.bin-dependencies]
  path-option = ["${X86_64_LIBS}", "${X86_64_MACRO_LIBS}"]
  package-option = {}
```

### entry/cjpm.lock

**路径**：`entry/cjpm.lock`

**说明**：仓颉包管理锁文件，用于锁定依赖版本。

```toml
version = 0

[requires]
```

### entry/src/main/module.json5

**说明**：模块配置文件，定义 Ability 等组件信息。

**需要替换**：
- `srcEntry` 中的包名引用
- `abilities[0].srcEntry` 中的包名引用

```json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": [
      "phone"
    ],
    "deliveryWithInstall": true,
    "installationFree": false,
    "srcEntry": "ohos_app_cangjie_entry.MyAbilityStage",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "ohos_app_cangjie_entry.MainAbility",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:layered_image",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:startIcon",
        "startWindowBackground": "$color:start_window_background",
        "exported": true,
        "skills": [
          {
            "entities": [
              "entity.system.home"
            ],
            "actions": [
              "action.system.home"
            ]
          }
        ]
      }
    ]
  }
}
```

---

## 仓颉源码

### ability_stage.cj

**说明**：AbilityStage 类，管理 Ability 生命周期。

**需要替换**：`package` 声明中的包名。

```cangjie
package ohos_app_cangjie_entry

import kit.AbilityKit.AbilityStage
import kit.PerformanceAnalysisKit.Hilog

class MyAbilityStage <: AbilityStage {
    public override func onCreate(): Unit {
        Hilog.info(1, "Cangjie", "MyAbilityStage onCreated.")
    }
}
```

### index.cj

**说明**：入口页面，使用仓颉 ArkUI 声明式语法编写的 UI 组件。

**需要替换**：`package` 声明中的包名。

```cangjie
package ohos_app_cangjie_entry

import kit.ArkUI.LengthProp
import kit.ArkUI.Column
import kit.ArkUI.Row
import kit.ArkUI.Text
import kit.ArkUI.CustomView
import kit.ArkUI.CJEntry
import kit.ArkUI.loadNativeView
import kit.ArkUI.FontWeight
import kit.ArkUI.SubscriberManager
import kit.ArkUI.ObservedProperty
import kit.ArkUI.LocalStorage
import ohos.arkui.state_macro_manage.Entry
import ohos.arkui.state_macro_manage.Component
import ohos.arkui.state_macro_manage.State

@Entry
@Component
class EntryView {
    @State
    var message: String = "Hello World"

    func build() {
        Row {
            Column {
                Text(this.message)
                    .fontSize(50)
                    .fontWeight(FontWeight.Bold)
                    .onClick ({
                        evt => this.message = "Hello Cangjie"
                    })
            }.width(100.percent)
        }.height(100.percent)
    }
}
```

### main_ability.cj

**说明**：主 Ability 类，应用的入口点。

**需要替换**：`package` 声明中的包名。

```cangjie
package ohos_app_cangjie_entry

import kit.PerformanceAnalysisKit.Hilog
import kit.AbilityKit.Want
import kit.AbilityKit.UIAbility
import kit.AbilityKit.LaunchParam
import kit.AbilityKit.LaunchReason
import kit.ArkUI.WindowStage

class MainAbility <: UIAbility {
    public init() {
        super()
        registerSelf()
    }

    public override func onCreate(want: Want, launchParam: LaunchParam): Unit {
        Hilog.info(1, "Cangjie", "MainAbility OnCreated.${want.abilityName}")
        match (launchParam.launchReason) {
            case LaunchReason.StartAbility => Hilog.info(1, "Cangjie", "START_ABILITY")
            case _ => ()
        }
    }

    public override func onWindowStageCreate(windowStage: WindowStage): Unit {
        Hilog.info(1, "Cangjie", "MainAbility onWindowStageCreate.")
        windowStage.loadContent("EntryView")
    }
}
```

---

## 测试模块配置

### entry/src/ohosTest/cangjie/cjpm.toml

**路径**：`entry/src/ohosTest/cangjie/cjpm.toml`

**说明**：ohosTest 模块的仓颉包管理配置，用于设备端测试。

```toml
[package]
  cjc-version = "1.1.0"
  compile-option = "--dy-std --cfg=\"${COMPILE_CONDITION_ENTRY}\""
  description = "CangjieUI Application"
  link-option = "--unresolved-symbols=ignore-all"
  name = "ohos_app_cangjie_entry_test"
  output-type = "dynamic"
  src-dir = "."
  target-dir = ""
  version = "1.0.0"
  package-configuration = {}
  scripts = {}

[dependencies]
  [dependencies.ohos_app_cangjie_entry]
    path = "../../../"
    version = "1.0.0"

[profile]
  [profile.build]
    incremental = true
    lto = ""
  [profile.customized-option]
    debug = "-g -Woff all -Won apilevel-check"
    release = "--fast-math -O2 -s -Woff all -Won apilevel-check"
    withoutCoverage = "--cfg=\"coverage=false\""
    withCoverage = "--cfg=\"coverage=true\""
  [profile.test]

[target.aarch64-linux-ohos]
  compile-option = "-B \"${DEVECO_CANGJIE_HOME}/build-tools/third_party/llvm/bin\" -B \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/aarch64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/aarch64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/clang/15.0.4/lib/aarch64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/aarch64-linux-ohos\" --sysroot \"${DEVECO_OH_NATIVE_HOME}/sysroot\""
[target.aarch64-linux-ohos.bin-dependencies]
  path-option = ["${AARCH64_LIBS}", "${AARCH64_MACRO_LIBS}", "${AARCH64_KIT_LIBS}"]
  package-option = {}

[target.x86_64-linux-ohos]
  compile-option = "-B \"${DEVECO_CANGJIE_HOME}/build-tools/third_party/llvm/bin\" -B \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/x86_64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/sysroot/usr/lib/x86_64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/clang/15.0.4/lib/x86_64-linux-ohos\" -L \"${DEVECO_OH_NATIVE_HOME}/llvm/lib/x86_64-linux-ohos\" --sysroot \"${DEVECO_OH_NATIVE_HOME}/sysroot\""
[target.x86_64-linux-ohos.bin-dependencies]
  path-option = ["${X86_64_OHOS_LIBS}", "${X86_64_OHOS_MACRO_LIBS}", "${X86_64_OHOS_KIT_LIBS}"]

[target.x86_64-unknown-windows-gnu.bin-dependencies]
  path-option = ["${X86_64_LIBS}", "${X86_64_MACRO_LIBS}"]
  package-option = {}
```

### entry/src/test/cangjie/cjpm.toml

**路径**：`entry/src/test/cangjie/cjpm.toml`

**说明**：本地测试模块的仓颉包管理配置。

```toml
[package]
  cjc-version = "1.1.0"
  compile-option = "--dy-std --cfg=\"${COMPILE_CONDITION_ENTRY}\""
  description = "CangjieUI Application"
  link-option = ""
  name = "ohos_app_cangjie_entry_local_test"
  output-type = "dynamic"
  src-dir = "."
  target-dir = ""
  version = "1.0.0"
  package-configuration = {}
  scripts = {}

[profile]
  [profile.build]
    incremental = true
    lto = ""
  [profile.customized-option]
    debug = "-g -Woff all -Won apilevel-check"
    release = "--fast-math -O2 -s -Woff all -Won apilevel-check"
  [profile.test]
```

---

## 资源文件

### string.json

**路径**：`entry/src/main/resources/base/element/string.json`

**说明**：字符串资源文件。

**需要替换**：根据项目需要修改字符串值。

```json
{
  "string": [
    {
      "name": "module_desc",
      "value": "module description"
    },
    {
      "name": "EntryAbility_desc",
      "value": "description"
    },
    {
      "name": "EntryAbility_label",
      "value": "label"
    }
  ]
}
```

### color.json

**路径**：`entry/src/main/resources/base/element/color.json`

**说明**：颜色资源文件。

```json
{
  "color": [
    {
      "name": "start_window_background",
      "value": "#FFFFFF"
    }
  ]
}
```

### main_pages.json

**路径**：`entry/src/main/resources/base/profile/main_pages.json`

**说明**：页面路由配置文件。

```json
{
}
```

### layered_image.json

**路径**：`entry/src/main/resources/base/media/layered_image.json`

**说明**：分层图标配置文件。

```json
{
  "layered-image":
  {
    "background" : "$media:background",
    "foreground" : "$media:foreground"
  }
}
```

---

## Hvigor 配置

### hvigor-config.json5

**路径**：`hvigor/hvigor-config.json5`

**说明**：Hvigor 构建工具配置文件。

```json5
{
  "modelVersion": "6.0.2",
  "dependencies": {
  },
  "execution": {
    // "analyze": "normal",                     /* Define the build analyze mode. Value: [ "normal" | "advanced" | "ultrafine" | false ]. Default: "normal" */
    // "daemon": true,                          /* Enable daemon compilation. Value: [ true | false ]. Default: true */
    // "incremental": true,                     /* Enable incremental compilation. Value: [ true | false ]. Default: true */
    // "parallel": true,                        /* Enable parallel compilation. Value: [ true | false ]. Default: true */
    // "typeCheck": false,                      /* Enable typeCheck. Value: [ true | false ]. Default: false */
    // "optimizationStrategy": "memory"         /* Define the optimization strategy. Value: [ "memory" | "performance" ]. Default: "memory" */
  },
  "logging": {
    // "level": "info"                          /* Define the log level. Value: [ "debug" | "info" | "warn" | "error" ]. Default: "info" */
  },
  "debugging": {
    // "stacktrace": false                      /* Disable stacktrace compilation. Value: [ true | false ]. Default: false */
  },
  "nodeOptions": {
    // "maxOldSpaceSize": 8192                  /* Enable nodeOptions maxOldSpaceSize compilation. Unit M. Used for the daemon process. Default: 8192*/
    // "exposeGC": true                         /* Enable to trigger garbage collection explicitly. Default: true*/
  }
}
```

---

## 图片资源文件

图片资源已包含在 skill 的 `references/assets/media/` 目录中，创建项目时自动拷贝：

| 源文件路径 | 目标路径 | 用途 |
|------------|----------|------|
| `references/assets/media/background.png` | `entry/src/main/resources/base/media/background.png` | 应用图标背景层 |
| `references/assets/media/foreground.png` | `entry/src/main/resources/base/media/foreground.png` | 应用图标前景层 |
| `references/assets/media/startIcon.png` | `entry/src/main/resources/base/media/startIcon.png` | 启动页图标 |

**拷贝命令**：
```bash
mkdir -p <项目目录>/entry/src/main/resources/base/media/
cp references/assets/media/*.png <项目目录>/entry/src/main/resources/base/media/
```