@echo off
echo ========================================
echo Configurando GitHub para Atualizações
echo ========================================
echo.

echo [1/4] Verificando Git...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git não encontrado!
    echo Por favor, instale Git em: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git encontrado

echo.
echo [2/4] Inicializando repositório Git...
git init
git add .
git commit -m "Primeiro release - Conversor TOTVS v1.1.0"
echo ✅ Repositório inicializado

echo.
echo [3/4] Próximos passos manuais necessários:
echo.
echo 1. Crie uma conta no GitHub (se ainda não tiver)
echo 2. Crie um repositório público chamado "conversor-totvs"
echo 3. Copie o comando abaixo:
echo.
echo    git remote add origin https://github.com/SEU-USUARIO/conversor-totvs.git
echo    git push -u origin main
echo.
echo 4. Substitua SEU-USUARIO pelo seu username do GitHub
echo 5. Execute os comandos no terminal
echo.
echo 6. Vá para o GitHub e crie um Release:
echo    - Tag: v1.1.0
echo    - Title: Conversor TOTVS v1.1.0
echo    - Upload do arquivo: instalador\ConversorTOTVS_Setup_v1.1.0.exe
echo.
echo [4/4] Arquivos preparados para GitHub!
echo ✅ Sistema de atualizações configurado no código
echo.
echo Após criar o repositório GitHub, o sistema de atualizações funcionará automaticamente!
pause
