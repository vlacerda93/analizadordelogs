# Script para remover atalhos do Fuinha Network Monitor no Windows

$StartMenuDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
$StartShortcutPath = "$StartMenuDir\Fuinha Network Monitor.lnk"

$DesktopDir = [Environment]::GetFolderPath("Desktop")
$DesktopShortcutPath = "$DesktopDir\Fuinha Network Monitor.lnk"

if (Test-Path $StartShortcutPath) {
    Remove-Item $StartShortcutPath -Force
    Write-Host "[SUCESSO] Atalho do Menu Iniciar removido!" -ForegroundColor Green
} else {
    Write-Host "[INFO] Atalho do Menu Iniciar nao foi encontrado." -ForegroundColor Yellow
}

if (Test-Path $DesktopShortcutPath) {
    Remove-Item $DesktopShortcutPath -Force
    Write-Host "[SUCESSO] Atalho da Area de Trabalho removido!" -ForegroundColor Green
} else {
    Write-Host "[INFO] Atalho da Area de Trabalho nao foi encontrado." -ForegroundColor Yellow
}
