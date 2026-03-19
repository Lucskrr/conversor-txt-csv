"""
Test the commercial-ready Conversor TOTVS application
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all module imports"""
    print("Testing imports...")
    
    try:
        from utils.config_service import get_config
        print("✓ Config service imported")
        
        from utils.logger import get_logger
        print("✓ Logger imported")
        
        from services.license_service import check_license
        print("✓ License service imported")
        
        from services.update_service import check_updates
        print("✓ Update service imported")
        
        from core.parsers import FormatDetector
        print("✓ Parsers imported")
        
        from core.converter_engine import ConversionEngine
        print("✓ Converter engine imported")
        
        from ui.ui_components_simple import HeaderFrame
        print("✓ UI components imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_license():
    """Test license validation"""
    try:
        from services.license_service import check_license
        is_valid, message = check_license()
        print(f"✓ License check: {is_valid} - {message}")
        return is_valid
    except Exception as e:
        print(f"❌ License test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    try:
        from utils.config_service import get_config
        config = get_config()
        print(f"✓ App: {config.get('APP_NAME')} v{config.get('VERSION')}")
        print(f"✓ Supported formats: {config.get('SUPPORTED_FORMATS')}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_parsing():
    """Test format detection"""
    try:
        from core.parsers import FormatDetector
        
        # Create test files
        test_files = {
            'test_gerr004.txt': 'GERR004 TEST\n1 123 Produto UN 456 10,5',
            'test_cdfr054.txt': 'CDFR054 TEST\n1 123 Produto 10 5,50 55,00'
        }
        
        for filename, content in test_files.items():
            with open(filename, 'w', encoding='latin1') as f:
                f.write(content)
            
            detected = FormatDetector.detect_format(filename)
            print(f"✓ {filename}: {detected}")
            os.remove(filename)
        
        return True
        
    except Exception as e:
        print(f"❌ Parsing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Conversor TOTVS - Commercial Ready Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("License", test_license),
        ("Parsing", test_parsing),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nSummary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Application is commercial ready.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
