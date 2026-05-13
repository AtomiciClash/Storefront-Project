import os
import sys

print("Python Version:", sys.version)
try:
    import _tkinter
    print("✅ SUCCESS: _tkinter found!")
except ImportError as e:
    print(f"❌ FAIL: {e}")
    print("\nLooking for tkinter files in Nix...")
    os.system("find /nix/store -name '_tkinter.cpython*.so' 2>/dev/null | head -n 5")