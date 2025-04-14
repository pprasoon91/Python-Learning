import pyautogui
import cv2
import numpy as np
from PIL import Image

def find_small_icon(large_image_path, small_icon_path, confidence=0.7):
    """
    Detects a small icon within a larger image using template matching.
    
    Args:
        large_image_path: Path to screenshot containing the icon
        small_icon_path: Path to small icon image to find
        confidence: Match threshold (0-1)
    
    Returns:
        (x, y) coordinates of icon center if found, else None
    """
    # Load images
    large_img = cv2.imread(large_image_path)
    small_icon = cv2.imread(small_icon_path)
    
    # Convert to grayscale (better for small icons)
    large_gray = cv2.cvtColor(large_img, cv2.COLOR_BGR2GRAY)
    icon_gray = cv2.cvtColor(small_icon, cv2.COLOR_BGR2GRAY)
    
    # Perform template matching
    res = cv2.matchTemplate(large_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
    
    # Get best match location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= confidence:
        # Calculate center coordinates
        icon_w, icon_h = small_icon.shape[1], small_icon.shape[0]
        center_x = max_loc[0] + icon_w // 2
        center_y = max_loc[1] + icon_h // 2
        return (center_x, center_y)
    return None

# Usage Example:
large_img = "screenshot.png"  # Your full screenshot
small_icon = "tiny_icon.png"  # The small icon to find

if pos := find_small_icon(large_img, small_icon, confidence=0.65):
    print(f"✅ Icon found at {pos}")
    pyautogui.click(pos)  # Click the detected position
else:
    print("❌ Icon not found")