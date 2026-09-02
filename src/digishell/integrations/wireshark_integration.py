"""
Wireshark / TShark Network Capture Integrations
"""

def build_tshark_command(interface: str = "eth0", duration: int = 10) -> str:
    return f"tshark -i {interface} -a duration:{duration}"
