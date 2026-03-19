"""
Core conversion engine for Conversor TOTVS
Handles the main conversion logic
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Callable

from .parsers import FormatDetector, ParserFactory, Record
from .exceptions import ConversionError, UnsupportedFormatError, FileProcessingError, OutputDirectoryError
from utils.config_service import get_config
from utils.logger import get_logger


class ConversionEngine:
    """Main conversion engine"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger(__name__)
    
    def convert_file(self, input_file: str, output_dir: str, 
                    progress_callback: Optional[Callable] = None) -> Tuple[str, str, int, str]:
        """
        Convert a single TXT file to CSV
        
        Args:
            input_file: Path to input TXT file
            output_dir: Directory to save output CSV
            progress_callback: Optional callback for progress updates
            
        Returns:
            Tuple of (output_path, format_type, record_count, fallback_message)
        """
        # Validate input file
        if not os.path.isfile(input_file):
            raise FileProcessingError(input_file, "File not found")
        
        # Detect format
        format_type = FormatDetector.detect_format(input_file)
        fallback_message = ''
        supported_formats = self.config.get('SUPPORTED_FORMATS')
        
        if format_type not in supported_formats:
            # Try parsing with all available parsers
            format_type, records = self._try_parse_with_all_parsers(input_file, progress_callback)
            if format_type:
                fallback_message = f"Formato detectado por parser: {format_type}."
            else:
                raise UnsupportedFormatError(format_type or "unknown", supported_formats)
        else:
            # Read file and parse with detected format
            records = self._parse_file(input_file, format_type, progress_callback)
        
        # Generate output path
        output_path = self._generate_output_path(input_file, output_dir)
        
        # Ensure output directory exists
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            raise OutputDirectoryError(f"Failed to create output directory: {e}")
        
        # Write CSV
        self._write_csv(output_path, records)
        
        # Log success
        self.logger.log_conversion_success(input_file, output_path, format_type, len(records))
        
        return output_path, format_type, len(records), fallback_message
    
    def _try_parse_with_all_parsers(self, input_file: str, 
                                  progress_callback: Optional[Callable] = None) -> Tuple[Optional[str], List[Record]]:
        """Try all parsers on the file"""
        try:
            with open(input_file, 'r', encoding=INPUT_ENCODING) as f:
                lines = f.readlines()
            
            return ParserFactory.try_parse_all(lines)
        except Exception as e:
            self.logger.error(f"Failed to try all parsers for {input_file}: {e}")
            return None, []
    
    def _parse_file(self, input_file: str, format_type: str, 
                   progress_callback: Optional[Callable] = None) -> List[Record]:
        """Parse file with specific format"""
        try:
            with open(input_file, 'r', encoding=self.config.get('INPUT_ENCODING')) as f:
                lines = f.readlines()
            
            parser = ParserFactory.create_parser(format_type)
            return parser.parse(lines, progress_callback)
            
        except UnicodeDecodeError as e:
            raise FileProcessingError(input_file, f"Encoding error: {e}")
        except Exception as e:
            raise FileProcessingError(input_file, f"Parsing error: {e}")
    
    def _generate_output_path(self, input_file: str, output_dir: str) -> str:
        """Generate output CSV file path"""
        base_name = Path(input_file).stem
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{base_name}_{timestamp}.csv"
        return os.path.join(output_dir, filename)
    
    def _write_csv(self, output_path: str, records: List[Record]) -> None:
        """Write records to CSV file"""
        try:
            with open(output_path, 'w', newline='', encoding=self.config.get('CSV_ENCODING')) as f:
                writer = csv.writer(f, delimiter=self.config.get('CSV_DELIMITER'))
                
                # Write header
                writer.writerow([
                    'seq',
                    'codigo_produto',
                    'descricao',
                    'codigo_barras',
                    'quantidade',
                    'valor_unitario',
                    'valor_total'
                ])
                
                # Write records
                for record in records:
                    writer.writerow([
                        record.seq,
                        record.codigo_produto,
                        record.descricao,
                        record.codigo_barras,
                        record.quantidade,
                        record.valor_unitario,
                        record.valor_total
                    ])
                    
        except Exception as e:
            raise ConversionError(f"Failed to write CSV file: {e}")


class BatchConverter:
    """Handles batch conversion of multiple files"""
    
    def __init__(self):
        self.engine = ConversionEngine()
        self.logger = app_logger
    
    def convert_batch(self, files: List[str], output_dir: str, 
                     progress_callback: Optional[Callable] = None) -> List[Tuple[bool, str, str]]:
        """
        Convert multiple files
        
        Args:
            files: List of input file paths
            output_dir: Directory to save output files
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of tuples (success, file_path, result_or_error)
        """
        results = []
        
        for idx, file_path in enumerate(files, start=1):
            if not file_path:
                continue
            
            try:
                output_path, format_type, record_count, fallback = self.engine.convert_file(
                    file_path, output_dir, progress_callback
                )
                results.append((True, file_path, output_path))
                
            except Exception as e:
                self.logger.log_conversion_error(file_path, e)
                results.append((False, file_path, str(e)))
        
        return results
