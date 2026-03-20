# 📋 Compatibilidade de Arquivos - Conversor TOTVS

## 🎯 Formatos Suportados

O Conversor TOTVS atualmente suporta os seguintes formatos de arquivos TXT:

### 📊 **GERR004 - Contagem de Estoque**
- **Arquivo Exemplo**: `gerr004.P00 contagem.txt`
- **Versão**: P00
- **Descrição**: Arquivo de contagem de estoque do sistema TOTVS
- **Estrutura**: Campos delimitados por pipe (|)
- **Uso**: Processamento de inventário e controle de estoque

### 📈 **CDFR054 - Relatório Financeiro**
- **Arquivo Exemplo**: `cdfr054.P08.txt`
- **Versão**: P08
- **Arquivo Exemplo**: `cdfr054.P06.txt`
- **Versão**: P06
- **Descrição**: Arquivo de relatório financeiro do sistema TOTVS
- **Estrutura**: Campos delimitados por ponto e vírgula (;)
- **Uso**: Geração de relatórios contábeis e financeiros

---

## 🔍 **Estrutura dos Arquivos**

### GERR004.P00
```
CAMPO1|CAMPO2|CAMPO3|CAMPO4|CAMPO5
VALOR1|VALOR2|VALOR3|VALOR4|VALOR5
```

### CDFR054.P08
```
CAMPO1;CAMPO2;CAMPO3;CAMPO4;CAMPO5
VALOR1;VALOR2;VALOR3;VALOR4;VALOR5
```

---

## ✅ **Teste de Compatibilidade**

Para testar a compatibilidade:

1. **Arraste e solte** os arquivos de exemplo no Conversor TOTVS
2. **Verifique o reconhecimento** automático do formato
3. **Confirme a conversão** para CSV
4. **Valide os dados** no arquivo gerado

---

## 🚀 **Adicionando Novos Formatos**

Para adicionar suporte a novos formatos:

1. **Adicione o arquivo exemplo** nesta pasta
2. **Atualize o parser** em `parsers.py`
3. **Documente o formato** neste README
4. **Teste exaustivamente**

---

## 📝 **Histórico de Versões**

| Versão | Formato | Status | Data |
|--------|---------|--------|------|
| P00 | GERR004 | ✅ Estável | 20/03/2026 |
| P08 | CDFR054 | ✅ Estável | 20/03/2026 |
| P06 | CDFR054 | ✅ Estável | 20/03/2026 |

---

## 🆘 **Suporte**

Se tiver arquivos de outros formatos que precisam de suporte:

1. **Envie o arquivo** (sem dados sensíveis)
2. **Descreva o formato** e estrutura
3. **Informe a versão** do arquivo TOTVS
4. **Nossa equipe analisará** a implementação

---

*Última atualização: 20/03/2026*
