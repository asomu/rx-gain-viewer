# RF S-parameter Analyzer - 프로젝트 구조

**작성일**: 2025-10-03 00:30

---

## 📁 전체 프로젝트 구조

```
html_exporter/
│
├── 📄 README.md                    # 프로젝트 개요
├── 📄 CLAUDE.md                    # Claude Code 가이드
├── 📄 requirements.txt             # Python 의존성 (pip)
├── 📄 pyproject.toml               # uv 프로젝트 설정
├── 📄 .gitignore                   # Git 제외 파일
│
├── 📁 docs/                        # 📚 프로젝트 문서
│   ├── project-discussion.md       # 프로젝트 정의 및 대화 기록
│   ├── tech-stack-decision.md      # 기술 스택 상세 문서
│   ├── quickstart.md               # 빠른 시작 가이드
│   ├── filename-rules.md           # 파일명 규칙 (일반)
│   └── actual-filename-format.md   # 실제 파일명 분석 ⭐
│
├── 📁 prototype/                   # ✅ Phase 1: 프로토타입
│   ├── __init__.py
│   ├── main.py                     # CLI 실행 스크립트
│   │
│   ├── parsers/                    # SnP/CSV 파서
│   │   ├── __init__.py
│   │   ├── snp_parser.py           # scikit-rf 기반
│   │   └── csv_parser.py
│   │
│   ├── utils/                      # 분석 & 차트 유틸
│   │   ├── __init__.py
│   │   ├── sparameter.py           # S-parameter 분석
│   │   └── chart_generator.py      # Plotly 차트
│   │
│   ├── tests/                      # 테스트
│   │   └── sample_data/            # 샘플 SnP 파일
│   │
│   └── 🌐 demo_*.html              # 생성된 데모 차트 (3개)
│
├── 📁 django_test/                 # 🚧 Phase 2: Django 웹 앱
│   ├── manage.py                   # Django 관리 스크립트
│   │
│   ├── config/                     # Django 프로젝트 설정
│   │   ├── __init__.py
│   │   ├── settings.py             # ✅ 설정 완료 (HTMX, rf_analyzer 추가)
│   │   ├── urls.py                 # ✅ URL 라우팅 완료
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── rf_analyzer/                # 📱 RF Analyzer 앱 ⭐
│       ├── __init__.py
│       ├── apps.py
│       ├── admin.py                # ⏳ TODO: Admin 인터페이스
│       ├── models.py               # ✅ Models 완료
│       ├── views.py                # ⏳ TODO: Views
│       ├── urls.py                 # ⏳ TODO: URL 패턴
│       ├── tests.py
│       │
│       ├── filename_parser.py      # ✅ 복잡한 파일명 파서
│       │
│       ├── templates/              # ⏳ TODO: HTMX 템플릿
│       │   └── rf_analyzer/
│       │       ├── base.html
│       │       ├── upload.html
│       │       └── partials/
│       │
│       ├── static/                 # ⏳ TODO: 정적 파일
│       │   └── rf_analyzer/
│       │       ├── css/
│       │       └── js/
│       │
│       └── migrations/             # ⏳ TODO: 마이그레이션 실행
│           └── __init__.py
│
└── 📁 .venv/                       # uv 가상환경
    └── (scikit-rf, pandas, numpy, plotly, Django, django-htmx)
```

---

## 🎯 현재 상태

### ✅ 완료된 작업

#### **Phase 1: 프로토타입** (100% 완료)
- [x] 프로젝트 구조 생성
- [x] SnP 파서 구현 (scikit-rf)
- [x] CSV 파서 구현
- [x] S-parameter 분석 유틸 (주파수 변환, 통계 등)
- [x] Plotly 차트 생성기 (단일, 비교, 그리드)
- [x] 데모 스크립트 실행 성공
- [x] HTML 출력 검증 (3개 파일)

#### **Phase 2: Django 앱** (40% 완료)
- [x] Django 5.2 + HTMX 설치
- [x] 테스트 프로젝트 생성 (`django_test/`)
- [x] rf_analyzer 앱 생성
- [x] Settings.py 설정 (HTMX, MEDIA, STATIC)
- [x] URL 라우팅 설정
- [x] **복잡한 파일명 파서 구현** ⭐
  - 정규식 패턴 완성
  - 파싱 로직 완성 및 테스트
  - 파일 조직화 로직
- [x] Django Models 정의
  - MeasurementSession (측정 세션)
  - MeasurementFile (업로드 파일)

---

### ⏳ 다음 작업 (남은 60%)

#### **즉시 다음 단계** (1-2시간)
- [ ] 마이그레이션 실행 (`python manage.py migrate`)
- [ ] Admin 인터페이스 등록
- [ ] rf_analyzer/urls.py 생성
- [ ] 파일 업로드 View 구현
- [ ] 기본 템플릿 구조 (base.html)

#### **핵심 기능 구현** (3-4시간)
- [ ] HTMX 파일 업로드 UI
- [ ] 파일명 자동 파싱 & 미리보기
- [ ] 그리드 구조 표시 (탭별)
- [ ] 프로토타입 차트 생성 코드 통합
- [ ] 차트 표시 (HTMX partial)

#### **고급 기능** (선택, 2-3시간)
- [ ] 사용자 인증 연동
- [ ] 측정 이력 저장
- [ ] PDF Export
- [ ] 프리셋 기능

---

## 📊 핵심 컴포넌트 분석

### **1. 복잡한 파일명 파서** ⭐

**파일**: `django_test/rf_analyzer/filename_parser.py`

**입력 예시**:
```
B1[B7]@MHBIN1_ANTU&ANT1&ANT2_X@MIMO_X@TRX_B3[B7]@1_B41S@2_(G0H).s9p
```

**파싱 결과**:
```python
{
    'main_band': 'B1',                      # 탭 구분
    'input_port': 'MHBIN1',
    'output_port': 'ANTU_ANT1_ANT2',
    'port_label': 'MHBIN1→ANTU_ANT1_ANT2',  # 행 레이블
    'ca_bands': ['B3_B7', 'B41'],
    'ca_label': 'B3_B7_B41',                # 열 레이블
    'condition': 'G0H',
    'is_valid': True
}
```

**조직화 기능**:
```python
ComplexFilenameParser.organize_files(uploaded_files)

# 반환:
{
    'B1': {
        'ca_conditions': ['B3_B7_B41', 'B3_B7_B7'],
        'ports': ['MHBIN1→ANTU_ANT1_ANT2', ...],
        'matrix': {
            'MHBIN1→ANTU_ANT1_ANT2': {
                'B3_B7_B41': file_object,
                ...
            }
        },
        'file_count': 12,
        'missing_cells': ['B3_B7_B41 × MHBIN2→...']
    }
}
```

---

### **2. Django Models**

**파일**: `django_test/rf_analyzer/models.py`

#### **MeasurementSession**
- 한 번의 분석 작업
- 사용자별 세션 관리
- JSON 그리드 설정 저장

#### **MeasurementFile**
- 업로드된 SnP 파일
- 파싱된 메타데이터 저장 (Band, CA, Port)
- 파일별 상태 관리 (is_parsed)

---

### **3. 프로토타입 차트 생성기**

**파일**: `prototype/utils/chart_generator.py`

**기능**:
- `create_single_chart()` - 단일 Gain 차트
- `create_comparison_chart()` - 오버레이 비교
- `create_grid_layout()` - NxM 그리드 레이아웃 ⭐
- `export_to_html()` - HTML 저장

**Django 통합 계획**:
```python
# Django View에서 사용
from prototype.utils.chart_generator import ChartGenerator

def generate_chart_view(request):
    # ... 파일 파싱 ...
    fig = ChartGenerator.create_grid_layout(...)
    chart_html = fig.to_html(include_plotlyjs='cdn')
    return render(request, 'rf_analyzer/partials/chart.html', {
        'chart': chart_html
    })
```

---

## 🔗 데이터 흐름

```
[사용자]
    ↓
[Django Web UI]
    ↓ (파일 업로드 - HTMX)
[rf_analyzer/views.py]
    ↓
[ComplexFilenameParser.organize_files()]
    ↓ (파싱된 그리드 구조)
[미리보기 표시 - HTMX partial]
    ↓ (분석 시작 버튼)
[prototype/parsers/snp_parser.py]
    ↓ (S-parameter 추출)
[prototype/utils/chart_generator.py]
    ↓ (Plotly 그리드 차트 생성)
[HTMX partial 업데이트]
    ↓
[사용자에게 인터랙티브 차트 표시]
```

---

## 🛠️ 기술 스택 요약

### **Backend**
- Python 3.12
- Django 5.2
- scikit-rf (SnP 파싱)
- Pandas, NumPy (데이터 처리)

### **Frontend**
- HTMX (동적 UI)
- Plotly.js (인터랙티브 차트)
- Alpine.js (선택적)
- Tailwind CSS (예정)

### **Dev Tools**
- uv (패키지 관리) ⚡
- pytest (테스트)
- black, ruff (코드 품질)

---

## 📈 다음 세션 시작 가이드

**프로젝트 재시작 시**:
```bash
cd C:\Project\html_exporter

# 1. 가상환경 활성화 (필요시)
# .venv\Scripts\activate

# 2. Django 개발 서버 실행
cd django_test
..\.venv\Scripts\python.exe manage.py runserver

# 3. 브라우저에서 확인
# http://localhost:8000/rf-analyzer/
```

**현재 작업 위치**: `django_test/rf_analyzer/`

**다음 작업**:
1. 마이그레이션 실행
2. Views.py 구현
3. Templates 생성
4. HTMX 파일 업로드 UI

---

## 💡 주요 의사결정 기록

1. **파일명 규칙**: 실제 측정 프로그램 형식 분석 완료
   - 복잡한 패턴: `B1[B7]@MHBIN1_ANTU&ANT1&ANT2_...`
   - 정규식 파서 구현 완료

2. **하이브리드 UI 방식**: 자동 파싱 + 수동 조정
   - 1차: 파일명 자동 파싱
   - 2차: 사용자 확인 및 수정

3. **테스트 프로젝트**: 실제 Django 프로젝트 통합 전 검증
   - `django_test/` → 나중에 실제 프로젝트로 복사

4. **프로토타입 재사용**: 차트 생성 로직 그대로 활용
   - `prototype/` 코드를 Django에서 import

---

**마지막 업데이트**: 2025-10-03 00:30
