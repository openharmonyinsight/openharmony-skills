#!/usr/bin/env python3
"""
Generate complete AppMgr API call chain from Client to Service.

This script generates all the code needed to add a new API to the AppMgr service,
including client, proxy, interface, and service implementations.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ApiInfo:
    """Stores information about the API to generate."""

    def __init__(self, name: str, return_type: str, params: List[Tuple[str, str]],
                 is_void: bool = False, is_const: bool = False):
        self.name = name
        self.return_type = return_type
        self.params = params  # List of (type, name) tuples
        self.is_void = is_void
        self.is_const = is_const


class AppMgrApiGenerator:
    """Generates the complete call chain for AppMgr APIs."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.client_h = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_client.h"
        self.client_cpp = project_root / "interfaces/inner_api/app_manager/src/appmgr/app_mgr_client.cpp"
        self.ipc_code_h = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h"
        self.proxy_h = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_proxy.h"
        self.proxy_cpp = project_root / "interfaces/inner_api/app_manager/src/appmgr/app_mgr_proxy.cpp"
        self.interface_h = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_interface.h"
        self.service_h = project_root / "services/appmgr/include/app_mgr_service.h"
        self.service_cpp = project_root / "services/appmgr/src/app_mgr_service.cpp"
        self.service_inner_h = project_root / "services/appmgr/src/app_mgr_service_inner.h"
        self.service_inner_cpp = project_root / "services/appmgr/src/app_mgr_service_inner.cpp"
        self.stub_cpp = project_root / "services/appmgr/src/appmgrstub/app_mgr_stub.cpp"

    def generate_all(self, api: ApiInfo, ipc_code: int) -> Dict[str, str]:
        """Generate all code modifications."""
        return {
            "client_h": self._generate_client_header(api),
            "client_cpp": self._generate_client_impl(api),
            "ipc_code_h": self._generate_ipc_code(api, ipc_code),
            "proxy_h": self._generate_proxy_header(api),
            "proxy_cpp": self._generate_proxy_impl(api, ipc_code),
            "interface_h": self._generate_interface(api),
            "service_h": self._generate_app_mgr_service_header(api),
            "service_cpp": self._generate_app_mgr_service_impl(api),
            "service_inner_h": self._generate_service_header(api),
            "service_inner_cpp": self._generate_service_impl(api),
            "stub_cpp": self._generate_stub_impl(api, ipc_code),
        }

    def _generate_client_header(self, api: ApiInfo) -> str:
        """Generate client header declaration."""
        params_str = self._format_params_declaration(api.params)
        const_str = " const" if api.is_const else ""

        return f'''    /**
     * {api.name} - {api.return_type}
     */
    virtual {api.return_type} {api.name}({params_str}){const_str};'''

    def _generate_client_impl(self, api: ApiInfo) -> str:
        """Generate client implementation."""
        params_str = self._format_params_call(api.params)
        param_names = [p[1] for p in api.params]
        param_names_str = ", ".join(param_names)

        return f'''{api.return_type} AppMgrClient::{api.name}({params_str})
{{{self._get_client_impl_body(api, param_names_str)}}}'''

    def _get_client_impl_body(self, api: ApiInfo, param_names: str) -> str:
        """Get client implementation body based on return type and existing patterns."""
        if api.is_void:
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service != nullptr) {{
        service->{api.name}({param_names});
    }}'''
        elif api.return_type == "AppMgrResultCode":
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service != nullptr) {{
        int32_t result = service->{api.name}({param_names});
        if (result == ERR_OK) {{
            return AppMgrResultCode::RESULT_OK;
        }}
        return AppMgrResultCode::ERROR_SERVICE_NOT_READY;
    }}
    return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;'''
        elif api.return_type.startswith("int32_t") or api.return_type.startswith("int"):
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;
    }}
    return service->{api.name}({param_names});'''
        else:
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        {self._get_default_return(api.return_type)}
    }}
    return service->{api.name}({param_names});'''

    def _get_default_return(self, return_type: str) -> str:
        """Get default return value for a type."""
        if return_type == "bool":
            return "return false;"
        return "return {};"

    def _generate_app_mgr_service_header(self, api: ApiInfo) -> str:
        """Generate AppMgrService header file declaration."""
        params_str = self._format_params_declaration(api.params)
        const_str = " const" if api.is_const else ""

        return f'''    /**
     * {api.name}
     */
    {api.return_type} {api.name}({params_str}){const_str};'''

    def _generate_app_mgr_service_impl(self, api: ApiInfo) -> str:
        """Generate AppMgrService implementation."""
        params_str = self._format_params_declaration(api.params)
        param_names = ", ".join([p[1] for p in api.params])

        return f'''{api.return_type} AppMgrService::{api.name}({params_str})
{{{self._get_app_mgr_service_impl_body(api, param_names)}}}'''

    def _get_app_mgr_service_impl_body(self, api: ApiInfo, param_names: str) -> str:
        """Get AppMgrService implementation body."""
        if api.is_void:
            return f'''    TAG_LOGD(AAFwkTag::APPMGR, "call");
    if (!IsReady()) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service not ready");
        return;
    }}
    appMgrServiceInner_->{api.name}({param_names});'''
        else:
            return f'''    TAG_LOGD(AAFwkTag::APPMGR, "call");
    if (!IsReady()) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service not ready");
        return AAFwk::ERR_APP_MGR_SERVICE_NOT_READY;
    }}
    return appMgrServiceInner_->{api.name}({param_names});'''

    def _generate_ipc_code(self, api: ApiInfo, ipc_code: int) -> str:
        """Generate IPC interface code enum entry."""
        enum_name = self._to_ipc_enum_name(api.name)
        return f"    {enum_name} = {ipc_code},"

    def _to_ipc_enum_name(self, api_name: str) -> str:
        """Convert API name to IPC enum name (Pascal case with underscores)."""
        # Convert camelCase to UPPER_SNAKE_CASE
        result = re.sub('([A-Z]+)', r'_\1', api_name).upper().lstrip('_')
        return f"APP_{result}" if not result.startswith("APP_") else result

    def _generate_proxy_header(self, api: ApiInfo) -> str:
        """Generate proxy header declaration."""
        params_str = self._format_params_declaration(api.params)
        const_str = " const" if api.is_const else ""
        override_str = " override" if not api.is_void else ""

        return f'''    /**
     * {api.name}
     */
    {api.return_type} {api.name}({params_str}){const_str}{override_str};'''

    def _generate_proxy_impl(self, api: ApiInfo, ipc_code: int) -> str:
        """Generate proxy implementation."""
        params_str = self._format_params_declaration(api.params)
        param_names = [p[1] for p in api.params]
        ipc_enum = self._to_ipc_enum_name(api.name)

        return f'''{api.return_type} AppMgrProxy::{api.name}({params_str})
{{{self._get_proxy_impl_body(api, ipc_enum)}}}'''

    def _get_proxy_impl_body(self, api: ApiInfo, ipc_enum: str) -> str:
        """Get proxy implementation body."""
        writes = self._get_param_writes(api.params)
        return_type_handling = self._get_return_handling(api)

        hitrace_line = ""
        if not api.is_void:
            hitrace_line = '    HITRACE_METER_NAME(HITRACE_TAG_ABILITY_MANAGER, __PRETTY_FUNCTION__);\n'

        return f'''    MessageParcel data;
    MessageParcel reply;
    MessageOption option(MessageOption::TF_SYNC);
{hitrace_line}    if (!WriteInterfaceToken(data)) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Write interface token failed");
{return_type_handling["error_return"]}
    }}
{writes}    PARCEL_UTIL_SENDREQ_RET_INT(AppMgrInterfaceCode::{ipc_enum}, data, reply, option);
{return_type_handling["normal_return"]}'''

    def _get_param_writes(self, params: List[Tuple[str, str]]) -> str:
        """Generate parameter write code."""
        writes = []
        for param_type, param_name in params:
            write = self._get_single_param_write(param_type, param_name)
            writes.append(write)
        return "\n".join(writes)

    def _get_single_param_write(self, param_type: str, param_name: str) -> str:
        """Generate write code for a single parameter."""
        if "sptr<" in param_type or "sptr<" in param_type:
            return f'    PARCEL_UTIL_WRITE_RET_INT(data, RemoteObject, {param_name}.GetRefPtr());'
        elif param_type == "std::string" or param_type == "const std::string&":
            return f'    PARCEL_UTIL_WRITE_RET_INT(data, String16, Str8ToStr16({param_name}));'
        elif param_type in ["int32_t", "int", "bool", "pid_t", "uint32_t"]:
            ptype = "Int32" if param_type in ["int32_t", "pid_t", "uint32_t"] else param_type.capitalize()
            ptype = "Int32" if ptype == "Uint32" else ptype
            ptype = "Int32" if ptype == "Pid_t" else ptype
            return f'    PARCEL_UTIL_WRITE_RET_INT(data, {ptype}, {param_name});'
        elif "vector<" in param_type:
            return f'    PARCEL_UTIL_WRITE_RET_INT(data, Vector, {param_name});'
        else:
            return f'    PARCEL_UTIL_WRITE_RET_INT(data, Object, {param_name});'

    def _get_return_handling(self, api: ApiInfo) -> Dict[str, str]:
        """Get return type handling code."""
        if api.is_void:
            return {
                "error_return": "return;",
                "normal_return": "    return;"
            }
        elif api.return_type == "AppMgrResultCode":
            return {
                "error_return": "return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;",
                "normal_return": "    return static_cast<AppMgrResultCode>(reply.ReadInt32());"
            }
        elif api.return_type in ["int32_t", "int"]:
            return {
                "error_return": "return ERR_NULL_OBJECT;",
                "normal_return": "    return reply.ReadInt32();"
            }
        elif api.return_type == "bool":
            return {
                "error_return": "return false;",
                "normal_return": "    return reply.ReadBool();"
            }
        elif api.return_type == "std::string":
            return {
                "error_return": 'return "";',
                "normal_return": "    return Str16ToStr8(reply.ReadString16());"
            }
        else:
            return {
                "error_return": "return {};",
                "normal_return": "    return {};"
            }

    def _generate_interface(self, api: ApiInfo) -> str:
        """Generate IAppMgr interface declaration."""
        params_str = self._format_params_declaration(api.params)
        const_str = " const" if api.is_const else ""

        default_impl = ""
        if api.return_type != "void" and not api.return_type.startswith("AppMgrResultCode"):
            default_impl = "\n    {\n        return 0;\n    }"

        return f'''    /**
     * {api.name}
     */
    virtual {api.return_type} {api.name}({params_str}){const_str}{default_impl}'''

    def _generate_service_header(self, api: ApiInfo) -> str:
        """Generate service header declaration."""
        params_str = self._format_params_declaration(api.params)
        const_str = " const" if api.is_const else ""

        return f'''    /**
     * {api.name}
     */
    {api.return_type} {api.name}({params_str}){const_str};'''

    def _generate_service_impl(self, api: ApiInfo) -> str:
        """Generate service implementation."""
        params_str = self._format_params_declaration(api.params)
        param_names = ", ".join([p[1] for p in api.params])

        return f'''{api.return_type} AppMgrServiceInner::{api.name}({params_str})
{{{self._get_service_impl_body(api, param_names)}}}'''

    def _get_service_impl_body(self, api: ApiInfo, param_names: str) -> str:
        """Get service implementation body."""
        if api.is_void:
            return f'''    TAG_LOGD(AAFwkTag::APPMGR, "called");
    // TODO: Implement {api.name}
    (void){param_names};'''
        else:
            return f'''    TAG_LOGD(AAFwkTag::APPMGR, "called");
    // TODO: Implement {api.name}
    (void){param_names};
    return {self._get_default_service_return(api.return_type)};'''

    def _get_default_service_return(self, return_type: str) -> str:
        """Get default return value for service."""
        if return_type == "AppMgrResultCode":
            return "AppMgrResultCode::ERROR_SERVICE_NOT_READY"
        elif return_type in ["int32_t", "int"]:
            return "ERR_NULL_OBJECT"
        elif return_type == "bool":
            return "false"
        elif return_type == "std::string":
            return '""'
        return "{}"

    def _generate_stub_impl(self, api: ApiInfo, ipc_code: int) -> str:
        """Generate stub implementation (IPC handler on service side)."""
        ipc_enum = self._to_ipc_enum_name(api.name)
        case_body = self._get_stub_case_body(api)

        return f'''    case AppMgrInterfaceCode::{ipc_enum}:
{{{case_body}
        break;}}'''

    def _get_stub_case_body(self, api: ApiInfo) -> str:
        """Get stub case body for IPC handling."""
        reads = self._get_param_reads(api.params)
        return_handling = self._get_stub_return_handling(api)

        return f'''{reads}{return_handling}'''

    def _get_param_reads(self, params: List[Tuple[str, str]]) -> str:
        """Generate parameter read code."""
        reads = []
        for param_type, param_name in params:
            read = self._get_single_param_read(param_type, param_name)
            reads.append(read)
        return "\n".join(reads)

    def _get_single_param_read(self, param_type: str, param_name: str) -> str:
        """Generate read code for a single parameter."""
        if param_type == "std::string" or param_type == "const std::string&":
            return f'        std::string {param_name} = Str16ToStr8(data.ReadString16());'
        elif param_type in ["int32_t", "int"]:
            return f'        int32_t {param_name} = data.ReadInt32();'
        elif param_type == "bool":
            return f'        bool {param_name} = data.ReadBool();'
        elif param_type == "pid_t":
            return f'        pid_t {param_name} = data.ReadInt32();'
        elif param_type == "uint32_t":
            return f'        uint32_t {param_name} = data.ReadUint32();'
        elif "sptr<" in param_type:
            inner_type = param_type.replace("sptr<", "").replace(">", "").replace("const ", "")
            return f'        sptr<{inner_type}> {param_name} = iface_cast<{inner_type}>(data.ReadRemoteObject());'
        elif "vector<" in param_type:
            inner = param_type.replace("std::vector<", "").replace(">", "")
            return f'        std::vector<{inner}> {param_name};'
            # Note: Vector reading requires more complex code
        else:
            return f'        {param_type} {param_name} = {{}};'

    def _get_stub_return_handling(self, api: ApiInfo) -> str:
        """Get return handling in stub."""
        if api.is_void:
            param_names = ", ".join([p[1] for p in api.params])
            return f'''        {self._get_stub_class_name()}->{api.name}({param_names});
        return ERR_NONE;'''
        else:
            param_names = ", ".join([p[1] for p in api.params])
            reply = self._get_reply_write(api.return_type)
            return f'''        auto result = {self._get_stub_class_name()}->{api.name}({param_names});
        if (!reply.{reply}) {{
            TAG_LOGE(AAFwkTag::APPMGR, "Write result error.");
            return IPC_STUB_ERR;
        }}
        return ERR_NONE;'''

    def _get_stub_class_name(self) -> str:
        """Get class name used in stub."""
        return "this"

    def _get_reply_write(self, return_type: str) -> str:
        """Get reply write code."""
        if return_type == "AppMgrResultCode":
            return "WriteInt32(static_cast<int32_t>(result))"
        elif return_type in ["int32_t", "int"]:
            return "WriteInt32(result)"
        elif return_type == "bool":
            return "WriteBool(result)"
        elif return_type == "std::string":
            return "WriteString16(Str8ToStr16(result))"
        else:
            return "WriteInt32(0)"

    def _format_params_declaration(self, params: List[Tuple[str, str]]) -> str:
        """Format parameters for function declaration."""
        if not params:
            return ""
        return ", ".join([f"{ptype} {pname}" for ptype, pname in params])

    def _format_params_call(self, params: List[Tuple[str, str]]) -> str:
        """Format parameters for function call."""
        if not params:
            return ""
        return ", ".join([f"{ptype} {pname}" for ptype, pname in params])


def get_next_ipc_code(project_root: Path) -> int:
    """Get the next available IPC interface code."""
    ipc_file = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h"
    content = ipc_file.read_text()

    # Find all numeric values in enum
    pattern = r'=\s*(\d+)'
    codes = re.findall(pattern, content)

    if codes:
        return max(map(int, codes)) + 1
    return 125  # Default next code


def prompt_user() -> ApiInfo:
    """Prompt user for API information."""
    print("\n=== AppMgr API Generator ===\n")

    name = input("API name (camelCase): ").strip()
    return_type = input("Return type (e.g., AppMgrResultCode, int32_t, void): ").strip()

    is_void = return_type == "void"
    is_const = input("Is const method? (y/n): ").strip().lower() == 'y'

    print("\nEnter parameters (one per line, format: type name). Empty line to finish:")
    params = []
    while True:
        param = input(f"param{len(params) + 1}> ").strip()
        if not param:
            break
        parts = param.split()
        if len(parts) >= 2:
            ptype = " ".join(parts[:-1])
            pname = parts[-1]
            params.append((ptype, pname))

    return ApiInfo(name, return_type, params, is_void, is_const)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_appmgr_api.py <project_root>")
        sys.exit(1)

    project_root = Path(sys.argv[1])
    if not project_root.exists():
        print(f"Error: Project root not found: {project_root}")
        sys.exit(1)

    api = prompt_user()
    ipc_code = get_next_ipc_code(project_root)

    generator = AppMgrApiGenerator(project_root)
    code_blocks = generator.generate_all(api, ipc_code)

    print("\n=== Generated Code ===\n")
    for file_name, code in code_blocks.items():
        print(f"--- {file_name} ---")
        print(code)
        print()


if __name__ == "__main__":
    main()
