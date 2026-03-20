#!/usr/bin/env python3
"""
Clean professional conversor app
"""

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# Add project root to path
def setup_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    if application_path not in sys.path:
        sys.path.insert(0, application_path)
    
    return application_path

class ProfessionalConversorApp:
    """Professional clean conversor app"""
    
    def __init__(self):
        self.app_dir = setup_path()
        self.selected_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup clean professional UI"""
        # Main window
        self.root = tk.Tk()
        self.root.title("Conversor TOTVS v2.0.0")
        self.root.geometry("900x700")
        self.root.configure(bg='#ffffff')
        self.root.resizable(True, True)
        
        # Configure styles
        self.setup_styles()
        
        # Header
        self.create_header()
        
        # Main content
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def setup_styles(self):
        """Setup professional styles"""
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff',
            'border': '#bdc3c7'
        }
        
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'subtitle': ('Segoe UI', 12),
            'normal': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'button': ('Segoe UI', 10, 'bold')
        }
    
    def create_header(self):
        """Create professional header"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title container
        title_container = tk.Frame(header_frame, bg=self.colors['primary'])
        title_container.pack(expand=True)
        
        title_label = tk.Label(
            title_container,
            text="Conversor TOTVS",
            font=self.fonts['title'],
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        title_label.pack(pady=(10, 2))
        
        subtitle_label = tk.Label(
            title_container,
            text="Sistema de Conversão TXT para CSV",
            font=self.fonts['subtitle'],
            fg=self.colors['light'],
            bg=self.colors['primary']
        )
        subtitle_label.pack()
    
    def create_main_content(self):
        """Create main content area"""
        content_frame = tk.Frame(self.root, bg=self.colors['white'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # File selection section
        self.create_file_section(content_frame)
        
        # Conversion section
        self.create_conversion_section(content_frame)
        
        # Info section
        self.create_info_section(content_frame)
    
    def create_file_section(self, parent):
        """Create file selection section"""
        # Section frame
        section_frame = tk.LabelFrame(
            parent,
            text="Seleção de Arquivos",
            font=self.fonts['subtitle'],
            bg=self.colors['white'],
            fg=self.colors['dark'],
            relief='solid',
            borderwidth=1
        )
        section_frame.pack(fill='x', pady=(0, 15))
        
        # Button container
        button_container = tk.Frame(section_frame, bg=self.colors['white'])
        button_container.pack(pady=15, padx=15)
        
        # Select files button
        select_btn = tk.Button(
            button_container,
            text="Selecionar Arquivos",
            command=self.select_files,
            font=self.fonts['button'],
            bg=self.colors['accent'],
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            width=15
        )
        select_btn.pack(side='left', padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(
            button_container,
            text="Limpar",
            command=self.clear_files,
            font=self.fonts['button'],
            bg=self.colors['danger'],
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            width=10
        )
        clear_btn.pack(side='left')
        
        # File list
        list_container = tk.Frame(section_frame, bg=self.colors['white'])
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Listbox with scrollbar
        list_frame = tk.Frame(list_container, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.file_listbox = tk.Listbox(
            list_frame,
            height=6,
            yscrollcommand=scrollbar.set,
            font=self.fonts['normal'],
            bg=self.colors['white'],
            fg=self.colors['dark'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['white'],
            relief='solid',
            borderwidth=1
        )
        self.file_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.file_listbox.yview)
    
    def create_conversion_section(self, parent):
        """Create conversion section"""
        # Section frame
        section_frame = tk.LabelFrame(
            parent,
            text="Conversão",
            font=self.fonts['subtitle'],
            bg=self.colors['white'],
            fg=self.colors['dark'],
            relief='solid',
            borderwidth=1
        )
        section_frame.pack(fill='x', pady=(0, 15))
        
        # Output directory
        output_container = tk.Frame(section_frame, bg=self.colors['white'])
        output_container.pack(fill='x', padx=15, pady=15)
        
        tk.Label(
            output_container,
            text="Pasta de Saída:",
            font=self.fonts['normal'],
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(side='left')
        
        self.output_var = tk.StringVar(value=str(Path.home() / "Desktop" / "Convertidos"))
        output_entry = tk.Entry(
            output_container,
            textvariable=self.output_var,
            font=self.fonts['normal'],
            bg=self.colors['white'],
            fg=self.colors['dark'],
            relief='solid',
            borderwidth=1
        )
        output_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        browse_btn = tk.Button(
            output_container,
            text="...",
            command=self.browse_output,
            font=self.fonts['normal'],
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            width=3
        )
        browse_btn.pack(side='left')
        
        # Convert button
        convert_container = tk.Frame(section_frame, bg=self.colors['white'])
        convert_container.pack(pady=15)
        
        self.convert_btn = tk.Button(
            convert_container,
            text="CONVERTER ARQUIVOS",
            command=self.convert_files,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            width=25,
            height=2
        )
        self.convert_btn.pack()
        
        # Progress
        self.progress_var = tk.StringVar(value="Pronto para converter")
        progress_label = tk.Label(
            section_frame,
            textvariable=self.progress_var,
            font=self.fonts['small'],
            bg=self.colors['white'],
            fg=self.colors['dark']
        )
        progress_label.pack(pady=(0, 10))
    
    def create_info_section(self, parent):
        """Create information section"""
        # Section frame
        section_frame = tk.LabelFrame(
            parent,
            text="Informações do Sistema",
            font=self.fonts['subtitle'],
            bg=self.colors['white'],
            fg=self.colors['dark'],
            relief='solid',
            borderwidth=1
        )
        section_frame.pack(fill='x')
        
        # Info content
        info_container = tk.Frame(section_frame, bg=self.colors['white'])
        info_container.pack(fill='x', padx=15, pady=15)
        
        info_text = """Sistema: Conversor TOTVS v2.0.0
Status: 100% Operacional

Formatos Suportados:
• gerr004 - Produtos com código de barras
• cdfr054 - Produtos com valores

Novos Formatos:
Edite o arquivo formats_config.json
Commit e push no GitHub
Sistema atualiza automaticamente

Atualizações:
Verificação automática de novas versões
Download com permissão do usuário
Interface amigável de atualização"""
        
        info_label = tk.Label(
            info_container,
            text=info_text,
            font=self.fonts['normal'],
            bg=self.colors['white'],
            fg=self.colors['dark'],
            justify='left'
        )
        info_label.pack()
    
    def create_footer(self):
        """Create footer"""
        footer_frame = tk.Frame(self.root, bg=self.colors['light'], height=30)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="FA MARINGA LTDA - Versão 2.0.0",
            font=self.fonts['small'],
            bg=self.colors['light'],
            fg=self.colors['dark']
        )
        footer_label.pack(expand=True)
    
    def select_files(self):
        """Select files for conversion"""
        files = filedialog.askopenfilenames(
            title="Selecione arquivos TXT",
            filetypes=[("Arquivos TXT", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))
            
            self.progress_var.set(f"{len(self.selected_files)} arquivo(s) selecionado(s)")
    
    def clear_files(self):
        """Clear selected files"""
        self.selected_files = []
        self.file_listbox.delete(0, tk.END)
        self.progress_var.set("Pronto para converter")
    
    def browse_output(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Selecione pasta de saída")
        if directory:
            self.output_var.set(directory)
    
    def convert_files(self):
        """Convert selected files"""
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo!")
            return
        
        output_dir = self.output_var.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Disable button during conversion
        self.convert_btn.config(state='disabled')
        self.progress_var.set("Convertendo arquivos...")
        self.root.update()
        
        try:
            # Try to use the real converter
            from core.enhanced_converter import get_batch_converter
            converter = get_batch_converter()
            
            converted = 0
            errors = 0
            
            for i, file_path in enumerate(self.selected_files, 1):
                filename = os.path.basename(file_path)
                self.progress_var.set(f"Convertendo {i}/{len(self.selected_files)}: {filename}")
                self.root.update()
                
                try:
                    success, message, output_file = converter.convert_file(file_path, output_dir)
                    if success:
                        converted += 1
                    else:
                        errors += 1
                except Exception as e:
                    errors += 1
            
            # Show result
            if converted > 0:
                messagebox.showinfo(
                    "Conversão Concluída",
                    f"Sucesso: {converted} arquivo(s)\nErros: {errors} arquivo(s)"
                )
            else:
                messagebox.showwarning("Conversão", "Nenhum arquivo foi convertido com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante conversão: {e}")
        
        finally:
            self.convert_btn.config(state='normal')
            self.progress_var.set("Conversão concluída")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = ProfessionalConversorApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()
