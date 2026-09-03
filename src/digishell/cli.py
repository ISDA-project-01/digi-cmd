"""
DigiShell Main CLI Entry Point
"""

import sys
import os
import argparse
from digishell.core.context import ShellContext
from digishell.core.parser import CommandParser
from digishell.ai.client import AICommandEngine
from digishell.instructors.dispatcher import InstructorDispatcher
from digishell.executors.shell import CommandExecutor
from digishell.reinforcement.location_resolver import LocationResolver
from digishell.reinforcement.self_healing import SelfHealingEngine
from digishell.system.memory_manager import MemoryManager
from digishell.system.cpu_allocator import CpuOptimizer
from digishell.agentic.app_controller import AppController
from digishell.executors.installer import AutoInstaller

def main():
    parser = argparse.ArgumentParser(description="DigiShell AI Terminal Shell")
    parser.add_argument("--gui", choices=["tk", "webview"], help="Launch DigiShell in GUI mode")
    args = parser.parse_args()

    if args.gui == "tk":
        from digishell.ui.tkinter.tk_app import launch_tkinter
        launch_tkinter()
        return
    elif args.gui == "webview":
        from digishell.ui.webview.webview_app import launch_webview
        launch_webview()
        return

    # Optimize process priority
    CpuOptimizer.optimize_process_priority()

    context = ShellContext()
    ai_engine = AICommandEngine()
    dispatcher = InstructorDispatcher(context, ai_engine)
    healing_engine = SelfHealingEngine(context, ai_engine)

    # Check RAM mode
    mem_stats = MemoryManager.get_memory_stats()
    context.mode = mem_stats["mode"]

    print(f"=== DigiShell v0.1.0 [Model: qwen2.5:3b | Mode: {context.mode.upper()} ({mem_stats['available_mb']}MB free)] ===")
    print("Type 'exit' or 'quit' to end session. Type 'help' or append instructors ($, @, !, ?, :, ;, *, -, #, ^).\n")

    while True:
        try:
            prompt_str = f"digishell [{os.path.basename(context.cwd) or context.cwd}]> "
            user_input = input(prompt_str).strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Exiting DigiShell.")
                break

            context.clear_workflow()
            parsed = CommandParser.parse(user_input)

            # Check @ location instructor payload for path resolution
            resolved_path = None
            if parsed.has_instructor("@"):
                loc_payload = parsed.get_instructor_payload("@")
                resolved_path = LocationResolver.resolve_location(loc_payload, parsed.clean_text)
                if resolved_path:
                    context.log_workflow(f"Location resolved: {resolved_path}")
                    print(f"[DigiShell Reinforcement Path] Resolved target path: {resolved_path}")

            # Translate command using AI or direct pass ($ instructor)
            if parsed.has_instructor("$"):
                cmd_to_run = parsed.clean_text
                context.log_workflow("Direct command bypass ($ symbol detected).")
            else:
                context.log_workflow(f"Translating query with AI: '{parsed.clean_text}'")
                cmd_to_run = ai_engine.translate_natural_language(parsed.clean_text, sys.platform, target_path=resolved_path)

            print(f"[DigiShell Executing]: {cmd_to_run}")

            # Check if command is opening an app
            if cmd_to_run.startswith("open ") or cmd_to_run.startswith("start "):
                app_target = cmd_to_run.split(" ", 1)[1]
                msg = AppController.open_application(app_target)
                print(msg)
                code, stdout, stderr = 0, msg, ""
            else:
                # Execute with self-healing if '#' instructor present
                if parsed.has_instructor("#"):
                    code, stdout, stderr = healing_engine.execute_with_healing(cmd_to_run)
                else:
                    code, stdout, stderr = CommandExecutor.execute(cmd_to_run, context.cwd)

            context.last_exit_code = code
            context.last_output = stdout
            context.last_error = stderr

            if stdout:
                print(stdout)
            if stderr:
                print(f"Error: {stderr}", file=sys.stderr)

            # Check '^' instructor for auto-installation
            if parsed.has_instructor("^"):
                pkg_payload = parsed.get_instructor_payload("^")
                inst_res = AutoInstaller.install_or_update(pkg_payload)
                print(f"[DigiShell Auto-Install]: {inst_res}")

            # Dispatch other instructors
            if parsed.instructors:
                results = dispatcher.process_instructors(parsed.instructors, cmd_to_run, stdout, stderr)
                for res in results:
                    if res["symbol"] not in ("$", "@", "#", "^"):
                        print(f"[{res['symbol']} Instructor]: {res['message']}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting DigiShell.")
            break

if __name__ == "__main__":
    main()
