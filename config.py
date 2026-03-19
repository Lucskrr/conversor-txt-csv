"""
Configuration module for Conversor TOTVS
Centralized application settings and constants
"""

import os
from pathlib import Path

# Application metadata
VERSION = '1.1.0'
APP_NAME = 'Conversor TOTVS'
APP_AUTHOR = 'Fa Maringa'
COMPANY_NAME = 'FA MARINGA LTDA'

# Supported formats
SUPPORTED_FORMATS = ['gerr004', 'cdfr054']

# File paths
APP_DIR = Path(__file__).parent.absolute()
LOG_FILE = APP_DIR / 'converter.log'
LOGO_CANDIDATES = ['logo.png', 'logo.gif']

# UI Configuration
WINDOW_SIZE = "760x620"
WINDOW_BG_COLOR = '#ECE9D8'
HEADER_BG_COLOR = '#ECE9D8'
FOOTER_BG_COLOR = '#E0E3E8'
PRIMARY_COLOR = '#4CAF50'
ACCENT_COLOR = '#1F4E79'
TEXT_COLOR = '#333333'
SECONDARY_TEXT_COLOR = '#555555'
DISABLED_TEXT_COLOR = '#444444'

# CSV Export configuration
CSV_DELIMITER = ','
CSV_ENCODING = 'utf-8'
INPUT_ENCODING = 'latin1'

# Progress tracking
PROGRESS_UPDATE_INTERVAL = 100  # milliseconds

# File filters
FILE_FILTERS = [("TXT files", "*.txt")]
ALL_FILES_FILTER = [("All files", "*.*")]

# Error messages
ERROR_MESSAGES = {
    'no_files': "Selecione pelo menos um arquivo TXT para converter.",
    'no_output_dir': "Seleção de pasta cancelada. Conversão abortada.",
    'incompatible_format': "Formato não compatível: '{format}'. Compatíveis: {supported}",
    'file_not_found': "Arquivo não encontrado: {file}",
    'permission_denied': "Sem permissão para acessar: {file}",
    'encoding_error': "Erro de codificação no arquivo: {file}",
    'unknown_error': "Erro desconhecido: {error}"
}

# Success messages
SUCCESS_MESSAGES = {
    'conversion_complete': "Conversão finalizada. Sucesso: {success}. Erros: {errors}.",
    'no_conversions': "Nenhum arquivo convertido. Erros: {errors}."
}

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5
