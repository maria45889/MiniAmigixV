$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "MiniAmigixV.lnk"
$LauncherPath = Join-Path $ProjectPath "iniciar_miniamigixv.bat"
$IconPath = Join-Path $ProjectPath "static\miniamigixv.ico"

if (!(Test-Path $LauncherPath)) {
    throw "No se encontro iniciar_miniamigixv.bat"
}

if (!(Test-Path $IconPath)) {
    throw "No se encontro el icono: $IconPath"
}

$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $LauncherPath
$Shortcut.WorkingDirectory = $ProjectPath
$Shortcut.Description = "Abrir MiniAmigixV"

$Shortcut.IconLocation = "$IconPath,0"

$Shortcut.Save()
Write-Host "Acceso directo creado en el escritorio: $ShortcutPath"
