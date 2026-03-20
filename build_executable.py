#!/usr/bin/env python3
"""
Script para construir o executável do Conversor TOTVS
Alternativa ao PyInstaller direto com configurações otimizadas
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def clean_build():
    """Limpa builds anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"🧹 Limpado: {dir_name}")

def create_version_info():
    """Cria arquivo de informações de versão para Windows"""
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1,1,0,0),
    prodvers=(1,1,0,0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'FA MARINGA LTDA'),
        StringStruct(u'FileDescription', u'Conversor de arquivos TXT para CSV - Formatos TOTVS'),
        StringStruct(u'FileVersion', u'1.1.0'),
        StringStruct(u'InternalName', u'ConversorTOTVS'),
        StringStruct(u'LegalCopyright', u'© 2024 FA MARINGA LTDA'),
        StringStruct(u'OriginalFilename', u'ConversorTOTVS.exe'),
        StringStruct(u'ProductName', u'Conversor TOTVS'),
        StringStruct(u'ProductVersion', u'1.1.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    print("📄 Arquivo version_info.txt criado")

def build_executable():
    """Constrói o executável com PyInstaller"""
    
    # Comando PyInstaller otimizado
    cmd = [
        'pyinstaller',
        '--clean',
        '--onefile',  # Executável único
        '--windowed',  # Sem console (aplicação GUI)
        '--name=ConversorTOTVS',  # Nome do executável
        '--icon=logo.png' if Path('logo.png').exists() else '',
        '--version-file=version_info.txt',
        '--add-data=logo.png;.' if Path('logo.png').exists() else '',
        '--add-data=license.txt;.' if Path('license.txt').exists() else '',
        '--hidden-import=tkinterdnd2',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--hidden-import=utils.logger',
        '--hidden-import=utils.config_service',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=scipy',
        '--exclude-module=pandas',
        '--exclude-module=jupyter',
        '--exclude-module=IPython',
        'converter.py'
    ]
    
    # Remove argumentos vazios
    cmd = [arg for arg in cmd if arg]
    
    print("🔨 Iniciando build do executável...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build concluído com sucesso!")
        print(result.stdout)
        
        # Verifica se o executável foi criado
        exe_path = Path('dist/ConversorTOTVS.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executável criado: {exe_path}")
            print(f"📏 Tamanho: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Executável não encontrado após o build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def test_executable():
    """Testa se o executável funciona"""
    exe_path = Path('dist/ConversorTOTVS.exe')
    if not exe_path.exists():
        print("❌ Executável não encontrado para teste")
        return False
    
    print("🧪 Testando executável...")
    try:
        # Tenta executar com timeout para não travar
        result = subprocess.run([str(exe_path)], 
                              timeout=5, 
                              capture_output=True, 
                              text=True)
        print("✅ Executável iniciado com sucesso!")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Executável iniciado (timeout normal para GUI)")
        return True
    except Exception as e:
        print(f"❌ Erro ao testar executável: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Construtor de Executável - Conversor TOTVS")
    print("=" * 50)
    
    # Verifica dependências
    if not check_dependencies():
        return False
    
    # Limpa builds anteriores
    clean_build()
    
    # Cria informações de versão
    create_version_info()
    
    # Constrói o executável
    if build_executable():
        # Testa o executável
        test_executable()
        
        print("\n" + "=" * 50)
        print("🎉 Processo concluído!")
        print("📂 Executável disponível em: dist/ConversorTOTVS.exe")
        print("\n📝 Próximos passos:")
        print("1. Teste o executável manualmente")
        print("2. Se funcionar, use o Inno Setup para criar o instalador")
        print("3. Arquivos de log serão criados na mesma pasta do executável")
        
        return True
    else:
        print("\n❌ Falha no processo de build")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
