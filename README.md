# Digi Shell (CMD with AI)

Digi Shell is an AI-powered command shell built in Python designed to work with local LLM Ollama (`qwen2.5:3b`). It translates natural language and tool-specific requests (Windows/Linux/macOS commands, `nmap`, `wireshark`, `git`, `gh`, etc.) into executable commands, with support for instruction modifiers (suffixes) and auto-correction workflows.

## Features & Instruction Modifiers Supported:
- `$` - Direct execution (Non-AI command).
- `@` - Location/directory context resolution (searches and resolves file/directory locations even if approximate).
- `!` - Teach mode (teaches AI custom commands or workflows for future use).
- `?` - Help & explanation (explains commands/options).
- `:` - Multi-command options (lists all possible candidate commands for ambiguous requests).
- `;` - Process workflow details (shows step-by-step reasoning and execution process).
- `*` - Output analysis / justification (AI explains command output).
- `-` - Command meaning breakdown (explains flags and components of the generated command).
- `#` - Auto-fix error recovery (analyzes errors, applies reinforcement logic, auto-fixes and re-executes).
- `^` - Dependency installer / updater (identifies missing tools and prompts/installs required dependencies).

## Quick Start

```bash
pip install -e .
digishell
```

Or run directly:

```bash
python3 -m digishell.cli
```
