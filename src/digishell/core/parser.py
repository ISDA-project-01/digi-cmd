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
        raw_input = user_input
        user_input = user_input.strip()
        if not user_input:
            return ParsedCommand("", "", [])

        # Non-AI direct pass through prefix/suffix check ($)
        if user_input.startswith("$") or user_input.endswith("$"):
            clean = user_input.strip("$").strip()
            return ParsedCommand(raw_input, clean, [("$", "")])

        instructors: List[Tuple[str, str]] = []
        clean_text = user_input

        # Extract @ location instructor if present
        at_pos = clean_text.find('@')
        if at_pos != -1:
            before_at = clean_text[:at_pos]
            after_at = clean_text[at_pos+1:]

            # Check if there are trailing instructor symbols after @ payload (e.g. *, #, ?, etc)
            inst_match = re.search(r'\s+([$!\?:;\*\-#\^])(?:\s+(.*))?$', after_at)
            if inst_match and (inst_match.group(1) in INSTRUCTOR_CHARS or inst_match.group(1) in ('*', '#', '?', '!', ':', ';', '^')):
                loc_and_rest = after_at[:inst_match.start()].strip()
                rest = after_at[inst_match.start():]
            else:
                loc_and_rest = after_at.strip()
                rest = ""

            loc_match = re.match(r'^(?:(?:disk|drive)\s*)?([a-zA-Z0-9_\-\.:/\\]+(?:\s+(?:file|app)?\s*[:\-]*\s*[a-zA-Z0-9_\-\.]+)?)(.*)$', loc_and_rest, re.IGNORECASE)
            if loc_match:
                loc_payload = loc_match.group(1).strip()
                trailing_q = loc_match.group(2).strip()
            else:
                loc_payload = loc_and_rest
                trailing_q = ""

            instructors.append(("@", loc_payload))

            if rest:
                pattern = r'([$@!\?:;\*\-#\^])\s*([^$@!\?:;\*\-#\^]*)'
                matches = re.findall(pattern, rest)
                for sym, payload in matches:
                    instructors.append((sym, payload.strip()))

            # Determine clean text
            file_part = re.search(r'(?:file|app)\s*[:\-]*\s*([a-zA-Z0-9_\-\.]+)', loc_payload, re.IGNORECASE)
            fname = file_part.group(1) if file_part else None
            if fname and fname.startswith('file-'):
                fname = fname[5:]

            clean_parts = [before_at.strip()]
            if fname and fname not in before_at and fname not in trailing_q:
                clean_parts.append(fname)
            if trailing_q:
                clean_parts.append(trailing_q)

            clean_text = " ".join(p for p in clean_parts if p).strip()
            clean_text = re.sub(r'\s+', ' ', clean_text)

        else:
            # No @ instructor
            pattern = r'([$@!\?:;\*\-#\^])\s*([^$@!\?:;\*\-#\^]*)'
            first_inst_idx = len(user_input)

            for i, char in enumerate(user_input):
                if char in INSTRUCTOR_CHARS:
                    is_prev_space = (i == 0 or user_input[i-1].isspace())
                    if is_prev_space:
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

        return ParsedCommand(raw_input, clean_text, instructors)
