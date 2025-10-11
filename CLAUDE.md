# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📊 Project Status

**Project**: RF S-parameter Analyzer for PA Module Testing
**Stage**: Active Development - Admin Dashboard Complete
**Last Updated**: 2025-10-11

### Current Progress
- **Phase 1 (Prototype)**: 100% ✅ Complete
- **Phase 1.5 (CSV Support + Grid Generation)**: 100% ✅ Complete
- **Phase 1.6 (PPT Automation)**: 80% ⏸️ Template needed
- **Phase 2 (Django App)**: 99% ✅ Session Management + Chart Export + Admin Dashboard complete
- **Overall**: ~99% Complete

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
│   └── session-*.md                # Development session logs
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
└── django_test/                # ✅ Phase 2: Django Web App (99%)
    ├── manage.py
    ├── config/                     # Django project settings
    │   ├── settings.py             # ✅ HTMX, rf_analyzer configured
    │   └── urls.py                 # ✅ Routing configured
    └── rf_analyzer/                # 📱 RF Analyzer App
        ├── models.py               # ✅ MeasurementSession, MeasurementFile, MeasurementData
        ├── admin.py                # ✅ Django Admin Dashboard (NEW)
        ├── filename_parser.py      # ✅ Complex filename parser ⭐
        ├── views.py                # ✅ Upload, Chart, PDF Export, Progress Tracking
        ├── urls.py                 # ✅ All routes configured
        └── templates/              # ✅ index.html, viewer.html with HTMX
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

### 2. Django Admin Dashboard (NEW) ⭐

**File**: `django_test/rf_analyzer/admin.py`

**Purpose**: 관리자 인터페이스로 모든 모델 관리

**Features**:

#### MeasurementSession Admin
- **리스트 뷰**: 이름, 사용자, 파일 개수, 데이터 포인트 개수, 생성일, 수정일
- **필터**: 생성일, 수정일
- **검색**: 이름, 설명, 사용자명
- **통계**: 파일 개수, 데이터 포인트 개수 자동 계산

#### MeasurementFile Admin
- **리스트 뷰**: 파일명, 세션, 타입, Band, CA, Port, 파싱 상태, 파일 크기(KB), 업로드일
- **필터**: 파일 타입, Band, 파싱 상태, 업로드일
- **검색**: 파일명, 세션명, Band, CA, Port
- **대량 작업**: "Mark as parsed/unparsed" 상태 변경

#### MeasurementData Admin
- **리스트 뷰**: 세션, Band, LNA 상태, 포트1, 포트2, RF 경로, 주파수, 게인
- **검색**: 세션명, Band, Nplexer Bank, RF 경로
- **대량 작업**: CSV 내보내기
- **성능 최적화**: 페이지당 100개 항목 제한

**Access**: http://127.0.0.1:8000/admin/

---

### 3. Session Management (NEW) ⭐

**Features**:
- **세션 정렬**: Newest, Oldest, Name (A-Z)
- **세션 편집**: ✏️ 버튼으로 이름/설명 수정
- **세션 삭제**: 🗑️ 버튼으로 세션 및 파일 삭제
- **자동 날짜 표시**: "Just now", "2 hours ago", "Yesterday" 등

**API Endpoints**:
- `POST /rf-analyzer/session/update/<id>/` - 세션 이름/설명 업데이트
- `POST /rf-analyzer/session/delete/<id>/` - 세션 삭제

**Files**:
- `templates/rf_analyzer/index.html` - UI 및 JavaScript
- `views.py` - update_session(), delete_session()

---

### 4. Chart Export Options (NEW) ⭐

**File**: `templates/rf_analyzer/viewer.html`

**Supported Formats**:
- **PNG 300 DPI** - 표준 해상도
- **PNG 600 DPI** - 고해상도 (출판용)
- **SVG** - 벡터 포맷 (무한 확대)
- **PDF** - 단일 차트 PDF

**Implementation**:
```javascript
function exportChart(format, dpi) {
    if (format === 'png') {
        const scale = dpi / 72;
        Plotly.downloadImage(chartDiv, {
            format: 'png',
            width: 1920 * scale,
            height: 1200 * scale,
            filename: filename + `_${dpi}dpi`
        });
    } else if (format === 'svg') {
        Plotly.downloadImage(chartDiv, {format: 'svg', ...});
    } else if (format === 'pdf') {
        window.open(`/rf-analyzer/api/export-pdf/${sessionId}/?band=...`);
    }
}
```

---

### 5. Real-time Progress Tracking ⭐

**Feature**: Server-Sent Events (SSE) based progress tracking for Full Report PDF generation

**Key Features**:
- **Real-time Updates**: Progress bar with percentage, current item, elapsed time, ETA
- **Task Cancellation**: User can stop PDF generation mid-process
- **Automatic Download**: PDF downloads automatically on completion
- **Visual Feedback**: Modal dialog with smooth animations

**Components**:
1. **ProgressTracker** (`utils/progress_tracker.py`) - Cache-based state management
2. **SSE Endpoint** (`views.py::progress_stream`) - Streams JSON updates
3. **Cancel Endpoint** (`views.py::cancel_generation`) - Stop generation API
4. **Progress Modal** (`viewer.html`) - EventSource API integration

**See**: [docs/session-2025-10-10.md](docs/session-2025-10-10.md)

---

## 🚀 Development Workflow

### Starting a Session

```bash
cd C:\Project\html_exporter

# For Django development:
cd django_test
..\.venv\Scripts\python.exe manage.py runserver
```

### Admin Access

```bash
# Create superuser (if not exists)
cd django_test
python manage.py createsuperuser

# Access admin at: http://127.0.0.1:8000/admin/
```

---

## 📚 Key Documentation

**Essential Reading**:
1. [docs/csv-format-analysis.md](docs/csv-format-analysis.md) - CSV format specification
2. [docs/session-2025-10-10.md](docs/session-2025-10-10.md) - SSE progress tracking
3. [docs/actual-filename-format.md](docs/actual-filename-format.md) - Filename parsing
4. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Complete structure

---

## ⚠️ Known Issues

### Issue 1: Claude Code Edit Tool Bug
- **Problem**: "File has been unexpectedly modified" error on Windows
- **Cause**: Known bug in Claude Code v1.0.111 (GitHub #7443, #7457, #7883)
- **Workaround**: Use Bash commands (sed, cat, mv) for file modifications
- **Status**: ⚠️ Ongoing, use Bash for all file edits

### Issue 2: Django Admin Distinct Error
- **Problem**: `TypeError: Cannot create distinct fields once a slice has been taken`
- **Cause**: list_filter on MeasurementData with large datasets
- **Solution**: Removed list_filter, use search instead
- **Status**: ✅ Resolved

---

## 💡 Tips for Future Development

1. **Use Bash commands** for file modifications due to Edit tool bug
2. **Always test filename parser** with new file patterns
3. **Use prototype code** for data processing logic
4. **Keep grid structure** consistent across tabs
5. **Document** any new filename patterns
6. **Update** session logs for major changes

---

## ⏭️ Next Development Steps

### Immediate (Next Session)

1. **PPT 자동화 완성** (Phase 1.6)
   - 템플릿 PPT 업로드 기능
   - 426장 자동 생성 로직
   - 진행률 표시 (SSE 재사용)

2. **최종 테스트 및 문서화**
   - 전체 워크플로우 테스트
   - 사용자 가이드 작성
   - 배포 준비

---

## 📊 Recent Updates (2025-10-11)

### Session Management Enhancements
- ✅ Session name/description editing with ✏️ button
- ✅ Sorting by Newest, Oldest, Name (A-Z)
- ✅ AJAX-based updates without page reload
- ✅ Fixed sorting using data attributes

### Chart Export Options
- ✅ PNG export with 300 DPI and 600 DPI options
- ✅ SVG vector export for scalable graphics
- ✅ PDF export for single charts
- ✅ Bootstrap dropdown menu UI

### Admin Dashboard
- ✅ Full Django admin interface for all models
- ✅ Custom list displays with calculated fields
- ✅ Bulk actions (mark as parsed, CSV export)
- ✅ Search and filter capabilities
- ✅ Performance optimized for large datasets

---

**Last Session**: 2025-10-11 (2 hours)
**Next Session Priority**: PPT 자동화 완성 (Phase 1.6)
**Estimated Remaining Time**: 2-3 hours to full completion
**Project Progress**: 99% Complete
