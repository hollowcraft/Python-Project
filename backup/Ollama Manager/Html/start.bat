@echo off
title Ollama Manager Web
echo Starting Ollama Manager Web...

:: Vérifier si Python est installé
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b
)

:: Vérifier si Flask est installé
python -c "import flask" 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installation de Flask...
    pip install flask
)

:: Vérifier si Ollama est installé
python -c "import ollama" 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installation de Ollama...
    pip install ollama
)

:: Démarrer le serveur Flask
echo Demarrage du serveur...
start "Ollama Manager Server" python server.py

:: Attendre quelques secondes pour que le serveur démarre
timeout /t 3 /nobreak >nul

:: Ouvrir le navigateur
echo Ouverture du site web...
start http://localhost:5000

echo.
echo Pour arreter le serveur, fermez cette fenetre
echo.
pause