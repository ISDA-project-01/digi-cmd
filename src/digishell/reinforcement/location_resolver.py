"""
Reinforcement Location Resolver
Handles syntax like '@ disk may be D and file app.py' or 'open app.py @D'
Resolves true path like 'D://new/py/app.py' via recursive path searching with depth limits.
"""

import os
import re
from typing import Optional

class LocationResolver:
    @staticmethod
    def resolve_location(location_hint: str) -> Optional[str]:
        if not location_hint:
            return None

        # Parse disk letter if present (e.g., 'disk may be D' -> 'D:', or '@D')
        drive_match = re.search(r'(?:disk|drive)?\s*(?:may be|=|is)?\s*([a-zA-Z]):?', location_hint, re.IGNORECASE)
        target_drive = f"{drive_match.group(1).upper()}:\\" if drive_match else os.getcwd()

        # Parse target filename (e.g. 'file app.py' or 'app.py')
        file_match = re.search(r'(?:file|app)\s+([a-zA-Z0-9_\-\.]+)', location_hint, re.IGNORECASE)
        filename = file_match.group(1) if file_match else None

        if not filename:
            tokens = location_hint.split()
            for t in tokens:
                if "." in t and not t.endswith(":"):
                    filename = t
                    break

        if not filename:
            return target_drive if os.path.exists(target_drive) else None

        search_root = target_drive if os.path.exists(target_drive) else os.getcwd()

        # Safe directory walk with max depth limit (3 levels) to avoid drive root hangs
        try:
            max_depth = 3
            initial_depth = search_root.rstrip(os.sep).count(os.sep)

            for root, dirs, files in os.walk(search_root):
                # Skip heavy or system folders
                dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ('node_modules', '$recycle.bin', 'system volume information', 'windows', 'program files')]

                current_depth = root.rstrip(os.sep).count(os.sep) - initial_depth
                if current_depth > max_depth:
                    continue

                if filename in files:
                    return os.path.join(root, filename)
        except Exception:
            pass

        return os.path.join(search_root, filename)
