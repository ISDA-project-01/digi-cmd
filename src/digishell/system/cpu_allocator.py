"""
CPU and Bios/Kernel Allocation Optimizer
"""

import os
import sys
import psutil

class CpuOptimizer:
    @staticmethod
    def optimize_process_priority():
        try:
            p = psutil.Process(os.getpid())
            if sys.platform == "win32":
                p.nice(psutil.HIGH_PRIORITY_CLASS)
            else:
                p.nice(-5)
            return "Process priority optimized to High."
        except Exception as e:
            return f"Priority optimization notice: {e}"
