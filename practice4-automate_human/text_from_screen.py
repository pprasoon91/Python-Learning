import pyautogui
import pytesseract
from PIL import Image
import time

# Optional: set path to tesseract binary if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def capture_screen_text(interval=5):
    print("Capturing screen text every", interval, "seconds. Press Ctrl+C to stop.")
    while True:
        # Take a screenshot
        screenshot = pyautogui.screenshot()

        # Use OCR to extract text from the screenshot
        text = pytesseract.image_to_string(screenshot)

        # Print the extracted text
        print("="*50)
        print("Captured Text:\n", text.strip())
        print("="*50)

        # Wait before next capture
        time.sleep(interval)

if __name__ == "__main__":
    capture_screen_text()
