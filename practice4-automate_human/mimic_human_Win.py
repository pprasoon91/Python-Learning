import subprocess
import time
import random
import pyautogui
import pyperclip
import psutil
import keyboard
import os
from docx import Document

# --- Configuration ---
FIREFOX_URL = "https://www.chatgpt.com"
TARGET_TEXT = "Trending News Today"
FIREFOX_OPEN_TIMEOUT = 20
INITIAL_TYPING_DELAY = 3
TYPING_SPEED_MIN = 0.1
TYPING_SPEED_MAX = 0.3
MISTAKE_PROBABILITY = 0.15
MAX_MISTAKE_LENGTH = 3
RESPONSE_WAIT_TIME = 30
OUTPUT_WORD_FILE = "chatgpt_response.docx"

# --- Helper Functions ---
def is_process_running(process_name):
    return any(proc.name().lower() == process_name.lower() for proc in psutil.process_iter())

def start_process(command):
    try:
        return subprocess.Popen(command)
    except FileNotFoundError:
        print(f"Error: Command not found: {' '.join(command)}")
        return None

def human_like_typing(text):
    for char in text:
        time.sleep(random.uniform(TYPING_SPEED_MIN, TYPING_SPEED_MAX))
        if random.random() < MISTAKE_PROBABILITY:
            mistake = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz ') for _ in range(random.randint(1, MAX_MISTAKE_LENGTH)))
            print(f"Mistake: {mistake}")
            pyautogui.write(mistake, interval=0.05)
            pyautogui.press('backspace', presses=len(mistake), interval=0.03)
        pyautogui.write(char)

def perform_copy_sequence():
    print("Pressing Shift+Tab 4 times...")
    for i in range(4):
        keyboard.press('shift')
        keyboard.press_and_release('tab')
        keyboard.release('shift')
        time.sleep(0.3)

    print("Pressing SPACE...")
    keyboard.press_and_release('space')
    time.sleep(1)

def save_response_to_word():
    try:
        # Get clipboard content
        markdown_text = pyperclip.paste()
        if not markdown_text.strip():
            print("Clipboard is empty or does not contain text.")
            return

        # Save as temporary markdown file
        temp_md_file = "temp_clipboard.md"
        with open(temp_md_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        # Convert to DOCX using Pandoc
        result = subprocess.run(
            ["pandoc", temp_md_file, "-o", OUTPUT_WORD_FILE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            print("Pandoc error:\n", result.stderr)
        else:
            print(f"✅ Markdown content saved to {OUTPUT_WORD_FILE}")

        # Optional: clean up
        os.remove(temp_md_file)

    except Exception as e:
        print(f"❌ Error: {e}")

# --- Main ---
print(f"Launching Firefox to {FIREFOX_URL}")
firefox_process = start_process(["C:\\Program Files\\Mozilla Firefox\\firefox.exe", "-private-window", FIREFOX_URL])

if firefox_process:
    start_time = time.time()
    while time.time() - start_time < FIREFOX_OPEN_TIMEOUT:
        if is_process_running("firefox.exe"):
            print("Firefox launched.")
            break
        time.sleep(1)

    time.sleep(INITIAL_TYPING_DELAY)
    print("Typing target text...")
    human_like_typing(TARGET_TEXT)
    pyautogui.press("enter")

    print(f"Waiting {RESPONSE_WAIT_TIME} seconds...")
    time.sleep(RESPONSE_WAIT_TIME)

    print("Copying response...")
    perform_copy_sequence()

    print("Saving response...")
    save_response_to_word()

    print("Closing Firefox...")
    firefox_process.terminate()
else:
    print("Failed to launch Firefox.")

print("Script completed.")
