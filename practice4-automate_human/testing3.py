#!/usr/bin/env python3
import uinput
import time

# Define all the keys we'll need
events = (
    uinput.KEY_LEFTSHIFT,
    uinput.KEY_TAB,
    uinput.KEY_SPACE, 
)

# Create the virtual keyboard device
time.sleep(5)
with uinput.Device(events, name="My Virtual Keyboard") as device:
    time.sleep(1)  # Let the system detect the new virtual keyboard
    
    for i in range(9):
        print(f"Sending Shift+Tab ({i+1}/6)...")
        # Press Shift
        device.emit(uinput.KEY_LEFTSHIFT, 1)
        time.sleep(0.05)
        
        # Press Tab
        device.emit(uinput.KEY_TAB, 1)
        time.sleep(0.05)
        
        # Release Tab
        device.emit(uinput.KEY_TAB, 0)
        time.sleep(0.05) 
        
        # Release Shift
        device.emit(uinput.KEY_LEFTSHIFT, 0)
        time.sleep(0.3)  # Small delay between sequences
        
    print("Sending Space to activate copy...")
    device.emit_click(uinput.KEY_SPACE)
    time.sleep(1)  # Wait a moment after the final press
    
print("Copy sequence completed with uinput!")

