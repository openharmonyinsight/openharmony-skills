"""Legacy API-signature completeness heuristics, NOT a C/ArkTS compiler.

These compatibility gates detect incomplete documentation in ODK signature
notation (name(arg: type): result). True does not establish language legality,
name resolution, ABI compatibility, or validity under a target SDK/toolchain.
Keep grammar changes separate from structural refactors and cover combinations.
"""
from __future__ import annotations

import re

from odk_document import PLACEHOLDER_RE, BRACKET_PLACEHOLDER_RE, meaningful


def _nesting_positions(text: str, delimiter: str) -> list[int] | None:
    """Return delimiter positions outside type nesting, or None for invalid nesting."""

    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    closing = set(pairs.values())
    stack: list[str] = []
    positions: list[int] = []
    quote: str | None = None
    escaped = False

    for index, char in enumerate(text):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char in pairs:
            stack.append(char)
            continue
        if char in closing:
            if char == ">" and index > 0 and text[index - 1] == "=":
                continue
            if not stack or pairs[stack[-1]] != char:
                return None
            stack.pop()
            continue
        if char == delimiter and not stack:
            positions.append(index)

    return positions if not stack and quote is None else None


def _outer_parameter_close(signature: str, opening: int) -> int | None:
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(opening, len(signature)):
        char = signature[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
            if depth < 0:
                return None
    return None


def _outer_parameter_open(signature: str) -> int | None:
    """Find the method parameter list outside method-generic constraints."""
    pairs = {"<": ">", "[": "]", "{": "}"}
    stack: list[str] = []
    quote: str | None = None
    escaped = False
    for index, char in enumerate(signature):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if char == ">" and index > 0 and signature[index - 1] == "=":
                continue
            if not stack or pairs[stack[-1]] != char:
                return None
            stack.pop()
        elif char == "(" and not stack:
            return index
    return None


def _c_identifier_sequence_complete(value: str) -> bool:
    """Validate adjacent identifiers in a simple C type-specifier sequence."""
    simple = re.sub(r"\[[^\]]*\]", "", value)
    simple = re.sub(r"[*&]", " ", simple).strip()
    if re.search(r"[^A-Za-z0-9_\s]", simple):
        return False
    words = simple.split()
    qualifiers = {"const", "volatile", "restrict", "_Atomic"}
    core = [word for word in words if word not in qualifiers]
    if not core:
        return False
    if core[0] in {"struct", "union", "enum"}:
        return len(core) == 2 and bool(re.fullmatch(r"[A-Za-z_]\w*", core[1]))
    if len(core) == 1:
        return bool(re.fullmatch(r"[A-Za-z_]\w*", core[0]))
    specifiers = {
        "signed",
        "unsigned",
        "short",
        "long",
        "int",
        "char",
        "float",
        "double",
        "void",
        "_Bool",
    }
    if not all(word in specifiers for word in core):
        return False
    counts = {word: core.count(word) for word in specifiers}
    if any(counts[word] > 1 for word in specifiers - {"long"}) or counts["long"] > 2:
        return False
    if counts["signed"] and counts["unsigned"]:
        return False
    if counts["void"] or counts["_Bool"] or counts["float"]:
        return len(core) == 1
    if counts["char"]:
        return not any(counts[word] for word in {"short", "long", "int", "double"})
    if counts["double"]:
        return (
            not any(counts[word] for word in {"signed", "unsigned", "short", "int"})
            and counts["long"] <= 1
        )
    return not (counts["short"] and counts["long"])


def _arkts_type_syntax_complete(value: str) -> bool:
    """Reject expression-only tokens and invalid adjacent names in ArkTS types."""
    if re.search(r"[*/+\-]", value) or re.search(r"(?<![=])=(?!>)", value):
        return False
    for match in re.finditer(r"=>", value):
        prefix = value[: match.start()].rstrip()
        remainder = value[match.end() :].lstrip()
        if (
            not prefix.endswith(")")
            or not remainder
            or remainder[0] in ")]}> ,;:"
        ):
            return False
        # Check every arrow, including those inside generics/object types.
        # Find its parameter group backwards so nested callback groups stay intact.
        depth = 0
        opening = None
        for index in range(len(prefix) - 1, -1, -1):
            if prefix[index] == ")":
                depth += 1
            elif prefix[index] == "(":
                depth -= 1
                if depth == 0:
                    opening = index
                    break
        if opening is None or not _api_parameters_complete(
            prefix[opening + 1 : -1], language="ArkTS"
        ):
            return False
    equals_positions = _nesting_positions(value, "=")
    if equals_positions is None:
        return False
    arrow_positions = [position for position in equals_positions if value[position : position + 2] == "=>"]
    if arrow_positions:
        arrow = arrow_positions[0]
        parameters = value[:arrow].strip()
        return_type = value[arrow + 2 :].strip()
        opening = _outer_parameter_open(parameters)
        if (
            opening is None
            or _outer_parameter_close(parameters, opening) != len(parameters) - 1
            or parameters[:opening].strip() not in {"", "new", "abstract new"}
            or not return_type
            or not _arkts_type_syntax_complete(return_type)
        ):
            return False
    for delimiter in (",", ";"):
        positions = _nesting_positions(value, delimiter)
        if positions is None or positions:
            return False
    colon_positions = _nesting_positions(value, ":")
    question_positions = _nesting_positions(value, "?")
    if colon_positions is None or question_positions is None:
        return False
    conditional_depth = 0
    previous_delimiter = -1
    for position, delimiter in sorted(
        [(position, "?") for position in question_positions]
        + [(position, ":") for position in colon_positions]
    ):
        if delimiter == "?":
            if not re.search(r"\bextends\b", value[previous_delimiter + 1 : position]):
                return False
            conditional_depth += 1
        else:
            if conditional_depth == 0:
                return False
            conditional_depth -= 1
        previous_delimiter = position
    if conditional_depth:
        return False
    adjacent_identifiers = re.findall(
        r"(?=\b([A-Za-z_$][A-Za-z0-9_$]*)\s+([A-Za-z_$][A-Za-z0-9_$]*)\b)",
        value,
    )
    prefix_operators = {
        "readonly",
        "keyof",
        "typeof",
        "infer",
        "unique",
        "abstract",
        "new",
        "in",
        "extends",
    }
    return all(
        first in prefix_operators or second in {"extends", "in"}
        for first, second in adjacent_identifiers
    )


def _c_parameter_declaration_complete(value: str) -> bool:
    """Accept a parameter type or a named declaration, not an arbitrary suffix."""
    if value == "void":
        return False  # Only the sole (void) case is accepted by the caller.
    if _api_type_complete(value, language="C"):
        return True
    keywords = {
        "const", "volatile", "restrict", "_Atomic", "struct", "union", "enum",
        "signed", "unsigned", "short", "long", "int", "char", "float", "double",
        "void", "_Bool", "auto", "register", "static", "extern", "typedef",
    }
    qualifier = r"(?:const|volatile|restrict|_Atomic)\b"
    pointer = rf"(?:\*\s*(?:{qualifier}\s*)*)+"
    named_pointer = re.search(rf"\(\s*{pointer}(?P<name>[A-Za-z_]\w*)\s*\)", value)
    # Array parameter names precede their dimensions rather than ending the
    # declaration. Remove only the name and keep the abstract array declarator.
    named_array = re.search(r"\b(?P<name>[A-Za-z_]\w*)\s*(?=(?:\[[^\[\]]*\]\s*)+$)", value)
    name = named_pointer or named_array or re.search(r"(?P<name>[A-Za-z_]\w*)\s*$", value)
    if name is None or name.group("name") in keywords:
        return False
    start, end = name.span("name")
    type_name = (value[:start] + value[end:]).strip()
    if type_name == "void":
        return False
    return _api_type_complete(type_name, language="C")


def _c_type_syntax_complete(value: str) -> bool:
    """Validate C type specifiers and abstract declarators used by API signatures."""
    # A numeric operand cannot be followed by another bare operand without an
    # operator. Check dimensions before either abstract or named declarations
    # can pass; do not interpret symbols or evaluate C constant expressions.
    for dimension in re.finditer(r"\[([^\[\]]*)\]", value):
        bound = dimension.group(1).strip()
        if re.search(r"\b[0-9][A-Za-z0-9_]*\s+[A-Za-z0-9_]", bound):
            return False
        if bound not in {"", "*"} and re.search(r"[+*/%&|^?:<>=!~\-]\s*$", bound):
            return False
        # Preserve the old adjacent-name rejection without interpreting symbols.
        # sizeof(type) and array qualifiers may legitimately precede a name.
        prefixes = {"sizeof", "_Alignof", "static", "const", "volatile", "restrict",
                    "signed", "unsigned", "short", "long", "struct", "union", "enum"}
        if any(first not in prefixes for first, _ in re.findall(
            r"(?=\b([A-Za-z_]\w*)\s+([A-Za-z_0-9]\w*)\b)", bound
        )):
            return False
    # Validate function-pointer parameter types recursively instead of treating
    # parenthesized text as opaque. Qualifiers belong to each pointer level,
    # not to the return type's identifier sequence.
    qualifier = r"(?:const|volatile|restrict|_Atomic)\b"
    pointer = rf"(?:\*\s*(?:{qualifier}\s*)*)+"
    function_pointer = re.fullmatch(
        rf"(.+?)\(\s*{pointer}\)\s*\((.*)\)", value, re.DOTALL
    )
    if function_pointer:
        return_type, parameters = function_pointer.groups()
        if not _api_type_complete(return_type, language="C"):
            return False
        parameters = parameters.strip()
        # Empty lists are valid C declarations; (void) explicitly has no args.
        if not parameters or parameters == "void":
            return True
        commas = _nesting_positions(parameters, ",")
        if commas is None:
            return False
        parts = [parameters[start:end].strip() for start, end in zip(
            [0] + [position + 1 for position in commas], commas + [len(parameters)]
        )]
        for index, parameter in enumerate(parts):
            if parameter == "...":
                if index == 0 or index != len(parts) - 1:
                    return False
            elif not _c_parameter_declaration_complete(parameter):
                return False
        return True
    # Array bounds are expressions, not type specifiers. Keep the dimension
    # checks above, but do not reject arithmetic in a bound as a type operator.
    type_shape = re.sub(r"\[[^\[\]]*\]", "", value)
    if re.search(r"[$|&.:<>{}?=+/\-]", type_shape):
        return False
    for delimiter in (",", ":", ";"):
        positions = _nesting_positions(value, delimiter)
        if positions is None or positions:
            return False
    identifiers = re.findall(r"\b[A-Za-z_]\w*\b", type_shape)
    qualifiers = {"const", "volatile", "restrict", "_Atomic"}
    if not identifiers or all(identifier in qualifiers for identifier in identifiers):
        return False
    if identifiers[-1] in {"struct", "union", "enum"}:
        return False
    if re.search(
        r"\*\s*(?!const\b|volatile\b|restrict\b|_Atomic\b)([A-Za-z_]\w*)",
        type_shape,
    ):
        return False
    if re.search(r"\(\s*\*\s*[A-Za-z_]\w*", type_shape):
        return False
    sequences = re.findall(r"\b[A-Za-z_]\w*(?:\s+[A-Za-z_]\w*)+\b", type_shape)
    return all(_c_identifier_sequence_complete(sequence) for sequence in sequences)


def _api_type_complete(type_name: str, *, language: str | None = None) -> bool:
    """Validate supported C/ArkTS type syntax without accepting expressions."""
    value = type_name.strip()
    # The document-wide [text] placeholder rule is not a type grammar: ArkTS
    # tuples legitimately have this shape. Explicit placeholder words still fail.
    tuple_shape = language == "ArkTS" and value.startswith("[") and value.endswith("]")
    if (
        (not meaningful(value) and not tuple_shape)
        or BRACKET_PLACEHOLDER_RE.search(value)
        or _nesting_positions(value, ",") is None
    ):
        return False

    if tuple_shape and re.fullmatch(r"\[\s*\]", value):
        return True

    without_literals = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', "literal", value)
    if not re.search(r"[A-Za-z_$][A-Za-z0-9_$]*|\d", without_literals):
        return False
    if re.search(r"[^A-Za-z0-9_$\s.,:;<>\[\]{}()?|&=*+\-/]", without_literals):
        return False
    if re.search(r"\?{2,}", without_literals):
        return False
    if re.search(r"\|\||&&|==", without_literals):
        return False
    if re.search(r"<\s*>", without_literals):
        return False
    if re.search(r",\s*[>)}\]]", without_literals):
        return False
    if re.search(r"(?:^|[<({\[:,;=])\s*[|&]", without_literals):
        return False
    if re.search(r"[|&]\s*(?:$|[>)}\],;])", without_literals):
        return False
    if re.search(r":\s*(?:$|[,;)}\]])", without_literals):
        return False
    if re.search(r"=>\s*$", without_literals):
        return False
    if re.search(r"(?:^|[^=])=\s*$", without_literals):
        return False
    arkts_valid = _arkts_type_syntax_complete(without_literals)
    c_valid = without_literals == value and _c_type_syntax_complete(without_literals)
    if language == "ArkTS":
        return arkts_valid
    if language == "C":
        return c_valid
    return arkts_valid or c_valid


def _api_generic_parameters_complete(parameters: str, *, language: str | None = None) -> bool:
    comma_positions = _nesting_positions(parameters, ",")
    if comma_positions is None:
        return False
    starts = [0] + [position + 1 for position in comma_positions]
    ends = comma_positions + [len(parameters)]
    identifier = r"[A-Za-z_$][A-Za-z0-9_$]*"
    for start, end in zip(starts, ends):
        declaration = parameters[start:end].strip()
        equal_positions = _nesting_positions(declaration, "=")
        if equal_positions is None:
            return False
        default_positions = [
            position
            for position in equal_positions
            if position + 1 >= len(declaration) or declaration[position + 1] != ">"
        ]
        if len(default_positions) > 1:
            return False
        if default_positions:
            position = default_positions[0]
            declaration, default = declaration[:position], declaration[position + 1 :]
        else:
            default = None
        match = re.fullmatch(
            r"(?P<name>" + identifier
            + r")(?:\s+extends(?:\s+|(?=[(\[{]))(?P<constraint>.+))?",
            declaration,
        )
        if match is None:
            return False
        for value in (match.group("constraint"), default):
            if value is not None and not _api_type_complete(value, language=language):
                return False
    return True


def _api_name_complete(
    name: str, *, name_style: str = "qualified", language: str | None = None
) -> bool:
    identifier = r"[A-Za-z_$][A-Za-z0-9_$]*"
    generic_parameters: str | None = None
    base_name = name
    generic_start = name.find("<")
    if generic_start >= 0:
        if not name.endswith(">"):
            return False
        base_name = name[:generic_start]
        generic_parameters = name[generic_start + 1 : -1]
        if not generic_parameters or _nesting_positions(name[generic_start:], ",") is None:
            return False
    qualified_pattern = rf"(?:{identifier}\.)+{identifier}"
    qualified = bool(re.fullmatch(qualified_pattern, base_name))
    free_function = bool(re.fullmatch(identifier, base_name))
    valid_name = {
        "qualified": qualified,
        "free": free_function,
        "either": qualified or free_function,
    }.get(name_style, False)
    if not valid_name:
        return False
    return generic_parameters is None or _api_generic_parameters_complete(
        generic_parameters, language=language
    )


def _api_parameters_complete(parameters: str, *, language: str | None = None) -> bool:
    if not parameters.strip():
        return True
    comma_positions = _nesting_positions(parameters, ",")
    if comma_positions is None:
        return False
    starts = [0] + [position + 1 for position in comma_positions]
    ends = comma_positions + [len(parameters)]
    for start, end in zip(starts, ends):
        parameter = parameters[start:end].strip()
        colon_positions = _nesting_positions(parameter, ":")
        if colon_positions is None or not colon_positions:
            return False
        colon = colon_positions[0]
        name = parameter[:colon].strip()
        type_name = parameter[colon + 1 :].strip()
        if not re.fullmatch(r"(?:\.\.\.)?[A-Za-z_$][A-Za-z0-9_$]*\??", name):
            return False
        if not _api_type_complete(type_name, language=language):
            return False
    return True


def api_signature_complete(
    signature: str, *, name_style: str = "qualified", language: str | None = None
) -> bool:
    normalized = canonical_api_signature(signature)
    if not normalized or PLACEHOLDER_RE.match(normalized) or BRACKET_PLACEHOLDER_RE.search(normalized):
        return False
    opening = _outer_parameter_open(normalized)
    if opening is None or opening <= 0:
        return False
    close = _outer_parameter_close(normalized, opening)
    if close is None:
        return False
    name = normalized[:opening].strip()
    parameters = normalized[opening + 1 : close].strip()
    return_match = re.fullmatch(r"\s*:\s*(\S[\s\S]*)", normalized[close + 1 :])
    if return_match is None:
        return False
    return_type = return_match.group(1).strip()
    if not _api_name_complete(name, name_style=name_style, language=language):
        return False
    if not _api_type_complete(return_type, language=language):
        return False
    if not _api_parameters_complete(parameters, language=language):
        return False
    return True


def canonical_api_signature(signature: str) -> str:
    source = signature.strip().strip("`")
    punctuation = set("(),:;<>[]{}?|&=*")
    result: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(source):
        char = source[index]
        if quote is not None:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
            result.append(char)
            index += 1
            continue
        if char.isspace():
            next_index = index + 1
            while next_index < len(source) and source[next_index].isspace():
                next_index += 1
            previous = result[-1] if result else ""
            following = source[next_index] if next_index < len(source) else ""
            if previous and following and previous not in punctuation and following not in punctuation:
                result.append(" ")
            index = next_index
            continue
        result.append(char)
        index += 1
    return "".join(result)
