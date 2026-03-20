[Setup]
; Informações do Aplicativo
AppName=Conversor TOTVS
AppVersion=1.1.0
AppVerName=Conversor TOTVS 1.1.0
AppPublisher=FA MARINGA LTDA
AppPublisherURL=http://www.famaringa.com.br
AppSupportURL=http://www.famaringa.com.br/suporte
AppUpdatesURL=http://www.famaringa.com.br/updates
AppComments=Conversor de arquivos TXT para CSV - Formatos TOTVS
AppCopyright=Copyright (C) 2024 FA MARINGA LTDA

; Configurações do Instalador
DefaultDirName={autopf}\ConversorTOTVS
DefaultGroupName=Conversor TOTVS
AllowNoIcons=yes
LicenseFile=license.txt
OutputDir=instalador
OutputBaseFilename=ConversorTOTVS_Setup_v1.1.0
SetupIconFile=logo-FA-semfundo.ico
Compression=lzma2/max
SolidCompression=yes
InternalCompressLevel=max
DiskSpanning=no
WizardStyle=modern

; Requisitos e Compatibilidade
MinVersion=6.1sp1
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UsePreviousAppDir=yes
UsePreviousGroup=yes
UsePreviousTasks=yes
UsePreviousLanguage=yes
ShowLanguageDialog=no

; Arquivos do Aplicativo
[Files]
; Executável principal
Source: "dist\ConversorTOTVS_v2.exe"; DestDir: "{app}"; DestName: "ConversorTOTVS.exe"; Flags: ignoreversion

; Arquivos de licença e configuração
Source: "license.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

; Recursos visuais
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo-FA-semfundo.ico"; DestDir: "{app}"; DestName: "logo.ico"; Flags: ignoreversion

; Documentação
Source: "Manual_Usuario.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

; Criar diretório para logs
[Dirs]
Name: "{app}\logs"

; Atalhos
[Icons]
; Menu Iniciar
Name: "{group}\Conversor TOTVS"; Filename: "{app}\ConversorTOTVS.exe"; IconFilename: "{app}\logo.ico"; Comment: "Conversor de arquivos TXT para CSV"
Name: "{group}\Manual do Usuário"; Filename: "{app}\Manual_Usuario.txt"; Comment: "Manual de instruções"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"; Comment: "Remover Conversor TOTVS"

; Área de Trabalho
Name: "{commondesktop}\Conversor TOTVS"; Filename: "{app}\ConversorTOTVS.exe"; IconFilename: "{app}\logo.ico"; Tasks: desktopicon; Comment: "Conversor TOTVS"

; Tarefas do Instalador
[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos"; Flags: unchecked
Name: "quicklaunchicon"; Description: "Criar atalho na barra de inicialização rápida"; GroupDescription: "Atalhos"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "associate"; Description: "Associar arquivos .txt ao Conversor TOTVS"; GroupDescription: "Associações de arquivo"; Flags: unchecked

; Código do Instalador
[Code]
var
  ResultCode: Integer;

function InitializeSetup(): Boolean;
begin
  // Verificar se o aplicativo já está instalado
  if RegKeyExists(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppName")}_is1') then
  begin
    if MsgBox('Conversor TOTVS já está instalado. Deseja desinstalar a versão anterior?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Executar desinstalação
      if not Exec(ExpandConstant('{uninstallexe}'), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode) then
      begin
        MsgBox('Erro ao desinstalar versão anterior. Código: ' + IntToStr(ResultCode), mbError, MB_OK);
        Result := False;
        Exit;
      end;
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
    RegWriteStringValue(HKLM, 'SOFTWARE\ConversorTOTVS', 'InstallDate', GetDateTimeString('yyyy/mm/dd hh:nn:ss', '-', ':'));
    
    // Registrar associação de arquivo se selecionado
    if IsTaskSelected('associate') then
    begin
      RegWriteStringValue(HKCR, '.txt\OpenWithList\ConversorTOTVS.exe', '', ExpandConstant('{app}\ConversorTOTVS.exe'));
      RegWriteStringValue(HKCR, 'Applications\ConversorTOTVS.exe\SupportedTypes', '.txt', '');
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Limpar entradas do registro
    RegDeleteKeyIncludingSubkeys(HKLM, 'SOFTWARE\ConversorTOTVS');
    
    // Remover associações de arquivo
    RegDeleteKeyIncludingSubkeys(HKCR, '.txt\OpenWithList\ConversorTOTVS.exe');
    RegDeleteKeyIncludingSubkeys(HKCR, 'Applications\ConversorTOTVS.exe');
  end;
end;
