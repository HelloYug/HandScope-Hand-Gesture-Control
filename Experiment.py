# import pyautogui
# pyautogui.hotkey("win", "l")

import os
import platform

def lock_system():
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif system_platform == "Linux":
        os.system("gnome-screensaver-command -l")
    elif system_platform == "Darwin":  # macOS
        os.system("/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend")
    else:
        print("Locking the system is not supported on this OS.")

# Call the function to lock the system
lock_system()
