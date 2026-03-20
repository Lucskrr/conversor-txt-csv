"""
Simple update checker for Conversor TOTVS v1.1
Add update capability to existing v1.1 installation
"""

import json
import urllib.request
import urllib.error
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

# Import existing config
from config import VERSION, APP_NAME


class UpdateChecker:
    """Simple update checker for v1.1"""
    
    def __init__(self):
        self.current_version = VERSION
        self.version_url = "https://api.github.com/repos/Lucskrr/conversor-txt-csv/releases/latest"
        self.download_base_url = "https://github.com/Lucskrr/conversor-txt-csv/releases/download"
        
    def check_for_updates(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Check if updates are available"""
        try:
            print(f"Checking for updates. Current version: {self.current_version}")
            
            # Get version info from GitHub
            release_info = self._get_latest_release_info()
            if not release_info:
                print("Could not fetch release info")
                return False, None
            
            latest_version = release_info.get('tag_name', '').lstrip('v')
            
            if self._is_newer_version(latest_version, self.current_version):
                print(f"Update available: {latest_version}")
                return True, release_info
            
            print("Application is up to date")
            return False, release_info
            
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False, None
    
    def _get_latest_release_info(self) -> Optional[Dict[str, Any]]:
        """Get latest release information from GitHub"""
        try:
            with urllib.request.urlopen(self.version_url, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                else:
                    print(f"GitHub API returned status {response.status}")
                    return None
                    
        except urllib.error.URLError as e:
            print(f"Network error checking updates: {e}")
            return None
        except Exception as e:
            print(f"Error fetching release info: {e}")
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
            print(f"Invalid version format: {latest} vs {current}")
            return False
    
    def download_and_install_update(self, release_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Download and install update"""
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
            
            print(f"Downloading update to: {download_path}")
            
            # Download the file
            with urllib.request.urlopen(download_url, timeout=30) as response:
                if response.status == 200:
                    with open(download_path, 'wb') as f:
                        import shutil
                        shutil.copyfileobj(response, f)
                else:
                    return False, f"Download failed with status {response.status}"
            
            print(f"Update downloaded successfully: {download_path}")
            
            # Create update script
            script_path = self._create_update_script(download_path)
            
            # Launch update script
            print("Launching update process...")
            subprocess.Popen(script_path, shell=True, close_fds=True)
            
            return True, "Atualização iniciada. A aplicação será reiniciada."
            
        except Exception as e:
            print(f"Error installing update: {e}")
            return False, f"Erro na instalação: {str(e)}"
    
    def _create_update_script(self, update_path: str) -> str:
        """Create update script to replace the executable"""
        current_exe = sys.executable if getattr(sys, 'frozen', False) else __file__
        script_path = Path(tempfile.mktemp(suffix='.bat'))
        
        # Create batch script for Windows
        script_content = f"""@echo off
echo Atualizando {APP_NAME}...
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
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return str(script_path)


def check_for_updates():
    """Convenience function to check for updates"""
    checker = UpdateChecker()
    return checker.check_for_updates()


def install_update(release_info: Dict[str, Any]):
    """Convenience function to install update"""
    checker = UpdateChecker()
    return checker.download_and_install_update(release_info)
