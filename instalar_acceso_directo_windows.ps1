$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "MiniAmigixV.lnk"
$LauncherPath = Join-Path $ProjectPath "iniciar_miniamigixv.bat"
$LogoPath = Join-Path $ProjectPath "static\logo.png"
$IconPath = Join-Path $ProjectPath "static\miniamigixv.ico"

if (!(Test-Path $LauncherPath)) {
    throw "No se encontro iniciar_miniamigixv.bat"
}

if (Test-Path $LogoPath) {
    Add-Type -AssemblyName System.Drawing
    $Bitmap = [System.Drawing.Bitmap]::FromFile($LogoPath)
    $IconHandle = $Bitmap.GetHicon()
    $Icon = [System.Drawing.Icon]::FromHandle($IconHandle)
    $Stream = [System.IO.File]::Create($IconPath)
    $Icon.Save($Stream)
    $Stream.Close()
    $Icon.Dispose()
    $Bitmap.Dispose()
}

$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $LauncherPath
$Shortcut.WorkingDirectory = $ProjectPath
$Shortcut.Description = "Abrir MiniAmigixV"

if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
}

$Shortcut.Save()
Write-Host "Acceso directo creado en el escritorio: $ShortcutPath"
