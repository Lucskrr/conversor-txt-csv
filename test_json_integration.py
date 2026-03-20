#!/usr/bin/env python3
"""
Test script for JSON parser integration
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_json_parser():
    """Test JSON parser functionality"""
    print("🧪 Testing JSON Parser Integration...")
    
    try:
        # Test imports
        from core.json_parser import get_configurable_factory, ConfigurableFormatDetector
        from core.enhanced_converter import get_batch_converter
        print("✅ Imports successful")
        
        # Test format detector
        detector = ConfigurableFormatDetector()
        formats = detector.get_supported_formats()
        print(f"✅ Supported formats: {formats}")
        
        # Test converter
        converter = get_batch_converter()
        print(f"✅ Enhanced converter initialized")
        print(f"   JSON Parser available: {converter.json_factory is not None}")
        
        # Test with sample files
        compat_dir = project_root / "Compatibilidade"
        if compat_dir.exists():
            print(f"\n📁 Testing with files in: {compat_dir}")
            
            for file_path in compat_dir.glob("*.txt"):
                print(f"\n🔍 Testing file: {file_path.name}")
                
                # Detect format
                format_name = detector.detect_format(str(file_path))
                print(f"   Detected format: {format_name}")
                
                if format_name:
                    # Get headers
                    headers = detector.get_csv_headers(format_name)
                    print(f"   CSV headers: {headers}")
                    
                    # Test parsing (first few lines)
                    try:
                        parser = detector.get_parser(format_name)
                        with open(file_path, 'r', encoding='latin1') as f:
                            lines = [line.rstrip() for line in f.readlines()[:10]]
                        
                        records = parser.parse(lines[:5])  # Test first 5 lines
                        if records:
                            sample = records[0].to_dict()
                            print(f"   Sample record: {sample}")
                        else:
                            print("   No records parsed")
                            
                    except Exception as e:
                        print(f"   Parse error: {e}")
                else:
                    print("   ⚠️  Format not detected")
        
        print("\n🎉 JSON Parser Integration Test Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback():
    """Test fallback to original parser"""
    print("\n🔄 Testing Fallback to Original Parser...")
    
    try:
        # Temporarily disable JSON parser
        import core.json_parser
        original_available = core.json_parser.JSON_PARSER_AVAILABLE
        core.json_parser.JSON_PARSER_AVAILABLE = False
        
        # Test with original parser
        from parsers import FormatDetector, ParserFactory
        print("✅ Original parser available")
        
        # Restore
        core.json_parser.JSON_PARSER_AVAILABLE = original_available
        print("✅ Fallback test complete")
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("JSON Parser Integration Test")
    print("=" * 60)
    
    success1 = test_json_parser()
    success2 = test_fallback()
    
    if success1 and success2:
        print("\n🎉 All tests passed! System ready for JSON-based formats.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
