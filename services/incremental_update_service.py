"""
Incremental update service for formats and configurations
Allows updating formats without full application restart
"""

import json
import urllib.request
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from utils.config_service import get_config
from utils.logger import get_logger


class IncrementalUpdateService:
    """Service for incremental updates of formats and configs"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.formats_url = "https://api.github.com/repos/Lucskrr/conversor-txt-csv/contents/formats_config.json"
        self.plugins_url = "https://api.github.com/repos/Lucskrr/conversor-txt-csv/contents/plugins"
    
    def check_format_updates(self) -> bool:
        """Check if there are format updates available"""
        try:
            # Check formats config
            local_formats = self._get_local_formats_hash()
            remote_formats = self._get_remote_formats_hash()
            
            return local_formats != remote_formats
            
        except Exception as e:
            self.logger.error(f"Error checking format updates: {e}")
            return False
    
    def update_formats(self) -> bool:
        """Download and update formats configuration"""
        try:
            # Download latest formats config
            formats_data = self._download_formats_config()
            if formats_data:
                # Save to local file
                formats_path = Path(__file__).parent.parent / 'formats_config.json'
                with open(formats_path, 'w', encoding='utf-8') as f:
                    json.dump(formats_data, f, indent=2, ensure_ascii=False)
                
                self.logger.info("Formats configuration updated successfully")
                return True
            
        except Exception as e:
            self.logger.error(f"Error updating formats: {e}")
        
        return False
    
    def _get_local_formats_hash(self) -> str:
        """Get hash of local formats config"""
        formats_path = Path(__file__).parent.parent / 'formats_config.json'
        
        if formats_path.exists():
            import hashlib
            with open(formats_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        
        return ""
    
    def _get_remote_formats_hash(self) -> str:
        """Get hash of remote formats config from GitHub API"""
        try:
            with urllib.request.urlopen(self.formats_url, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data.get('sha', '')
        except:
            pass
        
        return ""
    
    def _download_formats_config(self) -> Optional[Dict[str, Any]]:
        """Download formats configuration from GitHub"""
        try:
            # Get download URL
            with urllib.request.urlopen(self.formats_url, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    download_url = data.get('download_url')
                    
                    if download_url:
                        # Download actual file
                        with urllib.request.urlopen(download_url, timeout=10) as file_response:
                            if file_response.status == 200:
                                return json.loads(file_response.read().decode('utf-8'))
        
        except Exception as e:
            self.logger.error(f"Error downloading formats config: {e}")
        
        return None
    
    def get_update_info(self) -> Dict[str, Any]:
        """Get information about available updates"""
        return {
            'formats_update_available': self.check_format_updates(),
            'last_check': datetime.now().isoformat(),
            'formats_url': self.formats_url
        }


# Global incremental update service
_incremental_service = None


def get_incremental_service() -> IncrementalUpdateService:
    """Get global incremental update service instance"""
    global _incremental_service
    if _incremental_service is None:
        _incremental_service = IncrementalUpdateService()
    return _incremental_service
