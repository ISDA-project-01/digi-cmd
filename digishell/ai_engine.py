"""AI Engine for Digi Shell using local Ollama model qwen2.5:3b with heuristic fallback."""

import json
import os
import platform
import urllib.error
import urllib.request
from typing import Dict, List, Optional


class AIEngine:
    def __init__(self, model_name: str = "qwen2.5:3b", host: str = "http://localhost:11434"):
        self.model_name = os.getenv("DIGISHELL_MODEL", model_name)
        self.host = os.getenv("DIGISHELL_OLLAMA_HOST", host).rstrip('/')

    def _query_ollama(self, prompt: str, system: Optional[str] = None) -> Optional[str]:
        """Queries local Ollama API server."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    resp_data = json.loads(response.read().decode('utf-8'))
                    return resp_data.get("response", "").strip()
        except Exception:
            # Ollama not reachable or error, fallback will handle logic
            return None
        return None

    def generate_command(self, user_prompt: str, context: Optional[str] = None, OS_name: Optional[str] = None) -> str:
        """Translates natural language prompt into executable CLI command."""
        os_info = OS_name or f"{platform.system()} {platform.release()}"
        system_prompt = (
            "You are Digi Shell AI, an expert cross-platform command line assistant. "
            "Convert user requests into precise, executable terminal/shell commands for the target OS. "
            "Return ONLY the executable command string without markdown code blocks, explanation, or quotes."
        )
        full_prompt = f"Target OS: {os_info}\n"
        if context:
            full_prompt += f"Context/Location: {context}\n"
        full_prompt += f"User Request: {user_prompt}\nCommand:"

        ai_res = self._query_ollama(full_prompt, system=system_prompt)
        if ai_res:
            # Clean possible markdown formatting
            ai_res = ai_res.strip("`\n ")
            if ai_res.startswith("```"):
                ai_res = ai_res.strip("`").strip()
                if "\n" in ai_res:
                    ai_res = ai_res.split("\n", 1)[-1].strip()
            return ai_res

        # Fallback heuristic mapping if local Ollama is offline or unreachable
        return self._heuristic_command(user_prompt, context)

    def _heuristic_command(self, user_prompt: str, context: Optional[str] = None) -> str:
        p = user_prompt.lower()
        is_win = platform.system() == "Windows"

        if "list" in p or "ls" in p or "dir" in p or "show files" in p:
            cmd = "dir" if is_win else "ls -la"
        elif "open" in p or "run" in p or "exec" in p:
            file_target = user_prompt.split()[-1]
            if is_win:
                cmd = f"start {file_target}"
            elif platform.system() == "Darwin":
                cmd = f"open {file_target}"
            else:
                cmd = f"python3 {file_target}" if file_target.endswith(".py") else f"./{file_target}"
        elif "nmap" in p or "scan" in p:
            cmd = f"nmap -sV {user_prompt.split()[-1]}" if " " in user_prompt else "nmap -sV localhost"
        elif "git" in p:
            cmd = user_prompt if user_prompt.startswith("git") else f"git status"
        elif "wireshark" in p or "tshark" in p:
            cmd = "tshark -i 1"
        else:
            cmd = user_prompt

        if context and "@" not in user_prompt:
            # If target location resolved, append or cd
            if context.startswith("cd "):
                cmd = f"{context} && {cmd}"

        return cmd

    def explain_command(self, command: str) -> str:
        """Explains flags and components of the command ('-' flag)."""
        prompt = f"Explain the structure, subcommands, and flags of this CLI command in detail: `{command}`"
        system = "Provide a concise breakdown of the CLI command and its arguments."
        res = self._query_ollama(prompt, system=system)
        if res:
            return res
        return f"Breakdown for '{command}': Executable shell command with provided arguments."

    def list_options(self, user_prompt: str) -> List[str]:
        """Lists candidate commands for ambiguous request (':' flag)."""
        prompt = f"List 3-5 distinct CLI command variations or alternatives to accomplish: '{user_prompt}'. Output one command per line."
        system = "Output only the commands, one per line."
        res = self._query_ollama(prompt, system=system)
        if res:
            lines = [line.strip("- *`") for line in res.split("\n") if line.strip()]
            return lines[:5]

        # Fallback options
        return [
            f"{user_prompt}",
            f"{user_prompt} --help",
            f"python3 -m {user_prompt}"
        ]

    def justify_output(self, command: str, stdout: str, stderr: str) -> str:
        """Analyzes command execution output ('*' flag)."""
        prompt = f"Command: `{command}`\nStdout: {stdout}\nStderr: {stderr}\nProvide a concise analysis/justification of what this command achieved or produced."
        res = self._query_ollama(prompt)
        if res:
            return res
        return f"Output analysis: Executed `{command}`. Returned stdout length {len(stdout)} chars, stderr length {len(stderr)} chars."

    def get_help(self, subject: str) -> str:
        """Provides full help and explanation ('?' flag)."""
        prompt = f"Provide standard usage guide, description, and common examples for command or topic: '{subject}'"
        res = self._query_ollama(prompt)
        if res:
            return res
        return f"Help for '{subject}': Consult standard manual pages (`man {subject}` or `{subject} --help`)."
