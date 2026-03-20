# Configuração do Sistema de Atualizações

## 🎯 Passo 1: Criar Repositório GitHub

### 1.1 Criar Conta/Repositório
```bash
# 1. Vá para github.com
# 2. Crie repositório: conversor-totvs
# 3. Torne público (necessário para API)
```

### 1.2 Configurar Release Inicial
```bash
# 1. Faça upload do instalador
# 2. Crie release: v1.1.0
# 3. Adicione descrição e changelog
```

## 🔧 Passo 2: Configurar URLs no Código

### 2.1 Atualizar update_service.py
```python
# Alterar linhas 29-30:
self.version_url = "https://api.github.com/repos/SEU-USUARIO/conversor-totvs/releases/latest"
self.download_base_url = "https://github.com/SEU-USUARIO/conversor-totvs/releases/download"
```

### 2.2 Substituir SEU-USUARIO pelo seu username do GitHub

## 🚀 Passo 3: Publicar Novas Versões

### 3.1 Processo de Atualização
```bash
# 1. Atualize versão em config.py: VERSION = '1.2.0'
# 2. Crie novo executável: python build_executable.py
# 3. Crie instalador: build_installer.bat
# 4. Faça upload no GitHub
# 5. Crie nova release: v1.2.0
# 6. Adicione notas da versão
```

## 📱 Como o Usuário Visualiza:

### Tela de Atualização
```
┌─────────────────────────────────────┐
│  🔄 Nova Versão Disponível!        │
│                                     │
│  Versão Atual: 1.1.0               │
│  Nova Versão: 1.2.0 ✅              │
│                                     │
│  📝 Novidades:                      │
│  • Melhorias de performance         │
│  • Novos formatos suportados        │
│  • Correções de bugs               │
│                                     │
│  [🚀 Atualizar Agora]  [⏸️ Depois]  │
└─────────────────────────────────────┘
```

## ⚡ Funcionalidades:

### ✅ Automático
- Verificação a cada 24 horas
- Download em background
- Instalação silenciosa

### ✅ Seguro
- Verificação de integridade
- Backup automático
- Rollback se falhar

### ✅ Amigável
- Notificação não intrusiva
- Changelog informativo
- Escolha do usuário

## 🔍 Logs de Atualização:
```
2024-03-20 09:00:00 - INFO - Checking for updates. Current version: 1.1.0
2024-03-20 09:00:01 - INFO - New version available: 1.2.0
2024-03-20 09:00:02 - INFO - Downloading update to: C:\temp\conversor_update_xxx.exe
2024-03-20 09:00:15 - INFO - Update downloaded successfully
2024-03-20 09:00:16 - INFO - Update script created: C:\temp\update_xxx.bat
2024-03-20 09:00:17 - INFO - Update installation completed
```

## 🎯 Benefícios:
- 🔄 **Sem intervenção manual**
- 🛡️ **Sempre atualizado**
- 📊 **Estatísticas de uso**
- 🚀 **Experiência profissional**
