"""
Self-Healing Workflow Execution Engine
"""

from digishell.core.context import ShellContext
from digishell.executors.shell import CommandExecutor
from digishell.ai.client import AICommandEngine

class SelfHealingEngine:
    def __init__(self, context: ShellContext, ai_engine: AICommandEngine):
        self.context = context
        self.ai_engine = ai_engine

    def execute_with_healing(self, command: str, max_retries: int = 1) -> tuple:
        self.context.log_workflow(f"Attempting command: {command}")
        code, stdout, stderr = CommandExecutor.execute(command, self.context.cwd)

        if code == 0:
            self.context.log_workflow("Execution succeeded.")
            return code, stdout, stderr

        self.context.log_workflow(f"Execution failed with code {code}. Error: {stderr}")

        # Self healing retry
        for attempt in range(max_retries):
            self.context.log_workflow(f"Self-healing retry attempt {attempt + 1}...")
            fixed_cmd = self.ai_engine.client.generate(f"Fix this command '{command}' which gave error: {stderr}") if self.ai_engine.client.is_available() else command
            if fixed_cmd and fixed_cmd != command:
                self.context.log_workflow(f"Attempting fixed command: {fixed_cmd}")
                code, stdout, stderr = CommandExecutor.execute(fixed_cmd, self.context.cwd)
                if code == 0:
                    self.context.log_workflow("Self-healing fix succeeded!")
                    return code, stdout, stderr

        return code, stdout, stderr
