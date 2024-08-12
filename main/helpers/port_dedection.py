import sys

def detect_port():
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[-1])
        except ValueError:
            pass
    return 8000