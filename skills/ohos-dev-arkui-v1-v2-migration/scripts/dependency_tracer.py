#!/usr/bin/env python3
"""
V1->V2 Migration - Dependency Tracer
Traces component dependency chains to determine migration scope.
Given a target component, finds all parent/child components with data interaction.

Usage:
    python3 dependency_tracer.py <target_component> <project_dir> [--json] [--max-depth N]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

# Import component_analyzer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from component_analyzer import (
    analyze_file, analyze_directory, read_file, extract_components,
    normalize_decorator, V1_DECORATORS, V2_DECORATORS, SIMPLE_TYPES, BUILTIN_TYPES,
    _KEY_CHANNEL_DECORATORS,
)


def find_component_definition(target_name: str, project_dir: str) -> Optional[Dict]:
    """Find the file and details of a component by name. Returns the first match."""
    results = find_all_component_definitions(target_name, project_dir)
    return results[0] if results else None


def find_all_component_definitions(target_name: str, project_dir: str) -> List[Dict]:
    """Find all definitions of a component by name across the project."""
    all_defs = []
    for ets_file in Path(project_dir).glob('**/*.ets'):
        content = read_file(str(ets_file))
        if content is None:
            continue
        if not re_search_component(content, target_name):
            continue

        result = analyze_file(str(ets_file))
        for comp in result.get('components', []):
            if comp['name'] == target_name:
                comp['file'] = str(ets_file)
                all_defs.append(comp)
    return all_defs


def re_search_component(content: str, name: str) -> bool:
    """Quick check if a component struct exists in content."""
    import re
    return bool(re.search(rf'\bstruct\s+{re.escape(name)}\b', content))


def find_component_usages(target_name: str, project_dir: str) -> List[Dict]:
    """Find all files that use (instantiate) a target component."""
    import re
    usages = []
    pattern = re.compile(rf'\b{re.escape(target_name)}\s*\(')

    for ets_file in Path(project_dir).glob('**/*.ets'):
        content = read_file(str(ets_file))
        if content is None:
            continue
        if pattern.search(content):
            # Find which component(s) in this file use the target
            result = analyze_file(str(ets_file))
            for comp in result.get('components', []):
                if target_name in comp.get('usedComponents', []):
                    usages.append({
                        'file': str(ets_file),
                        'parentComponent': comp['name'],
                        'parentVersion': comp['version'],
                        'parentFile': str(ets_file),
                    })
    return usages


def analyze_state_passing(parent_content: str, child_name: str, parent_name: str) -> List[Dict]:
    """Analyze how state variables are passed from parent to child component."""
    import re
    passages = []

    # Find child component instantiation: ChildName({ prop: value, ... })
    pattern = re.compile(
        rf'\b{re.escape(child_name)}\s*\(\s*\{{([^}}]*)\}}',
        re.DOTALL
    )

    for m in pattern.finditer(parent_content):
        args_text = m.group(1)

        # Parse individual arguments: name: value
        for arg_match in re.finditer(r'(\w+)\s*:\s*([^,}\n]+)', args_text):
            arg_name = arg_match.group(1)
            arg_value = arg_match.group(2).strip()

            # Determine the type of value being passed
            passage_type = classify_passage_type(arg_value)
            passages.append({
                'childParam': arg_name,
                'parentExpression': arg_value,
                'passageType': passage_type,
            })

    return passages


def classify_passage_type(value_expr: str) -> str:
    """Classify the type of data being passed in a component parameter."""
    import re
    value_expr = value_expr.strip()

    # $$this.xxx or this.xxx!! - two-way binding
    if value_expr.startswith('$$') or '!!' in value_expr:
        return 'two_way_binding'

    # $varName - V1 @Link reference syntax (e.g. FontSizeAdjuster({ size: $fontSize }))
    if re.match(r'^\$\w+$', value_expr):
        return 'two_way_binding'

    # this.xxx or this.xxx.yyy.zzz (nested property access) - state variable
    # reference. Type impact is decided by the ROOT variable (this.<root>),
    # resolved by the caller via _passage_forces_migration.
    if re.match(r'this\.\w+(\.\w+)*$', value_expr):
        return 'state_variable_ref'

    # New expression - new XXX(...)
    if 'new ' in value_expr:
        return 'new_instance'

    # Arrow function - () => ...
    if value_expr.startswith('(') or value_expr.startswith('() =>') or '=>' in value_expr:
        return 'callback'

    # Literal values
    if re.match(r'^(\d+|true|false|null|undefined|\'[^\']*\'|"[^"]*")$', value_expr):
        return 'literal'

    # Function call
    if '(' in value_expr and ')' in value_expr:
        return 'function_call'

    return 'expression'


def build_key_coupling_map(project_dir: str) -> Dict:
    """Index key-channel bindings (Provide/Consume, Storage*) across the project.

    Returns {'compToKeys': {compName: [entry,...]}, 'keyToComps': {key: [entry,...]}}.
    Two components sharing a key are coupled even when the parent's build() passes
    NO constructor arguments — the binding lives in the decorator argument, which
    the expression-based passage scanner cannot see.
    """
    results = analyze_directory(project_dir, recursive=True)
    comp_to_keys: Dict[str, List[Dict]] = {}
    key_to_comps: Dict[str, List[Dict]] = {}
    for result in results:
        if 'error' in result:
            continue
        for comp in result.get('components', []):
            for sv in comp.get('stateVariables', []):
                dec = sv['decorator']
                key = sv.get('decoratorArg')
                if dec not in _KEY_CHANNEL_DECORATORS or not key:
                    continue
                entry = {
                    'component': comp['name'],
                    'file': result['file'],
                    'decorator': dec,
                    'key': key,
                    'variable': sv['name'],
                }
                comp_to_keys.setdefault(comp['name'], []).append(entry)
                key_to_comps.setdefault(key, []).append(entry)
    return {'compToKeys': comp_to_keys, 'keyToComps': key_to_comps}


def _edge_direction(passages: List[Dict], receiving_comp: Optional[Dict]) -> str:
    """Determine edge direction (one_way/two_way) from the decorator PAIR, not from
    the '$' syntax alone. two_way if any passage uses $$/!!/$var, OR the receiving
    component declares the bound param as @Link/@ObjectLink. one_way if @Param/@Prop.
    Falls back to 'unknown' when the receiving decorator can't be resolved."""
    for p in passages:
        if p['passageType'] == 'two_way_binding':
            return 'two_way'
    if receiving_comp:
        for p in passages:
            for sv in receiving_comp.get('stateVariables', []):
                if sv['name'] == p['childParam']:
                    if sv['decorator'] in ('@Link', '@ObjectLink'):
                        return 'two_way'
                    if sv['decorator'] in ('@Param', '@Prop'):
                        return 'one_way'
    return 'unknown'


def _resolve_referenced_var(parent_comp: Optional[Dict], var_name: str) -> Optional[Dict]:
    """Look up the state-variable declaration for `var_name` in the parent component."""
    if not parent_comp:
        return None
    for sv in parent_comp.get('stateVariables', []):
        if sv.get('name') == var_name:
            return sv
    return None


def _passage_forces_migration(passage: Dict, parent_comp: Optional[Dict]) -> bool:
    """Whether a parent->child passage forces the partner into mustMigrate.

    Per references/mixing-rules.md, simple types (number/string/boolean) can cross
    the V1/V2 boundary freely and do NOT force joint migration; only complex types
    (@Observed class / Array / Map / Set / Date) do. Two-way bindings always force
    because V2 has no bidirectional equivalent — both sides must be rewritten
    together. Unresolvable references default to forcing (conservative — avoids
    silently dropping a real coupling).
    """
    ptype = passage.get('passageType')
    if ptype == 'two_way_binding':
        return True
    if ptype != 'state_variable_ref':
        return False

    expr = passage.get('parentExpression', '').strip()
    var_name = expr[len('this.'):].split('.')[0] if expr.startswith('this.') else expr
    sv = _resolve_referenced_var(parent_comp, var_name)
    if sv is None:
        return True  # unknown → conservative
    return bool(sv.get('isClassType') or sv.get('isBuiltinType'))


def build_dependency_graph(
    target_name: str,
    project_dir: str,
    max_depth: int = 5
) -> Dict:
    """Build a complete dependency graph for a target component."""
    visited = set()
    graph = {}
    scope = {
        'mustMigrate': [],
        'mayNeedMigration': [],
        'reasons': {},
        'components': {},
    }

    def trace(name: str, direction: str, depth: int, path: List[str]):
        if depth > max_depth or name in visited:
            return
        visited.add(name)
        path = path + [name]

        comp = find_component_definition(name, project_dir)
        if comp is None:
            scope['components'][name] = {
                'name': name,
                'found': False,
                'reason': f'Component definition not found in project',
            }
            return

        scope['components'][name] = {
            'name': name,
            'file': comp['file'],
            'version': comp['version'],
            'hasInput': comp['hasInput'],
            'hasOutput': comp['hasOutput'],
            'stateVariables': comp['stateVariables'],
        }

        # Check if this component has data interactions requiring migration
        has_data_interaction = comp['hasInput'] or comp['hasOutput']

        if direction == 'down':
            # Trace children: find components used by this component
            for child_name in comp.get('usedComponents', []):
                child_comp = find_component_definition(child_name, project_dir)
                if child_comp is None:
                    continue

                # Check if there's data passing
                parent_content = read_file(comp['file'])
                if parent_content:
                    passages = analyze_state_passing(parent_content, child_name, name)
                else:
                    passages = []

                has_complex_passage = any(
                    _passage_forces_migration(p, comp) for p in passages
                )
                has_simple_ref = not has_complex_passage and any(
                    p.get('passageType') == 'state_variable_ref' for p in passages
                )

                if has_complex_passage and child_name not in [c for c in scope['mustMigrate']]:
                    scope['mustMigrate'].append(child_name)
                    scope['reasons'][f'{name}->{child_name}'] = {
                        'direction': 'parent->child',
                        'edgeDirection': _edge_direction(passages, child_comp),
                        'passages': passages,
                        'summary': _summarize_passages(passages),
                    }
                elif has_simple_ref \
                        and child_name not in scope['mustMigrate'] \
                        and child_name not in scope['mayNeedMigration']:
                    # Simple-type ref: V1/V2-compatible, no joint migration needed,
                    # but record so the coupling isn't silently lost.
                    scope['mayNeedMigration'].append(child_name)

                trace(child_name, 'down', depth + 1, path)

        if direction == 'up':
            # Trace parents: find components that use this component
            usages = find_component_usages(name, project_dir)
            for usage in usages:
                parent_name = usage['parentComponent']
                parent_content = read_file(usage['file'])
                if parent_content:
                    passages = analyze_state_passing(parent_content, name, parent_name)
                else:
                    passages = []

                # The referenced `this.xxx` lives in the PARENT; resolve its type
                # from the parent's state variables to decide if it forces migration.
                parent_comp = find_component_definition(parent_name, project_dir)

                has_complex_passage = any(
                    _passage_forces_migration(p, parent_comp) for p in passages
                )
                has_simple_ref = not has_complex_passage and any(
                    p.get('passageType') == 'state_variable_ref' for p in passages
                )

                if has_complex_passage and parent_name not in [c for c in scope['mustMigrate']]:
                    scope['mustMigrate'].append(parent_name)
                    scope['reasons'][f'{parent_name}->{name}'] = {
                        'direction': 'parent->child',
                        'edgeDirection': _edge_direction(passages, comp),
                        'passages': passages,
                        'summary': _summarize_passages(passages),
                    }
                elif has_simple_ref \
                        and parent_name not in scope['mustMigrate'] \
                        and parent_name not in scope['mayNeedMigration']:
                    scope['mayNeedMigration'].append(parent_name)

                trace(parent_name, 'up', depth + 1, path)

    # Start tracing from target
    target_comp = find_component_definition(target_name, project_dir)
    if target_comp is None:
        return {
            'error': f'Component "{target_name}" not found in {project_dir}',
            'targetComponent': target_name,
            'projectDir': project_dir,
        }

    scope['mustMigrate'].append(target_name)
    scope['components'][target_name] = {
        'name': target_name,
        'file': target_comp.get('file', 'unknown'),
        'version': target_comp['version'],
        'hasInput': target_comp['hasInput'],
        'hasOutput': target_comp['hasOutput'],
        'stateVariables': target_comp['stateVariables'],
    }

    # If target has inputs/outputs, trace both directions
    if target_comp['hasInput'] or target_comp['hasOutput']:
        trace(target_name, 'up', 0, [])
        visited.discard(target_name)  # Allow target to be traced in the other direction
        trace(target_name, 'down', 0, [])
    else:
        # No inputs/outputs, only this component needs migration
        pass

    # Key-based coupling: Provide/Consume and Storage bindings live in decorator
    # arguments (not constructor arguments), so the passage scan above cannot see
    # them. Pull in any component sharing a key with something already in
    # mustMigrate, iterating to fixpoint (key graphs are not strictly parent/child).
    key_index = build_key_coupling_map(project_dir)
    changed = True
    while changed:
        changed = False
        for comp_name in list(scope['mustMigrate']):
            for entry in key_index['compToKeys'].get(comp_name, []):
                for partner in key_index['keyToComps'][entry['key']]:
                    p_name = partner['component']
                    if p_name == comp_name or p_name in scope['mustMigrate']:
                        continue
                    scope['mustMigrate'].append(p_name)
                    key_val = entry['key']
                    scope['reasons'][f'{comp_name}<-key({key_val})->{p_name}'] = {
                        'direction': 'key_binding',
                        'edgeDirection': 'two_way',
                        'key': key_val,
                        'summary': (f"shared key '{key_val}': "
                                    f"{comp_name}({entry['decorator']} {entry['variable']}) "
                                    f"<-> {p_name}({partner['decorator']} {partner['variable']})"),
                    }
                    pdef = find_component_definition(p_name, project_dir)
                    if pdef:
                        scope['components'][p_name] = {
                            'name': p_name,
                            'file': pdef.get('file', 'unknown'),
                            'version': pdef['version'],
                            'hasInput': pdef['hasInput'],
                            'hasOutput': pdef['hasOutput'],
                            'stateVariables': pdef['stateVariables'],
                        }
                    changed = True

    # Deduplicate mustMigrate and mayNeedMigration (and keep them disjoint)
    scope['mustMigrate'] = list(dict.fromkeys(scope['mustMigrate']))
    must_set = set(scope['mustMigrate'])
    scope['mayNeedMigration'] = [
        c for c in dict.fromkeys(scope['mayNeedMigration']) if c not in must_set
    ]

    return {
        'targetComponent': target_name,
        'projectDir': project_dir,
        'migrationScope': scope,
        'dependencyGraph': _build_graph_summary(scope),
    }


def _summarize_passages(passages: List[Dict]) -> str:
    """Create a human-readable summary of state passing."""
    if not passages:
        return 'No data passing detected'

    summaries = []
    for p in passages:
        summaries.append(f"{p['childParam']}: {p['passageType']} ({p['parentExpression']})")
    return '; '.join(summaries)


def _build_graph_summary(scope: Dict) -> Dict:
    """Build a simplified dependency graph for display."""
    graph = {}
    for key, reason in scope.get('reasons', {}).items():
        parts = key.split('->')
        if len(parts) == 2:
            parent, child = parts
            if parent not in graph:
                graph[parent] = {'children': [], 'stateFlow': []}
            graph[parent]['children'].append(child)
            graph[parent]['stateFlow'].append(reason['summary'])

    return graph


def main():
    parser = argparse.ArgumentParser(
        description='Trace component dependency chains for V1->V2 migration scope'
    )
    parser.add_argument('target', help='Target component name to trace')
    parser.add_argument('project_dir', help='Project root directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--max-depth', type=int, default=5, help='Maximum trace depth')
    args = parser.parse_args()

    result = build_dependency_graph(args.target, args.project_dir, args.max_depth)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if 'error' in result:
            print(f"\nError: {result['error']}")
            sys.exit(1)

        print(f"\n{'='*60}")
        print(f"Dependency Trace: {result['targetComponent']}")
        print(f"Project: {result['projectDir']}")
        print(f"{'='*60}")

        scope = result['migrationScope']

        print(f"\n--- Migration Scope ---")
        print(f"Must Migrate: {', '.join(scope['mustMigrate'])}")
        if scope.get('mayNeedMigration'):
            print(f"May Need (simple-type coupling, optional): {', '.join(scope['mayNeedMigration'])}")

        print(f"\n--- Components ---")
        for name, comp in scope['components'].items():
            found = comp.get('found', True)
            if not found:
                print(f"  {name}: NOT FOUND - {comp.get('reason', '')}")
            else:
                print(f"  {name} ({comp['version']}) - {comp['file']}")
                print(f"    Has Input: {comp['hasInput']}, Has Output: {comp['hasOutput']}")
                if comp.get('stateVariables'):
                    for sv in comp['stateVariables']:
                        print(f"      {sv['decorator']} {sv['name']}: {sv['type']}")

        print(f"\n--- Data Flow Reasons ---")
        for key, reason in scope.get('reasons', {}).items():
            print(f"  {key}:")
            print(f"    {reason['summary']}")
            if reason.get('passages'):
                for p in reason['passages']:
                    print(f"      - {p['childParam']}: {p['parentExpression']} [{p['passageType']}]")

        print(f"\n--- Dependency Graph ---")
        for parent, info in result.get('dependencyGraph', {}).items():
            for i, child in enumerate(info['children']):
                flow = info['stateFlow'][i] if i < len(info['stateFlow']) else ''
                print(f"  {parent} -> {child}: {flow}")


if __name__ == '__main__':
    main()
