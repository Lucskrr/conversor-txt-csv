"""
Dialog components for Conversor TOTVS
Update and license validation dialogs
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from datetime import datetime

from utils.config_service import get_config
from utils.logger import get_logger


class UpdateDialog:
    """Dialog for update notifications and installation"""
    
    def __init__(self, parent, release_info: dict):
        self.parent = parent
        self.release_info = release_info
        self.config = get_config()
        self.logger = get_logger(__name__)
        
        self.dialog = None
        self.result = None
    
    def show(self) -> bool:
        """Show update dialog and return user choice"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Atualização Disponível")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self._create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        return self.result
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Header
        header_frame = tk.Frame(self.dialog, bg=self.config.get('ACCENT_COLOR'), pady=20)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text="🔄 Nova Versão Disponível",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.config.get('ACCENT_COLOR')
        ).pack()
        
        # Content
        content_frame = tk.Frame(self.dialog, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Version info
        current_version = self.config.get('VERSION')
        latest_version = self.release_info.get('tag_name', '').lstrip('v')
        
        tk.Label(
            content_frame,
            text=f"Versão Atual: {current_version}",
            font=('Arial', 12),
            fg=self.config.get('TEXT_COLOR')
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            content_frame,
            text=f"Nova Versão: {latest_version}",
            font=('Arial', 12, 'bold'),
            fg=self.config.get('PRIMARY_COLOR')
        ).pack(anchor='w', pady=(0, 15))
        
        # Release name
        release_name = self.release_info.get('name', '')
        if release_name:
            tk.Label(
                content_frame,
                text=release_name,
                font=('Arial', 11, 'bold'),
                fg=self.config.get('TEXT_COLOR')
            ).pack(anchor='w', pady=(0, 10))
        
        # Release notes
        tk.Label(
            content_frame,
            text="Novidades:",
            font=('Arial', 11, 'bold'),
            fg=self.config.get('TEXT_COLOR')
        ).pack(anchor='w', pady=(15, 5))
        
        # Scrollable text for release notes
        text_frame = tk.Frame(content_frame, relief='sunken', bd=1)
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        text_widget = tk.Text(text_frame, height=8, wrap='word', font=('Arial', 10))
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        release_notes = self.release_info.get('body', 'Sem informações disponíveis.')
        text_widget.insert('1.0', release_notes)
        text_widget.config(state='disabled')
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Update button
        update_btn = tk.Button(
            button_frame,
            text="Atualizar Agora",
            bg=self.config.get('PRIMARY_COLOR'),
            fg='white',
            font=('Arial', 11, 'bold'),
            command=self._on_update
        )
        update_btn.pack(side='right', padx=(10, 0))
        
        # Later button
        later_btn = tk.Button(
            button_frame,
            text="Depois",
            font=('Arial', 10),
            command=self._on_later
        )
        later_btn.pack(side='right')
    
    def _on_update(self):
        """Handle update button click"""
        self.result = True
        self.dialog.destroy()
    
    def _on_later(self):
        """Handle later button click"""
        self.result = False
        self.dialog.destroy()


class LicenseDialog:
    """Dialog for license validation and information"""
    
    def __init__(self, parent, license_info: dict):
        self.parent = parent
        self.license_info = license_info
        self.config = get_config()
        self.logger = get_logger(__name__)
        
        self.dialog = None
    
    def show_error(self, message: str):
        """Show license error dialog"""
        self._show_dialog("Licença Inválida", message, "error")
    
    def show_info(self):
        """Show license information dialog"""
        if not self.license_info:
            self.show_error("Informações de licença não disponíveis.")
            return
        
        title = "Informações da Licença"
        content = self._format_license_info()
        self._show_dialog(title, content, "info")
    
    def _format_license_info(self) -> str:
        """Format license information for display"""
        info = []
        
        info.append(f"Machine ID: {self.license_info.get('machine_id', 'N/A')}")
        
        issued_date = self.license_info.get('issued_date')
        if issued_date:
            try:
                issued = datetime.fromisoformat(issued_date.replace('Z', '+00:00'))
                info.append(f"Emitida em: {issued.strftime('%d/%m/%Y %H:%M')}")
            except:
                info.append(f"Emitida em: {issued_date}")
        
        expiry_date = self.license_info.get('expiry_date')
        if expiry_date:
            try:
                expiry = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
                info.append(f"Expira em: {expiry.strftime('%d/%m/%Y %H:%M')}")
            except:
                info.append(f"Expira em: {expiry_date}")
        
        license_key = self.license_info.get('license_key')
        if license_key:
            info.append(f"Chave: {license_key}")
        
        status = "VÁLIDA" if self.license_info.get('is_valid') else "INVÁLIDA"
        info.append(f"Status: {status}")
        
        return "\n\n".join(info)
    
    def _show_dialog(self, title: str, content: str, dialog_type: str):
        """Show generic information dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        # Icon based on type
        icon = "❌" if dialog_type == "error" else "ℹ️"
        color = "#d32f2f" if dialog_type == "error" else self.config.get('ACCENT_COLOR')
        
        # Header
        header_frame = tk.Frame(self.dialog, bg=color, pady=15)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text=f"{icon} {title}",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg=color
        ).pack()
        
        # Content
        content_frame = tk.Frame(self.dialog, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(content_frame, relief='sunken', bd=1)
        text_frame.pack(fill='both', expand=True)
        
        text_widget = tk.Text(text_frame, wrap='word', font=('Arial', 10))
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.insert('1.0', content)
        text_widget.config(state='disabled')
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Close button
        close_btn = tk.Button(
            self.dialog,
            text="Fechar",
            command=self.dialog.destroy,
            width=15
        )
        close_btn.pack(pady=(0, 20))
        
        # Wait for dialog to close
        self.dialog.wait_window()


class ProgressDialog:
    """Progress dialog for long operations"""
    
    def __init__(self, parent, title: str, message: str):
        self.parent = parent
        self.title = title
        self.message = message
        self.config = get_config()
        
        self.dialog = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
    
    def show(self):
        """Show progress dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (150 // 2)
        self.dialog.geometry(f"400x150+{x}+{y}")
        
        self._create_widgets()
        
        return self
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Content frame
        content_frame = tk.Frame(self.dialog, padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Status label
        self.status_label = tk.Label(
            content_frame,
            text=self.message,
            font=('Arial', 10),
            fg=self.config.get('TEXT_COLOR')
        )
        self.status_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            content_frame,
            mode='determinate',
            variable=self.progress_var,
            length=350
        )
        self.progress_bar.pack()
        
        # Prevent window closing
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def update_progress(self, value: int, maximum: int = 100, message: str = None):
        """Update progress"""
        if maximum:
            self.progress_bar['maximum'] = maximum
        self.progress_var.set(value)
        
        if message:
            self.status_label.config(text=message)
        
        self.dialog.update_idletasks()
    
    def close(self):
        """Close dialog"""
        if self.dialog:
            self.dialog.destroy()
