"""
OS/Kernel Level Memory Manager
Calculates available RAM and manages Full Mode (3GB+ free) vs Limited Mode (2.2GB free)
"""

import psutil

class MemoryManager:
    @staticmethod
    def get_available_memory_mb() -> float:
        mem = psutil.virtual_memory()
        return mem.available / (1024 * 1024)

    @classmethod
    def determine_mode(cls) -> str:
        avail = cls.get_available_memory_mb()
        if avail >= 3072.0:
            return "full"
        elif avail >= 2252.8:
            return "limited"
        else:
            return "minimal"

    @classmethod
    def get_memory_stats(cls) -> dict:
        mem = psutil.virtual_memory()
        return {
            "total_mb": round(mem.total / (1024 * 1024), 2),
            "available_mb": round(mem.available / (1024 * 1024), 2),
            "percent_used": mem.percent,
            "mode": cls.determine_mode()
        }
