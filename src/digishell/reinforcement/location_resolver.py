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
    def resolve_location(location_hint: str, query: str = None) -> Optional[str]:
        if not location_hint:
            return None

        # Parse disk letter if present (e.g., 'disk may be D' -> 'D:', or '@D')
        drive_match = re.search(r'(?:disk|drive)?\s*(?:may be|=|is)?\s*([a-zA-Z]):?', location_hint, re.IGNORECASE)
        target_drive_letter = drive_match.group(1).upper() if drive_match else None

        # Parse target filename (e.g. 'file app.py', 'file - testing.txt', or 'app.py')
        file_match = re.search(r'(?:file|app)\s*[:\-]*\s*([a-zA-Z0-9_\-\.]+)', location_hint, re.IGNORECASE)
        filename = file_match.group(1) if file_match else None

        if filename and filename.startswith('file-'):
            filename = filename[5:]

        if not filename:
            tokens = location_hint.split()
            for t in tokens:
                if "." in t and not t.endswith(":"):
                    filename = t
                    break

        if not filename and query:
            q_file_match = re.search(r'(?:file|name)\s*[:\-]*\s*([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)', query, re.IGNORECASE)
            if q_file_match:
                filename = q_file_match.group(1)
            else:
                ext_match = re.search(r'([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)', query)
                if ext_match:
                    filename = ext_match.group(1)

        search_root = f"{target_drive_letter}:\\" if (target_drive_letter and os.path.exists(f"{target_drive_letter}:\\")) else os.getcwd()

        if not filename:
            return search_root

        # Safe directory walk with max depth limit (3 levels) to avoid drive root hangs
        try:
            max_depth = 3
            initial_depth = search_root.rstrip(os.sep).count(os.sep)

            for root, dirs, files in os.walk(search_root):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ('node_modules', '$recycle.bin', 'system volume information', 'windows', 'program files')]

                current_depth = root.rstrip(os.sep).count(os.sep) - initial_depth
                if current_depth > max_depth:
                    continue

                if filename in files:
                    return os.path.join(root, filename)
        except Exception:
            pass

        if search_root.endswith(":\\"):
            return os.path.join(search_root, filename)
        else:
            return os.path.abspath(filename)
