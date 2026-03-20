# Como Criar Release no GitHub para Download

## 📋 Pré-requisitos:
- Conta no GitHub
- Repositório criado para o projeto

## 🚀 Passos:

### 1. Criar Repositório
```bash
# Se ainda não tiver, crie um repositório:
git init
git add .
git commit -m "Primeiro release - Conversor TOTVS v1.1.0"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/conversor-totvs.git
git push -u origin main
```

### 2. Criar Release no Site
1. Vá para: `github.com/SEU-USUARIO/conversor-totvs`
2. Clique em "Releases" > "Create a new release"
3. Preencha:
   - **Tag version**: `v1.1.0`
   - **Release title**: `Conversor TOTVS v1.1.0`
   - **Description**: Descreva as funcionalidades
4. Arraste o arquivo `ConversorTOTVS_Setup_v1.1.0.exe` para a área de upload
5. Clique em "Publish release"

### 3. Link de Download
O link de download será:
```
https://github.com/SEU-USUARIO/conversor-totvs/releases/download/v1.1.0/ConversorTOTVS_Setup_v1.1.0.exe
```

## 📝 Vantagens:
- ✅ Link permanente
- ✅ Controle de versões
- ✅ Estatísticas de download
- ✅ Profissional
- ✅ Gratuito
