#!/usr/bin/env python3
"""Bootstrap script: check and install Python dependencies for the scanner."""
import sys
import subprocess

def main():
    missing = []
    try:
        import openpyxl
    except ImportError:
        missing.append("openpyxl>=3.0.0")

    if not missing:
        print("✅ All dependencies satisfied.")
        return 0

    print(f"⚠️  Missing dependencies: {', '.join(missing)}")
    print("Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        print("✅ Dependencies installed.")
        return 0
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"   Please install manually: pip install {' '.join(missing)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
