#!/usr/bin/env python3
"""
V1->V2 Migration - Component Analyzer
Analyzes .ets files to extract component structure: decorators, state variables,
inputs/outputs, child components, and migration-relevant patterns.

Usage:
    python3 component_analyzer.py <file_or_dir> [--json] [--recursive]
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# V1 state decorators
V1_DECORATORS = {
    '@State', '@Prop', '@Link', '@ObjectLink', '@Provide', '@Consume',
    '@Watch', '@StorageLink', '@StorageProp', '@LocalStorageLink', '@LocalStorageProp',
}
# V2 state decorators
V2_DECORATORS = {
    '@Local', '@Param', '@Event', '@Provider', '@Consumer', '@Monitor',
    '@Computed', '@Once',
}
# Component-level decorators
COMPONENT_DECORATORS = {'@Component', '@ComponentV2'}
# Class-level decorators
CLASS_DECORATORS = {'@Observed', '@ObservedV2'}
# Reusable decorators
REUSABLE_DECORATORS = {'@Reusable', '@ReusableV2'}
# Simple types that can be passed between V1/V2 without restrictions
SIMPLE_TYPES = {'number', 'string', 'boolean', 'undefined', 'null', 'bool'}
# Built-in collection types
BUILTIN_TYPES = {'Array', 'Map', 'Set', 'Date'}
# Storage decorators whose argument is a key for cross-referencing with API calls
_STORAGE_KEY_DECORATORS = {'@StorageLink', '@StorageProp', '@LocalStorageLink', '@LocalStorageProp'}

# Decorators representing data flowing INTO a component — via constructor params
# (@Prop/@Link/@ObjectLink/@Param) OR via key-based subscription (@Consume/@Consumer,
# @StorageProp/@StorageLink/LocalStorage*). @Event counts as input (callback param).
# These are classified by decorator IDENTITY, independent of any init parameter, because
# key-based channels (Provide/Consume, Storage) carry data with no constructor argument.
INPUT_DECORATORS = {
    '@Prop', '@Link', '@ObjectLink', '@Param', '@Event',
    '@Consume', '@Consumer',
    '@StorageProp', '@StorageLink', '@LocalStorageProp', '@LocalStorageLink',
}
# Decorators representing data flowing OUT of a component — via emitted callbacks (@Event)
# OR via key-based publication (@Provide/@Provider).
OUTPUT_DECORATORS = {
    '@Event',
    '@Provide', '@Provider',
}
# Decorators that establish a key-based binding channel (used by the dependency tracer
# to couple components that share a key even when build() passes no arguments).
_KEY_CHANNEL_DECORATORS = {
    '@Provide', '@Provider', '@Consume', '@Consumer',
    '@StorageProp', '@StorageLink', '@LocalStorageProp', '@LocalStorageLink',
}


def read_file(filepath: str) -> Optional[str]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return None


def strip_comments(content: str) -> str:
    """Blank out ``//`` line comments and ``/* */`` block comments.

    Comment text is replaced with spaces while preserving length and newlines,
    so every character offset and line number computed downstream (e.g.
    ``_compute_line_number``) stays valid against the original file.

    String literals (``'...'``, ``"..."``, `` `...` ``) are respected so that
    ``//`` inside a string (e.g. a URL like ``'https://...'``) is not stripped.
    Escapes (``\\'`` etc.) are handled.

    Limitation: regex literals containing ``//`` (e.g. ``/https?:\\/\\//``) are
    not recognised and may be partially blanked. ArkUI UI code rarely uses such
    literals; verify manually if your code does.
    """
    out = list(content)
    i = 0
    n = len(content)
    in_str = None  # one of "'", '"', '`', or None
    while i < n:
        c = content[i]
        if in_str is not None:
            if c == '\\':
                i += 2  # skip the escaped char
                continue
            if c == in_str:
                in_str = None
            i += 1
            continue
        # not inside a string
        if c in ('"', "'", '`'):
            in_str = c
            i += 1
            continue
        if c == '/' and i + 1 < n and content[i + 1] == '/':
            j = i
            while j < n and content[j] != '\n':
                out[j] = ' '
                j += 1
            i = j
            continue
        if c == '/' and i + 1 < n and content[i + 1] == '*':
            out[i] = ' '
            out[i + 1] = ' '
            j = i + 2
            while j < n and not (content[j] == '*' and j + 1 < n and content[j + 1] == '/'):
                if content[j] != '\n':
                    out[j] = ' '
                j += 1
            if j < n:  # found closing */
                out[j] = ' '
                out[j + 1] = ' '
                j += 2
            i = j
            continue
        i += 1
    return ''.join(out)


def normalize_decorator(dec: str) -> str:
    return dec.strip().rstrip('()').split('(')[0].strip()


def extract_decorator_arg(dec: str) -> Optional[str]:
    """Extract the first string argument from a decorator.
    E.g. @StorageLink('PropA') -> 'PropA', @Provide('token') -> 'token'.
    Returns None if no string argument found.
    """
    m = re.search(r'\(\s*[\'\"]([^\'\"]+)[\'\"]', dec)
    return m.group(1) if m else None


def _get_file_type(filepath: str) -> str:
    """Return file type based on extension: 'ts', 'ets', or 'unknown'."""
    if filepath.endswith('.d.ts'):
        return 'd.ts'
    elif filepath.endswith('.ets'):
        return 'ets'
    elif filepath.endswith('.ts'):
        return 'ts'
    return 'unknown'


def extract_components(content: str, filepath: str) -> List[Dict]:
    """Extract all component definitions from .ets content."""
    components = []

    # Match @Component/@ComponentV2 (with optional export/other keywords) struct XXX
    pattern = r'(@Component(?:V2)?)\s+(?:export\s+)?(?:@\w+(?:\([^)]*\))?\s+)*struct\s+(\w+)'
    for m in re.finditer(pattern, content):
        comp_decorator = m.group(1)
        comp_name = m.group(2)
        start_pos = m.start()

        # Find the struct body by counting braces
        brace_start = content.find('{', m.end() - 1)
        if brace_start == -1:
            continue

        body = extract_brace_block(content, brace_start)
        if body is None:
            continue

        # Check for additional decorators between component decorator and struct
        between = content[m.end():content.find('struct', m.start())]
        extra_decorators = re.findall(r'(@\w+(?:\([^)]*\))?)', between)

        # Look backwards up to 500 chars for @Entry and @Reusable
        pre_text = content[max(0, start_pos - 500):start_pos]
        is_entry = bool(re.search(r'@Entry', pre_text))
        is_reusable = bool(re.search(r'@Reusable(?:V2)?', pre_text))

        state_vars = extract_state_variables(body)
        used_components = extract_child_components(body, comp_name)
        rendering_info = extract_rendering_patterns(body)
        app_state_info = extract_app_state_patterns(body)

        # Input/output are classified by decorator IDENTITY. Key-based channels
        # (@Provide/@Consume, Storage*) carry data with no constructor argument, so
        # they must NOT be gated on has_external_init (which is always False here).
        has_input = any(sv['decorator'] in INPUT_DECORATORS for sv in state_vars)
        # Output: an emitted callback (@Event), a key publication (@Provide/@Provider),
        # OR an implicit V1 output via passing @State/@Provide to a child @Prop/@Link.
        has_output = any(sv['decorator'] in OUTPUT_DECORATORS for sv in state_vars) \
            or len(used_components) > 0

        # Determine version
        version = 'V2' if comp_decorator == '@ComponentV2' else 'V1'

        components.append({
            'name': comp_name,
            'file': filepath,
            'version': version,
            'decorator': comp_decorator,
            'isEntry': is_entry,
            'isReusable': is_reusable,
            'stateVariables': state_vars,
            'inputs': [sv['name'] for sv in state_vars
                       if sv['decorator'] in ('@Prop', '@Link', '@ObjectLink', '@Param')],
            'outputs': [sv['name'] for sv in state_vars if sv['decorator'] == '@Event'],
            'hasInput': has_input,
            'hasOutput': has_output,
            'usedComponents': used_components,
            'rendering': rendering_info,
            'appState': app_state_info,
        })

    return components


def extract_brace_block(content: str, start: int) -> Optional[str]:
    """Extract content between matching braces starting at start position."""
    if start >= len(content) or content[start] != '{':
        return None
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[start + 1:i]
        i += 1
    return None


def extract_state_variables(body: str) -> List[Dict]:
    """Extract state variable declarations from component body."""
    results = []

    # Match decorator-decorated variable declarations
    # Pattern: optional multiple decorators, then variable declaration
    # Handle: @State @Watch('xxx') varName: Type = value
    lines = body.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        decorators_on_var = []

        # Collect decorators (may span multiple lines)
        while line.startswith('@') or (decorators_on_var and line.startswith('@')):
            dec_match = re.match(r'(@\w+(?:\([^)]*\))?)', line)
            if dec_match:
                decorators_on_var.append(dec_match.group(1))
                remaining = line[dec_match.end():].strip()
                if remaining:
                    line = remaining
                    break
                else:
                    i += 1
                    if i < len(lines):
                        line = lines[i].strip()
                    else:
                        break
            else:
                break

        if not decorators_on_var:
            i += 1
            continue

        # Now try to parse the variable declaration from the remaining line
        # Match: varName: Type (= value)?
        var_match = re.match(
            r'(?:public\s+|private\s+|protected\s+)?'
            r'(\w+)\s*:\s*([^=;\n]+?)'
            r'(?:\s*=\s*(.+?))?\s*[;\n]?$',
            line
        )

        if var_match:
            var_name = var_match.group(1)
            var_type = var_match.group(2).strip()
            var_value = var_match.group(3).strip() if var_match.group(3) else None

            # Determine primary decorator (first state-related one)
            primary_dec = None
            aux_decorators = []
            for d in decorators_on_var:
                norm = normalize_decorator(d)
                if norm in V1_DECORATORS or norm in V2_DECORATORS:
                    if primary_dec is None:
                        primary_dec = norm
                    else:
                        aux_decorators.append(norm)
                else:
                    aux_decorators.append(norm)

            if primary_dec:
                is_simple = is_simple_type(var_type)
                is_builtin = is_builtin_type(var_type)
                is_class = not is_simple and not is_builtin and var_type not in ('Function', 'object')

                # Extract key argument from primary decorator (e.g. @StorageLink('PropA'))
                decorator_arg = None
                for d in decorators_on_var:
                    norm = normalize_decorator(d)
                    if norm == primary_dec:
                        decorator_arg = extract_decorator_arg(d)
                        break

                results.append({
                    'name': var_name,
                    'decorator': primary_dec,
                    'decoratorArg': decorator_arg,
                    'auxDecorators': aux_decorators,
                    'type': var_type,
                    'isSimpleType': is_simple,
                    'isBuiltinType': is_builtin,
                    'isClassType': is_class,
                    'hasDefaultValue': var_value is not None,
                    'hasExternalInit': False,  # Will be updated by dependency tracer
                })

        i += 1

    return results


def is_simple_type(type_str: str) -> bool:
    """Check if a type string is a simple/primitive type."""
    type_str = type_str.strip().lower()
    base_types = {'number', 'string', 'boolean', 'bool', 'undefined', 'null',
                  'enum', 'void', 'object'}
    # Remove nullable markers
    type_str = type_str.replace('| undefined', '').replace('| null', '').strip()
    return type_str in base_types


def is_builtin_type(type_str: str) -> bool:
    """Check if type is a built-in collection type."""
    type_str = type_str.strip()
    for bt in BUILTIN_TYPES:
        if type_str.startswith(bt):
            return True
    return False


def extract_child_components(body: str, self_name: str) -> List[str]:
    """Extract component names used in the build() method."""
    components = set()

    # Find build() method body
    build_match = re.search(r'build\s*\(\s*\)\s*\{', body)
    if not build_match:
        # If no build method found, search the whole body
        search_area = body
    else:
        build_start = body.find('{', build_match.start())
        search_area = extract_brace_block(body, build_start) or body

    # Find PascalCase identifiers followed by ( which indicates component usage
    # Exclude common non-component identifiers
    exclude = {'Column', 'Row', 'Text', 'Button', 'Image', 'List', 'Grid', 'Stack',
               'Flex', 'Scroll', 'Tabs', 'TabContent', 'Navigation', 'NavDestination',
               'Divider', 'Blank', 'ForEach', 'LazyForEach', 'Repeat',
               'ListItem', 'GridItem', 'FlowItem', 'Swiper',
               'TextInput', 'TextArea', 'Toggle', 'Slider', 'Progress', 'Badge',
               'Rating', 'Select', 'Search', 'Video', 'Web', 'Canvas',
               'AlphabetIndexer', 'SideBarContainer', 'Panel', 'Refresh', 'WaterFlow',
               'RelativeContainer', 'Counter', 'DatePicker', 'TimePicker', 'TextPicker',
               'Radio', 'Checkbox', 'Marquee', 'QRCode', 'DataPanel', 'Gauge',
               'Hyperlink', 'ImageAnimator', 'PatternLock', 'RichText', 'Stepper',
               'StepperItem', 'Toolbar', 'SymbolSpan', 'Span', 'ContainerSpan',
               'FormComponent', 'PluginComponent', 'UIExtensionComponent',
               'Menu', 'MenuItem', 'MenuItemGroup', 'ContextMenu', 'BindContextMenu',
               'AlertDialog', 'ActionSheet', 'Toast',
               'If', 'Else', 'ElseIf', 'Array', 'Map', 'Set', 'String', 'Number',
               'Boolean', 'Object', 'Date', 'RegExp', 'Error', 'Promise', 'JSON',
               self_name}

    # Match PascalCase word followed by ({
    for m in re.finditer(r'\b([A-Z][a-zA-Z0-9]*)\s*\(', search_area):
        name = m.group(1)
        if name not in exclude and len(name) > 1:
            components.add(name)

    return sorted(components)


def extract_rendering_patterns(body: str) -> Dict:
    """Detect ForEach/LazyForEach/Repeat usage."""
    return {
        'hasForEach': bool(re.search(r'\bForEach\s*\(', body)),
        'hasLazyForEach': bool(re.search(r'\bLazyForEach\s*\(', body)),
        'hasRepeat': bool(re.search(r'\bRepeat\s*[\(<]', body)),
        'hasVirtualScroll': bool(re.search(r'\.virtualScroll\s*\(', body)),
    }


def extract_app_state_patterns(body: str) -> Dict:
    """Detect application-level state management usage."""
    return {
        'hasLocalStorage': bool(re.search(r'LocalStorage|localStorageLink|localStorageProp|@LocalStorageLink|@LocalStorageProp', body, re.IGNORECASE)),
        'hasAppStorage': bool(re.search(r'AppStorage|@StorageLink|@StorageProp|StorageLink|StorageProp', body, re.IGNORECASE)),
        'hasPersistentStorage': bool(re.search(r'PersistentStorage', body)),
        'hasEnvironment': bool(re.search(r'\bEnvironment\b', body)),
        'hasAnimateTo': bool(re.search(r'\banimateTo\s*\(', body)),
    }


# V1 static API classes with their key-bearing methods
_V1_STATIC_APIS = {
    'AppStorage': ['setOrCreate', 'set', 'get', 'link', 'setAndLink', 'prop',
                   'setAndProp', 'ref', 'setAndRef', 'has', 'delete',
                   'keys', 'clear', 'size'],
    'PersistentStorage': ['persistProp', 'deleteProp', 'keys'],
    'Environment': ['envProp', 'keys'],
}

# V2 static API classes with their methods
_V2_STATIC_APIS = {
    'AppStorageV2': ['connect', 'remove', 'keys'],
    'PersistenceV2': ['connect', 'globalConnect', 'save', 'notifyOnError'],
    'UIUtils': ['makeObserved', 'enableV2Compatibility', 'makeV1Observed',
                'applySync', 'flushUpdates', 'flushUIUpdates',
                'getTarget', 'getLifecycle', 'canBeObserved',
                'makeBinding', 'addMonitor', 'clearMonitor',
                'getCustomComponentContext'],
}

# LocalStorage instance methods (key-bearing)
_LS_INSTANCE_METHODS = ['setOrCreate', 'set', 'get', 'link', 'setAndLink', 'prop',
                         'setAndProp', 'ref', 'setAndRef', 'has', 'delete',
                         'keys', 'size', 'clear']

# Deprecated V1 PascalCase static APIs
_V1_DEPRECATED_STATIC_APIS = {
    'AppStorage': ['Link', 'SetAndLink', 'Prop', 'SetAndProp', 'Has', 'Get', 'Set',
                    'SetOrCreate', 'Delete', 'Keys', 'Clear', 'IsMutable', 'Size'],
    'PersistentStorage': ['PersistProp', 'DeleteProp', 'PersistProps', 'Keys'],
    'Environment': ['EnvProp', 'EnvProps', 'Keys'],
}


def _compute_line_number(content: str, pos: int) -> int:
    """Compute 1-based line number from character position."""
    return content[:pos].count('\n') + 1


def _extract_key_from_call(text: str) -> Optional[str]:
    """Extract the first string key argument from a method call fragment.
    E.g. setOrCreate('PropA', 47) -> 'PropA'
    Uses re.match to only match at the opening paren, avoiding false positives
    from subsequent calls in the remaining content.
    """
    m = re.match(r'\(\s*[\'"]([^\'"]+)[\'"]', text)
    return m.group(1) if m else None


def _extract_v2_key(text: str, method: str) -> Optional[str]:
    """Extract key from V2 API calls with more complex signatures.
    For AppStorageV2.connect(Type, 'key', ...) -> 'key' (second string arg)
    For PersistenceV2.globalConnect({key: 'key', ...}) -> 'key' (property in options)
    Falls back to first string arg via _extract_key_from_call.
    Uses re.match to avoid matching content beyond the current call.
    """
    key = _extract_key_from_call(text)
    if key:
        return key
    if method in ('connect',):
        m = re.match(r'\(\s*[^,]+,\s*[\'"]([^\'"]+)[\'"]', text)
        if m:
            return m.group(1)
    if method in ('globalConnect',):
        # Key is inside an options object, search within a bounded window
        m = re.search(r'key\s*:\s*[\'"]([^\'"]+)[\'"]', text[:300])
        if m:
            return m.group(1)
    return None


def extract_state_api_calls(content: str, filepath: str) -> List[Dict]:
    """Scan file for all state management API calls (V1 and V2).
    Returns a list of call records with class, method, key, line, etc."""
    calls = []

    # --- V1 static API calls: AppStorage.xxx('key', ...), PersistentStorage.xxx('key', ...) ---
    for cls_name, methods in _V1_STATIC_APIS.items():
        for method in methods:
            pattern = re.compile(
                rf'\b{re.escape(cls_name)}\s*\.\s*{re.escape(method)}\s*\(',
            )
            for m in pattern.finditer(content):
                # Extract the key from the opening parenthesis onwards
                rest = content[m.end() - 1:]  # includes the '('
                key = _extract_key_from_call(rest)
                line = _compute_line_number(content, m.start())
                # Get the raw call text (up to closing paren or end of line)
                raw_match = re.search(
                    rf'\b{re.escape(cls_name)}\s*\.\s*{re.escape(method)}\s*\([^)]*\)',
                    content[m.start():],
                )
                raw = raw_match.group(0) if raw_match else m.group(0)
                calls.append({
                    'class': cls_name,
                    'method': method,
                    'key': key,
                    'line': line,
                    'raw': raw,
                    'version': 'V1',
                    'file': filepath,
                })

    # --- V2 static API calls: AppStorageV2.connect(...), PersistenceV2.xxx(...), UIUtils.xxx(...) ---
    for cls_name, methods in _V2_STATIC_APIS.items():
        for method in methods:
            pattern = re.compile(
                rf'\b{re.escape(cls_name)}\s*\.\s*{re.escape(method)}\s*\(',
            )
            for m in pattern.finditer(content):
                rest = content[m.end() - 1:]
                key = _extract_v2_key(rest, method)
                line = _compute_line_number(content, m.start())
                raw_match = re.search(
                    rf'\b{re.escape(cls_name)}\s*\.\s*{re.escape(method)}\s*\([^)]*\)',
                    content[m.start():],
                )
                raw = raw_match.group(0) if raw_match else m.group(0)
                calls.append({
                    'class': cls_name,
                    'method': method,
                    'key': key,
                    'line': line,
                    'raw': raw,
                    'version': 'V2',
                    'file': filepath,
                })

    # --- LocalStorage instance method calls: xxx.setOrCreate('key', ...) ---
    # Match any identifier followed by a LocalStorage instance method
    for method in _LS_INSTANCE_METHODS:
        pattern = re.compile(
            rf'\b(\w+)\s*\.\s*{re.escape(method)}\s*\(',
        )
        for m in pattern.finditer(content):
            var_name = m.group(1)
            # Skip if the variable is actually a static API class name
            if var_name in _V1_STATIC_APIS or var_name in _V2_STATIC_APIS:
                continue
            rest = content[m.end() - 1:]
            key = _extract_key_from_call(rest)
            line = _compute_line_number(content, m.start())
            raw_match = re.search(
                rf'\b{re.escape(var_name)}\s*\.\s*{re.escape(method)}\s*\([^)]*\)',
                content[m.start():],
            )
            raw = raw_match.group(0) if raw_match else m.group(0)
            calls.append({
                'class': f'LocalStorage instance ({var_name})',
                'method': method,
                'key': key,
                'line': line,
                'raw': raw,
                'version': 'V1',
                'file': filepath,
            })

    # --- LocalStorage constructor: new LocalStorage({...}) or new LocalStorage() ---
    for m in re.finditer(r'\bnew\s+LocalStorage\s*\(', content):
        line = _compute_line_number(content, m.start())
        calls.append({
            'class': 'LocalStorage',
            'method': 'constructor',
            'key': None,
            'line': line,
            'raw': m.group(0).rstrip('(') + '(...)',
            'version': 'V1',
            'file': filepath,
        })

    # --- LocalStorage.getShared() ---
    for m in re.finditer(r'\bLocalStorage\s*\.\s*getShared\s*\(', content):
        line = _compute_line_number(content, m.start())
        calls.append({
            'class': 'LocalStorage',
            'method': 'getShared',
            'key': None,
            'line': line,
            'raw': 'LocalStorage.getShared()',
            'version': 'V1',
            'file': filepath,
        })

    # --- PersistentStorage.persistProps([...]) ---
    for m in re.finditer(r'\bPersistentStorage\s*\.\s*persistProps\s*\(', content):
        line = _compute_line_number(content, m.start())
        # Try to extract keys from the array argument
        rest = content[m.end() - 1:m.end() + 500]
        keys = re.findall(r"key\s*:\s*['\"]([^'\"]+)['\"]", rest)
        calls.append({
            'class': 'PersistentStorage',
            'method': 'persistProps',
            'key': keys if keys else None,
            'line': line,
            'raw': 'PersistentStorage.persistProps(...)',
            'version': 'V1',
            'file': filepath,
        })

    # --- Environment.envProps([...]) ---
    for m in re.finditer(r'\bEnvironment\s*\.\s*envProps\s*\(', content):
        line = _compute_line_number(content, m.start())
        rest = content[m.end() - 1:m.end() + 500]
        keys = re.findall(r"key\s*:\s*['\"]([^'\"]+)['\"]", rest)
        calls.append({
            'class': 'Environment',
            'method': 'envProps',
            'key': keys if keys else None,
            'line': line,
            'raw': 'Environment.envProps(...)',
            'version': 'V1',
            'file': filepath,
        })

    # --- Deprecated V1 PascalCase static API calls ---
    for cls_name, methods in _V1_DEPRECATED_STATIC_APIS.items():
        for method in methods:
            pattern = re.compile(
                rf'\b{re.escape(cls_name)}\s*\.\s*{re.escape(method)}\s*\(',
            )
            for m in pattern.finditer(content):
                rest = content[m.end() - 1:]
                key = _extract_key_from_call(rest)
                line = _compute_line_number(content, m.start())
                raw_match = re.search(
                    rf'\b{re.escape(cls_name)}\s*\.\s*{re.escape(method)}\s*\([^)]*\)',
                    content[m.start():],
                )
                raw = raw_match.group(0) if raw_match else m.group(0)
                calls.append({
                    'class': cls_name,
                    'method': method,
                    'key': key,
                    'line': line,
                    'raw': raw,
                    'version': 'V1',
                    'deprecated': True,
                    'file': filepath,
                })

    # --- Deprecated LocalStorage.GetShared() ---
    for m in re.finditer(r'\bLocalStorage\s*\.\s*GetShared\s*\(', content):
        line = _compute_line_number(content, m.start())
        calls.append({
            'class': 'LocalStorage',
            'method': 'GetShared',
            'key': None,
            'line': line,
            'raw': 'LocalStorage.GetShared()',
            'version': 'V1',
            'deprecated': True,
            'file': filepath,
        })

    return calls


def trace_storage_keys(results: List[Dict]) -> None:
    """Cross-reference Storage decorator keys with API call sites across all files.
    For each component variable decorated with @StorageLink/@StorageProp/@LocalStorageLink/@LocalStorageProp,
    finds all state management API calls that reference the same key.
    Modifies component dicts in-place, adding 'storageKeyTraces' field.
    Also tags each trace entry with fileType ('ts' or 'ets') for migration planning."""
    # Build a map: key -> list of API call sites using that key
    key_to_calls: Dict[str, List[Dict]] = {}
    for result in results:
        if 'error' in result:
            continue
        for call in result.get('stateApiCalls', []):
            keys = call.get('key')
            if keys is None:
                continue
            entry = {
                'class': call['class'],
                'method': call['method'],
                'key': keys if isinstance(keys, str) else None,
                'line': call['line'],
                'raw': call['raw'],
                'file': call['file'],
                'fileType': _get_file_type(call['file']),
                'version': call.get('version', 'V1'),
                'deprecated': call.get('deprecated', False),
            }
            if isinstance(keys, list):
                for k in keys:
                    key_to_calls.setdefault(k, []).append({**entry, 'key': k})
            else:
                key_to_calls.setdefault(keys, []).append(entry)

    # For each component with Storage decorators, look up the key
    for result in results:
        if 'error' in result:
            continue
        filepath = result.get('file', '')
        for comp in result.get('components', []):
            traces = []
            for sv in comp.get('stateVariables', []):
                if (sv['decorator'] in _STORAGE_KEY_DECORATORS
                        and sv.get('decoratorArg')):
                    key = sv['decoratorArg']
                    matching_calls = key_to_calls.get(key, [])
                    traces.append({
                        'variable': sv['name'],
                        'decorator': sv['decorator'],
                        'key': key,
                        'decoratorFile': filepath,
                        'decoratorFileType': _get_file_type(filepath),
                        'apiCalls': matching_calls,
                    })
            if traces:
                comp['storageKeyTraces'] = traces


def build_state_api_key_map(results: List[Dict]) -> Dict:
    """Build a structured map of all state management API usage grouped by key.

    For each Storage key found (via decorator arguments or API calls), this collects:
    - decoratorUsage: which components use the key via @StorageLink/@StorageProp/etc.
      These are always V1 components (V2 uses connect() instead of decorators).
    - apiCalls: all API call sites that reference the key, tagged with fileType and version
    - v1CallsSafeToRemove: True when decoratorUsage is empty (no V1 component still
      references this key via Storage decorators), meaning V1 API calls can be removed
    - removableV1Calls: list of V1 API calls that can be safely removed
      (only populated when v1CallsSafeToRemove is True)

    Migration decision rule:
    - decoratorUsage non-empty → V1 components still need this key → only ADD V2 API, keep V1
    - decoratorUsage empty → all components migrated → V1 API calls can be removed

    Returns: dict mapping key -> { decoratorUsage, apiCalls, v1CallsSafeToRemove, removableV1Calls }
    """
    key_map: Dict[str, Dict] = {}

    for result in results:
        if 'error' in result:
            continue
        filepath = result.get('file', '')
        file_type = _get_file_type(filepath)

        # Collect API call sites grouped by key
        for call in result.get('stateApiCalls', []):
            keys = call.get('key')
            if keys is None:
                continue
            keys_list = keys if isinstance(keys, list) else [keys]
            for k in keys_list:
                if k not in key_map:
                    key_map[k] = {'decoratorUsage': [], 'apiCalls': []}
                key_map[k]['apiCalls'].append({
                    'class': call['class'],
                    'method': call['method'],
                    'file': filepath,
                    'fileType': file_type,
                    'line': call['line'],
                    'raw': call['raw'],
                    'version': call.get('version', 'V1'),
                    'deprecated': call.get('deprecated', False),
                })

        # Collect decorator usage grouped by key (only V1 Storage decorators)
        for comp in result.get('components', []):
            for sv in comp.get('stateVariables', []):
                if sv['decorator'] in _STORAGE_KEY_DECORATORS and sv.get('decoratorArg'):
                    key = sv['decoratorArg']
                    if key not in key_map:
                        key_map[key] = {'decoratorUsage': [], 'apiCalls': []}
                    key_map[key]['decoratorUsage'].append({
                        'component': comp['name'],
                        'variable': sv['name'],
                        'decorator': sv['decorator'],
                        'file': filepath,
                        'fileType': file_type,
                    })

    # Determine which keys have V1 API calls safe to remove
    for key, data in key_map.items():
        v1_decorators_remaining = len(data['decoratorUsage']) > 0
        v1_api_calls = [c for c in data['apiCalls'] if c.get('version') != 'V2']
        safe = not v1_decorators_remaining and len(v1_api_calls) > 0
        data['v1CallsSafeToRemove'] = safe
        data['removableV1Calls'] = v1_api_calls if safe else []

    return key_map


def extract_classes(content: str, filepath: str) -> List[Dict]:
    """Extract observed class definitions with their decorators and tracked properties.

    Only classes carrying a class-level observation decorator (``@Observed`` /
    ``@ObservedV2``) are returned. Decorators are captured as the group
    immediately adjacent to ``class`` (only whitespace, or the ``export`` /
    ``abstract`` / ``default`` keywords, may sit between) — no arbitrary
    lookback — so decorators inside comments or belonging to an earlier class
    are never picked up. Callers should pass comment-stripped content.
    """
    classes = []

    # A run of @decorators immediately before `class` (optionally with
    # export/abstract/default keywords between the decorators and `class`).
    pattern = r'((?:@\w+(?:\([^)]*\))?\s*)+)(?:(?:export|abstract|default)\s+)*class\s+(\w+)'
    for m in re.finditer(pattern, content):
        dec_group = m.group(1)
        class_name = m.group(2)

        class_decorators = [normalize_decorator(d)
                            for d in re.findall(r'@\w+(?:\([^)]*\))?', dec_group)]
        observed_decs = [d for d in class_decorators if d in CLASS_DECORATORS]
        if not observed_decs:
            # Decorated class without an observation decorator (e.g. @Reusable only)
            continue

        # Find class body
        brace_start = content.find('{', m.end() - 1)
        body = extract_brace_block(content, brace_start) if brace_start != -1 else None

        properties = []
        if body:
            for prop_m in re.finditer(
                r'(@\w+(?:\([^)]*\))?\s+)*(?:public\s+|private\s+)?(\w+)\s*:\s*([^=;\n]+)',
                body
            ):
                prop_decorators = re.findall(r'(@\w+(?:\([^)]*\))?)', prop_m.group(0))
                prop_decorators = [normalize_decorator(d) for d in prop_decorators]
                prop_name = prop_m.group(2)
                prop_type = prop_m.group(3).strip()
                has_trace = '@Trace' in prop_decorators or '@Track' in prop_decorators
                properties.append({
                    'name': prop_name,
                    'type': prop_type,
                    'decorators': prop_decorators,
                    'hasTrace': has_trace,
                })

        classes.append({
            'name': class_name,
            'file': filepath,
            'observationDecorator': observed_decs[0],
            'classDecorators': class_decorators,
            'observedDecorators': observed_decs,
            'properties': properties,
        })

    return classes


def analyze_file(filepath: str) -> Dict:
    """Analyze a single .ets or .ts file."""
    content = read_file(filepath)
    if content is None:
        return {'file': filepath, 'error': 'Could not read file'}

    # Strip comments once, length/newline-preserving, so every downstream
    # extractor sees real code only (no commented-out components/classes/API
    # calls) while line numbers stay aligned with the original file.
    stripped = strip_comments(content)
    components = extract_components(stripped, filepath)
    classes = extract_classes(stripped, filepath)
    state_api_calls = extract_state_api_calls(stripped, filepath)

    return {
        'file': filepath,
        'fileType': _get_file_type(filepath),
        'components': components,
        'classes': classes,
        'stateApiCalls': state_api_calls,
    }


def analyze_directory(dirpath: str, recursive: bool = True) -> List[Dict]:
    """Analyze all .ets and .ts files in a directory."""
    results = []
    patterns = ['**/*.ets', '**/*.ts'] if recursive else ['*.ets', '*.ts']
    seen = set()
    for pattern in patterns:
        for f in Path(dirpath).glob(pattern):
            # Skip declaration files and avoid duplicates
            if f.name.endswith('.d.ts') or str(f) in seen:
                continue
            seen.add(str(f))
            results.append(analyze_file(str(f)))
    trace_storage_keys(results)
    return results


def scan_v1_components(project_dir: str) -> Dict:
    """Scan project for V1 components only, returning a structured result
    that includes explicit instructions for the caller to ask the user.
    Also builds a key-based map of all state management API usage for migration planning."""
    results = analyze_directory(project_dir, recursive=True)

    # Collect all state API calls across files for reference
    all_api_calls = []
    for result in results:
        if 'error' in result:
            continue
        all_api_calls.extend(result.get('stateApiCalls', []))

    # Build structured key map for Storage-related API analysis
    state_api_by_key = build_state_api_key_map(results)

    v1_components = []
    for result in results:
        if 'error' in result:
            continue
        for comp in result.get('components', []):
            if comp['version'] == 'V1':
                entry = {
                    'name': comp['name'],
                    'file': result['file'],
                    'isEntry': comp['isEntry'],
                    'stateVariables': [
                        f"{sv['decorator']} {sv['name']}: {sv['type']}"
                        for sv in comp.get('stateVariables', [])
                    ],
                }
                # Include storage key traces if present
                if comp.get('storageKeyTraces'):
                    entry['storageKeyTraces'] = comp['storageKeyTraces']
                v1_components.append(entry)

    return {
        'projectDir': project_dir,
        'totalV1Components': len(v1_components),
        'v1Components': v1_components,
        'stateApiCalls': all_api_calls,
        'stateApiByKey': state_api_by_key,
        'instruction': (
            '请先向用户确认要迁移以上哪个组件，不得跳过此步骤。'
            '将上述 V1 组件列表展示给用户，等待用户指定组件名后再进入第一步分析。'
            '如果列表为空，告知用户该工程中没有 V1 组件，无需迁移。'
        ),
    }


def main():
    parser = argparse.ArgumentParser(description='Analyze .ets components for V1->V2 migration')
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--recursive', action='store_true', default=True, help='Search directories recursively')
    parser.add_argument('--scan-v1', action='store_true',
                        help='Scan mode: list V1 components and output instruction to ask user')
    args = parser.parse_args()

    path = args.path

    # --scan-v1 mode: list V1 components and instruct caller to ask user
    if args.scan_v1:
        if not os.path.isdir(path):
            print(f"Error: {path} is not a valid directory for --scan-v1", file=sys.stderr)
            sys.exit(1)
        result = scan_v1_components(path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if os.path.isfile(path):
        results = [analyze_file(path)]
        trace_storage_keys(results)
    elif os.path.isdir(path):
        results = analyze_directory(path, args.recursive)
    else:
        print(f"Error: {path} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            if 'error' in result:
                print(f"\n[ERROR] {result['file']}: {result['error']}")
                continue

            print(f"\n{'='*60}")
            print(f"File: {result['file']}")
            print(f"{'='*60}")

            for cls in result.get('classes', []):
                print(f"\n  Class: {cls['name']} ({cls['observationDecorator']})")
                for prop in cls['properties']:
                    trace = ' [TRACKED]' if prop['hasTrace'] else ''
                    print(f"    - {prop['name']}: {prop['type']}{trace}")

            for comp in result.get('components', []):
                print(f"\n  Component: {comp['name']} ({comp['version']})")
                if comp['isEntry']:
                    print(f"    [Entry Component]")
                if comp['isReusable']:
                    print(f"    [Reusable]")
                print(f"    Has Input: {comp['hasInput']}")
                print(f"    Has Output: {comp['hasOutput']}")

                if comp['stateVariables']:
                    print(f"    State Variables:")
                    for sv in comp['stateVariables']:
                        aux = f" +{','.join(sv['auxDecorators'])}" if sv['auxDecorators'] else ''
                        print(f"      {sv['decorator']}{aux} {sv['name']}: {sv['type']}"
                              f"{' (class)' if sv['isClassType'] else ''}"
                              f"{' (builtin)' if sv['isBuiltinType'] else ''}")

                if comp['usedComponents']:
                    print(f"    Child Components: {', '.join(comp['usedComponents'])}")

                render = comp['rendering']
                render_items = []
                if render['hasForEach']: render_items.append('ForEach')
                if render['hasLazyForEach']: render_items.append('LazyForEach')
                if render['hasRepeat']: render_items.append('Repeat')
                if render_items:
                    print(f"    Rendering: {', '.join(render_items)}")

                app = comp['appState']
                app_items = []
                if app['hasLocalStorage']: app_items.append('LocalStorage')
                if app['hasAppStorage']: app_items.append('AppStorage')
                if app['hasPersistentStorage']: app_items.append('PersistentStorage')
                if app['hasEnvironment']: app_items.append('Environment')
                if app['hasAnimateTo']: app_items.append('animateTo')
                if app_items:
                    print(f"    App State: {', '.join(app_items)}")

                # Display storage key traces
                if comp.get('storageKeyTraces'):
                    print(f"    Storage Key Traces:")
                    for trace in comp['storageKeyTraces']:
                        dec_ft = trace.get('decoratorFileType', '')
                        dec_ft_tag = f" [{dec_ft}]" if dec_ft else ''
                        print(f"      {trace['decorator']}({trace['key']}) -> {trace['variable']}{dec_ft_tag}")
                        for api_call in trace['apiCalls']:
                            dep_marker = ' [deprecated]' if api_call.get('deprecated') else ''
                            ft_tag = f" [{api_call.get('fileType', '')}]" if api_call.get('fileType') else ''
                            print(f"        <- {api_call['class']}.{api_call['method']}()"
                                  f" at {api_call['file']}:{api_call['line']}{ft_tag}{dep_marker}")

            # Display state API calls found in this file
            state_calls = result.get('stateApiCalls', [])
            if state_calls:
                file_type = result.get('fileType', _get_file_type(result['file']))
                print(f"\n  State API Calls [{file_type}]:")
                for call in state_calls:
                    dep_marker = ' [deprecated]' if call.get('deprecated') else ''
                    ver_marker = f" [{call.get('version', 'V1')}]" if call.get('version') == 'V2' else ''
                    key_str = f" key='{call['key']}'" if call.get('key') else ''
                    print(f"    {call['class']}.{call['method']}({key_str})"
                          f" line {call['line']}{ver_marker}{dep_marker}")


if __name__ == '__main__':
    main()
