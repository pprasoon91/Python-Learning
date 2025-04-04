import subprocess
import time
import pyautogui

# Step 1: Open Firefox in Private Mode
subprocess.run(["firefox", "--private-window", "https://chat.openai.com/"])

# Step 2: Wait for Browser to Open
time.sleep(5)  # Adjust based on system speed

# Step 3: Emulate Keyboard Input (Login might be required)
time.sleep(2)
pyautogui.typewrite("Hello, what is AI?", interval=0.1)
pyautogui.press("enter")

# Step 4: Wait for the response to generate
time.sleep(10)  # Adjust based on response speed

# Step 5: Capture response using OCR (Optional, requires pytesseract)
# Screenshot area where response appears
screenshot = pyautogui.screenshot(region=(100, 300, 800, 500))  # Adjust coordinates
screenshot.save("chatgpt_response.png")

print("Screenshot saved. You can process it with OCR.")
