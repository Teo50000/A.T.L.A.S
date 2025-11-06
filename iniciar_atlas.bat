@echo off
echo Iniciando backend y frontend del proyecto ATLAS...

:: --- BACKEND ---
cd "./"
echo Instalando dependencias del backend...
call pip install -r requirements.txt
echo Iniciando backend...
start cmd /k "python prncpl.py"

:: --- FRONTEND ---
cd electronpusheable
echo Iniciando frontend...
call npm i
start cmd /k "npm start"

echo Todo iniciado correctamente.
pause