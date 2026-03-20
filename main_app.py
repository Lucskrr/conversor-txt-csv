"""
Main application module for Conversor TOTVS
Refactored main application with proper separation of concerns
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import re
from typing import List, Tuple

# Import application modules
from config import (WINDOW_SIZE, WINDOW_BG_COLOR, FILE_FILTERS, ERROR_MESSAGES, 
                   SUCCESS_MESSAGES, APP_NAME)
from logger import app_logger
from exceptions import ConversionError
from converter_engine import BatchConverter
from ui_components import (StyleManager, HeaderFrame, FooterFrame, FileSelectionFrame,
                          FileListFrame, ButtonPanelFrame, StatusFrame)
from update_checker import check_for_updates, install_update

# Drag-and-drop support
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class ConversorApp:
    """Main application class"""
    
    def __init__(self):
        self.root = self._create_root()
        self.batch_converter = BatchConverter()
        self.logger = app_logger
        
        # UI components
        self.file_selection = None
        self.file_list = None
        self.button_panel = None
        self.status_frame = None
        self.convert_button = None
        self.drag_label = None
        
        self._setup_ui()
        self._setup_drag_drop()
        self._check_for_updates()
        self._log_app_start()
    
    def _create_root(self) -> tk.Tk:
        """Create main window"""
        if DND_AVAILABLE:
            root = TkinterDnD.Tk()
        else:
            root = tk.Tk()
        
        root.title(f"{APP_NAME} - Conversor TXT → CSV")
        root.geometry(WINDOW_SIZE)
        root.configure(bg=WINDOW_BG_COLOR)
        
        return root
    
    def _setup_ui(self):
        """Setup user interface"""
        # Configure styles
        StyleManager.configure_styles()
        
        # Header
        header = HeaderFrame(self.root)
        header.pack(fill='x', padx=10, pady=8)
        
        # File selection frame
        self.file_selection = FileSelectionFrame(self.root)
        self.file_selection.pack(pady=5, padx=10, fill='x')
        
        # File list frame
        self.file_list = FileListFrame(self.root)
        self.file_list.pack(pady=5, padx=10, fill='both', expand=True)
        
        # Drag and drop label
        self.drag_label = tk.Label(
            self.root, 
            text='Solte os arquivos aqui', 
            fg='blue'
        )
        self.drag_label.pack(pady=2)
        
        # Button panel
        self.button_panel = ButtonPanelFrame(self.root)
        self.button_panel.pack(pady=10)
        
        # Setup button commands
        self._setup_button_commands()
        
        # Convert button
        self.convert_button = tk.Button(
            self.root, 
            text="Converter", 
            command=self._convert_files, 
            width=24, 
            bg='#4CAF50', 
            fg='white', 
            font=('Arial', 11, 'bold')
        )
        self.convert_button.pack(pady=12)
        
        # Status frame
        self.status_frame = StatusFrame(self.root)
        self.status_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Footer
        footer = FooterFrame(self.root)
        footer.pack(fill='x', side='bottom')
    
    def _setup_button_commands(self):
        """Setup button panel commands"""
        # Browse button
        self.file_selection.browse_button.config(command=self._select_single_file)
        
        # Button panel buttons
        self.button_panel.get_button("add").config(command=self._add_files)
        self.button_panel.get_button("remove").config(command=self._remove_selected_files)
        self.button_panel.get_button("clear").config(command=self._clear_file_list)
    
    def _setup_drag_drop(self):
        """Setup drag and drop functionality"""
        dnd_enabled = False
        
        if DND_AVAILABLE:
            try:
                self.file_list.listbox.drop_target_register(DND_FILES)
                self.file_list.listbox.dnd_bind('<<Drop>>', self._on_drop_files)
                dnd_enabled = True
            except Exception as e:
                self.logger.warning(f"DND failed on listbox: {e}")
        
        if not dnd_enabled:
            # Try native TkDND
            try:
                self.file_list.listbox.drop_target_register(tk.DND_FILES)
                self.file_list.listbox.dnd_bind('<<Drop>>', self._on_drop_files)
                dnd_enabled = True
            except Exception as e:
                self.logger.warning(f"Native DND not available: {e}")
        
        # Update drag label based on availability
        if dnd_enabled:
            self.drag_label.config(text='Solte os arquivos aqui', fg='darkgreen')
        else:
            self.drag_label.config(
                text='Solte os arquivos aqui (arraste e solte não suportado no ambiente)', 
                fg='red'
            )
    
    def _select_single_file(self):
        """Handle single file selection"""
        files = filedialog.askopenfilenames(filetypes=FILE_FILTERS)
        if files:
            # Set first file in selection field
            self.file_selection.set_file_path(files[0])
            # Add all files to list
            for file_path in files:
                self.file_list.add_file(file_path)
    
    def _add_files(self):
        """Add multiple files to the list"""
        files = filedialog.askopenfilenames(filetypes=FILE_FILTERS)
        for file_path in files:
            self.file_list.add_file(file_path)
    
    def _remove_selected_files(self):
        """Remove selected files from the list"""
        self.file_list.remove_selected()
    
    def _clear_file_list(self):
        """Clear all files from the list"""
        self.file_list.clear_all()
    
    def _on_drop_files(self, event):
        """Handle drag and drop file drop"""
        data = event.data
        if not data:
            return
        
        files = []
        # Parse dropped file paths (supports spaces and braces)
        tokens = re.findall(r"\{([^}]*)\}|([^\s]+)", data)
        for brace_path, simple_path in tokens:
            path = brace_path or simple_path
            if path:
                path = path.strip()
                if os.path.isfile(path) and path.lower().endswith('.txt'):
                    files.append(path)
        
        for file_path in files:
            self.file_list.add_file(file_path)
    
    def _convert_files(self):
        """Handle file conversion"""
        # Get files to convert
        manual_file = self.file_selection.get_file_path()
        list_files = self.file_list.get_files()
        
        all_files = list_files.copy()
        if manual_file and manual_file not in all_files:
            all_files.append(manual_file)
        
        if not all_files:
            messagebox.showerror("Erro", ERROR_MESSAGES['no_files'])
            return
        
        # Get output directory
        output_dir = filedialog.askdirectory(title="Selecione a pasta de saída")
        if not output_dir:
            messagebox.showwarning("Aviso", ERROR_MESSAGES['no_output_dir'])
            return
        
        # Start conversion in background thread
        self._start_conversion(all_files, output_dir)
    
    def _start_conversion(self, files: List[str], output_dir: str):
        """Start conversion in background thread"""
        # Update UI state
        self.root.config(cursor='watch')
        self.convert_button.config(state='disabled')
        self.status_frame.set_status('Iniciando conversão...')
        self.status_frame.reset_progress()
        
        # Start background thread
        thread = threading.Thread(
            target=self._convert_background,
            args=(files, output_dir),
            daemon=True
        )
        thread.start()
    
    def _convert_background(self, files: List[str], output_dir: str):
        """Background conversion process"""
        
        def progress_callback(value: int, maximum: int):
            """Update progress in main thread"""
            def update_ui():
                self.status_frame.set_progress(value, maximum)
                if maximum:
                    percentage = int(value / maximum * 100)
                    self.status_frame.set_status(f'Convertendo... {percentage}%')
                else:
                    self.status_frame.set_status('Convertendo...')
            
            self.root.after(0, update_ui)
        
        # Convert files
        results = []
        for idx, file_path in enumerate(files, start=1):
            if not file_path:
                continue
            
            # Update status for current file
            def set_file_status():
                filename = os.path.basename(file_path)
                self.status_frame.set_status(f'Processando ({idx}/{len(files)}): {filename}')
            
            self.root.after(0, set_file_status)
        
        # Perform batch conversion
        results = self.batch_converter.convert_batch(files, output_dir, progress_callback)
        
        # Finalize in main thread
        self.root.after(0, lambda: self._finalize_conversion(results, len(files)))
    
    def _finalize_conversion(self, results: List[Tuple[bool, str, str]], total_files: int):
        """Finalize conversion process"""
        success_count = sum(1 for success, _, _ in results if success)
        error_count = total_files - success_count
        
        # Show completion message
        if success_count > 0:
            message = SUCCESS_MESSAGES['conversion_complete'].format(
                success=success_count, errors=error_count
            )
            messagebox.showinfo("Conclusão", message)
        else:
            message = SUCCESS_MESSAGES['no_conversions'].format(errors=error_count)
            messagebox.showerror("Conclusão", message)
        
        # Reset UI
        self._reset_ui()
        self.status_frame.set_info(f"Processados: {success_count}/{total_files}")
    
    def _reset_ui(self):
        """Reset UI to initial state"""
        self.file_list.clear_all()
        self.file_selection.clear()
        self.status_frame.set_status('Concluído')
        self.status_frame.reset_progress()
        self.convert_button.config(state='normal')
        self.root.config(cursor='')
    
    def _log_app_start(self):
        """Log application start"""
        self.logger.log_app_start()
    
    def _log_app_close(self):
        """Log application close"""
        self.logger.log_app_close()
    
    def _check_for_updates(self):
        """Check for updates in background"""
        def check_updates_bg():
            try:
                update_available, release_info = check_for_updates()
                if update_available and release_info:
                    latest_version = release_info.get('tag_name', '').lstrip('v')
                    self.root.after(0, lambda: self._show_update_dialog(release_info))
            except Exception as e:
                print(f"Update check failed: {e}")
        
        # Run update check in background
        threading.Thread(target=check_updates_bg, daemon=True).start()
    
    def _show_update_dialog(self, release_info):
        """Show update dialog to user"""
        try:
            latest_version = release_info.get('tag_name', '').lstrip('v')
            release_notes = release_info.get('body', 'Nova versão disponível com melhorias e correções.')
            
            result = messagebox.askyesno(
                "Atualização Disponível",
                f"Nova versão {latest_version} disponível!\n\n"
                f"Novidades:\n{release_notes}\n\n"
                "Deseja atualizar agora?"
            )
            
            if result:
                self._install_update(release_info)
                
        except Exception as e:
            print(f"Update dialog failed: {e}")
    
    def _install_update(self, release_info):
        """Install update"""
        try:
            success, message = install_update(release_info)
            
            if success:
                messagebox.showinfo("Atualização", message)
                self.root.quit()
            else:
                messagebox.showerror("Erro na Atualização", message)
                
        except Exception as e:
            messagebox.showerror("Erro na Atualização", f"Falha na atualização: {e}")
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        finally:
            self._log_app_close()


def main():
    """Main entry point"""
    app = ConversorApp()
    app.run()


if __name__ == "__main__":
    main()
