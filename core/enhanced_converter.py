"""
Enhanced conversion engine with JSON parser integration
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Optional, Callable, Tuple

from parsers import Record, ParsingError, UnsupportedFormatError
from exceptions import ConversionError
from utils.logger import get_logger
from utils.config_service import get_config

# Import JSON-based parser
try:
    from core.json_parser import get_configurable_factory, ConfigurableFormatDetector
    JSON_PARSER_AVAILABLE = True
except ImportError:
    JSON_PARSER_AVAILABLE = False


class EnhancedBatchConverter:
    """Enhanced batch converter with JSON parser support"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = get_config()
        
        # Initialize JSON parser if available
        self.json_factory = get_configurable_factory() if JSON_PARSER_AVAILABLE else None
        self.json_detector = ConfigurableFormatDetector() if JSON_PARSER_AVAILABLE else None
        
        self.logger.info(f"JSON Parser available: {JSON_PARSER_AVAILABLE}")
    
    def convert_file(self, file_path: str, output_dir: str, 
                    progress_callback: Optional[Callable] = None) -> Tuple[bool, str, str]:
        """
        Convert a single file to CSV
        
        Returns:
            Tuple of (success, message, output_file_path)
        """
        try:
            # Detect format (try JSON parser first, then fallback to original)
            format_name = self._detect_format(file_path)
            
            if not format_name:
                error_msg = f"Formato não reconhecido: {os.path.basename(file_path)}"
                self.logger.error(error_msg)
                return False, error_msg, ""
            
            # Parse file
            records = self._parse_file(file_path, format_name, progress_callback)
            
            if not records:
                error_msg = f"Nenhum registro encontrado em: {os.path.basename(file_path)}"
                self.logger.warning(error_msg)
                return False, error_msg, ""
            
            # Generate output path
            output_path = self._generate_output_path(file_path, output_dir, format_name)
            
            # Write CSV
            self._write_csv(records, output_path, format_name)
            
            success_msg = f"Convertido com sucesso: {os.path.basename(file_path)} → {os.path.basename(output_path)} ({len(records)} registros)"
            self.logger.info(success_msg)
            
            return True, success_msg, str(output_path)
            
        except Exception as e:
            error_msg = f"Erro ao converter {os.path.basename(file_path)}: {e}"
            self.logger.error(error_msg)
            return False, error_msg, ""
    
    def convert_batch(self, file_paths: List[str], output_dir: str,
                     progress_callback: Optional[Callable] = None) -> List[Tuple[bool, str, str]]:
        """
        Convert multiple files to CSV
        
        Returns:
            List of tuples (success, message, output_file_path)
        """
        results = []
        total_files = len(file_paths)
        
        for i, file_path in enumerate(file_paths, start=1):
            if progress_callback:
                progress_callback(i, total_files)
            
            result = self.convert_file(file_path, output_dir, 
                                     lambda current, total: progress_callback(i, total_files))
            results.append(result)
        
        return results
    
    def _detect_format(self, file_path: str) -> Optional[str]:
        """Detect file format using available parsers"""
        # Try JSON parser first
        if self.json_detector:
            try:
                format_name = self.json_detector.detect_format(file_path)
                if format_name:
                    self.logger.debug(f"JSON parser detected format: {format_name}")
                    return format_name
            except Exception as e:
                self.logger.debug(f"JSON parser failed: {e}")
        
        # Fallback to original parser
        try:
            from parsers import FormatDetector
            format_name = FormatDetector.detect_format(file_path)
            if format_name:
                self.logger.debug(f"Original parser detected format: {format_name}")
                return format_name
        except Exception as e:
            self.logger.debug(f"Original parser failed: {e}")
        
        return None
    
    def _parse_file(self, file_path: str, format_name: str,
                   progress_callback: Optional[Callable] = None) -> List[Record]:
        """Parse file using appropriate parser"""
        # Try JSON parser first
        if self.json_factory:
            try:
                parser = self.json_factory.create_parser(format_name)
                return parser.parse(self._read_lines(file_path), progress_callback)
            except Exception as e:
                self.logger.debug(f"JSON parser failed for {format_name}: {e}")
        
        # Fallback to original parser
        try:
            from parsers import ParserFactory
            parser = ParserFactory.create_parser(format_name)
            return parser.parse(self._read_lines(file_path), progress_callback)
        except Exception as e:
            raise ParsingError(f"Failed to parse file with {format_name}: {e}")
    
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
            
            raise ParsingError(f"Could not read file {file_path} with any supported encoding")
    
    def _generate_output_path(self, file_path: str, output_dir: str, format_name: str) -> Path:
        """Generate output CSV file path"""
        input_path = Path(file_path)
        output_dir_path = Path(output_dir)
        
        # Ensure output directory exists
        output_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        base_name = input_path.stem
        output_filename = f"{base_name}_{format_name}.csv"
        output_path = output_dir_path / output_filename
        
        # Handle name conflicts
        counter = 1
        while output_path.exists():
            output_filename = f"{base_name}_{format_name}_{counter}.csv"
            output_path = output_dir_path / output_filename
            counter += 1
        
        return output_path
    
    def _write_csv(self, records: List[Record], output_path: Path, format_name: str):
        """Write records to CSV file"""
        try:
            # Get CSV headers (try JSON parser first)
            headers = None
            if self.json_detector:
                try:
                    headers = self.json_detector.get_csv_headers(format_name)
                    if headers:
                        # Filter headers to only include fields that exist in records
                        filtered_headers = []
                        sample_record = records[0].to_dict() if records else {}
                        for header in headers:
                            if header in sample_record:
                                filtered_headers.append(header)
                        headers = filtered_headers
                except:
                    headers = None
            
            # Fallback to default headers
            if not headers:
                headers = ['seq', 'codigo_produto', 'descricao', 'codigo_barras', 
                          'quantidade', 'valor_unitario', 'valor_total']
                # Filter to existing fields
                if records:
                    sample_dict = records[0].to_dict()
                    headers = [h for h in headers if h in sample_dict and sample_dict[h]]
            
            with open(output_path, 'w', newline='', encoding=self.config.get('CSV_ENCODING')) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for record in records:
                    # Convert record to dict and filter to only include headers
                    record_dict = record.to_dict()
                    filtered_dict = {k: v for k, v in record_dict.items() if k in headers}
                    writer.writerow(filtered_dict)
                    
        except Exception as e:
            raise ConversionError(f"Failed to write CSV file {output_path}: {e}")


# Backward compatibility - create alias
BatchConverter = EnhancedBatchConverter


# Global converter instance
_converter = None


def get_batch_converter() -> EnhancedBatchConverter:
    """Get global batch converter instance"""
    global _converter
    if _converter is None:
        _converter = EnhancedBatchConverter()
    return _converter
