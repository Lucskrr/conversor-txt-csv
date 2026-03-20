"""
Auto-update service for Conversor TOTVS
Simple and reliable update system using GitHub releases
"""

import json
import urllib.request
import urllib.error
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

from utils.config_service import get_config
from utils.logger import get_logger


class UpdateService:
    """Auto-update service for the application"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.current_version = self.config.VERSION
        # ATENÇÃO: Substitua SEU-USUARIO pelo seu username do GitHub
        self.version_url = "https://api.github.com/repos/famaringa/conversor-totvs/releases/latest"
        self.download_base_url = "https://github.com/famaringa/conversor-totvs/releases/download"
        
    def check_for_updates(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if updates are available
        
        Returns:
            Tuple of (update_available, release_info)
        """
        try:
            self.logger.info(f"Checking for updates. Current version: {self.current_version}")
            
            # Try to get version info from remote
            release_info = self._get_latest_release_info()
            if not release_info:
                self.logger.warning("Could not fetch release info")
                return False, None
            
            latest_version = release_info.get('tag_name', '').lstrip('v')
            
            if self._is_newer_version(latest_version, self.current_version):
                self.logger.info(f"Update available: {latest_version}")
                return True, release_info
            
            self.logger.info("Application is up to date")
            return False, release_info
            
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            return False, None
    
    def _get_latest_release_info(self) -> Optional[Dict[str, Any]]:
        """Get latest release information from GitHub"""
        try:
            # For development/testing, return mock data
            if self.config.VERSION.startswith('1.'):  # Development mode
                return {
                    'tag_name': 'v1.2.0',
                    'name': 'Conversor TOTVS v1.2.0',
                    'body': 'New features and bug fixes',
                    'published_at': datetime.now().isoformat(),
                    'assets': [
                        {
                            'name': 'ConversorTOTVS.exe',
                            'browser_download_url': f"{self.download_base_url}/v1.2.0/ConversorTOTVS.exe"
                        }
                    ]
                }
            
            # Production mode - fetch from GitHub
            with urllib.request.urlopen(self.version_url, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                else:
                    self.logger.warning(f"GitHub API returned status {response.status}")
                    return None
                    
        except urllib.error.URLError as e:
            self.logger.warning(f"Network error checking updates: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching release info: {e}")
            return None
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compare version strings"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad with zeros if needed
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
            
        except ValueError:
            self.logger.warning(f"Invalid version format: {latest} vs {current}")
            return False
    
    def download_update(self, release_info: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Download update package
        
        Returns:
            Tuple of (success, download_path_or_error)
        """
        try:
            assets = release_info.get('assets', [])
            if not assets:
                return False, "No download assets found"
            
            # Find the executable
            exe_asset = None
            for asset in assets:
                if asset['name'].endswith('.exe'):
                    exe_asset = asset
                    break
            
            if not exe_asset:
                return False, "No executable found in release"
            
            download_url = exe_asset['browser_download_url']
            filename = exe_asset['name']
            
            # Create temporary download directory
            temp_dir = tempfile.mkdtemp(prefix="conversor_update_")
            download_path = Path(temp_dir) / filename
            
            self.logger.info(f"Downloading update to: {download_path}")
            
            # Download the file
            with urllib.request.urlopen(download_url, timeout=30) as response:
                if response.status == 200:
                    with open(download_path, 'wb') as f:
                        shutil.copyfileobj(response, f)
                else:
                    return False, f"Download failed with status {response.status}"
            
            self.logger.info(f"Update downloaded successfully: {download_path}")
            return True, str(download_path)
            
        except Exception as e:
            self.logger.error(f"Error downloading update: {e}")
            return False, str(e)
    
    def prepare_update_script(self, update_path: str) -> str:
        """
        Create update script to replace the executable
        
        Returns:
            Path to the update script
        """
        current_exe = sys.executable if getattr(sys, 'frozen', False) else __file__
        script_path = Path(tempfile.mktemp(suffix='.bat'))
        
        # Create batch script for Windows
        script_content = f"""@echo off
echo Atualizando Conversor TOTVS...
timeout /t 2 /nobreak >nul

copy /Y "{update_path}" "{current_exe}" >nul 2>&1
if errorlevel 1 (
    echo Erro ao atualizar arquivo
    timeout /t 5
    exit /b 1
)

echo Atualizacao concluida com sucesso!
start "" "{current_exe}"
del "{script_path}"
exit /b 0
"""
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            self.logger.info(f"Update script created: {script_path}")
            return str(script_path)
            
        except Exception as e:
            self.logger.error(f"Error creating update script: {e}")
            raise
    
    def install_update(self, release_info: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Install update by downloading and preparing update script
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Download update
            success, result = self.download_update(release_info)
            if not success:
                return False, f"Download failed: {result}"
            
            update_path = result
            
            # Create update script
            script_path = self.prepare_update_script(update_path)
            
            # Launch update script and exit current application
            self.logger.info("Launching update process...")
            
            if getattr(sys, 'frozen', False):
                # Running as executable
                subprocess.Popen(script_path, shell=True, close_fds=True)
            else:
                # Running as script
                subprocess.Popen(['cmd', '/c', script_path], close_fds=True)
            
            return True, "Atualização iniciada. A aplicação será reiniciada."
            
        except Exception as e:
            self.logger.error(f"Error installing update: {e}")
            return False, f"Erro na instalação: {str(e)}"
    
    def get_update_info(self) -> Dict[str, Any]:
        """Get current update status information"""
        update_available, release_info = self.check_for_updates()
        
        result = {
            'current_version': self.current_version,
            'update_available': update_available,
            'last_check': datetime.now().isoformat()
        }
        
        if release_info:
            result.update({
                'latest_version': release_info.get('tag_name', '').lstrip('v'),
                'release_name': release_info.get('name', ''),
                'release_notes': release_info.get('body', ''),
                'release_date': release_info.get('published_at', '')
            })
        
        return result


# Global update service instance
_update_service = None


def get_update_service() -> UpdateService:
    """Get global update service instance"""
    global _update_service
    if _update_service is None:
        _update_service = UpdateService()
    return _update_service


def check_updates() -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Convenience function to check for updates"""
    service = get_update_service()
    return service.check_for_updates()
