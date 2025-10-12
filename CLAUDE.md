# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📊 Project Status

**Project**: RF S-parameter Analyzer for PA Module Testing
**Stage**: Active Development - PPT Automation Backend Complete
**Last Updated**: 2025-10-11 (Part 2)

### Current Progress
- **Phase 1 (Prototype)**: 100% ✅ Complete
- **Phase 1.5 (CSV Support + Grid Generation)**: 100% ✅ Complete
- **Phase 1.6 (PPT Automation)**: 95% 🚧 Backend complete, frontend JavaScript pending
- **Phase 2 (Django App)**: 99% ✅ All features complete
- **Overall**: ~99% Complete

---

## 🎯 Next Session Priority

**PPT Frontend JavaScript** (5 minutes):
- File: `viewer.html` line 395
- Replace: `alert('PPT export coming soon!')`
- Action: Copy PDF button code (line 257-392) and modify for PPT
- Details: See [docs/session-2025-10-11-part2.md](docs/session-2025-10-11-part2.md)

---

## 🔑 Key Components

### 1. PPT Automation (NEW - Phase 1.6) ⭐⭐⭐

**Status**: Backend 100% ✅ | Frontend 20% ⏸️

**Files**:
- `prototype/utils/ppt_generator.py` - Template layout auto-detection ✅
- `django_test/rf_analyzer/views.py` - export_full_report_ppt() ✅
- `django_test/rf_analyzer/urls.py` - API routing ✅
- `django_test/rf_analyzer/templates/rf_analyzer/viewer.html` - JavaScript pending ⏸️

**Key Features**:
- Template layout auto-detection ("Title and Content" priority)
- Placeholder auto-utilization (preserves company formatting)
- SSE progress tracking integration
- 426 slides auto-generation

**Next**: Add JavaScript to viewer.html (line 395)

**See**: [docs/session-2025-10-11-part2.md](docs/session-2025-10-11-part2.md)

---

### 2. Django Admin Dashboard ⭐

- Full CRUD interface for all models
- Custom list displays with calculated fields
- Bulk actions (CSV export, status changes)
- Performance optimized for large datasets

**Access**: http://127.0.0.1:8000/admin/

---

### 3. Session Management ⭐

- Session sorting (Newest, Oldest, Name)
- Edit session name/description with ✏️ button
- Delete sessions with 🗑️ button
- Relative time display

---

### 4. Chart Export Options ⭐

- PNG (300 DPI, 600 DPI)
- SVG (vector)
- PDF (single chart)
- Bootstrap dropdown menu

---

### 5. Real-time Progress Tracking ⭐

- SSE-based progress updates
- Task cancellation support
- Automatic download on completion
- Works for both PDF and PPT export

---

## 📚 Essential Documentation

1. **[docs/session-2025-10-11-part2.md](docs/session-2025-10-11-part2.md)** - ⭐ PPT automation details
2. **[docs/session-2025-10-10.md](docs/session-2025-10-10.md)** - SSE progress tracking
3. **[docs/csv-format-analysis.md](docs/csv-format-analysis.md)** - CSV format
4. **[docs/actual-filename-format.md](docs/actual-filename-format.md)** - Filename parsing

---

## ⚠️ Known Issues

### Issue 1: Claude Code Edit Tool Bug
- **Workaround**: Use Bash commands for file modifications
- **Status**: ⚠️ Ongoing

### Issue 2: viewer.html JavaScript Error
- **Problem**: Missing closing brace causes chart loading failure
- **Solution**: `git checkout` to restore
- **Status**: ✅ Resolved

---

## 🚀 Development Workflow

```bash
cd C:\Project\html_exporter\django_test
..\.venv\Scripts\python.exe manage.py runserver
```

**URL**: http://127.0.0.1:8000/rf-analyzer/

---

## 📊 Recent Updates (2025-10-11 Part 2)

### PPT Automation Backend (NEW)
- ✅ Template layout auto-detection in ppt_generator.py
- ✅ export_full_report_ppt() view with SSE progress
- ✅ URL routing: /api/export-full-report-ppt/
- ⏸️ Frontend JavaScript (5 min remaining)

### Session Management & Admin (Part 1)
- ✅ Session editing, sorting, deletion
- ✅ Chart export options (PNG/SVG/PDF)
- ✅ Full Django admin interface

---

**Last Session**: 2025-10-11 Part 2 (PPT Backend)
**Next Session**: viewer.html JavaScript (5 minutes)
**Project Progress**: 99% → 100% after frontend
