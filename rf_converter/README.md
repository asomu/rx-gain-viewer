# RF SnP to CSV Converter

RF S-parameter 측정 데이터를 CSV 형식으로 변환하는 도구

---

## 📋 프로젝트 개요

**목적**: RF 측정 엔지니어가 Network Analyzer(NA)에서 측정한 SnP 파일을 Bellagio CSV 형식으로 쉽게 변환

**대상 사용자**: RF 측정 엔지니어 (소프트웨어 비전문가)

**주요 특징**:
- ✅ s1p ~ s12p 파일 지원 (1-port ~ 12-port S-parameters)
- ✅ 파일명 자동 파싱 (Band, LNA, Port 자동 추출)
- ✅ 대역별 주파수 필터링
- ✅ 드래그&드롭 UI
- ✅ 실시간 진행률 표시
- ✅ 모듈형 아키텍처 (다중 UI 지원)
- ✅ 100% 한글 사용자 매뉴얼

---

## 🚀 빠른 시작

### 1. 가상환경 활성화
```bash
cd C:\Project\html_exporter
.venv\Scripts\activate
```

### 2. 의존성 설치 (최초 1회)
```bash
pip install pandas numpy PyQt6
```

### 3. GUI 실행
```bash
cd rf_converter\ui_pyqt6
set PYTHONPATH=..
python main.py
```

또는 `run_gui.bat` 실행

---

## 📁 프로젝트 구조

```
rf_converter/
│
├── core/                              # 핵심 비즈니스 로직 (UI 독립)
│   ├── models/                       # 데이터 모델
│   │   └── conversion_result.py
│   ├── parsers/                      # SnP 파일 파서
│   │   ├── base_parser.py           # 추상 클래스
│   │   ├── snp_reader.py            # SnP 리더 (s1p~s12p)
│   │   └── rx_parser.py             # Rx Gain 구현
│   ├── converters/                   # CSV 변환기
│   │   └── csv_writer.py
│   └── services/                     # 변환 서비스
│       └── conversion_service.py
│
├── ui_pyqt6/                          # PyQt6 데스크톱 UI
│   ├── main.py                       # 앱 진입점
│   ├── main_window.py                # 메인 윈도우
│   ├── widgets/                      # UI 위젯
│   │   ├── file_selector.py         # 파일 선택
│   │   └── progress_widget.py       # 진행률 표시
│   ├── run_gui.bat                   # 실행 스크립트
│   └── 테스트_가이드.md               # 테스트 매뉴얼
│
├── docs/                              # 문서
│   ├── 사용자_매뉴얼.md               # 한글 매뉴얼 (메인)
│   ├── USER_MANUAL.md                # 영문 매뉴얼
│   └── 세션-2025-10-26-pyqt6-ui-완성.md  # 개발 세션 로그
│
├── tests/                             # 테스트
│   └── test_core_simple.py           # Core 단위 테스트
│
└── test_data/                         # 테스트 데이터
    └── snp_files/                    # 샘플 SnP 파일
```

---

## 🎯 주요 기능

### 1. Core 모듈 (100% UI 독립)

**SnP 파일 읽기**:
- Touchstone 형식 지원 (s1p ~ s12p)
- 주파수 단위: Hz, KHz, MHz, GHz
- 데이터 형식: MA (magnitude/angle), RI (real/imaginary), DB (dB/angle)
- 자동 Real/Imaginary 변환

**파일명 파싱**:
```
X_ANT1_B1@1_(G0H).s2p
  ↓
Band: B1
Port In: ANT1
Port Out: RXOUT1 (자동 추론)
LNA State: G0_H
```

**RF 메트릭 계산**:
- Gain (dB) = 20*log10(|S21|)
- Reverse (dB) = 20*log10(|S12|)
- Input RL (dB) = -20*log10(|S11|)
- Output RL (dB) = -20*log10(|S22|)

**주파수 필터링**:
- 대역별 자동 필터링 (예: B1 → 2110-2170 MHz)
- 파일명에서 자동 대역 감지

### 2. PyQt6 Desktop UI

**파일 선택**:
- 드래그&드롭 폴더 선택
- Browse Folders 버튼
- s1p ~ s12p 자동 감지
- 대소문자 구분 없음

**변환 프로세스**:
- QThread 기반 비동기 처리 (UI 프리징 방지)
- 실시간 진행률 표시
- 파일별 처리 상태 업데이트

**결과 표시**:
- 항상 표시되는 결과 섹션 (레이아웃 안정성)
- 3가지 상태 관리 (Empty/Converting/Complete)
- 변환 통계 (파일 수, 행 수, 파일 크기, 성공률)
- 에러 상세 표시 (최대 5개)

**후처리**:
- Open CSV: 기본 프로그램으로 열기
- Open Folder: 출력 폴더 열기
- Convert More: UI 리셋

---

## 🎨 UI/UX 설계 원칙

### 1. 예측 가능한 레이아웃
- 결과 섹션 항상 표시 (setVisible 사용 안 함)
- 레이아웃 점프 없음
- 플레이스홀더로 빈 상태 표시

### 2. 명확한 상태 관리
- **Empty**: "Ready to Convert" (회색), 버튼 비활성화
- **Converting**: "Converting..." (파란색), 버튼 비활성화
- **Complete**: "✅ Conversion Successful!" (초록색), 버튼 활성화

### 3. 화면 크기 최적화
- 윈도우 높이: 850px (1080p 화면에 최적)
- QScrollArea로 내용 넘침 방지
- 최소/최대 크기 제한

### 4. 비전문가 친화적
- 드래그&드롭 직관적 UI
- 한글 메시지 및 매뉴얼
- EXE 파일 배포 계획

---

## 📚 문서

- **[사용자_매뉴얼.md](docs/사용자_매뉴얼.md)**: 최종 사용자용 한글 매뉴얼
- **[USER_MANUAL.md](docs/USER_MANUAL.md)**: 영문 매뉴얼
- **[테스트_가이드.md](ui_pyqt6/테스트_가이드.md)**: 개발자용 테스트 절차
- **[세션-2025-10-26-pyqt6-ui-완성.md](docs/세션-2025-10-26-pyqt6-ui-완성.md)**: 개발 세션 로그

---

## 🔧 기술 스택

### Core
- Python 3.12
- pandas (데이터 처리)
- numpy (수치 계산)

### UI
- PyQt6 (데스크톱 UI)
- QThread (비동기 처리)

### 향후 계획
- Flask + Eel (웹 UI)
- Electron (크로스 플랫폼 데스크톱)
- PyInstaller (EXE 빌드)

---

## 🏗️ 아키텍처

### Clean Architecture (계층 분리)

```
┌─────────────────────────────────────┐
│         UI Layer                    │
│  - PyQt6 (현재)                     │
│  - Flask (계획)                     │
│  - Electron (계획)                  │
└──────────────┬──────────────────────┘
               │
               │ ConversionService API
               ▼
┌─────────────────────────────────────┐
│    Business Logic (Core)            │
│  - 100% UI 독립                     │
│  - ConversionService                │
│  - Parsers (Base, SnP, Rx)          │
│  - Models, Converters               │
└─────────────────────────────────────┘
```

### Factory Pattern (확장성)

```python
# 새 측정 타입 추가 예시
class TxPowerParser(BaseMeasurementParser):
    def get_measurement_type(self) -> str:
        return 'tx_power'

    def calculate_metrics(self, s_params_df, metadata) -> pd.DataFrame:
        # Tx Power 메트릭 계산 로직
        pass
```

→ Core는 수정 없이 새 Parser 클래스만 추가하면 됨!

---

## 🧪 테스트

### Core 단위 테스트
```bash
cd rf_converter
python tests/test_core_simple.py
```

**예상 결과**:
```
Found 3 SnP files
[1/3] X_ANT1_B1@1_(G0).s2p
[2/3] X_ANT1_B1@1_(G0H).s2p
[3/3] X_ANT1_B1@1_(G1).s2p

Success: True
Files: 3/3
Rows: 183
Size: 21.7 KB
```

### GUI 테스트
[테스트_가이드.md](ui_pyqt6/테스트_가이드.md) 참조

---

## 🐛 문제 해결

### ModuleNotFoundError: No module named 'pandas'
```bash
cd C:\Project\html_exporter
.venv\Scripts\activate
pip install pandas numpy PyQt6
```

### ModuleNotFoundError: No module named 'core'
```bash
cd rf_converter\ui_pyqt6
set PYTHONPATH=..
python main.py
```

### GUI가 실행되지 않음
```bash
# Python 버전 확인
python --version

# 가상환경 활성화 확인
where python
# 출력: C:\Project\html_exporter\.venv\Scripts\python.exe
```

---

## 📈 로드맵

### Phase 1: Core + PyQt6 UI ✅ (완료)
- [x] Core 모듈 구현
- [x] PyQt6 데스크톱 UI
- [x] s1p~s12p 지원
- [x] 한글 매뉴얼
- [x] UX 개선 (레이아웃 안정성)

### Phase 2: Flask Web UI (진행 예정)
- [ ] Flask 앱 구조
- [ ] Eel 통신
- [ ] Bootstrap UI
- [ ] 파일 업로드
- [ ] 진행률 표시 (SSE)

### Phase 3: 배포 (계획)
- [ ] PyInstaller EXE 빌드
- [ ] 아이콘 및 리소스 포함
- [ ] 설치 가이드
- [ ] 자동 업데이트 (선택)

### Phase 4: Electron UI (선택)
- [ ] Electron 프로젝트 설정
- [ ] Python 백엔드 연동
- [ ] 현대적인 웹 UI
- [ ] 크로스 플랫폼 빌드

---

## 📝 변경 이력

### 2025-10-26
- ✅ PyQt6 UI 구현 완료
- ✅ s1p~s12p 지원 확장
- ✅ UX 개선 (항상 표시되는 결과 섹션, 레이아웃 안정성)
- ✅ 한글 문서 작성 (매뉴얼, 테스트 가이드, 세션 로그)
- ✅ 테스트 완료 (Core 단위 테스트, GUI 실행 확인)

---

## 👥 기여

**개발**: Claude (Anthropic) + Human Collaboration
**사용자 피드백**: RF 측정 엔지니어
**아키텍처 설계**: Clean Architecture + Factory Pattern

---

## 📄 라이선스

MIT License (예정)

---

## 📞 지원

**문서**: [docs/](docs/)
**이슈**: 스크린샷 + 에러 메시지 전체 복사
**세션 재개**: [세션-2025-10-26-pyqt6-ui-완성.md](docs/세션-2025-10-26-pyqt6-ui-완성.md) 참조

---

**Last Updated**: 2025-10-26
**Version**: 1.0.0
**Status**: ✅ PyQt6 UI 완성, Flask UI 대기 중
