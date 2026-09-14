---
name: ohos-dev-lite-adaptation
description: OpenHarmony Lite (L0/L1) 芯片适配 7 阶段工作流入口。Use when adapting an OpenHarmony Lite L0/L1 chip or board; triggers include 适配、移植、bring-up、board bring-up、走工作流、进入下一阶段、defconfig、HCS、HDF、BUILD.gn、XTS、烧录、HiBurn、LiteOS、交叉编译. 编译、测试或诊断请求路由到对应专用 skill。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: adaptation
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite 芯片适配工作流

本文件是公共入口。编排 P1–P7 七个阶段，执行基于证据的 GATE 门控，将阶段内工作路由到 [`skills/`](skills/) 下的各能力 skill。执行开始时读取完整 router 契约 [`skills/ohos-dev-workflow-router/SKILL.md`](skills/ohos-dev-workflow-router/SKILL.md)；阶段资产在 [`runtime/assets/workflow/`](runtime/assets/workflow/)。

没有对应证据不得声称门控通过。硬件或厂商 SDK 不可用时，如实记录为跳过或未验证，并保持工作流检查点明确。
