@echo off
echo ========================================
echo Construtor de Instalador - Conversor TOTVS
echo ========================================
echo.

REM Verificar se o executável existe
echo [1/4] Verificando executável...
if not exist "dist\ConversorTOTVS_v2.exe" (
    echo ❌ Executável não encontrado!
    echo Execute primeiro: python build_executable.py
    pause
    exit /b 1
)
echo ✅ Executável encontrado: dist\ConversorTOTVS_v2.exe

REM Verificar arquivos necessários
echo.
echo [2/4] Verificando arquivos do instalador...
if not exist "installer_script.iss" (
    echo ❌ Script do instalador não encontrado!
    pause
    exit /b 1
)

if not exist "license.txt" (
    echo ⚠️ Aviso: license.txt não encontrado
)

if not exist "logo.ico" (
    echo ⚠️ Aviso: logo.ico não encontrado
)

echo ✅ Arquivos verificados

REM Criar diretório de saída
echo.
echo [3/4] Preparando diretório de saída...
if not exist "instalador" mkdir instalador
echo ✅ Diretório instalador criado

REM Pedir caminho do Inno Setup
echo.
echo [4/4] Informe o caminho do Inno Setup
echo.
echo Exemplos comuns:
echo - C:\Program Files (x86)\Inno Setup 6\iscc.exe
echo - C:\Program Files\Inno Setup 6\iscc.exe
echo - C:\Arquivos de Programas (x86)\Inno Setup 6\iscc.exe
echo.
set /p INNO_PATH="Digite o caminho completo do iscc.exe: "

if not exist "%INNO_PATH%" (
    echo ❌ Arquivo não encontrado: %INNO_PATH%
    pause
    exit /b 1
)

echo ✅ Inno Setup encontrado: %INNO_PATH%

REM Compilar o instalador
echo.
echo Compilando instalador...
"%INNO_PATH%" "installer_script.iss"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ INSTALADOR CRIADO COM SUCESSO!
    echo ========================================
    echo 📦 Arquivo: instalador\ConversorTOTVS_Setup_v1.1.0.exe
    
    if exist "instalador\ConversorTOTVS_Setup_v1.1.0.exe" (
        for %%F in ("instalador\ConversorTOTVS_Setup_v1.1.0.exe") do echo 📏 Tamanho: %%~zF bytes
    )
    
    echo.
    echo 📝 Próximos passos:
    echo 1. Teste o instalador em uma máquina limpa
    echo 2. Verifique se todos os atalhos funcionam
    echo 3. Confirme se a aplicação inicia corretamente
    echo 4. Teste a desinstalação completa
    echo.
) else (
    echo.
    echo ❌ ERRO NA COMPILAÇÃO!
    echo Verifique o script installer_script.iss
    pause
    exit /b 1
)

echo Pressione qualquer tecla para abrir a pasta do instalador...
pause > nul
explorer "instalador"
