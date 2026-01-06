@echo off
cls

cd "C:\Users\Adam\Desktop\Mes Projects\python\web"
start http://localhost:8000
start /B python -m http.server 8000
start cmd /k "python "C:\Users\Adam\Desktop\Mes Projects\python\discord\main.py""