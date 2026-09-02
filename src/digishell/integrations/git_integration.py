"""
Git & GitHub Integration Commands
"""

def build_git_command(action: str, repo_or_file: str = "") -> str:
    if action == "status":
        return "git status"
    elif action == "commit":
        return f'git commit -m "{repo_or_file or "update"}"'
    elif action == "push":
        return "git push"
    elif action == "gh_pr":
        return "gh pr list"
    return f"git {action} {repo_or_file}".strip()
