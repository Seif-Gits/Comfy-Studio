@echo off
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Comfy Studio.lnk');$s.TargetPath='%~dp0Start Comfy Studio.bat';$s.WorkingDirectory='%~dp0';$s.IconLocation='%~dp0icon.ico';$s.Save()"
echo A "Comfy Studio" shortcut with its icon is now on your Desktop.
pause
