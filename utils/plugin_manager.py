"""
Plugin system for dynamic format support
Allows adding new conversion formats without full application update
"""

import json
import importlib
import os
from pathlib import Path
from typing import Dict, Any, List
from abc import ABC, abstractmethod

from utils.logger import get_logger


class FormatParser(ABC):
    """Abstract base class for format parsers"""
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Return format identifier"""
        pass
    
    @abstractmethod
    def get_file_pattern(self) -> str:
        """Return regex pattern to identify files"""
        pass
    
    @abstractmethod
    def parse_line(self, line: str) -> Dict[str, Any]:
        """Parse a single line and return structured data"""
        pass
    
    @abstractmethod
    def get_csv_headers(self) -> List[str]:
        """Return CSV column headers"""
        pass


class PluginManager:
    """Manages format plugins"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.plugins = {}
        self.config_formats = {}
        self._load_all_plugins()
    
    def _load_all_plugins(self):
        """Load all available plugins"""
        # Load from config file
        self._load_config_formats()
        
        # Load from plugins directory
        self._load_plugin_modules()
        
        self.logger.info(f"Loaded {len(self.get_supported_formats())} formats")
    
    def _load_config_formats(self):
        """Load formats from JSON config file"""
        config_path = Path(__file__).parent.parent / 'formats_config.json'
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.config_formats = config.get('formats', {})
                    self.logger.info(f"Loaded {len(self.config_formats)} formats from config")
            except Exception as e:
                self.logger.error(f"Error loading config formats: {e}")
    
    def _load_plugin_modules(self):
        """Load plugins from plugins directory"""
        plugins_dir = Path(__file__).parent.parent / 'plugins'
        
        if not plugins_dir.exists():
            plugins_dir.mkdir(exist_ok=True)
            return
        
        for plugin_file in plugins_dir.glob('*_plugin.py'):
            try:
                # Import plugin module
                spec = importlib.util.spec_from_file_location(
                    plugin_file.stem, plugin_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find parser classes in module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, FormatParser) and 
                        attr != FormatParser):
                        
                        parser = attr()
                        format_name = parser.get_format_name()
                        self.plugins[format_name] = parser
                        self.logger.info(f"Loaded plugin: {format_name}")
                
            except Exception as e:
                self.logger.error(f"Error loading plugin {plugin_file}: {e}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of all supported format names"""
        formats = list(self.plugins.keys()) + list(self.config_formats.keys())
        return list(set(formats))  # Remove duplicates
    
    def get_format_info(self, format_name: str) -> Dict[str, Any]:
        """Get information about a specific format"""
        if format_name in self.plugins:
            parser = self.plugins[format_name]
            return {
                'type': 'plugin',
                'name': parser.get_format_name(),
                'pattern': parser.get_file_pattern(),
                'headers': parser.get_csv_headers()
            }
        elif format_name in self.config_formats:
            return {
                'type': 'config',
                'name': format_name,
                'pattern': self.config_formats[format_name]['pattern'],
                'headers': [f['name'] for f in self.config_formats[format_name]['fields']]
            }
        return None
    
    def detect_format(self, filename: str) -> str:
        """Detect format from filename"""
        import re
        
        for format_name in self.get_supported_formats():
            info = self.get_format_info(format_name)
            if info:
                pattern = info['pattern']
                if re.search(pattern, filename, re.IGNORECASE):
                    return format_name
        
        return None


# Global plugin manager instance
_plugin_manager = None


def get_plugin_manager() -> PluginManager:
    """Get global plugin manager instance"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager
