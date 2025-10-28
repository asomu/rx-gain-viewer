# RF Converter

**RF S-parameter 측정 파일(SnP)을 CSV로 변환하는 전문 도구**

PA(Power Amplifier) 모듈 테스트 데이터를 분석하고 리포팅하기 위한 PyQt6 기반 데스크톱 애플리케이션

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-Internal-red.svg)]()

---

## 🎯 주요 특징

- ✅ **다중 파일 형식 지원**: S1P, S2P, S3P, S4P
- ✅ **48개 3GPP Band 지원**: LTE FDD/TDD, GSM, 5G NR
- ✅ **Rx/Tx 주파수 분리**: FDD 밴드 상향/하향링크 독립 필터링
- ✅ **자동 Band 인식**: 파일명에서 Band 정보 자동 추출
- ✅ **지역 코드 지원**: B41[NA], B41[EU], B41[CN], B41[SA]
- ✅ **CA 패턴 인식**: B1[B7], B3[B7] 등 35개 CA 조합
- ✅ **배치 변환**: 여러 파일 동시 처리
- ✅ **실시간 진행률**: 파일별 처리 상태 표시
- ✅ **설정 자동 저장**: 마지막 설정 자동 복원
- ✅ **변환 로그**: 히스토리 자동 저장

---

## 🚀 빠른 시작

### 설치 및 실행

**방법 1: 배치 파일 실행 (가장 간단)**
```bash
# 프로젝트 폴더에서 run_gui.bat 더블클릭
C:\Python\Project\rx-gain-viewer\rf_converter\run_gui.bat
```

**방법 2: Python 직접 실행**
```bash
cd C:\Python\Project\rx-gain-viewer
.venv\Scripts\python.exe rf_converter\ui_pyqt6\main.py
```

**방법 3: UV 실행**
```bash
cd C:\Python\Project\rx-gain-viewer
uv run rf_converter/ui_pyqt6/main.py
```

### 5단계 변환 과정

1. **프로그램 실행** - run_gui.bat 더블클릭
2. **파일 선택** - SnP 파일 드래그 & 드롭 또는 찾아보기
3. **출력 경로 확인** - 기본값 또는 원하는 위치 지정
4. **START CONVERSION** - 변환 시작
5. **결과 확인** - CSV 파일 열기 또는 폴더 열기

---

## 📁 프로젝트 구조

```
rx-gain-viewer/
├── rf_converter/                   ⭐ 주력 프로젝트
│   ├── core/                       # 핵심 로직
│   │   ├── parsers/                # SnP 파서
│   │   │   ├── base_parser.py      # 48개 밴드 설정
│   │   │   ├── rx_gain_parser.py   # Rx Gain 측정
│   │   │   ├── rx_sens_parser.py   # Rx Sensitivity
│   │   │   └── tx_parser.py        # Tx Power (예정)
│   │   └── logger.py               # 로깅 시스템
│   ├── ui_pyqt6/                   # PyQt6 UI
│   │   ├── main.py                 # 진입점
│   │   └── main_window.py          # 메인 윈도우
│   ├── tests/                      # 테스트
│   ├── icon.ico                    # 애플리케이션 아이콘
│   └── run_gui.bat                 # 빠른 실행 스크립트
│
├── django_test/                    # Django 웹 앱 (유지보수 모드)
│   ├── rf_analyzer/
│   └── manage.py
│
├── docs/                           # 문서
│   ├── rf-converter/               # RF Converter 문서
│   │   ├── USER_MANUAL_KR.md       # 📖 사용자 매뉴얼
│   │   ├── development-log.md      # 개발 로그
│   │   ├── workflow-diagrams.md    # 워크플로우 다이어그램
│   │   └── sessions/               # 세션 로그
│   └── django/                     # Django 문서
│
├── archive/                        # 사용하지 않는 코드
│   └── prototype/                  # 초기 프로토타입 (검증 완료)
│
├── pyproject.toml                  # 프로젝트 설정
└── README.md
```

---

## 📚 문서

- **[사용자 매뉴얼](docs/rf-converter/USER_MANUAL_KR.md)** - 초보자를 위한 완전한 가이드
- **[개발 로그](docs/rf-converter/development-log.md)** - 전체 개발 히스토리
- **[워크플로우 다이어그램](docs/rf-converter/workflow-diagrams.md)** - Mermaid 다이어그램

---

## 🔧 기술 스택

- **Python**: 3.11+
- **UI Framework**: PyQt6 6.5+
- **Data Processing**: Pandas, NumPy
- **RF Library**: scikit-rf
- **Logging**: Python logging + JSON
- **Settings**: QSettings (Windows Registry)

---

## 📊 지원 Band 목록

### LTE FDD (26개)
B1, B2, B3, B4, B5, B7, B8, B11, B12, B13, B14, B17, B18, B19, B20, B21, B25, B26, B28, B29, B30, B66, B71

### LTE TDD (10개)
B33, B34, B35, B36, B37, B38, B39, B40, B41, B42, B43, B48

### GSM (4개)
GSM850, GSM900, DCS, PCS

### 5G NR (14개)
N1, N2, N3, N5, N7, N8, N12, N20, N25, N28, N38, N41, N66, N71, N77, N78, N79

**총 48개 밴드 완전 지원**

---

## 🧪 테스트 검증

- ✅ **48개 밴드**: 100% 3GPP TS 36.101 준수
- ✅ **980개 실제 파일**: 100% 파싱 성공률
- ✅ **35개 CA 패턴**: B1[B7], B41[NA] 등 완전 지원

---

## 🔄 버전 히스토리

### v1.0 (2025-10-28) - Production Release
- ✅ 48개 3GPP 밴드 완전 지원
- ✅ Rx/Tx 주파수 분리
- ✅ 로깅 시스템 구현
- ✅ 설정 자동 저장/복원
- ✅ 커스텀 RF 아이콘
- ✅ UI 최적화 (850x1020)
- ✅ 지역 코드 파싱 (NA/EU/CN/SA)

### 향후 계획
- 🚧 Tx Power 측정 지원
- 🚧 데이터 시각화 통합
- 🚧 S-parameter 품질 분석

---

## 🤝 기여 및 지원

### 문제 보고
프로젝트 이슈 트래커를 통해 버그 리포트 또는 기능 제안을 해주세요.

### 로그 위치
- **변환 로그**: `~/.rf_converter/logs/rf_converter.log`
- **변환 히스토리**: `~/.rf_converter/logs/conversion_history.json`

---

## 🔒 라이선스

**Internal Use Only** (회사 내부용)

---

## 👥 개발팀

**RF Engineering Team**

---

## 📌 관련 프로젝트

- **[Django Web App](django_test/README.md)** - 웹 기반 S-parameter 뷰어 (유지보수 모드)
- **[Prototype](archive/prototype/)** - 초기 프로토타입 (참고용)

---

**Last Updated**: 2025-10-28
**Status**: ✅ Production Ready - v1.0
