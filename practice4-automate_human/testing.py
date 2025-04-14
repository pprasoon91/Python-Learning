import subprocess
import time
import os
import signal
import random
from docx import Document

# --- Configuration ---
FIREFOX_URL = "https://www.chatgpt.com"
TARGET_TEXT = "what is radar and which radar is having highest range and how it works?"
STARTUP_DELAY = 1  # Seconds to wait for ydotoold
FIREFOX_OPEN_TIMEOUT = 20  # Increased timeout for Firefox
YDOTool_RETRY_DELAY = 0.5  # Seconds to wait before retrying ydotool commands
MAX_YDOTool_RETRIES = 3
INITIAL_TYPING_DELAY = 3  # Delay before typing
TYPING_SPEED_MIN = 0.1  # Minimum delay between characters (simulates faster typing today
TYPING_SPEED_MAX = 0.3  # Maximum delay between characters (simulates slower typing)
MISTAKE_PROBABILITY = 0.15  # Probability of making a mistake while typing
MAX_MISTAKE_LENGTH = 3  # Maximum number of characters to mistype
DELETE_KEY = "backspace"
RESPONSE_WAIT_TIME = 30  # Seconds to wait for the response
OUTPUT_WORD_FILE = "chatgpt_response.docx"

# --- Helper Functions ---
def is_process_running(process_name):
    """Checks if a process with the given name is running."""
    try:
        subprocess.run(["pgrep", "-x", process_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def start_process(command, error_message):
    """Starts a process and handles potential FileNotFoundError."""
    try:
        process = subprocess.Popen(command)
        return process
    except FileNotFoundError:
        print(f"Error: {error_message} not found. Make sure it is installed and in your PATH.")
        return None

def run_ydotool_command(command_args):
    """Runs a ydotool command with retries and error handling."""
    for attempt in range(MAX_YDOTool_RETRIES):
        try:
            print(f"ydotool command: {command_args}, attempt {attempt+1}")  # Debugging
            subprocess.run(command_args, check=True)
            return True
        except FileNotFoundError:
            print("Error: ydotool not found. Make sure it is installed and in your PATH.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"ydotool error (attempt {attempt + 1}/{MAX_YDOTool_RETRIES}): {e}")
            if attempt < MAX_YDOTool_RETRIES - 1:
                time.sleep(YDOTool_RETRY_DELAY)
            else:
                print("Max retries reached for ydotool. Aborting.")
                return False
        except Exception as e:
            print(f"An unexpected error occurred during ydotool command: {e}")
            return False
    return False

def human_like_typing(text):
    """Simulates human-like typing with random delays and mistakes."""
    typed_so_far = ""
    for i, char in enumerate(text):
        time.sleep(random.uniform(TYPING_SPEED_MIN, TYPING_SPEED_MAX))
        if random.random() < MISTAKE_PROBABILITY:
            # Make a mistake
            mistake_length = random.randint(1, MAX_MISTAKE_LENGTH)
            random_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz ') for _ in range(mistake_length))
            print(f"Made a mistake: typing '{random_chars}'")
            for mistake_char in random_chars:
                run_ydotool_command(["ydotool", "type", "--", mistake_char])
                time.sleep(random.uniform(TYPING_SPEED_MIN / 2, TYPING_SPEED_MAX / 2)) # Type mistakes quickly

            # Delete the mistake
            print(f"Correcting mistake: deleting {mistake_length} characters")
            for _ in range(mistake_length):
                run_ydotool_command(["ydotool", "key", DELETE_KEY])
                time.sleep(random.uniform(TYPING_SPEED_MIN / 3, TYPING_SPEED_MAX / 3)) # Delete quickly

            # Re-type the correct character
            print(f"Re-typing correctly: '{char}'")
            run_ydotool_command(["ydotool", "type", "--", char])
        else:
            run_ydotool_command(["ydotool", "type", "--", char])
        typed_so_far += char
    print(f"Finished typing: '{typed_so_far}'")

import pyautogui
import time
import random

def perform_copy_sequence():
    """Copy sequence using Shift+Tab navigation and visual matching"""
    try:
        print("Starting copy sequence...")
        
        # Configuration
        max_attempts = 10
        confidence = 0.8  # Matching confidence threshold
        delay_between_attempts = 1  # seconds
        
        for attempt in range(1, max_attempts + 1):
            print(f"\nAttempt {attempt}/{max_attempts}")
            
            # Press SHIFT+TAB
            run_ydotool_command(["ydotool", "key", "shift+Tab"])
            time.sleep(delay_between_attempts)
            
            # 2. Try to find the copy icon
            print("Searching for copy icon...")
            try:
                # Search in central region of the screen (80% of width/height)
                screen_width, screen_height = pyautogui.size()
                region = (
                    int(screen_width * 0.1),  # left
                    int(screen_height * 0.1),  # top
                    int(screen_width * 0.8),  # width
                    int(screen_height * 0.8)   # height
                )
                
                copy_icon = pyautogui.locateOnScreen(
                    'copy_icon.png',
                #confidence=confidence,
                    region=region,
                    grayscale=True
                )
                
                if copy_icon:
                    print("Copy icon found! Attempting to click...")
                    icon_x, icon_y = pyautogui.center(copy_icon)
                    
                    # Human-like mouse movement with slight randomness
                    pyautogui.moveTo(
                        icon_x + random.randint(-5, 5),
                        icon_y + random.randint(-5, 5),
                        duration=random.uniform(0.2, 0.5)
                    )
                    time.sleep(0.2)
                    pyautogui.click()
                    print("Successfully clicked copy icon")
                    time.sleep(1)
                    return True
                
                print("Copy icon not found in this attempt")
            
            except Exception as e:
                print(f"Error during icon search: {e}")
            
            # Wait before next attempt
            time.sleep(delay_between_attempts)
        
        print(f"\nFailed to find copy icon after {max_attempts} attempts")
        return False
        
    except Exception as e:
        print(f"Fatal error in copy sequence: {e}")
        return False
    
def save_response_to_word():
    """Gets clipboard content and saves to Word file"""
    try:
        # Get clipboard content (Linux)
        clipboard_content = subprocess.check_output(["xclip", "-selection", "clipboard", "-o"], text=True)
        
        # Save to Word document
        doc = Document()
        doc.add_paragraph(clipboard_content)
        doc.save(OUTPUT_WORD_FILE)
        print(f"Response saved to {OUTPUT_WORD_FILE}")
    except Exception as e:
        print(f"Error saving response: {e}")

# --- Main Script ---
print("Starting ydotoold...")
ydotoold_process = start_process(["ydotoold"], "ydotoold")
if ydotoold_process:
    time.sleep(STARTUP_DELAY)
    print("ydotoold started (hopefully).")
else:
    print("Skipping Firefox and typing as ydotoold failed to start.")
    exit(1)

print(f"Launching Firefox in private mode with URL: {FIREFOX_URL}")
firefox_process = start_process(["firefox", "--private-window", FIREFOX_URL], "firefox")

if firefox_process:
    # Wait for Firefox to open with a timeout
    start_time = time.time()
    while time.time() - start_time < FIREFOX_OPEN_TIMEOUT:
        if is_process_running("firefox"):
            print("Firefox launched.")
            break
        time.sleep(1)
    else:
        print("Warning: Firefox did not open within the timeout period.")

    time.sleep(INITIAL_TYPING_DELAY)  # Initial delay before typing

    print(f"Typing '{TARGET_TEXT}' with human-like errors...")
    human_like_typing(TARGET_TEXT)

    print("Simulating Enter key press...")
    run_ydotool_command(["ydotool", "key", "enter"])

    print(f"Waiting {RESPONSE_WAIT_TIME} seconds for the response...")
    time.sleep(RESPONSE_WAIT_TIME)

    print("Performing copy sequence...")
    perform_copy_sequence()

    print("Saving response to Word document...")
    save_response_to_word()

    # Clean up: Attempt to terminate Firefox
    print("Attempting to close Firefox...")
    firefox_process.terminate()
    firefox_process.wait(timeout=5)  # Give it a few seconds to close
    if firefox_process.poll() is None:
        print("Firefox did not close gracefully, attempting to kill...")
        firefox_process.kill()
        firefox_process.wait()
    print("Firefox closed.")

# Clean up: Attempt to terminate ydotoold
print("Attempting to stop ydotoold...")
if ydotoold_process.poll() is None:  # Check if the process is still running
    os.kill(ydotoold_process.pid, signal.SIGTERM)
    ydotoold_process.wait(timeout=5)
    if ydotoold_process.poll() is None:
        print("ydotoold did not stop gracefully, attempting to kill...")
        ydotoold_process.kill()
        ydotoold_process.wait()
print("ydotoold stopped.")

print("Script finished.")