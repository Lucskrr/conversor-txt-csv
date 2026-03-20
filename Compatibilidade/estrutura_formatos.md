# 🔍 Estrutura Detalhada dos Formatos TOTVS

## 📊 GERR004.P00 - Relatório de Contagem

### 📋 **Identificação**
- **Formato**: GERR004
- **Versão**: P00
- **Descrição**: Relatório de contagem de estoque
- **Empresa**: 003 - FA MARINGA LTDA. - MATRIZ

### 🏗️ **Estrutura do Arquivo**

#### **Cabeçalho**
```
Linha 1: GERR004 - Relatório de Contagem
Linha 2: Linha separadora (-------------------)
Linha 3: Informações da empresa e situação
Linha 4-10: Dados do processo (número, anotador, descrição)
```

#### **Dados Principais**
- **Empresa**: Código da empresa (003)
- **Número**: Número do processo (1088)
- **Anotador**: Responsável pela contagem
- **Descrição**: Detalhes do processo
- **Situação**: Em andamento

#### **Campos Típicos**
- Código do produto
- Descrição do item
- Quantidade contada
- Unidade de medida
- Localização

---

## 📈 CDFR054.P08 - Movimentação de O.P.

### 📋 **Identificação**
- **Formato**: CDFR054
- **Versão**: P08
- **Descrição**: Relatório de movimentação de ordem de produção com valoração
- **Empresa**: 003 - FA MTZ - MODA

### 🏗️ **Estrutura do Arquivo**

#### **Cabeçalho**
```
Linha 1: Empresa + CDFR054 + Descrição completa
Linha 2-3: Parâmetros e configurações
Linha 4: Cabeçalho da tabela (Local, Grupo, Qt. produzida, Vl. unitario, Vl. total)
```

#### **Dados Principais**
- **Local**: Código do local de produção (21)
- **Grupo**: Tipo de serviço (CORTE)
- **Produto**: Código e descrição do produto
- **Quantidade**: Qt. produzida
- **Valores**: Vl. unitario e Vl. total

#### **Campos Típicos**
```
Servico: 21
Grupo: CORTE
Produto: 4 7200527E CAMISETA POLO MC MASC MONT LONG C/ BOLSO
Qt. produzida: 48,000
Vl. unitario: 2,5000
Vl. total: 120,0000
```

---

## � CDFR054.P06 - Movimentação de O.P. (Versão Atualizada)

### 📋 **Identificação**
- **Formato**: CDFR054
- **Versão**: P06
- **Descrição**: Relatório de movimentação de ordem de produção com valoração
- **Empresa**: 003 - FA MTZ - MODA
- **Data**: 20/03/2026

### 🏗️ **Estrutura do Arquivo**

#### **Cabeçalho**
```
Linha 1: Empresa + CDFR054 + Descrição completa
Linha 2-3: Parâmetros e configurações
Linha 4: Data do relatório
Linha 5: Cabeçalho da tabela (Local, Grupo, Qt. produzida, Vl. unitario, Vl. total)
```

#### **Dados Principais**
- **Local**: Código do local de produção (41)
- **Grupo**: Tipo de serviço (TINGIR BOTOES)
- **Produto**: Código e descrição do produto
- **Quantidade**: Qt. produzida
- **Valores**: Vl. unitario e Vl. total

#### **Campos Típicos**
```
Servico: 41
Grupo: TINGIR BOTOES
Produto: 105 7200527E CAMISETA POLO MC MASC MONT LONG C/ BOLSO
Qt. produzida: 528,000
Vl. unitario: 0,4000
Vl. total: 211,2000
```

---

## �🔧 **Processo de Conversão**

### **Etapa 1: Detecção Automática**
- Analisa as primeiras linhas do arquivo
- Identifica o formato (GERR004 ou CDFR054)
- Determina a versão (P00, P08, etc.)

### **Etapa 2: Parsing**
- Extrai cabeçalho e metadados
- Identifica estrutura de dados
- Mapeia campos para CSV

### **Etapa 3: Geração CSV**
- Cria colunas padronizadas
- Preenche dados extraídos
- Formata valores (números, datas)

---

## 📝 **Exemplo de Saída CSV**

### GERR004.P00 → CSV
```csv
empresa,numero,anotador,descricao,situacao
003,1088,"1173BEATRIZ G. R. DA SILVA - MODA","BAND P/ LOJINHA","Em andamento"
```

### CDFR054.P08 → CSV
```csv
local,grupo,produto,qt_produzida,vl_unitario,vl_total
21,"CORTE","4 7200527E CAMISETA POLO MC MASC MONT LONG C/ BOLSO",48.000,2.5000,120.0000
```

---

## 🚀 **Novos Formatos**

Para adicionar novos formatos:

1. **Analise a estrutura** do arquivo TXT
2. **Identifique padrões** fixos
3. **Mapeie campos** para CSV
4. **Crie parser** específico
5. **Teste com exemplos**
6. **Documente aqui**

---

*Documentação atualizada em: 20/03/2026*
