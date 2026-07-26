@echo off
title Desinstalador de Atalhos - Fuinha Network Monitor
echo ========================================================
echo         DESINSTALADOR DE ATALHOS - FUINHA NETWORK        
echo ========================================================
echo.

echo Removendo atalhos do Menu Iniciar e Area de Trabalho...
powershell -ExecutionPolicy Bypass -File .\uninstall_shortcut.ps1

echo.
echo ========================================================
echo  [SUCESSO] Atalhos do Fuinha foram removidos do Windows!
echo ========================================================
pause
