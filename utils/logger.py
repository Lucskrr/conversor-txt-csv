"""
Logging utility for Conversor TOTVS
Centralized logging configuration and utilities
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from .config_service import get_config


class AppLogger:
    """Centralized logger for the application"""
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or __name__
        self.config = get_config()
        self._logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Configure the application logger"""
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(getattr(logging, self.config.get('LOG_LEVEL', 'INFO')))
        
        # Remove existing handlers to avoid duplicates
        if self._logger.handlers:
            self._logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(self.config.get('LOG_FORMAT'))
        
        # Console handler for development
        if not self.config.is_frozen():
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
        
        # File handler with rotation
        try:
            log_file = self.config.get('LOG_FILE')
            if log_file:
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=self.config.get('MAX_LOG_SIZE', 10*1024*1024),
                    backupCount=self.config.get('BACKUP_COUNT', 5),
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.INFO)
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
        except (PermissionError, OSError) as e:
            # Fallback to basic logging if file access fails
            if not self._logger.handlers:
                logging.basicConfig(format=self.config.get('LOG_FORMAT'), level=logging.INFO)
                self._logger = logging.getLogger(self.name)
                self._logger.warning(f"Could not setup file logging: {e}")
    
    def info(self, message: str):
        """Log info message"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self._logger.error(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)
    
    def log_conversion_success(self, input_file: str, output_file: str, format_type: str, record_count: int):
        """Log successful conversion"""
        self.info(f"OK: {input_file} -> {output_file} | Formato: {format_type} | Registros: {record_count}")
    
    def log_conversion_error(self, input_file: str, error: Exception):
        """Log conversion error"""
        self.error(f"ERRO: {input_file} | {str(error)}")
    
    def log_app_start(self):
        """Log application start"""
        config = get_config()
        self.info(f"Application started - {config.get('APP_NAME')} v{config.get('VERSION')}")
    
    def log_app_close(self):
        """Log application close"""
        self.info("Application closed")
    
    def log_license_check(self, is_valid: bool, message: str):
        """Log license validation"""
        status = "VALID" if is_valid else "INVALID"
        self.info(f"License check: {status} - {message}")
    
    def log_update_check(self, update_available: bool, latest_version: str = None):
        """Log update check"""
        if update_available:
            self.info(f"Update available: {latest_version}")
        else:
            self.info("No updates available")


# Global logger instances
_loggers = {}


def get_logger(name: Optional[str] = None) -> AppLogger:
    """Get logger instance"""
    global _loggers
    if name not in _loggers:
        _loggers[name] = AppLogger(name)
    return _loggers[name]


def log_info(message: str):
    """Convenience function for info logging"""
    get_logger().info(message)


def log_error(message: str):
    """Convenience function for error logging"""
    get_logger().error(message)


def log_warning(message: str):
    """Convenience function for warning logging"""
    get_logger().warning(message)
