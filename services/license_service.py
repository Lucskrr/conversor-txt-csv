"""
Licensing service for Conversor TOTVS
Machine-based licensing system with local validation
"""

import json
import hashlib
import platform
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from utils.config_service import get_config
from utils.logger import get_logger


class LicenseService:
    """Machine-based licensing service"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.machine_id = self._generate_machine_id()
        self.license_file = Path(self.config.get('APP_DIR')) / "license.json"
        
    def _generate_machine_id(self) -> str:
        """Generate unique machine ID based on hardware"""
        try:
            # Collect machine identifiers
            machine_info = {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'machine': platform.machine(),
                'system': platform.system(),
                'node': platform.node()
            }
            
            # Create hash of machine info
            machine_string = json.dumps(machine_info, sort_keys=True)
            machine_hash = hashlib.sha256(machine_string.encode()).hexdigest()
            
            # Return first 16 characters for readability
            return machine_hash[:16].upper()
            
        except Exception as e:
            self.logger.error(f"Failed to generate machine ID: {e}")
            # Fallback to simple hash
            return hashlib.sha256(platform.node().encode()).hexdigest()[:16].upper()
    
    def get_machine_id(self) -> str:
        """Get current machine ID"""
        return self.machine_id
    
    def create_license(self, machine_id: str, expiry_days: int = 365) -> Dict[str, Any]:
        """Create a license for a specific machine"""
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        
        license_data = {
            'machine_id': machine_id,
            'issued_date': datetime.now().isoformat(),
            'expiry_date': expiry_date.isoformat(),
            'product': self.config.get('APP_NAME'),
            'version': self.config.get('VERSION'),
            'company': self.config.get('COMPANY_NAME'),
            'license_key': hashlib.sha256(f"{machine_id}{expiry_date}".encode()).hexdigest()[:32].upper()
        }
        
        return license_data
    
    def save_license(self, license_data: Dict[str, Any]) -> bool:
        """Save license to file"""
        try:
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(license_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"License saved for machine: {license_data.get('machine_id')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save license: {e}")
            return False
    
    def load_license(self) -> Optional[Dict[str, Any]]:
        """Load license from file"""
        try:
            if not self.license_file.exists():
                return None
            
            with open(self.license_file, 'r', encoding='utf-8') as f:
                license_data = json.load(f)
            
            return license_data
            
        except Exception as e:
            self.logger.error(f"Failed to load license: {e}")
            return None
    
    def validate_license(self) -> tuple[bool, str]:
        """
        Validate current license
        
        Returns:
            Tuple of (is_valid, message)
        """
        license_data = self.load_license()
        
        if not license_data:
            return False, "Nenhuma licença encontrada. Contate o suporte."
        
        # Check machine ID
        if license_data.get('machine_id') != self.machine_id:
            return False, f"Licença inválida para esta máquina. Machine ID: {self.machine_id}"
        
        # Check expiry date
        expiry_str = license_data.get('expiry_date')
        if expiry_str:
            try:
                expiry_date = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                if datetime.now() > expiry_date:
                    return False, f"Licença expirou em {expiry_date.strftime('%d/%m/%Y')}"
            except ValueError:
                return False, "Data de expiração inválida na licença."
        
        # Check product
        if license_data.get('product') != self.config.get('APP_NAME'):
            return False, f"Licença inválida para o produto {self.config.get('APP_NAME')}"
        
        # License is valid
        issued_date = license_data.get('issued_date', '')
        if issued_date:
            try:
                issued = datetime.fromisoformat(issued_date.replace('Z', '+00:00'))
                issued_str = issued.strftime('%d/%m/%Y')
                return True, f"Licença válida. Emitida em {issued_str}"
            except ValueError:
                pass
        
        return True, "Licença válida."
    
    def is_licensed(self) -> bool:
        """Check if application is properly licensed"""
        is_valid, _ = self.validate_license()
        return is_valid
    
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """Get license information for display"""
        license_data = self.load_license()
        if not license_data:
            return None
        
        is_valid, message = self.validate_license()
        
        return {
            'machine_id': license_data.get('machine_id'),
            'issued_date': license_data.get('issued_date'),
            'expiry_date': license_data.get('expiry_date'),
            'license_key': license_data.get('license_key'),
            'is_valid': is_valid,
            'validation_message': message
        }
    
    def generate_trial_license(self, days: int = 30) -> bool:
        """Generate a trial license for current machine"""
        trial_license = self.create_license(self.machine_id, days)
        trial_license['is_trial'] = True
        trial_license['notes'] = f"Licença trial de {days} dias"
        
        return self.save_license(trial_license)


# Global license service instance
_license_service = None


def get_license_service() -> LicenseService:
    """Get global license service instance"""
    global _license_service
    if _license_service is None:
        _license_service = LicenseService()
    return _license_service


def check_license() -> tuple[bool, str]:
    """Convenience function to check license"""
    service = get_license_service()
    return service.validate_license()
