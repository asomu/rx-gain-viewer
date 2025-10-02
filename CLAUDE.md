# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📊 Project Status

**Project**: RF S-parameter Analyzer for PA Module Testing
**Stage**: Active Development - Phase 2 (Django Web App)
**Last Updated**: 2025-10-03 00:35

### Current Progress
- **Phase 1 (Prototype)**: 100% ✅ Complete
- **Phase 2 (Django App)**: 40% 🚧 In Progress
- **Overall**: ~60% Complete

---

## 🎯 Project Overview

PA(Power Amplifier) 모듈 S-parameter 측정 데이터 분석 및 시각화 웹 도구

**Purpose**: Network Analyzer로 측정한 SnP 파일에서 Gain 데이터를 추출하고, 다양한 Band/CA 조건을 그리드 레이아웃으로 비교 분석

**Users**: RF 엔지니어 (회사 내부 10명 이내)

**Deployment**: 회사 인트라넷 웹 서비스

---

## 🏗️ Project Structure

```
html_exporter/
├── docs/                       # 📚 Documentation
│   ├── project-discussion.md       # Project definition & Q&A
│   ├── tech-stack-decision.md      # Tech stack details
│   ├── actual-filename-format.md   # Complex filename analysis ⭐
│   ├── quickstart.md               # Quick start guide
│   └── session-2025-10-02.md       # Development session log
│
├── prototype/                  # ✅ Phase 1: Working Prototype
│   ├── parsers/
│   │   ├── snp_parser.py           # scikit-rf based SnP parser
│   │   └── csv_parser.py           # CSV file parser
│   ├── utils/
│   │   ├── sparameter.py           # S-parameter analysis tools
│   │   └── chart_generator.py      # Plotly chart generator
│   ├── main.py                     # CLI demo script
│   └── demo_*.html                 # Generated demo charts (3 files)
│
└── django_test/                # 🚧 Phase 2: Django Web App
    ├── manage.py
    ├── config/                     # Django project settings
    │   ├── settings.py             # ✅ HTMX, rf_analyzer configured
    │   └── urls.py                 # ✅ Routing configured
    └── rf_analyzer/                # 📱 RF Analyzer App
        ├── models.py               # ✅ MeasurementSession, MeasurementFile
        ├── filename_parser.py      # ✅ Complex filename parser ⭐
        ├── views.py                # ⏳ TODO
        ├── urls.py                 # ⏳ TODO
        └── templates/              # ⏳ TODO
```

**See**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure

---

## 🔑 Key Components

### 1. Complex Filename Parser ⭐

**File**: `django_test/rf_analyzer/filename_parser.py`

**Purpose**: Parse complex measurement filenames from test equipment

**Example Input**:
```
B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
```

**Parsed Output**:
```python
{
    'main_band': 'B1',                      # → Tab grouping
    'ca_label': 'B3_B7_B41',               # → Grid column
    'port_label': 'MHBIN1→ANTU_ANT1_ANT2'  # → Grid row
}
```

**Key Functions**:
- `parse(filename)` - Extract metadata from filename
- `organize_files(files)` - Organize into grid structure
- `get_summary(organized)` - Generate summary text

**See**: [docs/actual-filename-format.md](docs/actual-filename-format.md)

---

### 2. Prototype Chart Generator

**File**: `prototype/utils/chart_generator.py`

**Key Methods**:
- `create_single_chart()` - Single Gain chart
- `create_comparison_chart()` - Overlay comparison
- `create_grid_layout()` - NxM grid layout ⭐
- `export_to_html()` - Save to HTML

**Integration**: Will be imported and used by Django views

---

### 3. SnP Parser

**File**: `prototype/parsers/snp_parser.py`

**Technology**: scikit-rf library

**Key Methods**:
- `load()` - Load Touchstone file
- `get_gain(input_port, output_port)` - Extract S21 Gain
- `get_return_loss(port)` - Extract S11/S22

---

## 🚀 Development Workflow

### Starting a Session

```bash
cd C:\Project\html_exporter

# Virtual environment auto-detected by uv
# No manual activation needed

# For Django development:
cd django_test
..\.venv\Scripts\python.exe manage.py runserver
```

### Running Prototype Demo

```bash
cd prototype
..\.venv\Scripts\python.exe main.py
# Generates: demo_single.html, demo_comparison.html, demo_grid.html
```

---

## ⏭️ Next Development Steps

### Immediate (Next Session)

1. **Run Migrations**
   ```bash
   cd django_test
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Admin Interface**
   - Register MeasurementSession, MeasurementFile in admin.py
   - Create superuser for testing

3. **Implement Views**
   - File upload view
   - Auto-parsing view
   - Chart generation view

4. **Create Templates**
   - `base.html` - Base layout
   - `upload.html` - File upload UI
   - `partials/grid-preview.html` - Auto-detection preview
   - `partials/chart.html` - Chart display

5. **Integrate Prototype Code**
   - Import prototype parsers and chart generators
   - Build data pipeline: SnP upload → Parse → Chart

### Core Features (3-4 hours)

6. HTMX file upload UI
7. Auto-parsing preview with grid structure
8. Tab navigation (Band-based)
9. Interactive Plotly charts

### Advanced Features (Optional, 2-3 hours)

10. User authentication integration
11. Measurement history
12. PDF export
13. Preset management

---

## 🛠️ Technology Stack

### Backend
- **Python**: 3.12
- **Django**: 5.2.7
- **scikit-rf**: 1.8.0 (SnP parsing)
- **Pandas**: 2.3.3 (data processing)
- **NumPy**: 2.3.3 (numerical computing)

### Frontend
- **HTMX**: 1.26.0 (dynamic UI, matches existing project style)
- **Plotly.js**: 6.3.0 (interactive charts)
- **Alpine.js**: Optional (lightweight JS)

### Development
- **uv**: Package manager (super fast! 1.48s install)
- **pytest**: Testing framework

---

## 📝 Important Conventions

### File Naming

Measurement files follow complex patterns from test equipment:
```
{MainBand}[{Sub}]@{Input}_{Output}_{Config}_{CABands}_{Condition}.s{N}p
```

**Parser handles**:
- Band extraction (for tab grouping)
- CA condition extraction (for grid columns)
- Port combination extraction (for grid rows)
- Automatic grid structure detection

### Grid Layout

**Structure**:
- **Tabs**: One per main Band (B1, B3, B41, etc.)
- **Rows**: Port combinations (e.g., MHBIN1→ANTU_ANT1_ANT2)
- **Columns**: CA conditions (e.g., B3_B7_B41, B3_B7_B7)
- **Cells**: Individual SnP file charts

**Example**:
```
B1 Tab:
         B3_B7_B41   B3_B7_B7
MHBIN1→  [Chart]     [Chart]
MHBIN2→  [Chart]     [Chart]
```

---

## 🧪 Testing

### Prototype Testing

```bash
cd prototype
python filename_parser.py  # Test parser standalone
python main.py             # Generate demo charts
```

### Django Testing

```bash
cd django_test
python manage.py test rf_analyzer
```

---

## 📚 Key Documentation

**Essential Reading**:
1. [docs/session-2025-10-02.md](docs/session-2025-10-02.md) - Latest development session
2. [docs/actual-filename-format.md](docs/actual-filename-format.md) - Filename parsing rules
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Complete project structure
4. [docs/tech-stack-decision.md](docs/tech-stack-decision.md) - Architecture decisions

**Quick Reference**:
- [docs/quickstart.md](docs/quickstart.md) - Prototype usage guide
- [docs/project-discussion.md](docs/project-discussion.md) - Requirements & Q&A

---

## 🎯 Development Strategy

### Phased Approach

**Phase 1: Prototype** ✅ (Complete)
- Standalone Python scripts
- Validate SnP parsing and chart generation
- No web interface, just HTML file output

**Phase 2: Django Test App** 🚧 (40% Complete)
- Build in `django_test/` folder
- Implement and test all features
- Use HTMX for dynamic UI

**Phase 3: Production Integration** ⏳ (Not Started)
- Copy to existing Django project
- Integrate with company intranet
- Add authentication and user management

### Code Reuse

**Prototype → Django Integration**:
```python
# Django views can import prototype code
from prototype.parsers.snp_parser import SnpParser
from prototype.utils.chart_generator import ChartGenerator

def generate_chart_view(request):
    parser = SnpParser(file_path)
    freq, gain = parser.get_gain(1, 2)
    fig = ChartGenerator.create_grid_layout(...)
    return render(request, 'chart.html', {'chart': fig.to_html()})
```

**Benefits**:
- Tested code from prototype
- Fast Django development
- Separation of concerns

---

## ⚠️ Important Notes

### File Handling

**Always use the filename parser**:
```python
from rf_analyzer.filename_parser import ComplexFilenameParser

parsed = ComplexFilenameParser.parse(filename)
if parsed and parsed['is_valid']:
    # Use parsed metadata
else:
    # Handle parsing failure
```

### Django Models

**MeasurementSession**: One analysis task
- Links to User
- Stores grid configuration as JSON
- Groups multiple files

**MeasurementFile**: Single uploaded SnP file
- Links to MeasurementSession
- Stores parsed metadata (band, ca_label, port_label)
- Tracks parsing status

### HTMX Patterns

**File Upload**:
```html
<form hx-post="/rf-analyzer/upload/"
      hx-target="#preview"
      hx-encoding="multipart/form-data">
  <input type="file" name="files" multiple>
  <button>Upload</button>
</form>
```

**Partial Updates**:
```python
# views.py
if request.htmx:
    return render(request, 'partials/grid-preview.html', context)
return render(request, 'upload.html', context)
```

---

## 🐛 Known Issues

### Issue 1: Windows Console Encoding
- **Problem**: UnicodeEncodeError with emoji/Korean characters
- **Solution**: Use English messages in console output
- **Status**: ✅ Resolved in prototype

### Issue 2: uv run Build Error
- **Problem**: hatchling cannot find package structure
- **Workaround**: Run Python directly: `.venv/Scripts/python.exe script.py`
- **Status**: ✅ Workaround applied, no impact on functionality

---

## 💡 Tips for Future Development

1. **Always test filename parser** with new file patterns
2. **Use prototype code** for data processing logic
3. **Keep grid structure** consistent across tabs
4. **Document** any new filename patterns in `actual-filename-format.md`
5. **Update** session logs for major changes

---

## 🔗 Integration with Existing Django Project

When ready to integrate into production:

1. **Copy `rf_analyzer` app** to existing Django project
2. **Update settings.py** with INSTALLED_APPS, MIDDLEWARE
3. **Update urls.py** with rf-analyzer routes
4. **Run migrations** on production database
5. **Copy static files** and templates
6. **Test** file upload and parsing with real data

**Estimated Integration Time**: 1-2 hours

---

**Last Session**: 2025-10-02 (2 hours)
**Next Session Priority**: Complete Django views and HTMX templates
**Estimated Remaining Time**: 6-8 hours to MVP
