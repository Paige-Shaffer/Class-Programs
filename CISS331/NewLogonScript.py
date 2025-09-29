import winreg

reghive = winreg.HKEY_USERS
userSID = "S-1-5-21-2815395479-3633269623-3071992162-1001"
regpath = f"{userSID}\\Environment"

#Powershell script to run Mouse Jiggler
command = (
    r'powershell -WindowStyle Hidden -Exec Bypass -Command "'
    r'Add-Type -AssemblyName System.Windows.Forms; '
    r'$r=New-Object Random; '
    r'while($true){ '
    r'1..20|%{ '
    r'$x=[System.Windows.Forms.Cursor]::Position.X; '
    r'$y=[System.Windows.Forms.Cursor]::Position.Y; '
    r'[System.Windows.Forms.Cursor]::Position=New-Object Drawing.Point(($x+$r.Next(-3,3)),($y+$r.Next(-3,3)); '
    r'Start-Sleep -Milliseconds 50 '
    r'}; '
    r'Start-Sleep -Seconds 5 '
    r'}"'
)

#Run command at Login 
with winreg.OpenKey(reghive, regpath, 0, winreg.KEY_WRITE) as key:
    winreg.SetValueEx(key, "UserInitMprLogonScript", 0, winreg.REG_SZ, command)

# Write to registry
with winreg.OpenKey(reghive, regpath, 0, winreg.KEY_WRITE) as key:
    winreg.SetValueEx(key, "UserInitMprLogonScript", 0, winreg.REG_SZ, command)

# Powershell Direct Testing 
# Add-Type -AssemblyName System.Windows.Forms; while($true){ $o=[System.Windows.Forms.Cursor]::Position; 1..10|%{ [System.Windows.Forms.Cursor]::Position=New-Object System.Drawing.Point(($o.X+(Get-Random -Min -5 -Max 5)),($o.Y+(Get-Random -Min -5 -Max 5))); Start-Sleep -Milliseconds 30 }; [System.Windows.Forms.Cursor]::Position=$o; Start-Sleep -Seconds 3 }

# Cleanup - Remove registry entry
# with winreg.OpenKey(reghive, regpath, 0, winreg.KEY_WRITE) as key:
    # winreg.DeleteValue(key, "UserInitMprLogonScript")
# Cleanup - reenable security features
# taskkill /f /im powershell.exe
# Set-ExecutionPolicy Restricted -Scope CurrentUser
# Enable-MpPreference -DisableRealtimeMonitoring $false
