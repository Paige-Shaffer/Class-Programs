import time
import pyautogui
import subprocess

# Open Notepad
subprocess.Popen("notepad.exe")
time.sleep(5)  

# Bring Notepad to focus
notepad_windows = [w for w in pyautogui.getWindowsWithTitle("Untitled - Notepad") if w.isActive]
notepad_windows[0].activate()
time.sleep(2)
pyautogui.write('I am Mr. Hacker. I am in your system.', interval=0.1)
pyautogui.press('enter')
pyautogui.write('You should have done a better job locking up.', interval=0.1)
pyautogui.press('enter')
pyautogui.write('I am now going to steal all your cookies.', interval=0.1)
pyautogui.press('enter')
