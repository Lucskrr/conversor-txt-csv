#!/usr/bin/env python3
"""
Script para atualizar versão do app manualmente
"""

from datetime import datetime

def update_version():
    """Atualiza a versão do app para nova release"""
    
    # Versão atual
    current_version = "1.1.0"
    
    # Nova versão com base nas mudanças
    new_version = "1.1.1"  # Incremento de patch
    
    # Data atual
    today = datetime.now().strftime("%d/%m/%Y")
    
    print("🔧 Atualizando Versão do Conversor TOTVS")
    print("=" * 50)
    print(f"Versão atual: {current_version}")
    print(f"Nova versão: {new_version}")
    print(f"Data: {today}")
    print("=" * 50)
    
    # Atualizar config.py
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir versão
        new_content = content.replace(
            f"VERSION = '{current_version}'",
            f"VERSION = '{new_version}'"
        )
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ config.py atualizado para versão {new_version}")
        
        # Atualizar update_service.py se necessário
        try:
            with open('services/update_service.py', 'r', encoding='utf-8') as f:
                update_content = f.read()
            
            # Atualizar comentários se necessário
            update_new_content = update_content.replace(
                "# ATENÇÃO: Substitua SEU-USUARIO pelo seu username do GitHub",
                "# ATENÇÃO: Substitua SEU-USUARIO pelo seu username do GitHub"
            )
            
            with open('services/update_service.py', 'w', encoding='utf-8') as f:
                f.write(update_new_content)
            
            print("✅ update_service.py verificado")
            
        except Exception as e:
            print(f"⚠️ Erro ao verificar update_service.py: {e}")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar config.py: {e}")
        return False
    
    print("\n🎯 Próximos passos:")
    print("1. Execute: build_test.bat")
    print("2. Teste as novas funcionalidades")
    print("3. Se tudo OK, crie novo release no GitHub")
    print("4. Sistema automático de atualizações funcionará")
    
    return True

if __name__ == "__main__":
    update_version()
