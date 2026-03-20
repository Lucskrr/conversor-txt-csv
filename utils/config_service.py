"""
Configuration service for Conversor TOTVS
Centralized configuration management
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigService:
    """Configuration management service"""
    
    def __init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from various sources"""
        
        # Application metadata
        config = {
            'VERSION': '1.0.0',
            'APP_NAME': 'Conversor TOTVS',
            'APP_AUTHOR': 'Fa Maringa',
            'COMPANY_NAME': 'FA MARINGA LTDA',
            
            # Supported formats
            'SUPPORTED_FORMATS': ['gerr004', 'cdfr054'],
            
            # File paths
            'APP_DIR': Path(__file__).parent.parent.absolute(),
            'LOG_FILE': None,  # Will be set after APP_DIR is known
            'LOGO_CANDIDATES': ['logo.png', 'logo.gif'],
            
            # UI Configuration
            'WINDOW_SIZE': "760x620",
            'WINDOW_BG_COLOR': '#ECE9D8',
            'HEADER_BG_COLOR': '#ECE9D8',
            'FOOTER_BG_COLOR': '#E0E3E8',
            'PRIMARY_COLOR': '#4CAF50',
            'ACCENT_COLOR': '#1F4E79',
            'TEXT_COLOR': '#333333',
            'SECONDARY_TEXT_COLOR': '#555555',
            'DISABLED_TEXT_COLOR': '#444444',
            
            # CSV Export configuration
            'CSV_DELIMITER': ',',
            'CSV_ENCODING': 'utf-8',
            'INPUT_ENCODING': 'latin1',
            
            # Progress tracking
            'PROGRESS_UPDATE_INTERVAL': 100,  # milliseconds
            
            # File filters
            'FILE_FILTERS': [("TXT files", "*.txt")],
            'ALL_FILES_FILTER': [("All files", "*.*")],
            
            # Error messages
            'ERROR_MESSAGES': {
                'no_files': "Selecione pelo menos um arquivo TXT para converter.",
                'no_output_dir': "Seleção de pasta cancelada. Conversão abortada.",
                'incompatible_format': "Formato não compatível: '{format}'. Compatíveis: {supported}",
                'file_not_found': "Arquivo não encontrado: {file}",
                'permission_denied': "Sem permissão para acessar: {file}",
                'encoding_error': "Erro de codificação no arquivo: {file}",
                'unknown_error': "Erro desconhecido: {error}",
                'license_invalid': "Licença inválida. A aplicação será encerrada.",
                'license_expired': "Licença expirada. Contate o suporte para renovar.",
                'license_missing': "Nenhuma licença encontrada. Contate o suporte."
            },
            
            # Success messages
            'SUCCESS_MESSAGES': {
                'conversion_complete': "Conversão finalizada. Sucesso: {success}. Erros: {errors}.",
                'no_conversions': "Nenhum arquivo convertido. Erros: {errors}.",
                'update_available': "Nova versão disponível: {version}",
                'update_downloaded': "Atualização baixada com sucesso",
                'license_valid': "Licença válida. Aplicação autorizada."
            },
            
            # Logging configuration
            'LOG_FORMAT': '%(asctime)s - %(levelname)s - %(message)s',
            'LOG_LEVEL': 'INFO',
            'MAX_LOG_SIZE': 10 * 1024 * 1024,  # 10MB
            'BACKUP_COUNT': 5,
            
            # Update configuration
            'UPDATE_CHECK_INTERVAL': 86400,  # 24 hours in seconds
            'AUTO_UPDATE_ENABLED': True,
            
            # License configuration
            'LICENSE_CHECK_INTERVAL': 3600,  # 1 hour in seconds
            'TRIAL_PERIOD_DAYS': 30
        }
        
        # Set dynamic paths
        config['LOG_FILE'] = config['APP_DIR'] / 'converter.log'
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self._config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
    
    def is_frozen(self) -> bool:
        """Check if running as frozen executable"""
        return getattr(sys, 'frozen', False)
    
    def get_executable_path(self) -> Path:
        """Get path to current executable"""
        if self.is_frozen():
            return Path(sys.executable)
        else:
            return Path(__file__).parent.parent / 'main_app.py'
    
    # Convenience properties for backward compatibility
    @property
    def VERSION(self):
        return self._config.get('VERSION', '1.1.0')
    
    @property
    def APP_NAME(self):
        return self._config.get('APP_NAME', 'Conversor TOTVS')
    
    @property
    def APP_AUTHOR(self):
        return self._config.get('APP_AUTHOR', 'Fa Maringa')
    
    @property
    def COMPANY_NAME(self):
        return self._config.get('COMPANY_NAME', 'FA MARINGA LTDA')


# Global config service instance
_config_service = None


def get_config() -> ConfigService:
    """Get global config service instance"""
    global _config_service
    if _config_service is None:
        _config_service = ConfigService()
    return _config_service


def get_setting(key: str, default: Any = None) -> Any:
    """Convenience function to get a setting"""
    config = get_config()
    return config.get(key, default)
