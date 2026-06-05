#!/usr/bin/env python3
"""
ohos_callgraph.py — OpenHarmony candidate call-edge finder.

This script is an auxiliary tool for the ohos-dev-cpp-callgraph-analysis skill. It discovers
candidate direct edges from LLVM bitcode and best-effort vtable/dlopen hints.
It does not prove call-chain completeness. The skill must still build an
evidence table and a modification coverage matrix from source evidence.

用法:
    python3 ohos_callgraph.py <function_name> [options]
    python3 ohos_callgraph.py <entry-function> --depth 3
    python3 ohos_callgraph.py <target-function> --depth 4 --reverse
    python3 ohos_callgraph.py <entry-function> --repo <repo-filter> --depth 2
    python3 ohos_callgraph.py <entry-function> --name-keyword <keyword>

要求:
    - OpenHarmony 已编译成功（需要 .o bitcode 文件）
    - LLVM 工具链可用（opt, llvm-dis, llvm-cxxfilt）
    - Agent must pass --oh-root and --repo explicitly; pass --product when known
"""

import argparse
import glob
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass


def find_llvm_tools(oh_root):
    """找到 LLVM 工具链路径"""
    candidates = [
        os.path.join(oh_root, "prebuilts/clang/ohos/linux-x86_64/llvm/bin"),
        os.path.join(oh_root, "prebuilts/clang/ohos/linux-aarch64/llvm/bin"),
    ]
    for c in candidates:
        if os.path.isfile(os.path.join(c, "opt")):
            return c
    return None


def find_product(oh_root):
    """自动检测编译产品名"""
    out_dir = os.path.join(oh_root, "out")
    if not os.path.isdir(out_dir):
        return None
    for d in os.listdir(out_dir):
        if os.path.isdir(os.path.join(out_dir, d, "obj")):
            return d
    return None


def resolve_source_root(oh_root, repo_filter):
    """Use explicit agent-provided context to choose the source scan root."""
    if not repo_filter:
        return oh_root
    for scope in ["foundation", "base", "drivers", "third_party"]:
        scope_dir = os.path.join(oh_root, scope)
        if not os.path.isdir(scope_dir):
            continue
        subsystem_candidate = os.path.join(scope_dir, repo_filter)
        if os.path.isdir(subsystem_candidate):
            return subsystem_candidate
        for subsystem in os.listdir(scope_dir):
            candidate = os.path.join(scope_dir, subsystem, repo_filter)
            if os.path.isdir(candidate):
                return candidate
    return oh_root


@dataclass
class CommandResult:
    """Result from an external command."""
    cmd: list
    returncode: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    missing_tool: bool = False

    @property
    def ok(self):
        return self.returncode == 0 and not self.timed_out and not self.missing_tool

    @property
    def output(self):
        return self.stdout + self.stderr


def run(cmd, timeout=120):
    """执行命令，返回结构化结果"""
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        return CommandResult(
            cmd=cmd,
            returncode=r.returncode,
            stdout=r.stdout.decode("utf-8", errors="replace"),
            stderr=r.stderr.decode("utf-8", errors="replace"),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode("utf-8", errors="replace") if exc.stdout else ""
        stderr = exc.stderr.decode("utf-8", errors="replace") if exc.stderr else ""
        stderr += f"\ncommand timed out after {timeout}s: {' '.join(cmd)}"
        return CommandResult(cmd=cmd, returncode=-1, stdout=stdout, stderr=stderr, timed_out=True)
    except FileNotFoundError as exc:
        return CommandResult(
            cmd=cmd,
            returncode=-1,
            stderr=f"missing tool: {exc.filename}",
            missing_tool=True,
        )


def demangle_batch(llvm_bin, symbols):
    """批量 C++ 符号 demangle"""
    if not symbols:
        return {}
    inp = "\n".join(symbols)
    try:
        r = subprocess.run(
            [os.path.join(llvm_bin, "llvm-cxxfilt")],
            input=inp.encode(), capture_output=True, timeout=30
        )
        results = r.stdout.decode("utf-8", errors="replace").strip().split("\n")
        return dict(zip(symbols, [r.strip() for r in results]))
    except Exception:
        return {s: s for s in symbols}


def find_bitcode_files(obj_dir, repo_filter=None):
    """扫描 obj 目录找所有 LLVM bitcode .o 文件"""
    files = []
    for f in glob.iglob(os.path.join(obj_dir, "**", "*.o"), recursive=True):
        if "/test/" in f or "/mock/" in f:
            continue
        if repo_filter and repo_filter not in f:
            continue
        files.append(f)
    return files


def extract_callgraph(llvm_bin, obj_file):
    """从单个 .o bitcode 提取调用图"""
    result = run([os.path.join(llvm_bin, "opt"), "--print-callgraph", obj_file], timeout=60)
    graph = defaultdict(set)
    current_func = None
    if not result.ok:
        return graph, result.output.strip() or f"opt failed for {obj_file}"
    for line in result.output.split("\n"):
        m = re.match(r"Call graph node for function: '([^']+)'", line)
        if m:
            current_func = m.group(1)
            continue
        if current_func:
            m2 = re.match(r"  CS<[^>]*> calls function '([^']+)'", line)
            if m2 and m2.group(1) != current_func:
                graph[current_func].add(("direct", m2.group(1)))
            if "calls external node" in line:
                graph[current_func].add(("indirect", None))
        if line.strip() == "":
            current_func = None
    return graph, None


def extract_vtable_calls(llvm_bin, obj_file):
    """从 LLVM IR 提取虚函数间接调用的接口类型"""
    ll_path = f"/tmp/ohos_cg_{os.getpid()}_{os.path.basename(obj_file)}.ll"
    result = run([os.path.join(llvm_bin, "llvm-dis"), "-o", ll_path, obj_file], timeout=60)
    vtable_calls = defaultdict(set)
    if not result.ok:
        return vtable_calls, result.output.strip() or f"llvm-dis failed for {obj_file}"
    if not os.path.exists(ll_path):
        return vtable_calls, f"llvm-dis did not create {ll_path}"
    current_func = None
    try:
        with open(ll_path, "r", errors="replace") as f:
            for line in f:
                m = re.match(r"define\s.*@([^\s(]+)", line)
                if m:
                    current_func = m.group(1).strip('"')
                    continue
                if line.startswith("}"):
                    current_func = None
                    continue
                if current_func and "type.test" in line:
                    m2 = re.search(r'metadata\s*!"(_ZTS[^"]+)"', line)
                    if m2:
                        vtable_calls[current_func].add(m2.group(1))
    finally:
        try:
            os.unlink(ll_path)
        except OSError:
            pass
    return vtable_calls, None


def discover_dlopen_map(src_root):
    """自动发现 dlopen 映射：Interface -> .so -> ConcreteClass"""
    registry = {}
    load_calls = run(["grep", "-rn", "LoadLibrary<", src_root,
                       "--include=*.cpp", "--include=*.h"], timeout=30).output
    so_names = run(["grep", "-rn", 'constexpr.*char.*LIB_.*"', src_root,
                     "--include=*.cpp", "--include=*.h"], timeout=30).output
    create_calls = run(["grep", "-rn", "extern.*C.*CreateInstance", src_root,
                         "--include=*.cpp"], timeout=30).output

    so_map = {}
    for line in so_names.split("\n"):
        m = re.search(r'constexpr\s+char\s+(\w+)\[\]\s*\{\s*"([^"]+)"', line)
        if m:
            so_map[m.group(1)] = m.group(2)

    create_map = {}
    for line in create_calls.split("\n"):
        m = re.match(r"([^:]+):.*(\w+)\*\s*CreateInstance", line)
        if m:
            create_map[m.group(2)] = m.group(1)

    for line in load_calls.split("\n"):
        m = re.search(r"LoadLibrary<(\w+)>\s*\([^,]+,\s*(\w+)\)", line)
        if m:
            iface = m.group(1)
            so_name = so_map.get(m.group(2), m.group(2))
            registry[iface] = {"so": so_name, "create_src": create_map.get(iface, ""),
                                "interface": iface}
    return registry


def resolve_vtable_to_impl(mangled_type, dlopen_map, llvm_bin):
    """将 vtable 类型元数据解析为可能的实现"""
    demangled = demangle_batch(llvm_bin, [mangled_type]).get(mangled_type, mangled_type)
    m = re.search(r"(\w+)$", demangled)
    iface_name = m.group(1) if m else demangled
    if iface_name in dlopen_map:
        info = dlopen_map[iface_name]
        return iface_name, [f"[dlopen:{info['so']}]"]
    return iface_name, [f"[vtable]"]


def short_name(demangled):
    """缩短函数名"""
    m = re.search(r"(\w+::\w+)\s*\(", demangled)
    if m:
        return m.group(1)
    m = re.search(r"(\w+)\s*\(", demangled)
    return m.group(1) if m else demangled


SKIP_PREFIXES = ["HiLog", "std::__h::", "OHOS::MMI::FormatLog", "OHOS::MMI::GetSysClockTime",
                 "OHOS::MMI::InnerFunction", "__cfi_slowpath", "__ubsan", "abort", "operator new",
                 "operator delete"]


def build_call_tree(target_func, all_graphs, vtable_info, dlopen_map,
                    llvm_bin, max_depth=5, reverse=False, check_keyword=None):
    """构建候选调用树并可选检查函数名关键字"""
    merged = defaultdict(set)
    for graph in all_graphs:
        for caller, callees in graph.items():
            merged[caller].update(callees)

    merged_vtable = defaultdict(set)
    for vt in vtable_info:
        for func, types in vt.items():
            merged_vtable[func].update(types)

    all_funcs = set(merged.keys())
    for callees in merged.values():
        for _, callee in callees:
            if callee:
                all_funcs.add(callee)
    all_funcs.update(merged_vtable.keys())

    demangled = demangle_batch(llvm_bin, list(all_funcs))

    matches = [(m, demangled.get(m, m)) for m in all_funcs
               if target_func in demangled.get(m, m) or target_func in m]

    if not matches:
        print(f"未找到包含 '{target_func}' 的函数（共 {len(all_funcs)} 个）", file=sys.stderr)
        return

    if len(matches) > 1:
        print(f"找到 {len(matches)} 个匹配，使用第一个：", file=sys.stderr)
        for _, d in matches[:5]:
            print(f"  {d}", file=sys.stderr)

    root_mangled, root_demangled = matches[0]
    print(f"\n{'=' * 80}")
    print(f"候选调用边: {root_demangled}")
    print("说明: 这是静态候选边发现结果，不证明调用链完整。")
    if reverse:
        print("Reverse 说明: 当前只反查 direct call；不反查 vtable/dlopen 候选边，相关边需要人工证据或运行时 trace。")
    if check_keyword:
        print(
            f"函数名关键字启发式: {check_keyword}"
            "（仅检查 demangled 函数名和直接子函数名；"
            "不能验证参数、调用实参、成员访问或状态传递）"
        )
    print(f"{'=' * 80}\n")

    if reverse:
        reverse_graph = defaultdict(set)
        for caller, callees in merged.items():
            for _, callee in callees:
                if callee:
                    reverse_graph[callee].add(caller)
        visited = set()
        _print_tree(root_mangled, reverse_graph, {}, demangled, dlopen_map,
                    llvm_bin, max_depth, 0, visited, check_keyword, is_reverse=True)
    else:
        visited = set()
        _print_tree(root_mangled, merged, merged_vtable, demangled, dlopen_map,
                    llvm_bin, max_depth, 0, visited, check_keyword)


def _print_tree(func, graph, vtable_info, demangled, dlopen_map,
                llvm_bin, max_depth, depth, visited, check_keyword=None, is_reverse=False):
    """递归打印候选调用树"""
    if depth > max_depth or func in visited:
        return
    visited.add(func)
    indent = "  " * depth

    if is_reverse:
        callees = {("caller", c) for c in graph.get(func, set())}
    else:
        callees = graph.get(func, set())

    for call_type, callee in sorted(callees, key=lambda x: x[1] or ""):
        if callee is None:
            continue
        callee_dm = demangled.get(callee, callee)
        if any(callee_dm.startswith(p) for p in SKIP_PREFIXES):
            continue

        tag = ""
        if check_keyword:
            if check_keyword.lower() in callee_dm.lower():
                tag = " ✅"
            elif any(check_keyword.lower() in demangled.get(cc, "").lower()
                     for cc in _child_symbols(graph, callee, is_reverse)):
                tag = " ⚡"  # 子节点包含关键字

        print(f"{indent}├── {short_name(callee_dm)}{tag}")
        _print_tree(callee, graph, vtable_info, demangled, dlopen_map,
                    llvm_bin, max_depth, depth + 1, visited, check_keyword,
                    is_reverse=is_reverse)

    if not is_reverse:
        for vtype in sorted(vtable_info.get(func, set())):
            iface_name, impls = resolve_vtable_to_impl(vtype, dlopen_map, llvm_bin)
            for impl in impls:
                print(f"{indent}├── {iface_name} {impl}")


def _child_symbols(graph, func, is_reverse=False):
    """Return child symbols from either forward or reverse graph shape."""
    if is_reverse:
        return list(graph.get(func, set()))
    return [callee for _, callee in graph.get(func, set()) if callee]


def main():
    parser = argparse.ArgumentParser(
        description="OpenHarmony candidate call-edge finder (not a completeness proof)"
    )
    parser.add_argument("function", help="目标函数名（支持部分匹配）")
    parser.add_argument("--depth", type=int, default=3, help="候选边展开深度（默认 3）")
    parser.add_argument("--reverse", action="store_true",
                        help="反向查询 direct callers；不反查 vtable/dlopen 候选边")
    parser.add_argument("--oh-root", required=True, help="OpenHarmony 根目录；由 agent 显式传入")
    parser.add_argument("--repo", required=True, help="只分析指定仓；由 agent 显式传入")
    parser.add_argument("--product", help="产品名；建议由 agent 显式传入")
    parser.add_argument("--name-keyword", metavar="KEYWORD",
                        help="仅检查 demangled 函数名和直接子函数名；不验证参数、实参或成员访问")
    parser.add_argument("--check-isolation", metavar="KEYWORD",
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    oh_root = args.oh_root

    llvm_bin = find_llvm_tools(oh_root)
    if not llvm_bin:
        print("错误：找不到 LLVM 工具链（prebuilts/clang/ohos/*/llvm/bin/）", file=sys.stderr)
        sys.exit(1)

    product = args.product or find_product(oh_root)
    if not product:
        print("错误：找不到编译产品，请用 --product 指定", file=sys.stderr)
        sys.exit(1)

    obj_dir = os.path.join(oh_root, "out", product, "obj")
    if not os.path.isdir(obj_dir):
        print(f"错误：{obj_dir} 不存在，请先编译", file=sys.stderr)
        sys.exit(1)

    repo_filter = args.repo

    print(f"OH root:  {oh_root}", file=sys.stderr)
    print(f"Product:  {product}", file=sys.stderr)
    print(f"Repo:     {repo_filter or '(all)'}", file=sys.stderr)

    # 发现 dlopen 映射（基于 agent 显式传入的源码根和仓过滤）
    src_root = resolve_source_root(oh_root, repo_filter)
    print(f"发现 dlopen 映射 (source={src_root})...", file=sys.stderr)
    dlopen_map = discover_dlopen_map(src_root)
    for iface, info in dlopen_map.items():
        print(f"  {iface} -> {info['so']}", file=sys.stderr)

    # 扫描 bitcode
    print(f"扫描 bitcode (filter={repo_filter})...", file=sys.stderr)
    obj_files = find_bitcode_files(obj_dir, repo_filter)
    print(f"找到 {len(obj_files)} 个文件", file=sys.stderr)

    if not obj_files:
        print("错误：未找到 bitcode 文件。确认已编译且 --repo 过滤正确", file=sys.stderr)
        sys.exit(1)

    all_graphs = []
    all_vtable = []
    failures = []
    for i, obj_file in enumerate(obj_files):
        if (i + 1) % 20 == 0:
            print(f"  分析 {i+1}/{len(obj_files)}...", file=sys.stderr)
        graph, graph_error = extract_callgraph(llvm_bin, obj_file)
        if graph_error:
            failures.append((obj_file, "opt", graph_error))
        if graph:
            all_graphs.append(graph)
        vtable, vtable_error = extract_vtable_calls(llvm_bin, obj_file)
        if vtable_error:
            failures.append((obj_file, "llvm-dis", vtable_error))
        if vtable:
            all_vtable.append(vtable)

    if failures:
        print(f"警告: {len(failures)} 个工具调用失败，候选边可能缺失。示例：", file=sys.stderr)
        for obj_file, tool, error in failures[:5]:
            print(f"  [{tool}] {obj_file}: {error.splitlines()[0] if error else 'unknown'}",
                  file=sys.stderr)
        if len(failures) > max(5, len(obj_files) // 5):
            print("错误：失败比例过高，停止输出不可信候选图。", file=sys.stderr)
            sys.exit(1)

    print(f"分析完成，共 {sum(len(g) for g in all_graphs)} 个调用节点", file=sys.stderr)

    keyword = args.name_keyword or args.check_isolation
    if args.check_isolation:
        print(
            "警告: --check-isolation 已降级为函数名启发式；请改用 --name-keyword。"
            "它不验证参数、调用实参、成员访问或状态传递。",
            file=sys.stderr
        )

    build_call_tree(
        args.function, all_graphs, all_vtable, dlopen_map,
        llvm_bin, max_depth=args.depth, reverse=args.reverse,
        check_keyword=keyword
    )


if __name__ == "__main__":
    main()
