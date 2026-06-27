# ohos-dev-arkuix-framework-api-adapter

Guide OHOS modules cross-platform adaptation with automated architecture analysis, code sync, configuration generation, and E2E verification. Use for adapting OHOS subsystem modules (@ohos.data.preferences, @ohos.intl, @ohos.multimedia.image, etc.) to Android/iOS. Provides 7-phase workflow: info collection → code sync → API analysis → architecture analysis → recommendation → implementation → E2E verification. Includes automated scripts for DTS analysis, architecture analysis, and configuration generation.

## Domain 说明

本 Skill 归属于 `domain/arkui` 命名空间，但机器名中使用 `arkuix` 作为 domain 细分。

- `arkui` — 标准 HarmonyOS ArkUI 框架
- `arkuix` — ArkUI-X 跨平台框架（Android/iOS），是 `arkui` 的跨平台延伸

本 Skill 专用于 ArkUI-X 跨平台场景下的 OHOS 模块适配，因此使用 `arkuix` 作为 domain 以区分标准 ArkUI 能力。