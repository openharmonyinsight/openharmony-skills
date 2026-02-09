"""Command-line interface for arkweb-app-debug."""

import argparse
import sys
import logging
from typing import Optional

from arkweb_app_debug.config.manager import ConfigManager
from arkweb_app_debug.device.manager import DeviceManager
from arkweb_app_debug.port.manager import PortForwardManager
from arkweb_app_debug.session.manager import SessionManager, DebugConfig
from arkweb_app_debug.utils.logger import setup_logger, log_info, log_success, log_error
from arkweb_app_debug.utils.chrome import ChromeDevTools


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="arkweb-app-debug",
        description="ArkWeb App debugging tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start debugging session
  arkweb-app-debug start --package com.example.app

  # Start with custom port
  arkweb-app-debug start --package com.example.app --local-port 9223

  # List devices
  arkweb-app-debug device list

  # Clean up orphaned forwards
  arkweb-app-debug port cleanup --orphans

  # List active sessions
  arkweb-app-debug session list

For more information, see: https://github.com/your-repo/arkweb-app-debug
        """,
    )

    # Global options
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--config", type=str, help="Path to configuration file"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # start command
    start_parser = subparsers.add_parser("start", help="Start debugging session")
    start_parser.add_argument(
        "--package", "-p", required=False, help="Application package name (auto-detect if not specified)"
    )
    start_parser.add_argument("--bundle", "-b", help="Ability name")
    start_parser.add_argument(
        "--hap-path", help="Path to HAP file for installation"
    )
    start_parser.add_argument(
        "--device", "-d", help="Device ID (auto-detect if not specified)"
    )
    start_parser.add_argument(
        "--local-port", "-l", type=int, help="Local port (default: 9222)"
    )
    start_parser.add_argument(
        "--device-port", type=int, default=8888, help="Device debug port (default: 8888)"
    )
    start_parser.add_argument(
        "--no-start",
        action="store_true",
        help="Don't auto-start the application",
    )
    start_parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't auto-cleanup on failure",
    )
    start_parser.add_argument(
        "--open-chrome",
        action="store_true",
        help="Open Chrome DevTools automatically",
    )

    # device command
    device_parser = subparsers.add_parser("device", help="Device management")
    device_parser.add_argument(
        "action",
        choices=["list", "info", "check"],
        help="Device action",
    )
    device_parser.add_argument("--device-id", "-d", help="Target device ID")

    # port command
    port_parser = subparsers.add_parser("port", help="Port forward management")
    port_parser.add_argument(
        "action",
        choices=["list", "create", "remove", "cleanup"],
        help="Port action",
    )
    port_parser.add_argument("--local-port", "-l", type=int, help="Local port")
    port_parser.add_argument("--device-port", type=int, help="Device port")
    port_parser.add_argument(
        "--orphans", action="store_true", help="Clean up orphaned forwards"
    )
    port_parser.add_argument("--device-id", "-d", help="Target device ID")

    # session command
    session_parser = subparsers.add_parser("session", help="Session management")
    session_parser.add_argument(
        "action",
        choices=["list", "stop", "cleanup"],
        help="Session action",
    )
    session_parser.add_argument(
        "--session-id", "-s", help="Session ID (for 'stop' action)"
    )
    session_parser.add_argument(
        "--all", action="store_true", help="Stop all sessions"
    )
    session_parser.add_argument(
        "--expired",
        action="store_true",
        help="Clean up expired sessions",
    )
    session_parser.add_argument(
        "--max-age",
        type=int,
        default=24,
        help="Max session age in hours (default: 24)",
    )

    # cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Resource cleanup")
    cleanup_parser.add_argument(
        "target",
        choices=["all", "orphans", "sessions"],
        help="Cleanup target",
    )

    # config command
    config_parser = subparsers.add_parser("config", help="Show configuration")
    config_parser.add_argument(
        "action",
        choices=["show"],
        help="Config action (show current configuration)",
    )

    return parser


def cmd_start(args, config: dict, logger: logging.Logger) -> int:
    """Handle start command."""
    log_info(logger, "🚀 Starting ArkWeb DevTools debugging session")

    # Get package name from args or config (with auto-detection)
    package = args.package or config.get("app", {}).get("package")
    if not package:
        log_error(logger, "❌ Package name not found. Please specify --package or run from a HarmonyOS project directory")
        log_error(logger, "   Tip: Ensure AppScope/app.json5 exists in your HarmonyOS project")
        return 1

    # Get HAP path from args or config
    hap_path = args.hap_path or config.get("app", {}).get("hap")

    # Get bundle name from args, config, or use package as default
    bundle = args.bundle or config.get("app", {}).get("bundle") or package

    # Get local port from args, config, or default
    local_port = args.local_port or config.get("app", {}).get("port") or config.get("defaults", {}).get("local_port_base", 9222)

    # Create debug config
    debug_config = DebugConfig(
        package=package,
        bundle=bundle,
        hap_path=hap_path,
        device_port=args.device_port,
        local_port=local_port,
        device_id=args.device,
        auto_start=not args.no_start,
        auto_cleanup=not args.no_cleanup,
    )

    # Create session
    session_mgr = SessionManager(logger=logger)

    session = session_mgr.create_session(debug_config)

    if not session:
        log_error(logger, "❌ Failed to create debug session")
        return 1

    # Print session info
    print()
    print("=" * 60)
    log_success(logger, "✅ Debug session started successfully")
    print("=" * 60)
    print(f"  Session ID: {session.session_id}")
    print(f"  Device: {session.device_id}")
    print(f"  Package: {debug_config.package}")
    print(f"  Local Port: {session.local_port}")
    print(f"  WebSocket: {session.websocket_url}")
    print()
    print("  Next steps:")
    print(f"    1. Open Chrome DevTools: chrome://inspect/#devices")
    print(f"    2. Add network target: localhost:{session.local_port}")
    print(f"    3. Wait for device to appear")
    print(f"    4. Click 'inspect' to open DevTools")
    print()

    # Open Chrome if requested
    if args.open_chrome:
        chrome = ChromeDevTools(logger=logger)
        chrome.open_devtools(session.local_port)

    return 0


def cmd_device(args, config: dict, logger: logging.Logger) -> int:
    """Handle device command."""
    device_mgr = DeviceManager(logger=logger)

    if args.action == "list":
        log_info(logger, "📱 Listing connected devices")
        devices = device_mgr.list_devices()
        device_mgr.print_device_list(devices)
        return 0

    elif args.action == "info":
        if not args.device_id:
            log_error(logger, "Device ID required for 'info' action")
            return 1

        device_info = device_mgr.get_device_info(args.device_id)
        if device_info:
            print(device_info)
            return 0
        return 1

    elif args.action == "check":
        log_info(logger, "🔍 Checking HDC tool")
        if device_mgr.check_hdc():
            log_success(logger, "✅ HDC tool is available")
            return 0
        return 1

    return 0


def cmd_port(args, config: dict, logger: logging.Logger) -> int:
    """Handle port command."""
    device_id = args.device_id

    # Auto-detect device if not specified
    if not device_id:
        device_mgr = DeviceManager(logger=logger)
        device_id = device_mgr.get_default_device()
        if not device_id:
            log_error(logger, "No device found")
            return 1

    port_mgr = PortForwardManager(device_id=device_id, logger=logger)

    if args.action == "list":
        log_info(logger, "🔌 Listing port forwards")
        port_mgr.print_forward_list()
        return 0

    elif args.action == "create":
        if not args.local_port or not args.device_port:
            log_error(logger, "Both --local-port and --device-port required")
            return 1

        log_info(logger, f"Creating port forward: {args.device_port} -> localhost:{args.local_port}")
        if port_mgr.create_forward(
            device_port=args.device_port,
            local_port=args.local_port,
            session_id="manual",
        ):
            log_success(logger, "✅ Port forward created")
            return 0
        return 1

    elif args.action == "remove":
        if not args.local_port:
            log_error(logger, "--local-port required")
            return 1

        log_info(logger, f"Removing port forward: localhost:{args.local_port}")
        if port_mgr.remove_forward(args.local_port):
            log_success(logger, "✅ Port forward removed")
            return 0
        return 1

    elif args.action == "cleanup":
        if args.orphans:
            log_info(logger, "🧹 Cleaning up orphaned port forwards")
            count = port_mgr.cleanup_orphans()
            log_success(logger, f"✅ Cleaned up {count} orphaned forward(s)")
            return 0
        else:
            log_info(logger, "🧹 Cleaning up all port forwards")
            count = port_mgr.remove_all_forwards()
            log_success(logger, f"✅ Removed {count} forward(s)")
            return 0

    return 0


def cmd_session(args, config: dict, logger: logging.Logger) -> int:
    """Handle session command."""
    session_mgr = SessionManager(logger=logger)

    if args.action == "list":
        log_info(logger, "📋 Listing active sessions")
        sessions = session_mgr.list_sessions()

        if not sessions:
            log_info(logger, "No active sessions")
            return 0

        print()
        for session in sessions:
            print(f"  Session: {session.session_id}")
            print(f"    Device: {session.device_id}")
            print(f"    Package: {session.config.package}")
            print(f"    Port: {session.local_port}")
            print(f"    Status: {session.status}")
            print()

        return 0

    elif args.action == "stop":
        if args.all:
            log_info(logger, "🛑 Stopping all sessions")
            count = session_mgr.cleanup_all_sessions()
            log_success(logger, f"✅ Stopped {count} session(s)")
            return 0

        elif args.session_id:
            log_info(logger, f"🛑 Stopping session: {args.session_id}")
            if session_mgr.stop_session(args.session_id):
                log_success(logger, "✅ Session stopped")
                return 0
            return 1

        else:
            log_error(logger, "Either --session-id or --all required")
            return 1

    elif args.action == "cleanup":
        if args.expired:
            log_info(logger, "🧹 Cleaning up expired sessions")
            count = session_mgr.cleanup_expired_sessions(args.max_age)
            log_success(logger, f"✅ Cleaned up {count} expired session(s)")
            return 0

        log_info(logger, "🧹 Cleaning up all sessions")
        count = session_mgr.cleanup_all_sessions()
        log_success(logger, f"✅ Cleaned up {count} session(s)")
        return 0

    return 0


def cmd_cleanup(args, config: dict, logger: logging.Logger) -> int:
    """Handle cleanup command."""
    session_mgr = SessionManager(logger=logger)

    if args.target == "all":
        log_info(logger, "🧹 Cleaning up all resources")
        device_mgr = DeviceManager(logger=logger)
        device_id = device_mgr.get_default_device()

        if device_id:
            port_mgr = PortForwardManager(device_id=device_id, logger=logger)
            port_mgr.remove_all_forwards()

        session_mgr.cleanup_all_sessions()
        log_success(logger, "✅ All resources cleaned up")
        return 0

    elif args.target == "orphans":
        log_info(logger, "🧹 Cleaning up orphaned resources")
        device_mgr = DeviceManager(logger=logger)
        device_id = device_mgr.get_default_device()

        if device_id:
            port_mgr = PortForwardManager(device_id=device_id, logger=logger)
            port_mgr.cleanup_orphans()

        session_mgr.cleanup_expired_sessions()
        log_success(logger, "✅ Orphaned resources cleaned up")
        return 0

    elif args.target == "sessions":
        log_info(logger, "🧹 Cleaning up all sessions")
        count = session_mgr.cleanup_all_sessions()
        log_success(logger, f"✅ Cleaned up {count} session(s)")
        return 0

    return 0


def cmd_config(args, config: dict, logger: logging.Logger) -> int:
    """Handle config command."""
    if args.action == "show":
        log_info(logger, "📋 Current configuration:")
        import json

        # Show configuration in a readable format
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return 0

    return 0


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(level=log_level, verbose=args.verbose)

    # Load configuration
    config_mgr = ConfigManager(logger=logger)
    config = config_mgr.load_config()

    # Apply CLI args to config
    cli_args = {
        "package": getattr(args, "package", None),
        "bundle": getattr(args, "bundle", None),
        "hap_path": getattr(args, "hap_path", None),
        "local_port": getattr(args, "local_port", None),
        "device_port": getattr(args, "device_port", None),
        "device_id": getattr(args, "device", None),
    }
    config = config_mgr.apply_cli_args(config, cli_args)

    # Execute command
    if not args.command:
        parser.print_help()
        return 0

    handlers = {
        "start": cmd_start,
        "device": cmd_device,
        "port": cmd_port,
        "session": cmd_session,
        "cleanup": cmd_cleanup,
        "config": cmd_config,
    }

    handler = handlers.get(args.command)
    if handler:
        return handler(args, config, logger)

    log_error(logger, f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
