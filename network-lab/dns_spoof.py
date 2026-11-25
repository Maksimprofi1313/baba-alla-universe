"""Offline DNS query parser demo.

Live DNS spoofing/interception is intentionally disabled. Use a dedicated,
isolated lab and purpose-built tools for authorized DNS protocol study.
"""
def parse_domain_name(data):
    """Extract a simple uncompressed DNS question name from a packet."""
    if len(data) < 13:
        return "invalid-packet"
    try:
        parts = []
        index = 12
        while index < len(data):
            length = data[index]
            if length == 0:
                return ".".join(parts) or "."
            # Compression pointers and malformed labels are not decoded here.
            if length & 0xC0 or length > 63 or index + 1 + length > len(data):
                return "unsupported-or-invalid-name"
            parts.append(data[index + 1:index + 1 + length].decode("ascii"))
            index += 1 + length
        return "invalid-packet"
    except (IndexError, UnicodeDecodeError):
        return "invalid-packet"

def main():
    print("DNS parser demo — network listening and response spoofing are disabled.")
    print("This script only parses a supplied packet in memory.")
    print("Import parse_domain_name(data) from another local test to inspect a DNS question.")

if __name__ == "__main__":
    main()
