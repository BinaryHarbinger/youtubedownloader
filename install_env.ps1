# PowerShell script: install_env.ps1
# Run as Administrator

# --- Check admin privileges ---
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Run this script as Administrator."
    exit 1
}

# --- Install Chocolatey if missing ---
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# --- Install Python and FFmpeg system-wide ---
choco install -y python ffmpeg

# --- Install Python dependencies ---
Write-Host "Installing Python packages..."
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install pyqt6 yt-dlp

# --- Define paths ---
$ProjectName = "yt-dlp-qt6"
$SourcePath = (Resolve-Path "$PSScriptRoot").Path  # project root (where script is)
$TargetDir = "C:\Program Files\$ProjectName"
$SrcDir = "$TargetDir\src"
$ShortcutPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\$ProjectName.lnk"

# --- Copy project files ---
Write-Host "Copying project files to $TargetDir..."
if (Test-Path $TargetDir) { Remove-Item $TargetDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item "$SourcePath\*" $TargetDir -Recurse -Force

# --- Create launcher batch file ---
$BatPath = "$TargetDir\$ProjectName.bat"
$PythonExe = (Get-Command python).Source
$MainScript = "$SrcDir\main.py"
Set-Content $BatPath "@echo off`ncd `"$SrcDir`"`n`"$PythonExe`" `"$MainScript`" %*"

# --- Add to PATH (system-wide) ---
$envPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($envPath -notmatch [regex]::Escape($TargetDir)) {
    [Environment]::SetEnvironmentVariable("Path", "$envPath;$TargetDir", "Machine")
}

# --- Create Start Menu shortcut ---
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatPath
$Shortcut.WorkingDirectory = $SrcDir
$Shortcut.Save()

# --- Register in "Apps & Features" ---
Write-Host "Registering in Windows Apps list..."
$RegPath = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$ProjectName"
if (-not (Test-Path $RegPath)) { New-Item -Path $RegPath | Out-Null }

Set-ItemProperty -Path $RegPath -Name "DisplayName" -Value $ProjectName
Set-ItemProperty -Path $RegPath -Name "DisplayVersion" -Value "1.0"
Set-ItemProperty -Path $RegPath -Name "Publisher" -Value "yt-dlp-qt6 Project"
Set-ItemProperty -Path $RegPath -Name "InstallLocation" -Value $TargetDir
Set-ItemProperty -Path $RegPath -Name "DisplayIcon" -Value "$TargetDir\preview.png"
Set-ItemProperty -Path $RegPath -Name "UninstallString" -Value "powershell -ExecutionPolicy Bypass -File `"$TargetDir\uninstall.ps1`""
Set-ItemProperty -Path $RegPath -Name "NoModify" -Value 1 -Type DWord
Set-ItemProperty -Path $RegPath -Name "NoRepair" -Value 1 -Type DWord

# --- Create uninstall script ---
$UninstallScript = @"
# PowerShell Uninstall Script for yt-dlp-qt6
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Run this script as Administrator."
    exit 1
}
Remove-Item -Path "C:\Program Files\yt-dlp-qt6" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\yt-dlp-qt6.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\yt-dlp-qt6" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "yt-dlp-qt6 uninstalled."
"@
Set-Content -Path "$TargetDir\uninstall.ps1" -Value $UninstallScript -Encoding UTF8

Write-Host "Installation complete."
Write-Host "You can now run 'yt-dlp-qt6' from Start Menu or any terminal."

