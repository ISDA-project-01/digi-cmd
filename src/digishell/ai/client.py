"""
Local Ollama qwen2.5:3b Client and Fallback Command Engine
"""

import re
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

    def translate_natural_language(self, query: str, os_type: str = "windows", target_path: Optional[str] = None) -> str:
        if self.client.is_available():
            prompt = f"Convert the following instruction into a single, executable {os_type} shell command. Output ONLY the raw executable command without codeblocks, markdown, or explanation."
            if target_path:
                prompt += f"\nTarget Path: {target_path}"
            prompt += f"\nQuery: {query}"
            try:
                cmd = self.client.generate(prompt)
                # Clean code blocks if present
                cmd = cmd.replace("```bash", "").replace("```powershell", "").replace("```cmd", "").replace("```", "").strip()
                return cmd
            except Exception:
                pass

        # Rule-based offline translation fallback
        return self._offline_translate(query, os_type, target_path)

    def _offline_translate(self, query: str, os_type: str, target_path: Optional[str] = None) -> str:
        q = query.lower().strip()
        is_win = os_type.lower() in ("windows", "win32", "nt")
        py_cmd = "python" if is_win else "python3"

        # Extract file path
        filePath = target_path
        if not filePath:
            m = re.search(r'([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)', query)
            if m:
                filePath = m.group(1)
            else:
                filePath = "testing.txt"

        filePath = filePath.replace('\\', '/')

        # 1. Host file/directory to local network
        if "host" in q or "serve" in q:
            port = 8000
            m_port = re.search(r'port\s*(\d+)', q)
            if m_port:
                port = m_port.group(1)
            return f"{py_cmd} -m http.server {port}"

        # 2. Rewrite file
        if "rewrite" in q or "overwrite" in q:
            if "india" in q:
                text = "India is a vibrant democracy in South Asia with a rich history spanning thousands of years, from the ancient Indus Valley Civilization to its independence in 1947.\\n"
                return f'{py_cmd} -c "open(\'{filePath}\', \'w\').write(\'{text}\')"'
            return f'{py_cmd} -c "open(\'{filePath}\', \'w\').write(\'Updated content.\\n\')"'

        # 3. Write features / specifications
        if "write" in q and ("feature" in q or "system" in q or "specification" in q or "spec" in q):
            py_code = (
                "import platform, psutil; "
                "content = 'DigiShell System Features & Specifications:\\n' "
                "+ 'OS: ' + platform.system() + ' ' + platform.release() + '\\n' "
                "+ 'Architecture: ' + platform.machine() + '\\n' "
                "+ 'Python: ' + platform.python_version() + '\\n' "
                "+ 'CPU Cores: ' + str(psutil.cpu_count()) + '\\n' "
                "+ 'RAM Available: ' + str(psutil.virtual_memory().available // (1024*1024)) + ' MB\\n'; "
                f"open('{filePath}', 'w').write(content)"
            )
            return f'{py_cmd} -c "{py_code}"'

        # 4. Create file
        if "create" in q or "make file" in q or "touch" in q:
            return f'type nul > "{filePath}"' if is_win else f'touch "{filePath}"'

        # 5. Show / display / cat file
        if "show" in q or "cat" in q or "display" in q or "read" in q or "view" in q:
            return f'type "{filePath}"' if is_win else f'cat "{filePath}"'

        # Fallbacks
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
