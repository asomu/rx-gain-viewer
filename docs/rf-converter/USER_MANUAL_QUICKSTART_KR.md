# RF Converter 빠른 시작 가이드

> 핵심만 빠르게! 5분 안에 첫 변환 완료하기

---

## 목차

1. [프로그램 실행](#1-프로그램-실행)
2. [5단계 변환](#2-5단계-변환)
3. [주요 버튼 기능](#3-주요-버튼-기능)
4. [지원 Band](#4-지원-band)
5. [흔한 문제 해결](#5-흔한-문제-해결)
6. [CSV 출력 형식](#6-csv-출력-형식)

---

## 1. 프로그램 실행

### 사용자용: EXE 파일 실행

```
RFConverter.exe 더블클릭
```

> ✅ **Python 설치 불필요!**
> EXE 파일만 있으면 바로 실행됩니다.

### 개발자용: 소스 코드 실행

<details>
<summary>개발 환경에서 실행 (클릭하여 펼치기)</summary>

**방법 1: 배치 파일**
```bash
run_gui.bat
```

**방법 2: Python 직접**
```bash
.venv\Scripts\python.exe rf_converter\ui_pyqt6\main.py
```

**방법 3: UV**
```bash
uv run rf_converter/ui_pyqt6/main.py
```

</details>

---

## 2. 5단계 변환

### 단계 1: 프로그램 실행
- `RFConverter.exe` 더블클릭

### 단계 2: 파일 선택
- **드래그 앤 드롭**: SnP 파일들을 화면에 드래그
- **버튼 클릭**: "Browse files..." 버튼으로 파일 선택

### 단계 3: 출력 경로 확인
- 기본값: `바탕화면\RF_Output.csv`
- 변경: "Browse..." 버튼 클릭

### 단계 4: 변환 시작
- "START CONVERSION" 버튼 클릭
- 진행률 확인

### 단계 5: 결과 확인
- "Open CSV": CSV 파일 열기
- "Open Folder": 저장 폴더 열기

### 첫 변환 체크리스트
```
☑ 프로그램 실행됨
☑ SnP 파일 선택됨 (파일 수 표시 확인)
☑ 출력 경로 확인
☑ Frequency filtering ON (권장)
☑ Auto-detect band ON (권장)
☑ START CONVERSION 클릭
☑ 100% 완료 확인
☑ CSV 파일 생성 확인
```

---

## 3. 주요 버튼 기능

### 파일 선택
| 버튼/영역 | 기능 | 단축 |
|----------|------|------|
| File Selection 영역 | 드래그 앤 드롭 가능 | Ctrl+A (탐색기) |
| Browse files... | 파일 선택 대화상자 | - |

### 변환 옵션
| 옵션 | 설명 | 권장 |
|------|------|------|
| Frequency filtering | Band 범위만 추출 | ✅ ON |
| Auto-detect band | 파일명에서 Band 자동 인식 | ✅ ON |
| Full frequency sweep | Band 외 주파수 포함 | ❌ OFF |

### 액션 버튼
| 버튼 | 기능 | 사용 시점 |
|------|------|----------|
| START CONVERSION | 변환 시작 | 파일 선택 후 |
| Open CSV | CSV 파일 열기 | 변환 완료 후 |
| Open Folder | 폴더 열기 | 변환 완료 후 |
| Convert More | 새로운 변환 | 추가 변환 필요 시 |

---

## 4. 지원 Band

### GSM (4개)
| Band | Uplink (MHz) | Downlink (MHz) |
|------|--------------|----------------|
| GSM850 | 824-849 | 869-894 |
| GSM900 | 890-915 | 935-960 |
| DCS | 1710-1785 | 1805-1880 |
| PCS | 1850-1910 | 1930-1990 |

### LTE FDD 주요 Band (16개)
| Band | Uplink (MHz) | Downlink (MHz) | 주 사용 지역 |
|------|--------------|----------------|--------------|
| B1 | 1920-1980 | 2110-2170 | Global |
| B2 | 1850-1910 | 1930-1990 | Americas |
| B3 | 1710-1785 | 1805-1880 | Europe/Asia |
| B4 | 1710-1755 | 2110-2155 | Americas |
| B5 | 824-849 | 869-894 | Americas |
| B7 | 2500-2570 | 2620-2690 | Europe/Asia |
| B8 | 880-915 | 925-960 | Global |
| B12 | 699-716 | 729-746 | Americas |
| B13 | 777-787 | 746-756 | Americas |
| B17 | 704-716 | 734-746 | Americas |
| B20 | 832-862 | 791-821 | Europe |
| B25 | 1850-1915 | 1930-1995 | Americas |
| B26 | 814-849 | 859-894 | Americas |
| B28 | 703-748 | 758-803 | Asia-Pacific |
| B66 | 1710-1780 | 2110-2200 | Americas |
| B71 | 663-698 | 617-652 | Americas |

### LTE TDD (8개)
| Band | 주파수 (MHz) | 주 사용 지역 |
|------|--------------|--------------|
| B34 | 2010-2025 | Global |
| B38 | 2570-2620 | Europe/Asia |
| B39 | 1880-1920 | Asia |
| B40 | 2300-2400 | Asia |
| B41 | 2496-2690 | Global |
| B42 | 3400-3600 | Global |
| B43 | 3600-3800 | Global |
| B48 | 3550-3700 | Americas |

### 5G NR 주요 Band (7개)
| Band | Uplink/Downlink (MHz) | 주 사용 지역 |
|------|----------------------|--------------|
| N1 | 1920-1980 / 2110-2170 | Global |
| N3 | 1710-1785 / 1805-1880 | Europe/Asia |
| N7 | 2500-2570 / 2620-2690 | Europe/Asia |
| N28 | 703-748 / 758-803 | Asia-Pacific |
| N41 | 2496-2690 (TDD) | Global |
| N77 | 3300-4200 (TDD) | Global |
| N78 | 3300-3800 (TDD) | Global |

**전체 지원**: 48개 Band (GSM 4 + LTE 30 + 5G NR 14)

---

## 5. 흔한 문제 해결

### 문제 1: 프로그램 실행 안됨

**증상**: EXE 파일 더블클릭해도 창이 안 열림

**해결**:
1. **관리자 권한으로 실행**: RFConverter.exe 우클릭 → "관리자 권한으로 실행"
2. **Windows Defender 확인**: 바이러스 검사에서 차단되었는지 확인
3. **경로 확인**: 한글이나 특수문자가 없는 경로에 EXE 파일 위치
4. **재다운로드**: 파일 손상 가능성 - 다시 다운로드

> **개발자용**: 소스 코드로 실행하려면 위의 "개발자용 실행" 섹션 참고

### 문제 2: 파일 선택 안됨

**증상**: 드래그해도 선택 안됨

**해결**:
- 파일 확장자 확인: `.s2p`, `.s1p`, `.s3p`, `.s4p` (대소문자 무관)
- 파일 경로 확인: 특수문자 없는 경로
- 파일 권한 확인: 읽기 권한 있는지

### 문제 3: 변환 실패

**증상**: "Conversion Failed" 오류

**해결**:
1. 로그 확인: `%USERPROFILE%\.rf_converter\logs\rf_converter.log`
2. 파일명 형식 확인: `[접두사]_ANT[1-4]_B[숫자]@[숫자]_(G[0-2][HL]).s2p`
3. 파일 10개씩 나눠서 변환 시도

### 문제 4: CSV 파일 열기 실패

**증상**: "Permission denied" 오류

**해결**:
- Excel 등에서 기존 파일 닫기
- 다른 폴더 선택 (바탕화면, 내문서)
- 디스크 공간 확인 (최소 100MB 필요)

### 문제 5: 결과가 이상함

**증상**: Row 수가 너무 적음

**해결**:
- "Frequency filtering" OFF로 전체 데이터 확인
- "Auto-detect band" ON 확인
- 파일명과 실제 측정 Band 일치 확인

### 오류 메시지 빠른 참조

| 오류 | 해결 방법 |
|------|-----------|
| "No files selected" | 파일 선택 후 재시도 |
| "Band B99 not found" | 파일명 확인 (지원 Band인지) |
| "Permission denied" | 관리자 권한 실행 또는 경로 변경 |
| "Memory allocation failed" | 파일 수 줄이기 (200개씩) |
| "Invalid S2P format" | 파일 재생성 또는 제외 |
| "Output file is locked" | Excel 닫고 재시도 |

---

## 6. CSV 출력 형식

### 컬럼 구조 (14개)

| 순서 | 컬럼명 | 예시 값 |
|------|--------|---------|
| 1 | Freq Type | IB (In-Band) |
| 2 | RAT | LTE |
| 3 | Cfg Band | B1 |
| 4 | Debug Band | B1 |
| 5 | Frequency | 2140.5 |
| 6 | Active RF Path | S0706 |
| 7 | Gain (dB) | 18.5 |
| 8 | Reverse (dB) | -45.2 |
| 9 | Input RL (dB) | 15.3 |
| 10 | Output RL (dB) | 12.8 |
| 11 | cfg_lna_gain_state | G0_H |
| 12 | cfg_active_port_1 | ANT1 |
| 13 | cfg_active_port_2 | RXOUT1 |
| 14 | ca_config | B1[B7] |

### 데이터 예시

```csv
Freq Type,RAT,Cfg Band,Debug Band,Frequency,Active RF Path,Gain (dB),Reverse (dB),Input RL (dB),Output RL (dB),cfg_lna_gain_state,cfg_active_port_1,cfg_active_port_2,ca_config
IB,LTE,B1,B1,2110.0,S0706,18.2,-45.5,15.8,12.3,G0_H,ANT1,RXOUT1,B1
IB,LTE,B1,B1,2111.0,S0706,18.3,-45.4,15.9,12.4,G0_H,ANT1,RXOUT1,B1
IB,LTE,B3,B3,1805.0,S0706,17.5,-46.2,14.2,11.8,G0_H,ANT1,RXOUT1,B3
```

### S-parameter 표기

| 입력 | 출력 | 표기 |
|------|------|------|
| ANT1 | RXOUT1 | S0706 |
| ANT1 | RXOUT2 | S0707 |
| ANT2 | RXOUT1 | S0806 |
| ANT2 | RXOUT2 | S0807 |

### CSV 크기 추정

```
파일 수 × 주파수 포인트 × 0.16 KB ≈ CSV 크기

예시:
- 50 파일 × 50 포인트 = 400 KB
- 100 파일 × 50 포인트 = 800 KB
- 500 파일 × 50 포인트 = 4 MB
```

---

## 파일명 규칙

### 표준 형식
```
X_ANT1_B1@1_(G0H).s2p
│  │    │ │  │
│  │    │ │  └─ LNA 상태 (G0H, G1L, G2H 등)
│  │    │ └──── 출력 포트 (@1=RXOUT1, @2=RXOUT2)
│  │    └────── Band 정보 (B1, B3[B7], B41[NA] 등)
│  └─────────── 입력 포트 (ANT1~ANT4)
└────────────── 접두사 (무시됨)
```

### Band 표기 예시
- 단일 Band: `B1`, `B3`, `B7`, `B41`
- 지역 코드: `B41[NA]`, `B41[EU]`, `B41[CN]`
- CA 설정: `B1[B7]`, `B3[B7]`, `B7[B28]`

---

## 로그 확인

### 로그 위치
```
C:\Users\사용자명\.rf_converter\logs\
├── rf_converter.log           # Python 로그
└── conversion_history.json    # 변환 이력
```

### 로그 열기
```bash
# 최신 로그 보기
type %USERPROFILE%\.rf_converter\logs\rf_converter.log

# 폴더 열기
explorer %USERPROFILE%\.rf_converter\logs
```

---

## 추가 도움말

### 상세 매뉴얼
- **완전 가이드**: [USER_MANUAL_KR.md](USER_MANUAL_KR.md)
- **Band Mapping**: [BAND_MAPPING_QUICKSTART_KR.md](BAND_MAPPING_QUICKSTART_KR.md)
- **개발 로그**: [development-log.md](development-log.md)

### 프로젝트 정보
- 위치: `C:\Python\Project\rx-gain-viewer`
- 버전: v1.1
- 지원 Band: 48개
- 측정 타입: Rx Gain (Tx Power, Isolation 준비 중)

---

**문서 버전**: v1.0 (Quick Start)
**최종 업데이트**: 2025-12-03
**작성자**: RF Analyzer Team

---

## 핵심 정리

1. **실행**: `run_gui.bat` 더블클릭
2. **파일**: SnP 파일 드래그 앤 드롭
3. **설정**: Frequency filtering ON, Auto-detect band ON
4. **변환**: START CONVERSION 클릭
5. **확인**: Open CSV 클릭

**5분이면 충분합니다!**
