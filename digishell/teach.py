"""Teach module for Digi Shell ('!' instructor) storing custom rules and workflows."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class TeachManager:
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".digishell"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.rules_file = self.config_dir / "taught_rules.json"
        self.rules: Dict[str, Any] = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        if self.rules_file.exists():
            try:
                with open(self.rules_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_rules(self) -> None:
        try:
            with open(self.rules_file, "w", encoding="utf-8") as f:
                json.dump(self.rules, f, indent=2)
        except Exception as e:
            print(f"[!] Warning: Failed to save taught rules: {e}")

    def add_rule(self, teach_input: str) -> str:
        """
        Processes teach input ('!' flag).
        Formats supported:
        - "alias=command" (e.g., "sysinfo = uname -a && lscpu")
        - "trigger -> action" (e.g., "clean logs -> rm -rf /tmp/*.log")
        - Natural language description / instruction rule.
        """
        raw = teach_input.strip()
        if not raw:
            return "No rule provided to teach."

        if "=" in raw:
            alias, target = raw.split("=", 1)
            alias = alias.strip().lower()
            target = target.strip()
            self.rules[alias] = target
            self.save_rules()
            return f"[!] Taught Digi Shell mapping: '{alias}' -> '{target}'"
        elif "->" in raw:
            trigger, target = raw.split("->", 1)
            trigger = trigger.strip().lower()
            target = target.strip()
            self.rules[trigger] = target
            self.save_rules()
            return f"[!] Taught Digi Shell workflow: '{trigger}' -> '{target}'"
        else:
            # General rule or preference
            rule_key = f"rule_{len(self.rules) + 1}"
            self.rules[rule_key] = raw
            self.save_rules()
            return f"[!] Taught Digi Shell rule saved: '{raw}'"

    def match_rule(self, prompt: str) -> Optional[str]:
        """Checks if user prompt matches a taught command mapping or rule."""
        p = prompt.strip().lower()
        if p in self.rules:
            val = self.rules[p]
            if isinstance(val, str):
                return val

        # Partial matching for triggers
        for key, value in self.rules.items():
            if key in p and isinstance(value, str):
                return value
        return None

    def get_all_rules(self) -> Dict[str, Any]:
        return self.rules
