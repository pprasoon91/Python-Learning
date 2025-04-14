import pyautogui
import time

while True:
        
    print("Move your mouse to the desired location and wait for the coordinates...")

    # Wait a few seconds so you can move your mouse to the target location
    time.sleep(5)

    # Capture the mouse position
    x, y = pyautogui.position()

    print(f"The coordinates of the current mouse position are: ({x}, {y})")

    if "t" == input("press t to terminate"):
        exit()
