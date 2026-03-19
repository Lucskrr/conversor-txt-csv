"""
Custom exceptions for Conversor TOTVS
Application-specific exception classes
"""


class ConversionError(Exception):
    """Base exception for conversion-related errors"""
    pass


class UnsupportedFormatError(ConversionError):
    """Raised when file format is not supported"""
    
    def __init__(self, format_name, supported_formats):
        self.format_name = format_name
        self.supported_formats = supported_formats
        super().__init__(f"Unsupported format: {format_name}")


class FileProcessingError(ConversionError):
    """Raised when file processing fails"""
    
    def __init__(self, file_path, original_error):
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(f"Failed to process file: {file_path}")


class ParsingError(ConversionError):
    """Raised when parsing fails"""
    pass


class OutputDirectoryError(ConversionError):
    """Raised when output directory operations fail"""
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass


class LicenseError(Exception):
    """Raised when license validation fails"""
    pass


class UpdateError(Exception):
    """Raised when update process fails"""
    pass
