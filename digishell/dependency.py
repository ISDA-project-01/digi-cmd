"""Dependency installer and checker module for Digi Shell ('^' instructor)."""

import platform
import shutil
import subprocess
from typing import List, Tuple, Optional


class DependencyManager:
    def __init__(self):
        self.os_type = platform.system()

    def check_tool_installed(self, tool_name: str) -> bool:
        """Checks if a binary executable is present in PATH."""
        return shutil.which(tool_name) is not None

    def get_install_command(self, tool_name: str) -> Optional[str]:
        """Determines appropriate package manager install command for given tool."""
        tool = tool_name.strip().lower()

        # Handle Python packages vs system binaries
        python_pkgs = {"playwright", "requests", "pytest", "numpy", "pandas", "flask", "django", "scapy"}
        if tool in python_pkgs or tool.startswith("python-"):
            return f"pip install --upgrade {tool}"

        if self.os_type == "Linux":
            if shutil.which("apt"):
                return f"sudo apt update && sudo apt install -y {tool}"
            elif shutil.which("dnf"):
                return f"sudo dnf install -y {tool}"
            elif shutil.which("pacman"):
                return f"sudo pacman -S --noconfirm {tool}"
        elif self.os_type == "Darwin":
            if shutil.which("brew"):
                return f"brew install {tool}"
        elif self.os_type == "Windows":
            if shutil.which("winget"):
                return f"winget install -e --id {tool}"
            elif shutil.which("choco"):
                return f"choco install -y {tool}"

        return None

    def process_dependency_flag(self, target: str) -> Tuple[bool, str, Optional[str]]:
        """
        Handles '^' instructor modifier.
        Returns (installed_status, status_message, install_cmd)
        """
        if not target:
            return False, "No package or tool target specified for '^' dependency check.", None

        tokens = target.split()
        tool_name = tokens[0]

        is_installed = self.check_tool_installed(tool_name)
        if is_installed:
            return True, f"Tool '{tool_name}' is already installed.", None

        install_cmd = self.get_install_command(tool_name)
        if install_cmd:
            return False, f"Tool '{tool_name}' is not installed. Recommended command: `{install_cmd}`", install_cmd
        else:
            return False, f"Tool '{tool_name}' is not installed and no default package manager was found.", None
