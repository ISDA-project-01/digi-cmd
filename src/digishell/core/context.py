"""
DigiShell Context Management
"""

import os
from typing import Dict, Any, Optional

class ShellContext:
    def __init__(self):
        self.cwd: str = os.getcwd()
        self.history = []
        self.last_command: Optional[str] = None
        self.last_output: Optional[str] = None
        self.last_error: Optional[str] = None
        self.last_exit_code: int = 0
        self.mode: str = "full"  # "full" (3GB+) or "limited" (2.2GB)
        self.learned_commands: Dict[str, str] = {}
        self.workflow_logs = []

    def update_cwd(self, new_dir: str):
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            os.chdir(new_dir)
            self.cwd = os.getcwd()

    def log_workflow(self, step: str):
        self.workflow_logs.append(step)

    def clear_workflow(self):
        self.workflow_logs.clear()
