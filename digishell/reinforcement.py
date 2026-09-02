"""Reinforcement module for Digi Shell handling '@' location resolution and '#' auto-fix reinforcement loop."""

import json
import os
import platform
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


class ReinforcementManager:
    def __init__(self, ai_engine=None):
        self.ai_engine = ai_engine

    def resolve_location(self, location_query: str) -> Optional[str]:
        """
        Resolves location hints supplied with '@' (e.g., '@ disk may be D and file app.py', '@ app.py').
        Searches filesystem to locate file or directory matching query, performing reinforcement search.
        """
        if not location_query:
            return None

        query = location_query.strip()

        # Extract file/dir targets from location query
        # Example queries: "disk may be D and file app.py", "open app.py @D", "app.py"
        target_name = None
        file_match = re.search(r'(?:file\s+)?([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)', query)
        if file_match:
            target_name = file_match.group(1)
        else:
            words = [w for w in query.split() if len(w) > 1 and not w.lower() in ("disk", "may", "be", "file", "folder", "and", "in")]
            if words:
                target_name = words[-1]

        current_dir = Path.cwd()

        # Search local directory tree recursively first
        if target_name:
            for root, dirs, files in os.walk(current_dir):
                if target_name in files:
                    full_path = Path(root) / target_name
                    return str(full_path)
                if target_name in dirs:
                    full_path = Path(root) / target_name
                    return str(full_path)

        # Fallback search parent directory
        if target_name and current_dir.parent:
            for root, dirs, files in os.walk(current_dir.parent):
                # Restrict search depth
                rel_depth = len(Path(root).relative_to(current_dir.parent).parts)
                if rel_depth > 3:
                    continue
                if target_name in files or target_name in dirs:
                    return str(Path(root) / target_name)

        # Drive letter or explicit path hint check (e.g. D: or /d/)
        drive_match = re.search(r'([a-zA-Z]):', query)
        if drive_match and platform.system() == "Windows":
            drive = drive_match.group(1).upper()
            return f"{drive}:\\"

        return query

    def reinforce_and_fix(self, failed_cmd: str, stdout: str, stderr: str, OS_name: Optional[str] = None) -> Tuple[str, str]:
        """
        Reinforcement workflow for '#' auto-fix instructor.
        Analyzes execution failure and produces corrected command + reasoning.
        """
        os_info = OS_name or f"{platform.system()} {platform.release()}"

        if self.ai_engine:
            prompt = (
                f"Target OS: {os_info}\n"
                f"Failed Command: `{failed_cmd}`\n"
                f"Stderr Output: {stderr}\n"
                f"Stdout Output: {stdout}\n"
                f"Analyze the error, fix the command, and return JSON format with keys:\n"
                f'{{"explanation": "Reason for error", "fixed_command": "Corrected command"}}'
            )
            system = "You are a command line reinforcement debugger. Return ONLY valid JSON."
            response = self.ai_engine._query_ollama(prompt, system=system)
            if response:
                try:
                    # Strip markdown code blocks if present
                    clean_res = response.strip()
                    if "```" in clean_res:
                        clean_res = re.sub(r'```(?:json)?\n?', '', clean_res).strip('`').strip()
                    parsed = json.loads(clean_res)
                    fixed_cmd = parsed.get("fixed_command", "").strip()
                    explanation = parsed.get("explanation", "Auto-fixed error.")
                    if fixed_cmd:
                        return fixed_cmd, explanation
                except Exception:
                    pass

        # Fallback heuristic reinforcement fixes
        explanation = "Detected execution error; applying heuristic fix."
        fixed_cmd = failed_cmd

        if "command not found" in stderr.lower() or "is not recognized" in stderr.lower():
            binary = failed_cmd.split()[0]
            if binary == "python":
                fixed_cmd = failed_cmd.replace("python", "python3", 1)
                explanation = "Replaced 'python' with 'python3'."
            elif binary == "pip":
                fixed_cmd = failed_cmd.replace("pip", "pip3", 1)
                explanation = "Replaced 'pip' with 'pip3'."
            elif binary == "pip3":
                fixed_cmd = f"python3 -m {failed_cmd}"
                explanation = "Used 'python3 -m pip' invocation."
        elif "no such file or directory" in stderr.lower() or "cannot find the path" in stderr.lower():
            # Try finding filename in local path
            tokens = failed_cmd.split()
            for token in tokens:
                if "." in token and not token.startswith("-"):
                    resolved = self.resolve_location(token)
                    if resolved and resolved != token:
                        fixed_cmd = failed_cmd.replace(token, resolved)
                        explanation = f"Resolved file path '{token}' -> '{resolved}'."
                        break

        return fixed_cmd, explanation
