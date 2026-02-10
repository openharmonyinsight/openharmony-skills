#!/usr/bin/env python3
"""
获取OpenHarmony编译命令的工具

使用方法:
    python3 get_compile_command.py <源文件路径>

示例:
    python3 get_compile_command.py frameworks/core/components_ng/base/frame_node.cpp
    python3 get_compile_command.py foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp
"""

import os
import sys
import re
from pathlib import Path


def find_ninja_files(out_dir):
    """查找所有相关的ninja文件"""
    ninja_files = []

    # 查找toolchain.ninja
    toolchain_ninja = os.path.join(out_dir, "toolchain.ninja")
    if os.path.exists(toolchain_ninja):
        ninja_files.append(('toolchain', toolchain_ninja))

    # 查找所有的子ninja文件
    obj_dir = os.path.join(out_dir, "obj")
    if os.path.exists(obj_dir):
        for root, dirs, files in os.walk(obj_dir):
            for file in files:
                if file.endswith('.ninja'):
                    ninja_files.append(('sub', os.path.join(root, file)))

    return ninja_files


def parse_cxx_rule(toolchain_ninja):
    """从toolchain.ninja解析cxx规则"""
    with open(toolchain_ninja, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    cxx_command = None
    in_cxx_rule = False

    for line in lines:
        if line.strip() == 'rule cxx':
            in_cxx_rule = True
            continue

        if in_cxx_rule:
            if line.strip().startswith('command ='):
                cxx_command = line.split('=', 1)[1].strip()
                break
            elif line.strip() and not line.startswith(' '):
                # 遇到新的规则，退出
                break

    return cxx_command


def parse_variables(ninja_file):
    """解析ninja文件中的所有变量"""
    variables = {}

    with open(ninja_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    for line in lines:
        # 解析变量定义 (var = value)
        if '=' in line and not line.strip().startswith('#'):
            # 跳过build规则
            if line.strip().startswith('build '):
                continue
            # 跳过rule定义
            if line.strip().startswith('rule '):
                continue

            parts = line.split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                var_value = parts[1].strip()

                # 只保存我们关心的变量
                if var_name in ['defines', 'include_dirs', 'cflags', 'cflags_cc',
                               'cflags_pch_cxx', 'root_out_dir', 'target_output_name']:
                    variables[var_name] = var_value

        # 遇到build规则就停止解析变量
        if line.strip().startswith('build '):
            break

    return variables


def find_build_rule(source_file, ninja_files):
    """在ninja文件中查找对应源文件的编译规则"""
    source_basename = os.path.basename(source_file)

    for ninja_type, ninja_path in ninja_files:
        if ninja_type == 'toolchain':
            continue

        # 只查找可能包含这个源文件的ninja文件
        # 根据源文件路径推断ninja文件位置
        if 'ace_engine' in source_file:
            if 'ace_engine' not in ninja_path:
                continue

        try:
            with open(ninja_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # 逐行查找，而不是使用正则表达式读取整个文件
            for i, line in enumerate(lines):
                # 查找包含源文件名的build规则
                if line.strip().startswith('build ') and source_basename in line:
                    # 检查是否是cxx编译规则
                    if '.o:' in line and 'cxx' in line:
                        # 获取下一行，查看source_file_part
                        if i + 1 < len(lines):
                            next_line = lines[i + 1]
                            if f'source_file_part = {source_basename}' in next_line:
                                # 提取输出文件路径和源文件路径
                                # 格式: build obj/.../xxx.o: cxx ../../path/to/source.cpp
                                # 提取 cxx 后面的源文件路径
                                if 'cxx' in line:
                                    # 分割获取cxx后面的部分
                                    cxx_part = line.split('cxx', 1)[1].strip()
                                    # 移除 || 后面的依赖部分
                                    source_path = cxx_part.split('||')[0].strip()
                                    # 提取输出文件路径
                                    build_part = line.split(':')[0].replace('build ', '').strip()
                                    return ninja_path, build_part, source_path

        except Exception as e:
            continue

    return None, None, None


def expand_variables(command_template, variables, output_file, source_file):
    """展开变量生成完整命令"""
    import re

    # 替换ninja变量
    command = command_template

    # 替换特殊变量
    command = command.replace('${out}', output_file)
    command = command.replace('${in}', source_file)

    # 替换其他变量
    for var_name, var_value in variables.items():
        placeholder = '${' + var_name + '}'
        if placeholder in command:
            # Unescape ninja variables to shell syntax
            # ninja escapes $ as \$, * as \*, < as \<, > as \>
            unescaped_value = var_value.replace('\\$', '$').replace('\\*', '*').replace('\\<', '<').replace('\\>', '>')

            # Fix shell arithmetic expressions in defines
            # The pattern is: N1$ op$ N2$ op$ N3 where $ appears after each number/operator
            # Convert to proper shell arithmetic: $((N1 op N2 op N3))
            if var_name in ['defines', 'cflags', 'cflags_cc']:
                # Match patterns like: 8$ *$ 1024$ *$ 1024 or 1$ <<$ 20
                # Group 1: first number, Group 2: operator (first), Group 3: second number, Group 4: operator (second), Group 5: third number
                unescaped_value = re.sub(
                    r'(\d+)\$\s*(\*|<<|>>)\$\s*(\d+)(?:\s*\$\s*(\*|<<|>>)\$\s*(\d+))?',
                    lambda m: f'$(({m.group(1)} {m.group(2)} {m.group(3)}{f" {m.group(4)} {m.group(5)}" if m.group(4) else ""}))',
                    unescaped_value
                )

            command = command.replace(placeholder, unescaped_value)

    return command


def get_compile_command(source_file, out_dir=None):
    """主函数：获取源文件的编译命令"""

    # 确定out目录
    if out_dir is None:
        # 默认查找out目录
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            potential_out = current_dir / "out" / "rk3568"
            if potential_out.exists():
                out_dir = str(potential_out)
                break
            current_dir = current_dir.parent

    if out_dir is None or not os.path.exists(out_dir):
        print(f"错误: 找不到out目录: {out_dir}")
        return None

    print(f"使用out目录: {out_dir}")

    # 规范化源文件路径
    source_file = source_file.replace('foundation/arkui/ace_engine/', '')
    source_file = source_file.replace('frameworks/', 'foundation/arkui/ace_engine/frameworks/')

    # 如果路径不包含ace_engine部分，尝试补充
    if 'ace_engine' not in source_file and source_file.startswith('frameworks/core'):
        source_file = f'foundation/arkui/ace_engine/{source_file}'

    print(f"查找源文件: {source_file}")

    # 1. 查找所有ninja文件
    ninja_files = find_ninja_files(out_dir)
    if not ninja_files:
        print("错误: 找不到ninja文件")
        return None

    print(f"找到 {len(ninja_files)} 个ninja文件")

    # 2. 获取cxx规则
    toolchain_ninja = None
    for ninja_type, ninja_path in ninja_files:
        if ninja_type == 'toolchain':
            toolchain_ninja = ninja_path
            break

    if not toolchain_ninja:
        print("错误: 找不到toolchain.ninja")
        return None

    cxx_template = parse_cxx_rule(toolchain_ninja)
    if not cxx_template:
        print("错误: 无法解析cxx规则")
        return None

    print(f"CXX模板: {cxx_template[:100]}...")

    # 3. 查找对应的build规则
    ninja_path, output_file, source_path_in_ninja = find_build_rule(source_file, ninja_files)

    if not ninja_path:
        print(f"错误: 找不到源文件的编译规则: {source_file}")
        return None

    print(f"找到编译规则在: {ninja_path}")
    print(f"输出文件: {output_file}")
    print(f"源文件路径: {source_path_in_ninja}")

    # 4. 解析变量
    variables = parse_variables(ninja_path)

    if not variables:
        print("警告: 无法解析变量，使用基础命令")

    # 5. 生成完整命令
    full_command = expand_variables(cxx_template, variables, output_file, source_path_in_ninja)

    return full_command


def save_command_to_file(command, source_file, out_dir):
    """将原始编译命令保存到文件"""
    # 生成输出文件名
    source_basename = os.path.basename(source_file).replace('.cpp', '').replace('.cc', '').replace('.c', '')
    output_file = os.path.join(out_dir, f"{source_basename}_compile_command.sh")

    # 生成脚本内容
    from datetime import datetime
    script_content = f"""#!/bin/bash
# 自动生成的编译脚本（原始命令，带ccache）
# 源文件: {source_file}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 说明: 使用原始编译命令，包含ccache加速，适合日常开发

cd {os.path.dirname(os.path.abspath(out_dir))}

{command}

echo "编译完成: {source_file}"
"""

    # 写入文件
    with open(output_file, 'w') as f:
        f.write(script_content)

    # 添加执行权限
    os.chmod(output_file, 0o755)

    return output_file


def save_enhanced_command_to_file(enhanced_command, source_file, out_dir):
    """
    将增强版编译命令（带性能监控）保存到文件
    文件名格式: compile_single_file_{file_name}.sh
    """
    # 生成输出文件名（使用用户要求的格式）
    source_basename = os.path.basename(source_file).replace('.cpp', '').replace('.cc', '').replace('.c', '')
    output_file = os.path.join(out_dir, f"compile_single_file_{source_basename}.sh")

    # 生成脚本内容
    from datetime import datetime
    script_content = f"""#!/bin/bash
# 增强编译脚本（带性能监控）
# 源文件: {source_file}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# 功能特性:
#   - 去除 ccache，获得真实编译性能数据
#   - 使用 -save-temps=obj 生成预编译文件 (.ii)
#   - 统计编译时间和峰值内存使用
#   - 一次编译同时生成 .ii 和 .o 文件
#
# 使用方法:
#   1. 此脚本必须在 out/{{product}} 目录下执行
#   2. 执行方式: bash compile_single_file_{source_basename}.sh
#   3. 可以多次重复执行以进行性能测试
#
# 输出文件:
#   - 预编译文件: .ii 文件（用于依赖分析）
#   - 目标文件: .o 文件（编译产物）
#

set -e

# 确保在正确的目录执行
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "增强编译（带性能监控）"
echo "========================================"
echo "源文件: {source_file}"
echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "工作目录: $(pwd)"
echo "========================================"
echo ""

# 执行增强编译命令
{enhanced_command}

echo ""
echo "========================================"
echo "✓ 编译完成！"
echo "========================================"
"""

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)

    # 添加执行权限
    os.chmod(output_file, 0o755)

    return output_file


def generate_enhanced_command(command, source_file):
    """
    生成增强的编译命令：
    1. 去掉 ccache
    2. 使用 -save-temps 一次编译同时生成 .ii 预编译文件和 .o 目标文件
    3. 增加统计编译时间和峰值内存的命令（简短格式）
    """
    import re

    # 1. 去掉 ccache（如果存在）
    enhanced_command = re.sub(r'/usr/bin/ccache\s+', '', command)
    enhanced_command = re.sub(r'^ccache\s+', '', enhanced_command)

    # 提取编译器路径和源文件
    compiler_match = re.search(r'(../../prebuilts/clang/ohos/\S+/llvm/bin/clang\+\+)', enhanced_command)
    if not compiler_match:
        return None
    compiler = compiler_match.group(1)

    source_match = re.search(r'-c\s+(\S+\.c[cp]{0,2})\s+-o\s+(\S+\.o)', enhanced_command)
    if not source_match:
        return None

    source_path = source_match.group(1)
    output_obj = source_match.group(2)

    # 生成文件路径
    source_basename = os.path.basename(source_file).replace('.cpp', '').replace('.cc', '').replace('.c', '')
    output_dir = os.path.dirname(output_obj)
    ii_file = os.path.join(output_dir, f"{source_basename}.ii")

    # 提取编译选项（除了 -c, -o, 源文件, 输出文件）
    base_options = enhanced_command
    base_options = re.sub(r'-c\s+\S+\.c[cp]{0,2}\s+-o\s+\S+\.o', '', base_options)
    base_options = re.sub(r'^\S+\s+', '', base_options)  # 移除编译器路径
    base_options = ' '.join(base_options.split())

    # 添加抑制 -save-temps 告警的选项
    # -save-temps 可能触发 -Wundefined-bool-conversion 告警
    # 添加 -Wno-undefined-bool-conversion 来抑制
    # 添加 -Wno-tautological-compare 和 -Wno-error=tautological-compare 来抑制自我比较告警
    base_options += ' -Wno-undefined-bool-conversion -Wno-tautological-compare'

    # 使用 -save-temps=obj 一次编译生成所有中间文件
    # -save-temps=obj 会在输出目录保存所有中间文件，包括 .i (预处理文件)
    # 编译完成后将 .i 重命名为 .ii
    script_cmd = f"""/usr/bin/time -f "编译时间: %E\\n峰值内存: %M KB" {compiler} -save-temps=obj -c {base_options} {source_path} -o {output_obj} && mv {output_dir}/{source_basename}.i {ii_file} 2>/dev/null || true && echo "✓ 已生成: {ii_file} {output_obj}" """

    return script_cmd


def main():
    if len(sys.argv) < 2:
        print("用法: python3 get_compile_command.py <源文件路径> [out目录] [选项]")
        print()
        print("选项:")
        print("  --save           保存原始编译命令到脚本文件")
        print("  --save-enhanced  保存增强编译命令（带性能监控）到脚本文件")
        print()
        print("示例:")
        print("  python3 get_compile_command.py frameworks/core/components_ng/base/frame_node.cpp")
        print("  python3 get_compile_command.py foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp")
        print("  python3 get_compile_command.py frameworks/core/components_ng/base/frame_node.cpp /path/to/out/rk3568")
        print("  python3 get_compile_command.py frameworks/core/components_ng/base/frame_node.cpp --save")
        print("  python3 get_compile_command.py frameworks/core/components_ng/base/frame_node.cpp --save-enhanced")
        sys.exit(1)

    source_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    save_to_file = '--save' in sys.argv
    save_enhanced = '--save-enhanced' in sys.argv

    command = get_compile_command(source_file, out_dir)

    if command:
        print()
        print("=" * 80)
        print("【1】原始编译命令（带ccache）:")
        print("=" * 80)
        print()
        print(command)

        # 生成增强命令
        enhanced = generate_enhanced_command(command, source_file)

        if enhanced:
            print()
            print()
            print("=" * 80)
            print("【2】增强编译命令（生成.ii + 无ccache + 性能统计）:")
            print("=" * 80)
            print()
            print(enhanced)

            print()
            print("=" * 80)
            print("说明:")
            print("  - 【1】原始命令: 使用ccache，适合日常开发，编译速度较快")
            print("  - 【2】增强命令: 使用 -save-temps 一次编译同时生成.ii和.o文件")
            print("    * -save-temps=obj 保留所有中间文件（包括预编译文件）")
            print("    * 添加 -Wno-undefined-bool-conversion 抑制相关告警")
            print("    * 添加 -Wno-tautological-compare")
            print("      抑制自我比较告警（避免编译失败）")
            print("    * 只需编译一次，同时获得 .ii 和 .o 文件")
            print("    * 去除 ccache 以获得真实性能数据")
            print("    * 统计整个编译过程的时间和内存")
            print()
            print("保存选项:")
            print("  --save           保存原始命令为 {file}_compile_command.sh")
            print("  --save-enhanced  保存增强命令为 compile_single_file_{file}.sh")
            print("                    （可在 out/{{product}} 目录重复执行）")
            print("=" * 80)
        else:
            print()
            print("警告: 无法生成增强命令（可能是命令格式不匹配）")

        print()

        # 保存到文件
        if save_to_file or save_enhanced:
            if out_dir is None:
                # 自动查找out目录
                current_dir = Path.cwd()
                while current_dir != current_dir.parent:
                    potential_out = current_dir / "out" / "rk3568"
                    if potential_out.exists():
                        out_dir = str(potential_out)
                        break
                    current_dir = current_dir.parent

            if out_dir:
                # 保存原始命令
                if save_to_file:
                    script_file = save_command_to_file(command, source_file, out_dir)
                    print()
                    print(f"✓ 原始编译命令已保存到: {script_file}")
                    print(f"  执行方式: bash {script_file}")

                # 保存增强命令
                if save_enhanced and enhanced:
                    enhanced_script = save_enhanced_command_to_file(enhanced, source_file, out_dir)
                    print()
                    print(f"✓ 增强编译命令已保存到: {enhanced_script}")
                    print(f"  执行方式: cd {out_dir} && bash {os.path.basename(enhanced_script)}")
                    print()
                    print(f"  脚本功能:")
                    print(f"    - 自动切换到正确的执行目录")
                    print(f"    - 带性能监控（编译时间 + 峰值内存）")
                    print(f"    - 生成 .ii 和 .o 文件")
                    print(f"    - 可重复执行多次进行性能测试")

    else:
        print("失败: 无法获取编译命令")
        sys.exit(1)


if __name__ == '__main__':
    main()
