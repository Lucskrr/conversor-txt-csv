"""
Logging module for Conversor TOTVS
Centralized logging configuration and utilities
"""

import logging
import logging.handlers
from pathlib import Path
from config import (LOG_FILE, LOG_FORMAT, LOG_LEVEL, MAX_LOG_SIZE, BACKUP_COUNT, 
                   APP_NAME, VERSION)


class AppLogger:
    """Centralized logger for the application"""
    
    def __init__(self):
        self._logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Configure the application logger"""
        self._logger = logging.getLogger(APP_NAME)
        self._logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
        
        # Remove existing handlers to avoid duplicates
        if self._logger.handlers:
            self._logger.handlers.clear()
        
        # Create file handler with rotation
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                LOG_FILE, 
                maxBytes=MAX_LOG_SIZE, 
                backupCount=BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(LOG_FORMAT)
            file_handler.setFormatter(formatter)
            
            self._logger.addHandler(file_handler)
        except (PermissionError, OSError) as e:
            # Fallback to basic logging if file access fails
            logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
            self._logger = logging.getLogger(APP_NAME)
            self._logger.warning(f"Could not setup file logging: {e}")
    
    def info(self, message):
        """Log info message"""
        self._logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self._logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self._logger.error(message)
    
    def debug(self, message):
        """Log debug message"""
        self._logger.debug(message)
    
    def log_conversion_success(self, input_file, output_file, format_type, record_count):
        """Log successful conversion"""
        self.info(f"OK: {input_file} -> {output_file} | Formato: {format_type} | Registros: {record_count}")
    
    def log_conversion_error(self, input_file, error):
        """Log conversion error"""
        self.error(f"ERRO: {input_file} | {str(error)}")
    
    def log_app_start(self):
        """Log application start"""
        self.info(f"Application started - {APP_NAME} v{VERSION}")
    
    def log_app_close(self):
        """Log application close"""
        self.info("Application closed")


# Global logger instance
app_logger = AppLogger()
