[Setup]
AppName=DCS Livery Updater
AppVersion=1.0
DefaultDirName={localappdata}\DCS_Livery_Updater
DefaultGroupName=DCS Livery Updater
UninstallDisplayIcon={app}\DcsLiveryUpdater.exe
OutputDir=.
OutputBaseFilename=DCS_Livery_Updater_Installer
SetupIconFile=icon.ico

[Files]
Source: "dist\DcsLiveryUpdater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DCS Livery Updater"; Filename: "{app}\DcsLiveryUpdater.exe"
Name: "{group}\Uninstall DCS Livery Updater"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\DcsLiveryUpdater.exe"; Description: "Launch DCS Livery Updater"; Flags: nowait postinstall
