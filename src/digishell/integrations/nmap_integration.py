"""
Nmap Network Scanning Integrations
"""

def build_nmap_command(target: str = "127.0.0.1", scan_type: str = "-sV") -> str:
    return f"nmap {scan_type} {target}"
