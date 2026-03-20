# 📚 Documentação Completa - Sistema de Atualização de Compatibilidades

## 🎯 Visão Geral

O Conversor TOTVS agora possui um sistema **híbrido de atualização** que permite adicionar novas compatibilidades de forma **rápida e eficiente**, sem precisar recompilar o aplicativo inteiro.

---

## 🔄 Fluxo de Atualização - Novo vs Antigo

### 🔴 **ANTIGO (Complicado)**
```
1. Identificar novo formato (2-4 horas)
2. Editar parsers.py (100+ linhas de código)
3. Testar localmente (1 hora)
4. Gerar executável PyInstaller (30 minutos)
5. Criar release no GitHub (15 minutos)
6. Usuários baixam 50MB (5-10 minutos)
7. Instalar nova versão (5 minutos)

🕐 **TOTAL: 4-6 horas por nova compatibilidade**
```

### 🟢 **NOVO (Rápido)**
```
1. Identificar novo formato (2-4 horas)
2. Editar formats_config.json (10 linhas)
3. Testar localmente (5 minutos)
4. Git push (1 minuto)
5. Sistema atualiza automaticamente (instantâneo)

🕐 **TOTAL: 2-4 horas por nova compatibilidade**
```

---

## 📋 Processo Detalhado - Adicionando Nova Compatibilidade

### **Etapa 1: Análise do Arquivo**

**Exemplo:** Você recebe um arquivo `novo_formato.P01.txt` com este conteúdo:
```
0011234567890123PRODUTO EXEMPLO A         0010,5010,50
0029876543210987OUTRO PRODUTO B          0005,2505,25
0035555555555555PRODUTO COMPLEXO C       0020,0020,00
```

### **Etapa 2: Identificar Padrão Regex**

**Análise:**
- `001` = seq (3 dígitos)
- `1234567890123` = código_produto (13 dígitos)  
- `PRODUTO EXEMPLO A` = descrição (texto variável)
- `0010,50` = quantidade (número com vírgula)
- `10,50` = valor_unitario (número com vírgula)

**Regex resultante:**
```regex
^(\d{3})(\d{13})(.+?)(\d{3},\d{2})(\d{3},\d{2})$
```

### **Etapa 3: Editar formats_config.json**

```json
{
  "formats": {
    // ... formatos existentes ...
    
    "novo_formato": {
      "pattern": "novo_formato\\.P\\d{2}\\.(txt|TXT)$",
      "content_pattern": "NOVO_FORMATO|PRODUTO",
      "description": "Novo formato - Produtos com valores",
      "record_pattern": "^(\\d{3})(\\d{13})(.+?)(\\d{3},\\d{2})(\\d{3},\\d{2})$",
      "field_mapping": {
        "seq": 1,
        "codigo_produto": 2,
        "descricao": 3,
        "codigo_barras": null,
        "quantidade": 4,
        "valor_unitario": 5,
        "valor_total": null
      },
      "multiline_description": false,
      "number_fields": ["quantidade", "valor_unitario"],
      "csv_headers": ["seq", "codigo_produto", "descricao", "quantidade", "valor_unitario"]
    }
  }
}
```

### **Etapa 4: Teste Local**

```bash
# Testar o novo formato
python test_json_integration.py
```

**Saída esperada:**
```
🧪 Testing JSON Parser Integration...
✅ Supported formats: ['gerr004', 'cdfr054', 'novo_formato']
🔍 Testing file: novo_formato.P01.txt
   Detected format: novo_formato
   CSV headers: ['seq', 'codigo_produto', 'descricao', 'quantidade', 'valor_unitario']
   Sample record: {'seq': '001', 'codigo_produto': '1234567890123', 'descricao': 'PRODUTO EXEMPLO A', 'quantidade': '10.50', 'valor_unitario': '10.50'}
```

### **Etapa 5: Deploy**

```bash
# Commit das mudanças
git add formats_config.json
git commit -m "feat: add novo_formato compatibility"
git push origin main
```

### **Etapa 6: Atualização Automática**

**O que acontece nos clientes:**
1. Sistema verifica atualizações (a cada 24h ou manual)
2. Detecta nova versão do `formats_config.json`
3. Baixa automaticamente o JSON atualizado
4. **Pronto!** Novo formato disponível instantaneamente

---

## 🎯 Casos de Uso Reais

### **Caso 1: Formato Simples (CSV-like)**

**Arquivo:**
```
001;12345678901234;Produto A;10;5,50
002;98765432109876;Produto B;5;12,30
```

**Config JSON:**
```json
{
  "csv_format": {
    "pattern": "csv_formato\\.P\\d{2}\\.(txt|TXT)$",
    "record_pattern": "^(\\d{3});(\\d{14});(.*);(\\d+);([\\d,]+)$",
    "field_mapping": {
      "seq": 1, "codigo_produto": 2, "descricao": 3, 
      "quantidade": 4, "valor_unitario": 5
    },
    "multiline_description": false,
    "number_fields": ["quantidade", "valor_unitario"],
    "csv_headers": ["seq", "codigo_produto", "descricao", "quantidade", "valor_unitario"]
  }
}
```

### **Caso 2: Formato Complexo (Multi-linhas)**

**Arquivo:**
```
001 12345678901234 PRODUTO COM
NOME GRANDE QUE CONTINUA
AQUI  0010,50 0010,50
002 98765432109876 PRODUTO
SIMples 0005,25 0005,25
```

**Config JSON:**
```json
{
  "multiline_format": {
    "pattern": "multiline\\.P\\d{2}\\.(txt|TXT)$",
    "record_pattern": "^(\\d{3})\\s+(\\d{14})\\s+(.*?)\\s+(\\d{3},\\d{2})\\s+(\\d{3},\\d{2})",
    "field_mapping": {
      "seq": 1, "codigo_produto": 2, "descricao": 3,
      "quantidade": 4, "valor_total": 5
    },
    "multiline_description": true,
    "multiline_pattern": "^(\\d{3}\\s+\\d{14})",
    "number_fields": ["quantidade", "valor_total"],
    "csv_headers": ["seq", "codigo_produto", "descricao", "quantidade", "valor_total"]
  }
}
```

---

## 🔧 Referência de Configuração

### **Campos Obrigatórios**

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `pattern` | string | Regex para nome do arquivo | `"formato\\.P\\d{2}\\.(txt|TXT)$"` |
| `record_pattern` | string | Regex para extrair dados | `"^(\\d{3})(.*)$"` |
| `field_mapping` | object | Mapeamento grupo→campo | `{"seq": 1, "descricao": 2}` |
| `csv_headers` | array | Colunas do CSV | `["seq", "descricao"]` |

### **Campos Opcionais**

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `content_pattern` | string | null | Regex para identificar conteúdo |
| `description` | string | "" | Descrição do formato |
| `multiline_description` | boolean | false | Suporte a descrições multi-linha |
| `multiline_pattern` | string | null | Regex para identificar nova linha |
| `multiline_stop_patterns` | array | [] | Padrões que param descrição |
| `number_fields` | array | [] | Campos que são números |

---

## 🚀 Sistema de Atualização Automática

### **Como Funciona**

1. **Verificação Periódica**: A cada 24h (ou manual via menu)
2. **Download**: Baixa `formats_config.json` do GitHub
3. **Validação**: Verifica se há novos formatos
4. **Aplicação**: Carrega novas configurações
5. **Notificação**: Mostra "Novos formatos disponíveis"

### **Logs do Sistema**

```
2026-03-20 10:15:00 - INFO - Checking for format updates...
2026-03-20 10:15:01 - INFO - Downloaded formats_config.json (2,456 bytes)
2026-03-20 10:15:01 - INFO - New formats detected: ['novo_formato', 'csv_format']
2026-03-20 10:15:01 - INFO - Format configuration updated successfully
2026-03-20 10:15:02 - INFO - Total supported formats: 4
```

---

## 📊 Benefícios Alcançados

### **Para Desenvolvedores**
- ⚡ **10x mais rápido** para adicionar formatos
- 🔧 **Sem rebuild** - apenas JSON
- 🧪 **Testes simples** - Python script
- 📝 **Documentação automática** - JSON autoexplicativo

### **Para Usuários**
- 🚀 **Atualizações instantâneas** - sem download
- 📱 **Sem reinstalação** - update automático
- 🎯 **Formatos específicos** - só campos que existem
- 🔄 **Compatibilidade total** - fallback automático

### **Para Negócio**
- 💰 **Custo reduzido** - menos tempo de desenvolvimento
- 📈 **Agilidade** - resposta rápida a clientes
- 🛡️ **Baixo risco** - mudanças isoladas
- 📊 **Escalabilidade** - formatos ilimitados

---

## 🔍 Troubleshooting

### **Problema: Formato não detectado**
```bash
# Verificar regex
python -c "
import re
pattern = 'seu_pattern_aqui'
filename = 'arquivo_teste.txt'
print(re.search(pattern, filename, re.IGNORECASE))
"
```

### **Problema: Campos não extraídos**
```bash
# Testar regex de captura
python -c "
import re
pattern = r'seu_record_pattern'
line = 'linha_exemplo'
match = re.match(pattern, line)
if match:
    print('Groups:', match.groups())
else:
    print('No match')
"
```

### **Problema: Atualização não aplicada**
```bash
# Verificar configuração
python -c "
import json
with open('formats_config.json', 'r') as f:
    config = json.load(f)
    print('Formats:', list(config['formats'].keys()))
"
```

---

## 📋 Checklist - Nova Compatibilidade

### **Antes de Commitar**
- [ ] Regex funciona com arquivos reais
- [ ] Todos os campos mapeados corretamente
- [ ] Números formatados corretamente
- [ ] Teste local passou
- [ ] JSON validado (sem erros de sintaxe)

### **Após Deploy**
- [ ] Sistema atualiza automaticamente
- [ ] Novo formato aparece na UI
- [ ] Conversão funciona em produção
- [ ] Logs mostram sucesso
- [ ] Usuários confirmam funcionamento

---

## 🎯 Exemplo Completo - Workflow Real

### **Dia 1: Solicitação do Cliente**
```
Cliente: "Precisamos converter arquivos do sistema X"
Arquivo exemplo: sistema_x.P01.txt
```

### **Dia 1 (Tarde): Análise**
```
1. Analisar estrutura do arquivo (30 min)
2. Criar regex patterns (45 min)
3. Configurar JSON (15 min)
4. Testar local (15 min)
```

### **Dia 1 (Noite): Deploy**
```
1. Commit e push (5 min)
2. Sistema atualiza automático (instantâneo)
3. Cliente testa (30 min)
4. Aprovação recebida 🎉
```

**Resultado: Novo formato implementado em menos de 24 horas!**

---

## 📚 Conclusão

O novo sistema transformou o processo de adicionar compatibilidades de:

- **SEMANAS** → **HORAS**
- **COMPLEXO** → **SIMPLES**  
- **ARRISCADO** → **SEGURO**
- **CUSTOSO** → **EFICIENTE**

**Agora qualquer novo formato pode ser adicionado em questão de horas, não dias!** 🚀

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar este documento
2. Executar testes locais
3. Consultar logs do sistema
4. Analisar exemplos em `formats_config_example.json`

**Desenvolvido por:** FA MARINGA LTDA  
**Versão do documento:** 1.0  
**Atualização:** 20/03/2026
