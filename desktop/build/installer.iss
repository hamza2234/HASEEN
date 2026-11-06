; ---------------------------------------------------------------------------
;  Inno Setup script - builds a normal Windows installer wizard
;  (Next -> Next -> Install -> Finish) for the desktop application.
;
;  Build:
;     1. run:  pyinstaller build\thesis_app.spec --noconfirm
;     2. install Inno Setup 6 (https://jrsoftware.org/isdl.php)
;     3. run:  iscc build\installer.iss
;
;  Output: build\Output\HybridPSOGA-Setup-1.0.0.exe
;  The installer works completely offline and needs no administrator rights
;  when installed for the current user only.
; ---------------------------------------------------------------------------

#define MyAppName "Hybrid PSO-GA Feature Selection System"
#define MyAppNameAr "نظام اختيار السمات الهجين PSO-GA"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Hussein Naser Hussein - Damghan University"
#define MyAppExeName "HybridPSOGA.exe"

[Setup]
AppId={{8E4C1B72-3A5D-4F91-9C2E-7B6A1D4E8F03}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\HybridPSOGA
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=no
AllowNoIcons=yes
OutputDir=Output
OutputBaseFilename=HybridPSOGA-Setup-{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=license.txt
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic";  MessagesFile: "compiler:Languages\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; the whole PyInstaller output folder, built from build\thesis_app.spec
Source: "..\dist\HybridPSOGA\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README_APP.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\docs\screenshots\*"; DestDir: "{app}\screenshots"; \
    Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppNameAr}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
    Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\screenshots"

[Code]
{ A short welcome line in the chosen language, plus the student's name on the
  final page so the installer is clearly part of this thesis. }
procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel2.Caption :=
    'This will install ' + '{#MyAppName}' + ' on your computer.' + #13#10 + #13#10 +
    'The application reproduces the master''s thesis of ' +
    'Hussein Naser Hussein (Damghan University).' + #13#10 + #13#10 +
    'It runs completely offline and supports Arabic and English.';
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
    WizardForm.FinishedLabel.Caption :=
      'The application has been installed.' + #13#10 + #13#10 +
      'Start it from the desktop shortcut or the Start menu, then choose ' +
      'Arabic or English in the sidebar.' + #13#10 + #13#10 +
      'Thank you.';
end;
