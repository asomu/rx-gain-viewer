# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📊 Project Status

**Project**: RF S-parameter Analyzer for PA Module Testing
**Stage**: Active Development - Real-time Progress Tracking Complete
**Last Updated**: 2025-10-10

### Current Progress
- **Phase 1 (Prototype)**: 100% ✅ Complete
- **Phase 1.5 (CSV Support + Grid Generation)**: 100% ✅ Complete
- **Phase 1.6 (PPT Automation)**: 80% ⏸️ Template needed
- **Phase 2 (Django App)**: 95% ✅ Chart UI + PDF Export + Real-time Progress complete
- **Overall**: ~95% Complete

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

### 4. CSV Parser (Enhanced) ⭐ NEW

**File**: `prototype/parsers/csv_parser.py`

**Purpose**: Parse both simple CSV and consolidated measurement data (89 columns)

**Supported Formats**:
1. **Simple CSV**: frequency, gain_db format
2. **Consolidated CSV**: 89-column format with 109K+ measurement points

**Key Features**:
- Auto-detection of CSV format
- Active RF Path mapping (S0706 = ANT1→RXOUT1)
- Multi-band support (22 bands: B1-B66, n70, n75, n76)
- Multi-port support (12 port combinations)

**Key Methods**:
- `auto_detect_and_load()` - Auto-detect format and load
- `load_consolidated()` - Load 89-column consolidated format
- `get_data_by_filter(band, active_rf_path)` - Extract filtered data
- `get_available_bands()` - List all bands
- `get_available_paths(band)` - List port combinations
- `get_band_frequency_range(band)` - Get frequency range

**Example Usage**:
```python
parser = CsvParser('data/Bellagio_POC_Rx.csv')
parser.load_consolidated()

# Get B1 band, ANT1→RXOUT1 data
data = parser.get_data_by_filter(band='B1', active_rf_path='S0706')
# Returns: frequency (549 points), gain_db, port labels, etc.
```

**See**: [docs/csv-format-analysis.md](docs/csv-format-analysis.md)

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


---

## 🔄 Real-time Progress Tracking (NEW) ⭐

**Feature**: Server-Sent Events (SSE) based progress tracking for Full Report PDF generation

**File**: [session-2025-10-10.md](docs/session-2025-10-10.md) - Complete implementation details

### Key Features
- **Real-time Updates**: Progress bar with percentage, current item, elapsed time, ETA
- **Task Cancellation**: User can stop PDF generation mid-process
- **Automatic Download**: PDF downloads automatically on completion
- **Visual Feedback**: Modal dialog with smooth animations

### Components
1. **ProgressTracker** ()
   - Cache-based state management
   - Methods: start(), update(), complete(), cancel(), is_cancelled()

2. **SSE Endpoint** ()
   - Streams JSON updates every 0.5 seconds
   - Format: 

3. **Cancel Endpoint** ()
   - API to stop ongoing generation
   - URL: 

4. **Progress Modal** ()
   - EventSource API for SSE consumption
   - Cancel button (red) and Close button (green)

### Usage
/rf-analyzer/api/progress-stream/14/

**See**: [session-2025-10-10.md](docs/session-2025-10-10.md) for complete implementation details

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

**SnP File Grid Structure**:
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

**CSV File Grid Structure** (New):
- **Tabs**: One per Band (B1, B3, B7, B41, etc.)
- **Rows**: Port combinations (ANT1→RXOUT1, ANT2→RXOUT1, etc.)
- **Columns**: LNA gain states (G0_H, G0_M, G0_L) or single column
- **Cells**: Filtered CSV data charts

**Supported Port Combinations** (CSV):
```
ANT1 → RXOUT1 (S0706)    ANT1 → RXOUT2 (S0306)
ANT2 → RXOUT1 (S0705)    ANT2 → RXOUT2 (S0305)
ANTL → RXOUT1 (S0702)    ANTL → RXOUT2 (S0302)
ANT1 → RXOUT3 (S0806)    ANT1 → RXOUT4 (S0406)
ANT2 → RXOUT3 (S0805)    ANT2 → RXOUT4 (S0405)
ANTL → RXOUT3 (S0802)    ANTL → RXOUT4 (S0402)
```

---

## 🧪 Testing

### Prototype Testing

```bash
cd prototype
python filename_parser.py  # Test parser standalone
python main.py             # Generate demo charts
```

### CSV Parser Testing ⭐ NEW

```bash
cd prototype
..\.venv\Scripts\python.exe test_csv_parser.py

# Test Results:
# ✓ Loaded 109,884 data points with 22 bands and 12 Active RF Paths
# ✓ Auto-detected consolidated format
# ✓ Extracted B1 band S0706 data: 549 points, 2110-2170 MHz
# ✓ Tested multiple bands: B1, B3, B7, B41
```

### Django Testing

```bash
cd django_test
python manage.py test rf_analyzer
```

---

## 📚 Key Documentation

**Essential Reading**:
1. **[docs/csv-format-analysis.md](docs/csv-format-analysis.md)** - ⭐ CSV format specification (NEW)
2. [docs/session-2025-10-02.md](docs/session-2025-10-02.md) - Latest development session
3. [docs/actual-filename-format.md](docs/actual-filename-format.md) - Filename parsing rules
4. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Complete project structure
5. [docs/tech-stack-decision.md](docs/tech-stack-decision.md) - Architecture decisions

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

---

## 📊 PPT Automation (Phase 1.6) ⭐ NEW

### PptGenerator 클래스
**File**: `prototype/utils/ppt_generator.py`

**Purpose**: PowerPoint 자동 생성 (기존 템플릿 지원)

**Key Features**:
- 기존 회사 템플릿 PPT 열기
- 슬라이드 자동 추가 (제목 + 이미지)
- 426장 배치 생성

**사용법**:
```python
from pathlib import Path
from utils.ppt_generator import PptGenerator

# 템플릿 사용
template = Path("company_template.pptx")
generator = PptGenerator(template)

# 슬라이드 추가
for band, lna, port in conditions:
    title = f"{band} {lna} {port} LNA Gain"
    image = Path(f"{band}_{lna}_{port}.png")
    generator.add_slide_with_image(title, image)

# 저장 (템플릿 + 새 슬라이드)
generator.save(Path("output.pptx"))
```

### 벡터 vs 래스터 이미지
| 포맷 | 타입 | 확대 품질 | PPT 지원 | 크기 |
|------|------|----------|----------|------|
| PNG | 래스터 | ❌ 지글지글 | ✅ 필수 | 213 KB |
| PDF | 벡터 | ✅ 선명 | ⚠️ 부분적 | 32 KB |
| SVG | 벡터 | ✅ 선명 | ❌ 미지원 | 32 KB |

**결론**: PPT는 PNG 필수, 벡터 품질 원하면 PDF/SVG 별도 보관

**Next**: 템플릿 PPT 업로드 → 426장 자동 생성 (4-5분)

**Session Log**: [docs/session-2025-10-03-part2.md](docs/session-2025-10-03-part2.md)
