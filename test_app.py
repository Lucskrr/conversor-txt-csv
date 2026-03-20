#!/usr/bin/env python3
"""
Test script to run the application and verify update status display
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    try:
        from app.main import main
        print("Starting Conversor TOTVS with update status display...")
        print("Features added:")
        print("- Version display in header")
        print("- Update status indicator")
        print("- Manual update check in Help menu")
        print("- About dialog with version info")
        print()
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
