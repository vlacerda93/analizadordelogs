# Script para registrar o Fuinha no Menu Iniciar do Windows e na Área de Trabalho com ícone oficial (.ico,0)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TargetExe = "$ScriptDir\dist\Fuinha.exe"
$IconIco = "$ScriptDir\ver3.0\assets\icon.ico"
$IconPng = "$ScriptDir\ver3.0\assets\icon.png"

$IconFile = if (Test-Path $IconIco) { $IconIco } else { $IconPng }
$IconLocationString = "$IconFile,0"

$WshShell = New-Object -ComObject WScript.Shell

# 1. Atalho no Menu Iniciar
$StartMenuDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
$StartShortcutPath = "$StartMenuDir\Fuinha Network Monitor.lnk"

if (Test-Path $StartShortcutPath) {
    Remove-Item $StartShortcutPath -Force
}

$StartShortcut = $WshShell.CreateShortcut($StartShortcutPath)

if (Test-Path $TargetExe) {
    $StartShortcut.TargetPath = $TargetExe
    $StartShortcut.WorkingDirectory = "$ScriptDir\dist"
    $StartShortcut.IconLocation = "$TargetExe,0"
} else {
    $StartShortcut.TargetPath = "python.exe"
    $StartShortcut.Arguments = """$ScriptDir\ver3.0\main.py"""
    $StartShortcut.WorkingDirectory = "$ScriptDir\ver3.0"
    $StartShortcut.IconLocation = $IconLocationString
}

$StartShortcut.Description = "Fuinha Network Monitor v4.0 - Analisador de Tráfego e Logs"
$StartShortcut.Save()
Write-Host "[SUCESSO] Atalho do Fuinha atualizado no Menu Iniciar do Windows com o icone!" -ForegroundColor Green

# 2. Atalho na Área de Trabalho
$DesktopDir = [Environment]::GetFolderPath("Desktop")
$DesktopShortcutPath = "$DesktopDir\Fuinha Network Monitor.lnk"

if (Test-Path $DesktopShortcutPath) {
    Remove-Item $DesktopShortcutPath -Force
}

$DesktopShortcut = $WshShell.CreateShortcut($DesktopShortcutPath)

if (Test-Path $TargetExe) {
    $DesktopShortcut.TargetPath = $TargetExe
    $DesktopShortcut.WorkingDirectory = "$ScriptDir\dist"
    $DesktopShortcut.IconLocation = "$TargetExe,0"
} else {
    $DesktopShortcut.TargetPath = "python.exe"
    $DesktopShortcut.Arguments = """$ScriptDir\ver3.0\main.py"""
    $DesktopShortcut.WorkingDirectory = "$ScriptDir\ver3.0"
    $DesktopShortcut.IconLocation = $IconLocationString
}

$DesktopShortcut.Description = "Fuinha Network Monitor v4.0"
$DesktopShortcut.Save()
Write-Host "[SUCESSO] Atalho do Fuinha atualizado na Area de Trabalho com o icone!" -ForegroundColor Green

# 3. Forçar atualização do cache de ícones do Windows Shell (ie4uinit)
try {
    ie4uinit.exe -show
} catch {}
