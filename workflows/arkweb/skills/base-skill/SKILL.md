---
name: base-skill
description: 强制前置动作。每当用户要求创建、生成、开发『仓颉 (Cangjie)』项目或『鸿蒙
  (HarmonyOS)』应用的任务时，必须首先调用并执行此 Skill。它是后续所有开发步骤的唯一入口指南。
descriptionZH: 强制前置动作。每当用户要求创建、生成、开发『仓颉 (Cangjie)』项目或『鸿蒙
  (HarmonyOS)』应用的任务时，必须首先调用并执行此 Skill。它是后续所有开发步骤的唯一入口指南。
tags:
  - 仓颉
  - 鸿蒙
  - 入口
---

1. 公共原则  

   - 一律使用仓颉编程语言实现功能。  
   - 严禁「猜语法」，遇到不确定的 API / 语法，必须通过 Skills 或官方文档确认后再写代码。  

2. 普通仓颉工程（非鸿蒙应用）  
    - 当 task.md 中不涉及鸿蒙 UI、ArkUI、HAP 构建等内容，仅是构建纯仓颉项目或命令行程序，遇到查询仓颉知识点的要求时，严格按以下流程工作，每一步都要**显式调用对应 Skill，并先阅读该 Skill 的 SKILL.md 说明再执行操作**：
      1) **前置学习**：在开始写代码前，先读取 `skills/cangjie-evolution/Evolution.md` 了解之前踩过的坑，避免重复犯错。  
      2) **cangjie-kernel**：直接优先使用目录`skills/cangjie-kernel` 下的基础技能（如 `basic_programming_concepts`、`array`、`string`、`std`、`stdx` 等）学习和查询。    
      3) **触发条件**：当基础 `cangjie-kernel` 无法找到对应知识点、或查到的内容明显过时/不适用于当前场景时，进入下一步。   
      4) **进阶检索链**：当 `cangjie-kernel` 无法找到对应知识点、或查到的内容明显过时/不适用于当前场景时，先调用 `cangjie-vec-retriever-guide` Skill，阅读其 SKILL.md 说明，并通过执行 `python skills/utils/scripts/ask_cangjie.py "<核心关键词>"` 进行 L混合检索；若混合检索返回 `NO_RAG_RESULT` 或结果明显不相关/不足以支撑实现，则再调用 `cangjie-doc-search-guide` Skill，按照其中的文档检索逻辑，基于 `skills/utils/scripts/hm-docs/` 目录下的本地官方文档进行全量搜索与精读。    
      5) **经验记录**：将构建过程中踩到的坑记录到 `skills/cangjie-evolution/Evolution.md` 中（注意：此文件与鸿蒙的 Evolution.md 独立）。 
      6) **修复报错**：每次修复报错前，先读取 `skills/cangjie-evolution/Evolution.md` 了解之前踩过的坑，避免重复犯错。   
      7) **配置文件:** 如果你的项目依赖了特定版本或外部模块，请使用工具修改自动生成的 `cjpm.toml`。
         如果你的代码中使用了 `stdx`，你**必须强制执行**以下步骤，否则编译一定会失败：
         1. 使用文件编辑工具，在当前生成项目的 `cjpm.toml` 末尾**必须**完整追加以下依赖声明。
         2. **关键绝对路径拼接**：注意你当前所在的工作目录可能是 `outputs/<项目名>`。你必须使其绝对指向目录 `skills/cangjie-stdx-dependency/stdx/dynamic/stdx`。
            ```toml
            # 示例配置如下：
            [target.x86_64-w64-mingw32]
               [target.x86_64-w64-mingw32.bin-dependencies]
                  path-option = ["D:/Projects/claude/cangjie-harmonyos-build/skills/cangjie-stdx-dependency/stdx/dynamic/stdx"]
            ```
            **注意**：Windows 系统路径必须使用正斜杠 `/`。严禁去修改 stdx 文件夹内的任何文件！

         3. 注意：stdx 本地库已预编译完成，无需额外修复版本字段。如果编译时报 stdx 相关错误，请检查路径配置是否正确。
         
         修复官方本地库的版本空缺 Bug：使用文件读取工具查看 `cjpm.toml` 文件。如果发现其中的 `cjc-version` 字段为空（如 `cjc-version = ""`）或缺失，**必须**使用文件编辑工具（如 `replace_in_file`）将其修改为 `cjc-version = "1.0.4"`。

3. 鸿蒙应用开发任务（HarmonyOS + 仓颉）  
   - 当 task.md 中要求开发鸿蒙应用（如 ArkUI、HAP 构建、module.json5、鸿蒙页面/组件等）时，严格按以下流程工作，每一步都要**显式调用对应 Skill，并先阅读该 Skill 的 SKILL.md 说明再执行操作**：  
     1) **需求分析（L0）**：调用 `harmonyos-requirement-analysis` Skill，先阅读其 SKILL.md 中的需求分析模板与示例，然后按照该 Skill 的流程将业务需求拆解成 UI 组件、数据结构和交互行为，不直接查业务词。  
     2) **基础仓颉技能优先**：在 L0 分析之后，调用 `skills/cangjie-kernel` 中对应的基础技能（如 `array`、`string`、`function`、`std`、`stdx` 等 Skill），阅读各自 SKILL.md 的用法说明，再按照其中的示例完成语法、类型和标准库层面的推理与修复。    
     3) **混合查询**：如需进一步知识检索，调用 `harmonyos-vec-retriever-guide` Skill，先阅读该 Skill 的 SKILL.md 中的环境配置、查询策略和脚本路径说明，再通过 `skills/utils/scripts/ask_cangjie.py` 按 API 关键字逐个检索。  
     4) **本地文档搜索**：如需进一步知识检索，调用 `harmonyos-doc-search-guide` Skill，按照其 SKILL.md 中的初始化说明，首次使用或需要确保官方文档已初始化时，可以执行 `python ask_cangjie.py "test"` 生成本地文档树（初始化）；当 混合查询 无结果或不够时，再根据该 Skill 中给出的路径和搜索命令，基于 `skills/utils/scripts/hm-docs/` 做本地官方文档搜索（UI、语法、stdx 文档），不要直接访问 `cangjie-docs-full`。  
     5) **stdx 依赖配置**：当鸿蒙工程中需要 stdx 能力或出现 stdx 相关构建错误时，调用 `harmonyos-stdx-dependency` Skill，先阅读其 SKILL.md，按照其中描述的「解压到 `<项目根>/cjnative/stdx` + 修改 entry/cjpm.toml bin-dependencies.path-option」的步骤，通过 `skills/harmonyos-stdx-dependency/` 中的资源自动或半自动完成配置。  
     6) **构建与排错**：调用 `harmonyos-build` Skill，严格按照其 SKILL.md 中的说明复制并执行 `build.py`，获取 `build-full.log`，每一次报错必须必须按文档中规定的优先级：先查 Evolution.md → 再用 `skills/cangjie-kernel` 调试 → 再用 `harmonyos-vec-retriever-guide` 调试 → 最后用 `harmonyos-doc-search-guide` 文档，分步处理构建错误。必须注意每一次鸿蒙项目构建报错都要按照skill的要求处理。
     7) **迭代记录**：每次构建成功后，调用 `harmonyos-evolution` Skill，阅读其 SKILL.md 中给出的记录格式和示例，将本次遇到的重要问题与解决方案记录到 `skills/utils/Evolution.md` 中，以便在后续项目中迁移复用。