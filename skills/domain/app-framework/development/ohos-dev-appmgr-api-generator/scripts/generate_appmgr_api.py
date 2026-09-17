#!/usr/bin/env python3
"""
Generate complete AppMgr API call chain from Client to Service.

This script generates all the code needed to add a new API to the AppMgr service,
including client, proxy, interface, and service implementations.

Output snippets follow the patterns used in the real ability_runtime codebase:
- AppMgrResultCode is a *client-facing* enum. Over IPC it is transported as
  int32_t: the Client returns AppMgrResultCode (mapping int32_t results to the
  enum), while IAppMgr / Proxy / Service / ServiceInner all return int32_t and
  the Stub writes `reply.WriteInt32(result)`. This mirrors the real
  ClearUpApplicationData path (Client -> AppMgrResultCode, IAppMgr/Proxy/... ->
  int32_t). The generator threads a transport return type through the IPC
  layers automatically.
- Proxy write/send choice depends on the IPC transport return type:
    void            -> PARCEL_UTIL_WRITE_NORET / PARCEL_UTIL_SENDREQ_NORET
    int32_t / int   -> PARCEL_UTIL_WRITE_RET_INT / PARCEL_UTIL_SENDREQ_RET_INT
                       (the macro runs IsForbidStart() + null-safe Remote()
                       internally and returns an int32_t errCode on failure)
    AppMgrResultCode -> transported as int32_t, so it uses the _RET_INT path
    bool / std::string -> explicit data.WriteXxx (type-safe failure return)
                       plus the unified AppMgrProxy::SendRequest wrapper. The
                       _RET_INT macro returns an int32_t that cannot convert to
                       these types (compile error for std::string; negative
                       error code -> true for bool).
- Proxy/Stub validate every parcel read (token, params, reply). A failed read
  returns a type-appropriate error instead of feeding a default value into the
  business layer. sptr parameters are null-guarded before dereference.
- Stub uses the Handle* dispatch pattern (each case delegates to a HandleXxx
  method), matching interfaces/inner_api/app_manager/src/appmgr/app_mgr_stub.cpp.
- Case labels use static_cast<uint32_t>(AppMgrInterfaceCode::xxx).
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Parameter types the generator can auto-marshal. Parcelable (AAFwk::Want,
# Configuration, ...) and std::vector<T> parameters need type-specific
# marshaling the generator does not model; they are rejected at input (and in
# validate_api_info) rather than emitting broken-looking WriteObject/WriteVector
# calls.
SUPPORTED_PARAM_TYPES = {
    "std::string", "const std::string&",
    "int32_t", "int", "pid_t", "uint32_t", "uint64_t", "bool",
}

# Return types the generator supports. AppMgrResultCode is the only enum; over
# IPC it is transported as int32_t (see _transport_return_type).
SUPPORTED_RETURN_TYPES = (
    "void", "int32_t", "int", "AppMgrResultCode", "bool", "std::string",
)

# A bare `sptr<X>` (optionally const-qualified / ref-qualified). The inner type
# is restricted to [^<>]+ so nested templates such as `std::vector<sptr<X>>` or
# `sptr<std::vector<X>>` cannot match — those need manual marshaling. The
# inner is additionally validated by _valid_sptr_inner() to be either
# IRemoteObject or an IRemoteBroker-named interface (IXxx), so sptr<int32_t>,
# sptr< >, sptr<IConfigurationObserver *> are rejected up front.
_SPTR_RE = re.compile(r'^(const\s+)?sptr<([^<>]+)>(\s*&)?$')


def _valid_sptr_inner(inner: str) -> bool:
    """Whether the inner type of a sptr<X> is one the generator can marshal:
    `IRemoteObject` (the object itself, written via GetRefPtr()) or an `IXxx`
    IRemoteBroker-named interface (written via ->AsObject()). Rejects scalars
    (sptr<int32_t> -> int has no AsObject()), pointers/refs/cv/whitespace
    declarators, and empty inner.

    The inner type is split by ``::`` and every segment is checked to be a
    valid C++ identifier and not a C++ keyword, so ``sptr<IObserver::class>``
    is rejected (``class`` is a keyword segment) and
    ``sptr<IConfigurationObserver *>`` is rejected (the ``*`` segment is not an
    identifier). The ``I`` + uppercase-letter broker naming convention is
    applied to the **last** segment only, so namespaced broker interfaces such
    as ``AAFwk::IUserCallback`` and ``OHOS::AAFwk::IUserCallback`` (which
    derive from ``IRemoteBroker`` in the real codebase) are accepted, while
    ``sptr<int32_t>`` (last segment ``int32_t`` does not start with ``I`` +
    uppercase) is rejected. A leading ``::`` (global-namespace qualifier) is
    allowed.
    """
    inner = inner.strip()
    # Allow an optional leading :: (global-namespace qualifier).
    if inner.startswith("::"):
        inner = inner[2:].strip()
    if not inner:
        return False
    segments = [s.strip() for s in inner.split("::")]
    for seg in segments:
        if not seg or not _IDENT_RE.fullmatch(seg):
            return False
        if seg in CPP_KEYWORDS:
            return False
    last = segments[-1]
    if last == "IRemoteObject":
        return True
    # IRemoteBroker interface naming convention: ``I`` + an uppercase letter
    # (e.g. IConfigurationObserver, IUserCallback). Scalar types (int32_t,
    # bool, std::string) do not follow this, so sptr<int32_t> is rejected.
    return len(last) > 1 and last[0] == "I" and last[1].isupper()


# C++17 keywords + alternative tokens that are valid identifiers by character
# shape but must not be used as a method or parameter name (generating
# `virtual int32_t class();` or `void Foo(int return)` fails to compile).
CPP_KEYWORDS = {
    "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor",
    "bool", "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t",
    "class", "compl", "concept", "const", "consteval", "constexpr", "constinit",
    "const_cast", "continue", "co_await", "co_return", "co_yield", "decltype",
    "default", "delete", "do", "double", "dynamic_cast", "else", "enum",
    "explicit", "export", "extern", "false", "float", "for", "friend", "goto",
    "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept",
    "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private",
    "protected", "public", "register", "reinterpret_cast", "requires",
    "return", "short", "signed", "sizeof", "static", "static_assert",
    "static_cast", "struct", "switch", "template", "this", "thread_local",
    "throw", "true", "try", "typedef", "typeid", "typename", "union",
    "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while",
    "xor", "xor_eq",
}

# Valid C++ identifier (methods and parameter names).
_IDENT_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')


def is_supported_param_type(ptype: str) -> bool:
    """Whether the generator can auto-marshal this parameter type.

    Uses a precise anchored regex for sptr rather than the loose `\"sptr<\" in
    ptype` substring test, so a nested `std::vector<sptr<IXxx>>` is no longer
    misclassified as a single broker sptr (which would generate
    `observers->AsObject()` on a `std::vector` and fail to compile). The sptr
    inner is validated by _valid_sptr_inner() to reject `sptr<int32_t>` (whose
    inner `int` has no `AsObject()`), `sptr< >`, and `sptr<IConfigurationObserver *>`.
    """
    ptype = ptype.strip()
    if ptype in SUPPORTED_PARAM_TYPES:
        return True
    # Any vector/map template needs type-specific marshaling the generator does
    # not model; reject up front even if it happens to contain an sptr.
    if "std::vector" in ptype or "std::map" in ptype or "vector<" in ptype:
        return False
    m = _SPTR_RE.match(ptype)
    if not m:
        return False
    return _valid_sptr_inner(m.group(2))


def validate_api_info(api: "ApiInfo") -> None:
    """Validate ApiInfo invariants. Raises ValueError on any violation.

    This is the single source of truth shared by both the interactive entry
    (prompt_user) and the programmatic entry (generate_all), so CLI typos (e.g.
    `std:string`), a C++ keyword as a name (`class`), duplicate parameter
    names, an illegal sptr inner (`sptr<int32_t>`), a non-void return type with
    TF_ASYNC, an unsupported parameter type like `std::vector<sptr<...>>`, or an
    `is_void`/return_type contradiction all fail closed here.
    """

    def _check_ident(name: str, kind: str) -> None:
        if not _IDENT_RE.fullmatch(name):
            raise ValueError(
                f"invalid {kind} name {name!r}: must be a C++ identifier")
        if name in CPP_KEYWORDS:
            raise ValueError(
                f"invalid {kind} name {name!r}: must not be a C++ keyword")

    _check_ident(api.name, "API")
    if api.return_type not in SUPPORTED_RETURN_TYPES:
        raise ValueError(
            f"unsupported return type {api.return_type!r}: must be one of "
            f"{', '.join(SUPPORTED_RETURN_TYPES)}")
    is_void = api.return_type == "void"
    if api.is_void != is_void:
        raise ValueError(
            f"is_void={api.is_void} contradicts return_type="
            f"{api.return_type!r} (is_void must be True iff return_type is "
            "'void')")
    if api.is_async and not is_void:
        raise ValueError(
            "async (TF_ASYNC) IPC has no reply — return type must be void")
    seen_names = set()
    for ptype, pname in api.params:
        _check_ident(pname, "parameter")
        if pname in seen_names:
            raise ValueError(
                f"duplicate parameter name {pname!r}: parameter names must be "
                "unique within an API signature")
        seen_names.add(pname)
        if not is_supported_param_type(ptype):
            raise ValueError(
                f"unsupported parameter type {ptype!r} for parameter "
                f"{pname!r}: only scalar types and sptr<IRemoteObject> / "
                "sptr<IXxx broker> are auto-marshaled. Parcelable "
                "(AAFwk::Want, Configuration), std::vector<T>, and non-broker "
                "sptr (e.g. sptr<int32_t>) need manual marshaling — add them "
                "by hand after generation")


class ApiInfo:
    """Stores information about the API to generate."""

    def __init__(self, name: str, return_type: str, params: List[Tuple[str, str]],
                 is_void: bool = False, is_async: bool = False):
        self.name = name
        self.return_type = return_type
        self.params = params  # List of (type, name) tuples
        self.is_void = is_void
        self.is_async = is_async


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
        self.service_inner_h = project_root / "services/appmgr/include/app_mgr_service_inner.h"
        self.service_inner_cpp = project_root / "services/appmgr/src/app_mgr_service_inner.cpp"
        # NOTE: stub lives under interfaces/, not services/appmgr/src/appmgrstub/.
        self.stub_h = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_stub.h"
        self.stub_cpp = project_root / "interfaces/inner_api/app_manager/src/appmgr/app_mgr_stub.cpp"

    def generate_all(self, api: ApiInfo, ipc_code: int,
                     used_enum_names=None) -> Dict[str, str]:
        """Generate all code modifications.

        Validates ApiInfo invariants first so a programmatic or interactive
        caller cannot bypass the declared capability boundary. Also rejects an
        IPC enum name that already exists in `app_mgr_ipc_interface_code.h`, so
        an existing API (e.g. `ClearUpApplicationData`) does not get a duplicate
        `APP_CLEAR_UP_APPLICATION_DATA` entry that would fail to compile with
        `redeclaration`. When `used_enum_names` is not supplied, the existing
        names are read from the enum file (empty set if the file is not
        readable, e.g. a tempdir project root in tests).
        """
        validate_api_info(api)
        enum_name = self._to_ipc_enum_name(api.name)
        existing = (used_enum_names if used_enum_names is not None
                    else self._read_existing_enum_names())
        if enum_name in existing:
            raise ValueError(
                f"IPC enum name {enum_name!r} already exists in "
                f"{self.ipc_code_h}. Pick a different API name, or extend the "
                "enum by hand if you intend to reuse an existing code.")
        return {
            "client_h": self._generate_client_header(api),
            "client_cpp": self._generate_client_impl(api),
            "ipc_code_h": self._generate_ipc_code(api, ipc_code),
            "proxy_h": self._generate_proxy_header(api),
            "proxy_cpp": self._generate_proxy_impl(api, ipc_code),
            "interface_h": self._generate_interface(api),
            "service_h": self._generate_app_mgr_service_header(api),
            "service_cpp": self._generate_app_mgr_service_impl(api),
            "service_inner_h": self._generate_service_inner_header(api),
            "service_inner_cpp": self._generate_service_inner_impl(api),
            "stub_h": self._generate_stub_header(api),
            "stub_cpp": self._generate_stub_impl(api, ipc_code),
        }

    def _read_existing_enum_names(self) -> set:
        """Names already declared in `app_mgr_ipc_interface_code.h`.

        Delegates to the shared ``_scan_ipc_enum`` so the CLI path
        (``get_next_ipc_code``) and the programmatic path
        (``generate_all``) use the **same** name scanner — no divergent
        name sets depending on the entry point.

        Returns an empty set if the file is not readable (e.g. a tempdir
        project root in tests), so the enum-name conflict check degrades to
        a no-op rather than crashing programmatic callers.
        """
        try:
            _, used_names = _scan_ipc_enum(self.ipc_code_h)
            return used_names
        except OSError:
            return set()

    # ------------------------------------------------------------------
    # Return-type helpers
    # ------------------------------------------------------------------

    def _transport_return_type(self, api: ApiInfo) -> str:
        """Return type used on the IPC transport layers
        (IAppMgr / Proxy / Service / ServiceInner).

        AppMgrResultCode is a client-facing enum; over IPC it is carried as
        int32_t (the real ClearUpApplicationData path: Client returns
        AppMgrResultCode, IAppMgr/Proxy/Service/ServiceInner return int32_t).
        The Client maps the int32_t result back to the enum.
        """
        return "int32_t" if api.return_type == "AppMgrResultCode" else api.return_type

    # ------------------------------------------------------------------
    # Client side (public return type — AppMgrResultCode stays an enum here)
    # ------------------------------------------------------------------

    def _generate_client_header(self, api: ApiInfo) -> str:
        """Generate client header declaration."""
        params_str = self._format_params_declaration(api.params)

        return f'''    /**
     * {api.name}
     */
    virtual {api.return_type} {api.name}({params_str});'''

    def _generate_client_impl(self, api: ApiInfo) -> str:
        """Generate client implementation."""
        params_str = self._format_params_declaration(api.params)
        body = self._get_client_impl_body(api)
        return f'''{api.return_type} AppMgrClient::{api.name}({params_str})
{{
{body}
}}'''

    def _get_client_impl_body(self, api: ApiInfo) -> str:
        """Get client implementation body based on return type."""
        param_names = ", ".join([p[1] for p in api.params])

        if api.is_void:
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return;
    }}
    service->{api.name}({param_names});'''

        if api.return_type == "AppMgrResultCode":
            # Service transports int32_t; the Client maps it to the enum.
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return AppMgrResultCode::ERROR_SERVICE_NOT_CONNECTED;
    }}
    int32_t result = service->{api.name}({param_names});
    if (result != ERR_OK) {{
        return AppMgrResultCode::ERROR_SERVICE_NOT_READY;
    }}
    return AppMgrResultCode::RESULT_OK;'''

        if api.return_type.startswith("int32_t") or api.return_type.startswith("int"):
            return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return AAFwk::ERR_APP_MGR_SERVICE_NOT_CONNECTED;
    }}
    return service->{api.name}({param_names});'''

        # Generic fallback (bool, struct, etc.)
        default_ret = self._get_default_client_return(api.return_type)
        return f'''    sptr<IAppMgr> service = iface_cast<IAppMgr>(mgrHolder_->GetRemoteObject());
    if (service == nullptr) {{
        TAG_LOGE(AAFwkTag::APPMGR, "Service is nullptr.");
        return {default_ret};
    }}
    return service->{api.name}({param_names});'''

    def _get_default_client_return(self, return_type: str) -> str:
        """Default return value when service is unavailable."""
        if return_type == "bool":
            return "false"
        return "{}"

    # ------------------------------------------------------------------
    # IPC interface code enum
    # ------------------------------------------------------------------

    def _generate_ipc_code(self, api: ApiInfo, ipc_code: int) -> str:
        """Generate IPC interface code enum entry."""
        enum_name = self._to_ipc_enum_name(api.name)
        return f"    {enum_name} = {ipc_code},"

    def _to_ipc_enum_name(self, api_name: str) -> str:
        """Convert API name to IPC enum name (APP_UPPER_SNAKE_CASE)."""
        result = re.sub('([A-Z]+)', r'_\1', api_name).upper().lstrip('_')
        return f"APP_{result}" if not result.startswith("APP_") else result

    # ------------------------------------------------------------------
    # Proxy (IPC transport return type)
    # ------------------------------------------------------------------

    def _generate_proxy_header(self, api: ApiInfo) -> str:
        """Generate proxy header declaration. All overrides use `override`."""
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)

        return f'''    /**
     * {api.name}
     */
    {rtype} {api.name}({params_str}) override;'''

    def _generate_proxy_impl(self, api: ApiInfo, ipc_code: int) -> str:
        """Generate proxy implementation."""
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)
        body = self._get_proxy_impl_body(api)
        return f'''{rtype} AppMgrProxy::{api.name}({params_str})
{{
{body}
}}'''

    def _get_proxy_impl_body(self, api: ApiInfo) -> str:
        """Get proxy implementation body.

        Write/send choice depends on the IPC transport return type:
        - void: _NORET macros (no reply, no return value).
        - int32_t/int (and AppMgrResultCode, which transports as int32_t):
          _RET_INT macros. The macro runs IsForbidStart() + null-safe Remote()
          internally and returns an int32_t errCode on failure, which is the
          correct transport return type.
        - bool/std::string: explicit data.WriteXxx for params (type-safe
          failure return) plus the unified AppMgrProxy::SendRequest wrapper
          (the same path the _RET_INT macro uses internally) and a
          type-adapted success return. The _RET_INT macro returns an int32_t
          on failure, which would not compile for std::string and would
          convert negative error codes to true for bool.

        Every read (token, params, reply) is validated; a failed read returns a
        type-appropriate error instead of feeding a default value forward.
        """
        transport = self._transport_return_type(api)
        use_ret_int = (not api.is_void) and transport in ("int32_t", "int")
        writes = self._get_param_writes(api)
        ipc_enum = self._to_ipc_enum_name(api.name)
        option_flag = "TF_ASYNC" if api.is_async else "TF_SYNC"

        # Every proxy method opens with a "called" tag, matching existing code.
        lines = [
            '    TAG_LOGD(AAFwkTag::APPMGR, "called");',
            '    MessageParcel data;',
            '    MessageParcel reply;',
            f'    MessageOption option(MessageOption::{option_flag});',
        ]
        if not api.is_void:
            lines.append(
                '    HITRACE_METER_NAME(HITRACE_TAG_ABILITY_MANAGER, __PRETTY_FUNCTION__);'
            )
        lines.extend([
            '    if (!WriteInterfaceToken(data)) {',
            f'        TAG_LOGE(AAFwkTag::APPMGR, "{api.name} write interface token failed");',
            f'        {self._get_proxy_error_return(api)}',
            '    }',
        ])
        # Parameter writes (may be empty)
        if writes.strip():
            lines.append(writes.rstrip())
        if api.is_void:
            lines.append(
                f'    PARCEL_UTIL_SENDREQ_NORET(AppMgrInterfaceCode::{ipc_enum}, '
                f'data, reply, option);'
            )
        elif use_ret_int:
            lines.append(
                f'    PARCEL_UTIL_SENDREQ_RET_INT(AppMgrInterfaceCode::{ipc_enum}, '
                f'data, reply, option);'
            )
            lines.append(self._get_proxy_normal_return(api))
        else:
            # bool / std::string: call the unified SendRequest wrapper (it runs
            # IsForbidStart() + null-safe Remote() just like the _RET_INT macro)
            # and adapt the int32_t errCode to the function's return type. Do
            # NOT use Remote()->SendRequest() here: that bypasses the policy/null
            # checks and behaves inconsistently with the int32_t/void paths.
            lines.extend([
                f'    int32_t errCode = SendRequest(',
                f'        AppMgrInterfaceCode::{ipc_enum}, data, reply, option);',
                '    if (errCode != ERR_NONE) {',
                f'        TAG_LOGE(AAFwkTag::APPMGR, "{api.name} SendRequest failed");',
                f'        {self._get_proxy_error_return(api)}',
                '    }',
                self._get_proxy_normal_return(api),
            ])
        return "\n".join(lines)

    def _get_param_writes(self, api: ApiInfo) -> str:
        """Generate parameter write block.

        The failure path is chosen per the IPC transport return type:
        - void: PARCEL_UTIL_WRITE_NORET (expands to `return;` — valid in a void fn).
        - int32_t/int (and AppMgrResultCode, transported as int32_t):
          PARCEL_UTIL_WRITE_RET_INT (returns IPC_PROXY_ERR — a valid int).
        - bool/std::string: an explicit `if (!data.WriteXxx(...))` with a
          type-safe failure return. The _NORET write macro's bare `return;`
          is ill-formed in a non-void function, and _RET_INT returns an int
          that cannot convert to these return types.

        sptr parameters (broker interfaces or IRemoteObject) are null-guarded
        before dereference: `name->AsObject()` / `name.GetRefPtr()` on a null
        sptr is undefined behavior.
        """
        lines = [self._get_single_param_write(api, pt, pn) for pt, pn in api.params]
        return "\n".join(lines)

    def _get_single_param_write(self, api: ApiInfo, param_type: str, param_name: str) -> str:
        """Generate write code for a single parameter, with a return-type-aware
        failure path and a null guard for sptr parameters."""
        err_ret = self._get_proxy_error_return(api)
        lines: list[str] = []
        if self._is_sptr(param_type):
            # broker/remote-object params may be null; dereferencing a null sptr
            # (->AsObject() / GetRefPtr()) is UB. Guard before the write.
            lines.append(f'    if (!{param_name}) {{')
            lines.append(f'        TAG_LOGE(AAFwkTag::APPMGR, "{api.name} null {param_name}");')
            lines.append(f'        {err_ret}')
            lines.append('    }')
        # AppMgrResultCode is transported as int32_t, so it shares the macro path.
        use_macro = api.is_void or self._transport_return_type(api) in ("int32_t", "int")
        if use_macro:
            macro = "PARCEL_UTIL_WRITE_RET_INT" if (not api.is_void) else "PARCEL_UTIL_WRITE_NORET"
            tag, arg = self._macro_write_args(param_type, param_name)
            lines.append(f'    {macro}(data, {tag}, {arg});')
        else:
            # bool / std::string: explicit type-safe write.
            method, arg = self._write_call(param_type, param_name)
            lines.append(f'    if (!data.{method}({arg})) {{')
            lines.append(f'        TAG_LOGE(AAFwkTag::APPMGR, "{api.name} write {param_name} failed");')
            lines.append(f'        {err_ret}')
            lines.append('    }')
        return "\n".join(lines)

    def _get_proxy_error_return(self, api: ApiInfo) -> str:
        """Return statement used when WriteInterfaceToken / param write /
        SendRequest / reply-read fails. Uses the IPC transport return type, so
        AppMgrResultCode returns an int32_t error (the Client maps it back)."""
        if api.is_void:
            return "return;"
        if self._transport_return_type(api) in ("int32_t", "int"):
            return "return IPC_PROXY_ERR;"
        if api.return_type == "bool":
            return "return false;"
        if api.return_type == "std::string":
            return 'return "";'
        return "return {};"

    def _get_proxy_normal_return(self, api: ApiInfo) -> str:
        """Validated reply-read block + return statement, used after a
        successful IPC send. A failed reply read returns the type-appropriate
        error instead of forwarding a default (0 / false / \"\") into the
        caller — an empty reply must not be misread as ERR_OK / true / \"\"."""
        err_ret = self._get_proxy_error_return(api)
        log = f'TAG_LOGE(AAFwkTag::APPMGR, "{api.name} read reply failed")'
        transport = self._transport_return_type(api)
        if transport in ("int32_t", "int"):
            return ("    int32_t ret;\n"
                    "    if (!reply.ReadInt32(ret)) {\n"
                    f"        {log};\n"
                    f"        {err_ret}\n"
                    "    }\n"
                    "    return ret;")
        if api.return_type == "bool":
            return ("    bool ret;\n"
                    "    if (!reply.ReadBool(ret)) {\n"
                    f"        {log};\n"
                    f"        {err_ret}\n"
                    "    }\n"
                    "    return ret;")
        if api.return_type == "std::string":
            return ('    std::u16string ret16;\n'
                    '    if (!reply.ReadString16(ret16)) {\n'
                    f"        {log};\n"
                    f"        {err_ret}\n"
                    '    }\n'
                    '    return Str16ToStr8(ret16);')
        return "    return {};"

    # ------------------------------------------------------------------
    # Interface (IAppMgr) — IPC transport return type
    # ------------------------------------------------------------------

    def _generate_interface(self, api: ApiInfo) -> str:
        """Generate IAppMgr interface declaration.

        All virtual methods get a default inline body so derived classes are not
        forced to implement every method (matches the existing interface style).
        """
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)
        if api.is_void:
            return f'''    /**
     * {api.name}
     */
    virtual void {api.name}({params_str}) {{}}'''
        default_ret = self._get_interface_default_return(api.return_type)
        return f'''    /**
     * {api.name}
     */
    virtual {rtype} {api.name}({params_str})
    {{
        return {default_ret};
    }}'''

    def _get_interface_default_return(self, return_type: str) -> str:
        """Default return value used in the interface's inline default body.
        Uses the IPC transport type (int32_t for AppMgrResultCode)."""
        if return_type == "AppMgrResultCode":
            return "0"
        if return_type in ("int32_t", "int"):
            return "0"
        if return_type == "bool":
            return "false"
        if return_type == "std::string":
            return '""'
        return "{}"

    # ------------------------------------------------------------------
    # AppMgrService (delegates to AppMgrServiceInner after a readiness check)
    # ------------------------------------------------------------------

    def _generate_app_mgr_service_header(self, api: ApiInfo) -> str:
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)
        return f'''    /**
     * {api.name}
     */
    {rtype} {api.name}({params_str});'''

    def _generate_app_mgr_service_impl(self, api: ApiInfo) -> str:
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)
        body = self._get_app_mgr_service_impl_body(api)
        return f'''{rtype} AppMgrService::{api.name}({params_str})
{{
{body}
}}'''

    def _get_app_mgr_service_impl_body(self, api: ApiInfo) -> str:
        param_names = ", ".join([p[1] for p in api.params])
        not_ready_ret = self._get_service_not_ready_return(api.return_type)
        head = f'    TAG_LOGD(AAFwkTag::APPMGR, "{api.name} called");'
        ready_check = "    if (!IsReady()) {"
        not_ready_log = f'        TAG_LOGE(AAFwkTag::APPMGR, "{api.name} failed");'
        delegate = f"    return appMgrServiceInner_->" f"{api.name}({param_names});"
        if api.is_void:
            return "\n".join([
                head,
                ready_check,
                not_ready_log,
                "        return;",
                "    }",
                f"    appMgrServiceInner_->{api.name}({param_names});",
            ])
        return "\n".join([
            head,
            ready_check,
            not_ready_log,
            f"        return {not_ready_ret};",
            "    }",
            delegate,
        ])

    def _get_service_not_ready_return(self, return_type: str) -> str:
        """Return value used by AppMgrService when IsReady() is false.
        Uses the IPC transport type (int32_t for AppMgrResultCode)."""
        if return_type == "AppMgrResultCode":
            return "AAFwk::ERR_APP_MGR_SERVICE_NOT_READY"
        if return_type in ("int32_t", "int"):
            return "AAFwk::ERR_APP_MGR_SERVICE_NOT_READY"
        if return_type == "bool":
            return "false"
        if return_type == "std::string":
            return '""'
        return "{}"

    # ------------------------------------------------------------------
    # AppMgrServiceInner
    # ------------------------------------------------------------------

    def _generate_service_inner_header(self, api: ApiInfo) -> str:
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)
        return f'''    /**
     * {api.name}
     */
    {rtype} {api.name}({params_str});'''

    def _generate_service_inner_impl(self, api: ApiInfo) -> str:
        params_str = self._format_params_declaration(api.params)
        rtype = self._transport_return_type(api)
        body = self._get_service_inner_impl_body(api)
        return f'''{rtype} AppMgrServiceInner::{api.name}({params_str})
{{
{body}
}}'''

    def _get_service_inner_impl_body(self, api: ApiInfo) -> str:
        param_names = ", ".join([p[1] for p in api.params])
        suppress = f"    (void){param_names};" if api.params else ""
        head = f'    TAG_LOGD(AAFwkTag::APPMGR, "{api.name} called");'
        if api.is_void:
            lines = [head]
            if suppress:
                lines.append(suppress)
            lines.append(f"    // TODO: implement {api.name}")
            return "\n".join(lines)
        default_ret = self._get_service_inner_default_return(api.return_type)
        lines = [head]
        if suppress:
            lines.append(suppress)
        lines.append(f"    // TODO: implement {api.name}")
        lines.append(f"    return {default_ret};")
        return "\n".join(lines)

    def _get_service_inner_default_return(self, return_type: str) -> str:
        """Uses the IPC transport type (int32_t for AppMgrResultCode)."""
        if return_type == "AppMgrResultCode":
            return "AAFwk::ERR_APP_MGR_SERVICE_NOT_READY"
        if return_type in ("int32_t", "int"):
            return "AAFwk::ERR_APP_MGR_SERVICE_NOT_READY"
        if return_type == "bool":
            return "false"
        if return_type == "std::string":
            return '""'
        return "{}"

    # ------------------------------------------------------------------
    # Stub (Handle* dispatch pattern)
    # ------------------------------------------------------------------

    def _generate_stub_header(self, api: ApiInfo) -> str:
        """Generate stub header declaration for the Handle* method."""
        handle_name = f"Handle{api.name}"
        return f'''    /**
     * {handle_name}
     */
    int32_t {handle_name}(MessageParcel &data, MessageParcel &reply);'''

    def _generate_stub_impl(self, api: ApiInfo, ipc_code: int) -> str:
        """Generate stub code: case label + Handle* method definition.

        The real stub file splits dispatch across OnRemoteRequestInnerN functions.
        Each case delegates to a Handle<ApiName> method. Output two snippets:
          1. case label to insert into the appropriate OnRemoteRequestInnerN switch
          2. Handle<ApiName> method definition to append in the same file

        The Handle<ApiName> declaration for app_mgr_stub.h is generated
        separately by _generate_stub_header().
        """
        ipc_enum = self._to_ipc_enum_name(api.name)
        handle_name = f"Handle{api.name}"
        handle_body = self._get_stub_handle_body(api)

        return f'''// (1) Add this case to the appropriate OnRemoteRequestInnerN switch
//     inside OnRemoteRequestInner() in app_mgr_stub.cpp:
        case static_cast<uint32_t>(AppMgrInterfaceCode::{ipc_enum}):
            return {handle_name}(data, reply);

// (2) Append this Handle* method definition to app_mgr_stub.cpp:
int32_t AppMgrStub::{handle_name}(MessageParcel &data, MessageParcel &reply)
{{
{handle_body}
}}'''

    def _get_stub_handle_body(self, api: ApiInfo) -> str:
        reads = self._get_param_reads(api.params)
        param_names = ", ".join([p[1] for p in api.params])
        if api.is_void:
            lines = [reads] if reads else []
            lines.extend([
                f"    this->{api.name}({param_names});",
                "    return ERR_NONE;",
            ])
            return "\n".join(lines)

        # Choose a result variable name that cannot collide with user-provided
        # parameter names. A leading underscore is reserved for implementation
        # detail in the codebase's naming conventions, so ``_stub_result`` is
        # safe even if the user names a parameter ``result`` or ``_stub_result``
        # is unlikely in practice. If it does collide, fall back to a longer
        # unique name.
        result_var = "_stub_result"
        param_name_set = {p[1] for p in api.params}
        if result_var in param_name_set:
            result_var = "_appmgr_stub_result"
        reply_write = self._get_reply_write(api.return_type, result_var)
        lines = [reads] if reads else []
        lines.extend([
            f"    auto {result_var} = this->{api.name}({param_names});",
            f"    if (!reply.{reply_write}) {{",
            '        TAG_LOGE(AAFwkTag::APPMGR, "Write reply failed.");',
            "        return IPC_STUB_ERR;",
            "    }",
            "    return ERR_NONE;",
        ])
        return "\n".join(lines)

    def _get_param_reads(self, params: List[Tuple[str, str]]) -> str:
        lines = [self._get_single_param_read(pt, pn) for pt, pn in params]
        return "\n".join(lines)

    def _get_single_param_read(self, param_type: str, param_name: str) -> str:
        """Generate a 4-space-indented read+validate block for use inside a
        Handle* method.

        Every read uses the bool-returning `ReadXxx(value)` form and returns
        ERR_INVALID_VALUE on failure, so a truncated/empty request cannot feed
        a default (0 / false / null) into the business layer. sptr results
        (ReadRemoteObject / iface_cast) are null-checked before being passed
        to the service.
        """
        log = f'TAG_LOGE(AAFwkTag::APPMGR, "read {param_name} failed")'
        if param_type in ("std::string", "const std::string&"):
            return (f'    std::u16string {param_name}16;\n'
                    f'    if (!data.ReadString16({param_name}16)) {{\n'
                    f'        {log};\n'
                    f'        return ERR_INVALID_VALUE;\n'
                    f'    }}\n'
                    f'    std::string {param_name} = Str16ToStr8({param_name}16);')
        if param_type in ("int32_t", "int", "pid_t"):
            return (f'    int32_t {param_name};\n'
                    f'    if (!data.ReadInt32({param_name})) {{\n'
                    f'        {log};\n'
                    f'        return ERR_INVALID_VALUE;\n'
                    f'    }}')
        if param_type == "uint32_t":
            return (f'    uint32_t {param_name};\n'
                    f'    if (!data.ReadUint32({param_name})) {{\n'
                    f'        {log};\n'
                    f'        return ERR_INVALID_VALUE;\n'
                    f'    }}')
        if param_type == "uint64_t":
            return (f'    uint64_t {param_name};\n'
                    f'    if (!data.ReadUint64({param_name})) {{\n'
                    f'        {log};\n'
                    f'        return ERR_INVALID_VALUE;\n'
                    f'    }}')
        if param_type == "bool":
            return (f'    bool {param_name};\n'
                    f'    if (!data.ReadBool({param_name})) {{\n'
                    f'        {log};\n'
                    f'        return ERR_INVALID_VALUE;\n'
                    f'    }}')
        if self._is_sptr(param_type):
            inner = self._sptr_inner_type(param_type)
            # IRemoteObject is the object itself; broker interfaces (IXxx
            # derived from IRemoteBroker) must be re-cast from the object.
            if self._inner_is_remote_object(inner):
                return (f'    sptr<IRemoteObject> {param_name} = data.ReadRemoteObject();\n'
                        f'    if (!{param_name}) {{\n'
                        f'        {log};\n'
                        f'        return ERR_INVALID_VALUE;\n'
                        f'    }}')
            return (f'    sptr<{inner}> {param_name} = '
                    f'iface_cast<{inner}>(data.ReadRemoteObject());\n'
                    f'    if (!{param_name}) {{\n'
                    f'        {log};\n'
                    f'        return ERR_INVALID_VALUE;\n'
                    f'    }}')
        raise ValueError(
            f"unsupported parameter type for stub read: {param_type!r}. "
            "Parcelable and std::vector parameters need manual marshaling."
        )

    def _get_reply_write(self, return_type: str, var_name: str = "result") -> str:
        # AppMgrResultCode is transported as int32_t, so the variable is already
        # an int32_t — no enum cast needed.
        if return_type == "AppMgrResultCode":
            return f"WriteInt32({var_name})"
        if return_type in ("int32_t", "int"):
            return f"WriteInt32({var_name})"
        if return_type == "bool":
            return f"WriteBool({var_name})"
        if return_type == "std::string":
            return f"WriteString16(Str8ToStr16({var_name}))"
        return "WriteInt32(0)"

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _is_sptr(self, param_type: str) -> bool:
        """Precise match against a bare sptr<X> shape (rejects nested
        templates like std::vector<sptr<X>>)."""
        return bool(_SPTR_RE.match(param_type.strip()))

    def _sptr_inner_type(self, param_type: str) -> str:
        """Extract the inner type from 'const sptr<X>&' / 'sptr<X>' etc.
        Uses the anchored _SPTR_RE so a nested vector can never be parsed as a
        single broker sptr."""
        m = _SPTR_RE.match(param_type.strip())
        return m.group(2).strip() if m else ""

    @staticmethod
    def _inner_is_remote_object(inner: str) -> bool:
        """Whether the inner type of a sptr is IRemoteObject, accepting
        namespaced/qualified forms (``OHOS::IRemoteObject``,
        ``::IRemoteObject``) by checking the **last** segment — consistent
        with ``_valid_sptr_inner`` which also checks the last segment for the
        ``IRemoteObject`` special case."""
        inner = inner.strip()
        if inner.startswith("::"):
            inner = inner[2:].strip()
        segments = [s.strip() for s in inner.split("::")]
        return bool(segments) and segments[-1] == "IRemoteObject"

    def _sptr_accessor(self, param_type: str, param_name: str) -> str:
        """Right-hand side for writing a sptr parameter to a parcel.

        - `sptr<IRemoteObject>` (including namespaced forms like
          `sptr<OHOS::IRemoteObject>` or `sptr<::IRemoteObject>`): the object
          itself — use `.GetRefPtr()`.
        - `sptr<IXxx>` where IXxx derives from IRemoteBroker (e.g.
          IConfigurationObserver, IApplicationStateObserver): write the
          underlying IRemoteObject via `->AsObject()`. GetRefPtr() would yield
          the interface pointer, not the IRemoteObject WriteRemoteObject expects.

        Callers null-guard `param_name` before evaluating this accessor.
        """
        inner = self._sptr_inner_type(param_type)
        if self._inner_is_remote_object(inner):
            return f"{param_name}.GetRefPtr()"
        return f"{param_name}->AsObject()"

    def _write_call(self, param_type: str, param_name: str) -> Tuple[str, str]:
        """Return (Write method name, argument expr) for an explicit data.WriteXxx(arg)."""
        if self._is_sptr(param_type):
            return ("WriteRemoteObject", self._sptr_accessor(param_type, param_name))
        if param_type in ("std::string", "const std::string&"):
            return ("WriteString16", f"Str8ToStr16({param_name})")
        if param_type in ("int32_t", "int", "pid_t"):
            return ("WriteInt32", param_name)
        if param_type == "uint32_t":
            return ("WriteUint32", param_name)
        if param_type == "uint64_t":
            return ("WriteUint64", param_name)
        if param_type == "bool":
            return ("WriteBool", param_name)
        raise ValueError(
            f"unsupported parameter type for write: {param_type!r}. "
            "Parcelable and std::vector parameters need manual marshaling."
        )

    def _macro_write_args(self, param_type: str, param_name: str) -> Tuple[str, str]:
        """Return (type-tag, argument) for PARCEL_UTIL_WRITE_*(data, TAG, arg)."""
        if self._is_sptr(param_type):
            return ("RemoteObject", self._sptr_accessor(param_type, param_name))
        if param_type in ("std::string", "const std::string&"):
            return ("String16", f"Str8ToStr16({param_name})")
        if param_type in ("int32_t", "int", "pid_t"):
            return ("Int32", param_name)
        if param_type == "uint32_t":
            return ("Uint32", param_name)
        if param_type == "uint64_t":
            return ("Uint64", param_name)
        if param_type == "bool":
            return ("Bool", param_name)
        raise ValueError(
            f"unsupported parameter type for write: {param_type!r}. "
            "Parcelable and std::vector parameters need manual marshaling."
        )

    def _format_params_declaration(self, params: List[Tuple[str, str]]) -> str:
        if not params:
            return ""
        return ", ".join([f"{ptype} {pname}" for ptype, pname in params])


def _scan_ipc_enum(ipc_file: Path) -> Tuple[set, set]:
    """Single source of truth for scanning ``AppMgrInterfaceCode`` enum entries.

    Parses the enum body once and returns ``(used_codes, used_names)``:

    - ``used_codes``: ``int`` values parsed from numeric-literal assignments
      (decimal or hex) **and** from simple constant expressions (e.g.
      ``1 << 2``, ``0xFF | 0x10``) restricted to digits and bitwise/arithmetic
      operators. Entries whose value cannot be evaluated (e.g. references to
      other enum members) are skipped.
    - ``used_names``: **all** enumerator names — explicit (``NAME = value``)
      and implicit (``NAME,``) — regardless of the value form, so an enum-name
      conflict is detected even when the existing entry uses an expression
      value or has no value at all.

    Both ``get_next_ipc_code`` (CLI path) and ``_read_existing_enum_names``
    (programmatic path inside ``generate_all``) delegate here, so the CLI and
    the generator never see divergent name sets.

    Raises ``OSError`` if ``ipc_file`` cannot be read; callers decide how to
    handle that (``_read_existing_enum_names`` swallows it, ``get_next_ipc_code``
    lets it propagate to ``main``).
    """
    content = ipc_file.read_text(encoding="utf-8")
    # Strip /* */ block comments so numbers/names inside comments are not counted.
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Strip line comments.
    content = re.sub(r'//[^\n]*', '', content)

    # Extract the enum body: ``enum [class] Name [: type] { ... }``.
    m = re.search(r'enum(?:\s+class)?\s+\w+\s*(?::[^{]+)?\{([^}]*)\}', content)
    if not m:
        return set(), set()
    body = m.group(1)

    used_codes: set = set()
    used_names: set = set()
    for entry in body.split(','):
        entry = entry.strip()
        if not entry:
            continue
        # Each entry is either ``NAME`` (implicit value) or ``NAME = value``.
        em = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(?:=\s*(.+?))?$', entry)
        if not em:
            continue
        name = em.group(1)
        used_names.add(name)
        raw_value = (em.group(2) or '').strip()
        if raw_value:
            # Try plain numeric literals first (decimal or hex).
            try:
                used_codes.add(int(raw_value, 0))
                continue
            except ValueError:
                pass
            # Try evaluating simple constant expressions involving integers
            # and bitwise/arithmetic operators (e.g. ``1 << 2``, ``0xFF | 0x10``).
            # This is restricted to a safe subset — no names, no calls — so
            # expression-valued enum entries contribute their actual code value
            # to the used_codes set, preventing the next-free-code picker from
            # recommending an already-occupied value.
            if re.fullmatch(r'[\d\s+\-*/%&|^~()<>]+', raw_value):
                try:
                    used_codes.add(int(eval(raw_value, {"__builtins__": {}}, {})))
                except Exception:
                    pass
    return used_codes, used_names


def get_next_ipc_code(project_root: Path) -> Tuple[int, set]:
    """Get the next available IPC interface code by scanning existing enum
    values.

    Returns ``(next_free_code, used_enum_names)`` so the caller can also
    detect an enum-name conflict before generating (an existing API must not
    get a duplicate ``APP_...`` entry that fails with ``redeclaration``).

    Delegates to ``_scan_ipc_enum`` — the same scanner used by
    ``_read_existing_enum_names`` inside ``generate_all`` — so the CLI path
    and the programmatic path never diverge on which enum names are
    considered ``existing``.
    """
    ipc_file = project_root / "interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h"
    used_codes, used_names = _scan_ipc_enum(ipc_file)

    if not used_codes:
        # The file exists but no enum values were parsed: the format may have
        # changed. Fail closed instead of returning a fixed value (125 is
        # already occupied by MAKE_IMAGE in the current enum).
        print(f"Error: could not parse any AppMgrInterfaceCode values from {ipc_file}. "
              "The file format may have changed — inspect it manually before adding a new code.")
        sys.exit(1)

    # Pick the smallest free value above the current maximum so newly suggested
    # codes never collide with an already-occupied one.
    candidate = max(used_codes) + 1
    while candidate in used_codes:
        candidate += 1
    return candidate, used_names


def prompt_user() -> ApiInfo:
    """Prompt user for API information."""
    print("\n=== AppMgr API Generator ===\n")

    name = input("API name (camelCase, e.g. GetConfiguration): ").strip()
    return_type = input("Return type (AppMgrResultCode | int32_t | void | bool | std::string): ").strip()

    is_void = return_type.lower() == "void"
    is_async = input("Async IPC (TF_ASYNC)? (y/n): ").strip().lower() == 'y'

    # Async (one-way) IPC has no reply to read, so the method must be void.
    # Non-void + TF_ASYNC would generate contradictory code (reads a reply
    # that never arrives).
    if is_async and not is_void:
        print("Note: async IPC (TF_ASYNC) requires void return type — "
              "forcing return type to void.")
        return_type = "void"
        is_void = True

    print("\nEnter parameters, one per line, format: <type> <name>")
    print("Examples:  'const std::string& bundleName'  |  'int32_t pid'  |  'const sptr<IConfigurationObserver>& observer'")
    print("Empty line to finish.")
    params = []
    while True:
        raw = input(f"param{len(params) + 1}> ").strip()
        if not raw:
            break
        parts = raw.split()
        if len(parts) < 2:
            # Fail closed: a malformed parameter (fewer than 2 words) must
            # not be silently dropped so the run completes with a different
            # signature (R5-F1). Abort so the user fixes the input and
            # re-runs.
            print("Error: format is '<type> <name>'. Example: 'const std::string& bundleName'")
            print("Aborting: the request signature must not be silently changed. "
                  "Re-run with a correctly formatted parameter.")
            sys.exit(1)
        ptype = " ".join(parts[:-1])
        pname = parts[-1]
        if not is_supported_param_type(ptype):
            # Fail closed: silently dropping the requested parameter would make
            # the generated signature diverge from what the user asked for
            # (R4-F1). Abort the run so the user fixes the input and re-runs.
            print(f"Error: parameter type '{ptype}' is not auto-generated. "
                  "Parcelable (e.g. AAFwk::Want), std::vector<T>, and non-broker "
                  "sptr (e.g. sptr<int32_t>) require manual parcel marshaling — "
                  "add them by hand after generation. Aborting: the request "
                  "signature must not be silently changed. Re-run with a "
                  "supported type.")
            sys.exit(1)
        params.append((ptype, pname))

    api = ApiInfo(name, return_type, params, is_void, is_async)
    # Re-validate so an invalid interactive input (e.g. a typo'd return type)
    # is rejected here with a clear message rather than later in generate_all.
    try:
        validate_api_info(api)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    return api


def _validate_project_structure(project_root: Path) -> None:
    """Validate that project_root looks like the ability_runtime tree by
    checking the IPC enum file and the 12 target files. Fail before any
    interactive input so a wrong directory (e.g. `/tmp`) does not waste a full
    prompt cycle and then crash with an uncaught traceback (R4-F6).
    """
    gen = AppMgrApiGenerator(project_root)
    required = [
        gen.ipc_code_h, gen.client_h, gen.client_cpp, gen.proxy_h,
        gen.proxy_cpp, gen.interface_h, gen.service_h, gen.service_cpp,
        gen.service_inner_h, gen.service_inner_cpp, gen.stub_h, gen.stub_cpp,
    ]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        print(f"Error: {project_root} does not look like an ability_runtime "
              "project root. Missing required files:")
        for path in missing:
            print(f"  - {path}")
        print("Pass the ability_runtime project root (the repo containing "
              "interfaces/inner_api/app_manager/ and services/appmgr/).")
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_appmgr_api.py <project_root>")
        sys.exit(1)

    project_root = Path(sys.argv[1])
    if not project_root.is_dir():
        print(f"Error: Project root not found: {project_root}")
        sys.exit(1)

    # Validate the project structure before collecting interactive input so a
    # wrong directory fails fast with a stable diagnostic instead of an
    # uncaught FileNotFoundError after a full prompt cycle.
    _validate_project_structure(project_root)

    api = prompt_user()
    try:
        ipc_code, used_enum_names = get_next_ipc_code(project_root)
    except OSError as e:
        print(f"Error: cannot read IPC enum file: {e}")
        sys.exit(1)

    generator = AppMgrApiGenerator(project_root)
    try:
        code_blocks = generator.generate_all(api, ipc_code, used_enum_names)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\nNext IPC code: {ipc_code}\n")
    print("=== Generated Code ===\n")
    for file_name, code in code_blocks.items():
        print(f"--- {file_name} ---")
        print(code)
        print()


if __name__ == "__main__":
    main()
