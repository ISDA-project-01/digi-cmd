"""
Input Validation Utilities
"""

def validate_command_string(cmd: str) -> bool:
    return bool(cmd and isinstance(cmd, str))
