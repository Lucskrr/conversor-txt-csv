"""
Main application entry point for Conversor TOTVS
Professional desktop application with licensing and updates
"""

import sys
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import application modules
from utils.config_service import get_config
from utils.logger import get_logger
from services.license_service import get_license_service, check_license
from services.update_service import get_update_service, check_updates
from ui.dialogs import UpdateDialog, LicenseDialog, ProgressDialog
from ui.ui_components_simple import (StyleManager, HeaderFrame, FooterFrame, FileSelectionFrame,
                                       FileListFrame, ButtonPanelFrame, StatusFrame)
from core.converter_engine import BatchConverter

# Drag-and-drop support
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class ConversorApp:
    """Main application class with licensing and updates"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger(__name__)
        self.license_service = get_license_service()
        self.update_service = get_update_service()
        
        # Check license first
        if not self._check_license():
            sys.exit(1)
        
        # Initialize UI
        self.root = self._create_root()
        self.batch_converter = BatchConverter()
        
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
    
    def _check_license(self) -> bool:
        """Check application license"""
        try:
            is_valid, message = check_license()
            self.logger.log_license_check(is_valid, message)
            
            if not is_valid:
                # Show license error dialog
                root = tk.Tk()
                root.withdraw()  # Hide main window
                
                license_dialog = LicenseDialog(root, None)
                license_dialog.show_error(message)
                
                root.destroy()
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"License check failed: {e}")
            messagebox.showerror("Erro de Licença", f"Falha na verificação da licença: {e}")
            return False
    
    def _create_root(self) -> tk.Tk:
        """Create main window"""
        if DND_AVAILABLE:
            root = TkinterDnD.Tk()
        else:
            root = tk.Tk()
        
        root.title(f"{self.config.get('APP_NAME')} - Conversor TXT → CSV")
        root.geometry(self.config.get('WINDOW_SIZE'))
        root.configure(bg=self.config.get('WINDOW_BG_COLOR'))
        
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
            bg=self.config.get('PRIMARY_COLOR'), 
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
    
    def _check_for_updates(self):
        """Check for updates in background"""
        if not self.config.get('AUTO_UPDATE_ENABLED', True):
            return
        
        def check_updates_bg():
            try:
                update_available, release_info = check_updates()
                if update_available and release_info:
                    # Show update dialog in main thread
                    self.root.after(0, lambda: self._show_update_dialog(release_info))
            except Exception as e:
                self.logger.error(f"Update check failed: {e}")
        
        # Run update check in background
        threading.Thread(target=check_updates_bg, daemon=True).start()
    
    def _show_update_dialog(self, release_info):
        """Show update dialog to user"""
        try:
            dialog = UpdateDialog(self.root, release_info)
            if dialog.show():
                # User wants to update
                self._install_update(release_info)
        except Exception as e:
            self.logger.error(f"Update dialog failed: {e}")
    
    def _install_update(self, release_info):
        """Install update"""
        try:
            # Show progress dialog
            progress = ProgressDialog(self.root, "Atualizando", "Baixando atualização...")
            progress.show()
            
            def update_progress():
                progress.update_progress(50, 100, "Instalando atualização...")
                self.root.after(1000, lambda: self._complete_update(release_info, progress))
            
            self.root.after(100, update_progress)
            
        except Exception as e:
            self.logger.error(f"Update installation failed: {e}")
            messagebox.showerror("Erro na Atualização", f"Falha na atualização: {e}")
    
    def _complete_update(self, release_info, progress):
        """Complete update process"""
        try:
            success, message = self.update_service.install_update(release_info)
            
            if success:
                progress.close()
                messagebox.showinfo("Atualização", message)
                self.root.quit()
            else:
                progress.close()
                messagebox.showerror("Erro na Atualização", message)
                
        except Exception as e:
            progress.close()
            self.logger.error(f"Update completion failed: {e}")
            messagebox.showerror("Erro na Atualização", f"Falha na atualização: {e}")
    
    def _select_single_file(self):
        """Handle single file selection"""
        files = filedialog.askopenfilenames(filetypes=self.config.get('FILE_FILTERS'))
        if files:
            # Set first file in selection field
            self.file_selection.set_file_path(files[0])
            # Add all files to list
            for file_path in files:
                self.file_list.add_file(file_path)
    
    def _add_files(self):
        """Add multiple files to the list"""
        files = filedialog.askopenfilenames(filetypes=self.config.get('FILE_FILTERS'))
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
        import re
        
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
            messagebox.showerror("Erro", self.config.get('ERROR_MESSAGES')['no_files'])
            return
        
        # Get output directory
        output_dir = filedialog.askdirectory(title="Selecione a pasta de saída")
        if not output_dir:
            messagebox.showwarning("Aviso", self.config.get('ERROR_MESSAGES')['no_output_dir'])
            return
        
        # Start conversion in background thread
        self._start_conversion(all_files, output_dir)
    
    def _start_conversion(self, files, output_dir):
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
    
    def _convert_background(self, files, output_dir):
        """Background conversion process"""
        
        def progress_callback(value, maximum):
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
    
    def _finalize_conversion(self, results, total_files):
        """Finalize conversion process"""
        success_count = sum(1 for success, _, _ in results if success)
        error_count = total_files - success_count
        
        # Show completion message
        if success_count > 0:
            message = self.config.get('SUCCESS_MESSAGES')['conversion_complete'].format(
                success=success_count, errors=error_count
            )
            messagebox.showinfo("Conclusão", message)
        else:
            message = self.config.get('SUCCESS_MESSAGES')['no_conversions'].format(errors=error_count)
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
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        finally:
            self._log_app_close()


def main():
    """Main entry point"""
    try:
        app = ConversorApp()
        app.run()
    except Exception as e:
        # Fallback error handling
        import traceback
        error_msg = f"Erro ao iniciar aplicação: {e}\n\n{traceback.format_exc()}"
        
        # Try to show error dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erro de Inicialização", error_msg)
            root.destroy()
        except:
            print(error_msg)
        
        sys.exit(1)


if __name__ == "__main__":
    main()
