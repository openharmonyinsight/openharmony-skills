---
name: harmonyos-project-init
description: 当用户要求创建、初始化、新建仓颉鸿蒙项目时，必须首先调用此
  Skill。当用户说『创建一个鸿蒙应用』、『新建仓颉鸿蒙工程』、『初始化鸿蒙项目』、『帮我搭建一个鸿蒙App』、『我要开发一个HarmonyOS应用』等表述时，触发此
  Skill。此 Skill 提供完整的项目模板结构和文件内容，用于从零开始创建一个可运行的仓颉鸿蒙 Hello World 项目。
descriptionZH: 当用户要求创建、初始化、新建仓颉鸿蒙项目时，必须首先调用此
  Skill。当用户说『创建一个鸿蒙应用』、『新建仓颉鸿蒙工程』、『初始化鸿蒙项目』、『帮我搭建一个鸿蒙App』、『我要开发一个HarmonyOS应用』等表述时，触发此
  Skill。此 Skill 提供完整的项目模板结构和文件内容，用于从零开始创建一个可运行的仓颉鸿蒙 Hello World 项目。
tags:
  - 鸿蒙
  - 项目初始化
  - HarmonyOS
  - 仓颉
---

# 仓颉鸿蒙项目初始化 Skill

## 目的

从零创建一个完整的仓颉鸿蒙（Cangjie + HarmonyOS）项目结构，使项目能够直接构建运行。

## 适用场景

- 用户要求创建新的鸿蒙应用项目
- 用户说"我想开发一个鸿蒙App"
- 用户需要初始化仓颉鸿蒙工程
- 用户没有现有项目，需要从头开始

## 项目创建流程

### 步骤 1：确认项目基本信息

在创建项目前，向用户确认以下信息：

1. **项目名称**：如 `MyApp`、`TodoApp` 等
2. **包名（bundleName）**：如 `com.example.myapp`，默认可使用 `com.example.<项目名>`
3. **项目路径**：项目存放的目录路径

如果用户未指定，使用以下默认值：
- 项目名称：`MyApplication`
- 包名：`com.example.myapplication`
- 路径：当前工作目录下创建以项目名命名的文件夹

### 步骤 2：创建项目目录结构

项目目录结构如下：

```
<项目名>/
├── .gitignore
├── build-profile.json5          # 项目级构建配置
├── code-linter.json5            # 代码检查配置
├── hvigorfile.ts                # 项目级 Hvigor 脚本
├── oh-package.json5             # 项目依赖配置
├── AppScope/
│   └── app.json5                # 应用全局配置
├── entry/                       # 主模块
│   ├── build-profile.json5      # 模块级构建配置
│   ├── hvigorfile.ts            # 模块级 Hvigor 脚本
│   ├── oh-package.json5         # 模块依赖配置
│   ├── cjpm.toml                # 仓颉包管理配置
│   ├── cjpm.lock                # 仓颉包锁定文件
│   └── src/
│       └── main/
│           ├── cangjie/         # 仓颉源代码目录
│           │   ├── ability_stage.cj
│           │   ├── index.cj
│           │   └── main_ability.cj
│           ├── module.json5     # 模块配置
│           └── resources/       # 资源文件
│               └── base/
│                   ├── element/
│                   │   ├── string.json
│                   │   └── color.json
│                   ├── media/
│                   │   ├── background.png
│                   │   ├── foreground.png
│                   │   ├── startIcon.png
│                   │   └── layered_image.json
│                   └── profile/
│                       └── main_pages.json
│       ├── ohosTest/
│       │   └── cangjie/
│       │       └── cjpm.toml    # ohosTest 模块配置
│       └── test/
│           └── cangjie/
│               └── cjpm.toml    # 本地测试模块配置
└── hvigor/
    └── hvigor-config.json5      # Hvigor 配置
```

### 步骤 3：写入模板文件

**重要**：所有模板文件内容请参阅 `references/project-template.md`。

按照以下顺序创建文件：

1. **根目录配置文件**
   - `.gitignore`
   - `build-profile.json5` - 需要替换 `bundleName` 为用户指定的包名
   - `code-linter.json5`
   - `hvigorfile.ts`
   - `oh-package.json5`

2. **AppScope 配置**
   - `AppScope/app.json5` - 需要替换 `bundleName`

3. **entry 模块配置**
   - `entry/build-profile.json5`
   - `entry/hvigorfile.ts`
   - `entry/oh-package.json5`
   - `entry/cjpm.toml` - 仓颉包管理配置（环境变量由构建脚本自动注入）
   - `entry/cjpm.lock` - 仓颉包锁定文件

4. **模块源码和配置**
   - `entry/src/main/module.json5` - 需要替换包名引用
   - `entry/src/main/cangjie/ability_stage.cj` - 需要替换包名
   - `entry/src/main/cangjie/index.cj` - 需要替换包名
   - `entry/src/main/cangjie/main_ability.cj` - 需要替换包名

5. **测试模块配置**
   - `entry/src/ohosTest/cangjie/cjpm.toml` - ohosTest 模块配置
   - `entry/src/test/cangjie/cjpm.toml` - 本地测试模块配置

6. **资源文件**
   - `entry/src/main/resources/base/element/string.json`
   - `entry/src/main/resources/base/element/color.json`
   - `entry/src/main/resources/base/profile/main_pages.json`
   - `entry/src/main/resources/base/media/layered_image.json`

7. **Hvigor 配置**
   - `hvigor/hvigor-config.json5`

### 步骤 4：包名替换规则

模板文件中需要替换以下占位符：

| 占位符 | 替换内容 | 示例 |
|--------|----------|------|
| `com.example.myapplication` | 用户指定的包名 | `com.mycompany.todoapp` |
| `ohos_app_cangjie_entry` | 仓颉包名（基于 bundleName 生成） | `ohos_app_cangjie_entry` 或根据包名生成 |

**包名转换规则**：
- bundleName: `com.example.myapplication` → 仓颉包名: `ohos_app_cangjie_entry`
- 这里的 `ohos_app_cangjie_entry` 是固定格式，不需要根据 bundleName 变化

### 步骤 5：拷贝图片资源文件

图片资源已打包在 skill 的 `references/assets/media/` 目录中，需要自动拷贝到项目：

**拷贝命令示例**（假设 skill 路径为 `skills/harmonyos-project-init`）：

```bash
# 创建目标目录
mkdir -p <项目目录>/entry/src/main/resources/base/media/

# 拷贝图片资源
cp skills/harmonyos-project-init/references/assets/media/background.png <项目目录>/entry/src/main/resources/base/media/
cp skills/harmonyos-project-init/references/assets/media/foreground.png <项目目录>/entry/src/main/resources/base/media/
cp skills/harmonyos-project-init/references/assets/media/startIcon.png <项目目录>/entry/src/main/resources/base/media/
```

**图片资源说明**：
| 文件 | 用途 |
|------|------|
| `background.png` | 应用图标背景层 |
| `foreground.png` | 应用图标前景层 |
| `startIcon.png` | 启动页图标 |

## 项目创建完成后的操作

项目创建完成后，告知用户后续步骤：

1. **使用 DevEco Studio 打开项目**（推荐）
   - 打开 DevEco Studio
   - 选择 "Open Project"
   - 选择创建的项目目录

2. **安装依赖**
   ```bash
   cd <项目目录>
   ohpm install
   ```

3. **构建项目**
   - 参考 `harmonyos-build` Skill 执行构建

4. **开始开发**
   - 参考 `base-skill` Skill 了解开发流程
   - 参考 `harmonyos-requirement-analysis` Skill 进行需求分析

## 关键文件说明

### app.json5 - 应用全局配置
定义应用的基本信息，包括 bundleName（包名）、版本号、应用图标和名称。

### module.json5 - 模块配置
定义模块的基本信息，包括：
- `name`: 模块名称
- `type`: 模块类型（entry 表示主模块）
- `mainElement`: 主 Ability 名称
- `abilities`: Ability 列表配置

### main_ability.cj - 主 Ability
应用的入口点，继承自 `UIAbility`，处理应用生命周期事件。

### index.cj - 入口页面
使用仓颉 ArkUI 声明式语法编写的主页面，包含 `@Entry` 和 `@Component` 注解。

### ability_stage.cj - AbilityStage
Ability 的生命周期管理类，在 Ability 创建时调用。

## 注意事项

1. **路径格式**：Windows 系统路径使用正斜杠 `/`
2. **编码格式**：所有 `.json5` 文件使用 UTF-8 编码
3. **包名规范**：bundleName 必须使用反向域名格式，如 `com.company.appname`
4. **首次构建**：首次构建前需要执行 `ohpm install` 安装依赖

## 与其他 Skill 的关系

此 Skill 仅负责创建初始项目结构。创建完成后，后续开发应调用：

- `base-skill` - 开发流程总入口
- `harmonyos-build` - 项目构建
- `harmonyos-requirement-analysis` - 需求分析
- `harmonyos-evolution` - 问题记录与进化