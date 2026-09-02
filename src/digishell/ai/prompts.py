"""
Ollama Prompt Engineering Utilities
"""

def build_command_prompt(user_query: str, os_info: str, cwd: str) -> str:
    return f"""
Operating System: {os_info}
Current Directory: {cwd}
User Intent: {user_query}

Translate the user intent into the exact executable terminal command for {os_info}.
Output only the command.
"""

def build_explanation_prompt(command: str) -> str:
    return f"Explain what the shell command '{command}' does in simple human language."

def build_justification_prompt(command: str, output: str) -> str:
    return f"Justify and verify the output of command '{command}':\nOutput:\n{output}\nProvide an AI emulsification/explanation of the output."

def build_fix_prompt(command: str, error_msg: str, os_info: str) -> str:
    return f"""
The command '{command}' failed on {os_info} with the following error:
{error_msg}

Suggest a corrected command to fix the issue. Output only the fixed command.
"""
