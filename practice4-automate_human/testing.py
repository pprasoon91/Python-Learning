import subprocess
import time

# Start ydotoold (needed for Wayland)
subprocess.Popen(["ydotoold"])
time.sleep(1)  # Give it time to start

# Launch Firefox in private mode
subprocess.Popen(["firefox", "--private-window", "https://www.google.co.in"])
time.sleep(5)  # Wait for Firefox to open

# Type text using ydotool (Wayland alternative)
subprocess.run(["ydotool", "type", "--", "hello world"])
subprocess.run(["ydotool", "key", "enter"])