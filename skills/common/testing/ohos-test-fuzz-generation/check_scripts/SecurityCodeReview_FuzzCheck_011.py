#!/usr/bin/env python3
"""
规则011: 系统安全准入条件
检查是否可能缺少权限、身份、状态等安全上下文构造
"""

import re
import os


def check_security_context(content):
    """
    规则011: 检查系统安全准入条件
    检测是否可能缺少权限、身份、状态等安全上下文构造
    """
    errors = []

    security_precondition_patterns = [
        (
            r"\b(?:SetPermission|CheckPermission|VerifyPermission|GrantPermission)\b",
            "权限校验",
        ),
        (r"\b(?:SetUid|SetCallerUid|SetPid|SetCallerPid|SetCaller)\b", "UID/PID校验"),
        (
            r"\b(?:SetCapability|CheckCapability|HasCapability)\b",
            "能力集(Capability)校验",
        ),
        (r"\b(?:SetAccessToken|SetToken|VerifyToken|Authenticate)\b", "会话/Token校验"),
        (r"\b(?:SetAcl|CheckAcl|AccessControl)\b", "安全标签/ACL校验"),
    ]

    has_security_precondition = False
    for pattern, desc in security_precondition_patterns:
        if re.search(pattern, content):
            has_security_precondition = True
            break

    state_init_patterns = [
        r"\bInit\b",
        r"\bInitialize\b",
        r"\bCreate\b",
        r"\bSetUp\b",
        r"\bOpen\b",
        r"\bConnect\b",
    ]
    state_dependent_patterns = [
        r"\bConfigure\b",
        r"\bSetMode\b",
        r"\bSetConfig\b",
    ]

    api_calls = re.findall(r"(?:\w+\s*->\s*|\w+\s*\.\s*|\b)(\w+)\s*\(", content)

    has_init = False
    has_dependent = False
    for call in api_calls:
        for pattern in state_init_patterns:
            if re.match(pattern + r"$", call):
                has_init = True
                break
        for pattern in state_dependent_patterns:
            if re.match(pattern + r"$", call):
                has_dependent = True
                break

    if has_dependent and not has_init and len(api_calls) >= 1:
        if not re.search(
            r"//.*(?:已初始化|initialized|prepared|setup)", content, re.IGNORECASE
        ):
            errors.append(
                "规则011[高危]: 检测到可能调用需要前置初始化的接口(如Configure/SetMode/SetConfig)，但未发现初始化调用。"
                "请检查目标 API 是否需要：1) 系统初始化 2) 权限设置 3) 会话建立 4) 状态准备。"
                "缺少安全准入条件会导致 fuzz 无法触及业务逻辑。"
            )

    if "OnRemoteRequest" in content:
        if not re.search(r"WriteInterfaceToken", content):
            errors.append(
                "规则011[高危]: 测试 OnRemoteRequest 时未调用 WriteInterfaceToken，"
                "可能导致权限校验失败，建议构造完整的 MessageParcel 包括接口 token"
            )

    if has_security_precondition:
        if not re.search(
            r"\bSetPermission\b|\bSetToken\b|\bSetUid\b|\bSetCallerUid\b|\bAuthenticate\b|\bWriteInterfaceToken\b",
            content,
        ):
            errors.append(
                "规则011[高危]: 检测到目标API可能存在安全准入条件校验，但用例中未构造对应的准入条件。"
                "请检查目标API源码中的安全校验逻辑，确保用例构造了满足准入条件的调用上下文。"
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
    
    result = check_security_context(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
