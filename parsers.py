"""
File parsing module for Conversor TOTVS
Handles parsing of different TXT formats
"""

import re
import os
from typing import List, Dict, Optional, Tuple, Callable
from exceptions import ParsingError, UnsupportedFormatError
from config import SUPPORTED_FORMATS, INPUT_ENCODING


class Record:
    """Represents a parsed record"""
    
    def __init__(self, seq: str = '', codigo_produto: str = '', descricao: str = '', 
                 codigo_barras: str = '', quantidade: str = '', valor_unitario: str = '', 
                 valor_total: str = ''):
        self.seq = seq
        self.codigo_produto = codigo_produto
        self.descricao = descricao
        self.codigo_barras = codigo_barras
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total
    
    def to_dict(self) -> Dict[str, str]:
        """Convert record to dictionary"""
        return {
            'seq': self.seq,
            'codigo_produto': self.codigo_produto,
            'descricao': self.descricao,
            'codigo_barras': self.codigo_barras,
            'quantidade': self.quantidade,
            'valor_unitario': self.valor_unitario,
            'valor_total': self.valor_total
        }


class FormatDetector:
    """Detects file format based on filename and content"""
    
    @staticmethod
    def detect_format(file_path: str) -> Optional[str]:
        """Detect format from filename and content"""
        # Try filename first
        filename = os.path.basename(file_path).lower()
        for format_name in SUPPORTED_FORMATS:
            if format_name in filename:
                return format_name
        
        # Try content detection
        try:
            with open(file_path, 'r', encoding=INPUT_ENCODING) as f:
                content = f.read(8192).upper()
                
            if 'GERR004' in content:
                return 'gerr004'
            if 'CDFR054' in content:
                return 'cdfr054'
            
            # Fallback: check for format-specific patterns
            if re.search(r'\bUN\b', content):
                return 'gerr004'
                
        except (UnicodeDecodeError, IOError) as e:
            raise ParsingError(f"Failed to read file for format detection: {e}")
        
        return None


class NumberParser:
    """Utility class for parsing numbers"""
    
    @staticmethod
    def parse_number(num_str: Optional[str]) -> str:
        """Parse and normalize number string"""
        if num_str is None or num_str == "":
            return ""
        
        normalized = num_str.strip().replace('.', '').replace(',', '.')
        try:
            return str(float(normalized))
        except ValueError:
            return num_str.strip()


class GERR004Parser:
    """Parser for GERR004 format"""
    
    @staticmethod
    def parse(lines: List[str], progress_callback: Optional[Callable] = None) -> List[Record]:
        """Parse GERR004 format lines"""
        records = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            match = re.match(r"\s*(\d+)\s+(\d+)\s+(.*?)\s+UN\s+(\d+)\s+([\d,]+)", line)
            
            if match:
                seq = match.group(1)
                codigo = match.group(2)
                descricao = match.group(3).strip()
                cod_barras = match.group(4)
                quantidade = NumberParser.parse_number(match.group(5))
                
                # Handle multi-line descriptions
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.strip() and not re.match(r"\s*\d+\s+\d+", next_line):
                        descricao += ' ' + next_line.strip()
                        i += 1
                
                records.append(Record(
                    seq=seq,
                    codigo_produto=codigo,
                    descricao=descricao.strip(),
                    codigo_barras=cod_barras,
                    quantidade=quantidade,
                    valor_unitario='',
                    valor_total=''
                ))
            
            i += 1
            if progress_callback:
                progress_callback(i, len(lines))
        
        return records


class CDFR054Parser:
    """Parser for CDFR054 format"""
    
    @staticmethod
    def _is_data_line(line: str) -> bool:
        """Check if line contains data"""
        return bool(re.match(r"^\s*(\d+)\s+([^\s]+)\s+(.+?)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s*$", line))
    
    @staticmethod
    def parse(lines: List[str], progress_callback: Optional[Callable] = None) -> List[Record]:
        """Parse CDFR054 format lines"""
        records = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            match = re.match(r"^\s*(\d+)\s+([^\s]+)\s+(.+?)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s*$", line)
            
            if match:
                seq = match.group(1)
                codigo = match.group(2)
                descricao = match.group(3).strip()
                quantidade = NumberParser.parse_number(match.group(4))
                valor_unitario = NumberParser.parse_number(match.group(5))
                valor_total = NumberParser.parse_number(match.group(6))
                
                # Handle multi-line descriptions
                while i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if (next_line.strip() and 
                        not CDFR054Parser._is_data_line(next_line) and 
                        not re.search(r'^(DATA SISTEMA|DATA/HORA|PAGINA)', next_line.strip().upper())):
                        descricao += ' ' + next_line.strip()
                        i += 1
                    else:
                        break
                
                records.append(Record(
                    seq=seq,
                    codigo_produto=codigo,
                    descricao=descricao.strip(),
                    codigo_barras='',
                    quantidade=quantidade,
                    valor_unitario=valor_unitario,
                    valor_total=valor_total
                ))
            
            i += 1
            if progress_callback:
                progress_callback(i, len(lines))
        
        return records


class ParserFactory:
    """Factory for creating appropriate parsers"""
    
    @staticmethod
    def create_parser(format_name: str):
        """Create parser for specified format"""
        parsers = {
            'gerr004': GERR004Parser,
            'cdfr054': CDFR054Parser
        }
        
        if format_name not in parsers:
            raise UnsupportedFormatError(format_name, list(parsers.keys()))
        
        return parsers[format_name]()
    
    @staticmethod
    def try_parse_all(lines: List[str]) -> Tuple[Optional[str], List[Record]]:
        """Try all parsers and return first successful result"""
        for format_name in SUPPORTED_FORMATS:
            try:
                parser = ParserFactory.create_parser(format_name)
                records = parser.parse(lines)
                if records:
                    return format_name, records
            except Exception:
                continue
        
        return None, []
