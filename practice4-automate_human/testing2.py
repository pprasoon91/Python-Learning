import subprocess
import time

def wtype_key(key_sequence):
    """
    Send a key sequence like 'Shift+Tab' or 'space' using wtype.
    """
    print(f"Sending: {key_sequence}")
    subprocess.run(["wtype", key_sequence])

# Allow time to switch to the target app
print("You have 5 seconds to switch to the target app!")
time.sleep(5)

# Send Shift+Tab 6 times
for i in range(6):
    wtype_key("Shift+Tab")
    time.sleep(0.3)

# Press Space
wtype_key("space")
time.sleep(1)

print("Copy sequence completed!")





             #
