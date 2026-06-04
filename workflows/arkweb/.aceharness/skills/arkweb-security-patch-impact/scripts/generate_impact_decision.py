#!/usr/bin/env python3
"""Generate 03_impact_decision artifacts from 01/02 archive outputs."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from archive_paths import validate_project_output_root


def first_issue(path: Path) -> dict:
    meta = json.loads(path.read_text(encoding="utf-8"))
    issues = meta.get("issues") if isinstance(meta, dict) else None
    return issues[0] if isinstance(issues, list) and issues else meta


def load_feature_lines(path: Path | None) -> list[str]:
    if path and path.is_file():
        return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return []


def current_chromium_version(project_root: Path) -> dict:
    version_path = project_root / "src/chrome/VERSION"
    version = {"milestone": "unknown", "full": "unknown"}
    if not version_path.is_file():
        return version
    entries: dict[str, str] = {}
    for line in version_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            entries[key.strip()] = value.strip()
    major = entries.get("MAJOR", "unknown")
    if major != "unknown":
        version["milestone"] = major
        version["full"] = ".".join(
            [
                entries.get("MAJOR", "0"),
                entries.get("MINOR", "0"),
                entries.get("BUILD", "0"),
                entries.get("PATCH", "0"),
            ]
        )
    return version


def current_build_config(project_root: Path) -> dict:
    args_path = project_root / "src/out/rk3568_64/args.gn"
    config = {"target_os": "unknown", "target_cpu": "unknown"}
    if not args_path.is_file():
        return config
    for line in args_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("target_os ="):
            config["target_os"] = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("target_cpu ="):
            config["target_cpu"] = line.split("=", 1)[1].strip().strip('"')
    return config


def parse_milestone(raw: str | None) -> int | None:
    if not raw:
        return None
    match = re.search(r"(\d+)", str(raw))
    return int(match.group(1)) if match else None


def normalize_label_value(label: str) -> str:
    match = re.search(r"(\d+)$", label)
    if not match:
        return label
    value = match.group(1)
    if len(value) == 4 and value.startswith("7"):
        return f"branch-head {value}"
    return f"M{value}"


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


def extract_keywords(*parts: str) -> str:
    return " ".join(part for part in parts if part).lower()


def has_hid_signal(text: str) -> bool:
    return bool(re.search(r"(^|[^a-z])hid([^a-z]|$)|hid_connection", text))


SECURITY_PATTERNS = [
    ("sandbox escape", "sandbox escape"),
    ("local file disclosure", "local file disclosure"),
    ("use-after-free", "use-after-free"),
    ("uaf", "use-after-free"),
    ("double-free", "double-free"),
    ("heap-buffer-overflow", "heap-buffer-overflow"),
    ("out-of-bounds", "out-of-bounds access"),
    ("oob", "out-of-bounds access"),
    ("heap corruption", "heap corruption"),
    ("stack overflow", "stack overflow"),
    ("overflow", "memory corruption / overflow"),
    ("bypass", "security policy bypass"),
    ("rce", "remote code execution"),
]


@dataclass
class ApplyCheck:
    apply_ok: bool
    reverse_ok: bool
    apply_detail: str
    reverse_detail: str


def run_git_apply_check(repo_root: Path, patch_path: Path, reverse: bool) -> tuple[bool, str]:
    cmd = ["git", "-C", str(repo_root), "apply", "--check"]
    if reverse:
        cmd.append("--reverse")
    cmd.append(str(patch_path))
    result = subprocess.run(cmd, text=True, capture_output=True)
    detail = (result.stderr or result.stdout).strip()
    if not detail:
        detail = "clean"
    return result.returncode == 0, detail


def repo_root_for_issue(project_root: Path, selected_url: str, modified_files: list[dict]) -> Path:
    src_root = project_root / "src"
    paths = "\n".join(item.get("path", "") for item in modified_files)
    low = f"{selected_url}\n{paths}".lower()
    if "skia-review.googlesource.com" in low or "/skia/" in low:
        return src_root / "third_party/skia"
    if "/angle/" in low or "libangle" in low or "translator" in low:
        return src_root / "third_party/angle"
    if low.startswith("https://chromium-review.googlesource.com/c/v8") or "\nv8/" in low:
        return src_root / "v8"
    return src_root


def local_path_for_modified(repo_root: Path, src_root: Path, rel_path: str) -> Path:
    if repo_root == src_root:
        return src_root / rel_path
    return repo_root / rel_path


def platform_scope(issue_text: str, modified_paths: list[str]) -> str:
    joined = "\n".join(modified_paths).lower()
    low = f"{issue_text}\n{joined}"
    if any(token in low for token in ("[linux]", " linux ", "/linux/", "xdg_runtime_dir", "var/lib/chrome-remote-desktop", "chrome-remote-desktop")):
        return "linux-only"
    if any(token in low for token in ("[ios]", " ios ", "recentactivitycoordinator", "downloadmanagercoordinator")):
        return "ios-only"
    if any(token in low for token in ("[fsa]", "fsevents", "_mac", "web_contents_view_cocoa", "drag_source_mac")):
        return "mac-only"
    if any(token in low for token in ("win::", " on windows ", "systemmediacontrolswin", "hidconnectionwin", "share_operation.cc", "\"save as\" dialog")):
        return "win-only"
    if any(token in low for token in ("/android/", ".java", "jnipaymentapp")):
        return "android-only"
    if all("/ios/" in path.lower() or path.lower().startswith("ios/") for path in modified_paths):
        return "ios-only"
    if all("/android/" in path.lower() or ".java" in path.lower() for path in modified_paths):
        return "android-only"
    if all("_mac" in path.lower() or path.lower().endswith(".mm") or "fsevents" in path.lower() for path in modified_paths):
        return "mac-only"
    if all("win/" in path.lower() or "_win" in path.lower() for path in modified_paths):
        return "win-only"
    return "cross-platform"


def classify_vulnerability(issue_title: str, issue_desc: str, subject: str) -> str:
    low = extract_keywords(issue_title, issue_desc, subject)
    if "use-after-free" in low or "heap-use-after-free" in low or " uaf " in f" {low} ":
        return "use-after-free"
    if "cwe-377" in low or "/tmp" in low or "socket path" in low:
        return "insecure temporary file / socket path"
    if "sandbox bypass" in low or "aaw" in low:
        return "sandbox bypass / arbitrary address write"
    if "front-facing camera" in low or "front_facing" in low:
        return "permission / feature gate bypass"
    if "reentrancy" in low and "drag" in low:
        return "ui spoofing / drag-drop reentrancy"
    if "frame size change" in low or "illegal state" in low:
        return "renderer-to-browser state validation failure"
    for key, value in SECURITY_PATTERNS:
        if key in low:
            return value
    return "logic security / lifecycle safety"


def boundary_impact(vuln_class: str, issue_text: str) -> dict:
    low = issue_text.lower()
    return {
        "permission": "涉及高权限浏览器进程对象生命周期" if any(k in vuln_class for k in ("use-after-free", "overflow", "corruption")) else "未见直接权限模型改动",
        "sandbox": "明确关联 sandbox escape / renderer-to-browser or renderer-to-gpu boundary" if "sandbox" in low else "可能位于 renderer/browser 或 renderer/gpu 跨进程边界",
        "privacy": "存在文件、Cookie、跨站点数据泄露风险" if any(k in low for k in ("cookie", "file disclosure", "downloadurl", "headers")) else "未见直接隐私接口改动，但可能间接受影响",
        "certificate_or_origin": "存在跨站点/跨源边界影响" if any(k in low for k in ("site isolation", "other sites", "origin", "cross-site", "cookie")) else "未见证书边界直接证据",
    }


def feature_for_issue(team: str, modified_paths: list[str], issue_text: str, feature_lines: list[str]) -> list[str]:
    low = extract_keywords(issue_text, "\n".join(modified_paths))
    preferred: list[str] = []

    if any(token in low for token in ("v8", "cppheappointer", "jsarraybuffer", "marking-visitor", "scavenger", "sweeper")):
        preferred.append("ArkWeb性能 > 存储&PA规格 > 堆内存分配、管理 > 安全特性")
    if any(token in low for token in ("webxr", "arcore", "front_facing", "front-facing")):
        preferred.append("ArkWeb外设服务 > 外设 > 硬件连接能力 > 支持虚拟现实设备")
    if any(token in low for token in ("named_mojo", "ipc_constants", "socket path", "chrome-remote-desktop", "chromoting")):
        preferred.append("ArkWeb云服务 > 云服务网络协议 > 协议栈 > 协议栈")
    if any(token in low for token in ("content_settings_extension_install_time_permission_provider", "extensioninstalltimepermissionprovider", "host_content_settings_map_factory")):
        preferred.append("ArkWeb云服务 > 云服务安全与扩展 > 浏览器扩展框架 > 浏览器扩展框架")
    if "ipcz" in low:
        preferred.append("ArkWeb交互安全 > 安全特性 > 安全架构 > 站点隔离")
    if "skia" in low:
        preferred.append("ArkWeb渲染合成 > 渲染基础 > skia > skia渲染后端")
    if "angle" in low or "libangle" in low or "translator" in low:
        preferred.append("ArkWeb渲染合成 > 渲染基础 > angle > angle渲染引擎")
    if "site isolation" in low or "headers from renderer" in low or "cookie" in low:
        preferred.append("ArkWeb交互安全 > 安全特性 > 安全架构 > 站点隔离")
        preferred.append("ArkWeb云服务 > 云服务网络协议 > Cookie管理 > Cookie管理")
    if "systemmediacontrols" in low or "thumbnail" in low:
        preferred.append("ArkWeb多媒体 > 网页媒体对接播控中心 > 接入播控 > 接入播控策略")
    if has_hid_signal(low):
        preferred.append("ArkWeb外设服务 > 外设 > 硬件连接能力 > 支持人机接口设备管理")
    if "download" in low:
        preferred.append("ArkWeb云服务 > 云服务网页加载 > 网络资源下载 > 网络资源下载")
    if "drag" in low:
        preferred.append("ArkWeb交互动效 > 拖拽 > 拖拽行为 > 拖出")
    if "touch" in low:
        preferred.append("ArkWeb交互动效 > 网页缩放 > 手势触发缩放 > w3c touch events")
    if "audioworklet" in low or "webaudio" in low or "web audio" in low:
        preferred.append("ArkWeb多媒体 > 网页音频播放 > 音频后台播放策略 > WebAudio API播放")
    if "h265" in low or "video" in low:
        preferred.append("ArkWeb多媒体 > 网页视频播放 > 视频解码 > 视频AvCodec硬解")
    if "pdf" in low:
        preferred.append("ArkWeb基础框架 > PDF文档加载 > 加载来源 > 网络文档加载")

    if not preferred:
        defaults = {
            "ArkWeb云服务": "ArkWeb云服务 > CVE&运维 > CVE > CVE",
            "ArkWeb渲染合成": "ArkWeb渲染合成 > 渲染基础 > angle > angle渲染引擎",
            "ArkWeb渲染引擎": "ArkWeb渲染引擎 > 网页绘制 > blink > W3C接口",
            "ArkWeb基础框架": "ArkWeb云服务 > CVE&运维 > CVE > CVE",
            "ArkWeb交互动效": "ArkWeb交互动效 > 拖拽 > 拖拽行为 > 拖出",
            "ArkWeb交互安全": "ArkWeb交互安全 > 安全特性 > 安全架构 > 站点隔离",
            "ArkWeb多媒体": "ArkWeb多媒体 > 网页视频播放 > 视频解码 > 视频AvCodec硬解",
            "ArkWeb JS引擎": "ArkWeb JS引擎 > 语言及标准库 > ES语言标准支持 > 现代语法支持",
        }
        preferred.append(defaults.get(team, "ArkWeb云服务 > CVE&运维 > CVE > CVE"))

    feature_set = set(feature_lines)
    resolved = [item for item in dedupe(preferred) if item in feature_set]
    same_team = [item for item in resolved if item.startswith(team + " >")]
    if same_team:
        return same_team
    if resolved:
        return resolved

    for line in feature_lines:
        if line.startswith(team + " >"):
            return [line]
    return feature_lines[:1]


def team_for_issue(modified_paths: list[str], issue_text: str) -> tuple[str, str]:
    low = extract_keywords(issue_text, "\n".join(modified_paths))
    if any(token in low for token in ("v8", "cppheappointer", "jsarraybuffer", "marking-visitor", "scavenger", "sweeper")):
        return "ArkWeb性能", "补丁位于 V8 GC/堆对象生命周期与句柄同步逻辑，归入性能责任田中的内存管理/安全特性。"
    if any(token in low for token in ("webxr", "arcore", "front_facing", "front-facing")):
        return "ArkWeb外设服务", "补丁涉及 WebXR/ARCore 虚拟现实设备能力与前置摄像头权限暴露，归入外设服务责任田。"
    if any(token in low for token in ("named_mojo", "ipc_constants", "chrome-remote-desktop", "chromoting", "socket path")):
        return "ArkWeb云服务", "补丁涉及 IPC 命名通道与远程服务进程的 socket 路径管理，归入云服务网络协议责任田。"
    if any(token in low for token in ("content_settings_extension_install_time_permission_provider", "extensioninstalltimepermissionprovider", "host_content_settings_map_factory")):
        return "ArkWeb云服务", "补丁涉及扩展权限与内容设置提供器的线程安全，归入云服务安全与扩展责任田。"
    if "ipcz" in low or "site isolation" in low:
        return "ArkWeb交互安全", "补丁涉及跨进程边界、站点隔离或 renderer/browser 安全语义，归入交互安全责任田。"
    if "skia" in low or "angle" in low:
        return "ArkWeb渲染合成", "补丁主要修改渲染/图形或跨进程图形基础库实现，归入渲染合成责任田。"
    if has_hid_signal(low):
        return "ArkWeb外设服务", "补丁涉及 HID 等外设连接能力，归入外设服务责任田。"
    if "webaudio" in low or "audioworklet" in low or "h265" in low or "video" in low or "systemmediacontrols" in low:
        return "ArkWeb多媒体", "补丁涉及音视频解码、音频工作线程或媒体播控链路，归入多媒体责任田。"
    if "touch" in low or "drag" in low:
        return "ArkWeb交互动效", "补丁涉及触摸/拖拽等输入事件或交互行为，归入交互动效责任田。"
    if "site isolation" in low or "cookie" in low or "renderer" in low and "other sites" in low:
        return "ArkWeb交互安全", "补丁涉及跨站点边界、renderer/browser 交互安全或站点隔离语义，归入交互安全责任田。"
    if any(token in low for token in ("download", "payment", "networkcontext", "nonce", "fsevents", "webshare", "file disclosure", "file system access")):
        return "ArkWeb云服务", "补丁主要位于浏览器服务、网络/下载/支付/设备接入链路，归入云服务责任田。"
    if "blink" in low or "harfbuzz" in low or "webnn" in low or "tflite" in low:
        return "ArkWeb渲染引擎", "补丁影响 Blink 渲染/排版/推理接口路径，归入渲染引擎责任田。"
    return "ArkWeb云服务", "补丁未能稳定映射到更细责任田，按云服务 CVE 通道兜底。"


def issue_field_evidence(issue: dict) -> list[dict]:
    entries: list[dict] = []
    milestone = issue.get("Milestone")
    if milestone:
        entries.append(
            {
                "field": "Milestone",
                "value": str(milestone),
                "meaning": "目标修复里程碑，只能说明上游计划/最终修复目标，不能单独证明受影响起点。",
                "confidence": "medium",
            }
        )
    for label in issue.get("Labels", []) or []:
        meaning = "标签仅供辅助判断。"
        confidence = "low"
        if label.startswith("FoundIn-"):
            meaning = "确认受影响的 Chromium milestone。"
            confidence = "high"
        elif label.startswith("Merged-"):
            meaning = "修复已进入对应 milestone 或 branch-head。"
            confidence = "high"
        elif label.startswith("Merge-Request"):
            meaning = "请求将修复合入分支，不代表已落地。"
            confidence = "medium"
        elif label.startswith("Merge-Approved"):
            meaning = "分支回合请求已批准，不代表已提交。"
            confidence = "medium"
        elif label.startswith("Merge-Review"):
            meaning = "仍在对应分支 review 阶段。"
            confidence = "medium"
        elif label.startswith("Merge-Delayed"):
            meaning = "对应分支合入被推迟。"
            confidence = "medium"
        entries.append(
            {
                "field": "Label",
                "value": label,
                "meaning": meaning,
                "confidence": confidence,
            }
        )
    return entries


def version_conclusion(issue: dict, selected_fix: dict, current_version: dict) -> tuple[dict, list[str]]:
    milestone = issue.get("Milestone", "unknown")
    labels = issue.get("Labels", []) or []
    found_in = [normalize_label_value(label) for label in labels if label.startswith("FoundIn-")]
    merged = [normalize_label_value(label) for label in labels if label.startswith("Merged-")]
    fixed_versions = dedupe(merged + ([f"M{milestone}"] if milestone not in (None, "", "unknown") else []))
    unknown_versions = [] if found_in else ["affected_start_unknown"]
    branch_evidence = [
        {
            "source": "Gerrit" if "googlesource.com" in selected_fix.get("url", "") else "patch",
            "url_or_commit": selected_fix.get("url") or selected_fix.get("commit_hash") or "",
            "branch": "main",
            "landing_state": "landed",
            "evidence": f"selected_fix commit_time={selected_fix.get('commit_time', 'unknown')}",
        }
    ]
    for label in labels:
        if label.startswith("Merged-"):
            value = label.split("Merged-", 1)[1]
            branch = f"refs/branch-heads/{value}" if value.isdigit() and len(value) == 4 else "release-branch"
            branch_evidence.append(
                {
                    "source": "issue_label",
                    "url_or_commit": label,
                    "branch": branch,
                    "landing_state": "cherry-picked",
                    "evidence": "Issue 标签明确记录 merged 到对应分支/里程碑。",
                }
            )
    basis = [
        f"当前 ArkWeb 基线版本为 Chromium {current_version['full']} (M{current_version['milestone']}).",
        f"Issue Milestone={milestone} 只表示目标修复窗口，不等同于受影响起点。",
    ]
    if found_in:
        conclusion = f"上游 issue 明确标记 FoundIn={', '.join(found_in)}，可确认这些 milestone 受影响；修复已至少进入 {', '.join(fixed_versions) or 'unknown'}。"
    elif fixed_versions:
        conclusion = (
            f"当前证据只确认修复已在 {', '.join(fixed_versions)} 落地或被合入，对受影响起始 milestone 缺少 FoundIn 级别证据，"
            "因此上游影响版本起点记为 unknown。"
        )
    else:
        conclusion = "仅能确认 issue 已 fixed 且 selected fix 已 landed，无法仅凭当前 issue 元数据精确锁定受影响/修复版本范围。"
    return (
        {
            "affected_versions": found_in,
            "fixed_versions": fixed_versions,
            "unknown_versions": unknown_versions,
            "issue_field_evidence": issue_field_evidence(issue),
            "upstream_branch_evidence": branch_evidence,
            "conclusion": conclusion,
            "conclusion_basis": basis,
        },
        basis,
    )


def merge_policy_from_requirements(impact_mode: str) -> dict:
    force_merge = impact_mode == "force_affected"
    return {
        "force_merge": force_merge,
        "impact_mode": impact_mode,
        "source": "requirements",
        "reason": (
            "需求描述写明“是否强制合入：是”，真实 arkweb_impact 仅用于记录证据，后续仍按强制合入策略继续。"
            if force_merge
            else "需求描述未启用强制合入，后续按真实影响结论流转。"
        ),
    }


def detect_security(issue: dict, selected_fix: dict) -> bool:
    low = extract_keywords(
        issue.get("Issue标题", ""),
        issue.get("Issue原始描述", ""),
        selected_fix.get("subject", ""),
        " ".join(issue.get("Labels", []) or []),
    )
    return any(
        token in low
        for token in (
            "security",
            "uaf",
            "use-after-free",
            "overflow",
            "oob",
            "sandbox escape",
            "disclosure",
            "double-free",
            "heap corruption",
            "security_release",
            "security_impact",
            "vulnerability",
        )
    )


def platform_matches_target(platform: str, target_os: str) -> bool | None:
    mapping = {
        "android-only": "android",
        "win-only": "win",
        "mac-only": "mac",
        "ios-only": "ios",
        "linux-only": "linux",
    }
    expected = mapping.get(platform)
    if expected is None or target_os == "unknown":
        return None
    return expected == target_os


def decide_impact(
    current_milestone: int | None,
    issue_milestone: int | None,
    platform: str,
    file_hits: list[Path],
    checks: ApplyCheck,
    target_os: str,
    modified_paths: list[str],
) -> tuple[str, str]:
    if checks.reverse_ok:
        return "unaffected", "选定补丁已可在当前源码树上反向 clean apply，说明等价修复大概率已存在。"

    before_fix = current_milestone is not None and issue_milestone is not None and current_milestone < issue_milestone
    has_code = bool(file_hits)
    platform_match = platform_matches_target(platform, target_os)

    if platform_match is False:
        return "unaffected", f"漏洞路径限定在 {platform}，而当前构建目标 target_os={target_os}，对应文件不会进入当前 ArkWeb 产物。"

    if any("content_settings_extension_install_time_permission_provider" in path for path in modified_paths):
        provider_hits = [path for path in modified_paths if "content_settings_extension_install_time_permission_provider" in path and Path(path).name]
        if not any(hit.name.startswith("content_settings_extension_install_time_permission_provider") for hit in file_hits):
            return "unaffected", "当前分支缺少上游 UAF 所在的 ExtensionInstallTimePermissionProvider 实现文件，HostContentSettingsMapFactory 也未注册该 provider，漏洞链路在本地代码中不可达。"

    if checks.apply_ok and platform == "cross-platform":
        return "affected", "补丁可在当前源码树 clean apply，且修改路径属于当前基线实际存在的跨平台实现。"

    if has_code and before_fix and platform == "cross-platform":
        return "affected", "当前基线版本早于上游修复里程碑，且本地存在对应代码路径但未见已修复证据。"

    if has_code and platform != "cross-platform":
        return "unknown", "源码中存在对应平台实现，但当前 ArkWeb 目标产品是否启用该平台路径仍需结合构建目标进一步确认。"

    if has_code:
        return "unknown", "本地存在对应实现，但补丁既无法正向 clean apply，也无法反向证明已修复，无法排除本地差异或部分修复。"

    return "unknown", "当前仅有上游修复证据，缺少足够的本地代码命中或分支信息，无法给出更强结论。"


def stability_flag(impact: str) -> bool:
    return impact in {"affected", "unknown"}


def compatibility_flag(impact: str) -> bool:
    return impact in {"affected", "unknown"}


def performance_flag(modified_paths: list[str]) -> bool:
    low = "\n".join(modified_paths).lower()
    return any(token in low for token in ("angle", "skia", "media", "audio", "video", "render", "gpu", "v8"))


def rom_impact(modified_paths: list[str]) -> str:
    return "是" if any(path in "\n".join(modified_paths) for path in ("DEPS", "README.chromium")) else "否"


def ram_impact(impact: str, modified_paths: list[str]) -> str:
    low = "\n".join(modified_paths).lower()
    if impact == "affected" and any(token in low for token in ("audio", "video", "skia", "angle", "touch", "network")):
        return "是"
    return "否"


def risk_level(impact: str, security_related: bool, platform: str) -> tuple[str, str]:
    if impact == "affected" and security_related and platform == "cross-platform":
        return "高", "真实结论为 affected，且属于安全相关漏洞，当前基线仍存在可达代码路径。"
    if impact == "affected":
        return "中", "真实结论为 affected，但存在平台限定或证据边界。"
    if impact == "unknown":
        return "中", "无法排除当前基线仍包含漏洞路径，需要后续合入/验证阶段继续收敛。"
    return "低", "已有较强证据表明当前基线已具备等价修复或代码路径不可达。"


def compat_risk_level(impact: str, modified_paths: list[str]) -> tuple[str, str]:
    low = "\n".join(modified_paths).lower()
    if impact == "affected" and any(token in low for token in ("skia", "angle", "media", "audio", "download", "network")):
        return "中", "补丁位于高频运行路径，后续合入需要关注行为兼容和回归。"
    if impact == "unknown":
        return "中", "本地差异尚未完全收敛，兼容风险需在后续合入和构建验证阶段继续确认。"
    return "低", "当前未见明显兼容性额外风险。"


def test_recommendation(team: str, features: list[str], security_related: bool, impact: str) -> str:
    pieces = [
        f"围绕责任田 {team} 和特性 {', '.join(features)} 执行定向单元/集成回归。",
        "对 patch 修改文件对应调用链执行异常输入、边界条件和回归场景覆盖。",
    ]
    if security_related:
        pieces.append("追加安全专项测试：畸形网页/IPC/媒体数据、跨源边界、权限与沙箱边界、崩溃与信息泄露回归。")
    if impact == "unknown":
        pieces.append("由于真实影响仍为 unknown，需在后续自动合入后结合编译和最小复现场景继续收敛。")
    return " ".join(pieces)


def markdown_report(record: dict, modified_paths: list[str], patch_files: list[dict]) -> str:
    lines = [
        "# 03 Impact Decision",
        "",
        "## Input summary",
        f"- Issue id: {record['IssueID']}",
        f"- Selected upstream fix: {record['selected_fix']['url']}",
        f"- Modified files: {len(modified_paths)}",
        f"- Patch files: {len(patch_files)}",
        "",
        "## Evidence chain",
        "### Issue evidence",
    ]
    lines.extend(f"- {item}" for item in record["evidence_chain"]["issue_evidence"])
    lines.extend(["", "### PR/CL evidence"])
    lines.extend(f"- {item}" for item in record["evidence_chain"]["pr_or_cl_evidence"])
    lines.extend(["", "### projectRoot code evidence"])
    lines.extend(f"- {item}" for item in record["evidence_chain"]["project_root_code_evidence"])
    lines.extend(
        [
            "",
            "## Chromium version impact",
            f"- Conclusion: {record['chromium_version_impact']['conclusion']}",
            f"- affected_versions: {record['chromium_version_impact']['affected_versions'] or ['unknown']}",
            f"- fixed_versions: {record['chromium_version_impact']['fixed_versions'] or ['unknown']}",
            f"- unknown_versions: {record['chromium_version_impact']['unknown_versions'] or []}",
            "",
            "## ArkWeb impact conclusion",
            f"- arkweb_impact: {record['arkweb_impact']}",
            f"- arkweb_vs_chromium_version_relation: {record['arkweb_vs_chromium_version_relation']}",
            "",
            "## Five-dimension analysis",
            f"- 稳定性相关: {record['稳定性相关']}",
            f"- 安全性相关: {record['安全性相关']}",
            f"- 性能相关: {record['性能相关']}",
            f"- 兼容性相关: {record['兼容性相关']}",
            f"- 业务逻辑正确性: {record['业务逻辑正确性']}",
            "",
            "## Security impact deep dive",
            f"- vulnerability_class: {record['security_impact']['vulnerability_class']}",
            f"- attack_surface: {record['security_impact']['attack_surface']}",
            f"- trigger_condition: {record['security_impact']['trigger_condition']}",
            f"- exploitability: {record['security_impact']['exploitability']}",
            f"- permission boundary: {record['security_impact']['boundary_impact']['permission']}",
            f"- sandbox boundary: {record['security_impact']['boundary_impact']['sandbox']}",
            f"- privacy boundary: {record['security_impact']['boundary_impact']['privacy']}",
            f"- certificate/origin boundary: {record['security_impact']['boundary_impact']['certificate_or_origin']}",
            f"- unfixed consequence: {record['security_impact']['unfixed_consequence']}",
            "",
            "## RAM/ROM impact",
            f"- 是否影响RAM: {record['是否影响RAM']}",
            f"- 是否影响ROM: {record['是否影响ROM']}",
            "",
            "## Ownership and feature",
            f"- 归属团队: {record['归属团队']}",
            f"- 归属团队原因: {record['归属团队原因']}",
            f"- 影响的特性: {', '.join(record['影响的特性'])}",
            "",
            "## Risk and recommendation",
            f"- 风险评估级别: {record['风险评估级别']}",
            f"- 风险评估级别原因: {record['风险评估级别原因']}",
            f"- 兼容性风险级别: {record['兼容性风险级别']}",
            f"- 兼容性风险级别原因: {record['兼容性风险级别原因']}",
            f"- 是否建议保留: {record['是否建议保留']}",
            f"- 是否建议保留原因: {record['是否建议保留原因']}",
            f"- 是否需要测试: {record['是否需要测试']}",
            f"- 测试建议: {record['测试建议']}",
        ]
    )
    return "\n".join(lines) + "\n"


def process_issue(issue_dir: Path, project_root: Path, current_version: dict, feature_lines: list[str], impact_mode: str) -> dict:
    issue = first_issue(issue_dir / "01_issue_analysis.json")
    patch = first_issue(issue_dir / "02_patch_fetch.json")
    selected = patch.get("selected_fix", {})
    modified = patch.get("modified_files", [])
    patch_files = patch.get("patch_files", [])
    modified_paths = [item.get("path", "") for item in modified]
    src_root = project_root / "src"
    build_config = current_build_config(project_root)
    repo_root = repo_root_for_issue(project_root, selected.get("url", ""), modified)
    patch_path = Path(patch_files[0]["path"]) if patch_files else None

    apply_ok = reverse_ok = False
    apply_detail = reverse_detail = "patch file missing"
    if patch_path and patch_path.is_file():
        apply_ok, apply_detail = run_git_apply_check(repo_root, patch_path, reverse=False)
        reverse_ok, reverse_detail = run_git_apply_check(repo_root, patch_path, reverse=True)
    checks = ApplyCheck(apply_ok, reverse_ok, apply_detail, reverse_detail)

    file_hits: list[Path] = []
    code_evidence: list[str] = [
        f"context.codebase={project_root}",
        f"target_os={build_config['target_os']}",
        f"target_cpu={build_config['target_cpu']}",
        f"源码检查根目录={repo_root}",
        f"git apply --check={apply_ok} ({apply_detail})",
        f"git apply --reverse --check={reverse_ok} ({reverse_detail})",
    ]
    for rel_path in modified_paths:
        local_path = local_path_for_modified(repo_root, src_root, rel_path)
        if local_path.exists():
            file_hits.append(local_path)
            code_evidence.append(f"{rel_path} -> FOUND at {local_path}")
        else:
            code_evidence.append(f"{rel_path} -> NOT_FOUND at expected path {local_path}")

    security_related = detect_security(issue, selected)
    issue_text = extract_keywords(issue.get("Issue标题", ""), issue.get("Issue原始描述", ""), selected.get("subject", ""))
    routing_text = extract_keywords(issue.get("Issue标题", ""), selected.get("subject", ""), "\n".join(modified_paths))
    vuln_class = classify_vulnerability(issue.get("Issue标题", ""), issue.get("Issue原始描述", ""), selected.get("subject", ""))
    platform = platform_scope(routing_text, modified_paths)
    issue_milestone = parse_milestone(issue.get("Milestone"))
    impact, impact_reason = decide_impact(
        parse_milestone(current_version["milestone"]),
        issue_milestone,
        platform,
        file_hits,
        checks,
        build_config["target_os"],
        modified_paths,
    )
    chromium_version, version_basis = version_conclusion(issue, selected, current_version)
    team, team_reason = team_for_issue(modified_paths, routing_text)
    features = feature_for_issue(team, modified_paths, routing_text, feature_lines)
    merge_policy = merge_policy_from_requirements(impact_mode)
    risk, risk_reason = risk_level(impact, security_related, platform)
    compat_risk, compat_risk_reason = compat_risk_level(impact, modified_paths)

    issue_evidence = [
        f"Issue状态={issue.get('Issue状态', 'unknown')}",
        f"Issue标题={issue.get('Issue标题', '')}",
        f"Milestone={issue.get('Milestone', 'unknown')}",
        f"Labels={issue.get('Labels', []) or []}",
        f"可信度={issue.get('可信度', 'unknown')}",
    ]
    pr_cl_evidence = [
        f"selected_fix.url={selected.get('url', '')}",
        f"selected_fix.change_id={selected.get('change_id', '')}",
        f"selected_fix.commit_hash={selected.get('commit_hash', '')}",
        f"selected_fix.commit_time={selected.get('commit_time', 'unknown')}",
        f"selected_fix.subject={selected.get('subject', '')}",
        f"modified_files={len(modified_paths)}",
        f"patch_files={len(patch_files)}",
    ]
    if patch.get("excluded_candidates"):
        pr_cl_evidence.append(f"excluded_candidates={len(patch.get('excluded_candidates', []))}")

    boundary = boundary_impact(vuln_class, issue_text)
    security_evidence = [
        f"漏洞类别={vuln_class}",
        f"平台范围={platform}",
        f"本地命中文件数={len(file_hits)}/{len(modified_paths)}",
        f"apply_check={apply_ok}, reverse_check={reverse_ok}",
    ]
    unfixed_consequence = (
        "若不修复，攻击者可继续利用当前可达代码路径触发浏览器进程内存破坏、跨站点数据泄露、沙箱边界突破或稳定性崩溃。"
        if impact == "affected"
        else "若后续证明当前基线仍包含该路径，则可能导致浏览器进程崩溃、信息泄露或边界绕过；当前证据仍需后续合入/构建阶段继续收敛。"
        if impact == "unknown"
        else "当前证据更倾向于本地已具备等价修复或链路不可达，残余安全风险较低。"
    )

    relation = (
        f"当前 ArkWeb 基线为 Chromium {current_version['full']} (M{current_version['milestone']}), 上游 issue 目标修复里程碑为 M{issue.get('Milestone', 'unknown')}。"
        f" {impact_reason}"
    )

    record = {
        "IssueID": issue_dir.name,
        "selected_fix": selected,
        "evidence_chain": {
            "issue_evidence": issue_evidence,
            "pr_or_cl_evidence": pr_cl_evidence,
            "project_root_code_evidence": code_evidence,
        },
        "chromium_version_impact": chromium_version,
        "arkweb_impact": impact,
        "merge_policy": merge_policy,
        "impact_evidence": [
            *version_basis,
            impact_reason,
            f"平台裁剪判断={platform}",
            f"本地代码命中={len(file_hits)}/{len(modified_paths)}",
        ],
        "arkweb_vs_chromium_version_relation": relation,
        "稳定性相关": stability_flag(impact),
        "安全性相关": security_related,
        "security_impact": {
            "is_security_related": security_related,
            "vulnerability_class": vuln_class,
            "attack_surface": (
                "网页内容、渲染器 IPC、媒体数据、下载/拖拽/输入等浏览器暴露面"
                if security_related
                else "not_applicable"
            ),
            "trigger_condition": "访问特制网页、提交特制媒体/脚本/IPC/交互输入，触发对应补丁修改的代码路径。",
            "exploitability": "high" if impact == "affected" and platform == "cross-platform" else "medium" if impact in {"affected", "unknown"} else "low",
            "boundary_impact": boundary,
            "unfixed_consequence": unfixed_consequence,
            "affected_or_unaffected_evidence": security_evidence,
            "security_test_recommendation": test_recommendation(team, features, True, impact),
        },
        "性能相关": performance_flag(modified_paths),
        "兼容性相关": compatibility_flag(impact),
        "业务逻辑正确性": impact in {"affected", "unknown"},
        "是否影响RAM": ram_impact(impact, modified_paths),
        "是否影响ROM": rom_impact(modified_paths),
        "归属团队": team,
        "归属团队原因": team_reason,
        "影响的特性": features,
        "风险评估级别": risk,
        "风险评估级别原因": risk_reason,
        "兼容性风险级别": compat_risk,
        "兼容性风险级别原因": compat_risk_reason,
        "是否建议保留": "是" if impact == "affected" or merge_policy["force_merge"] else "否",
        "是否建议保留置信度": 0.85 if impact == "affected" else 0.70 if impact == "unknown" and merge_policy["force_merge"] else 0.55,
        "是否建议保留原因": (
            "真实影响结论为 affected，应优先继续合入。"
            if impact == "affected"
            else "真实影响结论为 unaffected，但需求明确要求强制合入，后续按用户策略继续合入。"
            if impact == "unaffected" and merge_policy["force_merge"]
            else "真实影响结论未完全排除，且需求明确要求强制合入，后续按用户策略继续合入。"
            if merge_policy["force_merge"]
            else "当前证据不足以建议继续保留。"
        ),
        "是否需要测试": "是",
        "测试建议": test_recommendation(team, features, security_related, impact),
    }

    (issue_dir / "03_impact_decision.json").write_text(
        json.dumps({"issues": [record]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (issue_dir / "03_impact_decision.md").write_text(
        markdown_report(record, modified_paths, patch_files),
        encoding="utf-8",
    )
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--feature-tree", type=Path)
    parser.add_argument("--impact-mode", default="normal", choices=["normal", "force_affected"])
    args = parser.parse_args()

    output_root, project_root = validate_project_output_root(args.output_root, args.project_root)
    feature_lines = load_feature_lines(args.feature_tree)
    current_version = current_chromium_version(project_root)

    records = []
    for issue_dir in sorted(path for path in output_root.iterdir() if path.is_dir()):
        if (issue_dir / "01_issue_analysis.json").is_file() and (issue_dir / "02_patch_fetch.json").is_file():
            records.append(process_issue(issue_dir, project_root, current_version, feature_lines, args.impact_mode))

    print(json.dumps({"processed": len(records), "current_version": current_version, "issues": records}, ensure_ascii=False, indent=2))
    return 0 if records else 1


if __name__ == "__main__":
    raise SystemExit(main())
