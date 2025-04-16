#!/usr/bin/env python3
import subprocess
import time
import os
import sys

def debug_log(message):
    """Optional debug logging"""
    print(f"[DEBUG] {message}", file=sys.stderr)

def get_active_window():
    """Try multiple methods to detect active window"""
    # Method 1: xdotool (XWayland apps)
    try:
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            capture_output=True, text=True, timeout=1
        )
        if result.returncode == 0 and result.stdout.strip():
            debug_log(f"xdotool detected: {result.stdout.strip()}")
            return result.stdout.strip()
    except Exception as e:
        debug_log(f"xdotool failed: {str(e)}")

    # Method 2: wmctrl (X11 fallback)
    try:
        # Get active window ID
        active_id = subprocess.run(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
            capture_output=True, text=True, timeout=1
        )
        if active_id.returncode == 0:
            window_id = active_id.stdout.split()[-1]
            debug_log(f"Active window ID: {window_id}")
            
            # Get window list
            windows = subprocess.run(
                ["wmctrl", "-l"],
                capture_output=True, text=True, timeout=1
            )
            if windows.returncode == 0:
                for line in windows.stdout.splitlines():
                    if window_id.lower() in line.lower():
                        title = " ".join(line.split()[3:])
                        debug_log(f"wmctrl detected: {title}")
                        return title
    except Exception as e:
        debug_log(f"wmctrl failed: {str(e)}")

    # Method 3: Try D-Bus (for GNOME/KDE)
    try:
        # GNOME Shell
        result = subprocess.run(
            ["gdbus", "call", "--session", "--dest", "org.gnome.Shell", 
             "--object-path", "/org/gnome/Shell/Extensions/Windows", 
             "--method", "org.gnome.Shell.Extensions.Windows.GetWindows"],
            capture_output=True, text=True, timeout=1
        )
        if result.returncode == 0:
            debug_log(f"GNOME D-Bus raw: {result.stdout}")
            # Simple parsing of D-Bus output
            if "(" in result.stdout and ")" in result.stdout:
                windows = eval(result.stdout[result.stdout.find("("):result.stdout.rfind(")")+1])
                for window in windows:
                    if window[2]:  # is_active
                        debug_log(f"GNOME D-Bus detected: {window[1]}")
                        return window[1]
    except:
        pass

    return "No active window detected"

def monitor_active_window(interval=1):
    """Monitor with debug output"""
    print("Monitoring active window (press Ctrl+C to stop)...")
    print("Debug output will be shown for detection attempts")
    
    previous = None
    try:
        while True:
            current = get_active_window()
            if current != previous:
                print(f"\nActive Window: {current}")
                previous = current
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    if not any(os.path.exists(f"/usr/bin/{tool}") for tool in ["xdotool", "wmctrl", "gdbus"]):
        print("Warning: Some tools missing - detection may be limited")
        print("For best results: sudo apt install xdotool wmctrl libglib2.0-bin")
    
    monitor_active_window()