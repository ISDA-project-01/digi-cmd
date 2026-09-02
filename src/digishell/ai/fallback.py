"""
Offline Heuristics & Rule-based Command Fallback Engine
"""

class OfflineEngine:
    @staticmethod
    def fallback_parse(query: str) -> str:
        q = query.strip().lower()
        if "make directory" in q or "mkdir" in q:
            folder = q.replace("make directory", "").replace("mkdir", "").strip()
            return f"mkdir {folder or 'new_folder'}"
        if "remove file" in q or "delete" in q:
            target = q.replace("remove file", "").replace("delete", "").strip()
            return f"rm {target}"
        if "check ports" in q or "open ports" in q:
            return "netstat -ano"
        if "who am i" in q or "current user" in q:
            return "whoami"
        return query
