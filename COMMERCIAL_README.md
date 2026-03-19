# Conversor TOTVS - Commercial Edition

🏢 **Professional Desktop Application with Licensing & Auto-Update**

## 🎯 Overview

This is the commercial-ready version of Conversor TOTVS, transformed from a simple converter into a professional desktop application with enterprise features:

- ✅ **Machine-based Licensing System**
- ✅ **Auto-Update Mechanism** 
- ✅ **Professional Architecture**
- ✅ **Production-Ready Build**
- ✅ **Corporate UI Design**

## 📁 Project Structure

```
conversor-totvs/
├── app/                    # Application entry point
│   ├── __init__.py
│   └── main.py            # Main application with licensing & updates
├── core/                   # Business logic
│   ├── exceptions.py      # Custom exceptions
│   ├── parsers.py         # Format detection & parsing
│   └── converter_engine.py # Core conversion logic
├── services/              # Application services
│   ├── license_service.py # Machine-based licensing
│   └── update_service.py  # Auto-update system
├── ui/                     # User interface
│   ├── dialogs.py          # Update & license dialogs
│   └── ui_components_simple.py # Reusable UI components
├── utils/                  # Utilities
│   ├── __init__.py
│   ├── config_service.py  # Configuration management
│   └── logger.py          # Professional logging
├── app/                    # Application package
├── production.spec        # PyInstaller production build
├── generate_license.py    # License generation utility
├── test_commercial.py     # Test suite
├── license.json          # Generated license file
├── logo.png              # Application logo (optional)
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Generate License

```bash
python generate_license.py
```

This will:
- Show current Machine ID
- Generate license for current machine
- Save license to `license.json`

### 2. Run Application

```bash
python app/main.py
```

### 3. Build for Distribution

```bash
# Production build with optimizations
pyinstaller production.spec

# Executable will be in dist/ConversorTOTVS.exe
```

## 🔐 Licensing System

### How It Works

1. **Machine Identification**: Generates unique ID based on hardware
2. **License Validation**: Checks local license file on startup
3. **Graceful Blocking**: Shows professional error if license invalid

### License Generation

```bash
# Generate for current machine (365 days)
python generate_license.py

# Generate for specific machine
python generate_license.py
# Select option 2, enter Machine ID and days
```

### License File Format

```json
{
  "machine_id": "3CB5E14F2B01D229",
  "issued_date": "2026-03-19T14:31:23.163173",
  "expiry_date": "2027-03-19T14:31:23.163173",
  "product": "Conversor TOTVS",
  "version": "1.1.0",
  "company": "FA MARINGA LTDA",
  "license_key": "5B84A60CB9CD465C4D0F56C8101CF9BB"
}
```

## 🔄 Auto-Update System

### Features

- **Version Check**: Compares current version with GitHub releases
- **User Choice**: Shows update dialog with release notes
- **Seamless Update**: Downloads and replaces executable
- **Fallback Handling**: Graceful error handling for network issues

### Configuration

Update settings in `utils/config_service.py`:

```python
'UPDATE_CHECK_INTERVAL': 86400,  # 24 hours
'AUTO_UPDATE_ENABLED': True,
```

### GitHub Setup

1. Create releases on GitHub
2. Update `services/update_service.py` with your repo URL:
   ```python
   self.version_url = "https://api.github.com/repos/yourusername/conversor-totvs/releases/latest"
   ```

## 🏗️ Architecture

### Separation of Concerns

- **app/**: Application entry point and orchestration
- **core/**: Business logic and domain models
- **services/**: Cross-cutting concerns (licensing, updates)
- **ui/**: User interface components
- **utils/**: Shared utilities (config, logging)

### Design Patterns

- **Service Layer**: License and update services
- **Factory Pattern**: Parser creation
- **Observer Pattern**: Progress callbacks
- **Singleton Pattern**: Logger and config services

## 📦 Distribution

### PyInstaller Configuration

The `production.spec` includes:

- ✅ Optimized build settings
- ✅ Version info and metadata
- ✅ Resource inclusion (logos, licenses)
- ✅ Exclusion of unnecessary dependencies
- ✅ UPX compression for smaller size

### Build Commands

```bash
# Development build
pyinstaller --onefile --windowed app/main.py

# Production build (recommended)
pyinstaller production.spec
```

### Installer Creation

Use Inno Setup or NSIS to create professional installer:

```pascal
; Inno Setup example
[Setup]
AppName=Conversor TOTVS
AppVersion=1.1.0
DefaultDirName={pf}\ConversorTOTVS
DefaultGroupName=Conversor TOTVS

[Files]
Source: "dist\ConversorTOTVS.exe"; DestDir: "{app}"
Source: "license.json"; DestDir: "{app}"
```

## 🧪 Testing

### Test Suite

```bash
python test_commercial.py
```

Tests cover:
- ✅ Configuration loading
- ✅ Module imports
- ✅ License validation
- ✅ Format detection

### Manual Testing Checklist

- [ ] Application starts with valid license
- [ ] Application blocks with invalid license
- [ ] File conversion works correctly
- [ ] Update dialog appears (if newer version available)
- [ ] Drag-and-drop functionality
- [ ] Progress tracking during conversion

## 🔧 Configuration

### Application Settings

Edit `utils/config_service.py`:

```python
# Application metadata
'VERSION': '1.1.0'
'APP_NAME': 'Conversor TOTVS'
'COMPANY_NAME': 'FA MARINGA LTDA'

# UI Colors
'PRIMARY_COLOR': '#4CAF50'
'ACCENT_COLOR': '#1F4E79'

# Update settings
'UPDATE_CHECK_INTERVAL': 86400
'AUTO_UPDATE_ENABLED': True
```

### License Settings

```python
# License validation
'LICENSE_CHECK_INTERVAL': 3600  # 1 hour
'TRIAL_PERIOD_DAYS': 30
```

## 🚀 Future Enhancements

### Planned Features

- [ ] **Online License Validation**: Server-side license checking
- [ ] **Usage Analytics**: Track application usage
- [ ] **Multi-language Support**: Internationalization
- [ ] **Advanced Logging**: Remote log aggregation
- [ ] **Plugin System**: Extensible architecture

### Upgrade Path

The modular architecture makes it easy to:

1. Add new services in `services/`
2. Extend UI components in `ui/`
3. Add new parsers in `core/parsers.py`
4. Update configuration in `utils/config_service.py`

## 📞 Support

### License Issues

1. Check Machine ID: `python generate_license.py` (option 3)
2. Generate new license with correct Machine ID
3. Ensure `license.json` is in application directory

### Update Issues

1. Check internet connection
2. Verify GitHub repository URL in `update_service.py`
3. Check logs in `converter.log`

### General Issues

1. Check `converter.log` for detailed error information
2. Run test suite: `python test_commercial.py`
3. Verify all dependencies are installed

## 📄 License

This software is proprietary software of FA MARINGA LTDA.

© 2024 FA MARINGA LTDA - All rights reserved.

---

**Conversor TOTVS Commercial Edition** - Professional desktop application ready for enterprise distribution.
