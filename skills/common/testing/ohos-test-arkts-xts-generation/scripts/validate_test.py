#!/usr/bin/env python3
"""Phase 7 集成验证脚本 - 对生成的测试文件进行全面检查"""

import argparse
import re
import sys


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_no_as_any(test_content: str) -> tuple[bool, str]:
    if "as any" in test_content:
        return False, "发现 'as any'"
    return True, ""


def check_no_function_type(test_content: str) -> tuple[bool, str]:
    patterns = [": Function", ": Function)"]
    for p in patterns:
        if p in test_content:
            return False, f"发现 '{p}'"
    return True, ""


def check_no_any_unknown(test_content: str) -> tuple[bool, str]:
    patterns = [": any", ": unknown"]
    for p in patterns:
        if p in test_content:
            return False, f"发现 '{p}'"
    return True, ""


def check_router_import(test_content: str) -> tuple[bool, str]:
    wrong = "@ohos/router"
    if wrong in test_content:
        return False, f"发现 '{wrong}' 应为 '@ohos.router'"
    return True, ""


def check_tc_annotations(test_content: str) -> tuple[bool, str]:
    it_pattern = re.compile(r"\bit\s*\(\s*['\"]")
    tc_pattern = re.compile(r"@tc\.name")
    it_count = len(it_pattern.findall(test_content))
    tc_count = len(tc_pattern.findall(test_content))
    if it_count > 0 and tc_count < it_count:
        return False, f"it() 有 {it_count} 处，@tc.name 有 {tc_count} 处"
    return True, ""


def check_it_camel_case(test_content: str) -> tuple[bool, str]:
    pattern = re.compile(r"\bit\s*\(\s*'([A-Z])")
    match = pattern.search(test_content)
    if match:
        return False, f"it() 名称首字母大写: '...{match.group(0)}...'"
    return True, ""


def check_level_values(test_content: str) -> tuple[bool, str]:
    wrong_pattern = re.compile(r"Level\.Level\d")
    wrong_pattern2 = re.compile(r"Level\.level\d")
    wrong_pattern3 = re.compile(r"Level\.\d+")
    for pat in [wrong_pattern, wrong_pattern2, wrong_pattern3]:
        match = pat.search(test_content)
        if match:
            return False, f"发现错误写法 '{match.group(0)}'，应为 'Level.LEVEL0'~'Level.LEVEL4'"
    return True, ""


def check_esobject_style(test_content: str) -> tuple[bool, str]:
    has_json_parse = "JSON.parse" in test_content
    has_record_object = "Record<string, Object>" in test_content or "Record<string, object>" in test_content
    has_esobject = "ESObject" in test_content
    if has_json_parse and has_record_object and not has_esobject:
        return False, "JSON.parse 结果使用了 Record<string, Object>，应使用 ESObject"
    if has_record_object and not has_esobject:
        return False, "发现 Record<string, Object> 类型，建议使用 ESObject 与现有代码风格保持一致"
    return True, ""


def check_component_ids(test_content: str, page_content: str) -> tuple[bool, str]:
    inspector_pattern = re.compile(r"getInspectorByKey\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
    id_pattern = re.compile(r"\.id\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
    test_ids = set(inspector_pattern.findall(test_content))
    page_ids = set(id_pattern.findall(page_content))
    missing = test_ids - page_ids
    if missing:
        return False, f"测试中引用的组件id在页面中不存在: {sorted(missing)}"
    return True, ""


def check_design_doc_component_ids(design_content: str) -> tuple[bool, str]:
    case_pattern = re.compile(r"##\s+\d+\.\d+|###\s+用例|###\s+Test", re.IGNORECASE)
    id_field_pattern = re.compile(r"\*\*组件id\*\*|\*\*组件ID\*\*", re.IGNORECASE)
    cases = case_pattern.split(design_content)
    cases_with_checks = 0
    cases_missing_id = 0
    for case_block in cases[1:]:
        has_get_inspector = "getInspectorByKey" in case_block or "组件id" in case_block.lower() or "组件ID" in case_block
        if not has_get_inspector and not case_block.strip():
            continue
        has_id_field = bool(id_field_pattern.search(case_block))
        if has_get_inspector and not has_id_field:
            cases_missing_id += 1
        if has_get_inspector:
            cases_with_checks += 1
    all_cases = re.findall(r"^##\s+\d+\.\d+", design_content, re.MULTILINE)
    if not all_cases:
        all_cases = re.findall(r"^###\s+用例", design_content, re.MULTILINE)
    if not all_cases:
        return True, ""
    if cases_missing_id > 0:
        return False, f"有 {cases_missing_id} 个用例缺少 '**组件id**' 字段"
    return True, ""


def check_design_doc_ids_in_page(design_content: str, page_content: str) -> tuple[bool, str]:
    id_field_pattern = re.compile(r"\*\*组件id\*\*\s*[:：]?\s*`?([^`\n]+)`?", re.IGNORECASE)
    design_ids = set()
    for m in id_field_pattern.finditer(design_content):
        id_val = m.group(1).strip().strip("`").strip()
        if id_val:
            design_ids.add(id_val)
    id_pattern = re.compile(r"\.id\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
    page_ids = set(id_pattern.findall(page_content))
    missing = design_ids - page_ids
    if missing:
        return False, f"设计文档中的组件id在页面中不存在: {sorted(missing)}"
    return True, ""


def check_export_default_function(test_content: str) -> tuple[bool, str]:
    if "export default function" not in test_content:
        return False, "缺少 'export default function'"
    return True, ""


def check_hypium_import(test_content: str) -> tuple[bool, str]:
    if '@ohos/hypium' not in test_content:
        return False, "缺少 from \"@ohos/hypium\" 导入"
    return True, ""


# Hypium Assert 合法方法白名单（来自 01_hypium_framework.md）
# 包含 27 个方法：基础 23 + 扩展 4（assertLargerOrEqual, assertLessOrEqual, assertMatchObj, message）
# 外加 not 修饰器
VALID_ASSERT_METHODS = {
    'assertClose', 'assertContain', 'assertDeepEquals', 'assertEqual',
    'assertFail', 'assertFalse', 'assertTrue', 'assertInstanceOf',
    'assertLarger', 'assertLess', 'assertNaN', 'assertNegUnlimited',
    'assertNull', 'assertPosUnlimited', 'assertPromiseIsPending',
    'assertPromiseIsRejected', 'assertPromiseIsRejectedWith',
    'assertPromiseIsRejectedWithError', 'assertPromiseIsResolved',
    'assertPromiseIsResolvedWith', 'assertThrowError', 'assertUndefined',
    'assertLargerOrEqual', 'assertLessOrEqual', 'assertMatchObj',
    'not', 'message',
}


def check_assert_methods(test_content: str) -> tuple[bool, str]:
    """检查测试文件中使用的 expect().xxx() 断言方法是否在合法白名单中。

    检测 expect(...).assertXxx(...) 模式，对比 VALID_ASSERT_METHODS。
    常见错误：
      - assertLargerThan (不存在，应为 assertLarger)
      - assertLessThan (不存在，应为 assertLess)
      - assertNotNull (不存在，应用 not().assertNull())
      - assertNotEqual (不存在，应用 not().assertEqual())
    """
    # 匹配 expect(...).methodName( 模式
    pattern = re.compile(r'\.\b(assert[A-Z]\w*)\s*\(')
    # 匹配 expect(...).not() / .message() 模式
    modifier_pattern = re.compile(r'\.\b(not|message)\s*\(')

    all_methods = set(pattern.findall(test_content))
    all_modifiers = set(modifier_pattern.findall(test_content))

    # 合并所有方法名
    used = all_methods | all_modifiers

    # 过滤掉非 expect 链上的（getInspectorByKey 等 assert 开头的非断言方法不算）
    # 只关注 assert 开头的 + not/message 修饰器
    invalid = set()
    for m in used:
        if m.startswith('assert') and m not in VALID_ASSERT_METHODS:
            invalid.add(m)

    if not invalid:
        return True, ""

    # 生成修复建议
    suggestions = {
        'assertLargerThan': 'assertLarger',
        'assertLessThan': 'assertLess',
        'assertNotNull': 'not().assertNull()',
        'assertNotEqual': 'not().assertEqual()',
        'assertNotUndefined': 'not().assertUndefined()',
        'assertNotContain': 'not().assertContain()',
        'assertNotInstanceOf': 'not().assertInstanceOf()',
        'assertNotClose': 'not().assertClose()',
    }
    details = []
    for m in sorted(invalid):
        suggestion = suggestions.get(m)
        if suggestion:
            details.append(f"{m} → 应为 {suggestion}")
        else:
            details.append(f"{m} (不存在于 Hypium Assert 接口)")

    return False, f"发现不存在的断言方法: {'; '.join(details)}"


def main():
    parser = argparse.ArgumentParser(description="Phase 7 集成验证脚本")
    parser.add_argument("--test-file", required=True, help="测试文件路径 (.ets)")
    parser.add_argument("--page-file", default=None, help="页面文件路径 (.ets)，不提供则跳过组件id检查")
    parser.add_argument("--design-doc", default=None, help="设计文档路径 (.md)，不提供则跳过设计文档检查")
    args = parser.parse_args()

    test_content = read_file(args.test_file)
    page_content = read_file(args.page_file) if args.page_file else ""
    design_content = read_file(args.design_doc) if args.design_doc else ""

    checks = [
        ("A.1 无 as any", lambda: check_no_as_any(test_content)),
        ("A.2 无 Function 类型", lambda: check_no_function_type(test_content)),
        ("A.3 无 any/unknown 类型", lambda: check_no_any_unknown(test_content)),
        ("A.4 正确的 router 导入", lambda: check_router_import(test_content)),
        ("A.5 @tc 注释完整", lambda: check_tc_annotations(test_content)),
        ("A.6 it() 名称 camelCase", lambda: check_it_camel_case(test_content)),
        ("A.7 Level 值合法", lambda: check_level_values(test_content)),
        ("A.8 ESObject 类型风格", lambda: check_esobject_style(test_content)),
    ]

    # 需要 page-file 的检查
    if page_content:
        checks.extend([
            ("A.9 组件id一致性", lambda: check_component_ids(test_content, page_content)),
        ])
    
    # 需要 design-doc 的检查
    if design_content:
        checks.extend([
            ("A.10 设计文档组件id", lambda: check_design_doc_component_ids(design_content)),
        ])
    
    # 同时需要 page-file 和 design-doc 的检查
    if page_content and design_content:
        checks.extend([
            ("A.11 设计文档组件id一致性", lambda: check_design_doc_ids_in_page(design_content, page_content)),
        ])

    checks.extend([
        ("A.12 export default function", lambda: check_export_default_function(test_content)),
        ("A.13 hypium 导入", lambda: check_hypium_import(test_content)),
        ("A.14 断言方法合法性", lambda: check_assert_methods(test_content)),
    ])

    print("=== Phase 7 验证报告 ===")
    print(f"测试文件: {args.test_file}")
    print(f"页面文件: {args.page_file}")
    print(f"设计文档: {args.design_doc}")
    print("---")

    passed = 0
    failed = 0
    for name, check_fn in checks:
        ok, detail = check_fn()
        if ok:
            print(f"[PASS] {name}")
            passed += 1
        else:
            msg = f"{name}: {detail}" if detail else name
            print(f"[FAIL] {msg}")
            failed += 1

    print("===")
    print(f"通过: {passed}/{passed + failed}  失败: {failed}/{passed + failed}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
