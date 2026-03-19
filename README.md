# Conversor TOTVS

Uma aplicação desktop profissional para converter arquivos TXT dos sistemas TOTVS (formatos GERR004 e CDFR054) para CSV, desenvolvida em Python com Tkinter.

## 🚀 Características

- **Conversão em Lote**: Processa múltiplos arquivos simultaneamente
- **Detecção Automática**: Identifica automaticamente o formato do arquivo (GERR004/CDFR054)
- **Interface Profissional**: Design corporativo com suporte a drag-and-drop
- **Progresso em Tempo Real**: Barra de progresso detalhada durante a conversão
- **Logging Completo**: Sistema de logs para auditoria e debugging
- **Tratamento de Erros**: Mensagens amigáveis e recuperação de erros
- **Distribuição Pronta**: Configurado para PyInstaller com otimizações

## 📋 Formatos Suportados

### GERR004
Formato de relatório de estoque do TOTVS com campos:
- Sequencial
- Código do Produto
- Descrição
- Código de Barras
- Quantidade

### CDFR054
Formato de relatório financeiro do TOTVS com campos:
- Sequencial
- Código do Produto
- Descrição
- Quantidade
- Valor Unitário
- Valor Total

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Windows (recomendado)

### Dependências
```bash
pip install -r requirements.txt
```

### Opcional - Suporte Drag-and-Drop
```bash
pip install tkinterdnd2
```

## 🚀 Execução

### Modo Desenvolvimento
```bash
python main_app.py
```

### Compilação para Distribuição
```bash
# Usando o spec file otimizado
pyinstaller converter_new.spec

# Ou compilação simples
pyinstaller --onefile --windowed --name ConversorTOTVS main_app.py
```

## 📁 Estrutura do Projeto

```
conversor-totvs/
├── main_app.py              # Aplicação principal
├── config.py                # Configurações e constantes
├── logger.py                # Sistema de logging
├── exceptions.py            # Exceções personalizadas
├── parsers.py               # Parsers de formato
├── converter_engine.py      # Motor de conversão
├── ui_components.py         # Componentes UI reutilizáveis
├── requirements.txt         # Dependências
├── converter_new.spec       # Configuração PyInstaller
├── README.md               # Documentação
├── logo.png               # Logo da aplicação (opcional)
├── logo.gif               # Logo alternativo (opcional)
└── converter.log           # Arquivo de log (gerado automaticamente)
```

## 🔧 Configuração

### Personalização
Edite `config.py` para modificar:
- Cores da interface
- Formatos suportados
- Configurações de logging
- Metadados da aplicação

### Logo
Adicione `logo.png` ou `logo.gif` no diretório raiz para personalizar o ícone da aplicação.

## 📊 Uso

1. **Selecionar Arquivos**
   - Clique em "Selecionar arquivo" para escolher um arquivo
   - Use "Adicionar arquivos" para múltiplos arquivos
   - Arraste e solte arquivos TXT na lista

2. **Converter**
   - Clique em "Converter"
   - Escolha a pasta de saída
   - Aguarde o processamento

3. **Resultados**
   - Arquivos CSV são gerados com timestamp
   - Logs detalhados em `converter.log`
   - Relatório de sucesso/erros ao final

## 🐛 Troubleshooting

### Problemas Comuns

**Drag-and-drop não funciona**
- Instale: `pip install tkinterdnd2`
- Verifique se o ambiente suporta TkDND

**Erro de codificação**
- Verifique se os arquivos TXT usam encoding Latin-1 (ISO-8859-1)

**Formato não reconhecido**
- Verifique se o arquivo contém "GERR004" ou "CDFR054"
- O sistema tenta detectar automaticamente o formato

### Logs
Verifique `converter.log` para detalhes de:
- Conversões realizadas
- Erros encontrados
- Informações de debugging

## 🏗️ Arquitetura

### Separação de Responsabilidades
- **UI Layer**: `main_app.py`, `ui_components.py`
- **Business Logic**: `converter_engine.py`, `parsers.py`
- **Infrastructure**: `config.py`, `logger.py`, `exceptions.py`

### Design Patterns
- **Factory Pattern**: `ParserFactory` para criação de parsers
- **Strategy Pattern**: Diferentes parsers para cada formato
- **Observer Pattern**: Callbacks de progresso
- **Singleton Pattern**: Logger centralizado

## 📦 Distribuição

### Build de Produção
```bash
# Build otimizado
pyinstaller converter_new.spec

# O executável será gerado em dist/ConversorTOTVS.exe
```

### Instalador
Use ferramentas como Inno Setup ou NSIS para criar um instalador profissional com:
- Atalhos no menu iniciar
- Desinstalador
- Associação de arquivos .txt

## 🔮 Futuras Melhorias

### Planejado
- [ ] Sistema de auto-atualização via GitHub releases
- [ ] Sistema de licenciamento (validação por máquina)
- [ ] Suporte a mais formatos TOTVS
- [ ] Interface configurável (temas)
- [ ] Export direto para Excel
- [ ] Validação de dados avançada

### Extensibilidade
O código foi projetado para facilitar:
- Adição de novos formatos
- Personalização da interface
- Integração com outros sistemas

## 📝 Licença

© 2024 FA MARINGA LTDA - Todos os direitos reservados

Desenvolvido por: Fa Maringa

## 🤝 Suporte

Para suporte técnico:
- Verifique os logs em `converter.log`
- Consulte esta documentação
- Entre em contato com o desenvolvedor

---

**Conversor TOTVS** - Solução profissional para conversão de dados TOTVS
