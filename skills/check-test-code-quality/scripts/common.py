#!/usr/bin/env python3
"""XTS Test Code Quality Scanner - Common Utilities

This module contains shared utility code used by all rule scanners:
- Subsystem mapping (from references/subsystem_mapping.md)
- File type detection and collection
- Comment stripping
- Brace matching (string-aware)
- it()/describe() block parsing (from references/SCAN_ALGORITHMS.md)
- Independent XTS project finder (from references/project_level_scan.md)
- Assertion pattern detection
- Excel report generation (from references/REPORT_FORMAT.md)

NOTE: When references/subsystem_mapping.md is updated, SUBSYSTEM_MAPPING
must be synced accordingly.
NOTE: When references/project_level_scan.md is updated, find_independent_projects()
must be synced accordingly.
NOTE: When references/SCAN_ALGORITHMS.md is updated, _parse_blocks() must be synced accordingly.
"""
import os, re, sys, json, collections, time, logging
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

# ======================== SUBSYSTEM MAPPING ========================
# Source: references/subsystem_mapping.md (97 entries)
# Sync rule: Update when subsystem_mapping.md changes

SUBSYSTEM_MAPPING = {
    "ability/ability_runtime": "元能力", "ability/crossplatform": "元能力", "ability/form": "卡片框架",
    "account": "账号", "ai": "AI", "applications/settingsdata": "应用设置",
    "arkcompiler": "语言编译运行时", "arkui": "ArkUI", "bundlemanager": "包管理",
    "commonlibrary": "语言编译运行时",
    "communication/bluetooth_ble": "短距", "communication/bluetooth_bp": "短距",
    "communication/bluetooth_br": "短距", "communication/bluetooth_nop": "短距",
    "communication/btmanager_errorcode401": "短距", "communication/btmanager_switchoff": "短距",
    "communication/dsoftbus": "软总线", "communication/netmanager_base": "短距",
    "communication/nfc_Controller": "短距", "communication/nfc_ErrorCode": "短距",
    "communication/nfc_Permissions": "短距", "communication/nfc_SecureElement": "短距",
    "communication/nfc_SecureElement_2": "短距",
    "communication/wifi_ErrorCode201": "短距", "communication/wifi_ErrorCode401": "短距",
    "communication/wifi_enterprise": "短距", "communication/wifi_ets_standard": "短距",
    "communication/wifi_manager_nop": "短距",
}
for _i in range(3, 41):
    SUBSYSTEM_MAPPING[f"communication/wifi_p{_i}p"] = "短距"
SUBSYSTEM_MAPPING.update({
    "communication/wifi_p2p": "短距", "communication/wifi_standard": "短距",
    "customization": "定制化", "distributeddatamgr": "分布式数据", "global": "全球化",
    "graphic": "图形图像", "hdf": "驱动", "hiviewdfx": "DFX", "inputmethod": "输入法",
    "location": "位置服务", "multimedia/audio": "音频", "multimedia/avsource": "视频框架",
    "multimedia/camera": "相机图库框架", "multimedia/image": "相机图库框架",
    "multimedia/media": "视频框架", "multimedia/photoAccess": "相机图库框架",
    "multimodalinput": "多模输入", "pcs": "XTS专项小组", "print": "打印框架",
    "resourceschedule": "全局资源调度", "security": "安全",
    "security/certificate_manager": "安全", "storage": "文件管理",
    "telephony": "电话服务", "testfwk": "测试子系统", "theme": "主题",
    "time": "时间时区", "usb": "USB服务", "useriam": "用户IAM", "web": "Web",
    "validator/acts_validator/entry/src/main/ets/pages/PCS": "XTS专项小组",
})
SORTED_DIRS = sorted(SUBSYSTEM_MAPPING.keys(), key=len, reverse=True)

def get_subsystem(file_path):
    fp = file_path.replace("\\", "/")
    for d in SORTED_DIRS:
        if fp.startswith(d + "/"):
            return SUBSYSTEM_MAPPING[d]
    return "-"

# ======================== FILE UTILITIES ========================

ALL_SOURCE_EXTS = ['.ets', '.ts', '.js']
TEST_FILE_EXTS = ['.test.ets', '.test.ts', '.test.js']

def is_test_file(filepath):
    return filepath.endswith('.test.ets') or filepath.endswith('.test.ts') or filepath.endswith('.test.js')

def collect_files(scan_root, exts):
    result = []
    for root, dirs, files in os.walk(scan_root):
        for f in files:
            for ext in exts:
                if f.endswith(ext):
                    result.append(os.path.join(root, f))
                    break
    return result

def strip_comments(line):
    idx = line.find('//')
    if idx < 0:
        return line
    in_sq = in_dq = in_bt = False
    for c in line[:idx]:
        if c == '`' and not in_sq and not in_dq: in_bt = not in_bt
        elif c == "'" and not in_dq and not in_bt: in_sq = not in_sq
        elif c == '"' and not in_sq and not in_bt: in_dq = not in_dq
    if not in_sq and not in_dq and not in_bt:
        return line[:idx]
    return line

# ======================== BRACE MATCHING ========================
# Source: references/TRAPS.md (Trap 1, Trap 1b)
# Sync rule: Update when TRAPS.md trap descriptions change

def find_matching_brace(content, start):
    depth = 0; in_s = in_d = in_bt = False; i = start
    while i < len(content):
        c = content[i]
        if c == '\\' and (in_s or in_d or in_bt): i += 2; continue
        if c == '`' and not in_s and not in_d: in_bt = not in_bt
        elif c == "'" and not in_d and not in_bt: in_s = not in_s
        elif c == '"' and not in_s and not in_bt: in_d = not in_d
        if not in_s and not in_d and not in_bt:
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: return i
        i += 1
    return -1

# ======================== IT/DESCRIBE BLOCK PARSER ========================
# Source: references/SCAN_ALGORITHMS.md (Algorithm 1)
# Sync rule: Update when SCAN_ALGORITHMS.md it()/describe() algorithm changes

def _parse_blocks(content, keyword):
    blocks = []
    lines = content.split('\n')
    pattern = re.compile(rf'\b{keyword}(?:\.only|\.skip|\.each)?\s*\(\s*[\'"](.+?)[\'"]\s*,')
    for i, line in enumerate(lines):
        m = pattern.search(line)
        if not m:
            continue
        name = m.group(1); start = i + 1
        bo = 0; bc = 0
        in_s = in_d = in_bt = False; found = False
        for j in range(i, len(lines)):
            text = lines[j]; k = 0
            while k < len(text):
                c = text[k]
                if c == '\\' and (in_s or in_d or in_bt): k += 2; continue
                if c == '`' and not in_s and not in_d: in_bt = not in_bt
                elif c == "'" and not in_d and not in_bt: in_s = not in_s
                elif c == '"' and not in_s and not in_bt: in_d = not in_d
                if not in_s and not in_d and not in_bt:
                    if c == '{': bo += 1; found = True
                    elif c == '}': bc += 1
                k += 1
            if found and bc >= bo and bo > 0:
                blocks.append({'name': name, 'start': start, 'end': j + 1})
                break
    return blocks

def parse_it_blocks(content):
    return _parse_blocks(content, 'it')

def parse_describe_blocks(content):
    return _parse_blocks(content, 'describe')

def find_testcase_for_line(it_blocks, line_num):
    for b in it_blocks:
        if b['start'] <= line_num <= b['end']:
            return b['name']
    return "-"

# ======================== INDEPENDENT PROJECT FINDER ========================
# Source: references/project_level_scan.md, references/ENGINE_IDENTITY.md
# Sync rule: Update when project_level_scan.md or ENGINE_IDENTITY.md changes

def is_group_build_gn(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return bool(re.search(r'\bgroup\s*\(', f.read()))
    except Exception as e:
        print(f"  读取BUILD.gn失败 {filepath}: {e}", file=sys.stderr)
        return False

def find_independent_projects(scan_root):
    all_bg = set()
    for root, dirs, files in os.walk(scan_root):
        if 'BUILD.gn' in files:
            all_bg.add(os.path.abspath(root))
    non_group = {d for d in all_bg if not is_group_build_gn(os.path.join(d, 'BUILD.gn'))}
    parents = set()
    for d in all_bg:
        p = os.path.dirname(d)
        while p != os.path.abspath(scan_root) and p != '/':
            if p in non_group: parents.add(d); break
            p = os.path.dirname(p)
    indep = all_bg - parents - (all_bg - non_group)
    return sorted(indep)

# ======================== ASSERTION DETECTION ========================

ASSERTION_PATTERNS = [
    re.compile(r'\bexpect\s*\('), re.compile(r'\bassertEqual\s*\('),
    re.compile(r'\bassertTrue\s*\('), re.compile(r'\bassertFalse\s*\('),
    re.compile(r'\bassertNull\s*\('), re.compile(r'\bassertFail\s*\('),
    re.compile(r'\bassertInstanceOf\s*\('), re.compile(r'\bassertContains\s*\('),
    re.compile(r'\bassertDeepEquals\s*\('), re.compile(r'\bcheckResult\s*\('),
    re.compile(r'\bassertNotEqual\s*\('), re.compile(r'\bassertUndefined\s*\('),
    re.compile(r'\bassertDefined\s*\('), re.compile(r'\bassertThrowError\s*\('),
]

def has_assertion(text):
    if not text: return False
    eff = '\n'.join(l for l in text.split('\n') if not l.strip().startswith('//'))
    return any(p.search(eff) for p in ASSERTION_PATTERNS)

def _find_try_catch(body):
    result = []; lines = body.split('\n'); i = 0
    while i < len(lines):
        s = lines[i].strip()
        if re.match(r'try\s*\{', s):
            ts = i; bc = s.count('{') - s.count('}'); j = i + 1; te = -1
            while j < len(lines) and bc > 0:
                lj = lines[j].strip()
                if re.match(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', lj): te = j; break
                bc += lj.count('{') - lj.count('}')
                if bc == 0: te = j; break
                j += 1
            if te == -1: i += 1; continue
            try_c = '\n'.join(lines[ts:te+1]); cs = -1; catch_c = ''
            if re.match(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', lines[te].strip()):
                cs = te; cbc = 1; k = cs + 1
                while k < len(lines) and cbc > 0:
                    cbc += lines[k].count('{') - lines[k].count('}'); k += 1
                catch_c = '\n'.join(lines[cs:k])
            result.append({'try_content': try_c, 'catch_content': catch_c})
            i = k if cs != -1 else te + 1
        else: i += 1
    return result

# ======================== PROJECT-LEVEL SCAN UTILITIES ========================
# Source: references/project_level_scan.md
# Sync rule: Update when project_level_scan.md shared functions change

def get_project_source_files(project_dir):
    source_files = []
    for root, dirs, files in os.walk(project_dir):
        for f in files:
            if f.endswith(('.ets', '.ts', '.js')):
                source_files.append(os.path.join(root, f))
    return source_files

def collect_attr_values(project_dir, source_files, base_dir, pattern):
    items = []
    for file_path in source_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        for match in pattern.finditer(content):
            attr_value = match.group(2)
            if not attr_value:
                continue
            line_num = content[:match.start()].count('\n') + 1
            rel_path = os.path.relpath(file_path, base_dir)
            items.append({'value': attr_value, 'file': rel_path, 'line': line_num})
    return items

def find_duplicate_groups(items):
    value_to_occurrences = collections.defaultdict(list)
    for item in items:
        value_to_occurrences[item['value']].append(item)
    duplicates = []
    for value, occurrences in value_to_occurrences.items():
        if len(occurrences) > 1:
            first = occurrences[0]
            other_locs = [f"{occ['file']}:{occ['line']}" for occ in occurrences[1:]]
            duplicates.append({
                'value': value, 'count': len(occurrences),
                'first_file': first['file'], 'first_line': first['line'],
                'other_locations': other_locs,
            })
    return duplicates

# ======================== REPORT GENERATION ========================
# Source: references/REPORT_FORMAT.md
# Sync rule: Update when REPORT_FORMAT.md format spec changes

def write_excel_with_bom(filepath, wb):
    wb.save(filepath)

def generate_report(all_issues, report_dir, rules_info, rule_counts):
    os.makedirs(report_dir, exist_ok=True)
    wb = Workbook()
    ws1 = wb.active; ws1.title = "代码质量检查报告"
    ws1.append(["问题ID","问题类型","严重级别","文件路径","行号","所属用例","代码片段","修复建议","所属子系统","申请报备人","报备原因","是否报备通过"])
    for iss in all_issues:
        ws1.append([iss.get('rule',''),iss.get('type',''),iss.get('severity',''),iss.get('file',''),
            iss.get('line',''),iss.get('testcase','-'),iss.get('snippet',''),iss.get('suggestion',''),
            iss.get('subsystem','-'),'','',''])
    for col in ws1.columns:
        ml = max((len(str(c.value)) if c.value else 0) for c in col)
        ws1.column_dimensions[col[0].column_letter].width = min(ml + 2, 60)
    ws2 = wb.create_sheet("问题扫描结果汇总")
    ws2.append(["规则编号","问题类型","严重级别","问题数量"])
    for rid, rn, sev, _fn in rules_info:
        ws2.append([rid, rn, sev, rule_counts.get(rid, 0) if rule_counts.get(rid, 0) > 0 else 0])
    ep = os.path.join(report_dir, "XTS_代码质量检查报告.xlsx")
    write_excel_with_bom(ep, wb)
    return ep
