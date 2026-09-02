"""
Agentic Application Controller
"""

import os
import sys
import subprocess

class AppController:
    @staticmethod
    def open_application(app_name_or_path: str) -> str:
        app = app_name_or_path.strip()
        if sys.platform == "win32":
            try:
                os.startfile(app)
                return f"Opened application/file '{app}' via OS startfile."
            except Exception:
                subprocess.Popen(f"start {app}", shell=True)
                return f"Launched application '{app}'."
        elif sys.platform == "darwin":
            subprocess.Popen(["open", app])
            return f"Opened application '{app}' on macOS."
        else:
            subprocess.Popen(["xdg-open", app])
            return f"Opened application '{app}' on Linux."
