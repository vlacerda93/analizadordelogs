@echo off
title Criador de Executavel (.exe) & Instalador no Menu Iniciar - Fuinha
echo ========================================================
echo         GERADOR DE EXECUTAVEL WINDOWS - FUINHA          
echo ========================================================
echo.

echo Instalando PyInstaller e dependencias...
pip install pyinstaller -r requirements.txt --quiet

echo.
echo Compilando Fuinha em um unico executavel standalone Windows (.exe)...
pyinstaller --noconfirm --onefile --windowed --add-data "ver3.0/assets;assets" --add-data "ver3.0/locales;locales" --icon "ver3.0/assets/icon.ico" --name "Fuinha" ver3.0/main.py

if %errorlevel% equ 0 (
    echo.
    echo Registrando o Fuinha no Menu Iniciar do Windows e na Area de Trabalho...
    powershell -ExecutionPolicy Bypass -File .\create_shortcut.ps1
    
    echo.
    echo ========================================================
    echo  [SUCESSO] Executavel gerado e registrado com sucesso!
    echo  - Executavel: dist\Fuinha.exe
    echo  - Atalho no Menu Iniciar: "Fuinha Network Monitor"
    echo ========================================================
) else (
    echo.
    echo [ERRO] Ocorreu uma falha ao gerar o executavel.
)
pause
