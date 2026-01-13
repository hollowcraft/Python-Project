@echo off
set /p PathFolder="Path:"
set /p FolderName="Name:"
set CurrentFolder=%~1
echo %PathFolder% %CurrentFolder%
mklink /D "%CurrentFolder%\%FolderName%" "%PathFolder%"

pause
