#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FUZZ测试用例规范性检查工具 v2.2
检查26条自动可验证的规则（代码规范规则001-019 + 文件格式规则A-G）
所有规则统一通过 check_scripts/ 独立脚本执行，消除代码重复

更新日志:
v2.2 - 统一使用独立脚本、新增自动修复、优化规则编号对齐
     - 所有26条规则统一通过 check_scripts/ 导入执行，消除内联重复代码
     - 新增 --fix 自动修复支持（规则001/003/006/017/019/F）
     - 优化规则编号对齐（001-019 + A-G 与 SKILL.md 完全一致）
v2.1 - 优化Windows兼容性、减少误报、增强检测能力
"""

import re
import sys
import os
import argparse
import platform
from pathlib import Path

# Windows兼容性：强制UTF-8编码
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    os.environ["PYTHONIOENCODING"] = "utf-8"

# 导入所有独立检查脚本（26条规则）
check_scripts_dir = os.path.join(os.path.dirname(__file__), "..", "check_scripts")
if check_scripts_dir not in sys.path:
    sys.path.insert(0, check_scripts_dir)

try:
    from SecurityCodeReview_FuzzCheck_001 import check_unfuzzable_api as check_001
    from SecurityCodeReview_FuzzCheck_002 import check_missing_api_coverage as check_002
    from SecurityCodeReview_FuzzCheck_003 import check_fuzzed_data_usage as check_003
    from SecurityCodeReview_FuzzCheck_004 import check_reused_data as check_004
    from SecurityCodeReview_FuzzCheck_005 import check_complex_params as check_005
    from SecurityCodeReview_FuzzCheck_006 import check_target_size as check_006
    from SecurityCodeReview_FuzzCheck_007 import check_ipc_pattern as check_007
    from SecurityCodeReview_FuzzCheck_008 import check_seed_files as check_008
    from SecurityCodeReview_FuzzCheck_009 import check_buffer_overflow as check_009
    from SecurityCodeReview_FuzzCheck_010 import check_size_as_fuzz_data as check_010
    from SecurityCodeReview_FuzzCheck_011 import check_security_context as check_011
    from SecurityCodeReview_FuzzCheck_012 import check_branch_coverage as check_012
    from SecurityCodeReview_FuzzCheck_013 import check_enum_range as check_013
    from SecurityCodeReview_FuzzCheck_014 import check_fixed_params as check_014
    from SecurityCodeReview_FuzzCheck_015 import (
        check_intermediate_products as check_015,
    )
    from SecurityCodeReview_FuzzCheck_016 import check_type_mismatch as check_016
    from SecurityCodeReview_FuzzCheck_017 import check_random_usage as check_017
    from SecurityCodeReview_FuzzCheck_018 import check_raw_data_usage as check_018
    from SecurityCodeReview_FuzzCheck_019 import (
        check_global_initialization as check_019,
    )
    from SecurityCodeReview_FuzzCheck_A import check_header_file as check_A
    from SecurityCodeReview_FuzzCheck_B import check_build_gn as check_B
    from SecurityCodeReview_FuzzCheck_C import check_project_xml as check_C
    from SecurityCodeReview_FuzzCheck_D import check_directory_consistency as check_D
    from SecurityCodeReview_FuzzCheck_E import check_cpp_include as check_E
    from SecurityCodeReview_FuzzCheck_F import check_copyright as check_F
    from SecurityCodeReview_FuzzCheck_G import check_build_gn_target_name as check_G

    USE_INDEPENDENT_SCRIPTS = True
except ImportError as e:
    print(f"[WARN] 部分独立检查脚本导入失败: {e}")
    print("[WARN] 将使用内联实现作为降级方案")
    USE_INDEPENDENT_SCRIPTS = False

DEFAULT_MODULE_PREFIX = "//foundation/[模块类别]/[模块名]"
MODULE_PREFIX = os.environ.get("FUZZ_MODULE_PREFIX", DEFAULT_MODULE_PREFIX)

# 非枚举类型（typedef/alias，虽用大驼峰但不需要 uint8_t 限制）
NON_ENUM_TYPES = {
    "ScreenId",
    "NodeId",
    "WindowId",
    "DisplayId",
    "ProcessId",
    "UserId",
    "Uid",
    "Pid",
    "Handle",
    "Fd",
    "DrawableId",
}


def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, UnicodeDecodeError) as e:
        return None


def _resolve_header_path(header_str, search_dirs):
    path = header_str.strip().strip('"').strip("'")
    if os.path.isabs(path) and os.path.isfile(path):
        return path
    for base in search_dirs:
        candidate = Path(base) / path
        if candidate.is_file():
            return str(candidate)
        parts = Path(path).parts
        for i in range(len(parts)):
            candidate2 = Path(base) / Path(*parts[i:])
            if candidate2.is_file():
                return str(candidate2)
    return None


def parse_header_methods(header_path, target_class):
    if not header_path or not os.path.isfile(header_path):
        return []
    content = Path(header_path).read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"//[^\n]*", "", content)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    class_pattern = rf"\bclass\s+{re.escape(target_class)}\b.*?\{{"
    m = re.search(class_pattern, content)
    if not m:
        return []

    start = m.end() - 1
    brace_count = 0
    end = start
    for i in range(start, len(content)):
        if content[i] == "{":
            brace_count += 1
        elif content[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end = i
                break

    class_body = content[start : end + 1]
    pub_match = re.search(r"\bpublic\s*:", class_body)
    if not pub_match:
        return []

    pub_start = pub_match.end()
    next_access = re.search(r"\b(protected|private)\s*:", class_body[pub_start:])
    if next_access:
        pub_body = class_body[pub_start : pub_start + next_access.start()]
    else:
        pub_body = class_body[pub_start:]

    methods = []
    pattern = re.compile(
        r"(?:virtual|static|explicit|constexpr|inline|consteval|constinit|\[\[.*?\]\]|\s)*"
        r"(?P<ret>[~\w_][\w\s_:<>*,&.]*?)\s+"
        r"(?P<name>\w+)\s*\(\s*(?P<params>[^)]*)\s*\)\s*"
        r"(?:const\s*)?(?:override\s*)?(?:final\s*)?(?:noexcept\s*)?(?:=\s*0\s*)?;"
    )
    for match in pattern.finditer(pub_body):
        name = match.group("name")
        ret = match.group("ret").strip()
        params = match.group("params").strip()
        if (
            name == target_class
            or name.startswith("~")
            or ret
            in (
                "typedef",
                "using",
                "friend",
            )
        ):
            continue
        if not re.match(r"^[A-Za-z_]\w*$", name):
            continue
        if params == "" or params.lower() == "void":
            continue
        methods.append((name, params, ret))

    seen = set()
    unique = []
    for name, params, ret in methods:
        key = (name, params)
        if key not in seen:
            seen.add(key)
            unique.append((name, params, ret))
    return unique


def _extract_fuzzer_func_body(content, func_name, start_pos):
    """从函数名后的 '{' 开始提取完整函数体"""
    brace_count = 0
    end = start_pos
    for i in range(start_pos, len(content)):
        if content[i] == "{":
            brace_count += 1
        elif content[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end = i
                break
    return content[start_pos + 1 : end]


def check_unfuzzable_api(content):
    """
    规则001: 检查是否有不适合fuzz的API（无参数或仅固定参数）

    检测策略:
    1. 函数体中完全没有使用 fdp. 的情况 → 报错
    2. 有 fdp. 使用，但只使用了选择器变量（如 tarPos）而没有实际的业务参数消费 → 提示
    """
    errors = []
    pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )
    for m in pattern.finditer(content):
        func_name = m.group(1)
        start = m.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        # 1. 完全没有使用 fdp.
        if not re.search(r"fdp\.", body):
            errors.append(
                f"规则001[高危]: {func_name}() 中目标 API 调用未使用 FuzzedDataProvider 构造参数，"
                "属于无参数或固定参数 API，不适合 FUZZ 测试，建议移除或改为单元测试",
            )
            continue

        # 2. 有 fdp. 使用，但检查是否有实际的业务参数消费
        # 排除仅用于选择器的情况（如 tarPos = fdp.ConsumeIntegral<uint8_t>() % TARGET_SIZE）
        # 业务参数消费特征：
        # - fdp.ConsumeIntegral<T>() 且不是 % TARGET_SIZE 的选择器
        # - fdp.ConsumeBool()
        # - fdp.ConsumeFloatingPoint<T>()
        # - fdp.ConsumeRandomLengthString()
        # - fdp.ConsumeBytes()
        # - fdp.ConsumeRemainingBytes()

        # 查找所有 fdp.Consume 调用
        consume_calls = re.findall(r"fdp\.(Consume\w+)(?:<[^>]+>)?\s*\(", body)

        # 检查是否有选择器模式（如 tarPos = fdp.ConsumeIntegral<uint8_t>() % TARGET_SIZE）
        has_selector = bool(
            re.search(
                r"fdp\.ConsumeIntegral<\w+>\s*\(\)\s*%\s*\w+_SIZE|fdp\.ConsumeIntegral<\w+>\s*\(\)\s*%\s*TARGET_SIZE",
                body,
            )
        )

        # 检查是否有实际的业务参数消费（排除选择器）
        business_consumes = []
        for call in consume_calls:
            # 检查这个消费调用是否用于选择器
            # 获取消费调用的位置
            for match in re.finditer(rf"fdp\.{re.escape(call)}(?:<[^>]+>)?\s*\(", body):
                call_start = match.start()
                # 检查后面是否有 % TARGET_SIZE 或 % XXX_SIZE
                remaining = body[call_start : call_start + 100]
                if not re.search(r"%\s*(?:\w+_SIZE|TARGET_SIZE)", remaining):
                    business_consumes.append(call)

        # 如果只有选择器消费，没有业务参数消费
        if has_selector and not business_consumes and len(consume_calls) > 0:
            # 检查API调用是否有参数
            api_calls = re.findall(r"\w+\s*->\s*\w+\s*\(([^)]*)\)", body)
            for args_str in api_calls:
                args = [a.strip() for a in args_str.split(",") if a.strip()]
                if len(args) <= 1:  # 只有一个参数或没有参数（可能是this指针）
                    errors.append(
                        f"规则001[中危]: {func_name}() 中目标 API 调用参数过少（{len(args)}个），"
                        "可能不适合 FUZZ 测试，建议检查是否需要更多参数覆盖"
                    )
                    break

    return errors


def check_missing_api_coverage(filepath, content):
    """
    规则002: 检查API覆盖情况
    优化：增加覆盖率百分比计算
    """
    errors = []
    class_match = (
        re.search(r"std::make_shared<(\w+)>", content)
        or re.search(r"std::shared_ptr<(\w+)>", content)
        or re.search(r"std::unique_ptr<(\w+)>", content)
        or re.search(r"(\w+)::GetInstance\(\)", content)
        or re.search(r"(\w+)::Create\(\)", content)
        or re.search(r"(\w+)\*\s+g_\w+\s*=\s*nullptr", content)
    )
    if not class_match:
        return errors
    target_class = class_match.group(1)

    includes = re.findall(r'#include\s+"([^"]+\.h)"', content)
    fuzzer_h = os.path.basename(filepath).replace(".cpp", ".h")
    header_candidates = [inc for inc in includes if os.path.basename(inc) != fuzzer_h]
    if not header_candidates:
        return errors

    search_dirs = [
        Path(filepath).parent,
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path(__file__).parent.parent.parent,
        Path(__file__).parent.parent.parent.parent,
    ]

    all_header_methods = []
    for hc in header_candidates:
        resolved = _resolve_header_path(hc, search_dirs)
        if resolved and os.path.isfile(resolved):
            all_header_methods.extend(parse_header_methods(resolved, target_class))

    if not all_header_methods:
        return errors

    do_funcs = set(re.findall(r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider", content))
    covered = set()
    for do_name in do_funcs:
        if do_name.startswith("Do") and len(do_name) > 2:
            method = do_name[2:]
            covered.add(method)
        else:
            covered.add(do_name)

    missing = [name for name, _, _ in all_header_methods if name not in covered]

    # 优化：计算覆盖率百分比
    total_methods = len(all_header_methods)
    covered_methods = total_methods - len(missing)
    coverage_percent = (
        (covered_methods / total_methods * 100) if total_methods > 0 else 0
    )

    if missing:
        errors.append(
            f"规则002[高危]: 目标类 {target_class} 中有 {len(missing)} 个有参 public API 未覆盖 "
            f"(覆盖率: {coverage_percent:.1f}%, {covered_methods}/{total_methods}): "
            f"{', '.join(missing)}，建议补充对应的测试函数"
        )
    else:
        # 如果全部覆盖，也报告覆盖率
        if total_methods > 0:
            errors.append(
                f"规则002[信息]: 目标类 {target_class} 所有有参 public API 已覆盖 "
                f"(覆盖率: 100.0%, {total_methods}/{total_methods})"
            )

    return errors


def check_fuzz_file(filepath):
    content = read_file(filepath)
    if content is None:
        return [f"错误: 无法读取文件 {filepath}"]

    errors = []
    basename = os.path.basename(filepath)

    if USE_INDEPENDENT_SCRIPTS:
        # 所有26条规则统一通过独立脚本执行
        dirname = os.path.basename(os.path.dirname(filepath))
        filename = os.path.basename(filepath)

        # 文件格式规则 (A-G)
        if basename.endswith((".cpp", ".h")):
            errors.extend(check_F(filepath, content))  # 规则F: 版权头
        if basename.endswith(".cpp"):
            errors.extend(
                check_E(filename, content)
            )  # 规则E: .cpp头文件完整性（仅.cpp文件）
        if basename.endswith(".h"):
            errors.extend(
                check_A(filename, dirname, content)
            )  # 规则A: 头文件格式（仅.h文件）
        if basename == "BUILD.gn":
            errors.extend(check_B(content))  # 规则B: BUILD.gn规范
            errors.extend(check_G(filepath, content))  # 规则G: 目标命名
        if basename == "project.xml":
            errors.extend(check_C(filepath))  # 规则C: project.xml规范
        errors.extend(check_D(filepath))  # 规则D: 目录/文件一致性

        # 代码安全规则 (001-019)
        if basename.endswith(".cpp"):
            errors.extend(check_001(content))  # 规则001: FUZZ适用性
            errors.extend(check_002(filepath, content, []))  # 规则002: API覆盖
            errors.extend(check_003(content))  # 规则003: 变异数据使用
            errors.extend(check_004(content))  # 规则004: 变异数据复用
            errors.extend(check_005(content))  # 规则005: 复杂参数构造
            errors.extend(check_006(content))  # 规则006: 接口数量
            errors.extend(check_007(content))  # 规则007: IPC接口
            errors.extend(check_008(filepath, content))  # 规则008: 复杂函数
            errors.extend(check_009(content))  # 规则009: Driver安全性
            errors.extend(check_010(content))  # 规则010: size误用
            errors.extend(check_011(content))  # 规则011: 安全准入
            errors.extend(check_012(content))  # 规则012: 分支覆盖
            errors.extend(check_013(content))  # 规则013: 枚举值构造
            errors.extend(check_014(content))  # 规则014: 固定参数
            errors.extend(check_015(content))  # 规则015: 中间产物
            errors.extend(check_016(content))  # 规则016: 类型匹配
            errors.extend(check_017(content))  # 规则017: 随机函数
            errors.extend(check_018(content))  # 规则018: data指针
            errors.extend(check_019(content))  # 规则019: 全局变量初始化
    else:
        # 降级方案：使用内联实现
        if basename.endswith((".cpp", ".h")):
            errors.extend(check_copyright(filepath, content))
            errors.extend(check_file_format_rules(filepath, content))
        errors.extend(check_directory_consistency(filepath))
        if basename == "BUILD.gn":
            errors.extend(check_build_gn_target_name(filepath))
        if basename == "project.xml":
            errors.extend(check_project_xml(filepath))
        if basename.endswith(".cpp"):
            errors.extend(check_unfuzzable_api(content))
            errors.extend(check_missing_api_coverage(filepath, content))
            errors.extend(check_fuzzed_data_usage(content))
            errors.extend(check_reused_data(content))
            errors.extend(check_complex_params(content))
            errors.extend(check_target_size(content))
            errors.extend(check_ipc_pattern(content))
            errors.extend(check_seed_files(filepath, content))
            errors.extend(check_buffer_overflow(content))
            errors.extend(check_size_usage(content))
            errors.extend(check_security_context(content))
            errors.extend(check_branch_coverage(content))
            errors.extend(check_enum_range(content))
            errors.extend(check_fixed_params(content))
            errors.extend(check_intermediate_products(content))
            errors.extend(check_type_mismatch(content))
            errors.extend(check_random_usage(content))
            errors.extend(check_data_usage(content))
            errors.extend(check_global_init(content))

    return errors


def check_global_init(content):
    """
    规则019: 检查全局变量是否正确初始化

    检测策略:
    1. 全局指针是否初始化为nullptr
    2. 全局指针是否在LLVMFuzzerInitialize中初始化
    3. 全局对象是否正确构造
    """
    errors = []

    # 1. 检查全局指针声明
    global_ptrs = re.findall(r"(\w+)\*\s+(g_\w+)\s*=\s*nullptr\s*;", content)

    for ptr_type, var_name in global_ptrs:
        # 检查是否在LLVMFuzzerInitialize中初始化
        init_func = re.search(
            r"extern\s+\"C\"\s+int\s+LLVMFuzzerInitialize\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}",
            content,
            re.DOTALL,
        )

        if init_func:
            init_body = init_func.group(1)
            # 检查是否初始化为有效对象（包括 &Class::GetInstance() 等）
            # 匹配模式: var = &Something, var = new Something, var = Something::GetInstance()
            # 支持: g_var = &Class::GetInstance(), g_var = new Class(), g_var = &obj
            init_pattern = rf"{re.escape(var_name)}\s*=\s*(?:&\s*)?(?:(?:\w+::)+)?\w+(?:\s*\([^)]*\))?"
            if not re.search(init_pattern, init_body):
                errors.append(
                    f"规则019[高危]: 全局指针 {var_name} 声明为 nullptr，"
                    f"但在 LLVMFuzzerInitialize 中未正确初始化，"
                    f"可能导致空指针解引用"
                )
        else:
            errors.append(
                f"规则019[高危]: 全局指针 {var_name} 声明为 nullptr，"
                f"但未找到 LLVMFuzzerInitialize 函数进行初始化"
            )

    return errors


def check_target_size(content):
    """
    规则006: 检查单文件测试接口数量是否超过10个
    支持三种模式：
    1. TARGET_SIZE 常量定义
    2. 串行调用 DoXXX 函数
    3. switch-case 分支
    """
    errors = []

    # 1. 检查 TARGET_SIZE 常量
    match = re.search(r"const\s+\w+\s+TARGET_SIZE\s*=\s*(\d+)", content)
    if match:
        target_size = int(match.group(1))
        if target_size > 10:
            errors.append(
                f"规则006[中危]: TARGET_SIZE={target_size} 超过10，单文件接口过多会导致数据变异性差，建议拆分为多个fuzzer文件"
            )
            return errors

    # 2. 检查串行调用的 DoXXX 函数数量
    # 匹配 g_instance->DoXxx(fdp) 或 DoXxx(fdp) 的调用
    serial_calls = re.findall(r"\b(Do\w+)\s*\(\s*\w+\s*\)", content)
    # 去重
    unique_serial_calls = list(dict.fromkeys(serial_calls))
    if len(unique_serial_calls) > 10:
        errors.append(
            f"规则006[中危]: 发现 {len(unique_serial_calls)} 个串行调用的测试函数，超过10个会导致数据变异性差，"
            f"建议拆分为多个fuzzer文件或使用switch-case模式"
        )
        return errors

    # 3. 检查 switch-case 分支数量
    # 匹配 switch 语句中的 case 数量
    switch_pattern = re.compile(
        r"switch\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}", re.DOTALL
    )
    for switch_match in switch_pattern.finditer(content):
        switch_body = switch_match.group(1)
        # 统计 case 数量（包括 default）
        case_count = len(re.findall(r"\bcase\s+", switch_body))
        if case_count > 10:
            errors.append(
                f"规则006[中危]: switch-case 模式中有 {case_count} 个分支，超过10个会导致数据变异性差，"
                f"建议拆分为多个fuzzer文件"
            )
            return errors

    # 4. 检查 if-else if 链式调用（另一种多分支模式）
    # 统计连续的 if-else if 数量
    if_chain = re.findall(
        r"\bif\s*\([^)]*\)\s*\{[^}]*\}\s*(?:else\s+if\s*\([^)]*\)\s*\{[^}]*\}\s*)*",
        content,
        re.DOTALL,
    )
    for chain in if_chain:
        if_count = len(re.findall(r"\bif\s*\(", chain))
        if if_count > 10:
            errors.append(
                f"规则006[中危]: if-else if 链式调用中有 {if_count} 个分支，超过10个会导致数据变异性差，"
                f"建议拆分为多个fuzzer文件"
            )
            return errors

    return errors


def check_data_usage(content):
    """
    规则018: 检查data指针的直接使用
    禁止: 解引用、强转、当字符串/C数组使用、当句柄使用
    """
    errors = []

    # 1. 检查 data 指针解引用（如 *(int32_t*)data, *data）
    if re.search(r"\*\s*\(\s*\w+\s*\*\s*\)\s*data", content):
        errors.append(
            "规则018[高危]: 发现 data 指针解引用（如 *(Type*)data），应使用 FuzzedDataProvider 提取数据"
        )

    # 2. 检查 data 指针强转为结构体/类指针
    if re.search(r"\(\s*\w+\s*\*\s*\)\s*data", content):
        patterns = re.findall(r"\(\s*(\w+)\s*\*\s*\)\s*data", content)
        for p in patterns:
            if p not in ("const", "uint8_t", "char"):
                errors.append(
                    f"规则018[高危]: 发现 ({p}*)data 强转，应通过 FuzzedDataProvider 提取"
                )

    # 3. 检查 data 当作 C 风格字符串使用
    if re.search(r"char\s*\*\s*\w+\s*=\s*\(\s*char\s*\*\s*\)\s*data", content):
        errors.append(
            "规则018[高危]: 将 data 当作 C 风格字符串使用，二进制数据可能不含终止符，应使用 fdp.ConsumeRandomLengthString()"
        )

    # 4. 检查 data 当作句柄/描述符使用（如 int fd = *(int*)data）
    if re.search(
        r"(?:int|fd|handle)\s+\w+\s*=\s*\*\s*\(\s*(?:int|fd|handle)\s*\*\s*\)\s*data",
        content,
    ):
        errors.append(
            "规则018[高危]: 将 data 直接转为句柄/描述符使用，应使用 fdp.ConsumeIntegral<int>() 提取"
        )

    # 5. 检查 data[i] 直接索引使用（包括 data[0], data[i], data[size-1] 等）
    if re.search(r"data\s*\[\s*[^\]]+\s*\]", content):
        errors.append(
            "规则018[高危]: 发现 data[...] 直接索引使用，应使用 FuzzedDataProvider 提取数据"
        )

    # 6. 检查将 data 传给需要字符串/结构体的接口
    method_calls = re.findall(r"\w+\s*->\s*\w+\s*\(\s*data\s*\)", content)
    if method_calls:
        errors.append(
            "规则018[高危]: 将原始 data 指针直接传给业务接口，应使用 FuzzedDataProvider 提取参数"
        )

    return errors


def check_size_usage(content):
    """
    规则010: 检查size是否被当作变异数据使用
    size仅应用于FuzzedDataProvider初始化和边界检查
    """
    errors = []

    if not re.search(r"LLVMFuzzerTestOneInput", content):
        return errors

    # 检查LLVMFuzzerTestOneInput函数体
    func_match = re.search(
        r"extern\s+\"C\"\s+int\s+LLVMFuzzerTestOneInput\s*\([^)]*\)\s*\{", content
    )
    if not func_match:
        return errors

    func_body = _extract_fuzzer_func_body(
        content, "LLVMFuzzerTestOneInput", func_match.end() - 1
    )

    # 1. 检查将size直接传给被测API
    api_calls = re.finditer(r"(\w+)\s*->\s*(\w+)\s*\(([^)]*)\)", func_body)

    for match in api_calls:
        obj_name = match.group(1)
        method_name = match.group(2)
        args_str = match.group(3)

        # 排除FuzzedDataProvider构造
        if obj_name == "FuzzedDataProvider" or "FuzzedDataProvider" in args_str:
            continue

        # 检查参数中是否包含size
        if re.search(r"\bsize\b", args_str):
            # 排除: if (size < N) return 0; 这样的边界检查
            line_start = func_body.rfind("\n", 0, match.start()) + 1
            context = func_body[line_start : match.start()]

            if not re.search(r"return\s+0", context):
                errors.append(
                    f"规则010[高危]: 将size参数直接传给 {method_name}()，"
                    f"size由fuzz引擎决定不代表业务输入，应通过fdp.ConsumeIntegral<T>()提取"
                )

    # 2. 检查用size做业务分支判断
    branch_matches = re.finditer(
        r"if\s*\([^)]*\bsize\b[^)]*\)\s*\{[^}]*\w+\s*->\s*\w+\s*\(", func_body
    )

    for match in branch_matches:
        branch_text = match.group(0)
        if re.search(r"return\s+0", branch_text):
            continue
        if re.search(r"if\s*\(\s*size\s*[<>]=?\s*\d+\s*\)\s*\{?\s*return", branch_text):
            continue

        errors.append(
            "规则010[高危]: 用size参数做业务分支判断，"
            "size仅用于边界检查，业务分支条件应通过fdp.ConsumeBool()或fdp.ConsumeIntegral()提取"
        )

    # 3. 检查用size作为循环次数
    loop_patterns = [
        r"for\s*\([^)]*\bsize\b[^)]*\)",
        r"while\s*\([^)]*\bsize\b[^)]*\)",
    ]

    for pattern in loop_patterns:
        for match in re.finditer(pattern, func_body):
            loop_text = match.group(0)
            if re.search(r"size\s*[<>]=?\s*\d+", loop_text):
                continue
            errors.append(
                "规则010[高危]: 用size参数作为循环次数，"
                "循环次数应通过fdp.ConsumeIntegralInRange<T>(min, max)提取"
            )

    # 4. 检查size参与算术运算后作为参数
    arithmetic_matches = re.finditer(r"(\w+)\s*=\s*[^;]*\bsize\b[^;]*;", func_body)

    for match in arithmetic_matches:
        var_name = match.group(1)
        expr = match.group(0)

        if re.search(r"size\s*[<>]=?\s*\d+", expr):
            continue
        if "FuzzedDataProvider" in expr:
            continue

        api_usage = re.search(
            rf"\w+\s*->\s*(\w+)\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)",
            func_body[match.end() :],
        )

        if api_usage:
            method_name = api_usage.group(1)
            errors.append(
                f"规则010[高危]: size参数参与算术运算后作为参数传给 {method_name}()，"
                f"size由fuzz引擎决定，业务参数应通过fdp.ConsumeIntegral<T>()提取"
            )

    return errors


def check_type_mismatch(content):
    """
    规则016: 检查类型不匹配问题
    - fdp生成类型与变量声明类型不一致
    - 小字节类型赋值给大字节类型
    - 有符号/无符号混用
    - 整数与浮点混用
    - 指针与整数混用
    """
    errors = []

    # 1. 检查 data 强转为 char*（已在规则6检查，这里保留以防遗漏）
    if re.search(r"char\s*\*\s*\w+\s*=\s*\(\s*char\s*\*\s*\)\s*data", content):
        errors.append(
            "规则016[高危]: 将 data 强转为 char*，二进制数据不等于字符串，应使用 fdp.ConsumeRandomLengthString()"
        )

    # 2. 检查 fdp 生成类型与变量声明类型不一致（数据截断/扩展问题）
    # 匹配模式: Type var = fdp.ConsumeIntegral<OtherType>()
    type_mismatch_patterns = [
        # 大类型生成，小类型接收（数据截断）
        (
            r"uint8_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<uint(?:16|32|64)_t>",
            "uint8_t",
            "uint16/32/64_t",
        ),
        (
            r"int8_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int(?:16|32|64)_t>",
            "int8_t",
            "int16/32/64_t",
        ),
        (
            r"uint16_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<uint(?:32|64)_t>",
            "uint16_t",
            "uint32/64_t",
        ),
        (
            r"int16_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int(?:32|64)_t>",
            "int16_t",
            "int32/64_t",
        ),
        (
            r"uint32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<uint64_t>",
            "uint32_t",
            "uint64_t",
        ),
        (r"int32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int64_t>", "int32_t", "int64_t"),
        # 浮点数相关
        (r"float\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<\w+>", "float", "整数类型"),
        (r"double\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<\w+>", "double", "整数类型"),
    ]

    for pattern, var_type, fdp_type in type_mismatch_patterns:
        mismatches = re.findall(pattern, content)
        for var_name in mismatches:
            errors.append(
                f"规则016[高危]: 变量 {var_name} 声明为 {var_type}，但使用 fdp.ConsumeIntegral<{fdp_type}>() 赋值，"
                f"类型不匹配可能导致数据截断或精度丢失，应使用匹配的类型"
            )

    # 3. 检查小类型赋值给大类型（8位 -> 32/64位，变异空间受限）
    small_type_vars = re.findall(
        r"(uint8_t|int8_t)\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<(?:uint8_t|int8_t)>",
        content,
    )
    for _, var_name in small_type_vars:
        large_assign = re.search(
            rf"(uint64_t|int64_t|uint32_t|int32_t)\s+\w+\s*=\s*{re.escape(var_name)}\b",
            content,
        )
        if large_assign:
            errors.append(
                f"规则016[高危]: 将 8 位变量 {var_name} 赋值给 {large_assign.group(1)}，数据会被截断"
            )

    # 4. 检查有符号/无符号混用（负数变超大正数）
    signed_unsigned_patterns = [
        (
            r"int8_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int8_t>",
            r"size_t\s+\w+\s*=\s*\w+",
            "int8_t 赋值给 size_t",
        ),
        (
            r"int16_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int16_t>",
            r"size_t\s+\w+\s*=\s*\w+",
            "int16_t 赋值给 size_t",
        ),
        (
            r"int32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int32_t>",
            r"size_t\s+\w+\s*=\s*\w+",
            "int32_t 赋值给 size_t",
        ),
    ]

    for signed_pattern, unsigned_pattern, desc in signed_unsigned_patterns:
        signed_vars = re.findall(signed_pattern, content)
        for var_name in signed_vars:
            if re.search(rf"size_t\s+\w+\s*=\s*{re.escape(var_name)}\b", content):
                errors.append(
                    f"规则016[高危]: 有符号/无符号混用: {desc}，负数会被解释为超大正数，应使用匹配的类型"
                )

    # 5. 检查整数与浮点混用
    int_to_float_patterns = [
        (
            r"int32_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int32_t>",
            r"float\s+\w+\s*=\s*static_cast<float>\s*\(\s*\w+\s*\)",
        ),
        (
            r"int64_t\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<int64_t>",
            r"double\s+\w+\s*=\s*static_cast<double>\s*\(\s*\w+\s*\)",
        ),
    ]

    for int_pattern, float_pattern in int_to_float_patterns:
        int_vars = re.findall(int_pattern, content)
        for var_name in int_vars:
            if re.search(
                rf"float\s+\w+\s*=\s*static_cast<float>\s*\(\s*{re.escape(var_name)}\s*\)",
                content,
            ):
                errors.append(
                    f"规则016[高危]: 将整数变量 {var_name} 转为 float，会丢失小数部分，应使用 fdp.ConsumeFloatingPoint<float>()"
                )

    # 6. 检查指针与整数混用
    if re.search(r"uintptr_t\s+\w+\s*=\s*fdp\.ConsumeIntegral<uintptr_t>", content):
        if re.search(r"reinterpret_cast<void\*>\s*\(\s*\w+\s*\)", content):
            errors.append(
                "规则016[高危]: 将整数 reinterpret_cast 为指针，随机地址可能无效，应通过合法 API 构造对象"
            )

    return errors


def check_buffer_overflow(content):
    """
    规则009: 检查FUZZ Driver引入的安全问题
    - 内存安全类：堆溢出、栈溢出、数组越界、空指针解引用
    - 资源管理类：内存泄漏（new/delete不匹配）
    - 逻辑安全类：整数溢出/下溢、超大内存分配
    - 构造合理性问题：未初始化指针、未释放资源
    """
    errors = []
    # 1) 检测是否使用 data/size 进行 memcpy/memset 等可能堆溢出的操作
    # 要求：函数调用参数中包含 fdp 相关变量（fdp. 或从 fdp 获取的变量）
    dangerous_funcs = ["memcpy", "memset", "memmove", "strcpy", "strncpy"]
    for func in dangerous_funcs:
        for match in re.finditer(rf"\b{func}\s*\(", content):
            # 获取函数调用位置及参数
            call_start = match.start()
            call_end = content.find(")", call_start)
            if call_end == -1:
                call_end = len(content)
            call_content = content[call_start:call_end]
            # 检查参数是否包含 fdp 消费的数据或长度
            if re.search(
                r"fdp\.(Consume|Pick|PickValueInArray)", call_content
            ) or re.search(r"\b(data|size|len|length)\b", call_content):
                errors.append(
                    f"规则009[高危]: 发现 {func}() 操作使用 fuzz 数据，若目标缓冲区大小小于 source 长度可能导致堆溢出，"
                    "请确保目标缓冲区大小与复制长度严格匹配"
                )
                break

    # 2) 检测 ConsumeBytes / ConsumeRandomLengthString 是否使用了极大的无限制长度
    large_bytes = re.findall(r"ConsumeBytes<\w+>\(\s*(\d{6,})\s*\)", content)
    for val in large_bytes:
        errors.append(
            f"规则009[高危]: ConsumeBytes() 使用了极大长度 {val}，可能导致内存占用过高或堆溢出，"
            "建议限制在合理范围（如 ≤ 65535）"
        )

    # 2.1) 检测未限制大小的内存分配
    # 匹配 pattern: make_unique<Type[]>(...) 或 new Type[...]
    # 检查参数是否来自 fdp 且没有 % 限制
    alloc_patterns = [
        r"make_unique\<\s*\w+\s*\[]\>\s*\(([^)]+)\)",
        r"make_shared\<\s*\w+\s*\[]\>\s*\(([^)]+)\)",
        r"new\s+\w+\s*\[([^\]]+)\]",
    ]
    for pattern in alloc_patterns:
        for match in re.finditer(pattern, content):
            arg = match.group(1).strip()
            # 检查参数是否直接包含 fdp 消费（如 fdp.ConsumeIntegral）
            is_from_fdp = "fdp." in arg
            # 或者参数是变量，该变量从 fdp 获取
            if not is_from_fdp and re.match(r"^\w+$", arg):
                # 检查变量定义是否来自 fdp
                var_def_pattern = rf"\b{re.escape(arg)}\s*=\s*fdp\."
                if re.search(var_def_pattern, content):
                    is_from_fdp = True

            if is_from_fdp:
                # 检查是否有 % 限制（在分配附近）
                alloc_pos = match.start()
                nearby_content = content[max(0, alloc_pos - 200) : alloc_pos + 200]
                if not re.search(r"%\s*\d+", nearby_content):
                    errors.append(
                        "规则009[高危]: 发现未限制大小的内存分配（如 make_unique<Type[]>(fdp数据)），"
                        "可能分配超大内存导致卡住，应添加 % 限制大小（如 % 65536）"
                    )

    # 3) 检测数组越界访问（无范围校验的数组索引）
    # 匹配 pattern: Type values[N]; values[index] = ...（没有 if 检查）
    array_access = re.search(
        r"(\w+)\s+\w+\s*\[\s*(\d+)\s*\]\s*;[^}]*?\w+\s*\[\s*\w+\s*\]\s*=",
        content,
        re.DOTALL,
    )
    if array_access:
        # 检查前面是否有 if 校验
        array_size = array_access.group(2)
        # 简单检查：如果同一函数内没有 if (index < array_size) 之类的检查
        if not re.search(r"if\s*\([^)]*[<>]=?\s*" + array_size + r"[^)]*\)", content):
            errors.append(
                f"规则009[高危]: 发现数组访问未做范围校验（数组大小 {array_size}），可能导致数组越界，"
                f"应添加 if (index >= 0 && index < {array_size}) 检查"
            )

    # 4) 检测空指针解引用（将 nullptr 传给接口）
    if re.search(r"\w+\s*=\s*nullptr\s*;", content):
        # 检查是否有接口调用使用了这个 nullptr
        null_vars = re.findall(r"(\w+)\s*=\s*nullptr\s*;", content)
        for var in null_vars:
            if re.search(
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var)}\b[^)]*\)", content
            ):
                errors.append(
                    f"规则009[高危]: 将 nullptr 变量 {var} 传给接口调用，可能导致空指针解引用，"
                    f"应构造有效对象而非传递 nullptr"
                )

    # 4.1) 检测未初始化的指针使用
    # 匹配 pattern: Type* ptr; （没有初始化）后面使用 ptr
    uninitialized_ptr = re.search(
        r"(\w+)\s*\*\s*(\w+)\s*;(?![^}]*?=)",
        content,
    )
    if uninitialized_ptr:
        ptr_var = uninitialized_ptr.group(2)
        # 检查后面是否使用了这个未初始化的指针
        if re.search(
            rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(ptr_var)}\b[^)]*\)", content
        ):
            errors.append(
                f"规则009[高危]: 发现未初始化的指针 {ptr_var} 被使用，可能导致未定义行为，"
                f"应使用 make_unique/make_shared 或 new 初始化"
            )

    # 5) 检测整数下溢（减法未做保护）
    # 匹配 pattern: total = len - extra;（没有 if (len >= extra) 保护）
    sub_patterns = re.findall(
        r"(\w+)\s*=\s*(\w+)\s*-\s*(\w+)\s*;",
        content,
    )
    for result, left, right in sub_patterns:
        # 检查是否是 fdp 变量参与的运算
        if re.search(rf"{re.escape(left)}\s*=\s*fdp\.", content):
            # 检查是否有保护
            if not re.search(
                rf"if\s*\([^)]*{re.escape(left)}\s*[><]=?\s*{re.escape(right)}[^)]*\)",
                content,
            ):
                errors.append(
                    f"规则009[高危]: 发现整数减法 {result} = {left} - {right} 未做下溢保护，"
                    f"当 {left} < {right} 时会发生下溢，应添加 if ({left} >= {right}) 检查"
                )

    # 5.1) 检测整数溢出（乘法未做保护）
    mul_patterns = re.findall(
        r"(\w+)\s*=\s*(\w+)\s*\*\s*(\w+)\s*;",
        content,
    )
    for result, left, right in mul_patterns:
        # 检查是否是 fdp 变量参与的运算
        if re.search(rf"{re.escape(left)}\s*=\s*fdp\.", content) or re.search(
            rf"{re.escape(right)}\s*=\s*fdp\.", content
        ):
            # 检查是否有保护
            if not re.search(
                rf"if\s*\([^)]*{re.escape(result)}\s*[<>][^)]*\)", content
            ):
                errors.append(
                    f"规则009[高危]: 发现整数乘法 {result} = {left} * {right} 未做溢出保护，"
                    f"可能发生整数溢出，应添加范围检查"
                )

    # 6) 检测长度判断与实际读取不匹配
    # 匹配 pattern: if (bufferSize < N) return; 后面读取的字节数超过 N
    size_check = re.search(
        r"if\s*\(\s*(\w+)\s*<\s*(\d+)\s*\)\s*\{\s*return",
        content,
    )
    if size_check:
        var_name = size_check.group(1)
        checked_size = int(size_check.group(2))
        check_pos = size_check.end()
        remaining = content[check_pos:]
        # 统计所有 fdp 消费的字节数
        byte_consumes = {
            "int8_t": 1,
            "uint8_t": 1,
            "int16_t": 2,
            "uint16_t": 2,
            "int32_t": 4,
            "uint32_t": 4,
            "int64_t": 8,
            "uint64_t": 8,
            "char": 1,
            "short": 2,
            "int": 4,
            "long": 8,
            "float": 4,
            "double": 8,
        }
        total_bytes = 0
        for type_name, size in byte_consumes.items():
            count = len(
                re.findall(
                    rf"fdp\.ConsumeIntegral<{re.escape(type_name)}>\s*\(", remaining
                )
            )
            total_bytes += count * size
        # ConsumeBool 占 1 字节
        total_bytes += len(re.findall(r"fdp\.ConsumeBool\s*\(", remaining))
        # ConsumeFloatingPoint
        total_bytes += (
            len(re.findall(r"fdp\.ConsumeFloatingPoint<float>\s*\(", remaining)) * 4
        )
        total_bytes += (
            len(re.findall(r"fdp\.ConsumeFloatingPoint<double>\s*\(", remaining)) * 8
        )
        if total_bytes > checked_size:
            errors.append(
                f"规则009[高危]: 长度检查不足: {var_name} 只检查了 {checked_size} 字节，"
                f"但后续读取了约 {total_bytes} 字节，可能导致堆溢出"
            )

    # 7) 检测内存泄漏（new 后没有 delete）
    # 匹配 pattern: Type* var = new Type(...);
    new_allocations = re.findall(
        r"(\w+)\s*\*\s*(\w+)\s*=\s*new\s+\w+",
        content,
    )
    for type_name, var_name in new_allocations:
        # 检查是否有对应的 delete
        if not re.search(rf"delete\s+{re.escape(var_name)}", content) and not re.search(
            rf"delete\[\]\s+{re.escape(var_name)}", content
        ):
            errors.append(
                f"规则009[高危]: 发现内存泄漏: 使用 new 分配了 {var_name} 但未释放，"
                f"应使用 delete/delete[] 释放或使用智能指针（make_unique/make_shared）"
            )

    # 8) 检测 malloc 后没有 free
    malloc_allocations = re.findall(
        r"(\w+)\s*\*\s*(\w+)\s*=\s*\(\s*\w+\s*\*\s*\)\s*malloc",
        content,
    )
    for type_name, var_name in malloc_allocations:
        # 检查是否有对应的 free
        if not re.search(rf"free\s*\(\s*{re.escape(var_name)}\s*\)", content):
            errors.append(
                f"规则009[高危]: 发现内存泄漏: 使用 malloc 分配了 {var_name} 但未释放，"
                f"应使用 free 释放或使用智能指针"
            )

    # 9) 检测文件句柄泄漏（fopen/open 后没有 fclose/close）
    file_ops = re.findall(
        r"(?:FILE\s*\*|int)\s*(\w+)\s*=\s*(?:fopen|open)\s*\(",
        content,
    )
    for var_name in file_ops:
        if not re.search(
            rf"(?:fclose|close)\s*\(\s*{re.escape(var_name)}\s*\)", content
        ):
            errors.append(
                f"规则009[高危]: 发现文件句柄泄漏: 使用 fopen/open 打开了文件（{var_name}）但未关闭，"
                f"应使用 fclose/close 释放"
            )

    # 10) 检测越界偏移量计算（指针 + 偏移量 未做范围校验）
    offset_patterns = re.findall(
        r"(\w+)\s*\+\s*(\w+)",
        content,
    )
    for base, offset in offset_patterns:
        # 检查偏移量是否来自 fdp
        if re.search(rf"{re.escape(offset)}\s*=\s*fdp\.", content):
            # 检查是否有范围校验
            if not re.search(
                rf"if\s*\([^)]*{re.escape(offset)}\s*[<>]=?\s*\d+[^)]*\)", content
            ):
                errors.append(
                    f"规则009[高危]: 发现偏移量计算 {base} + {offset} 未做范围校验，"
                    f"偏移量来自 fdp 可能导致越界访问，应添加 if ({offset} < max_offset) 检查"
                )

    return errors


def check_ipc_pattern(content):
    """
    规则007: 检查IPC接口是否通过OnRemoteRequest直接测试stub
    跨进程调用无法被fuzz引擎监控，应改为直接调用stub的OnRemoteRequest

    优化：区分Proxy/Stub调用模式，减少误报
    - 如果代码中只使用了Proxy模式（如RSInterfaces），给出警告
    - 如果代码中使用了Stub模式但没有OnRemoteRequest，报错
    """
    errors = []

    # 检测 IPC proxy/stub 相关类
    has_proxy = re.search(r"\w*[Pp]roxy", content)
    has_stub = re.search(r"\b\w*[Ss]tub\b", content)
    has_ipc = re.search(r"\bIPC\w+", content)
    has_on_remote = "OnRemoteRequest" in content

    # 优化：区分模式
    if has_stub and not has_on_remote:
        # 使用了Stub但没有OnRemoteRequest，这是真正的问题
        errors.append(
            "规则007[高危]: 代码涉及 IPC Stub 接口但未通过 OnRemoteRequest 测试，"
            "跨进程调用无法被 fuzz 引擎监控，建议改为直接调用 stub 的 OnRemoteRequest"
        )
    elif has_proxy and not has_ipc and not has_on_remote:
        # 只使用了Proxy（如RSInterfaces），这是客户端调用
        # 给出低级别警告，因为客户端逻辑也可以被fuzz
        errors.append(
            "规则007[低危]: 代码使用 IPC Proxy 接口（如 RSInterfaces），"
            "只能覆盖客户端逻辑，服务端逻辑不受监控。"
            "如需覆盖服务端逻辑，建议通过 OnRemoteRequest 测试 Stub"
        )
    elif has_ipc and not has_on_remote:
        # 涉及IPC但没有OnRemoteRequest
        errors.append(
            "规则007[中危]: 代码涉及 IPC 通信但未通过 OnRemoteRequest 测试，"
            "建议区分测试客户端（Proxy）和服务端（Stub）逻辑"
        )

    return errors


def check_security_context(content):
    """
    规则011: 检查系统安全准入条件
    检测是否可能缺少权限、身份、状态等安全上下文构造
    """
    errors = []

    # 1. 检测是否调用了可能需要权限的敏感接口，但没有前置的权限设置
    # 常见需要权限的接口模式
    sensitive_apis = [
        r"\b(SetPermission|CheckPermission|VerifyToken|Authenticate)\b",
        r"\b(Sensitive|Secure|Admin|System)\w*\s*\(",
    ]

    # 检查是否有敏感接口调用
    has_sensitive_call = False
    for pattern in sensitive_apis:
        if re.search(pattern, content):
            has_sensitive_call = True
            break

    # 如果检测到敏感接口调用但没有权限设置，报告问题
    if has_sensitive_call:
        # 检查是否有权限设置前置调用
        has_permission_setup = re.search(
            r"\b(SetPermission|SetToken|SetUid|SetCaller|Authenticate|VerifyToken)\b",
            content,
        )
        if not has_permission_setup:
            errors.append(
                "规则011[高危]: 检测到敏感接口调用，但未发现权限设置或身份认证的前置调用。"
                "请检查是否需要构造：1) 权限token 2) 调用者身份 3) 会话信息。"
            )

    # 2. 检测常见的安全校验绕过或缺失
    # 检查是否直接调用了可能受权限保护的接口，而没有构造上下文
    # 匹配 g_instance->Xxx(...) 或 g_manager->Xxx(...) 等调用
    api_calls = re.findall(r"\w+\s*->\s*(\w+)\s*\(", content)

    # 检查是否调用了需要初始化的接口但没有初始化
    # 这是一个启发式检查，基于常见的命名模式
    # 只检查特定的高风险模式，避免误报普通 API
    needs_init_patterns = [
        r"Configure",
        r"SetMode",
        r"SetConfig",
    ]
    init_patterns = [
        r"^Init$",
        r"^Initialize$",
        r"^Prepare$",
        r"^SetUp$",
        r"^Create$",
        r"^Open$",
        r"^Connect$",
        r"^Login$",
    ]

    needs_init = False
    has_init = False
    for call in api_calls:
        # 检查是否需要初始化（特定高风险接口）
        for pattern in needs_init_patterns:
            if re.search(pattern, call):
                needs_init = True
                break
        # 检查是否有初始化调用
        for pattern in init_patterns:
            if re.match(pattern, call):
                has_init = True
                break

    # 如果可能需要初始化但没有初始化，给出警告
    if needs_init and not has_init and len(api_calls) > 0:
        # 检查是否有状态相关的注释或文档说明
        if not re.search(
            r"//.*(?:已初始化|initialized|prepared)", content, re.IGNORECASE
        ):
            errors.append(
                "规则011[高危]: 检测到可能调用需要前置初始化的接口，但未发现初始化调用。"
                "请检查目标 API 是否需要：1) 系统初始化 2) 权限设置 3) 会话建立 4) 状态准备。"
                "缺少安全准入条件会导致 fuzz 无法触及业务逻辑。"
            )

    # 3. 检测 IPC stub 接口是否绕过了安全校验
    # 如果测试的是 OnRemoteRequest，检查是否构造了完整的 MessageParcel
    if "OnRemoteRequest" in content:
        # 检查是否有 WriteInterfaceToken（通常用于权限校验）
        if not re.search(r"WriteInterfaceToken", content):
            errors.append(
                "规则011[高危]: 测试 OnRemoteRequest 时未调用 WriteInterfaceToken，"
                "可能导致权限校验失败，建议构造完整的 MessageParcel 包括接口 token"
            )

    return errors


def _is_output_param(var_name, body):
    """
    判断变量是否为输出参数（在API调用中被修改，调用后不再使用）

    优化：增强输出参数检测逻辑，减少误报
    """
    # 1. 检查变量是否在API调用中作为引用/指针参数
    api_call_pattern = rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)"
    api_calls = re.findall(api_call_pattern, body)

    if not api_calls:
        return False

    # 2. 检查变量初始化值
    init_match = re.search(rf"\b\w+\s+{re.escape(var_name)}\s*=\s*(\w+)", body)
    if init_match:
        init_value = init_match.group(1)
        # 常见输出参数初始化值：0, nullptr, false, 空字符串等
        if init_value in ("0", "nullptr", "false", "NULL", "{}", "0.0f"):
            # 进一步检查：API调用后是否还使用了这个变量
            for api_call in api_calls:
                api_pos = body.find(api_call)
                if api_pos >= 0:
                    after_api = body[api_pos + len(api_call) :]
                    # 如果API调用后不再使用（或只是return），则是输出参数
                    remaining_usage = re.findall(
                        rf"\b{re.escape(var_name)}\b", after_api
                    )
                    if not remaining_usage:
                        return True
                    # 检查后续使用是否只是return语句或(void)转换
                    for usage in remaining_usage:
                        usage_pos = after_api.find(var_name)
                        line_start = after_api.rfind("\n", 0, usage_pos) + 1
                        line = after_api[line_start : line_start + 100].strip()
                        if line.startswith("return") or line.startswith("(void)"):
                            return True

    # 3. 检查变量类型是否为引用或指针（从声明中推断）
    var_decl = re.search(rf"\b(\w+\s*\*?\s*\&?)\s*{re.escape(var_name)}\s*[=;]", body)
    if var_decl:
        type_str = var_decl.group(1).strip()
        if "*" in type_str or "&" in type_str:
            # 指针或引用类型，可能是输出参数
            for api_call in api_calls:
                api_pos = body.find(api_call)
                if api_pos >= 0:
                    after_api = body[api_pos + len(api_call) :]
                    if not re.search(rf"\b{re.escape(var_name)}\b", after_api):
                        return True

    return False


def check_branch_coverage(content):
    """
    规则012: 检查目标API内部分支覆盖是否可能不足
    检测常见的导致fuzz无法触及核心逻辑的问题

    优化：增强输出参数检测，减少固定值误报

    注意: 本规则专注于分支覆盖问题，不检测空容器/空指针构造
    （空容器/空指针由规则005负责检测）
    """
    errors = []

    # 1. 检测是否使用了固定值作为参数（排除小数值和输出参数初始化）
    # 按函数逐个检查
    func_pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*\&\s*\w+\s*\)\s*\{"
    )

    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1

        # 提取函数体
        brace_count = 0
        body_start = -1
        body = ""
        for i in range(start, len(content)):
            if content[i] == "{":
                brace_count += 1
                if brace_count == 1:
                    body_start = i + 1
            elif content[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    body = content[body_start:i]
                    break

        if not body:
            continue

        # 在函数体内查找固定值赋值
        fixed_assignments = re.findall(
            r"(?:uint32_t|int32_t|uint64_t|int64_t|uint8_t|int8_t|auto)\s+(\w+)\s*=\s*(\d+)\s*;",
            body,
        )

        for var_name, value in fixed_assignments:
            # 排除小数值（0-5通常用于索引、计数等）
            if value in ("0", "1", "2", "3", "4", "5"):
                continue

            # 优化：使用增强的输出参数检测
            if _is_output_param(var_name, body):
                continue  # 是输出参数，跳过

            # 检查是否使用了fdp（如果使用了fdp，固定值可能是合理的）
            if re.search(r"fdp\.Consume", body):
                # 如果函数中使用了fdp，但仍有固定值，可能是部分参数固定
                errors.append(
                    f"规则012[高危]: 函数 {func_name}() 中发现将固定值 {value} 作为参数传给接口，"
                    f"可能只覆盖了特定分支。应使用 fdp.ConsumeXxx() 产生变异数据以覆盖多分支。"
                )
                break  # 只报告一次

    # 4. 检测是否未构造前置依赖
    # 检查是否调用了需要前置状态的接口，但没有前置调用
    # 基于常见的命名模式
    # 注意：只检查特定的高风险模式，避免误报普通 API
    # 这些 API 通常需要前置的 Init/Create/Load 等调用
    dependent_apis_patterns = [
        r"^ProcessData$",
        r"^ProcessImage$",
        r"^HandleRequest$",
        r"^HandleEvent$",
        r"^ExecuteCommand$",
        r"^RenderFrame$",
        r"^DrawSurface$",
        r"^ReceiveData$",
        r"^ParseMessage$",
        r"^ParseData$",
        r"^Configure$",
        r"^Update$",
        r"^Modify$",
    ]
    setup_apis = [
        r"Init",
        r"Initialize",
        r"Create",
        r"Load",
        r"Open",
        r"Prepare",
        r"SetUp",
        r"Connect",
        r"Start",
        r"Begin",
    ]

    # 提取所有 API 调用
    api_calls = re.findall(r"\w+\s*->\s*(\w+)\s*\(", content)

    has_dependent = False
    has_setup = False
    for call in api_calls:
        # 严格匹配特定的高风险 API 名称
        for pattern in dependent_apis_patterns:
            if re.match(pattern, call):
                has_dependent = True
                break
        for pattern in setup_apis:
            if re.search(pattern, call):
                has_setup = True
                break

    # 如果调用了依赖型 API 但没有设置型 API，给出警告
    if has_dependent and not has_setup and len(api_calls) >= 1:
        # 排除已经有初始化注释的情况
        if not re.search(
            r"//.*(?:已初始化|initialized|prepared|setup)", content, re.IGNORECASE
        ):
            errors.append(
                "规则012[高危]: 检测到可能调用需要前置状态的接口，但未发现状态准备调用。"
                "请检查目标 API 是否需要先调用 Init/Create/Load 等接口构造前置条件。"
                "缺少前置依赖会导致 fuzz 无法触及核心业务逻辑。"
            )

    # 5. 检测是否使用了 ConsumeBytes 但长度为 0
    # 匹配 pattern: ConsumeBytes<Type>(0) 或没有 +1 保护
    zero_bytes = re.search(
        r"ConsumeBytes<\w+\u003e\(\s*0\s*\)",
        content,
    )
    if zero_bytes:
        errors.append(
            "规则012[高危]: 发现使用 ConsumeBytes 时长度为 0，将产生空数据，"
            "可能只覆盖空数据校验分支。应确保长度大于 0 以覆盖数据处理逻辑。"
        )

    # 6. 检测是否未使用 % 限制，导致参数范围过大
    # 对于需要特定范围的参数（如枚举、模式），检查是否有限制
    # 这是一个启发式检查，只针对明显是枚举/模式类型的参数名
    enum_param_names = ["mode", "type", "format", "status", "flag", "option", "code"]
    for param_name in enum_param_names:
        # 匹配: uint32_t mode = fdp.ConsumeIntegral<uint32_t>();
        enum_like_usage = re.search(
            rf"(?:uint32_t|uint64_t)\s+{param_name}\s*=\s*fdp\.ConsumeIntegral<(?:uint32_t|uint64_t)>\s*\(\)\s*;",
            content,
            re.DOTALL,
        )
        if enum_like_usage:
            # 检查附近是否有 % 限制
            nearby = content[
                max(0, enum_like_usage.start() - 50) : enum_like_usage.end() + 200
            ]
            if "%" not in nearby:
                errors.append(
                    f"规则012[高危]: 发现参数 '{param_name}' 使用大范围类型(uint32_t/uint64_t)提取但未做 % 限制，"
                    f"可能导致绝大多数输入被参数范围校验拦截。"
                    f"建议添加 % 限制使合法值有合理命中概率（如 % 16 或 % 256）。"
                )
                break

    return errors


def check_enum_range(content):
    """
    规则013: 检查枚举值构造是否合理
    核心原则: 使用 uint8_t 而非大整数类型，不要按业务上限取模
    """
    errors = []

    # 1. 检查使用 uint64_t/int64_t 构造枚举
    # 模式1: static_cast<Enum>(fdp.ConsumeIntegral<uint64_t>())
    enum_casts_64_direct = re.findall(
        r"static_cast\<(\w+)\>\s*\(\s*fdp\.ConsumeIntegral\<(uint64_t|int64_t)\>\s*\(",
        content,
    )
    for enum_name, src_type in enum_casts_64_direct:
        errors.append(
            f"规则013[中危]: 枚举 {enum_name} 使用 {src_type} 构造，范围过大（0~18446744073709551615），"
            f"合法值命中率极低，建议使用 uint8_t（0~255）提取"
        )

    # 模式2: uint64_t var = fdp.ConsumeIntegral<uint64_t>(); static_cast<Enum>(var);
    enum_casts_64_indirect = re.findall(
        r"static_cast\<(\w+)\>\s*\(\s*(\w+)\s*\)",
        content,
    )
    for enum_name, var_name in enum_casts_64_indirect:
        # 检查变量是否使用 uint64_t/int64_t
        if re.search(
            rf"(?:uint64_t|int64_t)\s+{re.escape(var_name)}\s*=\s*fdp\.ConsumeIntegral",
            content,
        ):
            errors.append(
                f"规则013[中危]: 枚举 {enum_name} 使用 uint64_t/int64_t 构造，范围过大（0~18446744073709551615），"
                f"合法值命中率极低，建议使用 uint8_t（0~255）提取"
            )

    # 2. 检查使用 uint32_t/int32_t 构造枚举（最常见的情况）
    # 匹配两种模式：
    # 模式1: static_cast<Enum>(fdp.ConsumeIntegral<uint32_t>())
    # 模式2: uint32_t var = fdp.ConsumeIntegral<uint32_t>(); static_cast<Enum>(var);
    enum_casts_32 = re.findall(
        r"static_cast<(\w+)>\s*\(\s*\w+\s*\)",
        content,
    )
    for enum_name in enum_casts_32:
        # 检查对应的变量是否使用了 uint32_t/int32_t
        if re.search(
            rf"\w+\s*=\s*fdp\.ConsumeIntegral<(uint32_t|int32_t)>\s*\(",
            content,
        ):
            errors.append(
                f"规则013[中危]: 枚举 {enum_name} 使用 uint32_t/int32_t 构造，范围过大（0~4294967295），"
                f"合法值命中率极低，建议使用 uint8_t（0~255）提取"
            )
            break  # 报一次即可

    # 3. 检查枚举赋值但未使用 uint8_t（没有 static_cast 的直接赋值）
    enum_assignments = re.findall(
        r"(\w+)\s+(\w+)\s*=\s*fdp\.ConsumeIntegral<(uint32_t|int32_t|uint64_t|int64_t)>\s*\(",
        content,
    )
    for enum_type, var_name, src_type in enum_assignments:
        # 跳过非枚举类型（typedef/alias）
        if enum_type in NON_ENUM_TYPES:
            continue
        # 判断是否为枚举类型（大驼峰命名）— 排除基础类型和指针
        if re.match(r"^[A-Z][a-zA-Z0-9_]*$", enum_type) and "*" not in enum_type:
            errors.append(
                f"规则013[中危]: 枚举类型 {enum_type} 的变量 {var_name} 使用 {src_type} 提取，"
                f"范围过大，建议使用 uint8_t（0~255）提取"
            )

    # 4. 检查是否按业务上限取模（危险做法）
    # 匹配 pattern: fdp.ConsumeIntegral<uint8_t>() % N（N 较小，如 6, 8, 10 等）
    # 这通常意味着将枚举限制到业务上限，会丢失非法值覆盖
    small_modulo = re.search(
        r"fdp\.ConsumeIntegral<\w+>\s*\(\)\s*%\s*(\d+)",
        content,
    )
    if small_modulo:
        mod_value = int(small_modulo.group(1))
        if mod_value <= 8:  # 只有非常小的模数（<=8）才报错，因为会严重限制枚举值范围
            # 检查是否是枚举相关代码（附近有 static_cast<Enum> 或枚举类型声明）
            mod_pos = small_modulo.start()
            nearby = content[max(0, mod_pos - 200) : mod_pos + 200]
            if re.search(r"static_cast<\w+>", nearby) or re.search(
                r"\benum\b", nearby, re.IGNORECASE
            ):
                errors.append(
                    f"规则013[中危]: 发现对枚举值取模 % {mod_value}，可能将枚举限制到业务上限，"
                    f"会丢失非法值处理分支的覆盖。建议直接使用 uint8_t 提取而不取模，"
                    f"或取模到更大的值（如 % 256）以保留非法值覆盖。"
                )

    # 5. 检查是否绕过校验和/签名验证（常见于协议/文件解析）
    # 如果代码中计算了 checksum 或 signature 但没有验证，可能导致绕过
    checksum_patterns = [
        r"\b(checksum|crc|hash|signature|md5|sha)\w*\s*=",
        r"\bCalculate(CRC|Checksum|Hash|Signature)\b",
        r"\bVerify(CRC|Checksum|Hash|Signature)\b",
    ]
    has_checksum_calc = False
    has_checksum_verify = False
    for pattern in checksum_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            if "verify" in pattern.lower() or "check" in pattern.lower():
                has_checksum_verify = True
            else:
                has_checksum_calc = True

    if has_checksum_calc and not has_checksum_verify:
        errors.append(
            "规则013[中危]: 发现计算了校验和/签名但没有验证，可能导致构造的数据绕过完整性检查。"
            "应确保校验和/签名验证逻辑被正确执行。"
        )

    return errors


def check_fixed_params(content):
    """
    规则014: 检查是否使用固定参数
    fuzz测试应使用变异数据，除非业务必需（API版本号、Magic Number等）

    检测策略:
    1. 如果函数中所有参数都是固定值（无论是否"合理"），则报错
    2. 如果存在多个不合理的固定值（非业务必需），则报错
    """
    errors = []

    # 可豁免的固定值（业务必需场景）
    reasonable_fixed = {
        # 协议 Magic Number
        "0x52494646",  # RIFF
        "0x12345678",  # 示例 Magic Number
        # 常见文件/协议头
        "0x504B0304",  # ZIP
        "0x89504E47",  # PNG
        "0xFFD8FF",  # JPEG
        # 版本号
        "1",
        "2",
        "3",
        "4",
        "5",
        # 布尔开关
        "true",
        "false",
        # 常见标志位掩码
        "0xFF",
        "0xFFFF",
        "0xFFFFFFFF",
        "0x00",
        "0x01",
        "0x02",
    }

    # 找到所有函数定义
    func_pattern = r"(?:void|bool|int|uint32_t|int32_t|size_t)\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)"

    for func_match in re.finditer(func_pattern, content):
        func_name = func_match.group(1)
        func_start = func_match.end()

        # 找到函数体（匹配大括号）
        brace_count = 0
        func_body_start = -1
        for i in range(func_start, len(content)):
            if content[i] == "{":
                brace_count += 1
                if brace_count == 1:
                    func_body_start = i + 1
            elif content[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    func_body = content[func_body_start:i]
                    break
        else:
            continue

        if func_body_start == -1:
            continue

        # 在函数体内查找所有变量赋值
        # 1. 查找 fdp.Consume 调用（变异数据）
        consume_calls = re.findall(r"\w+\s*=\s*fdp\.Consume\w+", func_body)

        # 2. 查找固定数字赋值（排除循环变量和const）
        fixed_assignments = []

        # 匹配: type var = value;
        assignment_patterns = [
            r"(?:uint32_t|int32_t|uint8_t|int8_t|uint16_t|int16_t|size_t|int|unsigned)\s+(\w+)\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*;",
            r"(\w+)\s*=\s*(0x[0-9A-Fa-f]{4,}|\d{4,})\s*;",
        ]

        for pattern in assignment_patterns:
            for var_match in re.finditer(pattern, func_body):
                var_name = var_match.group(1)
                value = var_match.group(2)

                # 排除 for 循环变量和 const 定义
                if re.search(rf"for\s*\([^)]*{re.escape(var_name)}[^)]*\)", func_body):
                    continue
                if re.search(rf"const\s+\w+\s+{re.escape(var_name)}", func_body):
                    continue

                fixed_assignments.append((var_name, value))

        # 3. 查找字符串固定值
        string_assignments = re.findall(r'\w+\s*=\s*"([^"]{4,})"\s*;', func_body)

        # 4. 查找 bool 固定值
        bool_assignments = re.findall(r"\w+\s*=\s*(true|false)\s*;", func_body)

        # 判断逻辑:
        # A. 如果没有任何 Consume 调用，且存在固定赋值，则所有参数都是固定的
        if len(consume_calls) == 0 and (
            len(fixed_assignments) > 0
            or len(string_assignments) > 0
            or len(bool_assignments) > 0
        ):
            errors.append(
                f"[规则14] 函数 '{func_name}' 中所有参数都使用固定值，未使用 fdp.Consume*() 获取变异数据"
            )
            continue

        # B. 如果有 Consume 调用，检查不合理的固定值
        unreasonable_count = 0
        unreasonable_details = []

        for var_name, value in fixed_assignments:
            if value not in reasonable_fixed:
                unreasonable_count += 1
                unreasonable_details.append(f"{var_name}={value}")

        unreasonable_count += len(string_assignments)
        unreasonable_count += len(bool_assignments)

        # 如果存在多个不合理的固定值（>2），则报错
        # 允许 1-2 个固定值（如 Magic Number + 版本号）
        if unreasonable_count > 2:
            errors.append(
                f"[规则14] 函数 '{func_name}' 中存在 {unreasonable_count} 个不合理的固定参数"
            )

    # 如果按函数检测没有结果，使用原来的全局检测作为后备
    if not errors:
        # 全局检测：查找明显的问题模式
        # 1. 检查字符串固定参数
        fixed_strings = re.findall(
            r'\w+\s*=\s*"([^"]{4,})"\s*;',
            content,
        )
        # 排除空字符串和常见格式字符串
        unreasonable_strs = [s for s in fixed_strings if s not in ("", " ", "\n")]

        # 2. 检查 bool 固定参数
        fixed_bools = re.findall(
            r"\w+\s*=\s*(true|false)\s*;",
            content,
        )

        total_unreasonable = len(unreasonable_strs) + len(fixed_bools)

        if total_unreasonable > 3:
            details = []
            if unreasonable_strs:
                details.append(f"{len(unreasonable_strs)} 个字符串固定值")
            if fixed_bools:
                details.append(f"{len(fixed_bools)} 个布尔固定值")

            errors.append(
                f"规则014[高危]: 发现 {total_unreasonable} 个可疑固定参数（{'，'.join(details)}），"
                f"fuzz 测试应使用变异数据构造参数以增加覆盖率（固定值仅在 API版本号、Magic Number 等业务必需场景可豁免）"
            )

    return errors


def check_fuzzed_data_usage(content):
    """
    规则003: 检查是否使用了变异数据
    必须在 LLVMFuzzerTestOneInput 或 DoXXX 函数中使用 fdp.ConsumeXxx 提取数据
    """
    errors = []

    # 1. 检查文件级别是否有 fdp.Consume
    if not re.search(r"fdp\.Consume", content):
        if re.search(r"LLVMFuzzerTestOneInput", content):
            errors.append(
                "规则003[高危]: 未使用 FuzzedDataProvider 提取变异数据，"
                "fuzz 测试必须通过 fdp.ConsumeXxx() 从变异数据中提取参数"
            )
        return errors

    # 2. 检查每个 DoXXX 函数内部是否使用了 fdp.Consume
    do_functions = re.findall(
        r"\bvoid\s+(Do\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{",
        content,
    )

    for func_name in do_functions:
        # 找到函数体
        func_match = re.search(
            rf"\bvoid\s+{re.escape(func_name)}\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{{",
            content,
        )
        if func_match:
            start = func_match.end() - 1
            body = _extract_fuzzer_func_body(content, func_name, start)

            # 检查函数体是否有 fdp.Consume
            if not re.search(r"fdp\.Consume", body):
                errors.append(
                    f"规则003[高危]: {func_name}() 函数未使用 fdp.ConsumeXxx() 提取变异数据，"
                    f"属于无参数或固定参数调用，不适合 FUZZ 测试"
                )

    # 3. 检查 LLVMFuzzerTestOneInput 函数内部是否使用了 fdp.Consume
    llvm_match = re.search(
        r"extern\s+\"C\"\s+int\s+LLVMFuzzerTestOneInput\s*\([^)]*\)\s*\{",
        content,
    )
    if llvm_match:
        start = llvm_match.end() - 1
        body = _extract_fuzzer_func_body(content, "LLVMFuzzerTestOneInput", start)

        # 检查是否有 fdp.Consume
        if not re.search(r"fdp\.Consume", body):
            # 检查是否有 FuzzedDataProvider 定义
            if re.search(r"FuzzedDataProvider\s+\w+", body):
                errors.append(
                    "规则003[高危]: LLVMFuzzerTestOneInput() 中定义了 FuzzedDataProvider 但未使用 fdp.ConsumeXxx() 提取数据"
                )

    return errors


def check_random_usage(content):
    """
    规则017: 检查是否使用不可重现的随机数生成
    fuzz测试必须使用FuzzedDataProvider提供的数据，确保可重现性
    """
    errors = []

    # 只在 LLVMFuzzerTestOneInput 函数内检查
    if "LLVMFuzzerTestOneInput" not in content:
        return errors

    # 过滤掉注释和字符串字面量中的匹配
    # 简单方法：移除 // 注释和 "..." 字符串
    filtered_content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
    filtered_content = re.sub(r'"(?:[^"\\]|\\.)*"', ' "" ', filtered_content)

    # 检查 C 风格随机函数
    if re.search(r"\brand\s*\(\)|\brandom\s*\(\)|\bsrand\s*\(", filtered_content):
        errors.append(
            "规则017[高危]: 发现使用 rand()/random()/srand()，这些函数不可重现且不受 fuzz 引擎控制，"
            "应使用 fdp.ConsumeIntegral() 等方法"
        )

    # 检查 C++ 风格随机库
    if re.search(r"std::random_device|std::mt19937|std::uniform_", filtered_content):
        errors.append(
            "规则017[高危]: 发现使用 std::random_device/mt19937，应使用 FuzzedDataProvider 提供的 Consume 方法"
        )

    # 检查其他随机源
    if re.search(
        r"\bgetrandom\s*\(|\barc4random\s*\(|\b/dev/urandom", filtered_content
    ):
        errors.append(
            "规则017[高危]: 发现使用系统随机源(getrandom/arc4random/urandom)，"
            "fuzz 测试必须使用 FuzzedDataProvider 以确保可重现性"
        )

    return errors


def _get_target_class(content):
    """从代码中推断被测试的目标类名"""
    m = (
        re.search(r"std::make_shared<(\w+)>", content)
        or re.search(r"(\w+)::GetInstance\(\)", content)
        or re.search(r"(\w+)::Create\(\)", content)
        or re.search(r"(\w+)\*\s+g_\w+\s*=\s*nullptr", content)
    )
    return m.group(1) if m else None


def check_complex_params(content):
    """
    规则005: 检查复杂参数是否合理构造
    - 不能传 nullptr 或空对象
    - 必须用 fdp 填充字段
    - 必须构造有意义的对象
    - 输出参数（由函数内部赋值的指针/引用参数）可以初始化为0/nullptr
    """
    errors = []

    # 排除的类型（不需要fdp填充的类型）
    SKIP_TYPES = {
        "FuzzedDataProvider",
        "std::string",
        "std::vector",
        "std::map",
        "std::set",
        "std::list",
        "std::shared_ptr",
        "std::unique_ptr",
        "MessageParcel",
        "MessageOption",
        "uint8_t",
        "uint16_t",
        "uint32_t",
        "uint64_t",
        "int8_t",
        "int16_t",
        "int32_t",
        "int64_t",
        "int",
        "bool",
        "char",
        "size_t",
        "float",
        "double",
        "void",
        "std::thread",
        "std::mutex",
        "std::lock_guard",
    }

    # 1. 检查智能指针（shared_ptr/unique_ptr/sptr）直接赋值为 nullptr
    # 优化：增加对sptr等自定义智能指针的检测
    smart_ptr_nullptr = re.findall(
        r"(std::shared_ptr<[^>]+>|std::unique_ptr<[^>]+>|\bsptr<[^>]+>|\bRefBase<[^>]+>)\s+(\w+)\s*=\s*nullptr\s*;",
        content,
    )
    for ptr_type, var_name in smart_ptr_nullptr:
        # 检查是否在后续代码中构造了有效对象（如 new 或 make_shared）
        has_construction = re.search(
            rf"\b{re.escape(var_name)}\s*=\s*(?:std::)?(?:make_shared|make_unique|new)\b",
            content,
        )
        # 检查是否是输出参数（初始化为nullptr，在API调用中被赋值）
        is_output = _is_output_param(var_name, content)

        if not has_construction and not is_output:
            errors.append(
                f"规则005[高危]: 智能指针 {var_name}（{ptr_type}）赋值为 nullptr 且未构造有效对象，"
                f"nullptr 会被业务前置校验拦截，应使用 make_shared/make_unique/new 构造有效对象"
            )

    # 2. 检查将 nullptr 作为回调（更宽泛的匹配）
    callback_nullptr = re.findall(
        r"(\w+)\s*=\s*nullptr\s*;",
        content,
    )
    for var_name in callback_nullptr:
        if re.search(
            rf"(?:\w+\s*->\s*\w+|(?:Set|Register|Add|Bind)\w+)\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)",
            content,
        ):
            if not re.search(
                rf"std::(?:shared_ptr|unique_ptr)<[^>]+>\s+{re.escape(var_name)}\b",
                content,
            ):
                errors.append(
                    f"规则005[高危]: 变量 {var_name} 为 nullptr 并传给接口，"
                    f"应构造有效的对象（如 lambda、函数对象等）"
                )

    # 3. 检查 make_shared/make_unique 无参构造（未从 fdp 获取参数）
    target_class = _get_target_class(content)
    make_empty = re.findall(
        r"(?:std::)?(?:make_shared|make_unique)<(\w+)>\s*\(\s*\)", content
    )
    for cls in make_empty:
        if cls == target_class:
            continue
        if not re.search(
            rf"(?:std::)?(?:make_shared|make_unique)<{re.escape(cls)}>\s*\([^)]*fdp\.",
            content,
        ):
            errors.append(
                f"规则005[高危]: make_shared/make_unique<{cls}>() 无参构造，"
                f"应从 FuzzedDataProvider 获取构造参数"
            )

    # 4. 检查结构体/类默认构造（无字段填充）
    # 按函数逐个检查，排除输出参数
    func_pattern = re.compile(
        r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider\s*&\s*\w+\s*\)\s*\{"
    )

    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        struct_patterns = re.findall(r"(\w+)\s+(\w+)\s*;", body)

        for struct_type, var_name in struct_patterns:
            if struct_type in SKIP_TYPES:
                continue
            if not re.match(r"^[A-Z][a-zA-Z0-9_]*$", struct_type):
                continue

            # 排除被赋值初始化的情况
            if re.search(
                rf"\b{re.escape(struct_type)}\s+{re.escape(var_name)}\s*=\s*fdp\.", body
            ):
                continue
            if re.search(
                rf"\b{re.escape(struct_type)}\s+{re.escape(var_name)}\s*\{{\s*fdp\.",
                body,
            ):
                continue

            # 检查是否是输出参数
            is_output_param = False
            init_pattern = (
                rf"\b{re.escape(struct_type)}\s+{re.escape(var_name)}\s*=\s*(0|nullptr)"
            )
            if re.search(init_pattern, body):
                api_call_pattern = (
                    rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)"
                )
                if re.search(api_call_pattern, body):
                    is_output_param = True

            has_fdp_fill = re.search(
                rf"{re.escape(var_name)}\.\w+\s*\(\s*fdp\.", body
            ) or re.search(rf"{re.escape(var_name)}\.\w+\s*=\s*fdp\.", body)

            if not has_fdp_fill and not is_output_param:
                errors.append(
                    f"规则005[高危]: 函数 {func_name}() 中结构体/类 {struct_type} 的变量 {var_name} "
                    f"默认构造后未用 fdp 填充字段，会被业务前置校验拦截，"
                    f"应使用 fdp.ConsumeXxx() 填充每个字段"
                )

    # 5. 检查空容器构造（排除通过赋值初始化的容器和作为API参数的容器）
    # 按函数逐个检查
    for func_match in func_pattern.finditer(content):
        func_name = func_match.group(1)
        start = func_match.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        # 查找函数体内的容器声明
        empty_containers = re.findall(
            r"(std::vector<[^>]+>|std::list<[^>]+>|std::map<[^>]+>)\s+(\w+)\s*;",
            body,
        )

        for container_type, var_name in empty_containers:
            # 排除通过 fdp 赋值初始化的（如 auto data = fdp.ConsumeBytes...）
            if re.search(rf"\b{re.escape(var_name)}\s*=\s*fdp\.Consume", body):
                continue

            # 检查是否有填充操作
            has_fill_ops = re.search(
                rf"{re.escape(var_name)}\.(?:push_back|emplace_back|emplace|insert|append|resize)\s*\(",
                body,
            )

            if has_fill_ops:
                continue  # 有填充操作，不报错

            # 检查是否被传给API（作为输入或输出参数）
            # 如果被传给API，我们不报错，因为API可能会填充它
            is_api_param = re.search(
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var_name)}\b[^)]*\)", body
            )

            if is_api_param:
                continue  # 作为API参数，不报错

            # 如果没有填充操作，且没有被传给API，则报错
            errors.append(
                f"规则005[高危]: 函数 {func_name}() 中容器 {container_type} 的变量 {var_name} 为空容器，"
                f"会被业务前置校验拦截或走空逻辑分支，应使用 fdp 填充元素"
            )

    # 6. 检查 C 风格指针传 nullptr
    if re.search(r"\w+\s*\*\s*\w+\s*=\s*nullptr\s*;", content):
        null_ptr_vars = re.findall(r"\w+\s*\*(\w+)\s*=\s*nullptr\s*;", content)
        for var in null_ptr_vars:
            if re.search(
                rf"\w+\s*->\s*\w+\s*\([^)]*\b{re.escape(var)}\b[^)]*\)", content
            ):
                errors.append(
                    f"规则005[高危]: C 风格指针 {var} 为 nullptr 并传给接口，"
                    f"会被业务前置校验拦截，应分配有效内存并填充数据"
                )

    return errors


def check_reused_data(content):
    """
    规则004: 检查在同一个函数体内，从fdp提取的变量是否被重复用于多个接口调用。

    优化：排除switch-case模式中的变量复用（这是正常的分发模式）

    问题场景：
    - 同一个变量被传给多个不同的方法
    - 同一组变量被重复用于多个业务调用
    """
    errors = []

    # 匹配所有函数（包括 DoXXX 和 LLVMFuzzerTestOneInput）
    pattern = re.compile(r"\b(?:void|extern\s+\"C\"\s+int)\s+(\w+)\s*\([^)]*\)\s*\{")

    for m in pattern.finditer(content):
        func_name = m.group(1)
        start = m.end() - 1
        body = _extract_fuzzer_func_body(content, func_name, start)

        # 跳过没有 fdp 使用的函数
        if not re.search(r"fdp\.", body):
            continue

        # 优化：排除switch-case模式
        # switch-case模式是正常的分发模式，变量在不同case中使用是合理的
        if re.search(r"\bswitch\s*\(", body):
            # 进一步检查：如果变量只在单个case中使用，不报错
            # 提取所有case块
            case_blocks = re.findall(
                r"case\s+\w+\s*:\s*(.*?)\s*(?:break\s*;|return\s+|case\s+|default\s*:|\})",
                body,
                re.DOTALL,
            )
            if case_blocks:
                # 如果函数体主要是switch-case结构，跳过检查
                switch_ratio = (
                    len("".join(case_blocks)) / len(body) if len(body) > 0 else 0
                )
                if switch_ratio > 0.5:
                    continue

        # 提取所有变量定义（从 fdp 提取的）
        # 匹配模式: Type var = fdp.ConsumeXxx(...)
        var_pattern = re.compile(
            r"(?:const\s+)?(?:[\w:]+\s+)?(?:\*?\s*)?(\w+)\s*=\s*fdp\.(Consume\w+)"
        )

        # 记录每个变量被哪些方法调用
        var_usage = {}

        # 先找到所有从fdp提取的变量
        for var_match in var_pattern.finditer(body):
            var_name = var_match.group(1)
            if var_name not in var_usage:
                var_usage[var_name] = {
                    "consume_type": var_match.group(2),
                    "methods": [],
                }

        # 再检查每个变量在哪些方法调用中被使用
        # 匹配 g_instance->Method(...) 或 obj.Method(...) 等调用
        method_call_pattern = re.compile(r"(?:g_\w+|\w+)\s*->\s*(\w+)\s*\([^)]*\)")

        for call_match in method_call_pattern.finditer(body):
            method_name = call_match.group(1)
            call_start = call_match.start()
            call_end = call_match.end()
            call_body = body[call_start:call_end]

            # 检查这个调用中使用了哪些fdp变量
            for var_name in var_usage:
                # 简单检查变量名是否出现在调用中
                # 使用单词边界匹配，避免部分匹配
                if re.search(rf"\b{re.escape(var_name)}\b", call_body):
                    if method_name not in var_usage[var_name]["methods"]:
                        var_usage[var_name]["methods"].append(method_name)

        # 排除在同一个函数中多次调用同一方法的情况（如getter/setter对）
        # 只保留真正被用于不同方法的变量
        filtered_reused = {}
        for var_name, info in var_usage.items():
            if len(info["methods"]) >= 2:
                # 检查是否是getter/setter模式
                methods = info["methods"]
                is_getter_setter = False
                for i, m1 in enumerate(methods):
                    for m2 in methods[i + 1 :]:
                        # 检查是否是GetXxx/SetXxx模式
                        if (m1.startswith("Get") and m2 == "Set" + m1[3:]) or (
                            m2.startswith("Get") and m1 == "Set" + m2[3:]
                        ):
                            is_getter_setter = True
                            break
                    if is_getter_setter:
                        break

                if not is_getter_setter:
                    filtered_reused[var_name] = info

        # 检查是否有变量被用于多个不同的方法
        reused_vars = []
        for var_name, info in filtered_reused.items():
            reused_vars.append({"var": var_name, "methods": info["methods"]})

        if reused_vars:
            details = []
            for rv in reused_vars:
                details.append(f"变量 '{rv['var']}' 被用于: {', '.join(rv['methods'])}")

            errors.append(
                f"规则004[中危]: {func_name}() 中发现 {len(reused_vars)} 个变异数据变量被重复用于多个接口调用，"
                f"会降低 fuzz 覆盖率和数据变异性。详情: {'; '.join(details)}"
            )

    return errors


def check_intermediate_products(content):
    """
    规则015: 检查中间产物是否由合法流程生成

    检测以下模式：
    1. 成对的编解码/序列化/加密/打包函数调用
    2. 使用固定值构造参数（如分辨率、刷新率等常见屏幕参数）
    3. 使用合法流程生成数据后再调用被测接口
    """
    errors = []

    # 1. 检测成对的编解码/序列化/加密/打包函数
    # 模式: Encode/Decode, Serialize/Deserialize, Encrypt/Decrypt, Pack/Unpack, ToJson/FromJson
    paired_patterns = [
        (r"[Ee]ncode\w*\s*\(", r"[Dd]ecode\w*\s*\(", "编解码"),
        (
            r"[Ss]erializ\w*\s*\(",
            r"[Dd]eserializ\w*\s*\(",
            "序列化/反序列化",
        ),
        (r"[Ee]ncrypt\w*\s*\(", r"[Dd]ecrypt\w*\s*\(", "加密/解密"),
        (r"[Pp]ack\w*\s*\(", r"[Uu]npack\w*\s*\(", "打包/解包"),
        (r"[Tt]o[Jj]son\s*\(", r"[Ff]rom[Jj]son\s*\(", "JSON序列化/反序列化"),
        (r"[Tt]o[Ss]tring\s*\(", r"[Ff]rom[Ss]tring\s*\(", "字符串序列化/反序列化"),
    ]

    for encode_pattern, decode_pattern, desc in paired_patterns:
        encode_matches = list(re.finditer(encode_pattern, content))
        decode_matches = list(re.finditer(decode_pattern, content))

        if encode_matches and decode_matches:
            # 检查是否在同一个函数内
            for enc_match in encode_matches:
                enc_line = content[: enc_match.start()].count("\n") + 1
                # 找到包含这个调用的函数
                func_start = content.rfind("void ", 0, enc_match.start())
                if func_start == -1:
                    func_start = content.rfind('extern "C" ', 0, enc_match.start())

                if func_start != -1:
                    func_name_match = re.search(
                        r"\b(\w+)\s*\(", content[func_start : enc_match.start()]
                    )
                    if func_name_match:
                        func_name = func_name_match.group(1)
                        # 检查同一个函数内是否有对应的decode
                        func_end = content.find("\n}", enc_match.start())
                        if func_end == -1:
                            func_end = len(content)
                        func_body = content[enc_match.start() : func_end]

                        if re.search(decode_pattern, func_body):
                            errors.append(
                                f"规则015[高危]: 函数 '{func_name}' 中检测到{desc}成对调用，"
                                f"中间产物经由合法流程生成，会过滤掉变异数据中的异常值，"
                                f"建议直接使用变异数据测试被测接口"
                            )
                            break

    # 2. 检测使用固定值构造屏幕参数
    # 常见的屏幕参数固定值
    # 注意：这些值也可能用于其他场景（如缓冲区大小），需要结合上下文判断
    screen_params_patterns = [
        (r"uint32_t\s+\w+\s*=\s*(1920|1080|720|480|2560|1440|3840|2160)\s*;", "分辨率"),
        (r"uint32_t\s+\w+\s*=\s*(60|120|144|240|30)\s*;", "刷新率"),
        (r"uint32_t\s+\w+\s*=\s*(24|32|16|8)\s*;", "位深/颜色格式"),
    ]

    for pattern, param_type in screen_params_patterns:
        matches = list(re.finditer(pattern, content))
        if len(matches) >= 2:  # 至少有两个固定参数
            # 检查是否在同一个函数内，且函数名或变量名暗示屏幕相关
            func_names = set()
            for match in matches:
                # 获取变量名
                var_match = re.search(r"uint32_t\s+(\w+)\s*=", match.group(0))
                var_name = var_match.group(1) if var_match else ""

                # 检查变量名或附近代码是否暗示屏幕/显示相关
                nearby = content[max(0, match.start() - 100) : match.end() + 100]
                screen_context = re.search(
                    r"\b(screen|display|resolution|width|height|refresh|fps|bpp|pixel|color)\b",
                    nearby,
                    re.IGNORECASE,
                )

                # 只有上下文暗示屏幕相关时才报告
                if screen_context or re.search(
                    r"\b(w|h|width|height|refresh|rate)\b", var_name, re.IGNORECASE
                ):
                    func_start = content.rfind("void ", 0, match.start())
                    if func_start != -1:
                        func_name_match = re.search(
                            r"\b(\w+)\s*\(", content[func_start : match.start()]
                        )
                        if func_name_match:
                            func_names.add(func_name_match.group(1))

            for func_name in func_names:
                errors.append(
                    f"规则015[高危]: 函数 '{func_name}' 中使用固定值构造{param_type}参数，"
                    f"无法测试内部对非法参数的处理，建议使用变异数据构造各种参数值"
                )

    # 3. 检测使用合法流程生成数据后再调用被测接口
    # 模式: 先调用某个生成函数，然后将结果传给被测接口
    generation_patterns = [
        r"\b(\w+)\s*=\s*(\w+)[Ee]ncode\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)[Ss]erializ\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)[Ee]ncrypt\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)[Pp]ack\w*\s*\(",
        r"\b(\w+)\s*=\s*(\w+)\.([Tt]o[Jj]son|[Tt]o[Ss]tring)\s*\(",
    ]

    for pattern in generation_patterns:
        for match in re.finditer(pattern, content):
            var_name = match.group(1)
            # 检查这个变量是否被传给被测接口
            # 查找 g_instance->Method(var_name) 或 obj.Method(var_name) 等调用
            usage_pattern = (
                rf"(?:g_\w+|\w+)\s*->\s*\w+\s*\([^)]*{re.escape(var_name)}[^)]*\)"
            )
            if re.search(usage_pattern, content[match.end() : match.end() + 500]):
                func_start = content.rfind("void ", 0, match.start())
                if func_start != -1:
                    func_name_match = re.search(
                        r"\b(\w+)\s*\(", content[func_start : match.start()]
                    )
                    if func_name_match:
                        func_name = func_name_match.group(1)
                        errors.append(
                            f"规则015[高危]: 函数 '{func_name}' 中先通过合法流程生成数据，"
                            f"再传给被测接口，建议直接使用变异数据"
                        )

    return errors


def check_file_format_rules(filepath, content):
    errors = []
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))

    if filename.endswith(".h"):
        errors.extend(check_header_file(filename, dirname, content))
    elif filename == "BUILD.gn":
        errors.extend(check_build_gn(content))
    elif filename.endswith(".cpp"):
        errors.extend(check_cpp_include(filename, content))

    return errors


def check_header_file(filename, dirname, content):
    errors = []
    # 定义必需的头文件组（C++风格和C风格都接受）
    required_header_groups = [
        ["<cstdint>", "<stdint.h>"],  # 整数类型
        ["<unistd.h>"],  # Unix标准（只有C风格）
        ["<climits>", "<limits.h>"],  # 限制宏
        ["<cstdio>", "<stdio.h>"],  # 标准IO
        ["<cstdlib>", "<stdlib.h>"],  # 标准库
        ["<fcntl.h>"],  # 文件控制（只有C风格）
    ]

    missing = []
    for header_group in required_header_groups:
        # 检查该组中是否有任何一个头文件被包含
        if not any(f"#include {h}" in content for h in header_group):
            # 如果没有，报告缺少该组的第一个（推荐）头文件
            missing.append(header_group[0])

    if missing:
        errors.append(f"规则A: 头文件缺少必需的系统头文件: {', '.join(missing)}")

    if not (
        re.search(r"#ifndef\s+\w+", content)
        and "#define" in content
        and "#endif" in content
    ):
        errors.append("规则A: 头文件缺少 #ifndef/#define/#endif 保护宏")

    fuzz_project_match = re.search(r'#define\s+FUZZ_PROJECT_NAME\s+"([^"]+)"', content)
    if not fuzz_project_match:
        errors.append("规则A: 头文件未定义 FUZZ_PROJECT_NAME 宏")
    else:
        project_name = fuzz_project_match.group(1)
        if project_name != dirname:
            errors.append(
                f"规则A: FUZZ_PROJECT_NAME '{project_name}' 与目录名 '{dirname}' 不一致"
            )
    return errors


def check_build_gn(content):
    errors = []
    target_name = None
    if "ohos_fuzztest(" not in content:
        if "ohos_fuzz_test(" in content:
            errors.append("规则B: 使用了旧版 ohos_fuzz_test()，应改为 ohos_fuzztest()")
        else:
            errors.append("规则B: BUILD.gn 必须使用 ohos_fuzztest() 模板")
    else:
        target_match = re.search(r'ohos_fuzztest\(\s*"([^"]+)"', content)
        if target_match:
            target_name = target_match.group(1)

    if "fuzz_config_file" not in content:
        if "fuzz_config" in content:
            errors.append("规则B: 使用了 fuzz_config，应改为 fuzz_config_file")
        else:
            errors.append("规则B: BUILD.gn 必须包含 fuzz_config_file 参数")
    else:
        config_match = re.search(r'fuzz_config_file\s*=\s*"([^"]+)"', content)
        if config_match:
            config_path = config_match.group(1)
            if not config_path.startswith("//"):
                errors.append("规则B: fuzz_config_file 路径必须以 // 开头")

    if 'group("fuzztest")' not in content:
        errors.append('规则B: BUILD.gn 必须包含 group("fuzztest") 部分')
    elif target_name:
        group_match = re.search(
            r'group\(\s*"fuzztest"\s*\)\s*\{([^}]*)\}', content, re.DOTALL
        )
        if group_match:
            group_body = group_match.group(1)
            # 更精确的匹配：deps = [":TargetName"] 或 deps += [":TargetName"]
            dep_pattern = rf'(?:deps\s*=\s*\[|deps\s*\+=\s*\[)[^\]]*":\s*{re.escape(target_name)}\s*"'
            if not re.search(dep_pattern, group_body):
                errors.append(
                    f'规则B: group("fuzztest") 中的 deps 应包含 ohos_fuzztest 目标名 "{target_name}"'
                )
    return errors


def check_cpp_include(filename, content):
    errors = []
    expected_header = filename.replace(".cpp", ".h")
    include_pattern = rf'#include\s+"{re.escape(expected_header)}"'
    if not re.search(include_pattern, content):
        # 检查是否有双引号包含的头文件
        quoted_includes = re.findall(r'#include\s+"([^"]+\.h)"', content)
        # 检查是否有尖括号包含的头文件（可能是自身头文件错误地使用了尖括号）
        angle_includes = re.findall(r"#include\s+<([^>]+\.h)>", content)

        if expected_header in angle_includes:
            errors.append(
                f"规则E: .cpp 文件使用了尖括号包含自身头文件 '<{expected_header}>'，应改为双引号 '#include \"{expected_header}\"'"
            )
        elif quoted_includes and expected_header not in quoted_includes:
            errors.append(
                f"规则E: .cpp 包含的头文件 '{quoted_includes[0]}' 与文件名 '{expected_header}' 不一致"
            )
        elif not quoted_includes and not angle_includes:
            errors.append(f"规则E: .cpp 文件未包含自身头文件 '{expected_header}'")
        elif not quoted_includes:
            errors.append(
                f"规则E: .cpp 文件未使用双引号包含自身头文件 '{expected_header}'"
            )

    system_headers = {
        "cstdint",
        "unistd.h",
        "climits",
        "cstdio",
        "cstdlib",
        "fcntl.h",
        "vector",
        "map",
        "set",
        "string",
        "memory",
        "functional",
        "algorithm",
        "array",
        "deque",
        "list",
        "queue",
        "stack",
        "tuple",
        "utility",
        "chrono",
        "thread",
        "mutex",
        "atomic",
        "condition_variable",
        "iostream",
        "fstream",
        "sstream",
        "iomanip",
        "iosfwd",
        "cmath",
        "complex",
        "numeric",
        "valarray",
        "cassert",
        "cerrno",
        "cfloat",
        "cinttypes",
        "climits",
        "clocale",
        "csignal",
        "cstdalign",
        "cstdarg",
        "cstdbool",
        "cstddef",
        "cstdint",
        "cstdio",
        "cstdlib",
        "cstring",
        "ctgmath",
        "ctime",
        "cuchar",
        "cwchar",
        "cwctype",
        "sys/types.h",
        "sys/stat.h",
        "sys/mman.h",
        "sys/socket.h",
        "netinet/in.h",
        "arpa/inet.h",
        "pthread.h",
        "dlfcn.h",
        "errno.h",
        "fcntl.h",
        "limits.h",
        "signal.h",
        "stdarg.h",
        "stddef.h",
        "stdint.h",
        "stdio.h",
        "stdlib.h",
        "string.h",
        "time.h",
        "unistd.h",
        "wchar.h",
        "wctype.h",
        "optional",
        "variant",
        "any",
        "string_view",
        "filesystem",
        "fuzzer/FuzzedDataProvider.h",
    }
    angle_bracket_includes = re.findall(r"#include\s*<([^>]+\.h)>", content)
    project_angle = [h for h in angle_bracket_includes if h not in system_headers]
    if project_angle:
        errors.append(
            f"规则E: 项目头文件应使用双引号包含而非尖括号，发现: <{', <'.join(project_angle)}>"
        )
    return errors


def check_seed_files(filepath, content):
    """
    规则008: 检查种子文件是否合理构造

    检测以下问题：
    1. corpus/ 目录是否存在
    2. corpus/ 目录是否为空
    3. 种子文件大小是否为0
    4. 种子文件格式是否与API类型匹配

    豁免场景：
    - 新生成的fuzzer（包含TODO注释或生成器标记）
    - 纯查询类API（无输入参数）
    """
    errors = []

    # 获取文件所在目录
    file_dir = os.path.dirname(filepath)
    corpus_dir = os.path.join(file_dir, "corpus")

    # 检查是否是新生成的fuzzer（包含TODO注释）
    # 新生成的fuzzer可能还没有种子文件，这是正常的
    if re.search(r"//\s*TODO|TODO:", content):
        # 新生成的fuzzer，跳过种子检查
        return errors

    # 检查是否是纯查询类API（无输入参数）
    # 如果没有使用fdp.Consume，说明是纯查询类API，不需要种子
    if not re.search(r"fdp\.Consume", content):
        return errors

    # 检查是否是新生成的fuzzer（文件创建时间在24小时内）
    # 新生成的fuzzer可能还没有种子文件，给予宽限期
    try:
        file_stat = os.stat(filepath)
        import time

        # 如果文件创建时间在24小时内，跳过检查
        if (time.time() - file_stat.st_ctime) < 24 * 3600:
            return errors
    except (OSError, AttributeError):
        pass

    # 检查是否是纯查询类API（无输入参数）
    # 如果没有使用fdp.Consume，说明是纯查询类API，不需要种子
    if not re.search(r"fdp\.Consume", content):
        return errors

    # 1. 检查 corpus/ 目录是否存在
    if not os.path.exists(corpus_dir):
        errors.append(
            "规则008[中危]: 未找到 corpus/ 目录，建议创建并放置合理的初始种子文件，"
            "可使用工具: python3 tools/seed_generator.py -t <type> -o corpus/init"
        )
        return errors

    # 2. 检查 corpus/ 目录是否为空
    if os.path.isdir(corpus_dir):
        seed_files = [
            f
            for f in os.listdir(corpus_dir)
            if os.path.isfile(os.path.join(corpus_dir, f))
        ]
        if not seed_files:
            errors.append(
                "规则008[中危]: corpus/ 目录为空，建议放置合理的初始种子文件，"
                "可使用工具: python3 tools/seed_generator.py -t <type> -o corpus/init"
            )
            return errors

        # 3. 检查种子文件大小
        for seed_file in seed_files:
            seed_path = os.path.join(corpus_dir, seed_file)
            file_size = os.path.getsize(seed_path)
            if file_size == 0:
                errors.append(
                    f"规则008[中危]: 种子文件 '{seed_file}' 大小为0，"
                    f"空文件无法提供有效的初始变异基础"
                )

        # 4. 检查种子文件格式是否与API类型匹配
        # 从文件名和API调用推断期望的种子类型
        api_types = infer_api_types(content)
        if api_types:
            for seed_file in seed_files:
                file_ext = os.path.splitext(seed_file)[1].lower()
                # 检查扩展名是否匹配
                if not is_seed_format_valid(file_ext, api_types):
                    errors.append(
                        f"规则008[中危]: 种子文件 '{seed_file}' 格式（{file_ext}）"
                        f"可能与API期望的输入类型（{', '.join(api_types)}）不匹配，"
                        f"建议使用: python3 tools/seed_generator.py 生成合适的种子"
                    )

    return errors


def infer_api_types(content):
    """
    从代码内容推断API期望的输入类型
    使用单词边界匹配，避免子字符串误匹配
    """
    api_types = set()

    # 图像处理相关API
    if re.search(r"\b(?:Decode|Encode|JPEG|PNG|Bitmap|Image)\b", content):
        # 排除纯文本处理（如 JSON/XML）的误匹配
        if not re.search(r"\b(?:Json|JSON|Xml|XML)\b", content):
            api_types.add("image")

    # JSON处理相关API
    if re.search(r"\b(?:Json|JSON|ParseJson|nlohmann::json)\b", content):
        api_types.add("json")

    # XML处理相关API
    if re.search(r"\b(?:Xml|XML|ParseXml|xml_parser)\b", content):
        api_types.add("xml")

    # 文本处理相关API
    # 排除 FuzzedDataProvider 自身的字符串消费方法（所有 fuzz 测试都会用）
    text_patterns = [
        r"\bstd::string\b",
        r"\bstring\b",
        r"\bParseString\b",
        r"\bText\b",
        r"\bStringData\b",
    ]
    for pattern in text_patterns:
        if re.search(pattern, content):
            api_types.add("text")
            break

    # 二进制数据处理
    if re.search(r"\bConsumeBytes\b", content):
        api_types.add("binary")

    # 协议/IPC相关API
    if re.search(
        r"\b(?:MessageParcel|Parcel|SendRequest|OnRemoteRequest|IPC|Binder)\b", content
    ):
        api_types.add("protocol")

    return api_types


def is_seed_format_valid(file_ext, api_types):
    """
    检查种子文件格式是否与API类型匹配
    """
    format_mapping = {
        ".jpg": ["image"],
        ".jpeg": ["image"],
        ".png": ["image"],
        ".gif": ["image"],
        ".bmp": ["image"],
        ".json": ["json"],
        ".xml": ["xml"],
        ".txt": ["text"],
        ".bin": ["binary", "protocol"],
        ".dat": ["binary", "protocol"],
        "": ["binary", "protocol"],  # 无扩展名
    }

    # 如果无法确定API类型，认为有效
    if not api_types:
        return True

    # 如果文件扩展名在映射中，检查是否匹配
    if file_ext in format_mapping:
        valid_types = format_mapping[file_ext]
        return any(api_type in valid_types for api_type in api_types)

    # 未知扩展名，认为可能有效
    return True


def check_directory_consistency(filepath):
    """
    规则D: 检查文件命名一致性
    - .cpp/.h 文件名应与目录名一致
    - 头文件中FUZZ_PROJECT_NAME应与目录名一致
    - 命名应符合 XxxXxx_fuzzer 格式

    注意: BUILD.gn中ohos_fuzztest目标名格式由规则G检查，不在本规则范围内
    """
    errors = []
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))

    def check_fuzzer_name_format(name):
        """检查fuzzer命名是否符合 XxxXxx_fuzzer 格式"""
        base_name = re.sub(r"\d+$", "", name)
        return bool(re.match(r"^[A-Z][a-zA-Z0-9]*_fuzzer$", base_name))

    # 检查目录名是否符合 XxxXxx_fuzzer 格式
    if not check_fuzzer_name_format(dirname):
        errors.append(
            f"规则D: 目录名 '{dirname}' 不符合命名规范，应为 XxxXxx_fuzzer 格式（驼峰式+下划线+fuzzer后缀）"
        )

    if filename.endswith((".cpp", ".h")):
        stem = os.path.splitext(filename)[0]
        if stem != dirname and not re.match(rf"^{re.escape(dirname)}\d*$", stem):
            errors.append(f"规则D: 文件名 '{filename}' 与目录名 '{dirname}' 不一致")
        # 检查文件名是否符合命名规范
        if not check_fuzzer_name_format(stem):
            errors.append(
                f"规则D: 文件名 '{filename}' 不符合命名规范，应为 XxxXxx_fuzzer 格式（驼峰式+下划线+fuzzer后缀）"
            )

    # 检查头文件中的FUZZ_PROJECT_NAME是否与目录名一致
    if filename.endswith(".h"):
        content = read_file(filepath) or ""
        fuzz_project_match = re.search(
            r'#define\s+FUZZ_PROJECT_NAME\s+"([^"]+)"', content
        )
        if fuzz_project_match:
            fuzz_project_name = fuzz_project_match.group(1)
            if fuzz_project_name != dirname:
                errors.append(
                    f"规则D: 头文件中 FUZZ_PROJECT_NAME '{fuzz_project_name}' 与目录名 '{dirname}' 不一致"
                )

    return errors


def check_fuzztest_target_name_format(target_name):
    """
    检查 ohos_fuzztest 目标名是否符合 XxxXxxFuzzTest 格式
    - 必须以 FuzzTest 结尾
    - 必须是驼峰式命名（不含下划线）
    """
    if not target_name.endswith("FuzzTest"):
        return False, f"目标名 '{target_name}' 不以 'FuzzTest' 结尾"

    # 去掉 FuzzTest 后缀，检查前缀是否为驼峰式
    prefix = target_name[:-8]  # 去掉 "FuzzTest"
    if not prefix:
        return False, f"目标名 '{target_name}' 前缀为空"

    # 检查是否包含下划线（驼峰式不应包含下划线）
    if "_" in prefix:
        return False, f"目标名 '{target_name}' 包含下划线，应为驼峰式命名"

    # 检查首字母是否大写
    if not prefix[0].isupper():
        return False, f"目标名 '{target_name}' 首字母应大写"

    # 检查是否只包含字母和数字
    if not re.match(r"^[A-Za-z][A-Za-z0-9]*$", prefix):
        return False, f"目标名 '{target_name}' 前缀应只包含字母和数字"

    return True, None


def check_build_gn_target_name(filepath):
    """
    规则G: 检查 BUILD.gn 中 ohos_fuzztest 目标名格式
    - 目标名必须以 FuzzTest 结尾
    - 目标名必须为驼峰式命名
    - group("fuzztest") 中的 deps 必须引用正确的目标名
    """
    errors = []
    filename = os.path.basename(filepath)

    if filename != "BUILD.gn":
        return errors

    content = read_file(filepath) or ""

    # 检查 ohos_fuzztest 目标名
    target_matches = re.findall(r'ohos_fuzztest\("([^"]+)"\)', content)
    for target_name in target_matches:
        is_valid, error_msg = check_fuzztest_target_name_format(target_name)
        if not is_valid:
            errors.append(f"规则G: {error_msg}")

    # 检查 group("fuzztest") 中的 deps 是否引用了 ohos_fuzztest 目标名
    group_pattern = r'group\("fuzztest"\)\s*\{[^}]*deps\s*=\s*\[([^\]]*)\]'
    group_match = re.search(group_pattern, content, re.DOTALL)
    if group_match:
        deps_content = group_match.group(1)
        deps = re.findall(r'":([^"]+)"', deps_content)

        for dep in deps:
            is_valid, error_msg = check_fuzztest_target_name_format(dep)
            if not is_valid:
                errors.append(f'规则G: group("fuzztest") deps 中的 {error_msg}')

    return errors


def check_project_xml(filepath):
    errors = []
    if not os.path.exists(filepath):
        return errors

    content = read_file(filepath)
    if content is None:
        return [f"规则C: 无法读取 {filepath}"]

    # 检查XML声明，允许前导空白字符和BOM
    content_stripped = content.lstrip("\ufeff\t\n\r ")
    if not content_stripped.startswith('<?xml version="1.0" encoding="utf-8"?>'):
        errors.append(
            '规则C: project.xml 必须以 <?xml version="1.0" encoding="utf-8"?> 开头'
        )

    if "<fuzz_config>" not in content:
        errors.append("规则C: project.xml 根元素必须是 <fuzz_config>")

    if "<fuzztest>" not in content:
        errors.append("规则C: project.xml 必须包含 <fuzztest> 子元素")

    for config in ["max_len", "max_total_time", "rss_limit_mb"]:
        if f"<{config}>" not in content:
            errors.append(f"规则C: project.xml 缺少 {config} 配置项")
    return errors


def check_copyright(filepath, content):
    errors = []
    filename = os.path.basename(filepath)
    first_lines = "\n".join(content.splitlines()[:30])

    copyright_pattern = r"Copyright\s*\(\s*c\s*\)\s*(202[0-9]|2030)\s+Huawei\s+Device\s+Co\.?\s*,?\s*Ltd\.?"
    has_copyright = re.search(copyright_pattern, first_lines)

    # 检查 Apache License 2.0 声明
    # 要求包含 "Apache License, Version 2.0" 或完整的许可证声明
    apache_patterns = [
        r"Apache\s+License,\s+Version\s+2\.0",
        r"Licensed\s+under\s+the\s+Apache\s+License,\s+Version\s+2\.0",
        r"you\s+may\s+not\s+use\s+this\s+file\s+except\s+in\s+compliance\s+with\s+the\s+License",
    ]
    has_apache = any(re.search(p, first_lines, re.IGNORECASE) for p in apache_patterns)

    if filename.endswith((".cpp", ".h")):
        if not has_copyright:
            errors.append(
                "规则F: .cpp/.h 文件版权头不正确，必须包含 'Copyright (c) <year> Huawei Device Co., Ltd.'（年份应为 2020-2030 的实际年份）"
            )
        if not has_apache:
            errors.append("规则F: .cpp/.h 文件缺少 Apache License 2.0 声明")
    elif filename == "BUILD.gn":
        if not has_copyright:
            errors.append(
                "规则F: BUILD.gn 版权头不正确，必须包含 '# Copyright (c) <year> Huawei Device Co., Ltd.'（年份应为 2020-2030 的实际年份）"
            )
        if not has_apache:
            errors.append("规则F: BUILD.gn 缺少 Apache License 2.0 声明")
    elif filename == "project.xml":
        if not has_copyright:
            errors.append(
                "规则F: project.xml 版权头不正确，必须包含 '<!-- Copyright (c) <year> Huawei Device Co., Ltd.'（年份应为 2020-2030 的实际年份）"
            )
        if not has_apache:
            errors.append("规则F: project.xml 缺少 Apache License 2.0 声明")
    return errors


def check_directory(directory):
    all_errors = {}
    checked_files = 0
    all_cpp_contents = {}  # 收集所有cpp文件内容用于项目级检查

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".cpp", ".h")) or file in ("BUILD.gn", "project.xml"):
                filepath = os.path.join(root, file)
                checked_files += 1
                try:
                    errors = check_fuzz_file(filepath)
                    if errors:
                        all_errors[filepath] = errors

                    # 收集cpp文件内容
                    if file.endswith(".cpp"):
                        content = read_file(filepath)
                        if content:
                            all_cpp_contents[filepath] = content

                except Exception as e:
                    all_errors[filepath] = [f"检查异常: {str(e)}"]

    # 项目级规则002检查：合并所有文件的覆盖率
    if all_cpp_contents:
        # 按目录分组（同一项目）
        project_groups = {}
        for filepath, content in all_cpp_contents.items():
            dir_path = os.path.dirname(filepath)
            if dir_path not in project_groups:
                project_groups[dir_path] = {}
            project_groups[dir_path][filepath] = content

        # 对每个项目进行规则002检查
        for project_dir, project_files in project_groups.items():
            # 选择第一个文件作为代表进行项目级检查
            first_file = list(project_files.keys())[0]
            first_content = project_files[first_file]

            try:
                project_errors = check_missing_api_coverage(
                    first_file, first_content, all_project_files=project_files
                )
                if project_errors:
                    # 将项目级错误添加到第一个文件
                    if first_file not in all_errors:
                        all_errors[first_file] = []
                    # 去重：避免重复添加相同的错误
                    for error in project_errors:
                        if error not in all_errors[first_file]:
                            all_errors[first_file].append(error)
            except Exception as e:
                pass  # 项目级检查失败不影响其他检查

    return all_errors, checked_files


def generate_report(all_errors, output_file=None, checked_files=0):
    lines = []
    lines.append("=" * 70)
    lines.append("FUZZ测试用例规范性检查报告")
    lines.append("=" * 70)
    lines.append("")

    total_errors = sum(len(errors) for errors in all_errors.values())
    total_files = len(all_errors)
    passed_files = checked_files - total_files

    lines.append(f"检查文件数: {checked_files}")
    lines.append(f"通过文件数: {passed_files}")
    lines.append(f"问题文件数: {total_files}")
    lines.append(f"发现问题数: {total_errors}")
    lines.append("")

    if not all_errors:
        lines.append("所有文件检查通过！")
    else:
        # 按规则分类统计
        rule_stats = {}
        for filepath, errors in all_errors.items():
            for error in errors:
                # 提取规则编号
                rule_match = re.search(r"规则(\w+)", error)
                if rule_match:
                    rule_num = rule_match.group(1)
                    if rule_num not in rule_stats:
                        rule_stats[rule_num] = 0
                    rule_stats[rule_num] += 1

        if rule_stats:
            lines.append("规则违规统计:")
            for rule_num, count in sorted(
                rule_stats.items(), key=lambda x: x[1], reverse=True
            ):
                lines.append(f"  规则{rule_num}: {count} 次")
            lines.append("")

        for filepath, errors in all_errors.items():
            lines.append("-" * 70)
            lines.append(f"文件: {filepath}")
            lines.append("-" * 70)
            for i, error in enumerate(errors, 1):
                lines.append(f"  {i}. {error}")
            lines.append("")

    report = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已保存到: {output_file}")

    return report


def fix_file(filepath, rules=None, dry_run=False):
    """
    自动修复可修复的规则问题
    支持规则: 017, 019, F
    """
    import re
    from datetime import datetime

    content = read_file(filepath)
    if content is None:
        return False, [f"错误: 无法读取文件 {filepath}"]

    original_content = content
    all_fixes = []

    # 规则017: 替换 rand()/random() 为 fdp 调用
    if rules is None or "017" in rules:
        if re.search(r"\brand\s*\(\s*\)", content):
            count = len(re.findall(r"\brand\s*\(\s*\)", content))
            content = re.sub(
                r"\brand\s*\(\s*\)", "fdp.ConsumeIntegral<uint32_t>()", content
            )
            all_fixes.append(
                f"规则017: 替换 {count} 处 rand() → fdp.ConsumeIntegral<uint32_t>()"
            )

        if re.search(r"\brandom\s*\(\s*\)", content):
            count = len(re.findall(r"\brandom\s*\(\s*\)", content))
            content = re.sub(
                r"\brandom\s*\(\s*\)", "fdp.ConsumeIntegral<uint32_t>()", content
            )
            all_fixes.append(
                f"规则017: 替换 {count} 处 random() → fdp.ConsumeIntegral<uint32_t>()"
            )

        if re.search(r"\bsrand\s*\(", content):
            count = len(re.findall(r"\bsrand\s*\([^)]*\)\s*;", content))
            content = re.sub(r"\bsrand\s*\([^)]*\)\s*;\s*\n?", "", content)
            all_fixes.append(f"规则017: 移除 {count} 处 srand() 调用")

    # 规则019: 添加全局指针初始化
    if rules is None or "019" in rules:
        global_ptrs = re.findall(r"(\w+)\*\s+(g_\w+)\s*=\s*nullptr\s*;", content)
        for ptr_type, var_name in global_ptrs:
            init_func = re.search(
                r"(extern\s+\"C\"\s+int\s+LLVMFuzzerInitialize\s*\([^)]*\)\s*\{)([^}]*(?:\{[^}]*\}[^}]*)*)(\})",
                content,
                re.DOTALL,
            )
            if not init_func:
                continue
            init_body = init_func.group(2)
            if re.search(rf"{re.escape(var_name)}\s*=", init_body):
                continue
            init_code = f"\n    // TODO: 添加 {var_name} 的初始化代码"
            new_body = re.sub(
                r"(\s+return\s+0\s*;)", init_code + r"\1", init_body, count=1
            )
            content = content.replace(init_body, new_body)
            all_fixes.append(f"规则019: 为全局指针 {var_name} 添加初始化代码")

    # 规则F: 添加/修正版权头
    if rules is None or "F" in rules:
        year = datetime.now().year
        has_copyright = re.search(r"Copyright\s+\(c\)\s+\d{4}", content, re.IGNORECASE)
        if not has_copyright:
            ext = os.path.splitext(filepath)[1]
            if ext in (".cpp", ".h"):
                copyright_header = f"""/*
 * Copyright (c) {year} Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

"""
                content = copyright_header + content
                all_fixes.append(f"规则F: 添加标准版权头 (Copyright {year})")
        else:
            old_year_match = re.search(
                r"Copyright\s+\(c\)\s+(\d{4})", content, re.IGNORECASE
            )
            if old_year_match:
                old_year = old_year_match.group(1)
                if old_year != str(year):
                    content = re.sub(
                        rf"Copyright\s+\(c\)\s+{old_year}",
                        f"Copyright (c) {year}",
                        content,
                    )
                    all_fixes.append(f"规则F: 更新版权年份 {old_year} → {year}")

    modified = content != original_content
    if modified and not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return modified, all_fixes


def main():
    parser = argparse.ArgumentParser(
        description="FUZZ测试用例规范性检查工具 v2.2 - 检查26条规则",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检查单个文件
  python3 fuzz_check.py path/to/XxxXxx_fuzzer.cpp

  # 检查目录
  python3 fuzz_check.py path/to/fuzztest/

  # 生成报告
  python3 fuzz_check.py path/to/fuzztest/ -o report.txt

  # 显示详细输出
  python3 fuzz_check.py path/to/fuzztest/ -v

  # 检查特定规则
  python3 fuzz_check.py path/to/fuzztest/ --rule 001,003,005

  # 自动修复问题（支持规则 017/019/F）
  python3 fuzz_check.py path/to/XxxXxx_fuzzer.cpp --fix
  python3 fuzz_check.py path/to/XxxXxx_fuzzer.cpp --fix --rules 017,F
  python3 fuzz_check.py path/to/XxxXxx_fuzzer.cpp --fix --dry-run
        """,
    )
    parser.add_argument("path", help="要检查的 .cpp/.h 文件或目录路径")
    parser.add_argument("-o", "--output", help="输出报告文件路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细输出")
    parser.add_argument("--version", action="version", version="%(prog)s 2.2")
    parser.add_argument("--rule", help="只检查指定规则（逗号分隔，如 001,003,005）")
    parser.add_argument(
        "--fix", action="store_true", help="自动修复可修复的规则问题（017/019/F）"
    )
    parser.add_argument("--rules", help="指定要修复的规则（逗号分隔，如 017,019,F）")
    parser.add_argument(
        "--dry-run", action="store_true", help="预览修复，不实际修改文件"
    )
    parser.add_argument(
        "--expected-methods",
        help="批量模式：逗号分隔的预期覆盖方法列表（用于规则002）",
    )

    args = parser.parse_args()

    # 处理自动修复模式
    if args.fix:
        if not os.path.isfile(args.path):
            print("错误: --fix 只支持单个文件")
            sys.exit(2)

        rules = None
        if args.rules:
            rules = [r.strip() for r in args.rules.split(",")]

        modified, fixes = fix_file(args.path, rules, args.dry_run)
        if fixes:
            prefix = "[DRY-RUN] " if args.dry_run else ""
            print(f"{prefix}修复结果:")
            for fix in fixes:
                print(f"  ✓ {fix}")
            if args.dry_run:
                print(f"\n预览完成: 发现 {len(fixes)} 处可修复问题")
            else:
                print(f"\n修复完成: 共修复 {len(fixes)} 处问题")
        else:
            print("未发现需要修复的问题")
        sys.exit(0)

    if os.path.isfile(args.path):
        try:
            errors = check_fuzz_file(args.path)

            # 批量模式：只有设置 expected-methods 时才过滤规则002
            if args.expected_methods and errors:
                expected = set(
                    m.strip() for m in args.expected_methods.split(",") if m.strip()
                )
                errors = [e for e in errors if "规则002" not in e]
                # 重新检查：当前文件应该覆盖的预期方法
                content = read_file(args.path)
                if content:
                    do_funcs = set(
                        re.findall(r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider", content)
                    )
                    covered = set()
                    for do_name in do_funcs:
                        if do_name.startswith("Do") and len(do_name) > 2:
                            covered.add(do_name[2:])
                        else:
                            covered.add(do_name)
                    missing = expected - covered
                    if missing:
                        errors.append(
                            f"规则002[高危]: 预期覆盖的 {len(expected)} 个接口中有 {len(missing)} 个未覆盖: "
                            f"{', '.join(sorted(missing))}"
                        )

            # 如果指定了规则，过滤结果
            if args.rule and errors:
                rule_nums = args.rule.split(",")
                errors = [e for e in errors if any(f"规则{r}" in e for r in rule_nums)]

            if errors:
                print(f"文件 '{args.path}' 发现 {len(errors)} 个问题:")
                for i, error in enumerate(errors, 1):
                    print(f"  {i}. {error}")
                sys.exit(1)
            else:
                print(f"文件 '{args.path}' 规范性检查通过")
                sys.exit(0)
        except Exception as e:
            print(f"检查文件 '{args.path}' 时发生错误: {e}")
            sys.exit(2)

    elif os.path.isdir(args.path):
        try:
            all_errors, checked_files = check_directory(args.path)

            # 如果指定了规则，过滤结果
            if args.rule and all_errors:
                rule_nums = args.rule.split(",")
                filtered_errors = {}
                for filepath, errors in all_errors.items():
                    filtered = [
                        e for e in errors if any(f"规则{r}" in e for r in rule_nums)
                    ]
                    if filtered:
                        filtered_errors[filepath] = filtered
                all_errors = filtered_errors

            if all_errors:
                report = generate_report(all_errors, args.output, checked_files)
                if args.verbose or not args.output:
                    print(report)
                print(
                    f"\n共检查 {checked_files} 个文件，发现 {sum(len(e) for e in all_errors.values())} 个问题，涉及 {len(all_errors)} 个文件"
                )
                sys.exit(1)
            else:
                report = generate_report(all_errors, args.output, checked_files)
                if args.verbose or not args.output:
                    print(report)
                print(f"目录 '{args.path}' 下共检查 {checked_files} 个文件，全部通过")
                sys.exit(0)
        except Exception as e:
            print(f"检查目录 '{args.path}' 时发生错误: {e}")
            sys.exit(2)
    else:
        print(f"错误: 路径 '{args.path}' 不存在")
        sys.exit(2)


if __name__ == "__main__":
    main()
