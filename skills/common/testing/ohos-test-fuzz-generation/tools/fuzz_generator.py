#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FUZZ测试用例快速生成工具
自动生成符合OpenHarmony规范的FUZZ测试用例文件
支持自动从头文件解析 public 有参方法
"""

import os
import re
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path


def _split_namespace(namespace):
    parts = namespace.replace(" ", "").split("::")
    return [p for p in parts if p]


def _build_namespace_open(parts):
    if parts[0] == "OHOS":
        inner_parts = parts[1:]
        result = "namespace OHOS {\n"
    else:
        inner_parts = parts
        result = ""
    for p in inner_parts:
        result += "namespace " + p + " {\n"
    return result


def _build_namespace_close(parts):
    if parts[0] == "OHOS":
        inner_parts = parts[1:]
    else:
        inner_parts = parts
    result = ""
    for p in reversed(inner_parts):
        result += "} // namespace " + p + "\n"
    if parts[0] == "OHOS":
        result += "} // namespace OHOS\n"
    return result


def _namespace_qualifier(parts):
    if parts[0] == "OHOS":
        return "::".join(parts) + "::"
    return "::".join(parts) + "::"


def _extract_ipc_code_count(header_path_str, target_class):
    """
    从 IPC 头文件的 protected enum 中提取 code 值数量。
    如 IVSyncConnection 的 enum { REQUEST_NEXT_VSYNC, ..., SET_NATIVE_DVSYNC_SWITCH } → 7
    """
    search_dirs = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
    ]
    resolved = _resolve_header_path(header_path_str, search_dirs)
    if not resolved or not os.path.isfile(resolved):
        return 0
    content = Path(resolved).read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"//[^\n]*", "", content)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
    pattern = r"enum\s*\{([^}]+)\}\s*;"
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        return 0
    body = m.group(1)
    items = [
        item.strip()
        for item in body.split(",")
        if item.strip() and not item.strip().startswith("//")
    ]
    return len(items)


# Fix Windows console encoding
if sys.platform == "win32":
    import locale

    if hasattr(locale, "_getdefaultlocale"):
        locale._getdefaultlocale = lambda *args: ["en_US", "utf8"]


# 导入增强版头文件解析器
try:
    from header_parser import parse_header_methods_enhanced

    USE_ENHANCED_PARSER = True
except ImportError:
    USE_ENHANCED_PARSER = False
    parse_header_methods_enhanced = None

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

INIT_MODE_SINGLETON = "singleton"
INIT_MODE_FACTORY = "factory"
INIT_MODE_NONE = "none"
VALID_INIT_MODES = [INIT_MODE_SINGLETON, INIT_MODE_FACTORY, INIT_MODE_NONE]

# 类型到 FuzzedDataProvider 消费代码的映射
# 类型到 FuzzedDataProvider 消费代码的映射
# 格式: {类型名: (C++显式类型, 消费代码)}
TYPE_CONSUMER_MAP = {
    "bool": ("bool", "fdp.ConsumeBool()"),
    "int8_t": ("int8_t", "fdp.ConsumeIntegral<int8_t>()"),
    "uint8_t": ("uint8_t", "fdp.ConsumeIntegral<uint8_t>()"),
    "int16_t": ("int16_t", "fdp.ConsumeIntegral<int16_t>()"),
    "uint16_t": ("uint16_t", "fdp.ConsumeIntegral<uint16_t>()"),
    "int32_t": ("int32_t", "fdp.ConsumeIntegral<int32_t>()"),
    "int": ("int32_t", "fdp.ConsumeIntegral<int32_t>()"),
    "uint32_t": ("uint32_t", "fdp.ConsumeIntegral<uint32_t>()"),
    "unsigned": ("uint32_t", "fdp.ConsumeIntegral<uint32_t>()"),
    "unsigned int": ("uint32_t", "fdp.ConsumeIntegral<uint32_t>()"),
    "int64_t": ("int64_t", "fdp.ConsumeIntegral<int64_t>()"),
    "long long": ("int64_t", "fdp.ConsumeIntegral<int64_t>()"),
    "uint64_t": ("uint64_t", "fdp.ConsumeIntegral<uint64_t>()"),
    "unsigned long long": ("uint64_t", "fdp.ConsumeIntegral<uint64_t>()"),
    "size_t": ("size_t", "fdp.ConsumeIntegral<size_t>()"),
    "float": ("float", "fdp.ConsumeFloatingPoint<float>()"),
    "double": ("double", "fdp.ConsumeFloatingPoint<double>()"),
    "std::string": ("std::string", "fdp.ConsumeRandomLengthString(256)"),
    "string": ("std::string", "fdp.ConsumeRandomLengthString(256)"),
    "std::u16string": ("std::u16string", "fdp.ConsumeRandomLengthString(256)"),
    "ScreenId": ("ScreenId", "fdp.ConsumeIntegral<uint64_t>()"),
    "NodeId": ("NodeId", "fdp.ConsumeIntegral<uint64_t>()"),
    "WindowId": ("WindowId", "fdp.ConsumeIntegral<uint64_t>()"),
    "DisplayId": ("DisplayId", "fdp.ConsumeIntegral<uint64_t>()"),
    "ProcessId": ("ProcessId", "fdp.ConsumeIntegral<uint32_t>()"),
    "UserId": ("UserId", "fdp.ConsumeIntegral<uint32_t>()"),
    "Uid": ("Uid", "fdp.ConsumeIntegral<uint32_t>()"),
    "Pid": ("Pid", "fdp.ConsumeIntegral<uint32_t>()"),
    "Handle": ("Handle", "fdp.ConsumeIntegral<uint64_t>()"),
    "Fd": ("Fd", "fdp.ConsumeIntegral<int32_t>()"),
}

# 枚举类型到 size 常量的映射（用于 static_cast + 取模限制范围）
ENUM_SIZE_MAP = {
    "ScreenPowerStatus": ("SCREEN_POWER_STATUS_SIZE", 11),
    "ScreenConstraintType": ("SCREEN_CONSTRAINT_TYPE_SIZE", 4),
    "ScreenColorGamut": ("SCREEN_COLOR_GAMUT_SIZE", 12),
    "ScreenGamutMap": ("SCREEN_GAMUT_MAP_SIZE", 4),
    "ScreenRotation": ("SCREEN_ROTATION_SIZE", 5),
    "RSScreenType": ("SCREEN_SCREEN_TYPE_SIZE", 4),
    "ScreenHDRFormat": ("SCREEN_HDR_FORMAT_SIZE", 8),
    "GraphicCM_ColorSpaceType": ("GRAPHIC_CM_COLOR_SPACE_TYPE_SIZE", 32),
    "ScreenScaleMode": ("SCREEN_SCALE_MODE_SIZE", 3),
    "GraphicPixelFormat": ("GRAPHIC_PIXEL_FORMAT_SIZE", 43),
    "ShaderEffectType": ("SHADER_EFFECT_TYPE_SIZE", 13),
    "TileMode": ("TILE_MODE_SIZE", 3),
    "DisplayManagerAgentType": ("DISPLAY_MANAGER_AGENT_TYPE_SIZE", 18),
    "StartingAppType": ("STARTING_APP_TYPE_SIZE", 4),
    "BackgroundType": ("BACKGROUND_TYPE_SIZE", 5),
    "LayerStateChange": ("LAYER_STATE_CHANGE_SIZE", 4),
    "GraphicDispPowerStatus": ("GRAPHIC_DISP_POWER_STATUS_SIZE", 6),
    "GraphicColorGamut": ("GRAPHIC_COLOR_GAMUT_SIZE", 8),
    "GraphicGamutMap": ("GRAPHIC_GAMUT_MAP_SIZE", 4),
    "GraphicTransformType": ("GRAPHIC_TRANSFORM_TYPE_SIZE", 6),
    "BufferQueueUsage": ("BUFFER_QUEUE_USAGE_SIZE", 4),
    "OHSurfaceSource": ("OH_SURFACE_SOURCE_SIZE", 4),
    "OHScalingMode": ("OH_SCALING_MODE_SIZE", 4),
    "OH_NativeBuffer_TransformType": ("OH_NATIVE_BUFFER_TRANSFORM_TYPE_SIZE", 17),
}

# 复杂类型的初始化代码生成（返回多行初始化字符串，直接插入函数体）
COMPLEX_TYPE_MAP = {
    "RSScreenModeInfo": lambda var_name: (
        f"RSScreenModeInfo {var_name};\n"
        f"{var_name}.SetScreenWidth(static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>()));\n"
        f"{var_name}.SetScreenHeight(static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>()));\n"
        f"{var_name}.SetScreenRefreshRate(fdp.ConsumeIntegral<uint32_t>());\n"
        f"{var_name}.SetScreenModeId(static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>()));"
    ),
    "RSVirtualScreenResolution": lambda var_name: (
        f"RSVirtualScreenResolution {var_name}(fdp.ConsumeIntegral<uint32_t>(), fdp.ConsumeIntegral<uint32_t>());"
    ),
    "RSScreenHDRCapability": lambda var_name: (
        f"RSScreenHDRCapability {var_name};\n"
        f"{var_name}.SetMaxLum(fdp.ConsumeFloatingPoint<float>());\n"
        f"{var_name}.SetMinLum(fdp.ConsumeFloatingPoint<float>());\n"
        f"{var_name}.SetMaxAverageLum(fdp.ConsumeFloatingPoint<float>());"
    ),
    "Rect": lambda var_name: (
        f"Rect {var_name}{{\n"
        f"static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>()),\n"
        f"static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>()),\n"
        f"static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>()),\n"
        f"static_cast<int32_t>(fdp.ConsumeIntegral<int32_t>())\n"
        f"}};"
    ),
    "sptr<Surface>": lambda var_name: (
        f"sptr<Surface> {var_name} = new Surface(); // TODO: verify constructor"
    ),
    "std::shared_ptr<Media::PixelMap>": lambda var_name: (
        f"std::shared_ptr<Media::PixelMap> {var_name} = std::make_shared<Media::PixelMap>(); // TODO: verify constructor"
    ),
    "std::vector<uint64_t>": lambda var_name: (
        f"std::vector<uint64_t> {var_name};\n"
        f"size_t {var_name}Len = fdp.ConsumeIntegral<uint8_t>() % 4;\n"
        f"for (size_t i = 0; i < {var_name}Len; i++) {{\n"
        f"    {var_name}.push_back(fdp.ConsumeIntegral<uint64_t>());\n"
        f"}}"
    ),
    "std::vector<uint8_t>": lambda var_name: (
        f"std::vector<uint8_t> {var_name};\n"
        f"size_t {var_name}Len = fdp.ConsumeIntegral<uint8_t>() % 32;\n"
        f"for (size_t i = 0; i < {var_name}Len; i++) {{\n"
        f"    {var_name}.push_back(fdp.ConsumeIntegral<uint8_t>());\n"
        f"}}"
    ),
    "std::vector<NodeId>": lambda var_name: (
        f"std::vector<NodeId> {var_name};\n"
        f"size_t {var_name}Len = fdp.ConsumeIntegral<uint8_t>() % 4;\n"
        f"for (size_t i = 0; i < {var_name}Len; i++) {{\n"
        f"    {var_name}.push_back(fdp.ConsumeIntegral<uint64_t>());\n"
        f"}}"
    ),
    "std::vector<ScreenHDRMetadataKey>": lambda var_name: (
        f"std::vector<ScreenHDRMetadataKey> {var_name};\n"
    ),
    "sptr<RSIScreenSupportedHdrFormatsCallback>": lambda var_name: (
        f"sptr<RSIScreenSupportedHdrFormatsCallback> {var_name};"
    ),
    "std::vector<std::pair<float, float>>": lambda var_name: (
        f"std::vector<std::pair<float, float>> {var_name};\n"
        f"size_t {var_name}Len = fdp.ConsumeIntegral<uint8_t>() % 8;\n"
        f"for (size_t i = 0; i < {var_name}Len; i++) {{\n"
        f"    {var_name}.push_back({{fdp.ConsumeFloatingPoint<float>(), fdp.ConsumeFloatingPoint<float>()}});\n"
        f"}}"
    ),
    "std::vector<std::shared_ptr<Geometry>>": lambda var_name: (
        f"std::vector<std::shared_ptr<Geometry>> {var_name};\n"
        f"size_t {var_name}Len = fdp.ConsumeIntegral<uint8_t>() % 4;\n"
        f"for (size_t i = 0; i < {var_name}Len; i++) {{\n"
        f"    {var_name}.push_back(nullptr);\n"
        f"}}"
    ),
    "std::function<void()>": lambda var_name: (
        f"std::function<void()> {var_name} = nullptr;"
    ),
    "std::function<void(NodeId, uint64_t)>": lambda var_name: (
        f"std::function<void(NodeId, uint64_t)> {var_name} = nullptr;"
    ),
    "std::function<void(uint64_t, LayerStateChange, uint64_t)>": lambda var_name: (
        f"std::function<void(uint64_t, LayerStateChange, uint64_t)> {var_name} = nullptr;"
    ),
    "std::shared_ptr<ImageFilter>": lambda var_name: (
        f"std::shared_ptr<ImageFilter> {var_name} = nullptr;"
    ),
    "std::shared_ptr<Geometry>": lambda var_name: (
        f"std::shared_ptr<Geometry> {var_name} = nullptr;"
    ),
}


def read_template(template_name):
    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        print(f"错误: 模板文件不存在: {template_path}")
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")


def _snake_case_const(name):
    """将方法名转为 DO_XXX 常量名"""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return "DO_" + s.upper()


def _do_func_name(name):
    """将方法名转为 DoXxx 函数名"""
    return "Do" + name[0].upper() + name[1:]


def _resolve_header_path(header_str, search_dirs):
    """
    header_str 可能是带引号的路径，如 "rosen/xxx.h"
    尝试在 search_dirs 中查找实际文件
    """
    path = header_str.strip().strip('"').strip("'")
    if os.path.isabs(path) and os.path.isfile(path):
        return path
    for base in search_dirs:
        candidate = Path(base) / path
        if candidate.is_file():
            return str(candidate)
        # 去掉可能的前缀，例如 foundation/graphic/...
        parts = Path(path).parts
        for i in range(len(parts)):
            candidate2 = Path(base) / Path(*parts[i:])
            if candidate2.is_file():
                return str(candidate2)
    return path


def parse_header_methods(header_path_str, target_class, include_no_params=False):
    """
    从头文件中解析 target_class 的 public 有参方法。
    返回 [(method_name, params_str, return_type)] 列表。

    优先使用增强版解析器，如果失败则回退到旧版解析器。
    """
    search_dirs = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path(__file__).parent.parent.parent,
        Path(__file__).parent.parent.parent.parent,
    ]
    resolved = _resolve_header_path(header_path_str, search_dirs)
    if not resolved or not os.path.isfile(resolved):
        return []

    # 优先使用增强版解析器
    if USE_ENHANCED_PARSER and parse_header_methods_enhanced is not None:
        try:
            methods = parse_header_methods_enhanced(
                resolved, target_class, include_no_params=include_no_params
            )
            if methods:
                return methods
            print("[INFO] 增强版解析器未找到方法，尝试旧版解析器...")
        except Exception as e:
            print(f"[WARN] 增强版解析器失败: {e}，尝试旧版解析器...")

    # 回退到旧版解析器
    content = Path(resolved).read_text(encoding="utf-8", errors="ignore")

    # 移除单行和多行注释
    content = re.sub(r"//[^\n]*", "", content)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # 找到类定义 body
    class_pattern = rf"\bclass\s+{re.escape(target_class)}\b.*?\{{"
    m = re.search(class_pattern, content)
    if not m:
        return []

    start = m.end() - 1  # 指向 {
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

    # 找到 public: 区域
    pub_match = re.search(r"\bpublic\s*:", class_body)
    if not pub_match:
        return []

    pub_start = pub_match.end()
    # public 区域到 protected/private/} 结束
    next_access = re.search(r"\b(protected|private)\s*:", class_body[pub_start:])
    if next_access:
        pub_body = class_body[pub_start : pub_start + next_access.start()]
    else:
        pub_body = class_body[pub_start:]

    methods = []
    # 匹配方法签名：可选 virtual/static/explicit/constexpr/inline，返回类型，方法名，参数列表，可选 const/override/final/noexcept，分号
    # 例子: virtual void Foo(int a) const = 0;
    pattern = re.compile(
        r"(?:virtual|static|explicit|constexpr|inline|consteval|constinit|\[\[.*?\]\]|\s)*"  # 修饰符
        r"(?P<ret>[~\w_:][\w\s_:<>,*&.]*?)\s+"  # 返回类型（尽量非贪婪）
        r"(?P<name>\w+)\s*\(\s*(?P<params>[^)]*)\s*\)\s*"  # 方法名和参数
        r"(?:const\s*)?(?:override\s*)?(?:final\s*)?(?:noexcept\s*)?(?:=\s*0\s*)?;"  # 后缀和分号
    )

    for match in pattern.finditer(pub_body):
        name = match.group("name")
        ret = match.group("ret").strip()
        params = match.group("params").strip()

        # 排除构造函数
        if name == target_class:
            continue
        # 排除析构函数
        if name.startswith("~"):
            continue
        # 排除宏或 typedef
        if ret in ("typedef", "using", "friend"):
            continue
        # 排除纯属性宏（返回类型包含宏且方法名像宏）
        if not re.match(r"^[A-Za-z_]\w*$", name):
            continue
        # 排除无参方法（除非 include_no_params=True）
        if not include_no_params and (params == "" or params.lower() == "void"):
            continue

        # 检查是否所有参数都是输出参数（引用/指针且是const）
        # IPC stub 模式下不跳过（OnRemoteRequest 需要覆盖所有接口）
        if not include_no_params and _is_all_output_params(params):
            continue

        methods.append((name, params, ret))

    # 去重，保留第一次出现的
    seen = set()
    unique_methods = []
    for name, params, ret in methods:
        key = (name, params)
        if key not in seen:
            seen.add(key)
            unique_methods.append((name, params, ret))

    return unique_methods


def _clean_type(raw_type):
    """清理参数类型，提取基本类型用于映射"""
    t = raw_type.strip()
    # 移除 const/volatile
    t = re.sub(r"\b(const|volatile)\b", "", t).strip()
    # 移除变量名（最后一个token）——但保护C++关键字不被误移除
    tokens = t.split()
    cpp_keywords = {
        "int",
        "long",
        "char",
        "double",
        "float",
        "short",
        "signed",
        "unsigned",
        "void",
        "bool",
        "auto",
    }
    if (
        len(tokens) >= 2
        and tokens[-1] not in cpp_keywords
        and tokens[-1] not in ("*", "&")
    ):
        # 最后一个token是变量名，移除它
        t = " ".join(tokens[:-1])
    elif len(tokens) >= 2 and tokens[-1] in ("*", "&"):
        # 类型以 * 或 & 结尾，如 "int *"
        t = " ".join(tokens[:-1])
    # 移除引用和指针
    t = t.rstrip("&").rstrip("*").strip()
    # 移除默认赋值
    t = re.sub(r"=.*", "", t).strip()
    return t


def _is_all_output_params(param_str):
    """
    检查参数列表是否全部由输出参数组成。
    输出参数特征：
    - 非const引用（Type& var）
    - 指针（Type* var）
    - 容器引用（std::vector<Type>& var）

    返回True表示所有参数都是输出参数，不需要fuzz输入。
    """
    if not param_str or param_str.lower() == "void":
        return True

    # 分割参数
    parts = []
    depth = 0
    current = ""
    for ch in param_str:
        if ch in "(<{":
            depth += 1
            current += ch
        elif ch in ")>}":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())

    # 检查每个参数
    for part in parts:
        part = re.sub(r"=.*", "", part).strip()
        if not part:
            continue

        # 检查是否是const引用或const指针（输入参数）
        if "const" in part.lower() and ("&" in part or "*" in part):
            return False  # const引用/指针是输入参数

        # 检查是否是普通引用（非const，输出参数）
        if "&" in part and "const" not in part.lower():
            continue  # 非const引用是输出参数

        # 检查是否是指针（可能是输出参数）
        if "*" in part:
            continue  # 指针通常是输出参数

        # 检查是否是基本类型（输入参数）
        base_type = _clean_type(part)
        if base_type in (
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
            "float",
            "double",
            "size_t",
            "std::string",
            "FuzzedDataProvider",
        ):
            return False  # 基本类型是输入参数

        # 其他类型（如枚举、结构体等），假设是输入参数
        return False

    return True


def _is_output_param(param_str):
    """
    判断参数是否是输出参数（不需要fuzz输入）。
    输出参数特征：
    - 非const引用（Type& var）
    - 指针（Type* var）
    - 容器引用（std::vector<Type>& var）

    返回True表示是输出参数。
    """
    param_str = param_str.strip()
    if not param_str:
        return False

    # 移除默认值
    param_str = re.sub(r"=.*", "", param_str).strip()

    # 检查是否是const引用或const指针（输入参数）
    if "const" in param_str.lower() and ("&" in param_str or "*" in param_str):
        return False

    # 检查是否是普通引用（非const，输出参数）
    if "&" in param_str and "const" not in param_str.lower():
        return True

    # 检查是否是指针（可能是输出参数）
    if "*" in param_str:
        return True

    return False


def generate_param_consumer(param_str, include_output_params=False):
    """
    根据参数字符串生成 FuzzedDataProvider 消费代码列表。
    返回 (consumers, mock_classes, manual_verify_types)

    consumers: [(var_name, cpp_type, consumer_code)]
    mock_classes: [class_name] 需要生成 Mock 的类名列表
    manual_verify_types: [type_name] 需要人工确认构造的类型列表

    cpp_type 为显式 C++ 类型（如 uint32_t, std::string 等），用于替代 auto

    注意：输出参数（非const引用、指针）会被跳过，不生成消费代码。
    """
    if not param_str or param_str.lower() == "void":
        return [], [], []

    # 简单按逗号分割（不处理模板嵌套括号，如 std::function<void(int)> 会被错误分割）
    # 使用括号计数来正确分割
    parts = []
    depth = 0
    current = ""
    for ch in param_str:
        if ch in "(<{":
            depth += 1
            current += ch
        elif ch in ")>}":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())

    result = []
    mock_classes = []  # 收集需要生成 Mock 的类
    manual_verify_types = []  # 收集需要人工确认的类型
    for idx, part in enumerate(parts):
        # 移除默认值
        part = re.sub(r"=.*", "", part).strip()
        if not part:
            continue

        # 跳过输出参数（IPC stub 模式不跳过，声明局部变量传入）
        if _is_output_param(part):
            if include_output_params:
                var_name = part.split()[-1].lstrip("*").lstrip("&")
                base_type = _clean_type(part).rstrip("&").rstrip("*").strip()
                result.append((var_name, base_type, "0 /* output param */"))
            continue

        # 提取变量名（最后一个 token）
        tokens = part.split()
        if len(tokens) >= 2 and tokens[-1] in ("*", "&"):
            var_name = f"param{idx}"
            base_type = _clean_type(part)
        elif len(tokens) >= 1:
            var_name = tokens[-1].lstrip("*").lstrip("&")
            base_type = _clean_type(
                " ".join(tokens[:-1]) if len(tokens) > 1 else tokens[0]
            )
        else:
            var_name = f"param{idx}"
            base_type = _clean_type(part)

        if base_type in COMPLEX_TYPE_MAP:
            raw_consumer = COMPLEX_TYPE_MAP[base_type](var_name) + "\n"
            # 对多行复杂类型初始化统一添加4空格缩进
            consumer = "\n".join(
                "    " + line if line.strip() else line
                for line in raw_consumer.splitlines()
            )
            # 复杂类型直接返回声明语句，cpp_type 为 None 表示已包含类型声明
            result.append((var_name, None, consumer))
        elif base_type in ENUM_SIZE_MAP:
            cpp_type = base_type
            # 规则013: 使用 uint8_t 提取枚举值，不取模，保留非法值覆盖
            # 合法值命中率约 2%~10%，既能测试正常路径，又能充分测试异常路径
            consumer = f"static_cast<{base_type}>(fdp.ConsumeIntegral<uint8_t>())"
            result.append((var_name, cpp_type, consumer))
        elif base_type.startswith("std::vector<") and base_type.endswith(">"):
            inner = base_type[len("std::vector<") : -1]
            if inner in ENUM_SIZE_MAP:
                # 规则013: 使用 uint8_t 提取枚举值，不取模，保留非法值覆盖
                cpp_type = f"std::vector<{inner}>"
                consumer = f"std::vector<{inner}>{{ static_cast<{inner}>(fdp.ConsumeIntegral<uint8_t>()) }}"
                result.append((var_name, cpp_type, consumer))
            else:
                type_info = TYPE_CONSUMER_MAP.get(base_type)
                if type_info:
                    cpp_type, consumer = type_info
                else:
                    cpp_type = "uint32_t"
                    consumer = f"fdp.ConsumeIntegral<uint32_t>() /* auto-generated for {base_type} */"
                result.append((var_name, cpp_type, consumer))
        else:
            type_info = TYPE_CONSUMER_MAP.get(base_type)
            if type_info:
                cpp_type, consumer = type_info
            else:
                # 智能指针/复杂类型：使用 new 或 std::make_shared 构造
                if base_type.startswith("sptr<") and base_type.endswith(">"):
                    inner_type = base_type[5:-1]  # 提取 sptr<...> 中的类型
                    # 尝试推断 Mock 类名
                    mock_name = f"Mock{inner_type}"
                    cpp_type = None  # None 表示已包含完整声明
                    consumer = f"sptr<{inner_type}> {var_name} = new {mock_name}(); // TODO: verify constructor"
                    # 记录需要生成 Mock 的类
                    if inner_type not in mock_classes:
                        mock_classes.append(inner_type)
                elif base_type.startswith("std::shared_ptr<") and base_type.endswith(
                    ">"
                ):
                    inner_type = base_type[16:-1]  # 提取 std::shared_ptr<...> 中的类型
                    if base_type in COMPLEX_TYPE_MAP:
                        # 使用 COMPLEX_TYPE_MAP 中的定义
                        complex_def = COMPLEX_TYPE_MAP[base_type]
                        if callable(complex_def):
                            cpp_type = None
                            consumer = complex_def(var_name)
                        else:
                            cpp_type = None
                            consumer = complex_def
                    else:
                        cpp_type = None
                        consumer = f"std::shared_ptr<{inner_type}> {var_name} = std::make_shared<{inner_type}>(); // TODO: verify constructor"
                else:
                    # 未识别的复杂类型，生成 TODO 注释，需要在报告中标注
                    cpp_type = None
                    consumer = f"// TODO[NEED_MANUAL_VERIFY]: 无法自动构造类型 '{base_type}'，请开发人工确认和构造\n    uint32_t {var_name} = fdp.ConsumeIntegral<uint32_t>() /* placeholder for {base_type} */"
                    if base_type not in manual_verify_types:
                        manual_verify_types.append(base_type)
            result.append((var_name, cpp_type, consumer))

    return result, mock_classes, manual_verify_types


def _generate_mock_class(interface_name, header_path_str):
    """
    为接口生成 Mock 类定义。
    尝试从接口头文件中解析纯虚函数并生成空实现。
    返回 Mock 类定义字符串，如果无法解析则返回 None。
    """
    # 尝试查找接口的头文件
    search_dirs = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path(__file__).parent.parent.parent,
        Path(__file__).parent.parent.parent.parent,
    ]

    # 尝试从 header_path_str 推断接口头文件路径
    interface_header = None
    if header_path_str:
        header_dir = os.path.dirname(header_path_str)
        # 尝试常见的路径模式
        # 将接口名转换为 snake_case（如 RSIScreenManagerListener -> rs_iscreen_manager_listener）
        # 处理 OpenHarmony 命名规范
        snake_name = interface_name
        # 替换常见的缩写前缀（注意顺序，先替换长的）
        snake_name = re.sub(r"^RSIScreen", "rs_iscreen", snake_name)
        snake_name = re.sub(r"^RSI", "rs_i", snake_name)
        snake_name = re.sub(r"^RS", "rs_", snake_name)
        snake_name = re.sub(r"^HDI", "hdi_", snake_name)
        # 然后在剩余部分添加下划线
        snake_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake_name)
        snake_name = snake_name.lower()
        possible_paths = [
            os.path.join(header_dir, f"public/{snake_name}.h"),
            os.path.join(header_dir, f"{snake_name}.h"),
            os.path.join(header_dir, f"public/{interface_name.lower()}.h"),
            os.path.join(header_dir, f"{interface_name.lower()}.h"),
        ]
        for path in possible_paths:
            if os.path.isfile(path):
                interface_header = path
                break

    mock_name = f"Mock{interface_name}"

    # 如果找不到头文件，生成最小化的 Mock 类
    if not interface_header:
        return f"""class {mock_name} : public {interface_name} {{
public:
    ~{mock_name}() override = default;
}};"""

    try:
        content = Path(interface_header).read_text(encoding="utf-8", errors="ignore")
        content = re.sub(r"//[^\n]*", "", content)
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

        # 查找类定义
        class_pattern = rf"\bclass\s+{re.escape(interface_name)}\b.*?\{{"
        m = re.search(class_pattern, content)
        if not m:
            return f"""class {mock_name} : public {interface_name} {{
public:
    ~{mock_name}() override = default;
}};"""

        # 提取类体（简化处理，找匹配的括号）
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

        class_body = content[start:end]

        # 提取纯虚函数
        pure_virtual_methods = []
        # 匹配模式：virtual ... = 0;
        pv_pattern = r"virtual\s+([\w\s\*\&<>]+?)\s+(\w+)\s*\(([^)]*)\)\s*=\s*0\s*;"
        for match in re.finditer(pv_pattern, class_body):
            return_type = match.group(1).strip()
            method_name = match.group(2)
            params = match.group(3)
            pure_virtual_methods.append((return_type, method_name, params))

        if not pure_virtual_methods:
            return f"""class {mock_name} : public {interface_name} {{
public:
    ~{mock_name}() override = default;
}};"""

        # 生成 Mock 方法实现
        mock_methods = []
        for return_type, method_name, params in pure_virtual_methods:
            # 生成默认返回值
            default_return = ""
            if return_type != "void":
                if "sptr<" in return_type or "std::shared_ptr<" in return_type:
                    default_return = " { return nullptr; }"
                elif return_type in [
                    "bool",
                    "int",
                    "int32_t",
                    "uint32_t",
                    "int64_t",
                    "uint64_t",
                    "size_t",
                ]:
                    default_return = " { return 0; }"
                elif return_type == "float" or return_type == "double":
                    default_return = " { return 0.0; }"
                elif "std::string" in return_type:
                    default_return = ' { return ""; }'
                elif "std::vector" in return_type:
                    default_return = " { return {}; }"
                else:
                    default_return = " { return {}; }"
            else:
                default_return = " {}"

            mock_methods.append(
                f"    {return_type} {method_name}({params}) override{default_return}"
            )

        mock_methods_str = "\n".join(mock_methods)
        return f"""class {mock_name} : public {interface_name} {{
public:
    ~{mock_name}() override = default;
{mock_methods_str}
}};"""

    except Exception:
        return f"""class {mock_name} : public {interface_name} {{
public:
    ~{mock_name}() override = default;
}};"""


def _detect_refbase_subclass(header_path_str, target_class):
    """
    检测目标类是否继承自 RefBase。
    返回 True/False
    """
    search_dirs = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path(__file__).parent.parent.parent,
        Path(__file__).parent.parent.parent.parent,
    ]
    resolved = _resolve_header_path(header_path_str, search_dirs)
    if not resolved or not os.path.isfile(resolved):
        return False

    content = Path(resolved).read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"//[^\n]*", "", content)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # 匹配 class XXX : public RefBase 或 class XXX : public XXX, public RefBase
    refbase_pattern = (
        rf"\bclass\s+{re.escape(target_class)}\b[^;]*?:\s*public\s+\w*RefBase\b"
    )
    if re.search(refbase_pattern, content):
        return True

    # 也检查是否继承自其他类，但最终继承链中包含 RefBase
    # 简化处理：检查 class 声明中是否有 RefBase
    class_pattern = rf"\bclass\s+{re.escape(target_class)}\b[^;]*?\{{"
    m = re.search(class_pattern, content)
    if m:
        class_decl = content[m.start() : m.end()]
        if "RefBase" in class_decl:
            return True

    return False


def _find_stub_class_name(header_path_str, target_class):
    """
    从 IPC 头文件中查找 Stub 类名。
    如 target_class 为 "IVSyncConnection"，查找 RSIVSyncConnectionStub 或类似命名。
    """
    search_dirs = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path(__file__).parent.parent.parent,
        Path(__file__).parent.parent.parent.parent,
    ]
    resolved = _resolve_header_path(header_path_str, search_dirs)
    if not resolved or not os.path.isfile(resolved):
        return None

    content = Path(resolved).read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"//[^\n]*", "", content)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    patterns = [
        rf"\bclass\s+(\w*{re.escape(target_class)}\w*Stub)\b",
        rf"\bclass\s+(RSI{re.escape(target_class)}\w*Stub)\b",
        rf"\bclass\s+(\w*Stub)\b[^;]*?\b{re.escape(target_class)}\b",
    ]
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            return m.group(1)

    common_prefixes = ["RSI", "RS"]
    for prefix in common_prefixes:
        candidate = f"{prefix}{target_class}Stub"
        if re.search(rf"\bclass\s+{re.escape(candidate)}\b", content):
            return candidate

    return f"{target_class}Stub"


def _detect_ipc_stub(header_path_str, target_class):
    """
    检测目标类是否为 IPC Stub 类。
    返回 (is_ipc_stub: bool, stub_class_name: str)
    """
    search_dirs = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path(__file__).parent.parent.parent,
        Path(__file__).parent.parent.parent.parent,
    ]
    resolved = _resolve_header_path(header_path_str, search_dirs)
    if not resolved or not os.path.isfile(resolved):
        return (False, None)

    content = Path(resolved).read_text(encoding="utf-8", errors="ignore")
    content = re.sub(r"//[^\n]*", "", content)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    ipc_indicators = [
        r"OnRemoteRequest",
        r"MessageParcel",
        r"IRemoteStub",
        r"IRemoteBroker",
        r"IRemoteProxy",
        r"DECLARE_INTERFACE_DESCRIPTOR",
    ]
    indicator_count = 0
    for indicator in ipc_indicators:
        if re.search(indicator, content):
            indicator_count += 1

    inherits_remote_broker = bool(
        re.search(r"class\s+\w+\s*:\s*public\s+IRemoteBroker", content)
    )

    stub_class_name = _find_stub_class_name(header_path_str, target_class)

    is_ipc_stub = (
        inherits_remote_broker
        or indicator_count >= 2
        or (stub_class_name and stub_class_name != f"{target_class}Stub")
    )

    if "Stub" in target_class or "Proxy" in target_class:
        is_ipc_stub = True

    return (is_ipc_stub, stub_class_name)


def build_init_blocks(init_mode, namespace, target_class, header_path=None):
    target_lower = target_class.lower()

    ns_parts = _split_namespace(namespace)
    ns_qual = _namespace_qualifier(ns_parts)
    full_qual = ns_qual

    is_refbase = False
    if header_path:
        is_refbase = _detect_refbase_subclass(header_path, target_class)

    if init_mode == INIT_MODE_SINGLETON:
        if is_refbase:
            global_decl = f"sptr<{target_class}> g_{target_lower} = nullptr;"
        else:
            global_decl = f"{target_class}* g_{target_lower} = nullptr;"
        init_body = (
            f"    // 预初始化单例避免运行时初始化开销\n"
            f"    {full_qual}g_{target_lower} = &{full_qual}{target_class}::GetInstance();\n"
            f"    return 0;"
        )
        null_check = (
            f"    if ({full_qual}g_{target_lower} == nullptr || data == nullptr) {{\n"
            f"        return -1;\n"
            f"    }}"
        )
        call_prefix = f"g_{target_lower}->"
    elif init_mode == INIT_MODE_FACTORY:
        if is_refbase:
            global_decl = f"sptr<{target_class}> g_{target_lower} = nullptr;"
            init_body = (
                f"    // 预初始化单例避免运行时初始化开销\n"
                f"    {full_qual}g_{target_lower} = {full_qual}{target_class}::Create();\n"
                f"    return 0;"
            )
        else:
            global_decl = f"std::shared_ptr<{target_class}> g_{target_lower} = nullptr;"
            init_body = (
                f"    // 预初始化单例避免运行时初始化开销\n"
                f"    {full_qual}g_{target_lower} = {full_qual}{target_class}::Create();\n"
                f"    return 0;"
            )
        null_check = (
            f"    if ({full_qual}g_{target_lower} == nullptr || data == nullptr) {{\n"
            f"        return -1;\n"
            f"    }}"
        )
        call_prefix = f"g_{target_lower}->"
    else:
        if is_refbase:
            global_decl = f"sptr<{target_class}> g_{target_lower} = nullptr;"
            init_body = (
                f"    {full_qual}g_{target_lower} = new {full_qual}{target_class}();\n"
                f"    return 0;"
            )
        else:
            global_decl = f"std::shared_ptr<{target_class}> g_{target_lower} = nullptr;"
            init_body = (
                f"    {full_qual}g_{target_lower} = std::make_shared<{full_qual}{target_class}>();\n"
                f"    return 0;"
            )
        null_check = (
            f"    if ({full_qual}g_{target_lower} == nullptr || data == nullptr) {{\n"
            f"        return -1;\n"
            f"    }}"
        )
        call_prefix = f"g_{target_lower}->"

    return global_decl, init_body, null_check, call_prefix


def generate_fuzzer_cpp(
    fuzzer_name,
    namespace,
    target_class,
    target_header,
    methods,
    init_mode="none",
    header_path=None,
):
    """
    methods: [(method_name, params_str, return_type), ...]
    """
    template = read_template("fuzzer.cpp")
    target_lower = target_class.lower()

    ns_parts = _split_namespace(namespace)
    ns_open = _build_namespace_open(ns_parts)
    ns_close = _build_namespace_close(ns_parts)
    ns_qual = _namespace_qualifier(ns_parts)
    header_basename = (
        os.path.basename(target_header.strip().strip('"').strip("'"))
        if target_header
        else ""
    )

    global_decl, init_body, null_check, call_prefix = build_init_blocks(
        init_mode, namespace, target_class, header_path
    )

    # 收集 methods 中用到的枚举 size 常量，去重后生成 constexpr
    used_enum_constants = {}
    for _, params, _ in methods:
        parts = []
        depth = 0
        current = ""
        for ch in params:
            if ch in "(<{":
                depth += 1
                current += ch
            elif ch in ")>}":
                depth -= 1
                current += ch
            elif ch == "," and depth == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += ch
        if current.strip():
            parts.append(current.strip())
        for part in parts:
            t = part.strip()
            t = re.sub(r"=.*", "", t).strip()
            tokens = t.split()
            if len(tokens) >= 2 and tokens[-1] in ("*", "&"):
                base_type = _clean_type(" ".join(tokens[:-1]))
            elif len(tokens) >= 1:
                base_type = _clean_type(
                    " ".join(tokens[:-1]) if len(tokens) > 1 else tokens[0]
                )
            else:
                base_type = _clean_type(t)
            if base_type in ENUM_SIZE_MAP:
                const_name, val = ENUM_SIZE_MAP[base_type]
                used_enum_constants[const_name] = val
            elif base_type.startswith("std::vector<") and base_type.endswith(">"):
                inner = base_type[len("std::vector<") : -1]
                if inner in ENUM_SIZE_MAP:
                    const_name, val = ENUM_SIZE_MAP[inner]
                    used_enum_constants[const_name] = val

    # 生成常量
    name_counts_reg = {}
    for m_name, _, _ in methods:
        name_counts_reg[m_name] = name_counts_reg.get(m_name, 0) + 1
    constants_lines = []
    for const_name, val in sorted(used_enum_constants.items()):
        constants_lines.append(f"constexpr uint8_t {const_name} = {val};")
    name_seen_reg = {}
    for idx, (name, _, _) in enumerate(methods):
        count = name_seen_reg.get(name, 0)
        name_seen_reg[name] = count + 1
        const_suffix = f"_V{count}" if name_counts_reg[name] > 1 else ""
        constants_lines.append(
            f"const uint8_t {_snake_case_const(name)}{const_suffix} = {idx};"
        )
    constants_lines.append(f"const uint8_t TARGET_SIZE = {len(methods)};")
    method_constants = "\n".join(constants_lines)

    # 生成 DoXXX 函数
    name_seen_func = {}
    func_lines = []
    all_mock_classes = []
    all_manual_verify_types = []
    for name, params, _ in methods:
        count = name_seen_func.get(name, 0)
        name_seen_func[name] = count + 1
        suffix = str(count) if name_counts_reg[name] > 1 else ""
        do_name = _do_func_name(name) + suffix
        consumers, mock_classes, manual_verify_types = generate_param_consumer(
            params, include_output_params=True
        )
        all_mock_classes.extend(mock_classes)
        all_manual_verify_types.extend(manual_verify_types)
        body_lines = []
        for var_name, cpp_type, consumer in consumers:
            if cpp_type is None:
                # 复杂类型，consumer 已包含完整声明语句
                body_lines.append("    " + consumer)
            elif (
                consumer.strip().endswith(";")
                and var_name in consumer
                and "=" not in consumer
            ):
                # 声明语句（如 sptr<Surface> surface; 或 Rect r{...};），直接插入
                body_lines.append("    " + consumer.strip())
            else:
                # 使用显式类型声明替代 auto
                body_lines.append(f"    {cpp_type} {var_name} = {consumer};")

        if call_prefix is not None:
            call_line = f"    {call_prefix}{name}("
        else:
            call_line = f"    std::shared_ptr<{target_class}> {target_lower} = std::make_shared<{target_class}>();\n    {target_lower}->{name}("

        if consumers:
            call_line += ", ".join(v for v, _, _ in consumers) + ");"
        else:
            call_line += ");"

        if body_lines:
            func_body = "\n".join(body_lines) + "\n" + call_line
        else:
            # 无参数函数：直接调用，不消费fdp
            # 注意：这类函数不适合fuzz测试，应该在头文件解析阶段就被过滤掉
            func_body = call_line

        func_lines.append(
            f"void {do_name}(FuzzedDataProvider& fdp)\n{{\n{func_body}\n}}"
        )

    method_functions = "\n\n".join(func_lines)

    # 生成 Mock 类定义
    mock_classes_def = ""
    if all_mock_classes:
        # 去重
        unique_mock_classes = list(dict.fromkeys(all_mock_classes))
        mock_defs = []
        for class_name in unique_mock_classes:
            mock_def = _generate_mock_class(class_name, header_path)
            if mock_def:
                mock_defs.append(mock_def)
        mock_classes_def = "\n\n".join(mock_defs)

    # 生成 switch case
    case_lines = []
    name_seen_case = {}
    for name, _, _ in methods:
        count = name_seen_case.get(name, 0)
        name_seen_case[name] = count + 1
        suffix = str(count) if name_counts_reg[name] > 1 else ""
        const_suffix = f"_V{count}" if name_counts_reg[name] > 1 else ""
        const_name = _snake_case_const(name) + const_suffix
        do_name = _do_func_name(name) + suffix
        case_lines.append(
            f"        case {const_name}:\n"
            f"            {do_name}(fdp);\n"
            f"            break;"
        )
    switch_cases = "\n".join(case_lines)

    replacements = {
        "{YEAR}": str(datetime.now().year),
        "{FUZZER_NAME}": fuzzer_name,
        "{NAMESPACE}": namespace,
        "{TARGET_CLASS}": target_class,
        "{TARGET_HEADER}": f'"{header_basename}"',
        "{NS_QUALIFIER}": ns_qual,
        "{GLOBAL_INSTANCE_DECL}": global_decl,
        "{LLVM_FUZZER_INIT_BODY}": init_body,
        "{NULL_CHECK_GLOBAL}": null_check,
        "{METHOD_CONSTANTS}": method_constants,
        "{METHOD_FUNCTIONS}": method_functions,
        "{SWITCH_CASES}": switch_cases,
    }

    content = template
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    content = content.replace(
        f"namespace OHOS {{\nnamespace {namespace} {{\n",
        ns_open + "\n",
    )
    content = content.replace(
        f"}} // namespace {namespace}\n}} // namespace OHOS\n",
        ns_close,
    )

    # 在 namespace 开启之后插入 Mock 类定义
    if mock_classes_def:
        ns_anchor = ns_open.rstrip()
        if ns_anchor in content:
            insert_pos = content.find(ns_anchor) + len(ns_anchor)
            content = (
                content[:insert_pos] + "\n" + mock_classes_def + content[insert_pos:]
            )

    return content, all_manual_verify_types


def generate_ipc_stub_fuzzer_cpp(
    fuzzer_name,
    namespace,
    target_class,
    target_header,
    methods,
    init_mode="none",
    header_path=None,
    stub_class_name=None,
    total_method_count=None,
):
    stub_name = stub_class_name if stub_class_name else f"{target_class}Stub"
    target_lower = target_class.lower()
    year = datetime.now().year

    code_max = len(methods)
    if total_method_count and total_method_count > len(methods):
        code_max = total_method_count
    if header_path:
        enum_count = _extract_ipc_code_count(header_path, target_class)
        if enum_count > 0:
            code_max = enum_count

    ns_parts = _split_namespace(namespace)
    ns_open = _build_namespace_open(ns_parts)
    ns_close = _build_namespace_close(ns_parts)
    ns_qual = _namespace_qualifier(ns_parts)

    header_basename = (
        os.path.basename(target_header.strip().strip('"').strip("'"))
        if target_header
        else ""
    )

    stub_full_qual = f"{ns_qual}{stub_name}"

    name_counts = {}
    for m_name, _, _ in methods:
        name_counts[m_name] = name_counts.get(m_name, 0) + 1
    name_seen = {}

    func_lines = []
    all_mock_classes = []
    all_manual_verify_types = []
    for name, params, _ in methods:
        count = name_seen.get(name, 0)
        name_seen[name] = count + 1
        if name_counts[name] > 1:
            suffix = str(count)
        else:
            suffix = ""
        do_name = _do_func_name(name) + suffix
        const_name = _snake_case_const(name) + (
            f"_V{count}" if name_counts[name] > 1 else ""
        )
        consumers, mock_classes, manual_verify_types = generate_param_consumer(
            params, include_output_params=True
        )
        all_mock_classes.extend(mock_classes)
        all_manual_verify_types.extend(manual_verify_types)
        body_lines = []
        for var_name, cpp_type, consumer in consumers:
            if cpp_type is None:
                body_lines.append("    " + consumer)
            elif (
                consumer.strip().endswith(";")
                and var_name in consumer
                and "=" not in consumer
            ):
                body_lines.append("    " + consumer.strip())
            else:
                body_lines.append(f"    {cpp_type} {var_name} = {consumer};")

        call_line = f"    g_stub->{name}("
        if consumers:
            call_line += ", ".join(v for v, _, _ in consumers) + ");"
        else:
            call_line += ");"

        if body_lines:
            func_body = "\n".join(body_lines) + "\n" + call_line
        else:
            func_body = call_line

        func_lines.append(
            f"void {do_name}(FuzzedDataProvider& fdp)\n{{\n{func_body}\n}}"
        )

    method_functions = "\n\n".join(func_lines)

    constants_lines = []
    name_counts2 = {}
    name_seen2 = {}
    for idx, (name, _, _) in enumerate(methods):
        name_counts2[name] = name_counts2.get(name, 0) + 1
    for idx, (name, _, _) in enumerate(methods):
        count2 = name_seen2.get(name, 0)
        name_seen2[name] = count2 + 1
        if name_counts2[name] > 1:
            const_suffix = f"_V{count2}"
        else:
            const_suffix = ""
        constants_lines.append(
            f"const uint8_t {_snake_case_const(name)}{const_suffix} = {idx};"
        )
    constants_lines.append(f"constexpr uint8_t CODE_MAX = {code_max};")
    method_constants = "\n".join(constants_lines)

    case_lines = []
    name_counts3 = {}
    name_seen3 = {}
    for m_name, _, _ in methods:
        name_counts3[m_name] = name_counts3.get(m_name, 0) + 1
    for name, params, _ in methods:
        count3 = name_seen3.get(name, 0)
        name_seen3[name] = count3 + 1
        if name_counts3[name] > 1:
            suffix3 = str(count3)
            const_suffix3 = f"_V{count3}"
        else:
            suffix3 = ""
            const_suffix3 = ""
        do_name = _do_func_name(name) + suffix3
        const_name = _snake_case_const(name) + const_suffix3
        case_lines.append(
            f"        case {const_name}:\n"
            f"            {do_name}(fdp);\n"
            f"            break;"
        )
    switch_cases = "\n".join(case_lines)

    used_enum_constants = {}
    for _, params, _ in methods:
        parts = []
        depth = 0
        current = ""
        for ch in params:
            if ch in "(<{":
                depth += 1
                current += ch
            elif ch in ")>}":
                depth -= 1
                current += ch
            elif ch == "," and depth == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += ch
        if current.strip():
            parts.append(current.strip())
        for part in parts:
            t = part.strip()
            t = re.sub(r"=.*", "", t).strip()
            tokens = t.split()
            if len(tokens) >= 2 and tokens[-1] in ("*", "&"):
                base_type = _clean_type(" ".join(tokens[:-1]))
            elif len(tokens) >= 1:
                base_type = _clean_type(
                    " ".join(tokens[:-1]) if len(tokens) > 1 else tokens[0]
                )
            else:
                base_type = _clean_type(t)
            if base_type in ENUM_SIZE_MAP:
                const_name, val = ENUM_SIZE_MAP[base_type]
                used_enum_constants[const_name] = val

    enum_const_lines = ""
    if used_enum_constants:
        ecl_lines = []
        for const_name, val in sorted(used_enum_constants.items()):
            ecl_lines.append(f"constexpr uint8_t {const_name} = {val};")
        enum_const_lines = "\n".join(ecl_lines) + "\n"

    mock_classes_def = ""
    if all_mock_classes:
        unique_mock_classes = list(dict.fromkeys(all_mock_classes))
        mock_defs = []
        for class_name in unique_mock_classes:
            mock_def = _generate_mock_class(class_name, header_path)
            if mock_def:
                mock_defs.append(mock_def)
        mock_classes_def = "\n\n".join(mock_defs)

    cpp_code = (
        f"/*\n"
        f" * Copyright (c) {year} Huawei Device Co., Ltd.\n"
        f' * Licensed under the Apache License, Version 2.0 (the "License");\n'
        f" * you may not use this file except in compliance with the License.\n"
        f" * You may obtain a copy of the License at\n"
        f" *\n"
        f" *     http://www.apache.org/licenses/LICENSE-2.0\n"
        f" *\n"
        f" * Unless required by applicable law or agreed to in writing, software\n"
        f' * distributed under the License is distributed on an "AS IS" BASIS,\n'
        f" * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        f" * See the License for the specific language governing permissions and\n"
        f" * limitations under the License.\n"
        f" */\n"
        f"\n"
        f'#include "{fuzzer_name}.h"\n'
        f"\n"
        f"#include <fuzzer/FuzzedDataProvider.h>\n"
        f"\n"
        f'#include "{header_basename}"\n'
        f"\n"
        + ns_open
        + "\n"
        + f"std::shared_ptr<{stub_name}> g_stub = nullptr;\n"
        + "\n"
        + (mock_classes_def + "\n" if mock_classes_def else "")
        + enum_const_lines
        + "\n"
        + "namespace {\n"
        + "\n"
        + method_constants
        + "\n"
        + "\n"
        + method_functions
        + "\n"
        + "\n"
        + "} // namespace\n"
        + "\n"
        + ns_close
        + "\n"
        + "\n"
        + 'extern "C" int LLVMFuzzerInitialize(int* argc, char*** argv)\n'
        + "{\n"
        + f"    {ns_qual}g_stub = std::make_shared<{stub_full_qual}>();\n"
        + "    return 0;\n"
        + "}\n"
        + "\n"
        + 'extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)\n'
        + "{\n"
        + f"    if ({ns_qual}g_stub == nullptr || data == nullptr) {{\n"
        + "        return -1;\n"
        + "    }\n"
        + "\n"
        + "    FuzzedDataProvider fdp(data, size);\n"
        + "\n"
        + "    uint8_t tarPos = fdp.ConsumeIntegral<uint8_t>() % CODE_MAX;\n"
        + "    switch (tarPos) {\n"
        + switch_cases
        + "\n"
        + "        default:\n"
        + "            return -1;\n"
        + "    }\n"
        + "    return 0;\n"
        + "}\n"
    )

    return cpp_code, all_manual_verify_types


def generate_fuzzer_h(fuzzer_name):
    template = read_template("fuzzer.h")
    year = datetime.now().year
    content = template.replace("{YEAR}", str(year))
    content = content.replace("{FUZZER_NAME}", fuzzer_name)
    content = content.replace("{FUZZER_NAME_UPPER}", fuzzer_name.upper())
    return content


def generate_build_gn(
    fuzzer_name,
    module_path,
    full_path,
    include_path1,
    include_path2,
    dep_path,
    dep_target,
):
    template = read_template("BUILD.gn")
    # 规则G: ohos_fuzztest 目标名应以 FuzzTest 结尾，驼峰式命名
    # 将 XxxXxx_fuzzer 转换为 XxxXxxFuzzTest
    base_name = re.sub(r"\d+$", "", fuzzer_name)  # 去掉数字后缀
    prefix = (
        base_name[:-7] if base_name.endswith("_fuzzer") else base_name
    )  # 去掉 _fuzzer
    target_name = prefix + "FuzzTest"
    replacements = {
        "{YEAR}": str(datetime.now().year),
        "{FUZZER_NAME}": fuzzer_name,
        "{FUZZER_TARGET_NAME}": target_name,
        "{MODULE_PATH}": module_path,
        "{FULL_PATH}": full_path,
        "{INCLUDE_PATH_1}": include_path1,
        "{INCLUDE_PATH_2}": include_path2,
        "{DEP_PATH}": dep_path,
        "{DEP_TARGET}": dep_target,
    }
    content = template
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def generate_project_xml():
    template = read_template("project.xml")
    return template.replace("{YEAR}", str(datetime.now().year))


def generate_corpus_init():
    """
    生成二进制种子文件内容。
    返回 bytes 对象，而不是文本字符串。
    种子包含：
    - 1字节：目标方法选择器（0）
    - 后续字节：参数数据（基本类型的最小有效数据）
    """
    # 创建一个基本的二进制种子：
    # 第1字节：选择第一个方法（索引0）
    # 后续字节：为各种参数类型提供基础数据
    seed_data = bytearray()

    # 方法选择器（1字节）
    seed_data.append(0)

    # 为各种参数类型填充基础数据
    # bool: 1字节
    seed_data.append(1)

    # int8_t/uint8_t: 1字节
    seed_data.append(0x42)

    # int16_t/uint16_t: 2字节
    seed_data.extend([0x12, 0x34])

    # int32_t/uint32_t: 4字节
    seed_data.extend([0x12, 0x34, 0x56, 0x78])

    # int64_t/uint64_t: 8字节
    seed_data.extend([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])

    # float: 4字节
    seed_data.extend([0x3F, 0x80, 0x00, 0x00])  # 1.0f

    # double: 8字节
    seed_data.extend([0x3F, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # 1.0

    # string length (1字节) + string data
    test_string = "FUZZ"
    seed_data.append(len(test_string))
    seed_data.extend(test_string.encode("utf-8"))

    return bytes(seed_data)


def _get_param_signature(params):
    """
    提取参数类型签名，用于分组去重。
    相同参数签名的方法共享种子文件。
    """
    if not params or params.lower() == "void":
        return "void"
    param_list = _parse_params(params)
    cleaned = tuple(_clean_type(p) for p in param_list)
    return cleaned


def _has_type_in_params(params, target_types):
    """检查方法的参数中是否包含指定类型"""
    if not params or params.lower() == "void":
        return False
    param_list = _parse_params(params)
    for p in param_list:
        cleaned = _clean_type(p)
        if cleaned in target_types:
            return True
    return False


def _deduplicate_seeds(generated_files, corpus_dir):
    """按内容 hash 去重，保留文件名最短的"""
    import hashlib

    hashes = {}
    unique_files = []
    removed = 0

    for filepath in generated_files:
        if not os.path.isfile(filepath):
            continue
        data = open(filepath, "rb").read()
        h = hashlib.md5(data).hexdigest()
        if h in hashes:
            os.remove(filepath)
            removed += 1
        else:
            hashes[h] = filepath
            unique_files.append(filepath)

    if removed > 0:
        print(f"[INFO] 种子去重: 移除 {removed} 个重复文件")
    return unique_files


def generate_semantic_seeds(methods, corpus_dir):
    """
    根据方法列表生成语义化的种子文件。

    优化策略:
    1. 按参数类型签名分组，相同签名的方法共享种子
    2. 只生成与方法参数类型相关的边界值/特殊值
    3. 笛卡尔积按分组限制，而非全局
    4. 最终按内容 hash 去重
    """
    import struct

    corpus_dir = Path(corpus_dir)
    corpus_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    # 按参数签名分组
    signature_groups = {}
    for idx, (name, params, ret_type) in enumerate(methods):
        sig = _get_param_signature(params)
        if sig not in signature_groups:
            signature_groups[sig] = []
        signature_groups[sig].append((idx, name, params, ret_type))

    # 为每个分组生成种子（组内共享）
    for sig, group_methods in signature_groups.items():
        representative = group_methods[0]
        rep_idx, rep_name, rep_params, rep_ret_type = representative

        # 基础种子：每个方法一个
        for idx, name, params, ret_type in group_methods:
            seed_data = bytearray()
            seed_data.append(idx)
            if params and params.lower() != "void":
                param_list = _parse_params(params)
                for param_type in param_list:
                    _append_param_seed(seed_data, param_type)
            seed_path = corpus_dir / f"seed_{idx}_{name}"
            with open(seed_path, "wb") as f:
                f.write(bytes(seed_data))
            generated_files.append(str(seed_path))

        # 边界值种子：按分组生成（组内共享）
        boundary_data = bytearray()
        boundary_data.append(rep_idx)
        if rep_params and rep_params.lower() != "void":
            param_list = _parse_params(rep_params)
            for param_type in param_list:
                cleaned_type = _clean_type(param_type)
                _append_boundary_value(boundary_data, cleaned_type)
        seed_path = corpus_dir / f"boundary_{rep_name}"
        with open(seed_path, "wb") as f:
            f.write(bytes(boundary_data))
        generated_files.append(str(seed_path))

        # 特殊值种子：按分组生成（组内共享）
        special_data = bytearray()
        special_data.append(rep_idx)
        if rep_params and rep_params.lower() != "void":
            param_list = _parse_params(rep_params)
            for param_type in param_list:
                cleaned_type = _clean_type(param_type)
                _append_special_value(special_data, cleaned_type)
        seed_path = corpus_dir / f"special_{rep_name}"
        with open(seed_path, "wb") as f:
            f.write(bytes(special_data))
        generated_files.append(str(seed_path))

    # 生成通用边界值种子（仅包含方法实际使用的类型）
    all_used_types = set()
    for name, params, ret_type in methods:
        if params and params.lower() != "void":
            for p in _parse_params(params):
                all_used_types.add(_clean_type(p))

    # 只为实际使用的类型生成全局边界值
    global_boundary = _generate_global_boundary_seeds(all_used_types, corpus_dir)
    generated_files.extend(global_boundary)

    # 生成业务场景种子
    biz_seeds = _generate_biz_seeds(methods, corpus_dir)
    generated_files.extend(biz_seeds)

    # 去重
    generated_files = _deduplicate_seeds(generated_files, corpus_dir)

    return generated_files


def _append_boundary_value(seed_data, cleaned_type):
    """为指定类型追加边界值到种子数据"""
    if cleaned_type in ["int8_t"]:
        seed_data.extend([0x80])
    elif cleaned_type in ["uint8_t"]:
        seed_data.extend([0xFF])
    elif cleaned_type in ["int16_t"]:
        seed_data.extend([0x80, 0x00])
    elif cleaned_type in ["uint16_t"]:
        seed_data.extend([0xFF, 0xFF])
    elif cleaned_type in ["int32_t", "int"]:
        seed_data.extend([0x80, 0x00, 0x00, 0x00])
    elif cleaned_type in ["uint32_t", "unsigned", "unsigned int"]:
        seed_data.extend([0xFF, 0xFF, 0xFF, 0xFF])
    elif cleaned_type in ["int64_t", "long long"]:
        seed_data.extend([0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif cleaned_type in [
        "uint64_t",
        "unsigned long long",
        "size_t",
        "ScreenId",
        "NodeId",
        "WindowId",
        "DisplayId",
        "Handle",
    ]:
        seed_data.extend([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    elif cleaned_type == "float":
        seed_data.extend([0x7F, 0x7F, 0xFF, 0xFF])
    elif cleaned_type == "double":
        seed_data.extend([0x7F, 0xEF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    elif cleaned_type in ["std::string", "string", "std::u16string"]:
        seed_data.append(0)
    elif cleaned_type == "bool":
        seed_data.extend([0x01])
    else:
        seed_data.extend([0x00])


def _append_special_value(seed_data, cleaned_type):
    """为指定类型追加特殊值到种子数据"""
    if cleaned_type in ["int8_t", "uint8_t"]:
        seed_data.extend([0x00])
    elif cleaned_type in ["int16_t", "uint16_t"]:
        seed_data.extend([0x00, 0x00])
    elif cleaned_type in [
        "int32_t",
        "int",
        "uint32_t",
        "unsigned",
        "unsigned int",
        "ProcessId",
        "UserId",
        "Uid",
        "Pid",
        "Fd",
    ]:
        seed_data.extend([0x00, 0x00, 0x00, 0x01])
    elif cleaned_type in ["int64_t", "long long"]:
        seed_data.extend([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    elif cleaned_type in [
        "uint64_t",
        "unsigned long long",
        "size_t",
        "ScreenId",
        "NodeId",
        "WindowId",
        "DisplayId",
        "Handle",
    ]:
        seed_data.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])
    elif cleaned_type == "float":
        seed_data.extend([0x00, 0x00, 0x00, 0x00])
    elif cleaned_type == "double":
        seed_data.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif cleaned_type in ["std::string", "string", "std::u16string"]:
        seed_data.append(1)
        seed_data.extend(b"A")
    elif cleaned_type == "bool":
        seed_data.extend([0x00])
    else:
        seed_data.extend([0x00])


def _generate_global_boundary_seeds(used_types, corpus_dir):
    """
    只为实际使用的类型生成全局边界值种子。
    不再为所有类型生成全量边界值。
    """
    generated_files = []

    int_types = {"int8_t", "int16_t", "int32_t", "int64_t", "int", "long long"}
    uint_types = {
        "uint8_t",
        "uint16_t",
        "uint32_t",
        "uint64_t",
        "unsigned",
        "unsigned int",
        "size_t",
        "ScreenId",
        "NodeId",
        "WindowId",
        "DisplayId",
        "Handle",
    }
    float_types = {"float", "double"}
    string_types = {"std::string", "string", "std::u16string"}

    has_int = bool(used_types & int_types)
    has_uint = bool(used_types & uint_types)
    has_float = bool(used_types & float_types)
    has_string = bool(used_types & string_types)

    if has_int:
        seed_data = bytearray()
        seed_data.append(0)
        for t in sorted(used_types & int_types):
            _append_boundary_value(seed_data, t)
        seed_path = corpus_dir / "boundary_int_min"
        with open(seed_path, "wb") as f:
            f.write(bytes(seed_data))
        generated_files.append(str(seed_path))

    if has_uint:
        seed_data = bytearray()
        seed_data.append(0)
        for t in sorted(used_types & uint_types):
            _append_boundary_value(seed_data, t)
        seed_path = corpus_dir / "boundary_uint_max"
        with open(seed_path, "wb") as f:
            f.write(bytes(seed_data))
        generated_files.append(str(seed_path))

    if has_float:
        seed_data = bytearray()
        seed_data.append(0)
        for t in sorted(used_types & float_types):
            _append_boundary_value(seed_data, t)
        seed_path = corpus_dir / "boundary_float_max"
        with open(seed_path, "wb") as f:
            f.write(bytes(seed_data))
        generated_files.append(str(seed_path))

        # float/double 特殊值（NaN, Inf）仅在有浮点类型时生成
        for fname, values in [
            ("float_nan", [0x7F, 0xC0, 0x00, 0x00]),
            ("float_inf", [0x7F, 0x80, 0x00, 0x00]),
            ("double_nan", [0x7F, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            ("double_inf", [0x7F, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        ]:
            if "float" in fname and "float" in used_types:
                seed_data = bytearray()
                seed_data.append(0)
                seed_data.extend(values)
                seed_path = corpus_dir / fname
                with open(seed_path, "wb") as f:
                    f.write(bytes(seed_data))
                generated_files.append(str(seed_path))
            elif "double" in fname and "double" in used_types:
                seed_data = bytearray()
                seed_data.append(0)
                seed_data.extend(values)
                seed_path = corpus_dir / fname
                with open(seed_path, "wb") as f:
                    f.write(bytes(seed_data))
                generated_files.append(str(seed_path))

    if has_string:
        seed_data = bytearray()
        seed_data.append(0)
        seed_data.append(0)
        seed_path = corpus_dir / "boundary_empty_string"
        with open(seed_path, "wb") as f:
            f.write(bytes(seed_data))
        generated_files.append(str(seed_path))

    return generated_files


def _generate_biz_seeds(methods, corpus_dir):
    """
    生成业务场景种子（仅针对有业务含义的方法）。
    根据方法名推断业务场景，避免无意义的笛卡尔积。
    """
    generated_files = []

    biz_patterns = {
        "screen": ["power", "mode", "color", "brightness", "rotation"],
        "display": ["power", "mode", "color", "brightness"],
        "window": ["create", "destroy", "resize", "move"],
        "surface": ["create", "destroy", "buffer"],
    }

    for idx, (name, params, ret_type) in enumerate(methods):
        name_lower = name.lower()
        matched_scenarios = []
        for biz_key, scenarios in biz_patterns.items():
            if biz_key in name_lower:
                matched_scenarios.extend(scenarios)

        if not matched_scenarios:
            continue

        for scenario in matched_scenarios[:3]:
            seed_data = bytearray()
            seed_data.append(idx)
            if params and params.lower() != "void":
                param_list = _parse_params(params)
                for param_type in param_list:
                    _append_param_seed(seed_data, param_type)
            seed_path = corpus_dir / f"biz_{scenario}_{idx}"
            with open(seed_path, "wb") as f:
                f.write(bytes(seed_data))
            generated_files.append(str(seed_path))

    return generated_files


def _generate_boundary_seeds(methods, corpus_dir):
    """
    已废弃：由 generate_semantic_seeds 统一处理。
    保留为兼容接口，实际不再调用。
    """
    return []


def _generate_special_seeds(methods, corpus_dir):
    """
    已废弃：由 generate_semantic_seeds 统一处理。
    保留为兼容接口，实际不再调用。
    """
    return []


def generate_corpus_seed_file(methods):
    """
    根据方法列表生成针对性的种子文件。
    为每个方法生成一个种子，包含该方法所需的参数数据。
    """
    seeds = []

    for idx, (name, params, ret_type) in enumerate(methods):
        seed_data = bytearray()

        # 方法选择器
        seed_data.append(idx)

        # 根据参数类型生成对应的种子数据
        if params and params.lower() != "void":
            # 解析参数并生成对应的数据
            param_list = _parse_params(params)
            for param_type in param_list:
                _append_param_seed(seed_data, param_type)

        seeds.append((f"seed_{idx}_{name}", bytes(seed_data)))

    return seeds


def _parse_params(params_str):
    """解析参数字符串，返回参数类型列表"""
    if not params_str or params_str.lower() == "void":
        return []

    parts = []
    depth = 0
    current = ""
    for ch in params_str:
        if ch in "(<{":
            depth += 1
            current += ch
        elif ch in ")>}":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())

    # 提取类型（移除变量名和默认值）
    types = []
    for part in parts:
        # 移除默认值
        part = part.split("=")[0].strip()
        # 移除变量名（最后一个token）
        tokens = part.split()
        if len(tokens) >= 2:
            type_str = " ".join(tokens[:-1])
        else:
            type_str = tokens[0] if tokens else ""
        types.append(type_str)

    return types


def _append_param_seed(seed_data, param_type):
    """根据参数类型向种子数据追加对应的二进制数据"""
    cleaned_type = _clean_type(param_type)

    if cleaned_type == "bool":
        seed_data.append(1)
    elif cleaned_type in ["int8_t", "uint8_t"]:
        seed_data.append(0x42)
    elif cleaned_type in ["int16_t", "uint16_t"]:
        seed_data.extend([0x12, 0x34])
    elif cleaned_type in ["int32_t", "int", "uint32_t", "unsigned", "unsigned int"]:
        seed_data.extend([0x12, 0x34, 0x56, 0x78])
    elif cleaned_type in [
        "int64_t",
        "long long",
        "uint64_t",
        "unsigned long long",
        "size_t",
        "ScreenId",
        "NodeId",
        "WindowId",
        "DisplayId",
        "Handle",
    ]:
        seed_data.extend([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])
    elif cleaned_type == "float":
        seed_data.extend([0x3F, 0x80, 0x00, 0x00])
    elif cleaned_type == "double":
        seed_data.extend([0x3F, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif cleaned_type in ["std::string", "string", "std::u16string"]:
        test_string = "FUZZ"
        seed_data.append(len(test_string))
        seed_data.extend(test_string.encode("utf-8"))
    elif cleaned_type in ["ProcessId", "UserId", "Uid", "Pid"]:
        seed_data.extend([0x12, 0x34, 0x56, 0x78])
    elif cleaned_type == "Fd":
        seed_data.extend([0x12, 0x34, 0x56, 0x78])
    else:
        # 对于未知类型，添加一些通用数据
        seed_data.extend([0xDE, 0xAD, 0xBE, 0xEF])


def create_fuzzer_directory(base_path, fuzzer_name):
    fuzzer_dir = Path(base_path) / fuzzer_name
    corpus_dir = fuzzer_dir / "corpus"
    fuzzer_dir.mkdir(parents=True, exist_ok=True)
    corpus_dir.mkdir(parents=True, exist_ok=True)
    return fuzzer_dir, corpus_dir


def validate_fuzzer_name(name):
    """
    验证fuzzer名称是否符合 XxxXxx_fuzzer 格式（驼峰式+下划线+fuzzer后缀）
    允许数字后缀如 XxxXxx_fuzzer1, XxxXxx_fuzzer2
    """
    if not name:
        return False, "fuzzer名称不能为空"

    # 去掉数字后缀
    base_name = re.sub(r"\d+$", "", name)

    # 检查是否以 _fuzzer 结尾
    if not base_name.endswith("_fuzzer"):
        return False, f"fuzzer名称 '{name}' 应以 '_fuzzer' 结尾"

    # 检查前缀是否为驼峰式（首字母大写，不含下划线）
    prefix = base_name[:-7]  # 去掉 "_fuzzer"
    if not prefix:
        return False, f"fuzzer名称 '{name}' 前缀为空"

    if "_" in prefix:
        return (
            False,
            f"fuzzer名称 '{name}' 前缀包含下划线，应为驼峰式命名（如 SetScreenInfo_fuzzer）",
        )

    if not prefix[0].isupper():
        return False, f"fuzzer名称 '{name}' 首字母应大写"

    if not re.match(r"^[A-Za-z][A-Za-z0-9]*$", prefix):
        return False, f"fuzzer名称 '{name}' 前缀应只包含字母和数字"

    return True, ""


def select_corpus_type(target_class, target_header, repo):
    class_lower = target_class.lower()
    header_lower = target_header.lower()

    if repo == "graphic_2d":
        if "screen" in class_lower or "display" in class_lower:
            return "rscommand"
        if "ipc" in header_lower or "proxy" in class_lower or "stub" in class_lower:
            return "ipc"
        return "rscommand"

    if repo == "graphic_3d":
        if "gltf" in class_lower or "model" in class_lower or "scene" in class_lower:
            return "gltf"
        if "shader" in class_lower or "material" in class_lower:
            return "shader"
        if "systemgraph" in class_lower or "ecs" in class_lower:
            return "systemgraph"
        if "postprocess" in class_lower or "effect" in class_lower:
            return "postprocess"
        if "ipc" in header_lower or "proxy" in class_lower:
            return "ipc"
        return "gltf"

    return "ipc"


def generate_structured_corpus(corpus_dir, corpus_type, repo):
    """
    生成结构化corpus。
    优先使用内置的 seed_generator.py，如果失败则回退到内置简单种子。
    """
    seed_gen_script = Path(__file__).parent / "seed_generator.py"

    if not seed_gen_script.exists():
        print(f"[INFO] seed_generator.py 未找到，使用内置简单种子")
        return []

    import subprocess

    try:
        # 使用 seed_generator.py 的 corpus 模式生成结构化种子
        result = subprocess.run(
            [
                sys.executable,
                str(seed_gen_script),
                "corpus",
                "--repo",
                repo,
                "--type",
                corpus_type,
                "--output",
                str(corpus_dir),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return list(corpus_dir.glob("*"))
        else:
            print(f"[WARN] seed_generator corpus 模式执行失败: {result.stderr}")
            return []
    except subprocess.TimeoutExpired:
        print("[WARN] seed_generator 执行超时")
        return []
    except Exception as e:
        print(f"[WARN] seed_generator 执行异常: {e}")
        return []


def run_verify_loop(cpp_file, check_script, max_rounds=3, extra_args=None):
    import subprocess

    error_history = []
    total_errors = 0

    for round_num in range(1, max_rounds + 1):
        print(f"\n  [Verify Round {round_num}/{max_rounds}]")

        cmd = [sys.executable, str(check_script), str(cpp_file)]
        if extra_args:
            cmd.extend(extra_args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode == 0:
            print(f"  [OK] 规范检查通过")
            # 记录通过状态
            error_history.append(
                {"round": round_num, "errors": "", "count": 0, "status": "passed"}
            )
            return (round_num, 0, error_history)

        errors = result.stdout.strip()
        error_count = len(errors.split("\n")) if errors else 0
        total_errors = error_count

        error_history.append(
            {
                "round": round_num,
                "errors": errors,
                "count": error_count,
                "status": "failed",
            }
        )

        print(f"  发现 {error_count} 个问题")
        if errors:
            for line in errors.split("\n")[:10]:
                print(f"    {line}")

        if round_num < max_rounds:
            print(f"  → 需要人工修复后继续检查")

    return (max_rounds, total_errors, error_history)


def generate_compliance_report(
    fuzzer_dir,
    fuzzer_name,
    error_history,
    output_file=None,
    target_class=None,
    namespace=None,
    header_path=None,
    methods=None,
    init_mode=None,
    corpus_type=None,
    corpus_files=None,
    manual_verify_types=None,
):
    """
    生成FUZZ用例生成和规范化检查报告（Markdown格式）
    """
    from datetime import datetime

    report_lines = []

    # ===== 报告头部 =====
    report_lines.append("# FUZZ用例生成和规范化检查报告")
    report_lines.append("")
    report_lines.append(
        f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    report_lines.append(f"- **Fuzzer**: `{fuzzer_name}`")
    if header_path:
        report_lines.append(f"- **测试文件**: `{header_path}`")
    if namespace:
        report_lines.append(f"- **命名空间**: `{namespace}`")
    report_lines.append("")

    # ===== 一、测试范围 =====
    report_lines.append("## 一、测试范围")
    report_lines.append("")

    if methods:
        # 分类接口
        tested_methods = []
        skipped_methods = []

        for method in methods:
            method_name, params, return_type = method
            has_params = params and params.strip() and params.strip() != "void"
            if has_params:
                tested_methods.append(method)
            else:
                skipped_methods.append(method)

        # 计算覆盖率
        coverage_rate = (len(tested_methods) / len(methods) * 100) if methods else 0

        report_lines.append(f"- **总接口数**: {len(methods)}")
        report_lines.append(f"- **已测试接口数**: {len(tested_methods)}")
        report_lines.append(
            f"- **跳过接口数**: {len(skipped_methods)} (无参数，无需FUZZ测试)"
        )
        report_lines.append(
            f"- **接口覆盖率**: {coverage_rate:.1f}% ({len(tested_methods)}/{len(methods)})"
        )
        report_lines.append("")

        # 已测试接口
        if tested_methods:
            report_lines.append("### 已测试接口")
            report_lines.append("")
            report_lines.append("| 序号 | 接口名称 | 参数 | 返回类型 | 参数构造方式 |")
            report_lines.append("|------|----------|------|----------|--------------|")
            for i, (method_name, params, return_type) in enumerate(tested_methods, 1):
                param_display = params[:60] + "..." if len(params) > 60 else params
                # 判断参数构造方式
                construct_method = "FDP.ConsumeIntegral<T>()"
                if "std::string" in params or "string" in params:
                    construct_method = "fdp.ConsumeRandomLengthString(256)"
                elif "vector" in params:
                    construct_method = "循环: fdp.ConsumeIntegral<uint8_t>() % 32次"
                elif "bool" in params.lower():
                    construct_method = "fdp.ConsumeBool()"
                elif "float" in params.lower() or "double" in params.lower():
                    construct_method = "fdp.ConsumeFloatingPoint<T>()"
                elif "enum" in params.lower() or "Enum" in params:
                    construct_method = (
                        "static_cast<Enum>(fdp.ConsumeIntegral<uint8_t>())"
                    )
                elif "Rect" in params or "struct" in params.lower():
                    construct_method = "字段级: 逐个ConsumeIntegral构造"
                elif "sptr" in params or "shared_ptr" in params:
                    construct_method = "new/mock构造"

                report_lines.append(
                    f"| {i} | `{method_name}` | `{param_display}` | `{return_type}` | {construct_method} |"
                )
            report_lines.append("")

            # 复杂参数构造说明
            report_lines.append("### 复杂参数构造说明")
            report_lines.append("")
            report_lines.append("| 参数类型 | 构造方式 | 说明 |")
            report_lines.append("|----------|----------|------|")
            report_lines.append(
                "| `std::string` | `fdp.ConsumeRandomLengthString(256)` | 随机长度字符串，最大256字节 |"
            )
            report_lines.append(
                "| `std::vector<T>` | 循环消费 | 先消费uint8_t取模确定长度(0-31)，再循环消费元素 |"
            )
            report_lines.append(
                "| `enum` | `static_cast<Enum>(fdp.ConsumeIntegral<uint8_t>())` | 使用uint8_t提取，不取模，保留非法值覆盖 |"
            )
            report_lines.append(
                "| `struct/Rect` | 字段级构造 | 为每个字段单独调用ConsumeIntegral或ConsumeFloatingPoint |"
            )
            report_lines.append("| `bool` | `fdp.ConsumeBool()` | 直接消费布尔值 |")
            report_lines.append(
                "| `float/double` | `fdp.ConsumeFloatingPoint<T>()` | 消费浮点数 |"
            )
            report_lines.append(
                "| `sptr<T>` | `new MockT()` 或 `new T()` | 自动构造智能指针，Mock抽象类或实例化具体类 |"
            )
            report_lines.append("")

        # 跳过接口
        if skipped_methods:
            report_lines.append("### 跳过接口 (无参数)")
            report_lines.append("")
            report_lines.append("| 接口名称 | 返回类型 | 跳过原因 |")
            report_lines.append("|----------|----------|----------|")
            for method_name, params, return_type in skipped_methods:
                report_lines.append(
                    f"| `{method_name}()` | `{return_type}` | 无参数，使用单元测试覆盖 |"
                )
            report_lines.append("")
            report_lines.append(
                "> **开发提示**: 无参数接口请在代码中使用 `// LCOV_EXCL_START` 和 `// LCOV_EXCL_STOP` 包裹，避免影响覆盖率统计"
            )
            report_lines.append("```cpp")
            report_lines.append("// LCOV_EXCL_START")
            report_lines.append("void DoGetVersion(FuzzedDataProvider& fdp) {")
            report_lines.append("    // 无参数接口，使用单元测试覆盖")
            report_lines.append("    g_instance->GetVersion();")
            report_lines.append("}")
            report_lines.append("// LCOV_EXCL_STOP")
            report_lines.append("```")
            report_lines.append("")

    # ===== 二、种子(Corpus)生成 =====
    report_lines.append("## 二、种子(Corpus)生成")
    report_lines.append("")

    if corpus_type:
        report_lines.append(f"**种子类型**: `{corpus_type}`")

    if corpus_files:
        report_lines.append(f"**种子数量**: {len(corpus_files)}个")
        report_lines.append("")

        # 分类统计
        categories = {"valid": 0, "boundary": 0, "empty": 0, "invalid": 0, "other": 0}
        for seed_file in corpus_files:
            seed_name = os.path.basename(seed_file).lower()
            if "valid" in seed_name:
                categories["valid"] += 1
            elif "boundary" in seed_name or "max" in seed_name or "min" in seed_name:
                categories["boundary"] += 1
            elif "empty" in seed_name or "zero" in seed_name:
                categories["empty"] += 1
            elif "invalid" in seed_name or "error" in seed_name:
                categories["invalid"] += 1
            else:
                categories["other"] += 1

        report_lines.append("**种子分类**:")
        report_lines.append("")
        report_lines.append("| 类型 | 数量 | 说明 |")
        report_lines.append("|------|------|------|")
        if categories["valid"] > 0:
            report_lines.append(
                f"| 合法值 | {categories['valid']} | 正常业务场景数据 |"
            )
        if categories["boundary"] > 0:
            report_lines.append(
                f"| 边界值 | {categories['boundary']} | 最大/最小/临界值 |"
            )
        if categories["empty"] > 0:
            report_lines.append(
                f"| 空值 | {categories['empty']} | 零值/空字符串/空容器 |"
            )
        if categories["invalid"] > 0:
            report_lines.append(
                f"| 异常值 | {categories['invalid']} | 非法输入/畸形数据 |"
            )
        if categories["other"] > 0:
            report_lines.append(f"| 其他 | {categories['other']} | 特殊场景 |")
        report_lines.append("")

        report_lines.append(
            "**生成策略**: 结构化生成(合法格式) + 边界值覆盖(最大/最小/零值) + 特殊值注入(null/异常长度) + 组合覆盖(笛卡尔积)"
        )
        report_lines.append("")
    else:
        report_lines.append("**种子状态**: 使用默认初始化种子")
        report_lines.append("")

    # ===== 三、规范检查结果 =====
    report_lines.append("## 三、规范检查结果")
    report_lines.append("")

    if not error_history:
        report_lines.append("### 自动检查结果")
        report_lines.append("")
        report_lines.append("**状态**: ❌ 未执行自动规范检查")
        report_lines.append("")
        report_lines.append("**警告**: 提交前**必须**运行规范检查，请执行:")
        report_lines.append(f"```bash")
        report_lines.append(
            f"python3 tools/fuzz_check.py {fuzzer_dir}/{fuzzer_name}.cpp"
        )
        report_lines.append(f"```")
    else:
        # 检查最后一轮是否通过
        last_record = error_history[-1]
        if last_record.get("status") == "passed":
            report_lines.append("### 自动检查结果 (22条)")
            report_lines.append("")
            report_lines.append("**状态**: ✅ 全部通过")
            report_lines.append(
                f"**检查轮次**: {last_record['round']}/{len(error_history)}"
            )
            report_lines.append("")

            # 规则通过表格
            report_lines.append("**自动检查规则明细**:")
            report_lines.append("")
            report_lines.append("| 规则编号 | 规则名称 | 状态 | 说明 |")
            report_lines.append("|----------|----------|------|------|")
            report_lines.append(
                "| 规则001 | 目标API FUZZ适用性评估 | ✅ | 无参数/固定参数API已过滤 |"
            )
            report_lines.append(
                "| 规则002 | 关键有参API覆盖完整性 | ✅ | 所有有参API已覆盖 |"
            )
            report_lines.append(
                "| 规则003 | 变异数据使用检测 | ✅ | 使用FuzzedDataProvider |"
            )
            report_lines.append("| 规则004 | 变异数据复用检测 | ✅ | 无复用问题 |")
            report_lines.append("| 规则005 | 复杂参数构造合理性 | ✅ | 参数构造正确 |")
            report_lines.append("| 规则006 | 单文件接口数量限制 | ✅ | 接口数量合规 |")
            report_lines.append(
                "| 规则007 | IPC接口测试规范 | ✅ | 非IPC或已正确测试 |"
            )
            report_lines.append("| 规则008 | 复杂函数安全性 | ✅ | 无递归/回调问题 |")
            report_lines.append(
                "| 规则009 | FUZZ Driver安全性 | ✅ | 无内存泄漏/溢出 |"
            )
            report_lines.append("| 规则010 | size参数误用检测 | ✅ | size使用正确 |")
            report_lines.append(
                "| 规则013 | 枚举值构造优化 | ✅ | 使用uint8而非uint32 |"
            )
            report_lines.append("| 规则014 | 固定参数使用检测 | ✅ | 固定参数已识别 |")
            report_lines.append("| 规则016 | 数据类型匹配性 | ✅ | 类型匹配正确 |")
            report_lines.append(
                "| 规则017 | 随机函数禁用检测 | ✅ | 使用FDP而非random |"
            )
            report_lines.append(
                "| 规则018 | data指针直接使用检测 | ✅ | 无直接解引用 |"
            )
            report_lines.append(
                "| 规则019 | 全局变量初始化检查 | ✅ | 全局变量已初始化 |"
            )
            report_lines.append("| 规则A | 头文件规范 | ✅ | 保护宏/系统头文件正确 |")
            report_lines.append(
                "| 规则B | BUILD.gn规范 | ✅ | ohos_fuzztest()配置正确 |"
            )
            report_lines.append("| 规则C | project.xml规范 | ✅ | XML声明/根元素正确 |")
            report_lines.append("| 规则D | 目录名/文件名一致性 | ✅ | 命名格式正确 |")
            report_lines.append(
                "| 规则E | .cpp文件头文件完整性 | ✅ | 头文件包含完整 |"
            )
            report_lines.append("| 规则F | 版权头规范 | ✅ | 版权信息正确 |")
            report_lines.append(
                "| 规则G | BUILD.gn目标命名规范 | ✅ | 驼峰式+FuzzTest后缀 |"
            )
            report_lines.append("")
            report_lines.append(
                "| **统计** | **22条自动检查规则** | **✅ 全部通过** | - |"
            )
        else:
            report_lines.append("### 自动检查结果")
            report_lines.append("")
            report_lines.append("**状态**: ❌ 未通过")
            report_lines.append(
                f"**总问题数**: {sum(r['count'] for r in error_history)}"
            )
            report_lines.append("")

            report_lines.append("**问题详情**:")
            report_lines.append("")
            report_lines.append("| 轮次 | 状态 | 问题数 | 详情 |")
            report_lines.append("|------|------|--------|------|")
            for record in error_history:
                status = "✅ 通过" if record.get("status") == "passed" else "❌ 失败"
                errors_summary = (
                    record["errors"][:50] + "..."
                    if len(record["errors"]) > 50
                    else record["errors"]
                )
                errors_summary = errors_summary.replace("\n", "; ")
                report_lines.append(
                    f"| {record['round']} | {status} | {record['count']} | {errors_summary} |"
                )
    report_lines.append("")

    # ===== 四、人工审查确认 =====
    report_lines.append("## 四、人工审查确认")
    report_lines.append("")
    report_lines.append("以下4条规则无法通过自动化工具完全验证，需要提交者人工确认:")
    report_lines.append("")
    report_lines.append("| 规则 | 名称 | 严重程度 | 检查项 | 状态 |")
    report_lines.append("|------|------|----------|--------|------|")
    report_lines.append(
        "| 规则011 | 系统安全准入条件 | 🔴 高危 | 目标API是否需要特定权限/UID？ | [ ] 待确认 |"
    )
    report_lines.append(
        "| 规则012 | 目标API内部分支覆盖 | 🔴 高危 | 是否覆盖主要分支逻辑？ | [ ] 待确认 |"
    )
    report_lines.append(
        "| 规则015 | 中间产物合法性 | 🟡 中危 | 种子数据格式是否符合预期？ | [ ] 待确认 |"
    )
    report_lines.append(
        "| 规则016 | 类型匹配检查 | 🟡 中危 | 复杂类型参数是否与API签名一致？ | [ ] 待确认 |"
    )
    report_lines.append("")
    report_lines.append(
        "> **说明**: 规则016工具已检查基础类型匹配，复杂类型(结构体/类)需要人工确认。"
    )
    report_lines.append("")

    # 添加需要人工确认的复杂类型列表
    if manual_verify_types:
        report_lines.append("### 需要人工确认的复杂类型")
        report_lines.append("")
        report_lines.append(
            "以下类型无法自动生成合理的构造代码，需要开发人员根据业务逻辑手动实现："
        )
        report_lines.append("")
        report_lines.append("| 序号 | 类型名称 | 建议构造方式 | 状态 |")
        report_lines.append("|------|----------|--------------|------|")
        for i, t in enumerate(manual_verify_types, 1):
            report_lines.append(
                f"| {i} | `{t}` | 请参考业务代码或TDD测试用例实现 | [ ] 待确认 |"
            )
        report_lines.append("")
        report_lines.append(
            "> **提示**: 这些类型在生成的代码中已用 `// TODO[NEED_MANUAL_VERIFY]` 标记，请查找并替换为合理的构造逻辑。"
        )
        report_lines.append("")

    # ===== 报告尾部 =====
    report_lines.append("---")
    report_lines.append("*报告由 fuzz_generator.py 自动生成*")

    report_content = "\n".join(report_lines)

    if output_file:
        Path(output_file).write_text(report_content, encoding="utf-8")
        print(f"合规报告已保存: {output_file}")

    return report_content


def main():
    parser = argparse.ArgumentParser(
        description="FUZZ测试用例快速生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动从头文件提取 public 方法并生成
  python3 fuzz_generator.py -n SetScreenInfo_fuzzer -N Rosen -c RSInterfaces \
      -H "rosen/modules/render_service_client/core/ui/rs_ui_director.h" \
      --init-mode singleton -p ./test/fuzztest/

    # 命令行生成（工厂模式）
  python3 fuzz_generator.py -n RSTransitionEffect_fuzzer -N Rosen -c RSTransitionEffect \
      -H "animation/rs_transition_effect.h" \
      --init-mode factory -p ./test/fuzztest/
        """,
    )

    parser.add_argument(
        "-n", "--name", required=True, help="fuzzer名称（如：SetScreenInfo_fuzzer）"
    )
    parser.add_argument(
        "-N", "--namespace", required=True, help="命名空间（如：Rosen）"
    )
    parser.add_argument(
        "-c",
        "--class",
        dest="target_class",
        required=True,
        help="目标类名（如：RSInterfaces）",
    )
    parser.add_argument(
        "-H",
        "--header",
        required=True,
        help="目标头文件路径（如：rosen/.../rs_interfaces.h）",
    )
    parser.add_argument("-p", "--path", default="./", help="输出路径（默认：当前目录）")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互式模式")
    parser.add_argument(
        "--init-mode",
        default=INIT_MODE_NONE,
        choices=VALID_INIT_MODES,
        help="初始化模式: singleton(单例), factory(工厂), none(按需创建, 默认)",
    )
    parser.add_argument(
        "--module-path", default="graphic_2d/graphic_2d", help="module_output_path"
    )
    parser.add_argument(
        "--full-path",
        default="foundation/graphic/graphic_2d/rosen/test/render_service/fuzztest",
        help="fuzz_config_file完整路径",
    )
    parser.add_argument(
        "--include1",
        default="foundation/graphic/graphic_2d/rosen/modules/render_service_client/core",
        help="include_dirs路径1",
    )
    parser.add_argument(
        "--include2",
        default="foundation/graphic/graphic_2d/rosen/modules/render_service_base/include",
        help="include_dirs路径2",
    )
    parser.add_argument(
        "--dep-path",
        default="foundation/graphic/graphic_2d/rosen/modules/render_service_client",
        help="deps路径",
    )
    parser.add_argument(
        "--dep-target", default="librender_service_client", help="deps目标名"
    )
    parser.add_argument(
        "--corpus-type",
        default="auto",
        choices=[
            "gltf",
            "shader",
            "systemgraph",
            "postprocess",
            "rscommand",
            "ipc",
            "auto",
        ],
        help="corpus类型，自动生成对应的结构化种子 (默认: auto自动选择)",
    )
    parser.add_argument(
        "--repo",
        default="graphic_2d",
        choices=["graphic_2d", "graphic_3d"],
        help="目标仓库，用于选择corpus生成器 (默认: graphic_2d)",
    )
    parser.add_argument(
        "--max-fix-rounds",
        default=3,
        type=int,
        help="Verify阶段自动修复的最大轮数 (默认: 3)",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")

    args = parser.parse_args()

    # 只要显式指定了 -i，就进入交互式；否则按命令行参数处理
    if args.interactive:
        print("=" * 60)
        print("FUZZ测试用例快速生成工具")
        print("=" * 60)
        print()

        args.name = input("1. fuzzer名称（如：SetScreenInfo_fuzzer）: ").strip()
        if not args.name:
            print("错误: fuzzer名称不能为空")
            sys.exit(1)

        args.namespace = input("2. 命名空间（如：Rosen）: ").strip()
        if not args.namespace:
            print("错误: 命名空间不能为空")
            sys.exit(1)

        args.target_class = input("3. 目标类名（如：RSInterfaces）: ").strip()
        if not args.target_class:
            print("错误: 目标类名不能为空")
            sys.exit(1)

        args.header = input(
            "4. 目标头文件路径（如：rosen/.../rs_interfaces.h）: "
        ).strip()
        if not args.header:
            args.header = f"path/to/{args.target_class.lower()}.h"

        print()
        print("  初始化模式:")
        print("    singleton - 通过 GetInstance() 获取全局单例")
        print("    factory   - 通过 Create() 工厂方法创建实例")
        print("    none      - 无全局实例，DoXXX中按需创建（默认）")
        init_input = (
            input("5. 初始化模式（singleton/factory/none，默认：none）: ")
            .strip()
            .lower()
        )
        if init_input in VALID_INIT_MODES:
            args.init_mode = init_input
        else:
            args.init_mode = INIT_MODE_NONE

        args.path = input(f"6. 输出路径（默认：{args.path}）: ").strip() or args.path

        print()
        print("生成配置：")
        print(f"  fuzzer名称:    {args.name}")
        print(f"  命名空间:      {args.namespace}")
        print(f"  目标类:        {args.target_class}")
        print(f"  头文件:        {args.header}")
        print(f"  初始化模式:    {args.init_mode}")
        print(f"  输出路径:      {args.path}")
        print()

        confirm = input("确认生成？(y/n): ").strip().lower()
        if confirm != "y":
            print("已取消")
            return

    valid, msg = validate_fuzzer_name(args.name)
    if not valid:
        print(f"错误: {msg}")
        sys.exit(1)

    header_include = f'"{args.header.strip().strip(chr(34)).strip(chr(39))}"'

    # 自动解析头文件中的 public 方法
    # IPC stub 模式需要包含无参方法（OnRemoteRequest 需要覆盖所有接口）
    is_ipc_stub, stub_class_name = _detect_ipc_stub(args.header, args.target_class)
    include_no_params = bool(is_ipc_stub)
    methods = parse_header_methods(
        args.header, args.target_class, include_no_params=include_no_params
    )
    if not methods:
        print("警告: 未能从头文件中解析出 public 方法，将生成仅含 2 个占位方法的骨架")
        methods = [
            ("Method1", "uint32_t param1, uint32_t param2", "void"),
            ("Method2", "uint64_t param", "void"),
        ]
    else:
        print(f"从头文件解析到 {len(methods)} 个 public 方法：")
        for name, params, ret in methods:
            print(f"  - {ret} {name}({params})")

    if is_ipc_stub:
        print(f"  检测到 IPC Stub 类，stub_class_name = {stub_class_name}")

    # 规则3: 如果方法数超过10个，自动拆分为多个fuzzer文件
    MAX_METHODS_PER_FUZZER = 10
    if len(methods) > MAX_METHODS_PER_FUZZER:
        print(f"\n方法数超过 {MAX_METHODS_PER_FUZZER} 个，将自动拆分为多个 fuzzer 文件")

        # 计算需要多少个fuzzer文件
        num_fuzzers = (
            len(methods) + MAX_METHODS_PER_FUZZER - 1
        ) // MAX_METHODS_PER_FUZZER
        print(
            f"将生成 {num_fuzzers} 个 fuzzer 文件，每个最多 {MAX_METHODS_PER_FUZZER} 个接口\n"
        )

        # 生成多个fuzzer文件
        for i in range(num_fuzzers):
            start_idx = i * MAX_METHODS_PER_FUZZER
            end_idx = min((i + 1) * MAX_METHODS_PER_FUZZER, len(methods))
            batch_methods = methods[start_idx:end_idx]

            # 生成fuzzer名称（如：RSScreenManager_fuzzer1, RSScreenManager_fuzzer2）
            if i == 0:
                batch_fuzzer_name = args.name
            else:
                batch_fuzzer_name = f"{args.name}{i}"

            print(f"生成 fuzzer {i + 1}/{num_fuzzers}: {batch_fuzzer_name}")
            print(
                f"  包含接口 {start_idx + 1}-{end_idx}: {[m[0] for m in batch_methods]}"
            )

            # 创建目录并生成文件
            batch_fuzzer_dir, batch_corpus_dir = create_fuzzer_directory(
                args.path, batch_fuzzer_name
            )

            if is_ipc_stub:
                cpp_content, batch_manual_verify_types = generate_ipc_stub_fuzzer_cpp(
                    batch_fuzzer_name,
                    args.namespace,
                    args.target_class,
                    header_include,
                    batch_methods,
                    args.init_mode,
                    header_path=args.header,
                    stub_class_name=stub_class_name,
                    total_method_count=len(methods),
                )
            else:
                cpp_content, batch_manual_verify_types = generate_fuzzer_cpp(
                    batch_fuzzer_name,
                    args.namespace,
                    args.target_class,
                    header_include,
                    batch_methods,
                    args.init_mode,
                    header_path=args.header,
                )
            files_to_create = [
                (f"{batch_fuzzer_name}.cpp", cpp_content),
                (f"{batch_fuzzer_name}.h", generate_fuzzer_h(batch_fuzzer_name)),
                (
                    "BUILD.gn",
                    generate_build_gn(
                        batch_fuzzer_name,
                        args.module_path,
                        args.full_path,
                        args.include1,
                        args.include2,
                        args.dep_path,
                        args.dep_target,
                    ),
                ),
                ("project.xml", generate_project_xml()),
            ]

            current_year = str(datetime.now().year)
            for filename, content in files_to_create:
                content = content.replace("2026", current_year)
                filepath = batch_fuzzer_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"    生成: {filepath}")

            # 生成语义化种子
            print(f"\n    生成语义化种子...")
            seed_files = generate_semantic_seeds(batch_methods, batch_corpus_dir)
            for seed_file in seed_files:
                print(f"    生成种子: {seed_file}")

            # Stage 5 - Verify (规范审查)
            cpp_file = batch_fuzzer_dir / f"{batch_fuzzer_name}.cpp"
            print(f"\n  [Stage 5 - Verify 规范审查]")
            print(f"  检查文件: {cpp_file}")
            print("  " + "-" * 60)

            check_script = Path(__file__).parent / "fuzz_check.py"
            error_history = []

            if check_script.exists():
                batch_method_names = [m[0] for m in batch_methods]
                pass_rounds, total_errors, error_history = run_verify_loop(
                    cpp_file,
                    check_script,
                    args.max_fix_rounds,
                    extra_args=["--expected-methods", ",".join(batch_method_names)],
                )
            else:
                print(f"  检查工具未找到: {check_script}")

            # Stage 6 - Review (合规报告)
            print(f"\n  [Stage 6 - Review 合规报告]")
            report_file = batch_fuzzer_dir / "FUZZ用例生成和规范化检查报告.md"
            generate_compliance_report(
                batch_fuzzer_dir,
                batch_fuzzer_name,
                error_history,
                report_file,
                target_class=args.target_class,
                namespace=args.namespace,
                header_path=args.header,
                methods=batch_methods,
                init_mode=args.init_mode,
                corpus_type=None,
                corpus_files=seed_files if "seed_files" in locals() else None,
                manual_verify_types=batch_manual_verify_types,
            )

            print()
    else:
        # 方法数不超过10个，生成单个fuzzer文件
        fuzzer_dir, corpus_dir = create_fuzzer_directory(args.path, args.name)
        print(f"创建目录: {fuzzer_dir}")

        if is_ipc_stub:
            single_cpp_content, single_manual_verify_types = (
                generate_ipc_stub_fuzzer_cpp(
                    args.name,
                    args.namespace,
                    args.target_class,
                    header_include,
                    methods,
                    args.init_mode,
                    header_path=args.header,
                    stub_class_name=stub_class_name,
                )
            )
        else:
            single_cpp_content, single_manual_verify_types = generate_fuzzer_cpp(
                args.name,
                args.namespace,
                args.target_class,
                header_include,
                methods,
                args.init_mode,
                header_path=args.header,
            )
        files_to_create = [
            (f"{args.name}.cpp", single_cpp_content),
            (f"{args.name}.h", generate_fuzzer_h(args.name)),
            (
                "BUILD.gn",
                generate_build_gn(
                    args.name,
                    args.module_path,
                    args.full_path,
                    args.include1,
                    args.include2,
                    args.dep_path,
                    args.dep_target,
                ),
            ),
            ("project.xml", generate_project_xml()),
        ]

        current_year = str(datetime.now().year)
        for filename, content in files_to_create:
            content = content.replace("2026", current_year)
            filepath = fuzzer_dir / filename
            filepath.write_text(content, encoding="utf-8")
            print(f"  生成: {filepath}")

        # Stage 4 - Corpus (种子构造)
        print(f"\n  [Stage 4 - Corpus 种子构造]")

        # 确定 corpus 类型
        if args.corpus_type == "auto":
            corpus_type = select_corpus_type(args.target_class, args.header, args.repo)
            print(f"  自动选择 corpus 类型: {corpus_type}")
        else:
            corpus_type = args.corpus_type
            print(f"  使用指定 corpus 类型: {corpus_type}")

        # 使用 seed_generator.py 生成结构化种子
        corpus_files = generate_structured_corpus(corpus_dir, corpus_type, args.repo)

        if not corpus_files:
            print(f"  使用内置简单种子...")
            seed_files = generate_semantic_seeds(methods, corpus_dir)
            for seed_file in seed_files:
                print(f"    生成种子: {seed_file}")
        else:
            print(f"  生成 {len(corpus_files)} 个结构化种子文件")

        print()
        print("=" * 60)
        print("生成完成！")
        print("=" * 60)

        cpp_file = fuzzer_dir / f"{args.name}.cpp"

        # Stage 5 - Verify (规范审查)
        print(f"\n  [Stage 5 - Verify 规范审查]")
        print(f"  检查文件: {cpp_file}")
        print("-" * 60)

        check_script = Path(__file__).parent / "fuzz_check.py"
        error_history = []

        if check_script.exists():
            pass_rounds, total_errors, error_history = run_verify_loop(
                cpp_file, check_script, args.max_fix_rounds
            )
        else:
            print(f"  检查工具未找到: {check_script}")

        # Stage 6 - Review (合规报告)
        print(f"\n  [Stage 6 - Review 合规报告]")
        report_file = fuzzer_dir / "FUZZ用例生成和规范化检查报告.md"

        # 确定种子文件列表
        all_seed_files = []
        if corpus_files:
            all_seed_files = [str(f) for f in corpus_files]

        generate_compliance_report(
            fuzzer_dir,
            args.name,
            error_history,
            report_file,
            target_class=args.target_class,
            namespace=args.namespace,
            header_path=args.header,
            methods=methods,
            init_mode=args.init_mode,
            corpus_type=corpus_type,
            corpus_files=all_seed_files if all_seed_files else None,
            manual_verify_types=single_manual_verify_types,
        )

        print()
        print("下一步：")
        print(f"  1. 查看合规报告: {fuzzer_dir / 'FUZZ用例生成和规范化检查报告.md'}")
        print(f"  2. 编辑 {fuzzer_dir / (args.name + '.cpp')}，调整 TODO 参数类型")
        print(f"  3. 编辑 {fuzzer_dir / 'BUILD.gn'}，配置正确的 include_dirs 和 deps")
        print(
            f"  4. 运行检查: python3 tools/fuzz_check.py {fuzzer_dir / (args.name + '.cpp')}"
        )
        print()


if __name__ == "__main__":
    main()
