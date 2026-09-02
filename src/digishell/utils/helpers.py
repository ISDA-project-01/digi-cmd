"""
DigiShell Helper Utilities
"""

import os
import sys

def format_command_output(output: str) -> str:
    return output.strip() if output else "No output."

def is_windows() -> bool:
    return sys.platform == "win32"
