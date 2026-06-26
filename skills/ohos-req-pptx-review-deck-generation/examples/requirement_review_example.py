# -*- coding: utf-8 -*-
"""AI Input Control Standard — 需求评审 Deck (按评审 PPT 模板).
Source: docs/features/ai-input-control-standard/04-feature.md
Fields absent from the source doc are marked 待评估/TBD."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deckbuilder import Deck

TBD = "待评估 / TBD"
deck = Deck()

# Cover --------------------------------------------------------------------
deck.cover(
    "PC 端 AI Agent Input 元素标准化操控规范",
    subtitle="智能、精准、无感的表单填充 — 需求评审",
    meta_lines=["ArkWeb SIG / AI Agent", "需求评审稿  2026-06-24"],
)

# P1. 需求性质与工作量概览 -------------------------------------------------
deck.table_slide("一、需求性质与工作量概览",
    ["分类", "说明"],
    [
        ["需求性质", "新增能力（非缺陷修复 / 非纯重构）；建立标准化 AI 操控 Input 元素规范；AI Agent 通过 NWeb API 实现智能表单填充；分两阶段交付"],
        ["复杂度驱动", "涉及 4 个代码仓（chromium_src / chromium_cef / chromium_arkweb / web_webview）；触及内核事件触发 + CEF API + ArkWeb 解耦层 + NWeb 接口四层；Phase 1 低风险先行，Phase 2 高风险（文件上传/原生选择器）跟进"],
        ["工作量概览", "总工作量约 7.0 人月（估算，详见 P8）；5 个 Proposal 按代码仓拆分；估算口径 S=0.5 / M=1 / L=2 人月；人员待指派"],
    ],
    takeaway="结论：新增能力，分两阶段交付；总工作量约 7.0 人月，涉及 4 个代码仓",
    col_widths=[1.8, 7])

# P2. 原始需求描述 ---------------------------------------------------------
deck.table_slide("二、原始需求描述",
    ["分类", "说明"],
    [
        ["需求来源", "来源产品：待产品确认 (TBD)；ArkWeb SIG / AI Agent 方向"],
        ["需求场景", "PC 端 AI Agent 需自动化填充 Web 表单（文本/数字/日期/文件等）；不同 Input 类型操控策略不统一，缺乏标准化事件注入机制"],
        ["需求描述", "AI Agent 通过 NWeb API 操控 Web 页面 Input 元素；实现 input/change/click/select 标准化事件注入；分阶段覆盖所有 HTML5 Input 类型"],
        ["特性概述", "Phase 1（P0）：文本/数字类操控（text/number/email/password/search/tel/url）；Phase 2（P1）：日期时间/文件上传/滑块/选项类操控；全阶段标准化事件注入"],
        ["影响范围与限制", "仅 PC 端标准 HTML5 表单元素；不含移动端 / Vue/React 自定义组件 / IE 模式；后续版本考虑 color/image 类型"],
        ["适用范围", "适用产品/地区：待确认 (TBD)；覆盖所有基于 ArkWeb 的 PC 端 AI 应用"],
    ],
    takeaway="结论：仅 PC 端标准 HTML5 表单元素，P0 文本类先行、P1 复杂类跟进",
    col_widths=[1.8, 7])

# P3. 特性及价值点 ---------------------------------------------------------
deck.table_slide("三、特性及价值点",
    ["分类", "说明"],
    [
        ["用户痛点", "PC 端 AI Agent 手动填充表单效率低、易出错；不同 Input 类型操控策略不统一；缺少标准化的事件注入机制导致事件触发不完整"],
        ["需求价值", "智能、精准、无感的表单填充；操作效率提升 40%；填充成功率达 98%；增强 AI Agent 能力，拓展 PC 端应用场景"],
        ["功能点与主要场景", "智能意图识别 → 类型映射 → 策略编排 → 事件注入；文本/数字类（Phase 1）；日期时间/文件上传/滑块/选项类（Phase 2）"],
        ["可量化目标", "填充成功率 ≥ 98%（50+ 表单测试集）；单表单耗时 ≤ 200ms；AI 意图识别 ≥ 90%；事件触发覆盖率 100%"],
    ],
    takeaway="结论：智能精准无感填充，效率 +40%、成功率 98%、单表单 ≤ 200ms",
    col_widths=[1.8, 7])

# P4a. 系统设计方案 — 高层架构 (跨仓模块交互) ------------------------------
deck.architecture_slide("四、系统设计方案（1/3）：跨仓模块交互", [
    {"id": "ai", "title": "AI Agent 应用", "lines": ["意图解析 / 操控编排"], "row": 0, "col": 1},
    {"id": "web", "title": "Web 页面", "lines": ["Input 元素 / 表单"], "row": 0, "col": 2},
    {"id": "nweb", "title": "web_webview", "lines": ["NWeb 接口定义 (nweb.h)"], "row": 1, "col": 1},
    {"id": "arkweb", "title": "chromium_arkweb", "lines": ["解耦层 ext/cef_ext/nweb"], "row": 2, "col": 1, "change": True},
    {"id": "cef", "title": "chromium_cef", "lines": ["CEF Input API"], "row": 2, "col": 0, "change": True},
    {"id": "src", "title": "chromium_src", "lines": ["Blink Input/Event 扩展"], "row": 2, "col": 2, "change": True},
], edges=[
    {"from": "ai", "to": "nweb", "label": "调用 NWeb API", "dir": "f", "accent": "accent"},
    {"from": "nweb", "to": "arkweb", "label": "接口实现", "dir": "f", "accent": "accent"},
    {"from": "arkweb", "to": "cef", "label": "ohos_cef_ext 同步", "dir": "both", "accent": "grey"},
    {"from": "arkweb", "to": "src", "label": "chromium_ext 同步", "dir": "both", "accent": "grey"},
    {"from": "src", "to": "web", "label": "DOM 事件触发", "dir": "f", "accent": "accent"},
], note=[
    "青绿＝数据/调用主链路；灰色＝解耦层同步依赖。涉及 4 个代码仓，同属 ArkWeb SIG。",
], takeaway="结论：变更集中在 chromium_src/cef/arkweb 三仓，NWeb 接口纯新增")

# P4b. 系统设计方案 — 控制面/数据面 ----------------------------------------
deck.layered_diagram_slide("四、系统设计方案（2/3）：控制面 / 数据面与变更点", [
    {"label": "控制面", "nodes": [
        {"title": "AI 意图解析", "lines": ["语义理解 / 意图识别"], "col": 0},
        {"title": "操控策略编排", "lines": ["Input 类型→策略映射"], "col": 1, "change": True},
    ]},
    {"label": "数据面", "nodes": [
        {"title": "NWeb API 调用", "lines": ["SendInputEvent"]},
        {"title": "ArkWeb 解耦层", "lines": ["chromium_ext 转发"], "change": True},
        {"title": "CEF Input API", "lines": ["事件封装"], "change": True},
        {"title": "Blink 事件触发", "lines": ["dispatchEvent"], "change": True},
        {"title": "表单填充", "lines": ["Input 元素更新"]},
    ]},
], connect=[[[0, 1], [1, 0]]],
   note=[
    "变更点：新增操控策略映射库；ArkWeb 解耦层/CEF/Blink 新增 Input 操控事件封装。",
    "控制面低频（AI 解析）→数据面高频（事件触发 ≤ 200ms/表单）。",
], takeaway="结论：控制面新增策略映射，数据面三仓新增 Input 事件封装")

# P4c. 系统设计方案 — 影响分析 ---------------------------------------------
deck.table_slide("四、系统设计方案（3/3）：对 OpenHarmony 的影响分析",
    ["维度", "变更与影响"],
    [
        ["数据结构变更", "chromium_src 新增 Input 操控事件封装 / InputType 枚举；CEF 新增 SendInputEvent/SendFileEvent API；ArkWeb 解耦层同步扩展"],
        ["外部接口变更", "新增 NWeb 接口（SendInputEvent / SendFileEvent / InputType 枚举）；现有 NWeb API 无修改；不新增公开 ArkTS/NAPI"],
        ["外部依赖分析", "AI Agent 应用层依赖 NWeb API；四仓解耦层同步依赖（chromium_ext / ohos_cef_ext）；无新增三方依赖"],
        ["性能 / 功耗", "单表单填充 ≤ 200ms；事件触发链路为同步调用，无额外异步开销；无新增常驻进程或高频轮询"],
        ["关键 KPI", "填充成功率 ≥ 98%；事件触发覆盖率 100%；AI 意图识别 ≥ 90%；单表单耗时 ≤ 200ms"],
        ["对用户/周边领域", "纯新增能力，不影响现有 Web 页面渲染和事件处理；仅 AI Agent 主动调用时触发"],
    ],
    takeaway="结论：纯新增 NWeb 接口与内核事件封装，现有 API 与页面渲染零影响",
    col_widths=[2, 6])

# P5. 兼容性分析 -----------------------------------------------------------
deck.table_slide("五、兼容性分析",
    ["兼容性维度", "评估与结论"],
    [
        ["系统机制 / 功能变化", "新增 Input 操控能力；现有 ArkWeb 应用和 NWeb 接口行为不变"],
        ["系统权限管理变化", "无变化；AI Agent 调用 NWeb API 沿用现有权限机制"],
        ["API 行为变化", "纯新增 API（SendInputEvent / SendFileEvent / InputType 枚举）；现有 API 无修改"],
        ["其它应用行为变化", "不影响现有 Web 页面渲染和事件处理；仅 AI Agent 主动调用时触发"],
        ["结论 / 适配计划", "纯新增能力，无兼容性影响；现有应用无需适配"],
    ],
    col_widths=[2.4, 6],
    takeaway="结论：纯新增 API、现有行为不变，应用无需适配（无兼容性影响）")

# P6. RAM / ROM 评估 -------------------------------------------------------
deck.table_slide("六、RAM / ROM 评估",
    ["维度", "项目", "估算值", "说明"],
    [
        ["RAM", "Input 类型映射库", "< 1 KB（估算）", "静态映射表，按 InputType 枚举索引"],
        ["RAM", "AI 意图解析上下文", "待实测", "应用层按需创建，与并发表单数相关"],
        ["RAM", "事件触发临时对象", "≈ 0", "同步调用后释放，无常驻开销"],
        ["RAM", "默认 / 未调用路径", "≈ 0", "懒创建，不预分配"],
        ["ROM", "chromium_src / cef / arkweb 代码新增", "+数十 KB（估算）", "仅新增 C++ 代码与单测"],
        ["ROM", "web_webview 接口定义", "+数 KB（估算）", "nweb.h 接口声明"],
        ["ROM", "新增资源（图片/SVG）", "无", "纯代码变更，无新增资源"],
        ["结论", "实测要求", "实现阶段输出", "Phase 1 完成后输出 RAM/ROM 实测报告"],
    ],
    takeaway="结论：未调用路径 RAM≈0、ROM 仅数十 KB 代码；Phase 1 后输出实测",
    col_widths=[0.9, 3.0, 2.0, 3.2])

# P7. 风险 Checklist -------------------------------------------------------
deck.table_slide("七、风险 Checklist",
    ["风险项", "评估"],
    [
        ["是否改变用户使用习惯", "否 — AI 自动操控对用户透明，无需用户行为变更"],
        ["是否有安全风险", "中 — password 类型填充需安全方案（不通过日志明文记录）；需 Security Team 评审"],
        ["是否涉及合法合规", "否 — 不涉及用户数据采集或隐私变更"],
        ["是否涉及外部承诺", "待确认 (TBD)"],
        ["性能 / 功耗 / RAM / ROM", "单表单填充 ≤ 200ms；纯代码新增，ROM 增量约数十 KB；RAM 按需创建，无常驻开销"],
        ["是否存在其他依赖", "依赖 chromium_src/cef/arkweb/webview 四仓协同；AI 意图解析模块设计 + 事件模拟库原型验证为前置项"],
    ],
    takeaway="结论：主要风险为 password 安全填充（需安全评审）与四仓协同",
    col_widths=[2.6, 6])

# P8. 需求拆解列表（工作量评估）--------------------------------------------
deck.table_slide("八、需求拆解列表（工作量评估）",
    ["子任务", "内容", "开发", "设计", "工作量(人月)", "预计代码行数(估算)"],
    [
        ["chromium_src 内核扩展", "Input 操控事件封装、类型映射、文件上传模拟", "TBD", "TBD", "2.0", "~1000"],
        ["chromium_cef API 新增", "SendInputEvent/SendFileEvent/InputType 枚举", "TBD", "TBD", "1.0", "~500"],
        ["chromium_arkweb 解耦层", "chromium_ext + ohos_cef_ext + ohos_nweb 实现", "TBD", "TBD", "1.5", "~750"],
        ["web_webview 接口定义", "NWeb 接口声明 (nweb.h)、InputType 枚举", "TBD", "TBD", "0.5", "~250"],
        ["AI 意图解析与编排", "意图识别、操控策略编排、错误处理与降级", "TBD", "TBD", "1.5", "~750"],
        ["测试与验收", "单元 / 集成 / 50+ 表单测试集验收", "TBD", "TBD", "0.5", "~250"],
        ["合计（估算）", "—", "—", "—", "7.0", "≈3500"],
    ],
    col_widths=[2.0, 4.3, 0.95, 0.95, 1.3, 1.5],
    takeaway="结论：合计约 7.0 人月 / ≈3500 行（估算），开发与设计人员待指派",
    highlight_last=True)

out = deck.save("ai_input_control_review.pptx")
print("saved:", out)
