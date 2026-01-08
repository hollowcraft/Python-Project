@echo off
set /p PathFolder=""
set /p FolderName=""
set CurrentFolder=%cd%
echo %PathFolder% %CurrentFolder%
mklink /D "%CurrentFolder%\%FolderName%" "%PathFolder%"
pause