"""Execution engine for Digi Shell managing subprocess calls and workflow tracking (';')."""

import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class ExecutionResult:
    command: str
    returncode: int
    stdout: str
    stderr: str
    workflow_steps: List[str]


class CommandExecutor:
    def __init__(self):
        self.workflow_logs: List[str] = []

    def log_workflow(self, message: str) -> None:
        self.workflow_logs.append(message)

    def execute(self, command: str, show_workflow: bool = False) -> ExecutionResult:
        """
        Executes shell command in subprocess.
        Handles built-in shell commands like 'cd'.
        """
        self.workflow_logs.clear()
        self.log_workflow(f"[Workflow Step 1] Prepared command: `{command}`")

        # Handle 'cd' command directly in process
        tokens = command.strip().split()
        if tokens and tokens[0] == "cd":
            target_dir = tokens[1] if len(tokens) > 1 else os.path.expanduser("~")
            try:
                os.chdir(target_dir)
                self.log_workflow(f"[Workflow Step 2] Changed current working directory to {os.getcwd()}")
                return ExecutionResult(
                    command=command,
                    returncode=0,
                    stdout=f"Changed directory to {os.getcwd()}\n",
                    stderr="",
                    workflow_steps=list(self.workflow_logs)
                )
            except Exception as e:
                self.log_workflow(f"[Workflow Step 2 Failed] Directory change error: {e}")
                return ExecutionResult(
                    command=command,
                    returncode=1,
                    stdout="",
                    stderr=str(e),
                    workflow_steps=list(self.workflow_logs)
                )

        use_shell = True
        self.log_workflow(f"[Workflow Step 2] Spawning subprocess on {platform.system()}...")

        try:
            process = subprocess.run(
                command,
                shell=use_shell,
                text=True,
                capture_output=True,
                timeout=120
            )
            self.log_workflow(f"[Workflow Step 3] Subprocess completed with exit code {process.returncode}")

            return ExecutionResult(
                command=command,
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
                workflow_steps=list(self.workflow_logs)
            )

        except subprocess.TimeoutExpired:
            self.log_workflow("[Workflow Step 3 Failed] Execution timed out after 120 seconds")
            return ExecutionResult(
                command=command,
                returncode=-1,
                stdout="",
                stderr="Execution timed out.",
                workflow_steps=list(self.workflow_logs)
            )
        except Exception as e:
            self.log_workflow(f"[Workflow Step 3 Failed] Subprocess error: {e}")
            return ExecutionResult(
                command=command,
                returncode=1,
                stdout="",
                stderr=str(e),
                workflow_steps=list(self.workflow_logs)
            )
