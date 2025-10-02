# 기술 스택 및 아키텍처 결정

**날짜**: 2025-10-02
**프로젝트**: RF S-parameter Analyzer

---

## 🎯 최종 결정: Python + Django 통합 전략

### **Phase 1: 프로토타입 (현재 폴더)**
독립적인 Python 스크립트로 핵심 기능 검증

### **Phase 2: Django 앱 통합**
검증된 코드를 기존 Django 프로젝트에 앱으로 통합

---

## 💻 기술 스택

### **Backend**
| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.11 | 기존 Django 프로젝트와 동일 |
| Django | 5.x | 웹 프레임워크, 인증, ORM |
| scikit-rf | 0.29+ | SnP(Touchstone) 파일 파싱 |
| Pandas | 2.1+ | 데이터 처리 및 변환 |
| NumPy | 1.25+ | 수치 계산 |

### **Frontend**
| 기술 | 용도 |
|------|------|
| HTMX | 기존 프로젝트 스타일 유지, 동적 UI |
| Plotly.js | 인터랙티브 차트 생성 |
| Alpine.js | 경량 JavaScript (선택적) |
| Tailwind CSS | 스타일링 (기존 프로젝트와 통일) |

### **파일 처리 & Export**
| 기술 | 용도 |
|------|------|
| WeasyPrint | HTML → PDF 변환 |
| Pillow | 이미지 처리 (선택적) |

### **배포**
| 기술 | 용도 |
|------|------|
| 기존 Django 인프라 | 인트라넷 배포 |
| PostgreSQL/SQLite | 측정 이력 저장 |

---

## 🏗️ 아키텍처 설계

### **Phase 1: 프로토타입 구조**

```
html_exporter/
├── docs/
│   ├── project-discussion.md
│   └── tech-stack-decision.md
├── prototype/
│   ├── __init__.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── snp_parser.py      # scikit-rf 기반 SnP 파싱
│   │   └── csv_parser.py       # CSV 파일 파싱
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── sparameter.py       # S-parameter 추출/계산
│   │   └── chart_generator.py  # Plotly 차트 생성
│   ├── tests/
│   │   ├── test_snp_parser.py
│   │   └── sample_data/        # 테스트용 SnP 파일
│   ├── main.py                 # 프로토타입 메인 스크립트
│   └── demo.html               # 차트 출력 예시
├── requirements.txt
└── README.md
```

### **Phase 2: Django 앱 구조**

```
your-django-project/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── manual_pages/           # 기존 HTMX 매뉴얼 앱
└── rf_analyzer/            # 새 앱 ✨
    ├── __init__.py
    ├── models.py           # 측정 세션, 파일 이력
    ├── views.py            # HTMX 뷰
    ├── urls.py
    ├── forms.py            # 파일 업로드 폼
    ├── admin.py            # Django Admin 설정
    ├── parsers/            # Phase 1에서 복사
    │   ├── snp_parser.py
    │   └── csv_parser.py
    ├── utils/              # Phase 1에서 복사
    │   ├── sparameter.py
    │   └── chart_generator.py
    ├── static/rf_analyzer/
    │   ├── css/
    │   │   └── charts.css
    │   └── js/
    │       └── chart-interactions.js
    ├── templates/rf_analyzer/
    │   ├── base.html       # 기존 프로젝트 base 상속
    │   ├── index.html      # 메인 페이지
    │   ├── upload.html     # 파일 업로드 (HTMX)
    │   ├── partials/       # HTMX 부분 템플릿
    │   │   ├── chart-grid.html
    │   │   └── tab-navigation.html
    │   └── charts.html     # 차트 표시
    └── migrations/
```

---

## 🎨 HTMX 통합 전략

### **HTMX의 장점**
- ✅ 기존 프로젝트와 일관된 UX
- ✅ JavaScript 최소화
- ✅ 서버 사이드 렌더링 + 동적 업데이트
- ✅ 파일 업로드 & 차트 렌더링에 최적

### **주요 패턴**

#### 1. 파일 업로드 (HTMX)
```html
<!-- templates/rf_analyzer/upload.html -->
<form hx-post="/rf-analyzer/upload/"
      hx-target="#chart-container"
      hx-encoding="multipart/form-data">
    <input type="file" name="snp_files" multiple accept=".snp,.s10p,.s12p">
    <button type="submit">Analyze</button>
</form>

<div id="chart-container">
    <!-- 차트가 여기에 동적으로 로드됨 -->
</div>
```

#### 2. 탭 네비게이션 (HTMX)
```html
<!-- templates/rf_analyzer/partials/tab-navigation.html -->
<div class="tabs">
    <button hx-get="/rf-analyzer/band/B1/"
            hx-target="#chart-grid">
        B1 CA Cases
    </button>
    <button hx-get="/rf-analyzer/band/B3/"
            hx-target="#chart-grid">
        B3 CA Cases
    </button>
</div>

<div id="chart-grid">
    <!-- 그리드 차트가 여기에 로드됨 -->
</div>
```

#### 3. Django View (HTMX 응답)
```python
# rf_analyzer/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('snp_files')

        # 파일 파싱 및 차트 생성
        charts_data = process_files(files)

        # HTMX partial 템플릿 반환
        return render(request, 'rf_analyzer/partials/chart-grid.html', {
            'charts': charts_data
        })

    return render(request, 'rf_analyzer/upload.html')
```

---

## 💾 데이터 모델 설계

### **Django Models**

```python
# rf_analyzer/models.py
from django.db import models
from django.contrib.auth.models import User

class MeasurementSession(models.Model):
    """측정 세션 (한 번의 분석 작업)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, help_text="세션 이름")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class MeasurementFile(models.Model):
    """업로드된 SnP 파일"""
    session = models.ForeignKey(MeasurementSession, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='measurements/%Y/%m/%d/')
    filename = models.CharField(max_length=255)

    # 메타데이터
    band = models.CharField(max_length=50, blank=True)  # B1, B3, B41
    ca_condition = models.CharField(max_length=100, blank=True)  # B1_B3
    port_config = models.CharField(max_length=100, blank=True)  # RxOut1

    # 분석 결과 캐싱 (선택적)
    gain_min = models.FloatField(null=True, blank=True)
    gain_max = models.FloatField(null=True, blank=True)
    freq_start = models.FloatField(null=True, blank=True)
    freq_end = models.FloatField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

class ChartPreset(models.Model):
    """자주 사용하는 차트 설정 저장"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    # 그리드 설정
    grid_rows = models.JSONField()  # ['RxOut1', 'RxOut2', 'RxOut3', 'RxOut4']
    grid_cols = models.JSONField()  # ['B1', 'B1_B3', 'B1_B41']

    # 차트 옵션
    chart_options = models.JSONField(blank=True, default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
```

---

## 📦 Dependencies

### **requirements.txt**

```txt
# Django
Django>=5.0,<6.0
django-htmx>=1.17.0

# RF Processing
scikit-rf>=0.29.0
pandas>=2.1.0
numpy>=1.25.0

# Visualization
plotly>=5.17.0

# PDF Export
weasyprint>=60.0

# Development
pytest>=7.4.0
pytest-django>=4.5.0
black>=23.9.0
ruff>=0.0.292

# Optional: Production
gunicorn>=21.2.0
```

---

## 🚀 개발 로드맵

### **Week 1-2: 프로토타입**
- [x] 프로젝트 기획 완료
- [ ] 개발 환경 설정
- [ ] SnP 파서 구현 (scikit-rf)
- [ ] 단일 차트 생성 (Plotly)
- [ ] 샘플 데이터 테스트

### **Week 3: 그리드 레이아웃**
- [ ] 다중 파일 처리
- [ ] 그리드 레이아웃 알고리즘
- [ ] HTML 출력 템플릿

### **Week 4: Django 통합 준비**
- [ ] 프로토타입 코드 정리
- [ ] Django 앱 구조 생성
- [ ] 코드 마이그레이션

### **Week 5: Django 기능 구현**
- [ ] HTMX 파일 업로드
- [ ] 사용자 인증 연동
- [ ] 데이터 모델 마이그레이션

### **Week 6: 고급 기능**
- [ ] 탭 네비게이션
- [ ] PDF Export
- [ ] 측정 이력 관리

### **Week 7: 테스트 & 배포**
- [ ] 통합 테스트
- [ ] 사용자 피드백
- [ ] 인트라넷 배포

---

## 🔄 Django 통합 체크리스트

### **준비 사항**
- [ ] 기존 Django 프로젝트 백업
- [ ] 새 브랜치 생성 (`git checkout -b rf-analyzer`)
- [ ] 의존성 패키지 설치 테스트

### **앱 생성**
- [ ] `python manage.py startapp rf_analyzer`
- [ ] `INSTALLED_APPS`에 추가
- [ ] URL 라우팅 설정

### **코드 이식**
- [ ] 파서 코드 복사
- [ ] Django 뷰로 변환
- [ ] 템플릿 생성 (HTMX 패턴)
- [ ] 정적 파일 설정

### **데이터베이스**
- [ ] 모델 정의
- [ ] 마이그레이션 생성 및 적용
- [ ] Admin 인터페이스 설정

### **인증 & 권한**
- [ ] 로그인 필수 설정
- [ ] 권한 그룹 생성 (RF Engineers)
- [ ] 사용자별 세션 분리

### **테스트**
- [ ] 단위 테스트 작성
- [ ] HTMX 동작 테스트
- [ ] 파일 업로드 테스트
- [ ] PDF Export 테스트

---

## 💡 HTMX + Plotly 통합 팁

### **서버 사이드 차트 생성**
```python
# rf_analyzer/utils/chart_generator.py
import plotly.graph_objects as go
import plotly.io as pio

def create_gain_chart(freq, gain, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=freq,
        y=gain,
        mode='lines',
        name='Gain'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Frequency (GHz)',
        yaxis_title='Gain (dB)',
        hovermode='x unified'
    )

    # HTML div로 변환 (HTMX 응답용)
    return pio.to_html(fig, include_plotlyjs='cdn', div_id=f'chart-{title}')
```

### **HTMX로 동적 로딩**
```html
<!-- 로딩 인디케이터 -->
<div hx-post="/rf-analyzer/upload/"
     hx-indicator="#loading">
    <button>Analyze</button>
</div>

<div id="loading" class="htmx-indicator">
    Processing...
</div>
```

---

## 🎯 성공 지표

### **Phase 1 완료 조건**
- ✅ SnP 파일 파싱 성공률 100%
- ✅ 단일 차트 생성 시간 < 1초
- ✅ 그리드 레이아웃 (4×3) 생성 시간 < 5초

### **Phase 2 완료 조건**
- ✅ Django 앱 통합 완료
- ✅ HTMX 파일 업로드 동작
- ✅ 사용자 인증 연동
- ✅ 측정 이력 저장 기능

### **최종 목표**
- ✅ 10명 사용자 동시 사용 가능
- ✅ 160개 파일 분석 시간 < 30초
- ✅ PDF Export 시간 < 10초
- ✅ 인트라넷 배포 완료
