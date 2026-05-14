#!/usr/bin/env python3
"""
规则002: 关键API需要FUZZ覆盖
检查目标类中所有有参public API是否都被FUZZ测试覆盖
"""

import re
import os
from pathlib import Path


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

    # 提取所有 public: 段（类可能有多个 public: 段）
    pub_bodies = []
    pos = 0
    while pos < len(class_body):
        pub_match = re.search(r"\bpublic\s*:", class_body[pos:])
        if not pub_match:
            break
        pub_start = pos + pub_match.end()
        next_access = re.search(r"\b(protected|private)\s*:", class_body[pub_start:])
        if next_access:
            pub_bodies.append(class_body[pub_start : pub_start + next_access.start()])
            pos = pub_start + next_access.end()
        else:
            pub_bodies.append(class_body[pub_start:])
            break

    if not pub_bodies:
        return []

    methods = []
    pattern = re.compile(
        r"(?:virtual|static|explicit|constexpr|inline|consteval|constinit|\[\[.*?\]\]|\s)*"
        r"(?P<ret>[~\w_][\w\s_:<>*,&.]*?)\s+"
        r"(?P<name>\w+)\s*\(\s*(?P<params>[^)]*)\s*\)\s*"
        r"(?:const\s*)?(?:override\s*)?(?:final\s*)?(?:noexcept\s*)?(?:=\s*0\s*)?;"
    )
    for pub_body in pub_bodies:
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


def check_missing_api_coverage(filepath, content, all_project_files=None):
    """
    规则002: 检查目标类中所有有参public API是否都被FUZZ测试覆盖

    参数:
        filepath: 当前检查的文件路径
        content: 当前文件内容
        all_project_files: 可选，项目中所有fuzzer文件的内容字典 {filepath: content}
                            如果提供，会合并所有文件的覆盖率进行检查
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
    header_found = False
    for hc in header_candidates:
        resolved = _resolve_header_path(hc, search_dirs)
        if resolved and os.path.isfile(resolved):
            header_found = True
            all_header_methods.extend(parse_header_methods(resolved, target_class))

    # 收集所有被fuzz测试覆盖的API方法名
    covered = set()

    # 如果提供了项目所有文件，合并所有文件的覆盖率
    files_to_check = {filepath: content}
    if all_project_files:
        files_to_check = all_project_files

    for file_path, file_content in files_to_check.items():
        # 只检查同一目录下的fuzzer文件（同一项目）
        if Path(file_path).parent != Path(filepath).parent and not all_project_files:
            continue

        # 模式1: DoXXX 函数名推断 (DoSetConfig -> SetConfig)
        do_funcs = set(
            re.findall(r"\bvoid\s+(\w+)\s*\(\s*FuzzedDataProvider", file_content)
        )
        for do_name in do_funcs:
            if do_name.startswith("Do") and len(do_name) > 2:
                covered.add(do_name[2:])
            else:
                covered.add(do_name)

        # 模式2: 从函数体内提取 g_instance->Method(...) 和 Class::Method(...) 调用
        arrow_calls = re.findall(r"(?:g_\w+|\w+)\s*->\s*(\w+)\s*\(", file_content)
        static_calls = re.findall(
            rf"{re.escape(target_class)}::(\w+)\s*\(", file_content
        )
        called_methods = set(arrow_calls + static_calls)
        covered.update(called_methods)

    # 精确检测: 头文件解析成功，对比public方法与覆盖
    if all_header_methods:
        missing = [name for name, _, _ in all_header_methods if name not in covered]
        if missing:
            errors.append(
                f"规则002[高危]: 目标类 {target_class} 中有 {len(missing)} 个有参 public API 未覆盖: "
                f"{', '.join(missing)}，建议补充对应的测试函数"
            )
        return errors

    # 后备检测: 头文件无法解析时，通过.cpp中的方法调用推断覆盖率
    if not header_found:
        if len(covered) <= 1:
            # 获取当前文件的方法调用
            current_arrow_calls = re.findall(
                r"(?:g_\w+|\w+)\s*->\s*(\w+)\s*\(", content
            )
            current_static_calls = re.findall(
                rf"{re.escape(target_class)}::(\w+)\s*\(", content
            )
            current_called_methods = set(current_arrow_calls + current_static_calls)

            if len(current_called_methods) >= 3:
                untested = current_called_methods - covered
                if untested:
                    errors.append(
                        f"规则002[高危]: 目标类 {target_class} 可能存在未覆盖的 API "
                        f"（已覆盖: {covered or '无'}，检测到调用: {', '.join(current_called_methods)}），"
                        f"建议补充对应的测试函数"
                    )

    return errors


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <cpp_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    result = check_missing_api_coverage(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
