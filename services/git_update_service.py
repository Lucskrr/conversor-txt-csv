"""
Git-based update service for development mode
Updates system by pulling latest changes from Git repository
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Tuple
from datetime import datetime

from utils.config_service import get_config
from utils.logger import get_logger


class GitUpdateService:
    """Service for Git-based updates during development"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.repo_url = "https://github.com/Lucskrr/conversor-txt-csv.git"
    
    def check_for_updates(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if there are updates in the Git repository
        
        Returns:
            Tuple of (update_available, update_info)
        """
        try:
            # Get current commit hash
            current_hash = self._get_current_commit()
            latest_hash = self._get_latest_commit()
            
            update_available = current_hash != latest_hash
            
            update_info = {
                'update_available': update_available,
                'current_commit': current_hash[:8],
                'latest_commit': latest_hash[:8],
                'commit_count': self._get_commit_count_behind(),
                'last_check': datetime.now().isoformat(),
                'update_type': 'git'
            }
            
            if update_available:
                self.logger.info(f"Git update available: {current_hash[:8]} → {latest_hash[:8]}")
            
            return update_available, update_info
            
        except Exception as e:
            self.logger.error(f"Error checking Git updates: {e}")
            return False, {'error': str(e)}
    
    def _get_current_commit(self) -> str:
        """Get current commit hash"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip()
        except:
            return ""
    
    def _get_latest_commit(self) -> str:
        """Get latest commit hash from remote"""
        try:
            result = subprocess.run(
                ['git', 'ls-remote', self.repo_url, 'HEAD'],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.split()[0] if result.stdout else ""
        except:
            return ""
    
    def _get_commit_count_behind(self) -> int:
        """Get number of commits behind"""
        try:
            # Fetch latest changes
            subprocess.run(['git', 'fetch', 'origin'], 
                         capture_output=True, timeout=30)
            
            # Count commits behind
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD..origin/main'],
                capture_output=True, text=True, timeout=10
            )
            return int(result.stdout.strip())
        except:
            return 0
    
    def update_system(self) -> Tuple[bool, str]:
        """
        Update system by pulling latest changes
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Pull latest changes
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0:
                self.logger.info("Git update successful")
                return True, "Sistema atualizado com sucesso via Git"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                self.logger.error(f"Git update failed: {error_msg}")
                return False, f"Falha na atualização: {error_msg}"
                
        except Exception as e:
            error_msg = f"Erro na atualização Git: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def get_update_info(self) -> Dict[str, Any]:
        """Get comprehensive update information"""
        update_available, git_info = self.check_for_updates()
        
        result = {
            'git_update_available': update_available,
            'git_info': git_info,
            'last_check': datetime.now().isoformat()
        }
        
        return result


# Global Git update service
_git_service = None


def get_git_update_service() -> GitUpdateService:
    """Get global Git update service instance"""
    global _git_service
    if _git_service is None:
        _git_service = GitUpdateService()
    return _git_service
