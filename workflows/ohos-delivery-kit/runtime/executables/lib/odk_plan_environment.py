"""Shared validation of declared host-only or target build environments."""
from __future__ import annotations

import re
import shlex

if __package__:
    from .odk_document import (
        BRACKET_PLACEHOLDER_RE, meaningful, require_unique_section,
        require_unique_table_with_columns, tables_with_columns,
    )
else:
    from odk_document import (
        BRACKET_PLACEHOLDER_RE, meaningful, require_unique_section,
        require_unique_table_with_columns, tables_with_columns,
    )

SECTION = "构建与验证环境"
EMULATOR = "模拟器命令（仅 arm64_virt）"
EXISTING_PREPARATION = "使用设备现有版本，不获取 daily、不刷机"
TARGET_COMMAND_RE = re.compile(
    r"\bhdc(?:\.exe)?\b|\bqemu-system-[A-Za-z0-9_-]+\b|--product-name\b|(?<![\w.-])build\.sh\b",
    re.IGNORECASE,
)
SHELLS = {"bash", "sh", "zsh", "dash"}


def _target_invocation(words: list[str]) -> bool:
    while words and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0])
                     or words[0] in {"if", "then", "elif", "while", "until", "do", "!"}):
        words = words[1:]
    if not words:
        return False
    executable = words[0].rsplit("/", 1)[-1].casefold()
    args = words[1:]
    if executable in {"env", "sudo", "command", "exec", "nohup", "time"}:
        while args and args[0].startswith("-"):
            option = args.pop(0)
            if option == "--":
                break
            if executable == "command" and option in {"-v", "-V", "-pv", "-pV"}:
                return False  # Tool lookup does not invoke the named tool.
            if option in {"-u", "-g", "-C", "--unset", "--chdir", "--user", "--group"} and args:
                args.pop(0)
        return _target_invocation(args)
    if executable in SHELLS:
        noexec = interactive = False
        while args and args[0].startswith(("-", "+")):
            option = args.pop(0)
            if option == "--":
                break
            if option in {"--help", "--version"}:
                return False
            short = option[1:] if not option.startswith("--") else ""
            if "n" in short or option == "--noexec":
                noexec = not option.startswith("+")
            if "i" in short:
                interactive = not option.startswith("+")
            if "c" in short:
                return bool(args) and not (noexec and not interactive) and command_uses_target(args[0])
            if option in {"-o", "+o", "-O", "+O", "--rcfile", "--init-file"} and args:
                value = args.pop(0)
                if option in {"-o", "+o"} and value == "noexec":
                    noexec = option == "-o"
        if noexec and not interactive:
            return False  # bash -n reads syntax without executing the script.
        return _target_invocation(args)
    if executable in {"build.sh", "hdc", "hdc.exe"} or executable.startswith("qemu-system-"):
        return True
    # Product flags on a wrapper command still declare a target dependency.
    if "--" in args:
        args = args[:args.index("--")]
    return any(arg == "--product-name" or arg.startswith("--product-name=") for arg in args)


def command_parts(command: str) -> list[str]:
    """Split shell operators without treating quoted arguments as operators."""
    parts, current = [], []
    quote = ""
    escaped = comment = word_started = False
    for char in command:
        if comment:
            if char != "\n":
                continue
            comment = False
        if escaped:
            current.append(char)
            escaped = False
            word_started = True
        elif char == "\\" and quote != "'":
            current.append(char)
            escaped = True
        elif quote:
            current.append(char)
            if char == quote:
                quote = ""
        elif char in "\"'":
            current.append(char)
            quote = char
            word_started = True
        elif char == "#" and not word_started:
            comment = True
        elif char in ";&|()\n":
            parts.append("".join(current))
            current = []
            word_started = False
        else:
            current.append(char)
            word_started = char not in " \t\r"
    parts.append("".join(current))
    return parts


def command_uses_target(command: str) -> bool:
    """Recognize direct tools and shell wrappers, rather than file arguments."""
    command = command.replace("`", "")  # Markdown inline-code delimiters.
    try:
        return any(_target_invocation(shlex.split(part)) for part in command_parts(command))
    except ValueError:
        # Ambiguous quoting cannot hide an otherwise explicit target command.
        return bool(TARGET_COMMAND_RE.search(command))


def task_verification_commands(plan: str) -> list[tuple[str, str]]:
    """Read executable table fields; comments and fenced examples are inert."""
    commands: list[tuple[str, str]] = []
    task_list = require_unique_section(plan, "Task 列表")
    if task_list is not None:
        rows = require_unique_table_with_columns(task_list, ["TASK ID", "验证命令"]) or []
        commands.extend((f"Task 列表 {row['TASK ID']}", row["验证命令"]) for row in rows)
    details = require_unique_section(plan, "Task 详情")
    if details is not None:
        for table in tables_with_columns(details, ["Command / Evidence"]):
            commands.extend(("Task 详情 Verification", row["Command / Evidence"]) for row in table)
    return commands


def _host_only_task_errors(plan: str) -> list[str]:
    errors = []
    try:
        for context, command in task_verification_commands(plan):
            if command_uses_target(command):
                errors.append(f"host-only {context} 包含目标编译或设备依赖；必须恢复产品确认和目标环境")
    except ValueError as error:
        errors.append(f"host-only Task 命令无法明确解析：{error}")
    return errors


def environment_errors(plan: str, template: str, *, host_only_required: bool = False) -> list[str]:
    # Lite is host-only even when a plan omits or obscures its environment.
    errors = _host_only_task_errors(plan) if host_only_required else []
    try:
        schema_body = require_unique_section(template, SECTION)
        schema = require_unique_table_with_columns(schema_body or "", ["配置项", "值"])
        if not schema:
            return errors + [f"模板 {SECTION} 缺少配置表"]
        body = require_unique_section(plan, SECTION)
        table = require_unique_table_with_columns(body or "", ["配置项", "值"])
    except ValueError as error:
        return errors + [f"{SECTION}: {error}"]
    if not table:
        return errors + [f"{SECTION} 缺少非空的「配置项 / 值」表"]

    values: dict[str, str] = {}
    for row in table:
        key = row["配置项"].strip().strip("`").strip()
        if key in values:
            errors.append(f"{SECTION} 配置项重复：{key}")
        values[key] = row["值"].strip().strip("`").strip()

    host_only = values.get("验证范围", "").strip().casefold() == "host-only"
    if host_only_required and not host_only:
        errors.append(f"{SECTION} lite 必须声明「验证范围 = host-only」")
    if host_only:
        command = values.get("测试命令", "")
        if (not meaningful(command) or BRACKET_PLACEHOLDER_RE.search(command)
                or re.search(r"\b(?:TBD|TODO)\b|待填写|\{product\}", command, re.I)):
            errors.append(f"{SECTION} host-only 必须填写实际测试命令")
        for key in ("编译产品", "可选编译产品", "编译命令（全量）", EMULATOR,
                    "设备版本策略", "设备版本准备方式"):
            if values.get(key, "") not in {"", "N/A", "不适用"}:
                errors.append(f"{SECTION} host-only 不得携带目标产品/设备配置：{key}")
        if command_uses_target(command):
            errors.append(f"{SECTION} host-only 命令包含目标编译或设备依赖")
        if not host_only_required:
            errors.extend(_host_only_task_errors(plan))
        return errors

    product = values.get("编译产品", "")
    for row in schema:
        key = row["配置项"]
        value = values.get(key, "")
        # Physical products may omit this field or mark it inapplicable, but
        # a supplied command must still have all placeholders resolved.
        if (key == EMULATOR and product != "arm64_virt"
                and value in {"", "N/A", "不适用", "不适用（物理板）"}):
            continue
        if (not meaningful(value) or BRACKET_PLACEHOLDER_RE.search(value)
                or re.search(r"\b(?:TBD|TODO)\b|待填写|待确认|待补充|\{product\}", value, re.I)):
            errors.append(f"{SECTION} 配置项缺失或未解析：{key}")

    options = values.get("可选编译产品", "").split()
    if not product or len(product.split()) != 1 or product not in options:
        errors.append(f"{SECTION} 编译产品必须是候选列表中的单个产品")
    if product == "arm64_virt":
        for key in ("设备版本策略", "设备版本准备方式"):
            if values.get(key) != "不适用（QEMU）":
                errors.append(f"{SECTION} QEMU 的{key}必须为「不适用（QEMU）」")
        if values.get(EMULATOR, "").startswith(("不适用", "N/A")):
            errors.append(f"{SECTION} QEMU 必须填写模拟器命令")
    else:
        policy = values.get("设备版本策略", "")
        preparation = values.get("设备版本准备方式", "")
        if policy not in {"daily", "existing"}:
            errors.append(f"{SECTION} 物理产品必须明确选择 daily 或 existing")
        elif policy == "existing" and EXISTING_PREPARATION not in preparation:
            errors.append(f"{SECTION} existing 的设备版本准备方式必须包含「{EXISTING_PREPARATION}」")
        elif policy == "daily" and (
            preparation.casefold().startswith(("不适用", "n/a"))
            or "使用设备现有版本" in preparation
        ):
            errors.append(f"{SECTION} daily 的设备版本准备方式必须说明镜像/设备准备，不能使用不适用或现有版本策略")
    return errors
