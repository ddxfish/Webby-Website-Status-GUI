import sys
import subprocess
#hello
while True:
    # Run your main PyQt5 application script
    retcode = subprocess.call([sys.executable, 'main.py'])
    if retcode != 42:  # Assume 42 is the restart code
        break
