"""
License generation utility for Conversor TOTVS
Generate license files for customers
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.license_service import LicenseService


def generate_license(machine_id: str, days: int = 365, output_file: str = None):
    """Generate a license file"""
    service = LicenseService()
    
    print(f"Generating license for machine: {machine_id}")
    print(f"Valid for: {days} days")
    
    # Create license
    license_data = service.create_license(machine_id, days)
    
    # Add metadata
    license_data['notes'] = f"License generated for {machine_id}"
    license_data['generated_by'] = 'License Generator v1.0'
    
    # Save license
    if not output_file:
        output_file = f"license_{machine_id}.json"
    
    success = service.save_license(license_data)
    
    if success:
        print(f"✅ License saved to: {output_file}")
        print(f"📋 License key: {license_data.get('license_key')}")
        print(f"📅 Expires: {license_data.get('expiry_date')}")
        
        # Copy to project directory
        project_license = project_root / "license.json"
        with open(project_license, 'w', encoding='utf-8') as f:
            json.dump(license_data, f, indent=2, ensure_ascii=False)
        print(f"📁 Also saved to: {project_license}")
    else:
        print("❌ Failed to save license")
        return False
    
    return True


def get_machine_id():
    """Get current machine ID"""
    service = LicenseService()
    machine_id = service.get_machine_id()
    print(f"Current Machine ID: {machine_id}")
    return machine_id


def main():
    """Main license generation interface"""
    print("=" * 60)
    print("Conversor TOTVS - License Generator")
    print("=" * 60)
    
    # Show current machine ID
    current_machine = get_machine_id()
    
    print("\nOptions:")
    print("1. Generate license for this machine")
    print("2. Generate license for custom machine ID")
    print("3. Show current machine ID only")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        days = input("Enter validity in days (default 365): ").strip()
        days = int(days) if days.isdigit() else 365
        generate_license(current_machine, days)
    
    elif choice == '2':
        machine_id = input("Enter target machine ID: ").strip()
        days = input("Enter validity in days (default 365): ").strip()
        days = int(days) if days.isdigit() else 365
        output_file = input("Enter output filename (optional): ").strip()
        output_file = output_file if output_file else None
        generate_license(machine_id, days, output_file)
    
    elif choice == '3':
        print(f"\nMachine ID: {current_machine}")
        print("Provide this ID to customers for license generation")
    
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
