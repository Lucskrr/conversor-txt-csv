@echo off
echo =====================================
echo Conversor TOTVS - Build do Instalador
echo =====================================

REM Verificar se o executável existe
if not exist "dist\ConversorTOTVS.exe" (
    echo ERRO: Executável não encontrado em dist\ConversorTOTVS.exe
    echo Execute: pyinstaller --onefile --windowed --name ConversorTOTVS app/main.py
    pause
    exit /b 1
)

REM Verificar se a licença existe
if not exist "license.json" (
    echo ERRO: Arquivo license.json não encontrado
    echo Execute: python generate_license.py
    pause
    exit /b 1
)

REM Criar diretório do instalador
if not exist "instalador" mkdir instalador

echo.
echo Compilando instalador com Inno Setup...
echo.

REM Compilar o instalador (assumindo que o Inno Setup está no PATH)
iscc installer_script.iss

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Instalador criado com sucesso!
    echo 📁 Arquivo: instalador\ConversorTOTVS_Setup_v1.1.0.exe
    echo.
    echo Para testar, execute o instalador em uma máquina limpa.
) else (
    echo.
    echo ❌ Erro na compilação do instalador
    echo Verifique se o Inno Setup está instalado corretamente
)

pause
