[Setup]
; Informações do Aplicativo
AppName=Conversor TOTVS
AppVersion=1.1.0
AppPublisher=FA MARINGA LTDA
AppPublisherURL=http://www.famaringa.com.br
AppSupportURL=http://www.famaringa.com.br/suporte
AppUpdatesURL=http://www.famaringa.com.br/updates

; Configurações do Instalador
DefaultDirName={pf}\ConversorTOTVS
DefaultGroupName=Conversor TOTVS
AllowNoIcons=yes
LicenseFile=license.txt
OutputDir=instalador
OutputBaseFilename=ConversorTOTVS_Setup_v1.1.0
SetupIconFile=logo.ico
Compression=lzma
SolidCompression=yes

; Requisitos
MinVersion=6.1sp1
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Arquivos do Aplicativo
[Files]
Source: "dist\ConversorTOTVS.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "license.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion; Tasks: desktopicon
Source: "logo.ico"; DestDir: "{app}"; Flags: ignoreversion

; Atalhos
[Icons]
Name: "{group}\Conversor TOTVS"; Filename: "{app}\ConversorTOTVS.exe"; IconFilename: "{app}\logo.ico"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Conversor TOTVS"; Filename: "{app}\ConversorTOTVS.exe"; IconFilename: "{app}\logo.ico"; Tasks: desktopicon

; Tarefas do Instalador
[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos"; Flags: unchecked

; Código do Instalador
[Code]
function InitializeSetup(): Boolean;
begin
  // Verificar se o aplicativo já está instalado
  if RegKeyExists(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppName")}_is1') then
  begin
    if MsgBox('Conversor TOTVS já está instalado. Deseja desinstalar a versão anterior?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Executar desinstalação
      Exec(ExpandConstant('{uninstallexe}'), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end
    else
    begin
      Result := False;
      Exit;
    end;
  end;
  
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Criar entrada no registro para auto-update
    RegWriteStringValue(HKLM, 'SOFTWARE\ConversorTOTVS', 'InstallPath', ExpandConstant('{app}'));
    RegWriteStringValue(HKLM, 'SOFTWARE\ConversorTOTVS', 'Version', '{#emit SetupSetting("AppVersion")}');
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Limpar entradas do registro
    RegDeleteKeyIncludingSubkeys(HKLM, 'SOFTWARE\ConversorTOTVS');
  end;
end;
