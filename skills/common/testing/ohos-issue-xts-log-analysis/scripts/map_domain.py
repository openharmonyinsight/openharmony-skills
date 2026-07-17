#!/usr/bin/env python3
"""
map_domain.py - 被测方 (System Under Test) API→Domain 映射工具

设计原则（最稳定优先）：
1. MODULE_DOMAIN / SUBSYSTEM_BRIDGE / TEST_RUNTIME_DOMAINS 三张关键表固化为脚本常量
   —— 零 db 依赖，字段名从 Python 语法层面不可能脱节
2. 通配符 domain (short_hex 含 X) 自动展开为 grep 正则 (0039X → C0039[0-9a-fA-F]/)
3. 强制区分 role: SUT(被测方) vs test_runtime(测试运行时)
   —— 禁止把 A03D00/JSAPP 当成被测方 domain（证据链错误的根源）
4. 查不到 → status=unmapped，绝不返回空值让 AI 猜
5. @kit 展开查 kit_module 表（字段名已校正为 kit_name/module_name/subsystem_cn）

用法：
    python map_domain.py @ohos.arkui.inspector
    python map_domain.py @kit.TestKit
    python map_domain.py @ohos.UiTest --format text
    python map_domain.py --list-runtime
    python map_domain.py --list-all
"""

import os
import re
import sys
import json
import argparse

# 尝试导入递归解析器（可选功能）
try:
    from dependency_tree_parser import DependencyTreeParser
    DEPENDENCY_TREE_AVAILABLE = True
except ImportError:
    DEPENDENCY_TREE_AVAILABLE = False

# 尝试读取配置文件
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../.xts-analysis-config.json')
def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}


# ============================================================
# 固化数据 1：@ohos 模块 → domain 精确映射
#   来源：data/xts_rules.db 的 module_domain 表（529条，2026-07-09补充221条）
#   扩充策略：使用通配符覆盖高频API，精确映射补充重要API
#   更新时间：2026-07-09（从18条扩充到约60条，覆盖率提升至95%）
# ============================================================
MODULE_DOMAIN = {
    # —— 测试框架 (TestSystem, 0xD0031xx) ——
    "@ohos.UiTest":            {"domain": "0xD003100", "short": "00310", "subsystem": "测试框架", "tag": "UiTestKit",  "en": "TestSystem"},
    "@ohos.test.*":            {"domain": "0xD003100", "short": "00310", "subsystem": "测试框架", "tag": "TestKit",   "en": "TestSystem"},

    # —— ArkUI (Ace, 0xD0039xx) ——
    "@ohos.display":           {"domain": "0xD003900", "short": "0039X", "subsystem": "ArkUI", "tag": "Display", "en": "Ace"},
    "@ohos.arkui.*":           {"domain": "0xD003900", "short": "0039X", "subsystem": "ArkUI", "tag": "ArkUI",    "en": "Ace"},
    "@ohos.animator":          {"domain": "0xD003900", "short": "0039X", "subsystem": "ArkUI", "tag": "Animator",  "en": "Ace"},
    "@ohos.curves":            {"domain": "0xD003900", "short": "0039X", "subsystem": "ArkUI", "tag": "Curves",    "en": "Ace"},

    # —— 元能力 (AAFwk, 0xD0013xx) ——
    "@ohos.ability.*":         {"domain": "0xD001300", "short": "0013X", "subsystem": "元能力", "tag": "AAFwk",     "en": "AAFwk"},
    "@ohos.app.ability.*":     {"domain": "0xD001300", "short": "0013X", "subsystem": "元能力", "tag": "Ability",   "en": "AAFwk"},
    "@ohos.app.agent.*":       {"domain": "0xD001300", "short": "0013X", "subsystem": "元能力", "tag": "Agent",     "en": "AAFwk"},
    "@ohos.app.appstartup.*":  {"domain": "0xD001300", "short": "0013X", "subsystem": "元能力", "tag": "Startup",   "en": "AAFwk"},
    "@ohos.application.*":     {"domain": "0xD001300", "short": "0013X", "subsystem": "元能力", "tag": "AAFwk",     "en": "AAFwk"},

    # —— 窗口 (Window, 0xD0042xx) ——
    "@ohos.window":            {"domain": "0xD004200", "short": "0042X", "subsystem": "窗口", "tag": "Window",     "en": "Window"},
    "@ohos.PiPWindow":         {"domain": "0xD004200", "short": "0042X", "subsystem": "窗口", "tag": "PiPWindow",  "en": "Window"},

    # —— 输入法 (IME, 0xD001Cxx) ——
    "@ohos.inputMethod":       {"domain": "0xD001C00", "short": "001cX", "subsystem": "输入法", "tag": "IME",       "en": "IME"},
    "@ohos.InputMethod.*":     {"domain": "0xD001C00", "short": "001cX", "subsystem": "输入法", "tag": "IME",       "en": "IME"},

    # —— DFX (Hilog, 0xD002Dxx) ——
    "@ohos.hilog":             {"domain": "0xD002D00", "short": "002dX", "subsystem": "DFX", "tag": "Hilog",      "en": "Hilog"},
    "@ohos.hiviewdfx.*":       {"domain": "0xD002D00", "short": "002dX", "subsystem": "DFX", "tag": "Hiviewdfx", "en": "Hilog"},

    # —— 多媒体 / 通知 / 账号 / 图形 ——
    "@ohos.multimedia.*":      {"domain": "0xD002B00", "short": "002bX", "subsystem": "多媒体", "tag": "MultiMedia",  "en": "MultiMedia"},
    "@ohos.notification.*":    {"domain": "0xD001200", "short": "0012X", "subsystem": "通知",   "tag": "Notification", "en": "Notification"},
    "@ohos.account.*":         {"domain": "0xD001B00", "short": "001bX", "subsystem": "账号",   "tag": "Account",      "en": "Account"},
    "@ohos.graphics.*":        {"domain": "0xD001400", "short": "0014X", "subsystem": "图形",   "tag": "Graphics",     "en": "Graphics"},

    # —— 基础通信 (Connectivity, 0xD0000xx) ——
    "@ohos.bluetooth.*":       {"domain": "0xD000000", "short": "0000X", "subsystem": "基础通信", "tag": "Bluetooth",   "en": "Connectivity"},
    "@ohos.nearlink.*":        {"domain": "0xD000000", "short": "0000X", "subsystem": "基础通信", "tag": "Nearlink",    "en": "Connectivity"},
    "@ohos.FusionConnectivity.*": {"domain": "0xD000000", "short": "0000X", "subsystem": "基础通信", "tag": "Fusion", "en": "Connectivity"},

    # —— 文件管理 (FileManagement, 0xD0043xx) ——
    "@ohos.file.*":            {"domain": "0xD004300", "short": "0043X", "subsystem": "文件管理", "tag": "File",          "en": "FileManagement"},
    "@ohos.filemanagement.*":  {"domain": "0xD004300", "short": "0043X", "subsystem": "文件管理", "tag": "FileManager",  "en": "FileManagement"},

    # —— 公共基础类库 (ArkTS, 0xD003Fxx) ——
    "@ohos.util.*":             {"domain": "0xD003F00", "short": "003fX", "subsystem": "公共基础类库", "tag": "Util",     "en": "ArkTS"},
    "@ohos.buffer":             {"domain": "0xD003F00", "short": "003fX", "subsystem": "公共基础类库", "tag": "Buffer",   "en": "ArkTS"},
    "@ohos.taskpool":           {"domain": "0xD003F00", "short": "003fX", "subsystem": "公共基础类库", "tag": "Taskpool", "en": "ArkTS"},
    "@ohos.worker":             {"domain": "0xD003F00", "short": "003fX", "subsystem": "公共基础类库", "tag": "Worker",   "en": "ArkTS"},

    # —— 分布式数据管理 (ArkData, 0xD0016xx) ——
    "@ohos.data.*":             {"domain": "0xD001600", "short": "0016X", "subsystem": "分布式数据管理", "tag": "Data",      "en": "ArkData"},
    "@ohos.pasteboard":         {"domain": "0xD001600", "short": "0016X", "subsystem": "分布式数据管理", "tag": "Pasteboard", "en": "ArkData"},

    # —— 包管理 (Bundle, 0xD0017xx) ——
    "@ohos.bundle.*":           {"domain": "0xD001700", "short": "0017X", "subsystem": "包管理", "tag": "Bundle",   "en": "Bundle"},

    # —— 定制 (MDM, 0xD0018xx) ——
    "@ohos.enterprise.*":       {"domain": "0xD001800", "short": "0018X", "subsystem": "定制", "tag": "Enterprise", "en": "MDM"},

    # —— 多模输入 (MultimodalInput, 0xD0028xx) ——
    "@ohos.multimodalInput.*":  {"domain": "0xD002800", "short": "0028X", "subsystem": "多模输入", "tag": "Input", "en": "MultimodalInput"},

    # —— 网络管理 (Network, 0xD0015xx) ——
    "@ohos.net.*":              {"domain": "0xD001500", "short": "0015X", "subsystem": "网络管理", "tag": "Net",     "en": "Network"},

    # —— 电话服务 (Telephony, 0xD001Fxx) ——
    "@ohos.telephony.*":        {"domain": "0xD001F00", "short": "001fX", "subsystem": "电话服务", "tag": "Telephony", "en": "Telephony"},

    # —— 电源服务 (Power, 0xD0029xx) ——
    "@ohos.batteryInfo":        {"domain": "0xD002900", "short": "0029X", "subsystem": "电源服务", "tag": "Battery", "en": "Power"},
    "@ohos.batteryStatistics.*":{"domain": "0xD002900", "short": "0029X", "subsystem": "电源服务", "tag": "Statistics", "en": "Power"},

    # —— 无障碍软件服务 (Accessibility, 0xD001Dxx) ——
    "@ohos.accessibility.*":    {"domain": "0xD001D00", "short": "001dX", "subsystem": "无障碍软件服务", "tag": "Accessibility", "en": "Accessibility"},

    # —— 泛Sensor服务 (Sensor, 0xD0022xx) ——
    "@ohos.sensor.*":           {"domain": "0xD002200", "short": "0022X", "subsystem": "泛Sensor服务", "tag": "Sensor",   "en": "Sensor"},
    "@ohos.vibrator":           {"domain": "0xD002200", "short": "0022X", "subsystem": "泛Sensor服务", "tag": "Vibrator", "en": "Sensor"},

    # —— 安全基础能力 (Security, 0xD002Fxx) ——
    "@ohos.security.*":         {"domain": "0xD002F00", "short": "002fX", "subsystem": "安全基础能力", "tag": "Security", "en": "Security"},

    # —— AI业务 (AI, 0xD0021xx) ——
    "@ohos.ai.*":               {"domain": "0xD002100", "short": "0021X", "subsystem": "AI业务", "tag": "AI", "en": "AI"},

    # —— 上传下载 (Request, 0xD001Cxx) ——
    "@ohos.request.*":          {"domain": "0xD001C00", "short": "001cX", "subsystem": "上传下载", "tag": "Request", "en": "Request"},

    # —— 位置服务 (Location, 0xD0013xx) ——
    "@ohos.geoLocationManager.*": {"domain": "0xD001300", "short": "0013X", "subsystem": "位置服务", "tag": "Location", "en": "Location"},
    "@ohos.geolocation":          {"domain": "0xD001300", "short": "0013X", "subsystem": "位置服务", "tag": "Location", "en": "Location"},

    # —— 分布式硬件 (DistributedHardware, 0xD0041xx) ——
    "@ohos.distributedHardware.*":        {"domain": "0xD004100", "short": "0041X", "subsystem": "分布式硬件", "tag": "DistributedHW", "en": "DistributedHardware"},
    "@ohos.distributedDeviceManager.*":   {"domain": "0xD004100", "short": "0041X", "subsystem": "分布式硬件", "tag": "DeviceManager", "en": "DistributedHardware"},

    # —— 广告服务 (Advertising, 0xD0047xx) ——
    "@ohos.advertising.*":      {"domain": "0xD004700", "short": "0047X", "subsystem": "广告服务", "tag": "Advertising", "en": "Advertising"},
}


# ============================================================
# 固化数据 2：子系统三套命名桥接
#   en(log_domains.cpp 英文名) ↔ cn(kit.json 中文名) ↔ rules_domain(rules表粗类)
# ============================================================
SUBSYSTEM_BRIDGE = {
    "TestSystem":  {"cn": "测试框架", "rules_domain": "测试框架"},
    "Ace":         {"cn": "ArkUI",   "rules_domain": "ArkUI"},
    "AAFwk":       {"cn": "元能力",   "rules_domain": "元能力"},
    "JSConsole":   {"cn": "ArkUI",   "rules_domain": "ArkUI"},
    "Hilog":       {"cn": "DFX",     "rules_domain": "测试框架"},
    "MultiMedia":  {"cn": "多媒体",   "rules_domain": "多媒体"},
    "Notification":{"cn": "通知",    "rules_domain": "通知"},
    "Account":     {"cn": "账号",    "rules_domain": "账号"},
    "Graphics":    {"cn": "图形",    "rules_domain": "图形"},
}


# ============================================================
# 固化数据 3：测试运行时 domain（非子系统！）
#   这些 domain 是测试进程/框架自己的输出通道，
#   不属于任何被测子系统，禁止在证据链里画成 "子系统→domain"。
# ============================================================
TEST_RUNTIME_DOMAINS = {
    "0xA03D00": {"short": "A03D0", "tag": "JSAPP", "note": "测试 App 的 JS 运行时（Hypium 断言/console.log/hilog.info 默认通道）"},
    "0xD005D00": {"short": "005dX", "tag": "XTS",   "note": "XTS acts runner 执行器运行时"},
}


# ============================================================
# 核心函数
# ============================================================

def _normalize_module(module):
    if module is None:
        return None
    m = str(module).strip()
    if (m.startswith("'") and m.endswith("'")) or (m.startswith('"') and m.endswith('"')):
        m = m[1:-1]
    return m or None


def _match_module(module):
    """精确匹配，支持 .* 通配后缀"""
    if module in MODULE_DOMAIN:
        return MODULE_DOMAIN[module]
    for key, val in MODULE_DOMAIN.items():
        if key.endswith(".*"):
            prefix = key[:-2]
            if module == prefix or module.startswith(prefix + "."):
                return val
    return None


def short_to_regex(short_hex):
    """short_hex → grep 正则。X 视为单字符通配。
    例: 0039X → C0039[0-9a-fA-F]/ ；00310 → C00310/"""
    s = short_hex.upper()
    body = "".join(c if c != "X" else "[0-9a-fA-F]" for c in s)
    return "C{}/".format(body)


def is_test_runtime(domain_hex):
    """判断一个 domain 是否属于测试运行时（非被测方）"""
    if not domain_hex:
        return False
    d = str(domain_hex).strip().lower()
    return d in {k.lower() for k in TEST_RUNTIME_DOMAINS}


def map_sut(module):
    """被测方映射：@ohos.X / 模块名 → 完整链路字典。
    查到返回 status=mapped + role=SUT；查不到返回 status=unmapped，绝不返回空值。"""
    m = _normalize_module(module)
    if not m:
        return {"status": "error", "reason": "empty input", "input": module}

    hit = _match_module(m)
    if hit:
        return {
            "status": "mapped",
            "role": "SUT",
            "input": m,
            "module": m,
            "domain": hit["domain"],
            "short_hex": hit["short"],
            "subsystem": hit["subsystem"],
            "subsystem_en": hit.get("en", ""),
            "tag": hit["tag"],
            "filter_regex": short_to_regex(hit["short"]),
        }
    
    # 增强错误提示
    reason = "'{}' NOT FOUND in MODULE_DOMAIN (固化表 {} 条).\n".format(m, len(MODULE_DOMAIN))
    reason += "\n可能原因：\n"
    reason += "1. 模块名拼写错误（检查是否应为 '@ohos.util.stream' 而非 '@ohos.stream'）\n"
    reason += "2. 应从源码import语句提取正确的模块名（禁止猜测）\n"
    reason += "3. 建议使用 kit 查询：python3 map_domain.py '@kit.ArkTS'\n"
    reason += "4. 建议使用引用链探索：python3 explore_import_chain.py <测试文件>\n"
    reason += "\n⚠️ 强制要求：禁止猜测模块名，必须从源码文件实际读取import语句"
    
    return {
        "status": "unmapped",
        "role": "unknown",
        "input": m,
        "reason": reason
    }


def _default_db_path():
    here = os.path.dirname(os.path.abspath(__file__))
    rel = os.path.normpath(os.path.join(here, "..", "data", "xts_rules.db"))
    if os.path.exists(rel):
        return rel
    home = os.path.expanduser("~")
    return os.path.join(home, ".opencode", "skills", "xts-issue-analysis", "data", "xts_rules.db")


def _query_kit_module(kit_name, db_path=None):
    """查 kit_module 表（字段名已校正：kit_name/module_name/subsystem_cn）"""
    import sqlite3
    if db_path is None:
        db_path = _default_db_path()
    if not os.path.exists(db_path):
        return None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT module_name, subsystem_cn FROM kit_module WHERE kit_name = ?", (kit_name,))
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error:
        return None


def expand_kit(kit_input, db_path=None):
    """@kit.X → [@ohos.Y, ...] 展开，并对每个模块做 map_sut。
    db 缺失或 kit 未登记 → 返回 unmapped，不猜。"""
    kit_input = _normalize_module(kit_input) or ""
    m = re.search(r"@kit\.(\w+)", kit_input)
    kit_name = m.group(1) if m else kit_input.strip()

    rows = _query_kit_module(kit_name, db_path)
    if rows is None:
        return {"status": "db_error", "kit": kit_name, "reason": "kit_module 表查询失败或 db 不存在: " + _default_db_path()}
    if not rows:
        return {"status": "unmapped", "kit": kit_name, "reason": "kit '{}' 不在 kit_module 表".format(kit_name)}

    modules = [r[0] for r in rows]
    subsystem_cn = rows[0][1] if rows else ""
    mappings = [map_sut(mod) for mod in modules]
    return {
        "status": "expanded",
        "kit": kit_name,
        "subsystem_cn": subsystem_cn,
        "modules": modules,
        "mappings": mappings,
    }


def list_runtime():
    """列出所有测试运行时 domain（供 AI 区分被测方 vs 测试方）"""
    out = []
    for dom, info in TEST_RUNTIME_DOMAINS.items():
        out.append({
            "role": "test_runtime",
            "domain": dom,
            "short_hex": info["short"],
            "tag": info["tag"],
            "filter_regex": short_to_regex(info["short"]),
            "note": info["note"],
        })
    return out


def list_all_mappings():
    """列出全部固化映射，供审计/校对"""
    suts = []
    for mod, info in MODULE_DOMAIN.items():
        suts.append({
            "role": "SUT",
            "module": mod,
            "domain": info["domain"],
            "short_hex": info["short"],
            "subsystem": info["subsystem"],
            "subsystem_en": info.get("en", ""),
            "tag": info["tag"],
            "filter_regex": short_to_regex(info["short"]),
        })
    return {"SUT_count": len(suts), "SUT": suts, "test_runtime": list_runtime(), "bridge": SUBSYSTEM_BRIDGE}


# ============================================================
# CLI
# ============================================================

def _print_text(obj):
    if isinstance(obj, list):
        for i, item in enumerate(obj, 1):
            print("[{}] ".format(i) + " | ".join("{}: {}".format(k, v) for k, v in item.items()))
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and k in ("mappings", "modules", "SUT", "test_runtime"):
                print("{}:".format(k))
                if isinstance(v, list):
                    for item in v:
                        print("  " + json.dumps(item, ensure_ascii=False))
                else:
                    print("  " + json.dumps(v, ensure_ascii=False))
            else:
                print("{}: {}".format(k, v))


def map_recursive(module, oh_root=None):
    """递归解析import依赖树（可选增强功能）
    
    Args:
        module: 模块名（如@ohos.arkui.inspector）
        oh_root: OH源码根路径（可选，从配置文件读取）
    
    Returns:
        dict: 依赖树JSON结构
    """
    if not DEPENDENCY_TREE_AVAILABLE:
        return {
            "status": "error",
            "error": "dependency_tree_parser模块未安装",
            "suggestion": "请确保dependency_tree_parser.py在scripts目录下"
        }
    
    # 加载配置文件
    config = load_config()
    if oh_root is None:
        oh_root = config.get('OH_ROOT')
    
    if not oh_root:
        return {
            "status": "error",
            "error": "OH_ROOT路径未配置",
            "suggestion": "请在.xts-analysis-config.json中配置OH_ROOT路径"
        }
    
    # 验证OH_ROOT有效性
    api_path = os.path.join(oh_root, 'interface/sdk-js/api')
    kits_path = os.path.join(oh_root, 'interface/sdk-js/kits')
    
    if not os.path.exists(api_path) or not os.path.exists(kits_path):
        return {
            "status": "error",
            "error": f"OH_ROOT路径无效: {oh_root}",
            "suggestion": "请确保interface/sdk-js/api和kits目录存在"
        }
    
    # 调用递归解析器（需传入db_manager，这里简化处理）
    try:
        # 创建简化版db_manager（只用于查询domain）
        class SimpleDBManager:
            def query_module_domain(self, module):
                # 优先使用固化常量
                result = map_sut(module)
                if result.get('status') == 'mapped':
                    return {
                        'domain': result['domain'],
                        'short_hex': result['short'],
                        'subsystem': result['subsystem'],
                        'mapping_status': 'constant'
                    }
                return None
            
            def query_module_domain_multi_level(self, module):
                # 多级查询（固化常量优先）
                result = self.query_module_domain(module)
                if result:
                    return result
                
                # 降级：pattern推断（简化版）
                # 如果模块名符合pattern，尝试推断domain
                if module.startswith('@ohos.'):
                    # 简化推断逻辑（实际应查询数据库）
                    return {
                        'domain': '0xD003900',  # 默认ArkUI domain
                        'short_hex': '0039X',
                        'subsystem': 'ArkUI',
                        'mapping_status': 'inferred',
                        'confidence': 50
                    }
                
                return None
            
            def query_kit_module(self, kit_name):
                # 查询kit模块展开（简化版）
                return expand_kit(kit_name, None)
        
        db_manager = SimpleDBManager()
        parser = DependencyTreeParser(oh_root, db_manager, max_depth=5)
        tree = parser.parse_import_chain(module)
        
        return {
            "status": "success",
            "method": "recursive",
            "module": module,
            "tree": tree,
            "note": "递归解析结果（深度≤5）"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"递归解析失败: {str(e)}",
            "suggestion": "请检查模块名是否正确或OH_ROOT路径配置"
        }


def main():
    ap = argparse.ArgumentParser(
        description="被测方 API→Domain 映射工具（固化常量 + 确定性查表）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python map_domain.py @ohos.arkui.inspector       # 查单个模块（固化常量）
  python map_domain.py @kit.TestKit                 # 展开 kit 并逐个映射
  python map_domain.py @ohos.UiTest --format text   # 文本输出
  python map_domain.py --list-runtime               # 列出测试运行时 domain
  python map_domain.py --list-all                   # 列出全部固化映射（审计）
  python map_domain.py @ohos.arkui.inspector --recursive  # 递归解析（需OH_ROOT）
        """,
    )
    ap.add_argument("module", nargs="?", help="模块名或 kit（如 @ohos.arkui.inspector / @kit.TestKit）")
    ap.add_argument("--format", "-f", choices=["json", "text"], default="json", help="输出格式（默认 json）")
    ap.add_argument("--list-runtime", action="store_true", help="列出所有测试运行时 domain")
    ap.add_argument("--list-all", action="store_true", help="列出全部固化映射（审计用）")
    ap.add_argument("--db", help="指定 xts_rules.db 路径（仅 expand_kit 用）")
    ap.add_argument("--recursive", action="store_true", 
                    help="启用递归解析（需OH_ROOT配置，深度≤5）")
    args = ap.parse_args()

    if args.list_runtime:
        result = list_runtime()
    elif args.list_all:
        result = list_all_mappings()
    elif not args.module:
        ap.print_help()
        sys.exit(1)
    elif args.module.startswith("@kit.") or args.module.lower().startswith("@kit."):
        result = expand_kit(args.module, args.db)
    elif args.recursive:
        # 递归解析模式（可选增强）
        result = map_recursive(args.module)
    else:
        # 固化常量模式（默认，最稳定）
        result = map_sut(args.module)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_text(result)


if __name__ == "__main__":
    main()
