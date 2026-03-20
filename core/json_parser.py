"""
Generic JSON-based parser for Conversor TOTVS
Uses formats_config.json to define parsing patterns
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Callable
from exceptions import ParsingError, UnsupportedFormatError

from parsers import Record, NumberParser


class JSONBasedParser:
    """Generic parser that uses JSON configuration"""
    
    def __init__(self, format_config: Dict):
        self.format_config = format_config
        self.record_pattern = re.compile(format_config['record_pattern'])
        self.field_mapping = format_config['field_mapping']
        self.number_fields = format_config.get('number_fields', [])
        self.multiline_description = format_config.get('multiline_description', False)
        
        # Compile multiline patterns
        if self.multiline_description:
            self.multiline_pattern = re.compile(format_config.get('multiline_pattern', r'^\s*\d+\s+\d+'))
            self.multiline_stop_patterns = [
                re.compile(pattern) 
                for pattern in format_config.get('multiline_stop_patterns', [])
            ]
    
    def parse(self, lines: List[str], progress_callback: Optional[Callable] = None) -> List[Record]:
        """Parse lines using JSON configuration"""
        records = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            match = self.record_pattern.match(line)
            
            if match:
                # Extract fields using regex groups
                field_values = {}
                for field_name, group_num in self.field_mapping.items():
                    if group_num is not None and group_num <= len(match.groups()):
                        value = match.group(group_num)
                        if value:
                            value = value.strip()
                            # Parse numbers if needed
                            if field_name in self.number_fields:
                                value = NumberParser.parse_number(value)
                        else:
                            value = ''
                        field_values[field_name] = value
                    else:
                        field_values[field_name] = ''
                
                # Handle multiline descriptions
                if self.multiline_description and 'descricao' in field_values:
                    descricao = field_values['descricao']
                    i += 1
                    
                    while i < len(lines):
                        next_line = lines[i]
                        
                        # Check if we should continue collecting description
                        should_continue = False
                        
                        if next_line.strip():
                            # Stop if matches multiline pattern (new record)
                            if self.multiline_pattern.match(next_line):
                                should_continue = False
                            else:
                                # Check stop patterns
                                for stop_pattern in self.multiline_stop_patterns:
                                    if stop_pattern.match(next_line.strip().upper()):
                                        should_continue = False
                                        break
                                else:
                                    # No stop pattern matched, continue
                                    should_continue = True
                        
                        if should_continue:
                            descricao += ' ' + next_line.strip()
                            i += 1
                        else:
                            break
                    
                    field_values['descricao'] = descricao.strip()
                    i -= 1  # Adjust for the main loop increment
                
                # Create Record object
                records.append(Record(**field_values))
            
            i += 1
            if progress_callback:
                progress_callback(i, len(lines))
        
        return records


class ConfigurableFormatDetector:
    """Format detector using JSON configuration"""
    
    def __init__(self):
        self.formats_config = self._load_formats_config()
    
    def _load_formats_config(self) -> Dict:
        """Load formats configuration from JSON file"""
        config_path = Path(__file__).parent.parent / 'formats_config.json'
        
        if not config_path.exists():
            raise ParsingError("formats_config.json not found")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ParsingError(f"Error loading formats config: {e}")
    
    def detect_format(self, file_path: str) -> Optional[str]:
        """Detect format from filename and content"""
        import os
        
        # Try filename patterns first
        filename = os.path.basename(file_path)
        for format_name, format_config in self.formats_config['formats'].items():
            pattern = format_config['pattern']
            if re.search(pattern, filename, re.IGNORECASE):
                return format_name
        
        # Try content patterns
        try:
            with open(file_path, 'r', encoding='latin1') as f:
                content = f.read(8192).upper()
                
            for format_name, format_config in self.formats_config['formats'].items():
                content_pattern = format_config.get('content_pattern')
                if content_pattern and re.search(content_pattern, content):
                    return format_name
                    
        except (UnicodeDecodeError, IOError) as e:
            raise ParsingError(f"Failed to read file for format detection: {e}")
        
        return None
    
    def get_parser(self, format_name: str) -> JSONBasedParser:
        """Get parser for specified format"""
        if format_name not in self.formats_config['formats']:
            raise UnsupportedFormatError(format_name, list(self.formats_config['formats'].keys()))
        
        format_config = self.formats_config['formats'][format_name]
        return JSONBasedParser(format_config)
    
    def get_csv_headers(self, format_name: str) -> List[str]:
        """Get CSV headers for format"""
        if format_name not in self.formats_config['formats']:
            return []
        
        return self.formats_config['formats'][format_name]['csv_headers']
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format names"""
        return list(self.formats_config['formats'].keys())


class ConfigurableParserFactory:
    """Factory for creating configurable parsers"""
    
    def __init__(self):
        self.detector = ConfigurableFormatDetector()
    
    def create_parser(self, format_name: str) -> JSONBasedParser:
        """Create parser for specified format"""
        return self.detector.get_parser(format_name)
    
    def try_parse_all(self, lines: List[str]) -> Tuple[Optional[str], List[Record]]:
        """Try all parsers and return first successful result"""
        for format_name in self.detector.get_supported_formats():
            try:
                parser = self.create_parser(format_name)
                records = parser.parse(lines)
                if records:
                    return format_name, records
            except Exception:
                continue
        
        return None, []


# Global instance
_configurable_factory = None


def get_configurable_factory() -> ConfigurableParserFactory:
    """Get global configurable parser factory"""
    global _configurable_factory
    if _configurable_factory is None:
        _configurable_factory = ConfigurableParserFactory()
    return _configurable_factory
