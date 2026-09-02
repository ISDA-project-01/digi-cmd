"""
Command Executor
"""

import os
import subprocess
import sys
from typing import Tuple

class CommandExecutor:
    @staticmethod
    def execute(command: str, cwd: str = None) -> Tuple[int, str, str]:
        if not command.strip():
            return 0, "", ""

        # Handle 'cd' builtin
        parts = command.strip().split()
        if parts[0] == "cd":
            target = parts[1] if len(parts) > 1 else os.path.expanduser("~")
            try:
                os.chdir(target)
                return 0, f"Changed directory to {os.getcwd()}", ""
            except Exception as e:
                return 1, "", str(e)

        try:
            proc = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd or os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate()
            return proc.returncode, stdout, stderr
        except Exception as e:
            return 1, "", str(e)
