# DigiShell README

# DigiShell - AI-Powered Command Line Shell

DigiShell is an ultra-agentic, AI-enhanced command-line interface for Windows, Linux, and macOS.
It integrates with a local Ollama instance running `qwen2.5:3b` to convert human/simple/social language queries into proper executable OS and tool commands.

## Key Features

1. **Multi-Platform & Multi-Tool Support**: Windows, Linux, macOS, Git/GitHub CLI, Nmap, Wireshark/TShark, etc.
2. **Command Analysis**: AI translates natural language queries into exact OS commands.
3. **10 Command Instructors**:
   - `$` : Non-AI direct command execution
   - `@` : Mention location/directory/area
   - `!` : Teach/alias commands
   - `?` : Help and explanation
   - `:` : Show all possible alternative commands
   - `;` : Show full workflow processes done
   - `*` : AI emulsification/justification for output
   - `-` : Detailed meaning & syntax breakdown
   - `#` : Auto-fix error if occurs
   - `^` : Install/update needed tools
4. **Reinforcement Path Resolver**: Resolves paths from vague location instructions (e.g., `"open app.py @ disk may be D and file app.py"`).
5. **Self-Healing Execution (`#`)**: Automatically attempts fix and retry on command errors.
6. **Ultra Agentic Power**: Direct operating of applications and system tasks.
7. **Resource & Memory Optimization**:
   - Full-fledged functionality mode with 3GB free RAM
   - Limited/simple functionality mode with 2.2GB free RAM
   - OS/Kernel process priority allocation
8. **Multiple Interfaces**:
   - Terminal Shell CLI (`digishell`)
   - Tkinter Desktop Window (`python -m digishell.cli --gui tk`)
   - PyWebView GUI Control Panel (`python -m digishell.cli --gui webview`)
   - Launcher scripts (`app.bat` for Windows and `app.sh` for Unix)

## Installation & Setup

```bash
pip install -e .
```

## Running DigiShell

- Command line: `digishell` or `app.bat` (Windows) / `./app.sh` (Unix)
- Tkinter GUI: `digishell --gui tk`
- PyWebView GUI: `digishell --gui webview`

## Running Tests

```bash
python3 -m unittest discover tests
```
