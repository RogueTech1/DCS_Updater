[Setup]
AppName=DCS Livery Updater
AppVersion=1.0
DefaultDirName={localappdata}\DCS_Livery_Updater
DefaultGroupName=DCS Livery Updater
UninstallDisplayIcon={app}\dcs_livery_installer.exe
OutputDir=.
OutputBaseFilename=DCS_Livery_Updater_Installer
SetupIconFile=icon.ico

[Files]
Source: "dist\dcs_livery_installer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DCS Livery Updater"; Filename: "{app}\dcs_livery_installer.exe"
Name: "{group}\Uninstall DCS Livery Updater"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\dcs_livery_installer.exe"; Description: "Launch DCS Livery Updater"; Flags: nowait postinstall
