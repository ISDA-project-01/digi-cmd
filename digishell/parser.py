"""Parser module for Digi Shell input and instructor flags."""

import re
from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class ParsedCommand:
    raw_input: str
    clean_prompt: str
    direct_execution: bool = False  # '$'
    location: Optional[str] = None  # '@'
    teach: Optional[str] = None     # '!'
    help: bool = False               # '?'
    options: bool = False            # ':'
    workflow: bool = False           # ';'
    justify: bool = False            # '*'
    explain: bool = False            # '-'
    autofix: bool = False            # '#'
    install: bool = False            # '^'
    instructors: Set[str] = field(default_factory=set)


def parse_input(user_input: str) -> ParsedCommand:
    """
    Parses user input into clean prompt and instructor flags.
    Instructors are passed as suffix flags or special instructor tokens at/near end of input.
    Supported instructors:
    - '$': Non-AI command (direct execution)
    - '@': Location/directory context hint
    - '!': Teach command or rule
    - '?': Help and explanation
    - ':': Show all possible commands
    - ';': Show full workflow process
    - '*': AI emulsification/justification for output
    - '-': Meaning breakdown of command
    - '#': Auto-fix error recovery
    - '^': Dependency install/update flag
    """
    raw = user_input.strip()
    if not raw:
        return ParsedCommand(raw_input="", clean_prompt="")

    clean = raw
    instructors = set()
    location_val: Optional[str] = None
    teach_val: Optional[str] = None

    # Check for suffix instructor characters / tokens at the end of the prompt
    # Supported flag symbols: $, ?, :, ;, *, -, #, ^
    flag_symbols = {'$', '?', ':', ';', '*', '-', '#', '^'}

    # Process trailing instructor characters / whitespace
    clean_stripped = clean.rstrip()

    while clean_stripped:
        last_char = clean_stripped[-1]
        if last_char in flag_symbols:
            # Check if '-' is part of a CLI option flag like -la or --help vs suffix instructor
            if last_char == '-':
                # If preceding character is alphanumeric or hyphen, it's a CLI flag in the prompt (e.g. -la or --help)
                if len(clean_stripped) > 1 and (clean_stripped[-2].isalnum() or clean_stripped[-2] == '-'):
                    break

            instructors.add(last_char)
            clean_stripped = clean_stripped[:-1].rstrip()
        else:
            break

    clean = clean_stripped

    # Extract '@' location instructor if present
    loc_match = re.search(r'@\s*([^!]+)?$', clean)
    if loc_match:
        loc_str = loc_match.group(1)
        location_val = loc_str.strip() if loc_str else ""
        instructors.add('@')
        clean = clean[:loc_match.start()].rstrip()

    # Extract '!' teach instructor if present
    teach_match = re.search(r'!\s*(.+)$', clean)
    if teach_match:
        teach_str = teach_match.group(1)
        teach_val = teach_str.strip() if teach_str else ""
        instructors.add('!')
        clean = clean[:teach_match.start()].rstrip()

    # Assign boolean flags based on collected instructors
    direct_execution = '$' in instructors
    help_flag = '?' in instructors
    options_flag = ':' in instructors
    workflow_flag = ';' in instructors
    justify_flag = '*' in instructors
    explain_flag = '-' in instructors
    autofix_flag = '#' in instructors
    install_flag = '^' in instructors

    clean_prompt = clean.strip()
    clean_prompt = re.sub(r'\s+', ' ', clean_prompt)

    return ParsedCommand(
        raw_input=raw,
        clean_prompt=clean_prompt,
        direct_execution=direct_execution,
        location=location_val,
        teach=teach_val,
        help=help_flag,
        options=options_flag,
        workflow=workflow_flag,
        justify=justify_flag,
        explain=explain_flag,
        autofix=autofix_flag,
        install=install_flag,
        instructors=instructors
    )
