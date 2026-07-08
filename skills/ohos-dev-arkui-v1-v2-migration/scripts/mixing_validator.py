#!/usr/bin/env python3
"""
V1->V2 Migration - Mixing Validator
Validates V1/V2 component mixing rules across a project.
Uses component_analyzer for component data, api_version_checker for API version.

Checks:
1. Cross-component data passing (type restrictions based on API version)
2. Bridge pattern detection (when @Observed class must cross V1->V2 boundary)
3. V2->V1 receiving restrictions
4. @Link initialization rule (only V1 state variables)
5. Within-component V1/V2 decorator mixing (e.g. @State inside @ComponentV2,
   or @Local inside @Component)
6. Class-level @Observed/@ObservedV2 coexistence on the same class

Usage:
    python3 mixing_validator.py <project_dir> [--json] [--target COMPONENT_NAME]
"""

import os
import re
import sys
import json
import argparse
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from component_analyzer import (
    analyze_file, analyze_directory, read_file, extract_components,
    normalize_decorator, V1_DECORATORS, V2_DECORATORS, BUILTIN_TYPES,
    strip_comments,
)
from api_version_checker import detect_api_version


# Decorators that CAN coexist with others on the same variable
AUX_DECORATORS = {'@Watch', '@Once', '@Require', '@Monitor'}
# V1 decorators that can receive data from V2 components (API < 19)
V1_RECEIVE_DECORATORS = {'@State', '@Prop', '@Provide'}
# V2 decorators that can receive data from V1 components
V2_RECEIVE_DECORATORS = {'@Param'}
# Simple types that can always cross V1/V2 boundary
SIMPLE_TYPES = {'boolean', 'number', 'string', 'null', 'undefined', 'bool', 'enum'}
# Built-in collection types that are restricted
BUILTIN_TYPES_SET = {'Array', 'Map', 'Set', 'Date'}


def validate_project(project_dir: str, target_component: Optional[str] = None) -> Dict:
    """Run all mixing validations on a project."""
    api_info = detect_api_version(project_dir)
    api_level = api_info['apiLevel']
    mixing_rules = api_info['mixingRules']

    # Analyze all .ets files
    analysis = analyze_directory(project_dir, recursive=True)

    all_components = []
    all_classes = []
    file_map = {}

    for result in analysis:
        if 'error' in result:
            continue
        filepath = result['file']
        file_map[filepath] = result
        for comp in result.get('components', []):
            comp['file'] = filepath
            all_components.append(comp)
        for cls in result.get('classes', []):
            cls['file'] = filepath
            all_classes.append(cls)

    # Build component name -> [components] lookup. Multi-valued on purpose so
    # same-named components in different files are all kept; child resolution
    # picks the right one via _resolve_child instead of silently overwriting.
    comps_by_name = defaultdict(list)
    for comp in all_components:
        comps_by_name[comp['name']].append(comp)

    # Run validations
    violations = []
    warnings = []
    suggestions = []

    # 1. Cross-component data passing
    _check_cross_component_passing(
        all_components, comps_by_name, file_map,
        api_level, violations, warnings, suggestions
    )

    # 2. Check bridge pattern need
    _check_bridge_pattern_need(
        all_components, comps_by_name, file_map,
        api_level, suggestions
    )

    # 3. Multiple decorators on same variable
    _check_multiple_decorators(all_components, violations)

    # 4. Within-component V1/V2 decorator mixing (e.g. @State in @ComponentV2)
    _check_within_component_mixing(all_components, violations)

    # 5. Class-level @Observed/@ObservedV2 coexistence on the same class
    _check_class_decorator_coexistence(all_classes, violations)

    # Filter by target if specified
    if target_component:
        violations = _filter_by_component(violations, target_component)
        warnings = _filter_by_component(warnings, target_component)
        suggestions = _filter_by_component(suggestions, target_component)

    # Build component interaction map
    interactions = _build_interaction_map(all_components, comps_by_name)

    return {
        'projectDir': project_dir,
        'apiVersion': api_info,
        'totalComponents': len(all_components),
        'v1Components': [c['name'] for c in all_components if c['version'] == 'V1'],
        'v2Components': [c['name'] for c in all_components if c['version'] == 'V2'],
        'violations': violations,
        'warnings': warnings,
        'suggestions': suggestions,
        'summary': {
            'violationCount': len(violations),
            'warningCount': len(warnings),
            'suggestionCount': len(suggestions),
            'isCompliant': len(violations) == 0,
        },
        'interactions': interactions,
    }


def _resolve_child(
    comps_by_name: Dict[str, List[Dict]],
    parent_file: str,
    child_name: str,
) -> Tuple[Optional[Dict], List[Dict]]:
    """Resolve a child component name to a single component record.

    Same-named components in different files are all kept in ``comps_by_name``
    (multi-valued). Resolution prefers a component defined in the same file as
    the parent — the common ArkUI case where a Page and its private child live
    in one file — which avoids cross-file collisions silently picking the wrong
    version.

    Returns ``(child_or_None, ambiguous_candidates)``:
    * ``child_or_None`` — the resolved component, or None if the name is unknown.
    * ``ambiguous_candidates`` — the full candidate list whenever the name is
      defined more than once in the project; empty only when the name is
      globally unique. Callers should emit an ``AMBIGUOUS_COMPONENT_NAME``
      warning when this is non-empty, because without import analysis the
      same-file pick is a guess.
    """
    cands = comps_by_name.get(child_name, [])
    if not cands:
        return None, []
    if len(cands) == 1:
        return cands[0], []
    # Multiple definitions exist. Prefer the same-file one as a best guess, but
    # flag it: the parent might actually mean an imported cross-file component.
    same_file = [c for c in cands if c.get('file') == parent_file]
    chosen = same_file[-1] if same_file else cands[0]
    return chosen, cands


def _ambiguous_warning(child_name: str, candidates: List[Dict]) -> Dict:
    """Build an AMBIGUOUS_COMPONENT_NAME warning for a same-named collision."""
    files = [c.get('file', '?') for c in candidates]
    return {
        'type': 'AMBIGUOUS_COMPONENT_NAME',
        'severity': 'warning',
        'component': child_name,
        'file': files[0] if files else '',
        'message': (
            f"组件名 '{child_name}' 在多个文件中定义：{files}。"
            f"已按同文件优先解析，但存在同名歧义，请人工确认实际依赖关系。"
        ),
    }


def _check_cross_component_passing(
    components: List[Dict],
    comps_by_name: Dict[str, List[Dict]],
    file_map: Dict[str, Dict],
    api_level: str,
    violations: List[Dict],
    warnings: List[Dict],
    suggestions: List[Dict],
):
    """Validate data passing between V1 and V2 components."""
    for comp in components:
        parent_version = comp['version']
        parent_name = comp['name']
        parent_file = comp.get('file', '')

        for child_name in comp.get('usedComponents', []):
            child_comp, ambiguous = _resolve_child(comps_by_name, parent_file, child_name)
            if ambiguous:
                warnings.append(_ambiguous_warning(child_name, ambiguous))
            if child_comp is None:
                continue

            child_version = child_comp['version']

            # Skip if same version
            if parent_version == child_version:
                continue

            # Analyze actual parameter passing (on comment-stripped text so
            # commented-out child calls are not treated as real data passing)
            parent_content = read_file(parent_file)
            if not parent_content:
                continue
            parent_content = strip_comments(parent_content)

            passages = _extract_passages(parent_content, child_name)

            if not passages:
                # No data passing - OK in both directions
                continue

            is_v1_to_v2 = (parent_version == 'V1' and child_version == 'V2')
            is_v2_to_v1 = (parent_version == 'V2' and child_version == 'V1')

            for passage in passages:
                param_name = passage['param']
                value_expr = passage['value']
                passage_type = passage['type']

                # Determine the state variable being passed
                sv = _find_state_var(parent_name, value_expr, comp)

                if is_v1_to_v2:
                    _validate_v1_to_v2(
                        parent_name, child_name, child_comp, sv, passage,
                        api_level, violations, warnings, suggestions
                    )
                elif is_v2_to_v1:
                    _validate_v2_to_v1(
                        parent_name, child_name, child_comp, sv, passage,
                        api_level, violations, warnings, suggestions
                    )


def _extract_passages(content: str, child_name: str) -> List[Dict]:
    """Extract parameter passages from parent to child component."""
    passages = []
    pattern = re.compile(
        rf'\b{re.escape(child_name)}\s*\(\s*\{{([^}}]*)\}}',
        re.DOTALL
    )

    for m in pattern.finditer(content):
        args_text = m.group(1)
        for arg_match in re.finditer(r'(\w+)\s*:\s*([^,}\n]+)', args_text):
            param_name = arg_match.group(1)
            value_expr = arg_match.group(2).strip()
            passages.append({
                'param': param_name,
                'value': value_expr,
                'type': _classify_value(value_expr),
            })

    return passages


def _classify_value(value_expr: str) -> str:
    """Classify the type of a value expression."""
    value_expr = value_expr.strip()
    if value_expr.startswith('$$') or '!!' in value_expr:
        return 'two_way_binding'
    if re.match(r'this\.\w+$', value_expr):
        return 'state_variable_ref'
    if 'new ' in value_expr:
        return 'new_instance'
    if value_expr.startswith('(') or '=>' in value_expr:
        return 'callback'
    if re.match(r'^(\d+|true|false|null|undefined|\'[^\']*\'|"[^"]*")$', value_expr):
        return 'literal'
    if '(' in value_expr and ')' in value_expr:
        return 'function_call'
    return 'expression'


def _find_state_var(parent_name: str, value_expr: str, parent_comp: Dict) -> Optional[Dict]:
    """Find the state variable in parent that matches the value expression."""
    # Extract variable name from this.xxx
    m = re.match(r'this\.(\w+)', value_expr.strip())
    if not m:
        return None
    var_name = m.group(1)

    for sv in parent_comp.get('stateVariables', []):
        if sv['name'] == var_name:
            return sv
    return None


def _validate_v1_to_v2(
    parent_name: str, child_name: str, child_comp: Dict,
    sv: Optional[Dict], passage: Dict,
    api_level: str, violations: List, warnings: List, suggestions: List,
):
    """Validate V1 -> V2 data passing rules."""
    passage_type = passage['type']
    param_name = passage['param']

    # Find the receiving param in child
    child_sv = _find_child_param(child_comp, param_name)

    if api_level == 'pre19':
        # API < 19: Strict rules
        if passage_type == 'state_variable_ref' and sv:
            var_type = sv['type']
            is_simple = _is_simple_or_enum(var_type)
            is_builtin = _is_builtin_type(var_type)
            is_class = sv.get('isClassType', False)

            if is_class and not is_builtin:
                violations.append({
                    'type': 'V1_TO_V2_COMPLEX_TYPE',
                    'severity': 'error',
                    'component': f'{parent_name} -> {child_name}',
                    'file': child_comp.get('file', ''),
                    'message': (f"Cannot pass @Observed class '{sv['name']}: {var_type}' "
                                f"from V1 component '{parent_name}' to V2 component '{child_name}'. "
                                f"API < 19 requires bridge pattern for complex types."),
                    'bridgePatternNeeded': True,
                })

            elif is_builtin:
                violations.append({
                    'type': 'V1_TO_V2_BUILTIN_TYPE',
                    'severity': 'error',
                    'component': f'{parent_name} -> {child_name}',
                    'file': child_comp.get('file', ''),
                    'message': (f"Cannot pass built-in type '{sv['name']}: {var_type}' "
                                f"from V1 to V2. API < 19 does not support "
                                f"Array/Map/Set/Date across V1/V2 boundary."),
                })

            elif not is_simple:
                warnings.append({
                    'type': 'V1_TO_V2_UNKNOWN_TYPE',
                    'severity': 'warning',
                    'component': f'{parent_name} -> {child_name}',
                    'file': child_comp.get('file', ''),
                    'message': (f"Type '{var_type}' passed from V1 to V2 may not be compatible. "
                                f"Verify manually: only simple types (boolean, number, string, "
                                f"null, undefined) can cross V1/V2 boundary at API < 19."),
                })

            # Check V2 receiving decorator
            if child_sv and child_sv['decorator'] not in V2_RECEIVE_DECORATORS:
                violations.append({
                    'type': 'V2_INVALID_RECEIVE_DECORATOR',
                    'severity': 'error',
                    'component': child_name,
                    'file': child_comp.get('file', ''),
                    'message': (f"V2 component '{child_name}' receives '{param_name}' with "
                                f"@{child_sv['decorator'][1:]}. V2 must use @Param to receive "
                                f"data from V1 components."),
                })

    else:
        # API >= 19: Relaxed rules with enableV2Compatibility
        if passage_type == 'state_variable_ref' and sv:
            var_type = sv['type']
            is_simple = _is_simple_or_enum(var_type)
            is_builtin = _is_builtin_type(var_type)
            is_class = sv.get('isClassType', False)

            if is_class and not is_simple:
                suggestions.append({
                    'type': 'V1_TO_V2_NEED_ENABLE_V2_COMPAT',
                    'severity': 'info',
                    'component': f'{parent_name} -> {child_name}',
                    'file': child_comp.get('file', ''),
                    'message': (f"Passing '{sv['name']}: {var_type}' from V1 to V2. "
                                f"Use UIUtils.enableV2Compatibility() at V2 component "
                                f"construction: {child_name}({{ {param_name}: "
                                f"UIUtils.enableV2Compatibility(this.{sv['name']}) }})"),
                })

            if is_builtin:
                suggestions.append({
                    'type': 'V1_TO_V2_BUILTIN_USE_MAKE_V1_OBSERVED',
                    'severity': 'info',
                    'component': f'{parent_name} -> {child_name}',
                    'file': child_comp.get('file', ''),
                    'message': (f"Built-in type '{var_type}' passed from V1 to V2. "
                                f"Use UIUtils.enableV2Compatibility("
                                f"UIUtils.makeV1Observed(...)) to avoid dual-proxy issues."),
                })

    # Two-way binding check (all API levels)
    if passage_type == 'two_way_binding' and sv:
        violations.append({
            'type': 'V1_TO_V2_TWO_WAY_BINDING',
            'severity': 'error',
            'component': f'{parent_name} -> {child_name}',
            'file': child_comp.get('file', ''),
            'message': (f"Two-way binding ($$ or !!) on '{sv['name']}' "
                        f"from V1 '{parent_name}' to V2 '{child_name}' is not supported. "
                        f"Use @Param + @Event pattern instead."),
        })


def _validate_v2_to_v1(
    parent_name: str, child_name: str, child_comp: Dict,
    sv: Optional[Dict], passage: Dict,
    api_level: str, violations: List, warnings: List, suggestions: List,
):
    """Validate V2 -> V1 data passing rules."""
    passage_type = passage['type']
    param_name = passage['param']

    # Find the receiving param in V1 child
    child_sv = _find_child_param(child_comp, param_name)

    if child_sv is None:
        return

    receive_dec = child_sv['decorator']

    # @Link can only be initialized by V1 state variables (all API levels)
    if receive_dec == '@Link':
        violations.append({
            'type': 'V2_TO_V1_LINK_INIT',
            'severity': 'error',
            'component': f'{parent_name} -> {child_name}',
            'file': child_comp.get('file', ''),
            'message': (f"V1 '@Link' in '{child_name}' cannot be initialized from "
                        f"V2 component '{parent_name}'. @Link must be initialized "
                        f"by V1 state variables only."),
        })

    # V1 receiving decorator restriction (API < 19)
    if api_level == 'pre19':
        if receive_dec not in V1_RECEIVE_DECORATORS and receive_dec not in AUX_DECORATORS:
            if receive_dec in ('@ObjectLink', '@StorageLink', '@StorageProp',
                               '@LocalStorageLink', '@LocalStorageProp'):
                violations.append({
                    'type': 'V2_TO_V1_INVALID_RECEIVE_DECORATOR',
                    'severity': 'error',
                    'component': f'{parent_name} -> {child_name}',
                    'file': child_comp.get('file', ''),
                    'message': (f"V1 component '{child_name}' uses '@{receive_dec[1:]}' "
                                f"to receive from V2 '{parent_name}'. "
                                f"V1 can only receive from V2 via "
                                f"@State, @Prop, or @Provide."),
                })

    # Built-in type restriction for V1 receiving
    if sv:
        var_type = sv['type']
        if _is_builtin_type(var_type) and api_level == 'pre19':
            violations.append({
                'type': 'V2_TO_V1_BUILTIN_TYPE',
                'severity': 'error',
                'component': f'{parent_name} -> {child_name}',
                'file': child_comp.get('file', ''),
                'message': (f"Cannot pass built-in type '{var_type}' from V2 to V1. "
                            f"V1 does not support receiving Array/Set/Map/Date from V2."),
            })

    # Function type restriction
    if passage_type == 'callback' and api_level == 'pre19':
        warnings.append({
            'type': 'V2_TO_V1_FUNCTION_TYPE',
            'severity': 'warning',
            'component': f'{parent_name} -> {child_name}',
            'file': child_comp.get('file', ''),
            'message': (f"Passing callback from V2 '{parent_name}' to V1 '{child_name}'. "
                        f"Function type is supported in V2 but may cause runtime issues "
                        f"in V1 decorators at API < 19."),
        })


def _check_bridge_pattern_need(
    components: List[Dict],
    comps_by_name: Dict[str, List[Dict]],
    file_map: Dict[str, Dict],
    api_level: str,
    suggestions: List[Dict],
):
    """Detect situations where bridge pattern is needed (V1 passing @Observed to V2)."""
    if api_level == 'post19':
        return  # API >= 19 can use enableV2Compatibility, no bridge needed

    for comp in components:
        if comp['version'] != 'V1':
            continue

        for child_name in comp.get('usedComponents', []):
            child_comp, _ = _resolve_child(comps_by_name, comp.get('file', ''), child_name)
            if not child_comp or child_comp['version'] != 'V2':
                continue

            # Check if any @Observed class is being passed
            for sv in comp.get('stateVariables', []):
                if sv.get('isClassType') and not _is_builtin_type(sv['type']):
                    suggestions.append({
                        'type': 'BRIDGE_PATTERN_SUGGESTED',
                        'severity': 'info',
                        'component': f'{comp["name"]} -> {child_name}',
                        'file': comp.get('file', ''),
                        'message': (f"V1 component '{comp['name']}' has class-typed state "
                                    f"'{sv['name']}: {sv['type']}'. If this is an @Observed "
                                    f"class being passed to V2 '{child_name}', a bridge "
                                    f"component is required:\n"
                                    f"  V1: {comp['name']} -> V1Bridge(@Component) -> "
                                    f"V2: {child_name}(@ComponentV2)\n"
                                    f"Bridge uses @Watch to sync data to "
                                    f"@ObservedV2/@Trace singleton."),
                    })


def _check_multiple_decorators(components: List[Dict], violations: List[Dict]):
    """Rule: Multiple state decorators on the same variable (except aux decorators)."""
    for comp in components:
        for sv in comp.get('stateVariables', []):
            primary = sv['decorator']
            aux = sv.get('auxDecorators', [])

            # Check for multiple state decorators (non-aux)
            non_aux = [d for d in [primary] + aux
                       if d not in AUX_DECORATORS and d in (V1_DECORATORS | V2_DECORATORS)]
            if len(non_aux) > 1:
                violations.append({
                    'type': 'MULTIPLE_STATE_DECORATORS',
                    'severity': 'error',
                    'component': comp['name'],
                    'file': comp.get('file', ''),
                    'message': (f"Variable '{sv['name']}' in '{comp['name']}' has multiple "
                                f"state decorators: {', '.join(non_aux)}. "
                                f"Only one state decorator is allowed per variable "
                                f"(auxiliary decorators like @Watch/@Once/@Require are ok)."),
                })


def _check_within_component_mixing(components: List[Dict], violations: List[Dict]):
    """Rule: V1 and V2 state decorators must not mix within one component.

    A @Component (V1) component must not carry V2 state decorators
    (@Local/@Param/@Event/@Provider/@Consumer/@Computed), and a @ComponentV2 (V2)
    component must not carry V1 state decorators (@State/@Prop/@Link/@Provide/
    @Consume/@ObjectLink/@StorageLink/@StorageProp/@LocalStorageLink/@LocalStorageProp).
    The compiler rejects this; the validator flags it too so it works as a grading
    oracle without a toolchain. Version-neutral aux decorators (@Watch/@Monitor/@Once/
    @Require) are excluded.
    """
    v1_state = V1_DECORATORS - AUX_DECORATORS
    v2_state = V2_DECORATORS - AUX_DECORATORS
    for comp in components:
        version = comp.get('version')
        if version not in ('V1', 'V2'):
            continue
        bad_v1: List[str] = []
        bad_v2: List[str] = []
        for sv in comp.get('stateVariables', []):
            dec = sv.get('decorator')
            if not dec or dec in AUX_DECORATORS:
                continue
            name = sv.get('name', '')
            if version == 'V2' and dec in v1_state:
                bad_v1.append(f"{dec} {name}".strip())
            elif version == 'V1' and dec in v2_state:
                bad_v2.append(f"{dec} {name}".strip())
        for offenders, msg in (
            (bad_v1, "is a V2 (@ComponentV2) component but uses V1 state decorators"),
            (bad_v2, "is a V1 (@Component) component but uses V2 state decorators"),
        ):
            if offenders:
                violations.append({
                    'type': 'WITHIN_COMPONENT_MIXING',
                    'severity': 'error',
                    'component': comp['name'],
                    'file': comp.get('file', ''),
                    'message': (f"'{comp['name']}' {msg}: {', '.join(offenders)}. "
                                f"V1 and V2 state decorators cannot be mixed within the "
                                f"same component (compiler error)."),
                })


def _check_class_decorator_coexistence(classes: List[Dict], violations: List[Dict]):
    """Rule: a class must not carry both @Observed and @ObservedV2.

    This is a compiler error, but the validator flags it too so it works as a
    grading oracle without a toolchain (matches SKILL.md checklist item
    "No @Observed and @ObservedV2 coexisting on the same class"). A botched
    migration that adds @ObservedV2 without removing @Observed is caught here
    instead of being reported as compliant.
    """
    for cls in classes:
        obs = set(cls.get('observedDecorators') or [])
        if '@Observed' in obs and '@ObservedV2' in obs:
            violations.append({
                'type': 'CLASS_OBSERVED_COEXISTENCE',
                'severity': 'error',
                'component': cls['name'],
                'file': cls.get('file', ''),
                'message': (
                    f"Class '{cls['name']}' is decorated with both @Observed and "
                    f"@ObservedV2. A class must use exactly one observation model "
                    f"(compiler error); remove one of them."
                ),
            })


def _find_child_param(child_comp: Dict, param_name: str) -> Optional[Dict]:
    """Find the state variable in child component that matches the param name."""
    for sv in child_comp.get('stateVariables', []):
        if sv['name'] == param_name:
            return sv
    return None


def _is_simple_or_enum(type_str: str) -> bool:
    """Check if type is simple or enum."""
    type_str = type_str.strip().lower()
    type_str = type_str.replace('| undefined', '').replace('| null', '').strip()
    return type_str in SIMPLE_TYPES or type_str.startswith('enum')


def _is_builtin_type(type_str: str) -> bool:
    """Check if type is a built-in collection type."""
    type_str = type_str.strip()
    for bt in BUILTIN_TYPES_SET:
        if type_str.startswith(bt):
            return True
    return False


def _filter_by_component(items: List[Dict], target: str) -> List[Dict]:
    """Filter violations/warnings to only those related to target component."""
    filtered = []
    for item in items:
        comp = item.get('component', '')
        if target in comp:
            filtered.append(item)
    return filtered


def _build_interaction_map(
    components: List[Dict],
    comps_by_name: Dict[str, List[Dict]],
) -> Dict:
    """Build a map of V1<->V2 component interactions."""
    interactions = {}
    for comp in components:
        parent_version = comp['version']
        for child_name in comp.get('usedComponents', []):
            child_comp, _ = _resolve_child(comps_by_name, comp.get('file', ''), child_name)
            if not child_comp:
                continue
            child_version = child_comp['version']
            if parent_version != child_version:
                key = f"{comp['name']}({parent_version})->{child_name}({child_version})"
                interactions[key] = {
                    'parent': comp['name'],
                    'parentVersion': parent_version,
                    'child': child_name,
                    'childVersion': child_version,
                    'direction': f"{parent_version}->{child_version}",
                }
    return interactions


def main():
    parser = argparse.ArgumentParser(
        description='Validate V1/V2 component mixing rules in a project'
    )
    parser.add_argument('project_dir', help='Project root directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--target', help='Focus on a specific component')
    args = parser.parse_args()

    if not Path(args.project_dir).is_dir():
        print(f"Error: {args.project_dir} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    result = validate_project(args.project_dir, args.target)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        api = result['apiVersion']
        print(f"\n{'='*60}")
        print(f"V1/V2 Mixing Validation: {result['projectDir']}")
        print(f"API Version: {api['compatibleApiVersion']} ({api['mixingRules']} rules)")
        print(f"{'='*60}")

        print(f"\n  Components: {result['totalComponents']} total "
              f"({len(result['v1Components'])} V1, {len(result['v2Components'])} V2)")

        if result['interactions']:
            print(f"\n  V1<->V2 Interactions:")
            for key, info in result['interactions'].items():
                print(f"    {key}")

        if result['violations']:
            print(f"\n  VIOLATIONS ({len(result['violations'])}):")
            for v in result['violations']:
                print(f"    [{v['severity'].upper()}] {v['type']}")
                print(f"      Component: {v['component']}")
                if v.get('file'):
                    print(f"      File: {v['file']}")
                print(f"      {v['message']}")
                print()

        if result['warnings']:
            print(f"\n  WARNINGS ({len(result['warnings'])}):")
            for w in result['warnings']:
                print(f"    [{w['severity'].upper()}] {w['type']}")
                print(f"      Component: {w['component']}")
                print(f"      {w['message']}")
                print()

        if result['suggestions']:
            print(f"\n  SUGGESTIONS ({len(result['suggestions'])}):")
            for s in result['suggestions']:
                print(f"    [{s['severity'].upper()}] {s['type']}")
                print(f"      Component: {s['component']}")
                print(f"      {s['message']}")
                print()

        s = result['summary']
        print(f"  Summary: {s['violationCount']} violations, "
              f"{s['warningCount']} warnings, {s['suggestionCount']} suggestions")
        if s['isCompliant']:
            print(f"  Result: COMPLIANT")
        else:
            print(f"  Result: NON-COMPLIANT - fix violations before proceeding")


if __name__ == '__main__':
    main()
