@echo off
title Fuinha Network Monitor
echo ========================================================
echo               FUINHA NETWORK MONITOR v4.0               
echo ========================================================
echo.
echo Verificando ambiente Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no seu sistema.
    echo Por favor, instale o Python 3 em https://www.python.org/ e tente novamente.
    pause
    exit /b
)

echo Verificando e instalando dependencias necessarias...
pip install -r requirements.txt --quiet

echo Registrando atalho no Menu Iniciar...
powershell -ExecutionPolicy Bypass -File .\create_shortcut.ps1 >nul 2>&1

echo.
echo Iniciando o Fuinha Network Monitor...
cd ver3.0
python main.py
if %errorlevel% neq 0 (
    echo Tentando iniciar em modo de usuario comum...
    python main.py --no-admin
)
