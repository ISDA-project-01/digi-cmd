"""
DigiShell Constants and Configuration Defaults
"""

import os

APP_NAME = "DigiShell"
VERSION = "0.1.0"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")

RAM_FULL_THRESHOLD_MB = 3072.0
RAM_LIMITED_THRESHOLD_MB = 2252.8
