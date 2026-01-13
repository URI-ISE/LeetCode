import subprocess
import sys

#!/usr/bin/env python3
"""
Standard Streams: A Deep Dive into Unix IPC
============================================
This script demonstrates process orchestration using subprocess and pipes.
It spawns a grep process, feeds it input via stdin, and captures filtered output.

Architecture:
    Python Process (PID X)         grep Process (PID Y)
    ┌──────────────────┐           ┌─────────────────┐
    │  User Space      │           │  User Space     │
    │  - Write logs    │──stdin──> │  - Read stdin   │
    │  - Read results  │<─stdout── │  - Write stdout │
    └────────┬─────────┘           └────────┬────────┘
             │                              │
    ═════════╪══════════════════════════════╪═════════
             │         Kernel Space         │
             │   ┌──────────────────────┐   │
             └──>│ Pipe Buffer (64KB)   │───┘
                 │ (Circular Buffer)    │
                 └──────────────────────┘

Backpressure Mechanism:
    - If grep reads slowly, pipe buffer fills
    - Kernel blocks our write() syscall until space available
    - Prevents unbounded memory growth
"""



def monitor_grep():
    """
    Spawn grep as a child process and filter logs through it.
    
    Why communicate() instead of manual I/O?
    ----------------------------------------
    1. **Deadlock Prevention**: If we write to stdin while the pipe buffer is full
       AND simultaneously try to read from stdout whose buffer is also full,
       we create a circular wait (classic deadlock). communicate() uses threads
       or select() internally to handle I/O in parallel.
    
    2. **Buffer Management**: Manual read() can hang if we don't know the exact
       output size. communicate() reads until EOF, handling chunking automatically.
    
    3. **Memory Safety**: communicate() accumulates output in memory-controlled
       chunks, whereas naive read() can consume unbounded memory if the child
       produces infinite output.
    
    Time Complexity: O(N) where N = total bytes transferred (input + output)
    Space Complexity: O(M) where M = max(input_size, output_size) held in memory
    """
    
    # Simulated log stream (in production, this could be tailing /var/log/app.log)
    log_data = """ERROR: disk full on /dev/sda1
INFO: service started successfully
ERROR: segmentation fault in module core.so
WARNING: high memory usage detected
INFO: connection established to database
ERROR: timeout waiting for response from api.example.com
DEBUG: processing request id=12345
INFO: cache hit ratio: 95%
"""
    
    # Security: shell=False prevents injection attacks like "grep 'foo'; rm -rf /"
    # bufsize=4096 aligns with typical OS page size, reducing syscall overhead
    try:
        process = subprocess.Popen(
            ['grep', 'ERROR'],  # argv array - no shell interpretation
            stdin=subprocess.PIPE,    # Create pipe for FD 0
            stdout=subprocess.PIPE,   # Create pipe for FD 1
            stderr=subprocess.PIPE,   # Create pipe for FD 2
            bufsize=4096,             # Buffer size matching OS page (4KB)
            text=True                 # Handle strings instead of bytes
        )
        
        # communicate() does three things atomically:
        # 1. Writes input to stdin (then closes the pipe to signal EOF)
        # 2. Reads stdout and stderr until EOF (child process exits)
        # 3. Waits for child termination (avoiding zombie processes)
        stdout_data, stderr_data = process.communicate(input=log_data)
        
        # Analyze exit code
        # grep exit codes: 0 = matches found, 1 = no matches, 2 = error
        return_code = process.returncode
        
        print("=" * 60)
        print("GREP OUTPUT (matches found):")
        print("=" * 60)
        print(stdout_data if stdout_data else "(no matches)")
        
        if stderr_data:
            print("\n" + "=" * 60)
            print("STDERR (diagnostics):")
            print("=" * 60)
            print(stderr_data)
        
        print("\n" + "=" * 60)
        print("PROCESS DIAGNOSTICS:")
        print("=" * 60)
        print(f"Return Code: {return_code}")
        
        if return_code == 0:
            print("✓ Status: Matches found - ERROR conditions detected in logs")
            print("  Interpretation: System requires immediate attention")
        elif return_code == 1:
            print("✓ Status: No matches - System is clean")
            print("  Interpretation: No ERROR-level events in the monitored period")
        else:
            print(f"✗ Status: grep encountered an error (code {return_code})")
            print("  Interpretation: Check if grep binary exists and is executable")
        
        print("=" * 60)
        
    except FileNotFoundError:
        print("ERROR: 'grep' command not found in PATH", file=sys.stderr)
        print("This script requires grep to be installed (standard on Unix systems)")
        sys.exit(127)
    except Exception as e:
        print(f"ERROR: Unexpected failure: {e}", file=sys.stderr)
        sys.exit(1)


def explain_deadlock_scenario():
    """
    Educational: Why manual I/O is dangerous.
    
    DEADLOCK SCENARIO:
    ------------------
    # DANGEROUS CODE (DO NOT USE):
    proc = subprocess.Popen(['grep', 'ERROR'], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(huge_input)  # Blocks when pipe buffer fills (64KB)
    output = proc.stdout.read()    # Never reached - we're stuck writing!
    
    The kernel blocks our write() because grep hasn't read enough to drain
    the pipe. But grep is blocked writing its output because WE haven't read
    from stdout. Classic circular wait → deadlock.
    
    FIX: communicate() spawns threads/uses select() to handle both streams
    concurrently, breaking the circular dependency.
    """
    print("\n" + "=" * 60)
    print("WHY communicate() IS CRITICAL:")
    print("=" * 60)
    print(explain_deadlock_scenario.__doc__)


if __name__ == "__main__":
    monitor_grep()
    explain_deadlock_scenario()