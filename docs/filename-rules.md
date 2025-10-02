# 파일명 규칙 정의

**작성일**: 2025-10-02

---

## 📋 측정 프로그램 파일명 규칙

### **기본 패턴 (예상)**

```
{Band}_{CA_Condition}_{Port}.s{N}p

예시:
- B1_RxOut1.s10p              → Band: B1, CA: B1, Port: RxOut1
- B1_B3_RxOut2.s10p           → Band: B1, CA: B1_B3, Port: RxOut2
- B1_B41_RxOut3.s10p          → Band: B1, CA: B1_B41, Port: RxOut3
- B3_B7_RxOut1.s12p           → Band: B3, CA: B3_B7, Port: RxOut1
```

### **패턴 구성 요소**

#### 1. Band (메인 Band)
- **형식**: `B{숫자}`
- **예시**: B1, B3, B7, B20, B28, B38, B41
- **용도**: 탭 구분 (각 Band별로 탭 생성)

#### 2. CA Condition (Carrier Aggregation)
- **형식**: `B{숫자}` 또는 `B{숫자}_B{숫자}` 또는 `B{숫자}_B{숫자}_B{숫자}`
- **예시**:
  - Single: B1, B3, B41
  - 2CA: B1_B3, B1_B41, B3_B7
  - 3CA: B1_B3_B41, B1_B7_B20
- **용도**: 그리드 열(Column) 구분

#### 3. Port (측정 포트)
- **형식**:
  - RX: `RxOut{숫자}` (RxOut1, RxOut2, RxOut3, RxOut4)
  - TX: `TxIn{숫자}_ANT{숫자}` (TxIn1_ANT1, TxIn2_ANT2)
  - 또는: `TxIn{숫자}`, `ANT{숫자}` 별도
- **용도**: 그리드 행(Row) 구분

#### 4. 확장자
- **형식**: `.s{N}p` (N = 포트 개수)
- **예시**: .s2p (2-port), .s10p (10-port), .s12p (12-port)

---

## 🔍 정규식 패턴

### **Pattern 1: 기본 패턴** (우선 구현)

```regex
^(B\d+)_(B\d+(?:_B\d+)*)_(RxOut\d+|TxIn\d+(?:_ANT\d+)?|ANT\d+)\.s\d+p$

분해:
- ^(B\d+)                        → 메인 Band (캡처 그룹 1)
- _(B\d+(?:_B\d+)*)              → CA 조건 (캡처 그룹 2)
- _(RxOut\d+|TxIn\d+|ANT\d+)    → Port (캡처 그룹 3)
- \.s\d+p$                       → 확장자
```

**매칭 예시:**
```
✓ B1_B1_RxOut1.s10p           → Band: B1, CA: B1, Port: RxOut1
✓ B1_B1_B3_RxOut2.s10p        → Band: B1, CA: B1_B3, Port: RxOut2
✓ B3_B3_B7_TxIn1.s12p         → Band: B3, CA: B3_B7, Port: TxIn1
✗ B1_RxOut1.s10p              → CA 누락 (규칙에 따라 허용/불허 결정)
```

### **Pattern 2: 유연한 패턴** (CA 생략 가능)

```regex
^(B\d+)(?:_(B\d+(?:_B\d+)*))?_(RxOut\d+|TxIn\d+|ANT\d+)\.s\d+p$

분해:
- ^(B\d+)                          → 메인 Band (필수)
- (?:_(B\d+(?:_B\d+)*))?          → CA 조건 (선택적)
- _(RxOut\d+|TxIn\d+|ANT\d+)      → Port (필수)
- \.s\d+p$                         → 확장자
```

**매칭 예시:**
```
✓ B1_RxOut1.s10p              → Band: B1, CA: B1 (자동), Port: RxOut1
✓ B1_B3_RxOut2.s10p           → Band: B1, CA: B1_B3, Port: RxOut2
✓ B41_B41_RxOut4.s10p         → Band: B41, CA: B41, Port: RxOut4
```

---

## 📊 자동 감지 로직

### **Step 1: 파일명 파싱**

```python
def parse_filename(filename: str) -> dict:
    """
    파일명에서 Band, CA, Port 추출

    Returns:
        {
            'main_band': str,      # 'B1'
            'ca_condition': str,   # 'B1_B3'
            'port': str,           # 'RxOut1'
            'extension': str       # 's10p'
        }
    """
```

### **Step 2: 파일 그룹화**

```python
def organize_files(files: list) -> dict:
    """
    파일들을 Band별 → CA별 → Port별로 그룹화

    Returns:
        {
            'B1': {
                'B1': {'RxOut1': file1, 'RxOut2': file2},
                'B1_B3': {'RxOut1': file3, 'RxOut2': file4}
            },
            'B3': {...}
        }
    """
```

### **Step 3: 그리드 구조 추출**

```python
def extract_grid_structure(organized: dict) -> dict:
    """
    그리드 행/열 정보 추출

    Returns:
        {
            'bands': ['B1', 'B3', 'B41'],
            'grids': {
                'B1': {
                    'ca_conditions': ['B1', 'B1_B3', 'B1_B41'],
                    'ports': ['RxOut1', 'RxOut2', 'RxOut3', 'RxOut4'],
                    'matrix': [[file, file, file], [file, file, None], ...]
                }
            },
            'warnings': [
                'B1_B1_B41 × RxOut3 파일 누락',
                'B3 탭에 파일 없음'
            ]
        }
    """
```

---

## 🎯 그리드 배치 규칙

### **탭 구성**
- **1개 탭 = 1개 메인 Band**
- 예: B1 탭, B3 탭, B41 탭

### **그리드 구성 (탭 내부)**
- **열(Column)**: CA 조건 (B1, B1_B3, B1_B41, ...)
- **행(Row)**: Port (RxOut1, RxOut2, RxOut3, RxOut4, ...)
- **셀(Cell)**: 각 SnP 파일

### **예시: B1 탭**

```
         B1        B1_B3      B1_B41     B1_B7
RxOut1  [file1]   [file2]    [file3]    [file4]
RxOut2  [file5]   [file6]    [file7]    [file8]
RxOut3  [file9]   [file10]   [file11]   [MISSING]
RxOut4  [file12]  [file13]   [file14]   [file15]
```

---

## ⚠️ 예외 처리

### **파일명 파싱 실패**
```python
# 알 수 없는 형식
unknown_files = [
    'test.s10p',           # Band/Port 정보 없음
    'measurement_1.snp',   # 비표준 확장자
    'B1_invalid.s10p'      # Port 정보 없음
]

# 처리 방법:
# 1. 사용자에게 경고 표시
# 2. '기타' 탭으로 분류
# 3. 수동 설정 유도
```

### **파일 누락**
```python
# 그리드에 빈 셀 발생
warnings = [
    'B1_B7 × RxOut3 파일이 없습니다',
    'B3 탭에 파일이 하나도 없습니다'
]

# 처리 방법:
# 1. 미리보기에 ⚠️ 표시
# 2. 해당 셀은 빈 그래프 또는 "데이터 없음" 표시
# 3. 사용자가 추가 업로드 가능하도록
```

### **중복 파일**
```python
# 같은 조건에 여러 파일
duplicates = [
    ('B1_B1_RxOut1.s10p', 'B1_B1_RxOut1_v2.s10p')
]

# 처리 방법:
# 1. 최신 파일 우선 (타임스탬프)
# 2. 사용자에게 선택 요청
# 3. 버전 번호가 있으면 최신 버전
```

---

## 🔄 실제 파일명 규칙 (확인 필요)

**TODO**: 실제 측정 프로그램의 파일명 예시를 확인하고 업데이트

**질문 사항**:
1. 실제 파일명 예시 3-5개를 제공해주세요
2. Band와 CA 조건이 항상 명시되나요?
3. 날짜/시간/버전 정보가 포함되나요?
4. TX 측정 시 파일명 형식은?
5. 특수한 측정 조건이 파일명에 포함되나요? (온도, 전압 등)

---

## 📝 업데이트 이력

- 2025-10-02: 초안 작성 (예상 패턴 기반)
- TODO: 실제 파일명 확인 후 업데이트
