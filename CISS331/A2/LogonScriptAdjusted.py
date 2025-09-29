import winreg
import sys
import os

# Path to the Python interpreter and script
python_path = sys.executable  
script_path = os.path.abspath("C:/Users/pshaf/VSCProjects/CISS331/Typewriter.py")  
command = f'"{python_path}" "{script_path}"'

# Registry key path
reghive = winreg.HKEY_CURRENT_USER
regpath = r"Software\Microsoft\Windows\CurrentVersion\Run"

# Open the registry key for writing
key = winreg.OpenKey(reghive, regpath, 0, access=winreg.KEY_WRITE)
winreg.SetValueEx(key, "MyPythonScript", 0, winreg.REG_SZ, command)
winreg.CloseKey(key)
    
   