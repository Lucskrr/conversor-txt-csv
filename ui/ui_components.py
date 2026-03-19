"""
UI components for Conversor TOTVS
Reusable UI elements and styling
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from utils.config_service import get_config
from utils.logger import get_logger


class StyleManager:
    """Manages UI styling and themes"""
    
    @staticmethod
    def configure_styles():
        """Configure ttk styles"""
        config = get_config()
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Primary.TButton', 
                       background=config.get('PRIMARY_COLOR'),
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Primary.TButton',
                 background=[('active', '#45a049')])
        
        style.configure('Secondary.TButton',
                       background='lightgray',
                       foreground=config.get('TEXT_COLOR'),
                       font=('Arial', 9),
                       borderwidth=1,
                       focuscolor='none')
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background='white',
                       relief='raised',
                       borderwidth=1)


class HeaderFrame(tk.Frame):
    """Application header with logo and title"""
    
    def __init__(self, parent, **kwargs):
        config = get_config()
        super().__init__(parent, padx=10, pady=10, relief='groove', bd=1, 
                        bg=config.get('HEADER_BG_COLOR'), **kwargs)
        
        self.logger = get_logger(__name__)
        self.logo_image = None
        self._load_logo()
        self._create_widgets()
    
    def _load_logo(self):
        """Load application logo"""
        config = get_config()
        logo_candidates = config.get('LOGO_CANDIDATES')
        
        for candidate in logo_candidates:
            logo_path = Path(__file__).parent.parent.parent / candidate
            if logo_path.exists():
                try:
                    self.logo_image = tk.PhotoImage(file=str(logo_path))
                    self.logger.info(f"Logo loaded: {logo_path}")
                    break
                except Exception as e:
                    self.logger.warning(f"Failed to load {logo_path}: {e}")
    
    def _create_widgets(self):
        """Create header widgets"""
        config = get_config()
        
        # Logo placeholder
        self.logo_label = tk.Label(
            self, 
            image=self.logo_image if self.logo_image else None,
            width=64, 
            height=64, 
            bg=config.get('HEADER_BG_COLOR')
        )
        
        if self.logo_image:
            self.logo_label.image = self.logo_image
        else:
            self.logo_label.config(
                text='[Logo]', 
                font=('Arial', 14, 'bold'), 
                bg='#f0f0f0', 
                width=8, 
                height=4
            )
        
        self.logo_label.pack(side='left', padx=(0, 12), pady=4)
        
        # Title frame
        self.title_frame = tk.Frame(self, bg=config.get('HEADER_BG_COLOR'))
        self.title_frame.pack(side='left', fill='both', expand=True)
        
        # App title
        self.app_label = tk.Label(
            self.title_frame,
            text=config.get('APP_NAME'),
            font=('Arial', 20, 'bold'),
            fg=config.get('ACCENT_COLOR'),
            bg=config.get('HEADER_BG_COLOR')
        )
        self.app_label.pack(anchor='w', pady=(10, 0))
        
        # Version info
        self.version_label = tk.Label(
            self.title_frame,
            text=f"Versão {config.get('VERSION')}",
            font=('Arial', 10),
            fg=config.get('SECONDARY_TEXT_COLOR'),
            bg=config.get('HEADER_BG_COLOR')
        )
        self.version_label.pack(anchor='w')


class FooterFrame(tk.Frame):
    """Application footer with copyright information"""
    
    def __init__(self, parent, **kwargs):
        config = get_config()
        super().__init__(parent, bg=config.get('FOOTER_BG_COLOR'), padx=10, pady=6, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create footer widgets"""
        from datetime import datetime
        config = get_config()
        current_year = datetime.now().year
        
        footer_text = f"© {current_year} {config.get('COMPANY_NAME')} • Desenvolvido por {config.get('APP_AUTHOR')} • Todos os direitos reservados"
        
        self.footer_label = tk.Label(
            self,
            text=footer_text,
            font=('Arial', 9),
            fg=config.get('DISABLED_TEXT_COLOR'),
            bg=config.get('FOOTER_BG_COLOR')
        )
        self.footer_label.pack(side='left')


class FileSelectionFrame(tk.Frame):
    """Frame for file selection"""
    
    def __init__(self, parent, **kwargs):
        config = get_config()
        super().__init__(parent, relief='groove', bd=1, padx=8, pady=8, 
                        bg=config.get('WINDOW_BG_COLOR'), **kwargs)
        
        self.entry_var = tk.StringVar()
        self._create_widgets()
    
    def _create_widgets(self):
        """Create file selection widgets"""
        config = get_config()
        
        # Label
        self.label = tk.Label(
            self, 
            text="Arquivo TXT (ou lote):", 
            font=('Arial', 10, 'bold'),
            bg=config.get('WINDOW_BG_COLOR')
        )
        self.label.grid(row=0, column=0, sticky='w')
        
        # Entry field
        self.entry = tk.Entry(self, width=70, font=('Arial', 10), textvariable=self.entry_var)
        self.entry.grid(row=1, column=0, sticky='ew', padx=(0, 5), pady=2)
        
        # Browse button
        self.browse_button = tk.Button(
            self, 
            text="Selecionar arquivo", 
            width=20
        )
        self.browse_button.grid(row=1, column=1, padx=5, pady=2)
        
        self.grid_columnconfigure(0, weight=1)
    
    def get_file_path(self) -> str:
        """Get current file path"""
        return self.entry_var.get().strip()
    
    def set_file_path(self, path: str):
        """Set file path"""
        self.entry_var.set(path)
    
    def clear(self):
        """Clear the entry field"""
        self.entry_var.set('')


class FileListFrame(tk.Frame):
    """Frame for displaying and managing file list"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, relief='sunken', bd=1, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create file list widgets"""
        # Listbox with scrollbar
        self.listbox = tk.Listbox(self, selectmode='extended', height=8)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.listbox.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='left', fill='y')
    
    def add_file(self, file_path: str):
        """Add file to list"""
        if file_path not in self.get_files():
            self.listbox.insert(tk.END, file_path)
    
    def remove_selected(self):
        """Remove selected files"""
        selection = self.listbox.curselection()
        for idx in reversed(selection):
            self.listbox.delete(idx)
    
    def clear_all(self):
        """Clear all files"""
        self.listbox.delete(0, tk.END)
    
    def get_files(self) -> list:
        """Get all files in list"""
        return list(self.listbox.get(0, tk.END))
    
    def get_selected_files(self) -> list:
        """Get selected files"""
        selection = self.listbox.curselection()
        return [self.listbox.get(idx) for idx in selection]


class ButtonPanelFrame(tk.Frame):
    """Panel with action buttons"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.buttons = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """Create button widgets"""
        button_configs = [
            ("add", "Adicionar arquivos", 0, 0),
            ("remove", "Remover selecionados", 0, 1),
            ("clear", "Limpar lista", 0, 2)
        ]
        
        for key, text, row, col in button_configs:
            btn = tk.Button(self, text=text, width=18)
            btn.grid(row=row, column=col, padx=6, pady=2)
            self.buttons[key] = btn
    
    def get_button(self, key: str) -> tk.Button:
        """Get button by key"""
        return self.buttons.get(key)


class StatusFrame(tk.Frame):
    """Frame for status information and progress"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, relief='groove', bd=1, padx=10, pady=8, 
                        bg=WINDOW_BG_COLOR, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create status widgets"""
        # Status label
        self.status_label = tk.Label(
            self, 
            text="Aguardando...", 
            font=('Arial', 10, 'bold'), 
            fg=TEXT_COLOR, 
            bg=WINDOW_BG_COLOR
        )
        self.status_label.grid(row=0, column=0, sticky='w')
        
        # Info label
        self.info_label = tk.Label(
            self, 
            text="Formato: - | Registros: -", 
            font=('Arial', 10), 
            fg=SECONDARY_TEXT_COLOR, 
            bg=WINDOW_BG_COLOR
        )
        self.info_label.grid(row=1, column=0, sticky='w', pady=(4, 0))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self, mode='determinate', length=520)
        self.progress_bar.grid(row=2, column=0, sticky='ew', pady=8)
        
        self.grid_columnconfigure(0, weight=1)
    
    def set_status(self, text: str):
        """Set status text"""
        self.status_label.config(text=text)
    
    def set_info(self, text: str):
        """Set info text"""
        self.info_label.config(text=text)
    
    def set_progress(self, value: int, maximum: int = None):
        """Set progress bar value"""
        if maximum is not None:
            self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = value
    
    def reset_progress(self):
        """Reset progress bar"""
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = 100
