#!/usr/bin/env python3
"""
Phone Agent iOS CLI - AI-powered iOS phone automation.

Usage:
    python ios.py [OPTIONS]

Environment Variables:
    PHONE_AGENT_BASE_URL: Model API base URL (default: http://localhost:8000/v1)
    PHONE_AGENT_MODEL: Model name (default: autoglm-phone-9b)
    PHONE_AGENT_API_KEY: API key for model authentication (default: EMPTY)
    PHONE_AGENT_MAX_STEPS: Maximum steps per task (default: 100)
    PHONE_AGENT_WDA_URL: WebDriverAgent URL (default: http://localhost:8100)
    PHONE_AGENT_WDA_INSECURE: Disable TLS verification for WDA HTTPS URL (optional)
    PHONE_AGENT_IOS_SCALE_FACTOR: Override iOS coordinate scale factor (optional)
    PHONE_AGENT_LANG: Language for system prompt (cn or en, default: cn)
"""

import argparse
import os
import sys

from phone_agent.ios import IOSAgentConfig, IOSPhoneAgent
from phone_agent.cli_checks import check_model_api
from phone_agent.ios.apps import list_supported_apps
from phone_agent.model import ModelConfig
from phone_agent.ios.wda import WDAConnection


def _env_truthy(name: str) -> bool:
    value = os.getenv(name, "")
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def check_system_requirements(
    wda_url: str = "http://localhost:8100", *, verify_tls: bool = True
) -> bool:
    """
    Check system requirements before running the agent.

    Checks:
    1. WebDriverAgent is running and reachable

    Args:
        wda_url: WebDriverAgent URL to check (must be reachable from this machine).

    Returns:
        True if all checks pass, False otherwise.
    """
    print("🔍 Checking system requirements...")
    print("-" * 50)

    all_passed = True

    # Check 1: WebDriverAgent running
    print(f"1. Checking WebDriverAgent ({wda_url})...", end=" ")
    try:
        conn = WDAConnection(wda_url=wda_url, verify_tls=verify_tls)

        if conn.is_wda_ready():
            print("✅ OK")
            # Get WDA status for additional info
            status = conn.get_wda_status()
            if status:
                session_id = status.get("sessionId", "N/A")
                print(f"   Session ID: {session_id}")
        else:
            print("❌ FAILED")
            print("   Error: WebDriverAgent is not running or not accessible.")
            print("   Solution:")
            print("     1. Run WebDriverAgent on your iOS device via Xcode")
            print(
                "     2. Ensure the WDA URL is reachable from this machine:"
            )
            print(
                "        - Wi‑Fi: use device IP, e.g. --wda-url http://192.168.1.100:8100"
            )
            print(
                "        - USB: forward :8100 to this machine, then use --wda-url http://localhost:8100"
            )
            print(
                f"     3. Verify in browser: open {wda_url.rstrip('/')}/status"
            )
            print("\n   Quick setup guide:")
            print(
                "     git clone https://github.com/appium/WebDriverAgent.git && cd WebDriverAgent"
            )
            print("     ./Scripts/bootstrap.sh")
            print("     open WebDriverAgent.xcodeproj")
            print("     # Configure signing, then Product > Test (Cmd+U)")
            all_passed = False
    except Exception as e:
        print("❌ FAILED")
        print(f"   Error: {e}")
        all_passed = False

    print("-" * 50)

    if all_passed:
        print("✅ All system checks passed!\n")
    else:
        print("❌ System check failed. Please fix the issues above.")

    return all_passed


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Phone Agent iOS - AI-powered iOS phone automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run with default settings
    python ios.py

    # Specify model endpoint
    python ios.py --base-url http://localhost:8000/v1

    # Use WiFi connection
    python ios.py --wda-url http://192.168.1.100:8100

    # List supported apps
    python ios.py --list-apps

    # Run a specific task
    python ios.py "Open Safari and search for iPhone tips"
        """,
    )

    # Model options
    parser.add_argument(
        "--base-url",
        type=str,
        default=os.getenv("PHONE_AGENT_BASE_URL", "http://localhost:8000/v1"),
        help="Model API base URL",
    )

    parser.add_argument(
        "--apikey",
        "--api-key",
        dest="api_key",
        type=str,
        default=os.getenv("PHONE_AGENT_API_KEY", "EMPTY"),
        help="API key for model authentication",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("PHONE_AGENT_MODEL", "autoglm-phone-9b"),
        help="Model name",
    )

    parser.add_argument(
        "--max-steps",
        type=int,
        default=int(os.getenv("PHONE_AGENT_MAX_STEPS", "100")),
        help="Maximum steps per task",
    )

    # iOS Device options
    parser.add_argument(
        "--wda-url",
        type=str,
        default=os.getenv("PHONE_AGENT_WDA_URL", "http://localhost:8100"),
        help="WebDriverAgent URL (default: http://localhost:8100)",
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        default=_env_truthy("PHONE_AGENT_WDA_INSECURE"),
        help="Disable TLS verification for WDA HTTPS URL",
    )

    scale_factor_env = os.getenv("PHONE_AGENT_IOS_SCALE_FACTOR")
    parser.add_argument(
        "--scale-factor",
        type=float,
        default=float(scale_factor_env) if scale_factor_env else None,
        help="Override iOS coordinate scale factor (auto-detected if omitted)",
    )

    parser.add_argument(
        "--wda-status",
        action="store_true",
        help="Show WebDriverAgent status and exit",
    )

    # Other options
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress verbose output"
    )

    parser.add_argument(
        "--list-apps", action="store_true", help="List supported apps and exit"
    )

    parser.add_argument(
        "--lang",
        type=str,
        choices=["cn", "en"],
        default=os.getenv("PHONE_AGENT_LANG", "cn"),
        help="Language for system prompt (cn or en, default: cn)",
    )

    parser.add_argument(
        "task",
        nargs="?",
        type=str,
        help="Task to execute (interactive mode if not provided)",
    )

    return parser.parse_args()


def handle_device_commands(args) -> bool:
    """
    Handle iOS device-related commands.

    Returns:
        True if a device command was handled (should exit), False otherwise.
    """
    conn = WDAConnection(wda_url=args.wda_url, verify_tls=not args.insecure)

    # Handle --wda-status
    if args.wda_status:
        print(f"Checking WebDriverAgent status at {args.wda_url}...")
        print("-" * 50)

        if conn.is_wda_ready():
            print("✓ WebDriverAgent is running")

            status = conn.get_wda_status()
            if status:
                print(f"\nStatus details:")
                value = status.get("value", {})
                print(f"  Session ID: {status.get('sessionId', 'N/A')}")
                print(f"  Build: {value.get('build', {}).get('time', 'N/A')}")

                current_app = value.get("currentApp", {})
                if current_app:
                    print(f"\nCurrent App:")
                    print(f"  Bundle ID: {current_app.get('bundleId', 'N/A')}")
                    print(f"  Process ID: {current_app.get('pid', 'N/A')}")
        else:
            print("✗ WebDriverAgent is not running")
            print("\nPlease start WebDriverAgent on your iOS device:")
            print("  1. Open WebDriverAgent.xcodeproj in Xcode")
            print("  2. Select your device (over WiFi is recommended)")
            print("  3. Run WebDriverAgentRunner (Product > Test or Cmd+U)")

        return True

    return False


def main():
    """Main entry point."""
    args = parse_args()

    # Handle --list-apps (no system check needed)
    if args.list_apps:
        print("Supported iOS apps:")
        print("\nNote: For iOS apps, Bundle IDs are configured in:")
        print("  phone_agent/ios/apps.py")
        print("\nCurrently configured apps:")
        for app in sorted(list_supported_apps()):
            print(f"  - {app}")
        print(
            "\nTo add iOS apps, find the Bundle ID and add to APP_PACKAGES_IOS dictionary."
        )
        return

    # Handle device commands (these may need partial system checks)
    if handle_device_commands(args):
        return

    # Run system requirements check before proceeding
    if not check_system_requirements(wda_url=args.wda_url, verify_tls=not args.insecure):
        sys.exit(1)

    # Check model API connectivity and model availability
    if not check_model_api(args.base_url, args.model, args.api_key):
        sys.exit(1)

    # Create configurations
    model_config = ModelConfig(
        base_url=args.base_url,
        model_name=args.model,
        api_key=args.api_key
    )

    agent_config = IOSAgentConfig(
        max_steps=args.max_steps,
        wda_url=args.wda_url,
        scale_factor=args.scale_factor,
        verify_tls=not args.insecure,
        verbose=not args.quiet,
        lang=args.lang,
    )

    # Create iOS agent
    agent = IOSPhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )

    # Print header
    print("=" * 50)
    print("Phone Agent iOS - AI-powered iOS automation")
    print("=" * 50)
    print(f"Model: {model_config.model_name}")
    print(f"Base URL: {model_config.base_url}")
    print(f"WDA URL: {args.wda_url}")
    print(f"Max Steps: {agent_config.max_steps}")
    print(f"Language: {agent_config.lang}")

    print("=" * 50)

    # Run with provided task or enter interactive mode
    if args.task:
        print(f"\nTask: {args.task}\n")
        result = agent.run(args.task)
        print(f"\nResult: {result}")
    else:
        # Interactive mode
        print("\nEntering interactive mode. Type 'quit' to exit.\n")

        while True:
            try:
                task = input("Enter your task: ").strip()

                if task.lower() in ("quit", "exit", "q"):
                    print("Goodbye!")
                    break

                if not task:
                    continue

                print()
                result = agent.run(task)
                print(f"\nResult: {result}\n")
                agent.reset()

            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
