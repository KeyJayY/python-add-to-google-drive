import winreg
import sys
import os

python_exePath = sys.executable
pythonDirPath, _ = os.path.split(python_exePath)
pythonw_exePaht = os.path.join(pythonDirPath, "pythonw.exe")

currentDir, _ = os.path.split(__file__)
pythonScriptPath = os.path.join(currentDir, "script.py")

path = winreg.HKEY_CLASSES_ROOT

files = winreg.OpenKeyEx(path, r"*\shell")
fileNewKey = winreg.CreateKey(files, "Upload")
fileSubKey = winreg.CreateKey(fileNewKey, "command")

winreg.SetValueEx(fileNewKey, "", 0, winreg.REG_SZ, "Upload to Google Drive")
winreg.SetValueEx(
    fileSubKey, "", 0, winreg.REG_SZ, f'"{pythonw_exePaht}" "{pythonScriptPath}" "%1"'
)

directories = winreg.OpenKeyEx(path, r"Directory\shell")
dirNewKey = winreg.CreateKey(directories, "Upload")
dirSubKey = winreg.CreateKey(dirNewKey, "command")

winreg.SetValueEx(dirNewKey, "", 0, winreg.REG_SZ, "Upload to Google Drive")
winreg.SetValueEx(
    dirSubKey, "", 0, winreg.REG_SZ, f'"{pythonw_exePaht}" "{pythonScriptPath}" "%1"'
)
