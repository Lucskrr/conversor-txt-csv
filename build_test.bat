@echo off
echo ========================================
echo Build de Teste - Nova Versão
echo ========================================
echo.

echo [1/4] Limpando builds anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo [2/4] Reconstruindo executável com novas funcionalidades...
python build_executable.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Falha no build do executável
    pause
    exit /b 1
)

echo [3/4] Verificando novo executável...
if exist "dist\ConversorTOTVS_v2.exe" (
    echo ✅ Executável criado com sucesso!
    for %%F in ("dist\ConversorTOTVS_v2.exe") do echo 📏 Tamanho: %%~zF bytes
    
    echo.
    echo [4/4] Testando novo executável...
    echo Iniciando o Conversor TOTVS com novas funcionalidades...
    echo.
    echo 🎯 Novidades incluídas:
    echo   ✅ Suporte a CDFR054.P06 (975 registros)
    echo   ✅ Testes de compatibilidade automatizados
    echo   ✅ Documentação técnica completa
    echo.
    start "" "dist\ConversorTOTVS_v2.exe"
    
    echo.
    echo ✅ Teste iniciado! Verifique as novas funcionalidades.
    echo 📁 Para testar os arquivos de exemplo:
    echo    1. Arraste: Compatibilidade\*.txt
    echo    2. Verifique o reconhecimento automático
    echo    3. Confirme a conversão para CSV
    echo.
) else (
    echo ❌ Executável não encontrado após o build
    pause
    exit /b 1
)

echo.
echo 🎉 Build de teste concluído!
pause
