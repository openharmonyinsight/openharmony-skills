#!/usr/bin/env bash
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -euo pipefail

SSH_PORT="${SSH_PORT:-22}"
REVERSE_SSH_PORT="${REVERSE_SSH_PORT:-2222}"
VERIFY_TUNNEL=0
BLOCKERS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { printf '%b[INFO]%b %s\n' "$GREEN" "$NC" "$*"; }
warn() { printf '%b[WARN]%b %s\n' "$YELLOW" "$NC" "$*"; }
fail() { printf '%b[ERROR]%b %s\n' "$RED" "$NC" "$*" >&2; }

block() {
    fail "$*"
    BLOCKERS=$((BLOCKERS + 1))
}

usage() {
    printf '%s\n' "Usage: reverse_ssh_linux_setup.sh [--verify-tunnel]"
}

parse_args() {
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --verify-tunnel) VERIFY_TUNNEL=1 ;;
            -h|--help) usage; exit 0 ;;
            *) usage >&2; exit 2 ;;
        esac
        shift
    done
}

is_root() {
    [ "${EUID}" -eq 0 ]
}

service_name() {
    if systemctl list-unit-files sshd.service >/dev/null 2>&1; then
        printf '%s\n' sshd
    else
        printf '%s\n' ssh
    fi
}

install_and_start_sshd() {
    local service
    if ! command -v sshd >/dev/null 2>&1; then
        info "Installing openssh-server"
        if command -v apt >/dev/null 2>&1; then
            apt update
            apt install -y openssh-server
        elif command -v dnf >/dev/null 2>&1; then
            dnf install -y openssh-server
        elif command -v yum >/dev/null 2>&1; then
            yum install -y openssh-server
        else
            fail "Unsupported package manager; install openssh-server manually"
            return 1
        fi
    fi

    command -v systemctl >/dev/null 2>&1 || {
        fail "systemctl is required for automatic sshd setup"
        return 1
    }
    service=$(service_name)
    systemctl enable "$service"
    systemctl start "$service"
    systemctl is-active --quiet "$service" || {
        fail "${service} did not become active"
        return 1
    }
}

enable_reverse_forwarding() {
    local config=/etc/ssh/sshd_config
    local service
    [ -f "$config" ] || {
        fail "Missing ${config}"
        return 1
    }

    if grep -qE '^[[:space:]]*AllowTcpForwarding[[:space:]]+no([[:space:]]|$)' "$config"; then
        cp -p "$config" "${config}.ohos-hdc.bak"
        sed -i -E 's/^[[:space:]]*AllowTcpForwarding[[:space:]]+no([[:space:]]*)$/AllowTcpForwarding yes/' "$config"
        sshd -t || {
            cp -p "${config}.ohos-hdc.bak" "$config"
            fail "sshd_config validation failed; original restored"
            return 1
        }
        service=$(service_name)
        systemctl restart "$service"
        systemctl is-active --quiet "$service" || {
            fail "${service} failed after configuration update"
            return 1
        }
    fi
}

configure_ssh_firewall() {
    if command -v firewall-cmd >/dev/null 2>&1 && firewall-cmd --state >/dev/null 2>&1; then
        firewall-cmd --permanent --add-port="${SSH_PORT}/tcp"
        firewall-cmd --reload
        firewall-cmd --query-port="${SSH_PORT}/tcp" >/dev/null || {
            fail "firewalld did not retain ${SSH_PORT}/tcp"
            return 1
        }
    elif command -v ufw >/dev/null 2>&1 && ufw status 2>/dev/null | grep -q '^Status: active'; then
        ufw allow "${SSH_PORT}/tcp"
        ufw status | grep -Eq "${SSH_PORT}/tcp[[:space:]]+ALLOW" || {
            fail "ufw did not retain ${SSH_PORT}/tcp"
            return 1
        }
    elif command -v iptables >/dev/null 2>&1; then
        fail "iptables detected; verify and persist ${SSH_PORT}/tcp ingress manually because policy is distribution-specific"
        return 1
    else
        info "No active supported host firewall detected"
    fi
}

check_sshd() {
    command -v sshd >/dev/null 2>&1 || {
        block "sshd is not installed"
        return
    }

    if command -v systemctl >/dev/null 2>&1; then
        if ! systemctl is-active --quiet sshd 2>/dev/null && ! systemctl is-active --quiet ssh 2>/dev/null; then
            block "sshd is not active"
        fi
    elif command -v ss >/dev/null 2>&1; then
        ss -tln | grep -qE "[:.]${SSH_PORT}[[:space:]]" || block "No listener detected on SSH port ${SSH_PORT}"
    else
        block "Cannot verify the SSH listener because systemctl and ss are unavailable"
    fi
}

check_forwarding() {
    local effective
    if effective=$(sshd -T 2>/dev/null); then
        printf '%s\n' "$effective" | grep -qE '^allowtcpforwarding (yes|all|remote)$' || block "Effective sshd config disables remote TCP forwarding"
    elif [ -r /etc/ssh/sshd_config ]; then
        if grep -qE '^[[:space:]]*AllowTcpForwarding[[:space:]]+no([[:space:]]|$)' /etc/ssh/sshd_config; then
            block "AllowTcpForwarding is disabled"
        else
            block "Could not verify effective forwarding policy with sshd -T; Match blocks may disable it"
        fi
    else
        block "Cannot verify AllowTcpForwarding"
    fi
}

check_firewall_visibility() {
    local ufw_status
    if command -v firewall-cmd >/dev/null 2>&1 && firewall-cmd --state >/dev/null 2>&1; then
        firewall-cmd --query-port="${SSH_PORT}/tcp" >/dev/null || block "firewalld does not allow ${SSH_PORT}/tcp"
    elif command -v ufw >/dev/null 2>&1; then
        if ! ufw_status=$(ufw status 2>/dev/null); then
            block "Cannot verify ufw policy without administrator assistance"
        elif printf '%s\n' "$ufw_status" | grep -q '^Status: active'; then
            printf '%s\n' "$ufw_status" | grep -Eq "${SSH_PORT}/tcp[[:space:]]+ALLOW" || block "ufw does not allow ${SSH_PORT}/tcp"
        fi
    elif command -v iptables >/dev/null 2>&1 && ! is_root; then
        block "Cannot verify iptables SSH ingress without administrator assistance"
    fi
}

check_tunnel_listener() {
    command -v ss >/dev/null 2>&1 || {
        block "ss is required to verify the reverse listener"
        return
    }
    if ! ss -tln | grep -qE "127[.]0[.]0[.]1:${REVERSE_SSH_PORT}[[:space:]]"; then
        block "No loopback reverse listener on 127.0.0.1:${REVERSE_SSH_PORT}"
        warn "Confirm reverse_ssh_windows_setup.bat is still running and its Linux host/user and SSH/reverse ports match this setup"
    fi
}

show_recovery_actions() {
    printf '%s\n' "Recovery checks:"
    printf '%s\n' "  1. Check reverse_ssh_windows_setup.bat configuration and confirm the process is still running."
    printf '%s\n' "  2. Check Linux sshd, AllowTcpForwarding, authorized_keys, SSH ingress, and network/firewall reachability."
    printf '%s\n' "  3. After SSH recovers, rerun Windows-side hdc checkserver and hdc list targets -v."
    printf '%s\n' "  4. For [Empty], Unauthorized, or Offline, check device power/boot, USB debugging, data cable, direct USB port, Windows driver, and trust authorization."
    printf '%s\n' "  5. If USB is enumerated but HDC daemon/version fails, verify the intended board/product image, HDC daemon, and SDK/image compatibility."
    printf '%s\n' "Preserve logs and obtain explicit user approval before reflashing."
}

show_prerequisite_status() {
    printf '\n'
    if [ "$BLOCKERS" -ne 0 ]; then
        fail "Linux prerequisite checks failed with ${BLOCKERS} blocker(s)"
        show_recovery_actions
        return 1
    fi

    info "Linux prerequisites passed"
    printf '%s\n' "Windows must now create:"
    printf '  -R 127.0.0.1:%s:localhost:<WINDOWS_SSH_PORT>\n' "$REVERSE_SSH_PORT"
    printf '%s\n' "Then verify Windows SSH and Windows-side hdc list targets -v before declaring readiness."
}

main() {
    parse_args "$@"

    if [ "$VERIFY_TUNNEL" -eq 0 ] && is_root; then
        install_and_start_sshd || block "Automatic sshd setup failed"
        enable_reverse_forwarding || block "Failed to enable reverse forwarding"
        configure_ssh_firewall || block "Failed to configure Linux SSH ingress"
    elif [ "$VERIFY_TUNNEL" -eq 0 ]; then
        warn "Non-root mode: read-only checks; no packages, services, config, or firewall rules will be changed"
    fi

    check_sshd
    check_forwarding
    check_firewall_visibility
    if [ "$VERIFY_TUNNEL" -eq 1 ]; then
        check_tunnel_listener
    fi
    show_prerequisite_status
}

main "$@"
