"""
Handlers for end-of-command instructors:
$ - non-AI command pass
@ - mention location/directory/area
! - teach custom command/alias
? - help & explanation
: - show all possible alternative commands
; - show full processes done with workflow
* - AI emulsification/justification for command output
- - detailed meanings
# - auto fix error if occurs
^ - install anything needed and update needed
"""

import sys
import subprocess
from typing import Dict, Any, List, Tuple
from digishell.core.context import ShellContext
from digishell.ai.client import AICommandEngine

class InstructorRegistry:
    def __init__(self, context: ShellContext, engine: AICommandEngine):
        self.context = context
        self.engine = engine

    def handle_symbol(self, symbol: str, payload: str, command: str, output: str = "", error: str = "") -> Dict[str, Any]:
        result = {"processed": True, "symbol": symbol, "message": ""}

        if symbol == "$":
            result["message"] = "Bypassed AI translation; direct execution."
        elif symbol == "@":
            result["message"] = f"Resolved location target: {payload}"
        elif symbol == "!":
            if "=" in payload:
                alias, real_cmd = payload.split("=", 1)
                self.context.learned_commands[alias.strip()] = real_cmd.strip()
                result["message"] = f"Learned command alias '{alias.strip()}' -> '{real_cmd.strip()}'"
            else:
                result["message"] = f"Learned command pattern: {payload}"
        elif symbol == "?":
            explanation = self.engine.client.generate(f"Explain what '{command}' does and how to use it.") if self.engine.client.is_available() else f"Help: '{command}' executes system command."
            result["message"] = f"Explanation for '{command}':\n{explanation}"
        elif symbol == ":":
            alts = [command, f"{command} --help", f"sudo {command}" if sys.platform != "win32" else f"powershell {command}"]
            result["message"] = f"Possible alternative commands for request:\n" + "\n".join(f"- {a}" for a in alts)
        elif symbol == ";":
            workflow = self.context.workflow_logs
            result["message"] = "Full processes done with workflow:\n" + ("\n".join(f"[{i+1}] {step}" for i, step in enumerate(workflow)) if workflow else "No workflow steps logged.")
        elif symbol == "*":
            justification = f"AI Emulsification & Justification:\nCommand '{command}' ran with exit code {self.context.last_exit_code}.\nOutput summary: {(output[:200] + '...') if len(output) > 200 else output}"
            result["message"] = justification
        elif symbol == "-":
            result["message"] = f"Detailed Meaning & Syntax Analysis:\nCommand: {command}\nPayload/Params: {payload or 'Default flags'}"
        elif symbol == "#":
            if error or self.context.last_error:
                err_text = error or self.context.last_error
                fixed_cmd = self.engine.client.generate(f"Fix this error for command '{command}': {err_text}") if self.engine.client.is_available() else command
                result["fixed_command"] = fixed_cmd
                result["message"] = f"Auto-fix suggested for error '{err_text[:50]}...': {fixed_cmd}"
            else:
                result["message"] = "No error detected to fix."
        elif symbol == "^":
            pkg = payload or command.split()[0] if command else "package"
            result["install_target"] = pkg
            result["message"] = f"Initiating install/update check for '{pkg}'..."

        return result
