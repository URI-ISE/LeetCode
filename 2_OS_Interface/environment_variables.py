import os
import subprocess
import sys

# Read the database URL from environment variables
DB_URL = os.environ.get('DATABASE_URL')

# Check if the database URL is missing
if DB_URL is None:
    print("Error: DATABASE_URL is not set.")
    sys.exit(1)



# Spawn a child process with the modified environment
try:
    subprocess.run([sys.executable, '-c', 'import os; os.environ["DEBUG"] = "1"; print(f"DEBUG in child: {os.environ.get(\'DEBUG\')}")'])
except Exception as e:
    print(f"Failed to spawn child process: {e}")
    sys.exit(1)

# Verify the parent's environment remains unchanged
try:
    print(f"DEBUG in parent: {os.environ.get('DEBUG')}")
except Exception as e:
    print(f"Failed to access parent environment: {e}")
    sys.exit(1)
