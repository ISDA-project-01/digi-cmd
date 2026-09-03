"""
Local Ollama qwen2.5:3b Client and Fallback Command Engine
"""

import ollama
from typing import Dict, Any, Optional, List
from digishell.config.settings import OLLAMA_HOST, DEFAULT_MODEL
from digishell.config.prompts import SYSTEM_PROMPT

class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = DEFAULT_MODEL):
        self.host = host.rstrip('/')
        self.model = model

    def is_available(self) -> bool:
        try:
            ollama.list()
            return True
        except Exception:
            return False

    def generate(self, prompt: str, system: str = SYSTEM_PROMPT) -> str:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.get('message', {}).get('content', '').strip()
        except Exception as e:
            raise RuntimeError(f"Ollama connection error: {e}")

class AICommandEngine:
    def __init__(self, client: Optional[OllamaClient] = None):
        self.client = client or OllamaClient()

    def translate_natural_language(self, query: str, os_type: str = "windows") -> str:
        if self.client.is_available():
            prompt = f"Convert the following instruction into a single, executable {os_type} shell command. Output ONLY the raw executable command without codeblocks, markdown, or explanation.\nQuery: {query}"
            try:
                cmd = self.client.generate(prompt)
                # Clean code blocks if present
                cmd = cmd.replace("```bash", "").replace("```powershell", "").replace("```cmd", "").replace("```", "").strip()
                return cmd
            except Exception:
                pass

        # Rule-based offline translation fallback
        return self._offline_translate(query, os_type)

    def _offline_translate(self, query: str, os_type: str) -> str:
        q = query.lower()
        is_win = os_type.lower() in ("windows", "win32", "nt")

        if "list" in q or "dir" in q or "ls" in q or "show files" in q:
            return "dir" if is_win else "ls -la"
        if "process" in q or "task" in q:
            return "tasklist" if is_win else "ps aux"
        if "network" in q or "ip" in q or "ipconfig" in q or "ifconfig" in q:
            return "ipconfig /all" if is_win else "ifconfig -a"
        if "ping" in q:
            parts = q.split()
            host = parts[-1] if len(parts) > 1 and "." in parts[-1] else "google.com"
            return f"ping {host}"
        if "git status" in q or "git" in q:
            return "git status"
        if "nmap" in q:
            return "nmap 127.0.0.1"
        if "open" in q:
            parts = q.split()
            target = parts[-1] if len(parts) > 1 else ""
            return f"start {target}" if is_win else f"xdg-open {target}"

        return query
