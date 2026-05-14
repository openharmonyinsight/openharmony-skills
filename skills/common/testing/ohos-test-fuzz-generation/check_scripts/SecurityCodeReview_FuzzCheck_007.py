#!/usr/bin/env python3
"""
规则007: 目标API跨进程
检查IPC接口是否通过OnRemoteRequest直接测试stub
"""

import re
import os


def check_ipc_pattern(content):
    """
    规则007: 检查IPC接口是否通过OnRemoteRequest直接测试stub
    跨进程调用无法被fuzz引擎监控，应改为直接调用stub的OnRemoteRequest
    """
    errors = []

    # 已经通过 OnRemoteRequest 测试，不需要报错
    if "OnRemoteRequest" in content:
        return errors

    # 1. 检测通过 Proxy 对象发起 IPC 调用（如 proxy->Method(...)）
    proxy_calls = re.findall(
        r"(\w*[Pp]roxy\w*)\s*->\s*(\w+)\s*\(",
        content,
    )
    for proxy_var, method in proxy_calls:
        # 排除变量名本身就是 proxy 但只是普通变量
        if re.search(rf"\b{re.escape(proxy_var)}\s*=\s*\w+::GetInstance", content):
            errors.append(
                f"规则007[高危]: 通过 Proxy 对象 {proxy_var} 调用 {method}()，"
                f"服务端代码在另一个进程，fuzz 无法监控。建议直接调用 stub 的 OnRemoteRequest"
            )

    # 2. 检测 RemoteObject / IRemoteBroker 相关的跨进程调用
    if re.search(r"sptr<IRemoteObject>", content) or re.search(
        r"RemoteObject", content
    ):
        # 如果有 SendRequest 调用（客户端 IPC），且没有 OnRemoteRequest
        if re.search(r"SendRequest\s*\(", content):
            errors.append(
                "规则007[高危]: 代码使用 SendRequest 发起 IPC 跨进程调用，"
                "fuzz 无法监控服务端逻辑，建议改为直接调用 stub 的 OnRemoteRequest"
            )

    # 3. 检测直接通过 Stub 类名构造但没有调用 OnRemoteRequest
    stub_construct = re.findall(
        r"make_(?:unique|shared)<(\w*Stub\w*)>",
        content,
    )
    for stub_class in stub_construct:
        if not re.search(r"OnRemoteRequest", content):
            errors.append(
                f"规则007[高危]: 构造了 Stub 对象 {stub_class} 但未调用 OnRemoteRequest，"
                f"建议构造 MessageParcel 并调用 stub->OnRemoteRequest(code, data, reply, option)"
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
    
    result = check_ipc_pattern(content)
    if result:
        print(f"Found {len(result)} issues:")
        for issue in result:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("No issues found.")
        sys.exit(0)
