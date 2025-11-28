# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📊 Project Overview

**Project**: RF Converter - S-parameter to CSV Converter
**Focus**: Desktop application for RF measurement data conversion
**Stage**: Production Ready - v1.1 (Band Mapping System)
**Last Updated**: 2025-11-27

---

## 🎯 Current Project Status

### Main Project: RF Converter ⭐ (100% Complete)
**Location**: `rf_converter/`
**Status**: ✅ Production Ready v1.1
**Purpose**: PyQt6 desktop app for converting SnP files to CSV with 3GPP band filtering

**Key Features**:
- 50 3GPP bands (LTE/5G NR/GSM) with Rx/Tx separation (B32, B202 added)
- Automatic band detection from filenames
- Regional code support (B41[NA], B41[EU], etc.)
- **Band notation mapping system** (Phase 5 - NEW)
- Batch conversion with real-time progress
- Settings persistence and logging
- Custom RF-themed icon

**Quick Start**:
```bash
cd C:\Python\Project\rx-gain-viewer
rf_converter\run_gui.bat
```

### Maintenance: Django Web App
**Location**: `django_test/`
**Status**: Maintenance only (no active development)
**Purpose**: Web-based S-parameter viewer
**Note**: Main development has been merged to another project

### Archived: Prototype
**Location**: `archive/prototype/`
**Status**: Archived (validation complete)
**Purpose**: Initial proof of concept
**Note**: No longer in active use

---

## 📁 Project Structure

```
rx-gain-viewer/
├── rf_converter/                   ⭐ MAIN PROJECT
│   ├── core/
│   │   ├── parsers/
│   │   │   ├── base_parser.py      # 50 band configs + filtering
│   │   │   ├── rx_gain_parser.py   # Rx Gain measurement
│   │   │   ├── rx_sens_parser.py   # Rx Sensitivity
│   │   │   └── tx_parser.py        # Tx Power (template)
│   │   ├── band_mapper.py          # Band notation mapping (NEW)
│   │   ├── mappings/               # Mapping config files (NEW)
│   │   │   ├── README.txt
│   │   │   ├── example_alpha1c_evb1.json
│   │   │   ├── example_basic.json
│   │   │   └── example_comprehensive.json
│   │   └── logger.py               # Logging system
│   ├── ui_pyqt6/
│   │   ├── main.py                 # Entry point
│   │   └── main_window.py          # Main window (850x1020)
│   ├── tests/                      # Test files
│   │   ├── test_band_filtering.py
│   │   ├── test_band_mapper.py     # BandMapper tests (NEW)
│   │   ├── test_mapping_integration.py  # Integration tests (NEW)
│   │   ├── test_filename_parsing.py
│   │   └── test_real_files.py
│   ├── icon.ico                    # Custom RF icon
│   └── run_gui.bat                 # Quick launcher
│
├── django_test/                    # Maintenance only
├── archive/prototype/              # Old prototype
│
├── docs/                           # ALL DOCUMENTATION
│   ├── rf-converter/               # RF Converter docs
│   │   ├── USER_MANUAL_KR.md       # 📖 User manual
│   │   ├── development-log.md      # Development history
│   │   ├── workflow-diagrams.md    # Mermaid diagrams
│   │   └── sessions/               # Session logs
│   └── django/                     # Django docs
│
├── pyproject.toml
├── README.md                       # Main README (RF Converter focus)
└── CLAUDE.md                       # This file
```

---

## 🔑 Key Files and Their Purpose

### RF Converter Core Files

**`rf_converter/core/parsers/base_parser.py`** (Lines 24-90)
- **Purpose**: 50 3GPP band configurations with Rx/Tx frequency separation
- **Format**: `'Band': ((uplink_min, uplink_max), (downlink_min, downlink_max))`
- **Key Method**: `filter_frequency(df, band, direction='rx')` - Filter by band and Rx/Tx direction
- **Why Important**: Core of frequency filtering logic, supports future Tx Power feature

**`rf_converter/core/band_mapper.py`** (NEW - Phase 5)
- **Purpose**: Optional band notation mapping system (filename → N-plexer bank)
- **Pattern**: Singleton with O(1) lookup, JSON config files
- **Key Method**: `map(original: str) -> str` - Translate band notation
- **Why Important**: Enables comparison between different site notation systems

**`rf_converter/core/logger.py`**
- **Purpose**: Conversion history logging and application event tracking
- **Logs**: Python log + JSON history at `~/.rf_converter/logs/`
- **Why Important**: Tracks all conversions for debugging and audit

**`rf_converter/ui_pyqt6/main_window.py`**
- **Purpose**: Main application window (850x1020, optimized for no-scroll)
- **Settings**: QSettings integration for auto-save/restore
- **Features**: Drag & drop, real-time progress, quick access buttons, band mapping (NEW)
- **Why Important**: Main user interface with all features integrated

### Documentation Files

**`docs/rf-converter/USER_MANUAL_KR.md`**
- Complete Korean user manual for first-time users
- 8 Mermaid diagrams, troubleshooting guide
- **When to update**: After adding new features or UI changes

**`docs/rf-converter/development-log.md`**
- Complete development history with code examples
- All 8 user requests and implementations
- **When to update**: After significant development milestones

**`docs/rf-converter/sessions/`**
- Individual session logs with specific changes
- **When to add**: Create new file for each major feature development

---

## 🚀 Development Workflow

### For RF Converter Changes

1. **Before Starting**:
   - Read current status in this file
   - Check `docs/rf-converter/development-log.md` for context
   - Verify tests still pass: `python rf_converter/tests/test_*.py`

2. **During Development**:
   - Update code
   - Add/update tests in `rf_converter/tests/`
   - Update docstrings and comments

3. **After Completion**:
   - Update `docs/rf-converter/development-log.md` if significant
   - Create session log in `docs/rf-converter/sessions/` if major feature
   - Update `docs/rf-converter/USER_MANUAL_KR.md` if user-facing changes
   - Update this CLAUDE.md with new status
   - Run full test suite

4. **Git Workflow**:
   ```bash
   git add .
   git commit -m "Feat: [Description] with [Details]"
   git push origin main
   ```

### For Django Maintenance

- **Policy**: Maintenance only, no new features
- **Changes**: Bug fixes and critical updates only
- **Documentation**: Update `docs/django/` if needed

---

## 📝 Important Implementation Details

### 1. 3GPP Band Configuration
- **Total**: 48 bands (LTE FDD/TDD, GSM, 5G NR)
- **Format**: Tuple of tuples for UL/DL separation
- **Validated**: 100% success rate on 980 real files

### 2. Filename Parsing Pattern
- **Regex**: `B\d+(?:\[[^\]]+\])?` - Matches any bracket content
- **Supports**: B1, B41[NA], B1[B7] patterns
- **Test**: `rf_converter/tests/test_filename_parsing.py`

### 3. UI Layout
- **Window**: 850x1020 (no scroll required)
- **Spacing**: 10px main layout, 8px between sections
- **Font**: QGroupBox titles 12pt (increased by 4pt)

### 4. Logging System
- **Location**: `~/.rf_converter/logs/`
- **Files**: `rf_converter.log` (Python) + `conversion_history.json` (structured)
- **Auto-rotation**: 10MB max size, 5 backup files

### 5. Settings Persistence
- **Technology**: QSettings (Windows Registry)
- **Location**: `HKEY_CURRENT_USER\Software\RF Analyzer\RF Converter`
- **Stored**: Checkboxes, measurement type, output path

---

## 🧪 Testing Standards

### Before Committing
1. Run all tests: `python rf_converter/tests/test_*.py`
2. Verify band filtering: `test_band_filtering.py` (48/48 pass)
3. Verify filename parsing: `test_filename_parsing.py` (100% success)
4. Visual UI check: Run GUI and verify layout

### Test Coverage
- ✅ 48 bands validated
- ✅ 980 real files tested
- ✅ 35 CA patterns verified

---

## ⚠️ Known Issues and Considerations

### Issue 1: Claude Code Edit Tool
- **Problem**: Edit tool may fail with large files
- **Workaround**: Use Bash commands for file modifications
- **Status**: Ongoing, no action required

### Issue 2: Regional Codes
- **Solution**: Fixed regex pattern supports any bracket content
- **Validation**: 100% success on real data
- **Status**: ✅ Resolved

---

## 🎯 Future Roadmap

### Phase 5: Band Mapping System ✅ COMPLETE
- [x] BandMapper singleton class (300 lines)
- [x] JSON mapping file system
- [x] GUI integration (checkbox + file selector + status)
- [x] Unit tests (25 tests, 100% pass)
- [x] Integration tests (5 tests, 100% pass)
- [x] Example mapping files (3 files)
- [x] Documentation and user guide

### Phase 6: Tx Power Feature (Planned)
- [ ] Implement `tx_parser.py` (currently template)
- [ ] Add Tx Power radio button to UI
- [ ] Test uplink frequency filtering
- [ ] Validate against Tx Power measurement data

### Phase 7: Data Visualization (Potential)
- [ ] Matplotlib integration for inline plotting
- [ ] Export to PNG/PDF with graphs
- [ ] Comparison overlay (Our Measurement vs Client Data)

### Phase 8: Advanced Analysis (Potential)
- [ ] S-parameter quality metrics
- [ ] Frequency response analysis
- [ ] Band edge detection
- [ ] Automatic pass/fail criteria

---

## 📚 Documentation Index

### RF Converter Documentation
1. **[USER_MANUAL_KR.md](docs/rf-converter/USER_MANUAL_KR.md)** - Complete user guide (Korean)
2. **[development-log.md](docs/rf-converter/development-log.md)** - Full development history
3. **[workflow-diagrams.md](docs/rf-converter/workflow-diagrams.md)** - 17 Mermaid diagrams
4. **[sessions/](docs/rf-converter/sessions/)** - Individual session logs

### Django Documentation
1. **[session-2025-10-10.md](docs/django/session-2025-10-10.md)** - SSE progress tracking
2. **[session-2025-10-11.md](docs/django/session-2025-10-11.md)** - Session management
3. **[ppt-automation.md](docs/django/ppt-automation.md)** - PPT export feature

---

## 🎓 Learning Resources

### For New Developers
1. Start with **[USER_MANUAL_KR.md](docs/rf-converter/USER_MANUAL_KR.md)** to understand features
2. Read **[development-log.md](docs/rf-converter/development-log.md)** for technical details
3. Review `base_parser.py` for band configuration logic
4. Check `main_window.py` for UI implementation

### For Understanding 3GPP Specs
- Reference: 3GPP TS 36.101 (LTE bands)
- All band configurations validated against official specs
- Rx/Tx separation follows FDD/TDD standards

---

## 🔧 Quick Commands

### Run Application
```bash
# Quick start
rf_converter\run_gui.bat

# Manual start
.venv\Scripts\python.exe rf_converter\ui_pyqt6\main.py

# UV start
uv run rf_converter/ui_pyqt6/main.py
```

### Run Tests
```bash
# Band filtering and parsing tests
.venv\Scripts\python.exe rf_converter/tests/test_band_filtering.py
.venv\Scripts\python.exe rf_converter/tests/test_filename_parsing.py
.venv\Scripts\python.exe rf_converter/tests/test_real_files.py

# Band mapper tests (NEW)
.venv\Scripts\python.exe rf_converter/tests/test_band_mapper.py
.venv\Scripts\python.exe rf_converter/tests/test_mapping_integration.py
```

### View Logs
```bash
# Open log directory
explorer %USERPROFILE%\.rf_converter\logs

# View latest log
type %USERPROFILE%\.rf_converter\logs\rf_converter.log

# View conversion history
type %USERPROFILE%\.rf_converter\logs\conversion_history.json
```

---

## ✅ Project Completion Checklist

- [x] Core SnP parsing functionality
- [x] 50 3GPP bands with Rx/Tx separation (B32, B202 added)
- [x] Regional code support (NA, EU, CN, SA)
- [x] Band notation mapping system (Phase 5)
- [x] UI optimization (no scroll required)
- [x] Custom icon integration
- [x] Logging system
- [x] Settings persistence
- [x] 100% parsing success rate
- [x] Complete documentation
- [x] User manual (Korean)
- [x] LNA Gain State extraction fixed
- [x] Production ready

---

## 📝 Recent Changes

### v1.1 - 2025-11-27 (Band Mapping System)

**Phase 5 Complete**: Band notation mapping system
- **BandMapper class**: Singleton with O(1) lookup, JSON configuration
- **GUI integration**: Checkbox + file selector + status display
- **CSV output**: Added `debug-nplexer_bank` column for mapped notation
- **Test coverage**: 25 unit tests + 5 integration tests (100% pass)
- **Example files**: 3 mapping templates with comprehensive documentation

**Problem Solved**: Different sites use different notation for same bands (B41[CN] vs 34_39+41)

**Files**: [session-2025-11-27-band-mapping.md](docs/rf-converter/sessions/session-2025-11-27-band-mapping.md)

### v1.0.1 - 2025-11-03 (Bug Fix + New Bands)

- **LNA Gain State Extraction**: Fixed regex pattern (G0H → G0_H, G1 → G1)
- **B32**: 1452-1496 MHz (3GPP SDL)
- **B202**: 2483.5-2500 MHz (Custom band)
- **Total Bands**: 48 → 50 ✅

---

**Project Status**: ✅ **PRODUCTION READY - v1.1**

**Main Focus**: RF Converter (rf_converter/)
**Maintenance**: Django Web App (django_test/)
**Archived**: Prototype (archive/prototype/)

**Last Updated**: 2025-11-03
**Next Session**: New features or enhancements as requested
