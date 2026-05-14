#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FUZZ种子与语料生成工具 (增强版 v2.0)
合并了 seed_generator 和 corpus_generator 的功能

支持两种模式：
1. seed模式 - 生成通用种子数据（二进制、JSON、JPEG等）
2. corpus模式 - 生成领域特定结构化语料（RSCommand、GLTF、Shader等）

增强特性：
- 完整边界值集合（含浮点特殊值 NaN/Inf/-Inf）
- 智能语义推断（基于参数名称如 screenId、width、callback）
- 增强字典生成（魔数、协议关键字、安全测试字符串）
- 笛卡尔积组合种子生成
- 畸形数据测试种子

用法：
    # Seed模式 - 通用种子
    python3 seed_generator.py seed -t json -o corpus/init.json
    python3 seed_generator.py seed --analyze path/to/fuzzer.cpp -o corpus/

    # Corpus模式 - 领域特定语料
    python3 seed_generator.py corpus --repo graphic_2d --type rscommand --output ./corpus/
    python3 seed_generator.py corpus --repo graphic_3d --type gltf --output ./corpus/
"""

import argparse
import sys
import os
import io
import json
import struct
import re
import math
import itertools
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Callable

# Windows兼容性：强制UTF-8编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    os.environ["PYTHONIOENCODING"] = "utf-8"


# ============================================================================
# 边界值与特殊值字典
# ============================================================================

BOUNDARY_VALUES = {
    "int8_t": [-128, -1, 0, 1, 64, 127],
    "uint8_t": [0, 1, 127, 128, 255],
    "int16_t": [-32768, -1, 0, 1, 32767],
    "uint16_t": [0, 1, 32768, 65535],
    "int32_t": [-2147483648, -1, 0, 1, 2147483647],
    "uint32_t": [0, 1, 2147483648, 4294967295],
    "int64_t": [-9223372036854775808, -1, 0, 1, 9223372036854775807],
    "uint64_t": [0, 1, 9223372036854775808, 18446744073709551615],
    "float": [0.0, -0.0, 1.0, -1.0, 1.175494e-38, 3.402823e38],
    "double": [0.0, -0.0, 1.0, -1.0, 2.225074e-308, 1.797693e308],
}

FLOAT_SPECIAL_BYTES = {
    "nan": b"\x00\x00\xc0\x7f",
    "snan": b"\x00\x00\xc0\xff",
    "inf": b"\x00\x00\x80\x7f",
    "neg_inf": b"\x00\x00\x80\xff",
    "denorm_min": b"\x00\x00\x00\x01",
    "neg_denorm_min": b"\x00\x00\x00\x81",
}

DOUBLE_SPECIAL_BYTES = {
    "nan": b"\x00\x00\x00\x00\x00\x00\xf8\x7f",
    "inf": b"\x00\x00\x00\x00\x00\x00\xf0\x7f",
    "neg_inf": b"\x00\x00\x00\x00\x00\x00\xf0\xff",
    "denorm_min": b"\x00\x00\x00\x00\x00\x00\x00\x01",
}

SEMANTIC_HINTS = {
    "size": [0, 1, 1024, 4096, 65535, 0xFFFFFF],
    "width": [0, 1, 320, 640, 1080, 1920, 3840, 4096, 8192],
    "height": [0, 1, 240, 480, 720, 1080, 2160, 4096, 8192],
    "id": [0, 1, 0xFFFFFFFF, 0xDEADBEEF],
    "handle": [0, 1, 0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF],
    "fd": [0, 1, -1, 1024],
    "screenid": [0, 1, 0xFFFFFFFF],
    "nodeid": [0, 1, 0xFFFFFFFFFFFFFFFF],
    "windowid": [0, 1, 0xFFFFFFFF],
    "displayid": [0, 1, 0xFFFFFFFF],
    "processid": [0, 1, 0xFFFF],
    "userid": [0, 1, 1000, 0xFFFF],
    "pid": [0, 1, 0xFFFF],
    "uid": [0, 1, 1000, 0xFFFF],
    "path": ["", "/dev/null", "/tmp/test", "/data/local/tmp", "."],
    "file": ["", "test.txt", "config.json", "../../../etc/passwd"],
    "url": ["", "http://test", "file:///dev/null"],
    "uri": ["", "content://test", "file:///test"],
    "timeout": [0, 1, 1000, 10000, 0xFFFFFFFF, -1],
    "delay": [0, 1, 100, 1000, 0xFFFFFFFF],
    "count": [0, 1, 10, 100, 0x7FFFFFFF, 0xFFFFFFFF],
    "num": [0, 1, 10, 100, 0x7FFFFFFF],
    "index": [0, 1, -1, 0x7FFFFFFF],
    "offset": [0, 1, 1024, 0xFFFFFFFF, -1],
    "flag": [0, 1, 0xFF, 0xFFFFFFFF],
    "mode": [0, 1, 2, 0xFF, 0xFFFFFFFF],
    "option": [0, 1, 0xFF, 0xFFFFFFFF],
    "callback": [0, 0xDEADBEEF, 0xFFFFFFFF],
    "handler": [0, 0xDEADBEEF, 0xFFFFFFFF],
    "listener": [0, 0xDEADBEEF, 0xFFFFFFFF],
    "rate": [0, 30, 60, 90, 120, 144, 240],
    "fps": [0, 30, 60, 90, 120, 144],
    "refreshrate": [0, 30, 60, 90, 120, 144],
    "rotation": [0, 90, 180, 270],
    "scale": [0.0, 0.5, 1.0, 2.0, -1.0],
    "alpha": [0.0, 0.5, 1.0, -0.1, 1.1],
    "color": [0, 0xFFFFFFFF, 0xFF000000, 0x00FFFFFF],
    "x": [0, 100, 1000, -100, 0x7FFFFFFF],
    "y": [0, 100, 1000, -100, 0x7FFFFFFF],
    "z": [0, 100, 1000, -100, 0x7FFFFFFF],
    "name": ["", "test", "default", "A" * 256],
    "type": [0, 1, 0xFF],
    "version": [0, 1, 2, 0xFF],
    "status": [0, 1, 0xFF],
    "error": [0, -1, 0x7FFFFFFF],
    "result": [0, -1, 1],
    "value": [0, 1, -1, 0x7FFFFFFF, 0xFFFFFFFF],
    "key": [0, 1, 0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF],
    "token": [0, 1, 0xFFFFFFFFFFFFFFFF],
}

SECURITY_TEST_STRINGS = [
    b"",
    b"%s%s%s%s%s%s",
    b"%n%n%n%n",
    b"%x%x%x%x",
    b"%p%p%p%p",
    b"../../../etc/passwd",
    b"..\\..\\..\\windows\\system32",
    b"<script>alert(1)</script>",
    b"'; DROP TABLE users--",
    b"{{}}}",
    b"${{7*7}}",
    b"\x00\x00\x00\x00",
    b"\xff\xff\xff\xff",
    b"A" * 4096,
    b"A" * 65536,
    b"\xef\xbf\xbf",
    b"\xed\xa0\x80\xed\xb2\x80",
]

MAGIC_NUMBERS = {
    "png": b"\x89PNG\r\n\x1a\n",
    "jpeg": b"\xff\xd8\xff",
    "gif87a": b"GIF87a",
    "gif89a": b"GIF89a",
    "bmp": b"BM",
    "webp": b"RIFF",
    "pdf": b"%PDF-",
    "zip": b"PK\x03\x04",
    "gz": b"\x1f\x8b",
    "tar": b"ustar",
    "elf": b"\x7fELF",
    "xml": b"<?xml",
    "json": b'{"',
    "http": b"HTTP/1.",
    "glb": b"glTF",
}

PROTOCOL_KEYWORDS = {
    "gltf": [
        "asset",
        "scene",
        "scenes",
        "nodes",
        "meshes",
        "materials",
        "textures",
        "images",
        "accessors",
        "bufferViews",
        "buffers",
        "animations",
        "skins",
        "cameras",
        "lights",
        "extensions",
        "extras",
        "KHR_draco_mesh_compression",
        "KHR_materials_pbrSpecularGlossiness",
        "KHR_materials_unlit",
        "KHR_lights_punctual",
        "KHR_texture_transform",
    ],
    "rscommand": [
        "type",
        "subType",
        "nodeId",
        "payload",
        "commandCount",
        "timestamp",
        "syncId",
        "followType",
        "mergeType",
    ],
    "shader": [
        "attribute",
        "uniform",
        "varying",
        "in",
        "out",
        "layout",
        "precision",
        "highp",
        "mediump",
        "lowp",
        "float",
        "int",
        "vec2",
        "vec3",
        "vec4",
        "mat2",
        "mat3",
        "mat4",
        "sampler2D",
        "samplerCube",
        "void",
        "main",
    ],
    "ipc": [
        "code",
        "flags",
        "data",
        "reply",
        "descriptor",
        "offset",
        "WriteInt32",
        "ReadInt32",
        "WriteString",
        "ReadString",
    ],
}

STRUCT_TEMPLATES = {
    "Rect": lambda: struct.pack("<iiii", 0, 0, 1024, 768),
    "Rect_large": lambda: struct.pack("<iiii", 0, 0, 8192, 8192),
    "Rect_invalid": lambda: struct.pack("<iiii", -1000, -1000, 0xFFFFFF, 0xFFFFFF),
    "Point": lambda: struct.pack("<ii", 0, 0),
    "Point_origin": lambda: struct.pack("<ii", 0, 0),
    "Point_large": lambda: struct.pack("<ii", 10000, 10000),
    "Size": lambda: struct.pack("<ii", 1024, 768),
    "Size_zero": lambda: struct.pack("<ii", 0, 0),
    "Size_large": lambda: struct.pack("<ii", 8192, 8192),
    "Color": lambda: struct.pack("<BBBB", 255, 255, 255, 255),
    "Color_transparent": lambda: struct.pack("<BBBB", 255, 255, 255, 0),
    "Color_black": lambda: struct.pack("<BBBB", 0, 0, 0, 255),
    "Matrix4x4": lambda: struct.pack(
        "<16f", *[1.0 if i % 5 == 0 else 0.0 for i in range(16)]
    ),
    "Matrix4x4_zero": lambda: struct.pack("<16f", *[0.0 for _ in range(16)]),
}


# ============================================================================
# Seed 模式 - 通用种子生成
# ============================================================================

SEED_TEMPLATES = {
    "binary": {
        "description": "通用二进制数据（包含Magic + Version + 空Payload）",
        "generator": lambda: generate_binary_seed(),
    },
    "json": {
        "description": "基础JSON结构",
        "generator": lambda: generate_json_seed(),
    },
    "jpeg": {
        "description": "最小JPEG文件（仅SOI + APP0头）",
        "generator": lambda: generate_jpeg_seed(),
    },
    "png": {
        "description": "最小PNG文件（PNG签名 + IHDR头）",
        "generator": lambda: generate_png_seed(),
    },
    "text": {
        "description": "通用文本数据",
        "generator": lambda: generate_text_seed(),
    },
    "protobuf": {
        "description": "Protocol Buffer最小消息",
        "generator": lambda: generate_protobuf_seed(),
    },
    "xml": {
        "description": "基础XML结构",
        "generator": lambda: generate_xml_seed(),
    },
    "parcel": {
        "description": "IPC MessageParcel格式",
        "generator": lambda: generate_parcel_seed(),
    },
    "custom": {
        "description": "自定义格式（根据API参数生成）",
        "generator": lambda params=None: generate_custom_seed(params),
    },
}


def generate_binary_seed():
    """生成通用二进制种子"""
    magic = b"FUZZ"
    version = struct.pack("<H", 1)
    payload = b"\x00" * 16
    return magic + version + payload


def generate_json_seed():
    """生成基础JSON种子"""
    data = {"type": "test", "version": 1, "data": {}}
    return json.dumps(data, indent=2).encode("utf-8")


def generate_jpeg_seed():
    """生成最小JPEG文件"""
    soi = b"\xff\xd8"
    app0 = b"\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    image_data = b"\xff\xdb\x00C\x00" + b"\x10" * 59
    image_data += b"\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x03\x01\x11\x00"
    image_data += b"\xff\xc4\x00\x1f\x00" + b"\x00" * 27
    image_data += b"\xff\xda\x00\x08\x01\x01\x00\x00?\x00"
    eoi = b"\xff\xd9"
    return soi + app0 + image_data + eoi


def generate_png_seed():
    """生成最小PNG文件"""
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00"
    ihdr_crc = struct.pack(">I", 0x5A2DD5C8)
    ihdr = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + ihdr_crc
    idat_data = b"\x78\x9c\x63\x60\x00\x00\x00\x02\x00\x01"
    idat_crc = struct.pack(">I", 0x5D6E2D48)
    idat = struct.pack(">I", len(idat_data)) + b"IDAT" + idat_data + idat_crc
    iend_crc = struct.pack(">I", 0xAE426082)
    iend = struct.pack(">I", 0) + b"IEND" + iend_crc
    return signature + ihdr + idat + iend


def generate_text_seed():
    """生成通用文本种子"""
    text = """Test data for fuzzing.
This is a sample text that can be mutated by the fuzzer.
Line 1: Basic text content
Line 2: Special chars: !@#$%^&*()
Line 3: Numbers: 1234567890
"""
    return text.encode("utf-8")


def generate_protobuf_seed():
    """生成Protocol Buffer最小消息"""
    return b"\x08\x00"


def generate_xml_seed():
    """生成基础XML种子"""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item type="test">
        <name>example</name>
        <value>0</value>
    </item>
</root>
"""
    return xml.encode("utf-8")


def generate_parcel_seed():
    """生成IPC MessageParcel格式种子"""
    header = struct.pack("<I", 0)
    data = struct.pack("<I", 1)
    data += struct.pack("<I", 0)
    return header + data


def generate_custom_seed(params=None):
    """根据API参数生成自定义种子"""
    if not params:
        seed = b""
        seed += b"CUST"
        seed += struct.pack("<I", 1)
        seed += struct.pack("<I", 3)
        seed += struct.pack("<I", 0)
        seed += struct.pack("<I", 4)
        seed += struct.pack("<i", 42)
        seed += struct.pack("<I", 1)
        seed += struct.pack("<I", 5)
        seed += b"hello"
        seed += struct.pack("<I", 2)
        seed += struct.pack("<I", 4)
        seed += b"\x00\x01\x02\x03"
        return seed

    seed = b""
    seed += b"CUST"
    seed += struct.pack("<I", 1)
    seed += struct.pack("<I", len(params))

    for param in params:
        param_type = param.get("type", "int")
        param_value = param.get("value", None)

        if param_type in ("int", "int32", "int32_t", "uint32", "uint32_t"):
            seed += struct.pack("<I", 0)
            seed += struct.pack("<I", 4)
            if param_value is not None:
                seed += struct.pack("<i", int(param_value))
            else:
                seed += struct.pack("<i", 0)
        elif param_type in ("int64", "int64_t", "uint64", "uint64_t"):
            seed += struct.pack("<I", 3)
            seed += struct.pack("<I", 8)
            if param_value is not None:
                seed += struct.pack("<q", int(param_value))
            else:
                seed += struct.pack("<q", 0)
        elif param_type in ("string", "std::string"):
            seed += struct.pack("<I", 1)
            if param_value is not None:
                value_bytes = str(param_value).encode("utf-8")
            else:
                value_bytes = b"test"
            seed += struct.pack("<I", len(value_bytes))
            seed += value_bytes
        elif param_type in ("bytes", "std::vector<uint8_t>"):
            seed += struct.pack("<I", 2)
            if param_value is not None:
                value_bytes = bytes(param_value)
            else:
                value_bytes = b"\x00" * 16
            seed += struct.pack("<I", len(value_bytes))
            seed += value_bytes
        else:
            seed += struct.pack("<I", 0)
            seed += struct.pack("<I", 4)
            seed += struct.pack("<i", 0)

    return seed


# ============================================================================
# 智能语义推断与增强种子生成
# ============================================================================


def infer_value_from_param_name(param_name: str, param_type: str) -> List[Any]:
    """
    基于参数名称推断合理的测试值

    Args:
        param_name: 参数名称（如 screenId, width, callback）
        param_type: 参数类型（如 uint64_t, int32_t, std::string）

    Returns:
        推断的测试值列表
    """
    name_lower = param_name.lower()

    for semantic_key, values in SEMANTIC_HINTS.items():
        if semantic_key in name_lower:
            if param_type in ["std::string", "string", "std::u16string"]:
                return [v for v in values if isinstance(v, str)][:4]
            elif param_type in ["float", "double"]:
                return [float(v) if not isinstance(v, str) else 0.0 for v in values[:4]]
            else:
                return [int(v) if not isinstance(v, str) else 0 for v in values[:4]]

    return []


def generate_boundary_seed_for_type(param_type: str) -> List[bytes]:
    """
    为指定类型生成所有边界值种子

    Args:
        param_type: 参数类型

    Returns:
        边界值字节列表
    """
    seeds = []
    type_lower = param_type.lower()

    if type_lower in BOUNDARY_VALUES:
        for val in BOUNDARY_VALUES[type_lower]:
            seeds.append(pack_value(param_type, val))

    if "float" in type_lower:
        for name, bytes_val in FLOAT_SPECIAL_BYTES.items():
            seeds.append(bytes_val)

    if "double" in type_lower:
        for name, bytes_val in DOUBLE_SPECIAL_BYTES.items():
            seeds.append(bytes_val)

    return seeds


def pack_value(param_type: str, value: Any) -> bytes:
    """
    将值打包为字节

    Args:
        param_type: 参数类型
        value: 值

    Returns:
        字节数据
    """
    type_lower = param_type.lower()

    if "bool" in type_lower:
        return struct.pack("<?", bool(value))
    elif "int8" in type_lower or type_lower == "char":
        return struct.pack("<b", int(value))
    elif "uint8" in type_lower or "unsigned char" in type_lower:
        return struct.pack("<B", int(value) & 0xFF)
    elif "int16" in type_lower or "short" in type_lower:
        return struct.pack("<h", int(value))
    elif "uint16" in type_lower or "unsigned short" in type_lower:
        return struct.pack("<H", int(value) & 0xFFFF)
    elif "int32" in type_lower or type_lower == "int":
        return struct.pack("<i", int(value))
    elif "uint32" in type_lower or "unsigned int" in type_lower:
        return struct.pack("<I", int(value) & 0xFFFFFFFF)
    elif "int64" in type_lower or "long long" in type_lower:
        return struct.pack("<q", int(value))
    elif "uint64" in type_lower or "unsigned long long" in type_lower:
        return struct.pack("<Q", int(value) & 0xFFFFFFFFFFFFFFFF)
    elif "float" in type_lower and "double" not in type_lower:
        return struct.pack("<f", float(value))
    elif "double" in type_lower:
        return struct.pack("<d", float(value))
    elif "string" in type_lower:
        str_bytes = str(value).encode("utf-8")
        return struct.pack("<I", len(str_bytes)) + str_bytes
    elif "size_t" in type_lower:
        return struct.pack("<Q", int(value))
    else:
        return struct.pack("<I", int(value))


def generate_cartesian_seeds(
    params: List[Dict], output_dir: str, max_combinations: int = 30
) -> List[str]:
    """
    使用笛卡尔积生成组合种子

    优化:
    - 默认 max_combinations 从 100 降至 30
    - 按内容 hash 去重
    - 限制每个参数的取值数量（最多 4 个）

    Args:
        params: 参数列表 [{"name": "xxx", "type": "xxx"}, ...]
        output_dir: 输出目录
        max_combinations: 最大组合数量（默认 30，避免过度膨胀）

    Returns:
        生成的种子文件路径列表
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    param_value_lists = []
    for param in params:
        param_name = param.get("name", "")
        param_type = param.get("type", "int32_t")

        values = infer_value_from_param_name(param_name, param_type)
        if values is None:
            boundary_seeds = generate_boundary_seed_for_type(param_type)
            if boundary_seeds:
                values = boundary_seeds[:4]
            else:
                values = [pack_value(param_type, 0), pack_value(param_type, 1)]

        # 限制每个参数的取值数量，防止笛卡尔积爆炸
        values = values[:4]
        param_value_lists.append(values)

    generated_files = []
    seen_hashes = set()
    combo_count = 0

    for combo in itertools.product(*param_value_lists):
        if combo_count >= max_combinations:
            break

        seed = bytearray()
        seed.append(0)
        for val_bytes in combo:
            if isinstance(val_bytes, bytes):
                seed.extend(val_bytes)
            else:
                seed.extend(
                    pack_value(
                        params[combo_count % len(params)].get("type", "int32_t"),
                        val_bytes,
                    )
                )

        # 去重：跳过内容相同的种子
        seed_bytes = bytes(seed)
        import hashlib

        seed_hash = hashlib.md5(seed_bytes).hexdigest()
        if seed_hash in seen_hashes:
            continue
        seen_hashes.add(seed_hash)

        seed_file = output_path / f"init_combo_{combo_count}.bin"
        seed_file.write_bytes(seed_bytes)
        generated_files.append(str(seed_file))
        combo_count += 1

    return generated_files


def generate_enhanced_dict(
    context: str = "general", api_info: Optional[Dict] = None
) -> str:
    """
    生成增强版fuzzer字典

    Args:
        context: 上下文类型（gltf, rscommand, shader, ipc, general）
        api_info: API信息（可选）

    Returns:
        字典文件内容
    """
    entries = []

    entries.append("# Auto-generated fuzzer dictionary")
    entries.append('# Format: keyword="value"')
    entries.append("")

    for name, magic in MAGIC_NUMBERS.items():
        entries.append(f'magic_{name}="{magic.hex()}"')

    entries.append("")
    entries.append("# Security test strings")
    for s in SECURITY_TEST_STRINGS[:10]:
        safe_repr = repr(s).replace('"', "'")
        entries.append(f"security={safe_repr}")

    entries.append("")
    entries.append("# Protocol keywords")
    if context in PROTOCOL_KEYWORDS:
        for kw in PROTOCOL_KEYWORDS[context]:
            entries.append(f'keyword="{kw}"')
    else:
        for ctx, keywords in PROTOCOL_KEYWORDS.items():
            for kw in keywords[:5]:
                entries.append(f'keyword_{ctx}="{kw}"')

    entries.append("")
    entries.append("# Integer boundaries")
    for bits in [8, 16, 32, 64]:
        max_signed = (1 << (bits - 1)) - 1
        min_signed = -(1 << (bits - 1))
        max_unsigned = (1 << bits) - 1
        entries.append(f'int{bits}_max="{max_signed}"')
        entries.append(f'int{bits}_min="{min_signed}"')
        entries.append(f'uint{bits}_max="{max_unsigned}"')

    entries.append("")
    entries.append("# Float special values (hex)")
    for name, bytes_val in FLOAT_SPECIAL_BYTES.items():
        entries.append(f'float_{name}="{bytes_val.hex()}"')

    entries.append("")
    entries.append("# Double special values (hex)")
    for name, bytes_val in DOUBLE_SPECIAL_BYTES.items():
        entries.append(f'double_{name}="{bytes_val.hex()}"')

    if api_info:
        entries.append("")
        entries.append("# API-specific entries")
        for param in api_info.get("params", []):
            param_name = param.get("name", "")
            if param_name:
                entries.append(f'param_{param_name}="{param_name}"')

    return "\n".join(entries)


def generate_structured_type_seed(param_type: str) -> bytes:
    """
    为结构化类型生成种子数据

    Args:
        param_type: 类型名称（如 Rect, Point, Size）

    Returns:
        字节数据
    """
    type_lower = param_type.lower()

    for struct_name, generator in STRUCT_TEMPLATES.items():
        if struct_name.lower().startswith(type_lower):
            return generator()

    if "rect" in type_lower:
        return STRUCT_TEMPLATES["Rect"]()
    elif "point" in type_lower:
        return STRUCT_TEMPLATES["Point"]()
    elif "size" in type_lower:
        return STRUCT_TEMPLATES["Size"]()
    elif "color" in type_lower:
        return STRUCT_TEMPLATES["Color"]()
    elif "matrix" in type_lower:
        return STRUCT_TEMPLATES["Matrix4x4"]()

    return b"\x00" * 16


def generate_seed(seed_type, output_path, params=None):
    """生成种子文件"""
    if seed_type not in SEED_TEMPLATES:
        print(f"错误: 不支持的种子类型 '{seed_type}'")
        print(f"支持的类型: {', '.join(SEED_TEMPLATES.keys())}")
        return False

    try:
        if seed_type == "custom" and params:
            seed_data = SEED_TEMPLATES[seed_type]["generator"](params)
        else:
            seed_data = SEED_TEMPLATES[seed_type]["generator"]()

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(seed_data)

        print(f"[OK] Generated seed: {output_path}")
        print(f"   Type: {seed_type}")
        print(f"   Size: {len(seed_data)} bytes")
        print(f"   Description: {SEED_TEMPLATES[seed_type]['description']}")

        return True
    except Exception as e:
        print(f"[FAIL] 生成种子失败: {e}")
        return False


def analyze_fuzzer_code(fuzzer_path: str) -> Dict:
    """分析fuzzer代码，提取被测API信息"""
    result = {
        "api_calls": [],
        "data_types": [],
        "includes": [],
        "seed_hints": [],
        "struct_types": [],
        "enums": [],
    }

    try:
        with open(fuzzer_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[WARN] 无法读取fuzzer代码: {e}")
        return result

    includes = re.findall(r'#include\s+["<]([^">]+)[">]', content)
    result["includes"] = includes

    api_calls = re.findall(r"(?:g_\w+|\w+)\s*->\s*(\w+)\s*\(", content)
    result["api_calls"] = list(set(api_calls))

    consume_types = re.findall(r"fdp\.Consume(\w+)", content)
    result["data_types"] = list(set(consume_types))

    seed_hints = []
    content_lower = content.lower()
    for call in api_calls:
        call_lower = call.lower()
        if any(kw in call_lower for kw in ["jpeg", "jpg", "image", "decode", "encode"]):
            seed_hints.append("jpeg")
        elif any(kw in call_lower for kw in ["png", "image"]):
            seed_hints.append("png")
        elif any(kw in call_lower for kw in ["json", "parsejson", "fromjson"]):
            seed_hints.append("json")
        elif any(kw in call_lower for kw in ["xml", "parsexml"]):
            seed_hints.append("xml")
        elif any(kw in call_lower for kw in ["protobuf", "proto", "serialize"]):
            seed_hints.append("protobuf")
        elif any(
            kw in call_lower for kw in ["parcel", "ipc", "message", "remoterequest"]
        ):
            seed_hints.append("parcel")
        elif any(kw in call_lower for kw in ["string", "text", "config"]):
            seed_hints.append("text")

    for ctype in consume_types:
        if "String" in ctype:
            seed_hints.append("text")
        elif "Bytes" in ctype:
            seed_hints.append("binary")
        elif "Integral" in ctype:
            seed_hints.append("binary")

    for include in includes:
        include_lower = include.lower()
        if "json" in include_lower:
            seed_hints.append("json")
        elif "xml" in include_lower:
            seed_hints.append("xml")
        elif "image" in include_lower or "jpeg" in include_lower:
            seed_hints.append("jpeg")
        elif "parcel" in include_lower or "ipc" in include_lower:
            seed_hints.append("parcel")

    result["seed_hints"] = list(set(seed_hints)) if seed_hints else ["binary"]

    struct_types = re.findall(r"(\w+)\s+\w+\s*=", content)
    result["struct_types"] = list(set(struct_types))

    enum_patterns = re.findall(r"static_cast<(\w+)>", content)
    result["enums"] = list(set(enum_patterns))

    return result


def generate_seeds_from_analysis(
    fuzzer_path: str, header_path: Optional[str], output_dir: str
) -> List[str]:
    """分析fuzzer代码并生成合适的种子"""
    generated_files = []

    print(f"[INFO] 分析fuzzer代码: {fuzzer_path}")
    api_info = analyze_fuzzer_code(fuzzer_path)

    print(
        f"[INFO] 发现API调用: {', '.join(api_info['api_calls']) if api_info['api_calls'] else '无'}"
    )
    print(
        f"[INFO] 数据类型: {', '.join(api_info['data_types']) if api_info['data_types'] else '无'}"
    )
    print(f"[INFO] 种子类型提示: {', '.join(api_info['seed_hints'])}")

    for seed_type in api_info["seed_hints"]:
        if seed_type not in SEED_TEMPLATES:
            continue

        main_seed_path = os.path.join(output_dir, f"init_{seed_type}")
        try:
            seed_data = SEED_TEMPLATES[seed_type]["generator"]()

            os.makedirs(output_dir, exist_ok=True)
            with open(main_seed_path, "wb") as f:
                f.write(seed_data)

            print(f"[OK] 生成种子: {main_seed_path} ({len(seed_data)} bytes)")
            generated_files.append(main_seed_path)

        except Exception as e:
            print(f"[FAIL] 生成种子失败: {e}")

    if not generated_files:
        print("[WARN] 未能推断种子类型，生成默认binary种子")
        main_seed_path = os.path.join(output_dir, "init_binary")
        if generate_seed("binary", main_seed_path):
            generated_files.append(main_seed_path)

    return generated_files


# ============================================================================
# Corpus 模式 - 领域特定语料生成
# ============================================================================


class CorpusGenerator:
    """Corpus生成器基类"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self) -> List[Path]:
        """生成corpus文件，返回生成的文件路径列表"""
        raise NotImplementedError

    def _write_file(self, filename: str, content: bytes) -> Path:
        """写入文件"""
        filepath = self.output_dir / filename
        filepath.write_bytes(content)
        return filepath


class RSCommandCorpusGenerator(CorpusGenerator):
    """graphic_graphic_2d RSCommand IPC协议Corpus生成器 (增强版)"""

    RS_COMMAND_TYPES = {
        "valid": list(range(0x0000, 0x0010)),
        "boundary": [0x00FF, 0x0100, 0xFFFE],
        "invalid": [0xFFFF, 0x0000],
    }

    RS_SUB_TYPES = {
        "valid": list(range(0x0000, 0x0008)),
        "boundary": [0x00FE, 0xFFFE],
        "invalid": [0xFFFF],
    }

    def generate(self) -> List[Path]:
        """生成RSCommand corpus"""
        generated_files = []

        for i, cmd_type in enumerate(self.RS_COMMAND_TYPES["valid"][:8]):
            for j, sub_type in enumerate(self.RS_SUB_TYPES["valid"][:4]):
                data = self._build_rscommand(cmd_type, sub_type)
                filename = f"rscommand_valid_{cmd_type:04x}_{sub_type:04x}_{i}_{j}.bin"
                filepath = self._write_file(filename, data)
                generated_files.append(filepath)

        for cmd_type in self.RS_COMMAND_TYPES["boundary"]:
            data = self._build_rscommand(cmd_type, 0x0000)
            filename = f"rscommand_boundary_type{cmd_type:04x}.bin"
            filepath = self._write_file(filename, data)
            generated_files.append(filepath)

        for sub_type in self.RS_SUB_TYPES["boundary"]:
            data = self._build_rscommand(0x0000, sub_type)
            filename = f"rscommand_boundary_sub{sub_type:04x}.bin"
            filepath = self._write_file(filename, data)
            generated_files.append(filepath)

        boundary_data = self._build_boundary_rscommand()
        filepath = self._write_file("rscommand_max_boundary.bin", boundary_data)
        generated_files.append(filepath)

        multi_cmd_data = self._build_multi_rscommand()
        filepath = self._write_file("rscommand_multi.bin", multi_cmd_data)
        generated_files.append(filepath)

        malformed_files = self._build_malformed_commands()
        generated_files.extend(malformed_files)

        print(f"[RSCommand] 生成 {len(generated_files)} 个corpus文件")
        return generated_files

    def _build_rscommand(
        self, cmd_type: int, sub_type: int, node_id: int = 0x1234
    ) -> bytes:
        """构建单个RSCommand"""
        data = bytearray()
        data.extend(struct.pack("<H", cmd_type))
        data.extend(struct.pack("<H", sub_type))
        data.extend(struct.pack("<Q", node_id))
        payload = b"\x00" * 16
        data.extend(struct.pack("<I", len(payload)))
        data.extend(payload)
        return bytes(data)

    def _build_boundary_rscommand(self) -> bytes:
        """构建边界值RSCommand"""
        data = bytearray()
        data.extend(struct.pack("<H", 0xFFFF))
        data.extend(struct.pack("<H", 0xFFFF))
        data.extend(struct.pack("<Q", 0xFFFFFFFFFFFFFFFF))
        data.extend(struct.pack("<I", 1024))
        data.extend(b"\xff" * 1024)
        return bytes(data)

    def _build_malformed_commands(self) -> List[Path]:
        """构建畸形命令测试种子"""
        files = []

        truncated = bytearray()
        truncated.extend(struct.pack("<H", 0x0001))
        filepath = self._write_file("rscommand_truncated_header.bin", bytes(truncated))
        files.append(filepath)

        mismatched = bytearray()
        mismatched.extend(struct.pack("<H", 0x0001))
        mismatched.extend(struct.pack("<H", 0x0000))
        mismatched.extend(struct.pack("<Q", 0x1234))
        mismatched.extend(struct.pack("<I", 1000))
        mismatched.extend(b"\x00" * 10)
        filepath = self._write_file("rscommand_length_mismatch.bin", bytes(mismatched))
        files.append(filepath)

        empty = bytearray()
        filepath = self._write_file("rscommand_empty.bin", bytes(empty))
        files.append(filepath)

        oversized = bytearray()
        oversized.extend(struct.pack("<H", 0x0001))
        oversized.extend(struct.pack("<H", 0x0000))
        oversized.extend(struct.pack("<Q", 0x1234))
        oversized.extend(struct.pack("<I", 0xFFFFFFFF))
        oversized.extend(b"\xaa" * 64)
        filepath = self._write_file("rscommand_oversized_claim.bin", bytes(oversized))
        files.append(filepath)

        negative_size = bytearray()
        negative_size.extend(struct.pack("<H", 0x0001))
        negative_size.extend(struct.pack("<H", 0x0000))
        negative_size.extend(struct.pack("<Q", 0x1234))
        negative_size.extend(struct.pack("<I", 0x80000000))
        filepath = self._write_file("rscommand_negative_size.bin", bytes(negative_size))
        files.append(filepath)

        return files

    def _build_multi_rscommand(self) -> bytes:
        """构建多命令序列"""
        data = bytearray()
        data.extend(struct.pack("<I", 3))
        valid_types = self.RS_COMMAND_TYPES["valid"]
        valid_subs = self.RS_SUB_TYPES["valid"]
        for i in range(3):
            cmd = self._build_rscommand(
                valid_types[i % len(valid_types)],
                valid_subs[i % len(valid_subs)],
                node_id=0x1000 + i,
            )
            data.extend(struct.pack("<I", len(cmd)))
            data.extend(cmd)
        return bytes(data)


class GLTFCorpusGenerator(CorpusGenerator):
    """graphic_graphic_3d GLTF/GLB格式Corpus生成器 (增强版)"""

    def generate(self) -> List[Path]:
        """生成GLTF/GLB corpus"""
        generated_files = []

        gltf_minimal = self._build_minimal_gltf()
        filepath = self._write_file("minimal.gltf", gltf_minimal.encode("utf-8"))
        generated_files.append(filepath)

        gltf_mesh = self._build_mesh_gltf()
        filepath = self._write_file("mesh.gltf", gltf_mesh.encode("utf-8"))
        generated_files.append(filepath)

        gltf_animation = self._build_animation_gltf()
        filepath = self._write_file("animation.gltf", gltf_animation.encode("utf-8"))
        generated_files.append(filepath)

        glb_minimal = self._build_minimal_glb()
        filepath = self._write_file("minimal.glb", glb_minimal)
        generated_files.append(filepath)

        gltf_boundary = self._build_boundary_gltf()
        filepath = self._write_file("boundary.gltf", gltf_boundary.encode("utf-8"))
        generated_files.append(filepath)

        gltf_material = self._build_material_gltf()
        filepath = self._write_file("material.gltf", gltf_material.encode("utf-8"))
        generated_files.append(filepath)

        gltf_texture = self._build_texture_gltf()
        filepath = self._write_file("texture.gltf", gltf_texture.encode("utf-8"))
        generated_files.append(filepath)

        gltf_extensions = self._build_extensions_gltf()
        filepath = self._write_file("extensions.gltf", gltf_extensions.encode("utf-8"))
        generated_files.append(filepath)

        gltf_skin = self._build_skin_gltf()
        filepath = self._write_file("skin.gltf", gltf_skin.encode("utf-8"))
        generated_files.append(filepath)

        malformed_files = self._build_malformed_gltf()
        generated_files.extend(malformed_files)

        print(f"[GLTF/GLB] 生成 {len(generated_files)} 个corpus文件")
        return generated_files

    def _build_minimal_gltf(self) -> str:
        """构建最小GLTF JSON"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{}],
        }
        return json.dumps(gltf, indent=2)

    def _build_mesh_gltf(self) -> str:
        """构建带mesh的GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [{"primitives": [{"attributes": {"POSITION": 0}}]}],
            "accessors": [
                {"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3"}
            ],
            "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": 36}],
            "buffers": [
                {
                    "uri": "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "byteLength": 36,
                }
            ],
        }
        return json.dumps(gltf, indent=2)

    def _build_animation_gltf(self) -> str:
        """构建带动画的GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{}],
            "animations": [
                {
                    "channels": [
                        {"sampler": 0, "target": {"node": 0, "path": "rotation"}}
                    ],
                    "samplers": [{"input": 0, "interpolation": "LINEAR", "output": 1}],
                }
            ],
            "accessors": [
                {
                    "bufferView": 0,
                    "componentType": 5126,
                    "count": 2,
                    "type": "SCALAR",
                    "max": [1.0],
                    "min": [0.0],
                },
                {"bufferView": 1, "componentType": 5126, "count": 2, "type": "VEC4"},
            ],
            "bufferViews": [
                {"buffer": 0, "byteOffset": 0, "byteLength": 8},
                {"buffer": 0, "byteOffset": 8, "byteLength": 32},
            ],
            "buffers": [
                {
                    "uri": "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "byteLength": 40,
                }
            ],
        }
        return json.dumps(gltf, indent=2)

    def _build_minimal_glb(self) -> bytes:
        """构建最小GLB文件"""
        json_data = self._build_minimal_gltf().encode("utf-8")
        json_padding = b" " * ((4 - len(json_data) % 4) % 4)
        json_chunk = json_data + json_padding

        glb = bytearray()
        glb.extend(struct.pack("<I", 0x46546C67))
        glb.extend(struct.pack("<I", 2))
        glb.extend(struct.pack("<I", 12 + 8 + len(json_chunk)))
        glb.extend(struct.pack("<I", len(json_chunk)))
        glb.extend(struct.pack("<I", 0x4E4F534A))
        glb.extend(json_chunk)
        return bytes(glb)

    def _build_boundary_gltf(self) -> str:
        """构建边界测试GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0, 1, 2, 3, 4]}],
            "nodes": [{}, {}, {}, {}, {}],
        }
        return json.dumps(gltf, indent=2)

    def _build_material_gltf(self) -> str:
        """构建带材质的GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [
                {"primitives": [{"attributes": {"POSITION": 0}, "material": 0}]}
            ],
            "materials": [
                {
                    "pbrMetallicRoughness": {
                        "baseColorFactor": [1.0, 0.0, 0.0, 1.0],
                        "metallicFactor": 0.5,
                        "roughnessFactor": 0.5,
                    },
                    "name": "TestMaterial",
                }
            ],
            "accessors": [
                {"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3"}
            ],
            "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": 36}],
            "buffers": [
                {
                    "uri": "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "byteLength": 36,
                }
            ],
        }
        return json.dumps(gltf, indent=2)

    def _build_texture_gltf(self) -> str:
        """构建带纹理的GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [
                {"primitives": [{"attributes": {"POSITION": 0, "TEXCOORD_0": 1}}]}
            ],
            "textures": [{"sampler": 0, "source": 0}],
            "samplers": [{"magFilter": 9729, "minFilter": 9987}],
            "images": [
                {
                    "uri": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADggG/wGKXAAAAABJRU5ErkJggg=="
                }
            ],
            "accessors": [
                {"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3"},
                {"bufferView": 1, "componentType": 5126, "count": 3, "type": "VEC2"},
            ],
            "bufferViews": [
                {"buffer": 0, "byteOffset": 0, "byteLength": 36},
                {"buffer": 0, "byteOffset": 36, "byteLength": 24},
            ],
            "buffers": [
                {
                    "uri": "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "byteLength": 60,
                }
            ],
        }
        return json.dumps(gltf, indent=2)

    def _build_extensions_gltf(self) -> str:
        """构建带扩展的GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "extensionsUsed": ["KHR_materials_unlit", "KHR_texture_transform"],
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [
                {"primitives": [{"attributes": {"POSITION": 0}, "material": 0}]}
            ],
            "materials": [
                {
                    "extensions": {"KHR_materials_unlit": {}},
                    "name": "UnlitMaterial",
                }
            ],
            "accessors": [
                {"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3"}
            ],
            "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": 36}],
            "buffers": [
                {
                    "uri": "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "byteLength": 36,
                }
            ],
        }
        return json.dumps(gltf, indent=2)

    def _build_skin_gltf(self) -> str:
        """构建带蒙皮的GLTF"""
        gltf = {
            "asset": {"version": "2.0"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0, "skin": 0}],
            "meshes": [
                {
                    "primitives": [
                        {"attributes": {"POSITION": 0, "JOINTS_0": 1, "WEIGHTS_0": 2}}
                    ]
                }
            ],
            "skins": [{"joints": [0], "inverseBindMatrices": 3}],
            "accessors": [
                {"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3"},
                {"bufferView": 1, "componentType": 5121, "count": 3, "type": "VEC4"},
                {"bufferView": 2, "componentType": 5126, "count": 3, "type": "VEC4"},
                {"bufferView": 3, "componentType": 5126, "count": 1, "type": "MAT4"},
            ],
            "bufferViews": [
                {"buffer": 0, "byteOffset": 0, "byteLength": 36},
                {"buffer": 0, "byteOffset": 36, "byteLength": 12},
                {"buffer": 0, "byteOffset": 48, "byteLength": 48},
                {"buffer": 0, "byteOffset": 96, "byteLength": 64},
            ],
            "buffers": [
                {
                    "uri": "data:application/octet-stream;base64," + "A" * 160,
                    "byteLength": 160,
                }
            ],
        }
        return json.dumps(gltf, indent=2)

    def _build_malformed_gltf(self) -> List[Path]:
        """构建畸形GLTF测试种子"""
        files = []

        invalid_json = "{invalid json}"
        filepath = self._write_file(
            "malformed_invalid_json.gltf", invalid_json.encode("utf-8")
        )
        files.append(filepath)

        empty = "{}"
        filepath = self._write_file("malformed_empty.gltf", empty.encode("utf-8"))
        files.append(filepath)

        missing_asset = {"scene": 0}
        filepath = self._write_file(
            "malformed_missing_asset.gltf", json.dumps(missing_asset).encode("utf-8")
        )
        files.append(filepath)

        invalid_version = {"asset": {"version": "1.0"}}
        filepath = self._write_file(
            "malformed_invalid_version.gltf",
            json.dumps(invalid_version).encode("utf-8"),
        )
        files.append(filepath)

        negative_index = {
            "asset": {"version": "2.0"},
            "scene": -1,
            "scenes": [{"nodes": [-100]}],
        }
        filepath = self._write_file(
            "malformed_negative_index.gltf", json.dumps(negative_index).encode("utf-8")
        )
        files.append(filepath)

        overflow_index = {
            "asset": {"version": "2.0"},
            "scene": 0xFFFFFFFF,
            "scenes": [{"nodes": [0xFFFFFFFF]}],
        }
        filepath = self._write_file(
            "malformed_overflow_index.gltf", json.dumps(overflow_index).encode("utf-8")
        )
        files.append(filepath)

        return files


class ShaderCorpusGenerator(CorpusGenerator):
    """Shader语料生成器 (增强版)"""

    def generate(self) -> List[Path]:
        """生成Shader corpus"""
        generated_files = []

        vertex_shader = self._build_vertex_shader()
        filepath = self._write_file("vertex.glsl", vertex_shader.encode("utf-8"))
        generated_files.append(filepath)

        fragment_shader = self._build_fragment_shader()
        filepath = self._write_file("fragment.glsl", fragment_shader.encode("utf-8"))
        generated_files.append(filepath)

        compute_shader = self._build_compute_shader()
        filepath = self._write_file("compute.glsl", compute_shader.encode("utf-8"))
        generated_files.append(filepath)

        minimal_shader = self._build_minimal_shader()
        filepath = self._write_file("minimal.glsl", minimal_shader.encode("utf-8"))
        generated_files.append(filepath)

        geometry_shader = self._build_geometry_shader()
        filepath = self._write_file("geometry.glsl", geometry_shader.encode("utf-8"))
        generated_files.append(filepath)

        tess_control_shader = self._build_tess_control_shader()
        filepath = self._write_file(
            "tess_control.glsl", tess_control_shader.encode("utf-8")
        )
        generated_files.append(filepath)

        tess_eval_shader = self._build_tess_eval_shader()
        filepath = self._write_file("tess_eval.glsl", tess_eval_shader.encode("utf-8"))
        generated_files.append(filepath)

        malformed_files = self._build_malformed_shaders()
        generated_files.extend(malformed_files)

        print(f"[Shader] 生成 {len(generated_files)} 个corpus文件")
        return generated_files

    def _build_vertex_shader(self) -> str:
        """构建顶点Shader"""
        return """#version 300 es
in vec4 a_position;
in vec2 a_texCoord;
out vec2 v_texCoord;
void main() {
    gl_Position = a_position;
    v_texCoord = a_texCoord;
}
"""

    def _build_fragment_shader(self) -> str:
        """构建片段Shader"""
        return """#version 300 es
precision mediump float;
in vec2 v_texCoord;
out vec4 fragColor;
uniform sampler2D u_texture;
void main() {
    fragColor = texture(u_texture, v_texCoord);
}
"""

    def _build_compute_shader(self) -> str:
        """构建计算Shader"""
        return """#version 310 es
layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;
layout(std430, binding = 0) buffer InputBuffer {
    float data[];
} inputBuffer;
layout(std430, binding = 1) buffer OutputBuffer {
    float data[];
} outputBuffer;
void main() {
    uint idx = gl_GlobalInvocationID.x;
    outputBuffer.data[idx] = inputBuffer.data[idx] * 2.0;
}
"""

    def _build_minimal_shader(self) -> str:
        """构建最小Shader"""
        return """#version 300 es
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

    def _build_geometry_shader(self) -> str:
        """构建几何Shader"""
        return """#version 310 es
layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;
in vec2 v_texCoord[];
out vec2 g_texCoord;
void main() {
    for(int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        g_texCoord = v_texCoord[i];
        EmitVertex();
    }
    EndPrimitive();
}
"""

    def _build_tess_control_shader(self) -> str:
        """构建细分控制Shader"""
        return """#version 310 es
layout(vertices = 3) out;
in vec2 v_texCoord[];
out vec2 tc_texCoord[];
void main() {
    if(gl_InvocationID == 0) {
        gl_TessLevelInner[0] = 1.0;
        gl_TessLevelOuter[0] = 1.0;
        gl_TessLevelOuter[1] = 1.0;
        gl_TessLevelOuter[2] = 1.0;
    }
    tc_texCoord[gl_InvocationID] = v_texCoord[gl_InvocationID];
    gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
}
"""

    def _build_tess_eval_shader(self) -> str:
        """构建细分评估Shader"""
        return """#version 310 es
layout(triangles, equal_spacing, ccw) in;
in vec2 tc_texCoord[];
out vec2 te_texCoord;
void main() {
    gl_Position = gl_TessCoord.x * gl_in[0].gl_Position +
                  gl_TessCoord.y * gl_in[1].gl_Position +
                  gl_TessCoord.z * gl_in[2].gl_Position;
    te_texCoord = gl_TessCoord.x * tc_texCoord[0] +
                  gl_TessCoord.y * tc_texCoord[1] +
                  gl_TessCoord.z * tc_texCoord[2];
}
"""

    def _build_malformed_shaders(self) -> List[Path]:
        """构建畸形Shader测试种子"""
        files = []

        empty_shader = ""
        filepath = self._write_file(
            "malformed_empty.glsl", empty_shader.encode("utf-8")
        )
        files.append(filepath)

        syntax_error = """#version 300 es
void main() {
    gl_FragColor = vec4(1.0, 0.0 0.0, 1.0);  // missing comma
}
"""
        filepath = self._write_file(
            "malformed_syntax_error.glsl", syntax_error.encode("utf-8")
        )
        files.append(filepath)

        undefined_var = """#version 300 es
void main() {
    gl_FragColor = undefinedVariable;
}
"""
        filepath = self._write_file(
            "malformed_undefined_var.glsl", undefined_var.encode("utf-8")
        )
        files.append(filepath)

        version_missing = """
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""
        filepath = self._write_file(
            "malformed_no_version.glsl", version_missing.encode("utf-8")
        )
        files.append(filepath)

        infinite_loop = """#version 300 es
void main() {
    while(true) {
        // infinite loop
    }
}
"""
        filepath = self._write_file(
            "malformed_infinite_loop.glsl", infinite_loop.encode("utf-8")
        )
        files.append(filepath)

        array_overflow = """#version 300 es
void main() {
    float arr[4];
    for(int i = 0; i < 1000000; i++) {
        arr[i] = 1.0;  // potential overflow
    }
}
"""
        filepath = self._write_file(
            "malformed_array_overflow.glsl", array_overflow.encode("utf-8")
        )
        files.append(filepath)

        return files


CORPUS_GENERATORS = {
    "rscommand": RSCommandCorpusGenerator,
    "gltf": GLTFCorpusGenerator,
    "shader": ShaderCorpusGenerator,
}


# ============================================================================
# 主入口
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="FUZZ种子与语料生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # Seed模式 - 生成通用种子
  python3 seed_generator.py seed -t json -o corpus/init.json
  python3 seed_generator.py seed --analyze path/to/fuzzer.cpp -o corpus/
  
  # Corpus模式 - 生成领域特定语料
  python3 seed_generator.py corpus --repo graphic_2d --type rscommand --output ./corpus/
  python3 seed_generator.py corpus --repo graphic_3d --type gltf --output ./corpus/
  python3 seed_generator.py corpus --repo graphic_3d --type shader --output ./corpus/
        """,
    )

    subparsers = parser.add_subparsers(dest="mode", help="工作模式")

    # Seed模式
    seed_parser = subparsers.add_parser("seed", help="生成通用种子数据")
    seed_parser.add_argument(
        "-t",
        "--type",
        choices=list(SEED_TEMPLATES.keys()),
        default="binary",
        help="种子类型（默认: binary）",
    )
    seed_parser.add_argument("-o", "--output", required=True, help="输出文件路径或目录")
    seed_parser.add_argument(
        "-p", "--params", help="自定义参数（JSON格式，仅custom类型使用）"
    )
    seed_parser.add_argument(
        "--analyze", help="分析fuzzer代码路径（自动推断种子类型并生成）"
    )
    seed_parser.add_argument("--header", help="头文件路径（配合--analyze使用）")
    seed_parser.add_argument(
        "-l", "--list", action="store_true", help="列出所有支持的种子类型"
    )

    # Corpus模式
    corpus_parser = subparsers.add_parser("corpus", help="生成领域特定结构化语料")
    corpus_parser.add_argument(
        "--repo",
        choices=["graphic_2d", "graphic_3d"],
        required=True,
        help="目标仓库",
    )
    corpus_parser.add_argument(
        "--type",
        choices=list(CORPUS_GENERATORS.keys()),
        required=True,
        help="语料类型",
    )
    corpus_parser.add_argument("--output", required=True, help="输出目录")
    corpus_parser.add_argument(
        "-l", "--list", action="store_true", help="列出所有支持的语料类型"
    )

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    if args.mode == "seed":
        if args.list:
            print("支持的种子类型:")
            for seed_type, info in SEED_TEMPLATES.items():
                print(f"  {seed_type:12s} - {info['description']}")
            return

        if args.analyze:
            if not os.path.exists(args.analyze):
                print(f"错误: fuzzer文件不存在: {args.analyze}")
                sys.exit(1)

            generated = generate_seeds_from_analysis(
                args.analyze, args.header, args.output
            )
            if generated:
                print(f"\n[OK] 成功生成 {len(generated)} 个种子文件")
                for f in generated:
                    print(f"   - {f}")
            else:
                print("\n[FAIL] 未能生成任何种子文件")
                sys.exit(1)
        else:
            params = None
            if args.params:
                try:
                    params = json.loads(args.params)
                except Exception:
                    print("错误: 参数格式不正确，应为JSON格式")
                    sys.exit(1)

            if not generate_seed(args.type, args.output, params):
                sys.exit(1)

    elif args.mode == "corpus":
        if args.list:
            print("支持的语料类型:")
            for corpus_type, generator_class in CORPUS_GENERATORS.items():
                print(f"  {corpus_type:12s} - {generator_class.__doc__}")
            return

        if args.type not in CORPUS_GENERATORS:
            print(f"错误: 不支持的语料类型 '{args.type}'")
            sys.exit(1)

        generator_class = CORPUS_GENERATORS[args.type]
        generator = generator_class(args.output)
        generated_files = generator.generate()

        if generated_files:
            print(f"\n[OK] 成功生成 {len(generated_files)} 个语料文件")
            for f in generated_files:
                print(f"   - {f}")
        else:
            print("\n[FAIL] 未能生成任何语料文件")
            sys.exit(1)


if __name__ == "__main__":
    main()
