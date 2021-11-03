; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Fishbowl Label Generator"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Dominick Faurote"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "FishbowlLabelGenerator.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{9A984455-4B16-4716-8D5A-5DA73003C4EF}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\Installer
OutputBaseFilename=Fishbowl Label Generator Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_asyncio.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_cffi_backend.cp38-win_amd64.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_multiprocessing.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_overlapped.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_queue.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\_win32sysloader.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\d3dcompiler_47.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\libcrypto-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\libEGL.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\libffi-7.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\libGLESv2.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\libssl-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\main.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\mfc140u.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\MSVCP140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\MSVCP140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\opengl32sw.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\python38.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\pythoncom38.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\pywintypes38.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Core.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5DBus.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Gui.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Network.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Qml.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5QmlModels.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Quick.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Svg.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5WebSockets.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Qt5Widgets.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\VCRUNTIME140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\win32api.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\win32trace.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\win32ui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\win32wnet.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\Crypto\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\pip-21.3.dist-info\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\PyQt5\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\setuptools-51.0.0.dist-info\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\wheel-0.36.1.dist-info\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\output\FishbowlLabelGenerator\win32com\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\Labels\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Nick Gamming\Documents\Python\FishbowlLabelGenerator\Dymo Software\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

