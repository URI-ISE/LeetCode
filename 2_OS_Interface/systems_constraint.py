import signal
import time
import sys

# Handler for SIGINT
def signal_handler(sig, frame):
    print("Cleaning up...")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Infinite loop doing "work"
try:
    while True:
        time.sleep(1)  # Simulating work by sleeping
except KeyboardInterrupt:
    # This block is not necessary since we handle SIGINT with the signal handler
    pass
