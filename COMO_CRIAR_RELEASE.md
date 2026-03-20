# Como Criar Release para Atualização do Sistema

## 📋 Passos para Criar Release:

### 1. **Acessar GitHub**
- Vá para: https://github.com/Lucskrr/conversor-txt-csv/releases

### 2. **Criar Nova Release**
- Clique em "Create a new release"
- Tag version: `v1.2.0`
- Release title: `Conversor TOTVS v1.2.0 - Compatibilidade JSON`

### 3. **Descrição da Release**
```
## 🎉 Nova Versão v1.2.0

### ✨ Novidades:
- **Sistema de Compatibilidade JSON**: Adicione novos formatos editando apenas um arquivo JSON
- **Campos Dinâmicos**: Cada formato mostra apenas os campos que existem
- **Atualizações Instantâneas**: Sem precisar compilar novo executável
- **Interface Melhorada**: Status de atualização visível no header

### 🔧 Melhorias:
- Parser híbrido (JSON + original)
- Detecção automática de formatos
- Fallback para compatibilidade 100%
- Sistema de plugins preparado

### 📋 Formatos Suportados:
- gerr004 (com código de barras)
- cdfr054 (com valores)

### 🚀 Como Adicionar Novos Formatos:
1. Edite `formats_config.json`
2. Commit e push
3. Pronto! Sistema atualiza automaticamente

---

**Desenvolvido por:** FA MARINGA LTDA  
**Atualização:** 20/03/2026
```

### 4. **Publish Release**
- Clique em "Publish release"

## 🔄 Resultado:
- ✅ Sistema detectará nova versão `v1.2.0`
- ✅ Usuários receberão notificação de atualização
- ✅ Novas funcionalidades disponíveis imediatamente
