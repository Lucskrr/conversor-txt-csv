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

# Import JSON-based parser
try:
    from core.json_parser import get_configurable_factory, ConfigurableFormatDetector
    JSON_PARSER_AVAILABLE = True
except ImportError:
    JSON_PARSER_AVAILABLE = False


class ConversionEngine:
    """Main conversion engine"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger(__name__)
        
        # Initialize JSON parser if available
        self.json_factory = get_configurable_factory() if JSON_PARSER_AVAILABLE else None
        self.json_detector = ConfigurableFormatDetector() if JSON_PARSER_AVAILABLE else None
    
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
        
        # Detect format (try JSON parser first, then fallback to original)
        format_type = self._detect_format(input_file)
        
        if not format_type:
            raise UnsupportedFormatError("unknown", self.config.get('SUPPORTED_FORMATS'))
        
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
        
        return output_path, format_type, len(records), ''
    
    def _try_parse_with_all_parsers(self, input_file: str, 
                                  progress_callback: Optional[Callable] = None) -> Tuple[Optional[str], List[Record]]:
        """Try all parsers on the file"""
        try:
            with open(input_file, 'r', encoding=self.config.get('INPUT_ENCODING')) as f:
                lines = f.readlines()
            
            return ParserFactory.try_parse_all(lines)
        except Exception as e:
            self.logger.error(f"Failed to try all parsers for {input_file}: {e}")
            return None, []
    
    def _parse_file(self, input_file: str, format_type: str, 
                   progress_callback: Optional[Callable] = None) -> List[Record]:
        """Parse file with specific format"""
        # Try JSON parser first
        if self.json_factory:
            try:
                parser = self.json_factory.create_parser(format_type)
                return parser.parse(self._read_lines(input_file), progress_callback)
            except Exception as e:
                self.logger.debug(f"JSON parser failed for {format_type}: {e}")
        
        # Fallback to original parser
        try:
            parser = ParserFactory.create_parser(format_type)
            return parser.parse(self._read_lines(input_file), progress_callback)
        except Exception as e:
            raise FileProcessingError(input_file, f"Parsing error: {e}")
    
    def _detect_format(self, input_file: str) -> Optional[str]:
        """Detect file format using available parsers"""
        # Try JSON parser first
        if self.json_detector:
            try:
                format_name = self.json_detector.detect_format(input_file)
                if format_name:
                    self.logger.debug(f"JSON parser detected format: {format_name}")
                    return format_name
            except Exception as e:
                self.logger.debug(f"JSON parser failed: {e}")
        
        # Fallback to original parser
        try:
            format_name = FormatDetector.detect_format(input_file)
            if format_name:
                self.logger.debug(f"Original parser detected format: {format_name}")
                return format_name
        except Exception as e:
            self.logger.debug(f"Original parser failed: {e}")
        
        return None
    
    def _read_lines(self, file_path: str) -> List[str]:
        """Read file lines with proper encoding"""
        try:
            with open(file_path, 'r', encoding=self.config.get('INPUT_ENCODING')) as f:
                return [line.rstrip('\n\r') for line in f if line.strip()]
        except UnicodeDecodeError:
            # Try alternative encodings
            for encoding in ['utf-8', 'cp1252', 'latin1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return [line.rstrip('\n\r') for line in f if line.strip()]
                except UnicodeDecodeError:
                    continue
            
            raise FileProcessingError(file_path, "Could not read file with any supported encoding")
    
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
        self.logger = get_logger(__name__)
    
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
