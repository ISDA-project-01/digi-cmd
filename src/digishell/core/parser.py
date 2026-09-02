"""
DigiShell Command Parser and Instructor Extractor
"""

import re
from typing import List, Tuple

INSTRUCTOR_CHARS = set(['$', '@', '!', '?', ':', ';', '*', '#', '^'])

class ParsedCommand:
    def __init__(self, raw_input: str, clean_text: str, instructors: List[Tuple[str, str]]):
        self.raw_input = raw_input
        self.clean_text = clean_text  # Command or query without instructors
        self.instructors = instructors  # List of (instructor_symbol, payload/argument)

    def has_instructor(self, symbol: str) -> bool:
        return any(s == symbol for s, _ in self.instructors)

    def get_instructor_payload(self, symbol: str) -> str:
        payloads = [p for s, p in self.instructors if s == symbol]
        return payloads[0] if payloads else ""

class CommandParser:
    @staticmethod
    def parse(user_input: str) -> ParsedCommand:
        user_input = user_input.strip()
        if not user_input:
            return ParsedCommand("", "", [])

        # Non-AI direct pass through prefix/suffix check ($)
        if user_input.startswith("$") or user_input.endswith("$"):
            clean = user_input.strip("$").strip()
            return ParsedCommand(user_input, clean, [("$", "")])

        instructors: List[Tuple[str, str]] = []

        # Find position of instructor block starting with an instructor character
        # Instructors are $ @ ! ? : ; * - # ^
        pattern = r'([$@!\?:;\*\-#\^])\s*([^$@!\?:;\*\-#\^]*)'

        first_inst_idx = len(user_input)

        for i, char in enumerate(user_input):
            if char in INSTRUCTOR_CHARS:
                first_inst_idx = i
                break
            elif char == '-':
                # Dash is an instructor ONLY if preceded by space and NOT followed immediately by word chars (like -la, -m, --help)
                is_prev_space = (i > 0 and user_input[i-1].isspace())
                is_flag = (i < len(user_input) - 1 and user_input[i+1].isalnum())
                if is_prev_space and not is_flag:
                    first_inst_idx = i
                    break

        clean_text = user_input[:first_inst_idx].strip()
        instructor_part = user_input[first_inst_idx:]

        if instructor_part:
            matches = re.findall(pattern, instructor_part)
            for sym, payload in matches:
                instructors.append((sym, payload.strip()))

        if not clean_text and not instructors:
            clean_text = user_input

        return ParsedCommand(user_input, clean_text, instructors)
