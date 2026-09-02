"""
Instructor Dispatcher
"""

from typing import List, Tuple, Dict, Any
from digishell.core.context import ShellContext
from digishell.ai.client import AICommandEngine
from digishell.instructors.handlers import InstructorRegistry

class InstructorDispatcher:
    def __init__(self, context: ShellContext, engine: AICommandEngine):
        self.registry = InstructorRegistry(context, engine)

    def process_instructors(self, instructors: List[Tuple[str, str]], command: str, output: str = "", error: str = "") -> List[Dict[str, Any]]:
        results = []
        for sym, payload in instructors:
            res = self.registry.handle_symbol(sym, payload, command, output, error)
            results.append(res)
        return results
