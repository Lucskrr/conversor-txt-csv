import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv
import re
import os
import threading
import base64
from datetime import datetime

# Importando sistema de logging profissional
try:
    from utils.logger import get_logger
    from utils.config_service import get_config
    LOGGER_AVAILABLE = True
except ImportError:
    LOGGER_AVAILABLE = False
    def _write_log(msg):
        log_file = os.path.join(os.path.dirname(__file__), 'converter.log')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {msg}\n")

VERSION = '1.1.0'
APP_NAME = 'Conversor TOTVS'
APP_AUTHOR = 'Fa Maringa'
COMPANY_NAME = 'FA MARINGA LTDA'

# Preferência por logo em arquivo local (PNG/GIF).
# Coloque c:\Users\Admin\Desktop\normalizar\logo.png ou logo.gif para exibir.
LOGO_CANDIDATES = ['logo.png', 'logo.gif']

# Drag-and-drop interoperability
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


def _parse_number(num_str):
    if num_str is None or num_str == "":
        return ""

    normalized = num_str.strip().replace('.', '').replace(',', '.')
    try:
        return float(normalized)
    except ValueError:
        return num_str.strip()


FORMATOS_COMPATIVEIS = ['gerr004', 'cdfr054']


def _get_logger():
    """Get logger instance with fallback"""
    if LOGGER_AVAILABLE:
        return get_logger('converter')
    else:
        class SimpleLogger:
            def info(self, msg): _write_log(f"INFO - {msg}")
            def error(self, msg): _write_log(f"ERROR - {msg}")
            def warning(self, msg): _write_log(f"WARNING - {msg}")
        return SimpleLogger()


def _get_output_csv_path(arquivo_txt, pasta_saida):
    base = os.path.splitext(os.path.basename(arquivo_txt))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = f"{base}_{timestamp}.csv"
    return os.path.join(pasta_saida, nome_arquivo)


def _detectar_formato(arquivo_txt):
    nome = os.path.basename(arquivo_txt).lower()
    if 'gerr004' in nome:
        return 'gerr004'
    if 'cdfr054' in nome:
        return 'cdfr054'

    with open(arquivo_txt, 'r', encoding='latin1') as f:
        conteudo = f.read(8192).upper()

    if 'GERR004' in conteudo:
        return 'gerr004'
    if 'CDFR054' in conteudo:
        return 'cdfr054'

    # fallback: gerr004 tem marca "UN" e cdfr054 tem colunas de valor unitário/total
    if re.search(r'\bUN\b', conteudo):
        return 'gerr004'

    return None


def _parse_gerr004(linhas, progress_callback=None, total=0):
    registros = []
    i = 0

    while i < len(linhas):
        linha = linhas[i]
        match = re.match(r"\s*(\d+)\s+(\d+)\s+(.*?)\s+UN\s+(\d+)\s+([\d,]+)", linha)

        if match:
            seq = match.group(1)
            codigo = match.group(2)
            descricao = match.group(3).strip()
            cod_barras = match.group(4)
            quantidade = _parse_number(match.group(5))

            if i + 1 < len(linhas):
                prox = linhas[i + 1]
                if prox.strip() and not re.match(r"\s*\d+\s+\d+", prox):
                    descricao += ' ' + prox.strip()
                    i += 1

            registros.append({
                'seq': seq,
                'codigo_produto': codigo,
                'descricao': descricao.strip(),
                'codigo_barras': cod_barras,
                'quantidade': quantidade,
                'valor_unitario': '',
                'valor_total': ''
            })

        i += 1
        if progress_callback:
            progress_callback(i, total)

    return registros


def _is_cdfr054_linha_dados(line):
    return bool(re.match(r"^\s*(\d+)\s+([^\s]+)\s+(.+?)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s*$", line))


def _parse_cdfr054(linhas, progress_callback=None, total=0):
    registros = []
    i = 0

    while i < len(linhas):
        linha = linhas[i]
        match = re.match(r"^\s*(\d+)\s+([^\s]+)\s+(.+?)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s*$", linha)

        if match:
            seq = match.group(1)
            codigo = match.group(2)
            descricao = match.group(3).strip()
            quantidade = _parse_number(match.group(4))
            valor_unitario = _parse_number(match.group(5))
            valor_total = _parse_number(match.group(6))

            while i + 1 < len(linhas):
                prox = linhas[i + 1]
                if prox.strip() and not _is_cdfr054_linha_dados(prox) and not re.search(r'^(DATA SISTEMA|DATA/HORA|PAGINA)', prox.strip().upper()):
                    descricao += ' ' + prox.strip()
                    i += 1
                else:
                    break

            registros.append({
                'seq': seq,
                'codigo_produto': codigo,
                'descricao': descricao.strip(),
                'codigo_barras': '',
                'quantidade': quantidade,
                'valor_unitario': valor_unitario,
                'valor_total': valor_total
            })

        i += 1
        if progress_callback:
            progress_callback(i, total)

    return registros


def _try_parse_format(linhas):
    for fmt in FORMATOS_COMPATIVEIS:
        if fmt == 'gerr004':
            registros = _parse_gerr004(linhas)
        elif fmt == 'cdfr054':
            registros = _parse_cdfr054(linhas)
        else:
            registros = []

        if registros:
            return fmt, registros

    return None, []


def normalizar_txt_para_csv(arquivo_txt, pasta_saida, progress_callback=None):
    with open(arquivo_txt, 'r', encoding='latin1') as f:
        linhas = f.readlines()

    total_linhas = len(linhas)
    formato = _detectar_formato(arquivo_txt)
    registros = []
    fallback = ''

    if formato in FORMATOS_COMPATIVEIS:
        if formato == 'gerr004':
            registros = _parse_gerr004(linhas, progress_callback=progress_callback, total=total_linhas)
        elif formato == 'cdfr054':
            registros = _parse_cdfr054(linhas, progress_callback=progress_callback, total=total_linhas)
    else:
        # tenta deduzir por parser direto
        fmt, registros = _try_parse_format(linhas)
        if fmt:
            fallback = f"Formato detectado por parser: {fmt}."
            formato = fmt

    if formato not in FORMATOS_COMPATIVEIS or not registros:
        raise ValueError(f"Formato não compatível: '{formato}'. Compatíveis: {', '.join(FORMATOS_COMPATIVEIS)}")

    caminho_csv = _get_output_csv_path(arquivo_txt, pasta_saida)

    os.makedirs(pasta_saida, exist_ok=True)

    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'seq',
            'codigo_produto',
            'descricao',
            'codigo_barras',
            'quantidade',
            'valor_unitario',
            'valor_total'
        ])

        for registro in registros:
            writer.writerow([
                registro.get('seq', ''),
                registro.get('codigo_produto', ''),
                registro.get('descricao', ''),
                registro.get('codigo_barras', ''),
                registro.get('quantidade', ''),
                registro.get('valor_unitario', ''),
                registro.get('valor_total', '')
            ])

    return caminho_csv, formato, len(registros), fallback


def selecionar_arquivo():
    arquivos = filedialog.askopenfilenames(filetypes=[("TXT files", "*.txt")])
    if arquivos:
        # manter o campo manual com o primeiro arquivo para compatibilidade
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, arquivos[0])
        for arquivo in arquivos:
            if arquivo not in listbox_files.get(0, tk.END):
                listbox_files.insert(tk.END, arquivo)


def add_files():
    arquivos = filedialog.askopenfilenames(filetypes=[("TXT files", "*.txt")])
    for arquivo in arquivos:
        if arquivo not in listbox_files.get(0, tk.END):
            listbox_files.insert(tk.END, arquivo)


def remove_selected_file():
    selection = listbox_files.curselection()
    for idx in reversed(selection):
        listbox_files.delete(idx)


def clear_files():
    listbox_files.delete(0, tk.END)


def _on_drop_files(event):
    data = event.data
    if not data:
        return
    arquivos = []

    # suporta caminhos com espaços e colocados entre chaves {C:/meu arquivo.txt}
    tokens = re.findall(r"\{([^}]*)\}|([^\s]+)", data)
    for brace_path, simple_path in tokens:
        path = brace_path or simple_path
        if path:
            path = path.strip()
            if os.path.isfile(path) and path.lower().endswith('.txt'):
                arquivos.append(path)

    for arquivo in arquivos:
        if arquivo not in listbox_files.get(0, tk.END):
            listbox_files.insert(tk.END, arquivo)


def _converter_background(arquivos, pasta_saida):

    def update_progress(value, maximum):
        def cb():
            progress['maximum'] = maximum
            progress['value'] = value
            if maximum:
                label_status.config(text=f'Convertendo... {int(value/maximum*100)}%')
            else:
                label_status.config(text='Convertendo...')
        janela.after(0, cb)

    results = []

    for idx, arquivo in enumerate(arquivos, start=1):
        if not arquivo:
            continue

        def set_file_label():
            label_status.config(text=f'Processando ({idx}/{len(arquivos)}): {os.path.basename(arquivo)}')
        janela.after(0, set_file_label)

        try:
            caminho_csv, formato, total, fallback = normalizar_txt_para_csv(arquivo, pasta_saida, progress_callback=update_progress)
            logger = _get_logger()
            logger.log_conversion_success(arquivo, caminho_csv, formato, total)
            results.append((True, arquivo, caminho_csv, formato, total, fallback))

        except Exception as e:
            logger = _get_logger()
            logger.log_conversion_error(arquivo, e)
            results.append((False, arquivo, str(e)))

    def finalize():
        sucesso = sum(1 for r in results if r[0])
        erro = sum(1 for r in results if not r[0])

        if sucesso > 0:
            mensagem = f"Conversão finalizada. Sucesso: {sucesso}. Erros: {erro}."
            messagebox.showinfo("Conclusão", mensagem)
        else:
            mensagem = f"Nenhum arquivo convertido. Erros: {erro}."
            messagebox.showerror("Conclusão", mensagem)

        # limpar seleções e permitir novo batch com entrada limpa
        listbox_files.delete(0, tk.END)
        entry_arquivo.delete(0, tk.END)

        label_status.config(text='Concluído')
        label_info.config(text=f"Processados: {sucesso}/{len(arquivos)}")
        botao_converter.config(state='normal')
        progress.stop()
        progress['value'] = 0
        janela.config(cursor='')

    janela.after(0, finalize)


def converter():
    # Prioriza lista batch, mas permite inserir caminho direto no campo
    caminho_manual = entry_arquivo.get().strip()
    arquivos = list(listbox_files.get(0, tk.END))

    if caminho_manual and caminho_manual not in arquivos:
        arquivos.append(caminho_manual)

    if not arquivos:
        messagebox.showerror("Erro", "Selecione pelo menos um arquivo TXT para converter.")
        return

    pasta_saida = filedialog.askdirectory(title="Selecione a pasta de saída")
    if not pasta_saida:
        messagebox.showwarning("Aviso", "Seleção de pasta cancelada. Conversão abortada.")
        return

    janela.config(cursor='watch')
    botao_converter.config(state='disabled')
    label_status.config(text='Iniciando conversão...')
    progress['value'] = 0

    t = threading.Thread(target=_converter_background, args=(arquivos, pasta_saida), daemon=True)
    t.start()


# janela
if DND_AVAILABLE:
    janela = TkinterDnD.Tk()
else:
    janela = tk.Tk()

janela.title("Conversor TXT → CSV")
janela.geometry("760x620")
janela.configure(bg='#ECE9D8')

# cabeçalho do app com logo, título e versão
logo_image = None
for candidate in LOGO_CANDIDATES:
    logo_path = os.path.join(os.path.dirname(__file__), candidate)
    if os.path.isfile(logo_path):
        try:
            logo_image = tk.PhotoImage(file=logo_path)
            logger = _get_logger()
            logger.info(f"Logo carregado: {logo_path}")
        except Exception as e:
            logo_image = None
            logger = _get_logger()
            logger.error(f"Falha ao carregar {logo_path}: {e}")
        break

header_frame = tk.Frame(janela, padx=10, pady=10, relief='groove', bd=1, bg='#ECE9D8')
header_frame.pack(fill='x', padx=10, pady=8)

# logo + metadados título
logo_label = tk.Label(header_frame, image=logo_image if logo_image else None, width=64, height=64, bg='#ECE9D8')
if logo_image:
    logo_label.image = logo_image
else:
    logo_label.config(text='[Logo]', font=('Arial', 14, 'bold'), bg='#f0f0f0', width=8, height=4)
logo_label.pack(side='left', padx=(0, 12), pady=4)

title_frame = tk.Frame(header_frame, bg='#ECE9D8')
title_frame.pack(side='left', fill='both', expand=True)

label_app = tk.Label(
    title_frame,
    text=APP_NAME,
    font=('Arial', 20, 'bold'),
    fg='#1f4e79',
    bg='#ECE9D8'
)
label_app.pack(anchor='w', pady=10)
# campo de seleção de arquivos em batch
frame_arquivo = tk.Frame(janela, relief='groove', bd=1, padx=8, pady=8, bg='#ECE9D8')
frame_arquivo.pack(pady=5, padx=10, fill='x')

label = tk.Label(frame_arquivo, text="Arquivo TXT (ou lote):", font=('Arial', 10, 'bold'))
label.grid(row=0, column=0, sticky='w')

entry_arquivo = tk.Entry(frame_arquivo, width=70, font=('Arial', 10))
entry_arquivo.grid(row=1, column=0, sticky='ew', padx=(0, 5), pady=2)

botao_buscar = tk.Button(frame_arquivo, text="Selecionar arquivo", command=selecionar_arquivo, width=20)
botao_buscar.grid(row=1, column=1, padx=5, pady=2)

frame_arquivo.grid_columnconfigure(0, weight=1)

frame_listbox = tk.Frame(janela, relief='sunken', bd=1)
frame_listbox.pack(pady=5, padx=10, fill='both', expand=True)

listbox_files = tk.Listbox(frame_listbox, selectmode='extended', height=8)
scrollbar_files = tk.Scrollbar(frame_listbox, orient='vertical', command=listbox_files.yview)
listbox_files.config(yscrollcommand=scrollbar_files.set)
listbox_files.pack(side='left', fill='both', expand=True)
scrollbar_files.pack(side='left', fill='y')

label_drag = tk.Label(janela, text='Solte os arquivos aqui', fg='blue')
label_drag.pack(pady=2)

# Suporte para arrastar e soltar (se disponível)
dnd_enabled = False
if DND_AVAILABLE:
    try:
        listbox_files.drop_target_register(DND_FILES)
        listbox_files.dnd_bind('<<Drop>>', _on_drop_files)
        dnd_enabled = True
    except Exception as e:
        logger = _get_logger()
        logger.warning(f"DND falhou na lista: {e}")

if not dnd_enabled:
    # Tentar o modo nativo TkDND se disponível
    try:
        listbox_files.drop_target_register(tk.DND_FILES)
        listbox_files.dnd_bind('<<Drop>>', _on_drop_files)
        dnd_enabled = True
    except Exception as e:
        logger = _get_logger()
        logger.warning(f"DND nativo não disponível: {e}")

if dnd_enabled:
    label_drag.config(text='Solte os arquivos aqui', fg='darkgreen')
else:
    label_drag.config(text='Solte os arquivos aqui (arraste e solte não suportado no ambiente)', fg='red')


frame_list_buttons = tk.Frame(janela)
frame_list_buttons.pack(pady=10)

botao_add = tk.Button(frame_list_buttons, text="Adicionar arquivos", command=add_files, width=18)
botao_add.grid(row=0, column=0, padx=6, pady=2)

botao_remove = tk.Button(frame_list_buttons, text="Remover selecionados", command=remove_selected_file, width=18)
botao_remove.grid(row=0, column=1, padx=6, pady=2)

botao_clear = tk.Button(frame_list_buttons, text="Limpar lista", command=clear_files, width=18)
botao_clear.grid(row=0, column=2, padx=6, pady=2)

botao_converter = tk.Button(janela, text="Converter", command=converter, width=24, bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'))
botao_converter.pack(pady=12)

status_frame = tk.Frame(janela, relief='groove', bd=1, padx=10, pady=8, bg='#ECE9D8')
status_frame.pack(fill='x', padx=10, pady=(0, 10))

label_status = tk.Label(status_frame, text="Aguardando...", font=('Arial', 10, 'bold'), fg='#333333', bg='#ECE9D8')
label_status.grid(row=0, column=0, sticky='w')

label_info = tk.Label(status_frame, text="Formato: - | Registros: -", font=('Arial', 10), fg='#555555', bg='#ECE9D8')
label_info.grid(row=1, column=0, sticky='w', pady=(4,0))

progress = ttk.Progressbar(status_frame, mode='determinate', length=520)
progress.grid(row=2, column=0, sticky='ew', pady=8)

status_frame.grid_columnconfigure(0, weight=1)

footer_frame = tk.Frame(janela, bg='#ECE9D8', padx=10, pady=6)
footer_frame.pack(fill='x', side='bottom')

current_year = datetime.now().year

footer_text = f"© {current_year} {COMPANY_NAME} • Desenvolvido por {APP_AUTHOR} • Todos os direitos reservados"
footer_label = tk.Label(footer_frame, text=footer_text, font=('Arial', 9), fg='#444444', bg='#e0e3e8')
footer_label.pack(side='left')

janela.mainloop()