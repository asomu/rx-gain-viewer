# Quick Start Guide

RF S-parameter Analyzer 빠른 시작 가이드

## 📋 필수 요구사항

- **Python**: 3.11 이상 (3.12 권장)
- **uv**: 빠른 패키지 관리자 (선택적)

## 🚀 설치 및 실행

### 1. 저장소 클론 (또는 다운로드)

```bash
cd C:\Project\html_exporter
```

### 2. 개발 환경 구축

#### Option A: uv 사용 (추천 ⚡)

```bash
# 가상환경 생성
uv venv

# 의존성 설치
uv pip install scikit-rf pandas numpy plotly
```

#### Option B: pip 사용

```bash
# 가상환경 생성
python -m venv venv
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 데모 실행

```bash
cd prototype
python main.py
```

**생성되는 파일**:
- `demo_single.html` - 단일 Gain 차트
- `demo_comparison.html` - CA 조건 비교 차트
- `demo_grid.html` - 2×3 그리드 레이아웃 (자동으로 브라우저 열림)

---

## 📊 SnP 파일 분석

실제 SnP 파일을 분석하려면:

```bash
python main.py --input your_file.s10p --output result.html
```

**옵션**:
- `--input, -i`: SnP 파일 경로
- `--output, -o`: 출력 HTML 파일명 (기본: output.html)
- `--port-in`: 입력 포트 번호 (기본: 1)
- `--port-out`: 출력 포트 번호 (기본: 2)

**예시**:
```bash
# S21 Gain 분석 (Port 1 → Port 2)
python main.py -i B1_RxOut1.s10p -o B1_gain.html

# S32 분석 (Port 2 → Port 3)
python main.py -i test.s12p --port-in 2 --port-out 3 -o s32_gain.html
```

---

## 🐍 Python API 사용

### 기본 사용법

```python
from parsers.snp_parser import SnpParser
from utils.sparameter import SParameterAnalyzer
from utils.chart_generator import ChartGenerator

# 1. SnP 파일 파싱
parser = SnpParser('sample.s10p')
parser.load()

# 2. Gain 데이터 추출 (S21)
freq, gain = parser.get_gain(input_port=1, output_port=2)

# 3. 주파수 단위 변환 (Hz → GHz)
freq_ghz = SParameterAnalyzer.convert_frequency_unit(freq, 'Hz', 'GHz')

# 4. 차트 생성
fig = ChartGenerator.create_single_chart(
    freq=freq_ghz,
    gain=gain,
    title="B1 Band Gain Analysis"
)

# 5. HTML 저장
ChartGenerator.export_to_html(fig, 'my_chart.html', auto_open=True)
```

### 비교 차트 생성

```python
# 여러 조건 비교
data_list = [
    {'freq': freq1_ghz, 'gain': gain1, 'label': 'B1 Only', 'color': 'blue'},
    {'freq': freq2_ghz, 'gain': gain2, 'label': 'B1_B3', 'color': 'red'},
    {'freq': freq3_ghz, 'gain': gain3, 'label': 'B1_B41', 'color': 'green'}
]

fig = ChartGenerator.create_comparison_chart(
    data_list=data_list,
    title="CA Condition Comparison"
)

ChartGenerator.export_to_html(fig, 'comparison.html')
```

### 그리드 레이아웃

```python
# 2x3 그리드 (RxOut1/2 × B1/B1_B3/B1_B41)
data_grid = [
    [  # RxOut1 행
        {'freq': f_b1, 'gain': g_b1, 'label': 'RxOut1-B1'},
        {'freq': f_b1b3, 'gain': g_b1b3, 'label': 'RxOut1-B1_B3'},
        {'freq': f_b1b41, 'gain': g_b1b41, 'label': 'RxOut1-B1_B41'}
    ],
    [  # RxOut2 행
        {'freq': f2_b1, 'gain': g2_b1, 'label': 'RxOut2-B1'},
        {'freq': f2_b1b3, 'gain': g2_b1b3, 'label': 'RxOut2-B1_B3'},
        {'freq': f2_b1b41, 'gain': g2_b1b41, 'label': 'RxOut2-B1_B41'}
    ]
]

fig = ChartGenerator.create_grid_layout(
    data_grid=data_grid,
    row_labels=['RxOut1', 'RxOut2'],
    col_labels=['B1', 'B1_B3', 'B1_B41'],
    title="Comprehensive Gain Analysis"
)

ChartGenerator.export_to_html(fig, 'grid.html')
```

---

## 🔧 고급 기능

### S11/S22 (Return Loss) 분석

```python
# Return Loss 추출
freq, s11_db = parser.get_return_loss(port=1)

fig = ChartGenerator.create_single_chart(
    freq=freq/1e9,
    gain=s11_db,
    title="S11 Return Loss",
    ylabel="S11 (dB)"
)
```

### 통계 정보

```python
# Gain 통계 계산
stats = SParameterAnalyzer.calculate_gain_statistics(gain)
print(f"Mean: {stats['mean']:.2f} dB")
print(f"Max: {stats['max']:.2f} dB")
print(f"Min: {stats['min']:.2f} dB")
```

### Band 자동 감지

```python
# 주파수에서 Band 자동 감지
band = SParameterAnalyzer.detect_band_from_frequency(freq)
print(f"Detected Band: {band}")  # 예: 'B1'
```

---

## 📁 프로젝트 구조

```
prototype/
├── parsers/
│   ├── snp_parser.py      # SnP 파일 파싱
│   └── csv_parser.py      # CSV 파일 파싱
├── utils/
│   ├── sparameter.py      # S-parameter 분석 도구
│   └── chart_generator.py # Plotly 차트 생성
├── tests/
│   └── sample_data/       # 테스트용 SnP 파일
└── main.py                # CLI 실행 스크립트
```

---

## 🐛 문제 해결

### ImportError: scikit-rf not found

```bash
uv pip install scikit-rf
```

### UnicodeEncodeError 발생 시

한글 출력 문제는 main.py에서 영문으로 변경됨 (이미 해결됨)

### 차트가 열리지 않을 때

```python
# auto_open=False로 설정
ChartGenerator.export_to_html(fig, 'output.html', auto_open=False)

# 수동으로 HTML 파일 열기
import webbrowser
webbrowser.open('output.html')
```

---

## 📝 다음 단계

1. **실제 SnP 파일로 테스트**
   - 회사 측정 데이터로 검증
   - 파일명 파싱 규칙 정의

2. **Django 앱 통합 준비**
   - HTMX 파일 업로드 UI 개발
   - 사용자 인증 연동
   - 측정 이력 저장

3. **고급 기능 추가**
   - PDF Export
   - 자동 Band/CA/Port 감지
   - 차트 프리셋 저장

---

## 📞 문의

RF Engineering Team
