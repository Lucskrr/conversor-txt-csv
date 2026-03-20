# Como Adicionar Novos Formatos ao Conversor TOTVS

## 📋 Resumo

**Não precisa mais criar novo executável!** Agora você pode adicionar novos formatos apenas editando o arquivo `formats_config.json` e fazendo commit no Git.

## 🔧 Como Funciona

### 1. **Estrutura do JSON**

Cada formato tem estas propriedades:

```json
{
  "nome_do_formato": {
    "pattern": "regex para identificar arquivo",
    "content_pattern": "regex para identificar conteúdo", 
    "description": "Descrição do formato",
    "record_pattern": "regex para extrair dados da linha",
    "field_mapping": { "campo": numero_grupo_regex },
    "multiline_description": true/false,
    "number_fields": ["campos_que_sao_numeros"],
    "csv_headers": ["colunas_do_csv"]
  }
}
```

### 2. **Exemplo Prático**

#### **Formato Original (parsers.py):**
```python
# GERR004Parser.py
match = re.match(r"\s*(\d+)\s+(\d+)\s+(.*?)\s+UN\s+(\d+)\s+([\d,]+)", line)
seq = match.group(1)
codigo = match.group(2)
descricao = match.group(3)
cod_barras = match.group(4)
quantidade = NumberParser.parse_number(match.group(5))
```

#### **Equivalente em JSON:**
```json
{
  "gerr004": {
    "record_pattern": "^\\s*(\\d+)\\s+(\\d+)\\s+(.*?)\\s+UN\\s+(\\d+)\\s+([\\d,]+)",
    "field_mapping": {
      "seq": 1,
      "codigo_produto": 2,
      "descricao": 3,
      "codigo_barras": 4,
      "quantidade": 5
    },
    "number_fields": ["quantidade"]
  }
}
```

## 🚀 Adicionando Novo Formato

### **Passo 1: Analisar o Arquivo**

Suponha que você tenha um arquivo assim:
```
001;12345678901234;PRODUTO EXEMPLO;10;5,50;55,00
002;98765432109876;OUTRO PRODUTO;5;12,30;61,50
```

### **Passo 2: Criar Regex**

```regex
^(\d{3});(\d{14});(.*);(\d+);([\d,]+);([\d,]+)$
```

### **Passo 3: Adicionar ao JSON**

```json
{
  "meu_novo_formato": {
    "pattern": "meu_formato\\.P\\d{2}\\.(txt|TXT)$",
    "content_pattern": "PRODUTO|EXEMPLO",
    "description": "Meu novo formato - CSV delimitado por ponto e vírgula",
    "record_pattern": "^(\\d{3});(\\d{14});(.*);(\\d+);([\\d,]+);([\\d,]+)$",
    "field_mapping": {
      "seq": 1,
      "codigo_produto": 2,
      "descricao": 3,
      "codigo_barras": null,
      "quantidade": 4,
      "valor_unitario": 5,
      "valor_total": 6
    },
    "multiline_description": false,
    "number_fields": ["quantidade", "valor_unitario", "valor_total"],
    "csv_headers": ["seq", "codigo_produto", "descricao", "codigo_barras", "quantidade", "valor_unitario", "valor_total"]
  }
}
```

### **Passo 4: Atualizar Sistema**

```bash
git add formats_config.json
git commit -m "feat: add novo formato meu_novo_formato"
git push origin main
```

### **Passo 5: Pronto!**

- ✅ Sistema detecta automaticamente o novo formato
- ✅ Aplicativo atualiza formatos sem precisar de novo executável
- ✅ Usuários veem o novo formato funcionando imediatamente

## 📖 Referência de Campos

| Campo | Descrição | Exemplo |
|-------|----------|---------|
| `pattern` | Regex para nome do arquivo | `"meu_formato\\.P\\d{2}\\.(txt|TXT)$"` |
| `content_pattern` | Regex para conteúdo do arquivo | `"PRODUTO\|EXEMPLO"` |
| `record_pattern` | Regex para extrair dados | `"^(\\d{3});(.*)$"` |
| `field_mapping` | Mapeamento grupo → campo | `{"seq": 1, "descricao": 2}` |
| `multiline_description` | Suporte a descrições multi-linha | `true/false` |
| `number_fields` | Campos que são números | `["quantidade", "valor"]` |
| `csv_headers` | Cabeçalhos do CSV final | `["seq", "descricao"]` |

## 🎯 Vantagens

- ✅ **Sem rebuild** - Não precisa compilar novo executável
- ✅ **Atualização instantânea** - Sistema baixa JSON automaticamente  
- ✅ **Fácil testar** - Apenas edite o JSON e teste
- ✅ **Versionamento** - Git controla mudanças nos formatos
- ✅ **Rollback** - Pode voltar para versão anterior facilmente

## 🔍 Testando Novo Formato

1. **Edite local**: `formats_config.json`
2. **Teste**: `python test_json_parser.py`
3. **Ajuste**: Regex até funcionar
4. **Commit**: `git push`
5. **Deploy**: Sistema atualiza automaticamente

**Agora adicionar novos formatos é tão fácil quanto editar um arquivo JSON!** 🎉
