"""
Package & Tool Installer Handler for '^' Instructor
"""

import sys
import subprocess

class AutoInstaller:
    @staticmethod
    def install_or_update(target: str) -> str:
        if not target:
            return "No package specified for installation."

        # Determine package manager
        if sys.platform == "win32":
            cmd = f"winget install {target} --accept-source-agreements --accept-package-agreements || choco install {target} -y || pip install {target}"
        else:
            cmd = f"pip install {target} || sudo apt-get install -y {target} || brew install {target}"

        try:
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            if res.returncode == 0:
                return f"Successfully installed/updated '{target}':\n{res.stdout[:200]}"
            else:
                return f"Attempted installation of '{target}' with notice:\n{res.stderr[:200] or res.stdout[:200]}"
        except Exception as e:
            return f"Installation process exception for '{target}': {e}"
