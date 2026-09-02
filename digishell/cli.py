"""Command Line Interface and REPL shell loop for Digi Shell."""

import os
import sys
import platform
from digishell.parser import parse_input
from digishell.ai_engine import AIEngine
from digishell.teach import TeachManager
from digishell.reinforcement import ReinforcementManager
from digishell.dependency import DependencyManager
from digishell.executor import CommandExecutor


class DigiShellCLI:
    def __init__(self):
        self.ai = AIEngine()
        self.teach = TeachManager()
        self.reinforcement = ReinforcementManager(ai_engine=self.ai)
        self.dependency = DependencyManager()
        self.executor = CommandExecutor()

    def print_banner(self):
        print("=" * 65)
        print(" DIGI SHELL - AI Master CMD Shell (qwen2.5:3b local LLM)")
        print(" Instructors: $ (direct) | @ (location) | ! (teach) | ? (help)")
        print("              : (options)| ; (workflow)| * (justify)| - (explain)")
        print("              # (autofix)| ^ (deps)")
        print(" Type 'exit' or 'quit' to close.")
        print("=" * 65)

    def process_command(self, raw_input: str) -> None:
        if not raw_input.strip():
            return

        parsed = parse_input(raw_input)

        # Handle '!' Teach instructor
        if '!' in parsed.instructors and parsed.teach:
            teach_msg = self.teach.add_rule(parsed.teach)
            print(f"[DigiShell] {teach_msg}")
            if not parsed.clean_prompt:
                return

        # Handle '^' Dependency installer check instructor
        if '^' in parsed.instructors:
            target = parsed.clean_prompt or parsed.raw_input
            status, msg, install_cmd = self.dependency.process_dependency_flag(target)
            print(f"[DigiShell Dependency Check] {msg}")
            if install_cmd:
                choice = input(f"Do you want to run install command `{install_cmd}`? [y/N]: ").strip().lower()
                if choice == 'y':
                    res = self.executor.execute(install_cmd)
                    print(res.stdout or res.stderr)
            if not parsed.clean_prompt or not status:
                return

        # Handle '?' Help instructor
        if parsed.help:
            subject = parsed.clean_prompt or "Digi Shell"
            help_text = self.ai.get_help(subject)
            print(f"\n--- DigiShell Help & Guide for '{subject}' ---")
            print(help_text)
            print("-" * 50)

        # Handle ':' Options instructor
        if parsed.options:
            options = self.ai.list_options(parsed.clean_prompt)
            print(f"\n--- Candidate Commands for '{parsed.clean_prompt}' ---")
            for idx, opt in enumerate(options, 1):
                print(f" {idx}. {opt}")
            print("-" * 50)

        # Determine target command to execute
        target_cmd = ""
        resolved_loc = None

        if parsed.direct_execution:
            target_cmd = parsed.clean_prompt
        else:
            # Check taught rules first
            matched_rule = self.teach.match_rule(parsed.clean_prompt)
            if matched_rule:
                print(f"[DigiShell] Matched taught rule -> {matched_rule}")
                target_cmd = matched_rule
            else:
                # Handle '@' Location instructor
                if parsed.location:
                    resolved_loc = self.reinforcement.resolve_location(parsed.location)
                    print(f"[DigiShell Location Resolved] {parsed.location} -> {resolved_loc}")

                target_cmd = self.ai.generate_command(parsed.clean_prompt, context=resolved_loc)

        if not target_cmd:
            print("[DigiShell] Unable to generate command.")
            return

        # Handle '-' Command breakdown explanation instructor
        if parsed.explain:
            explanation = self.ai.explain_command(target_cmd)
            print(f"\n--- Command Breakdown ({target_cmd}) ---")
            print(explanation)
            print("-" * 50)

        # Execute command
        print(f"[DigiShell Executing] > {target_cmd}")
        res = self.executor.execute(target_cmd, show_workflow=parsed.workflow)

        # Print outputs
        if res.stdout:
            print(res.stdout, end="")
        if res.stderr:
            print(res.stderr, end="", file=sys.stderr)

        # Handle ';' Workflow details instructor
        if parsed.workflow:
            print("\n--- Process Workflow Details ---")
            for step in res.workflow_steps:
                print(step)
            print("-" * 50)

        # Handle '#' Auto-fix error reinforcement instructor
        if res.returncode != 0 and parsed.autofix:
            print("\n[DigiShell Reinforcement Auto-Fix Initiated...]")
            fixed_cmd, reasoning = self.reinforcement.reinforce_and_fix(
                failed_cmd=target_cmd,
                stdout=res.stdout,
                stderr=res.stderr
            )
            print(f"[DigiShell Fix Reasoning] {reasoning}")
            print(f"[DigiShell Re-Executing Fixed Command] > {fixed_cmd}")
            res_fixed = self.executor.execute(fixed_cmd, show_workflow=parsed.workflow)
            if res_fixed.stdout:
                print(res_fixed.stdout, end="")
            if res_fixed.stderr:
                print(res_fixed.stderr, end="", file=sys.stderr)
            res = res_fixed

        # Handle '*' Output analysis / justification instructor
        if parsed.justify:
            justification = self.ai.justify_output(res.command, res.stdout, res.stderr)
            print(f"\n--- Output Analysis & Justification (*) ---")
            print(justification)
            print("-" * 50)

    def run_repl(self):
        self.print_banner()
        while True:
            try:
                cwd = os.getcwd()
                prompt_str = f"digi-shell:{cwd}$ "
                user_input = input(prompt_str)
                if user_input.strip().lower() in ("exit", "quit"):
                    print("Exiting Digi Shell.")
                    break
                self.process_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting Digi Shell.")
                break


def main():
    cli = DigiShellCLI()
    if len(sys.argv) > 1:
        # One-off command invocation
        cli.process_command(" ".join(sys.argv[1:]))
    else:
        cli.run_repl()


if __name__ == "__main__":
    main()
