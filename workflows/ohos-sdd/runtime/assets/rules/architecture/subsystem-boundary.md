# Rule: 子系统边界

## Rule ID

OH-ARCH-SUBSYSTEM

## Applies To

- Feature Design
- Feature Spec
- Task Spec
- AI implementation
- Design / GB 基线审查

适用于跨子系统、跨仓、跨部件调用，以及新增模块边界或依赖关系的变更。

## Must

- 必须明确每个受影响子系统、部件、模块的职责。
- 必须通过公开接口、System API、IPC/SAF 或既有协议进行跨子系统交互。
- 必须在设计中说明调用方、被调用方、接口契约和数据流。
- 必须在 bundle.json 或 BUILD.gn 中显式声明必要依赖。
- 必须在 `context-references` 中记录跨仓上下文查询和关键参考文件。

## Must Not

- 禁止跨子系统引用内部实现类、私有头文件或私有模块。
- 禁止绕过公开接口直接链接其他子系统内部库。
- 禁止通过共享全局变量、直接内存访问或隐式文件路径耦合子系统。
- 禁止新增子系统间循环依赖。
- 禁止把本应由目标子系统承担的职责放到调用方中规避边界。

## Evidence

- 子系统/部件/模块职责表。
- 跨子系统调用关系图或数据流表。
- 公开接口、IPC/SAF、协议或 API 路径说明。
- BUILD.gn/bundle.json 依赖变更。
- DeepWiki/源码查询记录。

## Check

- 检查跨子系统调用是否经过允许的接口机制。
- 检查是否引用了其他子系统的内部路径、内部类或未公开头文件。
- 检查依赖声明是否完整且无循环。
- 检查职责划分是否符合现有仓和模块边界。
