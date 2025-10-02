# RF S-parameter Analyzer

PA 모듈 S-parameter 측정 데이터 분석 및 시각화 도구

## 프로젝트 개요

Network Analyzer로 측정한 SnP 파일에서 Gain 데이터를 추출하고, 다양한 Band/CA 조건을 그리드 레이아웃으로 비교 분석하는 웹 기반 도구입니다.

**개발 단계**: Phase 1 - 프로토타입

## 주요 기능

- ✅ SnP (Touchstone) 파일 파싱
- ✅ S21 (Gain) 데이터 자동 추출
- ✅ 인터랙티브 차트 생성 (Plotly)
- ✅ 그리드 레이아웃 비교 시각화
- 🚧 Django 웹 앱 통합 (Phase 2)
- 🚧 PDF Export (Phase 2)

## 프로젝트 구조

```
html_exporter/
├── docs/                          # 프로젝트 문서
│   ├── project-discussion.md      # 프로젝트 정의 및 대화 기록
│   └── tech-stack-decision.md     # 기술 스택 결정 문서
├── prototype/                     # Phase 1 프로토타입
│   ├── parsers/                   # SnP/CSV 파서
│   │   ├── snp_parser.py
│   │   └── csv_parser.py
│   ├── utils/                     # 유틸리티
│   │   ├── sparameter.py          # S-parameter 분석
│   │   └── chart_generator.py     # Plotly 차트 생성
│   ├── tests/                     # 테스트 코드
│   └── main.py                    # 메인 스크립트
├── requirements.txt               # Python 의존성
└── README.md
```

## 설치 및 실행

### 1. 개발 환경 구축

```bash
# Python 3.11 필요
python --version  # 3.11 확인

# 가상환경 생성 (Windows)
python -m venv venv
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 데모 실행

```bash
# 샘플 데이터로 차트 생성
cd prototype
python main.py

# 생성된 파일:
# - demo_single.html      (단일 차트)
# - demo_comparison.html  (비교 차트)
# - demo_grid.html        (그리드 레이아웃)
```

### 3. SnP 파일 분석

```bash
# SnP 파일 분석 (예시)
python main.py --input path/to/file.s10p --output result.html

# 포트 지정
python main.py --input file.s10p --port-in 1 --port-out 2
```

## 사용 예시

### Python API

```python
from parsers.snp_parser import SnpParser
from utils.chart_generator import ChartGenerator

# SnP 파일 파싱
parser = SnpParser('sample.s10p')
parser.load()

# Gain 추출 (S21)
freq, gain = parser.get_gain(input_port=1, output_port=2)

# 차트 생성
fig = ChartGenerator.create_single_chart(
    freq=freq/1e9,  # Hz → GHz
    gain=gain,
    title="B1 Band Gain"
)

# HTML 저장
ChartGenerator.export_to_html(fig, 'output.html', auto_open=True)
```

## 다음 단계

### Phase 2: Django 앱 통합 (예정)
- [ ] Django 앱 구조 생성
- [ ] HTMX 파일 업로드 UI
- [ ] 사용자 인증 연동
- [ ] 측정 이력 저장 (DB)
- [ ] PDF Export 기능

### Phase 3: 고급 기능 (예정)
- [ ] S11/S22 지원
- [ ] 파일명 자동 파싱
- [ ] 차트 프리셋 저장

## 기술 스택

- **Python**: 3.11
- **RF Library**: scikit-rf
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Future**: Django 5.x + HTMX

## 문서

자세한 내용은 [docs/](docs/) 폴더 참조:
- [프로젝트 논의 기록](docs/project-discussion.md)
- [기술 스택 결정](docs/tech-stack-decision.md)

## 라이선스

Internal Use Only (회사 내부용)

## 작성자

RF Engineering Team
